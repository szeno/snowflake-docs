# CoCo CLI reference

Command line reference for CoCo CLI. CoCo CLI operates in two modes:

- **Interactive mode** (default): Start a persistent session where you type prompts and slash commands at an
  interactive prompt. CoCo maintains conversation context across multiple exchanges.
- **Batch mode**: Pass a single prompt on the command line or from a file. CoCo processes it and exits
  without starting an interactive session.

The sections below cover the startup command, CLI options shared by both modes, subcommands you run
*before* entering a session, interactive-mode commands you use *within* a session, and batch-mode usage.

## Starting CoCo

| Command | Description |
| --- | --- |
| `cortex` | Start in current directory |
| `cortex -c production` | Start with specific connection |
| `cortex -w /path/to/project` | Start in specific directory |
| `cortex -w /new/project -c myconn` | Combine workdir and connection |
| `cortex --continue` | Continue last session |
| `cortex --resume <session_id>` | Resume specific session |
| `cortex --cloud` | Run tools in a managed container |

Expand

Show lessSee more

## CLI options

| Option | Description |
| --- | --- |
| `-c, --connection <name>` | Use specific Snowflake connection |
| `-w, --workdir <path>` | Set working directory for file operations |
| `-m, --model <model_name>` | Specify AI model to use |
| `--mode <standard|code>` | Agent tool mode; `code` uses a lean coding tool set (see [Code mode](/user-guide/cortex-code/code-mode)) |
| `--plan` | Plan mode: require approval before all actions |
| `--auto-accept-plans` | Auto-accept plan mode requests and confirmations without prompting |
| `--bypass`, `--dangerously-allow-all-tool-calls` | Enable bypass mode, automatically approving all tool calls |
| `--allowed-tools <tools>` | Tools that execute without prompting for permission (for example, `"Bash(git *)"`) |
| `--disallowed-tools <tools>` | Tools that are removed from the model’s context and can’t be used |
| `--continue` | Resume most recent conversation |
| `-r, --resume [<session_id>]` | Resume specific session by ID, or `last` for the most recent session |
| `-p, --print "<prompt>"` | Pass specified prompt, print response, and exit |
| `--output-format stream-json` | JSON output (for scripting) |
| `--effort <level>` | Thinking effort level: `minimal`, `low`, `medium`, `high`, or `max` |
| `--max-turns <n>` | Maximum number of agentic turns per conversation round |
| `--private` | Don’t save this session to history (disables conversation persistence and server-side logging) |
| `--cloud [<workspace>]` | Run tools in a Snowflake-managed container |
| `--no-workspace` | With `--cloud`, use an ephemeral workspace |
| `--github <secret>` | With `--cloud`, allow authenticated GitHub access |
| `-V, --version` | Show installed version |
| `--help` | Show CLI help |

Expand

Show lessSee more

Connections must be defined in `~/.snowflake/connections.toml`. See [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) for connection setup. Session IDs are shown at startup and at exit, and they are stored in `~/.snowflake/cortex/conversations/`.

`--bypass` and `--dangerously-allow-all-tool-calls` are aliases of the same option. Omit the value of `-r, --resume` to open the
resume picker instead of naming a session. Use `--allowed-tools` to pre-approve specific tools (for example, `"Bash(git *)"` to
approve all git commands); use `--disallowed-tools` to prevent specific tools from being offered to the model at all.

Warning

Bypass mode approves every tool call without prompting you first. Use it only when you trust every action the agent might take.

See [CoCo CLI cloud sandbox](/user-guide/cortex-code/cloud-sandbox) for details on `--cloud`, `--no-workspace`, and `--github`. `--cloud` optionally takes a workspace name (`DATABASE.SCHEMA.NAME`) to mount; `--github` takes the name of a Snowflake secret (`DATABASE.SCHEMA.SECRET`) holding a GitHub personal access token, and implies `--cloud`.

### Examples

Start with working directory:

Copy code

```
cortex -w /path/to/project
```

Resume last session with specific connection:

Copy code

```
cortex --continue -c production
```

One-off prompt (JSON output):

Copy code

```
cortex -p "List all Python files" --output-format stream-json
```

## Commands

These subcommands run from your shell *before* or *instead of* starting an interactive session.
They are distinct from the slash commands (like `/mcp`) that you type inside an interactive session.

### `update`

Update CoCo CLI to the latest version.

| Command | Description |
| --- | --- |
| `cortex update` | Update to latest version |
| `cortex --version` | Verify after update |

Expand

Show lessSee more

### `exec`

Use `exec` to run CoCo CLI non-interactively, which is useful in continuous integration and continuous delivery (CI/CD)
pipelines. Plan mode is always disabled and interactive prompts are automatically rejected.

| Command | Description |
| --- | --- |
| `cortex exec "<prompt>"` | Run a prompt and exit |
| `cortex exec --file <file>` | Read the prompt from a file |
| `cortex exec --file -` | Read the prompt from standard input |

Expand

Show lessSee more

### `mcp`

Manage Model Context Protocol (MCP) server connections from the command line.

| Command | Description |
| --- | --- |
| `cortex mcp list` | List configured servers |
| `cortex mcp add <name> <command_or_url> [args...]` | Add new server |
| `cortex mcp get <name>` | Show details for a configured server |
| `cortex mcp remove <name>` | Remove server |
| `cortex mcp reconnect [name]` | Reconnect one server, or all servers if you don’t provide a name |
| `cortex mcp start` | Start configured servers |

Expand

Show lessSee more

The `add` subcommand accepts the following options:

| Option | Description |
| --- | --- |
| `-t, --transport <type>` | Transport to use: `stdio`, `sse`, or `http`. Default: `stdio`. |
| `-e, --env <KEY=value>` | Set an environment variable. Repeat the option for multiple variables. |
| `-H, --header "<name>: <value>"` | Set an HTTP header. Repeat the option for multiple headers. |
| `--timeout <milliseconds>` | Connection timeout. |

Expand

Show lessSee more

See [MCP (Model Context Protocol)](extensibility#extensibility-mcp) for details.

## Interactive mode

Interactive mode is the default when you run `cortex` without `-p` or `exec`. CoCo opens a persistent
session where you type natural-language prompts and slash commands at the `>` prompt. The agent processes
your request, potentially using multiple tools, and then returns to the prompt for your next input.

Keyboard shortcuts and slash commands described in this section work only in interactive mode. They
don’t apply in batch mode or inside a file passed to `cortex exec --file`.

### Keyboard shortcuts

These shortcuts are active at the interactive prompt and while the agent is working:

| Shortcut | Action |
| --- | --- |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+C Ctrl+C` | Exit CoCo CLI |
| `Ctrl+L` | Clear terminal screen (keeps conversation) |
| `Up/Down arrows` | Navigate command history |
| `Tab` | Command completion |

Expand

Show lessSee more

### Slash commands

Slash commands are special commands you type at the interactive prompt. They start with `/` and
control CoCo’s behavior without being sent to the AI model as a prompt. Slash commands work only
in interactive mode.

#### Session management

| Command | Description |
| --- | --- |
| `/help` | Show interactive help |
| `/clear`, `/cls` | Clear the screen |
| `/new` | Start a new session |
| `/rename <title>` | Rename current session |
| `/quit`, `/exit` | Exit CoCo CLI |
| `/resume`, `/r`, `/sessions` | List and resume sessions |
| `/rewind` | Go back *n* steps in conversation or pick interactively |
| `/fork` | Fork current session into a new session |

Expand

Show lessSee more

#### Model and mode

| Command | Description |
| --- | --- |
| `/model` | Show/select AI model |
| `/plan` | Enable plan mode |
| `/plan-off` | Disable plan mode |
| `/bypass` | Enable bypass mode (auto-approve all including tool calls) |
| `/bypass-off` | Disable bypass mode |
| `/status` | Show current configuration |

Expand

Show lessSee more

#### Snowflake and data

| Command | Description |
| --- | --- |
| `/sql <query>` | Execute SQL query |
| `/sql <query> --limit <n>` | Limit displayed rows |
| `/table [<file>]`, `/csv` | Open table viewer |
| `/connections`, `/conn` | Manage Snowflake connections |

Expand

Show lessSee more

#### Development tools

| Command | Description |
| --- | --- |
| `/sh`, `! <command>` | Execute shell command |
| `/diff`, `/changes`, `/review` | Review git changes |
| `/worktree` | Manage git worktrees |
| `/fdbt` | Fast dbt project analysis |
| `/lineage` | dbt lineage visualization |

Expand

Show lessSee more

#### Configuration

| Command | Description |
| --- | --- |
| `/settings` | View/modify settings |
| `/theme` | Select color theme |
| `/sandbox` | Manage sandbox settings |
| `/workspace` | Browse and switch the mounted workspace (cloud only) |
| `/add-dir <path>` | Add working directory |

Expand

Show lessSee more

#### Extensibility

| Command | Description |
| --- | --- |
| `/skill`, `/skills` | Manage skills |
| `/skill new`, `/skill create` | Create a new skill |
| `/mcp` | MCP server status |
| `/hooks` | View hooks configuration |
| `/commands`, `/cmds` | Manage custom commands |
| `/agents` | View subagents |

Expand

Show lessSee more

#### Utilities

| Command | Description |
| --- | --- |
| `/bashes`, `/shells`, `/tasks` | View and manage background shells |
| `/feedback` | Provide session feedback, saved locally as a .tgz file |
| `/update` | Update CoCo |

Expand

Show lessSee more

### Session storage

| Command | Description |
| --- | --- |
| `~/.snowflake/cortex/conversations/` | Session files |
| `~/.snowflake/cortex/settings.json` | General settings |
| `~/.snowflake/cortex/permissions.json` | Permission preferences |

Expand

Show lessSee more

See [CoCo CLI Settings](/user-guide/cortex-code/settings) for configuration details.

### Command details

#### `/sql`: Execute SQL query

Basic query:

```
/sql SELECT * FROM users
```

With row limit:

```
/sql SELECT * FROM large_table --limit 1000
```

Multi-line queries (use Ctrl+J for newlines):

```
/sql SELECT
  customer_id,
  SUM(amount) as total
FROM orders
GROUP BY customer_id
```

Results open automatically in the table viewer (Ctrl+T).

#### `/worktree`: Git worktrees

Git worktrees let you work on multiple branches simultaneously without switching back and forth.
CoCo creates worktrees under your project directory by default (in a `.worktrees/` subdirectory
or alongside your main checkout, depending on your git configuration).

| Command | Description |
| --- | --- |
| `/worktree create feature-branch` | Create new worktree |
| `/worktree list` | List all worktrees |
| `/worktree switch feature-branch` | Switch to worktree |
| `/worktree delete feature-branch` | Delete worktree |

Expand

Show lessSee more

#### `/sandbox`: Sandbox control

CoCo’s sandbox isolates shell commands in a restricted environment so they can’t modify files
outside your working directory or access sensitive system resources. This is a CoCo-specific
security feature. The container sandbox uses Docker, while the runtime sandbox uses OS-level
restrictions (macOS sandbox or Linux namespaces).

| Command | Description |
| --- | --- |
| `/sandbox` | Interactive selector |
| `/sandbox on` | Enable container sandbox |
| `/sandbox off` | Disable container sandbox |
| `/sandbox status` | Show sandbox status |
| `/sandbox runtime on` | Enable OS sandbox |
| `/sandbox runtime off` | Disable OS sandbox |
| `/sandbox mode auto` | Auto-allow sandboxed commands |
| `/sandbox mode regular` | Prompt for all commands |

Expand

Show lessSee more

To run tools in a Snowflake-managed container instead of on your machine, start CoCo CLI with `--cloud`. See [CoCo CLI cloud sandbox](/user-guide/cortex-code/cloud-sandbox).

#### `/mcp`: MCP servers

`/mcp` takes no subcommands. It opens an interactive viewer that lists every configured server and lets you start, stop,
reconnect, authenticate, edit, and remove servers from within the session. For non-interactive management, use the
`cortex mcp` subcommands described in [mcp](/user-guide/cortex-code/cli-reference#label-coco-cli-mcp-subcommands).

## Batch mode

Batch mode runs a single prompt without starting an interactive session. CoCo processes the request,
prints the result, and exits. This is useful for scripting, CI/CD pipelines, and one-off questions
where you don’t need a back-and-forth conversation.

Use `-p` for inline prompts or `cortex exec` for prompts from files or stdin. Slash commands don’t
work in batch mode because there’s no interactive prompt.

| Command | Description |
| --- | --- |
| `cortex -p "<prompt>"` | Run single prompt and exit |
| `cortex exec --file request.txt` | Read prompt from file |
| `cortex --output-format stream-json -p "<prompt>"` | JSON output |
| `cortex -c prod --workdir /app -p "..."` | Control context |

Expand

Show lessSee more

## Exit codes

CoCo CLI returns `0` on success and a non-zero value on failure. It doesn’t guarantee a stable mapping of specific
non-zero codes to error categories, so scripts should test only for zero versus non-zero. Error details are written to
standard error.

## Configuration and setup

### Updating CoCo CLI

CoCo CLI updates itself when a new version is available. You can also manually update to the latest version
by issuing `cortex update`. Issue `cortex update <version>` to install the specified version.

To disable automatic updates, edit `~/.snowflake/cortex/settings.json` and add `"autoUpdate": false`.

### Manually adding a connection

To manually create or edit the `~/.snowflake/connections.toml` file to define your connection, follow these steps:

1. Create the `~/.snowflake/connections.toml` file if it doesn’t already exist.

   Copy code

   ```
   mkdir -p ~/.snowflake
   touch ~/.snowflake/connections.toml
   ```
2. Use the `chmod` command to set its permissions so that only you can read and write it.

   Copy code

   ```
   chmod 600 ~/.snowflake/connections.toml
   ```
3. Open the file in a text editor (here, `nano`).

   Copy code

   ```
   nano ~/.snowflake/connections.toml
   ```
4. Add lines like the following to define a connection. Enter the name of the connection in place of `myaccount` and
   replace the placeholder values with your Snowflake account details. Use browser-based SSO (external browser
   authentication) or PAT (programmatic access token). You can obtain a PAT from Snowsight (see
   [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens)). Include only the `authenticator` value or `password` value,
   depending on the authentication method you choose.

   Copy code

   ```
   [myaccount]
   account       = "<ACCOUNT>"
   user          = "<USERNAME>"
   authenticator = "externalbrowser" # For browser-based SSO; omit for PAT
   password      = "<PAT>"           # For PAT authentication; omit for SSO
   warehouse     = "<WAREHOUSE>"
   role          = "<ROLE>"
   database      = "<DATABASE>"
   schema        = "<SCHEMA>"
   ```
5. Save and close the file.

### Setting up shell completions

To give your shell the ability to auto-complete CoCo CLI commands and options, use one of the following methods.

Tip

If you’re not sure which shell you’re using, issue `echo $(basename $SHELL)` in your terminal. The name printed is the default
shell for your account, and may not be accurate if you have started a different shell manually.

The quickest way is to let CoCo CLI install the completion script for you. Issue the following command to install for your
current shell, or add `--all` to install for every supported shell:

Copy code

```
cortex completion install
```

To install for a specific shell, pass `--shell`:

Copy code

```
cortex completion install --shell zsh
```

Alternatively, generate the script yourself and write it to the location your shell expects:

| Shell | Command |
| --- | --- |
| `bash` | `cortex completion generate --shell bash > ~/.bash_completion.d/cortex` |
| `zsh` | `cortex completion generate --shell zsh > ~/.zsh/completions/_cortex` |
| `fish` | `cortex completion generate --shell fish > ~/.config/fish/completions/cortex.fish` |

Expand

Show lessSee more

Restart your shell with `exec $SHELL` after you install or generate the completion script.

### Directory structure

CoCo CLI stores its configuration and state under your home directory as follows. It creates files and directories as
they are needed, so not all of them are present on a new installation.

```
~/.snowflake/cortex/
   ├── settings.json          # Main configuration (includes hook configuration)
   ├── mcp.json               # MCP server configs
   ├── hooks.json             # Global hook configuration
   ├── conversations/         # Session history
   ├── skills/                # Global skills
   ├── commands/              # Custom commands
   ├── profiles/              # Team profiles
   └── cache/                 # Temporary cache
```

## Troubleshooting

Following are common error messages you may encounter during installation and setup.

### Command not found

Make sure that the installation directory `~/.local/bin` is included in your `PATH` environment variable.
For example, if you are using `bash`, issue the following commands:

Copy code

```
export PATH="~/.local/bin:$PATH"
echo 'export PATH="~/.local/bin:$PATH"' >> ~/.bashrc
```

### Permission denied

Make sure that the `cortex` executable has execute permissions. Issue the following command:

Copy code

```
chmod +x ~/.local/bin/cortex
```

### Connection errors

Make sure that the connection file `~/.snowflake/connections.toml` exists and contains valid connection details.

Copy code

```
cat ~/.snowflake/connections.toml
```

Try invoking the `cortex` command with a connection explicitly specified using the `-c` option. For example:

Copy code

```
cortex -c myaccount
```

## See also

[CoCo CLI](/user-guide/cortex-code/cortex-code-cli)
:   Installation, setup, and first prompts

[CoCo CLI Settings](/user-guide/cortex-code/settings)
:   Configuration file reference

[CoCo CLI workflow examples](/user-guide/cortex-code/workflows)
:   Capabilities and workflow examples
