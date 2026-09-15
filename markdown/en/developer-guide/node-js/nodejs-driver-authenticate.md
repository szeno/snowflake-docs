# Authenticating connections

To authenticate to Snowflake, you can use one of the following options:

- Password-based authentication

  To use this method, set the `password` option when establishing the connection.
- [Single sign-on (SSO)](#label-nodejs-sso) through a web browser
- [Native SSO](#label-nodejs-native-sso) through Okta
- [Key pair authentication](#label-nodejs-key-pair-authentication)
- [OAuth](#label-nodejs-oauth)
- [MFA](#label-nodejs-mfa)

Additionally, the Snowflake Node.js driver supports the ability to cache SSO and MFA tokens. For more information, see [Authentication token caching](#label-nodejs-token-caching).

## Use single sign-on (SSO) through a web browser

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure
your client application to use browser-based SSO for authentication.

In your application code:

1. Set the `authenticator` option to `EXTERNALBROWSER`.
2. To establish a connection, call the `connect` or `connectAsync` method.

For example:

Copy code

```
// Use a browser to authenticate via SSO.
const connection = snowflake.createConnection({
  ...,
  authenticator: 'EXTERNALBROWSER'
});

// Establish a connection.
connection.connect((err, conn) => {
  if (err) {
    ... // Handle any errors.
  } else {
    // Execute SQL statements.
    const statement = connection.execute({...});
  }
});
```

For more information about using browser-based SSO for authentication, see [Browser-based SSO](/user-guide/admin-security-fed-auth-use#label-browser-based-sso).

## Use native SSO through Okta

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview) through Okta, you can
configure your client application to use native SSO authentication through Okta.

In your application code:

1. Set the following options:

   - Set the `authenticator` option to the Okta URL endpoint for your Okta account (e.g.
     `https://<okta_account_name>.okta.com`).
   - Set the `username` and `password` options to the user name and password for your Identity Provider (IdP).
2. To establish a connection, call the `connect` or `connectAsync` method.

For example:

Copy code

```
// Use native SSO authentication through Okta.
const connection = snowflake.createConnection({
  ...,
  username: '<user_name_for_okta>',
  password: '<password_for_okta>',
  authenticator: 'https://myaccount.okta.com'
});

// Establish a connection.
connection.connect((err, conn) => {
  if (err) {
    ... // Handle any errors.
  } else {
    // Execute SQL statements.
    const statement = connection.execute({...});
  }
});
```

For more information about using native SSO authentication through Okta, see [Native SSO — \*Okta only\*](/user-guide/admin-security-fed-auth-use#label-native-sso-okta).

## Use key-pair authentication and key-pair rotation

The driver supports key pair authentication and key rotation. To use key-pair authentication and key rotation, follow the steps below:

1. Configure key pair authentication, as explained in [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
2. In your application code:
   1. Set the `authenticator` option to `SNOWFLAKE_JWT`.
   2. Use the private key to authenticate in one of the following ways:
      - Set the `privateKey` option to the private key.
      - Set the `privateKeyPath` option to the path to the private key file.

        If the file is encrypted, you must also set the `privateKeyPass` option to the passphrase to decrypt the private
        key.

> The following example loads the private key from a file and sets the `privateKey` option to the private key:
>
> Copy code
>
> ```
> import crypto from 'crypto';
> import fs from 'fs';
>
> // Read the private key file from the filesystem.
> const privateKeyFile = fs.readFileSync('<path_to_private_key_file>/rsa_key.p8');
>
> // Get the private key from the file as an object.
> const privateKeyObject = crypto.createPrivateKey({
>   key: privateKeyFile,
>   format: 'pem',
>   passphrase: 'passphrase'
> });
>
> // Extract the private key from the object as a PEM-encoded string.
> const privateKey = privateKeyObject.export({
>   format: 'pem',
>   type: 'pkcs8'
> });
>
> // Use the private key for authentication.
> const connection = snowflake.createConnection({
>   ...
>   authenticator: 'SNOWFLAKE_JWT',
>   privateKey: privateKey
> });
>
> // Establish a connection.
> connection.connect((err, conn) => {
>   ... // Handle any errors.
> });
>
> // Execute SQL statements.
> const statement = connection.execute({...});
> ```
>
> The following example sets the `privateKeyPath` option to an encrypted private key file and sets the
> `privateKeyPass` option to the passphrase used to decrypt the private key:
>
> Copy code
>
> ```
> // Use an encrypted private key file for authentication.
> // Specify the passphrase for decrypting the key.
> const connection = snowflake.createConnection({
>   ...
>   authenticator: 'SNOWFLAKE_JWT',
>   privateKeyPath: '<path-to-privatekey>/privatekey.p8',
>   privateKeyPass: '<passphrase_to_decrypt_the_private_key>'
> });
>
> // Establish a connection.
> connection.connect((err, conn) => {
>   ... // Handle any errors.
> });
>
> // Execute SQL statements.
> const statement = connection.execute({...});
> ```

## Use OAuth

To connect using OAuth, set the `authenticator` option to `OAUTH` and the `token` option to the OAuth access
token. For example:

Copy code

```
// Use OAuth for authentication.
const connection = snowflake.createConnection({
  ...
  authenticator: 'OAUTH',
  token: '<your_oauth_token>'
});

// Establish a connection.
connection.connect((err, conn) => {
  ... // Handle any errors.
});

// Execute SQL statements.
const statement = connection.execute({...});
```

For more information, see [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).

## Use the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials.

To enable the OAuth 2.0 Authorization Code flow:

1. Set the `authenticator` connection parameter to `oauth_authorization_code`.
2. Set the following OAuth connection parameters:
   - `oauthClientId`: Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `oauthClientSecret`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `oauthAuthorizationUrl`: Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `oauthTokenRequestUrl`: Identity provider endpoint supplying the access tokens to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `oauthScope`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.
   - `oauthRedirectUri`: URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

## Use the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data.

To enable the OAuth 2.0 Client Credentials flow:

1. Set the `authenticator` connection parameter to `oauth_client_credentials`.
2. Set the following OAuth connection parameters:
   - `oauthClientId`: Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `oauthClientSecret`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata)
   - `oauthTokenRequestUrl`: Identity provider endpoint supplying the access tokens to the driver.
   - `oauthScope`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

## Authenticate with workload identity federation (WIF)

[Workload identity federation](/user-guide/workload-identity-federation) provides a service-to-service authentication method for Snowflake. This method enables applications, services, or containers to authenticate with Snowflake by leveraging their cloud provider’s native identity system, such as AWS IAM, Microsoft Entra ID, or Google Cloud service accounts. This approach eliminates the need for managing long-lived credentials and simplifies credential acquisition compared to other methods like External OAuth. Snowflake connectors are designed to automatically obtain short-lived credentials from the platform’s identity provider.

To enable the Workload Identity Federation authenticator, do the following:

1. Set the `authenticator` connection parameter to `WORKLOAD_IDENTITY`.
2. Set the `workloadIdentityProvider` connection parameter to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on your platform.
3. For OpenID Connect (OIDC), specify the `token` connection parameter.

## Use an MFA passcode

Note

This feature requires Snowflake Node.js driver version 1.13.1 or higher.

You can connect to Snowflake by passing a multi-factor authentication (MFA) passcode instead of waiting for an external confirmation, such as a push notification from Duo. The driver provides the following ways to specify an MFA passcode:

- Set the `passcodeInPassword` option to `true` and include the passcode as part of the password string, similar to the following:

  Copy code

  ```
  const connection = snowflake.createConnection({
    account: '<account_identifier>',
    username: '<username>',
    ...
    authenticator: 'USERNAME_PASSWORD_MFA',
    password: 'abc123987654', // passcode 987654 is part of the password
    passcodeInPassword: true // because passcodeInPassword is true
  });
  ```
- Set the `passcode` option to the value of the passcode to specify the password and the passcode separately, similar to the following:

  Copy code

  ```
  const connection = snowflake.createConnection({
    account: '<account_identifier>',
    username: '<username>',
    ...
    authenticator: 'USERNAME_PASSWORD_MFA',
    password: 'abc123', // password and MFA passcode are input separately
    passcode: '987654'
  });
  ```

  To use this approach, ensure that the `passcodeInPassword` option is `false` (the default value).

Note

If you enable the `passcodeInPassword` option and set the `passcode` option, the `passcodeInPassword` option takes precedence.

For more information about these options, see [passcode](/developer-guide/node-js/nodejs-driver-options#label-nodejs-mfa-options).

## Authentication token caching

The Snowflake Node.js driver provides the ability to cache SSO and MFA tokens.

Important

Token caching is disabled by default. Caching tokens locally increases security risks. Because tokens do not expire for four hours, someone who accesses a token on a local system can impersonate the token owner until the token naturally expires. Consequently, before choosing to cache tokens, consider the following:

- Be aware and mindful of the potential risks.
- Consult with your internal security and compliance personnel to check whether your organization’s policies permit token caching.
- With the default settings, the file that stores the cached tokens is written in your `$HOME` directory, or in a path you configure. You are responsible for the security of the data in the designated directory.
- You are responsible to ensure that the file has proper permissions to be accessed only by the file owner.

### Cache SSO (ID) tokens

An SSO (ID) token is generated from the request when you connect to Snowflake with [external browser authentication](#label-nodejs-sso). Caching SSO (ID) tokens on the client driver’s side only works if the server allows them to be cached. Caching SSO tokens can be enabled on the server-side with executing the following SQL statement, as described in [Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients):

Copy code

```
ALTER ACCOUNT SET ALLOW_ID_TOKEN = TRUE;
```

To use an SSO token cache in the Node.js driver, set the following options in the `snowflake.createConnection()` call:

- Set `authenticator` to `EXTERNALBROWSER`. For details, see [Authentication options](/developer-guide/node-js/nodejs-driver-options#label-nodejs-auth-options).
- Set `clientStoreTemporaryCredential` to `true`.

Copy code

```
const connection = snowflake.createConnection({
  account: '<account_identifier>',
  username: '<username>',
  authenticator: 'EXTERNALBROWSER',
  clientStoreTemporaryCredential: true
});
```

When enabled, driver uses the cached token for subsequent connections until the token expires. If the driver opens a browser to authenticate the connection again, either the driver cannot find the token information in the local credential storage or the token has expired.

### Cache MFA tokens

An MFA token is generated from the request when you connect to Snowflake with [USERNAME\_PASSWORD\_MFA](#label-nodejs-mfa) authentication. Caching MFA tokens on the client driver’s side only works if the server allows them to be cached. Caching MFA tokens can be enabled on the server-side with executing the following SQL statement, as described in [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching):

Copy code

```
ALTER ACCOUNT SET ALLOW_CLIENT_MFA_CACHING = TRUE;
```

To use an MFA token cache in the Node.js driver, set the following options in the `snowflake.createConnection()` call:

- Set `authenticator` to `USERNAME_PASSWORD_MFA`. For details, see [Authentication options](/developer-guide/node-js/nodejs-driver-options#label-nodejs-auth-options).
- Set `clientRequestMFAToken` to `true`.

Copy code

```
const connection = snowflake.createConnection({
  account: '<account_identifier>',
  username: '<username>',
  password: '<password>',
  authenticator: 'USERNAME_PASSWORD_MFA',
  clientRequestMFAToken: true
});
```

When enabled, driver uses the cached token for subsequent connections until the token expires. If the driver reaches out to the MFA provider again, either the driver cannot find the token information in the local credential storage or the token has expired.

### Use the default credential manager

The Snowflake Node.js driver provides a credential manager and credential storage. By default, the driver stores cached tokens in your `$HOME` directory.

If you want to store the cached tokens in an alternate location, you can specify the desired location in the `credentialCacheDir` parameter of the `snowflake.createConnection()` function. You can specify either a relative or absolute path, as shown below:

- Relative path

  Copy code

  ```
  const connection = snowflake.createConnection({
    credentialCacheDir: '../../<folder name>'
  });
  ```
- Absolute path

  Copy code

  ```
  const connection = snowflake.createConnection({
    credentialCacheDir: 'C:\\<folder name>\\<subfolder name>'
  });
  ```

If you do not configure `credentialCacheDir`, the Snowflake Node.js driver uses `${HOME}/temporary_credential.json` to store the credentials.

### Use a custom credential manager

The Snowflake node.js driver provides a default credential manager, which uses a local JSON file to store the credentials. When no credential manager is explicitly configured, the driver will use this default credential manager.

If you prefer not to use the default credential manager, you can create a custom credential manager. A custom credential manager must meet the following requirements:

- It must minimally contain `read`, `write`, and `remove` functions. You can include other functions as well.
- It must be an `object` data type.

The following example shows a template for minimal custom credential manager.

Copy code

```
const sampleCustomManager = {
  read: function (key) {
    // (do something with the key)
    return token;
  },
  write: function (key, token) {
    // (do something with the key and token)
  },
  remove: function (key) {
    // (do something with the key)
  }
};
```

After completing your custom credential manager, you can configure it for the driver in the `snowflake.configure()` method, as shown. This example reflects MFA tokens, though you can also create custom credential managers for SSO tokens.

Copy code

```
import snowflake from 'snowflake-sdk';
import myCredentialManager from '<your custom credential manager module>';

snowflake.configure({
  customCredentialManager: myCredentialManager
});

const connection = snowflake.createConnection({
  account: '<account_identifier>',
  username: '<username>',
  password: '<password>',
  authenticator: 'USERNAME_PASSWORD_MFA',
  clientRequestMFAToken: true
});
```

Although the Snowflake Node.js driver provides a plugin-like interface to implement and use custom credential managers, Snowflake is not responsible for creating, implementing, or supporting custom credential managers for the customers.
