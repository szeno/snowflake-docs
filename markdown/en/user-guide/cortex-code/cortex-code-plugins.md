# CoCo CLI plugins

A CoCo CLI **plugin** is a self-contained package that bundles skills, subagents, slash commands, hooks, and MCP servers under a single manifest. Plugins let you ship a curated set of agent extensions as one unit — share them across a team from a Git repository, install them from the official marketplace, or develop them locally inside a project.

This topic covers the plugin manifest, where CoCo looks for plugins, how to install and manage them, and how plugins compose with the other extensibility surfaces.

## What a plugin contributes

A plugin can contribute any combination of the following:

| Component | Description | Reference |
| --- | --- | --- |
| Skills | Markdown skill files that inject domain-specific instructions and knowledge into a session. | [Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills) |
| Subagents | Custom agent definitions for specialized, autonomous tasks. | [Subagents](#extensibility-subagents) |
| Slash commands | Project-style commands invoked from the CoCo CLI prompt. | [CLI reference](/user-guide/cortex-code/cli-reference) |
| Hooks | Lifecycle hooks that run on events such as `PreToolUse` or `UserPromptSubmit`. | [Hooks](#extensibility-hooks) |
| MCP servers | Model Context Protocol servers that expose external tools to the agent. | [Model Context Protocol (MCP)](#extensibility-mcp) |

Expand

Show lessSee more

Inactive plugins do not contribute their components to the running session. If a plugin includes an `activation.md` file, CoCo generates a small stub skill that lets the user discover and re-enable the plugin from a session.

## Plugin layout

A plugin is a directory with a manifest file at a well-known path:

```
my-plugin/
├── .cortex-plugin/                # or .claude-plugin/
│   ├── plugin.json                # manifest (required)
│   └── activation.md              # optional; surfaces a re-enable skill when inactive
├── skills/                        # auto-discovered if present
│   └── my-skill/SKILL.md
├── commands/                      # auto-discovered if present
│   └── my-command.md
├── agents/                        # auto-discovered if present
│   └── my-agent.md
├── hooks/hooks.json               # optional; can also be inline in plugin.json
└── .mcp.json                      # optional; can also be inline in plugin.json
```

CoCo accepts manifests at either `.cortex-plugin/plugin.json` or `.claude-plugin/plugin.json`. If both are present, `.cortex-plugin` wins.

The `commands`, `skills`, `agents`, `hooks`, and `mcpServers` fields in `plugin.json` are optional. If you omit them, CoCo automatically picks up the standard subdirectories (`./commands`, `./skills`, `./agents`) and the standard files (`./hooks/hooks.json`, `./.mcp.json`) when they exist.

## Plugin manifest

The manifest is a JSON file with the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `name` | string | Required. Lowercase kebab-case identifier (for example, `data-engineering`). |
| `description` | string | Short, human-readable summary of what the plugin does. |
| `version` | string | Optional semantic version (for example, `1.2.0`). |
| `author` | object | Optional. `{ "name": "...", "url": "..." }`. |
| `commands` | string or array of strings | One or more directories containing slash command Markdown files. Defaults to `./commands`. |
| `skills` | string or array of strings | One or more directories containing skill `SKILL.md` files. Defaults to `./skills`. |
| `agents` | string or array of strings | One or more directories containing subagent definition files. Defaults to `./agents`. |
| `hooks` | object, string, or array of strings | Inline `HooksConfig` (the same schema used in `settings.json`), a path to a JSON file with that schema, or a list of such paths. |
| `mcpServers` | object, string, or array of strings | Inline map of `MCPServerConfig` entries, a path to a JSON file, or a list of such paths. Defaults to `./.mcp.json` if that file exists. |
| `requiresSandbox` | boolean | When `true`, signals that the plugin expects to run inside the CoCo sandbox. See [Sandbox-aware plugins](#label-plugins-sandbox). |

Expand

Show lessSee more

The `mcpServers` block uses the same schema as user MCP configuration. See [Model Context Protocol (MCP)](#extensibility-mcp) for the full server schema.

Sample manifest:

Copy code

```
{
  "name": "data-engineering",
  "description": "Skills, hooks, and MCP servers for Snowflake data engineering",
  "version": "1.0.0",
  "author": { "name": "Data Platform Team" },
  "skills": ["./skills"],
  "agents": ["./agents"],
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "bash",
        "hooks": [
          { "type": "command", "command": "bash hooks/validate-bash.sh" }
        ]
      }
    ]
  },
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://internal.example.com/mcp"
    }
  }
}
```

## Where CoCo looks for plugins

CoCo discovers plugins from multiple sources at session start. Plugins are deduplicated by `name` — the first source that provides a plugin wins, in this order:

1. **CLI argument.** Directories passed with one or more `--plugin-dir` arguments at launch.
2. **Connection profile.** Plugins declared by your active Snowflake connection profile.
3. **User settings.** Directories listed in the `plugins` array of `~/.snowflake/cortex/settings.json`.
4. **Managed registry.** Plugins installed under `~/.snowflake/cortex/plugins/` and tracked in `~/.snowflake/cortex/plugins/registry.json`. This is where `cortex plugin install` puts plugins.
5. **Project plugins.** `.cortex/plugins/` and `.claude/plugins/` in the current working directory.
6. **Bundled plugins.** Plugins shipped with the CoCo binary, active by default. Some bundled plugins are gated behind feature flags and may not be present on every build.
7. **Bundled external plugins.** Plugins synced from the CoCo skills repository, inactive by default. Enable them with `cortex plugin enable <name>`.

When you install, enable, or disable a plugin from the command line, already-running CoCo sessions do not pick up the change automatically. Run `/plugin reload` in the session to re-aggregate plugin contributions, or restart CoCo.

The `origin` of a discovered plugin is reported in `cortex plugin list` and in `/plugin info <name>`.

## Managing plugins

You can manage plugins from the command line using `cortex plugin`, or interactively from a CoCo session using the `/plugin` slash command.

### Command reference

| Command | Description |
| --- | --- |
| `cortex plugin install <source>` | Install a plugin from the marketplace, a GitHub shorthand (`owner/repo`), or a full Git URL. Use `--inactive` to install but leave disabled. Aliases: `add`. |
| `cortex plugin uninstall <name>` | Remove a managed plugin from the registry. Aliases: `remove`, `delete`, `rm`. |
| `cortex plugin enable <name>` | Enable a managed plugin. Alias: `activate`. |
| `cortex plugin disable <name>` | Disable a managed plugin without uninstalling it. Alias: `deactivate`. |
| `cortex plugin list` | List every discovered plugin with its origin, components, and active state. |
| `cortex plugin validate [target]` | Validate a plugin’s manifest and components. `target` can be a plugin name or a directory; defaults to the current working directory. |
| `cortex plugin update [name]` | Pull the latest version of a managed plugin from its registered source. Omit `name` to update all managed plugins. |

Expand

Show lessSee more

### Interactive management

Run `/plugin` (alias `/plugins`) inside a CoCo CLI session to manage plugins without leaving the session. The available subcommands are:

| Subcommand | Description |
| --- | --- |
| `/plugin list` | List every discovered plugin. |
| `/plugin info <name>` | Show detailed metadata for a single plugin. |
| `/plugin install [--inactive] <source>` | Install a plugin from the marketplace or a Git source. |
| `/plugin uninstall <name>` | Remove a managed plugin. |
| `/plugin enable <name>` | Activate a plugin. |
| `/plugin disable <name>` | Deactivate a plugin. |
| `/plugin update [name]` | Update one plugin or all managed plugins. |
| `/plugin validate` | Validate the current plugin directory. |
| `/plugin reload` | Reload the plugin runtime from disk. |

Expand

Show lessSee more

## Install sources

`cortex plugin install` accepts three kinds of sources:

| Source form | Example | Behavior |
| --- | --- | --- |
| Marketplace name | `cortex plugin install python-repl` | Resolves the name through the official CoCo plugin marketplace. |
| GitHub shorthand | `cortex plugin install owner/repo` or `cortex plugin install github:owner/repo@branch` | Resolves to a public GitHub repository. |
| Git URL | `cortex plugin install https://github.com/owner/repo.git` | Clones the repository directly. Also supports `git@`, `ssh://`, and `file://` URLs. |

Expand

Show lessSee more

CoCo clones the source into the managed plugins directory, validates the manifest, and registers it in:

```
~/.snowflake/cortex/plugins/registry.json
```

Each registry entry records the plugin’s source, install timestamp, last update timestamp, and whether the plugin is currently active. `cortex plugin update` re-fetches from the registered source.

## How plugins compose with the runtime

When a session starts (or when you run `/plugin reload`), CoCo aggregates the contributions of every active plugin into the live runtime:

- **Skills** from each plugin are added to the skill registry alongside user, project, and bundled skills. Plugin skills are tagged with their origin so you can see them in `/skill list`.
- **Subagents** are added to the subagent search path.
- **Slash commands** are registered with the command loader.
- **Hooks** are merged into the global hook list with a fixed source priority — global, then user, then project, then local project, then plugin, then connection profile (highest). When two hooks conflict, the higher-priority source wins.
- **MCP servers** are added to the MCP connection manager. Plugin servers have lower priority than user and profile servers and are skipped entirely when the administrator disables user MCP servers.

If any active plugin sets `requiresSandbox: true`, CoCo starts the sandbox runtime for the session when the sandbox feature is available. See [Sandbox-aware plugins](#label-plugins-sandbox).

## Sandbox-aware plugins

A plugin that runs untrusted code or interacts with external services can declare `"requiresSandbox": true` in its manifest. CoCo reads this flag during integration and starts the sandbox runtime for the session if the sandbox feature is enabled.

The flag is informational on platforms or builds that do not support the sandbox — it does not block the plugin from loading. See [sandbox](/user-guide/cortex-code/sandbox) for details on the sandbox runtime.

## Managed plugin registry

Plugins installed with `cortex plugin install` are written to:

```
~/.snowflake/cortex/plugins/
```

The registry file `registry.json` in that directory tracks each managed plugin:

Copy code

```
{
  "data-engineering": {
    "source": "github:my-org/cortex-code-data-eng#main",
    "installedAt": "2026-04-24T10:15:00Z",
    "updatedAt": "2026-04-24T10:15:00Z",
    "active": true,
    "lastUpdateError": null
  }
}
```

The registry is locked during writes to prevent concurrent modifications. `lastUpdateError` records the most recent failure from `cortex plugin update`.

## Authoring a plugin

To build a plugin locally:

1. Create a directory for your plugin and initialize the manifest:

   Copy code

   ```
   mkdir -p my-plugin/.cortex-plugin
   ```
2. Create `my-plugin/.cortex-plugin/plugin.json` with at minimum a `name` and `description`:

   Copy code

   ```
   {
     "name": "my-plugin",
     "description": "What this plugin does",
     "version": "0.1.0"
   }
   ```
3. Add components alongside the manifest. The standard layout is automatically discovered:

   ```
   my-plugin/
   ├── .cortex-plugin/plugin.json
   ├── skills/my-skill/SKILL.md
   ├── agents/my-agent.md
   ├── commands/my-command.md
   ├── hooks/hooks.json
   └── .mcp.json
   ```
4. Validate the plugin:

   Copy code

   ```
   cortex plugin validate ./my-plugin
   ```

   The validator reports issues by component (manifest, activation, skills, commands, agents, hooks, MCP servers).
5. Use the plugin locally without installing it by passing `--plugin-dir` at launch:

   Copy code

   ```
   cortex --plugin-dir ./my-plugin
   ```

   Or drop the directory into `.cortex/plugins/` in your project to load it automatically.
6. When you’re ready to share, push the plugin to a Git repository. Other developers can install it with:

   Copy code

   ```
   cortex plugin install your-org/your-plugin-repo
   ```

## Name conflicts and component overrides

When two plugins contribute components with the same name, the first source in the discovery order wins (see [Where CoCo looks for plugins](#label-plugins-sources)). For example, a project plugin in `.cortex/plugins/` overrides a managed plugin of the same name installed via `cortex plugin install`. Use `cortex plugin list` to see which plugin wins.

For skills specifically, see [Skill conflicts](/user-guide/cortex-code/extensibility#label-extensibility-skills) — when the same skill name comes from multiple roots, CoCo shows a conflict indicator in `/skill list`.

## Administrator controls

Administrators can ship plugins as part of a Snowflake connection profile so that every user of that profile gets a consistent baseline of skills, agents, hooks, and MCP servers. Profile-shipped plugins appear with origin `profile` in `cortex plugin list`.

User MCP enforcement also affects plugin-declared MCP servers: when `areUserMcpServersAllowed` is `false` in managed settings, plugin MCP servers are skipped along with user MCP servers. See [managed settings](/user-guide/cortex-code/managed-settings) for the full enforcement schema.

## Plugin troubleshooting

### A plugin doesn’t appear in `cortex plugin list`

- Confirm the manifest exists at `.cortex-plugin/plugin.json` or `.claude-plugin/plugin.json`.
- Run `cortex plugin validate <path>` to surface manifest errors.
- If you installed via Git, check the registry at `~/.snowflake/cortex/plugins/registry.json` for an entry with a non-null `lastUpdateError`.

### Skills, commands, or agents from a plugin aren’t loading

- Confirm the plugin is active: `cortex plugin list` and look for `active: true`.
- Run `cortex plugin validate <name>` to see component-level issues.
- Run `/plugin reload` in a session to re-aggregate plugin contributions without restarting CoCo.

### A plugin’s MCP servers are missing

- Confirm the plugin is active and its `mcpServers` block is valid JSON.
- Check whether your administrator has disabled user MCP servers; plugin MCP servers are skipped in that mode.
- Use `/mcp` to verify the server appears as a known server.

## Plugin best practices

- **Pin a version.** Include a `version` field in your manifest so users can tell what they’re running.
- **Validate before shipping.** Run `cortex plugin validate` as part of your release process.
- **Keep MCP credentials out of the manifest.** Use environment variable expansion or OAuth in MCP server entries; never check tokens into plugin source.
- **Prefer convention over configuration.** Use the default `./skills`, `./agents`, `./commands` directories so the manifest stays minimal.
- **Provide an `activation.md`.** When the plugin is disabled, an `activation.md` lets users discover it through a stub skill instead of having to know its exact name.
