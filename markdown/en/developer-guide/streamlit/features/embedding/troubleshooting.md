# Troubleshoot embedded Streamlit in Snowflake apps

This page covers problems specific to embedding a Streamlit in Snowflake app in an external page. For problems with the
app itself, see [Troubleshooting Streamlit in Snowflake](/developer-guide/streamlit/troubleshooting).

Embedding fails in one of two places, and knowing which one narrows the cause considerably:

- **The mint request** is the call your backend makes to Snowflake. It fails with an HTTP status you
  can read directly from your backend logs. See [The mint request fails](#label-sis-embed-ts-mint).
- **The render** is the browser loading the embed URL in an iframe. The mint succeeded, so there’s no
  HTTP error to read; the symptom is a blank frame or a console error. See
  [The app doesn’t render](#label-sis-embed-ts-render).

## The mint request fails

| Status | Likely cause |
| --- | --- |
| `400` | The `X-Snowflake-Role` header is missing or blank. The endpoint has no default-role fallback, so it must be sent explicitly. |
| `403` naming the role | The role in `X-Snowflake-Role` isn’t granted to the authenticating user. |
| `403` and the app definitely exists | The header role is missing USAGE on the app, schema, or database, or it’s missing EMBED. Owning the app doesn’t grant EMBED. |
| `403` mentioning allowed embedding domains | `parent_origin` isn’t in `STREAMLIT_EMBEDDING_CONTROLS.allowed_embedding_domains`. |
| `401` | The credential itself was rejected. Check the token hasn’t expired and that `X-Snowflake-Authorization-Token-Type` matches the credential you’re sending. |
| Connection failure or a rejection before any privilege error | A [network policy](/user-guide/network-policies) on the account or on the minting user doesn’t allow your backend’s egress IP range. |

Expand

Show lessSee more

A role that can’t see the app and a role that has USAGE but not EMBED both return `403`. The responses
are deliberately similar so that a caller can’t use the endpoint to discover which apps exist. If you
can’t tell which one you’re hitting, check both grants:

Copy code

```
SHOW GRANTS ON STREAMLIT mydb.public.my_app;
```

Confirm the minting role appears with both `USAGE` and `EMBED`. If EMBED is absent, grant it:

Copy code

```
GRANT EMBED ON STREAMLIT mydb.public.my_app TO ROLE <role_name>;
```

Adding a programmatic access token to the service user is a separate failure: the user needs a network
policy attached before you can add a PAT.

## The app doesn’t render

| Symptom | Likely cause |
| --- | --- |
| The iframe loads blank, or the console shows a CSP error | Your page isn’t served from the origin you passed as `parent_origin`. It must match exactly. |
| The embed URL works once, then fails on reload | The URL is single-use. Mint a fresh one per embed session, and check your frontend isn’t fetching it twice. A React component that mounts twice in development will spend the code on the first mount. |
| The app shows a loading spinner indefinitely on first load | The container may be cold. It wakes automatically and the app renders once the container is ready, typically within a few minutes. |
| The app loads for you but not for some viewers | A network policy doesn’t allow the network those viewers are on. Policies apply to the viewer session, not just to the mint request. See [Network policies](/developer-guide/streamlit/features/embedding/overview#label-sis-embed-network-policies). |
| A download button does nothing | You set the iframe’s `sandbox` attribute without `allow-downloads`. |
| A microphone or camera prompt never appears | You set the iframe’s `sandbox` attribute without `allow-popups`. |
| Fonts fall back to system fonts | The font’s origin isn’t reachable, or the app is a Native App rather than Streamlit in Snowflake. External fonts over HTTPS are permitted in Streamlit in Snowflake. See [Security overview for Streamlit in Snowflake](/developer-guide/streamlit/object-management/security). |

Expand

Show lessSee more

To distinguish a render failure from an app that’s simply slow to start, listen for the lifecycle
events the embedded app posts to the parent window. `SNOWFLAKE_EMBED_ERROR` means the app failed;
continued silence after `SNOWFLAKE_EMBED_LOADED` never arrives usually means a cold container. For the
event list and a listener example, see the last step of either tutorial.

## What’s next?

- [Embed a Streamlit in Snowflake app for viewers without a Snowflake account](/developer-guide/streamlit/features/embedding/external-users): Embed for viewers who don’t have
  a Snowflake account.
- [Embed a Streamlit in Snowflake app for viewers with a Snowflake account](/developer-guide/streamlit/features/embedding/snowflake-users): Embed for viewers who sign in to
  Snowflake.
- [Troubleshooting Streamlit in Snowflake](/developer-guide/streamlit/troubleshooting): General Streamlit in Snowflake troubleshooting.
