# Cortex Code Agent SDK reference – TypeScript

This topic provides the complete API reference for the Cortex Code Agent SDK for TypeScript, including all functions,
types, and interfaces.

## Installation

Copy code

```
npm install cortex-code-agent-sdk
```

Requires Node.js 18 or later. The package is ESM-only.
The SDK expects the Cortex Code CLI to be installed separately. If it is not on
your `PATH`, set `CORTEX_CODE_CLI_PATH=/path/to/cortex` or pass `cliPath`
in the session options.

## Functions

### query()

The primary function for interacting with Cortex Code. Creates an async generator that streams messages as they arrive.

Copy code

```
function query({
  prompt,
  options,
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: CortexCodeSessionOptions;
}): Query;
```

**Parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `prompt` | `string | AsyncIterable<SDKUserMessage>` | A single user prompt, or an async iterable of SDK user messages for streaming input |
| `options` | `CortexCodeSessionOptions | undefined` | Optional configuration object (see [Options](#label-cortex-code-agent-sdk-ts-options)) |

Expand

Show lessSee more

**Returns**

A `Query` object that extends `AsyncGenerator<CortexCodeEvent>` with additional control methods.

**Example**

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Fix the bug in utils.py",
  options: { cwd: "/path/to/project" },
})) {
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  }
  if (message.type === "result") {
    console.log("Done:", message.subtype);
  }
}
```

### createCortexCodeSession()

Creates a persistent session for multi-turn conversations.

Copy code

```
function createCortexCodeSession(
  options: CortexCodeSessionOptions
): Promise<CortexCodeSession>;
```

**Example**

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  model: "claude-sonnet-4-6",
  permissionMode: "bypassPermissions",
  allowDangerouslySkipPermissions: true,
});

await session.send("What files are here?");
for await (const event of session.stream()) {
  if (event.type === "assistant") { /* handle */ }
  if (event.type === "result") break;
}

// Send another prompt (same context)
await session.send("Now refactor the main function");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

await session.close();
```

## Query object

Returned by `query()`. Extends `AsyncGenerator<CortexCodeEvent>`.

| Method | Description |
| --- | --- |
| `interrupt(): Promise<void>` | Send SIGINT to the underlying process |
| `setPermissionMode(mode: PermissionMode): Promise<void>` | Change the permission mode for later turns in the active query |
| `setModel(model: string): Promise<void>` | Change the model for subsequent turns |
| `initializationResult(): Promise<QueryInitializationResult>` | Return initialize-handshake metadata from the CLI |
| `supportedCommands(): Promise<SlashCommand[]>` | Return slash command metadata from the initialize response, when advertised by the CLI |
| `supportedModels(): Promise<ModelInfo[]>` | Return model metadata from the initialize response, when advertised by the CLI |
| `supportedAgents(): Promise<AgentInfo[]>` | Return custom agent metadata from the initialize response, when advertised by the CLI |
| `accountInfo(): Promise<AccountInfo>` | Return account metadata from the initialize response, when advertised by the CLI |
| `streamInput(stream: AsyncIterable<SDKUserMessage>): Promise<void>` | Stream additional SDK user messages into the active query |
| `stopTask(taskId: string): Promise<void>` | Cancel a running background task by ID |
| `close(): void` | Close the session and terminate the process |

Expand

Show lessSee more

## CortexCodeSession interface

Returned by `createCortexCodeSession()`. Supports multi-turn conversations and implements `AsyncDisposable`
for use with `await using` (Node.js 24+).

| Property / Method | Description |
| --- | --- |
| `pid: number | undefined` | PID of the underlying CLI process |
| `send(message: string | SDKUserMessage): Promise<void>` | Send a plain-text or structured SDK user message |
| `stream(): AsyncGenerator<CortexCodeEvent>` | Stream events from the agent |
| `initializationResult(): Promise<QueryInitializationResult>` | Return initialize-handshake metadata from the CLI |
| `interrupt(): Promise<void>` | Send interrupt signal |
| `setPermissionMode(mode: PermissionMode): Promise<void>` | Change the permission mode for later turns in the session |
| `setModel(model: string): Promise<void>` | Change model mid-session |
| `stopTask(taskId: string): Promise<void>` | Cancel a running background task by ID |
| `close(): Promise<void>` | End session and terminate process |
| `[Symbol.asyncDispose](): Promise<void>` | Calls `close()`. Enables `await using session = ...` syntax. |

Expand

Show lessSee more

## Options

Configuration passed to `query()` or `createCortexCodeSession()`.

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `cwd` | `string` | Current process working directory | Working directory for the session. If omitted, the SDK inherits the current process working directory. |
| `model` | `string` | CLI default | Model to use. Use `"auto"` for automatic selection, or a specific identifier like `"claude-sonnet-4-6"`. See [Supported models](/user-guide/cortex-code-agent-sdk/cortex-code-agent-sdk#label-cortex-code-agent-sdk-supported-models). |
| `connection` | `string` | CLI default | Snowflake connection name from Snowflake CLI connection settings, typically `~/.snowflake/connections.toml`, with `~/.snowflake/config.toml` also supported for existing setups. If omitted, the CLI uses `default_connection_name` from the TOML file. See [Configuring connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| `profile` | `string` | `undefined` | Profile name (loads from `~/.snowflake/cortex/profiles/`) |
| `resume` | `string` | `undefined` | Session ID to resume a previous conversation |
| `continue` | `boolean` | `false` | Continue the most recent conversation. Resumes the last session without needing a session ID. |
| `forkSession` | `boolean` | `false` | Fork a resumed session into a new session ID instead of continuing in-place. Use with `resume`. |
| `sessionId` | `string` | `undefined` | Explicit session ID for the conversation. If omitted, the CLI generates one automatically. |
| `permissionMode` | `string` | `"default"` | `"default"` | `"autoAcceptPlans"` | `"plan"` | `"bypassPermissions"`. Note: `"bypassPermissions"` requires `allowDangerouslySkipPermissions: true`. In `"plan"` mode, `AskUserQuestion` and `ExitPlanMode` can be routed through `canUseTool`; denying `ExitPlanMode` keeps planning active, and approving it exits plan mode so later turns resume normal permissions. |
| `allowDangerouslySkipPermissions` | `boolean` | `false` | Safety flag required when using `permissionMode: "bypassPermissions"`. This flag alone does not bypass permissions; it only allows the bypass when explicitly requested via permissionMode. |
| `allowedTools` | `string[]` | `undefined` | Tools to auto-approve without prompting |
| `disallowedTools` | `string[]` | `undefined` | Tools to always deny |
| `canUseTool` | [CanUseTool](#label-cortex-code-agent-sdk-ts-canuse) | `undefined` | Custom permission handler called before each tool execution. See [canUseTool callback](#label-cortex-code-agent-sdk-ts-canuse). |
| `permissionPromptToolName` | `string` | `undefined` | MCP tool name used for permission prompts. When `canUseTool` is provided, the SDK automatically uses `"stdio"`. |
| `maxTurns` | `number` | `undefined` | Maximum number of agentic turns before stopping. When reached, the session emits an `error_max_turns` result. |
| `effort` | `string` | `undefined` | Thinking effort level for the model. One of `"minimal"`, `"low"`, `"medium"`, `"high"`, or `"max"`. |
| `additionalDirectories` | `string[]` | `undefined` | Additional working directories to make available to the session |
| `plugins` | `Array<string | { type: "local"; path: string }>` | `undefined` | Plugin directories to load. Accepts paths as strings or `{ type: "local", path: "..." }` objects. |
| `env` | `Record<string, string | undefined>` | `undefined` | Environment variables merged into the spawned process environment. Set a key to `undefined` to remove an inherited variable. |
| `abortController` | `AbortController` | `undefined` | Send an interrupt signal by calling `abort()` on the controller. The session stays alive for further prompts. Equivalent to pressing ESC in the CLI. |
| `systemPrompt` | `string | SystemPromptPreset` | `undefined` | Custom system prompt. Pass a string to replace the default entirely, or a [SystemPromptPreset](#label-cortex-code-agent-sdk-ts-systemprompt) to extend it. |
| `appendSystemPrompt` | `string` | `undefined` | Text appended to the default system prompt. Use this to add instructions without replacing the built-in prompt. |
| `hooks` | `Partial<Record<HookEvent, HookMatcher[]>>` | `undefined` | Hook callbacks for intercepting tool execution and other agent events. See [Hooks](#label-cortex-code-agent-sdk-ts-hooks). |
| `settingSources` | `SettingSource[]` | `undefined` | Setting sources to load. Array of `"user"`, `"project"`, and/or `"local"`. |
| `includePartialMessages` | `boolean` | `false` | Include token-level streaming events |
| `mcpServers` | `Record<string, Record<string, unknown>>` | `undefined` | External MCP server configurations. Keys are server names, values are server configs (for example, `{ command: "node", args: ["server.js"] }`). See [MCP servers](/user-guide/cortex-code-agent-sdk/mcp-custom-tools). |
| `noMcp` | `boolean` | `false` | Disable MCP servers |
| `outputFormat` | `{ type: "json_schema"; schema: object }` | `undefined` | Structured output – validates final response against JSON Schema |
| `cliPath` | `string` | `process.env.CORTEX_CODE_CLI_PATH ?? "cortex"` | Path to custom CLI binary. If omitted, the SDK first checks `CORTEX_CODE_CLI_PATH` and otherwise falls back to `cortex` on `PATH`. |
| `extraArgs` | `Record<string, string | null>` | `undefined` | Additional CLI arguments as key-value pairs |

Expand

Show lessSee more

### canUseTool callback

A custom permission handler called before each tool execution. Return an allow or deny result to control
whether the tool call proceeds.

For many ordinary tool permission checks, the callback input contains fields such as
`{ action, resource }`. The allow/deny result and optional deny message are used for these checks.
`updatedInput` is used for SDK-routed pseudo-tools such as `AskUserQuestion` and `ExitPlanMode`, which contain
tool-specific fields.

Copy code

```
type CanUseTool = (
  toolName: string,
  input: Record<string, unknown>,
  context: ToolPermissionContext,
) => Promise<PermissionResult>;

type ToolPermissionContext = {
  signal: AbortSignal;
  blockedPath?: string;
  decisionReason?: string;
  toolUseID: string;
  agentID?: string;
};

type PermissionResult = PermissionResultAllow | PermissionResultDeny;

type PermissionResultAllow = {
  behavior: "allow";
  updatedInput?: Record<string, unknown>;
  toolUseID?: string;
};

type PermissionResultDeny = {
  behavior: "deny";
  message?: string;
  interrupt?: boolean;
  toolUseID?: string;
};
```

**Example**

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
 canUseTool: async (toolName, input, context) => {
   if (toolName === "Write" && String(input.resource).endsWith(".env")) {
     return { behavior: "deny", message: "Destructive commands not allowed" };
   }
   return { behavior: "allow" };
  },
});
```

### SystemPromptPreset

Instead of replacing the system prompt entirely, use a preset object to extend the built-in prompt.

Copy code

```
type SystemPrompt = string | SystemPromptPreset;

type SystemPromptPreset = {
  type: "preset";
  append?: string;
};
```

**Example**

Copy code

```
// Replace the system prompt entirely
const session1 = await createCortexCodeSession({
  cwd: process.cwd(),
  systemPrompt: "You are a code reviewer. Prioritize finding issues and suggesting fixes.",
});

// Extend the default prompt
const session2 = await createCortexCodeSession({
  cwd: process.cwd(),
  systemPrompt: {
    type: "preset",
    append: "Always write tests for any code you create.",
  },
});
```

### Hooks

Hooks let you intercept agent events such as tool execution. Each hook event maps to an array of matchers,
and each matcher contains an optional pattern and one or more callbacks.

Copy code

```
type HookEvent =
  | "PreToolUse" | "PostToolUse" | "UserPromptSubmit"
  | "Stop" | "SubagentStop" | "PreCompact"
  | "Notification" | "PermissionRequest";

type HookMatcher = {
  matcher?: string;       // Match value pattern (optional)
  hooks: HookCallback[];
  timeout?: number;       // Timeout in seconds
};

type HookCallback = (
  input: HookInput,
  toolUseId: string | null,
  context: HookContext,
) => Promise<HookOutput>;
```

**Example**

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  hooks: {
    PostToolUse: [
      {
        matcher: "Write",
        hooks: [
          async (input, toolUseId, context) => {
            console.log("File written:", input.tool_input?.file_path);
            return { continue: true };
          },
        ],
      },
    ],
  },
});
```

## Message types

Events yielded by `query()` and `session.stream()`:

### SDKAssistantMessage

Emitted when the agent produces a response. Contains one or more content blocks.

Copy code

```
type SDKAssistantMessage = {
  type: "assistant";
  content: ContentBlock[];
  message: {
    role: "assistant";
    content: ContentBlock[];
    model: string;
  };
  session_id: string;
}
```

### SDKResultMessage

Emitted when the agent finishes a turn. Check `subtype` for success or error.

Copy code

```
type SDKResultMessage =
  | { type: "result"; subtype: "success"; is_error: false; result: string; session_id: string; }
  | { type: "result"; subtype: "error_during_execution" | "error_max_turns" | "error_max_budget_usd";
      is_error: true; errors: string[]; session_id: string; }
```

### SDKUserMessage

Echoed back when a user message is processed.

Copy code

```
type SDKUserMessage = {
  type: "user";
  message: { role: "user"; content: ContentBlock[]; };
  session_id: string;
}
```

### SDKSystemMessage

System events such as session initialization.

Copy code

```
type SDKSystemMessage = {
  type: "system";
  subtype: string;  // e.g. "init"
  session_id: string;
}
```

### Content blocks

| Type | Fields |
| --- | --- |
| `TextBlock` | `{ type: "text", text: string }` |
| `ThinkingBlock` | `{ type: "thinking", thinking: string }` |
| `ToolUseBlock` | `{ type: "tool_use", id: string, name: string, input: object }` |
| `ToolResultBlock` | `{ type: "tool_result", tool_use_id: string, content: string }` |

Expand

Show lessSee more

### Streaming events

| Type | Description |
| --- | --- |
| `SDKPartialAssistantMessage` | Partial text/thinking streaming (requires `includePartialMessages: true`) |
| `StdErrEvent` | `{ type: "stderr", data: string }` – stderr from the CLI |
| `ParseErrorEvent` | `{ type: "parse_error", raw: string, error: string }` |

Expand

Show lessSee more

`SDKPartialAssistantMessage` is emitted for partial text and thinking blocks. Complete tool calls still arrive as
`AssistantMessage` blocks, and tool results still arrive as `UserMessage` blocks.

## Structured output

Force the agent to return a response matching a JSON Schema:

Copy code

```
const result = query({
  prompt: "Analyze the codebase and return a summary",
  options: {
    cwd: process.cwd(),
    outputFormat: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          languages: { type: "array", items: { type: "string" } },
          file_count: { type: "number" },
          summary: { type: "string" },
        },
        required: ["languages", "file_count", "summary"],
      },
    },
  },
});

for await (const msg of result) {
  if (msg.type === "result" && msg.subtype === "success") {
    // The final text content will be valid JSON matching the schema
  }
}
```

For more information, see [Structured output](/user-guide/cortex-code-agent-sdk/structured-output).

## Error handling

Copy code

```
try {
  for await (const message of query({ prompt: "...", options: { cwd: "." } })) {
    if (message.type === "result" && message.is_error) {
      console.error("Agent error:", message.errors.join(", "));
    }
  }
} catch (err) {
  // Thrown if the CLI binary is not found, session fails to start, etc.
  console.error("SDK error:", err.message);
}
```

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
