# Configuring the JDBC Driver

This topic describes how to configure the JDBC driver, including how to
connect to Snowflake using the driver.

Note

The connection parameters are now documented in the [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters).

## JDBC Driver class

Version 4.xVersion 3.x

Use `net.snowflake.client.api.driver.SnowflakeDriver` as the driver class in your JDBC application.

Note

- Don’t reference any other Snowflake classes or methods in your application code because they are subject to change in the future to implement improvements and fixes.
- The previous driver class, `net.snowflake.client.api.driver.SnowflakeDriver`, is still supported but is deprecated (meaning it will be removed in a future release). Any code that references the previous class name will continue to work, but you should update the code to reference the new class name because the change has been implemented.

Use `net.snowflake.client.jdbc.SnowflakeDriver` as the driver class in your JDBC application.

Note

- Don’t reference any other Snowflake classes or methods in your application code because they are subject to change in the future to implement improvements and fixes.
- The previous driver class, `com.snowflake.client.jdbc.SnowflakeDriver`, is still supported but is deprecated (meaning it will be removed in a future release, TBD).
  Any code that references the previous class name will continue to work, but you should update the code to reference the new class name because the
  change has been implemented.

## JDBC Driver connection string

Important

Beginning with Snowflake version 8.24, network administrators have the option to require multi-factor authentication (MFA) for all connections to Snowflake. If your administrator decides to enable this feature, you must configure your client or driver to use MFA when connecting to Snowflake. For more information, see the following resources:

- [8.24 release notes](/release-notes/2024/8_24#label-authentication-policies-new-multi-factor-authentication-parameters)
- [Multi-factor authentication (MFA)](/user-guide/security-mfa)
- [Troubleshooting service users authentication issues with Snowflake MFA](https://community.snowflake.com/s/article/Troubleshooting-service-users-authentication-issues-with-Snowflake-MFA) Knowledge Base article

Using the JDBC driver to connect to Snowflake requires a connection string with the syntax described below.

You can generate the basic connection string in Snowsight. For information, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

Note

You cannot set the [SEARCH\_PATH](/sql-reference/parameters#label-search-path) parameter within a JDBC client connection string. You must
establish a session before setting a search path.

### Syntax

Copy code

```
jdbc:snowflake://<account_identifier>.snowflakecomputing.com/?<connection_params>
```

### Connection parameters

Note

For documentation on individual connection parameters, see the [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters).

`<account_identifier>`
:   Specifies the account identifier for your Snowflake account. For details, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).
    For examples of the account identifier used in a JDBC connection string, see [Examples](#label-other-jdbc-connection-string-examples).

`<connection_params>`
:   Specifies a series of one or more [JDBC connection parameters](/developer-guide/jdbc/jdbc-parameters)
    and [session parameters](/sql-reference/parameters), in the form of `<param>=<value>`, with
    each parameter separated by the ampersand character (`&`), and no spaces anywhere in the connection string.

    If you need to set parameter values that use spaces, ampersands (`&`), equals signs (`=`), or other special characters, you
    should [URL-encode](https://en.wikipedia.org/wiki/Percent-encoding) the special characters. For example, if you need to
    specify a value that contains a space, ampersand, and equals sign in the [query\_tag](/sql-reference/parameters#label-query-tag) session parameter:

    Copy code

    ```
    String connectionURL = "jdbc:snowflake://myorganization-myaccount.snowflakecomputing.com/?query_tag='folder=folder1 folder2&'
    ```

    encode the space as `%20`, the ampersand as `%26`, and the equals sign as `%3D`:

    Copy code

    ```
    String connectionURL = "jdbc:snowflake://myorganization-myaccount.snowflakecomputing.com/?query_tag='folder%3Dfolder1%20folder2%26'
    ```

    As an alternative, rather than specifying these parameters in the connection string, you can set these parameters in a
    `Properties` object that you pass to the `DriverManager.getConnectionIO` method.

    Copy code

    ```
    Properties props = new Properties();
    props.put("parameter1", parameter1Value);
    props.put("parameter2", parameter2Value);
    Connection con = DriverManager.getConnection("jdbc:snowflake://<account_identifier>.snowflakecomputing.com/", props);
    ```

Note

For documentation on individual connection parameters, see the [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters).

### Other parameters

Any session parameter can be included in the connection string. For example:

> `BROWSER_RESPONSE_TIMEOUT=<Integer>`
> :   Specifies the timeout, in seconds, to wait for a successful authentication from an external browser.
>
>     Default is `120`.
>
> `CLIENT_OUT_OF_BAND_TELEMETRY_ENABLED=<Boolean>`
> :   Specifies whether to enable out-of-band telemetry.
>
>     Default is `true`.
>
> `CLIENT_SESSION_KEEP_ALIVE=<Boolean>`
> :   Specifies whether to keep the current session active after a period of inactivity, or to force the user to login again. If the value is `true`, Snowflake keeps the session active indefinitely,
>     even if there is no activity from the user. If the value is `false`, the user must log in again after four hours of inactivity.
>
>     Default is `false`.
>
> `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY=<Integer>`
> :   Specifies the number of seconds (900-3600) in-between client attempts to update the token for the session.
>
>     Default is `3600`.

> `net.snowflake.jdbc.commons_logging_wrapper`
> :   Specifies how to handle logs from commons logging. Possible values are:
>
>     - `ALL`: All logs from common logging are passed to `SFLogger` (`java.util.logging` or SLF4J is used internally).
>     - `Default`: All logs from commons logging are forwarded to `java.util.logging`, and no logs are forwarded to the SLF4J logger.
>     - `OFF`: No logs from commons logging are forwarded. You can use this value if you need to replace commons logging with the SLF4J bridge when using a thin JAR file.
>
> `JDBC_QUERY_RESULT_FORMAT=JSON`
> :   Specifies `JSON` as the result format to use while fetching or processing the results of a query sent to Snowflake.
>
>     Default is `Arrow`.

For descriptions of all the session parameters, see [Parameters](/sql-reference/parameters).

### Examples

The following is an example of the connection string that uses the
[account name as an identifier](/user-guide/admin-account-identifier#label-account-name-using) for the account `myaccount` in the organization
`myorganization`.

> Copy code
>
> ```
> jdbc:snowflake://myorganization-myaccount.snowflakecomputing.com/?user=peter&warehouse=mywh&db=mydb&schema=public
> ```

The following is an example of a connection string that uses the [account locator](/user-guide/admin-account-identifier#label-account-locator)
`xy12345` as the account identifier:

> Copy code
>
> ```
> jdbc:snowflake://xy12345.snowflakecomputing.com/?user=peter&warehouse=mywh&db=mydb&schema=public
> ```

Note that this example uses an account in the AWS US West (Oregon) region. If the account is in a different region or if the
account uses a different cloud provider, you need to
[specify additional segments after the account locator](/user-guide/admin-account-identifier#label-account-locator).

## Connecting using the `connections.toml` file

The JDBC driver lets you add connection definitions to a `connections.toml` configuration file.
A connection definition refers to a collection of connection-related parameters. The driver currently supports TOML version 1.0.0.

For more information about `toml` file formats, see [TOML (Tom’s Obvious Minimal Language)](https://toml.io/en/).

The connection string prefix: `jdbc:snowflake:auto` tells the driver to look for the connection configuration within the predefined (default) files.
The JDBC driver looks for the `connections.toml` file in the following locations, in order:

- The location specified by the `SNOWFLAKE_HOME` environment variable.
- The `~/.snowflake/connections.toml` file, if the `~/.snowflake` directory exists.

You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
[Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

If you want to switch between multiple existing connections, you can configure them in the `connections.toml` file. The default key is `default`, but you change the name of the default connection by setting the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` shell environment variable.

The following sample `connections.toml` files defines three connections:

```
[default]
account = 'my_organization-my_account'
user = 'test_user'
warehouse = 'testw'
database = 'test_db'
schema = 'test_nodejs'
protocol = 'https'
port = '443'
authenticator = 'oauth'
token_file_path = '/Users/test/.snowflake/token'

[production]
account = 'my_organization-my_account'
user = 'prod_user'
warehouse = 'prodw'
database = 'prod_db'
schema = 'prod_nodejs'
protocol = 'https'
port = '443'
authenticator = 'oauth'
token_file_path = '/Users/test/.snowflake/token'

[aws-oauth-file]
account = 'my_organization-my_account'
user = 'test_user'
warehouse = 'testw'
database = 'test_db'
schema = 'test_nodejs'
protocol = 'https'
port = '443'
authenticator = 'oauth'
token_file_path = '/Users/test/.snowflake/token'
```

### Specifying a connection to use in the `auto` connection prefix

You can specify which connection configuration to use by appending the connection name to the `auto` prefix in the connection string. Continuing the previous example, to connect with `aws-oauth-file`, use the following connection string:

Copy code

```
jdbc:snowflake:auto?connectionName=aws-oauth-file
```

This connection string tells the JDBC driver to look for the `aws-oauth-file` connection definition in the `connections.toml` file.

The driver determines which connection to use in the following order:

1. Connection name specified in the connection string using the `jdbc:snowflake:auto?connectionName=<connection_name_in_toml_file>` syntax
2. Connection name specified in the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` shell environment variable
3. The default connection name, `default`

If the connection name specified in the connection string does not exist in the `connections.toml` file, the driver does the following:

- Logs a message indicating the missing name and the file path checked.
- Throws an exception containing the name of the missing connection, in the following format:
  `The Connection <connection name> not found in connections.toml file.`
- Terminates the connection attempt.

## Using single sign-on (SSO) for authentication

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure
your client application to use SSO for authentication. See [Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients) for details.

## Using multi-factor authentication

Snowflake supports caching MFA tokens, including combining MFA token caching with SSO.

For more information, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

## Using key pair authentication and key rotation

The Snowflake JDBC driver supports key pair authentication and key rotation. This authentication method requires a 2048-bit (minimum) RSA key pair.

To start, complete the initial configuration for key pair authentication as shown in [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

Next, choose one of the following three options to configure either the JDBC connection properties or the JDBC connection string.

1. Specify the private key via the privateKey property in the connection properties.
2. Specify the private key file name and password for that file as separate properties in the connection properties.
3. Specify the private key file name and password for that file as part of the connection string.

These options are described in more detail in the next three sections.

### `privateKey` property in connection properties

This section provides an example of setting the `privateKey` property to a private key in a file.

This example uses the [Bouncy Castle Crypto APIs](https://www.bouncycastle.org/java.html). In order to compile and run this
example, you must include the following JAR files in your classpath:

- the provider JAR file (`bcprov-jdkversions.jar`)
- the PKIX / CMS / EAC / PKCS / OCSP / TSP / OPENSSL JAR file (`bcpkix-jdkversions.jar`)

where `versions` specifies the versions of the JDK that the JAR file supports.

To use this example:

1. Copy the [sample code below](/developer-guide/jdbc/jdbc-configure#label-jdbc-private-key-auth-example), and replace the following placeholder values:

   | Placeholder | Description |
   | --- | --- |
   | `path/rsa_key.p8` | Set this to the path and name of the private key file that you generated earlier. |
   | `private_key_passphrase` | If you generated an encrypted key, implement the `getPrivateKeyPassphrase()` method to return the passphrase for decrypting that key. |
   | `account_identifier` | Set this to your [account identifier](/user-guide/gen-conn-config). |
   | `user` | Set this to your Snowflake login name. |
   | `database_name` | Set this to the name of the database that you want to use. |
   | `schema_name` | Set this to the name of the schema that you want to use. |
   | `warehouse_name` | Set this to the name of the warehouse that you want to use. |
   | `role` | Set this to the name of the role that you want to use. |

   Expand

   Show lessSee more
2. Compile and run the sample code. Include the Bouncy Castle JAR files in the classpath.

   For example, on Linux and macOS:

   Copy code

   ```
   javac -cp bcprov-jdk<versions>.jar:bcpkix-jdk<versions>.jar TestJdbc.java

   java -cp .:snowflake-jdbc-<ver>.jar:bcprov-jdk<versions>.jar:bcpkix-jdk<versions>.jar TestJdbc.java
   ```

   On Windows:

   Copy code

   ```
   javac -cp bcprov-jdk<versions>.jar;bcpkix-jdk<versions>.jar TestJdbc.java

   java -cp .;snowflake-jdbc-<ver>.jar;bcprov-jdk<versions>.jar;bcpkix-jdk<versions>.jar TestJdbc.java
   ```

**Sample code**

Copy code

```
import org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;
import org.bouncycastle.openssl.jcajce.JceOpenSSLPKCS8DecryptorProviderBuilder;
import org.bouncycastle.operator.InputDecryptorProvider;
import org.bouncycastle.operator.OperatorCreationException;
import org.bouncycastle.pkcs.PKCS8EncryptedPrivateKeyInfo;
import org.bouncycastle.pkcs.PKCSException;

import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.security.PrivateKey;
import java.security.Security;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.DriverManager;
import java.util.Properties;

public class TestJdbc
{
  // Path to the private key file that you generated earlier.
  private static final String PRIVATE_KEY_FILE = "/<path>/rsa_key.p8";

  public static class PrivateKeyReader
  {

    // If you generated an encrypted private key, implement this method to return
    // the passphrase for decrypting your private key.
    private static String getPrivateKeyPassphrase() {
      return "<private_key_passphrase>";
    }

    public static PrivateKey get(String filename)
            throws Exception
    {
      PrivateKeyInfo privateKeyInfo = null;
      Security.addProvider(new BouncyCastleProvider());
      // Read an object from the private key file.
      PEMParser pemParser = new PEMParser(new FileReader(Paths.get(filename).toFile()));
      Object pemObject = pemParser.readObject();
      if (pemObject instanceof PKCS8EncryptedPrivateKeyInfo) {
        // Handle the case where the private key is encrypted.
        PKCS8EncryptedPrivateKeyInfo encryptedPrivateKeyInfo = (PKCS8EncryptedPrivateKeyInfo) pemObject;
        String passphrase = getPrivateKeyPassphrase();
        InputDecryptorProvider pkcs8Prov = new JceOpenSSLPKCS8DecryptorProviderBuilder().build(passphrase.toCharArray());
        privateKeyInfo = encryptedPrivateKeyInfo.decryptPrivateKeyInfo(pkcs8Prov);
      } else if (pemObject instanceof PrivateKeyInfo) {
        // Handle the case where the private key is unencrypted.
        privateKeyInfo = (PrivateKeyInfo) pemObject;
      }
      pemParser.close();
      JcaPEMKeyConverter converter = new JcaPEMKeyConverter().setProvider(BouncyCastleProvider.PROVIDER_NAME);
      return converter.getPrivateKey(privateKeyInfo);
    }
  }

  public static void main(String[] args)
      throws Exception
  {
    String url = "jdbc:snowflake://<account_identifier>.snowflakecomputing.com";
    Properties prop = new Properties();
    prop.put("user", "<user>");
    prop.put("privateKey", PrivateKeyReader.get(PRIVATE_KEY_FILE));
    prop.put("db", "<database_name>");
    prop.put("schema", "<schema_name>");
    prop.put("warehouse", "<warehouse_name>");
    prop.put("role", "<role_name>");

    Connection conn = DriverManager.getConnection(url, prop);
    Statement stat = conn.createStatement();
    ResultSet res = stat.executeQuery("select 1");
    res.next();
    System.out.println(res.getString(1));
    conn.close();
  }
}
```

Note

Use forward slashes as file path separators on all operating systems, including Windows. The JDBC driver replaces forward slashes
with the appropriate path separator for the platform.

### Private key file name and password as connection properties

You can specify the private key file name and password as separate connection properties, for example:

Copy code

```
Properties props = new Properties();
props.put("private_key_file", "/tmp/rsa_key.p8");
props.put("private_key_file_pwd", "dummyPassword");
Connection connection = DriverManager.getConnection("jdbc:snowflake://myorganization-myaccount.snowflake.com", props);
```

If you specify the `private_key_file` and `private_key_file_pwd` parameters, do not specify the
`privateKey` parameter in the connection properties.

Note

Use forward slashes as file path separators on all operating systems, including Windows. The JDBC driver replaces forward slashes
with the appropriate path separator for the platform.

### Private key file name and password in connection string

You can specify the private key file name and password in the connection string, as shown below:

Copy code

```
Connection connection = DriverManager.getConnection(
    "jdbc:snowflake://myorganization-myaccount.snowflake.com/?private_key_file=/tmp/rsa_key.p8&private_key_file_pwd=dummyPassword",
    props);
```

Note

Use forward slashes as file path separators on all operating systems, including Windows. The JDBC driver replaces forward slashes
with the appropriate path separator for the platform.

If you specify the private key and password in the connection string, then do not specify the parameters
`private_key_file`, `private_key_file_pwd`, or `privateKey` in the connection properties.

### Key decryption errors

If you use encrypted keys that were generated using OpenSSL V3, you might receive errors similar to the following:

```
java.security.NoSuchAlgorithmException: 1.2.840.113549.1.5.13 SecretKeyFactory not available

java.security.InvalidKeyException: IOException : DER input, Integer tag error
```

In this situation, you can use Bouncy Castle to decrypt the key by specifying the following JVM argument:

Version 4.xVersion 3.x

Copy code

```
-Dnet.snowflake.jdbc.useBundledBouncyCastleForPrivateKeyDecryption=true
```

The default value is `true`, which means that the bundled Bouncy Castle library is used to decrypt the key.

Copy code

```
-Dnet.snowflake.jdbc.enableBouncyCastle=true
```

## Using the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials.

To enable the OAuth 2.0 Authorization Code flow:

1. Set the `authenticator` connection parameter to `oauth_authorization_code`.
2. Set the following OAuth connection parameters:
   - `oauthClientId`: Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata). Default: `LOCAL_APPLICATION` if unset and the IDP is Snowflake.
   - `oauthClientSecret`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata). Default: `LOCAL_APPLICATION` if unset and the IDP is Snowflake.
   - `oauthAuthorizationUrl`: Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `oauthTokenRequestUrl`: Identity provider endpoint supplying the access tokens to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `oauthScope`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.
   - `oauthRedirectUri`: URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

## Using the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data.

To enable the OAuth 2.0 Client Credentials flow:

1. Set the `authenticator` connection parameter to `oauth_client_credentials`.
2. Set the following OAuth connection parameters:
   - `oauthClientId`: Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `oauthClientSecret`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata)
   - `oauthTokenRequestUrl`: Identity provider endpoint supplying the access tokens to the driver.
   - `oauthScope`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

## Authenticating with a programmatic access token (PAT)

Programmatic access token (PAT) is a Snowflake-specific authentication method. The feature must be enabled for the account before usage (see the [Prerequisites](/user-guide/programmatic-access-tokens#label-pat-prerequisites) for more information). Authentication with PAT doesn’t involve any human interaction.

## Authenticating with workload identity federation (WIF)

[Workload identity federation](/user-guide/workload-identity-federation) provides a service-to-service authentication method for Snowflake. This method enables applications, services, or containers to authenticate with Snowflake by leveraging their cloud provider’s native identity system, such as AWS IAM, Microsoft Entra ID, or Google Cloud service accounts. This approach eliminates the need for managing long-lived credentials and simplifies credential acquisition compared to other methods like External OAuth. Snowflake connectors are designed to automatically obtain short-lived credentials from the platform’s identity provider.

To enable the workload identity federation authenticator, do the following:

1. Set the `authenticator` connection parameter to `WORKLOAD_IDENTITY`.
2. Set the `workloadIdentityProvider` connection parameter to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on your platform.
3. For OpenID Connect (OIDC), specify the `token` connection parameter.

## Verifying the network connection to Snowflake with SnowCD

After configuring your driver, you can evaluate and troubleshoot your network connectivity to Snowflake using [SnowCD](/user-guide/snowcd).

You can use SnowCD during the initial configuration process and on-demand at any time to evaluate and troubleshoot your network connection to Snowflake.

## Connecting using a proxy server

You can use a proxy server with the Snowflake JDBC Driver in the following ways:

- [Set system properties](#label-jdbc-proxy-java) for your proxy settings in the JVM (Java Virtual Machine) for your client application.
- [Include the proxy host and port information in the JDBC connection string](#label-java-connecting-using-a-proxy-server-using-connection-string) or the `Properties` object passed to the
  `DriverManager.getConnection()` method.

Note

Proxy settings specified in the connection string take precedence over JVM system properties.

Tip

Snowflake’s security model does not allow Transport Layer Security (TLS) proxies (using an HTTPS certificate). Your
proxy server must use a publicly-available Certificate Authority (CA), reducing potential security risks such as
a MITM (Man In The Middle) attack through a compromised proxy.

If you must use your TLS proxy, we strongly recommend that you update the server policy to pass through
the Snowflake certificate such that no certificate is altered in the middle of communications.

As an alternative, you can set the `nonProxyHosts` parameter in the connection string or `Properties` object to
bypass the proxy for specific communications. For example, Amazon S3 access can be bypassed by specifying
`nonProxyHosts=".amazonaws.com"`.

### Specifying a proxy server by setting Java system properties

To connect through a proxy server, you can set the proxy system properties. You can either set these in
your code or pass them on the command line to the JVM (Java virtual machine) for your client application.

For more information, see [Java Networking and Proxies](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html).

To set the system properties in your code, call `System.setProperty`:

> Copy code
>
> ```
> System.setProperty("http.useProxy", "true");
> System.setProperty("http.proxyHost", "proxyHost Value");
> System.setProperty("http.proxyPort", "proxyPort Value");
> System.setProperty("http.proxyUser", "proxyUser Value");
> System.setProperty("http.proxyPassword", "proxyPassword Value");
> System.setProperty("https.proxyHost", "proxyHost HTTPS Value");
> System.setProperty("https.proxyPort", "proxyPort HTTPS Value");
> System.setProperty("https.proxyUser", "proxyUser HTTPS Value");
> System.setProperty("https.proxyPassword", "proxyPassword HTTPS Value");
> System.setProperty("http.proxyProtocol", "https");
> ```

To pass the system properties on the command line to your JVM, use the `-D` command-line option:

> Copy code
>
> ```
> -Dhttp.useProxy=true
> -Dhttps.proxyHost=<proxy_host>
> -Dhttps.proxyPort=<proxy_port>
> -Dhttps.proxyUser=<proxy_user>
> -Dhttps.proxyPassword=<proxy_password>
> -Dhttp.proxyHost=<proxy_host>
> -Dhttp.proxyPort=<proxy_port>
> -Dhttp.proxyUser=<proxy_user>
> -Dhttp.proxyPassword=<proxy_password>
> -Dhttp.proxyProtocol="https"
> ```

To bypass the proxy for one or more IP addresses or hosts, set the `http.nonProxyHosts` system property to the list of these
hosts:

- Use a pipe symbol (`|`) to separate the host names.
- To specify hostnames that match a pattern, use an asterisk (`*`) as a wildcard character.

The following example demonstrates how to set this system property on the command line:

Copy code

```
-Dhttp.nonProxyHosts="*.example.com%localhost%myorganization-myaccount.snowflakecomputing.com|192.168.91.*"
```

### Specifying a proxy server in the JDBC connection string

Note

Specifying the proxy information as part of the URL is less secure than other methods of specifying the
proxy information.

To use a proxy server by setting the following parameters in the JDBC connection string:

- [useProxy](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-use-proxy)
- [proxyHost](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-proxy-host)
- [proxyPort](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-proxy-port)
- [proxyUser](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-proxy-user)
- [proxyPassword](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-proxy-password)
- [proxyProtocol](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-proxy-protocol)

If your proxy server does not require authentication, you can omit the `proxyUser` and `proxyPassword` parameters.

If your proxy server connection requires authentication using a proxy username and proxy password, those
credentials may be exposed as plain text by other applications when using the HTTP protocol. To avoid
exposing these credentials, use the `proxyProtocol` parameter to specify the HTTPS protocol.

Copy code

```
jdbc:snowflake://<account_identifier>.snowflakecomputing.com/?warehouse=<warehouse_name>&useProxy=true&proxyHost=<ip_address>&proxyPort=<port>&proxyUser=test&proxyPassword=test
```

For example:

Copy code

```
jdbc:snowflake://myorganization-myaccount.snowflakecomputing.com/?warehouse=DemoWarehouse1&useProxy=true&proxyHost=172.31.89.76&proxyPort=8888&proxyUser=test&proxyPassword=test
```

The proxy settings specified in the connection string take precedence over JVM system properties.

If the proxy JVM arguments are set and you do not want to proxy any of your connections, do not set `useProxy=false`, as it has no effect. Instead, use the following, which effectively bypasses the JVM proxy settings:

Copy code

```
useProxy=true
proxyHost=127.0.0.1
proxyPort=8080
nonProxyHosts=*
```

#### Bypassing the Proxy Server

If you need to bypass the proxy server when connecting to one or more hosts, specify the list of hosts in the
`nonProxyHosts` parameter:

Copy code

```
&nonProxyHosts=<bypass_proxy_for_these_hosts>
```

Separate the hostnames with a URL-escaped pipe symbol (`%7C`). You can also use an asterisk (`*`) as a wildcard. For example:

Copy code

```
&nonProxyHosts=*.example.com%7Clocalhost%7Cmyorganization-myaccount.snowflakecomputing.com%7C192.168.91.*
```

#### Specifying the Protocol Used to Connect to the Proxy Server

- To specify the protocol used to connect to the proxy server, use the `proxyProtocol` parameter. The default value is `http`, but `https` is also valid.

For example:

Copy code

```
&proxyProtocol=https
```

## OCSP

When the driver connects, Snowflake sends a certificate to confirm that the connection is to Snowflake rather than to
a host that is impersonating Snowflake. The driver sends that certificate to an OCSP (Online Certificate Status
Protocol) server to verify that the certificate has not been revoked.

If the driver cannot reach the OCSP server to verify the certificate, the driver can
[“fail open” or “fail closed”](/user-guide/ocsp#label-ocsp-fail-open-or-fail-close).

### Choosing fail-open or fail-close mode

JDBC Driver versions prior to 3.8.0 default to fail-close. Versions 3.8.0 and later default to fail-open.
You can override the default behavior in any of the following ways:

- Set the connection property `ocspFailOpen` to `true` or `false`. For example:

  Copy code

  ```
  Properties connection_properties = new Properties();
  connection_properties.put("ocspFailOpen", "false");
  ...
  connection = DriverManager.getConnection(connectionString, connection_properties);
  ```
- Set the system property `net.snowflake.jdbc.ocspFailOpen` to `true` or `false`. For
  example:

  Copy code

  ```
  Properties p = new Properties(System.getProperties());
  p.put("net.snowflake.jdbc.ocspFailOpen", "false");
  System.setProperties(p);
  ```

### Verifying the OCSP connector or driver version

For more information about the driver or connector version, configuration, and OCSP behavior, see
[OCSP Configuration](/user-guide/ocsp).

### OCSP response cache server

Note

The OCSP response cache server is currently supported by the Snowflake JDBC Driver 3.6.0 and higher.

Snowflake clients initiate every connection to a Snowflake service endpoint with a “handshake” that establishes a secure connection before actually transferring data. As part of the handshake, a
client authenticates the TLS certificate for the service endpoint. The revocation status of the certificate is checked by sending a client certificate request to one of the OCSP
(Online Certificate Status Protocol) servers for the CA (certificate authority).

A connection failure occurs when the response from the OCSP server is delayed beyond a reasonable time. The following caches persist the revocation status, helping alleviate these issues:

- Memory cache, which persists for the life of the process.
- File cache, which persists until the cache directory (e.g. `~/.cache/snowflake` or `~/.snowsql/ocsp_response_cache`) is purged.
- Snowflake OCSP response cache server, which fetches OCSP responses from the CA’s OCSP servers hourly and stores them for 24 hours. Clients can then request the validation status of a given Snowflake
  certificate from this server cache.

  Important

  If your server policy denies access to most or all external IP addresses and web sites, you must allowlist the cache server
  address to allow normal service operation. The cache server hostname is `ocsp*.snowflakecomputing.com:80`.

  If you need to disable the cache server for any reason, set the `SF_OCSP_RESPONSE_CACHE_SERVER_ENABLED` environment variable to `false`. Note that the value is case-sensitive and must
  be in lowercase.

If none of the cache layers contain the OCSP response, the client then attempts to fetch the validation status directly from the OCSP server for the CA.

## File caches

To improve usability, the driver uses file caches for authentication and OCSP responses. By default, these files are stored in the following directories:

Linux:
:   `~/.cache/snowflake`

macOS:
:   `~/Library/Caches/Snowflake`

Windows:
:   `%USERPROFILE%AppDataLocalSnowflakeCaches`

If the JDBC application user does not have a user profile in the local operating system, the driver attempts to store the cache files in the temporary directory. You can configure the driver to write
cache files to another directory using the following environment variables:

> `SF_TEMPORARY_CREDENTIAL_CACHE_DIR=string`
> :   Specifies the location of the temporary credential cache file in a local directory. This can also be configured with the JVM option `-Dnet.snowflake.jdbc.temporaryCredentialCacheDir=string`
>     on launch.
>
> `SF_OCSP_RESPONSE_CACHE_DIR=string`
> :   Specifies the location of the OCSP response cache file in a local directory. This can also be configured with the JVM option `-Dnet.snowflake.jdbc.ocspResponseCacheDir=string` on launch.
>
>     For more information, see [OCSP Response Cache Server](#ocsp-response-cache-server) (in this topic).

Note that the JVM options should be set on launch, and not programmatically (via `System.setProperty()`). If both environment variable and JVM options are provided, the JVM option will be used.

## Configuring JDBC logging

Starting with version 3.0.4, the JDBC driver supports the following logging frameworks:

- [Java Core Logging Facilities](#label-configuring-jdbc-java-core-logging) (default logger for the driver)
- [Simple Logging Facade for Java](#label-configuring-jdbc-logging-facade)
- [Logging Configuration File](#label-configuring-jdbc-logging-config)

### Java core logging facilities (`Java.util.logging`)

By default, the `java.util.logging` uses `ConsoleHandler` to write to the standard error stream. You can set the Boolean `JAVA_LOGGING_CONSOLE_STD_OUT` java or connection property to `true`, which writes all logs to the standard output stream. The default value is `false`.

If you enable `JAVA_LOGGING_CONSOLE_STD_OUT`, you can also set the `JAVA_LOGGING_CONSOLE_STD_OUT_THRESHOLD` java or connection property to set the maximum log level the driver should write to standard output. Any log messages with a higher level than specified are sent to standard error. Possible values for this property include:

- `OFF`
- `SEVERE`
- `WARNING`
- `INFO`
- `CONFIG`
- `FINE`
- `FINER`
- `FINEST`
- `ALL`

To choose this logger explicitly, specify the following option for the JVM:

> `-Dnet.snowflake.jdbc.loggerImpl=net.snowflake.client.log.JDK14Logger`

Then, you can customize the logging configuration using the application programming interface (API) for the logger.

For more details, see the [java.util.logging Package documentation](https://docs.oracle.com/javase/8/docs/api/java/util/logging/package-summary.html).

For example, create a file named `logging.properties` that includes the following contents:

> Copy code
>
> ```
> ###########################################################
> #   Default Logging Configuration File
> #
> # You can use a different file by specifying a filename
> # with the java.util.logging.config.file system property.
> # For example java -Djava.util.logging.config.file=myfile
> ############################################################
>
> ############################################################
> #   Global properties
> ############################################################
>
> # "handlers" specifies a comma-separated list of log Handler
> # classes.  These handlers will be installed during VM startup.
> # Note that these classes must be on the system classpath.
> # ConsoleHandler and FileHandler are configured here such that
> # the logs are dumped into both a standard error and a file.
> handlers = java.util.logging.ConsoleHandler, java.util.logging.FileHandler
>
> # Default global logging level.
> # This specifies which kinds of events are logged across
> # all loggers.  For any given facility this global level
> # can be overriden by a facility specific level.
> # Note that the ConsoleHandler also has a separate level
> # setting to limit messages printed to the console.
> .level = INFO
>
> ############################################################
> # Handler specific properties.
> # Describes specific configuration information for Handlers.
> ############################################################
>
> # default file output is in the tmp dir
> java.util.logging.FileHandler.pattern = /tmp/snowflake_jdbc%u.log
> java.util.logging.FileHandler.limit = 5000000000000000
> java.util.logging.FileHandler.count = 10
> java.util.logging.FileHandler.level = INFO
> java.util.logging.FileHandler.formatter = net.snowflake.client.log.SFFormatter
>
> # Limit the messages that are printed on the console to INFO and above.
> java.util.logging.ConsoleHandler.level = INFO
> java.util.logging.ConsoleHandler.formatter = net.snowflake.client.log.SFFormatter
>
> # Example to customize the SimpleFormatter output format
> # to print one-line log message like this:
> #     <level>: <log message> [<date/time>]
> #
> # java.util.logging.SimpleFormatter.format=%4$s: %5$s [%1$tc]%n
>
> ############################################################
> # Facility specific properties.
> # Provides extra control for each logger.
> ############################################################
>
> # Snowflake JDBC logging level.
> net.snowflake.level = INFO
> net.snowflake.handler = java.util.logging.FileHandler
> ```

Specify the JVM parameters in the command line:

> Copy code
>
> ```
> java -jar application.jar -Dnet.snowflake.jdbc.loggerImpl=net.snowflake.client.log.JDK14Logger -Djava.util.logging.config.file=logging.properties
> ```

Where `application.jar` references the application code for the JDBC driver. The log files are located in `/tmp/snowflake_jdbc*`.

### Simple logging facade for Java (`org.slf4j`)

To choose this logger, set the JVM option:

> `-Dnet.snowflake.jdbc.loggerImpl=net.snowflake.client.log.SLF4JLogger`.
>
> You must add `slf4j-api` and its implementation (for example, `logback`) to the `classpath`.

For more information, see the [Simple Logging Facade for Java (SLF4J) documentation](http://www.slf4j.org).

### Bridging logs from commons-logging

Some of the libraries use Apache commons-logging for logging. Handling these logs is configured by the `net.snowflake.jdbc.commons_logging_wrapper` JVM option that was added in version 3.22.0. For details, see [Other parameters](#label-other-jdbc-connection-parameters).

### Logging configuration file

Alternatively, you can easily specify the [log level](https://github.com/snowflakedb/snowflake-jdbc/blob/master/src/main/java/net/snowflake/client/log/SFLogLevel.java) and
the directory in which to save log files in the `sf_client_config.json` configuration file.

Note

This logging configuration file feature supports only the following log levels:

> - `DEBUG`
> - `ERROR`
> - `INFO`
> - `OFF`
> - `TRACE`
> - `WARNING`

This configuration file uses JSON to define the `log_level` and `log_path` logging parameters, as follows:

Copy code

```
{
  "common": {
    "log_level": "DEBUG",
    "log_path": "/home/user/logs"
  }
}
```

The driver looks configuration details in the following order:

- `client_config_file` [connection parameter](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-client-config-file),
  containing the full path to the user-defined logging configuration file. For example:

  Copy code

  ```
  client_config_file=/opt/snowflake/snowflake_jdbc/my_jdbc_config.json
  ```
- `SF_CLIENT_CONFIG_FILE` environment variable, containing the full path to the user-defined logging configuration file.

  Copy code

  ```
  export SF_CLIENT_CONFIG_FILE=/home/myuser/my_jdbc_config.json
  ```
- JDBC driver installation directory, where the file must be named `sf_client_config.json`.
- User’s home directory, where the file must be named `sf_client_config.json`.

Note

- If the configuration file is not found in any of the preceding locations, the driver uses the
  [Java core logging facilities](#label-configuring-jdbc-java-core-logging).
- If a configuration file specified in either the `client_config_file` connection parameter or
  `SF_CLIENT_CONFIG_FILE` environment variable cannot be found or read, the driver throws an error message.

## Disabling PUT and GET commands

By default, the JDBC driver allows you to execute PUT and GET commands. If you don’t want to allow PUT and GET
commands access to the local file system, you can disable these commands in the following ways:

Version 4 .xVersion 3.x

- Set the [JDBC\_ENABLE\_PUT\_GET](/sql-reference/parameters#label-jdbc-enable-put-get) server parameter to `FALSE`.
- Set the JDBC [enablePutGet](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-enableputget) connection parameter to `false`.

- Set the [JDBC\_ENABLE\_PUT\_GET](/sql-reference/parameters#label-jdbc-enable-put-get) server parameter to `FALSE`.
- Set the JDBC [enablePutGet](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-enableputget) connection parameter to `false`.
- Call the `SFBaseSession.setEnablePutGet(false)` method.

## HTTP headers customization feature in Snowflake JDBC driver

To programmatically add custom HTTP headers to requests made by the Snowflake JDBC driver, implement the `HttpHeadersCustomizer` interface and register your implementation(s). This allows flexible, programmatic injection of dynamic or static headers.

Key considerations:

- The driver iterates registered customizers for applicable requests (Snowflake API, S3, private link OCSP). Then it calls `applies()`, then `newHeaders()` (respecting `invokeOnce()` for retries).
- Customizers cannot override essential driver-set headers. This is enforced by the driver.
- Keep `applies()` and `newHeaders()` efficient.

The following example shows how to implement `net.snowflake.client.jdbc.HttpHeadersCustomizer`.

Copy code

```
public class MyDynamicCustomizer implements HttpHeadersCustomizer {
    public boolean applies(String method, String uri, Map<String, List> headers) {
        return true;
    }

    public Map<String, List<String>> newHeaders() {
        Map<String, List<String>> headers = new HashMap<>();
        headers.put("X-Dynamic-Token", Collections.singletonList("token-" + System.nanoTime()));
        return headers;
    }

    public boolean invokeOnce() {
        return false;
    }
}
```

The following examples show different ways to register customizers:

- Via `net.snowflake.client.jdbc.SnowflakeBasicDataSource`:

  Copy code

  ```
  SnowflakeBasicDataSource ds = new SnowflakeBasicDataSource();
  // ... set URL, user, password ...
  List<HttpHeadersCustomizer> myCustomizers = new ArrayList<>();
  myCustomizers.add(new MyDynamicHeaderCustomizer());
  Properties props = new Properties();
  props.put(HttpHeadersCustomizer.HTTP_HEADER_CUSTOMIZERS_PROPERTY_KEY, myCustomizers);
  ds.setConnectionProperties(props);
  ```
- Via `java.sql.DriverManager`:

  Copy code

  ```
  Properties props = new Properties();
  // ... set user, password ...
  List<HttpHeadersCustomizer> myCustomizers = new ArrayList<>();
  myCustomizers.add(new MyDynamicHeaderCustomizer());
  props.put(HttpHeadersCustomizer.HTTP_HEADER_CUSTOMIZERS_PROPERTY_KEY, myCustomizers);
  Connection conn = DriverManager.getConnection(jdbcUrl, props);
  ```

## Troubleshooting tips

### Ensure properties are set correctly

The `DriverManager.getConnection()` method reads only the values of the
Properties parameter that match specific, predefined names (“password”, “warehouse”, etc.). If you
misspell a property name, or include extra properties, the driver ignores those properties without issuing an
error or warning message. This can make it difficult to detect minor misspellings.

### Use the right values for connection string and account

If you can’t establish a connection, verify that you are specifying the account identifier correctly in the JDBC connection
string. For more information about finding your account identifier, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).
