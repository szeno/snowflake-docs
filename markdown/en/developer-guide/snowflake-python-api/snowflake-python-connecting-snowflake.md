# Connect to Snowflake with the Snowflake Python APIs

Before you can perform actions with the Snowflake Python APIs, you must define a connection to Snowflake. With the connection, you can
create a `Root` object for access to resources modeled by the API.

## Specify connection properties

You can define a connection to Snowflake using one of the following mechanisms:

- [Python dictionary](#label-snowflake-python-connect-dictionary)
- [Configuration file](#label-snowflake-python-connect-config-file)

### Connect using a Python dictionary

You can specify the values needed to connect to Snowflake by using a Python dictionary. When you connect, you pass this dictionary as an
argument to the function or method you’re using to connect:

Copy code

```
import os

CONNECTION_PARAMETERS = {
    "account": os.environ["snowflake_account_demo"],
    "user": os.environ["snowflake_user_demo"],
    "password": os.environ["snowflake_password_demo"],
    "role": "test_role",
    "database": "test_database",
    "warehouse": "test_warehouse",
    "schema": "test_schema",
}
```

### Connect using a configuration file

You can specify connection definitions in a [TOML configuration file](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml). This eliminates the need to
explicitly define a connection to Snowflake in your code.

You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
[Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

You can also configure the connection settings manually. For example, create a configuration file located at
`~/.snowflake/connections.toml`, and add connection settings similar to the following:

Copy code

```
[myconnection]
account = "test-account"
user = "test_user"
password = "******"
role = "test_role"
warehouse = "test_warehouse"
database = "test_database"
schema = "test_schema"
```

In this example, you define a Snowflake connection named `myconnection` with the account `test-account`, user `test_user`,
password credentials, and database information.

Note

Underscores are not supported in the `account` setting. If the [account identifier](/user-guide/admin-account-identifier)
includes underscores, replace them with dashes. For more information, see [Account name in your organization](/user-guide/admin-account-identifier#label-account-name).

Connection definitions support the same configuration options available in the
[Snowflake Python Connector](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).

## Connect and create a `Root` object

Using the connection properties you’ve specified, you can create a connection to Snowflake. With the connection, you can create a
Snowflake Python APIs `Root` object with which to begin using the API.

You can connect using one of the following objects:

- [A Snowpark Session object](#label-snowflake-python-connect-snowpark-session)
- [A Snowflake Python Connector Connection object](#label-snowflake-python-connect-connection)

### Connect with a Snowpark `Session`

If you’re using the [Snowpark API for Python](/developer-guide/snowpark/python/index), you can create a connection to Snowflake
by using its `snowflake.snowpark.Session` object.

The Snowpark Python library is not automatically installed as a dependency of `snowflake.core`. To connect to Snowflake using the
Snowpark `Session` object, follow these steps:

1. To install the `snowflake-snowpark-python` package, run the following command:

   Copy code

   ```
   pip install 'snowflake-snowpark-python>=1.5.0,<2.0.0'
   ```
2. To create a connection to Snowflake, run code similar to the following example:

   Copy code

   ```
   from snowflake.core import Root
   from snowflake.snowpark import Session

   session = Session.builder.config("connection_name", "myconnection").create()
   root = Root(session)
   ```

   In this example, the code creates a `Session` object using a connection definition named `myconnection`, which is specified in a
   configuration file. Using the resulting `Session` object, the code creates a `Root` object from which to use the API.

For more information about creating a `Session`, see [Creating a Session for Snowpark Python](/developer-guide/snowpark/python/creating-session).

### Connect with a Python Connector `Connection`

If you’re using the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector), you can create a connection
to Snowflake by using its `snowflake.connector.connect` function. The function returns a `Connection` object.

You don’t need to install the Python Connector library separately. The `snowflake-connector-python` package is installed automatically as
a dependency when you install the `snowflake` parent package.

Code in the following example creates a `Connection` object using a connection definition named `myconnection`, which is specified
in a configuration file. Using the resulting `Connection` object, the code creates a `Root` object from which to use the API:

Copy code

```
from snowflake.connector import connect
from snowflake.core import Root

connection = connect(connection_name="myconnection")
root = Root(connection)
```

For more information about the Snowflake Connector for Python API, see [Python Connector API](/developer-guide/python-connector/python-connector-api).

## Use the `Root` object

With a `Root` object [created from your connection to Snowflake](#label-snowflake-python-connect-connecting), you can access
objects and methods of the Snowflake Python APIs. The `Root` object is the root of the resource tree modeled by the API.
You use the `Root` object to interact with Snowflake objects represented by the API.

Code in the following example uses the `Root` object to access Snowflake objects in order to resume the task named `mytask`.
The task is in the schema named `myschema`, which is in the database named `mydb`. The code uses the `databases`,
`schemas`, and `tasks` methods to get an object that represents this task:

Copy code

```
tasks = root.databases["mydb"].schemas["myschema"].tasks
mytask = tasks["mytask"]
mytask.resume()
```
