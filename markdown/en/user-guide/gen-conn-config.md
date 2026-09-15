# Configuring a client, driver, library, or third-party application to connect to Snowflake

To configure a client, driver, library, or third-party application to connect to Snowflake, you must specify your Snowflake
account identifier. In addition, you might need to specify the warehouse, database, schema, and role that should be used.

You can find this information in Snowsight or by executing SQL commands:

- [Using Snowsight to get connection settings](#label-client-config-settings-snowsight)
- [Using SQL commands to get connection settings](#label-client-config-settings-sql)

## Using Snowsight to get connection settings

To get the settings that you can use to configure a client, driver, library, or third-party application:

1. [Sign in](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to Snowsight.
2. Open the user menu by selecting your user name.

   ![Account menu](/static/images/snowsight/snowsight-gs-user-menu.png)
3. From the user menu, select **Connect a tool to Snowflake** to display the **Account Details** dialog.

   Tip

   You can also display the account details from the [account selector](/user-guide/ui-snowsight-gs#label-snowsight-account-details).
4. Select one of the following tabs:

   - If your client, driver, library, or third-party application supports using a TOML configuration file (for example,
     [Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli),
     [Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake#label-snowflake-python-connect-config-file), or the
     [Snowflake Connector for Python](/developer-guide/python-connector/python-connector-connect#label-python-connection-toml):

     1. Select the **Config file** tab.
     2. To specify a warehouse in the configuration file, select the warehouse from the **Warehouse** menu.
     3. To specify a database and schema in the configuration file, use the **Database** menu to select the database
        and schema.
     4. From the **Connection Method** menu, select the method that you plan to use to authenticate:

        - To use [browser-based single sign-on (SSO)](/user-guide/admin-security-fed-auth-use#label-browser-based-sso), select **Web Browser**.
        - To use a password, select **Password**.

        Note

        Clients, drivers, libraries, and third-party applications support additional authentication methods not listed in
        the menu. For information, see [Securing Snowflake](/guides-overview-secure).
     5. Select the copy icon (![For assistive technology, the copy button.](/static/images/snowsight/snowsight-query-copy.png)) to copy the content for the configuration file.

     Note

     For the [Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake#label-snowflake-python-connect-config-file), underscores are not supported in the
     `account` setting. If the account identifier includes underscores, replace them with dashes.
   - If your client, driver, library, or third-party application supports specifying a connection string (for example,
     the [ODBC Driver](/developer-guide/odbc/odbc-parameters#label-odbc-connection-string), [JDBC Driver](/developer-guide/jdbc/jdbc-configure#label-jdbc-connection-string),
     [Go Snowflake Driver](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Connection_String), or
     [.NET Driver](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/Connecting.md)):

     1. Select the **Connectors/Drivers** tab.
     2. From the **Select Connector or Driver** menu, select the driver that you want to use.
     3. To specify a warehouse in the connection string, select the warehouse from the **Warehouse** menu. (Note that this menu
        is not present for ODBC and .NET.)
     4. To specify a database and schema in the connection string, use the **Database** menu to select the database
        and schema.
     5. From the **Connection Method** menu, select the method that you plan to use to authenticate:

        - To use [browser-based single sign-on (SSO)](/user-guide/admin-security-fed-auth-use#label-browser-based-sso), select **Web Browser**.
        - To use a password, select **Password**.

        Note

        Clients, drivers, libraries, and third-party applications support additional authentication methods not listed in
        the menu. For information, see [Securing Snowflake](/guides-overview-secure).
     6. Select the copy icon (![For assistive technology, the copy button.](/static/images/snowsight/snowsight-query-copy.png)) to copy the resulting connection string.
   - To execute SQL commands to get the configuration information:

     1. Select the **SQL Commands** tab.
     2. Select the copy icon (![For assistive technology, the copy button.](/static/images/snowsight/snowsight-query-copy.png)) next to the command that provides the information that you need, paste the
        command into a worksheet, and execute the command.

## Using SQL commands to get connection settings

You can execute SQL commands to get the following information needed to configure your client, driver, library, or application:

| Setting | SQL command |
| --- | --- |
| Account identifier for the current account | - To get the `organization_name-account_name` form of your account identifier:   Copy code  ``` SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME(); ```   - To get the [account locator](/user-guide/admin-account-identifier#label-account-locator) form of your account identifier:   Copy code  ``` SELECT CURRENT_ACCOUNT(); ``` |
| Current user name | Copy code  ``` SELECT CURRENT_USER(); ``` |
| Current role | Copy code  ``` SELECT CURRENT_ROLE(); ``` |
| Current region | Copy code  ``` SELECT CURRENT_REGION(); ``` |
| Current warehouse | Copy code  ``` SELECT CURRENT_WAREHOUSE(); ``` |
| Current database | Copy code  ``` SELECT CURRENT_DATABASE(); ``` |
| Current schema | Copy code  ``` SELECT CURRENT_SCHEMA(); ``` |

Expand

Show lessSee more

## Account formats used by clients and drivers

For different clients and drivers, you use different syntaxes for specifying your account.

In general, you should use the variation that includes the organization name (`orgname`) and account name
(`account_name`).

One exception to this rule is when you’re using the [Client Redirect](/user-guide/client-redirect) feature. If you’re
using this feature, replace the name of the account (`account_name`) with the name of the connection
(`connection_name`). For examples of this syntax, see [Using a connection URL](/user-guide/client-redirect#label-using-a-connection-url).

To configure a private connection to the Snowflake service, add `.privatelink` to either the account name or the account
locator syntax. To determine which value you should use to connect to Snowflake when using private connectivity, call the
[SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function in your Snowflake account.

If you need to use the account locator, you might also need to specify the cloud region ID, the cloud, and the level of government
compliance as additional segments after the account locator. For the format to use, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator). In the
examples below, `account_locator_with_additional_segments` represents the account location with any additional segments
that are required.

Snowflake CLI:
:   - Account name: `snow sql --account orgname-account_name`
    - Account locator: `snow sql --account account_locator_with_additional_segments`

    You can also specify this information in the `account` parameter for the connection in the Snowflake CLI `config.toml` configuration file.

    For additional information, see [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect).

SnowSQL:
:   - Account name: `snowsql -a orgname-account_name`
    - Account locator: `snowsql -a account_locator_with_additional_segments`

    For additional information, see [Connection syntax](/user-guide/snowsql-start#label-connection-syntax).

JDBC:
:   - Account name: `jdbc:snowflake://orgname-account_name.snowflakecomputing.com/?connection_params`
    - Account locator: `jdbc:snowflake://account_locator_with_additional_segments.snowflakecomputing.com/?connection_params`

    For additional information, see [JDBC Driver connection string](/developer-guide/jdbc/jdbc-configure#label-jdbc-connection-string).

ODBC:
:   - Account name:

      - Server: `orgname-account_name.snowflakecomputing.com`
    - Account locator:

      - Server: `account_locator_with_additional_segments.snowflakecomputing.com}`

    For additional information, see [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters).

Python:
:   - Account name:

      - Set the `ACCOUNT` parameter value as `orgname-account_name`.
    - Account locator:

      - Set the `ACCOUNT` parameter value as `account_locator_with_additional_segments`.

    For additional information, see [Connecting to Snowflake with the Python Connector](/developer-guide/python-connector/python-connector-connect).

.Net:
:   - Account name:

      - Set the `ACCOUNT` parameter value as `orgname-account_name`.
      - Set the `HOST` parameter value as the default (`.snowflakecomputing.com`).
    - Account locator:

      - Set the `ACCOUNT` parameter value as `account_locator_with_additional_segments`.
      - Set the `HOST` parameter value as the default `.snowflakecomputing.com`. Specify if your Snowflake account is not
        in the `us-west` region.

    For additional information, see
    [Connecting](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/Connecting.md).

Golang:
:   - Account name: `db, err := sql.Open("snowflake", "jsmith:mypassword@orgname-account_name/mydb/testschema?warehouse=mywh")`
    - Account locator: `sql.Open("snowflake", "jsmith:mypassword@account_locator_with_additional_segments/mydb/testschema?warehouse=mywh")`

    For additional information, see
    [Connection String](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#hdr-Connection_String).

node.js:
:   - Account name: Set the `ACCOUNT` parameter value as `orgname-account_name`.
    - Account locator: Set the `ACCOUNT` parameter value as `account_locator_with_additional_segments`.

    For additional information, see [Managing connections](/developer-guide/node-js/nodejs-driver-connect).

Spark (connector):
:   - Account name: Same as JDBC
    - Account locator: Same as JDBC

    For additional information, see [Setting Configuration Options for the Connector](/user-guide/spark-connector-use#label-spark-options).

Spark (Databricks):
:   - Account name: `{Account URL for Snowflake account}`
    - Account locator: `{Account Locator URL for Snowflake account}`

    For additional information, see [Configuring Snowflake for Spark in Databricks](/user-guide/spark-connector-databricks).

Spark (Qubole):
:   - Account name: Set the **Host Address** field value as `orgname-account_name.snowflakecomputing.com`.
    - Account locator: Set the **Host Address** field value as
      `account_locator_with_additional_segments.snowflakecomputing.com`.

    For additional information, see [Configuring Snowflake for Spark in Qubole](/user-guide/spark-connector-qubole).

PHP:
:   - Account name:

      - Set the `ACCOUNT` parameter value as `orgname-account_name`.
      - Leave the `REGION` parameter value blank for all regions.
    - Account locator:

      - Set the `ACCOUNT` parameter value as `account_locator`.
      - Set the `REGION` parameter value if your Snowflake account is not in the `us-west` region.

    For additional information, see
    [Connecting to the Snowflake database](https://github.com/snowflakedb/pdo_snowflake/blob/master/README.rst#connecting-to-the-snowflake-database).

SQLAlchemy:
:   - Account name: `snowflake://user_login_name:password@orgname-account_name`
    - Account locator: `snowflake://user_login_name:password@account_locator_with_additional_segments`

    For additional information, see [Using the Snowflake SQLAlchemy toolkit with the Python Connector](/developer-guide/python-connector/sqlalchemy).

## Additional configuration steps

The next topics cover specific areas of configuring a connection:

- [Allowing Host names](/user-guide/hostname-allowlist)
- [OCSP Configuration](/user-guide/ocsp)
