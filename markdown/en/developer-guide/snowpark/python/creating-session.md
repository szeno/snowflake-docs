# Creating a Session for Snowpark Python

To use Snowpark in your application, you need to create a session. For convenience in writing code, you can also import the names
of packages and objects.

## Creating a Session

The first step in using the library is establishing a session with the Snowflake database.

Import the Session class.

Copy code

```
from snowflake.snowpark import Session
```

To authenticate, you use the same mechanisms that the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector-example) supports.

Establish a session with a Snowflake database using the same parameters (for example, the account name, user name, etc.) that you use in the `connect` function in the Snowflake
Connector for Python. For more information, see the [parameters for the connect function](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods) in the Python Connector API documentation.

## Connect by using the `connections.toml` file

To add credentials in a connections configuration file:

1. In a text editor, open the `connections.toml` file for editing. For example, to open the file in the Linux **vi** editor:

   Copy code

   ```
   vi connections.toml
   ```
2. Add a new Snowflake connection definition.

   You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
   [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

   For example, to add a Snowflake connection called `myconnection` with the account `myaccount`,
   user `johndoe`, and password credentials, as well as database information,
   add the following lines to the configuration file:

   Copy code

   ```
   [myconnection]
   account = "myaccount"
   user = "jdoe"
   password = "******"
   warehouse = "my-wh"
   database = "my_db"
   schema = "my_schema"
   ```

   Connection definitions support the same configuration options available in the
   [snowflake.connector.connect](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect) method.
3. Optional: Add more connections, as shown:

   Copy code

   ```
   [myconnection_test]
   account = "myaccount"
   user = "jdoe-test"
   password = "******"
   warehouse = "my-test_wh"
   database = "my_test_db"
   schema = "my_schema"
   ```
4. Save changes to the file.
5. In your Python code, supply connection name to `snowflake.connector.connect` and then add it to `session`, similar to the following:

   Copy code

   ```
   session = Session.builder.config("connection_name", "myconnection").create()
   ```

For more information, see [configuration file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).

## Connect by specifying connection parameters

Construct a dictionary (`dict`) containing the names and values of these parameters
(e.g. `account`, `user`, `role`, `warehouse`, `database`, `schema`, etc.).

To create the session:

1. Create a Python dictionary (`dict`) containing the names and values of the parameters for connecting to Snowflake.
2. Pass this dictionary to the `Session.builder.configs` method to return a builder object that has these connection parameters.
3. Call the `create` method of the `builder` to establish the session.

The following example uses a `dict` containing connection parameters to create a new session:

Copy code

```
connection_parameters = {
  "account": "<your snowflake account>",
  "user": "<your snowflake user>",
  "password": "<your snowflake password>",
  "role": "<your snowflake role>",  # optional
  "warehouse": "<your snowflake warehouse>",  # optional
  "database": "<your snowflake database>",  # optional
  "schema": "<your snowflake schema>",  # optional
}

new_session = Session.builder.configs(connection_parameters).create()
```

For the `account` parameter, use your [account identifier](/user-guide/admin-account-identifier).
Note that the account identifier does not include the snowflakecomputing.com suffix.

Note

This example shows you one way to create a session but there are several other ways that you can connect, including:
the default authenticator, single sign-on (SSO), multi-factor authentication (MFA), key pair authentication,
using a proxy server, and OAuth. For more information, see [Connecting to Snowflake with the Python Connector](/developer-guide/python-connector/python-connector-connect).

## Using single sign-on (SSO) through a web browser

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure
your client application to use browser-based SSO for authentication.

Construct a dictionary (`dict`) containing the names and values of these parameters
(e.g. `account`, `user`, `role`, `warehouse`, `database`, `authenticator`, etc.).

To create the session:

1. Create a Python dictionary (`dict`) containing the names and values of the parameters for connecting to Snowflake.
2. Pass this dictionary to the `Session.builder.configs` method to return a builder object that has these connection parameters.
3. Call the `create` method of the `builder` to establish the session.

The following example uses a `dict` containing connection parameters to create a new session. Set the `authenticator` option to `externalbrowser`.

Copy code

```
from snowflake.snowpark import Session
connection_parameters = {
  "account": "<your snowflake account>",
  "user": "<your snowflake user>",
  "role":"<your snowflake role>",
  "database":"<your snowflake database>",
  "schema":"<your snowflake schema",
  "warehouse":"<your snowflake warehouse>",
  "authenticator":"externalbrowser"
}
session = Session.builder.configs(connection_parameters).create()
```

## Closing a Session

If you no longer need to use a session for executing queries and you want to
cancel any queries that are currently running, call the close method of the Session object.
For example:

Copy code

```
new_session.close()
```
