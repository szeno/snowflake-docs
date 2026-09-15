# Authenticating SCIM API requests

Snowflake authenticates SCIM API requests from identity providers through a Bearer token in the Authorization header of HTTP
requests. Snowflake accepts different types of tokens in the header.

This topic describes how to configure Snowflake to authenticate with the following types of tokens:

- [External OAuth tokens](/user-guide/oauth-ext-overview)
- [Programmatic access tokens](/user-guide/programmatic-access-tokens)
- [SCIM access tokens](#label-scim-auth-long-lived-token) (legacy)

## Configuration workflow

Except when using a [SCIM access token](#label-scim-auth-long-lived-token), configuring Snowflake to accept tokens in a
SCIM request consists of the following steps:

1. [Create or use an existing SCIM security integration](#label-scim-auth-scim-integration).
2. [Create a service user](#label-scim-auth-service-user) for the SCIM identity provider that is provisioning Snowflake users.
3. [Create a role](#label-scim-auth-create-role) and grant it to the new service user.
4. [Grant the new role the USAGE privilege on the SCIM integration](#label-scim-auth-usage).
5. [Set up the Snowflake authentication method](#label-scim-auth-method).

### Create or use an existing SCIM security integration

A SCIM security integration creates the interface between Snowflake and the identity provider (IdP) that sends SCIM requests to
provision users. If you don’t already have one, you need to run a
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-scim) command to create the security integration of
type `SCIM`.

For more information about setting up the interface between Snowflake and the SCIM IdP, see [SCIM security integrations](/user-guide/scim-security-integrations).

### Create a service user for the SCIM identity provider

The SCIM IdP is a service-to-service application, so it must correspond to a Snowflake service user; that is, a user object of type
`SERVICE`. Use the [CREATE USER](/sql-reference/sql/create-user) command to create a service user for the SCIM IdP.

- If you are authenticating with programmatic access tokens (PATs), the user has no special requirements except that it must be of type `SERVICE`.
- If you are authenticating with External OAuth, you must configure the service user as described in the following section.

When authenticating with External OAuth, the SCIM identity provider (IdP) acts as a client application that authenticates to Snowflake
without human intervention. Snowflake maps a claim in the OAuth token to a property of the Snowflake service user. When you create the
service user, set the property that you plan to use for mapping (either `LOGIN_NAME` or `EMAIL_ADDRESS`) to the value that
the authorization server includes in the token.

For example, if the authorization server identifies the SCIM IdP by a GUID in the token, set the `LOGIN_NAME` of the service user
to that GUID:

Copy code

```
CREATE USER scim_idp_user
  LOGIN_NAME = '6B29FC40-CA47-1067-B31D-00DD01062DA'
  TYPE = SERVICE;
```

You specify which token claim contains this value and which Snowflake user property to match it against when you
[set up the External OAuth integration](#label-scim-auth-external-oauth).

### Create a new role for the service user

Create an access control role and grant it to the service user you created for the SCIM IdP (in the
[previous step](#label-scim-auth-service-user)). You also need to make this role the default role of the service user. This process
consists of the following steps:

1. Run a [CREATE ROLE](/sql-reference/sql/create-role) command to create the role for the service user.
2. Run a [GRANT ROLE](/sql-reference/sql/grant-role) command to grant the new role to the service user.
3. Run an [ALTER USER](/sql-reference/sql/alter-user) command to set the role as the user’s default role.

If the service user you created is `scim_idp_user` and you want the new role to be `scim_role`, run the following commands:

Copy code

```
CREATE ROLE scim_role;

GRANT ROLE scim_role TO USER scim_idp_user;

ALTER USER scim_idp_user SET DEFAULT_ROLE = scim_role;
```

### Grant the USAGE privilege on the SCIM integration

Grant the USAGE privilege on the SCIM integration to the service user’s role. You created this role in the
[previous step](#label-scim-auth-create-role). Suppose you have the following implementation:

- Your SCIM security integration is `okta_provisioning`.
- The role that you created for the service user is `scim_role`.

Given this implementation, run the following command:

Copy code

```
GRANT USAGE ON INTEGRATION okta_provisioning TO ROLE scim_role;
```

### Set up your authentication method

The setup for your authentication method depends on which method you are using. Choose the method that best fits your security requirements.

- [Set up programmatic access tokens](#set-up-programmatic-access-tokens)
- [Set up External OAuth](#set-up-external-oauth)

#### Set up programmatic access tokens

Generate a PAT for the [service user that you created](#label-scim-auth-service-user) for the SCIM IdP. When generating
the PAT, you must set the ROLE\_RESTRICTION parameter to the name of the [role that you created](#label-scim-auth-create-role) for the
service user.

For example, to generate a PAT for the user, run the following command:

Copy code

```
ALTER USER IF EXISTS scim_idp_user
  ADD PROGRAMMATIC ACCESS TOKEN scim_pat_token
    ROLE_RESTRICTION = 'scim_role';
```

For more information about managing PATs, including how to rotate them, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

#### Set up External OAuth

You can configure your SCIM identity provider to authenticate with OAuth tokens issued by a third-party authorization server. In this
method, the SCIM identity provider (IdP) acts as an OAuth client that obtains tokens from an authorization server and
includes them in requests sent to Snowflake’s SCIM endpoints.

In this framework, the third-party IdP is the authorization server, the SCIM IdP is the client, and Snowflake is the resource
server. This implementation consists of the following steps:

1. Outside of Snowflake, establish a relationship between the IdP that sends SCIM requests (the client) and the IdP that is issuing
   OAuth tokens (the authorization server). Most likely, the SCIM IdP uses a client credentials flow to obtain the tokens.
2. Establish a relationship between Snowflake and the authorization server, as described in the following section.

External OAuth is the Snowflake authentication method that lets a client application like the SCIM IdP authenticate with OAuth
tokens obtained from a third-party authorization server.

An External OAuth security integration creates the interface between Snowflake and the IdP that issues OAuth tokens. When you create
this integration, ensure that you configure the following parameters:

- `EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM` parameter: Specifies the token claim (or claims) that Snowflake uses to identify the
  caller. Set this to the claim in your OAuth token whose value matches the `LOGIN_NAME` or `EMAIL_ADDRESS` of the SCIM
  service user. You can specify multiple claims; Snowflake tries each one in order and uses the first match.
- `EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE` parameter: Specifies which Snowflake user property to match the token claim
  against. Set this to `LOGIN_NAME` or `EMAIL_ADDRESS`.

For example, the following External OAuth security integration uses the `sub` claim in the OAuth token to identify the caller,
and matches it against the `LOGIN_NAME` of the Snowflake service user:

Copy code

```
CREATE SECURITY INTEGRATION external_oauth_for_scim
  TYPE = EXTERNAL_OAUTH
  ENABLED = TRUE
  EXTERNAL_OAUTH_TYPE = OKTA
  EXTERNAL_OAUTH_ISSUER = '<issuer_url>'
  EXTERNAL_OAUTH_JWS_KEYS_URL = '<jws_keys_url>'
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'sub'
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name';
```

In this example, the `sub` claim in the OAuth token must contain the same value as the `LOGIN_NAME` of the
[service user](#label-scim-auth-service-user) you created for the SCIM IdP.

For more information about setting up External OAuth, including other provider types and parameters, see
[External OAuth overview](/user-guide/oauth-ext-overview).

## Send SCIM requests

After configuring authentication, you can send SCIM requests to Snowflake. There are two base URL formats:

Copy code

```
https://<account_identifier>.snowflakecomputing.com/scim/v2/<integration_uuid>/
```

Copy code

```
https://<account_identifier>.snowflakecomputing.com/scim/v2/
```

If you are authenticating with **External OAuth** or **programmatic access tokens**, use the UUID-based URL. If your
account has only one enabled SCIM security integration, you can omit the UUID and use the shorter base URL.

If you are authenticating with a [SCIM access token](#label-scim-auth-long-lived-token), use the shorter base
URL.

To obtain the UUID of your SCIM security integration, run a [DESCRIBE SECURITY INTEGRATION](/sql-reference/sql/desc-integration)
command and copy the value of the `SCIM_ENDPOINT_ID` property. For example:

Copy code

```
DESC SECURITY INTEGRATION okta_provisioning;
```

For the list of available SCIM endpoints, see [SCIM API requests](/user-guide/scim-api-references).

## Authenticating SCIM requests with a SCIM access token (legacy)

Snowflake provides a long-lived token that is unique to SCIM API requests. This token is valid for six months.

To obtain a SCIM access token to authenticate SCIM API requests, run the [SYSTEM$GENERATE\_SCIM\_ACCESS\_TOKEN](/sql-reference/functions/system_generate_scim_access_token)
function. For example, if your security integration is named `OKTA_PROVISIONING`, run:

Copy code

```
SELECT SYSTEM$GENERATE_SCIM_ACCESS_TOKEN('OKTA_PROVISIONING');
```

When your token expires, you can generate a new access token by running the SYSTEM$GENERATE\_SCIM\_ACCESS\_TOKEN function again.

To invalidate an existing access token for a SCIM integration, run a [DROP INTEGRATION](/sql-reference/sql/drop-integration) statement.
To continue using SCIM with Snowflake, recreate the SCIM integration with a [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-scim) statement and generate a new access token using [SYSTEM$GENERATE\_SCIM\_ACCESS\_TOKEN](/sql-reference/functions/system_generate_scim_access_token).
