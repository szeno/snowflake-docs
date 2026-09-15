# CoCo CLI Settings

CoCo CLI settings control tool permissions, connections, and session behavior. You can
configure settings using managed policy (if provided by your organization), configuration files,
environment variables, and command-line arguments.

## Configuration files

The following configuration files are used by CoCo CLI:

| File | Purpose |
| --- | --- |
| `<admin-managed path>/managed-settings.json` | Organization-managed policy file (optional). For OS-specific locations, see [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-settings). |
| `~/.snowflake/cortex/settings.json` | Main CoCo CLI settings file. |
| `~/.snowflake/cortex/permissions.json` | Permission preferences. |
| `~/.snowflake/cortex/mcp.json` | MCP server configuration (see ). |
| `~/.snowflake/config.toml` | Snowflake connections (see [CoCo CLI](/user-guide/cortex-code/cortex-code-cli)). Shared with Snowflake CLI. |

Expand

Show lessSee more

The full layout of the main configuration directory is:

```
~/.snowflake/cortex/        # Main Cortex Code CLI config directory
├── settings.json          # Main settings
├── mcp.json               # MCP server configs
├── permissions.json       # Saved permissions
├── hooks.json             # Global hooks
├── history                # Command history
├── conversations/         # Session files
├── cache/                 # Temporary cache
│   ├── table_cache.json   # SQL result metadata
│   └── sql_result_cache/  # Parquet files
├── logs/                  # Log files (coco.log, coco_errors.log)
├── memory/                # Persistent memory
├── agents/                # Custom agents
├── skills/                # Global skills
├── commands/              # Custom commands
├── hooks/                 # Hook scripts
└── remote_cache/          # Cloned repos
```

### Settings precedence

Settings are applied in the following order of precedence (highest to lowest):

1. Managed settings restrictions (`settings.*` fields in `managed-settings.json`). Can’t be overridden by any user-level configuration. See [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-settings).
2. Profile overrides (`settingsOverrides` from the active profile, if any).
3. Project settings (`.cortex/settings.json` or `.claude/settings.json` in the working directory).
4. Managed settings defaults (`defaults.*` fields in `managed-settings.json`). Users can override these in their own `settings.json`.
5. Global user settings (`~/.snowflake/cortex/settings.json`).
6. Default values embedded in the CoCo CLI.

Permissions follow a separate evaluation order. See [Permission evaluation](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-permission-evaluation).

### `settings.json`

`~/.snowflake/cortex/settings.json`
:   Main settings file for CoCo CLI.

Example content:

Copy code

```
{
   "compactMode": true,
   "autoUpdate": true,
   "theme": "dark"
}
```

The following settings are available:

- `compactMode`: Enables compact output formatting.
- `autoUpdate`: Enables automatic updates.
- `theme`: Sets the CLI theme (`light` or `dark`).

### `permissions.json`

`~/.snowflake/cortex/permissions.json`
:   Controls tool access permissions.

Example content:

Copy code

```
{
  "onlyAllow": ["read_file", "execute_sql"],
  "defaultMode": "ask",
  "dangerouslyAllowAll": false
}
```

The following settings are available:

- `onlyAllow`: List of allowed tool patterns.
- `defaultMode`: Default permission mode (`ask`, `allow`, `deny`).
- `dangerouslyAllowAll`: Allows all tools without prompts (unsafe).

### Managed settings (organization policy)

Administrators can deploy a system-level JSON policy file to enforce CoCo CLI behavior across an organization, restricting tools, accounts, and minimum versions. For details, see [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings).

## Environment variables

CoCo CLI recognizes the following configuration environment variables:

| Variable | Description |
| --- | --- |
| `SNOWFLAKE_HOME` | Overrides the default `~/.snowflake` directory. |
| `CORTEX_AGENT_MODEL` | Overrides model selection. |
| `CORTEX_ENABLE_MEMORY` | Enables the memory tool (set to `true` or `1`). |
| `COCO_DANGEROUS_MODE_REQUIRE_SQL_WRITE_PERMISSION` | Requires confirmation for SQL write operations in bypass mode. |
| `COCO_LOG_LEVEL` | Minimum log level written to disk: `DEBUG`, `INFO`, `WARNING`, or `ERROR`. Default: `INFO`. |
| `COCO_DEBUG` | Set to `1`, `true`, or `yes` to force debug logging. Overrides `COCO_LOG_LEVEL`. |
| `COCO_LOG_DIR` | Directory for `coco.log` and `coco_errors.log`. Default: `$SNOWFLAKE_HOME/cortex/logs`, where `SNOWFLAKE_HOME` defaults to `~/.snowflake`. |

Expand

Show lessSee more

Note

For additional permission-related environment variables, see [Security](/user-guide/cortex-code/security).

## Command-line overrides

CoCo CLI settings can be overridden via command-line arguments, which include the following:

| Example | Description |
| --- | --- |
| `cortex -c production` | Specifies the connection. |
| `cortex --workdir /path` | Sets the working directory. |
| `cortex --continue` | Continues the last session. |
| `cortex --resume <session_id>` | Resumes a specific session. |
| `cortex --plan` | Enables planning mode. |
| `cortex --dangerously-allow-all-tool-calls` | Disables permission prompts (unsafe). |

Expand

Show lessSee more

## Session storage

Conversations and settings are stored in:

| Location | Description |
| --- | --- |
| `~/.snowflake/cortex/conversations/` | Session files. |
| `~/.snowflake/cortex/permissions.json` | Permission preferences. |
| `~/.snowflake/cortex/mcp.json` | MCP configuration. |

Expand

Show lessSee more
