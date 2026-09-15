# Permission modes

Permission modes control when CoCo stops to ask before the agent runs tools that touch your machine, your code, or your Snowflake account. Every chat has an **approval mode** (Default Approvals or Bypass Approvals) that determines when the agent pauses for confirmation and when it acts on its own.

Important

Bypass Approvals turns off manual approval for **every** tool call, including file edits, terminal commands, and Snowflake SQL. Only enable it for trusted prompts, in trusted projects, when you understand what the agent is about to do. The agent can still make destructive changes; you just won’t be asked first.

## Approval modes at a glance

The approval mode picker lives in the bottom-left of the chat input. Switch at any time; the change applies to the current chat and all future chats until you change it back.

| Mode | Icon | Behavior |
| --- | --- | --- |
| **Default Approvals** | shield | CoCo uses your configured per-tool, per-edit, and per-URL approval settings. New or risky tool calls prompt for confirmation. This is the recommended setting for everyday use. |
| **Bypass Approvals** | warning | Every tool call is auto-approved without prompting. Use sparingly, in trusted contexts only. |

Expand

Show lessSee more

The approval mode is a **machine-wide** setting. Switching it in one chat affects every chat in every project on the same machine.

## Default Approvals

Under Default Approvals, the agent stops and asks before running tool calls that could have side effects. Approving once for a tool typically allows it for the rest of the chat; you can also choose to allow it permanently. Approvals are tracked in three independent categories:

### Tool calls

Calls to tools like `bash`, terminal commands, MCP tools, browser automation, and SQL execution prompt for approval. Each prompt offers:

- **Allow once:** run this single call.
- **Allow for session:** skip future prompts for this tool in this chat.
- **Always allow:** never prompt for this tool again on this machine.
- **Reject:** cancel this call and let the agent try something else.

Some tools are intentionally **ineligible for auto-approval** and always prompt, no matter what you click. See [Tools that always prompt](#always-prompt).

#### SQL and stored procedure approvals

SQL execution is treated like any other tool call, so the same **Allow once**, **Allow for session**, and **Always allow** choices apply. Note the following behavior specific to SQL:

- **Stored procedure calls (`CALL`) can prompt again even after “Always allow.”** Because a `CALL` can change state and the agent can’t always determine what the procedure does, you may be prompted again for `CALL` statements you approved earlier. To reduce prompts when you run the same procedure repeatedly (for example, switching context across many accounts), choose **Allow for session**, or use **Bypass Approvals** in a trusted context.
- **Statement text matters.** An approval applies to the specific statement that was shown. A statement that differs (a different procedure, arguments, or target) is treated as new and prompts again.

If approvals seem “stuck” on always allow, or you want the agent to start prompting again, [reset tool confirmations](#reset-confirmations).

### File edits

File edits are gated by a list of glob patterns that decide whether an edit is auto-approved or prompts you. The defaults auto-approve most files but require explicit approval for:

- `**/.vscode/*.json`
- `**/.git/**`
- Critical project files: `package.json`, `package-lock.json`, `.env`, `build.rs`, etc.
- Project files: `*.code-workspace`, `*.csproj`, `*.fsproj`, `*.vcxproj`, `*.proj`, `*.targets`, `*.props`

The last matching pattern wins. You can add your own patterns to lock down extra files, or expand auto-approval, in settings.

### URLs

Network-fetching tools check a configurable list of URL patterns. Patterns can be exact hosts (`https://example.com`), wildcards (`https://*.example.com`), or path-scoped (`https://example.com/api/*`). Each entry can approve a URL outright, always prompt for it, or distinguish between approving the request and approving the response.

## Bypass Approvals

Switching to Bypass Approvals **disables every approval check** above. The agent will:

- Run any terminal command without asking.
- Edit any file in the project without asking.
- Call any tool, including MCP tools, without asking.
- Execute any Snowflake SQL without asking.

Bypass Approvals overrides per-tool, per-edit, and per-URL settings. A few high-risk tools still always prompt. See [Tools that always prompt](#always-prompt).

Important

A prompt-injection attack via a webpage, file, or model output can cause the agent to issue commands you didn’t intend. Anything that ends up in the agent’s context (web fetches, file contents, tool outputs) can contain instructions. With Default Approvals you’d see the prompt and reject it; with Bypass Approvals it just runs. Treat Bypass Approvals like running unverified scripts as root.

### Block Bypass Approvals across an organization

Administrators can disable Bypass Approvals fleet-wide with the `permissions.dangerouslyAllowAll` managed setting. When it’s blocked, the mode picker shows Bypass Approvals disabled with a “Blocked by your organization” message, and anyone who previously enabled it is reset to Default Approvals. See [Managed settings](/user-guide/cortex-code/cortex-code-desktop/managed-settings).

## Reset tool confirmations

Every “Always allow” choice and every per-workspace approval you grant is remembered between sessions. To clear them and have the agent prompt again from a clean slate:

1. Open the Command Palette with **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows).
2. Run **Reset Tool Confirmations**.

This helps when you accidentally chose “Always allow” or “allow in this workspace” and want the agent to start checking with you again, or when you’re handing a machine or project to someone else. Resetting confirmations doesn’t change your approval mode: it only clears the remembered per-tool, per-edit, per-URL, and per-workspace approvals.

## Choosing a mode

- **New project or task you don’t fully trust.** Default Approvals.
- **Untrusted source** (a prompt copied from the internet, a file from a customer, a web page being fetched). Default Approvals.
- **Highly repetitive, well-understood task in a sandboxed branch** (for example, a codemod across many files). Bypass Approvals can be reasonable. Flip back as soon as the task is done.
- **Running an automation overnight.** Default Approvals. An automation that hits a confirmation prompt will stall, but that’s safer than auto-approving a runaway agent. To avoid stalls, use *Run now* once on a new automation and approve the tools it needs; future runs proceed without prompting. See *Automations* > *Permissions*.

## Tools that always prompt

A handful of tools are intentionally exempt from auto-approval and **always prompt**, regardless of approval mode or admin policy:

- **Browser code execution** (`browser_evaluate`, `browser_run_code`): arbitrary JS in a live page is the highest-risk tool, so a prompt-injection on any visited page can’t silently exfiltrate data after a benign first invocation.
- **Clipboard reads** (`browser_read_clipboard`): the system clipboard may contain passwords or tokens.
- **Subagents** and certain other destructive tools that opt out of auto-approval.

## Agent terminal sandbox

For an extra layer of protection around agentic terminal use, you can have CoCo wrap the commands the agent runs in a sandbox. When the sandbox is enabled, terminal commands issued by the chat agent run inside a restricted environment rather than directly on your machine.

Enable it by setting the following in your settings:

Copy code

```
"chat.agent.sandbox.enabled": "on"
```

The sandbox is a defense-in-depth measure that complements approval modes. It limits what an approved (or auto-approved) terminal command can do, which is especially useful when running with Bypass Approvals or when executing prompts from untrusted sources.
