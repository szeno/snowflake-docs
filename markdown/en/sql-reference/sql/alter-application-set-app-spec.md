# ALTER APPLICATION SET SPECIFICATION

Creates or updates an [app specification](/developer-guide/native-apps/requesting-app-specs) for a Snowflake Native App.

Note

This command can only be used by a Snowflake Native App.

See also:
:   [ALTER APPLICATION](/sql-reference/sql/alter-application),
    [ALTER APPLICATION … { APPROVE | DECLINE} SPECIFICATION](/sql-reference/sql/alter-application-sequence-number), [ALTER APPLICATION DROP SPECIFICATION](/sql-reference/sql/alter-application-drop-app-spec)

## Syntax

### External access integration

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = EXTERNAL_ACCESS
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  { HOST_PORTS | PRIVATE_HOST_PORTS } = ( '<value>' [, '<value>', ... ] )
```

### Security integration (CLIENT\_CREDENTIALS)

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
    TYPE = SECURITY_INTEGRATION
    LABEL = '<string_literal>'
    DESCRIPTION = '<string_literal>'
    OAUTH_TYPE = 'CLIENT_CREDENTIALS'
    OAUTH_TOKEN_ENDPOINT = '<string_literal>'
    OAUTH_ALLOWED_SCOPES = ( '<scope>' [ , '<scope>' ... ] );
```

### Security integration (AUTHORIZATION\_CODE)

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = SECURITY_INTEGRATION
  LABEL = '<string_literal>'
  DESCRIPTION = '<string_literal>'
  OAUTH_TYPE = 'AUTHORIZATION_CODE'
  OAUTH_TOKEN_ENDPOINT = '<string_literal>'
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_ALLOWED_SCOPES = ( '<scope>' [ , '<scope>' ... ] ) ];
```

### Security integration (JWT\_BEARER)

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = SECURITY_INTEGRATION
  LABEL = '<string_literal>'
  DESCRIPTION = '<string_literal>'
  OAUTH_TYPE = 'JWT_BEARER'
  OAUTH_TOKEN_ENDPOINT = '<string_literal>'
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_ALLOWED_SCOPES = ( '<scope>' [ , '<scope>' ... ] ) ];
```

### Listing

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = LISTING
  LABEL = '<string_literal>'
  DESCRIPTION = '<string_literal>'
  TARGET_ACCOUNTS = '<account_list>'
  LISTING = <listing_name>
  [ AUTO_FULFILLMENT_REFRESH_SCHEDULE = '<schedule>' ]
```

### Inter-App Communication

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = CONNECTION
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  SERVER_APPLICATION = <server_app>
  SERVER_APPLICATION_ROLES = ( <app_role1> [ , <app_role2> ... ] );
```

### Setting

Copy code

```
ALTER APPLICATION SET SPECIFICATION <app_spec_name>
  TYPE = SETTING
  LABEL = '<label>'
  DESCRIPTION = '<description>'
  SETTING = <setting_name>
  [ VALUE = '<value>' ]
```

## General parameters

`app_spec_name`
:   Identifier for the [app specification](/developer-guide/native-apps/requesting-app-specs).

`TYPE = \{EXTERNAL_ACCESS | SECURITY_INTEGRATION | LISTING | CONNECTION | SETTING}\}`
:   Specifies the type of app specification. Supported values are:

    - [EXTERNAL\_ACCESS](/developer-guide/external-network-access/creating-using-external-network-access)
    - [SECURITY\_INTEGRATION](/sql-reference/sql/create-security-integration-api-auth)
    - [LISTING](/developer-guide/native-apps/requesting-app-specs-listing)
    - [CONNECTION](/developer-guide/native-apps/inter-app-communication)
    - [SETTING](/developer-guide/native-apps/requesting-app-specs-setting)

    Important

    The type of an app specification cannot be changed once it has been created. Attempting to
    alter the type will result in an error.

`LABEL = 'label'`
:   Specifies a label for the app specification. This label is the name of the
    app specification that is visible to the consumer. Each app specification must
    have a unique label.

    Note

    Changing only the label will not trigger a new approval request. To require consumer
    approval, you must also change the app specification definition (such as HOST\_PORTS,
    OAUTH\_TOKEN\_ENDPOINT, or TARGET\_ACCOUNTS).

`DESCRIPTION = 'description'`
:   Specifies a description of the app specification. Snowflake recommends
    including information about the app specification type and why it is
    required by the app.

    Note

    Changing only the description will not trigger a new approval request. To require consumer
    approval, you must also change the app specification definition (such as HOST\_PORTS,
    OAUTH\_TOKEN\_ENDPOINT, or TARGET\_ACCOUNTS).

## External access integration parameters

`{HOST_PORTS | PRIVATE_HOST_PORTS} = ( 'value' [ , 'value', ... ] )`
:   Specifies a list of host ports or private host ports that the app can connect to.
    These ports are used by external access integrations.

## Security integration parameters - CLIENT\_CREDENTIALS

`OAUTH_TYPE = 'CLIENT_CREDENTIALS'`
:   Specifies the type of security integration for external API Authentication. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_TOKEN_ENDPOINT = 'string_literal'`
:   Specifies the token endpoint used by the client to obtain an access token by presenting its authorization
    grant or refresh token. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_ALLOWED_SCOPES = ( 'scope' [ , 'scope' ... ] )`
:   Specifies a comma-separated list of scopes, with single quotes surrounding each scope, to use when making
    a request from the OAuth by a role with USAGE on the integration during the OAuth client credentials
    flow. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_ACCESS_TOKEN_VALIDITY = integer`
:   Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

## Security integration parameters - AUTHORIZATION\_CODE

`OAUTH_TYPE = 'AUTHORIZATION_CODE'`
:   Specifies the type of security integration for external API Authentication. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_TOKEN_ENDPOINT = 'string_literal'`
:   Specifies the token endpoint used by the client to obtain an access token by presenting its authorization
    grant or refresh token. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_AUTHORIZATION_ENDPOINT = 'string_literal'`
:   Specifies the URL for authenticating to the external service. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_ACCESS_TOKEN_VALIDITY = integer`
:   Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_REFRESH_TOKEN_VALIDITY = integer`
:   Specifies the default lifetime of the OAuth refresh token (in seconds) issued by an OAuth server. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

## Security integration parameters - JWT\_BEARER

`OAUTH_TYPE = 'JWT_BEARER'`
:   Specifies the type of security integration for external API Authentication. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_TOKEN_ENDPOINT = 'string_literal'`
:   Specifies the token endpoint used by the client to obtain an access token by presenting its authorization
    grant or refresh token. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_AUTHORIZATION_ENDPOINT = 'string_literal'`
:   Specifies the URL for authenticating to the external service. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

`OAUTH_REFRESH_TOKEN_VALIDITY = integer`
:   Specifies the default lifetime of the OAuth refresh token (in seconds) issued by an OAuth server. See
    [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) for more information.

## Listing parameters

`TARGET_ACCOUNTS = 'account_list'`
:   Specifies a single-quoted string of target accounts, separated by commas, with
    no spaces. Each account must be specified in the format
    `OrgName.AccountName`; for example:
    `'ProviderOrg.ProviderAccount,PartnerOrg.PartnerAccount'`. When the
    specification is approved, these accounts are added to the listing. When
    declined, all accounts are removed from the listing.

`LISTING = listing_name`
:   Specifies the identifier of the external listing created by the app. The listing must already exist
    and must have been created by the app with a share attached. After the listing is set in an app specification,
    the listing name cannot be changed.

`AUTO_FULFILLMENT_REFRESH_SCHEDULE = 'schedule'`
:   Optional. Specifies the refresh schedule for cross-region data sharing. This parameter is required
    when sharing data across regions. The value can be specified in two formats:

    - `num MINUTE`: Number of minutes, with a minimum of 10 minutes and
      a maximum of 11,520 minutes (eight days).
    - `USING CRON expression time_zone`: Cron expression with time zone
      for the refresh.

## Inter-app communication parameters

`SERVER_APPLICATION = server_app`
:   The name of the server application to be connected to. The following operations
    are not supported:

    - Updating this setting for an existing specification.
    - More than one specification targeting the same server application.

`SERVER_APPLICATION_ROLES = ( app_role1 [ , app_role2 ... ] )`
:   Specifies a comma-separated list of application roles in the server application
    to be granted to this application.

## Setting parameters

`SETTING = setting_name`
:   Specifies the name of the account-level setting to request. The value can’t be
    changed after the app specification is created. Supported values are:

    - `ENABLE_UNLOAD_TO_INTERNAL_STAGES`: When approved, allows the app to copy
      data to internal stages contained within the application, even when the
      `PREVENT_UNLOAD_TO_INTERNAL_STAGES` account parameter is enabled.

`VALUE = 'value'`
:   Specifies the value for the setting. For boolean settings, this parameter
    may be omitted (the value defaults to `'true'`), or if specified, must be
    `'true'`. For non-boolean settings, this parameter is required.

## Usage notes

- To use this command, providers must ensure that the manifest file of the app
  uses `manifest_version: 2`.

## Examples

Create an app specification for external access:

Copy code

```
ALTER APPLICATION SET SPECIFICATION eai_spec
  TYPE = EXTERNAL_ACCESS
  LABEL = 'External API Access'
  DESCRIPTION = 'Connect to external weather API'
  HOST_PORTS = ('api.weather.com:443', 'api.openweather.org:443');
```

Create an app specification for OAuth security integration:

Copy code

```
ALTER APPLICATION SET SPECIFICATION oauth_spec
  TYPE = SECURITY_INTEGRATION
  LABEL = 'OAuth Integration'
  DESCRIPTION = 'Connect to Microsoft Graph API'
  OAUTH_TYPE = 'CLIENT_CREDENTIALS'
  OAUTH_TOKEN_ENDPOINT = 'https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token'
  OAUTH_ALLOWED_SCOPES = ('https://graph.microsoft.com/.default');
```

Create an app specification for data sharing through a listing:

Copy code

```
ALTER APPLICATION SET SPECIFICATION shareback_spec
  TYPE = LISTING
  LABEL = 'Telemetry Data Sharing'
  DESCRIPTION = 'Share telemetry and usage data with provider'
  TARGET_ACCOUNTS = 'ProviderOrg.ProviderAccount,PartnerOrg.PartnerAccount'
  LISTING = telemetry_listing
  AUTO_FULFILLMENT_REFRESH_SCHEDULE = '720 MINUTE';
```

Create an app specification to request a behavioral setting:

Copy code

```
ALTER APPLICATION SET SPECIFICATION unload_setting_spec
  TYPE = SETTING
  LABEL = 'Write to internal stages'
  DESCRIPTION = 'Allows the app to copy data to internal stages'
  SETTING = ENABLE_UNLOAD_TO_INTERNAL_STAGES;
```
