# System prompts

System prompts let you constrain agent behavior, add domain-specific context, or set the tone and style of
responses.

By default, the SDK uses a built-in system prompt that provides the agent with its core capabilities, including
file editing, code search, and shell access. You can either replace this prompt entirely or append additional
instructions to it.

## Replace the default prompt

Pass a string to the `systemPrompt` option to fully replace the built-in system prompt. Use this when you
need complete control over the agent’s behavior and don’t want any of the default instructions.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  systemPrompt: `You are a code review assistant.
Prioritize finding bugs, security issues, and maintainability risks.
Explain the issue and suggest concrete fixes.`,
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    system_prompt="""You are a code review assistant.
Prioritize finding bugs, security issues, and maintainability risks.
Explain the issue and suggest concrete fixes.""",
)) as client:
    await client.query("Review the auth module for security issues")
    async for msg in client.receive_response():
        pass
```

Warning

Replacing the default prompt removes all built-in instructions, including tool usage guidance and safety
guardrails. Only replace the prompt when you need full control over agent behavior.

## Append to the default prompt

To keep the built-in capabilities while adding your own instructions, use a system prompt preset object with the
`append` field. The preset name is implicit, so you only need `{"type": "preset", "append": ...}`.
This adds your instructions after the default system prompt.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  systemPrompt: {
    type: "preset",
    append: "Focus on Python files. Always run pytest after making changes.",
  },
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    system_prompt={
        "type": "preset",
        "append": "Focus on Python files. Always run pytest after making changes.",
    },
)) as client:
    await client.query("Fix the failing test in test_auth.py")
    async for msg in client.receive_response():
        pass
```

Both SDKs also provide an append-only shorthand:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  appendSystemPrompt: "Focus on Python files. Always run pytest after making changes.",
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeAgentOptions

options = CortexCodeAgentOptions(
    append_system_prompt="Focus on Python files. Always run pytest after making changes.",
)
```

## Common patterns

### Review-focused code reviewer

Bias the agent toward analysis-first code review behavior:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  appendSystemPrompt: `You are a code reviewer. Follow these rules:
- Prioritize reading code and analyzing behavior before proposing changes.
- Do not modify files unless the user explicitly asks for an implementation.
- Identify bugs, security issues, and style problems.
- Provide specific line numbers and suggested fixes in your response.`,
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    system_prompt={
        "type": "preset",
        "append": """You are a code reviewer. Follow these rules:
- Prioritize reading code and analyzing behavior before proposing changes.
- Do not modify files unless the user explicitly asks for an implementation.
- Identify bugs, security issues, and style problems.
- Provide specific line numbers and suggested fixes in your response.""",
    },
)) as client:
    ...
```

### Domain-specific expert

Focus the agent on a particular technology or domain:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  appendSystemPrompt: `You are a SQL and database specialist working with Snowflake.
- Write efficient SQL queries optimized for Snowflake's columnar storage.
- Use Snowflake-specific features like VARIANT columns and FLATTEN.
- Always include LIMIT clauses in exploratory queries.
- Validate SQL syntax before suggesting changes.`,
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    system_prompt={
        "type": "preset",
        "append": """You are a SQL and database specialist working with Snowflake.
- Write efficient SQL queries optimized for Snowflake's columnar storage.
- Use Snowflake-specific features like VARIANT columns and FLATTEN.
- Always include LIMIT clauses in exploratory queries.
- Validate SQL syntax before suggesting changes.""",
    },
)) as client:
    ...
```

### Style enforcer

Ensure the agent follows specific coding standards:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  appendSystemPrompt: `Enforce these coding standards in all changes:
- Use TypeScript strict mode conventions.
- Prefer const over let; never use var.
- All functions must have explicit return types.
- Use async/await instead of raw Promises.
- Run "npm run lint" after every file change.`,
});
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(
    system_prompt={
        "type": "preset",
        "append": """Enforce these coding standards in all changes:
- Follow PEP 8 style guidelines.
- Use type hints for all function signatures.
- Prefer f-strings over .format() or % formatting.
- Run "ruff check" after every file change.""",
    },
)) as client:
    ...
```

## Best practices

### When to append vs. replace

| Append to the default prompt | Replace the default prompt |
| --- | --- |
| You want to add domain context or constraints | You need full control over agent behavior |
| You want to keep built-in tool usage guidance | You are building a highly specialized agent |
| You want to maintain safety guardrails | The default instructions conflict with your use case |

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
