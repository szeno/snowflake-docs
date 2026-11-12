# Snowflake App Runtime SDK for Node.js

The Snowflake App Runtime SDK for Node.js,
[`@snowflake/sar-sdk`](https://www.npmjs.com/package/@snowflake/sar-sdk), gives
the server code of a Snowflake App Runtime app access to Snowflake. It runs
queries with owner’s rights or caller’s rights, handles large and long-running
results, reads secrets, and calls the account’s REST APIs. In a deployed app it
uses the credentials Snowflake provides; on your machine it uses a connection
configured in `connections.toml` or `config.toml`. The SDK works with any Node.js web framework and is built on the
[Snowflake Node.js driver](/developer-guide/node-js/nodejs-driver), which it
installs as a dependency.

The Next.js template that the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill scaffolds is built on the SDK: its `lib/snowflake.ts` creates the client
for you. For how to query from that template, see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).

The SDK runs in Node.js server code only. Don’t import it from code that runs in
the browser. Browser code calls your app’s own server endpoints, and those
endpoints query Snowflake.

## Requirements

- Node.js 22 or later.
- For TypeScript, set `moduleResolution` to `NodeNext` or `Bundler` and include
  the Node.js type declarations. The SDK is tested with TypeScript 5.9.

The package includes both ES module and CommonJS builds.

## Install the SDK

Copy code

```
npm install @snowflake/sar-sdk
```

## Create a client

Create one client per server process, reuse it across requests, and close it
when the process shuts down. Storing the client on `globalThis` keeps a single
client when a development server reloads your modules:

Copy code

```
import { createSarClient, type SarClient } from "@snowflake/sar-sdk";
import { createConnectionOptions, fromDefault } from "@snowflake/sar-sdk/auth";

const cache = globalThis as typeof globalThis & { snowflake?: SarClient };

export const snowflake = (cache.snowflake ??= createSarClient(
  createConnectionOptions(fromDefault(), {
    callerAsOwner: process.env.NODE_ENV === "development",
  }),
));
```

`fromDefault()` reads the
[session token](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens)
that Snowflake writes for a deployed app, and the default connection in
`connections.toml` or `config.toml` when that token isn’t there. The client reads credentials only when a
query or request needs them, and reads the session token again for each new
session, so token rotation needs no restart. For `callerAsOwner`, see
[Run queries with caller’s rights](#label-snowflake-app-runtime-sdk-callers-rights).

To stop the client, call `await snowflake.close()`. It stops new work, gives
running queries a grace period (10 seconds by default), and then releases its
sessions.

## Run queries

`query()` runs a statement with owner’s rights, as the app’s service identity,
and returns its rows:

Copy code

```
const { rows } = await snowflake.query(
  "SELECT name, price FROM products WHERE id = ?",
  { binds: [productId] },
);
```

- Each row is an object keyed by column name. Unquoted column names are
  uppercase, such as `NAME` and `PRICE`.
- `NUMBER` values are returned as strings, which keeps their full precision. To
  get JavaScript numbers, pass `numbers: "number"`. A value that a JavaScript
  number can’t represent exactly fails with `RESULT_CONVERSION_UNSUPPORTED`
  instead of being rounded.
- The result also contains `queryId`, `columns`, `rowCount` (the number of rows
  returned), and, for DML statements, `affectedRows`.

Each query runs in its own session. For session state that spans statements, see
[Run a transaction](#label-snowflake-app-runtime-sdk-transactions). For owner’s rights and
caller’s rights, bind variables, and choosing a warehouse, see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).

## Run queries with caller’s rights

`asCaller()` returns a caller view of the client that runs queries as the
signed-in user who sent the request. Create it from the request’s headers:

Copy code

```
export async function GET(request: Request) {
  const caller = snowflake.asCaller({ headers: request.headers });
  const { rows } = await caller.query("SELECT CURRENT_USER() AS name");
  return Response.json(rows[0]);
}
```

- The caller view reads the caller’s token from the
  `Sf-Context-Current-User-Token` header that Snowflake adds to each request.
  Use the caller view only within the request it was created for.
- A caller view created without caller headers throws
  `CALLER_CONTEXT_REQUIRED`. It never falls back to owner’s rights.
- Caller queries use the user’s default role and warehouse. For users without a
  default warehouse, pass `warehouse` with each query, or set the
  `SNOWFLAKE_WAREHOUSE` environment variable for the app.
- Caller queries need caller grants on the data and the warehouses they use. See
  [Scoping caller’s rights](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-callers-rights-controls).

On your machine, requests don’t carry a caller token. When you create the client
with `callerAsOwner: true`, as in the
[client example](#label-snowflake-app-runtime-sdk-create-client), caller views
run with the app’s own credentials instead of failing. Set `callerAsOwner` from
a condition that’s true only during development, so a deployed app keeps the
caller’s identity.

## Stream large results

By default, `query()` fails with `RESULT_LIMIT_EXCEEDED` when a result exceeds
100,000 rows or 32 MiB. For larger results, use `stream()` and read the rows as
they arrive:

Copy code

```
const stream = await snowflake.stream("SELECT * FROM events ORDER BY created_at");
for await (const row of stream) {
  await write(row);
}
```

A stream has one reader. Leaving the loop early, or calling `stream.close()`,
releases its session.

## Run a transaction

`transaction()` runs its callback in one session. It commits when the callback
finishes and rolls back when the callback throws:

Copy code

```
await snowflake.transaction(async (tx) => {
  await tx.query("UPDATE accounts SET balance = balance - ? WHERE id = ?", {
    binds: [100, "A"],
  });
  await tx.query("UPDATE accounts SET balance = balance + ? WHERE id = ?", {
    binds: [100, "B"],
  });
});
```

Await every statement in the callback. Keep DDL statements, such as
`CREATE TEMPORARY TABLE`, out of the callback, because DDL commits an open
transaction in Snowflake. See [DDL](/sql-reference/transactions#label-transactions-ddl).

For other work that spans statements, such as temporary tables or session
variables, use `withConnection()`. It passes your callback a Snowflake Node.js
driver connection and releases the connection when the callback’s promise
settles.

## Run long-running queries

A query that can outlast an HTTP request, or the server instance that started
it, can run as a detached query. One request submits the query and returns right
away. Later requests check on it, and any instance of the app can handle them:

Copy code

```
// Submit the query, save its reference with the user it belongs to, and return.
const reference = await snowflake.submitDetached("CALL refresh_report()", {
  executionTimeoutMs: 600_000,
});
await jobs.save({ userId, reference });
return Response.json({ queryId: reference.queryId }, { status: 202 });
```

Copy code

```
// In a later request: load the saved reference for this user and check once.
const { reference } = await jobs.load(userId, queryId);
const outcome = await snowflake.pollQuery(reference);
if (outcome.status === "pending") {
  return Response.json(outcome, { status: 202 });
}
return Response.json(outcome.result.rows);
```

In these examples, `jobs` stands for storage that your app provides and that all
of its instances share.

- `pollQuery()` checks the query once and returns `pending` while it runs. The
  browser decides when to ask again.
- The reference holds the query ID and the identity that ran it, but no
  credentials. It isn’t proof of access: store it on the server with the user it
  belongs to, and never accept a reference from the browser. Each lookup checks
  that the current identity matches the reference, and fails with
  `QUERY_IDENTITY_MISMATCH` otherwise.
- For results larger than the row and size limits saved with the reference, use
  `streamQuery()`.
  To check status without reading results, use `getQueryStatus()`, and to stop a
  query, use `cancelQuery()`. Closing the browser doesn’t cancel the query.
- Submitting a detached query requires
  [ABORT\_DETACHED\_QUERY](/sql-reference/parameters#label-abort-detached-query)
  set to `FALSE` and [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) set to
  `TRUE`. Otherwise the SDK throws
  `DETACHED_QUERY_NOT_SUPPORTED`.

Caller views have the same methods. To look up a caller’s query from a later
request, the owner role needs the `CALLER MONITOR` caller grant on the
warehouse; without it, the lookup fails with `QUERY_UNAVAILABLE`. To cancel a
caller’s query, it needs `CALLER OPERATE`; without it, the cancel request fails
with Snowflake error `003001`, and the query keeps running.

To wait for a query within one process instead, use `submit()`. It returns a
handle with `status()`, `result()`, and `cancel()`. The handle exists only in the
process that created it.

## Read secrets

To read a secret that you declare under
[`secrets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-secrets)
in `app.yml`, pass its name:

Copy code

```
const apiKey = await snowflake.secrets.getString("API_KEY");
const { username, password } = await snowflake.secrets.getPassword("DB_CREDS");
const token = await snowflake.secrets.getAccessToken("PARTNER_API");
```

In a deployed app, the SDK reads the
[secret files](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-secret-files) under
`/secrets/<name>/` on every call, so a rotated secret takes effect without a
restart. On your machine, it reads environment variables instead, such as
`SNOWFLAKE_SECRET_API_KEY_SECRET_STRING`, or `SNOWFLAKE_SECRET_DB_CREDS_USERNAME`
and `SNOWFLAKE_SECRET_DB_CREDS_PASSWORD`. Reading secrets doesn’t open a
Snowflake session.

## Call account REST APIs

`fetch()` sends an authenticated request to one of the account’s
[REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api) with the same
identity as the client’s queries, and returns a standard `Response`:

Copy code

```
const response = await snowflake.fetch("/api/v2/warehouses");
if (!response.ok) {
  await response.body?.cancel();
  throw new Error(`Account API returned HTTP ${response.status}`);
}
const warehouses = await response.json();
```

- Pass a path on the account, not a full URL.
- To call the API as the signed-in user, use
  `snowflake.asCaller({ headers: request.headers }).fetch(path)`.
- `fetch()` needs an OAuth or programmatic access token connection. A deployed
  app’s session token is an OAuth token. On your machine, a connection that signs
  in with a password, a key pair, or a browser can run queries but can’t call
  `fetch()`.
- Each request times out after 120 seconds by default. Pass `timeoutMs` for
  longer requests, such as streaming responses.
- Read or cancel every response body. HTTP error statuses aren’t thrown or
  retried.

## Connect from your machine

On your machine, `fromDefault()` reads the default connection from
`connections.toml` or `config.toml`, the configuration files that the Snowflake
CLI and other Snowflake tools share. For where those files live and how to
define a connection, see
[Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections). To use
another connection, pass `fromToml({ name: "my_connection" })` to
`createConnectionOptions()` instead of `fromDefault()`.

- On macOS and Linux, the configuration file must be readable only by you
  (`chmod 0600`).
- For a connection that signs in with a browser (`EXTERNALBROWSER`), the SDK
  turns on the driver’s token cache, so you aren’t asked to sign in for every
  query. The account must allow it with
  [ALLOW\_ID\_TOKEN](/sql-reference/parameters#label-allow-id-token).

## Handle errors

Errors that the SDK throws have a stable `code`. When Snowflake rejects a
statement, `details.errorCode` holds Snowflake’s error code:

Copy code

```
import { isSarError } from "@snowflake/sar-sdk";

try {
  await snowflake.query("UPDATE orders SET status = 'SHIPPED' WHERE id = ?", {
    binds: [orderId],
  });
} catch (error) {
  if (isSarError(error) && error.details.errorCode === "002003") {
    return new Response("Orders table unavailable", { status: 503 });
  }
  throw error;
}
```

- The SDK never retries SQL. Before you retry a write yourself, check
  `details.completion`: `"succeeded"` means the statement ran even though reading
  its result failed, and `"unknown"` means it might have run.
- Snowflake’s error message can quote values from the SQL, so it’s kept out of
  the error’s `message` and `toJSON()` and appears only in its `cause`. Log
  errors on the server and
  [return a generic message](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-error-handling)
  to the user.
- Configuration errors include a `details.nextStep` hint.

The following table lists common error codes:

| Code | Meaning |
| --- | --- |
| `AUTH_FAILED` | Signing in to Snowflake failed. |
| `CALLER_CONTEXT_REQUIRED` | A caller view was created without the caller’s token. |
| `CONFIG_NOT_FOUND` | The connection or configuration file wasn’t found. |
| `QUERY_FAILED` | Snowflake rejected or failed the statement. See `details.errorCode`. |
| `QUERY_UNAVAILABLE` | A long-running query’s status or results aren’t available: it expired, the identity can’t see it, or it’s unknown. |
| `RESULT_LIMIT_EXCEEDED` | The result exceeds the `query()` row or size limit. Use [`stream()`](#label-snowflake-app-runtime-sdk-stream). |
| `TIMEOUT` | An operation didn’t finish before its deadline. |

Expand

Show lessSee more

## API reference

The [package README](https://github.com/snowflakedb/sar-sdk/blob/main/nodejs/README.md)
is the full reference. It covers every option, default, and error code, along
with connection pool settings, logging, and direct use of the Snowflake Node.js
driver. The
[examples](https://github.com/snowflakedb/sar-sdk/tree/main/nodejs/examples)
show complete programs, and the
[changelog](https://github.com/snowflakedb/sar-sdk/blob/main/nodejs/CHANGELOG.md)
lists the changes in each release. To report a problem, open an issue in the
[snowflakedb/sar-sdk](https://github.com/snowflakedb/sar-sdk/issues) repository.
