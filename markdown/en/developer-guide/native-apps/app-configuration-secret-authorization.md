# Request OAuth authorization from consumers

This topic describes how to use the `SECRET_AUTHORIZATION` configuration type to
enable an OAuth authorization code grant flow in a Snowflake Native App. This is a specialized
flow for the `AUTHORIZATION_CODE` security integration type described in
[Request OAuth connection](/developer-guide/native-apps/requesting-app-specs-sec-integ).

## Overview

Some Snowflake Native Apps require consumers to authenticate with a third-party service before
the app can access external resources on their behalf. The authorization code grant flow
allows consumers to complete OAuth authentication directly, without sharing any credentials
with the app provider.

The provider configures the OAuth integration and secret in the app’s setup script.
The consumer then completes a standard OAuth consent flow to authorize the connection. After
the consumer authenticates, the app can use the resulting tokens to access external resources.

## Provider setup

### Step 1: Create a security integration

Create a security integration of type `API_AUTHENTICATION` with the authorization code
grant flow. For more information, see
[CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

Copy code

```
CREATE SECURITY INTEGRATION oauth_integration
  TYPE = API_AUTHENTICATION
  AUTH_TYPE = OAUTH2
  OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_POST
  OAUTH_CLIENT_ID = '<client_id>'
  OAUTH_CLIENT_SECRET = '<client_secret>'
  OAUTH_GRANT = 'AUTHORIZATION_CODE'
  OAUTH_TOKEN_ENDPOINT = 'https://provider.example.com/oauth2/token'
  OAUTH_AUTHORIZATION_ENDPOINT = 'https://provider.example.com/oauth2/authorize'
  ENABLED = TRUE;
```

### Step 2: Create a secret

Create a secret linked to the security integration:

Copy code

```
CREATE SECRET app_schema.oauth_secret
  TYPE = oauth2
  API_AUTHENTICATION = oauth_integration;
```

### Step 3: Create an app specification

Create an app specification for the security integration so that the consumer can review
and approve the OAuth connection details. For more information, see
[Request OAuth connection](/developer-guide/native-apps/requesting-app-specs-sec-integ).

Copy code

```
ALTER APPLICATION SET SPECIFICATION oauth_spec
  TYPE = SECURITY_INTEGRATION
  LABEL = 'OAuth connection to external provider'
  DESCRIPTION = 'Connects to external provider using Authorization Code grant'
  OAUTH_TYPE = 'AUTHORIZATION_CODE'
  OAUTH_TOKEN_ENDPOINT = 'https://provider.example.com/oauth2/token'
  OAUTH_AUTHORIZATION_ENDPOINT = 'https://provider.example.com/oauth2/authorize';
```

Approving the app specification lets the consumer approve the OAuth connection metadata, but
it doesn’t complete authentication. The consumer also needs to complete the OAuth flow described
in [Consumer authentication](#label-native-apps-secret-auth-consumer-flow), which is driven by the configuration you
create in Step 5.

### Step 4: Grant application roles access to complete the OAuth flow

Grant USAGE on the security integration and MODIFY on the secret to the application roles
that need access:

Copy code

```
GRANT USAGE ON INTEGRATION oauth_integration TO APPLICATION ROLE app_user;
GRANT MODIFY ON SECRET app_schema.oauth_secret TO APPLICATION ROLE app_user;
```

Without these grants, consumers cannot complete the OAuth flow and may hit a permission error
with no additional context.

### Step 5: Create the SECRET\_AUTHORIZATION configuration

Create a `SECRET_AUTHORIZATION` configuration that coordinates the consumer-side
OAuth flow:

Copy code

```
ALTER APPLICATION SET CONFIGURATION DEFINITION oauth_config
  TYPE = SECRET_AUTHORIZATION
  SECRET = app_schema.oauth_secret
  LABEL = 'Authenticate with external provider'
  DESCRIPTION = 'Complete the OAuth flow to connect the app to the external provider'
  APPLICATION_ROLES = (app_user);
```

The `SECRET` parameter specifies the secret that is populated with tokens when the
consumer completes the OAuth flow. You can specify the secret as `<schema_name>.<secret_name>`
(the app’s own database is implied) or as the fully qualified
`<database_name>.<schema_name>.<secret_name>`. In either form, the secret must be owned by
the application, and the application roles specified in `APPLICATION_ROLES` must have the
MODIFY privilege on the secret.

### Step 6: Use the OAuth tokens in app code

After the consumer completes the OAuth flow, the secret is populated with the access token
that the app can use in external access calls. Pass the secret to a UDF, stored procedure, or
Snowpark Container Services container through the `SECRETS` property of the object:

- For UDFs and stored procedures, see
  [Accessing the Google Translate API with OAuth](/developer-guide/external-network-access/external-network-access-examples#label-creating-using-external-access-integration-accessing-translate-api) for a
  complete example that uses `_snowflake.get_oauth_access_token` to retrieve the token.
- For Snowpark Container Services, see
  [Passing credentials to a container using Snowflake secrets](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-additional-considerations-pass-secrets) for how to pass
  the secret to a container at runtime.

## Consumer authentication

After the provider sets up the app, the consumer completes the OAuth authentication
using Snowsight, the Python Permission SDK, or SQL.

Important

Before completing the OAuth flow, the consumer must first approve the corresponding
security integration app specification. For more information, see
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

SnowsightPython Permission SDKSQL

1. Sign in to Snowsight using a role that has been granted an application
   role with access to the OAuth configuration. Completing the OAuth flow requires
   the MODIFY VALUE privilege on the configuration, which is granted to the
   application roles listed in the `APPLICATION_ROLES` parameter when the provider
   creates the configuration.

   If the security integration app specification isn’t already approved, the role
   also needs the MANAGE APPLICATION SPECIFICATIONS privilege on the account to
   approve it. For more information, see [Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).
2. Navigate to the app’s page.
3. In the application page, select the **Configurations** tab.
4. Under **External connections**, click **Review** and approve the security integration.

   Note

   The corresponding security integration app specification must be approved before
   authenticating. If it isn’t approved, the flow fails with the following error:
   `Applications can not use security integration without a corresponding approved application specification.`
5. Under **Authentication**, click **Review**, then click **Authenticate** on the OAuth
   configuration.
6. Complete the OAuth consent flow in the browser popup.
7. After successful authentication, the configuration status is automatically updated.

If the app has a Streamlit frontend, the provider can call
[request\_application\_configuration\_value()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-request-application-configuration-value)
to prompt the consumer to complete the OAuth flow directly from the app:

Copy code

```
from snowflake.permissions import request_application_configuration_value

request_application_configuration_value(config_names=['oauth_config'])
```

The SDK overlays the configuration dialog on top of the Streamlit app. When the consumer
completes the OAuth flow in the dialog, the configuration status is automatically updated.
For more information, see [request\_application\_configuration\_value()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-request-application-configuration-value).

**Step 1: Identify the secret name**

The secret name used in the OAuth flow is the fully qualified name in the format
`<database_name>.<schema_name>.<secret_name>`, where `<database_name>` is the name
under which the app is installed in the consumer account.

Providers typically document the secret name in their app’s installation guide. If it
isn’t documented, you can retrieve it from the `additionalProperties` column of the
configuration:

Copy code

```
SHOW CONFIGURATIONS IN APPLICATION example_app;

DESCRIBE CONFIGURATION oauth_config IN APPLICATION example_app;
```

The `additionalProperties` column contains a JSON string with the secret name:

Copy code

```
{
  "secret": "database_name.schema_name.secret_name"
}
```

**Step 2: Complete the OAuth flow**

Execute [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow)
with the secret name to get an authorization URL, then open the URL in a browser to
complete the OAuth consent process:

Copy code

```
SELECT SYSTEM$START_OAUTH_FLOW('database_name.schema_name.secret_name');
```

After completing the consent in the browser, execute
[SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow) in
the same session with the query string from the browser redirect URL:

Copy code

```
SELECT SYSTEM$FINISH_OAUTH_FLOW('query_string_from_redirect');
```

**Step 3: Set the configuration to configured**

After the OAuth flow is complete, set the configuration value to `configured`:

Copy code

```
ALTER APPLICATION example_app SET CONFIGURATION oauth_config VALUE = 'configured';
```

Note

The configuration value can only be set to `configured`. No other value is accepted.
Setting this value signals to the app that the OAuth flow is complete. The actual tokens
are stored in the secret; the configuration value only triggers the configuration
callbacks.

The Snowflake Native App Framework automatically verifies that the secret is populated with tokens and then triggers
the `before_configuration_change` and `after_configuration_change` callbacks.

To unset the configuration later, use:

Copy code

```
ALTER APPLICATION example_app UNSET CONFIGURATION oauth_config;
```

This also triggers the `before_configuration_change` and `after_configuration_change`
callbacks.

Warning

Unsetting the configuration does not invalidate or revoke the OAuth tokens stored in the
secret. To prevent the app from using the tokens, decline the corresponding security
integration app specification. To fully revoke the tokens at the provider level, use
the third-party provider’s token revocation process. For more information, see
[Approve app specifications](/developer-guide/native-apps/ui-consumer-app-spec).

## Token expiration and re-authentication

Snowflake uses the refresh token stored in the secret to obtain a new access token when the
current access token expires. If the refresh token itself expires or is revoked by the
third-party provider, external access calls from the app fail and the consumer needs to
re-authenticate.

Providers can prompt consumers to re-authenticate through Snowsight, the
Python Permission SDK, or SQL.

SnowsightPython Permission SDKSQL

Direct consumers to the **Configurations** tab on the app’s page. Under
**Authentication**, click **Reauthenticate** on the OAuth configuration to refresh
the tokens.

If the app has a Streamlit frontend, call
[request\_application\_configuration\_value()](/developer-guide/native-apps/requesting-permission-sdk-ref#label-request-application-configuration-value)
to overlay the configuration dialog on the Streamlit app and prompt the consumer to
re-authenticate:

Copy code

```
from snowflake.permissions import request_application_configuration_value

request_application_configuration_value(config_names=['oauth_config'])
```

Consumers can re-run [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow)
and [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow)
on the same secret to refresh the tokens. To re-trigger the
`before_configuration_change` and `after_configuration_change` callbacks,
the consumer must set the configuration value again:

Copy code

```
ALTER APPLICATION example_app SET CONFIGURATION oauth_config VALUE = 'configured';
```
