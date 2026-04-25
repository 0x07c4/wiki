# Codex Integration Checklist

Use this checklist when connecting this wiki to the user's Codex environment or verifying that the connection still works.

## Scope

The default integration is a Codex skill, not a daemon:

- skill path: `$HOME/.codex/skills/llm-wiki`
- wiki repo: `$HOME/workspace/wiki`
- wrapper: `$HOME/.codex/skills/llm-wiki/scripts/llm-wiki`

Do not edit global `$HOME/.codex/AGENTS.md` unless the user explicitly asks. Prefer a concise `ACTIVE.md` rule and the skill's trigger metadata.

## Verify Skill Files

```bash
find "$HOME/.codex/skills/llm-wiki" -maxdepth 3 -type f | sort
```

Expected files:

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/llm-wiki`

## Validate Skill Structure

```bash
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" \
  "$HOME/.codex/skills/llm-wiki"
```

Expected result:

```text
Skill is valid!
```

## Verify CLI Wrapper

```bash
"$HOME/.codex/skills/llm-wiki/scripts/llm-wiki" status --json
"$HOME/.codex/skills/llm-wiki/scripts/llm-wiki" query "Obsidian Agent Workbench" --json
```

The wrapper should work even when `llm-wiki` is not installed globally.

## Verify Global Routing

Check `$HOME/.codex/memories/ACTIVE.md` contains a concise rule telling Codex to prefer the wiki skill for local long-term context and traceable knowledge tasks.

Do not put the full workflow in global `AGENTS.md`; keep the workflow in `SKILL.md`.

## Fresh Session Smoke Test

Start a new Codex session and ask a query that should trigger the skill, for example:

```text
用本地 wiki 查一下 Obsidian Agent Workbench 当前实现到哪一步了
```

Expected behavior:

- Codex reads global memory first.
- Codex triggers the `llm-wiki` skill.
- Codex uses `scripts/llm-wiki query ... --json` or `search ... --json`.
- Codex answers with concrete wiki paths or source-backed context.

## Optional Sync

The user's agent config sync script copies non-system skills from `$HOME/.codex/skills`. Run it only when the user wants to publish/sync the current Codex config snapshot:

```bash
"$HOME/.codex/bin/sync-agent-config.sh" --dry-run
"$HOME/.codex/bin/sync-agent-config.sh"
```
