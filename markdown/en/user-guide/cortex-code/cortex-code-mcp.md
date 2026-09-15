# CoCo CLI Model Context Protocol (MCP) support

CoCo CLI implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), an open standard that connects AI agents to external tools and data sources such as GitHub, Jira, internal APIs, and databases. Once you add an MCP server to CoCo, its tools become available to the agent automatically: no code changes are required.

This topic covers how to add and manage MCP servers, the full configuration schema, credential handling, and administrator controls.

## Transport types

CoCo supports three MCP transport types. Choose the transport that matches your server:

| Type | Use case | How CoCo connects |
| --- | --- | --- |
| `stdio` | Local tools, CLI wrappers, language-specific MCP servers | Spawns a subprocess and communicates over `stdin`/`stdout` |
| `http` | Web services, hosted APIs | Streamable HTTP requests |
| `sse` | Real-time streaming services | Server-Sent Events over HTTPS |

Expand

Show lessSee more

## Managing MCP servers

You can manage MCP servers from the command line using `cortex mcp`, or interactively from a CoCo session using the `/mcp` slash command.

### Command reference

| Command | Description |
| --- | --- |
| `cortex mcp add <name> <commandOrUrl> [args...]` | Register a new MCP server. See [Adding a server](#label-mcp-adding-server) for flags. |
| `cortex mcp list` | List all configured servers with transport, URL or command, and masked credential keys. |
| `cortex mcp get <name>` | Show detailed configuration for a single server, including OAuth fields. |
| `cortex mcp remove <name>` | Remove a server from configuration and delete its stored credentials. |
| `cortex mcp start` | Connect to all configured servers and report connected and failed counts. Waits up to 300 seconds for servers to load. |

Expand

Show lessSee more

### Interactive management

Run `/mcp` in a CoCo CLI session to open an interactive MCP status viewer. The viewer shows:

- Each server’s name, transport type, and connection state (`connecting`, `connected`, `reconnecting`, `failed`, `not_started`)
- The number of tools exposed by each connected server
- The last error reported by any failed server
- Toggle buttons to enable or disable individual servers without editing configuration files

### Adding a server

Use `cortex mcp add` to register a new MCP server from the command line:

Copy code

```
cortex mcp add <name> <commandOrUrl> [args...]
```

Flags:

| Flag | Description |
| --- | --- |
| `-t, --transport` (alias `--type`) | Transport type: `stdio`, `http`, or `sse`. Defaults to `stdio`. CoCo warns if the transport is inconsistent with the URL pattern. |
| `-e, --env <KEY=value>` | Set an environment variable for the subprocess (`stdio` only). Repeatable. |
| `-H, --header <Header: value>` | Set an HTTP header (`http` and `sse` only). Repeatable. |
| `--timeout <ms>` | Tool call timeout in milliseconds. |

Expand

Show lessSee more

Common examples:

| Action | Command |
| --- | --- |
| Add a stdio server | `cortex mcp add git-server uvx mcp-server-git` |
| Add an HTTP server | `cortex mcp add api-server https://api.example.com --type http` |
| Add with environment variable | `cortex mcp add my-server npx my-mcp-server -e API_KEY=secret` |
| Add with header | `cortex mcp add my-api https://api.example.com -H "Authorization: Bearer token"` |

Expand

Show lessSee more

Sensitive values passed via `-e` or `-H` are migrated into the OS keychain on first connection (see [Credential storage](#label-mcp-credentials)).

## Configuration file

MCP servers are configured in:

```
~/.snowflake/cortex/mcp.json
```

The top-level key is `mcpServers`. Each entry is keyed by server name:

Copy code

```
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "command-to-run",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### Server fields

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | Required. One of `stdio`, `http`, `sse`. |
| `command` | string | The executable to launch for `stdio` transports. |
| `args` | array of strings | Arguments passed to `command`. |
| `cwd` | string | Working directory for the `stdio` subprocess. |
| `url` | string | The endpoint URL for `http` and `sse` transports. |
| `env` | object | Environment variables for the `stdio` subprocess. Migrated to the keychain on first use. |
| `headers` | object | HTTP headers for `http` and `sse` transports. Migrated to the keychain on first use. |
| `timeout` | number | Tool call timeout in milliseconds. Defaults to 60,000 (60 seconds). Can also be overridden globally via the `COCO_MCP_TOOL_TIMEOUT_MS` environment variable. |
| `oauth` | object | OAuth 2.0 configuration for `http` transports. See [OAuth authentication](#label-mcp-oauth). |

Expand

Show lessSee more

### Environment variable expansion

CoCo expands environment variables in every field of `mcp.json` before connecting. Three syntaxes are supported:

| Syntax | Behavior |
| --- | --- |
| `${VAR}` | Replaced with the value of `VAR`. If `VAR` is not set, the literal `${VAR}` is preserved. |
| `${VAR:-default}` | Replaced with `VAR` if set, otherwise with `default`. |
| `$VAR` | Short form of `${VAR}`. |

Expand

Show lessSee more

Important

Use environment variables for credentials. Do not hardcode tokens or secrets in `mcp.json`. Export sensitive values from your shell profile (`~/.bashrc`, `~/.zshrc`) so they are not checked into source control.

Copy code

```
export GITHUB_TOKEN="your_token_here"
```

### Configuration precedence

CoCo merges MCP servers from multiple sources in the following order (later sources win when names collide, with the exception of plugins):

1. **Administrator-enforced** servers from the managed settings enforcement file.
2. **Connection profile** servers declared in your active Snowflake connection.
3. **User** servers from `~/.snowflake/cortex/mcp.json` (only if your administrator allows user MCP servers).
4. **Plugin** servers declared by installed plugins (skipped when user MCP servers are disabled by the administrator). Plugin servers never overwrite an existing server that was configured at a higher level.
5. **Administrator URL allowlist**. After merging, any server whose `url` is not permitted by managed settings is silently removed.

See [managed settings](/user-guide/cortex-code/managed-settings) for details on enforcement policies.

## Tool names and permissions

MCP tools are namespaced by server name so that two servers can expose tools of the same name without conflict. The composed tool name has the form:

```
mcp__<server-name>__<tool-name>
```

For example, a tool named `search` exposed by the server `github` is visible to the agent as `mcp__github__search`.

Tool names are limited to 64 characters and must contain only alphanumeric characters, underscores, and hyphens.

### Permissions

MCP tools participate in the standard CoCo permission system. Default permission decisions can be configured in:

```
~/.snowflake/cortex/permissions.json
```

You can match individual tools by their full composed name, or match all tools from a server with a wildcard pattern:

Copy code

```
{
  "allow": ["mcp__github__read_file", "mcp__github__list_repos"],
  "deny": ["mcp__github__delete_repo"],
  "ask": ["mcp__*"]
}
```

At runtime, permissions are also requested on first use and can be remembered for the session.

## Credential storage

When a server is added or configured with `env`, `headers`, or OAuth, CoCo migrates sensitive values out of `mcp.json` and into the OS keychain on first connection. The `mcp.json` file is rewritten with those fields removed.

- Credentials are stored under the keychain entry `mcp_oauth_<server-name>` as a unified blob containing tokens, OAuth client registration, headers, and environment variables.
- `cortex mcp list` and `cortex mcp get` display key names but never display secret values.
- `cortex mcp remove` removes both the configuration entry and the keychain entry.

If the OS keychain is unavailable (for example, in a headless container), credential storage degrades gracefully and no secrets are written to disk.

## OAuth authentication

For HTTP MCP servers that require OAuth 2.0, add an `oauth` block to the server configuration:

Copy code

```
{
  "mcpServers": {
    "my-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "oauth": {
        "client_id": "pre-registered-client-id",
        "client_name": "Cortex Code",
        "redirect_port": 8585,
        "scope": "openid mcp read write",
        "authorization_server_url": "https://auth.example.com"
      }
    }
  }
}
```

On first connection, CoCo opens your system browser for authentication. The resulting access and refresh tokens are stored in the OS keychain and are refreshed automatically before expiry.

| Field | Description |
| --- | --- |
| `client_id` | The OAuth client ID registered with the authorization server. If omitted, CoCo attempts Dynamic Client Registration. |
| `client_name` | Human-readable client name shown during dynamic registration. |
| `redirect_port` | Local port used for the OAuth redirect URI. Defaults to `8585`. |
| `scope` | Space-separated list of OAuth scopes to request. |
| `authorization_server_url` | URL of the authorization server. If omitted, CoCo discovers it from the MCP server’s metadata. |

Expand

Show lessSee more

Note

To reset OAuth credentials for a server, run `cortex mcp remove <server>` and re-add the server. You can then run `cortex mcp start` to reconnect all configured servers and trigger a fresh OAuth flow.

## Disabling servers

You can temporarily disable an MCP server without removing it from configuration. From the `/mcp` viewer, select the server and toggle it off. The disabled state is persisted to:

```
~/.snowflake/cortex/mcp-disabled.json
```

Disabled servers are not connected at session start, their tools are not exposed to the agent, and they are not auto-reconnected. Re-enable them at any time from `/mcp`.

## Using MCP tools

Once configured, MCP tools are available in every CoCo CLI session automatically. Invoke them through natural language:

```
Show me recent GitHub pull requests
Create a Jira ticket for this bug
Query the PostgreSQL database for user activity
```

Tool results are capped at 50 KB. If a tool returns more data, the output is truncated and CoCo appends a notice at the truncation point.

## Sample configurations

### Git server (stdio)

Copy code

```
{
  "mcpServers": {
    "git": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

### HTTP API with OAuth

Copy code

```
{
  "mcpServers": {
    "my-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "oauth": {
        "client_id": "my-client-id",
        "redirect_port": 8585,
        "scope": "openid mcp"
      }
    }
  }
}
```

### SSE server with headers

Copy code

```
{
  "mcpServers": {
    "realtime": {
      "type": "sse",
      "url": "https://realtime.example.com/events",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-Custom-Header": "value"
      },
      "timeout": 30000
    }
  }
}
```

### Sourcegraph integration (stdio with env)

Copy code

```
{
  "mcpServers": {
    "sourcegraph": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@sourcegraph/mcp-server"],
      "env": {
        "SRC_ACCESS_TOKEN": "${SOURCEGRAPH_TOKEN}",
        "SRC_ENDPOINT": "https://sourcegraph.company.com"
      }
    }
  }
}
```

## Plugin-declared MCP servers

Plugins can ship MCP servers with their distribution by declaring them in `plugin.json`. These servers are loaded automatically when the plugin is active:

Copy code

```
{
  "name": "my-plugin",
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "my_mcp_server"]
    }
  }
}
```

Plugin MCP servers have lower priority than user or profile servers: a plugin can’t overwrite a server that you configured directly. See the CoCo CLI plugins documentation for details.

## Administrator controls

Administrators can restrict MCP usage through managed settings:

- **Disable user MCP servers.** When `areUserMcpServersAllowed` is set to `false`, CoCo ignores `~/.snowflake/cortex/mcp.json` entirely and only servers provided by the administrator or the Snowflake connection profile are loaded. Plugin-declared MCP servers are also skipped in this mode.
- **URL allowlist.** Administrators can restrict the set of allowed MCP endpoint URLs. Servers whose URL is not permitted are silently removed after configuration is merged.
- **Enforced servers.** Administrators can ship a base `mcp.json` that is always applied. Users cannot remove or modify enforced servers.

See [managed settings](/user-guide/cortex-code/managed-settings) for the full enforcement schema.

## MCP troubleshooting

### Server not connecting

- Run `/mcp` and check the server’s status and last error.
- Run `cortex mcp start` from the terminal and watch for error output.
- Check `~/.snowflake/cortex/logs/` for MCP client and manager logs.
- Confirm that any required environment variables are set in your shell (`echo $VAR`).

### Tools not appearing

- Run `cortex mcp list` to confirm the server is configured.
- Make sure tool names are alphanumeric, underscore, or hyphen and 64 characters or fewer; MCP servers exposing invalid tool names are rejected.
- Confirm the server is not disabled in `~/.snowflake/cortex/mcp-disabled.json`.

### OAuth issues

- Clear cached credentials with `cortex mcp remove <server>` and re-add the server to trigger a fresh flow.
- Confirm that port `8585` (or your configured `redirect_port`) is available.
- If your authorization server supports Dynamic Client Registration, omit `client_id` and let CoCo register on your behalf.

### Environment variables not expanding

- Prefer `${VAR}` with braces over bare `$VAR` to avoid ambiguity.
- Verify the variable is exported in your shell (`echo $VAR`).
- Remember that CoCo expands variables from the process environment when the CLI was launched, not from an editor’s embedded shell.

### Output truncated

Tool results are capped at 50 KB. For large datasets, have the MCP server return a summary, a reference, or a pointer to a file that CoCo can read in a follow-up step.

## MCP best practices

- **Use descriptive server names.** Server names appear in the tool namespace, so pick names that make tool calls self-describing (for example, `mcp__github__search` is clearer than `mcp__gh1__search`).
- **Secure credentials.** Use environment variables or OAuth; never hardcode tokens in `mcp.json`.
- **Set appropriate timeouts.** The default tool timeout is 60 seconds. Increase it for long-running tools, or decrease it to fail fast on unresponsive servers.
- **Test connectivity first.** Run `cortex mcp start` after adding or updating a server to confirm it connects and exposes the tools you expect before relying on it from an agent session.
- **Scope permissions narrowly.** Use the `allow` and `deny` lists in `permissions.json` to pre-approve safe read-only tools and explicitly deny destructive ones.
