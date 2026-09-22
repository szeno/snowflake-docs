# Embed a Streamlit in Snowflake app for viewers with a Snowflake account

This tutorial embeds a Streamlit in Snowflake app in an external page for viewers who are already provisioned in
Snowflake, typically through an external identity provider (IdP) such as Okta. The app runs as the
viewer rather than as a shared service user, so each viewer sees only the data their own privileges
allow.

If your viewers don’t have Snowflake accounts, follow
[Embed a Streamlit in Snowflake app for viewers without a Snowflake account](/developer-guide/streamlit/features/embedding/external-users) instead. For background on the two
models, see [Embedding Streamlit in Snowflake apps in external pages](/developer-guide/streamlit/features/embedding/overview).

The examples assume the app needs to query a schema the app owner’s role can’t reach directly,
`mydb.finance`, accessible only to the `finance` role, which is held by the viewers who should see that
data.

## Before you begin

- You need an existing Streamlit in Snowflake app on a container runtime. If you don’t have one, see
  [Getting started with Streamlit in Snowflake](/developer-guide/streamlit/getting-started/overview). To check or change an app’s runtime, see
  [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).
- You need the ACCOUNTADMIN role, or another role with the ALTER ACCOUNT privilege, to register
  allowed embedding domains.
- Your web server must be able to make outbound HTTPS calls to Snowflake.
- Your page must be served over HTTPS from the same origin you register. For local development, an
  `http://localhost` origin is also allowed.

This model has two additional prerequisites:

- Your IdP must be configured as a Snowflake External OAuth integration, so that Snowflake accepts
  tokens it issues. For setup instructions, see [External OAuth overview](/user-guide/oauth-ext-overview).
- Your backend must be able to obtain a valid OAuth access token for each viewer. See
  [Step 5: Decide how your backend gets each viewer’s token](#label-sis-embed-callers-token-flow).
- Your app must run on a container runtime, which is required for restricted caller’s rights. See
  [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

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

## Step 2: Grant privileges to your viewers’ roles

With this model the embed URL is minted under the *viewer’s* role, not a service role. That means each
role your viewers use needs both privileges on the app:

Copy code

```
GRANT USAGE ON DATABASE  mydb               TO ROLE finance;
GRANT USAGE ON SCHEMA    mydb.public        TO ROLE finance;
GRANT USAGE ON STREAMLIT mydb.public.my_app TO ROLE finance;
GRANT EMBED ON STREAMLIT mydb.public.my_app TO ROLE finance;
```

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

A viewer whose role has USAGE but not EMBED can open the app in Snowsight but can’t be served
it through your embedded page. That’s the useful distinction: EMBED controls who may be shown the app
in an external page, separately from who may view it in Snowflake.

## Step 3: Set up caller grants

For the app to query data on the viewer’s behalf, an ACCOUNTADMIN, or a role with the MANAGE CALLER
GRANTS privilege, must authorize the app owner’s role to pass caller privileges through to the target
schema. The following example uses the
[high-level caller privilege](/developer-guide/restricted-callers-rights/high-level-caller-privileges)
DATA READ:

Copy code

```
-- Run as ACCOUNTADMIN, or the owner of mydb.finance
GRANT CALLER DATA READ ON SCHEMA mydb.finance TO ROLE <app_owner_role>;
```

This doesn’t give the app owner read access to `mydb.finance`. It only authorizes the app owner’s role
to delegate the viewer’s own `finance` privileges through the app. Viewers who hold `finance` see the
data; viewers who don’t are denied.

For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

## Step 4: Use a caller’s rights connection in your app

In your app code, use the named connection for restricted caller’s rights:

Copy code

```
conn = st.connection("snowflake-callers-rights")
```

Queries run through this connection execute as the viewer, so row access policies and privilege checks
reflect the viewer’s grants rather than the app owner’s.

## Step 5: Decide how your backend gets each viewer’s token

Unlike the service-user model, there’s no single stored credential here. Your backend authenticates to
Snowflake as the viewer, using an OAuth access token that your IdP issued for that viewer. Where that
token comes from is your application’s decision, and there are two common patterns.

**Server-side token (recommended).** Your backend already authenticated the viewer, so it holds their
tokens in a server-side session store. The token never enters the browser, and your minting route
looks it up from the session:

Copy code

```
// Preferred: the token is looked up server-side from the viewer's session.
const session = await getSession(request); // your existing auth layer
const embedUrl = await mintEmbedUrl(session.snowflakeAccessToken, session.snowflakeRole);
```

**Token forwarded from the browser.** If your frontend obtains the token directly from the IdP, for
example with an IdP SDK that performs the authorization code flow in the browser, it forwards that
token to your backend on each request:

Copy code

```
// Frontend: attach the viewer's IdP access token to the mint request.
const token = await idp.getAccessToken(); // e.g. an MSAL or Okta SDK call
const res = await fetch("/api/embed-url", {
  cache: "no-store",
  headers: { Authorization: `Bearer ${token}` },
});
const { embedUrl } = await res.json();
```

Your backend then reads that header, which is the `oauthToken` the next step consumes.

Note

Prefer the server-side pattern where you can. A token in the browser is exposed to anything running on
the page, and it authenticates as the viewer against Snowflake, not just against your application.

Whichever pattern you use, each mint request carries a different viewer’s token, so there’s nothing to
pool or reuse between viewers.

## Step 6: Mint the embed URL per viewer

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

For this model, send `OAUTH` as the token type, and set `X-Snowflake-Role` to the role that viewer
should be served the app under:

```
SNOWFLAKE_ACCOUNT_URL=https://myorg-myacct.snowflakecomputing.com
STREAMLIT_APP=mydb.public.my_app
PARENT_ORIGIN=https://portal.example.com
```

Copy code

```
// app/api/embed-url/route.ts
import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic"; // never cache the single-use embed URL

async function mintEmbedUrl(oauthToken: string, role: string): Promise<string> {
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
        // The viewer's OAuth access token from Step 5.
        Authorization: `Bearer ${oauthToken}`,
        "X-Snowflake-Authorization-Token-Type": "OAUTH",
        // The viewer's role. It needs USAGE and EMBED on the app.
        "X-Snowflake-Role": role,
      },
      body: JSON.stringify({ parent_origin: process.env.PARENT_ORIGIN }),
    },
  );
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return (await res.json()).embed_url;
}

export async function GET(request: Request) {
  // Server-side pattern: read the viewer's token and role from their session.
  // If you forward the token from the browser instead, read it from the
  // Authorization header here and reject the request when it's absent.
  const session = await getSession(request);
  if (!session) {
    return NextResponse.json({ error: "Not signed in" }, { status: 401 });
  }
  try {
    return NextResponse.json({
      embedUrl: await mintEmbedUrl(
        session.snowflakeAccessToken,
        session.snowflakeRole,
      ),
    });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}
```

Important

Decide the role on your backend, from the viewer’s authenticated session. If you let the browser choose
the value of `X-Snowflake-Role`, a viewer can ask to be served the app under any role granted to them,
which may not be the one you intended for the embedded view.

Note

Because your backend makes the mint request, that request is attributed to your backend’s IP address
rather than the viewer’s, so per-user [network policies](/user-guide/network-policies) don’t apply to
the mint step. The viewer’s own session with the app is still subject to policy. If your backend has a
static egress IP, allow-list it. For details, see
[Network policies](/developer-guide/streamlit/features/embedding/overview#label-sis-embed-network-policies).

## Step 7: Render the app in an iframe

If you forward the viewer’s token from the browser, add the `Authorization` header shown in
[Step 5: Decide how your backend gets each viewer’s token](#label-sis-embed-callers-token-flow) to the `fetch` calls below. With the server-side pattern, the
frontend calls `/api/embed-url` with no extra headers, exactly as shown.

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
- [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights): How caller grants scope what an
  app can do on a viewer’s behalf.
- [Row access policies in Streamlit in Snowflake](/developer-guide/streamlit/features/row-access): Filter rows per viewer with row access policies.
- [Security considerations](/developer-guide/streamlit/features/embedding/overview#label-sis-embed-security): What the
  embedding domain list does and doesn’t protect against.
