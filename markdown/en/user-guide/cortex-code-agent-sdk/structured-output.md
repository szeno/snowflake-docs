# Structured output

This topic describes how to return schema-validated JSON from agent workflows using JSON Schema. The agent can use any
tools it needs to complete the task, and on successful validation the result includes structured data that matches your
schema.

Define a [JSON Schema](https://json-schema.org/understanding-json-schema/about) for the structure you need, and the
SDK validates the model’s final output against it.

## Why structured outputs?

Agents return free-form text by default, which works for conversational use cases but not when you need to use the
output programmatically. Structured outputs provide typed data you can pass directly to your application logic,
database, or UI components.

Consider an agent that analyzes a codebase. Without structured outputs you get free-form text that you would need to
parse yourself. With structured outputs you define the shape you want and get typed data you can use directly:

| Without structured outputs | With structured outputs |
| --- | --- |
| ``` This codebase uses Python and TypeScript. It has 42 files and the main entry point is... ``` | Copy code  ``` { "languages": ["Python", "TypeScript"],   "file_count": 42,   "entry_point": "src/main.ts" } ``` |

Expand

Show lessSee more

## Quick start

Pass a JSON Schema to the `outputFormat` (TypeScript) or `output_format` (Python) option. When validation
succeeds, the result message includes a `structured_output` field with data matching your schema. If the agent
cannot satisfy the schema after retries, the SDK returns an error result instead.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

const schema = {
  type: "object",
  properties: {
    company_name: { type: "string" },
    founded_year: { type: "number" },
    headquarters: { type: "string" },
  },
  required: ["company_name"],
};

for await (const message of query({
  prompt: "Research Snowflake and provide key company information",
  options: {
    cwd: process.cwd(),
    outputFormat: { type: "json_schema", schema },
  },
})) {
  if (message.type === "result" && message.structured_output) {
    console.log(message.structured_output);
    // { company_name: "Snowflake", founded_year: 2012, headquarters: "Bozeman, MT" }
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, CortexCodeAgentOptions, ResultMessage

schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "founded_year": {"type": "number"},
        "headquarters": {"type": "string"},
    },
    "required": ["company_name"],
}

async def main():
    async for message in query(
        prompt="Research Snowflake and provide key company information",
        options=CortexCodeAgentOptions(
            cwd=".",
            output_format={"type": "json_schema", "schema": schema},
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            print(message.structured_output)
            # {'company_name': 'Snowflake', 'founded_year': 2012, 'headquarters': 'Bozeman, MT'}

asyncio.run(main())
```

## Type-safe schemas with Zod and Pydantic

Instead of writing JSON Schema by hand, use [Zod](https://zod.dev/) (TypeScript) or
[Pydantic](https://docs.pydantic.dev/latest/) (Python) to define your schema. These libraries generate the
JSON Schema for you and let you parse the response into a fully typed object with autocomplete and type checking.

TypeScript (Zod)Python (Pydantic)

Copy code

```
import { z } from "zod";
import { query } from "cortex-code-agent-sdk";

const FeaturePlan = z.object({
  feature_name: z.string(),
  summary: z.string(),
  steps: z.array(
    z.object({
      step_number: z.number(),
      description: z.string(),
      estimated_complexity: z.enum(["low", "medium", "high"]),
    })
  ),
  risks: z.array(z.string()),
});

type FeaturePlan = z.infer<typeof FeaturePlan>;

const schema = z.toJSONSchema(FeaturePlan);

for await (const message of query({
  prompt: "Plan how to add dark mode support to a React app.",
  options: {
    cwd: process.cwd(),
    outputFormat: { type: "json_schema", schema },
  },
})) {
  if (message.type === "result" && message.structured_output) {
    const parsed = FeaturePlan.safeParse(message.structured_output);
    if (parsed.success) {
      const plan: FeaturePlan = parsed.data;
      console.log(`Feature: ${plan.feature_name}`);
      plan.steps.forEach((step) => {
        console.log(`${step.step_number}. [${step.estimated_complexity}] ${step.description}`);
      });
    }
  }
}
```

Copy code

```
import asyncio
from pydantic import BaseModel
from cortex_code_agent_sdk import query, CortexCodeAgentOptions, ResultMessage

class Step(BaseModel):
    step_number: int
    description: str
    estimated_complexity: str  # 'low', 'medium', 'high'

class FeaturePlan(BaseModel):
    feature_name: str
    summary: str
    steps: list[Step]
    risks: list[str]

async def main():
    async for message in query(
        prompt="Plan how to add dark mode support to a React app.",
        options=CortexCodeAgentOptions(
            cwd=".",
            output_format={
                "type": "json_schema",
                "schema": FeaturePlan.model_json_schema(),
            },
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            plan = FeaturePlan.model_validate(message.structured_output)
            print(f"Feature: {plan.feature_name}")
            for step in plan.steps:
                print(f"{step.step_number}. [{step.estimated_complexity}] {step.description}")

asyncio.run(main())
```

## Example: TODO tracking agent

This example shows structured outputs with multi-step tool use. The agent finds TODO comments in a codebase using
built-in tools (Grep, Bash), then returns the results as structured data. Optional fields like `author` handle cases
where git blame information may not be available.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

const todoSchema = {
  type: "object",
  properties: {
    todos: {
      type: "array",
      items: {
        type: "object",
        properties: {
          text: { type: "string" },
          file: { type: "string" },
          line: { type: "number" },
          author: { type: "string" },
          date: { type: "string" },
        },
        required: ["text", "file", "line"],
      },
    },
    total_count: { type: "number" },
  },
  required: ["todos", "total_count"],
};

for await (const message of query({
  prompt: "Find all TODO comments in this codebase and identify who added them",
  options: {
    cwd: process.cwd(),
    outputFormat: { type: "json_schema", schema: todoSchema },
  },
})) {
  if (message.type === "result" && message.structured_output) {
    const data = message.structured_output;
    console.log(`Found ${data.total_count} TODOs`);
    data.todos.forEach((todo) => {
      console.log(`${todo.file}:${todo.line} - ${todo.text}`);
      if (todo.author) {
        console.log(`  Added by ${todo.author} on ${todo.date}`);
      }
    });
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, CortexCodeAgentOptions, ResultMessage

todo_schema = {
    "type": "object",
    "properties": {
        "todos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "number"},
                    "author": {"type": "string"},
                    "date": {"type": "string"},
                },
                "required": ["text", "file", "line"],
            },
        },
        "total_count": {"type": "number"},
    },
    "required": ["todos", "total_count"],
}

async def main():
    async for message in query(
        prompt="Find all TODO comments in this codebase and identify who added them",
        options=CortexCodeAgentOptions(
            cwd=".",
            output_format={"type": "json_schema", "schema": todo_schema},
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            data = message.structured_output
            print(f"Found {data['total_count']} TODOs")
            for todo in data["todos"]:
                print(f"{todo['file']}:{todo['line']} - {todo['text']}")
                if "author" in todo:
                    print(f"  Added by {todo['author']} on {todo['date']}")

asyncio.run(main())
```

## Example: SQL query results

Cortex Code has built-in Snowflake SQL tools. You can combine them with structured output to get typed query results:

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

const schema = {
  type: "object",
  properties: {
    top_customers: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          total_revenue: { type: "number" },
          order_count: { type: "number" },
        },
        required: ["name", "total_revenue", "order_count"],
      },
    },
    query_used: { type: "string" },
  },
  required: ["top_customers", "query_used"],
};

for await (const message of query({
  prompt: "Find the top 5 customers by revenue from the ORDERS table",
  options: {
    cwd: process.cwd(),
    connection: "my-connection",
    outputFormat: { type: "json_schema", schema },
  },
})) {
  if (message.type === "result" && message.structured_output) {
    const { top_customers, query_used } = message.structured_output;
    console.log(`Query: ${query_used}`);
    top_customers.forEach((c) => {
      console.log(`${c.name}: $${c.total_revenue} (${c.order_count} orders)`);
    });
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, CortexCodeAgentOptions, ResultMessage

schema = {
    "type": "object",
    "properties": {
        "top_customers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "total_revenue": {"type": "number"},
                    "order_count": {"type": "number"},
                },
                "required": ["name", "total_revenue", "order_count"],
            },
        },
        "query_used": {"type": "string"},
    },
    "required": ["top_customers", "query_used"],
}

async def main():
    async for message in query(
        prompt="Find the top 5 customers by revenue from the ORDERS table",
        options=CortexCodeAgentOptions(
            cwd=".",
            connection="my-connection",
            output_format={"type": "json_schema", "schema": schema},
        ),
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            data = message.structured_output
            print(f"Query: {data['query_used']}")
            for c in data["top_customers"]:
                print(f"{c['name']}: ${c['total_revenue']} ({c['order_count']} orders)")

asyncio.run(main())
```

## Output format configuration

The `outputFormat` (TypeScript) or `output_format` (Python) option accepts an object with the following fields:

| Field | Value | Description |
| --- | --- | --- |
| `type` | `"json_schema"` | Required. Only `json_schema` is supported. |
| `schema` | JSON Schema object | Defines the output structure. Generate from Zod with `z.toJSONSchema()` or Pydantic with `.model_json_schema()`. |

Expand

Show lessSee more

Standard JSON Schema features are supported: all basic types (`object`, `array`, `string`, `number`,
`boolean`, `null`), `enum`, `const`, `required`, nested objects, and `$ref` definitions.

## Error handling

Structured output generation can fail when the agent cannot produce valid JSON matching your schema. When this happens,
the result message has a `subtype` indicating what went wrong:

| Subtype | Meaning |
| --- | --- |
| `success` | Output was generated and validated successfully |
| `error_max_structured_output_retries` | Agent could not produce valid output after multiple attempts |

Expand

Show lessSee more

TypeScriptPython

Copy code

```
for await (const msg of query({
  prompt: "Extract contact info from the document",
  options: {
    cwd: process.cwd(),
    outputFormat: { type: "json_schema", schema: contactSchema },
  },
})) {
  if (msg.type === "result") {
    if (msg.subtype === "success" && msg.structured_output) {
      console.log(msg.structured_output);
    } else if (msg.subtype === "error_max_structured_output_retries") {
      console.error("Could not produce valid output");
    }
  }
}
```

Copy code

```
async for message in query(
    prompt="Extract contact info from the document",
    options=CortexCodeAgentOptions(
        cwd=".",
        output_format={"type": "json_schema", "schema": contact_schema},
    ),
):
    if isinstance(message, ResultMessage):
        if message.subtype == "success" and message.structured_output:
            print(message.structured_output)
        elif message.subtype == "error_max_structured_output_retries":
            print("Could not produce valid output")
```

Tip

**Tips for avoiding errors:**

- **Keep schemas focused.** Deeply nested schemas with many required fields are harder to satisfy. Start simple and
  add complexity as needed.
- **Match schema to task.** If the task might not have all the information your schema requires, make those fields
  optional.
- **Use clear prompts.** Ambiguous prompts make it harder for the agent to know what output to produce.

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
