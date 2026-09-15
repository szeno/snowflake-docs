# Hooks

Hooks let you run shell commands automatically at key points during agent execution.
Use them to enforce policies, inject context, validate tool inputs, auto-approve permissions,
or integrate with external systems. Hooks can observe what the agent is doing, modify its
inputs, or block operations entirely.

[![Hooks panel in Agent Settings showing event types and the Add New Hook form](/static/images/user-guide/cortex-code/cortex-code-desktop/hooks/hooks-settings-overview.png)](/static/images/user-guide/cortex-code/cortex-code-desktop/hooks/hooks-settings-overview.png)

## Hook events

Each hook is attached to an event that fires at a specific point in the agent lifecycle:

| Event | When it fires | Can block |
| --- | --- | --- |
| `PreToolUse` | Before a tool is executed | Yes |
| `PostToolUse` | After a tool finishes executing | No |
| `PermissionRequest` | When a permission dialog is about to be shown | Yes (auto-allow or auto-deny) |
| `SessionStart` | When a new chat session is created | No |
| `UserPromptSubmit` | When the user submits a prompt | Yes |
| `Stop` | When the agent’s turn ends | No (but can force continuation) |
| `Notification` | When a notification is sent | No |
| `PreCompact` | Before conversation summarization/compaction | No |
| `SessionEnd` | When a session ends (clear, logout, exit) | No |
| `SubagentStop` | When a sub-agent’s turn ends | No |
| `Setup` | When the agent performs initial environment setup | Yes |

Expand

Show lessSee more

## Managing hooks

Open **Agent Settings** and select **Hooks** from the sidebar.
The panel lists all event types as expandable sections with a badge showing the count of
configured hooks (enabled / total).

To add a new hook:

1. Click the **+** button next to the event you want to hook into.
2. Choose the **Storage Location**:
   - **User** — stored globally in `~/.snowflake/cortex/settings.json`.
   - **Workspace** — stored in `<workspace>/.snowflake/cortex/settings.json`.
3. Configure using the **Form** view or switch to **JSON** for raw editing.
4. Set the fields:
   - **Tool Matcher** — regex pattern to filter which tools trigger the hook (for tool events). Use `*` for all tools.
   - **Command** — the shell command to execute (for example, `./my-hook-script.sh`).
   - **Timeout** — seconds to wait before timing out (default 60).
   - **Status Message** — custom message displayed as a spinner while the hook runs.
5. Click **Save**.

## Configuration file

Hooks are stored in the `hooks` key of your settings file:

| Scope | Path |
| --- | --- |
| User (global) | `~/.snowflake/cortex/settings.json` |
| Workspace | `<workspace>/.snowflake/cortex/settings.json` or `<workspace>/.cortex/settings.json` |

Expand

Show lessSee more

CoCo Desktop also loads a dedicated global hooks file at `~/.snowflake/cortex/hooks.json`
(using the same `{ "hooks": { ... } }` schema) alongside your `settings.json` hooks, and reloads it
when it changes. This file is shared with CoCo CLI and isn’t shown in the Desktop hooks UI,
so editing hooks in the UI won’t overwrite it. Its hooks are added to, not layered over, the hooks
from your settings files.

Example configuration:

Copy code

```
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "./validate-tool-call.sh",
            "timeout": 60,
            "enabled": true,
            "statusMessage": "Validating..."
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Session started'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Hook fields

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | `"command"` — runs a shell command. |
| `command` | string | The shell command to execute. |
| `timeout` | number | Seconds to wait before timing out (default: 60). |
| `enabled` | boolean | Whether the hook is active (default: true). |
| `statusMessage` | string | Message shown as a spinner while the hook runs. |

Expand

Show lessSee more

### Tool matcher

For tool-based events (`PreToolUse`, `PostToolUse`, `PermissionRequest`),
the `matcher` field is a regex pattern tested against the tool name. Use `"*"` or
leave empty to match all tools. Multiple matchers with different hooks can be configured for the same event.

The tool name is case-sensitive. Built-in tool names are lowercase, so a matcher of `bash` matches and
`Bash` doesn’t. A matcher that names no existing tool never fires, and no error is reported.

## Execution context

When a hook fires, the full execution context is piped to the command’s **stdin as JSON**.
This includes information about the current session and the triggering event:

| Field | Available on | Description |
| --- | --- | --- |
| `session_id` | All events | Unique session identifier |
| `cwd` | All events | Current working directory |
| `hook_event_name` | All events | The event being triggered |
| `tool_name` | Tool events | Name of the tool being called |
| `tool_input` | Tool events | Input parameters (JSON object) |
| `tool_response` | PostToolUse | The tool’s response text |
| `prompt` | UserPromptSubmit | The user’s submitted prompt text |

Expand

Show lessSee more

## Hook output

Hook commands communicate back via **stdout** (JSON) and **exit code**:

### Exit codes

| Exit code | Meaning |
| --- | --- |
| `0` | Success — proceed normally |
| `2` | Block — prevent the operation. Stderr content becomes the block reason. |
| Other non-zero | Error — logged but does not block |

Expand

Show lessSee more

### JSON output (stdout)

For more control, your hook can output JSON to stdout:

Copy code

```
{
  "decision": "approve",
  "reason": "All checks passed",
  "additionalContext": "Extra context injected into the conversation",
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "updatedInput": { "command": "modified-command" }
  }
}
```

| Field | Description |
| --- | --- |
| `decision` | `"approve"` or `"block"` — whether to proceed or block. |
| `reason` | Explanation (shown to agent if blocked). |
| `additionalContext` | Text injected into the conversation as context for the agent. |
| `hookSpecificOutput.permissionDecision` | For `PermissionRequest`: `"allow"`, `"deny"`, or `"ask"`. |
| `hookSpecificOutput.updatedInput` | For `PreToolUse`: modified tool input parameters. |

Expand

Show lessSee more

If stdout is not valid JSON, it is treated as `additionalContext` text.

## Blocking operations

`PreToolUse`, `PermissionRequest`, and `UserPromptSubmit` hooks can block operations.
When a hook blocks:

- The tool call (or prompt submission) is prevented.
- The block reason is shown to the agent so it can adjust its approach.
- The agent sees a message like: *“[Hook] Tool execution blocked: <reason>”*

To block from a hook, either:

- Exit with code `2` and write the reason to stderr.
- Output JSON with `"decision": "block"` and a `"reason"` field.

## Examples

### Block writes to production files

Copy code

```
#!/bin/bash
# block-prod-writes.sh — PreToolUse hook for edit/write tools
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$FILE" == */production/* ]]; then
  echo "Cannot modify files in the production directory" >&2
  exit 2
fi
```

### Auto-approve read-only tools

Copy code

```
#!/bin/bash
# auto-approve-reads.sh — PermissionRequest hook
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

case "$TOOL" in
  read|grep|glob)
    echo '{"hookSpecificOutput":{"permissionDecision":"allow"}}'
    ;;
  *)
    echo '{"hookSpecificOutput":{"permissionDecision":"ask"}}'
    ;;
esac
```

### Inject project context on session start

Copy code

```
#!/bin/bash
# session-context.sh — SessionStart hook
echo "This project uses Python 3.12, pytest for testing, and ruff for linting."
```

## Configuration precedence

Hooks from multiple sources are merged. Workspace hooks fire before user hooks.
Plugins and profiles can also contribute hooks (shown as read-only in the UI).
