# SHOW VIEWS

Lists the views, including secure views, for which you have access privileges. The command can be used to list views for the
current/specified database or schema, or across your entire account.

The output returns view metadata and properties, ordered lexicographically by database, schema, and view name. This is important to note
if you wish to filter the results using the provided filters.

See also:
:   [ALTER VIEW](/sql-reference/sql/alter-view) , [CREATE VIEW](/sql-reference/sql/create-view) , [DROP VIEW](/sql-reference/sql/drop-view) , [DESCRIBE VIEW](/sql-reference/sql/desc-view)

    [VIEWS view](/sql-reference/info-schema/views) (Information Schema)

## Syntax

Copy code

```
SHOW [ TERSE ] VIEWS [ LIKE '<pattern>' ]
                     [ IN { ACCOUNT | DATABASE [ <db_name> ] | [ SCHEMA ] [ <schema_name> ] | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> } ]
                     [ STARTS WITH '<name_string>' ]
                     [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Optionally returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`
    - `database_name`
    - `schema_name`

    Default: No value (all columns are included in the output)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN ACCOUNT | [ DATABASE ] db_name | [ SCHEMA ] schema_name | [ APPLICATION ] application_name | [ APPLICATION PACKAGE ] application_package_name`
:   Optionally specifies the scope of the command, which determines whether the command lists records only for the current/specified
    database or schema, or across your entire account:

    The `APPLICATION` and `APPLICATION PACKAGE` keywords are not required, but they specify the scope for the named Snowflake Native App.

    The `DATABASE` or `SCHEMA` keyword is not required; you can set the scope by specifying only the database or schema name.
    Likewise, the database or schema name is not required if the session currently has a database in use:

    - If `DATABASE` or `SCHEMA` is specified without a name and the session does not currently have a database in use, the
      parameter has no effect on the output.
    - If `SCHEMA` is specified with a name and the session does not currently have a database in use, the schema name must
      be fully qualified with the database name (e.g. `testdb.testschema`).

    Default: Depends on whether the session currently has a database in use:

    - Database: `DATABASE` is the default (i.e. the command returns the objects you have privileges to view in the database).
    - No database: `ACCOUNT` is the default (i.e. the command returns the objects you have privileges to view in your account).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The command output provides view properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | The timestamp at which the view was created. |
| name | The name of the view. |
| reserved | (Reserved for future use.) |
| kind | The kind of view, either `VIEW` or `MATERIALIZED_VIEW`. |
| database\_name | The name of the database in which the view exists. |
| schema\_name | The name of the schema in which the view exists. |
| owner | The owner of the view. |
| comment | Optional comment. |
| text | The text of the command that created the view (e.g. CREATE VIEW …). |
| is\_secure | True if the view is a secure view; false otherwise. |
| is\_materialized | True if the view is a materialized view; false otherwise. |
| owner\_role\_type | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| change\_tracking | Either `ON` or `OFF`. `ON` indicates enabled, and you query the change tracking data using streams or the CHANGES clause for SELECT statements. `OFF` indicates disabled, but you can optionally [enable](/user-guide/streams-manage) change tracking as needed. |

Expand

Show lessSee more

## Usage notes

- By design, the command output includes secure views, but does not provide certain information about these views unless you are using
  the role that has ownership of the view. To view details for secure views, you must use the role that owns the view or use the
  [VIEWS](/sql-reference/info-schema/views) view in the Information Schema.

- The output of this command might include objects with names like `SN_TEMP_OBJECT_n` (where `n` is a number). These are
  temporary objects that are created by the [Snowpark](/developer-guide/snowpark/index) library on behalf of the user.

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

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Show all views whose names start with `line` that you have privileges to see in the `mydb.public` schema:

> Copy code
>
> ```
> SHOW VIEWS LIKE 'line%' IN mydb.public;
>
> +-------------------------------+---------+----------+---------------+-------------+----------+---------+-------------------------------------------------------+-----------+-----------------+-----------------+-----------------+
> | created_on                    | name    | reserved | database_name | schema_name | owner    | comment | text                                                  | is_secure | is_materialized | change_tracking | owner_role_type |
> +-------------------------------+---------+----------+---------------+-------------+----------+---------+-------------------------------------------------------+-----------+-----------------+-----------------+-----------------+
> | 2019-05-24 18:41:14.247 -0700 | liners1 |          | MYDB          | PUBLIC      | SYSADMIN |         | create materialized views liners1 as select * from t; | false     | false           | on              | ROLE            |
> +-------------------------------+---------+----------+---------------+-------------+----------+---------+-------------------------------------------------------+-----------+-----------------+-----------------+-----------------+
> ```
