# Authenticate Cortex Agent SDK requests

— Open

Available to all accounts.

The Cortex Agent SDK authenticates Cortex Agent REST API requests by asking an authenticator for HTTP headers. The SDK
calls the authenticator before every request attempt, including transport retries and auth-refresh replays, so callable
authenticators can pick up rotated credentials without recreating the client.

Keep Programmatic Access Tokens (PATs), private keys, OAuth refresh tokens, client secrets, and Snowflake session
tokens in trusted server-side code. Don’t ship these credentials to browser code.

## Account endpoints

Pass `account` to derive the default API origin:

```
https://<account>.snowflakecomputing.com
```

If the account identifier contains an underscore (`_`), the SDK uses Snowflake’s canonical hyphenated host form for
the derived URL. For example, `myorg_myaccount` derives `https://myorg-myaccount.snowflakecomputing.com`.

Pass `baseUrl` instead of `account` when you need a full regional, PrivateLink, pre-production, or proxy endpoint:

Copy code

```
const client = new CortexAgentClient({
  baseUrl: process.env.SNOWFLAKE_BASE_URL!,
  auth: process.env.SNOWFLAKE_PAT!,
});
```

Set `SNOWFLAKE_BASE_URL` to the trusted Cortex Agent API endpoint for the Snowflake account that owns the credential.

## Header formats

PAT, OAuth, and JWT credentials use the Snowflake token-type header format:

Copy code

```
Authorization: Bearer <token>
X-Snowflake-Authorization-Token-Type: <token-type>
```

Snowflake SQL session tokens use a different header format:

Copy code

```
Authorization: Snowflake Token="<session-token>"
```

Session-token authentication doesn’t send `X-Snowflake-Authorization-Token-Type`.

## Use a Programmatic Access Token

Use a PAT when your trusted server application can store and rotate a Snowflake Programmatic Access Token.

TypeScriptPython

Copy code

```
import { CortexAgentClient, PatAuth } from "@snowflake/cortex-agent-sdk";

const client = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  // `auth: process.env.SNOWFLAKE_PAT!` is equivalent.
  auth: new PatAuth(process.env.SNOWFLAKE_PAT!),
});
```

The SDK sends:

Copy code

```
Authorization: Bearer <pat>
X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN
```

Copy code

```
import os

from cortex_agent_sdk import CortexAgentClient, PatAuth

client = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    # `auth=os.environ["SNOWFLAKE_PAT"]` is equivalent.
    auth=PatAuth(os.environ["SNOWFLAKE_PAT"]),
)
```

The SDK sends:

Copy code

```
Authorization: Bearer <pat>
X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN
```

## Use a key-pair JWT

Use key-pair JWT authentication when a server-to-server application can protect a private key and mint short-lived
JWTs. The application owns signing and renewal. The SDK calls the JWT provider before request attempts and sends the
returned token.

TypeScriptPython

The TypeScript example below mints an RS256 JWT from the private key, Snowflake account identifier, username, and
public-key fingerprint.

Copy code

```
import { createHash, createPrivateKey, createPublicKey, sign } from "node:crypto";
import { CallableAuth, CortexAgentClient } from "@snowflake/cortex-agent-sdk";

const privateKeyPem = process.env.SNOWFLAKE_PRIVATE_KEY_PEM!;
const accountIdentifier = process.env.SNOWFLAKE_JWT_ACCOUNT_IDENTIFIER!.toUpperCase();
const username = process.env.SNOWFLAKE_USER!.toUpperCase();
const qualifiedUser = `${accountIdentifier}.${username}`;

function base64Url(value: string | Buffer): string {
  return Buffer.from(value).toString("base64url");
}

function publicKeyFingerprint(): string {
  const privateKey = createPrivateKey(privateKeyPem);
  const publicKeyDer = createPublicKey(privateKey).export({ type: "spki", format: "der" });
  return `SHA256:${createHash("sha256").update(publicKeyDer).digest("base64")}`;
}

function mintJwt(): string {
  const now = Math.floor(Date.now() / 1_000);
  const header = base64Url(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const payload = base64Url(
    JSON.stringify({
      iss: `${qualifiedUser}.${publicKeyFingerprint()}`,
      sub: qualifiedUser,
      iat: now,
      exp: now + 55 * 60,
    }),
  );
  const signed = `${header}.${payload}`;
  return `${signed}.${sign("RSA-SHA256", Buffer.from(signed), privateKeyPem).toString("base64url")}`;
}

const client = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: new CallableAuth(mintJwt, "KEYPAIR_JWT"),
  // If Snowflake rejects an expired JWT, regenerate it and replay the request.
  refreshAuth: async () => undefined,
});
```

The Python SDK doesn’t sign the JWT for you. Pass a callable that returns a currently valid signed JWT, for example
from your own signer or from Snowflake connector key-pair authentication code.

Copy code

```
import os

from cortex_agent_sdk import CortexAgentClient, KeyPairJwtAuth

def mint_jwt() -> str:
    # Sign a short-lived JWT with your protected private key.
    return os.environ["SNOWFLAKE_KEYPAIR_JWT"]

client = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=KeyPairJwtAuth(mint_jwt),
    refresh_auth=lambda _context: None,
)
```

The SDK sends:

Copy code

```
Authorization: Bearer <jwt>
X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT
```

## Use OAuth

Use OAuth when your service receives Snowflake OAuth or External OAuth access tokens and can refresh them on the
server. Store the OAuth client secret and refresh token in an encrypted server-side secret store.

TypeScriptPython

Copy code

```
import { CortexAgentClient, OAuthAuth } from "@snowflake/cortex-agent-sdk";

interface OAuthTokens {
  access_token: string;
  refresh_token?: string;
  expiresAt: number;
}

const tokenEndpoint = process.env.SNOWFLAKE_OAUTH_TOKEN_ENDPOINT!;
const clientId = process.env.SNOWFLAKE_OAUTH_CLIENT_ID!;
const clientSecret = process.env.SNOWFLAKE_OAUTH_CLIENT_SECRET!;
let accessToken: string | undefined = process.env.SNOWFLAKE_OAUTH_ACCESS_TOKEN;
let refreshToken: string | undefined = process.env.SNOWFLAKE_OAUTH_REFRESH_TOKEN;
let expiresAt = Number(process.env.SNOWFLAKE_OAUTH_EXPIRES_AT ?? 0);

async function exchangeRefreshToken(currentRefreshToken: string): Promise<OAuthTokens> {
  const response = await fetch(tokenEndpoint, {
    method: "POST",
    headers: {
      Authorization: `Basic ${Buffer.from(`${clientId}:${clientSecret}`).toString("base64")}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ grant_type: "refresh_token", refresh_token: currentRefreshToken }),
  });
  if (!response.ok) throw new Error(`OAuth refresh failed: ${await response.text()}`);
  const payload = (await response.json()) as {
    access_token: string;
    refresh_token?: string;
    expires_in: number;
  };
  return {
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
    expiresAt: Date.now() + payload.expires_in * 1_000,
  };
}

async function forceRefresh(): Promise<void> {
  if (!refreshToken) throw new Error("No OAuth refresh token is available.");
  const tokens = await exchangeRefreshToken(refreshToken);
  accessToken = tokens.access_token;
  if (tokens.refresh_token) refreshToken = tokens.refresh_token;
  expiresAt = tokens.expiresAt;
}

async function getValidAccessToken(): Promise<string> {
  if (!accessToken || Date.now() >= expiresAt - 2 * 60_000) await forceRefresh();
  if (!accessToken) throw new Error("OAuth refresh did not return an access token.");
  return accessToken;
}

const client = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: new OAuthAuth(getValidAccessToken),
  refreshAuth: forceRefresh,
});
```

Copy code

```
import base64
import json
import os
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from cortex_agent_sdk import CortexAgentClient, OAuthAuth

token_endpoint = os.environ["SNOWFLAKE_OAUTH_TOKEN_ENDPOINT"]
client_id = os.environ["SNOWFLAKE_OAUTH_CLIENT_ID"]
client_secret = os.environ["SNOWFLAKE_OAUTH_CLIENT_SECRET"]
access_token: str | None = os.environ.get("SNOWFLAKE_OAUTH_ACCESS_TOKEN")
refresh_token: str | None = os.environ.get("SNOWFLAKE_OAUTH_REFRESH_TOKEN")
expires_at = float(os.environ.get("SNOWFLAKE_OAUTH_EXPIRES_AT", "0"))

def refresh_access_token() -> None:
    global access_token, refresh_token, expires_at
    if refresh_token is None:
        raise RuntimeError("No OAuth refresh token is available.")

    basic_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    request = Request(
        token_endpoint,
        data=urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token}).encode(),
        headers={
            "Authorization": f"Basic {basic_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urlopen(request) as response:
        payload = json.load(response)
    access_token = payload["access_token"]
    refresh_token = payload.get("refresh_token", refresh_token)
    expires_at = time.time() + payload["expires_in"]

def get_valid_access_token() -> str:
    if access_token is None or time.time() >= expires_at - 120:
        refresh_access_token()
    assert access_token is not None
    return access_token

client = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=OAuthAuth(get_valid_access_token),
    refresh_auth=lambda _context: refresh_access_token(),
)
```

The SDK sends:

Copy code

```
Authorization: Bearer <oauth-access-token>
X-Snowflake-Authorization-Token-Type: OAUTH
```

## Use a Snowflake session token

Use a Snowflake session token when your application already has an authenticated Snowflake SQL driver session and
wants Cortex Agent API requests to run with that session.

TypeScriptPython

The Node.js `snowflake-sdk` driver doesn’t currently expose stable public methods to read both the current session
token and resolved access URL from a connection. The example below uses the driver’s serialized connection state to
extract the session token. This works with the current driver shape, but if this integration breaks, use PAT, OAuth, or
key-pair JWT authentication instead.

Copy code

```
import snowflake, { type Connection, type ConnectionOptions } from "snowflake-sdk";
import { CortexAgentClient, SnowflakeSessionTokenAuth } from "@snowflake/cortex-agent-sdk";

const options: ConnectionOptions = {
  account: process.env.SNOWFLAKE_ACCOUNT!,
  username: process.env.SNOWFLAKE_USER!,
  password: process.env.SNOWFLAKE_PASSWORD!,
};

async function connect(): Promise<Connection> {
  const connection = snowflake.createConnection(options);
  await connection.connectAsync();
  return connection;
}

let connection = await connect();

function sessionToken(): string {
  const serialized = JSON.parse(connection.serialize()) as {
    services?: { sf?: { tokenInfo?: { sessionToken?: unknown } } };
  };
  const token = serialized.services?.sf?.tokenInfo?.sessionToken;
  if (typeof token !== "string") throw new Error("The Snowflake connection did not yield a session token.");
  return token;
}

const client = new CortexAgentClient({
  ...(process.env.SNOWFLAKE_BASE_URL ? { baseUrl: process.env.SNOWFLAKE_BASE_URL } : { account: options.account! }),
  auth: new SnowflakeSessionTokenAuth(sessionToken),
  refreshAuth: async () => {
    const previous = connection;
    connection = await connect();
    previous.destroy(() => undefined);
  },
});
```

Copy code

```
import os

import snowflake.connector
from cortex_agent_sdk import CortexAgentClient, SnowflakeSessionTokenAuth

connection = snowflake.connector.connect(
    connection_name=os.getenv("CORTEX_EXAMPLE_CONNECTION", "my_connection")
)
api_host = connection.host.replace("_", "-")

def session_token() -> str:
    rest = connection.rest
    if rest is None or not isinstance(rest.token, str):
        raise RuntimeError("The Snowflake connection did not yield a session token.")
    return rest.token

client = CortexAgentClient(
    base_url=f"https://{api_host}",
    auth=SnowflakeSessionTokenAuth(session_token),
)
```

The SDK sends:

Copy code

```
Authorization: Snowflake Token="<session-token>"
```

## Use a custom authenticator

Use a custom authenticator when your application has its own credential store or needs to generate headers directly.

TypeScriptPython

Copy code

```
import { CortexAgentClient, type Authenticator } from "@snowflake/cortex-agent-sdk";

async function readPatFromSecretStore(): Promise<string> {
  // Replace with a secret-manager lookup.
  return process.env.SNOWFLAKE_PAT!;
}

class SecretStorePatAuth implements Authenticator {
  async getAuthHeaders(): Promise<Record<string, string>> {
    const token = await readPatFromSecretStore();
    return {
      Authorization: `Bearer ${token}`,
      "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
    };
  }
}

const client = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: new SecretStorePatAuth(),
});
```

Copy code

```
import os

from cortex_agent_sdk import CortexAgentClient

class SecretStorePatAuth:
    def get_auth_headers(self) -> dict[str, str]:
        token = os.environ["SNOWFLAKE_PAT"]
        return {
            "Authorization": f"Bearer {token}",
            "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
        }

client = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=SecretStorePatAuth(),
)
```

## Refresh expired credentials

Pass `refreshAuth` in TypeScript or `refresh_auth` in Python when the credential source needs an explicit refresh
signal after Snowflake returns an expired-token or expired-session response.

When the SDK detects an expired credential response:

1. It calls the refresh callback with request context, including the HTTP method, path, request ID when present, and
   refresh attempt number.
2. If the callback succeeds, the SDK asks the authenticator for headers again and immediately replays the same
   request.
3. By default, the SDK performs one auth refresh and one replay per request.

If the refresh callback fails, the SDK raises the original typed API error, such as `AuthenticationError`, and attaches
safe refresh diagnostics. The error metadata doesn’t include authorization headers or token values.

TypeScriptPython

Copy code

```
import { AuthenticationError } from "@snowflake/cortex-agent-sdk";

try {
  await conversation.send("Analyze Q1 revenue.");
} catch (error) {
  if (error instanceof AuthenticationError) {
    console.error(error.authRefresh?.provider);
    console.error(error.authRefresh?.attempt);
    console.error(error.authRefresh?.requestId);
    console.error(error.cause);
  }
}
```

Copy code

```
from cortex_agent_sdk import AuthenticationError

try:
    conversation.send("Analyze Q1 revenue.")
except AuthenticationError as error:
    print(error.auth_refresh.provider if error.auth_refresh else None)
    print(error.auth_refresh.attempt if error.auth_refresh else None)
    print(error.auth_refresh.request_id if error.auth_refresh else None)
    print(error.__cause__)
```

## Next steps

- [Conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations): Maintain conversation state across turns
- [Direct Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents): Use low-level run, thread, and agent-object resources
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): Review response objects, errors, retries, and request options

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
