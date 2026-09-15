# SHOW PARAMETERS

Lists all the account, session, and object parameters that can be set, as well as the current and default values for each parameter:

- Account parameters can only be set at the account level.
- Session parameters can be set at the account, user, and session level.
- Object parameters can be set at the account and object level.

If a parameter has been explicitly set, the output of this command also shows the level at which the parameter has been set.

For descriptions of the different parameter types, as well as detailed descriptions for each parameter, see [Parameters](/sql-reference/parameters).

## Syntax

Copy code

```
SHOW PARAMETERS
  [ LIKE '<pattern>' ]
  [ { IN | FOR } {
        { SESSION | ACCOUNT }
      | { USER | WAREHOUSE | DATABASE | SCHEMA | TASK } [ <name> ]
      | TABLE [ <table_or_view_name> ]
    } ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN | FOR`
:   `IN ...` or `FOR ...` specifies the scope of the command, which determines the parameters that are returned:

    `SESSION`
    :   Returns all the session parameters and their settings for the current session. A user can change these parameters for their session
        using [ALTER SESSION](/sql-reference/sql/alter-session).

    `ACCOUNT`
    :   Returns a list of the account, session, and object parameters that can be set at the account level. A user with the ACCOUNTADMIN role
        (i.e. account administrator) can change these parameters via [ALTER ACCOUNT](/sql-reference/sql/alter-account). For more information, see
        [Parameter management](/user-guide/admin-account-management).

    `USER [ name ]`
    :   Returns a list of the session parameter defaults that are set for the specified user (or the current user) each time the user
        logs in.

        - If no user is specified, the command returns results for the current user.
        - An administrator with the appropriate user privileges can change the session parameter defaults for a user using [ALTER USER](/sql-reference/sql/alter-user).
        - Individual users can also change their session parameter defaults using [ALTER USER](/sql-reference/sql/alter-user).

    `WAREHOUSE | DATABASE | SCHEMA | TASK [ name ]`
    :   Returns the object parameters that can be set for the current/specified object. Users with the appropriate privileges can change these
        parameters using the corresponding [ALTER <object>](/sql-reference/sql/alter) command.

    `TABLE [ table_or_view_name ]`
    :   Returns the object parameters that can be set for the specified table or view. Users with the appropriate privileges can change these
        parameters using the [ALTER TABLE](/sql-reference/sql/alter-table) command.

        Use `TABLE` as the domain for all table-like objects, such as tables, views, and materialized views.

    Default: `SESSION`

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Show all the session parameters that can be set for the current session:

> Copy code
>
> ```
> SHOW PARAMETERS;
>
> +-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> | key                                 | value                            | default                          | level   | description                                                                                                                                                                         |
> |-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | ABORT_DETACHED_QUERY                | false                            | false                            | SESSION | If true, Snowflake will automatically abort queries when it detects that the client has disappeared.                                                                                |
> | AUTOCOMMIT                          | true                             | true                             | SESSION | The autocommit property determines whether is statement should to be implicitly                                                                                                     |
> |                                     |                                  |                                  |         | wrapped within a transaction or not. If autocommit is set to true, then a                                                                                                           |
> |                                     |                                  |                                  |         | statement that requires a transaction is executed within a transaction                                                                                                              |
> |                                     |                                  |                                  |         | implicitly. If autocommit is off then an explicit commit or rollback is required                                                                                                    |
> |                                     |                                  |                                  |         | to close a transaction. The default autocommit value is true.                                                                                                                       |
> | AUTOCOMMIT_API_SUPPORTED            | true                             | true                             |         | Whether autocommit feature is enabled for this client. This parameter is for                                                                                                        |
> |                                     |                                  |                                  |         | Snowflake use only.                                                                                                                                                                 |
> | BINARY_INPUT_FORMAT                 | HEX                              | HEX                              |         | input format for binary                                                                                                                                                             |
> | BINARY_OUTPUT_FORMAT                | HEX                              | HEX                              |         | display format for binary                                                                                                                                                           |
> | CLIENT_SESSION_KEEP_ALIVE           | false                            | false                            |         | If true, client session will not expire automatically                                                                                                                               |
> | DATE_INPUT_FORMAT                   | AUTO                             | AUTO                             |         | input format for date                                                                                                                                                               |
> | DATE_OUTPUT_FORMAT                  | YYYY-MM-DD                       | YYYY-MM-DD                       |         | display format for date                                                                                                                                                             |
> | ERROR_ON_NONDETERMINISTIC_MERGE     | true                             | true                             |         | raise an error when attempting to merge-update a row that joins many rows                                                                                                           |
> | ERROR_ON_NONDETERMINISTIC_UPDATE    | false                            | false                            |         | raise an error when attempting to update a row that joins many rows                                                                                                                 |
> | LOCK_TIMEOUT                        | 43200                            | 43200                            |         | Number of seconds to wait while trying to lock a resource, before timing out                                                                                                        |
> |                                     |                                  |                                  |         | and aborting the statement. A value of 0 turns off lock waiting i.e. the                                                                                                            |
> |                                     |                                  |                                  |         | statement must acquire the lock immediately or abort. If multiple resources                                                                                                         |
> |                                     |                                  |                                  |         | need to be locked by the statement, the timeout applies separately to each                                                                                                          |
> |                                     |                                  |                                  |         | lock attempt.                                                                                                                                                                       |
> | QUERY_TAG                           |                                  |                                  |         | String (up to 2000 characters) used to tag statements executed by the session                                                                                                       |
> | QUOTED_IDENTIFIERS_IGNORE_CASE      | false                            | false                            |         | If true, the case of quoted identifiers is ignored                                                                                                                                  |
> | ROWS_PER_RESULTSET                  | 0                                | 0                                |         | maxium number of rows in a result set                                                                                                                                               |
> | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS | 0                                | 0                                |         | Timeout in seconds for queued statements: statements will automatically be canceled if they are queued on a warehouse for longer than this amount of time; disabled if set to zero. |
> | STATEMENT_TIMEOUT_IN_SECONDS        | 0                                | 0                                |         | Timeout in seconds for statements: statements will automatically be canceled if they run for longer than this amount of time; disabled if set to zero.                              |
> | TIMESTAMP_DAY_IS_ALWAYS_24H         | false                            | true                             | SYSTEM  | If set, arithmetic on days always uses 24 hours per day,                                                                                                                            |
> |                                     |                                  |                                  |         | possibly not preserving the time (due to DST changes)                                                                                                                               |
> | TIMESTAMP_INPUT_FORMAT              | AUTO                             | AUTO                             |         | input format for timestamp                                                                                                                                                          |
> | TIMESTAMP_LTZ_OUTPUT_FORMAT         |                                  |                                  |         | Display format for TIMESTAMP_LTZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                 |
> | TIMESTAMP_NTZ_OUTPUT_FORMAT         | YYYY-MM-DD HH24:MI:SS.FF3        | YYYY-MM-DD HH24:MI:SS.FF3        | SYSTEM  | Display format for TIMESTAMP_NTZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                 |
> | TIMESTAMP_OUTPUT_FORMAT             | YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM | YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM | SYSTEM  | Default display format for all timestamp types.                                                                                                                                     |
> | TIMESTAMP_TYPE_MAPPING              | TIMESTAMP_NTZ                    | TIMESTAMP_NTZ                    | SYSTEM  | If TIMESTAMP type is used, what specific TIMESTAMP* type it should map to:                                                                                                          |
> |                                     |                                  |                                  |         |   TIMESTAMP_LTZ (default), TIMESTAMP_NTZ or TIMESTAMP_TZ                                                                                                                            |
> | TIMESTAMP_TZ_OUTPUT_FORMAT          |                                  |                                  |         | Display format for TIMESTAMP_TZ values. If empty, TIMESTAMP_OUTPUT_FORMAT is used.                                                                                                  |
> | TIMEZONE                            | America/Los_Angeles              | America/Los_Angeles              |         | time zone                                                                                                                                                                           |
> | TIME_INPUT_FORMAT                   | AUTO                             | AUTO                             |         | input format for time                                                                                                                                                               |
> | TIME_OUTPUT_FORMAT                  | HH24:MI:SS                       | HH24:MI:SS                       |         | display format for time                                                                                                                                                             |
> | TRANSACTION_ABORT_ON_ERROR          | false                            | false                            |         | If this parameter is true, and a statement issued within a non-autocommit                                                                                                           |
> |                                     |                                  |                                  |         | transaction returns with an error, then the non-autocommit transaction is                                                                                                           |
> |                                     |                                  |                                  |         | aborted. All statements issued inside that transaction will fail until an                                                                                                           |
> |                                     |                                  |                                  |         | commit or rollback statement is executed to close that transaction.                                                                                                                 |
> | TRANSACTION_DEFAULT_ISOLATION_LEVEL | READ COMMITTED                   | READ COMMITTED                   |         | The default isolation level when starting a starting a transaction, when no                                                                                                         |
> |                                     |                                  |                                  |         | isolation level was specified                                                                                                                                                       |
> | TWO_DIGIT_CENTURY_START             | 1970                             | 1970                             |         | For 2-digit dates, defines a century-start year.                                                                                                                                    |
> |                                     |                                  |                                  |         | For example, when set to 1980:                                                                                                                                                      |
> |                                     |                                  |                                  |         |   - parsing a string '79' will produce 2079                                                                                                                                         |
> |                                     |                                  |                                  |         |   - parsing a string '80' will produce 1980                                                                                                                                         |
> | UNSUPPORTED_DDL_ACTION              | ignore                           | ignore                           |         | The action to take upon encountering an unsupported ddl statement                                                                                                                   |
> | USE_CACHED_RESULT                   | true                             | true                             |         | If enabled, query results can be reused between successive invocations of the same query as long as the original result has not expired                                             |
> +-------------------------------------+----------------------------------+----------------------------------+---------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> ```
>
> Note that the output for this example does not include any of the account or object parameters because they cannot be set at the session level.
>
> For more information about account parameters, as well as setting parameters at the account level, see [Parameter management](/user-guide/admin-account-management).

Show all the object parameters that can be set for the specified warehouse (`testwh`):

> Copy code
>
> ```
> SHOW PARAMETERS IN WAREHOUSE testwh;
>
> +-------------------------------------+--------+---------+-------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> | key                                 | value  | default | level | description                                                                                                                                                                                                                   |
> |-------------------------------------+--------+---------+-------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | MAX_CONCURRENCY_LEVEL               | 8      | 8       |       | Concurrency level for SQL statements (i.e. queries and DML) executed by a warehouse cluster (used to determine when statements are queued or additional clusters are started). Small SQL statements count as a fraction of 1. |
> | STATEMENT_QUEUED_TIMEOUT_IN_SECONDS | 0      | 0       |       | Timeout in seconds for queued statements: statements will automatically be canceled if they are queued on a warehouse for longer than this amount of time; disabled if set to zero.                                           |
> | STATEMENT_TIMEOUT_IN_SECONDS        | 172800 | 172800  |       | Timeout in seconds for statements: statements are automatically canceled if they run for longer; if set to zero, max value (604800) is enforced.                                                                              |
> +-------------------------------------+--------+---------+-------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> ```

Show all the object parameters that can be set for the current database (`testdb`):

> Copy code
>
> ```
> USE DATABASE testdb;
>
> SHOW PARAMETERS IN DATABASE;
>
> +-----------------------------+-------+---------+-------+------------------------------------------------------------------+
> | key                         | value | default | level | description                                                      |
> |-----------------------------+-------+---------+-------+------------------------------------------------------------------|
> | DATA_RETENTION_TIME_IN_DAYS | 1     | 1       |       | number of days to retain the old version of deleted/updated data |
> +-----------------------------+-------+---------+-------+------------------------------------------------------------------+
> ```
