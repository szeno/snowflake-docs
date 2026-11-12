# Query Snowflake

Import `snowflake` and `asCaller` from `lib/snowflake.ts` to run SQL. The
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill adds that file when it scaffolds the app. The file creates a client from the
[Snowflake App Runtime SDK for Node.js](/developer-guide/snowflake-app-runtime/nodejs-sdk),
`@snowflake/sar-sdk`, and keeps one client per server process. When the app is
deployed, the client uses the
[session token](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens)
Snowflake writes for the service. On your machine it uses the default connection in
`connections.toml` or `config.toml`.

If the project doesn’t have `lib/snowflake.ts`, ask the skill from the project
directory: `$snowflake-apps Add lib/snowflake.ts from the template` in
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), or
`/snowflake-apps Add lib/snowflake.ts from the template` in
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps).

## Run a query

Call `snowflake.query()` from a server component, route handler, or server
action. It runs the query with owner’s rights, as the service role, and returns
the rows:

Copy code

```
import { snowflake } from "@/lib/snowflake";

const { rows } = await snowflake.query("SELECT * FROM sales.summary");
```

To run queries as the signed-in user, call `asCaller()` in the request and query
through the caller view it returns. The template’s `asCaller()` takes no
arguments; to create a caller view from the SDK directly, see
[Run queries with caller’s rights](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-callers-rights).

Copy code

```
import { asCaller } from "@/lib/snowflake";

const caller = await asCaller();
const { rows } = await caller.query("SELECT * FROM sales.detail");
```

Pass values with [`binds`](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-bind-variables)
and `?` placeholders:

Copy code

```
const { rows } = await snowflake.query(
  "SELECT * FROM orders WHERE customer_id = ? AND status = ?",
  { binds: [customerId, status] },
);
```

To run a statement on a specific warehouse, pass `warehouse`. When you omit
it, the query uses the connection’s default warehouse (from
[`query_warehouse`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-query-warehouse)
when the app is deployed, or from your local connection on your machine).

Copy code

```
const { rows } = await snowflake.query("SELECT * FROM sales.summary", {
  warehouse: "ANALYTICS_WH",
});
```

`query()` fails with `RESULT_LIMIT_EXCEEDED` when a result exceeds 100,000 rows
or 32 MiB. For larger results, and for
statements that can outlast a request, such as large scans or stored procedures,
see [Stream large results](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-stream)
and [Run long-running queries](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-long-running).

## Owner’s rights and caller’s rights

Each query runs in one of two modes:

| Mode | How it works | When to use it |
| --- | --- | --- |
| **Owner’s rights** | Queries run as the service’s own identity (the owner role). All users see the same data. | Shared dashboards, aggregate views, internal tools where every user sees the same results. |
| **Caller’s rights** | Queries run as the end user who opened the app. Snowflake applies that user’s role and privileges. | Apps where different users should see different data, per-user audit trails, row-level security. |

Expand

Show lessSee more

Caller’s rights is available on Application Services without an `app.yml`
setting. Queries through `snowflake` use owner’s rights. Queries through the
caller view that `asCaller()` returns use caller’s rights for the current
request; use the caller view only within that request.

When you run the app on your machine with `npm run dev`, requests don’t carry a
caller token, so `asCaller()` queries run with your local connection instead.

Where the execution role comes from is covered in
[Execution context](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-execute-as-role).
For when to prefer caller’s rights, see
[Data access design](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-data-access).

## Caller grants

Caller’s rights uses
[restricted caller’s rights](/developer-guide/restricted-callers-rights).
The calling user’s privileges and the service owner’s caller grants must
both allow the operation. Without those grants, a caller’s rights query
can’t read the caller’s data.

Copy code

```
GRANT CALLER USAGE ON DATABASE my_db TO ROLE service_owner_role;
GRANT CALLER USAGE ON SCHEMA my_db.my_schema TO ROLE service_owner_role;
GRANT CALLER SELECT ON ALL TABLES IN SCHEMA my_db.my_schema TO ROLE service_owner_role;
```

Caller’s rights queries that use a warehouse also need caller grants on that
warehouse, such as `CALLER USAGE`. For the types of caller grants and the administrator controls around them, see
[Scoping caller’s rights](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-callers-rights-controls).

## How the client authenticates

The client picks credentials in this order:

1. **Session token** at `/snowflake/session/token`. This is the path in a
   deployed app. For owner’s rights, the client uses that token. For
   caller’s rights, `asCaller()` also reads the
   `Sf-Context-Current-User-Token` request header and combines the two.
   See
   [Session and caller tokens](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens)
   for the paths and how the tokens rotate.
2. **The default connection** in `connections.toml` or `config.toml`, the
   configuration files that the Snowflake CLI and other Snowflake tools share.
   Used for local runs. For where those files live, see
   [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

If neither is present, the first query fails with `CONFIG_NOT_FOUND`.

To use the SDK outside the template, see
[Snowflake App Runtime SDK for Node.js](/developer-guide/snowflake-app-runtime/nodejs-sdk). To wire the tokens
yourself, see
[Tutorial 7: Create a Snowpark Container Services service that uses caller’s rights](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-7-callers-rights).
