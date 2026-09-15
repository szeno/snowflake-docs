# Key-pair authentication and key-pair rotation

This topic describes using key pair authentication and key pair rotation in Snowflake.

## Overview

Snowflake supports using key pair authentication for enhanced authentication security as an alternative to basic authentication, such as
username and password.

This authentication method requires, as a minimum, a 2048-bit RSA key pair. You can generate the Privacy Enhanced Mail (PEM)
private-public key pair using OpenSSL. Some of the [Supported Snowflake Clients](#supported-snowflake-clients) allow using encrypted private keys to connect to
Snowflake. The public key is assigned to the Snowflake user who uses the Snowflake client to connect and authenticate to Snowflake.

Snowflake also supports rotating public keys in an effort to allow compliance with more robust security and governance postures.

## Supported Snowflake clients

The following table summarizes support for key pair authentication among Snowflake Clients. A checkmark (✔) indicates full support.
A missing checkmark indicates key pair authentication is not supported.

| Client | Key Pair Authentication | Key Pair Rotation | Unencrypted Private Keys | Encrypted Private Keys |
| --- | --- | --- | --- | --- |
| [Snowflake CLI](/developer-guide/snowflake-cli/index) | ✔ | ✔ | ✔ | ✔ |
| [SnowSQL (CLI client)](/user-guide/snowsql) | ✔ | ✔ | ✔ | ✔ |
| [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) | ✔ | ✔ | ✔ | ✔ |
| [Snowflake Connector for Spark](/user-guide/spark-connector) | ✔ | ✔ | ✔ |  |
| [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) | ✔ | ✔ | ✔ |  |
| [Snowflake Horizon Catalog endpoint](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) | ✔ | ✔ | ✔ | ✔ |
| [Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake) | ✔ | ✔ | ✔ |  |
| [JDBC Driver](/developer-guide/jdbc/jdbc) | ✔ | ✔ | ✔ | ✔ |
| [ODBC Driver](/developer-guide/odbc/odbc) | ✔ | ✔ | ✔ | ✔ |
| [Node.js Driver](/developer-guide/node-js/nodejs-driver) | ✔ | ✔ | ✔ | ✔ |
| [.NET Driver](/developer-guide/dotnet/dotnet-driver) | ✔ | ✔ | ✔ | ✔ |
| [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) | ✔ | ✔ | ✔ | ✔ |

Expand

Show lessSee more

## Configuring key-pair authentication

Complete the following steps to configure key pair authentication for all supported Snowflake clients.

### Generate the private keys

Depending on which one of the [Supported Snowflake Clients](#supported-snowflake-clients) you use to connect to Snowflake, you have the option to generate encrypted or
unencrypted private keys. Generally, it is safer to generate encrypted keys. Snowflake recommends communicating with your internal security
and governance officers to determine which key type to generate prior to completing this step.

Snowflake supports cryptographic keys generated using the following algorithms:

- RSA digital signature algorithms RS256, RS384, and RS512.
- (Python driver only) Elliptic Curve Digital Signature Algorithms (ECDSA) algorithms ES256 (P-256), ES384 (P-384), and ES512 (P-521).

These signatures use the SHA-256, SHA-384, and SHA-512 hash algorithms, respectively.

Tip

The command to generate an encrypted key prompts for a passphrase to regulate access to the key. Snowflake recommends using a passphrase
that complies with PCI DSS standards to protect the locally generated private key. Additionally, Snowflake recommends storing the
passphrase in a secure location. If you are using an encrypted key to connect to Snowflake, enter the passphrase during the initial
connection. The passphrase is only used for protecting the private key and will never be sent to Snowflake.

To generate a long and complex passphrase based on PCI DSS standards:

> 1. Access the [PCI Security Standards Document Library](https://www.pcisecuritystandards.org/document_library).
> 2. For **PCI DSS**, select the most recent version and your desired language.
> 3. Complete the form to access the document.
> 4. Search for `Passwords/passphrases must meet the following:` and follow the recommendations for password/passphrase
>    requirements, testing, and guidance. Depending on the document version, the phrase is likely located in a section called
>    `Requirement 8: Identify and authenticate access to system components` or a similar name.

To start, open a terminal window and generate a private key.

You can generate either an encrypted version of the private key or an unencrypted version of the private key.

To generate an unencrypted version, use the following command:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

To generate an encrypted version, use the following command, which omits `-nocrypt`:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8
```

The commands generate a private key in PEM format.

Copy code

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIE6T...
-----END ENCRYPTED PRIVATE KEY-----
```

### Generate a public key

From the command line, generate the public key by referencing the private key. The following command assumes the private key is encrypted
and contained in the file named `rsa_key.p8`.

Copy code

```
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

The command generates the public key in PEM format.

Copy code

```
-----BEGIN PUBLIC KEY-----
MIIBIj...
-----END PUBLIC KEY-----
```

### Store the private and public keys securely

Copy the public and private key files to a local directory for storage. Record the path to the files. Note that the private key is stored
using the PKCS#8 (Public Key Cryptography Standards) format and is encrypted using the passphrase you specified in the previous step.

However, the file should still be protected from unauthorized access using the file permission mechanism provided by your operating system.
It is your responsibility to secure the file when it is not being used.

### Grant the privilege to assign a public key to a Snowflake user

To assign a public key to a user, you must have one of the following
[roles or privileges](/user-guide/security-access-control-overview):

- MODIFY PROGRAMMATIC AUTHENTICATION METHODS privilege on the user.
- OWNERSHIP privilege on the user.

You can use the [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) or [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to grant the
MODIFY PROGRAMMATIC AUTHENTICATION METHODS or OWNERSHIP privilege on the user to a role.

For example, suppose that you want users with the `my_service_owner_role` custom role to assign the public key to the service
user `my_service_user`. The following statement grants the MODIFY PROGRAMMATIC AUTHENTICATION METHODS privilege on the
`my_service_user` user to the role `my_service_owner_role`:

Copy code

```
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER my_service_user
  TO ROLE my_service_owner_role;
```

### Assign the public key to a Snowflake user

Snowflake supports two ways to assign a public key to a user. Snowflake recommends registering a named key pair with
[ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair), which supports role restriction, named key
management, and key expiration.

#### Register a named key pair (recommended)

Use [ALTER USER … ADD KEY PAIR](/sql-reference/sql/alter-user-add-key-pair) to register a named key pair for the user:

Copy code

```
ALTER USER example_user ADD KEY PAIR my_key
  PUBLIC_KEY = 'MIIBIjANBgkqh...';
```

You can list a user’s named key pairs with [SHOW USER KEY PAIRS](/sql-reference/sql/show-user-key-pairs), and rotate, modify, or remove a key
pair with the corresponding [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair),
[ALTER USER … MODIFY KEY PAIR](/sql-reference/sql/alter-user-modify-key-pair), and [ALTER USER … REMOVE KEY PAIR](/sql-reference/sql/alter-user-remove-key-pair) commands.

#### Set the RSA\_PUBLIC\_KEY user property

Alternatively, you can set the `RSA_PUBLIC_KEY` property of the user with [ALTER USER](/sql-reference/sql/alter-user). This approach
does not support role restriction or expiration.

Copy code

```
ALTER USER example_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
```

Note

- Exclude the public key delimiters in the SQL statement.

### Verify the user’s public key fingerprint

1. Execute the following command to retrieve the user’s public key fingerprint:

   Copy code

   ```
   DESC USER example_user
     ->> SELECT SUBSTR(
        (SELECT "value" FROM $1
           WHERE "property" = 'RSA_PUBLIC_KEY_FP'),
        LEN('SHA256:') + 1) AS key;
   ```

   Output:

   ```
   Azk1Pq...
   ```
2. Copy the output.
3. Run the following command on the command line:

   Copy code

   ```
   openssl rsa -pubin -in rsa_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
   ```

   Output:

   ```
   writing RSA key
   Azk1Pq...
   ```
4. Compare both outputs. If both outputs match, the user correctly configured their public key.

### Configure the Snowflake client to use key-pair authentication

Update the client to use key pair authentication to connect to Snowflake.

- [Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-private-key)
- [SnowSQL](/user-guide/snowsql-start#label-snowsql-key-pair-authn-rotation)
- [Python connector](/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation)
- [Spark connector](/user-guide/spark-connector-use#label-spark-key-pair-authn-rotation)
- [Kafka connector](/user-guide/kafka-connector-install#label-kafka-key-pair-authn-rotation)
- [Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake)
- [JDBC driver](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication)
- [ODBC driver](/developer-guide/odbc/odbc-parameters#label-odbc-key-pair-authentication)
- [.NET driver](https://github.com/snowflakedb/snowflake-connector-net/blob/master/README.md)
- [Node.js Driver](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-key-pair-authentication)

## Configuring key-pair rotation

Rotate and replace your public and private keys based on the expiration schedule you follow internally. Snowflake supports two
ways to rotate a key:

- Rotate a named key pair with [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) (recommended).
- Replace one of two `RSA_PUBLIC_KEY` user properties with [ALTER USER](/sql-reference/sql/alter-user).

### Rotate a named key pair (recommended)

Use [ALTER USER … ROTATE KEY PAIR](/sql-reference/sql/alter-user-rotate-key-pair) to replace the public key associated with a named key pair. The prior
public key is retained for a configurable grace period so that in-flight clients can transition without downtime.

1. Generate a new private and public key set, following the steps in [Configuring key-pair authentication](#label-configuring-key-pair-authentication).
2. Replace the public key on the existing key pair:

   Copy code

   ```
   ALTER USER example_user ROTATE KEY PAIR my_key
     PUBLIC_KEY = 'JERUEHtcve...';
   ```

   By default, the prior key remains valid for 24 hours. To change the grace period, set
   `EXPIRE_ROTATED_KEY_PAIR_AFTER_HOURS` (`0` to expire the prior key immediately).
3. Update the code to connect to Snowflake using the new private key. After the grace period expires, Snowflake stops
   accepting the prior key.

### Rotate the RSA\_PUBLIC\_KEY user properties

Snowflake also supports the `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` properties on [ALTER USER](/sql-reference/sql/alter-user) for
associating up to 2 public keys with a user. Use this approach if you assigned the public key with the
`RSA_PUBLIC_KEY` property.

1. Complete all steps in [Configuring key-pair authentication](#label-configuring-key-pair-authentication) with the following updates:

   - Generate a new private and public key set.
   - Assign the public key to the user. Set the public key value to either `RSA_PUBLIC_KEY` or `RSA_PUBLIC_KEY_2`, whichever key
     value is not currently in use. For example:

     Copy code

     ```
     ALTER USER example_user SET RSA_PUBLIC_KEY_2='JERUEHtcve...';
     ```
2. Update the code to connect to Snowflake. Specify the new private key.

   Snowflake verifies the correct active public key for authentication based on the private key submitted with your connection information.
3. Remove the old public key from the user profile using an [ALTER USER](/sql-reference/sql/alter-user) command.

   Copy code

   ```
   ALTER USER example_user UNSET RSA_PUBLIC_KEY;
   ```
