# Runtime environment

Snowflake sets the listen address, connection details, and session token
for the running app. Declare
[`environment_variables`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-environment-variables)
and
[`secrets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-secrets)
in [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml).

## Listen address

Read `PORT` and `HOSTNAME` and listen on that address:

Copy code

```
const port = Number(process.env.PORT ?? 8080);
const hostname = process.env.HOSTNAME ?? "0.0.0.0";

app.listen(port, hostname);
```

In Python:

Copy code

```
import os

import uvicorn

uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
```

`HOSTNAME` is the bind address. Users reach the app over HTTPS at a
`*.snowflakecomputing.app` URL; the app serves plain HTTP.
On [serverless compute](/developer-guide/snowflake-app-runtime/serverless)
(Public Preview), the URL is on the account’s `snowflake.app` domain instead. See
[URL prefix](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-app-runtime-app-yml-serverless-url).

## Language runtime

Set the top-level
[`runtime`](/developer-guide/snowflake-app-runtime/app-yml) key in `app.yml`
to `node` or `python`. The value is case-insensitive and defaults to `node`.
Snowflake ignores a `runtime` key inside a target.

### Node.js

Apps run on Node.js 22. You can use `npm`, `npx`, and `pnpm` for install and
build steps. Snowflake doesn’t preinstall Node.js packages, so list your
dependencies in `package.json`. For a complete app, see
[Build a Node.js app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-nodejs-app).

### Python

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Set `runtime: python`. Python apps run on Python 3.13 on
[serverless compute](/developer-guide/snowflake-app-runtime/serverless),
so also set `compute_resource: SERVERLESS`.

You can use `pip` and `uv` to install dependencies. Install them into the
project directory so they’re included in the deployed app. For example, this
`install` command writes packages to `.python_packages`:

Copy code

```
install:
  commands:
    - ["pip", "install", "--upgrade", "--target", ".python_packages", "-r", "requirements.txt"]
```

Python doesn’t search `.python_packages` by default, so add it to `sys.path`
before you import your dependencies:

Copy code

```
import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parent / ".python_packages"))
```

Add `.venv` and `.python_packages` to `ignore` so the source upload excludes
local dependencies. For a complete app, see
[Build a Python app for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/build-python-app).

## Built-in environment variables

Snowflake sets these at runtime. Read them from `process.env` in Node.js or
`os.environ` in Python.

**Listen**

| Variable | Purpose |
| --- | --- |
| `PORT` | The port to listen on |
| `HOSTNAME` | The address to bind |

Expand

Show lessSee more

**Account**

| Variable | Purpose |
| --- | --- |
| `SNOWFLAKE_ACCOUNT` | [Account locator](/user-guide/admin-account-identifier#label-account-locator) for the account the service runs in |
| `SNOWFLAKE_HOST` | Hostname for a driver connection from the running app |
| `SNOWFLAKE_PORT` | Connection port when Snowflake sets one (often `443`) |
| `SNOWFLAKE_PROTOCOL` | Connection protocol when it isn’t `https` (usually unset) |
| `SNOWFLAKE_AUTH_MODE` | Always `oauth` |
| `SNOWFLAKE_INSECURE_MODE` | Always `true` |

Expand

Show lessSee more

**Service object**

| Variable | Purpose |
| --- | --- |
| `SNOWFLAKE_DATABASE` | Database that contains the Application Service |
| `SNOWFLAKE_SCHEMA` | Schema that contains the Application Service |
| `SNOWFLAKE_SERVICE_NAME` | Name of the Application Service |

Expand

Show lessSee more

Together they are the fully qualified name of the service:

Copy code

```
const database = process.env.SNOWFLAKE_DATABASE;
const schema = process.env.SNOWFLAKE_SCHEMA;
const serviceName = process.env.SNOWFLAKE_SERVICE_NAME;
const fqn = `${database}.${schema}.${serviceName}`;
```

## Secret files

Snowflake mounts each secret listed under
[`secrets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-secrets)
in `app.yml` as one or more files under `/secrets/<name>/`, where `<name>` is
the mount name from the manifest. File content updates in place when
Snowflake rotates the secret.

The files written depend on the secret type:

| Secret type | Files under `/secrets/<name>/` |
| --- | --- |
| Generic string | `secret_string` |
| Password | `username`, `password` |
| OAuth2 | `access_token` |

Expand

Show lessSee more

Read a generic string secret:

Copy code

```
import { readFileSync } from "node:fs";
const apiKey = readFileSync("/secrets/API_KEY/secret_string", "utf8").trim();
```

Read a password secret:

Copy code

```
import { readFileSync } from "node:fs";
const username = readFileSync("/secrets/DB_CREDENTIALS/username", "utf8").trim();
const password = readFileSync("/secrets/DB_CREDENTIALS/password", "utf8").trim();
```

Read an OAuth2 access token:

Copy code

```
import { readFileSync } from "node:fs";
const oauthToken = readFileSync("/secrets/OAUTH_TOKEN/access_token", "utf8").trim();
```

Read secrets fresh on each use so a rotation takes effect without a
redeploy. Don’t log secret values or return them in a response.

## Session and caller tokens

Snowflake writes the credentials the app uses to query Snowflake:

- **Session token.** An OAuth token at `/snowflake/session/token`. The
  token rotates, so read it fresh on each request.
- **Caller token.** For caller’s rights queries, Snowflake adds an
  `Sf-Context-Current-User-Token` HTTP header to each incoming request.

How you authenticate caller’s rights queries depends on the compute option:

- **Managed compute.** Combine the two tokens
  (`serviceToken + "." + callerToken`) and authenticate with
  `authenticator: "OAUTH"`.
- **Serverless compute (Public Preview).** The header holds the caller’s complete
  OAuth token. Authenticate with that token alone and
  `authenticator: "OAUTH"`. A joined token fails at login.

Read the session token on managed compute:

Copy code

```
import { readFileSync } from "node:fs";

// Managed compute: join with the caller token for caller's rights queries
const serviceToken = readFileSync("/snowflake/session/token", "utf8").trim();
```

To select the token in an app that runs on either compute option, see
[Caller’s rights](/developer-guide/snowflake-app-runtime/query-snowflake#label-query-snowflake-callers-rights-serverless).

In apps created from the template, `lib/snowflake.ts` reads both tokens for you
through the
[Snowflake App Runtime SDK for Node.js](/developer-guide/snowflake-app-runtime/nodejs-sdk).

## Next steps

- Choose which identity a query runs as and grant it access: [Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).
