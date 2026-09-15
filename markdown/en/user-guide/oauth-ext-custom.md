# Configure custom authorization servers for External OAuth

This topic describes how to create an External OAuth security integration in Snowflake, so clients can access Snowflake data by
authenticating with a custom authorization server.

If your authorization server is a [supported identity provider (IdP)](/user-guide/oauth-ext-overview#label-ext-oauth-overview) rather than a custom one, refer to the
topic focused on configuring that specific IdP.

## External OAuth token payload requirements

The access token that custom authentication servers send to Snowflake must contain the following payload information. For more information
about the Claims column, see [JWT Claims](https://tools.ietf.org/html/rfc7519#section-4).

| Claims | Description |
| --- | --- |
| scp | Scopes. A list of scopes in the access token. |
| scope | Scopes.  A comma-separated string of scopes in the access token.  Snowflake supports specifying any single character for the delimiter, such as a space (i.e. `' '`), by setting the `EXTERNAL_OAUTH_SCOPE_DELIMITER` property when [creating](/sql-reference/sql/create-security-integration-oauth-external) or [modifying](/sql-reference/sql/alter-security-integration-oauth-external) the External OAuth security integration for custom authorization servers.  Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to enable this property in your Snowflake account. |
| aud | Audience. Identifies the recipients that the access token is intended for as a string URI. |
| exp | Expiration time. Identifies the expiration time on or after which the access token must not be accepted for processing. |
| iss | Issuer. Identifies the principal that issued the access token as a string URI. |
| iat | Issued at. Required. Identifies the time at which the JWT was issued. |

Expand

Show lessSee more

Note

Snowflake supports the `nbf` (not before) claim, which identifies the time before which the access token must not be
accepted for processing.

If your custom authorization server supports the `nbf` (not before) claim, you can optionally include the `nbf` claim in the
access token.

To verify your token contains the required information, you can test the token on this [JSON Web Tokens](https://jwt.ms) site.

As a representative example, the **PAYLOAD: DATA** interface displays the token payload as follows.

Copy code

```
{
  "aud": "<audience_url>",
  "iat": 1576705500,
  "exp": 1576709100,
  "iss": "<issuer_url>",
  "scp": [
    "session:role:analyst"
  ]
}
```

## Configuration procedure

The following steps assume that your custom authorization server and environment can be configured to obtain the necessary values to create
the Snowflake Security Integration.

Important

The steps in this topic are a representative example on how to configure custom authorization servers.

You can configure your environment to any desired state and use any desired OAuth flow provided that you can obtain the necessary
information for the [External OAuth security integration](#label-ext-oauth-integration-custom).

Note that the following steps serve as a guide to obtain the necessary information to create the External OAuth security integration in
Snowflake.

Consult your internal security policies before configuring a custom authorization server to ensure your organization meets all regulations
and compliance requirements.

### Obtain key environment values to use External OAuth

When you configure your IdP and authorization server, you must collect the following values to define an External OAuth security
integration:

Issuer URL:
:   Include this URL with the `external_oauth_issuer` parameter.

RSA Public Key:
:   Include this value with the `external_oauth_rsa_public_key` parameter.

Audience URLs:
:   If more than one Audience URL is necessary, separate each URL with a comma in the `external_oauth_audience_list` parameter.

Scope attribute:
:   You can set this value to `scp` or `scope`. By default, this value is `scp`.

    You can set the value of the `external_oauth_scope_mapping_attribute` parameter to this value.

    If you do not use the default value, `scp`, then set value of the `external_oauth_scope_mapping_attribute` parameter to
    `scope`.

    For more information, refer to [External OAuth token payload requirements](#label-ext-oauth-token-payload-reqs).

User Attribute:
:   This attribute refers to attribute to identify users in your IdP. Include this attribute value in the
    `external_oauth_user_mapping_claim` parameter.

Snowflake User Attribute:
:   The attribute in Snowflake to identify users. Include this value in the `external_oauth_snowflake_user_mapping_attribute` parameter.

### Create an External OAuth security integration in Snowflake

This step creates an External OAuth security integration in Snowflake. The External OAuth security integration ensures that Snowflake can
communicate securely with and validate access tokens from your custom authorization server, and provide users access to Snowflake data based
on their user role associated with the access token. For more information, see
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-external).

Important

Only account administrators or a role with the global CREATE INTEGRATION privilege can execute this SQL command.

The External OAuth security integration parameter values are case-sensitive, and the values you put into the External OAuth security
integration must match the values in your environment. If the case of a value does not match, the access token will not be validated,
resulting in a failed authentication attempt.

**Create an External OAuth security integration in Snowflake**

> Copy code
>
> ```
> create security integration external_oauth_custom
>     type = external_oauth
>     enabled = true
>     external_oauth_type = custom
>     external_oauth_issuer = '<authorization_server_url>'
>     external_oauth_rsa_public_key = '<public_key_value>'
>     external_oauth_audience_list = ('<audience_url_1>', '<audience_url_2>')
>     external_oauth_token_user_mapping_claim = 'upn'
>     external_oauth_snowflake_user_mapping_attribute = 'login_name';
> ```

# Modifying Your External OAuth Security Integration

You can update your External OAuth security integration by executing an ALTER statement on the security integration.

For more information, see [ALTER SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/alter-security-integration-oauth-external).

### Using ANY role with External OAuth

In the configuration step to create a security integration in Snowflake, the OAuth access token includes the scope definition. Therefore, at runtime, using the External OAuth security integration allows neither the OAuth client nor the user to use an undefined role in the OAuth access token.

After validating the access token and creating a session, the ANY role can allow the OAuth client and user to decide its role. If necessary, the client or the user can switch to a role that is different that the role defined in the OAuth access token.

To configure ANY role, define the scope as `SESSION:ROLE-ANY` and configure the security integration with the `external_oauth_any_role_mode` parameter. This parameter can have three possible string values:

- `DISABLE` does not allow the OAuth client or user to switch roles (i.e. `use role role;`). Default.
- `ENABLE` allows the OAuth client or user to switch roles.
- `ENABLE_FOR_PRIVILEGE` allows the OAuth client or user to switch roles only for a client or user with the `USE_ANY_ROLE` privilege. This privilege can be granted and revoked to one or more roles available to the user. For example:

  Copy code

  ```
  grant USE_ANY_ROLE on integration external_oauth_1 to role1;
  ```

  Copy code

  ```
  revoke USE_ANY_ROLE on integration external_oauth_1 from role1;
  ```

Define the security integration as follows:

Copy code

```
create security integration external_oauth_1
    type = external_oauth
    enabled = true
    external_oauth_any_role_mode = 'ENABLE'
    ...
```

### Using secondary roles with External OAuth

The desired scope for the primary role is passed in the external token: either the default role for the user (`session:role-any`) or
a specific role that was granted to the user (`session:role:role_name`).

By default, Snowflake does not activate the default [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) for a user (i.e.
the DEFAULT\_SECONDARY\_ROLES) user in the session.

To activate the default secondary roles for a user in a session and allow executing the [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)
command while using External OAuth, complete the following steps:

1. Configure the security integration for the connection. Set the EXTERNAL\_OAUTH\_ANY\_ROLE\_MODE parameter value to either ENABLE or
   ENABLE\_FOR\_PRIVILEGE when you create the security integration (using CREATE SECURITY INTEGRATION) or later (using ALTER SECURITY
   INTEGRATION).
2. Configure the authorization server to pass the static value of `session:role-any` in the scope attribute of the token. For more
   information about the scope parameter, see [External OAuth overview](/user-guide/oauth-ext-overview).

### Using Client Redirect with External OAuth

Snowflake supports using Client Redirect with External OAuth, including using Client Redirect and External OAuth with supported Snowflake
Clients.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

### Using network policies with External OAuth

Currently, network policies cannot be added to your External OAuth security integration. However, you can still implement network policies that apply broadly to the entire Snowflake account.

If your use case requires a network policy that is specific to the OAuth security integration, use [Snowflake OAuth](oauth-intro). This approach allows the Snowflake OAuth network policy to be distinct from other network policies that may apply to the Snowflake account.

For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

### Using replication with External OAuth

Snowflake supports replication and failover/failback of the External OAuth security integration from a source account to a target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

## Configuring agent sessions

Snowflake supports designating External OAuth integrations as agentic. When an integration is configured with `IS_AGENTIC = TRUE`, Snowflake automatically recognizes and treats all incoming requests from that client as an AI agent acting on behalf of a user.

As a result, the system function [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) will return `TRUE` for these sessions.

Set `IS_AGENTIC = TRUE` if you expect all authentication requests for this integration to be agentic. This enables enhanced auditing and specialized governance for your AI workflows, ensuring that agent-driven data access is explicitly tracked, monitored, and secured.

For an overview of agent identity, including other ways Snowflake marks sessions as agentic, see
[Agent identity](/user-guide/agent-identity). For more information about the OAuth parameters, see
[CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external) and
[ALTER SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/alter-security-integration-oauth-external).

## Testing procedure

To test the configuration of a custom authorization server:

1. Verify that the test user exists in your IdP and has a password.
2. Verify that the test user exists in Snowflake with their `login_name` attribute value set to the
   `<external_oauth_token_user_mapping_claim>`.
3. Register an OAuth 2.0 client
4. Allow the OAuth 2.0 client to make a POST request to the custom token endpoint as follows:
   - Grant type set to Resource Owner
   - HTTP Basic Authorization header containing the clientID and secret
   - FORM data containing the username & password
   - Include scopes

The sample command requests the `ANALYST` custom role and that assumes the `session:role:analyst` has been defined in the custom
authorization server.

Here is an example for getting an access token using cURL.

Copy code

```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
  --user <OAUTH_CLIENT_ID>:<OAUTH_CLIENT_SECRET> \
  --data-urlencode "username=<IdP_USER_USERNAME>" \
  --data-urlencode "password=<IdP_USER_PASSWORD>" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "scope=session:role:analyst" \
  <IdP_TOKEN_ENDPOINT>
```

## Connecting to Snowflake with External OAuth

After configuring your security integration and obtaining your access token, you can connect to Snowflake using one of the following:

- [SnowSQL](/user-guide/snowsql-start#label-snowsql-auth)
- [Python Connector](/developer-guide/python-connector/python-connector-connect#label-oauth-python)
- [Go Driver](https://godoc.org/github.com/snowflakedb/gosnowflake#hdr-Connection_Parameters)
- [JDBC Driver](/developer-guide/jdbc/jdbc-configure#label-jdbc-connection-parameters)
- [ODBC Driver](/developer-guide/odbc/odbc-parameters#label-conn-param-odbc)
- [Spark Connector](/user-guide/spark-connector-use#label-spark-ext-oauth)
- [.NET Driver](https://github.com/snowflakedb/snowflake-connector-net/blob/master/README.md#create-a-connection)
- [Node.js Driver](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-oauth)

Note the following:

- It is necessary to set the `authenticator` parameter to `oauth` and the `token` parameter to the `external_oauth_access_token`.
- When passing the `token` value as a URL query parameter, it is necessary to URL-encode the `token` value.
- When passing the `token` value to a Properties object (e.g. JDBC Driver), no modifications are necessary.

For example, if using the Python Connector, set the connection string as shown below.

Copy code

```
ctx = snowflake.connector.connect(
   user="<username>",
   host="<hostname>",
   account="<account_identifier>",
   authenticator="oauth",
   token="<external_oauth_access_token>",
   warehouse="test_warehouse",
   database="test_db",
   schema="test_schema"
)
```

You can now use External OAuth to connect to Snowflake securely.
