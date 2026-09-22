# Embedding Streamlit in Snowflake apps in external pages

Feature — Generally Available

Not supported in government regions.

You can configure a Streamlit in Snowflake app to embed in an external web page, such as a customer portal or an
internal dashboard, using a single `<iframe>` tag.

This page introduces the feature and the decisions you need to make before you implement it. When
you’re ready to build, follow the tutorial for the kind of viewers you have.

## How embedding works

Three parties are involved: your Snowflake account, your web server backend, and the browser that
loads your page.

1. **An account administrator enables embedding.** Embedding only works on pages served from origins
   that an administrator has registered on the account. This is what stops an unrelated site from
   putting your app in an iframe.
2. **Your backend mints an embed URL.** When someone loads your page, your backend calls a Snowflake
   REST endpoint and gets back a short-lived, single-use URL for the app. Your backend authenticates
   to Snowflake to do this, so the credential never reaches the browser.
3. **Your page renders the URL in an iframe.** The browser loads the URL, redeems the one-time code it
   carries, and gets an isolated viewer session for the app.

The embed URL is the security boundary. It’s minted server-side, expires quickly, works only once, and
grants exactly the access of the role it was minted under. Nothing about embedding requires you to
give browsers Snowflake credentials.

## Choose an embedding model

Embedding supports two models. The difference is who the app runs as, which determines what data each
viewer sees. Choose before you start, because the model decides which identity your backend
authenticates as.

|  | Viewers without a Snowflake account | Viewers with a Snowflake account |
| --- | --- | --- |
| Who your viewers are | Anyone who can load your page. They don’t sign in to Snowflake. | Users already provisioned in Snowflake, typically through an external identity provider. |
| The app runs as | A dedicated service user you create. | The viewer. |
| What viewers see | The same data for everyone. | Data scoped to each viewer’s own privileges. |
| Your backend authenticates as | The service user, using a long-lived credential you manage. | Each viewer, using that viewer’s OAuth token. |

Expand

Show lessSee more

Both models use the same endpoint and the same iframe markup. If you’re unsure, the deciding question
is whether different viewers must see different data. If they must, you need Snowflake-provisioned
viewers, because that’s what lets Snowflake evaluate each viewer’s privileges.

## Security considerations

Embedding puts a Streamlit in Snowflake app on a page you control but that Snowflake doesn’t. The controls described in
the tutorials decide who can mint a URL and where the app is allowed to load. They don’t control what
a viewer does with the app after it renders. Review this section before you embed an app that reads
sensitive data.

Important

Embedded Streamlit in Snowflake apps are intended for access by you and the users you authorize under your Snowflake
account. You’re responsible for making sure that only authorized users can reach an embedded app and
see what it displays, and for the activity that takes place through it.

### What the allowed-domains list does and doesn’t do

Registering an origin prevents an arbitrary third-party page from putting your app in an iframe.
That’s worth configuring carefully: it’s what stops another site from framing your app to stage
clickjacking and similar attacks against your viewers.

It isn’t a guarantee that your app and its data are only ever visible on your page. A viewer who can
load the app can also read what it renders, and can copy that content elsewhere, whether by hand, with
a scraper, or by extracting the short-lived session token the browser uses to talk to the app.
Restricting embedding domains raises the effort required, but it can’t prevent a determined viewer from
reproducing your dashboard’s content elsewhere.

Treat an embedded app the way you’d treat any other page you publish:

- Decide what data belongs in an app whose viewers you don’t authenticate. Anything an anonymous
  viewer can see is effectively public, whatever origin it’s framed on.
- Keep the minting role’s grants minimal. The viewer session inherits the role the URL was minted
  under, so a broad role widens what that session can reach. Grant USAGE and EMBED on the one app you
  intend to embed, and nothing more.
- If each viewer should see different data, authenticate them and run the app as the viewer, rather
  than relying on the embedding domain list to separate them.

### External content in embedded apps

Embedded apps run under the same Content Security Policy as any other Streamlit in Snowflake app. The CSP blocks
scripts and styles from external domains, but it permits fonts, images, and media from any HTTPS
origin. This is deliberate, so that apps can use external font services for advanced theming.

Balancing security with usability means the CSP doesn’t restrict every potentially dangerous behavior
for untrusted content. An embedded app that renders user-contributed or otherwise untrusted markup can
have that content reach an external server, for example using calls to third-party font styles. Don’t
render untrusted content in an embedded app, and don’t rely on the CSP to stop an app from
communicating outward. For details, see [Security overview for Streamlit in Snowflake](/developer-guide/streamlit/object-management/security).

### Network policies

Embedding doesn’t create an exception to your account’s network rules. If your account or users have
[network policies](/user-guide/network-policies) attached, those policies still apply, and they apply
in two separate places:

- **The mint request.** Your backend calls the endpoint as a Snowflake user, so that call is subject
  to that user’s network policy. Allow-list your backend’s egress IP range, or the mint fails before
  it ever reaches the app. If your backend has a static egress IP, this is also a useful restriction
  to add on purpose, so that the minting credential is only usable from your infrastructure.
- **The viewer session.** The browser that loads the iframe connects to the app directly, so a viewer
  outside the allowed ranges can’t reach an embedded app even with a valid embed URL. An app embedded
  on an internet-facing page is still only reachable from the networks your policies permit.

The second point is what makes network policies useful alongside the embedding domain list: the domain
list controls *where* the app may be framed, and network policies control *from what networks* it can
be reached at all.

One caveat applies to Snowflake-provisioned viewers. Because your backend establishes the connection
that mints each URL, the mint is attributed to your backend’s IP address rather than to the individual
viewer. You can’t apply per-user network policies to the mint step for those viewers, though the
viewer session itself is still subject to policy.

## What’s next?

- [Embed a Streamlit in Snowflake app for viewers without a Snowflake account](/developer-guide/streamlit/features/embedding/external-users): Embed for viewers who don’t have
  a Snowflake account. The app runs as a service user, and every viewer sees the same data.
- [Embed a Streamlit in Snowflake app for viewers with a Snowflake account](/developer-guide/streamlit/features/embedding/snowflake-users): Embed for viewers who sign in to
  Snowflake. The app runs as each viewer, scoped to their own privileges.
- [Troubleshoot embedded Streamlit in Snowflake apps](/developer-guide/streamlit/features/embedding/troubleshooting): Diagnose mint failures, blank
  iframes, and apps that load for some viewers but not others.
- [Sharing Streamlit in Snowflake apps](/developer-guide/streamlit/features/sharing-streamlit-apps): Share apps with users inside your
  Snowflake account instead of embedding them.
