# Authenticating to the server

This topic describes how to authenticate to the server when using the Snowflake SQL API.

When you send a request, the request must include authentication information. The next sections explain how to add
this information to the request:

- [Using OAuth](#label-sql-api-authenticating-oauth)
- [Using key-pair authentication](#label-sql-api-authenticating-key-pair)
- [Using workload identity federation](#label-sql-api-authenticating-wif)

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
   $ snow connection test --account <account_identifier> --user <user> --authenticator=oauth --token=<oauth_token>
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

## Using key-pair authentication

To use key pair authentication, follow these steps:

1. Set up key-pair authentication.

   As part of this process, you must:

   1. Generate a public-private key pair. The generated private key should be in a file (e.g. named `rsa_key.p8`).
   2. Assign the public key to your Snowflake user. After you assign the key to the user, run the
      [DESCRIBE USER](/sql-reference/sql/desc-user) command. In the output, the `RSA_PUBLIC_KEY_FP` property should be set to the fingerprint of the public key assigned to the user.

   For instructions on how to generate the key pair and assign a key to a user,
   see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth). For language-specific examples of creating a fingerprint and generating a
   JWT token, see the following:

   - [Python](#label-sql-api-authenticating-key-pair-python)
   - [Java](#label-sql-api-authenticating-key-pair-java)
   - [Node.js](#label-sql-api-authenticating-key-pair-nodejs)
2. Use Snowflake CLI to verify that you can use the generated private key to
   [connect to Snowflake](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-private-key):

   Copy code

   ```
   $ snow connection generate-jwt --account <account_identifier> --user <user> --private-key-path <path>/rsa_key.p8
   ```

   The command prompts you for a private key passphrase to complete the connection. You can avoid the prompt by providing the passphrase in the `PRIVATE_KEY_PASSPHRASE` environment variable.
3. In your application code:

   1. Generate the fingerprint (a SHA-256 hash) of the public key for the user. Prefix the fingerprint with `SHA256:`.
      For example:

      `SHA256:hash`

      You can also execute the SQL [DESCRIBE USER](/sql-reference/sql/desc-user) command to get the value from
      the RSA\_PUBLIC\_KEY\_FP property.
   2. Generate [a JSON Web Token (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token) with the following fields in the payload:

      | Field | Description | Example |
      | --- | --- | --- |
      | `iss` | Issuer of the JWT. Set it to the following value: `account_identifier.user.SHA256:public_key_fingerprint` where:  - `account_identifier` is your Snowflake [account identifier](/user-guide/admin-account-identifier). If you are using the [account locator](/user-guide/admin-account-identifier#label-account-locator), exclude any region information from the account locator.  - `user` is your Snowflake user name. - `SHA256:public_key_fingerprint` is the fingerprint that you generated in the previous step. Note  The `account_identifier` and `user` values must use all uppercase characters. If your account ID contains periods (`.`), you must replace them with hyphens (`-`), as periods in an account identifier cause the JWT to be invalid. | `MYORGANIZATION-MYACCOUNT.MYUSER.SHA256:public_key_fingerprint` |
      | `sub` | Subject for the JWT. Set it to the following value: `account_identifier.user` | `MYORGANIZATION-MYACCOUNT.MYUSER` |
      | `iat` | Issue time for the JWT in UTC. Set the value to the current time value as either seconds or milliseconds. | `1615370644` (seconds)   `1615370644000` (milliseconds) |
      | `exp` | Expiration time for the JWT in UTC. You can specify the value as either seconds or milliseconds.  Note  The JWT is valid for at most one hour after the token is issued, even if you specify a longer expiration time. | `1615374184` (seconds)   `1615374184000` (milliseconds) |

      Expand

      Show lessSee more
   3. In each API request that you send, set the following headers:

      - `Authorization: Bearer JWT`

        where `JWT` is the token that you generated.
      - (Optional) `X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT`

        If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.

        Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:

        - `KEYPAIR_JWT` (for key-pair authentication)
        - `OAUTH` (for OAuth)
        - `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](/user-guide/programmatic-access-tokens))

### Python example

The following sections describe how to generate a JWT and fingerprint using Python.

For an example of generating a JWT in Python, see [sql-api-generate-jwt.py](/static/samples/sql-api/sql-api-generate-jwt.py). The
`sql-api-generate-jwt.py` example uses the [PyJWT module](https://pypi.org/project/PyJWT/), which you can install by running:

> Copy code
>
> ```
> pip install pyjwt
> ```

#### Generating a JWT in Python

The following sections of code demonstrate how to generate a JWT. For a full example,
see [sql-api-generate-jwt.py](/static/samples/sql-api/sql-api-generate-jwt.py).

Note

This example is intended for use as a reference only. Do not use this code in production applications or environments.

> Copy code
>
> ```
> from datetime import timedelta, timezone, datetime
>
> # This example relies on the PyJWT module (https://pypi.org/project/PyJWT/).
> import jwt
>
> # Construct the fully qualified name of the user in uppercase.
> # - Replace <account_identifier> with your account identifier.
> #   (See https://docs.snowflake.com/en/user-guide/admin-account-identifier.html .)
> # - Replace <user_name> with your Snowflake user name.
> account = "<account_identifier>"
>
> # Get the account identifier without the region, cloud provider, or subdomain.
> if not '.global' in account:
>     idx = account.find('.')
>     if idx > 0:
>         account = account[0:idx]
>     else:
>         # Handle the replication case.
>         idx = account.find('-')
>         if idx > 0:
>             account = account[0:idx]
>
> # Use uppercase for the account identifier and user name.
> account = account.upper()
> user = "<user_name>".upper()
> qualified_username = account + "." + user
>
> # Get the current time in order to specify the time when the JWT was issued and the expiration time of the JWT.
> now = datetime.now(timezone.utc)
>
> # Specify the length of time during which the JWT will be valid. You can specify at most 1 hour.
> lifetime = timedelta(minutes=59)
>
> # Create the payload for the token.
> payload = {
>
>     # Set the issuer to the fully qualified username concatenated with the public key fingerprint (calculated in the  previous step).
>     "iss": qualified_username + '.' + public_key_fp,
>
>     # Set the subject to the fully qualified username.
>     "sub": qualified_username,
>
>     # Set the issue time to now.
>     "iat": now,
>
>     # Set the expiration time, based on the lifetime specified for this object.
>     "exp": now + lifetime
> }
>
> # Generate the JWT. private_key is the private key that you read from the private key file in the previous step when you generated the public key fingerprint.
> encoding_algorithm="RS256"
> token = jwt.encode(payload, key=private_key, algorithms=encoding_algorithm)
>
> # If you are using a version of PyJWT prior to 2.0, jwt.encode returns a byte string, rather than a string.
> # If the token is a byte string, convert it to a string.
> if isinstance(token, bytes):
>   token = token.decode('utf-8')
> print(token)
> decoded_token = jwt.decode(token, key=private_key.public_key(), algorithms=[encoding_algorithm])
> print("Generated a JWT with the following payload:\n{}".format(decoded_token))
> ```

#### Generating a fingerprint in Python

The following sections of code demonstrate how to generate the fingerprint. For a full example, see
[sql-api-generate-jwt.py](/static/samples/sql-api/sql-api-generate-jwt.py).

> Copy code
>
> ```
> from cryptography.hazmat.primitives.serialization import load_pem_private_key
> from cryptography.hazmat.primitives.serialization import Encoding
> from cryptography.hazmat.primitives.serialization import PublicFormat
> from cryptography.hazmat.backends import default_backend
> ..
> import base64
> from getpass import getpass
> import hashlib
> ..
> # If you generated an encrypted private key, implement this method to return
> # the passphrase for decrypting your private key. As an example, this function
> # prompts the user for the passphrase.
> def get_private_key_passphrase():
>     return getpass('Passphrase for private key: ')
>
> # Private key that you will load from the private key file.
> private_key = None
>
> # Open the private key file.
> # Replace <private_key_file_path> with the path to your private key file (e.g. /x/y/z/rsa_key.p8).
> with open('<private_key_file_path>', 'rb') as pem_in:
>     pemlines = pem_in.read()
>     try:
>         # Try to access the private key without a passphrase.
>         private_key = load_pem_private_key(pemlines, None, default_backend())
>     except TypeError:
>         # If that fails, provide the passphrase returned from get_private_key_passphrase().
>         private_key = load_pem_private_key(pemlines, get_private_key_passphrase().encode(), default_backend())
>
> # Get the raw bytes of the public key.
> public_key_raw = private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
>
> # Get the sha256 hash of the raw bytes.
> sha256hash = hashlib.sha256()
> sha256hash.update(public_key_raw)
>
> # Base64-encode the value and prepend the prefix 'SHA256:'.
> public_key_fp = 'SHA256:' + base64.b64encode(sha256hash.digest()).decode('utf-8')
> ```

### Snowflake CLI example

You can use the Snowflake CLI `snow connection generate-jwt` command to generate a JWT for key-pair authentication. For more information, see [snow connection generate-jwt](/developer-guide/snowflake-cli/command-reference/connection-commands/generate-jwt).

This example generates a token for account `TEST` and user `JDOE`, using the private key from `rsa_key.p8`:

Copy code

```
snow connection generate-jwt --user JDOE --account TEST --private-key-file=rsa_key.p8
```

The command prompts you for a private key passphrase to complete the connection. You can avoid the prompt by providing the passphrase in the `PRIVATE_KEY_PASSPHRASE` environment variable.

### Java example

For an example of generating a JWT in Java, see
[SimpleStatementsApi.java](/static/samples/sql-api/SimpleStatementsApi.java).

Note

This example is intended for use as a reference only. Do not use this code in production applications or environments.

This example uses the following third-party libraries:

- [Swagger Codegen](https://swagger.io/tools/swagger-codegen/download/): an open source library useful in developing REST
  APIs and applications.
- [Auth0](https://auth0.com/docs/libraries): provides Java APIs for authentication and generating JWT tokens.

### Node.js example

For an example of generating a JWT in Node.js, see
[sql-api-generate-jwt.js](/static/samples/sql-api/sql-api-generate-jwt.js).

Note

This example is intended for use as a reference only. Do not use this code in production applications or environments.

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
