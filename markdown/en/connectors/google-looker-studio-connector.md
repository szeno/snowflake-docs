# Use the Snowflake Connector for Google Looker Studio

This topic describes how to use the Snowflake Connector for Google Looker Studio.

The Snowflake Connector for Google Looker Studio provides an interface to [Google Looker Studio](https://cloud.google.com/looker-studio), a data visualization software that you can use to
transform your raw data into the metrics and dimensions needed to create reports and dashboards.
This connector is available to users with a Google account as a Partner Connector within Google Looker Studio.

## Authentication methods

The Snowflake Connector for Google Looker Studio supports the following authentication methods for connecting to Snowflake:

- Username and password
- Key-pair authentication

With the username and password authentication method, users can authenticate the connection by providing their Snowflake credentials.
The key-pair method enables a more secure connection by using a private key for authentication instead of a password. To learn more about configuring
key-pair authentication in a Snowflake database, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

When configuring the public key for a user in the Snowflake database, ensure that you meet the following requirements:

- The key does not include the strings `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----`.
- All newline characters are removed from the public key. This is required for proper authentication.

Note

Because of its design for system-to-system communication, the connector is not compatible with interactive authentication methods,
such as multi-factor authentication (MFA) with Duo Push.

## Connect your Snowflake account to Google Looker Studio

1. Sign in to [Google Looker Studio](https://cloud.google.com/looker-studio).
2. Click **+**, and then select **Data Source**.
3. Under the **Partner Connectors** section, select the Snowflake connector (the connector with the Snowflake logo).
4. If required, authorize Google Looker Studio to use this community connector.
5. Enter the following Snowflake user credentials to connect to Snowflake:

   - Username
   - Password or private key
6. Click **Submit**.
7. Provide the following parameters required to connect to your Snowflake account:

   - Account URL
   - Role
   - Warehouse
   - Database
   - Schema
   - SQL query

   Note

   The SQL query cannot end with a semicolon.
8. Click **Connect**.

   A page containing data source fields is displayed.
9. To visualize your data, click **Create Report** or **Explore**.

Note

If you have trouble connecting to your Snowflake account, use the following procedure to revoke access, and then try to connect again.

### Revoke access

1. Sign in to [Google Looker Studio](https://cloud.google.com/looker-studio).
2. Select **Data Sources**.
3. Browse or search for the Snowflake connector, and then click **More options**.
4. Click **Revoke access**.

## Mapping Snowflake data types to Looker Studio data types

The connector maps your Snowflake database data types to a [unified set of data types](https://support.google.com/datastudio/answer/9514333) as follows:

| Snowflake data type | Google Looker Studio data type |
| --- | --- |
| `BOOLEAN` | `BOOLEAN` |
| `FIXED` | `NUMBER` |
| `REAL` | `NUMBER` |
| `BINARY` | `TEXT` |
| `TEXT` | `TEXT` |
| `GEOGRAPHY` | `TEXT` \* |
| `DATE` | `YEAR_MONTH_DAY` |
| `TIMESTAMP_LTZ` | `YEAR_MONTH_DAY_SECOND` |
| `TIMESTAMP_NTZ` | `YEAR_MONTH_DAY_SECOND` |
| `TIMESTAMP_TZ` | `YEAR_MONTH_DAY_SECOND` |
| `TIME` | `TEXT` |
| `OBJECT` | `TEXT` \* |
| `VARIANT` | `TEXT` \* |
| `ARRAY` | `TEXT` \* |

Expand

Show lessSee more

[\*]
Google Looker Studio does not support complex spatial types, so they are represented as text. The text format allows you to freely process data in custom visualizations.

Note

If Google Looker Studio encounters a column in a table or query of an unsupported type, it does not create a field for that
column.

For more information about Snowflake data types, see [SQL data types reference](/sql-reference-data-types).

## Network policy access

Connections from Google Looker Studio to Snowflake come from ephemeral Google servers with no fixed IP addresses. If your
network uses [network policies](/user-guide/network-policies), you may need to open up the policy for the Looker Studio user to either allow *all* IP addresses
(0.0.0.0/0) or use [this shell script](https://gist.github.com/n0531m/f3714f6ad6ef738a3b0a) to get a list of possible Google Cloud IP addresses with subnets.

## Identifying Connector queries in your query history

The Snowflake Connector for Google Looker Studio uses user-provided SQL statements as an inner SELECT statement for each
generated query to a database. Therefore, your query history may contain optimized queries that differ from
the queries you entered when configuring a data source.

In your query history, the queries from the connector will include this inner SELECT statement.

## Supported SQL queries

Only the `SELECT`, `SHOW`, and `DESCRIBE` SQL statements are supported. The connector only supports specifying a single SQL statement as the query; it does not support selecting tables and views from a list.

## Limitations

- The connector does not support the use of encrypted private keys for key-pair authentication.
- Because of its design for system-to-system communication, the connector is not compatible with interactive authentication methods, such as MFA with Duo Push.
- The current sign-in flow only supports a single sign-in (username and password or private key), which only works for different accounts if
  all accounts use the same username and password or private key. The connector does not support using multiple sign-ins to the same or different Snowflake accounts.
- Google limits the returned data set to 1 million rows and 50 MB of data. Unexpected errors may occur when you try to
  return more data.
- Column headers (field names) must use ASCII characters only; non-ASCII characters are not supported.
- Reports containing `REGEXP_PARTIAL_MATCH` and `REGEXP_EXACT_MATCH` operators are not optimized by [pushdown filters](https://developers.google.com/datastudio/connector/filters)
  because Snowflake and Google Looker Studio support different regexp types.
- [Pushdown filters](https://developers.google.com/datastudio/connector/filters) are not supported for the `SHOW` and `DESCRIBE` statements and for `DATE`, `TIME`, and `TIMESTAMP` columns.

Note

If MFA is enabled for the Snowflake username used in the connector, it can lead to excessive Duo Push notifications, which can cause inconvenience to users.
This behavior arises because the connector may trigger multiple authentication requests during connection attempts.
To mitigate this issue, consider using the key-pair authentication method instead of username and password.
