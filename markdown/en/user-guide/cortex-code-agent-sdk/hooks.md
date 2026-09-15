# Hooks

This topic describes how to use hooks to run custom code at key points in the agent lifecycle. Hooks let you
intercept tool calls, audit agent behavior, enforce policies, inject context, and control execution flow.

## How hooks work

Hooks follow a four-step process: an **event** fires, the SDK checks if any **matcher** applies, it calls your
**callback**, and your callback returns a **decision** that controls what happens next.

1. The agent triggers an event (for example, it’s about to call a tool).
2. The SDK checks each hook matcher registered for that event type.
3. If a matcher matches (or has no matcher pattern, meaning it matches everything), the SDK calls the associated
   callback functions.
4. Each callback returns an output object that can allow, block, or modify the operation.

## Hook events

The following events are available:

| Event | When it fires |
| --- | --- |
| `PreToolUse` | Before a tool executes. Can block the tool or modify its input. |
| `PostToolUse` | After a tool executes successfully. Can inject additional context. |
| `PostToolUseFailure` | After a tool execution fails. |
| `UserPromptSubmit` | When the user sends a prompt. Can inject additional context. |
| `Stop` | When the agent is about to stop. Can inject context or halt the session. |
| `SubagentStart` | When a sub-agent starts. |
| `SubagentStop` | When a sub-agent is about to stop. |
| `PreCompact` | Before the conversation is compacted (summarized to fit the context window). |
| `Notification` | When the agent emits a notification. |
| `PermissionRequest` | When a tool permission check occurs. |

Expand

Show lessSee more

## Configuring hooks

Pass hooks through the `hooks` option when creating a session. Each hook event maps to a list of
[matchers](#label-cortex-code-agent-sdk-hooks-matchers), and each matcher contains a list of callback functions.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  hooks: {
    PreToolUse: [
      {
        matcher: "Bash",
        hooks: [
          async (input, toolUseId, context) => {
            console.log("Bash command:", input.tool_input);
            return {};
          },
        ],
      },
    ],
  },
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, HookMatcher

async def log_bash(input, tool_use_id, context):
    print("Bash command:", input["tool_input"])
    return {}

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[log_bash]),
        ],
    },
)) as client:
    await client.query("List files in the current directory")
    async for msg in client.receive_response():
        pass
```

## Matchers

Each hook matcher has three fields:

| Field | Type | Description |
| --- | --- | --- |
| `matcher` | `string` (optional) | A regex pattern used by events that support matching. `PreToolUse`, `PostToolUse`, and `PermissionRequest` match on tool name. `Notification` matches on notification type. `PreCompact` matches on the trigger value (`"auto"` or `"manual"`). If omitted, the hook fires for all values for that event. |
| `hooks` | list of callbacks | One or more callback functions to run when the matcher matches. |
| `timeout` | `number` (optional) | Maximum time in seconds for all callbacks in this matcher. Defaults to 60. |

Expand

Show lessSee more

The `matcher` field accepts any valid regex pattern. For example:

- `"Bash"` – matches only the Bash tool
- `"Write|Edit"` – matches Write or Edit
- `".*"` – matches all tools (same as omitting the matcher)

## Callback inputs

Every callback receives three arguments:

| Argument | Description |
| --- | --- |
| `input` | An object containing event-specific data. All events include `session_id`, `transcript_path`, `cwd`, `permission_mode`, and `hook_event_name`. Tool events also include `tool_name`, `tool_input`, and `tool_use_id`. |
| `toolUseId` / `tool_use_id` | The tool use ID (for tool-related events) or `null`. |
| `context` | A context object. Reserved for future use (for example, abort signals). |

Expand

Show lessSee more

Input fields vary by event:

| Event | Additional input fields |
| --- | --- |
| `PreToolUse` | `tool_name`, `tool_input`, `tool_use_id` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` |
| `PostToolUseFailure` | `tool_name`, `tool_input`, `tool_use_id`, `error`, optional `is_interrupt` |
| `UserPromptSubmit` | `prompt` |
| `Stop` | `stop_hook_active` |
| `SubagentStart` | `agent_id`, `agent_type` |
| `SubagentStop` | `stop_hook_active`, `agent_id`, `agent_transcript_path`, `agent_type` |
| `PreCompact` | `trigger` (`"manual"` or `"auto"`), `custom_instructions` |
| `Notification` | `message`, `notification_type`, optional `title` |
| `PermissionRequest` | `tool_name`, `tool_input`, optional `permission_suggestions` |

Expand

Show lessSee more

Tool-lifecycle hooks and `PermissionRequest` can also include optional `agent_id` and `agent_type` fields when
they fire from a sub-agent.

## Callback outputs

Callbacks return an output object that controls execution. The following fields are available:

| Field | Type | Description |
| --- | --- | --- |
| `continue` / `continue_` | `boolean` | Whether processing should proceed. Set to `false` to stop further processing for the current hook site or turn. Default: `true`. |
| `stopReason` | `string` | Message shown when `continue` is `false`. |
| `decision` | `"block"` | Set to `"block"` to block the current operation. |
| `reason` | `string` | Feedback message for the agent about the decision. |
| `systemMessage` | `string` | Warning message displayed to the user. |
| `hookSpecificOutput` | `object` | Event-specific controls (see below). |

Expand

Show lessSee more

Note

The Python SDK uses `continue_` (with a trailing underscore) instead of `continue` to avoid the Python keyword
conflict. The SDK automatically converts this to `continue` when communicating with the CLI.

### Hook-specific outputs

The `hookSpecificOutput` field accepts event-specific controls:

**PreToolUse**

| Field | Description |
| --- | --- |
| `permissionDecision` | `"allow"`, `"deny"`, or `"ask"`. Controls whether the tool can execute. |
| `permissionDecisionReason` | Reason for the permission decision. |
| `updatedInput` | Modified tool input to use instead of the original. |

Expand

Show lessSee more

**PostToolUse**

| Field | Description |
| --- | --- |
| `additionalContext` | Extra context injected into the conversation after tool execution. |

Expand

Show lessSee more

**UserPromptSubmit**

| Field | Description |
| --- | --- |
| `additionalContext` | Extra context injected into the conversation. |

Expand

Show lessSee more

**PermissionRequest**

| Field | Description |
| --- | --- |
| `decision.behavior` | `"allow"` or `"deny"`. Controls the permission result. |
| `decision.message` | Message shown when denying the permission request. |

Expand

Show lessSee more

## Examples

### Block dangerous tools

Prevent the agent from running specific bash commands:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  hooks: {
    PreToolUse: [
      {
        matcher: "Bash",
        hooks: [
          async (input) => {
            const command = (input.tool_input as any)?.command ?? "";
            if (command.includes("rm -rf") || command.includes("DROP TABLE")) {
              return {
                decision: "block",
                reason: "Destructive commands are not allowed",
              };
            }
            return {};
          },
        ],
      },
    ],
  },
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, HookMatcher

async def block_dangerous(input, tool_use_id, context):
    command = input.get("tool_input", {}).get("command", "")
    if "rm -rf" in command or "DROP TABLE" in command:
        return {
            "decision": "block",
            "reason": "Destructive commands are not allowed",
        }
    return {}

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(matcher="Bash", hooks=[block_dangerous]),
        ],
    },
)) as client:
    ...
```

### Auto-allow read-only permission requests

Allow permission requests for tools that only read data:

TypeScriptPython

Copy code

```
hooks: {
  PermissionRequest: [
    {
      matcher: "Read%Glob%Grep",
      hooks: [
        async (input) => {
          return {
            hookSpecificOutput: {
              hookEventName: "PermissionRequest",
              decision: { behavior: "allow" },
            },
          };
        },
      ],
    },
  ],
}
```

Copy code

```
async def auto_approve_reads(input, tool_use_id, context):
    return {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "allow"},
        },
    }

hooks = {
    "PermissionRequest": [
        HookMatcher(matcher="Read%Glob%Grep", hooks=[auto_approve_reads]),
    ],
}
```

### Modify tool input

Add a timeout to all bash commands before they execute:

TypeScriptPython

Copy code

```
hooks: {
  PreToolUse: [
    {
      matcher: "Bash",
      hooks: [
        async (input) => {
          const originalCommand = (input.tool_input as any)?.command ?? "";
          return {
            hookSpecificOutput: {
              hookEventName: "PreToolUse",
              updatedInput: { command: `timeout 30 ${originalCommand}` },
            },
          };
        },
      ],
    },
  ],
}
```

Copy code

```
async def add_timeout(input, tool_use_id, context):
    original = input.get("tool_input", {}).get("command", "")
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "updatedInput": {"command": f"timeout 30 {original}"},
        },
    }

hooks = {
    "PreToolUse": [
        HookMatcher(matcher="Bash", hooks=[add_timeout]),
    ],
}
```

### Audit logging

Log all tool calls for auditing purposes without affecting execution:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";
import { appendFileSync } from "node:fs";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  hooks: {
    PostToolUse: [
      {
        hooks: [
          async (input) => {
            const entry = {
              timestamp: new Date().toISOString(),
              tool: input.tool_name,
              input: input.tool_input,
              sessionId: input.session_id,
            };
            appendFileSync("audit.log", JSON.stringify(entry) + "\n");
            return {};
          },
        ],
      },
    ],
  },
});
```

Copy code

```
import json
from datetime import datetime, timezone
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, HookMatcher

async def audit_log(input, tool_use_id, context):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": input.get("tool_name"),
        "input": input.get("tool_input"),
        "session_id": input.get("session_id"),
    }
    with open("audit.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {}

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    hooks={
        "PostToolUse": [
            HookMatcher(hooks=[audit_log]),
        ],
    },
)) as client:
    ...
```

## Hooks vs. canUseTool

Both hooks and the `canUseTool` callback can intercept tool calls, but they serve different purposes:

| Feature | `canUseTool` | Hooks |
| --- | --- | --- |
| Scope | Pre-execution permission check only | Multiple lifecycle events (tool lifecycle, prompt submit, stop, sub-agent lifecycle, notification, and compaction) |
| Events | One: permission request | Ten: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`, `Notification`, and `PreCompact` |
| Pattern matching | No matcher support. Invoked for permission requests that are not already resolved by rule lists. | Yes (regex matchers filter by tool name, notification type, or compaction trigger depending on the event) |
| Modify input | Limited. `updatedInput` is currently used for SDK-routed pseudo-tools such as `AskUserQuestion` and `ExitPlanMode`. | Yes (`hookSpecificOutput.updatedInput`) |
| Best for | Simple allow/deny decisions | Audit logging, context injection, complex policies, post-execution actions |

Expand

Show lessSee more

You can use both together. The `canUseTool` callback runs as part of the CLI’s permission system, while
`PreToolUse` hooks run separately.

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
