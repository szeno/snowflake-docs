# Feb 26, 2025: Generating connection settings for a client, driver, library, or third-party application

We are pleased to announce that you can now use Snowsight to generate the connection settings for a client, driver,
library, or third-party application.

You can use the new **Account Details** dialog to generate a connection string for the ODBC or JDBC driver or settings in
TOML file format for Snowflake CLI, Snowflake Python APIs, or the Snowflake Connector for Python. The generated configuration information
includes the following:

- Your account identifier
- Settings for authenticating to Snowflake
- The warehouse, database, and schema to use for the session

The **Account Details** dialog also provides quick access to the SQL commands that you can execute to get the settings yourself
(for example, if you need to specify the settings in a format other than a connection string or a TOML file).

For more information, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).
