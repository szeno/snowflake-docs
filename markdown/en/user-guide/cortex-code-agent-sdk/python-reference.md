# Cortex Code Agent SDK reference – Python

This topic provides the complete API reference for the Cortex Code Agent SDK for Python, including all functions,
classes, and types.

## Installation

Copy code

```
pip install cortex-code-agent-sdk
```

Requires Python 3.10 or later. Dependencies: `anyio`, `mcp`, `typing_extensions`.
Import the package as `cortex_code_agent_sdk`.
The SDK expects the Cortex Code CLI to be installed separately. If it is not on
your `PATH`, set `CORTEX_CODE_CLI_PATH=/path/to/cortex` or pass `cli_path`
in `CortexCodeAgentOptions`.

## Functions

### query()

The primary function for interacting with Cortex Code. Returns an async iterator that yields messages as they arrive.

Copy code

```
async def query(
    *,
    prompt: str | AsyncIterable[dict],
    options: CortexCodeAgentOptions | None = None,
    transport: Transport | None = None,
) -> AsyncIterator[Message]: ...
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `prompt` | `str | AsyncIterable[dict]` | User prompt string, or async iterable of message dicts for streaming input |
| `options` | `CortexCodeAgentOptions | None` | Configuration options. Defaults to `CortexCodeAgentOptions()` |
| `transport` | `Transport | None` | Custom transport. Defaults to subprocess CLI transport |

Expand

Show lessSee more

**Returns**

An async iterator yielding `Message` objects (`AssistantMessage`, `ResultMessage`, `UserMessage`,
`SystemMessage`, `StreamEvent`).

**Example**

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, AssistantMessage, ResultMessage, CortexCodeAgentOptions

async def main():
    async for message in query(
        prompt="Fix the bug in utils.py",
        options=CortexCodeAgentOptions(cwd="/path/to/project"),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="")
        elif isinstance(message, ResultMessage):
            print(f"\nDone: {message.subtype}")

asyncio.run(main())
```

## CortexCodeSDKClient

For multi-turn interactive conversations. Supports the async context manager protocol.

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, AssistantMessage

async with CortexCodeSDKClient(CortexCodeAgentOptions(permission_mode="bypassPermissions", allow_dangerously_skip_permissions=True)) as client:
    # First turn
    await client.query("What files are in this directory?")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if hasattr(b, "text"):
                    print(b.text, end="")

    # Second turn (context preserved)
    await client.query("Now refactor the main function")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if hasattr(b, "text"):
                    print(b.text, end="")
```

### Methods

| Method | Description |
| --- | --- |
| `connect()` | Connect to the CLI process and keep the session open for later turns. |
| `query(prompt, session_id?)` | Send a prompt to the agent |
| `receive_messages()` | Yield all messages from the agent |
| `receive_response()` | Yield messages until a `ResultMessage` (inclusive) |
| `interrupt()` | Send interrupt signal |
| `set_permission_mode(mode)` | Change the permission mode for later turns in the conversation |
| `set_model(model)` | Change model during conversation |
| `stop_task(task_id)` | Stop a running subagent task |
| `disconnect()` | Disconnect from the CLI process |

Expand

Show lessSee more

## Options

Configuration passed to `query()` or `CortexCodeSDKClient`.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `cwd` | `str | Path | None` | `None` | Working directory for the session |
| `model` | `str | None` | `None` | Model to use. Use `"auto"` for automatic selection, or a specific identifier like `"claude-sonnet-4-6"`. See [Supported models](/user-guide/cortex-code-agent-sdk/cortex-code-agent-sdk#label-cortex-code-agent-sdk-supported-models). |
| `connection` | `str | None` | `None` | Snowflake connection name from Snowflake CLI connection settings, typically `~/.snowflake/connections.toml`, with `~/.snowflake/config.toml` also supported for existing setups. If omitted, the CLI uses `default_connection_name` from the TOML file. See [Configuring connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| `profile` | `str | None` | `None` | Profile name (loads from `~/.snowflake/cortex/profiles/`) |
| `permission_mode` | `PermissionMode | None` | `None` | `"default"` | `"autoAcceptPlans"` | `"plan"` | `"bypassPermissions"`. Note: `"bypassPermissions"` requires `allow_dangerously_skip_permissions=True`. In `"plan"` mode, `AskUserQuestion` and `ExitPlanMode` can be routed through `can_use_tool`; denying `ExitPlanMode` keeps planning active, and approving it exits plan mode so later turns resume normal permissions. |
| `allow_dangerously_skip_permissions` | `bool` | `False` | Safety flag required when using `permission_mode="bypassPermissions"`. This flag alone does not bypass permissions; it only allows the bypass when explicitly requested via permission\_mode. |
| `allowed_tools` | `list[str]` | `[]` | Tools to auto-approve without prompting |
| `disallowed_tools` | `list[str]` | `[]` | Tools to always deny |
| `max_turns` | `int | None` | `None` | Limit the number of agent turns per query |
| `effort` | `str | None` | `None` | Model effort level: `"minimal"` | `"low"` | `"medium"` | `"high"` | `"max"` |
| `system_prompt` | `str | SystemPromptPreset | None` | `None` | Custom system prompt. Pass a string for a full override, or `{"type": "preset", "append": "extra text"}` to append to the default prompt. |
| `continue_conversation` | `bool` | `False` | Continue the most recent session instead of starting a new one |
| `resume` | `str | None` | `None` | Session ID to resume a previous conversation |
| `fork_session` | `bool` | `False` | When resuming, fork to a new session ID instead of continuing the previous session |
| `add_dirs` | `list[str | Path]` | `[]` | Additional directories to add to the agent’s context |
| `env` | `dict[str, str]` | `{}` | Environment variables to pass to the CLI process |
| `plugins` | `list[SdkPluginConfig]` | `[]` | Plugin configurations. Currently supports local plugins: `{"type": "local", "path": "/path/to/plugin"}` |
| `abort_event` | `asyncio.Event | None` | `None` | An `asyncio.Event` that, when set, sends an interrupt to the running agent. The session stays alive for further prompts. Python equivalent of `AbortController` in the TypeScript SDK. |
| `mcp_servers` | `dict[str, McpServerConfig]` | `{}` | External MCP server configurations. Pass a dict that maps server names to stdio, HTTP, or SSE configs. The current SDK transport supports dict-based MCP configuration only. |
| `hooks` | `dict | None` | `None` | Hook event handlers (see [Hooks](#label-cortex-code-agent-sdk-py-hooks)) |
| `can_use_tool` | `CanUseTool | None` | `None` | Custom tool permission callback (see [Tool permissions](#label-cortex-code-agent-sdk-py-permissions)) |
| `include_partial_messages` | `bool` | `False` | Include token-level streaming events (`StreamEvent`) |
| `output_format` | `dict | None` | `None` | Structured output format. Example: `{"type": "json_schema", "schema": {...}}` |
| `no_mcp` | `bool` | `False` | Disable MCP servers |
| `session_id` | `str | None` | `None` | Explicit session ID to use |
| `setting_sources` | `list[str] | None` | `None` | Setting sources to load: `"user"` | `"project"` | `"local"` |
| `cli_path` | `str | Path | None` | `os.environ.get("CORTEX_CODE_CLI_PATH") or "cortex"` | Path to CLI binary. If omitted, the SDK first checks `CORTEX_CODE_CLI_PATH` and otherwise falls back to `cortex` on `PATH`. |
| `extra_args` | `dict[str, str | None]` | `{}` | Additional CLI flags as key-value pairs. Use `None` value for boolean flags. |
| `stderr` | `Callable[[str], None] | None` | `None` | Callback invoked with each line of CLI stderr output |

Expand

Show lessSee more

## Message types

### AssistantMessage

Emitted when the agent produces a response. Contains one or more content blocks.

Copy code

```
@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str
    parent_tool_use_id: str | None = None
    error: AssistantMessageError | None = None
```

`AssistantMessageError` is one of: `"authentication_failed"`, `"billing_error"`, `"rate_limit"`,
`"invalid_request"`, `"server_error"`, `"unknown"`.

### ResultMessage

Emitted when the agent finishes a turn. Check `subtype` and `is_error` for success or failure.

Copy code

```
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    duration_api_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    stop_reason: str | None = None
    total_cost_usd: float | None = None
    usage: dict[str, Any] | None = None
    result: str | None = None
    structured_output: Any = None
```

### UserMessage

Echoed back when a user message is processed.

Copy code

```
@dataclass
class UserMessage:
    content: str | list[ContentBlock]
    uuid: str | None = None
    parent_tool_use_id: str | None = None
    tool_use_result: dict[str, Any] | None = None
```

### SystemMessage

System events such as session initialization and task updates.

Copy code

```
@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]
```

The SDK also provides specialized subclasses for task-related system messages:

| Subclass | Description |
| --- | --- |
| `TaskStartedMessage` | Emitted when a subagent task starts. Fields: `task_id`, `description`, `uuid`, `session_id`, `tool_use_id`, `task_type`. |
| `TaskProgressMessage` | Emitted while a task is running. Fields: `task_id`, `description`, `usage` (`TaskUsage`), `uuid`, `session_id`, `last_tool_name`. |
| `TaskNotificationMessage` | Emitted when a task completes, fails, or is stopped. Fields: `task_id`, `status` (`"completed"` | `"failed"` | `"stopped"`), `output_file`, `summary`, `uuid`, `session_id`, `usage`. |

Expand

Show lessSee more

These subclasses extend `SystemMessage`, so existing `isinstance(msg, SystemMessage)` checks continue to match.

### StreamEvent

Partial message updates during token-level streaming. Requires `include_partial_messages=True`.

Copy code

```
@dataclass
class StreamEvent:
    uuid: str
    session_id: str
    event: dict[str, Any]   # Partial text/thinking stream event from Cortex Code
    parent_tool_use_id: str | None = None
```

`StreamEvent` is emitted for partial text and thinking blocks. Complete tool calls still arrive as
`AssistantMessage` content blocks, and tool results still arrive as `UserMessage` content blocks.

### Content blocks

| Type | Fields |
| --- | --- |
| `TextBlock` | `.type = "text"`, `.text: str` |
| `ThinkingBlock` | `.type = "thinking"`, `.thinking: str`, `.signature: str` |
| `ToolUseBlock` | `.type = "tool_use"`, `.id: str`, `.name: str`, `.input: dict` |
| `ToolResultBlock` | `.type = "tool_result"`, `.tool_use_id: str`, `.content: str | list | None`, `.is_error: bool | None` |

Expand

Show lessSee more

## Hooks

Hooks let you intercept lifecycle events for logging, validation, or custom behavior.

### Configuring hooks

Hooks are configured via the `hooks` option on `CortexCodeAgentOptions`. Each hook event maps to a list of
`HookMatcher` objects.

Copy code

```
from cortex_code_agent_sdk import CortexCodeAgentOptions, HookMatcher

async def my_pre_tool_hook(input_data, tool_use_id, context):
    print(f"Tool {input_data['tool_name']} about to run")
    return {"continue_": True}

options = CortexCodeAgentOptions(
    hooks={
        "PreToolUse": [
            HookMatcher(
                matcher="Bash",          # Only match Bash tool, or None for all
                hooks=[my_pre_tool_hook],
                timeout=30.0,            # Timeout in seconds (default: 60)
            ),
        ],
    },
)
```

### Hook callback signature

Copy code

```
HookCallback = Callable[
    [HookInput, str | None, HookContext],
    Awaitable[HookJSONOutput],
]
```

- **input**: Strongly-typed hook input (see table below)
- **tool\_use\_id**: Optional tool use identifier
- **context**: `HookContext` with a `signal` field (reserved for future abort signal support)

### Hook events

| Event | Input Type | Description |
| --- | --- | --- |
| `PreToolUse` | `PreToolUseHookInput` | Before a tool is executed. Fields: `tool_name`, `tool_input`, `tool_use_id`. |
| `PostToolUse` | `PostToolUseHookInput` | After a tool completes. Fields: `tool_name`, `tool_input`, `tool_response`, `tool_use_id`. |
| `UserPromptSubmit` | `UserPromptSubmitHookInput` | When user submits a prompt. Fields: `prompt`. |
| `Stop` | `StopHookInput` | When the agent stops. Fields: `stop_hook_active`. |
| `SubagentStop` | `SubagentStopHookInput` | When a subagent finishes. Fields: `stop_hook_active`. |
| `Notification` | `NotificationHookInput` | On notification events. Fields: `message`, `notification_type`. |
| `PermissionRequest` | `PermissionRequestHookInput` | When a tool requests permission. Fields: `tool_name`, `tool_input`. |
| `PreCompact` | `PreCompactHookInput` | Before context compaction. Fields: `trigger` (`"manual"` | `"auto"`), `custom_instructions`. |

Expand

Show lessSee more

All hook inputs include base fields: `session_id`, `transcript_path`, `cwd`, and optionally
`permission_mode`.

### Hook output

Hook callbacks return a synchronous output object:

Copy code

```
# Synchronous output
SyncHookJSONOutput = TypedDict("SyncHookJSONOutput", {
    "continue_": bool,               # Whether agent should proceed (default: True)
    "stopReason": str,                # Message shown when continue_ is False
    "decision": Literal["block"],     # Block the action
    "reason": str,                    # Feedback for the agent
    "hookSpecificOutput": ...,        # Event-specific controls
}, total=False)
```

Note

The Python SDK uses `continue_` (with a trailing underscore) to avoid the Python keyword conflict. This is
automatically converted to `continue` when sent to the CLI.

## Tool permissions

The `can_use_tool` callback lets you programmatically control tool permissions.

For many ordinary tool permission checks, the callback input contains fields such as
`{"action": ..., "resource": ...}`. The allow/deny result and optional deny message are used for these checks.
`updated_input` is used for SDK-routed pseudo-tools such as `AskUserQuestion` and `ExitPlanMode`, which
contain tool-specific fields.

Copy code

```
from typing import Any

from cortex_code_agent_sdk import (
    CortexCodeAgentOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def my_permission_handler(
    tool_name: str,
    tool_input: dict[str, Any],
    context: ToolPermissionContext,
) -> PermissionResultAllow | PermissionResultDeny:
    if tool_name == "Write" and str(tool_input.get("resource", "")).endswith(".env"):
        return PermissionResultDeny(message="Writing env files is not allowed")
    return PermissionResultAllow()

options = CortexCodeAgentOptions(can_use_tool=my_permission_handler)
```

**Types**

Copy code

```
CanUseTool = Callable[
    [str, dict[str, Any], ToolPermissionContext],
    Awaitable[PermissionResult],
]

@dataclass
class ToolPermissionContext:
    signal: Any | None = None
    blocked_path: str | None = None
    decision_reason: str | None = None
    tool_use_id: str = ""
    agent_id: str | None = None

@dataclass
class PermissionResultAllow:
    behavior: Literal["allow"] = "allow"
    updated_input: dict[str, Any] | None = None
    tool_use_id: str | None = None

@dataclass
class PermissionResultDeny:
    behavior: Literal["deny"] = "deny"
    message: str = ""
    interrupt: bool = False
    tool_use_id: str | None = None
```

## MCP server configuration

The `mcp_servers` option accepts a dict mapping server names to external MCP server configurations:

| Config type | Description |
| --- | --- |
| `McpStdioServerConfig` | External process via stdio. Fields: `command`, `args`, `env`. |
| `McpSSEServerConfig` | Server-sent events. Fields: `type="sse"`, `url`, `headers`. |
| `McpHttpServerConfig` | HTTP transport. Fields: `type="http"`, `url`, `headers`. |

Expand

Show lessSee more

**Example**

Copy code

```
options = CortexCodeAgentOptions(
    mcp_servers={
        "external": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
         },
     },
 )
```

## Error handling

Copy code

```
from cortex_code_agent_sdk import (
    query, CortexCodeAgentOptions, ResultMessage,
    CortexCodeSDKError, CLINotFoundError, CLIConnectionError,
)

try:
    async for message in query(prompt="...", options=CortexCodeAgentOptions()):
        if isinstance(message, ResultMessage) and message.is_error:
            print(f"Agent error ({message.subtype}): {message.result}")
except CLINotFoundError:
    print("Cortex CLI not found. Is it installed and on PATH?")
except CLIConnectionError:
    print("Failed to connect to CLI process")
except CortexCodeSDKError as e:
    print(f"SDK error: {e}")
```

### Error types

| Exception | Description |
| --- | --- |
| `CortexCodeSDKError` | Base exception for all SDK errors |
| `CLINotFoundError` | CLI binary not found on PATH |
| `CLIConnectionError` | Failed to connect to or communicate with CLI |
| `ProcessError` | CLI process exited unexpectedly |
| `CLIJSONDecodeError` | Failed to parse JSON from CLI output |

Expand

Show lessSee more

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
