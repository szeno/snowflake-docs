# Embed a Streamlit in Snowflake app for viewers without a Snowflake account

This tutorial embeds a Streamlit in Snowflake app in an external page for viewers who don’t sign in to Snowflake, such
as a customer-facing dashboard on a public portal or a status page. The app runs as a service user you
create, so every viewer sees the same data.

If each viewer should instead see data scoped to their own Snowflake privileges, follow
[Embed a Streamlit in Snowflake app for viewers with a Snowflake account](/developer-guide/streamlit/features/embedding/snowflake-users) instead. For background on the two
models, see [Embedding Streamlit in Snowflake apps in external pages](/developer-guide/streamlit/features/embedding/overview).

## Before you begin

- You need an existing Streamlit in Snowflake app on a container runtime. If you don’t have one, see
  [Getting started with Streamlit in Snowflake](/developer-guide/streamlit/getting-started/overview). To check or change an app’s runtime, see
  [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).
- You need the ACCOUNTADMIN role, or another role with the ALTER ACCOUNT privilege, to register
  allowed embedding domains.
- Your web server must be able to make outbound HTTPS calls to Snowflake.
- Your page must be served over HTTPS from the same origin you register. For local development, an
  `http://localhost` origin is also allowed.

## Step 1: Register allowed embedding domains

Register the external domains where embedded apps are allowed to load by setting the
`STREAMLIT_EMBEDDING_CONTROLS` account parameter. Embedding only works for the domains you register
here. Run the following as ACCOUNTADMIN:

Copy code

```
ALTER ACCOUNT SET STREAMLIT_EMBEDDING_CONTROLS = $$
allowed_embedding_domains:
  - https://portal.example.com
  - https://analytics.example.com
$$;
```

Each entry must be an absolute HTTPS origin: `https://host` or `https://host:port`. Wildcards, paths,
and query strings aren’t supported. Matching ignores scheme and host case, default ports, and trailing
slashes.

For local development, you can also register a `localhost` origin over `http`, for example
`http://localhost:3000`. All other hosts must use `https`.

Snowflake validates the document when you set the parameter, so malformed YAML, an unrecognized
top-level key, or an invalid origin is rejected before the value is saved.

## Step 2: Create the service user and grant privileges

Your backend needs a Snowflake identity to mint embed URLs with. Use a `TYPE = SERVICE` user with a
narrow, dedicated role, because it only needs to reach the one app you’re embedding.

Copy code

```
-- Run as ACCOUNTADMIN, or a role that can manage users and grants

-- Service user for URL minting only
CREATE USER IF NOT EXISTS embed_svc TYPE = SERVICE;

-- Dedicated role
CREATE ROLE IF NOT EXISTS embed_minter;
GRANT ROLE embed_minter TO USER embed_svc;
ALTER USER embed_svc SET DEFAULT_ROLE = embed_minter;

-- USAGE to resolve the app, EMBED to mint a URL for it
GRANT USAGE ON DATABASE  mydb               TO ROLE embed_minter;
GRANT USAGE ON SCHEMA    mydb.public        TO ROLE embed_minter;
GRANT USAGE ON STREAMLIT mydb.public.my_app TO ROLE embed_minter;
GRANT EMBED ON STREAMLIT mydb.public.my_app TO ROLE embed_minter;
```

The service user doesn’t need a warehouse. Minting an embed URL doesn’t open a SQL session.

The role that mints the embed URL needs two privileges on the app:

- USAGE, to resolve the app. A role without it gets the same response as if the app didn’t exist.
- EMBED, to mint an embed URL for it.

Important

Owning the app doesn’t imply EMBED. The app owner must be granted EMBED explicitly, the same as any
other role.

Because EMBED is granted separately from USAGE, you can share an app with a role for viewing in
Snowsight without also letting that role publish it to an external page. To stop a role from
minting embed URLs while leaving its ability to view the app intact, revoke EMBED on its own:

Copy code

```
REVOKE EMBED ON STREAMLIT mydb.public.my_app FROM ROLE <role_name>;
```

For more information, see [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).

Important

Every viewer of the embedded app shares this role’s access. Grant it USAGE and EMBED on the one app you
intend to embed, and nothing else, because the viewer session inherits the role the URL was minted
under.

## Step 3: Configure credentials

Choose the credential type that fits where your backend runs, then finish configuring the `embed_svc`
user you created in Step 2.

PATKey-pair JWTWIF

A programmatic access token is the simplest option. The service user needs a network policy before you
can add one.

1. Create a network policy that restricts connections to your backend’s egress IP range:

Copy code

```
CREATE NETWORK POLICY IF NOT EXISTS embed_svc_np
  ALLOWED_IP_LIST = ('203.0.113.0/24');  -- replace with your backend's IPs

ALTER USER embed_svc SET NETWORK_POLICY = embed_svc_np;
```

2. Generate the token. The secret is shown exactly once, so copy it before you close the results:

Copy code

```
ALTER USER embed_svc ADD PROGRAMMATIC ACCESS TOKEN embed_pat
  ROLE_RESTRICTION = 'EMBED_MINTER'
  DAYS_TO_EXPIRY   = 90
  COMMENT          = 'Embed URL minting';
-- Returns: token_name | token_secret
```

3. Store `token_secret` in your backend’s secret store. Never commit it to source control.

For more information, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

Key-pair authentication avoids a shared secret and supports key rotation.

1. Generate an encrypted RSA key pair:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 aes-256-cbc -inform PEM -out rsa_key.p8
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

2. Register the public key on the service user:

Copy code

```
ALTER USER embed_svc SET RSA_PUBLIC_KEY = 'MIIBIjANBgkqhki...';
```

3. Verify the fingerprint:

Copy code

```
DESC USER embed_svc;
-- RSA_PUBLIC_KEY_FP should be set in the output
```

Store the private key file securely on your backend. Your backend signs a short-lived JWT with it on
each mint. For more information, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

Workload identity federation lets a workload authenticate using its cloud provider’s native identity,
such as an AWS IAM role, a Microsoft Entra ID identity, a GCP service account, or any OIDC issuer, so
there’s no long-lived secret to store.

1. As a workload administrator, configure your service so its provider can issue an attestation of the
   workload’s identity.
2. As a Snowflake administrator, map that identity onto the `embed_svc` user you already created. For
   example, with an OIDC issuer:

Copy code

```
ALTER USER embed_svc SET
  WORKLOAD_IDENTITY = (
    TYPE   = OIDC
    ISSUER = 'https://your-idp.example.com'
    SUBJECT = 'your-workload-subject'
  );
```

Because WIF authenticates with a live federated token, your backend must run in the environment that
issues it. For more information, see [Workload identity federation](/user-guide/workload-identity-federation).

## Step 4: Mint the embed URL from your backend

Your backend mints an embed URL by calling the following endpoint. No SQL session and no Snowflake
driver are required.

```
POST /api/v2/databases/{database}/schemas/{schema}/streamlits/{name}:generate-embed-url
```

Send the following headers:

| Header | Value |
| --- | --- |
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer <token>`, where the token depends on your credential type |
| `X-Snowflake-Authorization-Token-Type` | The credential type, such as `PROGRAMMATIC_ACCESS_TOKEN`, `KEYPAIR_JWT`, `OAUTH`, or `WORKLOAD_IDENTITY_FEDERATION` |
| `X-Snowflake-Role` | The role to resolve and mint the app under |

Expand

Show lessSee more

`X-Snowflake-Role` is required. The endpoint doesn’t fall back to the user’s default role or to
PUBLIC, and a request without it fails with `400`. The role you name must be granted to the
authenticating user and must hold USAGE and EMBED on the app.

The request body names the origin that will host the iframe:

Copy code

```
{ "parent_origin": "https://portal.example.com" }
```

The origin must be registered in `allowed_embedding_domains` and must be the exact origin the browser
loads your page from. The response is the embed URL:

Copy code

```
{ "embed_url": "https://…" }
```

Important

Treat the embed URL as a bearer credential. It grants a viewer session for the app with the
privileges of the role it was minted under. The authorization code it carries is valid for 10 minutes,
is single-use, and is invalidated the first time it’s redeemed. Don’t log, cache, or persist it. Mint
a fresh URL for each embed session, and never expose your minting endpoint publicly or without
authentication.

Each credential type is the same request with a different `Authorization` header:

| Credential | `Authorization` | `X-Snowflake-Authorization-Token-Type` |
| --- | --- | --- |
| PAT | `Bearer <token_secret>` | `PROGRAMMATIC_ACCESS_TOKEN` |
| Key-pair JWT | `Bearer <RS256 JWT>` | `KEYPAIR_JWT` |
| WIF | `Bearer WIF.<AWS|AZURE|GCP|OIDC>.<token>` | `WORKLOAD_IDENTITY_FEDERATION` |

Expand

Show lessSee more

The following examples use a Next.js route handler. Any server-side language works, because the
endpoint takes a plain HTTPS POST.

PATKey-pair JWTWIF

Set environment variables in `.env.local`. Never commit this file, and store these values in a secret
store when you deploy:

```
SNOWFLAKE_ACCOUNT_URL=https://myorg-myacct.snowflakecomputing.com
SNOWFLAKE_PAT=<token_secret from Step 3>
SNOWFLAKE_ROLE=embed_minter
STREAMLIT_APP=mydb.public.my_app
PARENT_ORIGIN=https://portal.example.com
```

Copy code

```
// app/api/embed-url/route.ts
import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic"; // never cache the single-use embed URL

export async function GET() {
  try {
    return NextResponse.json({
      embedUrl: await mintEmbedUrl({
        Authorization: `Bearer ${process.env.SNOWFLAKE_PAT}`,
        "X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN",
      }),
    });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}

async function mintEmbedUrl(auth: Record<string, string>): Promise<string> {
  const [db, schema, name] = process.env
    .STREAMLIT_APP!.split(".")
    .map(encodeURIComponent);
  const res = await fetch(
    `${process.env.SNOWFLAKE_ACCOUNT_URL}/api/v2/databases/${db}/schemas/${schema}` +
      `/streamlits/${name}:generate-embed-url`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Required: the app is resolved under this role. No default-role fallback.
        "X-Snowflake-Role": process.env.SNOWFLAKE_ROLE!,
        ...auth,
      },
      body: JSON.stringify({ parent_origin: process.env.PARENT_ORIGIN }),
    },
  );
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return (await res.json()).embed_url;
}
```

Set environment variables in `.env.local`. Never commit this file or your private key:

```
SNOWFLAKE_ACCOUNT_URL=https://myorg-myacct.snowflakecomputing.com
SNOWFLAKE_ACCOUNT=MYORG-MYACCT
SNOWFLAKE_USER=embed_svc
SNOWFLAKE_PRIVATE_KEY_PATH=/absolute/path/to/rsa_key.p8
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=<passphrase>
SNOWFLAKE_ROLE=embed_minter
STREAMLIT_APP=mydb.public.my_app
PARENT_ORIGIN=https://portal.example.com
```

Copy code

```
// app/api/embed-url/route.ts
import { NextResponse } from "next/server";
import crypto from "node:crypto";
import fs from "node:fs";

export const runtime = "nodejs";
export const dynamic = "force-dynamic"; // never cache the single-use embed URL

export async function GET() {
  try {
    return NextResponse.json({
      embedUrl: await mintEmbedUrl({
        Authorization: `Bearer ${keypairJwt()}`,
        "X-Snowflake-Authorization-Token-Type": "KEYPAIR_JWT",
      }),
    });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}

/** RS256 JWT: iss = ACCOUNT.USER.SHA256:<public key fingerprint>, sub = ACCOUNT.USER. */
function keypairJwt(): string {
  const passphrase = process.env.SNOWFLAKE_PRIVATE_KEY_PASSPHRASE;
  const key = crypto.createPrivateKey({
    key: fs.readFileSync(process.env.SNOWFLAKE_PRIVATE_KEY_PATH!),
    ...(passphrase && { passphrase }),
  });
  const fingerprint = crypto
    .createHash("sha256")
    .update(crypto.createPublicKey(key).export({ type: "spki", format: "der" }))
    .digest("base64");

  // Account and user must be uppercase; periods in the account are invalid in a JWT.
  const account = process.env.SNOWFLAKE_ACCOUNT!.toUpperCase().replace(/\./g, "-");
  const qualifiedUser = `${account}.${process.env.SNOWFLAKE_USER!.toUpperCase()}`;
  const now = Math.floor(Date.now() / 1000);

  const b64 = (o: object) => Buffer.from(JSON.stringify(o)).toString("base64url");
  const body = `${b64({ alg: "RS256", typ: "JWT" })}.${b64({
    iss: `${qualifiedUser}.SHA256:${fingerprint}`,
    sub: qualifiedUser,
    iat: now,
    exp: now + 3540, // maximum lifetime is one hour
  })}`;
  return `${body}.${crypto.sign("RSA-SHA256", Buffer.from(body), key).toString("base64url")}`;
}

async function mintEmbedUrl(auth: Record<string, string>): Promise<string> {
  const [db, schema, name] = process.env
    .STREAMLIT_APP!.split(".")
    .map(encodeURIComponent);
  const res = await fetch(
    `${process.env.SNOWFLAKE_ACCOUNT_URL}/api/v2/databases/${db}/schemas/${schema}` +
      `/streamlits/${name}:generate-embed-url`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Snowflake-Role": process.env.SNOWFLAKE_ROLE!,
        ...auth,
      },
      body: JSON.stringify({ parent_origin: process.env.PARENT_ORIGIN }),
    },
  );
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return (await res.json()).embed_url;
}
```

With WIF the identity is carried in the token, so there’s no user name to configure:

```
SNOWFLAKE_ACCOUNT_URL=https://myorg-myacct.snowflakecomputing.com
SNOWFLAKE_WIF_TOKEN=<OIDC JWT from your provider>
SNOWFLAKE_ROLE=embed_minter
STREAMLIT_APP=mydb.public.my_app
PARENT_ORIGIN=https://portal.example.com
```

Copy code

```
// app/api/embed-url/route.ts
import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic"; // never cache the single-use embed URL

export async function GET() {
  try {
    return NextResponse.json({
      embedUrl: await mintEmbedUrl({
        // WIF.{AWS|AZURE|GCP|OIDC}.{token}: identity comes from the token, not a user name
        Authorization: `Bearer WIF.OIDC.${process.env.SNOWFLAKE_WIF_TOKEN}`,
        "X-Snowflake-Authorization-Token-Type": "WORKLOAD_IDENTITY_FEDERATION",
      }),
    });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}

async function mintEmbedUrl(auth: Record<string, string>): Promise<string> {
  const [db, schema, name] = process.env
    .STREAMLIT_APP!.split(".")
    .map(encodeURIComponent);
  const res = await fetch(
    `${process.env.SNOWFLAKE_ACCOUNT_URL}/api/v2/databases/${db}/schemas/${schema}` +
      `/streamlits/${name}:generate-embed-url`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Snowflake-Role": process.env.SNOWFLAKE_ROLE!,
        ...auth,
      },
      body: JSON.stringify({ parent_origin: process.env.PARENT_ORIGIN }),
    },
  );
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return (await res.json()).embed_url;
}
```

## Step 5: Render the app in an iframe

Pass the embed URL from your backend to the `src` attribute of an `<iframe>`.

Plain HTMLReact

Copy code

```
<p id="msg">Loading…</p>

<script>
  fetch("/api/embed-url", { cache: "no-store" })
    .then((r) => r.json())
    .then((d) => {
      if (!d.embedUrl) throw new Error(d.error);
      const frame = document.createElement("iframe");
      frame.src = d.embedUrl;
      frame.title = "My Streamlit app";
      frame.allow = "clipboard-read; clipboard-write; fullscreen";
      frame.style = "width:100%; height:800px; border:none;";
      document.body.replaceChildren(frame);
    })
    .catch((e) => {
      document.getElementById("msg").textContent = "Error: " + e.message;
    });
</script>
```

Copy code

```
// app/page.tsx
"use client";
import { useEffect, useRef, useState } from "react";

export default function EmbeddedApp() {
  const [embedUrl, setEmbedUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const requested = useRef(false);

  useEffect(() => {
    if (requested.current) return; // the embed URL is single-use, so mint once
    requested.current = true;
    fetch("/api/embed-url", { cache: "no-store" })
      .then((r) => r.json())
      .then((d) => (d.embedUrl ? setEmbedUrl(d.embedUrl) : setError(d.error)))
      .catch(() => setError("Could not load the app."));
  }, []);

  if (error) return <p>{error}</p>;
  if (!embedUrl) return <p>Loading…</p>;

  return (
    <iframe
      src={embedUrl}
      title="My Streamlit app"
      allow="clipboard-read; clipboard-write; fullscreen"
      style={{ width: "100%", height: "100vh", border: "none" }}
    />
  );
}
```

Keep the following in mind:

- The page must be served from the exact origin you passed as `parent_origin` when you minted the URL.
  A non-matching origin is rejected when the app renders, even though the URL minted successfully.
- Mint the URL once per embed session. Fetching it with `cache: "no-store"`, and guarding against a
  second fetch, keeps a component that mounts twice from spending the single-use code.
- If your app uses a download button such as `st.download_button`, and you set the `sandbox`
  attribute on the iframe, include `allow-downloads`. Otherwise the browser blocks the download.
- If your app uses a widget that captures audio or video, such as `st.audio_input` or
  `st.camera_input`, and you set the `sandbox` attribute, include `allow-popups`. Otherwise the
  browser blocks the prompt that asks for microphone or camera access.

### Listen for lifecycle events

The embedded app sends `postMessage` events to the parent window, so your page can tell the difference
between an app that is still starting and one that failed.

| Event | When it fires |
| --- | --- |
| `SNOWFLAKE_EMBED_LOADED` | The app is fully rendered and interactive. |
| `SNOWFLAKE_EMBED_ERROR` | The app failed to load. |
| `SNOWFLAKE_EMBED_SUSPENDED` | The app was suspended due to inactivity. |
| `SNOWFLAKE_EMBED_SESSION_EXPIRED` | The embed session expired and can no longer be refreshed. |

Expand

Show lessSee more

Each message has a `type` field, a `timestamp` in Unix milliseconds, and an optional `appId` that
identifies which app sent the event when you embed more than one app on a page.

Copy code

```
window.addEventListener("message", (event) => {
  // Only accept messages from the Snowflake app origin
  if (!event.origin.endsWith(".snowflake.app")) return;

  switch (event.data?.type) {
    case "SNOWFLAKE_EMBED_LOADED":
      console.log("App is ready", event.data.appId);
      break;
    case "SNOWFLAKE_EMBED_ERROR":
      console.error("App failed to load", event.data.appId);
      break;
    case "SNOWFLAKE_EMBED_SUSPENDED":
      console.warn("App suspended", event.data.appId);
      break;
    case "SNOWFLAKE_EMBED_SESSION_EXPIRED":
      console.warn("Session expired. Reload the page to get a fresh embed URL.");
      break;
  }
});
```

## What’s next?

- [Troubleshoot embedded Streamlit in Snowflake apps](/developer-guide/streamlit/features/embedding/troubleshooting): Diagnose mint failures, blank
  iframes, and apps that load for some viewers but not others.
- [Security considerations](/developer-guide/streamlit/features/embedding/overview#label-sis-embed-security): What the
  embedding domain list does and doesn’t protect against before you expose sensitive data.
- [Embed a Streamlit in Snowflake app for viewers with a Snowflake account](/developer-guide/streamlit/features/embedding/snowflake-users): Scope each viewer’s data to their
  own Snowflake privileges instead.
- [Embedding samples](https://github.com/Snowflake-Labs/snowflake-demo-streamlit/tree/main/Embedding%20Streamlit%20in%20Snowflake): Runnable backends for each
  credential type, including a zero-dependency Node example.
