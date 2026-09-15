# Cortex Code Agent SDK quickstart

This topic walks you through building an AI agent that reads a data pipeline script, finds bugs, and fixes them
automatically using the Cortex Code Agent SDK.

**What you will do:**

1. Set up a project with the Cortex Code Agent SDK.
2. Create a data pipeline script with some bugs.
3. Run an agent that finds and fixes the bugs without manual intervention.

## Prerequisites

- **Node.js 22+** (for TypeScript) or **Python 3.10+** (for Python).
- **Snowflake connection** configured through Snowflake CLI connection settings, typically in
  `~/.snowflake/connections.toml`, with `~/.snowflake/config.toml` also supported for existing setups
  (see [Configuring connections](/developer-guide/snowflake-cli/connecting/configure-connections)):

  Copy code

  ```
  [my-connection]
  account = "myorg-myaccount"
  user = "myuser"
  authenticator = "externalbrowser"
  ```

  **For CI/CD pipelines** (GitLab, GitHub Actions, and similar): instead of a config file, you can
  authenticate using environment variables. Set the generic Snowflake CLI environment variables and
  pass `connection: "my-connection"` in your SDK options, or omit it to use the default connection:

  Copy code

  ```
  export SNOWFLAKE_ACCOUNT="myorg-myaccount"
  export SNOWFLAKE_USER="myuser"
  export SNOWFLAKE_PASSWORD="..."    # or use SNOWFLAKE_PRIVATE_KEY_RAW for key-pair auth
  ```

  The Snowflake CLI reads these variables automatically. For key-pair authentication without a local
  key file, use `SNOWFLAKE_PRIVATE_KEY_RAW` with the PEM content. For a full list of supported
  environment variables and CI/CD authentication patterns, see
  [Use environment variables for Snowflake credentials](/developer-guide/snowflake-cli/connecting/configure-connections#use-environment-variables-for-snowflake-credentials).

## Setup

### 1. Install the Cortex Code CLI

Install the CLI:

Copy code

```
curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh
```

Verify the installation:

Copy code

```
cortex --version
```

### 2. Set up your project

Create and enter a project directory:

Copy code

```
mkdir my-agent && cd my-agent
```

### 3. Install the SDK

TypeScriptPython

Copy code

```
npm init -y
npm install cortex-code-agent-sdk
```

Copy code

```
python3 -m venv .venv && source .venv/bin/activate
pip install cortex-code-agent-sdk
```

## Create a data pipeline script

Create a data pipeline script with some intentional bugs for the agent to fix:

Python (report.py)TypeScript (report.ts)

Copy code

```
import json

def load_results(rows):
    """Load query results into a list of campaign dicts."""
    return [
        {
            "campaign": row["campaign_name"],
            "impressions": row["impressions"],
            "clicks": row["clicks"],
            "conversions": row["conversions"],
        }
        for row in rows
    ]

def compute_conversion_rate(results):
    """Add conversion_rate (conversions / clicks) to each campaign."""
    for row in results:
        row["conversion_rate"] = row["conversions"] / row["clicks"]  # Bug: ZeroDivisionError when clicks is 0
    return results

def format_report(results):
    """Return a JSON summary with total conversions and the top campaign."""
    total = sum(r["conversions"] for r in results)
    top = max(results, key=lambda r: r["conversion_rate"])  # Bug: crashes on empty list
    return json.dumps({"total_conversions": total, "top_campaign": top["campaign"]})
```

Copy code

```
interface Row {
  campaign_name: string;
  impressions: number;
  clicks: number;
  conversions: number;
}

interface Result {
  campaign: string;
  impressions: number;
  clicks: number;
  conversions: number;
  conversion_rate?: number;
}

export function loadResults(rows: Row[]): Result[] {
  return rows.map(row => ({
    campaign: row.campaign_name,
    impressions: row.impressions,
    clicks: row.clicks,
    conversions: row.conversions,
  }));
}

export function computeConversionRate(results: Result[]): Result[] {
  return results.map(row => ({
    ...row,
    conversion_rate: row.conversions / row.clicks,  // Bug: NaN or Infinity when clicks is 0
  }));
}

export function formatReport(results: Result[]): string {
  const total = results.reduce((sum, r) => sum + r.conversions, 0);
  const top = results.reduce((best, r) =>
    r.conversion_rate! > best.conversion_rate! ? r : best  // Bug: crashes on empty array
  );
  return JSON.stringify({ total_conversions: total, top_campaign: top.campaign });
}
```

This code has two issues:

1. `computeConversionRate` / `compute_conversion_rate` divides by `clicks` without checking for zero, returning
   `NaN` or `Infinity` (TypeScript) or raising a `ZeroDivisionError` (Python) for campaigns with no clicks.
2. `formatReport` / `format_report` calls `max` / `reduce` on the results list without checking whether it is
   empty, which raises a `ValueError` (Python) or `TypeError` (TypeScript) when there are no rows.

## Build an agent that finds and fixes bugs

TypeScriptPython

Copy code

```
// agent.mjs
import { query } from "cortex-code-agent-sdk";

// Agentic loop: streams messages as the agent works
for await (const message of query({
  prompt: "Review report.ts for bugs in the data pipeline. Fix any issues you find.",
  options: {
    cwd: process.cwd(),
    connection: "my-connection",          // Snowflake CLI connection name
    allowedTools: ["Read", "Edit", "Bash"],  // Auto-approve these tools without prompting
  },
})) {
  // Print human-readable output
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);  // Agent's reasoning
      } else if (block.type === "tool_use") {
        console.log(`Tool: ${block.name}`);  // Tool being called
      }
    }
  } else if (message.type === "result") {
    console.log(`\nDone: ${message.subtype}`);  // Final result
  }
}
```

Copy code

```
# agent.py
import asyncio
from cortex_code_agent_sdk import query, AssistantMessage, ResultMessage, CortexCodeAgentOptions

async def main():
    # Agentic loop: streams messages as the agent works
    async for message in query(
        prompt="Review report.py for bugs in the data pipeline. Fix any issues you find.",
        options=CortexCodeAgentOptions(
            cwd=".",
            connection="my-connection",              # Snowflake CLI connection name
            allowed_tools=["Read", "Edit", "Bash"],  # Auto-approve these tools without prompting
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="")  # Agent's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"\nDone: {message.subtype}")  # Final result

asyncio.run(main())
```

This code has three main parts:

1. **query()**: The main entry point that creates the agentic loop. It returns an async iterator that you consume
   in your language’s async loop syntax to stream messages as the agent works. See the full API in the
   [TypeScript](/user-guide/cortex-code-agent-sdk/typescript-reference) or
   [Python](/user-guide/cortex-code-agent-sdk/python-reference) reference.
2. **prompt**: What you want the agent to do. It tells the agent what task to complete.
3. **options**: Configuration for the agent. `connection` specifies which Snowflake CLI connection to authenticate
   with. `allowedTools` specifies which tools are auto-approved without prompting, and `disallowedTools` can block
   tools entirely. Other options include `model`, `mcp_servers`, and more.

The streaming loop runs as the agent thinks, calls tools, observes results, and decides what to do next. Each
iteration yields a message: the agent’s reasoning, a tool call, a tool result, or the final outcome. The SDK handles
the orchestration.

### Run your agent

TypeScriptPython

Copy code

```
node agent.mjs
```

Copy code

```
python3 agent.py
```

After running, check your report file. You’ll see defensive code handling empty results and zero-click campaigns.
Your agent autonomously:

1. **Read** the file to understand the code.
2. **Analyzed** the logic and identified edge cases that would crash.
3. **Edited** the file to add proper error handling.

## Multi-turn conversations

For interactive sessions where you send multiple prompts with shared context, use the **Client** API:

TypeScriptPython

Copy code

```
import {
  createCortexCodeSession,
  type CortexCodeEvent,
} from "cortex-code-agent-sdk";

async function printResponse(stream: AsyncIterable<CortexCodeEvent>) {
  for await (const event of stream) {
    if (event.type === "assistant") {
      for (const block of event.content) {
        if (block.type === "text") process.stdout.write(block.text);
      }
    } else if (event.type === "result") {
      break;
    }
  }
}

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  connection: "my-connection",
});

// First turn
await session.send("Summarize what report.ts does and what data it expects.");
await printResponse(session.stream());

// Second turn (same session, remembers context)
await session.send("Now add type annotations to each function.");
await printResponse(session.stream());

await session.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, AssistantMessage

async with CortexCodeSDKClient(
    CortexCodeAgentOptions(
        cwd=".",
        connection="my-connection",
    )
) as client:
    # First turn
    await client.query("Summarize what report.py does and what data it expects.")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if hasattr(b, "text"):
                    print(b.text, end="")

    # Second turn (same session, remembers context)
    await client.query("Now add docstrings to each function.")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for b in msg.content:
                if hasattr(b, "text"):
                    print(b.text, end="")
```

### Try other prompts

Now that your agent is set up, try some different prompts:

- `"Find the top 10 campaigns by conversion rate in the SALES.PUBLIC schema and run the query"`
- `"Check the SALES.PUBLIC schema for data quality issues: empty tables, stale loads, and high NULL rates"`
- `"Generate a dbt staging model for the ORDERS table based on its actual columns in Snowflake"`
- `"Profile the columns of the CUSTOMERS table: report the data type, distinct count, and NULL rate for each"`

## Key concepts

### Permission modes

Permission modes control the level of human oversight for tool calls:

| Mode | Behavior | Use case |
| --- | --- | --- |
| `"bypassPermissions"` (with safety flag) | Runs every tool without prompts. Requires `allowDangerouslySkipPermissions: true` (TypeScript) or `allow_dangerously_skip_permissions=True` (Python). | Sandboxed CI, fully trusted environments |
| `"default"` | Uses standard permission checks. In SDK sessions, configure `allowedTools`, `disallowedTools`, or `canUseTool` to control permission-checked tools. | Controlled workflows with explicit permission policy |
| `"autoAcceptPlans"` | Auto-approves plan requests and plan-exit confirmations. It does not bypass ordinary tool permissions. | Specialized workflows that want plan approvals to proceed automatically |
| `"plan"` | Starts in planning; approving `ExitPlanMode` lets execution continue and later turns resume normal permissions | Code review, analysis |

Expand

Show lessSee more

For granular control over individual tool calls, use the `canUseTool` callback. See
[Handle approvals and user input](/user-guide/cortex-code-agent-sdk/user-input) for details.

## Next steps

- [Handle approvals and user input](/user-guide/cortex-code-agent-sdk/user-input): Control which tools the
  agent can use with the `canUseTool` callback.
- [TypeScript SDK reference](/user-guide/cortex-code-agent-sdk/typescript-reference): Complete API docs for
  `query()`, `createCortexCodeSession()`, types, and events.
- [Python SDK reference](/user-guide/cortex-code-agent-sdk/python-reference): Complete API docs for
  `query()`, `CortexCodeSDKClient`, MCP tools, and hooks.

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
