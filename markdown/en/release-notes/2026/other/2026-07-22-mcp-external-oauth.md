# Jul 22, 2026: External OAuth and configurable scopes for MCP servers (*General availability*)

Two new hierarchical parameters let you bind MCP servers to your organization’s existing identity provider (IdP) and control which OAuth scopes MCP clients discover. This enables MCP clients such as Claude, Cursor, and ChatGPT to authenticate against your corporate IdP instead of Snowflake OAuth.

## New parameters

`OAUTH_AUTHORIZATION_SERVER`
:   Specifies the name of an [External OAuth security integration](/sql-reference/sql/create-security-integration-oauth-external) to use as the authorization server for MCP servers. When set, Snowflake advertises the external issuer in the Protected Resource Metadata endpoint and rejects OAuth tokens that weren’t issued by that authorization server. Enforcement applies only to OAuth calls against MCP server endpoints.

`OAUTH_SCOPES_SUPPORTED`
:   Specifies a comma-separated list of OAuth scopes to advertise in the Protected Resource Metadata endpoint for MCP servers. For accepted scope values, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

Both parameters are settable at the account, database, and schema levels using `ALTER ACCOUNT`, `ALTER DATABASE`, or `ALTER SCHEMA`. They follow Snowflake’s standard lineage inheritance: a schema-level value overrides a database-level value, which overrides an account-level value.

## Use cases

- **External IdP authentication**: Bind MCP servers to Okta, Microsoft Entra ID, or another IdP so that MCP clients auto-discover and use your corporate authorization server.
- **Scope customization**: Advertise specific roles or IdP-defined scopes to restrict which Snowflake roles MCP clients can request.
- **Hierarchical configuration**: Set the parameters once at the account, database, or schema level so MCP servers in that scope inherit the binding.

## Example

The following example configures a schema-level External OAuth binding so that all MCP servers in the `mcp_schema` schema use an Okta integration for authentication.

**Step 1**: Create an External OAuth security integration:

Copy code

```
CREATE SECURITY INTEGRATION external_oauth_okta
  TYPE = EXTERNAL_OAUTH
  ENABLED = TRUE
  EXTERNAL_OAUTH_TYPE = OKTA
  EXTERNAL_OAUTH_ISSUER = '<OKTA_ISSUER>'
  EXTERNAL_OAUTH_JWS_KEYS_URL = '<OKTA_JWS_KEY_ENDPOINT>'
  EXTERNAL_OAUTH_AUDIENCE_LIST = ('https://<orgname>-<account_name>.snowflakecomputing.com')
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'sub'
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name';
```

**Step 2**: Bind the integration to a schema and configure scopes:

Copy code

```
ALTER SCHEMA analytics_db.mcp_schema
  SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta
      OAUTH_SCOPES_SUPPORTED = 'session:role:ANALYST,session:role:ANALYST_READONLY';
```

**Step 3**: Create an MCP server in the schema. The server inherits the OAuth binding from the schema:

Copy code

```
CREATE MCP SERVER analytics_db.mcp_schema.docs_mcp_server
  FROM SPECIFICATION $$
  tools:
    - name: "docs-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "analytics_db.mcp_schema.docs_search_service"
      description: "Search service for internal documentation"
      title: "Documentation Search"
  $$;
```

After this setup, MCP clients that connect to `docs_mcp_server` automatically discover the Okta authorization server issuer and the advertised scopes through the Protected Resource Metadata endpoint.

## Behavior when integration is unavailable

If the security integration referenced by `OAUTH_AUTHORIZATION_SERVER` is dropped or disabled after the parameter is set, the Protected Resource Metadata endpoint publishes an empty `authorization_servers` list. Snowflake doesn’t fall back to Snowflake OAuth. Inbound OAuth requests to MCP servers in that scope are rejected until you restore the integration, bind a different one, or unset the parameter.

## Related information

- [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth)
- [External OAuth overview](/user-guide/oauth-ext-overview)
- [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external)
- [Parameters reference: OAUTH\_AUTHORIZATION\_SERVER and OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters)
- [ALTER ACCOUNT](/sql-reference/sql/alter-account)
- [ALTER DATABASE](/sql-reference/sql/alter-database)
- [ALTER SCHEMA](/sql-reference/sql/alter-schema)
