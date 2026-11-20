# Query Snowflake

A deployed app queries Snowflake with credentials that Snowflake gives it. The
app doesn’t store passwords or keys. Query from Node.js with the
[Snowflake App Runtime SDK](/developer-guide/snowflake-app-runtime/nodejs-sdk),
or from any language with a Snowflake driver, such as the
[Snowflake Connector for Python](/developer-guide/python-connector/python-connector).

## Owner’s rights and caller’s rights

Each query runs in one of two modes:

| Mode | How it works | When to use it |
| --- | --- | --- |
| **Owner’s rights** | Queries run as the service’s own identity (the owner role). All users see the same data. | Shared dashboards, aggregate views, internal tools where every user sees the same results. |
| **Caller’s rights** | Queries run as the end user who opened the app. Snowflake applies that user’s role and privileges. | Apps where different users should see different data, per-user audit trails, row-level security. |

Expand

Show lessSee more

Queries with owner’s rights use the session token that Snowflake writes at
`/snowflake/session/token`. Queries with caller’s rights also use the caller
token that Snowflake adds to each request in the `Sf-Context-Current-User-Token`
header. Caller’s rights needs no `app.yml` setting. Use a caller’s connection
only within the request it came from. See
[Session and caller tokens](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens).

How you use the caller token depends on the
[compute option](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-compare):

- **Serverless compute** (Public Preview): the caller token is a complete OAuth
  token. Authenticate with it alone.
- **Managed compute**: join the session token and the caller token with a dot
  (`<session>.<caller>`).

The Node.js SDK handles both. With a driver, choose the token yourself. The
session token contains dots on managed compute and doesn’t on serverless
compute, so an app that runs on either can check it.

## Query from Node.js

Install the SDK and create one client per server process. See
[Create a client](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-create-client).

Copy code

```
npm install @snowflake/sar-sdk
```

Call `query()` from server code to run a statement with owner’s rights. Pass
values with [`binds`](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-bind-variables)
and `?` placeholders:

Copy code

```
const { rows } = await snowflake.query(
  "SELECT * FROM orders WHERE customer_id = ? AND status = ?",
  { binds: [customerId, status] },
);
```

To query as the signed-in user, create a caller view from the request’s
headers:

Copy code

```
export async function GET(request: Request) {
  const caller = snowflake.asCaller({ headers: request.headers });
  const { rows } = await caller.query("SELECT * FROM sales.detail");
  return Response.json(rows);
}
```

To run a statement on a specific warehouse, pass `warehouse`. Otherwise the
query uses [`query_warehouse`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-query-warehouse)
from `app.yml`, or your local connection’s warehouse on your machine.

`query()` fails with `RESULT_LIMIT_EXCEEDED` when a result exceeds 100,000 rows
or 32 MiB. For larger results and long-running statements, see
[Stream large results](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-stream)
and [Run long-running queries](/developer-guide/snowflake-app-runtime/nodejs-sdk#label-snowflake-app-runtime-sdk-long-running).

On your machine, the SDK uses the default connection in your Snowflake CLI
configuration. Requests don’t carry a caller token there, so caller’s rights
queries run as that connection’s user.

### Apps created from the template

Apps from the Next.js template include `lib/snowflake.ts`, which creates the
client and exports `snowflake` and an `asCaller()` helper that reads the
current request’s headers:

Copy code

```
import { snowflake, asCaller } from "@/lib/snowflake";

const { rows } = await snowflake.query("SELECT * FROM sales.summary");
const caller = await asCaller();
const detail = await caller.query("SELECT * FROM sales.detail");
```

Projects created with an older version of the
[`snowflake-apps`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-snowflake-apps)
skill can have a `lib/snowflake.ts` that always joins the two tokens, which
fails on serverless compute. To update it, ask the current skill from your
project directory:

```
> $snowflake-apps Update lib/snowflake.ts from the current template and preserve project-specific changes
```

## Query from Python

Use the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector).
Add `snowflake-connector-python` to `requirements.txt`, and connect with OAuth
and the token for the query:

Copy code

```
import os
from pathlib import Path

import snowflake.connector

def connect(token):
    return snowflake.connector.connect(
        host=os.environ["SNOWFLAKE_HOST"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        authenticator="oauth",
        token=token,
        warehouse="MY_WH",
    )

def session_token():
    # The token rotates, so read it for each connection.
    return Path("/snowflake/session/token").read_text().strip()

def caller_token(request):
    caller = request.headers.get("sf-context-current-user-token", "")
    session = session_token()
    # Serverless: the caller token alone. Managed: join the two tokens.
    return caller if "." not in session else f"{session}.{caller}"
```

Run owner’s rights queries with `connect(session_token())`, and caller’s rights
queries with `connect(caller_token(request))` in the request handler:

Copy code

```
with connect(caller_token(request)) as conn:
    rows = conn.cursor().execute("SELECT * FROM sales.detail").fetchall()
```

Pass values as bind parameters, not by building SQL strings. See
[Binding data](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-data).

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

## Next steps

- Choose where the app’s own role comes from and share the app: [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).
- Design data access for least privilege: [Build secure Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/secure-development).
