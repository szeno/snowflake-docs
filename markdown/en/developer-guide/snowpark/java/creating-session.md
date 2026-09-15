# Creating a Session for Snowpark Java

To use Snowpark in your application, you need to create a session. For convenience in writing code, you can also import the names
of packages and objects.

## Importing Names from Packages for Snowpark

The Snowpark API provides a number of classes in different packages. For convenience, you can import these packages to avoid
having to use qualified names for classes.

For example:

- The [com.snowflake.snowpark\_java package](../reference/java/com/snowflake/snowpark_java/package-summary.html) contains the main classes for the Snowpark API. To import the names in this package:

  Copy code

  ```
  import com.snowflake.snowpark_java.*;
  ```
- The [com.snowflake.snowpark\_java.types package](../reference/java/com/snowflake/snowpark_java/types/package-summary.html) defines classes that you can use to define schemas for semi-structured data.

  Copy code

  ```
  import com.snowflake.snowpark_java.types.*;
  ```

## Creating a Session for Snowpark

The first step in using the library is establishing a session with the Snowflake database. To create a session, use the methods in
the `SessionBuilder` class. You can access a `SessionBuilder` object by calling the static `builder` method in
the `Session` class:

Copy code

```
import com.snowflake.snowpark_java.*;

...
// Get a SessionBuilder object.
SessionBuilder builder = Session.builder();
```

To provide the details to establish a session with a Snowflake database (for example, the account identifier, user name, etc.),
either create a properties file (a text file) or programmatically build a `Map` containing the properties.

In the properties file or `Map`, set the following properties:

- `URL`: Set this to the URL for your account in the form `https://account_identifier.snowflakecomputing.com`.

  See [Account identifiers](/user-guide/admin-account-identifier).

  If the account identifier contains underscores (`_`), replace those underscores with hyphens (`-`).
- Any additional JDBC parameters (see [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters) in the JDBC driver documentation) needed to connect
  to Snowflake (e.g. `USER`, `ROLE`, `WAREHOUSE`, `DB`, `SCHEMA`, etc.).

  Note

  To change the logging level (e.g. from `INFO` to `DEBUG`), see [Changing the logging settings](/developer-guide/snowpark/java/troubleshooting#label-snowpark-java-change-log-level).
- (Optional) `snowpark_request_timeout_in_seconds`: Set this to the maximum number of seconds that the Snowpark library
  should wait in the following cases:

  - Waiting for [dependencies to be uploaded to a stage](/developer-guide/snowpark/java/creating-udfs#label-snowpark-java-udf-inline-dependencies).
  - Waiting for an [asynchronous action](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-action-method-async) to complete.

  The default value of this property is 86400 seconds (1 day).

  Note

  This property was introduced in Snowpark 0.10.0.

To authenticate, you can use the same mechanisms that the JDBC Driver supports. For example, you can use:

- password-based authentication (by setting the `PASSWORD` property)
- [key-pair authentication](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication)
- [single sign-on (SSO)](/developer-guide/jdbc/jdbc-configure#label-jdbc-sso)

For key-pair authentication, you can either:

- Set the `PRIVATE_KEY_FILE` property to the path to the private key file.

  If the private key is encrypted, set the `PRIVATE_KEY_FILE_PWD` property to the passphrase for decrypting the key.
- Set the `PRIVATEKEY` property to the string value of the unencrypted private key from the private key file.
  (If the private key is encrypted, you must decrypt the key before setting it as the value of the `PRIVATEKEY` property.)

To create the session:

1. Set the properties in the `SessionBuilder` object.

   - If you created a properties file, pass the path to the properties file to the `configFile` method of the
     `SessionBuilder` object.
   - If you programmatically built a `Map` of the properties, pass the `Map` to the `configs` method of the
     `SessionBuilder` object.

   Both methods return a `SessionBuilder` object that has these properties.
2. Call the `create` method of the `SessionBuilder` object to establish the session.

The following is an example of a properties file that sets the basic parameters for connecting to a Snowflake database. The
example is set up to use key-pair authentication. Set `PRIVATE_KEY_FILE` to the path to the private key file. In addition,
if the private key is encrypted, you must set `PRIVATE_KEY_FILE_PWD` to the passphrase for decrypting the private key:

Copy code

```
# profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATE_KEY_FILE = </path/to/private_key_file.p8>
PRIVATE_KEY_FILE_PWD = <if the private key is encrypted, set this to the passphrase for decrypting the key>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

As an alternative, you can set the `PRIVATEKEY` property to the unencrypted private key from the private key file.

Copy code

```
# profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

The following example uses this properties file to create a new session:

Copy code

```
// Create a new session, using the connection properties
// specified in a file.
Session session = Session.builder().configFile("/path/to/properties/file").create();
```

The following example uses a Map to set the properties:

Copy code

```
import com.snowflake.snowpark_java.*;
import java.util.HashMap;
import java.util.Map;
...
// Create a new session, using the connection properties
// specified in a Map.
// Replace the <placeholders> below.
Map<String, String> properties = new HashMap<>();
properties.put("URL", "https://<account_identifier>.snowflakecomputing.com:443");
properties.put("USER", "<user name>");
properties.put("PRIVATE_KEY_FILE", "</path/to/private_key_file.p8>");
properties.put("PRIVATE_KEY_FILE_PWD", "<if the private key is encrypted, set this to the passphrase for decrypting the key>");
properties.put("ROLE", "<role name>");
properties.put("WAREHOUSE", "<warehouse name>");
properties.put("DB", "<database name>");
properties.put("SCHEMA", "<schema name>");
Session session = Session.builder().configs(properties).create();
```

## Closing a Session

If you no longer need to use a session for executing queries and you want to cancel any queries that are currently running, call
`close` method of the `Session` object. For example:

Copy code

```
// Close the session, cancelling any queries that are currently running, and
// preventing the use of this Session object for performing any subsequent queries.
session.close();
```
