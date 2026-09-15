# Configure Microsoft Entra ID for External OAuth

This topic describes how to configure Snowflake as an OAuth Resource and Microsoft Entra ID as an External OAuth Authorization Server to
facilitate secure, programmatic access to Snowflake data.

## Configuration procedure

The following four steps assume that your environment does not have anything configured relating to Microsoft Entra ID OAuth authorization
servers, OAuth clients, scopes, and necessary metadata.

The information from Steps 1-3 will be used to create a security integration in Snowflake.

If you already have an Microsoft Entra ID OAuth authorization server and client configured, it is not necessary to complete all of the steps
below. Rather, skim the following three steps and verify that you can obtain the desired information, create scopes, assign scopes to one or
more policies, and access the metadata.

If you do not have an Microsoft Entra ID OAuth authorization server and client configured, complete all of the following four steps.

Important

The steps in this topic are a representative example on how to configure Microsoft Entra ID for External OAuth.

You can configure Microsoft Entra ID to any desired state and use any desired OAuth flow provided that you can obtain the necessary
information for the [security integration](#label-ext-oauth-integration-aad) (in this topic).

Note that the following steps serve as a guide to obtain the necessary information to create the security integration in Snowflake.

Steps 1-3 are derived from the Microsoft Entra ID documentation on OAuth 2.0 and authentication. For more information on how Microsoft
defines its terms, its user interface, and options relating to OAuth 2.0 and authentication consult the following Microsoft Entra ID guides:

- [Microsoft identity platform (v2.0) overview](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-overview)
- [Authentication protocol (and related topics)](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-app-types)
- [Application configuration (and related topics)](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)
- [How-to guides for authentication & application configuration (and related topics)](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-enterprise-app-role-management)

### Determine the OAuth flow in Microsoft Entra ID

Microsoft Entra ID supports two different OAuth flows in which an OAuth Client can get an access token.

1. The authorization server can grant the OAuth client an access token on behalf of the user.
2. The authorization server can grant the OAuth client an access token for the OAuth client itself.

In the first flow, the identity in the access token references the user. In the second flow, the identity in the access token references
the OAuth client.

Microsoft Entra ID does not allow the same role format for each of these two OAuth flows. The role format to use depends on the OAuth
flow in use. After determining which OAuth flow to use:

- Complete sub-step 10 or 11 in [Configure the OAuth resource in Microsoft Entra ID](#label-configure-oauth-resource-in-microsoft-idp)
- Complete sub-step 13 or 14 in [Create an OAuth client in Microsoft Entra ID](#label-create-an-oauth-client-in-microsoft-idp)

### Configure the OAuth resource in Microsoft Entra ID

1. Navigate to the [Microsoft Azure Portal](https://portal.azure.com) and authenticate.
2. Navigate to Microsoft Entra ID.
3. Click on **App Registrations**.
4. Click on **New Registration**.
5. Enter `Snowflake OAuth Resource`, or similar value as the **Name**.
6. Verify the **Supported account types** is set to **Single Tenant**.
7. Click **Register**.
8. Click on **Expose an API**.
9. Click on the **Set** link next to **Application ID URI** to set the `Application ID URI`.

   > Important
   >
   > The `Application ID URI` must be unique within your organization’s directory, such as
   > `https://your.example.com/4d2a8c2b-a5f4-4b86-93ca-294185f45f2e`. This value will be referred to as the
   > `<SNOWFLAKE_APPLICATION_ID_URI>` in the subsequent configuration steps.
   >
   > For help obtaining your Application ID URI, please contact your internal Microsoft Entra ID administrator.
   >
   > If the Application ID URI is not used, then it is necessary to create a security integration with audiences using the Snowflake
   > Account URL (that is, `<account_identifier>.snowflakecomputing.com`). For more information, see:
   >
   > - The audience integration in [Create a security integration in Snowflake](#create-a-security-integration-in-snowflake).
   > - [Account identifiers](/user-guide/admin-account-identifier).
10. To add a Snowflake Role as an OAuth scope for OAuth flows where the programmatic client acts on behalf of a user, click on
    **Add a scope** to add a scope representing the Snowflake role.

- Enter the scope by having the name of the Snowflake role with the `session:scope:` prefix. For example, for the Snowflake
  Analyst role, enter `session:scope:analyst`.
- Select who can consent.
- Enter a **display name** for the scope (for example, Account Admin).
- Enter a **description** for the scope (for example, Can administer the Snowflake account).
- Click **Add Scope**.

11. To add a Snowflake Role as a Role for OAuth flows where the programmatic client requests an access token for itself:

- Click on **Manifest**.
- Locate the `appRoles` element.
- Enter an **App Role** with the following settings.

  | Setting | Description |
  | --- | --- |
  | allowedMemberTypes | Application. |
  | description | A description of the role. |
  | displayName | A friendly name for users to view. |
  | id | A unique ID. You can use the `[System.Guid]::NewGuid()` function from PowerShell to generate a unique ID if needed. |
  | isEnabled | Set to `true`. |
  | lang | The language. Set to `null`. |
  | origin | Set to `Application`. |
  | value | Set to the name of the Snowflake role with the `session:role:` prefix.   For the Analyst role, enter `session:role:analyst`. |

  Expand

  Show lessSee more

  The **App Role** manifests as follows.

  Copy code

  ```
  "appRoles":[
      {
          "allowedMemberTypes": [ "Application" ],
          "description": "Account Administrator.",
          "displayName": "Account Admin",
          "id": "3ea51f40-2ad7-4e79-aa18-12c45156dc6a",
          "isEnabled": true,
          "lang": null,
          "origin": "Application",
          "value": "session:role:analyst"
      }
  ]
  ```

12. Click **Save**.

### Create an OAuth client in Microsoft Entra ID

1. Navigate to the [Microsoft Azure Portal](https://portal.azure.com) and authenticate.
2. Navigate to Azure Active Directory.
3. Click on **App Registrations**.
4. Click on **New Registration**.
5. Enter a name for the client such as `Snowflake OAuth Client`.
6. Verify the Supported account types is set to Single Tenant.
7. Click **Register**.
8. In the **Overview** section, copy the `ClientID` from the **Application (client) ID** field. This will be known as the
   `<OAUTH_CLIENT_ID>` in the following steps.
9. Click on **Certificates & secrets** and then **New client secret**.
10. Add a description of the secret.
11. Select **never expire**. For testing purposes, select secrets that never expire.
12. Click **Add**. Copy the secret. This will be known as the `<OAUTH_CLIENT_SECRET>` in the following steps.
13. For programmatic clients that will request an Access Token on behalf of a user, configure Delegated permissions for Applications as
    follows.

- Click on **API Permissions**.
- Click on **Add Permission**.
- Click on the Microsoft Entra ID setting that corresponds to the available APIs (for example, **My APIs** or **APIs my organization uses**).
- Click on the **Snowflake OAuth Resource** that you created in [Configure the OAuth resource in Microsoft Entra ID](#label-configure-oauth-resource-in-microsoft-idp).
- Click on the **Delegated Permissions** box.
- Check on the Permission related to the Scopes defined in the Application that you wish to grant to this client.
- Click **Add Permissions**.
- Click on the **Grant Admin Consent** button to grant the permissions to the client. Note that for testing purposes, permissions
  are configured this way. However, in a production environment, granting permissions in this manner is not advisable.
- Click **Yes**.

14. For programmatic clients that will request an Access Token for themselves, configure **API permissions for Applications** as
    follows.

- Click on **API Permissions**.
- Click on **Add Permission**.
- Click on **My APIs**.
- Click on the **Snowflake OAuth Resource** that you created in [Configure the OAuth resource in Microsoft Entra ID](#label-configure-oauth-resource-in-microsoft-idp).
- Click on the **Application Permissions**.
- Check on the **Permission** related to the Roles manually defined in the `Manifest` of the Application that you wish to
  grant to this client.
- Click **Add Permissions**.
- Click on the **Grant Admin Consent** button to grant the permissions to the client. Note that for testing purposes, permissions
  are configured this way. However, in a production environment, granting permissions in this manner is not advisable.
- Click **Yes**.

### Collect Azure AD information for Snowflake

1. Navigate to the [Microsoft Azure Portal](https://portal.azure.com) and authenticate.
2. Navigate to Azure Active Directory.
3. Click on **App Registrations**.
4. Click on the **Snowflake OAuth Resource** that you created in [Configure the OAuth resource in Microsoft Entra ID](#label-configure-oauth-resource-in-microsoft-idp).
5. Click on **Endpoints** in the **Overview** interface.
6. On the right-hand side, copy the **OAuth 2.0 token endpoint (v2)** and note the URLs for **OpenID Connect metadata** and
   **Federation Connect metadata**.
   - The **OAuth 2.0 token endpoint (v2)** will be known as the `<AZURE_AD_OAUTH_TOKEN_ENDPOINT>` in the following configuration
     steps. The endpoint should be similar to
     `https://login.microsoftonline.com/90288a9b-97df-4c6d-b025-95713f21cef9/oauth2/v2.0/token`.
   - For the **OpenID Connect metadata**, open in a new browser window.

     - Locate the `"jwks_uri"` parameter and copy its value.
     - This parameter value will be known as the `<AZURE_AD_JWS_KEY_ENDPOINT>` in the following configuration steps. The endpoint
       should be similar to `https://login.microsoftonline.com/90288a9b-97df-4c6d-b025-95713f21cef9/discovery/v2.0/keys`.
   - For the **Federation metadata document**, open the URL in a new browser window.

     - Locate the `"entityID"` parameter in the `XML Root Element` and copy its value.
     - This parameter value will be known as the `<AZURE_AD_ISSUER>` in the following configuration steps. The entityID value should
       be similar to `https://sts.windows.net/90288a9b-97df-4c6d-b025-95713f21cef9/`.

### Create a security integration in Snowflake

This step involves creating a security integration in Snowflake to ensure that Snowflake can communicate with Microsoft Entra ID securely,
validate the tokens from Microsoft Entra ID, and provide the appropriate Snowflake data access to users based on the user role associated with
the OAuth token.

Choose the security integration that best addresses your use case and configuration needs. If your integration is only based on the
preceding configuration, use the first security integration. For more information, see
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-external).

Important

If you are trying to create a security integration for Microsoft Power BI, follow the setup instructions in [Power BI SSO to Snowflake](/user-guide/oauth-powerbi).

Only account administrators (that is, users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute
this SQL command.

The security integration parameter values are case-sensitive, and the values you put into the security integration must match those
values in your environment. If the case does not match, it is possible that the access token will not be validated, resulting in a failed
authentication attempt.

Verify all values are an exact match. For example, if the Issuer value does not end with a backslash and the security integration is
created with a backslash character at the end of the URL, an error message will occur. It would then be necessary to drop the security
integration object using [DROP INTEGRATION](/sql-reference/sql/drop-integration) and then create the object again with the correct Issuer value
using CREATE SECURITY INTEGRATION.

**Create a security integration for Microsoft Entra ID**

> Copy code
>
> ```
> create security integration external_oauth_azure_1
>     type = external_oauth
>     enabled = true
>     external_oauth_type = azure
>     external_oauth_issuer = '<AZURE_AD_ISSUER>'
>     external_oauth_jws_keys_url = '<AZURE_AD_JWS_KEY_ENDPOINT>'
>     external_oauth_token_user_mapping_claim = 'upn'
>     external_oauth_snowflake_user_mapping_attribute = 'login_name';
> ```

**Create a security integration with audiences**

> The `external_oauth_audience_list` parameter of the security integration must match the **Application ID URI** that you specified
> while configuring Microsoft Entra ID.
>
> Copy code
>
> ```
> create security integration external_oauth_azure_2
>     type = external_oauth
>     enabled = true
>     external_oauth_type = azure
>     external_oauth_issuer = '<AZURE_AD_ISSUER>'
>     external_oauth_jws_keys_url = '<AZURE_AD_JWS_KEY_ENDPOINT>'
>     external_oauth_audience_list = ('<SNOWFLAKE_APPLICATION_ID_URI>')
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

In the context of testing OAuth while using Microsoft Entra ID as an authorization server, you must:

1. Verify that the test user exists in Microsoft Entra ID and has a password.
2. Verify that the test user exists in Snowflake with their `login_name` attribute value set to the `<AZURE_AD_USER_USERNAME>`
3. Grant the SYSADMIN role to this user.
4. Register an OAuth Client.
5. Allow the OAuth Client to make a POST request to the Microsoft Entra ID Token endpoint as follows:
   - Grant type set to Resource Owner
   - HTTP Basic Authorization header containing the clientID and secret
   - FORM data containing the user’s username & password
   - Include scopes

Here is an example for getting an access token using cURL. Note that the scope must be fully qualified, including the Microsoft Entra ID App
URI (for example, `scope=https://example.com/wergheroifvj25/session:role-any`).

Copy code

```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
  --data-urlencode "client_id=<OAUTH_CLIENT_ID>" \
  --data-urlencode "client_secret=<OAUTH_CLIENT_SECRET>" \
  --data-urlencode "username=<AZURE_AD_USER>" \
  --data-urlencode "password=<AZURE_AD_USER_PASSWORD>" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "scope=<AZURE_APP_URI+AZURE_APP_SCOPE>" \
  '<AZURE_AD_OAUTH_TOKEN_ENDPOINT>'
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
