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

const VIEW_TYPE_AGENT_WORKBENCH = "llm-wiki-agent-workbench";

interface AgentWorkbenchSettings {
  llmWikiCommand: string;
  repoRoot: string;
}

const DEFAULT_SETTINGS: AgentWorkbenchSettings = {
  llmWikiCommand: "llm-wiki",
  repoRoot: "",
};

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
      name: "Copy llm-wiki status command",
      callback: () => {
        void this.copyCommand(["status", "--json"]);
      },
    });

    this.addCommand({
      id: "copy-active-search-json-command",
      name: "Copy llm-wiki search command for active page",
      callback: () => {
        const topic = this.getActiveTopic();
        void this.copyCommand(["search", topic, "--json"]);
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

  buildCommand(args: string[]): string {
    const command = [this.settings.llmWikiCommand, "--repo-root", this.getRepoRoot(), ...args];
    return command.map(shellQuote).join(" ");
  }

  async copyCommand(args: string[]) {
    const command = this.buildCommand(args);
    await navigator.clipboard.writeText(command);
    new Notice("Copied llm-wiki command.");
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
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass("agent-workbench");

    const file = this.app.workspace.getActiveFile();
    container.createEl("h2", { text: "Agent Workbench" });

    this.renderActivePage(container, file);
    this.renderRelatedContext(container, file);
    this.renderRepoHealth(container);
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
      list.createEl("li", { text: link.link });
    }
    if (links.length > 12) {
      section.createEl("p", {
        text: `${links.length - 12} more links omitted.`,
        cls: "agent-workbench-muted",
      });
    }
  }

  private renderRepoHealth(container: Element) {
    const section = createSection(container, "Repo Health");
    createCommandButton(section, "Copy status JSON", () => {
      void this.plugin.copyCommand(["status", "--json"]);
    });
    createCommandButton(section, "Copy graph JSON", () => {
      void this.plugin.copyCommand(["graph", "--json"]);
    });
    createKV(section, "Repo Root", this.plugin.getRepoRoot());
  }

  private renderAgentHandoff(container: Element, file: TFile | null) {
    const section = createSection(container, "Agent Handoff");
    const topic = file ? this.plugin.getActiveTopic() : "overview";

    createCommandButton(section, "Copy search JSON", () => {
      void this.plugin.copyCommand(["search", topic, "--json"]);
    });
    createCommandButton(section, "Copy query JSON", () => {
      void this.plugin.copyCommand(["query", topic, "--json"]);
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
      .setDesc("Command used when preparing shell handoff commands.")
      .addText((text) =>
        text
          .setPlaceholder("llm-wiki")
          .setValue(this.plugin.settings.llmWikiCommand)
          .onChange(async (value) => {
            this.plugin.settings.llmWikiCommand = value.trim() || DEFAULT_SETTINGS.llmWikiCommand;
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
