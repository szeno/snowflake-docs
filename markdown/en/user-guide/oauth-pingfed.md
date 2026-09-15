# Configure PingFederate for External OAuth

This topic describes how to configure Snowflake as an OAuth Resource and Ping Identity PingFederate as an External OAuth authorization
server to facilitate secure, programmatic access to Snowflake data.

## Configuration procedure

The following two steps assume that your environment does not have anything configured relating to PingFederate OAuth authorization
servers, OAuth clients, scopes, and necessary metadata. These steps are also a representative example on how to configure PingFederate.

The information from the first step will be used to create a security integration in Snowflake.

If you already have a PingFederate authorization server and client configured, it is not necessary to complete all of the steps below.
Rather, skim the first step and verify that you can obtain the desired information, create scopes, assign scopes to one or more policies,
and access the metadata.

If you do not have a PingFederate OAuth authorization server and client configured, complete both steps.

Important

The steps in this topic are a representative example on how to configure PingFederate for External OAuth.

You can configure PingFederate to any desired state and use any desired OAuth flow provided that you can obtain the necessary information
for the [security integration](#label-ext-oauth-integration-pingfed) (in this topic).

Note that the following steps serve as a guide to obtain the necessary information to create the security integration in Snowflake.

Be sure to consult your internal security policies with regard to configuring an authorization server to ensure your organization meets
all necessary regulations and compliance requirements.

Step 1 is derived from the PingIdentity documentation on OAuth 2.0. For more information on how PingIdentity defines its terms, its user
interface, and options relating to Authorization Servers consult the following PingIdentity guide:

- [OAuth 2.0 Developer’s Guide](https://www.pingidentity.com/content/developer/en/resources/oauth-2-0-developers-guide.html)

### Configure PingFederate

1. Navigate to the PingFederate Server downloads page and either download or upgrade your PingFederate instance based on your
   [operating system](https://www.pingidentity.com/en/resources/downloads/pingfederate.html).
2. Use the PingFederate installation guide for your operating system. After installation, access PingFederate.
3. Create the OAuth Scopes by navigating to the **Exclusive Scopes** interface in the **OAuth Server** panel.
4. To add a Snowflake Role as a scope, add the role to the **Scope Value**. The Snowflake role must have the `session:role:`
   prefix (for example, for the Snowflake Analyst role, enter `session:role:analyst`).
5. Enter a description for the scope in the **Scope Description** box and click **Add**.
6. Navigate to the **OAuth Server** tab and create a new client. Verify the following values.

   > | Field | Value |
   > | --- | --- |
   > | NAME | A friendly name for the PingFederate OAuth Authorization server |
   > | DESCRIPTION | A friendly description for the PingFederate OAuth Authorization Server |
   > | CLIENT AUTHENTICATION | CLIENT SECRET |
   > | EXCLUSIVE SCOPES | Select the Scopes (that is, Snowflake Roles) |
   > | ALLOWED GRANT TYPES | Choose **Refresh Token** and **Resource Owner Password Credentials** |
   > | DEFAULT ACCESS TOKEN MANAGER | JSON Web Tokens |
   >
   > Expand
   >
   > Show lessSee more
7. Navigate to the **Security** tab and export the certificate. Extract the public key from the certificate for use in the following
   steps.
8. Navigate to the **Instance Configuration** tab under the **OAuth Server** tab and
   **Access Token Management | Create Access Token Management Instance**, and then:

   - Update the **ISSUER CLAIM VALUE** to the unique identifier referencing this OAuth Authorization Server.
   - Update the **AUDIENCE CLAIM VALUE** to your Snowflake account URL
     (for example, `https://<account_identifier>.snowflakecomputing.com`). For a list of possible URL formats, see
     [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url).
9. Download the PingFederate OAuth Playground add on from the
   [Developer Tools](https://www.pingidentity.com/en/resources/downloads/pingfederate.html) section. This client performs API requests.
10. Install the
    [OAuth Playground](https://www.pingidentity.com/content/dam/developer/downloads/Software/OAuth%20Grant%20Types%20using%20the%20OAuth%20PlayGround.pdf).

### Create a security integration in Snowflake

This step creates a security integration in Snowflake to ensure that Snowflake can communicate with PingIdentity
securely, validate the tokens from PingIdentity, and provide the appropriate Snowflake data access to users based on the user role
associated with the OAuth token.

Execute the following statement in the Snowflake web interface, Snowflake CLI, or SnowSQL.

Note that the value for `external_oauth_issuer` must be the unique identifier set in Step 1.8. For example, if the unique identifier
value is `27f10cde-a964-4499-a88c-0c598883e5ad`, replace `<unique_id>` with `'27f10cde-a964-4499-a88c-0c598883e5ad'`. The
unique identifier must be in single (that is, vertical) quotes.

Choose the security integration that best addresses your use case and configuration needs. For more information, see
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-external).

Important

Only account administrators (that is, users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute
this SQL command.

The security integration parameter values are case-sensitive and the values you put into the security integration must match those values
in your environment. If the case does not match, it is possible that the access token will not be validated resulting in a failed
authentication attempt.

**Create a security integration for PingFederate**

> Copy code
>
> ```
> create or replace security integration external_oauth_pf_1
>     type = external_oauth
>     enabled = true
>     external_oauth_type = ping_federate
>     external_oauth_rsa_public_key = '<BASE64_PUBLIC_KEY>'
>     external_oauth_issuer = '<unique_id>'
>     external_oauth_token_user_mapping_claim = 'username'
>     external_oauth_snowflake_user_mapping_attribute = 'login_name';
> ```
>
> This security integration uses the `external_oauth_rsa_public_key` parameter. Snowflake uses the public key value to verify the
> Signature on JWT Access Token.

**Create a security integration with audiences**

> > The `external_oauth_audience_list` parameter of the security integration must match the **Audience Claim Value** that you
> > specified while configuring PingFederate.
>
> Copy code
>
> ```
> create security integration external_oauth_pf_2
>     type = external_oauth
>     enabled=true
>     external_oauth_type = ping_federate
>     external_oauth_issuer = '<ISSUER>'
>     external_oauth_rsa_public_key = '<BASE64_PUBLIC_KEY>'
>     external_oauth_audience_list = ('<snowflake_account_url>')
>     external_oauth_token_user_mapping_claim = 'username'
>     external_oauth_snowflake_user_mapping_attribute = 'login_name';
> ```
>
> This security integration uses the `external_oauth_rsa_public_key` parameter. Snowflake uses the public key value to verify the
> Signature on JWT Access Token.

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

### Using network policies with External OAuth

Currently, network policies cannot be added to your External OAuth security integration. However, you can still implement network policies that apply broadly to the entire Snowflake account.

If your use case requires a network policy that is specific to the OAuth security integration, use [Snowflake OAuth](oauth-intro). This approach allows the Snowflake OAuth network policy to be distinct from other network policies that may apply to the Snowflake account.

For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

### Using replication with External OAuth

Snowflake supports replication and failover/failback of the External OAuth security integration from a source account to a target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).

## Testing procedure

In the context of testing OAuth while using PingFederate as an authorization server, you must:

1. Verify that the test user exists in PingIdentity and has a password.
2. Verify that the test user exists in Snowflake with their `login_name` attribute value set to the `<PING_USER_USERNAME>`
3. Grant the Analyst role to this user.
4. Register an OAuth Client.
5. Allow the OAuth Client to make a POST request to the PingFederate Token endpoint as follows:
   - Grant type set to Resource Owner.
   - HTTP Basic Authorization header containing the clientID and secret.
   - FORM data containing the user’s username and password.
   - Include any necessary scopes.

The sample command requests the Analyst role and that assumes the `session:role:analyst` is defined in
**PingFederate > OAuth Server > Exclusive Scopes**.

Use the following command to obtain an access token from Ping.

Copy code

```
curl -k 'https://10.211.55.4:9031/as/token.oauth2' \
  --data-urlencode 'client_id=<CLIENT_ID>&grant_type=password&username=<USERNAME>&password=<PASSWORD>&client_secret=<CLIENT_SECRET>&scope=session:role:analyst'
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
