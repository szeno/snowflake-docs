# Apr 30, 2025: Programmatic access tokens

You can now generate and use programmatic access tokens to authenticate to the following Snowflake endpoints:

- [Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api).
- [The Snowflake SQL API](/developer-guide/sql-api/index).
- [The Snowflake Catalog SDK](/user-guide/tables-iceberg-catalog).

Note

Using programmatic access tokens to authenticate to
[Snowpark Container Services](/developer-guide/snowpark-container-services/working-with-services) endpoints is not yet
supported.

You can also use a programmatic access token as a replacement for a password in:

- [Snowflake drivers](/developer-guide/drivers).
- [Third-party applications that connect to Snowflake](/user-guide/ecosystem) (such as Tableau and PowerBI).
- Snowflake APIs and libraries (such as the [Snowpark API](/developer-guide/snowpark/index) and the
  [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-overview).
- Snowflake command-line clients (such as the [Snowflake CLI](/developer-guide/snowflake-cli/index) and
  [SnowSQL](/user-guide/snowsql).

You can generate programmatic access tokens for human users (users with TYPE=PERSON) as well as for service users (users with
TYPE=SERVICE).

For more information, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).
