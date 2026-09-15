# Authenticating Snowflake REST APIs with Snowflake

This topic describes how to authenticate to the server when using the Snowflake REST APIs.

When you send a request, the request must include authentication information using either of the following:

- [Using key pair authentication](#label-sfrest-api-authenticating-key-pair)
- [Using OAuth](#label-sfrest-authenticating-oauth)
- [Using a programmatic access token (PAT)](#label-sfrest-authenticating-pat)
- [Using workload identity federation](#label-sfrest-authenticating-wif)

## Using key pair authentication

When using key pair authentication, you need to complete the following tasks:

1. [Set up key pair authentication](#label-sfrest-api-setup-authenticating-key-pair)
2. [Generate a JWT token](#label-sfrest-api-jwt-token)

### Set up key pair authentication

To use key pair authentication, follow these steps:

1. Set up key pair authentication.

   As part of this process, you must:

   1. Generate a public-private key pair. The generated private key should be in a file (e.g. named `rsa_key.p8`).
   2. Assign the public key to your Snowflake user. After you assign the key to the user, run the
      [DESCRIBE USER](/sql-reference/sql/desc-user) command. In the output, the `RSA_PUBLIC_KEY_FP` property should be set to the fingerprint of the public key assigned to the user.

   For instructions on how to generate the key pair and assign a key to a user,
   see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
2. Use Snowflake CLI to verify that you can use the generated private key to
   [connect to Snowflake](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-private-key):

   Copy code

   ```
   $ snow connection test --account <account_identifier> --user <user> --private-key-path <path>/rsa_key.p8
   ```

   If you generated an encrypted private key, Snowflake CLI prompts you for the passphrase that you created when you generated the key.

### Generate a JWT token

To generate a JWT token in your application code, use the following steps:

1. Generate the fingerprint (a SHA-256 hash) of the public key for the user. Prefix the fingerprint with `SHA256:`.
   For example:

   `SHA256:hash`

   You can also execute the SQL [DESCRIBE USER](/sql-reference/sql/desc-user) command to get the value from
   the RSA\_PUBLIC\_KEY\_FP property.
2. Generate [a JSON Web Token (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token) with the following fields in the payload:

   > | Field | Description | Example |
   > | --- | --- | --- |
   > | `iss` | Issuer of the JWT. Set it to the following value: `account_identifier.user.SHA256:public_key_fingerprint` where:  - `account_identifier` is your Snowflake [account identifier](/user-guide/admin-account-identifier). If you are using the [account locator](/user-guide/admin-account-identifier#label-account-locator), exclude any region information from the account locator.  - `user` is your Snowflake user name. - `SHA256:public_key_fingerprint` is the fingerprint that you generated in the previous step. Note  The `account_identifier` and `user` values must use all uppercase characters. | `MYORGANIZATION-MYACCOUNT.MYUSER.SHA256:public_key_fingerprint` |
   > | `sub` | Subject for the JWT. Set it to the following value: `account_identifier.user` | `MYORGANIZATION-MYACCOUNT.MYUSER` |
   > | `iat` | Issue time for the JWT in UTC. Set the value to the current time value as either seconds or milliseconds. | `1615370644` (seconds)   `1615370644000` (milliseconds) |
   > | `exp` | Expiration time for the JWT in UTC. You can specify the value as either seconds or milliseconds.  Note  The JWT is valid for at most one hour after the token is issued, even if you specify a longer expiration time. | `1615374184` (seconds)   `1615374184000` (milliseconds) |
   >
   > Expand
   >
   > Show lessSee more
3. In each API request that you send, set the following headers:

   - `Authorization: Bearer JWT`

     where `JWT` is the token that you generated.
   - (Optional) `X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT`

     If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

     Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

     - `KEYPAIR_JWT` (for key-pair authentication)
     - `OAUTH` (for OAuth)
     - `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](/user-guide/programmatic-access-tokens))

## Using OAuth

To use OAuth, follow these steps:

1. Set up OAuth for authentication.

   See [Introduction to OAuth](/user-guide/oauth-intro) for details on how to set up OAuth and get an OAuth token.
2. Use Snowflake CLI to verify that you can use a generated OAuth token to connect to Snowflake:

   - For Linux and MacOS systems

   Copy code

   ```
   $ snow connection test --account <account_identifier> --user <user> --authenticator=oauth --token=<oauth_token>
   ```

   - For Windows systems

   Copy code

   ```
   $ snow connection test --account <account_identifier> --user <user> --authenticator=oauth --token="<oauth_token>"
   ```
3. In each API request you send, set the following headers:

   - `Authorization: Bearer oauth_token`

     where `oauth_token` is the generated OAuth token.
   - (Optional) `X-Snowflake-Authorization-Token-Type: OAUTH`

     If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

     Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

     - `KEYPAIR_JWT` (for key-pair authentication)
     - `OAUTH` (for OAuth)
     - `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](/user-guide/programmatic-access-tokens))

## Using a programmatic access token (PAT)

To authenticate with a programmatic access token, set the following HTTP headers in the request:

- `Authorization: Bearer token_secret`
- `X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN` (optional)

For example, if you are using cURL to send a request to a
[Snowflake REST API](/developer-guide/snowflake-rest-api/snowflake-rest-api) endpoint:

Copy code

```
curl --location 'https://myorganization-myaccount.snowflakecomputing.com/api/v2/databases' \
  --header "Authorization: Bearer <token_secret>"
```

If the request fails with a `PAT_INVALID` error, the error might have occurred for one of the following reasons:

- The user associated with the programmatic access token was not found.
- Validation failed.
- The role associated with the programmatic access token was not found.
- The user is not associated with the specified programmatic access token.

For more information, see [Using a programmatic access token to authenticate to an endpoint](/user-guide/programmatic-access-tokens#label-pat-use-endpoint).

## Using workload identity federation

To use workload identity federation, follow these steps:

1. As a workload administrator, configure your cloud provider or OpenID Connect (OIDC) provider to issue an attestation:

   - [AWS](/user-guide/workload-identity-federation#label-wif-aws-configure-aws)
   - Microsoft Azure (see [Configure Microsoft Entra ID](/user-guide/workload-identity-federation#label-wif-azure-configure-entra) and [Configure Azure](/user-guide/workload-identity-federation#label-wif-azure-configure-azure))
   - [Google Cloud](/user-guide/workload-identity-federation#label-wif-gcp-configure-gcp)
   - [Amazon Elastic Kubernetes Service (EKS)](/user-guide/workload-identity-federation#label-wif-oidc-aws-kubernetes-configure-aws)
   - [Azure Kubernetes Service (AKS)](/user-guide/workload-identity-federation#label-wif-oidc-azure-kubernetes-configure-azure)
   - [Google Kubernetes Engine (GKE)](/user-guide/workload-identity-federation#label-wif-oidc-google-kubernetes-configure-google)
   - [Custom OIDC provider](/user-guide/workload-identity-federation#label-wif-oidc-custom-configure-custom)
2. As a Snowflake administrator, create a service user for the workload that is authenticating:

   - [AWS](/user-guide/workload-identity-federation#label-wif-aws-authentication-snowflake)
   - [Microsoft Azure](/user-guide/workload-identity-federation#label-wif-azure-configure-snowflake)
   - [Google Cloud](/user-guide/workload-identity-federation#label-wif-gcp-authentication-snowflake)
   - [Amazon Elastic Kubernetes Service (EKS)](/user-guide/workload-identity-federation#label-wif-oidc-aws-kubernetes-configure-snowflake)
   - [Azure Kubernetes Service (AKS)](/user-guide/workload-identity-federation#label-wif-oidc-azure-kubernetes-configure-snowflake)
   - [Google Kubernetes Engine (GKE)](/user-guide/workload-identity-federation#label-wif-oidc-google-kubernetes-configure-snowflake)
   - [Custom OIDC provider](/user-guide/workload-identity-federation#label-wif-oidc-custom-configure-snowflake)
3. Obtain a token that can be included in the authorization header of your request:

   - **AWS**: For a workload with an attached IAM role, [follow the AWS steps](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetWebIdentityToken.html) to get a JWT token. Be sure to set the audience to `snowflakecomputing.com`.
   - **Microsoft Azure**: For a workload with an attached managed identity, [follow the Azure steps](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-http) to get an access token. Be sure to set the resource to `api://fd3f753b-eed3-462c-b6a7-a4b5bb650aad`.
   - **Google Cloud**: For a workload with an attached service account, [follow the Google Cloud steps](https://cloud.google.com/docs/authentication/get-id-token#metadata-server) to get an ID token. Be sure to set the audience to `snowflakecomputing.com`.
   - **Kubernetes / Custom OIDC**: Use the token issued by your OIDC provider.
4. Put the token in the authorization header of your request using the following format:

   Copy code

   ```
   Authorization: Bearer WIF.{provider}.{token}
   X-Snowflake-Authorization-Token-Type: WORKLOAD_IDENTITY_FEDERATION
   ```

   Where:

   - `{provider}` corresponds to your cloud provider. Specify one of the following values: `AWS`, `AZURE`, `GCP`, or `OIDC`.
   - `{token}` is the token obtained in the previous step.
