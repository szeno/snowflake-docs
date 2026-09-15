# SHOW VERSIONS IN APPLICATION PACKAGE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the versions defined in the specified application package.

See also:
:   [ALTER APPLICATION](/sql-reference/sql/alter-application), [CREATE APPLICATION](/sql-reference/sql/create-application), [DESCRIBE APPLICATION](/sql-reference/sql/desc-application), [DROP APPLICATION](/sql-reference/sql/drop-application)

## Syntax

Copy code

```
SHOW VERSIONS [ LIKE <pattern> ]
  IN APPLICATION PACKAGE <name>;
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN APPLICATION PACKAGE name`
:   Specifies the identifier for the application package whose versions you want to view.

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

## Example

Copy code

```
SHOW VERSIONS IN APPLICATION PACKAGE hello_snowflake_app;
```

```
+----------------+-------+---------+---------+-------------------------------+------------+-----------+-------------+-------+---------------+
| version        | patch | label   | comment | created_on                    | dropped_on | log_level | trace_level | state | review_status |
|----------------+-------+---------+---------+-------------------------------+------------+-----------+-------------+-------+---------------|
| V1_0           |     0 | NULL    | NULL    | 2023-05-10 17:11:47.696 -0700 | NULL       | OFF       | OFF         | READY | NOT_REVIEWED  |
+----------------+-------+---------+---------+-------------------------------+------------+-----------+-------------+-------+---------------+
```
