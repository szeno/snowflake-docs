# snow ai claude

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Launches Claude Code with its model requests routed through Cortex AI Gateway, using the endpoint and
credential from the selected connection.

## Syntax

Copy code

```
snow ai claude
  --gateway-name <gateway_name>
  <connection_options>
  --agent-args <claude_arguments>
```

## Arguments

None

## Options

`--gateway-name TEXT`
:   Name of the AI Gateway to route requests through. The host always comes from the connection. Default:
    `SNOWFLAKE`.

`--agent-args`
:   Passes everything after it to `claude` unchanged. Must be the last Snowflake CLI option on the command line.
    See [Passing arguments to the agent](/developer-guide/snowflake-cli/command-reference/ai-commands/overview#label-snowcli-ai-passing-arguments).

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your `config.toml` file. Default: `default`.

`<connection_options>`
:   The standard Snowflake CLI connection options, such as `--account`, `--user`, `--role`, `--authenticator`,
    `--token`, and `--token-file-path`, which override the values in the connection. See
    [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). The connection must use a
    supported authenticator. See
    [Authentication](/developer-guide/snowflake-cli/command-reference/ai-commands/overview#label-snowcli-ai-authentication).

`--help`
:   Displays the help text for this command.

## Usage notes

- Claude Code must already be installed. See
  [How `snow ai` works](/developer-guide/snowflake-cli/command-reference/ai-commands/overview#label-snowcli-ai-how-it-works).
- Claude Code uses the Messages API, so only Claude models work. To choose one, pass Claude Code’s own
  `--model` option, for example `--agent-args --model claude-sonnet-4-5`.
- `snow ai claude` passes the following to the `claude` process:

  | Setting | Value |
  | --- | --- |
  | `ANTHROPIC_BASE_URL` | The gateway endpoint, without `/v1`. Claude Code appends `/v1/messages` itself. |
  | `ANTHROPIC_AUTH_TOKEN` | The PAT or OAuth access token from the connection. Not set when the connection uses credential renewal; see the next note. |
  | `ANTHROPIC_CUSTOM_HEADERS` | Adds `X-Snowflake-Application: snowflake-cli` and `snow-agent-name: claude`. Existing values in this variable take precedence. |
  | `CLAUDE_CODE_ENABLE_TELEMETRY`, `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`, `CLAUDE_CODE_PROPAGATE_TRACEPARENT`, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Each set to `1`, but only when Snowflake CLI telemetry is enabled for the connection, which is the default, and only if you haven’t set the variable yourself. |
  | `OTEL_TRACES_EXPORTER` | `console`, under the same conditions. Claude Code needs a trace exporter to send `traceparent` headers to the gateway. No OTLP endpoint is configured. |

  Expand

  Show lessSee more
- When the connection uses `authenticator = oauth_authorization_code`, `snow ai claude` doesn’t pass a
  fixed token. It removes `ANTHROPIC_AUTH_TOKEN` and `CLAUDE_CODE_OAUTH_TOKEN` from the agent’s
  environment and adds a `--settings` argument with inline JSON that sets `apiKeyHelper` to the
  Snowflake CLI token helper and pins `env.ANTHROPIC_BASE_URL` to the gateway. Claude Code calls the helper
  for a fresh token as needed. In this mode:

  - You can’t also pass `--settings` or `--safe-mode` in `--agent-args`, or set
    `CLAUDE_CODE_SAFE_MODE=1`.
  - Managed settings that your organization deploys take precedence over `--settings`. If they set
    `apiKeyHelper` or `env.ANTHROPIC_BASE_URL`, they replace what `snow ai claude` configures.
- Claude Code can send the credential in both the `Authorization` and `X-Api-Key` headers. Treat both
  as secrets in any request capture or logs.
- `snow ai claude` refuses to launch when `ANTHROPIC_API_KEY`, `CLAUDE_CODE_USE_BEDROCK`, or
  `CLAUDE_CODE_USE_VERTEX` is set.

## Examples

- Start an interactive session with the default connection:

  Copy code

  ```
  snow ai claude
  ```
- Use a specific connection:

  Copy code

  ```
  snow ai claude -c ai-gateway-oauth
  ```
- Run a single prompt non-interactively, with verbose output:

  Copy code

  ```
  snow ai claude --agent-args -p 'explain this repo' --verbose
  ```
- Choose the model:

  Copy code

  ```
  snow ai claude --agent-args --model claude-opus-4-5
  ```
