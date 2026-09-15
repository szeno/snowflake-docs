# Security

This page is a security overview for CoCo Desktop. It explains the trust boundaries the
product enforces, the recommended baseline for everyday use, and the limitations you should know
about before granting the agent broader permissions.

For the per-feature controls, see:

- [Permission modes](/user-guide/cortex-code/cortex-code-desktop/permission-modes)
- [Managed settings](/user-guide/cortex-code/cortex-code-desktop/managed-settings)
- [Plugins](/user-guide/cortex-code/cortex-code-desktop/plugins)
- [Skills](/user-guide/cortex-code/cortex-code-desktop/skills)
- [MCP support](/user-guide/cortex-code/cortex-code-desktop/mcp-support)
- [Hooks](/user-guide/cortex-code/cortex-code-desktop/hooks)
- [Subagents](/user-guide/cortex-code/cortex-code-desktop/agents)
- [Agentic Browser](/user-guide/cortex-code/cortex-code-desktop/agentic-browser)
- [Scheduled tasks](/user-guide/cortex-code/cortex-code-desktop/scheduled-tasks)
- [Onboarding and authentication](/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication)

## The trust model

CoCo Desktop enforces several distinct trust boundaries. Each one has its own approval flow
and its own scope; together they decide what the agent and any extensions can do on your behalf.

| Boundary | What it gates | Where it lives |
| --- | --- | --- |
| **Workspace** | Whether the agent runs in this folder at all. Until you trust the workspace, the chat widget is replaced by a *Trust Workspace* gate and the agent’s hooks, MCP servers, subagents, project skills, prompt files, `AGENTS.md` instructions, and file access stay disabled. Adding a workspace to Agent Manager auto-trusts it. | Workspace Trust dialog. |
| **Permission mode** | Whether the agent stops to ask before running tools, edits, and SQL. | Default Approvals or Bypass Approvals; switch from the chat input. See [Permission modes](/user-guide/cortex-code/cortex-code-desktop/permission-modes). |
| **Plugins, skills, MCP servers** | Whether a given source (GitHub repo, Snowflake stage, local folder, MCP URL) is registered and active. | One-time consent when you add the source. Sources are not cryptographically signed. MCP servers re-prompt when their config changes; skills, hooks, and local plugins do not. |
| **Network domains** | Whether the agent can reach a given URL or host. | Per-URL approvals. |
| **Snowflake credentials** | Where authentication material is stored and which processes can read it. | OS-native credential store. |

Expand

Show lessSee more

Warning

The agent treats user-supplied content as instructions and acts on it: files
in trusted workspaces, prompts, fetched URLs, and outputs from MCP servers,
plugins, and subagents. Defending against prompt injection in the inputs you
supply is your responsibility. Vet untrusted sources before letting the agent
read them, and prefer Plan Mode or Default Approvals when working with
unfamiliar content. For more on protecting against prompt injection, see
Cortex AI Guardrails.

## Recommended security baseline

Apply these defaults for everyday use:

- **Use Default Approvals.** The agent prompts you before each tool call. **Bypass Approvals**
  auto-approves every tool call; reserve it for isolated environments.
- **Use Plan Mode for unfamiliar prompts.** Plan Mode is read-only and lets you confirm the
  approach before any side effects. See
  [Agent mode and Plan mode](/user-guide/cortex-code/cortex-code-desktop/agent-mode-and-plan-mode).
- **Review file edits before accepting them.** Tighten the auto-approve glob list for sensitive
  files in your repo (`package.json`, `.env`, secrets, build scripts).
- **Scope tool approvals to sessions.** Pick “Allow once” or “Allow for session” rather than
  “Always allow” when you are not sure.
- **Vet plugins, skills, and MCP servers before you trust them.** Read the manifest, the skills
  it bundles, and the MCP servers and hooks it registers. Pin sources to specific commits or
  stage paths whenever you can.
- **Apply auto-updates promptly.** See [Auto-update](#auto-update) for why this matters and
  how stale installs are handled.
- **Don’t install unnecessary extensions.** Extensions come from third-party developers and
  contain code that runs with the same privileges as CoCo Desktop.

### File permissions

If you have a `connections.toml` file, restrict it and the agent’s data directory to your
user only and add it to `.gitignore`:

Copy code

```
[ -f ~/.snowflake/connections.toml ] && chmod 600 ~/.snowflake/connections.toml
chmod 700 ~/.snowflake/cortex
chmod 700 ~/.snowflake/cortex/conversations
echo "~/.snowflake/connections.toml" >> ~/.gitignore
```

### Credentials

We recommend using `authenticator = "oauth_authorization_code"` as the default authentication method to avoid plaintext credential storage.
See [Onboarding and authentication](/user-guide/cortex-code/cortex-code-desktop/onboarding-and-authentication)
for the supported methods.

For MCP servers:

- **Use OAuth where supported.** The token lands in OS-native secret storage and refreshes
  automatically; `mcp.json` never sees it.
- **For static API keys, use `${input:...}` with `password: true`.** The
  desktop prompts you on first run and stores the value encrypted in workspace
  state, not in `mcp.json`:

  Copy code

  ```
  {
    "mcpServers": {
      "my-server": {
        "command": "npx",
        "args": ["-y", "my-mcp-server"],
        "env": { "API_KEY": "${input:api-key}" }
      }
    },
    "inputs": [
      { "id": "api-key", "type": "promptString", "password": true }
    ]
  }
  ```
- **Authorization headers in mcp.json are stored as plaintext on disk.**

### Roles and least privilege

CoCo Desktop runs SQL with whatever role the active connection
specifies. The `role` field in `connections.toml` is optional; if you leave it
out, the session uses your Snowflake user’s *default* role.

CoCo Desktop does not restrict secondary roles on its own.

### Conversation history

CoCo Desktop persists conversations under `~/.snowflake/cortex/conversations/`. They
include any file content, tool output, and SQL the agent saw.

### Workspace restricted mode

Note

Workspace restricted mode is in preview.

Use restricted mode when operating on an untrusted codebase.
When a workspace is untrusted, CoCo Desktop behaves in the following way:

- **Editor view** uses the persisted trusted-folders list. An untrusted folder
  runs in restricted mode: chat is blocked, and workspace-scope hooks, MCP
  servers, subagents, project skills, and prompt files are disabled. Plain editing and the integrated terminal still
  work. The status bar shows “Trusted” or “Restricted Mode”.
- **Agent view** uses the Agent Manager project list. Adding a folder prompts
  the *“Trust this folder?”* confirmation; on confirm the folder is added as
  a trusted Agent view project.
- **Editor view and Agent view trust are linked, but asymmetrically:**
  - Trusting a project in Editor view does *not* automatically add it to Agent
    view. It has to be added in Agent view separately.
  - Adding and trusting a project in Agent view automatically marks it as
    trusted in Editor view.
  - Distrusting a project in Editor view removes it from Agent view.

## Agent code execution

CoCo Desktop is an agentic IDE: with your approval, the agent can run shell commands, edit
files, and execute SQL on your machine and your Snowflake account. This capability is an inherent
property of the product, not a defect, and it stays under controls you own:

- **Tool approvals are on by default.** The agent prompts before consequential tool calls. Bypass Approvals is an explicit, informed opt-in for trusted workflows, not the default state. See [Permission modes](/user-guide/cortex-code/cortex-code-desktop/permission-modes).
- **The agent terminal sandbox is intentionally scoped to Bash**, the highest-risk surface. File edits and SQL execution go through the same approval mechanism when Bypass Approvals is off. Sandbox expansion to more tool surfaces is actively being tracked.

## Prompt injection defenses

The agent treats content it reads as potential instructions, including files in trusted
workspaces, prompts, fetched URLs, and outputs from MCP servers, plugins, and subagents. Cortex
Code Desktop defends against prompt injection in depth:

- **Server-side I/O Guardrails** scan tool outputs, including MCP responses, for known injection patterns using vector similarity.
- **Cortex AI Guardrails** apply centrally at the platform layer to catch indirect injection in tool calls and novel or zero-day patterns beyond signature matching.
- **User approval gates** mean a successful injection still requires human confirmation before a consequential action runs, as long as Bypass Approvals is off.
- **Write-scope protections** gate writes to sensitive paths and locations outside the workspace, blocking persistence-grade injection outcomes.
- **No auto-execution on workspace open.** MCP servers, skills, and hooks don’t run when you open a workspace unless you’ve opted in, which closes the malicious-repository attack path.

Note

Known limitations, actively tracked: web fetch content enters the main context window rather than an isolated one, and coverage of novel injection patterns isn’t complete.

## Extensions

CoCo Desktop ships with [Open VSX](https://open-vsx.org/) as its extension store, but the
catalog you can install from is **curated and vetted by Snowflake**. Rather than exposing the
entire Open VSX marketplace, CoCo Desktop restricts installs to an allowlist of trusted
publishers and extensions that the Snowflake security team has reviewed and scanned. Known
competing or high-risk extensions are explicitly blocked. As a result:

- Only allowlisted extensions appear in the Extensions panel, so not every extension on Open VSX is available.
- Adding a new extension to the catalog requires security review, so an extension you’re looking for may not be available yet. Request it through your Snowflake contact if you need it.

This curation bounds the supply-chain surface to a known, reviewed set rather than the open Open
VSX marketplace. Allowlisted extensions still run with the same privileges as the app, and new
versions of an allowlisted extension are auto-updated.

### Sideloading

The publisher allowlist applies to **all** installs, not just the Extensions panel. Installing a
VSIX file directly is gated by the same allowlist, so an extension whose publisher isn’t on the
approved list is blocked or disabled regardless of how it’s installed. Users can’t browse or
install arbitrary extensions from any store, which keeps the supply chain bounded and known.

## Auto-update

CoCo Desktop checks for updates, downloads them, and prompts you to install. The
auto-update mechanism verifies the update’s signature before applying it. Significantly outdated
installations are required to update.

## Build and release security

For enterprise reviews of the build and release pipeline:

- **Binary signing.** macOS builds are notarized by Apple; Windows builds are signed with DigiCert. The auto-update mechanism verifies signatures before applying an update.
- **Dependency scanning (SCA).** Snyk is configured for the codebase and tracks open-source vulnerabilities against Snowflake’s remediation SLOs.
- **Static analysis (SAST).** Per Snowflake’s continuous-monitoring policy, SAST scanning runs on all pull requests. Findings route to the owning team and must be remediated before merge.
- **Vulnerability management.** The team tracks Electron and VS Code upstream versions against a strict upgrade SLA and patches critical vulnerabilities outside the normal release cadence.

## Drift detection

Once a workspace is trusted, **most config sources reload silently** when their files
change. This includes skills, hooks, and, in some cases, MCP server configurations.

## Sandbox

Note

The agent terminal sandbox is experimental and subject to change.

The agent terminal sandbox wraps every terminal command the agent runs inside an isolated
sandbox process. Enabling it is the recommended extra layer of protection when you want
to limit what shell commands the agent can execute, even in trusted workspaces.

### Enable the sandbox

1. Open **Settings** (gear icon or `Cmd/Ctrl+,`).
2. Search for `chat.agent.sandbox`.
3. Set `chat.agent.sandbox.enabled` to `"on"`.

Or add it directly to your `settings.json`:

Copy code

```
{
  "chat.agent.sandbox.enabled": "on"
}
```

When the sandbox is active, agent-initiated terminal commands are wrapped at the executor
level. Commands you run manually in the integrated terminal are not affected.

### Limitations

- The sandbox applies only to terminal commands the **agent** runs via the Bash tool.
  It does not restrict file edits, SQL execution, or MCP tool calls.
- Sandbox behavior depends on OS-level sandboxing capabilities and may vary between
  macOS, Windows, and Linux.
- Some agent workflows that depend on shell side-effects (for example, installing packages
  that affect the current shell session) may behave differently inside the sandbox.

CoCo Desktop will adopt the VSCode native agent sandbox and agent-tools framework
as those features stabilize upstream. For more information, see
[VSCode agent tools](https://code.visualstudio.com/docs/copilot/agents/agent-tools) and
[VSCode Copilot security](https://code.visualstudio.com/docs/copilot/security).

## Audit logging and observability

Administrators can monitor CoCo Desktop usage with Snowflake AI Observability. Interaction
events are written to the `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` event table. Access to event
content is governed by Snowflake’s observability access controls: content is redacted by default,
and viewing it requires an explicit grant to a designated role.

For what’s captured, queries, and access setup, see
[Observability](/user-guide/cortex-code/observability) and the
[Snowflake AI Observability reference](/user-guide/snowflake-cortex/ai-observability/reference).

## Enterprise policies

Administrators can centrally configure CoCo Desktop with a managed-settings file to enforce
a permission allowlist or denylist, set the default permission mode, disable conversation history,
and show a managed-by-organization banner. For the file location, supported keys, permission
pattern syntax, and examples, see
[Managed settings](/user-guide/cortex-code/cortex-code-desktop/managed-settings).

## Deploying in a managed environment

If your IT or security team needs to review CoCo Desktop before approving it, the following
points usually cover what they ask about:

- **No WSL requirement.** On Windows, the app uses PowerShell by default for shell commands and doesn’t require Windows Subsystem for Linux. See the [FAQ](/user-guide/cortex-code/cortex-code-desktop/faq).
- **Credential storage.** Authentication tokens are stored in OS-native secret storage (Keychain, DPAPI, or libsecret), never in plaintext config. See [Credentials](#credentials).
- **Network access.** The app connects to your Snowflake account using the Snowflake Node.js driver, which handles proxy and TLS the same way other Snowflake clients do. Extensions, plugins, and MCP servers can make their own outbound requests, which you can constrain with per-URL approvals and the managed-settings allowlist.
- **Curated extensions.** The extension store is restricted to an allowlist of trusted publishers, and known competing AI extensions are explicitly blocked. See [Extensions](#extensions).
- **Central control.** Use [managed settings](/user-guide/cortex-code/cortex-code-desktop/managed-settings) to set the default permission mode, restrict tools, disable history, and lock down the dangerous-options UI across your fleet.
