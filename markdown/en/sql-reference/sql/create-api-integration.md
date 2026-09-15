# CREATE API INTEGRATION

Creates a new API integration object in the account or replaces an existing API integration.

An API integration object stores information about a service reached via HTTPS API, including information about some of the following:

> - A cloud platform provider (such as Amazon AWS).
> - A Git repository API.
> - An external Model Context Protocol (MCP) server, used by
>   [MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors) to expose
>   third-party tools to a Cortex Agent.
> - The type of service (such as when a cloud platform provider offers more than one type of proxy service).
> - The identifier and access credentials for the external service that has sufficient privileges to use the
>   service. For example, on AWS, the role’s ARN (Amazon resource name) serves as the identifier and access
>   credentials.
>
>   When this user is granted appropriate privileges, Snowflake can use this user to access resources. For example, this might be an instance
>   of the cloud platform’s native HTTPS proxy service, for example, an instance of an Amazon API Gateway.
> - An API integration object also specifies allowed (and optionally blocked) endpoints and resources on those services.

See also:
:   [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [Writing external functions](/sql-reference/external-functions) ,
    [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function)

## Syntax

The syntax is different for each external API.

### For Amazon API Gateway

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = { aws_api_gateway | aws_private_api_gateway | aws_gov_api_gateway | aws_gov_private_api_gateway }
  API_AWS_ROLE_ARN = '<iam_role>'
  [ API_KEY = '<api_key>' ]
  API_ALLOWED_PREFIXES = ('<...>')
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Note that `aws_api_gateway` or `aws_private_api_gateway` or `aws_gov_api_gateway` or `aws_gov_private_api_gateway` should
not be in quotation marks.

### For Azure API Management

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = azure_api_management
  AZURE_TENANT_ID = '<tenant_id>'
  AZURE_AD_APPLICATION_ID = '<azure_application_id>'
  [ API_KEY = '<api_key>' ]
  API_ALLOWED_PREFIXES = ( '<...>' )
  [ API_BLOCKED_PREFIXES = ( '<...>' ) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Note that `azure_api_management` should not be in quotation marks.

### For Google Cloud API Gateway

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = google_api_gateway
  GOOGLE_AUDIENCE = '<google_audience_claim>'
  API_ALLOWED_PREFIXES = ( '<...>' )
  [ API_BLOCKED_PREFIXES = ( '<...>' ) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Note that `google_api_gateway` should not be in quotation marks.

### For Git repository

When integrating with a Git repository, you can use a personal access token or OAuth.

TokenGitHub appOAuth2 parametersPrivate Link

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('<...>')
  [ API_BLOCKED_PREFIXES = ('<...>') ]
  [ ALLOWED_AUTHENTICATION_SECRETS = ( { <secret_name> [, <secret_name>, ... ] } ) | all | none ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/<...>')
  [ API_BLOCKED_PREFIXES = ('<...>') ]
  API_USER_AUTHENTICATION = (
    TYPE = SNOWFLAKE_GITHUB_APP
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://example.com/<...>')
  [ API_BLOCKED_PREFIXES = ('<...>') ]
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    {oauth_parameters}
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('<...>')
  [ API_BLOCKED_PREFIXES = ('<...>') ]
  [ ALLOWED_AUTHENTICATION_SECRETS = ( { <secret_name> [, <secret_name>, ... ] } ) | all | none ]
  USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
  [ TLS_TRUSTED_CERTIFICATES = ( { <secret_name> [, <secret_name>, ... ] } ) ]
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Note that `git_https_api` should not be in quotation marks.

### For external MCP server

When integrating with an external Model Context Protocol (MCP) server, use either standard
OAuth 2.0 or OAuth Dynamic Client Registration (DCR). For end-to-end setup, see
[MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).

OAuth 2.0Dynamic Client Registration

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('<...>')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = '<client_id>'
    OAUTH_CLIENT_SECRET = '<client_secret>'
    OAUTH_TOKEN_ENDPOINT = '<token_endpoint_url>'
    OAUTH_AUTHORIZATION_ENDPOINT = '<authorization_endpoint_url>'
    [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST | NONE } ]
    [ OAUTH_DISCOVERY_URL = '<discovery_url>' ]
    [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Copy code

```
CREATE [ OR REPLACE ] API INTEGRATION [ IF NOT EXISTS ] <integration_name>
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('<...>')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH_DYNAMIC_CLIENT
    OAUTH_RESOURCE_URL = '<resource_url>'
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
  ;
```

Note that `external_mcp` should not be in quotation marks.

## Required parameters

### For Amazon API Gateway

`integration_name`
:   Specifies the name of the API integration. This name follows the rules for [Object identifiers](/sql-reference/identifiers).
    The name must be unique among API integrations in your account.

`API_PROVIDER = { aws_api_gateway | aws_private_api_gateway | aws_gov_api_gateway | aws_gov_private_api_gateway }`
:   Specifies the HTTPS proxy service type. Valid values are:

    > - `aws_api_gateway`: for Amazon API Gateway using regional endpoints.
    > - `aws_private_api_gateway`: for Amazon API Gateway using private endpoints.
    > - `aws_gov_api_gateway`: for Amazon API Gateway using U.S. government GovCloud endpoints.
    > - `aws_gov_private_api_gateway`: for Amazon API Gateway using U.S. government GovCloud endpoints that are also private
    >   endpoints.

`API_AWS_ROLE_ARN = iam_role`
:   > For Amazon AWS, this is the ARN (Amazon resource name) of a cloud platform role.

`API_ALLOWED_PREFIXES = (...)`
:   Explicitly limits external functions that use the integration to reference one or more HTTPS proxy
    service endpoints (such as Amazon API Gateway) and resources within those proxies. Supports a comma-separated
    list of URLs, which are treated as prefixes (for details, see below).

    Each URL in `API_ALLOWED_PREFIXES = (...)` is treated as a prefix. For example, if you specify:

    `https://xyz.amazonaws.com/production/`

    that means all resources under

    `https://xyz.amazonaws.com/production/`

    are allowed. For example the following is allowed:

    `https://xyz.amazonaws.com/production/ml1`

    To maximize security, you should restrict allowed locations as narrowly as practical.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any external function that relies
    on it will not work.

    The value is case-insensitive.

    The default is `TRUE`.

### For Azure API Management Service

`integration_name`
:   Specifies the name of the API integration. This name follows the rules for [Object identifiers](/sql-reference/identifiers).
    The name should be unique among API integrations in your account.

`API_PROVIDER = azure_api_management`
:   Specifies that this integration is used with Azure API Management services. Do not use quotation marks around `azure_api_management`.

`AZURE_TENANT_ID = tenant_id`
:   Specifies the ID for your Office 365 tenant that all Azure API Management instances belong to. An API integration
    can authenticate to only one tenant, and so the allowed and blocked locations must refer to API Management
    instances that all belong to this tenant.

    To find your tenant ID, sign in to the Azure portal and select **Azure Active Directory** » **Properties**.
    The tenant ID is displayed in the **Tenant ID** field.

`AZURE_AD_APPLICATION_ID = azure_application_id`
:   The “Application (client) id” of the Azure AD (Active Directory) app for your remote service.
    If you followed the instructions in [Creating external functions on Microsoft Azure](/sql-reference/external-functions-creating-azure),
    then this is the `Azure Function App AD Application ID` that you recorded in the worksheet in those instructions.

`API_ALLOWED_PREFIXES = (...)`
:   Explicitly limits external functions that use the integration to reference one or more HTTPS proxy
    service endpoints (such as Azure API Management services) and resources within those proxies. Supports a comma-separated
    list of URLs, which are treated as prefixes (for details, see below).

    Each URL in `API_ALLOWED_PREFIXES = (...)` is treated as a prefix. For example, if you specify:

    `https://my-external-function-demo.azure-api.net/my-function-app-name`

    that means all resources under

    `https://my-external-function-demo.azure-api.net/my-function-app-name`

    are allowed. For example the following is allowed:

    `https://my-external-function-demo.azure-api.net/my-function-app-name/my-http-trigger-function`

    To maximize security, you should restrict allowed locations as narrowly as practical.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any external function that relies
    on it will not work.

    The value is case-insensitive.

    The default is `TRUE`.

### For Google Cloud API Gateway

`integration_name`
:   Specifies the name of the API integration. This name follows the rules for [Object identifiers](/sql-reference/identifiers).
    The name should be unique among API integrations in your account.

`API_PROVIDER = google_api_gateway`
:   Specifies that this integration is used with Google Cloud. The only valid value for this purpose is `google_api_gateway`.
    The value must not be in quotation marks.

`GOOGLE_AUDIENCE = google_audience`
:   This is used as the audience claim when generating the JWT (JSON Web Token) to authenticate to the Google API Gateway.
    For more information about authenticating with Google, please see the Google service account
    [authentication documentation.](https://cloud.google.com/api-gateway/docs/authenticate-service-account#configure_auth)

`API_ALLOWED_PREFIXES = (...)`
:   Explicitly limits external functions that use the integration to reference one or more HTTPS proxy
    service endpoints (such as Google Cloud API Gateways) and resources within those proxies. Supports a comma-separated
    list of URLs, which are treated as prefixes (for details, see below).

    Each URL in `API_ALLOWED_PREFIXES = (...)` is treated as a prefix. For example, if you specify:

    `https://my-external-function-demo.uc.gateway.dev/x`

    that means all resources under

    `https://my-external-function-demo.uc.gateway.dev/x`

    are allowed. For example the following is allowed:

    `https://my-external-function-demo.uc.gateway.dev/x/y`

    To maximize security, you should restrict allowed locations as narrowly as practical.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this API integration is enabled or disabled. If the API integration is disabled, any external function that relies
    on it will not work.

    The value is case-insensitive.

    The default is `TRUE`.

### For Git repository

For an example, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

`integration_name`
:   Specifies the name of the API integration. This name follows the rules for [Object identifiers](/sql-reference/identifiers).
    The name must be unique among API integrations in your account.

`API_PROVIDER = git_https_api`
:   Specifies that this integration is used with [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository) to create an
    [integration with a remote Git repository](/developer-guide/git/git-overview). The only valid value for this purpose is
    `git_https_api`. The value must not be in quotation marks.

`API_ALLOWED_PREFIXES = (...)`
:   Explicitly limits requests that use the integration to reference one or more HTTPS endpoints and resources beneath those
    endpoints. Supports a comma-separated list of URLs, which are treated as prefixes.

    In most cases, Snowflake supports any HTTPS Git repository URL. For example, you can specify a custom URL to a corporate Git server
    within your own domain.

    `https://example.com/my-repo`

    Each URL in `API_ALLOWED_PREFIXES = (...)` is treated as a prefix. For example, you can specify the following:

    `https://example.com/my-account`

    With this prefix, all resources under that URL are allowed. For example, the following is allowed:

    `https://example.com/my-account/myproject`

    To maximize security, you should restrict allowed locations as narrowly as practical.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this API integration is enabled or disabled. If the API integration is disabled, the Git repository will not be accessible.

    The value is case-insensitive.

    The default is `TRUE`.

### For external MCP server

For end-to-end setup, see [MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).

`integration_name`
:   Specifies the name of the API integration. This name follows the rules for [Object identifiers](/sql-reference/identifiers).
    The name must be unique among API integrations in your account.

`API_PROVIDER = external_mcp`
:   Specifies that this integration connects to an external Model Context Protocol (MCP) server,
    used by [MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors) to expose third-party
    tools to a Cortex Agent. The only valid value for this purpose is `external_mcp`. The
    value must not be in quotation marks.

`API_ALLOWED_PREFIXES = (...)`
:   Explicitly limits requests that use the integration to reference one or more HTTPS endpoints
    beneath the listed URL prefixes. Supports a comma-separated list of URLs, which are treated as
    prefixes. Set this to the base URL of the external MCP server, for example
    `'https://mcp.atlassian.com/v1/mcp'`.

    To maximize security, restrict allowed locations as narrowly as practical.

`API_USER_AUTHENTICATION = (...)`
:   Specifies the OAuth settings used to connect to the external MCP server. EXTERNAL\_MCP only
    supports OAuth, so this parameter is required. For the full list of sub-parameters under
    `TYPE = OAUTH2` and `TYPE = OAUTH_DYNAMIC_CLIENT`, see
    [For external MCP server](#label-create-api-integration-external-mcp-optional-parameters) below.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether this API integration is enabled or disabled. If the API integration is
    disabled, the external MCP server is not accessible to Cortex Agents.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

### For all integrations

`API_KEY = api_key`
:   The [API key](/sql-reference/external-functions-security#label-external-functions-api-key) (also called a “subscription key”).

`API_BLOCKED_PREFIXES = (...)`
:   Lists the endpoints and resources in the HTTPS proxy service that are not allowed to be called from Snowflake.

    The possible values for locations follow the same rules as for API\_ALLOWED\_PREFIXES above.

    API\_BLOCKED\_PREFIXES takes precedence over API\_ALLOWED\_PREFIXES. If a prefix matches both, then it is blocked.
    In other words, Snowflake allows all values that match API\_ALLOWED\_PREFIXES except values that also
    match API\_BLOCKED\_PREFIXES.

    If a value is outside API\_ALLOWED\_PREFIXES, you do not need to explicitly block it.

`COMMENT = 'string_literal'`
:   A description of the integration.

### For Git repository

In addition to parameters for all integrations, use the following parameters when you’re using the integration
to connect to a remote Git repository by setting the integration’s API\_PROVIDER parameter to `git_https_api`.

`ALLOWED_AUTHENTICATION_SECRETS = ( secret_name [, secret_name ... ] | all | none )`
:   Specifies the secrets that UDF or procedure handler code can use when accessing the Git repository at the API\_ALLOWED\_PREFIXES value. You
    specify a secret from this list when specifying Git credentials with the [GIT\_CREDENTIALS parameter](/sql-reference/sql/create-git-repository#label-create-git-repository-optional-parameters).

    This parameter’s value must be one of the following:

    - One or more fully-qualified Snowflake secret names to allow any of the listed secrets.
    - (Default) `all` to allow any secret.
    - `none` to allow no secrets.

    The ALLOWED\_API\_AUTHENTICATION\_INTEGRATIONS parameter can also specify allowed secrets. For more information, see
    [Usage notes](/sql-reference/sql/create-external-access-integration#label-create-external-access-integration-usage).

    For reference information about secrets, refer to [CREATE SECRET](/sql-reference/sql/create-secret).

`API_USER_AUTHENTICATION = ( TYPE = snowflake_github_app | TYPE = OAUTH2 oauth_parameters )`
:   Specifies security integration settings for an OAuth 2.0 flow.

    How you set this parameter differs depending on the repository provider. For more information, see [Configure for authenticating with OAuth](/developer-guide/git/git-setting-up-public#label-git-setup-oauth).

    - `TYPE = snowflake_github_app`: Authenticate with GitHub using the Snowflake GitHub App, as described in
      [Configure for authenticating with OAuth](/developer-guide/git/git-setting-up-public#label-git-setup-oauth). No other values are required for API\_USER\_AUTHENTICATION in this case.
    - `TYPE = OAUTH2`: Authenticate using OAuth2 parameters, as described in [Configure for authenticating with OAuth](/developer-guide/git/git-setting-up-public#label-git-setup-oauth).

      When you specify this value, you must also specify the parameters, as required, under `oauth_parameters` (next).
    - `oauth_parameters`: Authenticate using the specified OAuth 2.0 parameters, including the following parameters:

      - `OAUTH_AUTHORIZATION_ENDPOINT = 'endpoint_url'`

        Specifies the URL for authenticating to the repository.
      - `OAUTH_TOKEN_ENDPOINT = 'token_endpoint_url'`

        Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token.
        The client uses the token endpoint with every authorization grant except for the implicit grant type (because an access token is
        issued directly).
      - `OAUTH_CLIENT_ID = 'client_id'`

        Specifies the client ID for the OAuth application in the repository provider. The value for this parameter is specific to your
        organization.
      - `OAUTH_CLIENT_SECRET = 'client_secret'`

        Specifies the client secret for the OAuth application in the repository provider. The value for this parameter is specific to your
        organization.
      - `OAUTH_ACCESS_TOKEN_VALIDITY = integer`

        Specifies the default lifetime, in seconds, of the OAuth access token issued by an OAuth server.

        The value set in this property is used if the access token lifetime is not returned as part of OAuth token response. When both
        values are available, the smaller of the two values is used to refresh the access token.
      - `OAUTH_REFRESH_TOKEN_VALIDITY = integer`

        Specifies the value, in seconds, to determine the validity of the refresh token obtained from the OAuth server.
      - `OAUTH_ALLOWED_SCOPES = ( { 'read_api' | 'read_repository' | 'write_repository' } [ , ... ] )`
        Specifies the scope to use when making a request from the provider. Specify the following values:

        - `'read_api'`: Read from the repository provider’s API.
        - `'read_repository'`: Read from the repository.
        - `'write_repository'`: Write to the repository.
      - `OAUTH_USERNAME = 'string_literal'`

        Optional. The Git repository username. Set this value based on the repository provider’s requirements. For example, for Bitbucket,
        set this `x-token-auth`.

`TLS_TRUSTED_CERTIFICATES = ( {secret_name} [, {secret_name} ... ] )`
:   Specifies secrets containing self-signed certificates to be used when
    [authenticating with a Git repository server](/developer-guide/git/git-setting-up-private#label-git-setup-private-link-snowflake-access) over private link. This parameter is
    needed only when the certificate is self-signed, rather than signed by a certificate authority.

    This parameter’s value must be one or more fully qualified Snowflake secret names. The secrets must be of type
    [generic string](/sql-reference/sql/create-secret#label-create-secret-generic-string) whose SECRET\_STRING value is Base64-encoded certificate data.

`USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }`
:   Specifies whether this API integration will be used only to
    [configure access to a remote Git repository over an outbound private link connection](/developer-guide/git/git-setting-up-private#label-git-setup-private-network) through
    [private connectivity](/user-guide/private-connectivity-outbound).

    This parameter must be set to `FALSE` (the default) for public Git servers.

    The default is `FALSE`.

### For external MCP server

In addition to parameters for all integrations, use the following parameters when you’re connecting
to an external Model Context Protocol (MCP) server by setting the integration’s API\_PROVIDER parameter
to `external_mcp`. For end-to-end setup, see
[MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).

`API_USER_AUTHENTICATION = ( TYPE = OAUTH2 oauth_parameters | TYPE = OAUTH_DYNAMIC_CLIENT dcr_parameters )`
:   Specifies the OAuth settings used to connect to the external MCP server.

    - `TYPE = OAUTH2`: Authenticate using standard OAuth 2.0 with a client ID and client secret
      obtained from the MCP server provider. Specify the following sub-parameters:

      - `OAUTH_CLIENT_ID = 'client_id'`

        Specifies the client ID issued by the MCP server provider.
      - `OAUTH_CLIENT_SECRET = 'client_secret'`

        Specifies the client secret issued by the MCP server provider.
      - `OAUTH_TOKEN_ENDPOINT = 'token_endpoint_url'`

        Specifies the endpoint used to exchange authorization codes for access tokens.
      - `OAUTH_AUTHORIZATION_ENDPOINT = 'authorization_endpoint_url'`

        Specifies the endpoint where users authorize the connection.
      - `OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST | NONE }`

        Optional. Authentication method used by the client. Set this to `NONE` for a public
        client that authenticates with a static client ID and no client secret. Default:
        `CLIENT_SECRET_BASIC`.
      - `OAUTH_DISCOVERY_URL = 'discovery_url'`

        Optional. OpenID Connect discovery URL for automatic endpoint resolution.
      - `OAUTH_REFRESH_TOKEN_VALIDITY = integer`

        Optional. Validity, in seconds, of the OAuth refresh token issued by the external MCP service.
        When set, the value must be at least `3600` (one hour). The default is `0`, which
        Snowflake treats as a refresh token that never expires. Snowflake recommends setting an explicit,
        finite value so users periodically re-authenticate to the external MCP service.
    - `TYPE = OAUTH_DYNAMIC_CLIENT`: Authenticate using OAuth Dynamic Client Registration
      (DCR). Snowflake registers itself with the MCP service automatically. Specify the following
      sub-parameter:

      - `OAUTH_RESOURCE_URL = 'resource_url'`

        Specifies the resource URL of the external MCP service.

      `OAUTH_REFRESH_TOKEN_VALIDITY` does not apply to Dynamic Client Registration.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Only Snowflake roles with OWNERSHIP or USAGE privileges on the API integration can use the API integration directly
  (for example, by creating an external function that specifies that API integration).
- An API integration object is tied to a specific cloud platform account and role within that account, but not
  to a specific HTTPS proxy URL. You can create more than one instance of an HTTPS proxy service in a cloud provider
  account, and you can use the same API integration to authenticate to multiple proxy services in that account.
- Your Snowflake account can have multiple API integration objects, for example, for different cloud platform accounts.
- Multiple external functions can use the same API integration object, and thus the same HTTPS proxy service.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

### Amazon API Gateway

The following example shows creation of an API integration and use of that API integration in a subsequent
CREATE EXTERNAL FUNCTION statement:

Copy code

```
CREATE OR REPLACE API INTEGRATION demonstration_external_api_integration_01
  API_PROVIDER = aws_api_gateway
  API_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/my_cloud_account_role'
  API_ALLOWED_PREFIXES = ('https://xyz.execute-api.us-west-2.amazonaws.com/production')
  ENABLED = TRUE;

CREATE OR REPLACE EXTERNAL FUNCTION local_echo(string_col VARCHAR)
  RETURNS VARIANT
  API_INTEGRATION = demonstration_external_api_integration_01
  AS 'https://xyz.execute-api.us-west-2.amazonaws.com/production/remote_echo';
```

### Git repository

For an example of an API integration used to integrate a Git repository, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

### External MCP server

The following example creates an API integration for the Atlassian MCP server using
OAuth Dynamic Client Registration, and then creates an external MCP server object
that references it.

Copy code

```
CREATE API INTEGRATION jira_mcp_api_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://mcp.jira.atlassian.com')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH_DYNAMIC_CLIENT
    OAUTH_RESOURCE_URL = 'https://mcp.atlassian.com/v1/mcp'
  )
  ENABLED = TRUE;

CREATE EXTERNAL MCP SERVER atlassian_mcp_server
  WITH DISPLAY_NAME = 'Atlassian (Jira & Confluence)'
  URL = 'https://mcp.atlassian.com/v1/mcp'
  API_INTEGRATION = jira_mcp_api_integration;
```

The following example uses standard OAuth 2.0 against a custom MCP server, and sets
`OAUTH_REFRESH_TOKEN_VALIDITY` to 24 hours so refresh tokens have a finite lifetime
(the default of `0` is treated as a refresh token that never expires):

Copy code

```
CREATE API INTEGRATION custom_mcp_api_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://internal.mycompany.com/mcp')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = 'your_client_id'
    OAUTH_CLIENT_SECRET = 'your_client_secret'
    OAUTH_TOKEN_ENDPOINT = 'https://internal.mycompany.com/oauth/token'
    OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_BASIC
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://internal.mycompany.com/oauth/authorize'
    OAUTH_REFRESH_TOKEN_VALIDITY = 86400
  )
  ENABLED = TRUE;
```

The following example uses `OAUTH_CLIENT_AUTH_METHOD = NONE` for a public client that
authenticates with a static client ID issued by the provider and no client secret:

Copy code

```
CREATE API INTEGRATION custom_mcp_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://internal.mycompany.com')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = 'your_static_client_id'
    OAUTH_CLIENT_AUTH_METHOD = NONE
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://internal.mycompany.com/oauth/authorize'
    OAUTH_TOKEN_ENDPOINT = 'https://internal.mycompany.com/oauth/token'
  )
  ENABLED = TRUE;
```

For provider-specific setup steps and additional connectors (GitHub, Glean, Linear,
Salesforce), see [MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).
