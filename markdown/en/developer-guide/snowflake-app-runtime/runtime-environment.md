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

`HOSTNAME` is the bind address. Users reach the app over HTTPS at a
`*.snowflakecomputing.app` URL; the app serves plain HTTP.

## Built-in environment variables

Snowflake sets these at runtime. Read them from `process.env` (or
`os.environ`).

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

Copy code

```
with open("/secrets/API_KEY/secret_string") as f:
    api_key = f.read().strip()
```

Read a password secret:

Copy code

```
import { readFileSync } from "node:fs";
const username = readFileSync("/secrets/DB_CREDENTIALS/username", "utf8").trim();
const password = readFileSync("/secrets/DB_CREDENTIALS/password", "utf8").trim();
```

Copy code

```
with open("/secrets/DB_CREDENTIALS/username") as f:
    username = f.read().strip()
with open("/secrets/DB_CREDENTIALS/password") as f:
    password = f.read().strip()
```

Read an OAuth2 access token:

Copy code

```
import { readFileSync } from "node:fs";
const oauthToken = readFileSync("/secrets/OAUTH_TOKEN/access_token", "utf8").trim();
```

Copy code

```
with open("/secrets/OAUTH_TOKEN/access_token") as f:
    oauth_token = f.read().strip()
```

Read secrets fresh on each use so a rotation takes effect without a
redeploy. Don’t log secret values or return them in a response.

## Session and caller tokens

Snowflake writes the credentials the app uses to query Snowflake:

- **Session token.** An OAuth token at `/snowflake/session/token`. The
  token rotates, so read it fresh on each request.
- **Caller token.** For caller’s rights queries, Snowflake adds an
  `Sf-Context-Current-User-Token` HTTP header to each incoming request.
  Combine the two tokens (`serviceToken + "." + callerToken`) and
  authenticate with `authenticator: "OAUTH"`.

Copy code

```
import { readFileSync } from "node:fs";

const serviceToken = readFileSync("/snowflake/session/token", "utf8").trim();
```

[`lib/snowflake.ts`](/developer-guide/snowflake-app-runtime/query-snowflake)
reads these for you. For which identity a query runs as and how to grant it
access, see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake).
