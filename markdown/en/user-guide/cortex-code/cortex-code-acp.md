# CoCo CLI Agent Client Protocol (ACP) support

CoCo CLI implements the [Agent Client Protocol (ACP)](https://agentclientprotocol.com/), an open standard that lets editors and IDEs embed an external agent as a local subprocess. When you run CoCo in ACP mode, your editor drives the session and CoCo streams agent responses, tool calls, and file diffs back over stdin/stdout.

ACP support lets you use CoCo inside editors that speak ACP without leaving your development environment.

## Supported ACP clients

CoCo CLI can be used as the agent backend for any ACP-compatible client, including:

- Zed
- JetBrains IDEs
- Neovim

For Visual Studio Code, use the [Snowflake extension for Visual Studio Code](/user-guide/vscode-ext#label-cortex-code-vscode-extension) instead of ACP.

For editor-specific setup steps, see [Configure Zed](#label-acp-configure-zed) and [Configure JetBrains IDEs](#label-acp-configure-jetbrains) below.

## Prerequisites

Before you configure an ACP client to use CoCo, make sure that:

- CoCo CLI is installed and available on your `PATH`. Run `cortex --version` to confirm.
- You have at least one Snowflake connection configured. Run `cortex auth login` or configure a connection in `~/.snowflake/connections.toml`.
- Your ACP client supports external agents over stdio using newline-delimited JSON (ndjson).

Note

ACP mode does not prompt for authentication. CoCo uses the Snowflake connection that you pass with `-c` (or the default `cortexAgentConnectionName` from your settings). Authenticate before launching your editor.

## Starting CoCo in ACP mode

Editors start CoCo as a subprocess using the `acp serve` command. You do not run this command directly in a terminal for normal use; your editor runs it for you based on its configuration.

Copy code

```
cortex acp serve -c <connection_name> [--bypass] [-m <model>] [-w <workdir>]
```

### Command options

| Option | Description |
| --- | --- |
| `-c, --connection <name>` | Snowflake connection to use. Defaults to the `cortexAgentConnectionName` setting if omitted. |
| `--bypass` | Auto-approve all tool calls for the session. Gated by your administrator’s policy; see [managed settings](/user-guide/cortex-code/managed-settings). |
| `-m, --model <model>` | Override the default model for the session. |
| `-w, --workdir <path>` | Working directory for the agent. Defaults to the process’s current working directory. |
| `--plugin-dir <path>` | Plugin directory or GitHub repo (`owner/repo`, `owner/repo#branch`, or URL). Can be repeated. |

Expand

Show lessSee more

Important

CoCo speaks ACP over the process’s stdin and stdout. Do not write to stdout from wrapper scripts, shell init files, or pre-run hooks when launching `cortex acp serve`: any extra output on stdout corrupts the protocol stream. Log to stderr or a file instead.

## Configuring an ACP client

Most ACP clients accept a JSON or TOML block describing the subprocess to launch. The minimum configuration specifies the `cortex` command and the `acp serve` arguments.

Generic ACP configWith model and workdir

Copy code

```
{
  "command": "cortex",
  "args": ["acp", "serve", "-c", "my_connection"]
}
```

Copy code

```
{
  "command": "cortex",
  "args": [
    "acp", "serve",
    "-c", "my_connection",
    "-m", "claude-sonnet-4-6",
    "-w", "/Users/me/projects/my-repo"
  ]
}
```

If your editor exposes environment variables for the agent subprocess, you can pass Snowflake credential overrides (for example `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`) through that mechanism. CoCo inherits the environment of the ACP client process.

### Configure Zed

To use CoCo in Zed, add it as a custom external agent. Before you start, complete the [Prerequisites](#prerequisites) and confirm that `cortex acp serve -c <connection_name>` runs successfully in a terminal.

The configuration below uses the same `agent_servers` structure described in the [Zed external agents documentation](https://zed.dev/docs/ai/external-agents). The only difference is the `command` and `args` values, which launch Cortex Code’s ACP subprocess (`cortex acp serve`) instead of a generic agent executable.

1. In Zed, open [Agent Settings](https://zed.dev/docs/ai/agent-settings) by running `agent: open settings`.
2. Go to the **External Agents** page and click **Add Agent**.
3. Choose **Add Custom Agent**. Zed opens your settings file with an `agent_servers` entry.
4. Replace the placeholder entry with a Cortex Code agent. Use your Snowflake connection name in place of `my_connection`:

Copy code

```
{
  "agent_servers": {
    "Cortex Code": {
      "type": "custom",
      "command": "cortex",
      "args": ["acp", "serve", "-c", "my_connection"],
      "env": {}
    }
  }
}
```

5. Save the settings file.
6. In the Agent panel, start a new thread and select **Cortex Code** as the external agent.

Optional: to set the agent working directory, add the Cortex Code CLI `-w` (`--workdir`) flag to `args`. This is a Cortex Code option, not a Zed setting. See [Command options](#label-acp-starting) above.

Copy code

```
{
  "agent_servers": {
    "Cortex Code": {
      "type": "custom",
      "command": "cortex",
      "args": ["acp", "serve", "-c", "my_connection", "-w", "/path/to/your/project"],
      "env": {}
    }
  }
}
```

For more detail, see the [Zed external agents documentation](https://zed.dev/docs/ai/external-agents).

### Configure JetBrains IDEs

To use CoCo in a JetBrains IDE that supports ACP, add it as a custom agent in `~/.jetbrains/acp.json`. Before you start, complete the [Prerequisites](#prerequisites) and confirm that `cortex acp serve -c <connection_name>` runs successfully in a terminal.

1. Open the **AI Chat** tool window.
2. Click the **three vertical dots** button in the upper-right corner of the AI Chat tool window and select **Add Custom Agent**.

   Choosing this option creates `~/.jetbrains/acp.json` and opens it for editing.
3. Find the absolute path to the `cortex` executable:

Copy code

```
which cortex
```

4. Populate `acp.json` with a Cortex Code entry under `agent_servers`. Use the absolute path from step 3 and your Snowflake connection name in place of `my_connection`:

Copy code

```
{
  "default_mcp_settings": {},
  "agent_servers": {
    "Cortex Code": {
      "command": "/absolute/path/to/cortex",
      "args": ["acp", "serve", "-c", "my_connection"],
      "env": {}
    }
  }
}
```

5. Save the file. The IDE can also detect ACP-compatible agents already installed on your machine and offer to add them with **Add to configuration**.
6. In AI Chat, select **Cortex Code**, enter a prompt, and send it.

Optional: to set the agent working directory, add the Cortex Code CLI `-w` (`--workdir`) flag to `args`. This is a Cortex Code option, not a JetBrains setting. See [Command options](#label-acp-starting) above.

Copy code

```
"args": ["acp", "serve", "-c", "my_connection", "-w", "/path/to/your/project"]
```

JetBrains requires an absolute path in the `command` field. If the agent fails to start, verify the path with `which cortex` and update `acp.json`.

Optionally, you can set `use_idea_mcp` and `use_custom_mcp` under `default_mcp_settings` to expose IDE MCP servers to the agent. For details on these settings, see the [JetBrains ACP documentation](https://www.jetbrains.com/help/ai-assistant/acp.html#add-custom-agent).

## Sessions and conversation history

Sessions started in ACP mode are stored in the same location as sessions created from the CoCo CLI:

```
~/.snowflake/cortex/conversations/<sessionId>.json
~/.snowflake/cortex/conversations/<sessionId>.history.jsonl
```

The `<sessionId>.json` file contains a complete snapshot of the session, including metadata and conversation history, written on save. The `<sessionId>.history.jsonl` file is an append-only log of chat messages that provides incremental durability between snapshots. Both files belong to the session and are managed together.

This means that:

- You can open the same session later from the CoCo CLI with `/resume`, or from a different ACP client.
- When an ACP client requests `loadSession`, CoCo replays the full conversation history as ACP `SessionUpdate` notifications so the editor can repopulate its UI.
- The `/wipe-session` command removes the full session trace, including any messages added from ACP clients.

## Session configuration options

When a session is created or loaded, CoCo reports configuration options that ACP clients render as dropdowns. You can change these options at any time during the session; changes apply to subsequent prompts.

| Option | Values | Description |
| --- | --- | --- |
| `mode` | `standard`, `plan`, `bypass` | Controls tool-approval behavior. `standard` prompts for sensitive actions; `plan` produces a plan before taking action; `bypass` auto-approves all tool calls. |
| `model` | Any model returned by CoCo’s supported-models list | Selects the underlying model for the session. If no model is set, CoCo uses its automatic selection (reported as `auto`). |

Expand

Show lessSee more

Note

The `bypass` option is available only when your administrator has allowed dangerous mode. In managed environments, selecting `bypass` returns an error and the session’s previous mode is retained. See [managed settings](/user-guide/cortex-code/managed-settings).

## Extending the agent with editor tools

ACP clients can expose their own tools to CoCo by passing a `_meta.clientTools` array in the `newSession` or `loadSession` request. CoCo registers each entry as a client tool: when the agent invokes one, CoCo calls back to the editor over the ACP connection, the editor executes the tool locally, and the result is returned to the agent.

A client tool definition contains:

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique tool name. By convention, names should not start with `mcp__`, which is the reserved prefix for MCP tools. |
| `description` | No | Natural-language description shown to the agent. |
| `inputSchema` | No | JSON schema describing the tool’s inputs. Defaults to an empty object schema. |

Expand

Show lessSee more

Client tools are registered per-session and are removed automatically when the session ends or the ACP connection closes. Permissions for client tools follow the active session mode: `bypass` auto-approves them, `standard` and `plan` prompt the user through the editor.

## Streaming updates

While a prompt is in flight, CoCo emits ACP `SessionUpdate` notifications that map to the following events:

| Update | Emitted when |
| --- | --- |
| `agent_message_chunk` | The agent streams response text. |
| `agent_thought_chunk` | The agent streams internal reasoning (for models that support thinking). |
| `tool_call` | The agent invokes a tool. Includes a tool-call identifier, a human-readable title derived from the tool name, a kind, and the raw input. |
| `tool_call_update` | A tool call progresses, completes, or fails. For file edits, the update includes a `diff` content block with the original and new file contents. |
| `plan` | Plan mode generates or updates a list of planned steps. |
| `user_message_chunk` | A prior user message is replayed during `loadSession`. |

Expand

Show lessSee more

File-edit tools (for example `edit`, `str_replace_editor`, and `write`) emit diff updates so that your editor can render a visual diff inline.

## Canceling a prompt

ACP clients can cancel an in-flight prompt by sending a `cancel` notification for the active session. CoCo aborts any running tool calls, stops streaming, and returns a `cancelled` stop reason. The session itself remains open and can be reused for the next prompt.

## Limitations

- The `listSessions` method is currently exposed as `unstable_listSessions` and may change as the ACP specification evolves.
- CoCo slash commands are not yet exposed to ACP clients as first-class commands; use them by typing them as part of a prompt (for example, `/skill list`).
- ACP does not provide a separate authentication flow. CoCo uses the Snowflake connection configured at launch.

## Troubleshooting

### The editor reports that the agent exited immediately

Run the same command from a terminal:

Copy code

```
cortex acp serve -c <connection_name>
```

If CoCo prints an authentication or connection error, fix the underlying connection before relaunching your editor. CoCo exits before speaking ACP if it can’t initialize the Snowflake connection.

### The agent hangs on startup or produces garbled output

Confirm that no shell startup file (`.bashrc`, `.zshrc`, and so on) or wrapper script writes to stdout. ACP uses stdout as the protocol channel; any stray output breaks the ndjson framing. Redirect diagnostic output to stderr or a log file.

### Tool approvals never appear

Check the session `mode`. In `bypass` mode, tool calls are auto-approved and no prompts are sent. Switch to `standard` or `plan` in your editor’s session settings to restore approvals.

### The model dropdown is empty

The model list is fetched from Snowflake at session creation. An empty list usually indicates that the Snowflake connection is invalid or that the account has no models enabled. Verify with `cortex auth status` and retry.
