# Build a chat assistant

A chat assistant lets people ask an app questions in plain language. The app
sends each question to a model through the
[Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api), runs the
tools the model asks for, and returns the answer. The tools are the same
functions that serve the app’s pages, so chat answers match what the UI shows.
The whole loop runs inside the app, and it needs no other Snowflake objects.

The example on this page uses a Next.js app built from the App Runtime
template, and the tool list from
[Build an MCP server with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-mcp-server). An app can have a
chat assistant, an MCP server, or both.

## Before you begin

- A Node.js app on App Runtime that uses the
  [Node.js SDK](/developer-guide/snowflake-app-runtime/nodejs-sdk). See
  [Build a Node.js app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-nodejs-app).
- A `lib/tools.ts` file that lists your tools, as described in
  [Add an MCP server to a Node.js app](/developer-guide/snowflake-app-runtime/build-mcp-server#label-snowflake-app-runtime-mcp-nodejs).
  You don’t need to add the MCP route, but install Zod with `npm install zod`.
- Access to the Cortex REST API and the model you choose for the app’s owner
  role, through the `SNOWFLAKE.CORTEX_USER` or
  `SNOWFLAKE.CORTEX_REST_API_USER` database role. `SNOWFLAKE.CORTEX_USER` is
  granted to `PUBLIC` by default. See
  [Cortex REST API](/user-guide/snowflake-cortex/cortex-rest-api)
  and [Model availability for Snowflake Cortex AI](/user-guide/snowflake-cortex/model-availability).

## How the assistant works

Each question runs as a short loop on the app’s server:

1. The chat route sends the conversation and the tool list to the Cortex Chat
   Completions API, `/api/v2/cortex/v1/chat/completions`.
2. If the model asks for tools, the route runs them from `lib/tools.ts` and
   sends the results back.
3. When the model answers without asking for a tool, the route returns that
   answer to the browser.

The SDK’s [`fetch()`](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-rest)
signs each request with the app’s own token, so the app stores no API key.

## Add the chat route

Create `app/api/chat/route.ts`:

Copy code

```
import { z } from "zod";
import { snowflake } from "@/lib/snowflake";
import { tools } from "@/lib/tools";

export const dynamic = "force-dynamic";

const MODEL = "claude-sonnet-5";
const MAX_TURNS = 5;
const MAX_RESULT_CHARS = 20_000;

const SYSTEM_PROMPT =
  "You answer questions about this app's data. Use the tools to look up figures, " +
  "and say which tool each figure came from. If the tools can't answer, say so.";

const requestSchema = z.object({
  messages: z
    .array(z.object({ role: z.enum(["user", "assistant"]), content: z.string().max(4_000) }))
    .min(1)
    .max(40),
});

const toolDefinitions = tools.map((tool) => ({
  type: "function",
  function: {
    name: tool.name,
    description: tool.description,
    parameters: z.toJSONSchema(tool.schema, { io: "input" }),
  },
}));

async function complete(messages: unknown[]) {
  const response = await snowflake.fetch("/api/v2/cortex/v1/chat/completions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model: MODEL, messages, tools: toolDefinitions }),
  });
  if (!response.ok) {
    console.error("[chat] Cortex returned", response.status, (await response.text()).slice(0, 300));
    throw new Error("The model request failed");
  }
  const body = await response.json();
  return body.choices[0].message;
}

async function runTool(name: string, rawArgs: string, request: Request): Promise<string> {
  const tool = tools.find((t) => t.name === name);
  if (!tool) return JSON.stringify({ error: `Unknown tool: ${name}` });
  try {
    const args = tool.schema.parse(JSON.parse(rawArgs || "{}"));
    const text = JSON.stringify(await tool.run(args, request));
    return text.length > MAX_RESULT_CHARS
      ? text.slice(0, MAX_RESULT_CHARS) + " [result cut: ask for fewer rows]"
      : text;
  } catch (e) {
    console.error(`[chat] ${name} failed`, e);
    // Tell the model what was wrong with its arguments; keep query errors generic.
    if (e instanceof z.ZodError) {
      return JSON.stringify({ error: `Invalid arguments: ${e.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ")}` });
    }
    return JSON.stringify({ error: "The tool failed. Try different arguments." });
  }
}

export async function POST(request: Request): Promise<Response> {
  const parsed = requestSchema.safeParse(await request.json().catch(() => null));
  if (!parsed.success) return Response.json({ error: "Invalid request" }, { status: 400 });

  const messages: any[] = [{ role: "system", content: SYSTEM_PROMPT }, ...parsed.data.messages];
  try {
    for (let turn = 0; turn < MAX_TURNS; turn++) {
      const message = await complete(messages);
      if (!message.tool_calls?.length) return Response.json({ reply: message.content ?? "" });

      messages.push(message);
      for (const call of message.tool_calls) {
        console.log(`[chat] tool=${call.function.name}`);
        messages.push({
          role: "tool",
          tool_call_id: call.id,
          content: await runTool(call.function.name, call.function.arguments, request),
        });
      }
    }
    return Response.json({ reply: "I couldn't finish that answer. Try a narrower question." });
  } catch {
    return Response.json({ error: "The assistant is unavailable. Try again." }, { status: 502 });
  }
}
```

The route follows the same rules as the MCP server:

- **It validates every argument** with the tool’s schema before it runs the
  tool, and the tools pass arguments to SQL as bind variables.
- **It returns tool errors to the model** instead of failing the request, so
  the model can try again. Argument errors say which argument was wrong. Query
  errors stay generic, and the full error goes to the app log.
- **It limits the work for each question** with `MAX_TURNS` and
  `MAX_RESULT_CHARS`.
- **It keeps no state between requests.** The browser sends the whole
  conversation each time, so any instance of the app can answer.

To use a different model, change `MODEL` to a model that supports tool calling.
See [Tool calling](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-tool-calling-chain-of-thought).

## Add the chat page

Create `app/chat/page.tsx`. The page keeps the conversation in the browser and
sends it to the chat route with each question:

Copy code

```
"use client";

import { useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  async function send(event: React.FormEvent) {
    event.preventDefault();
    if (!input.trim() || busy) return;
    const next: Message[] = [...messages, { role: "user", content: input.trim() }];
    setMessages(next);
    setInput("");
    setBusy(true);
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next }),
      });
      const body = await response.json();
      setMessages([...next, { role: "assistant", content: body.reply ?? body.error }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-4 text-2xl font-semibold">Ask about orders</h1>
      <div className="space-y-3">
        {messages.map((m, i) => (
          <p key={i} className={m.role === "user" ? "font-medium" : "whitespace-pre-wrap"}>
            {m.content}
          </p>
        ))}
        {busy && <p className="text-gray-500">Thinking...</p>}
      </div>
      <form onSubmit={send} className="mt-4 flex gap-2">
        <input
          className="flex-1 rounded border px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Which region had the largest order this week?"
        />
        <button className="rounded border px-4 py-2" disabled={busy}>
          Send
        </button>
      </form>
    </main>
  );
}
```

## Choose whose rights chat uses

The example calls the Cortex REST API and runs its tools with the app’s owner
rights. Everyone who can open the app gets the same answers.

To answer as the signed-in user, use caller’s rights in both places: query
with `snowflake.asCaller({ headers: request.headers })` in the tools, and call
the model with `snowflake.asCaller({ headers: request.headers }).fetch()`.
Each user then needs access to the Cortex REST API and the model. See
[Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).

## Run and deploy

1. Run the app locally and open `/chat`. On your machine, `fetch()` needs a
   Snowflake CLI connection that signs in with OAuth or a
   [programmatic access token](/user-guide/programmatic-access-tokens). A
   connection that uses a password, a key pair, or a browser can run queries
   but can’t call the Cortex REST API. See
   [Call account REST APIs](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-rest).
2. Ask a question that needs a tool, and check the app’s output for
   `[chat] tool=` lines.
3. Deploy the app, and open `/chat` on the deployed app. See
   [Deploy an app to Snowflake App Runtime](/developer-guide/snowflake-app-runtime/deploy).

Note

A programmatic access token signs in only when your user has a network
policy, unless an authentication policy sets
`NETWORK_POLICY_EVALUATION = ENFORCED_NOT_REQUIRED`. See
[Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

## Limitations and considerations

- Each question runs within one request. `fetch()` times out after 120 seconds
  by default; pass `timeoutMs` for slower models or longer loops.
- If the app restarts during a question, that answer is lost and the user asks
  again.
- The example waits for the whole answer. To show text as it arrives, request
  a streaming response and forward it to the browser. See
  [Streaming](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-streaming).
- Model calls use Cortex REST API credits. See
  [Cost and credit usage for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/cost) and the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
