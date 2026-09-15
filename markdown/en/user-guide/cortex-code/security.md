# Security best practices for CoCo CLI

Essential security practices for CoCo CLI include using secure authentication methods, protecting configuration files, managing roles and access appropriately, handling conversation history securely, ensuring MCP server integrity, and following production safety protocols.

Important

In managed environments, your organization may deploy a system-level managed settings file that enforces policy (for example, restricting tool access, limiting allowed accounts, or disabling bypass capabilities). For details, see [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-settings).

## Credentials

[Recommended] Use browser-based authentication when possible.
:   The default authentication method for CoCo CLI is browser-based authentication. Use `authenticator = "externalbrowser"` in your `connections.toml` file to set this option manually.

Use programmatic access tokens (PATs), when trying to scope access to a specific role.
:   Generate dedicated PATs in Snowsight (see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens)). Set expiration ≤ 90 days, use descriptive names, and rotate regularly.

Protect configuration files
:   Use mode `600` for configuration files and `700` for directories to restrict access to only your user.

    Copy code

    ```
    chmod 600 ~/.snowflake/connections.toml
    chmod 700 ~/.snowflake/cortex
    ```

Never commit credentials
:   Add sensitive configuration files to `.gitignore`.

    Copy code

    ```
    echo "~/.snowflake/connections.toml" >> ~/.gitignore
    ```

    Use environment variables to hold credentials and tokens, and incorporate them in your configuration files using `${VARIABLE_NAME}` syntax.

## Roles & access

Use appropriate roles per environment
:   For example, use a read-only role in production and a more expansive role in development.

    Copy code

    ```
    [dev]
    role = "DEVELOPER"

    [prod_readonly]
    role = "ANALYST"
    ```

    Never use `ACCOUNTADMIN` for routine operations. Grant least privileges.

## Conversation history

Conversations are stored in `~/.snowflake/cortex/conversations/`. Use `cortex --private` when starting CoCo to disable session saving for sensitive work.
Alternatively, use the `/clear` command to clear the current session before exiting CoCo CLI.

Use mode 700 to restrict access to conversation history to only your user.

Copy code

```
chmod 700 ~/.snowflake/cortex/conversations
```

## MCP security

Only install trusted MCP servers
:   Verify the source and integrity of MCP servers before adding them. Use the following commands to get a list of servers and remove any untrusted ones:

    Copy code

    ```
    cortex mcp list
    cortex mcp remove <server>
    ```

Never hardcode MCP credentials
:   Use environment variables. First, set in your shell:

    Copy code

    ```
    export GITHUB_TOKEN="your_token"
    ```

    Then reference them in your MCP configuration:

    Copy code

    ```
    {
       "mcpServers": {
          "github": {
             "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
          }
       }
    }
    ```

## Production safety

Enable planning mode
:   Use the `/plan` command to review intended actions before execution.

    ```
    /plan
    Drop and recreate the ANALYTICS schema
    ```

## If your personal access token is compromised

Revoke the PAT in Snowsight immediately! Then generate a new token and start using it instead. Remember, don’t use the
token in configuration files; use environment variables instead.

Review the query history to identify any suspicious activity. Use `INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER` for real-time results (no special privileges required to view your own history):

Copy code

```
SELECT *
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY_BY_USER(
    USER_NAME => '<username>',
    RESULT_LIMIT => 1000
))
ORDER BY START_TIME DESC;
```

Account administrators can also query `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` for a full account-wide view, but that view has up to 45 minutes of latency.

## Managed settings (enterprise policy)

In some organizations, administrators deploy managed settings that enforce policy for CoCo CLI. Managed settings can constrain or override user-level configuration (including permission prompts and bypass behavior).

For more information, see [Managed settings (organization policy)](/user-guide/cortex-code/managed-settings#label-cortex-code-managed-settings).

## Permissions

CoCo has three operational modes:

| Mode | Indicator | Slash commands | Description |
| --- | --- | --- | --- |
| Confirm actions | Blue ⏵⏵ | Default mode | Prompts for permission before potentially dangerous actions. |
| Plan | Orange ⏸ | `/plan`, `/plan-off` | Presents a plan before taking any action. |
| Bypass | Red >> | `/bypass`, `/bypass-off` | All tool calls are approved. |

Expand

Show lessSee more

Press `Shift-Tab` in CoCo CLI to cycle among these modes.

Warning

The Bypass mode disables all confirmation prompts. Use it only in trusted environments.

### Permission types

The following permission levels apply to CoCo tool calls:

| Type | Description |
| --- | --- |
| EXECUTE\_COMMAND | Run bash/shell commands |
| FILE\_READ | Read file contents |
| FILE\_WRITE | Create/modify files |
| FILE\_EDIT | Edit existing files |
| WEB\_ACCESS | Web search/fetch operations |

Expand

Show lessSee more

### Trust model

Support for this feature is experimental and may be subject to change.
CoCo makes an attempt to classify commands and operations by risk, as shown in the following table:

| Level | Examples | Behavior |
| --- | --- | --- |
| SAFE | `ls`, `cat`, `echo`, `grep` | Auto-approved |
| LOW | Create new files (e.g., `touch file.txt`) | Usually auto-approved |
| MEDIUM | Edit files (e.g., `nano file.txt`), moderate bash | Prompts in Confirm mode |
| HIGH | `rm`, `curl`, `wget`, `sudo` | Always prompts |
| CRITICAL | `rm -rf`, destructive ops | Extra confirmation |

Expand

Show lessSee more

#### SQL queries

SQL is categorized by operation type:

| Category | Operations | Behavior |
| --- | --- | --- |
| READ\_ONLY | SELECT, SHOW, DESCRIBE | Auto-approved |
| WRITE | INSERT, UPDATE, DELETE, CREATE | Prompts |
| USE\_ROLE | USE ROLE, USE WAREHOUSE | Prompts |

Expand

Show lessSee more

### Sandbox

CoCo CLI supports sandboxing to isolate command execution. For full details on configuring
and using the sandbox, see [Sandbox](/user-guide/cortex-code/sandbox).

### Hook integration

You can customize permission policy using hooks. Here is an example pre-execution hook that approves auto-approves bash commands:

```
{
   "hooks": {
      "PreToolUse": [
         {
         "matcher": "bash",
         "hooks": [
            {
               "type": "command",
               "command": "bash .claude/hooks/auto-approve.sh"
            }
         ]
         }
      ]
   }
}
```

This hook might return a JSON response like the following to auto-approve bash commands.

Copy code

```
{
   "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "allow",
      "permissionDecisionReason": "Approved by policy"
   }
}
```

### Permission prompts and caching

When CoCo requires your permission to proceed with an operation, it prompts you with details about the request.
You can choose to approve or deny the request. You can also opt to remember your choice for future similar requests:

- “Always allow (this session)” remembers until you exit CoCo CLI.
- “Always allow (persist)” remembers indefinitely.

These responses are cached and scoped to the project directory, the tool type, or the command pattern as appropriate.

Persistent permissions are stored in `~/.snowflake/cortex/permissions.json`. The following is an example cache:

Copy code

```
{
   "/path/to/project": {
      "Bash": {
         "npm test": "allow",
         "make build": "allow"
      },
      "Write": {
         "*": "allow"
      }
   }
}
```

Delete this file to reset all persistent permissions. To reset permissions for a specific project, delete the corresponding entry.

To reset the session cache, use the `/new` command, which begins a new session, or exit and re-start CoCo CLI.

### Configuration

Set the environment variables described below to control permission behavior:

| Variable | Description |
| --- | --- |
| `CORTEX_PERMISSION_CACHE_TTL_SECONDS` | Sets the default timeout for session permission cache (in seconds). |
| `COCO_DANGEROUS_MODE_REQUIRE_SQL_WRITE_PERMISSION=true` | If set to `1`, always prompt for SQL write operations, even in bypass mode |

Expand

Show lessSee more

## Security Checklist

- Use PATs with at most a 90 day expiration
- Set file permissions to 600/700
- Never commit credentials to git
- Use least privilege roles
- Never use ACCOUNTADMIN for routine work
- Enable planning mode for production and reserve bypass mode for trusted environments
- Only install trusted MCP servers
- Store credentials in environment variables
- Use hooks to enforce policies by automating custom security checks
- Periodically audit permissions
