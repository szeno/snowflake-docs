# Node.js options reference

When constructing a new `Connection` object, you pass in a JavaScript object that specifies the options for the connection
(e.g. your account identifier, your user name, etc.). The following sections describe the options that you can set. To set an
option, specify the option name as the property name in the JavaScript object.

- Connection options

  - [Required connection options](#label-nodejs-required-options)
  - [Authentication options](#label-nodejs-auth-options)
  - [Additional connection options](#label-nodejs-addl-options)
- Other options

  - [xmlParserConfig options](#label-nodejs-xml-parser-options)
  - [Certificate revocation list (CRL) options](#label-nodejs-crl-validation-options)

## Required connection options

`account`
:   Your [account identifier](/user-guide/gen-conn-config).

`region` (**Deprecated**)
:   The ID for the [region](/user-guide/intro-regions) where your account is located.

    Note

    This option is deprecated and is included here only for backward compatibility.
    Snowflake recommends transitioning to embedding the region in the account identifier,
    as described in [Using an account locator as an identifier](/user-guide/admin-account-identifier#label-account-locator-identifier), such as follows.

    Copy code

    ```
    const connection = snowflake.createConnection({
      account: "myaccount.us-east-2",
      username: "myusername",
      password: "mypassword"
    });
    ```

In addition, you must specify the [options for authenticating to the server](#label-nodejs-auth-options).

## Authentication options

`application`
:   Specifies the name of the client application connecting to Snowflake.

`authenticator`
:   Specifies the authenticator to use for verifying user login credentials. You can set this to one of the following values:

    | Value | Description |
    | --- | --- |
    | `SNOWFLAKE` | Use the internal Snowflake authenticator. You must also set the `password` option. |
    | `EXTERNALBROWSER` | [Use your web browser](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-sso) to authenticate with Okta, AD FS, or any other SAML 2.0-compliant identity provider (IdP) that has been defined for your account. |
    | `https://<okta_account_name>.okta.com` | [Use Native SSO through Okta](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-native-sso). |
    | `OAUTH` | Use OAuth for authentication. You must also set the `token` option to the OAuth token ([see below](/developer-guide/node-js/nodejs-driver-options#label-nodejs-auth-options-token)). |
    | `SNOWFLAKE_JWT` | Use key pair authentication. See [Use key-pair authentication and key-pair rotation](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-key-pair-authentication). |
    | `USERNAME_PASSWORD_MFA` | Use multi-factor authentication (MFA). See [Use an MFA passcode](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-mfa). |
    | `OAUTH_AUTHORIZATION_CODE` | Manually authenticate using an OAuth authorization code with your web browser and a chosen identity provider (including Snowflake as an IdP). For more information, see [Use the OAuth 2.0 Authorization Code flow](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-oauth-code-flow). |
    | `OAUTH_CLIENT_CREDENTIALS` | Automatically authenticate using OAuth client credentials with your chosen identity provider (Snowflake as an IdP doesn’t support the client credentials flow). For more information, see [Use the OAuth 2.0 Client Credentials flow](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-oauth-client-flow). |
    | `PROGRAMMATIC_ACCESS_TOKEN` | Authenticate with a programmatic access token (PAT). It reads the token from the `token` or `password` options. For more information, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens). |
    | `WORKLOAD_IDENTITY` | Authenticate with the [workload identity federation (WIF)](/user-guide/workload-identity-federation) authenticator. |

    Expand

    Show lessSee more

    The default value is `SNOWFLAKE`.

    For more information on authentication, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use) and
    [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).

`username`
:   The login name for your Snowflake user or your Identity Provider (e.g. your login name for Okta). Set this option if you set the `authenticator` option to `SNOWFLAKE`, `SNOWFLAKE_JWT`, or the
    [Okta URL endpoint for your Okta account](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-native-sso) (e.g. `https://<okta_account_name>.okta.com`).
    If you don’t set the `authenticator` option, you must set this value.

`password`
:   Password for the user. Set this option if you set the `authenticator` option to `SNOWFLAKE` or the
    [Okta URL endpoint for your Okta account](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-native-sso) (e.g. `https://<okta_account_name>.okta.com`)
    or if you left the `authenticator` option unset.

    If you set the `authenticator` option to `PROGRAMMATIC_ACCESS_TOKEN`, you can pass the programmatic access token in this option.

`token`
:   Specifies the OAuth token to use for authentication or programmatic access token. Set this option if you set the `authenticator` option to
    `OAUTH` or `PROGRAMMATIC_ACCESS_TOKEN`.

`privateKey`
:   Specifies the private key (in PEM format) for key pair authentication. For details, see
    [Use key-pair authentication and key-pair rotation](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-key-pair-authentication).

`privateKeyPath`
:   Specifies the local path to the private key file (e.g. `rsa_key.p8`). For details, see
    [Use key-pair authentication and key-pair rotation](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-key-pair-authentication).

`privateKeyPass`
:   Specifies the passcode to decrypt the private key file, if the file is encrypted. For details, see
    [Use key-pair authentication and key-pair rotation](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-key-pair-authentication).

`oauthClientId`
:   Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

`oauthClientSecret`
:   Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

`oauthAuthorizationUrl`
:   Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.

`oauthTokenRequestUrl`
:   Identity Provider endpoint supplying the access tokens to the driver. When using Snowflake as an Identity Provider, this value is derived from the `server` or `account` parameters.

`oauthScope`
:   Scope requested in the Identity Provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

`oauthRedirectUri`
:   URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

`workloadIdentityProvider`
:   Description:
    :   Platform of the workload identity provider. Possible values include: `AWS`, `AZURE`, `GCP`, and `OIDC`.

`workloadIdentityAzureClientId`
:   The Azure Managed Identity Client ID to use when connecting to Snowflake. Applies only when `workloadIdentityProvider=AZURE`.

`workloadIdentityImpersonationPath`
:   An array of strings that provides an identity chain to use when connecting to Snowflake. Array elements are either a full service account address or a service account’s unique ID.

    Impersonation works by following each array entry in order to obtain a token that allows authorization of the next service account. Each account in the identity chain needs permissions to impersonate the next account only. The final account in the list obtains your Snowflake connection token and is used to connect to Snowflake.

    This argument is supported for AWS and Google Cloud workloads and only applies when `authenticator=WORKLOAD_IDENTITY`.

`passcode`
:   Specifies the `passcode` provided by Duo when using multi-factor authentication (MFA) for logins. For details, see [Use an MFA passcode](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-mfa).

`passcodeInPassword`
:   Specifies whether the MFA `passcode` is embedded in the login password. If `true`, the MFA passcode is appended to the end of the `password`. Default: `false`. For details, see [Use an MFA passcode](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-mfa).

## Additional connection options

`accessUrl`
:   Specifies a fully-qualified endpoint for connecting to Snowflake. The `accessUrl` includes the full schema and host,
    as well as an optional port number, similar to `https://myaccount.us-east-1.snowflakecomputing.com`.

    Note

    When using the `accessUrl` option, the value specified in the `account` option is not used.

`browserActionTimeout`
:   Specifies the timeout, in milliseconds, for browser activities related to SSO authentication. The default value is
    120000 (milliseconds).

`openExternalBrowserCallback`
:   Opens a browser window for SSO authentication. By default, the driver uses the npm `open` package. For example:

    Copy code

    ```
    var connection = snowflake.createConnection({
      ...,
      openExternalBrowserCallback: () => {
        // your custom code to open browser window instead of our default implementation
      }
    });
    ```

`clientConfigFile`
:   Path to the client configuration file associated with the [easy logging](/developer-guide/node-js/nodejs-driver-logs#label-nodejs-easy-logging) feature.

`clientRequestMFAToken`
:   Sets whether the driver uses the MFA token in the local credential storage for authentication instead of requesting a new token from the server. Default: `false`.

`clientStoreTemporaryCredential`
:   Sets whether the driver uses the SSO token in the local credential storage for authentication instead of requesting a new token from the server. Default: `false`.

`clientSessionKeepAlive`
:   By default, client connections typically time out approximately 3-4 hours after the most recent query was executed.

    If the `clientSessionKeepAlive` option is set to `true`, the client’s connection to the server will be kept alive
    indefinitely, even if no queries are executed.

    The default setting of this option is `false`.

    If you set this option to `true`, make sure that your program explicitly disconnects from the server when your
    program has finished. Do not exit without disconnecting.

`clientSessionKeepAliveHeartbeatFrequency`
:   (Applies only when `clientSessionKeepAlive` is true)

    Sets the frequency (interval in seconds) between heartbeat messages.

    You can loosely think of a connection heartbeat message as substituting for a query and restarting the timeout
    countdown for the connection. In other words, if the connection would time out after at least 4 hours of inactivity,
    the heartbeat resets the timer so that the timeout will not occur until at least 4 hours after the most recent
    heartbeat (or query).

    The default value is 3600 seconds (one hour). The valid range of values is 900 - 3600. Because timeouts usually
    occur after at least 4 hours, a heartbeat every 1 hour is normally sufficient to keep the connection alive.
    Heartbeat intervals of less than 3600 seconds are rarely necessary or useful.

`credentialCacheDir`
:   Sets the directory in which to store the credential cache when token caching is enabled. Default: user’s `$HOME` directory.

`database`
:   The default database to use for the session after connecting.

`disableSamlUrlCheck`
:   Specifies whether to disable the validation check of a SAML response. Default: `false`.

`host`
:   Host address to which the driver should connect.

`keepAlive`
:   Specifies whether to enable keep-alive functionality on the socket immediately after receiving a new connection request.

    By default, the HTTP protocol creates a new TCP connection for every request. Enabling this parameter allows the driver to re-use connections for multiple requests
    instead of creating new connections for each request.

    The default value is `true`.

`noProxy`
:   Specifies the lists of hosts that the driver should connect to directly, bypassing the proxy
    server (e.g. `*.amazonaws.com` to bypass Amazon S3 access). For multiple hosts, separate the hostnames with a pipe
    symbol (`|`). You can also use an asterisk as a wild card. For example:

    `noProxy: "*.amazonaws.com|*.example.com"`

`proxyHost`
:   Specifies the hostname of an authenticated proxy server.

`proxyPassword`
:   Specifies the password for the user specified by `proxyUser`.

`proxyPort`
:   Specifies the port of an authenticated proxy server.

`proxyProtocol`
:   Specifies the protocol used to connect to the authenticated proxy server.
    Use this property to specify the HTTP protocol: `http` or `https`.

`proxyUser`
:   Specifies the username used to connect to an authenticated proxy server.

`queryTag`
:   The optional [QUERY\_TAG](/sql-reference/parameters#label-query-tag) to use for the connection, for tagging statements.

`role`
:   The default security role to use for the session after connecting.

`schema`
:   The default schema to use for the session after connecting.

`timeout`
:   Number of milliseconds to keep the connection alive with no response. Default: 60000 (1 minute).

`warehouse`
:   The default virtual warehouse to use for the session after connecting. Used for performing queries, loading data, etc.

Some connection options assume that the specified database object (database, schema, warehouse, or role) already
exists in the system. If the specified object does not exist, a default is not set during connection.

After connecting, all of the optional connection options can also be set or overridden through the [USE <object>](/sql-reference/sql/use) command.

## Configuration options

`arrayBindingThreshold`
:   Sets the maximum number of binds the driver uses in a bulk insert operation. The default value is 65280.

`cwd`
:   Current working directory to use for GET and PUt operations when it differs from the connector directory.

`representNullAsStringNull`
:   Specifies how the `fetchAsString` method returns null values.

    - `true` (enabled): Returns null values as the string, “NULL”.
    - `false` (disabled): Returns null values as `null`.

    Default: `true` (enabled)

`resultPrefetch`
:   Number of threads for clients to use to prefetch large result sets. Valid values: 1-10.

`rowMode`
:   Specifies how to return results that contain duplicate column names. Values include:

    - `array`: returns the result set as an array, including duplicate column names.
    - `object`: returns the result set as an object, omitting duplicate column names.
    - `object_with_renamed_duplicated_columns`: returns the result set as an object, while adding suffixes to duplicate names to make them unique.

    The default value is `object`.

## xmlParserConfig options

Beginning with version 1.7.0 of the driver, you can use the following `fast-xml-parser`
library configuration options to customize how the driver processes XML document attributes when querying columns
with XML content.

You can download the [fast-xml-parser](https://www.npmjs.com/package/fast-xml-parser).

By default, the Node.js driver ignores XML element attributes when returning XML data from a query. For example,
in the following XML content, the `<animal>` element includes an `id` attribute:

Copy code

```
<exhibit name="Polar Bear Plunge">
  <animal id="000001">
    <scientificName>Ursus maritimus</scientificName>
    <englishName>Polar Bear</englishName>
    <name>Kalluk</name>
  </animal>
  <animal id="000002">
    <scientificName>Ursus maritimus</scientificName>
    <englishName>Polar Bear</englishName>
    <name>Chinook</name>
  </animal>
</exhibit>
```

By default, when the Node.js driver returns the result set, it ignores the `id` attribute and returns the following
output. Notice the attribute names and values are not included.

```
{
  exhibit: {
    animal: [
      {
        "scientificName": "Ursus maritimus",
        "englishName": "Polar Bear",
        "name": "Kalluk",
      },
      {
        "scientificName": "Ursus maritimus",
        "englishName": "Polar Bear",
        "name": "Chinook"
      }
    ]
  }
}
```

For information about how to set these options, refer to [Parsing XML data](/developer-guide/node-js/nodejs-driver-consume#label-parsing-xml-data).

To help illustrate how the following options affect how the driver parses XML data, each option description shows how it
affects this example.

`ignoreAttributes`
:   Whether to ignore XML attributes during parsing. If you want to use the other parser options, you must set
    `ignoreAttributes: false`.

    Default: `true`

    When set to `false`, the driver returns the output as follows. Notice the `id` attribute is now
    included in the output (by default, the driver prefixes attribute names with `@_`):

    ```
    {
        exhibit: {
          animal: [
            {
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Kalluk",
              "@_id": "000001"
            },
            {
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Chinook",
              "@_id": "000002"
            }
          ],
          "@_name": "Polar Bear Plunge"
        }
    }
    ```

`alwaysCreateTextNode`
:   Whether to create a property with the tag name and assign the value directly.

    Default: `false`

    When set to `true`, the driver returns the output as follows:

    ```
    {
      exhibit: {
        animal: [
          {
            "scientificName": {
              "#text": "Ursus maritimus"
            },
            "englishName": {
              "#text": "Polar Bear"
            },
            "name": {
              "#text": "Kalluk"
            },
            "@_id": "000001"
          },
          {
            "scientificName": {
              "#text": "Ursus maritimus"
            },
            "englishName": {
              "#text": "Polar Bear"
            },
            "name": {
              "#text": "Chinook"
            },
            "@_id": "000002"
          }
          "@_name": "Polar Bear Plunge"
        ]
      }
    }
    ```

`attributeNamePrefix`
:   String to prepend to attribute names.

    Default: “@\_”

    When set to `""` to specify no prefix for attribute names, the driver returns the output as follows:

    ```
    {
        exhibit: {
          animal: [
            {
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Kalluk",
              "id": "000001"
            },
            {
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Chinook",
              "id": "000002"
            }
          ],
          "name": "Polar Bear Plunge"
        }
    }
    ```

`attributesGroupName`
:   Groups all attributes of a tag under a specified property name.

    Default: unset

    When set to `@@` to group all tag attributes in an element named `@@,` the driver returns the output as follows:

    ```
    {
        exhibit: {
          "@@": {
            "@_name": "Polar Bear Plunge"
          }
          animal: [
            {
              "@@": {
                "@_id": "000001"
              },
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Kalluk"
            },
            {
              "@@": {
                "@_id": "000002"
              },
              "scientificName": "Ursus maritimus",
              "englishName": "Polar Bear",
              "name": "Chinook"
            } an
          ]
        }
    }
    ```

## Certificate revocation list (CRL) options

These options are available in driver versions 2.3.0 and later.

`certRevocationCheckMode`
:   How to treat certificate revocation. The following values are supported:

    - `ENABLED`: Enables CRLs. Connections are terminated if there are errors related to obtaining and parsing the CRL.
    - `ADVISORY`: Enables CRLs. Errors related to obtaining and parsing the CRL are reported, but no certificates are revoked and the connection is allowed.
    - `DISABLED`: Disables CRLs. Certificates can only be revoked manually.

    Default: `DISABLED`

`crlAllowCertificatesWithoutCrlURL`
:   Whether certificates without an associated CRL are accepted. Applies only when `certRevocationCheckMode` is not `DISABLED`.

    Default: `false`

`crlInMemoryCache`
:   Whether CRLs should be cached in memory. Applies only when `certRevocationCheckMode` is not `DISABLED`.

    Default: `true`

`crlOnDiskCache`
:   Whether CRLs should be cached to disk. Applies only when `certRevocationCheckMode` is not `DISABLED`.

    Default: `true`
