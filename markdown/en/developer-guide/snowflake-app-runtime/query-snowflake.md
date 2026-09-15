# Query Snowflake

Call `querySnowflake` from `lib/snowflake.ts` to run SQL. The
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill adds that file when it scaffolds the app. The helper wraps the Snowflake
driver and manages a connection pool. When the app is deployed it uses the
[session token](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens)
Snowflake writes for the service. On your machine it uses your local Snowflake
connection.

If the project doesn’t have `lib/snowflake.ts`, ask the skill from the project
directory: `$snowflake-apps Add lib/snowflake.ts from the template` in
[Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli), or
`/snowflake-apps Add lib/snowflake.ts from the template` in
[Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps).

## Run a query

Call `querySnowflake` from a server component or route handler. The default
is owner’s rights: the query runs as the service role.

Copy code

```
const rows = await querySnowflake("SELECT * FROM sales.summary");
```

Pass `{ callersRights: true }` to run that query as the signed-in user:

Copy code

```
const rows = await querySnowflake("SELECT * FROM sales.detail", {
  callersRights: true,
});
```

Pass values with [`binds`](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-bind-variables)
and `?` placeholders:

Copy code

```
const rows = await querySnowflake(
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
const rows = await querySnowflake("SELECT * FROM sales.summary", {
  warehouse: "ANALYTICS_WH",
});
```

For statements that can run longer than a few seconds (large scans,
aggregations, or stored procedures), use `querySnowflakeLongRunning`. It
submits the statement, waits for it to finish, then returns the rows. The
same `callersRights`, `binds`, and `warehouse` options apply.

Copy code

```
const rows = await querySnowflakeLongRunning("CALL MY_LONG_JOB()");
```

## Owner’s rights and caller’s rights

Each query runs in one of two modes:

| Mode | How it works | When to use it |
| --- | --- | --- |
| **Owner’s rights** | Queries run as the service’s own identity (the owner role). All users see the same data. | Shared dashboards, aggregate views, internal tools where every user sees the same results. |
| **Caller’s rights** | Queries run as the end user who opened the app. Snowflake applies that user’s role and privileges. | Apps where different users should see different data, per-user audit trails, row-level security. |

Expand

Show lessSee more

Caller’s rights is available on Application Services without an `app.yml`
setting. Each `querySnowflake` call uses owner’s rights unless you pass
`{ callersRights: true }`.

`{ callersRights: true }` has no effect when you run the app on your
machine. The helper uses your local connection instead, and logs a warning.

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

For the types of caller grants and the administrator controls around them, see
[Scoping caller’s rights](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-callers-rights-controls).

## How the helper authenticates

The helper picks credentials in this order:

1. **Session token** at `/snowflake/session/token`. This is the path in a
   deployed app. For owner’s rights, the helper uses that token. For
   caller’s rights, it also reads the
   `Sf-Context-Current-User-Token` request header and combines the two.
   See
   [Session and caller tokens](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens)
   for the paths and how the tokens rotate.
2. **`SNOWFLAKE_USER` and `SNOWFLAKE_PASSWORD`** in the process environment.
   Used for local runs when those variables are set.
3. **Your default Snowflake CLI connection** in `~/.snowflake/connections.toml`
   or `~/.snowflake/config.toml`. Used for local runs when no password
   variables are set.

If none of those are present, the helper fails with
`No Snowflake credentials found.`

To wire the tokens yourself instead of using `lib/snowflake.ts`, see
[Tutorial 7:Create a Snowpark Container Services service that uses caller’s rights](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-7-callers-rights).
