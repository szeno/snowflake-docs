# Handle approvals and user input

Use `allowedTools` / `disallowedTools` rules and the `canUseTool` callback to control which tools the agent can
use and how permission requests are handled.

By default, the SDK enforces tool permissions and does not bypass them. The `canUseTool` callback gives you
granular control over permission requests that are not already resolved by `allowedTools` /
`disallowedTools` rules or by an explicit permission mode such as `bypassPermissions`.

The SDK does not provide an interactive permission prompt by default. If a permission-checked request reaches the SDK
and `canUseTool` is not provided, the request fails.

## How it works

When you provide a `canUseTool` callback, the SDK calls it before each permission-checked tool execution. Your
callback decides what happens:

1. The agent decides to use a permission-checked tool.
2. The SDK calls your `canUseTool` callback with the tool name, request input, and permission context.
3. Your callback returns `allow` or `deny`.
4. The tool execution proceeds or is blocked accordingly.

For many ordinary tool permission checks, the callback input contains fields such as
`{ action, resource }`. SDK-routed pseudo-tools such as `AskUserQuestion` and `ExitPlanMode` contain
tool-specific fields.

If `canUseTool` is not provided and a permission-checked request reaches the SDK, the SDK returns an error instead
of prompting interactively.

## Basic example

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  canUseTool: async (toolName, input, context) => {
    console.log(`Tool requested: ${toolName}`, input);

    // Allow read-only tools, deny destructive ones
    if (["Read", "Glob", "Grep"].includes(toolName)) {
      return { behavior: "allow" };
    }

    return { behavior: "deny", message: "Only read-only tools are allowed" };
  },
});

await session.send("What files are in this directory?");
for await (const event of session.stream()) {
  if (event.type === "assistant") {
    for (const b of event.content) {
      if (b.type === "text") process.stdout.write(b.text);
    }
  }
  if (event.type === "result") break;
}
await session.close();
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    CortexCodeAgentOptions,
    CortexCodeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    print(f"Tool requested: {tool_name}", tool_input)

    # Allow read-only tools, deny destructive ones
    if tool_name in ("Read", "Glob", "Grep"):
        return PermissionResultAllow()

    return PermissionResultDeny(message="Only read-only tools are allowed")

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    can_use_tool=can_use_tool,
)) as client:
    await client.query("What files are in this directory?")
    async for msg in client.receive_response():
        ...
```

## Response patterns

### Allow a tool call

Return `{ behavior: "allow" }` to let the tool execute with its original input:

TypeScriptPython

Copy code

```
canUseTool: async (toolName, input, context) => {
  return { behavior: "allow" };
}
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import PermissionResultAllow, ToolPermissionContext

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow:
    return PermissionResultAllow()
```

### Deny a tool call

Return `{ behavior: "deny" }` with an optional message. The agent sees the denial message and can adjust its
approach:

TypeScriptPython

Copy code

```
canUseTool: async (toolName, input, context) => {
  if (toolName === "Bash") {
    return { behavior: "deny", message: "Bash commands are not allowed in this session" };
  }
  return { behavior: "allow" };
}
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    if tool_name == "Bash":
        return PermissionResultDeny(message="Bash commands are not allowed in this session")
    return PermissionResultAllow()
```

## The AskUserQuestion tool

Cortex Code has a built-in `AskUserQuestion` tool that the agent uses when it needs clarification from the user.
When the agent calls `AskUserQuestion`, the SDK routes it through your `canUseTool` callback with
`toolName` set to `"AskUserQuestion"`. The input contains the agent’s questions as structured multiple-choice
options.

### Handling questions

Check for `toolName === "AskUserQuestion"` in your `canUseTool` callback. The `input` contains a `questions`
array where each question has:

| Field | Description |
| --- | --- |
| `question` | The full question text to display |
| `header` | Short label for the question |
| `options` | Array of choices, each with `label`, `description`, `freeForm` (bool), and `isCancel` (bool) |
| `multiSelect` | If `true`, users can select multiple options |

Expand

Show lessSee more

Return `allow` with an `updatedInput` that includes the original `questions` and an `answers` map. Each key
is the question text and each value is the selected option’s label. For multi-select questions, join labels with
`", "`.

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  canUseTool: async (toolName, input, context) => {
    if (toolName === "AskUserQuestion") {
      const answers: Record<string, string> = {};
      for (const q of input.questions) {
        // Present q.question and q.options to the user, collect their choice
        const selected = await promptUser(q.question, q.options);
        answers[q.question] = selected;
      }
      return {
        behavior: "allow",
        updatedInput: { questions: input.questions, answers },
      };
    }
    return { behavior: "allow" };
  },
});
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    PermissionResultAllow,
    ToolPermissionContext,
)

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow:
    if tool_name == "AskUserQuestion":
        answers: dict[str, str] = {}
        for q in tool_input.get("questions", []):
            # Present q["question"] and q["options"] to the user, collect their choice
            selected = await prompt_user(q["question"], q["options"])
            answers[q["question"]] = selected
        return PermissionResultAllow(
            updated_input={"questions": tool_input["questions"], "answers": answers}
        )
    return PermissionResultAllow()
```

To deny a question (cancel the interaction), return `deny`:

TypeScriptPython

Copy code

```
return { behavior: "deny", message: "User cancelled" };
```

Copy code

```
return PermissionResultDeny(message="User cancelled")
```

Tip

`AskUserQuestion` is routed through `canUseTool`. Without a callback, the interaction cannot be completed and
the request errors instead of silently proceeding.

## The ExitPlanMode tool

When a session is in `plan` mode, Cortex Code stays in planning until the plan is approved. The approval request is
routed through your `canUseTool` callback with `toolName` / `tool_name` set to `"ExitPlanMode"`.

The input contains:

| Field | Description |
| --- | --- |
| `plan` | The proposed plan text the agent wants to execute |
| `question` | Optional additional approval prompt from the agent |

Expand

Show lessSee more

### Approving or rejecting a plan

Return `allow` to approve the plan. You can optionally include `updatedInput.message` to pass review context back
to the agent before it leaves plan mode.

Return `deny` to reject the plan. Use `message` when you want the agent to revise the plan with specific feedback.
Rejecting `ExitPlanMode` keeps the current turn in plan mode so the agent can update the plan and ask again.

Approving `ExitPlanMode` ends plan mode for the current turn. Subsequent turns resume the session’s normal
non-plan permission behavior, so later tool calls are evaluated the same way they would be outside plan mode.

### Recommended interaction pattern

Use plan mode as a review loop:

1. Start the session with `permissionMode: "plan"` (TypeScript) or `permission_mode="plan"` (Python).
2. Let the agent gather any missing information through `AskUserQuestion`.
3. When the agent calls `ExitPlanMode`, inspect the proposed `plan` text.
4. Return `deny` with a precise review message if the plan needs changes.
5. Return `allow` once the plan is acceptable. You can optionally include `updatedInput.message` /
   `updated_input["message"]` with reviewer guidance for execution.
6. After approval, later turns go back to the session’s normal non-plan permission behavior.

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  permissionMode: "plan",
  canUseTool: async (toolName, input, context) => {
    if (toolName === "ExitPlanMode") {
      const plan = String(input.plan ?? "");
      if (!plan.includes("test")) {
        return {
          behavior: "deny",
          message: "Add a test or verification step before leaving plan mode.",
        };
      }
      return {
        behavior: "allow",
        updatedInput: {
          message: "Approved. Run the verification step before the final answer.",
        },
      };
    }
    return { behavior: "allow" };
  },
});
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    CortexCodeAgentOptions,
    CortexCodeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    if tool_name == "ExitPlanMode":
        plan = str(tool_input.get("plan", ""))
        if "test" not in plan:
            return PermissionResultDeny(
                message="Add a test or verification step before leaving plan mode."
            )
        return PermissionResultAllow(
            updated_input={
                "message": "Approved. Run the verification step before the final answer."
            }
        )
    return PermissionResultAllow()

client = CortexCodeSDKClient(CortexCodeAgentOptions(
    cwd=".",
    permission_mode="plan",
    can_use_tool=can_use_tool,
))
```

### Review-loop example

The simplest review loop is to reject a weak plan once with specific feedback, then approve the revised plan:

TypeScriptPython

Copy code

```
let rejectedOnce = false;

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  permissionMode: "plan",
  canUseTool: async (toolName, input) => {
    if (toolName === "ExitPlanMode") {
      const plan = String(input.plan ?? "");
      if (!rejectedOnce) {
        rejectedOnce = true;
        return {
          behavior: "deny",
          message: "Add a verification step and say which file you will edit.",
        };
      }
      return {
        behavior: "allow",
        updatedInput: {
          message: `Approved plan: ${plan}`,
        },
      };
    }
    return { behavior: "allow" };
  },
});
```

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

state = {"rejected_once": False}

async def can_use_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    if tool_name == "ExitPlanMode":
        plan = str(tool_input.get("plan", ""))
        if not state["rejected_once"]:
            state["rejected_once"] = True
            return PermissionResultDeny(
                message="Add a verification step and say which file you will edit."
            )
        return PermissionResultAllow(
            updated_input={"message": f"Approved plan: {plan}"}
        )
    return PermissionResultAllow()
```

## Rule-based permissions

For common permission patterns, you can use rule-based configuration instead of writing callback logic. The
`allowedTools` and `disallowedTools` options let you define lists of tools that are automatically approved or
blocked:

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  allowedTools: ["Read", "Glob", "Grep", "Bash(npm test:*)"],
  disallowedTools: ["Write"],
});
```

Copy code

```
client = CortexCodeSDKClient(CortexCodeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Bash(npm test:*)"],
    disallowed_tools=["Write"],
))
```

`allowedTools` entries can include patterns. For example, `Bash(npm test:*)` auto-approves any Bash command
matching that pattern. `disallowedTools` entries block specific tools entirely.

These rules are evaluated by the CLI before the `canUseTool` callback. If a tool matches an allowed or disallowed
rule, the callback is not invoked for that tool.

## Combining with permission modes

The `canUseTool` callback works alongside permission modes. When both are set, the CLI’s built-in permission mode
filters run first, and your callback handles any remaining tool calls that need approval.

The available permission modes are:

| Mode | Description |
| --- | --- |
| `default` | Uses standard permission checks. In SDK sessions, control permission-checked tools with `allowedTools`, `disallowedTools`, or `canUseTool`. |
| `autoAcceptPlans` | Auto-approves plan requests and plan-exit confirmations. It does not bypass ordinary tool permissions. |
| `plan` | The agent plans changes but does not execute them without approval. With `canUseTool`, plan-mode approvals are routed through `ExitPlanMode`. Denying that request keeps planning active; approving it exits plan mode and later turns resume normal permissions. |
| `bypassPermissions` | Skip all permission checks. Requires `allowDangerouslySkipPermissions: true` (TypeScript) or `allow_dangerously_skip_permissions=True` (Python) as a safety flag. |

Expand

Show lessSee more

### Change permission mode during a session

You can change permission mode after the session starts. TypeScript exposes `setPermissionMode()` on both
`Query` and `CortexCodeSession`. Python exposes `set_permission_mode()` on `CortexCodeSDKClient`.

The updated mode applies to later turns after the control request is processed. It does not retroactively change a
tool call that is already running.

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
});

await session.setPermissionMode("plan");
await session.send("Review the repo and propose a plan before editing.");

await session.setPermissionMode("default");
await session.send("Now implement the approved change.");
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeAgentOptions, CortexCodeSDKClient

async with CortexCodeSDKClient(CortexCodeAgentOptions(cwd=".")) as client:
    await client.set_permission_mode("plan")
    await client.query("Review the repo and propose a plan before editing.")

    await client.set_permission_mode("default")
    await client.query("Now implement the approved change.")
```

## Hooks

Hooks let you intercept tool execution at different lifecycle stages. Unlike `canUseTool` which only controls
whether a tool runs, hooks can inspect tool results, inject context, and control agent flow.

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
            console.log(`About to run Bash: ${input.tool_input?.command}`);
            return {};  // Allow execution to proceed
          },
        ],
      },
    ],
    PostToolUse: [
      {
        hooks: [
          async (input, toolUseId, context) => {
            console.log(`Tool ${input.tool_name} completed`);
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

async def log_bash(input_data, tool_use_id, context):
    print(f"About to run Bash: {input_data.get('tool_input', {}).get('command')}")
    return {}

async def log_completion(input_data, tool_use_id, context):
    print(f"Tool {input_data.get('tool_name')} completed")
    return {}

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    hooks={
        "PreToolUse": [HookMatcher(matcher="Bash", hooks=[log_bash])],
        "PostToolUse": [HookMatcher(hooks=[log_completion])],
    },
)) as client:
    ...
```

### Hook events

| Event | When it fires |
| --- | --- |
| `PreToolUse` | Before a tool executes. Can block execution or modify input. |
| `PostToolUse` | After a tool completes successfully. |
| `UserPromptSubmit` | When a user prompt is submitted. |
| `Stop` | When the agent stops. |
| `SubagentStop` | When a sub-agent stops. |
| `Notification` | When the agent emits a notification. |
| `PermissionRequest` | When a tool permission request occurs. |
| `PreCompact` | Before context compaction. |

Expand

Show lessSee more

The `matcher` field on a hook entry is optional. When provided, it filters by the event’s match value:
tool name for `PreToolUse`, `PostToolUse`, and `PermissionRequest`; notification type for `Notification`;
and trigger for `PreCompact`. When omitted, the hook fires for all values for that event.

See the [TypeScript SDK reference](/user-guide/cortex-code-agent-sdk/typescript-reference) and
[Python SDK reference](/user-guide/cortex-code-agent-sdk/python-reference) for the complete hook input and
output type definitions.

## Choosing an approach

| Approach | When to use |
| --- | --- |
| `permissionMode: "bypassPermissions"` with safety flag | Sandboxed environments, CI pipelines, or fully trusted scenarios where you don’t need to review tool calls. Requires `allowDangerouslySkipPermissions: true` (TypeScript) or `allow_dangerously_skip_permissions=True` (Python). |
| `allowedTools` / `disallowedTools` | When you can express your permission policy as a static list of allowed or blocked tools |
| `canUseTool` callback | Production systems where you need to audit, filter, or modify tool calls before they execute |
| Permission mode only (no callback) | When `autoAcceptPlans` is sufficient and you do not need custom callback handling |
| Hooks | When you need to observe or react to tool results, inject context, or control agent flow beyond allow/deny decisions |

Expand

Show lessSee more

Note

The SDK does not bypass permissions or prompt interactively by default. If a permission-checked request reaches the
SDK and `canUseTool` is not provided, the request fails. To bypass permissions, you must explicitly set
`permissionMode: "bypassPermissions"` with the appropriate safety flag.

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
