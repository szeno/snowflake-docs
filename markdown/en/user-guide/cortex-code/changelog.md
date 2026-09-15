# Cortex Code changelog

This page documents notable changes to Cortex Code.

## 1.1.78 (September 7, 2026)

### Added

- Skill catalog on by default: The skill catalog is now available to everyone without an experimental flag, so you can browse and install shared skills from the catalog with no extra configuration. To turn it off, set `CORTEX_CODE_EXPERIMENTAL_FEATURES={"enableSkillCatalog":false}`.
- `/restart` command: Added the `/restart` command to relaunch the current session with the same flags. Unlike an in-place reload, a restart picks up a new binary after `cortex update`, along with changed environment variables and startup settings. It’s equivalent to quitting and rerunning `cortex --resume` with the same flags.

### Fixed

- Model preserved on resume: Resuming a session no longer drops the model you chose and falls back to the global default. The CLI now stores the model you selected with `--model` or `/model` in the session and restores it when you resume.
- Steering messages on cancel: A message you type while the agent is busy, and send with double-Enter, is no longer lost or resubmitted after you cancel the turn.
- Interface freeze after background subagents: Fixed a case where the CLI could stay in a responding state and stop accepting input after a background subagent finished or failed.
- Nested skills in `cortex skill add`: `cortex skill add <org>/<repo>` no longer fails with a “No valid skills found” error when a repository’s `SKILL.md` files are nested more than one level deep.

## 1.1.65 (2026-08-11)

### Added

- Data exploration subagent: CoCo CLI now includes a `data-discovery` subagent that can explore your Snowflake databases, schemas, and tables to answer questions about your data. It’s enabled by default for all accounts. To turn it off, set `CORTEX_CODE_EXPERIMENTAL_FEATURES={"dataDiscovery":false}`.
- Managed settings enforcement: Administrators can enforce organization policies through a managed settings file. You can limit the Snowflake accounts and authentication methods that CoCo CLI is allowed to use, and require a minimum CLI version. Use `cortex managed-settings` to inspect the active policy.
- Snowflake authentication for MCP servers: HTTP and SSE MCP servers can now authenticate with a named Snowflake connection. Add a `snowflake_connection` field to the server’s entry in `mcp.json`, or use `cortex mcp add`, and CoCo CLI injects a fresh session token on every request. This gives you zero-configuration access to MCP servers hosted on Snowpark Container Services without a static token.
- Ignore ambient MCP servers: Added the `--only-explicit-mcp-servers` flag so a session loads only the MCP servers you pass in, for example with `--mcp-config`, and skips the servers configured in `mcp.json` and `~/.claude.json`.

### Changed

- `/clear` resets your conversation: `/clear` now starts a new conversation and clears the context instead of only clearing the screen. To clear just the screen, use the new `/cls` command or `Ctrl+L`. Your previous session is still available through `/resume`.
- Automatic VM sandbox management: When you use the VM sandbox, CoCo CLI now installs and maintains a version-matched sandbox for you. The `cortex update --with-vm-sandbox` flag has been removed because it’s no longer needed.

### Fixed

- Symlink handling in file permission checks: File write and edit permission checks now resolve symbolic links before deciding whether a path is inside your workspace. Previously a symlink inside the workspace could point outside it and slip past the sandbox boundary.
- Typing lag: Fixed occasional input lag while typing in the CLI inside a Git repository, caused by a repeated `git` lookup on every keystroke.

## 1.1.60

This release is identical to version 1.1.53 and contains no new features, fixes, or other changes. We published it only to revert an earlier, unintended rollout: a later build that hadn’t finished testing was briefly promoted to the stable channel by mistake. Version 1.1.60 returns the stable channel to the known-good 1.1.53 build, so if you auto-updated during that window, updating to 1.1.60 restores you to the same code as 1.1.53.

## 1.1.53

### Added

- Private sessions with `--private`: Added the `--private` flag to `cortex` and `cortex exec` so a session runs without saving conversation history. Previously you could only turn history off with the `CORTEX_CODE_NO_HISTORY_MODE` environment variable or `cortex exec --no-history`.
- Reuse your Claude Code configuration: Cortex Code can now pick up an existing Claude Code setup. It merges MCP servers from `~/.claude.json` at read time (your Cortex Code, profile, and plugin servers still win on a name conflict), and the new `/import-claude-config` command does a one-time import of your theme and permission rules. Set `importClaudeMcpServers` to `false` to opt out of the MCP merge.
- MCP OAuth authorization server override: MCP server OAuth configuration now honors the `authorization_server_url` field, so you can point Cortex Code at a specific authorization server instead of the one it discovers from the MCP server. This helps with Snowflake-managed MCP servers that authenticate against an external identity provider.
- Find sessions by directory: The `/resume` picker adds a “This Directory” tab that lists sessions started in your current working directory, so you can change into a project folder and pick up its sessions first.

### Fixed

- Session resume across repositories: The “This Branch” tab in `cortex --resume` and `/resume` now also matches the current repository, so sessions from other repositories that share a branch name (for example, `main`) no longer appear there. They move to “Other Sessions”.
- Safer command approval: Fixed a case where approving a base command (for example, `git` or `curl`) for the session could then auto-approve a later command that redirects to a network path such as `/dev/tcp`, or writes to an unexpected file. Those commands now prompt for approval again.
- File mentions for added directories: `@` file completion now includes directories added with `/add-dir`, not just the directory you started in.
- Local plugin install: `cortex plugin install <path>` no longer crashes when a plugin’s `plugin.json` has a `commands`, `skills`, or `agents` field that isn’t a string. Cortex Code ignores the malformed field, warns you about it, and finishes the install.
- Large paste responsiveness: Resizing the terminal, or exiting fullscreen, in a session that contains a very large pasted message no longer freezes the interface for several seconds.

### Changed

- Thinking metrics in the status bar: While the model is thinking, the status bar now shows the current `/effort` level, an estimated token count, and elapsed thinking time instead of opaque activity blocks.
- Terminal-aware SQL tables: Inline SQL result tables now size to your terminal width instead of a fixed width, and the fullscreen table view starts with a collapsed query panel (press `e` to expand) so a large query doesn’t hide the results.

## 1.1.52

### Added

- `cortex agent-studio` commands: The commands for managing Semantic Views and Cortex Agents (read, write, deploy, query, and evaluate) are now available in the CLI without an experimental flag.
- MCP OAuth client secrets: MCP server OAuth configuration now accepts a `client_secret`, so you can connect to servers that use a pre-registered confidential OAuth client.
- Inherit a subagent’s model: The `task` tool accepts `model: "inherit"` so a subagent runs with the same model as the session that spawned it. You can also set `model: inherit` in an agent definition’s front matter.
- More object types in object search: `cortex search object` can now search for streams, stages, tasks, and pipes with `--types`, in addition to the object types it already supported.

### Fixed

- Proxy support for model streaming: The CLI again honors the `HTTP_PROXY` and `HTTPS_PROXY` environment variables when it streams responses from the model. Proxy support on this path regressed after Cortex Code moved to the Node.js runtime.
- Selection prompts: Fixed rendering problems in interactive selection prompts, such as permission approvals, plan review, and clarifying questions. Long option lists could hide choices, the prompt could overwrite earlier transcript output, and text could be truncated even when space was available.
- Windows sign-in: Fixed a “Cannot find module” error during connection setup on Windows that could interfere with OAuth sign-in, including authorization for MCP servers.

### Changed

- Fewer prompts for read-only system functions: Expanded the read-only SQL allowlist so that more read-only `SYSTEM$` functions run without a permission prompt. For example, `SYSTEM$GET_SERVICE_STATUS`, `SYSTEM$CLUSTERING_INFORMATION`, and `SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW`.
- Catalog skills install globally: Skills that you install from the catalog now always install to `~/.snowflake/cortex/skills/`, so they’re available from any Cortex Code session no matter which directory you start from. Skills installed by earlier versions continue to load.
- Live output for background subagents: When you wait on a background subagent, its output now streams live as it runs instead of appearing all at once after it finishes.

## 1.1.47

### Added

- MCP OAuth for remote and headless machines: HTTP MCP servers that require OAuth can now be authorized by opening the printed authorization URL in any browser and pasting the redirect URL back into the terminal, so sign-in completes even when the OAuth callback can’t reach a cloud workspace or remote development box.
- FIPS 140 mode for government and FedRAMP accounts: The CLI now bundles the CMVP-validated OpenSSL 3.1.2 FIPS provider across all supported platforms and enables FIPS 140 mode automatically on government and FedRAMP deployments.
- Background monitors view: Added the `/monitors` command and monitor detail panels to inspect long-running background processes, plus a footer hint that shows the number of active monitors.
- Warehouse credit attribution: Added the `COCO_ADDITIONAL_QUERY_TAGS` environment variable to inject custom key-value pairs into the `QUERY_TAG` on every Snowflake connection, so you can attribute warehouse credits by application or team.

### Fixed

- Plan mode commands: Bash commands in plan mode again defer to the normal permission system instead of being blocked. A previous change restricted plan mode to a handful of commands, which prevented routine read-only commands and produced worse plans.
- Model picker: The `/model` picker now shows a clear warning when it can’t reach the model service and falls back to a default list, and it no longer hangs on a stalled request because of a new 15-second timeout.
- Windows connection sync: Sync from Snowflake no longer hangs on Windows hosts where `localhost` resolves to IPv6 first.
- Profile handling: The CLI no longer crashes when a profile name is empty or undefined.

### Changed

- Faster Cortex Extension plugin installs: `cortex plugin install` now downloads extension files in parallel, which greatly reduces install time for large extensions. For example, a 108-file extension dropped from about 50 seconds to about 12 seconds.
- Project settings source: Cortex Code no longer reads `.claude/settings.json` as project settings. Only its own `.cortex/settings.json` is used, so move any project-level configuration into `.cortex/settings.json`.

## 1.1.41

### Added

- Team mode: Run collaborative multi-agent workflows with shared session semantics and improved cleanup on interrupt.
- Connections manager: The `/connections` page supports add, edit, and delete with in-place list refresh after changes.
- Authenticator picker: Choose an authentication method from a unified picker with per-method guidance and conditional credential fields.
- Plugin discovery: `cortex plugin find` prefers Snowscope search for extension discovery.
- Usage tracking: Subagent token usage is recorded in `stats/usage.json` alongside the main session.
- SQL read-only allowlist: Added `SYSTEM$GET_APPLICATION_SERVICE_DEFAULTS` to the read-only SQL function allowlist.

### Fixed

- `/automation history` no longer hangs when an account has a very large automation history.
- Ctrl-Z and foreground resume no longer drop conversation chunks from the transcript.
- Permission prompts behave correctly when multiple clients operate on the same thread.
- Skill improver and curator background review no longer loop indefinitely.
- Windows hosts bind the connection-retrieval helper to `localhost` instead of `127.0.0.1` to avoid IPv6 resolution hangs.

### Changed

- `cortex ws` workspace commands are generally available; an internal kill switch remains for emergency disable.
- Skill and plugin catalog installs report progress, honor certified versions, and align behavior with Snowsight catalog flows.
- Government and FedRAMP deployments bundle the validated OpenSSL FIPS provider alongside runtime FIPS enforcement.

## 1.1.27

### Added

- Named Restricted Session Scope: Use `--with-restricted-session-scope`, `--with-default-restricted-session-scope`, and `/guardrails` to discover and apply named RSS objects.
- FIPS 140 mode: Government and FedRAMP accounts enforce FIPS 140 mode on Snowflake connections.
- Windows signed CLI: Windows ships a signed single-file executable to reduce false positives from antivirus tools.
- Sandbox AWS SigV4: Phased support for AWS SigV4 signing inside the sandbox for guest workloads.
- Undo and external editor: Esc-u undoes the last `/rewind` step, and Ctrl-Q opens the current prompt in `$EDITOR`.
- Workspace CLI improvements: `cortex workspace` emits usage metrics and clearer copy summaries.

### Fixed

- Windows self-update works with the Node-based launcher and correct install paths.
- RSS role catalog fetching retries when the SQL connection is stale and parses `SHOW TERSE ROLES` output reliably.
- Plugin registry recovery clears stale lock files instead of failing permanently.
- Skill improver background review no longer enters a dead loop.

### Changed

- Auto-update follows the stable or beta channel pointer, including downgrades when stable is rolled back to an earlier build.
- Two sandbox experimental capabilities are enabled by default for new sessions.
- Auto-approve `sql_execute` when an active Restricted Session Scope child session is in effect.

## 1.1.8

### Added

- `cortex exec`: Run Cortex Code non-interactively for CI/CD and automation pipelines.
- `cortex workspace`: Manage Snowflake Workspace files from the CLI.
- Restricted Session Scope: Initial SQL session guardrails limit what the agent can run before broader RSS features shipped in later releases.
- Profile subagents: Profiles can reference subagents, and plan auto-accept settings propagate through spawned subagents.
- Plugin trust boundary: Untrusted plugins cannot silently register MCP servers, OAuth flows, or skill updates.
- MCP reconnect: Reconnect failed MCP servers from `/mcp` or reconnect all servers in one action.
- Memory setting: The `enableMemory` setting gates all memory read and write features.
- Government indicator: The CLI footer shows when you are connected to a government region.
- Skill sync: Background skill channel sync and the `cortex skill sync` command keep bundled skills current between releases.

### Fixed

- Plugin MCP tools no longer double-prefix tool names, which had prevented plugin tools from running.
- The `/mcp` manager stops flashing on refresh and supports Enter to reconnect failed servers.
- Profile inheritance through subagent spawn chains applies the intended profile and skill paths.
- `--resume` no longer corrupts transcripts when static logs contained ANSI color codes.

### Changed

- SQL execution tool naming: The permission pattern and tool name are `sql_execute` instead of `snowflake_sql_execute`. Update managed settings and allowlists that still reference the old name.

## 1.0.77

### Added

- `/changelog` command: View release notes directly in the CLI.
- `/mcp` manager overhaul: Split-pane view with search and filter, add/edit/delete server controls, source badges, OAuth state display, invalid-tool diagnostics, and correct disable semantics.
- SQL read-only mode: `--sql-read-only` launch flag and `/sql-writes on|off|status` slash command to restrict write operations.
- Project skill discovery: Added `.agents/skills` as a project-level skill discovery directory alongside the existing `.snowflake/cortex/skills`.
- Clipboard shortcut: Added `ESC+C` to copy the current input to the clipboard.
- Fast in-repo search: Added `/index` command backed by an FTS5 trigram index for instant grep across large codebases.
- ACP session identity: Editor integrations can now supply a session ID via `_meta.sessionId` in ACP requests.
- GPT 5.5 model support: Added GPT 5.5 to available coding and reasoning models.
- Mac workspace acceleration: `ws create --hv=vz` uses the Apple Virtualization framework directly for ~1-second boots without Lima.
- Rule management: Session-scoped rule suppression and inline editing of rule text, category, and tags.
- Agent SDK: Support for custom MCP tool definitions and hook callbacks.

### Fixed

- Role switching: `USE ROLE` via `sql_execute` no longer causes 403 errors on subsequent agent API calls (dedicated connection isolation).
- Large command output: Bash commands producing more than 30K characters are no longer silently truncated; output between 30K–50K is preserved inline and output over 50K is offloaded to a file.
- Plan mode: Plan mode is now correctly disabled immediately after the user approves a plan.
- Memory search: No longer silently disabled when the snowmem embed endpoint returns a malformed response.
- Snowflake OAuth retry: Retrying OAuth no longer purges all stored credentials.
- `data_diff`: Now works correctly on user machines after bundling the required PBS Python runtime.
- Snowmem embed parsing: Fixed incorrect 1-dimensional response handling; responses are now correctly parsed as 1024-dimensional vectors.

### Changed

- Permission prompts: `tgrep` and `cron_create` now prompt for permission approval instead of auto-approving.

## 1.0.65

### Added

- Managed plugins and marketplace installs: Added registry-backed plugin install, update, enable, disable, validate, and uninstall flows, plus marketplace-backed installs and a fullscreen plugin manager.
- Runtime plugin refresh: Added in-process plugin reloads so lifecycle changes can refresh commands, skills, agents, hooks, and MCP servers without restarting Cortex Code.

### Changed

- Disabled plugin handling: Switched disabled plugins to explicit activation metadata so inactive installs stay discoverable without loading their full runtime contents.

## 1.0.59

### Added

- Postgres connections and SQL workflows: Added Postgres connection management, Snowflake Postgres token authentication, and dialect-aware `/sql` execution across Snowflake and Postgres.
- ACP editor integration: Added `cortex acp serve` with streaming editor sessions, native permission routing, clarifying-question prompts, and diff-based file edit previews.

### Changed

- Postgres safety and credential handling: Hardened Postgres permission analysis, secured Snowflake Postgres token generation, and removed shell-exposed password flags in favor of secure prompts or `~/.pgpass`.

## 1.0.28+173700.0975210405a4 (2026-03-02)

### Added

- Faster guardrails: Reduced guardrail latency so protected requests feel less disruptive during streaming.
- Browser workflows: Added `cortex browser` and improved browser recovery flows.
- Team workflows: Expanded swarm and background-agent collaboration flows.

### Changed

- Sandbox coverage: Expanded sandbox support across more platforms and workflows.
- Profiles and tool controls: Added richer profiles and easier tool allow or deny controls.

## 1.0.17+201538.00c735fc7e3a (2026-02-19)

### Added

- Windows platform support: Added broader Windows compatibility across shell, file, and CLI workflows.
- Background agents: Improved reconnect, resume, and navigation flows for `/agents`.
- Permission rules: Added configurable permission rules for safer command execution.

### Fixed

- Auth and credential resilience: Improved token storage, migration, and recovery for authentication flows.
- Shell safety and controls: Strengthened shell safeguards and expanded usage, model, and view controls.

## 1.0.11+011422.721be00264d0 (2026-02-12)

### Added

- Skill updates and remote plugins: Added versioned skill updates and support for plugins hosted in GitHub repositories.
- Inter-agent coordination: Added agent-to-agent messaging and stronger multi-agent task coordination.
- Model discovery: Improved model discovery and request routing.

### Changed

- Resume and sandbox controls: Improved session resume behavior and sandbox testing controls.

## 1.0.10+223843.7a31e1a1441a (2026-02-11)

### Added

- Skill and plugin packaging: Bundled the Airflow plugin and added tarball-based skill installs.
- Performance and output handling: Improved startup time and large tool-output handling.
- Notebook execution robustness: Improved notebook execution permissions, reliability, and diagnostics.

### Changed

- Inter-agent orchestration: Expanded agent coordination and task flows.
- Model and skill management: Improved model discovery and skill update flows.

## 1.0.9+154353.e3dd198d62ee (2026-02-09)

### Added

- Instruction management: Added instruction settings and clearer visibility into loaded instruction files.
- Fork and rewind reliability: Made `/fork` and `/rewind` more reliable and easier to follow.
- Custom slash commands: Expanded custom slash command naming and collision handling.

### Changed

- MCP workflow: Improved live updates when changing MCP server configurations.
- Rendering polish: Reduced noisy spinners and improved transcript rendering behavior.

## 1.0.7+015551.0d10922ac7fe (2026-02-06)

### Added

- Background agents and `/agents`: Added background-agent launch flows and stronger plan handling for interactive sessions.
- Settings and fullscreen controls: Added tabbed settings views and a more capable fullscreen settings experience.
- Session browsing and docs: Added session search and a `/docs` shortcut to open documentation.

### Changed

- Model selection: Expanded `/model` options and improved default model behavior for subagents.
- Semantic and dbt helpers: Improved semantic and dbt assistant workflows.

## 1.0.6+020057.75a0ba5e6a69 (2026-02-04)

### Added

- Snowflake config and path handling: Improved Snowflake home and config resolution plus safer connection setup workflows.
- Secret and connection tooling: Added `cortex secret` and better support for local connections.
- Worktree and remote-source improvements: Expanded worktree creation and improved remote skill and repository sourcing.

### Changed

- Notebook actions: Improved notebook permissions and notebook-action reliability.
- CLI and session resilience: Improved interrupt handling, screen clearing, and table rendering in the terminal.
