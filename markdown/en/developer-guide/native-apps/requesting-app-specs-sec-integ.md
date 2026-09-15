# Request OAuth connection

This topic describes how to configure a Snowflake Native App to use app specifications to request
access to security integrations in the consumer account. Security integrations allow
an app to connect to third-party authentication providers such as OAuth.

## Access third-party authentication providers from an app

To implement a third-party authentication service, Snowflake provides security integrations. A
security integration allows an app to connect to a third-party authentication service such as OAuth.

> Note
>
> Snowflake Native Apps only support security integrations of type `API_AUTHENTICATION`. For more
> information, see [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

## App specification workflow for security integrations

The general workflow for configuring an app to use a security integration is as follows:

1. Providers configure [automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs) for the app.
   This grants the app privileges to create a security integration.

   > Note
   >
   > App specifications require that `manifest_version: 2` be set in the manifest file.
2. Providers add the
   [CREATE SECURITY INTEGRATION privilege](#label-native-apps-app-spec-add-si-priv) to the
   manifest file.
3. Providers add SQL statements to the setup script to create the following objects as required:

   - [Security integration](/sql-reference/sql/create-security-integration)
   - [App specification](/sql-reference/sql/alter-application-set-app-spec)

   Providers can add these commands directly in the setup script, which causes these objects to
   be created when the app is installed. Alternatively, these commands can be added to a stored
   procedure that is called at runtime to create these objects.
4. Consumers approve information related to OAuth integration when configuring the app. For more
   information on how consumers view and approve app specifications, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## App specification definition for security integrations

For a security integration, the [app specification definition](/developer-guide/native-apps/requesting-app-specs#label-native-apps-app-spec-definition) contains the properties required to connect
to a third-party provider. For OAuth, the app specification definition depends on the
OAuth type. The following table lists the app specification definition for each type:

| Security integration type | Values defined in the app specification |
| --- | --- |
| `CLIENT_CREDENTIALS` | - `OAUTH_TOKEN_ENDPOINT` (required) - `OAUTH_ALLOWED_SCOPES` (required) |
| `AUTHORIZATION_CODE` | - `OAUTH_TOKEN_ENDPOINT` (required) - `OAUTH_AUTHORIZATION_ENDPOINT` (optional) - `OAUTH_ALLOWED_SCOPES` (optional) |
| `JWT_BEARER` | - `OAUTH_TOKEN_ENDPOINT` (required) - `OAUTH_AUTHORIZATION_ENDPOINT` (optional) - `OAUTH_ALLOWED_SCOPES` (optional) |

Expand

Show lessSee more

## Set the version of the manifest file

To enable automated granting of privileges for an app, set the version at the beginning of the
manifest file as shown in the following example:

Copy code

```
manifest_version: 2
```

## Add the CREATE SECURITY INTEGRATION privilege to the manifest file

- To allow an app to create a security integration, add the
  `CREATE SECURITY INTEGRATION` privilege
  to the manifest file, as shown in the following example:

  Copy code

  ```
  manifest_version: 2
  ...
  privileges:
    - CREATE SECURITY INTEGRATION:
     description: "Allows the app to create security integrations to access external auth providers"
  ...
  ```

If you set the `manifest_version` to 2 in the manifest file, Snowflake automatically grants
the CREATE SECURITY INTEGRATION privilege to the app during installation or upgrade.

## Add a security integration to the setup script

Security integrations allow an app to connect to a third-party authentication service
like OAuth. To create a security integration for an app, add the
[CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) command to the
setup script as shown in the following example:

Copy code

```
CREATE SECURITY INTEGRATION external_oauth_provider
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = OAUTH2
  OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
  OAUTH_CLIENT_ID = 'YOUR_CLIENT_ID'
  OAUTH_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
  OAUTH_GRANT = 'CLIENT_CREDENTIALS'
  OAUTH_TOKEN_ENDPOINT = 'https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token'
  OAUTH_ALLOWED_SCOPES = ('https://graph.microsoft.com/.default')
  ENABLED = TRUE;
```

This example shows how to create a security integration to connect to Microsoft Graph using
OAuth with client credentials. For other supported methods of connecting to an OAuth provider, see
[CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

## Create an app specification for a security integration

The following example shows how to create an app specification for a security integration
using the CLIENT\_CREDENTIALS OAuth type:

Copy code

```
ALTER APPLICATION SET SPECIFICATION oauth_app_spec
  TYPE = SECURITY_INTEGRATION
  LABEL = 'Connection to an external OAuth provider'
  DESCRIPTION = 'Integrates an external identity provider in the app'
  OAUTH_TYPE = 'CLIENT_CREDENTIALS'
  OAUTH_TOKEN_ENDPOINT = 'https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token'
  OAUTH_ALLOWED_SCOPES = ('https://graph.microsoft.com/.default');
```

Note

The values you provide when creating the app specification must be the same as those
you use when [creating the security integration](#label-native-apps-app-spec-add-si)
in the setup script.

For information on using other OAuth types, see [ALTER APPLICATION SET SPECIFICATION](/sql-reference/sql/alter-application-set-app-spec).

## Authorization code grant flow

For security integrations that use the `AUTHORIZATION_CODE` grant type, you can use the
`SECRET_AUTHORIZATION` application configuration to enable consumers to complete the OAuth
consent flow directly. This allows the app to obtain tokens on behalf of the consumer without
the consumer sharing any credentials with the app provider.

For the full setup and consumer authentication steps, see
[Request OAuth authorization from consumers](/developer-guide/native-apps/app-configuration-secret-authorization).

## Approve the app specification in the consumer account

After the provider configures the app to create the security integration and app specification, consumers can view the app specification and approve or decline it as necessary when configuring the app. For more information, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).
