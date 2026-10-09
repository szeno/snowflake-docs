# snow ai opencode

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Launches OpenCode with its Snowflake provider pointed at Cortex AI Gateway, using the endpoint and
credential from the selected connection.

## Syntax

Copy code

```
snow ai opencode
  --gateway-name <gateway_name>
  <connection_options>
  --agent-args <opencode_arguments>
```

## Arguments

None

## Options

`--gateway-name TEXT`
:   Name of the AI Gateway to route requests through. The host always comes from the connection. Default:
    `SNOWFLAKE`.

`--agent-args`
:   Passes everything after it to `opencode` unchanged. Must be the last Snowflake CLI option on the command
    line. See
    [Passing arguments to the agent](/developer-guide/snowflake-cli/command-reference/ai-commands/overview#label-snowcli-ai-passing-arguments).

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

- OpenCode must already be installed. See
  [How `snow ai` works](/developer-guide/snowflake-cli/command-reference/ai-commands/overview#label-snowcli-ai-how-it-works).
- `snow ai opencode` passes its configuration in the `OPENCODE_CONFIG_CONTENT` environment variable,
  which OpenCode merges on top of your global and project configuration for that process only. The
  configuration it passes is equivalent to:

  Copy code

  ```
  {
    "$schema": "https://opencode.ai/config.json",
    "model": "snowflake-cortex/openai-gpt-5.4",
    "small_model": "snowflake-cortex/openai-gpt-5.4",
    "provider": {
      "snowflake-cortex": {
        "options": {
          "baseURL": "https://<account-host>/api/v2/aigateways/<gateway-name>/v1",
          "account": "<account-host>",
          "apiKey": "<credential from the connection>",
          "headers": {
            "X-Snowflake-Application": "snowflake-cli",
            "snow-agent-name": "opencode"
          }
        },
        "models": {
          "openai-gpt-5.4": {
            "options": { "reasoningEffort": "none" }
          }
        }
      }
    }
  }
  ```

  Where:

  - `account` is the gateway host. OpenCode’s `snowflake-cortex` provider needs it to apply its
    Snowflake request compatibility handling.
  - `small_model` is set to the same model as `model`, so OpenCode’s lightweight requests, such as
    session titles, also use a model the gateway serves.

  Your organization’s managed OpenCode settings are applied after `OPENCODE_CONFIG_CONTENT` and might override these values.
- OpenCode uses the Chat Completions API, which doesn’t serve Claude models. The default model is
  `openai-gpt-5.4`. To choose another model, pass OpenCode’s own `-m` option with the provider name,
  for example `--agent-args -m snowflake-cortex/<model>`.
- When the connection uses `authenticator = oauth_authorization_code`, `apiKey` is set to a placeholder
  value instead of a token, and the configuration also loads a plugin bundled with Snowflake CLI. Before each
  model request, the plugin calls the Snowflake CLI token helper and sets the `Authorization` header to a
  fresh access token. In this mode, you can’t pass OpenCode’s `--pure` or `--attach` options, or set
  `OPENCODE_PURE`, because they would skip the plugin.
- `snow ai opencode` doesn’t add any telemetry plugin. Any OpenCode plugins or exporter settings in your
  own configuration still apply.
- `snow ai opencode` refuses to launch when `SNOWFLAKE_CORTEX_TOKEN` or `SNOWFLAKE_CORTEX_PAT` is set.

## Examples

- Start an interactive session with the default connection:

  Copy code

  ```
  snow ai opencode
  ```
- Use a specific connection:

  Copy code

  ```
  snow ai opencode -c ai-gateway-oauth
  ```
- Run a single task non-interactively:

  Copy code

  ```
  snow ai opencode --agent-args run 'fix the failing test'
  ```
- Choose the model:

  Copy code

  ```
  snow ai opencode --agent-args -m snowflake-cortex/openai-gpt-4.1
  ```
- Start the OpenCode server:

  Copy code

  ```
  snow ai opencode --agent-args serve --port 3000
  ```
