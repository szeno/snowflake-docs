# Managed settings (organization policy)

Managed settings allow IT administrators to enforce CoCo behavior across an organization. They apply to both **CoCo CLI** and **CoCo Desktop**, which read the same `managed-settings.json` file from the same system path. Settings are deployed to a system-owned file that users can’t modify, and they take precedence over all user-level configuration.

Note

CoCo Desktop and CoCo CLI share this schema, but some keys apply to the CLI only and have no effect in Desktop: `required.minimumVersion` (Desktop has its own auto-update), `settings.forceSandboxEnabled` / `settings.forceSandboxMode`, `files.connectionsFile` / `files.mcpFile`, `defaults.*`, and `account()` (Desktop reads the setting but doesn’t enforce it; account restrictions are CLI-only). The `permissions`, `settings.forceNoHistoryMode`, and `ui.*` keys apply to both.

When managed settings are present, CoCo displays a banner at startup indicating that it’s running in managed mode.

## How managed settings work

Managed settings are read from a JSON file placed in a platform-specific system directory, a location that requires administrator or root privileges to write to. Because users can’t modify files in these locations, managed settings can’t be overridden by user configuration files, environment variables, or command-line arguments (except where explicitly noted).

Administrators typically deploy the managed settings file using MDM tools (Jamf, Intune, SCCM), configuration management systems (Ansible, Chef, Puppet), or manual deployment during device provisioning.

## File locations

Place the `managed-settings.json` file in the following system directory for your operating system:

| Platform | Path |
| --- | --- |
| macOS | `/Library/Application Support/Cortex/managed-settings.json` |
| Linux and WSL | `/etc/cortex/managed-settings.json` |
| Windows | `%ProgramData%\Cortex\managed-settings.json` |

Expand

Show lessSee more

If the file doesn’t exist, the CLI runs in unmanaged mode and all user-level defaults apply.

Note

If the file exists but contains invalid JSON or fails schema validation, the CLI applies a restrictive fallback configuration and displays a banner reading “Enforcement config error - restricted mode”. This prevents a malformed policy file from silently granting unrestricted access.

## Configuration schema

The `managed-settings.json` file must contain a `version` field. All top-level sections are optional.

Copy code

```
{
  "version": "1.0",
  "permissions": { },
  "settings":    { },
  "required":    { },
  "defaults":    { },
  "files":       { },
  "ui":          { }
}
```

The `version` field must be `"1.0"`.

### `permissions`

Controls which tools, skills, MCP servers, and Snowflake accounts the CLI may use. For the full pattern syntax, see [Permission patterns](#label-cortex-code-managed-permission-patterns).

Copy code

```
{
  "permissions": {
    "onlyAllow": ["read", "write", "bash(git:*)", "skill(bundled:*)"],
    "deny": ["bash(rm:*)", "skill(remote:*)"],
    "defaultMode": "allow",
    "dangerouslyAllowAll": false
  }
}
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `onlyAllow` | `string[]` | — | Allowlist of permission patterns. If set, only matching items are permitted. Items not matched by any pattern are blocked unless `defaultMode` is `"allow"`. |
| `deny` | `string[]` | — | Denylist of permission patterns. Deny takes precedence over allow. A match here always blocks, regardless of `onlyAllow`. |
| `defaultMode` | `"allow"` or `"deny"` | `"allow"` | Behavior when no pattern matches. Use `"deny"` for a strict allowlist posture. |
| `dangerouslyAllowAll` | `boolean` | `false` | Controls whether users can use the `--dangerously-allow-all-tool-calls` flag. In managed mode, defaults to `false`. Set to `true` only in explicitly trusted environments. |

Expand

Show lessSee more

### `settings`

Forces specific runtime behaviors that can’t be overridden by users.

Copy code

```
{
  "settings": {
    "forceNoHistoryMode": true,
    "forceSandboxEnabled": true,
    "forceSandboxMode": "regular"
  }
}
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `forceNoHistoryMode` | `boolean` | `false` | When `true`, disables all conversation history persistence. Session files aren’t written to disk. Use in high-security or compliance environments where chat history must not be stored. |
| `forceSandboxEnabled` | `boolean` | `false` | When `true`, forces the sandbox to be enabled regardless of user settings. The sandbox restricts filesystem access during tool execution. |
| `forceSandboxMode` | `"regular"` or `"autoAllow"` | — | Forces a specific sandbox mode. `"regular"` prompts the user before allowing new filesystem paths. `"autoAllow"` silently permits all paths within the sandbox boundary. Only takes effect when the sandbox is enabled. |

Expand

Show lessSee more

The sandbox limits which directories the CLI can read and write during a session. It adds a confirmation step before tools access paths outside the pre-approved set. `"regular"` mode requires user confirmation for each new directory; `"autoAllow"` mode trusts all directories within the working tree without prompting. Sandbox is an experimental feature. For details, see [Sandbox](/user-guide/cortex-code/sandbox).

### `required`

Enforces a minimum CLI version. The CLI exits with an error if the installed version doesn’t meet the requirement.

Copy code

```
{
  "required": {
    "minimumVersion": "0.26.0"
  }
}
```

| Field | Type | Description |
| --- | --- | --- |
| `minimumVersion` | `string` | Minimum CLI version in semver format (for example, `"0.26.0"`). Users on older versions see an error and are prompted to update before they can continue. |

Expand

Show lessSee more

Use this field to ensure all users are on a version that supports any security fix or feature your policy depends on.

### `defaults`

Sets organization-recommended defaults that users can override in their own `settings.json`. Unlike the `settings` section, these are suggestions, not enforcement.

Copy code

```
{
  "defaults": {
    "connectionName": "prod",
    "profileName": "data-analyst",
    "theme": "dark"
  }
}
```

| Field | Type | Description |
| --- | --- | --- |
| `connectionName` | `string` | Default Snowflake connection name from `connections.toml`. Users can override this with `-c` or by changing their own settings. |
| `profileName` | `string` | Default profile to load at startup. |
| `theme` | `"dark"`, `"light"`, or `"pro"` | Default UI color theme. |

Expand

Show lessSee more

### `files`

Points the CLI to admin-provided configuration files. These are loaded in addition to, or instead of, the user’s own equivalents.

Copy code

```
{
  "files": {
    "connectionsFile": "/etc/cortex/connections.toml",
    "mcpFile": "/etc/cortex/mcp.json"
  }
}
```

| Field | Type | Description |
| --- | --- | --- |
| `connectionsFile` | `string` | Absolute path to an admin-provided `connections.toml`. Use this to pre-configure Snowflake connections for all users without requiring individual setup. |
| `mcpFile` | `string` | Absolute path to an admin-provided `mcp.json`. Use this to deploy organization-approved MCP servers to all users. |

Expand

Show lessSee more

### `ui`

Customizes UI elements to indicate managed state.

Copy code

```
{
  "ui": {
    "showManagedBanner": true,
    "bannerText": "Managed by Acme IT - support: helpdesk@acme.com",
    "hideDangerousOptions": true
  }
}
```

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `showManagedBanner` | `boolean` | `false` | When `true`, displays a banner in the welcome screen indicating this is a managed installation. Helps users understand why certain features may be restricted. |
| `bannerText` | `string` | `"This device is managed by your organization"` | Custom text for the managed banner. Use this to include a support contact or policy reference. |
| `hideDangerousOptions` | `boolean` | `false` | When `true`, suppresses dangerous options from help output and UI menus. |

Expand

Show lessSee more

## Permission patterns

The `onlyAllow` and `deny` arrays in the `permissions` section accept patterns in two forms:

- **Simple name**: matches a named tool or feature category exactly. For example, `"bash"` or `"read"`.
- **Filtered name**: `type(filter)`. This matches a specific tool invocation or resource within a category. For example, `"bash(git:*)"` or `"account(myorg-prod)"`.

Both forms support `*` (any characters) and `?` (single character) glob wildcards. Matching is case-insensitive.

### Pattern reference

| Pattern | What it controls |
| --- | --- |
| `"read"` | The `read` (file reading) tool |
| `"write"` | The `write` (file writing) tool |
| `"edit"` | The `edit` (file editing) tool |
| `"grep"` | The `grep` (file content search) tool |
| `"glob"` | The `glob` (file pattern matching) tool |
| `"bash"` | All bash shell invocations |
| `"bash(git:*)"` | Bash restricted to `git` commands |
| `"bash(dbt:*)"` | Bash restricted to `dbt` commands |
| `"bash(ls:*)"` | Bash restricted to `ls` commands |
| `"bash(rm:*)"` | Bash `rm` commands (commonly denied) |
| `"sql_execute"` | SQL execution against Snowflake |
| `"mcp(*)"` | All MCP servers |
| `"mcp(https://*.company.com/*)"` | MCP servers matching a URL glob |
| `"skill(bundled:*)"` | Built-in (bundled) skills |
| `"skill(profile:*)"` | Skills from any loaded profile |
| `"skill(profile:my-profile)"` | Skills from a specific named profile |
| `"skill(user:*)"` | Skills installed to the user’s home directory |
| `"skill(project:*)"` | Skills in the project’s `.cortex/skills/` directory |
| `"skill(remote:*)"` | Remotely installed skills (via git or tarball) |
| `"plugin(*)"` | All plugins |
| `"plugin(bundled:*)"` | Built-in plugins only |
| `"account(myorg)"` | Exact Snowflake account name (CLI-only; Desktop reads but doesn’t enforce this setting) |
| `"account(myorg-*)"` | Snowflake accounts matching a glob (CLI-only; Desktop reads but doesn’t enforce this setting) |

Expand

Show lessSee more

### `bash(command:*)` filtering

When using bash filtering patterns, the filter matches the first token of the shell command. For example, `"bash(git:*)"` permits `git status`, `git commit`, and any other `git` subcommand, but blocks `curl`, `python`, and any other command.

Note

If `"bash"` (without a filter) appears in `onlyAllow`, then any bash command is permitted for that rule. If `"bash(git:*)"` appears but plain `"bash"` doesn’t, then only `git` commands are allowed and all other bash commands are blocked.

## Permission evaluation

When the CLI decides whether a tool, skill, MCP server, or Snowflake account is permitted, it evaluates the following rules in order:

1. **Managed `deny` matches: block.** If any pattern in the managed settings `deny` array matches, access is denied. This can’t be overridden by profiles or user settings.
2. **Profile `deny` matches: block.** If any pattern in the active profile’s deny list matches, access is denied.
3. **Managed `onlyAllow` is set and no pattern matches: block.** If `onlyAllow` is configured in managed settings and the item doesn’t match any listed pattern, access is denied.
4. **Profile `onlyAllow` is set for this type and no pattern matches: block.** Profile `onlyAllow` is type-scoped: it only restricts types that are explicitly listed. If the profile lists `skill(bundled:*)` but says nothing about `bash`, bash access isn’t affected by the profile.
5. **`defaultMode` determines the outcome.** If `defaultMode` is `"deny"`, access is blocked. If `"allow"` (the default), access is permitted.

Key guarantees:

- A profile can’t grant access that managed settings have explicitly denied.
- A profile can’t expand the managed settings allowlist.
- Profiles can only further restrict: they operate within the boundary that managed settings define.

## Common policy examples

### Basic corporate setup

Allow all default tools but block bypass mode and display a managed banner.

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "dangerouslyAllowAll": false,
    "defaultMode": "allow"
  },
  "required": {
    "minimumVersion": "0.26.0"
  },
  "ui": {
    "showManagedBanner": true,
    "bannerText": "Managed by Corporate IT - helpdesk@example.com"
  }
}
```

### Restrict to approved Snowflake accounts

Only allow connections to specific accounts. Users who try to connect to any other account see an error.

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "onlyAllow": [
      "account(mycompany-prod)",
      "account(mycompany-staging)"
    ],
    "defaultMode": "allow"
  }
}
```

### Lock down to approved tools only

Only allow file reading, SQL execution, and bundled skills. Block all bash, MCP, and user-installed skills.

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "onlyAllow": [
      "read",
      "write",
      "edit",
      "grep",
      "glob",
      "sql_execute",
      "skill(bundled:*)",
      "skill(profile:*)"
    ],
    "defaultMode": "deny"
  }
}
```

### Allow bash but block dangerous commands

Permit bash access but explicitly deny `rm`, `curl`, and `wget`.

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "deny": [
      "bash(rm:*)",
      "bash(curl:*)",
      "bash(wget:*)"
    ],
    "dangerouslyAllowAll": false,
    "defaultMode": "allow"
  }
}
```

### High-security deployment

Force no history, force sandbox, block bypass mode, restrict to specific accounts and MCP servers, and block remote skill installation.

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "onlyAllow": [
      "read", "write", "edit", "bash", "sql_execute",
      "skill(bundled:*)", "skill(profile:*)",
      "mcp(https://*.mycompany.com/*)",
      "account(mycompany-*)"
    ],
    "deny": [
      "bash(rm:*)",
      "bash(curl:*)",
      "skill(remote:*)"
    ],
    "defaultMode": "allow",
    "dangerouslyAllowAll": false
  },
  "settings": {
    "forceNoHistoryMode": true,
    "forceSandboxEnabled": true,
    "forceSandboxMode": "regular"
  },
  "required": {
    "minimumVersion": "0.26.0"
  },
  "files": {
    "connectionsFile": "/etc/cortex/connections.toml",
    "mcpFile": "/etc/cortex/mcp.json"
  },
  "ui": {
    "showManagedBanner": true,
    "bannerText": "Managed by IT Security - policy questions: security@mycompany.com",
    "hideDangerousOptions": true
  }
}
```

## Verification

To confirm that managed settings are active and review what restrictions are applied, inspect the welcome banner on startup. When managed settings are present and `showManagedBanner` is `true`, a banner is shown at the top of the session output.

To check the enforcement config path for your platform, verify whether the file exists at the OS-specific path listed in [File locations](#label-cortex-code-managed-file-locations).

To inspect the active policy from the CLI, run `cortex managed-settings`. The command prints the parsed schema, the resolved permission mode, and any validation errors or warnings.
