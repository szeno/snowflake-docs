# Managed settings

Administrators can centrally configure CoCo Desktop with a managed-settings file. The app
reads this file at startup and applies it on top of (and where it conflicts, in place of) user
settings, so users can’t loosen the controls it sets.

| Platform | Path |
| --- | --- |
| macOS | `/Library/Application Support/Cortex/managed-settings.json` |
| Windows | `C:\ProgramData\Cortex\managed-settings.json` |
| Linux | `/etc/cortex/managed-settings.json` |

Expand

Show lessSee more

Today the file supports these keys:

- `version` (required): must be `"1.0"`. If the file is missing this, malformed, or unreadable, the app enters a fail-closed restricted mode (it shows a banner and applies a default-deny permission mode).
- `permissions.onlyAllow` (array): allowlist of permission patterns. When set, only matching actions are permitted.
- `permissions.deny` (array): denylist of permission patterns, evaluated before `onlyAllow`. A deny match always blocks.
- `permissions.defaultMode` (string): fallback when no pattern matches, `"allow"` (default) or `"deny"`. Use `"deny"` for a strict allowlist posture.
- `permissions.dangerouslyAllowAll` (boolean): when `false`, administrators block Bypass Approvals. The mode picker shows Bypass Approvals disabled with a “Blocked by your organization” message, and any user who previously enabled it is reset to Default Approvals.
- `settings.forceNoHistoryMode` (boolean): when `true`, conversations aren’t persisted.
- `ui.showManagedBanner` (boolean) and `ui.bannerText` (string): show a managed-by-organization banner with custom text.
- `ui.hideDangerousOptions` (boolean): hide the dangerous-options UI.

Note

The managed-settings schema is shared with CoCo CLI, but some CLI-only keys have no effect in Desktop: `required.minimumVersion` (Desktop has its own auto-update), `settings.forceSandboxEnabled` / `settings.forceSandboxMode`, `files.connectionsFile` / `files.mcpFile`, `defaults.*`, and `account()` (Desktop reads the setting but does not enforce it; account restrictions are CLI-only). For the complete schema and pattern reference, see [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings).

Desktop also uses a different pattern name for SQL tool permissions: use `snowflake_sql_execute` in Desktop policies. The CLI uses `sql_execute` (renamed in CLI v1.1.8). If you use the same policy file for both surfaces, list both names in `onlyAllow` or `deny`.

## Permission patterns

Patterns in `onlyAllow` and `deny` are either a bare tool name or `type(filter)`, where `filter` is a case-insensitive glob (`*` and `?`). For `bash`, the filter matches the first token of the command.

| Pattern | What it controls |
| --- | --- |
| `read`, `write`, `edit` | The file read, write, and edit tools |
| `grep`, `glob` | The file content search and file pattern matching tools |
| `bash` | All shell commands |
| `bash(git:*)`, `bash(dbt:*)` | Shell restricted to `git` / `dbt` commands |
| `bash(rm:*)`, `bash(curl:*)` | Specific commands (commonly denied) |
| `snowflake_sql_execute` | SQL execution against Snowflake |
| `mcp(*)`, `mcp(https://*.acme.com/*)` | MCP servers, all or by URL glob |
| `skill(bundled:*)`, `skill(user:*)`, `skill(remote:*)` | Skills by source |
| `account(myorg-*)` | Snowflake accounts by name (CLI-only; Desktop reads but does not enforce this setting) |

Expand

Show lessSee more

## Examples

The following policy allows shell access but blocks dangerous commands, forces private mode, and shows a managed banner:

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "deny": ["bash(rm:*)", "bash(curl:*)", "bash(wget:*)", "skill(remote:*)"],
    "defaultMode": "allow"
  },
  "settings": {
    "forceNoHistoryMode": true
  },
  "ui": {
    "showManagedBanner": true,
    "bannerText": "Managed by your organization.",
    "hideDangerousOptions": true
  }
}
```

To restrict to an approved set instead, use `onlyAllow` with `"defaultMode": "deny"`:

Copy code

```
{
  "version": "1.0",
  "permissions": {
    "onlyAllow": ["read", "write", "edit", "grep", "glob", "sql_execute", "skill(bundled:*)"],
    "defaultMode": "deny"
  }
}
```

Deploy the file with your existing device-management tooling (for example, Jamf, Intune, or a
configuration-management system) to the path for each platform.
