# Build a data copilot

This tutorial builds a data engineering copilot: a small web app whose features are each powered by the Cortex Code
Agent SDK. Instead of hand-writing SQL, you describe what you want in natural language, and the agent uses its
built-in SQL tool to write and run queries against Snowflake, then returns typed, structured results your application
can use directly.

The focus is the SDK usage, not the web framework. The examples use a [Next.js](https://nextjs.org/) app because it
makes the agent easy to drive from a browser, but every SDK pattern here works the same way in a plain script, a
scheduled job, or a continuous integration and continuous delivery (CI/CD) step.

## What you’ll build

A data engineering copilot with three tools, each backed by the SDK:

- **Pipeline health audit**: describe a schema, and the agent discovers its tables, counts rows, checks load
  freshness, and returns a typed health report. Uses [structured output](/user-guide/cortex-code-agent-sdk/structured-output).
- **Schema drift detector**: compare two schemas and get a typed list of added, removed, and type-changed columns,
  with breaking changes flagged. Plugs directly into a deploy gate.
- **AI query optimizer**: paste a slow query, and a multi-turn agent session diagnoses the bottleneck in the first
  turn and produces an optimized rewrite in the second, keeping full context between turns.

Each tool is a small API route that sends a natural-language prompt to the SDK and lets the agent do the SQL work. The
app never hard-codes a query.

## Prerequisites

- **Node.js 22 or later**.
- **Cortex Code CLI** installed:

  Copy code

  ```
  curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh
  ```
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
- **A schema to point the copilot at.** Any schema in your account works. [Optional: create demo data](#optional-create-demo-data)
  includes a script that creates a small schema with tables in deliberately mixed health states.

## Project setup

Create the project and install the SDK:

Copy code

```
npx create-next-app@latest data-copilot --ts --app --no-src-dir
cd data-copilot
npm install cortex-code-agent-sdk
```

The SDK authenticates through your Snowflake CLI connection. It uses your default connection unless you point it at a
named one. The app reads the connection name from an environment variable so the same code works locally, in Cortex
Code Desktop, and in Snowpark Container Services. Two variables are supported, checked in this order:

- `SNOWFLAKE_DEFAULT_CONNECTION_NAME`: the primary variable. Cortex Code Desktop and Snowpark Container Services set
  this automatically, so you might already have it set without knowing it.
- `SNOWFLAKE_CONNECTION_NAME`: an override you can set to point the app at a different named connection.

If neither is set, the SDK falls back to the Snowflake CLI default connection.

Copy code

```
# Optional: only needed to override the automatically detected connection
export SNOWFLAKE_DEFAULT_CONNECTION_NAME=my-connection
```

Before building the web UI, confirm the SDK can reach Snowflake with a one-file script. Save it as `scripts/smoke-test.ts`
and run it with `npx tsx scripts/smoke-test.ts`:

Copy code

```
// scripts/smoke-test.ts
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "List the tables in the SALES.PUBLIC schema with their row counts.",
  options: { allowedTools: ["SQL"] }, // auto-approve the SQL tool so the script runs unattended
})) {
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "text") process.stdout.write(block.text);
    }
  }
}
```

Once that prints results, you’re connected. The rest of this guide wraps this same `query()` call in API routes.

### Project structure

The finished app has one API route per tool, a shared SDK helper, and a UI page per tool. Only the API routes and the
helper contain SDK code; the pages are ordinary React:

```
data-copilot/
├─ app/
│  ├─ api/
│  │  ├─ pipeline-audit/route.ts   # structured-output audit, streamed to the UI
│  │  ├─ schema-diff/route.ts      # structured-output diff for a deploy gate
│  │  └─ query-optimizer/route.ts  # multi-turn diagnose-then-rewrite session
│  ├─ pipeline-audit/page.tsx      # UI for each tool (no SDK code)
│  ├─ schema-diff/page.tsx
│  └─ query-optimizer/page.tsx
└─ lib/
   └─ sdk.ts                       # shared SDK options and helpers
```

### Optional: create demo data

To reproduce the audit against a schema with known issues, run this script in a worksheet. It creates five tables in
deliberately different states: healthy, stale, empty, and high-null.

Copy code

```
CREATE DATABASE IF NOT EXISTS DATA_COPILOT_DEMO;
CREATE SCHEMA IF NOT EXISTS DATA_COPILOT_DEMO.PUBLIC;
USE SCHEMA DATA_COPILOT_DEMO.PUBLIC;

-- Healthy: recently loaded
CREATE OR REPLACE TABLE ORDERS (
  order_id INTEGER, customer_id INTEGER, amount DECIMAL(10, 2),
  status VARCHAR(20), created_at TIMESTAMP_NTZ, loaded_at TIMESTAMP_NTZ
);
INSERT INTO ORDERS
SELECT seq4() + 1, UNIFORM(1, 5000, RANDOM()),
  ROUND(UNIFORM(10, 2000, RANDOM()), 2)::DECIMAL(10, 2),
  CASE UNIFORM(1, 3, RANDOM()) WHEN 1 THEN 'PENDING' WHEN 2 THEN 'SHIPPED' ELSE 'DELIVERED' END,
  DATEADD('minute', -UNIFORM(1, 1440, RANDOM()), CURRENT_TIMESTAMP()),
  DATEADD('minute', -UNIFORM(5, 90, RANDOM()), CURRENT_TIMESTAMP())
FROM TABLE(GENERATOR(ROWCOUNT => 100000));

-- Healthy: fully populated
CREATE OR REPLACE TABLE CUSTOMERS (
  customer_id INTEGER, name VARCHAR(100), email VARCHAR(200),
  region VARCHAR(50), plan_tier VARCHAR(20), loaded_at TIMESTAMP_NTZ
);
INSERT INTO CUSTOMERS
SELECT seq4() + 1, 'Customer_' || LPAD(seq4() + 1, 5, '0'),
  'user' || (seq4() + 1) || '@example.com',
  CASE UNIFORM(1, 4, RANDOM()) WHEN 1 THEN 'North' WHEN 2 THEN 'South' WHEN 3 THEN 'East' ELSE 'West' END,
  CASE UNIFORM(1, 3, RANDOM()) WHEN 1 THEN 'free' WHEN 2 THEN 'pro' ELSE 'enterprise' END,
  DATEADD('minute', -UNIFORM(10, 120, RANDOM()), CURRENT_TIMESTAMP())
FROM TABLE(GENERATOR(ROWCOUNT => 10000));

-- Stale: last loaded about 3 days ago
CREATE OR REPLACE TABLE PRODUCT_EVENTS (
  event_id INTEGER, product_id INTEGER, event_type VARCHAR(50),
  session_id VARCHAR(50), user_id INTEGER, loaded_at TIMESTAMP_NTZ
);
INSERT INTO PRODUCT_EVENTS
SELECT seq4() + 1, UNIFORM(1, 500, RANDOM()),
  CASE UNIFORM(1, 4, RANDOM()) WHEN 1 THEN 'view' WHEN 2 THEN 'click' WHEN 3 THEN 'add_to_cart' ELSE 'purchase' END,
  'sess_' || UNIFORM(10000, 99999, RANDOM()), UNIFORM(1, 10000, RANDOM()),
  DATEADD('hour', -UNIFORM(80, 96, RANDOM()), CURRENT_TIMESTAMP())
FROM TABLE(GENERATOR(ROWCOUNT => 25000));

-- Empty: pipeline never populated it
CREATE OR REPLACE TABLE SESSION_METRICS (
  session_id VARCHAR(100), user_id INTEGER, duration_seconds INTEGER,
  page_views INTEGER, bounce BOOLEAN, loaded_at TIMESTAMP_NTZ
);

-- High nulls: about a third of campaign_id and channel are NULL
CREATE OR REPLACE TABLE AD_SPEND (
  spend_id INTEGER, campaign_id VARCHAR(50), channel VARCHAR(50),
  impressions INTEGER, clicks INTEGER, cost DECIMAL(10, 2), loaded_at TIMESTAMP_NTZ
);
INSERT INTO AD_SPEND
SELECT seq4() + 1,
  CASE WHEN UNIFORM(1, 3, RANDOM()) = 1 THEN NULL ELSE 'campaign_' || LPAD(UNIFORM(1, 30, RANDOM()), 3, '0') END,
  CASE WHEN UNIFORM(1, 3, RANDOM()) = 1 THEN NULL
       ELSE CASE UNIFORM(1, 4, RANDOM()) WHEN 1 THEN 'email' WHEN 2 THEN 'social' WHEN 3 THEN 'search' ELSE 'display' END END,
  UNIFORM(100, 50000, RANDOM()), UNIFORM(5, 2000, RANDOM()),
  ROUND(UNIFORM(50, 5000, RANDOM()), 2)::DECIMAL(10, 2),
  DATEADD('hour', -UNIFORM(1, 6, RANDOM()), CURRENT_TIMESTAMP())
FROM TABLE(GENERATOR(ROWCOUNT => 8000));
```

## Walk through the key SDK usage

### A shared options helper

Every tool configures the SDK the same way, so it’s worth centralizing in `lib/sdk.ts`. The app runs the agent
unattended (there’s no human to approve each tool call in a web request), so it auto-approves tools with
`permissionMode: "bypassPermissions"` and the required `allowDangerouslySkipPermissions` safety flag, disables
external Model Context Protocol (MCP) servers, and picks up the connection name from the environment.

The same file also holds two small helpers that pull text and SQL out of the agent’s streamed messages, which the
tools reuse to show the agent’s work in the browser:

Copy code

```
// lib/sdk.ts
import type {
  CortexCodeSessionOptions,
  ContentBlock,
  TextBlock,
  ToolUseBlock,
} from "cortex-code-agent-sdk";

export function sdkOptions(
  override?: Partial<CortexCodeSessionOptions>,
): CortexCodeSessionOptions {
  // Cortex Code Desktop and Snowpark Container Services set SNOWFLAKE_DEFAULT_CONNECTION_NAME.
  const connection =
    process.env.SNOWFLAKE_DEFAULT_CONNECTION_NAME ||
    process.env.SNOWFLAKE_CONNECTION_NAME;

  return {
    permissionMode: "bypassPermissions",
    allowDangerouslySkipPermissions: true,
    noMcp: true,
    ...(connection ? { connection } : {}),
    ...override,
  };
}

// Plain text the agent streams back (its reasoning and explanations).
export function textBlocks(content: ContentBlock[]): TextBlock[] {
  return content.filter((b): b is TextBlock => b.type === "text");
}

// Each SQL statement the agent runs, so the UI can show its work.
export function sqlToolUses(content: ContentBlock[]): string[] {
  return content
    .filter((b): b is ToolUseBlock => b.type === "tool_use" && b.name === "SQL")
    .map((b) => {
      const input = b.input as Record<string, unknown>;
      // The SQL tool input uses "command" or "query" depending on CLI version.
      return (input.command ?? input.query ?? JSON.stringify(input)) as string;
    });
}
```

Warning

`permissionMode: "bypassPermissions"` runs every tool without prompting. Use it only in trusted, sandboxed
environments such as your own server or a CI/CD job. For workflows that need human oversight, use `allowedTools`,
`disallowedTools`, or the `canUseTool` callback instead. See
[Handle approvals and user input](/user-guide/cortex-code-agent-sdk/user-input).

### Tool 1: Pipeline health audit

The audit sends one prompt and a JSON Schema, then lets the agent write and run the SQL. Because the request passes
`outputFormat`, the final result is validated against the schema, so the route receives a typed report instead of free
text it would have to parse. As the agent works, the route streams its text and each SQL statement to the browser
using the helpers from `lib/sdk.ts`.

TypeScriptPython

Copy code

```
// app/api/pipeline-audit/route.ts (SDK essentials)
import { query } from "cortex-code-agent-sdk";
import { sdkOptions, textBlocks, sqlToolUses } from "@/lib/sdk";

const AUDIT_OUTPUT_SCHEMA = {
  type: "object",
  properties: {
    tables: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          rowCount: { type: "number" },
          lastLoaded: { type: ["string", "null"] },
          hoursSinceLoad: { type: ["number", "null"] },
          status: { type: "string", enum: ["healthy", "stale", "empty", "high_nulls"] },
          recommendation: { type: "string" },
        },
        required: ["name", "rowCount", "lastLoaded", "hoursSinceLoad", "status", "recommendation"],
      },
    },
    total: { type: "number" },
    healthy: { type: "number" },
    issues: { type: "number" },
  },
  required: ["tables", "total", "healthy", "issues"],
};

const prompt = `Audit schema ${database}.${schema} in Snowflake. For each BASE TABLE:
1. Get the row count from INFORMATION_SCHEMA.TABLES (ROW_COUNT column)
2. Find the most recent timestamp column: LOADED_AT, UPDATED_AT, CREATED_AT, or any TIMESTAMP/DATE column in INFORMATION_SCHEMA.COLUMNS
3. For tables with a timestamp column, query MAX of that column to compute hours since last load
4. Classify each table: "empty" (0 rows), "stale" (last load > 24h ago), "high_nulls" (if you detect high null rates), or "healthy"
5. Write a short, specific recommendation for each non-healthy table

Return the full health report as structured JSON.`;

for await (const event of query({
  prompt,
  options: sdkOptions({
    allowedTools: ["SQL"],
    // The SDK types this field as Record<string, unknown>, so cast the const schema.
    outputFormat: { type: "json_schema", schema: AUDIT_OUTPUT_SCHEMA as Record<string, unknown> },
  }),
})) {
  if (event.type === "system" && event.subtype === "init") {
    // The init event reports which model the agent is using.
    console.log(`Agent started, model: ${event.model}`);
  }
  if (event.type === "assistant") {
    for (const block of textBlocks(event.content)) {
      // stream block.text to the UI
    }
    for (const sql of sqlToolUses(event.content)) {
      // stream each SQL statement the agent runs to the UI
    }
  }
  if (event.type === "result" && event.subtype === "success") {
    // structured_output is typed unknown, so cast it to the shape you asked for.
    const report = event.structured_output as {
      tables: unknown[];
      total: number;
      healthy: number;
      issues: number;
    };
    console.log(`${report.issues} issue(s) across ${report.total} tables`);
  }
}
```

Copy code

```
from pydantic import BaseModel
from cortex_code_agent_sdk import query, AssistantMessage, ResultMessage, CortexCodeAgentOptions

class TableHealth(BaseModel):
    name: str
    row_count: int
    last_loaded: str | None
    hours_since_load: float | None
    status: str  # "healthy" | "stale" | "empty" | "high_nulls"
    recommendation: str

class PipelineReport(BaseModel):
    tables: list[TableHealth]
    total: int
    healthy: int
    issues: int

async for msg in query(
    prompt=f"Audit schema {database}.{schema}: flag stale (>24h), empty, and high-null tables",
    options=CortexCodeAgentOptions(
        connection="my-connection",
        allowed_tools=["SQL"],
        output_format={"type": "json_schema", "schema": PipelineReport.model_json_schema()},
    ),
):
    if isinstance(msg, ResultMessage) and msg.structured_output:
        report = PipelineReport(**msg.structured_output)
        print(f"{report.issues} issue(s) across {report.total} tables")
```

### Tool 2: Schema drift detector

The drift detector uses the same structured-output pattern, but the typed result drives a decision: if the agent
finds any breaking change, the app can fail a deploy. This turns a natural-language request into a deterministic gate.

TypeScriptPython

Copy code

```
// app/api/schema-diff/route.ts (SDK essentials)
import { query } from "cortex-code-agent-sdk";
import { sdkOptions } from "@/lib/sdk";

const SCHEMA_DIFF_OUTPUT = {
  type: "object",
  properties: {
    sourceSchema: { type: "string" },
    targetSchema: { type: "string" },
    tablesCompared: { type: "number" },
    addedTables: { type: "array", items: { type: "string" } },
    removedTables: { type: "array", items: { type: "string" } },
    changes: {
      type: "array",
      items: {
        type: "object",
        properties: {
          tableName: { type: "string" },
          columnName: { type: "string" },
          changeType: { type: "string", enum: ["added", "removed", "type_changed"] },
          sourceType: { type: ["string", "null"] },
          targetType: { type: ["string", "null"] },
          isBreaking: { type: "boolean" },
        },
        required: ["tableName", "columnName", "changeType", "sourceType", "targetType", "isBreaking"],
      },
    },
    breakingChanges: { type: "number" },
  },
  required: ["sourceSchema", "targetSchema", "tablesCompared", "addedTables", "removedTables", "changes", "breakingChanges"],
};

const prompt = `Compare the column schemas of every table in ${srcDb}.${srcSchema} with its counterpart in ${tgtDb}.${tgtSchema}.
Use INFORMATION_SCHEMA.COLUMNS to get column names and data types for both schemas.
Identify columns that were added, removed, or had their type changed between source and target.
Flag type changes as breaking if they narrow the type (for example, a wider VARCHAR to a narrower VARCHAR, or NUMBER with reduced precision).
Also identify tables that exist in one schema but not the other.
Return a complete structured diff.`;

for await (const event of query({
  prompt,
  options: sdkOptions({
    allowedTools: ["SQL"],
    // The SDK types this field as Record<string, unknown>, so cast the const schema.
    outputFormat: { type: "json_schema", schema: SCHEMA_DIFF_OUTPUT as Record<string, unknown> },
  }),
})) {
  if (event.type === "result" && event.subtype === "success") {
    // structured_output is typed unknown, so cast it to the shape you asked for.
    const diff = event.structured_output as { breakingChanges: number };
    if (diff.breakingChanges > 0) {
      process.exit(1); // In CI, block the deploy
    }
  }
}
```

Copy code

```
from pydantic import BaseModel
from cortex_code_agent_sdk import query, ResultMessage, CortexCodeAgentOptions

class ColumnChange(BaseModel):
    table_name: str
    column_name: str
    change_type: str  # "added" | "removed" | "type_changed"
    source_type: str | None
    target_type: str | None
    is_breaking: bool

class SchemaDiff(BaseModel):
    source_schema: str
    target_schema: str
    tables_compared: int
    added_tables: list[str]
    removed_tables: list[str]
    changes: list[ColumnChange]
    breaking_changes: int

async for msg in query(
    prompt=(
        "Compare schemas STAGING.PUBLIC and PROD.PUBLIC using INFORMATION_SCHEMA. "
        "Flag removed or type-narrowed columns as breaking."
    ),
    options=CortexCodeAgentOptions(
        connection="my-connection",
        allowed_tools=["SQL"],
        output_format={"type": "json_schema", "schema": SchemaDiff.model_json_schema()},
    ),
):
    if isinstance(msg, ResultMessage) and msg.structured_output:
        diff = SchemaDiff(**msg.structured_output)
        if diff.breaking_changes > 0:
            raise SystemExit(f"Deploy blocked: {diff.breaking_changes} breaking change(s)")
```

### Tool 3: AI query optimizer

The optimizer needs two turns that share context: first diagnose, then rewrite. Instead of `query()`, it uses a
session so the second prompt can rely on everything the agent learned in the first. It also appends a system prompt to
steer the agent toward Snowflake-specific advice.

TypeScriptPython

Copy code

```
// app/api/query-optimizer/route.ts (SDK essentials)
import { createCortexCodeSession } from "cortex-code-agent-sdk";
import { sdkOptions, textBlocks, sqlToolUses } from "@/lib/sdk";

const session = await createCortexCodeSession(
  sdkOptions({
    allowedTools: ["SQL"],
    appendSystemPrompt:
      "You are a Snowflake SQL expert. When diagnosing queries, be specific about " +
      "micro-partition pruning, clustering keys, partition pruning ratios, and warehouse " +
      "sizing. Reference Snowflake-native features by name.",
  }),
);

// A session reports its model through initializationResult() instead of an init event.
const init = await session.initializationResult();
const model = (init as Record<string, unknown>).model as string;
console.log(`Agent started, model: ${model}`);

// Stream one turn's text and SQL to the UI. Both turns are handled the same way,
// so the agent's rewrite in turn 2 is streamed just like the diagnosis in turn 1.
async function streamTurn() {
  for await (const event of session.stream()) {
    if (event.type === "assistant") {
      for (const block of textBlocks(event.content)) { /* stream the text to the UI */ }
      for (const ranSql of sqlToolUses(event.content)) { /* stream the SQL the agent ran */ }
    }
    if (event.type === "result") break;
  }
}

// Turn 1: diagnose the bottleneck
await session.send(
  `Diagnose this Snowflake SQL query. Identify the main performance bottleneck and explain why it's slow:\n\n\`\`\`sql\n${sql}\n\`\`\``,
);
await streamTurn();

// Turn 2: rewrite. The agent still has the full diagnosis in context.
await session.send(
  "Now produce the full optimized rewrite of that query with inline comments explaining each key change.",
);
await streamTurn();

await session.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, AssistantMessage

system_prompt = {"type": "preset", "append": (
    "You are a Snowflake SQL expert. When diagnosing queries, be specific about "
    "micro-partition pruning, clustering keys, partition pruning ratios, and warehouse "
    "sizing. Reference Snowflake-native features by name."
)}

async with CortexCodeSDKClient(
    CortexCodeAgentOptions(connection="my-connection", allowed_tools=["SQL"], system_prompt=system_prompt)
) as client:
    # Turn 1: diagnose
    await client.query(f"Diagnose this Snowflake SQL query. Identify the main performance bottleneck and explain why it's slow:\n\n```sql\n{slow_query}\n```")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if hasattr(block, "text"):
                    print(block.text, end="")

    # Turn 2: rewrite. The agent still has full context from turn 1.
    await client.query("Now produce the full optimized rewrite of that query with inline comments explaining each key change.")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if hasattr(block, "text"):
                    print(block.text, end="")
```

## Run it

Start the app:

Copy code

```
npm run dev
```

Open `http://localhost:3000`, choose a tool, and describe what you want. The rest of this section shows the kind of
output each tool produces.

### Pipeline health audit output

As the audit runs, the route streams the agent’s reasoning and each SQL statement it writes, so the browser shows the
work in progress:

```
Agent started, model: auto
Auditing DATA_COPILOT_DEMO.PUBLIC: fetching tables, row counts, and timestamp columns
SQL: SELECT table_name, row_count FROM DATA_COPILOT_DEMO.INFORMATION_SCHEMA.TABLES WHERE table_schema = 'PUBLIC'
SQL: SELECT MAX(loaded_at) FROM DATA_COPILOT_DEMO.PUBLIC.PRODUCT_EVENTS
```

The final `result` event carries the typed `PipelineReport`. The app renders it as a summary count plus one row per
table:

| Table | Rows | Last loaded | Status | Recommendation |
| --- | --- | --- | --- | --- |
| `ORDERS` | 100,000 | ~1 hour ago | healthy | None |
| `CUSTOMERS` | 10,000 | ~1 hour ago | healthy | None |
| `PRODUCT_EVENTS` | 25,000 | ~3 days ago | stale | Last load is about 3 days old; run the ingestion job to pick up new events. |
| `SESSION_METRICS` | 0 | Never | empty | Table has no rows; confirm the pipeline populates it or drop it. |
| `AD_SPEND` | 8,000 | ~2 hours ago | high\_nulls | `campaign_id` and `channel` are about 33% NULL; check the source mapping. |

Expand

Show lessSee more

Two tables are healthy; three need attention: `PRODUCT_EVENTS` is stale, `SESSION_METRICS` is empty, and `AD_SPEND`
has a high NULL rate.

### Schema drift detector output

Comparing a staging schema against production returns a typed `SchemaDiff` your deploy gate can act on:

Copy code

```
{
  "sourceSchema": "STAGING.PUBLIC",
  "targetSchema": "PROD.PUBLIC",
  "tablesCompared": 12,
  "addedTables": ["FEATURE_FLAGS"],
  "removedTables": [],
  "changes": [
    { "tableName": "ORDERS", "columnName": "discount_pct", "changeType": "added", "sourceType": null, "targetType": "NUMBER(5,2)", "isBreaking": false },
    { "tableName": "CUSTOMERS", "columnName": "email", "changeType": "type_changed", "sourceType": "VARCHAR(255)", "targetType": "VARCHAR(100)", "isBreaking": true },
    { "tableName": "SESSIONS", "columnName": "user_agent", "changeType": "removed", "sourceType": "VARCHAR(1000)", "targetType": null, "isBreaking": true }
  ],
  "breakingChanges": 2
}
```

Because `breakingChanges` is above zero, the CI step from the previous section exits non-zero and blocks the deploy.

### AI query optimizer output

Paste a slow query:

Copy code

```
SELECT
  u.userid,
  u.firstname || ' ' || u.lastname AS buyer_name,
  u.city,
  COUNT(s.salesid) AS total_purchases,
  SUM(s.qtysold * s.pricepaid) AS total_spent,
  AVG(s.pricepaid) AS avg_ticket_price
FROM SAMPLES.TICKIT.SALES s
JOIN SAMPLES.TICKIT.USERS u ON s.buyerid = u.userid
JOIN SAMPLES.TICKIT.EVENT e ON s.eventid = e.eventid
WHERE s.saletime >= DATEADD('month', -6, CURRENT_TIMESTAMP())
  AND e.catid IN (1, 2, 3)
GROUP BY 1, 2, 3
ORDER BY total_spent DESC
LIMIT 100;
```

**Turn 1 diagnoses the bottleneck.** The agent inspects the table metadata and reports the primary problem, a full
micro-partition scan on `SALES`:

```
SALES: 172,456 rows | cluster_by: (none) | automatic_clustering: OFF
```

The predicate `s.saletime >= DATEADD('month', -6, CURRENT_TIMESTAMP())` can’t prune any micro-partitions because
`SALES` has no clustering key, so Snowflake scans every partition. The agent also flags a secondary bottleneck: the
`e.catid IN (1, 2, 3)` filter lives on `EVENT` and only removes `SALES` rows after the join completes.

**Turn 2 produces the rewrite,** reusing the diagnosis from turn 1. It pre-filters `EVENT` in a CTE, reorders the
joins so the smallest filtered set drives the query, and groups by raw columns instead of positional aliases:

Copy code

```
-- OPTIMIZED REWRITE: SAMPLES.TICKIT buyer summary
WITH eligible_events AS (
  -- [1] Pre-filter EVENT before any join to SALES, so only matching eventids reach the SALES join.
  SELECT eventid
  FROM SAMPLES.TICKIT.EVENT
  WHERE catid IN (1, 2, 3)
)
SELECT
  u.userid,
  -- [4] Concatenation deferred until after grouping (runs on ~100 result rows, not every input row).
  u.firstname || ' ' || u.lastname AS buyer_name,
  u.city,
  COUNT(s.salesid)             AS total_purchases,
  SUM(s.qtysold * s.pricepaid) AS total_spent,
  AVG(s.pricepaid)             AS avg_ticket_price
FROM SAMPLES.TICKIT.SALES s
JOIN eligible_events e       ON s.eventid = e.eventid  -- [2] join the smallest filtered table first
JOIN SAMPLES.TICKIT.USERS u  ON s.buyerid = u.userid   -- [3] USERS joins already-filtered SALES rows
WHERE s.saletime >= DATEADD('month', -6, CURRENT_TIMESTAMP())  -- [5] benefits from CLUSTER BY (saletime)
GROUP BY u.userid, u.firstname, u.lastname, u.city
ORDER BY total_spent DESC
LIMIT 100;
```

The rewrite delivers its full benefit only after a one-time clustering change, which the agent calls out as a
prerequisite:

Copy code

```
-- Snowflake reclusters asynchronously in the background.
ALTER TABLE SAMPLES.TICKIT.SALES CLUSTER BY (saletime);
```

## Extend it

The same building blocks support more automation:

- **Run it headless in CI/CD**: drive the audit or drift check from a scheduled job with no human in the loop. Cap
  runaway work with `maxTurns`.
- **Log every query the agent runs**: add a `PostToolUse` hook to append each SQL statement to an audit log for
  compliance. See [Hooks](/user-guide/cortex-code-agent-sdk/hooks).
- **Combine local files with Snowflake**: give the agent the `Read`, `Glob`, and `Write` tools alongside `SQL` and
  point `cwd` at a dbt project, so it can cross-reference your models against the actual schema.

## Next steps

- [Structured output](/user-guide/cortex-code-agent-sdk/structured-output): Return validated JSON from agent workflows
- [Multi-turn sessions and streaming input](/user-guide/cortex-code-agent-sdk/streaming-input): Maintain context across multiple exchanges
- [Handle approvals and user input](/user-guide/cortex-code-agent-sdk/user-input): Control which tools the agent can use
- [Hooks](/user-guide/cortex-code-agent-sdk/hooks): Run custom code at key points in the agent lifecycle
- [TypeScript SDK reference](/user-guide/cortex-code-agent-sdk/typescript-reference): Full TypeScript API reference
- [Python SDK reference](/user-guide/cortex-code-agent-sdk/python-reference): Full Python API reference

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
