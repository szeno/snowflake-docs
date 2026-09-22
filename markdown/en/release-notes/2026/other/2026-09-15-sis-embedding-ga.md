# Sep 15, 2026: Embedding Streamlit in Snowflake apps in external pages (*General availability*)

Embedding Streamlit in Snowflake apps in external pages is now generally available. You can render a container-runtime
app inside a page you host, such as a customer portal or an internal dashboard, using a single
`<iframe>` tag.

An account administrator registers the domains where embedded apps may load, your backend mints a
short-lived embed URL through the Snowflake REST API, and your page passes that URL to an iframe. The
mint call is a plain HTTPS request, so no SQL session and no Snowflake driver are required:

```
POST /api/v2/databases/{database}/schemas/{schema}/streamlits/{name}:generate-embed-url
```

Two embedding models are supported. Apps embedded for viewers without a Snowflake account run as a
service user you create, so every viewer sees the same data. Apps embedded for viewers who are
provisioned in Snowflake run as the viewer, so each one sees only the data their own privileges allow.

Minting an embed URL requires the new EMBED privilege on the Streamlit app, in addition to USAGE:

Copy code

```
GRANT USAGE ON STREAMLIT mydb.public.my_app TO ROLE embed_minter;
GRANT EMBED ON STREAMLIT mydb.public.my_app TO ROLE embed_minter;
```

EMBED is granted separately from USAGE and isn’t implied by OWNERSHIP, so you can share an app with a
role for viewing in Snowsight without also allowing that role to publish it to an external
page.

Embedding is available in all commercial regions. Government and China regions aren’t supported.

For more information, see:

- [Embedding Streamlit in Snowflake apps in external pages](/developer-guide/streamlit/features/embedding/overview)
- [Embed a Streamlit in Snowflake app for viewers without a Snowflake account](/developer-guide/streamlit/features/embedding/external-users)
- [Embed a Streamlit in Snowflake app for viewers with a Snowflake account](/developer-guide/streamlit/features/embedding/snowflake-users)
- [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges)
