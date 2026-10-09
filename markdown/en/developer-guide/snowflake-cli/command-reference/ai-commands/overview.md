# snow ai commands

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The `snow ai` commands launch a coding agent that’s already installed on your machine and route its
model requests through [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway). The
gateway endpoint and the credential both come from the Snowflake CLI connection you select.

The following commands are available:

- [snow ai claude](/developer-guide/snowflake-cli/command-reference/ai-commands/claude)
- [snow ai opencode](/developer-guide/snowflake-cli/command-reference/ai-commands/opencode)

While the feature is in preview, the `ai` command group doesn’t appear in `snow --help`. Run
`snow ai --help` to see it.

## How `snow ai` works

When you run a `snow ai` command, Snowflake CLI does the following:

1. **Finds the agent executable.** `snow ai claude` runs the first executable named `claude` on your
   `PATH`, and `snow ai opencode` runs the first one named `opencode`. If OpenCode isn’t on your `PATH`,
   Snowflake CLI also looks for `~/.opencode/bin/opencode`. Snowflake CLI doesn’t check the executable’s version,
   signature, or origin. Run `which claude` or `which opencode` to see which one will run.
2. **Resolves and authenticates the connection** using the same rules as any other Snowflake CLI command:
   the `--connection` option, your `config.toml` and `connections.toml` files, and environment
   variables.
3. **Builds the gateway endpoint** from the host of the authenticated connection:
   `https://<account-host>/api/v2/aigateways/SNOWFLAKE/`. For a connection that uses private
   connectivity, `<account-host>` is the connection’s private connectivity host, and the endpoint
   follows the same format.
4. **Starts the agent with process-local settings.** The gateway endpoint, the credential, and the
   agent’s settings are passed in the child process’s environment. Snowflake CLI never edits the agent’s
   configuration files, such as `~/.claude/settings.json` or `opencode.json`, so running `claude` or
   `opencode` directly afterward behaves as it did before.

When the agent exits, the `snow ai` command exits with the same exit code.

## Authentication

The connection’s `authenticator` decides which credential the agent receives. `snow ai` supports these
authenticators:

| Authenticator | Behavior |
| --- | --- |
| `oauth_authorization_code` | Browser-based OAuth sign-in. You sign in when the command starts, and the agent gets new access tokens from a Snowflake CLI helper while it runs. Refresh tokens stay in the connector’s credential cache and are never passed to the agent. See [Use OAuth with credential renewal](#label-snowcli-ai-oauth). |
| `oauth` | An OAuth access token that another application supplies through `token` or `token_file_path`. The token is copied once at launch. When it expires, renew it with the application that issued it and relaunch the agent. |
| `PROGRAMMATIC_ACCESS_TOKEN` | A [programmatic access token](/user-guide/programmatic-access-tokens) from `token` or `token_file_path`. The token is copied once at launch and isn’t renewed. |

Expand

Show lessSee more

If both `token_file_path` and `token` are set, `token_file_path` is used. An empty or unreadable token
file stops the command instead of falling back to `token`.

Other authenticators, including key pair, OAuth client credentials, and workload identity federation,
aren’t supported. `snow ai` stops before launching the agent if the connection uses one of them.

### Use OAuth with credential renewal

To have the agent’s credential renew while it runs, use a named connection like this one:

Copy code

```
[ai-gateway-oauth]
account = "<org-account>"
user = "<your_user>"
role = "<gateway_role>"
authenticator = "oauth_authorization_code"
client_store_temporary_credential = true
oauth_enable_refresh_tokens = true
```

Then launch the agent with that connection:

Copy code

```
snow ai claude -c ai-gateway-oauth
```

Credential renewal has these requirements. `snow ai` checks them and stops before launching the agent
if any aren’t met:

- A named connection that sets `user` and `role` explicitly. Temporary connections (`-x`) aren’t
  supported.
- `client_store_temporary_credential` and `oauth_enable_refresh_tokens` set to `true`.
- The default Snowflake OAuth client. Custom OAuth clients, endpoints, and scopes, external identity
  providers, and secondary roles aren’t supported.
- Snowflake CLI installed as a Python package on macOS or Linux, with Snowflake Connector for Python 4.7.5
  or later. Windows and the standalone Snowflake CLI executables aren’t supported.
- No explicit transport settings on the connection, such as `port`, `protocol`, proxy, TLS, timeout,
  or custom redirect URI settings.

Each time the agent asks for a token, the helper signs in again through the connector, which adds the
latency of a connection. The helper never opens a browser. If your refresh token has expired, the
agent’s request fails, and you need to relaunch with `snow ai` to sign in again.

## Security considerations

The agent receives a live account credential. The access token or PAT isn’t limited to the gateway: it
authenticates to your account’s REST APIs with the connection’s role, and every command the agent runs
inherits it. To limit exposure:

- Use a role with only the privileges the agent needs, such as USAGE on the gateway and access to the
  models you allow.
- Use OAuth rather than a PAT where you can. An OAuth access token expires within minutes, while a PAT
  stays valid until it expires or is revoked. If you do use a PAT, restrict it to a least-privilege
  role, give it a short expiry, and require a [network policy](/user-guide/network-policies). See
  [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).
- Don’t print the agent’s resolved configuration. Agent commands that display their effective
  configuration can show the credential that `snow ai` passed in.

`snow ai` also adds `X-Snowflake-Application: snowflake-cli` and a `snow-agent-name` header to each
request to identify the launcher and agent. Any client can send these headers, so don’t base access or spending decisions on them.

## Environment variables that block a launch

Some environment variables make an agent use a different credential or endpoint from the ones
`snow ai` passes in. When one of these is set in your shell, `snow ai` refuses to launch and names the
variable:

- `snow ai claude`: `ANTHROPIC_API_KEY`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`
- `snow ai opencode`: `SNOWFLAKE_CORTEX_TOKEN`, `SNOWFLAKE_CORTEX_PAT`

Unset the variable, or run the command in a shell where it isn’t set. Other environment variables are
inherited by the agent unchanged.

## Passing arguments to the agent

Everything after `--agent-args` is passed to the agent unchanged, in the agent’s own argument format.
Snowflake CLI stops parsing at `--agent-args`, so a flag that both tools define, such as `--debug`,
`--verbose`, or `--port`, reaches the agent instead of Snowflake CLI:

Copy code

```
snow ai claude --agent-args -p 'explain this repo' --verbose
snow ai opencode --agent-args serve --port 3000
```

Snowflake CLI options, such as `--connection`, go before `--agent-args`. If you pass an agent flag without
`--agent-args`, Snowflake CLI rejects it and shows how to pass it to the agent.

## Choosing a model

The gateway takes model names without a vendor prefix, such as `claude-sonnet-4-5` or
`openai-gpt-5.4`, and the model has to match the API the agent uses:

- Claude Code uses the Messages API, which serves Claude models only.
- OpenCode uses the Chat Completions API, which serves every model except Claude models.

For the models available to your account, see
[Model availability](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-complete-llm-model-availability).
