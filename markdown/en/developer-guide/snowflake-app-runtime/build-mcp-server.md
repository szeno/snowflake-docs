# Build an MCP server

A Snowflake App Runtime app can serve its own tools over the
[Model Context Protocol](https://modelcontextprotocol.io) (MCP). Agents such as
Snowflake CoCo then call the app’s queries and actions directly, without opening
its UI. The app keeps a single sign-in, a single set of grants, and a single
copy of its query code for both people and agents.

The same tools can also power a chat assistant inside the app. See
[Build a chat assistant with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-chat-assistant).

## Before you begin

- An app that runs on App Runtime. See
  [Build a Node.js app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-nodejs-app) or
  [Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app).
- [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) or
  [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop) to test
  the server.

## How the server fits in the app

Follow these rules in any language:

- **Serve one endpoint at `/api/mcp`.** A fixed path keeps the URL
  predictable for anyone who connects.
- **Run stateless Streamable HTTP.** Create the server and transport for each
  request and don’t issue session IDs. App Runtime can run more than one
  instance and can restart the app, so state held in memory between requests
  is lost or split across instances.
- **Accept only `POST`.** Answer `GET` and `DELETE` with `405`. In stateless
  mode there’s no stream or session for them to open or close, and an SDK that
  receives a `GET` holds it open as an empty event stream.
- **Return JSON, not an event stream,** when the SDK lets you choose. Each call
  returns one result, and a JSON body is easier to debug.
- **Don’t add your own authentication.** The App Runtime ingress signs the
  caller in before the request reaches your app, as it does for every other
  route, and adds the caller’s identity headers. Don’t add an API key check or
  an OAuth flow.

## Choose whose rights each tool uses

MCP requests come through the same ingress as browser requests, so each tool
runs queries with
[owner’s rights or caller’s rights](/developer-guide/snowflake-app-runtime/query-snowflake#label-snowflake-app-runtime-query-snowflake-modes),
as your other routes do:

- **Owner’s rights** give every caller what the app’s owner role can read.
  Don’t expose a tool that the UI keeps behind an admin check unless the tool
  makes the same check. Keep write and delete actions off MCP unless you
  intend agents to perform them.
- **Caller’s rights** run as the signed-in user. Use them for data protected
  by row access or masking policies, or for per-user data. If a request
  doesn’t carry the caller’s token, fail the call. Don’t fall back to owner’s
  rights.

## Add an MCP server to a Node.js app

These steps use a Next.js app built from the App Runtime template. To run it
locally, see [Run locally](/developer-guide/snowflake-app-runtime/build-nodejs-app#label-snowflake-app-runtime-build-nodejs-app-run-locally).
For Express, use `StreamableHTTPServerTransport`, the Node.js `http` variant of the
transport.

1. Install the MCP SDK and Zod, which describes each tool’s arguments:

   Copy code

   ```
   npm install @modelcontextprotocol/sdk zod
   ```
2. Create `lib/tools.ts` with your tools. Each tool has a name, a description,
   an argument schema, and a function that calls the same queries your pages
   and API routes use. The MCP server and a
   [chat assistant](/developer-guide/snowflake-app-runtime/build-chat-assistant)
   can both read this list:

   Copy code

   ```
   import { z } from "zod";
   import { snowflake } from "@/lib/snowflake";

   const MAX_ROWS = 200;

   export type Tool = {
     name: string;
     description: string;
     schema: z.ZodObject;
     run: (args: any, request: Request) => Promise<unknown>;
   };

   export const tools: Tool[] = [
     {
       name: "list_orders",
       description:
         "Orders for one region, newest first. Returns ORDER_ID, ORDER_DATE (ISO 8601 date), and AMOUNT (USD).",
       schema: z.object({
         region: z.enum(["AMER", "EMEA", "APJ"]).describe("Sales region"),
         limit: z.number().int().min(1).max(MAX_ROWS).default(50),
       }),
       run: async ({ region, limit }) => {
         const { rows } = await snowflake.query(
           "SELECT ORDER_ID, ORDER_DATE, AMOUNT FROM DB.SCHEMA.ORDERS WHERE REGION = ? ORDER BY ORDER_DATE DESC LIMIT ?",
           { binds: [region, limit] },
         );
         return rows;
       },
     },
   ];
   ```

   For a caller’s rights tool, query with `await asCaller()` from
   `@/lib/snowflake` instead of `snowflake`. Outside the template, use
   `snowflake.asCaller({ headers: request.headers })`.
   See [Query from Node.js](/developer-guide/snowflake-app-runtime/query-snowflake#label-snowflake-app-runtime-query-snowflake-nodejs).
3. Create `app/api/mcp/route.ts`. It registers every tool in the list and
   returns errors as tool results:

   Copy code

   ```
   import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
   import { WebStandardStreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/webStandardStreamableHttp.js";
   import { tools } from "@/lib/tools";

   export const dynamic = "force-dynamic";

   function createServer(request: Request): McpServer {
     const server = new McpServer({ name: "my-app", version: "1.0.0" });
     for (const tool of tools) {
       server.registerTool(
         tool.name,
         { description: tool.description, inputSchema: tool.schema.shape },
         async (args) => {
           console.log(`[mcp] tool=${tool.name}`);
           try {
             const result = await tool.run(args, request);
             return { content: [{ type: "text", text: JSON.stringify(result) }] };
           } catch (e) {
             console.error(`[mcp] ${tool.name} failed`, e);
             return { content: [{ type: "text", text: "Query failed" }], isError: true };
           }
         },
       );
     }
     return server;
   }

   async function handle(request: Request): Promise<Response> {
     const startedAt = Date.now();
     const server = createServer(request);
     const transport = new WebStandardStreamableHTTPServerTransport({
       sessionIdGenerator: undefined,
       enableJsonResponse: true,
     });
     await server.connect(transport);
     const response = await transport.handleRequest(request);
     console.log(`[mcp] ${request.method} status=${response.status} ms=${Date.now() - startedAt}`);
     return response;
   }

   // Next.js answers GET and DELETE with 405 because the route exports only POST.
   export const POST = handle;
   ```

## Add an MCP server to a Python app

These steps add a server to the FastAPI app from
[Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app). Python apps are in
Public Preview. The steps use version 2 of the `mcp` package, which renamed
`FastMCP` to `MCPServer`. Code written for version 1 imports
`mcp.server.fastmcp` and fails on version 2.

1. Add the SDK to `requirements.txt`:

   ```
   mcp>=2.3
   ```
2. Add the server to `app.py`. Put the imports below the `sys.path.insert`
   line, because `mcp` installs into `.python_packages`. Replace
   `app = FastAPI()` with the `app = FastAPI(lifespan=lifespan)` line below,
   and keep your `/` route and the `uvicorn.run` block. `run_query` stands for
   your app’s query helper; see
   [Query from Python](/developer-guide/snowflake-app-runtime/query-snowflake#label-snowflake-app-runtime-query-snowflake-python).

   Copy code

   ```
   from contextlib import asynccontextmanager
   from fastapi import FastAPI, Response
   from mcp.server.mcpserver import MCPServer
   from mcp.server.transport_security import TransportSecuritySettings

   mcp = MCPServer("my-app")

   @mcp.tool()
   def list_orders(region: str, limit: int = 50) -> list[dict]:
       """Orders for one region, newest first, with ORDER_ID, ORDER_DATE, and AMOUNT (USD)."""
       return run_query(
           "SELECT ORDER_ID, ORDER_DATE, AMOUNT FROM DB.SCHEMA.ORDERS "
           "WHERE REGION = %s ORDER BY ORDER_DATE DESC LIMIT %s",
           (region, min(limit, 200)),
       )

   @asynccontextmanager
   async def lifespan(app):
       async with mcp.session_manager.run():
           yield

   app = FastAPI(lifespan=lifespan)

   # Register before the mount so that this route handles GET and DELETE.
   @app.api_route("/api/mcp", methods=["GET", "DELETE"])
   def mcp_post_only() -> Response:
       return Response(status_code=405, headers={"allow": "POST"})

   app.mount("/api", mcp.streamable_http_app(
       stateless_http=True,
       json_response=True,
       transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
   ))
   ```

   `list_orders` runs with owner’s rights.
3. To run a tool with caller’s rights, add a `Context` argument. The `mcp`
   package fills it in and leaves it out of the tool’s schema, and
   `ctx.headers` holds the request’s headers, including the caller token.
   `connect` and `caller_token` come from
   [Query from Python](/developer-guide/snowflake-app-runtime/query-snowflake#label-snowflake-app-runtime-query-snowflake-python):

   Copy code

   ```
   from mcp.server.mcpserver import Context

   @mcp.tool()
   def my_orders(ctx: Context, limit: int = 50) -> list[dict]:
       """Orders the signed-in user can see, newest first, with ORDER_ID, ORDER_DATE, and AMOUNT (USD)."""
       with connect(caller_token(ctx)) as conn:
           cur = conn.cursor(snowflake.connector.DictCursor)
           return cur.execute(
               "SELECT ORDER_ID, ORDER_DATE, AMOUNT FROM DB.SCHEMA.ORDERS "
               "ORDER BY ORDER_DATE DESC LIMIT %s",
               (min(limit, 200),),
           ).fetchall()
   ```

Important

By default, the `mcp` package rejects any `Host` header other than
`localhost` with `421 Invalid Host header`. Behind the App Runtime ingress,
every request carries the app’s public host name, so the server works on your
machine and fails once deployed. Turn off the check as shown, or set
`allowed_hosts` to the app’s exact host name. Wildcards such as `*.domain`
don’t match. The ingress authenticates every request, so the check isn’t
needed in a deployed app.

## Share tools with in-app chat

If your app has a chat assistant, give it the same tools as the MCP server:

- **Define each tool once.** Keep one list, as in `lib/tools.ts` above, and
  have the MCP route and the chat route both read it. Agents and the in-app
  chat then get the same descriptions, limits, and answers.
- **Mark tools that stay in the app.** A tool that needs an admin check, or
  that writes data, can stay in chat behind the app’s own checks and off the
  MCP server. Filter it out when you register MCP tools.
- **Apply the same limits in both places.** Cap rows in the shared tool, not
  in each route, so both models see the same rows. The chat route also cuts
  long results to fit the model’s context, with `MAX_RESULT_CHARS`.

For the chat side, see [Build a chat assistant with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-chat-assistant).

## Write tools that agents can use

- **Reuse the app’s query code.** A tool calls the same helper as the page or
  route that shows the same data, so agents and the UI get the same numbers.
  Don’t open a second connection or copy SQL.
- **Bind every argument.** A model writes the tool arguments. Pass them as
  [bind variables](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-bind-variables),
  never in the SQL text.
- **Describe tools for a model.** Say what the tool returns, the units, and
  when to use it. Give each argument a type, and enums and limits where they
  apply.
- **Limit results.** Cap rows (for example, at 200) and say in the result when
  you cut it. Return dates as ISO 8601 strings.
- **Return errors as tool results.** Set `isError: true` with a short message
  instead of returning HTTP 500, so the agent can read the error and recover.
  Log the full error in the app.
- **Log one line for each request** with the method, tool name, status, and
  duration. The [app logs](/developer-guide/snowflake-app-runtime/observability)
  are the only record of what an agent called.

## Test the server

CoCo CLI and CoCo Desktop both connect to the server. They read the same
`~/.snowflake/cortex/mcp.json` file, so a server you add with `cortex mcp add`
appears in both. To manage servers, see
[CoCo CLI Model Context Protocol (MCP) support](/user-guide/cortex-code/cortex-code-mcp) and
[MCP support in CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/mcp-support).

1. Run the app locally and list its tools. Replace `<port>` with the port the
   app listens on:

   Copy code

   ```
   curl -s http://localhost:<port>/api/mcp \
     -H 'content-type: application/json' \
     -H 'accept: application/json, text/event-stream' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
   ```

   Then call a tool with
   `"method":"tools/call","params":{"name":"<tool>","arguments":{...}}` and
   check that it returns real data.
2. Add the local server to CoCo, and try the tools from an agent
   before you deploy. A local server needs no sign-in:

   Copy code

   ```
   cortex mcp add my-app-local http://localhost:<port>/api/mcp --type http
   ```

   In CoCo CLI, new servers start turned off: turn the server on in `/mcp`.

   On your machine, the Node.js SDK runs queries as the default connection in
   your Snowflake CLI configuration, including caller’s rights queries. A
   Python app needs its own local connection, because the session token file
   exists only in a deployed app.
3. Deploy the app, and find its URL in the output of
   [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services).
4. Add the deployed server. `--snowflake-connection` names the connection
   that CoCo signs in with, so you don’t create or store a token:

   Copy code

   ```
   cortex mcp add my-app https://<app-host>/api/mcp --type http --snowflake-connection <connection>
   ```

   In `mcp.json`, the entry looks like this:

   Copy code

   ```
   "my-app": {
     "type": "http",
     "url": "https://<app-host>/api/mcp",
     "snowflake_connection": "<connection>"
   }
   ```

   The tools appear in your next CoCo session. Turn the server on in
   `/mcp` in CoCo CLI, as for the local server.

## Share the server

Anyone who connects to the server needs the same access as someone who opens
the app in a browser. See [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).
