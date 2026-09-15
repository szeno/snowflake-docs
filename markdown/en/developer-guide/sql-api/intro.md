# Introduction to the SQL API

The Snowflake SQL API is a REST API that you can use to access and update data in a Snowflake database. You can use
this API to develop custom applications and integrations that:

- Perform queries.
- Manage your deployment (e.g. provision users and roles, create tables, etc.).

## Capabilities of the SQL API

The Snowflake SQL API provides operations that you can use to:

- Submit SQL statements for execution.
- Check the status of the execution of a statement.
- Cancel the execution of a statement.
- Fetch query results concurrently.

You can use this API to execute [standard queries](/sql-reference/constructs) and most
[DDL](/sql-reference/sql-ddl-summary) and [DML](/sql-reference/sql-dml) statements.
See [Limitations of the SQL API](#label-sql-api-limitations) for the types of statements that are not supported.

For queries, the SQL API returns data in partitions. Snowflake determines the number of partitions returned and the size of each partition.

The endpoint for the SQL API (`/api/v2/statements`) is protected by the [network policies](/user-guide/network-policies)
that restrict access to the account where the API is enabled.

Note

The [AUTOCOMMIT](/sql-reference/parameters#label-autocommit) parameter must be set to `TRUE` per query or statement level, regardless of the
value set at the user or account level.

## Limitations of the SQL API

The SQL API has the following limitations:

- The following commands are not supported:
  - The [PUT](/sql-reference/sql/put) command (in Snowflake SQL)
  - The [GET](/sql-reference/sql/get) command (in Snowflake SQL)

The following commands and statements are supported only within a
[request that specifies multiple statements](/developer-guide/sql-api/submitting-multiple-statements):

> - Commands that perform explicit transactions, including:
>
>   - [BEGIN](/sql-reference/sql/begin)
>   - [COMMIT](/sql-reference/sql/commit)
>   - [ROLLBACK](/sql-reference/sql/rollback)
> - Commands that change the context of the session, including:
>
>   - [USE <object>](/sql-reference/sql/use)
>   - [ALTER SESSION](/sql-reference/sql/alter-session)
> - Statements that set session variables.
> - Statements that create temporary tables and stages (tables and stages that are available only in the current session).

The SQL API does not support certain types of stored procedures. You might encounter errors, for example, when trying to call Python and Java/Scala stored procedures
that return a `resultset` in Arrow format. Even if you don’t directly call these stored procedures from the SQL API, but call another stored procedure,
such as SQL, errors might result when the outer procedure internally calls an inner Python or Java/Scala stored procedure.

## Billing considerations when using the SQL API

The SQL API leverages the cloud services layer when fetching some query results. For more information about cloud services,
see [Cloud Services Credit Usage](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage).
