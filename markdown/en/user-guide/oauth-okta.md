# Configure Okta for External OAuth

This topic describes how to configure Snowflake as an OAuth Resource and Okta as an External OAuth authorization server to facilitate
secure, programmatic access to Snowflake data.

## Configuration procedure

The following five steps assume that your environment does not have anything configured relating to Okta OAuth authorization servers,
OAuth clients, scopes, and necessary metadata.

The information from Steps 1-3 will be used to create a security integration in Snowflake.

If you already have an Okta authorization server and client configured, it is not necessary to complete all of the steps below. Rather,
skim the following four steps and verify that you can obtain the desired information, create scopes, assign scopes to one or more policies,
and access the metadata.

If you do not have an Okta OAuth authorization server and client configured, complete all of the following five steps.

Important

The steps in this topic are a representative example on how to configure Okta for External OAuth.

You can configure Okta to any desired state and use any desired OAuth flow provided that you can obtain the necessary information for the
[security integration](#label-ext-oauth-integration-okta) (in this topic).

Note that the following steps serve as a guide to obtain the necessary information to create the security integration in Snowflake.

Be sure to consult your internal security policies with regard to configuring an authorization server to ensure your organization meets
all necessary regulations and compliance requirements.

Steps 1-3 are derived from the Okta documentation on Authorization Servers. For more information on how Okta defines its terms, its user
interface, and options relating to Authorization Servers, consult the following Okta guides:

- [Create an Authorization Server](https://developer.okta.com/docs/guides/customize-authz-server/overview/)
- [Implement the Authorization Code Flow](https://developer.okta.com/docs/guides/implement-auth-code/overview/)
- [Implement the Authorization Code Flow with PKCE](https://developer.okta.com/docs/guides/implement-auth-code-pkce/overview/)
- [Implement the Client Credentials Flow](https://developer.okta.com/docs/guides/implement-client-creds/overview/)
- [Implement the Resource Owner Password Flow](https://developer.okta.com/docs/guides/implement-password/overview/)
- [Refresh Access Tokens](https://developer.okta.com/docs/guides/refresh-tokens/overview/)

### Create an OAuth compatible client to use with Snowflake

1. Navigate to the Okta Admin Console.
2. Click **Applications**.
3. Click **Add Application**.
4. Click **Create New App**.

   - For **Platform**, select **Native App**.
5. Click **Create**.
6. Enter a name for the application.
7. In the **Login redirect URIs** box, add the full Snowflake account URL
   (i.e. `https://<account_identifier>.snowflakecomputing.com`). For a list of possible URL formats, see
   [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url).
8. Click **Save**.
9. From **New Applications** in the **General** interface, click **Edit**.
10. Check **Refresh Token** and **Resource Owner Password**.
11. Click **Save**.
12. Click the **Edit** button next to **Client Credentials**.
13. Select the **Use Client Authentication** option.
14. Click **Save**.
15. In the **Client Credentials** container, save the **ClientID** and **Secret**. These two values will be known as the
    `<OAUTH_CLIENT_ID>` and `<OAUTH_CLIENT_SECRET>`, respectively in the following steps.

### Create an OAuth authorization server

1. Navigate to the Okta Admin Console.
2. In the **Security** menu, click **API**.
3. Click **Authorization Servers**.
4. Click **Add Authorization Server**.
5. Enter a name.
6. Enter the Snowflake account URL as the **Audience** value. For a list of possible URL formats, see [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url).
7. Click **Save**.

Complete the following steps for the newly added Authorization Server.

1. Copy the **Issuer** value. Its format should resemble `https://dev-390798.oktapreview.com/oauth2/auslh9j9vf9ej7NfT0h7`. This
   value will be known as the `<OKTA_ISSUER>` in the following steps.
2. Click on **Scopes**.
3. Click on **Add Scope**.
4. To add a Snowflake Role as a scope, enter the scope by having the name of the Snowflake role with the `session:role:` prefix
   (e.g.: for the Snowflake Analyst role, enter `session:role:analyst`).
5. Click **Create**.
6. Click on **Access Policies**.
7. Click **Add Policy**.
8. Enter a name and a description for the policy. Assign it to the client created earlier and click **Create**.
9. In the newly added Access Policy, click **Add Rule**.
10. Enter a rule name.
11. Select the authorized **Grant Types**. You should select **Resource Owner Password** and **Client Credentials** along
    with any others that match your organization’s policies.
12. For scopes, you can select any of the scopes or select the desired scopes created earlier that clients assigned to this policy will be
    able to request (including offline\_access for refresh tokens if needed). Configure any additional settings as needed.
13. Click **Create Rule**.

### Collect Okta information

1. Go to the Okta Admin Console.
2. In the **Security** menu, click **API**.
3. Click **Authorization Servers**.
4. Click on the Authorization Server for the Snowflake Resource.
5. In the **Settings** tab, copy the **Issuer** value. This value will be known as the `<OKTA_ISSUER>` in the following
   steps. Its format should resemble `https://dev-111111.oktapreview.com/oauth2/auslh9j9vf9ej7NfT0h7`.

In the **Metadata** document:

1. Copy the **Metadata URI** value, open a browser tab, and paste the URL in the address bar.
2. You should see JSON text in the browser. You can work with this text in a text editor or in the browser itself.
3. Locate the `"jwks_uri"` parameter and copy its value. Its format should resemble
   `https://dev-111111.oktapreview.com/oauth2/auslh9j9vf9ej7NfT0h7/v1/keys`. This endpoint will be known as the
   `<OKTA_JWS_KEY_ENDPOINT>` in the following steps.
4. Locate the `"token_endpoint"` parameter and copy its value. Its format should resemble
   `https://dev-111111.oktapreview.com/oauth2/auslh9j9vf9ej7NfT0h7/v1/token`. This endpoint will be known as the `<OKTA_OAUTH_TOKEN_ENDPOINT>` in the following steps.

### Create a security integration for Okta

This step creates a security integration in Snowflake. The security integration ensures that Snowflake can communicate with Okta securely,
validates the tokens from Okta, and provides the appropriate Snowflake data access to users based on the user role associated with the
OAuth token.

For more information, see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-external).

Important

Only account administrators (i.e. users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute
this SQL command.

The security integration parameter values are case-sensitive and the values you put into the security integration must match those values
in your environment. If the case does not match, it is possible that the access token will not be validated resulting in a failed
authentication attempt.

**Create a security integration with audiences**

> The `external_oauth_audience_list` parameter of the security integration must match the **Audience** that you specified
> while configuring Okta.
>
> Copy code
>
> ```
> create security integration external_oauth_okta_2
>     type = external_oauth
>     enabled = true
>     external_oauth_type = okta
>     external_oauth_issuer = '<OKTA_ISSUER>'
>     external_oauth_jws_keys_url = '<OKTA_JWS_KEY_ENDPOINT>'
>     external_oauth_audience_list = ('<snowflake_account_url>')
>     external_oauth_token_user_mapping_claim = 'sub'
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

Snowflake supports using Client Redirect with External OAuth, including using Client Redirect and OAuth with supported Snowflake Clients.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

### Using network policies with External OAuth

Currently, network policies cannot be added to your External OAuth security integration. However, you can still implement network policies that apply broadly to the entire Snowflake account.

If your use case requires a network policy that is specific to the OAuth security integration, use [Snowflake OAuth](oauth-intro). This approach allows the Snowflake OAuth network policy to be distinct from other network policies that may apply to the Snowflake account.

For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

### Using replication with External OAuth

Snowflake supports replication and failover/failback of the External OAuth security integration from a source account to a target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

## Testing procedure

In the context of testing OAuth while using Okta as an authorization server, you must:

1. Verify that the test user exists in Okta and has a password.
2. Verify that the test user exists in Snowflake with their `login_name` attribute value set to the `<OKTA_USER_USERNAME>`
3. Register an OAuth Client.
4. Allow the OAuth Client to make a POST request to the Okta Token endpoint as follows:
   - Grant type set to Resource Owner
   - HTTP Basic Authorization header containing the clientID and secret
   - FORM data containing the user’s username & password
   - Include scopes

The sample command requests the Analyst and that assumes the `session:role:analyst` have been defined in
**Okta > OAuth App Resource**.

Here is an example for getting an access token using cURL.

Copy code

```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
  --user <OAUTH_CLIENT_ID>:<OAUTH_CLIENT_SECRET> \
  --data-urlencode "username=<OKTA_USER_USERNAME>" \
  --data-urlencode "password=<OKTA_USER_PASSWORD>" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "scope=session:role:analyst" \
  <OKTA_OAUTH_TOKEN_ENDPOINT>
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
