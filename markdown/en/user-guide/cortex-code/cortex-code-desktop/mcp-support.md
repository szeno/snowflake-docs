# CoCo Desktop Model Context Protocol (MCP) support

CoCo Desktop implements the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), an open standard that connects AI agents to external tools and data sources
such as GitHub, Jira, internal APIs, and databases. Once you add an MCP server to
CoCo Desktop, its tools become available to the agent automatically — no code
changes are required.

This topic covers how to add and manage MCP servers using the graphical interface,
the full configuration schema, credential handling, and administrator controls.

## Transport types

CoCo Desktop supports two MCP transport types. Choose the transport that matches your server:

| Transport | Use case | How it works |
| --- | --- | --- |
| stdio | Local tools, CLI wrappers, language-specific MCP servers | Spawns a subprocess and communicates over stdin/stdout |
| http | Web services, hosted APIs, real-time streaming services | Streamable HTTP requests (also supports SSE fallback) |

Expand

Show lessSee more

## Managing MCP servers

You manage MCP servers through the **Agent Settings** panel in CoCo Desktop.
Open Agent Settings and select **MCP** from the sidebar to view, add, and configure MCP connectors.

[![MCP Connectors panel in Agent Settings showing the list of configured servers and the Add New MCP Server form](/static/images/user-guide/cortex-code/cortex-code-desktop/mcp/mcp-settings-overview.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/mcp/mcp-settings-overview.png)

### Adding a server via the UI

To add a new MCP server from the graphical interface:

1. Open **Agent Settings** and navigate to the **MCP** tab.
2. Click **+ New** to open the Add New MCP Server form.
3. Select the **Configuration Scope**:
   - **Global** — stored in `~/.snowflake/cortex/mcp.json`, available in all workspaces.
   - **Workspace** — stored in `<workspace>/.snowflake/cortex/mcp.json`, scoped to the current project.
4. Choose to configure the server using the **Form** view or switch to the **JSON** tab for raw editing.
5. Fill in the server details:
   - **Server Name** — a unique identifier for this server (for example, `my-mcp-server`).
   - **Server Type** — select `Command (stdio)` or `Remote (HTTP)`.
   - For **Command (stdio)**: enter the command to run (for example, `uvx mcp-server-git`).
   - For **Remote (HTTP)**: enter the Server URL (for example, `https://your-mcp-server-url`).
6. Optionally add **Headers** (for HTTP servers) or **Environment Variables** (for stdio servers).
7. Click **Save**.

### Adding a server via JSON

In the Add New MCP Server form, switch to the **JSON** tab to paste or edit configuration directly.
This supports the same schema as the configuration file (see [Configuration file](#configuration-file)).

### Browsing the MCP gallery

CoCo Desktop includes a gallery of MCP servers that you can browse and install directly from the UI.
Click **+ New** and select **Browse MCP Servers** to discover available integrations.

### Server status and management

The MCP Connectors panel displays the status of each configured server. From here you can:

- Start, stop, or restart individual servers.
- View the number of tools exposed by each connected server.
- Filter servers by source using the **All Sources** dropdown.
- View server output logs for troubleshooting.

## Configuration file

MCP servers are configured in JSON files at these locations:

| Scope | Path |
| --- | --- |
| Global | `~/.snowflake/cortex/mcp.json` |
| Workspace | `<workspace>/.snowflake/cortex/mcp.json` or `<workspace>/.cortex/mcp.json` |

Expand

Show lessSee more

The top-level key is `"mcpServers"`. Each entry is keyed by server name:

Copy code

```
{
  "mcpServers": {
    "server-name": {
      "command": "command-to-run",
      "args": ["arg1", "arg2"]
    }
  }
}
```

### Server fields

#### Stdio servers (Command)

| Field | Type | Description |
| --- | --- | --- |
| `command` | string | Required. The executable to launch. |
| `args` | array of strings | Arguments passed to the command. |
| `env` | object | Environment variables for the subprocess. |
| `envFile` | string | Path to a `.env` file to load environment variables from. Supports `${workspaceFolder}`. |
| `cwd` | string | Working directory for the subprocess. |

Expand

Show lessSee more

#### HTTP servers (Remote)

| Field | Type | Description |
| --- | --- | --- |
| `url` | string | Required. The endpoint URL for the MCP server. |
| `headers` | object | HTTP headers sent with each request (for example, authorization tokens). |

Expand

Show lessSee more

### Environment variable expansion

CoCo Desktop expands environment variables in configuration fields before connecting. Three syntaxes are supported:

| Syntax | Behavior |
| --- | --- |
| `${VAR}` | Replaced with the value of `VAR`. If not set, the literal is preserved. |
| `${VAR:-default}` | Replaced with `VAR` if set, otherwise with `default`. |
| `$VAR` | Short form of `${VAR}`. |

Expand

Show lessSee more

Additionally, CoCo Desktop supports `${workspaceFolder}` to reference the
current workspace root in paths like `cwd` and `envFile`.

Important

Use environment variables for credentials. Do not hardcode tokens or secrets in `mcp.json`.
Export sensitive values from your shell profile (`~/.bashrc`, `~/.zshrc`) so they are
not checked into source control.

### Variable inputs for secrets

CoCo Desktop supports an `inputs` array in configuration files for prompting users to provide secrets at connection time,
avoiding the need to store them in plain text:

Copy code

```
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "${input:api-key}"
      }
    }
  },
  "inputs": [
    {
      "id": "api-key",
      "type": "promptString",
      "description": "Enter your API key",
      "password": true
    }
  ]
}
```

### Configuration precedence

CoCo Desktop merges MCP servers from multiple sources in the following order (later sources win when names collide):

1. Administrator-enforced servers from managed settings.
2. User servers from `~/.snowflake/cortex/mcp.json` (global).
3. Workspace servers from `<workspace>/.snowflake/cortex/mcp.json`.
4. Plugin-declared servers from installed plugins.
5. Servers discovered from other applications (Claude Desktop, Cursor, Windsurf) if discovery is enabled.

### Importing from other applications

CoCo Desktop can automatically discover MCP servers configured in other tools:

- **Claude Desktop** — `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- **Cursor** — `~/.cursor/mcp.json`
- **Windsurf** — `~/.codeium/windsurf/mcp_config.json`

Discovery sources are individually toggleable via the `chat.mcp.discovery.enabled` setting.

## Tool names and permissions

MCP tools are namespaced by server name so that two servers can expose tools of
the same name without conflict. The composed tool name has the form:

Copy code

```
mcp__<server-name>__<tool-name>
```

For example, a tool named `search` exposed by the server `github` is visible to
the agent as `mcp__github__search`.

Tool names are limited to 64 characters and must contain only alphanumeric characters,
underscores, and hyphens.

### Permissions

MCP tools participate in the standard CoCo permission system. At runtime,
permissions are requested on first use and can be remembered for the session.
Default permission rules can be configured in:

Copy code

```
~/.snowflake/cortex/settings.json
```

You can match individual tools by their full composed name, or match all tools from a server with a wildcard:

Copy code

```
{
  "permissions": {
    "allow": ["mcp__github__read_file", "mcp__github__list_repos"],
    "deny": ["mcp__github__delete_repo"],
    "ask": ["mcp__*"]
  }
}
```

## Using MCP tools

Once configured, MCP tools are available in every CoCo Desktop session automatically.
Invoke them through natural language in the chat:

Copy code

```
Show me recent GitHub pull requests
Create a Jira ticket for this bug
Query the PostgreSQL database for user activity
```

Tool results are capped at 50 KB. If a tool returns more data, the output is truncated and a notice is appended.

## Sample configurations

### Git server (stdio)

Copy code

```
{
  "mcpServers": {
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    }
  }
}
```

### HTTP API with headers

Copy code

```
{
  "mcpServers": {
    "my-api": {
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### NPM package with environment variables

Copy code

```
{
  "mcpServers": {
    "sourcegraph": {
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

### Workspace-scoped server with envFile

Copy code

```
{
  "mcpServers": {
    "project-api": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "envFile": "${workspaceFolder}/.env",
      "cwd": "${workspaceFolder}"
    }
  }
}
```

## Plugin-declared MCP servers

Plugins can ship MCP servers with their distribution by declaring them in `plugin.json`.
These servers are loaded automatically when the plugin is active:

Copy code

```
{
  "name": "my-plugin",
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"]
    }
  }
}
```

Plugin MCP servers have lower priority than user or workspace servers — a plugin
cannot overwrite a server that you configured directly.

## Administrator controls

Administrators can restrict MCP usage through [managed settings](https://docs.snowflake.com/user-guide/cortex-code/managed-settings).

## MCP troubleshooting

### Server not connecting

- Check the server status in the MCP Connectors panel under Agent Settings.
- Click on the server to view its output log and inspect error messages.
- Confirm that any required environment variables are set in your shell (`echo $VAR`).
- For stdio servers, verify the command is available on your `PATH`.

### Tools not appearing

- Confirm the server status shows as connected in the MCP panel.
- Ensure tool names are alphanumeric, underscore, or hyphen and shorter than 64 characters.
  Servers exposing invalid tool names are rejected.
- Check if the server is disabled or filtered out by administrator URL allowlists.

### Environment variables not expanding

- Prefer `${VAR}` with braces over bare `$VAR` to avoid ambiguity.
- Verify the variable is exported in your shell (`echo $VAR`).
- Remember that CoCo Desktop expands variables from the process environment at launch time.

### Output truncated

Tool results are capped at 50 KB. For large datasets, have the MCP server return a summary,
a reference, or a pointer to a file that CoCo can read in a follow-up step.

## MCP best practices

- **Use descriptive server names.** Server names appear in the tool namespace, so pick names that make tool calls self-describing (for example, `mcp__github__search` is clearer than `mcp__gh1__search`).
- **Secure credentials.** Use environment variables, `envFile`, or the `inputs` prompt mechanism. Never hardcode tokens in `mcp.json`.
- **Use workspace scope for project-specific servers.** Keep project-specific MCP configurations in the workspace `mcp.json` so they travel with the project.
- **Set appropriate timeouts.** The default tool timeout is 60 seconds. This can be overridden globally via the `COCO_MCP_TOOL_TIMEOUT_MS` environment variable.
- **Scope permissions narrowly.** Use the `allow` and `deny` lists in `permissions.json` to pre-approve safe read-only tools and explicitly deny destructive ones.
