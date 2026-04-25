import {
  App,
  FileSystemAdapter,
  ItemView,
  MarkdownView,
  Notice,
  Plugin,
  PluginSettingTab,
  Setting,
  TFile,
  WorkspaceLeaf,
} from "obsidian";
import { execFile } from "child_process";
import path from "path";
import { promisify } from "util";

const VIEW_TYPE_AGENT_WORKBENCH = "llm-wiki-agent-workbench";
const FALLBACK_LLM_WIKI_COMMAND = "llm-wiki";
const COMMAND_OUTPUT_MAX_BUFFER = 10 * 1024 * 1024;
const execFileAsync = promisify(execFile);

interface AgentWorkbenchSettings {
  llmWikiCommand: string;
  repoRoot: string;
}

const DEFAULT_SETTINGS: AgentWorkbenchSettings = {
  llmWikiCommand: "",
  repoRoot: "",
};

interface LlmWikiInvocation {
  executable: string;
  args: string[];
  commandText: string;
  env: NodeJS.ProcessEnv;
}

interface StatusCounts {
  raw_inbox: number;
  raw_sources: number;
  raw_markdown_total: number;
  wiki_pages: number;
  all_markdown_pages_tracked: number;
}

interface StatusNode {
  path: string;
  title: string;
  page_type: string;
  backlinks: number;
  outbound: number;
  outbound_targets?: string[];
}

interface StatusPayload {
  schema_version: string;
  command: string;
  counts: StatusCounts;
  page_types: Record<string, number>;
  hubs: StatusNode[];
  orphans: StatusNode[];
}

export default class AgentWorkbenchPlugin extends Plugin {
  settings: AgentWorkbenchSettings = DEFAULT_SETTINGS;

  async onload() {
    await this.loadSettings();

    this.registerView(
      VIEW_TYPE_AGENT_WORKBENCH,
      (leaf) => new AgentWorkbenchView(leaf, this),
    );

    this.addRibbonIcon("bot", "Open Agent Workbench", () => {
      void this.activateView();
    });

    this.addCommand({
      id: "open-agent-workbench",
      name: "Open Agent Workbench",
      callback: () => {
        void this.activateView();
      },
    });

    this.addCommand({
      id: "refresh-agent-workbench",
      name: "Refresh Agent Workbench",
      callback: () => {
        this.refreshViews();
      },
    });

    this.addCommand({
      id: "copy-status-json-command",
      name: "Copy llm-wiki status JSON",
      callback: () => {
        void this.copyCommandOutput(["status", "--json"], "status JSON");
      },
    });

    this.addCommand({
      id: "copy-active-search-json-command",
      name: "Copy llm-wiki search JSON for active page",
      callback: () => {
        const topic = this.getActiveTopic();
        void this.copyCommandOutput(["search", topic, "--json"], "search JSON");
      },
    });

    this.registerEvent(
      this.app.workspace.on("active-leaf-change", () => {
        this.refreshViews();
      }),
    );

    this.addSettingTab(new AgentWorkbenchSettingTab(this.app, this));
  }

  onunload() {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE_AGENT_WORKBENCH);
  }

  async activateView() {
    const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE_AGENT_WORKBENCH)[0];
    if (existing) {
      await this.app.workspace.revealLeaf(existing);
      return;
    }

    const leaf = this.app.workspace.getRightLeaf(false);
    if (!leaf) {
      new Notice("No workspace leaf available for Agent Workbench.");
      return;
    }

    await leaf.setViewState({ type: VIEW_TYPE_AGENT_WORKBENCH, active: true });
    await this.app.workspace.revealLeaf(leaf);
  }

  async loadSettings() {
    this.settings = {
      ...DEFAULT_SETTINGS,
      ...(await this.loadData()),
    };
  }

  async saveSettings() {
    await this.saveData(this.settings);
    this.refreshViews();
  }

  getRepoRoot(): string {
    const configured = this.settings.repoRoot.trim();
    if (configured) {
      return configured;
    }

    const adapter = this.app.vault.adapter;
    if (adapter instanceof FileSystemAdapter) {
      return adapter.getBasePath();
    }

    return ".";
  }

  buildInvocation(args: string[]): LlmWikiInvocation {
    const repoRoot = this.getRepoRoot();
    const configured = this.settings.llmWikiCommand.trim();

    if (configured) {
      const configuredArgs = splitCommandLine(configured);
      const [executable, ...prefixArgs] = configuredArgs;
      const invocationArgs = [...prefixArgs, "--repo-root", repoRoot, ...args];
      return {
        executable,
        args: invocationArgs,
        commandText: [...configuredArgs, "--repo-root", repoRoot, ...args].map(shellQuote).join(" "),
        env: { ...process.env },
      };
    }

    const localSrc = path.join(repoRoot, "src");
    const pythonPath = process.env.PYTHONPATH
      ? `${localSrc}${path.delimiter}${process.env.PYTHONPATH}`
      : localSrc;
    const invocationArgs = ["-m", "llm_wiki.cli", "--repo-root", repoRoot, ...args];

    return {
      executable: "python3",
      args: invocationArgs,
      commandText: `PYTHONPATH=${shellQuote(pythonPath)} ${["python3", ...invocationArgs]
        .map(shellQuote)
        .join(" ")}`,
      env: {
        ...process.env,
        PYTHONPATH: pythonPath,
      },
    };
  }

  buildCommand(args: string[]): string {
    return this.buildInvocation(args).commandText;
  }

  async copyCommand(args: string[]) {
    const command = this.buildCommand(args);
    await navigator.clipboard.writeText(command);
    new Notice("Copied llm-wiki command.");
  }

  async runCommand(args: string[]): Promise<string> {
    const invocation = this.buildInvocation(args);
    const { stdout } = await execFileAsync(invocation.executable, invocation.args, {
      cwd: this.getRepoRoot(),
      env: invocation.env,
      maxBuffer: COMMAND_OUTPUT_MAX_BUFFER,
    });
    return String(stdout);
  }

  async readJson<T>(args: string[]): Promise<T> {
    return JSON.parse(await this.runCommand(args)) as T;
  }

  async readStatus(): Promise<StatusPayload> {
    const status = await this.readJson<StatusPayload>(["status", "--json"]);
    if (status.command !== "status" || status.schema_version !== "1") {
      throw new Error("Unsupported llm-wiki status payload.");
    }
    return status;
  }

  async copyCommandOutput(args: string[], label: string) {
    try {
      await navigator.clipboard.writeText(await this.runCommand(args));
      new Notice(`Copied ${label}.`);
    } catch (error) {
      const invocation = this.buildInvocation(args);
      console.error("Agent Workbench failed to run llm-wiki.", error);
      await navigator.clipboard.writeText(invocation.commandText);
      new Notice("Could not run llm-wiki; copied command instead.");
    }
  }

  getActiveTopic(): string {
    const file = this.app.workspace.getActiveFile();
    if (!file) {
      return "overview";
    }

    const cache = this.app.metadataCache.getFileCache(file);
    return cache?.frontmatter?.title ?? file.basename.replace(/-/g, " ");
  }

  refreshViews() {
    for (const leaf of this.app.workspace.getLeavesOfType(VIEW_TYPE_AGENT_WORKBENCH)) {
      const view = leaf.view;
      if (view instanceof AgentWorkbenchView) {
        view.render();
      }
    }
  }
}

class AgentWorkbenchView extends ItemView {
  private renderRunId = 0;

  constructor(
    leaf: WorkspaceLeaf,
    private readonly plugin: AgentWorkbenchPlugin,
  ) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE_AGENT_WORKBENCH;
  }

  getDisplayText(): string {
    return "Agent Workbench";
  }

  getIcon(): string {
    return "bot";
  }

  async onOpen() {
    this.render();
  }

  render() {
    const renderRunId = ++this.renderRunId;
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass("agent-workbench");

    const file = this.app.workspace.getActiveFile();
    container.createEl("h2", { text: "Agent Workbench" });

    this.renderActivePage(container, file);
    this.renderRelatedContext(container, file);
    this.renderRepoHealth(container, renderRunId);
    this.renderAgentHandoff(container, file);
    this.renderReviewQueue(container);
  }

  private renderActivePage(container: Element, file: TFile | null) {
    const section = createSection(container, "Active Page");
    if (!file) {
      section.createEl("p", {
        text: "No active markdown page.",
        cls: "agent-workbench-muted",
      });
      return;
    }

    const cache = this.app.metadataCache.getFileCache(file);
    const frontmatter = cache?.frontmatter ?? {};
    const heading = cache?.headings?.[0]?.heading ?? file.basename;

    createKV(section, "Path", file.path);
    createKV(section, "Title", heading);
    createKV(section, "Page Type", stringify(frontmatter.page_type));
    createKV(section, "Last Updated", stringify(frontmatter.last_updated));
    createKV(section, "Source Count", stringify(frontmatter.source_count));
    createKV(section, "Source Path", stringify(frontmatter.source_path));
  }

  private renderRelatedContext(container: Element, file: TFile | null) {
    const section = createSection(container, "Related Context");
    if (!file) {
      section.createEl("p", {
        text: "Open a wiki page to inspect links.",
        cls: "agent-workbench-muted",
      });
      return;
    }

    const cache = this.app.metadataCache.getFileCache(file);
    const links = cache?.links ?? [];
    if (!links.length) {
      section.createEl("p", {
        text: "No outbound wiki links found by Obsidian metadata.",
        cls: "agent-workbench-muted",
      });
      return;
    }

    const list = section.createEl("ul", { cls: "agent-workbench-list" });
    for (const link of links.slice(0, 12)) {
      const item = list.createEl("li");
      const destination = this.app.metadataCache.getFirstLinkpathDest(link.link, file.path);
      const anchor = item.createEl("a", {
        text: link.link,
        href: "#",
        cls: destination ? "agent-workbench-link" : "agent-workbench-link is-missing",
      });
      anchor.addEventListener("click", (event) => {
        event.preventDefault();
        if (!destination) {
          new Notice("Linked page not found.");
          return;
        }
        void this.app.workspace.openLinkText(link.link, file.path, false);
      });
    }
    if (links.length > 12) {
      section.createEl("p", {
        text: `${links.length - 12} more links omitted.`,
        cls: "agent-workbench-muted",
      });
    }
  }

  private renderRepoHealth(container: Element, renderRunId: number) {
    const section = createSection(container, "Repo Health");
    const statusContainer = section.createEl("div", { cls: "agent-workbench-status" });
    statusContainer.createEl("p", {
      text: "Loading repo status...",
      cls: "agent-workbench-muted",
    });
    void this.renderRepoHealthSnapshot(statusContainer, renderRunId);

    createCommandButton(section, "Copy status JSON", () => {
      void this.plugin.copyCommandOutput(["status", "--json"], "status JSON");
    });
    createCommandButton(section, "Copy graph JSON", () => {
      void this.plugin.copyCommandOutput(["graph", "--json"], "graph JSON");
    });
    createKV(section, "Repo Root", this.plugin.getRepoRoot());
  }

  private async renderRepoHealthSnapshot(container: Element, renderRunId: number) {
    try {
      const status = await this.plugin.readStatus();
      if (renderRunId !== this.renderRunId) {
        return;
      }
      container.empty();
      this.renderStatusSummary(container, status);
    } catch (error) {
      if (renderRunId !== this.renderRunId) {
        return;
      }
      console.error("Agent Workbench failed to render repo health.", error);
      container.empty();
      container.createEl("p", {
        text: "Repo status unavailable. Use Copy status JSON for command handoff.",
        cls: "agent-workbench-muted",
      });
    }
  }

  private renderStatusSummary(container: Element, status: StatusPayload) {
    const statGrid = container.createEl("div", { cls: "agent-workbench-stat-grid" });
    createStat(statGrid, "Raw", status.counts.raw_sources);
    createStat(statGrid, "Wiki", status.counts.wiki_pages);
    createStat(statGrid, "Inbox", status.counts.raw_inbox);
    createStat(statGrid, "Orphans", status.orphans.length);

    const hubs = status.hubs.slice(0, 3);
    if (hubs.length) {
      container.createEl("p", {
        text: "Top hubs",
        cls: "agent-workbench-subheading",
      });
      const list = container.createEl("ol", { cls: "agent-workbench-compact-list" });
      for (const hub of hubs) {
        const item = list.createEl("li");
        this.createVaultPathLink(item, hub.path, hub.title || hub.path);
        item.createSpan({
          text: ` ${hub.backlinks} backlinks`,
          cls: "agent-workbench-inline-muted",
        });
      }
    }

    if (status.orphans.length) {
      container.createEl("p", {
        text: "Orphans",
        cls: "agent-workbench-subheading",
      });
      const list = container.createEl("ul", { cls: "agent-workbench-compact-list" });
      for (const orphan of status.orphans.slice(0, 5)) {
        const item = list.createEl("li");
        this.createVaultPathLink(item, orphan.path, orphan.title || orphan.path);
      }
      if (status.orphans.length > 5) {
        container.createEl("p", {
          text: `${status.orphans.length - 5} more orphans omitted.`,
          cls: "agent-workbench-muted",
        });
      }
    }
  }

  private createVaultPathLink(container: Element, filePath: string, label: string) {
    const destination = this.app.vault.getAbstractFileByPath(filePath);
    if (!(destination instanceof TFile)) {
      container.createSpan({
        text: label,
        cls: "agent-workbench-inline-muted",
      });
      return;
    }

    const anchor = container.createEl("a", {
      text: label,
      href: "#",
      cls: "agent-workbench-link",
    });
    anchor.addEventListener("click", (event) => {
      event.preventDefault();
      void this.app.workspace.openLinkText(filePath, "", false);
    });
  }

  private renderAgentHandoff(container: Element, file: TFile | null) {
    const section = createSection(container, "Agent Handoff");
    const topic = file ? this.plugin.getActiveTopic() : "overview";

    createCommandButton(section, "Copy search JSON", () => {
      void this.plugin.copyCommandOutput(["search", topic, "--json"], "search JSON");
    });
    createCommandButton(section, "Copy query JSON", () => {
      void this.plugin.copyCommandOutput(["query", topic, "--json"], "query JSON");
    });
    createCommandButton(section, "Copy lint command", () => {
      void this.plugin.copyCommand(["lint"]);
    });
  }

  private renderReviewQueue(container: Element) {
    const section = createSection(container, "Review Queue");
    section.createEl("p", {
      text: "Read-only skeleton: use git status and wiki/log.md until review queue data is formalized.",
      cls: "agent-workbench-muted",
    });
  }
}

class AgentWorkbenchSettingTab extends PluginSettingTab {
  constructor(
    app: App,
    private readonly plugin: AgentWorkbenchPlugin,
  ) {
    super(app, plugin);
  }

  display() {
    const { containerEl } = this;
    containerEl.empty();
    containerEl.createEl("h2", { text: "Agent Workbench" });

    new Setting(containerEl)
      .setName("llm-wiki command")
      .setDesc("Optional override. Leave blank to run the local repo CLI with python3 and PYTHONPATH=src.")
      .addText((text) =>
        text
          .setPlaceholder("llm-wiki")
          .setValue(this.plugin.settings.llmWikiCommand)
          .onChange(async (value) => {
            this.plugin.settings.llmWikiCommand = value.trim();
            await this.plugin.saveSettings();
          }),
      );

    new Setting(containerEl)
      .setName("Repository root")
      .setDesc("Optional override. Leave blank to use the vault base path on desktop.")
      .addText((text) =>
        text
          .setPlaceholder("/path/to/wiki")
          .setValue(this.plugin.settings.repoRoot)
          .onChange(async (value) => {
            this.plugin.settings.repoRoot = value.trim();
            await this.plugin.saveSettings();
          }),
      );
  }
}

function createSection(container: Element, title: string): HTMLElement {
  const section = container.createEl("section", { cls: "agent-workbench-section" });
  section.createEl("h3", { text: title });
  return section;
}

function createKV(container: Element, key: string, value: string) {
  const row = container.createEl("div", { cls: "agent-workbench-kv" });
  row.createEl("span", { text: key, cls: "agent-workbench-key" });
  row.createEl("code", { text: value || "-", cls: "agent-workbench-value" });
}

function createStat(container: Element, label: string, value: number) {
  const stat = container.createEl("div", { cls: "agent-workbench-stat" });
  stat.createEl("span", { text: String(value), cls: "agent-workbench-stat-value" });
  stat.createEl("span", { text: label, cls: "agent-workbench-stat-label" });
}

function createCommandButton(container: Element, label: string, onClick: () => void) {
  const button = container.createEl("button", {
    text: label,
    cls: "agent-workbench-button",
  });
  button.addEventListener("click", onClick);
}

function stringify(value: unknown): string {
  if (value === undefined || value === null || value === "") {
    return "-";
  }
  return String(value);
}

function shellQuote(value: string): string {
  if (/^[A-Za-z0-9_./:=@%+-]+$/.test(value)) {
    return value;
  }
  return `'${value.replace(/'/g, "'\\''")}'`;
}

function splitCommandLine(input: string): string[] {
  const parts: string[] = [];
  let current = "";
  let quote: "'" | '"' | null = null;
  let escaping = false;

  for (const char of input) {
    if (escaping) {
      current += char;
      escaping = false;
      continue;
    }

    if (char === "\\") {
      escaping = true;
      continue;
    }

    if (quote) {
      if (char === quote) {
        quote = null;
      } else {
        current += char;
      }
      continue;
    }

    if (char === "'" || char === '"') {
      quote = char;
      continue;
    }

    if (/\s/.test(char)) {
      if (current) {
        parts.push(current);
        current = "";
      }
      continue;
    }

    current += char;
  }

  if (escaping) {
    current += "\\";
  }
  if (current) {
    parts.push(current);
  }

  return parts.length ? parts : [FALLBACK_LLM_WIKI_COMMAND];
}
