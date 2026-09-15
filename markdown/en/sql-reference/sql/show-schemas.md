# SHOW SCHEMAS

Lists the schemas for which you have access privileges, including dropped schemas that are still within the Time Travel retention period
and, therefore, can be undropped. The command can be used to list schemas for the current/specified database, or across your entire
account.

The output returns schema metadata and properties, ordered lexicographically by database and schema name. This is important to note if
you wish to filter the results using the provided filters.

See also:
:   [CREATE SCHEMA](/sql-reference/sql/create-schema) , [ALTER SCHEMA](/sql-reference/sql/alter-schema) , [DESCRIBE SCHEMA](/sql-reference/sql/desc-schema) , [DROP SCHEMA](/sql-reference/sql/drop-schema) , [UNDROP SCHEMA](/sql-reference/sql/undrop-schema)

    [SCHEMATA view](/sql-reference/info-schema/schemata) (Information Schema)

## Syntax

Copy code

```
SHOW [ TERSE ] SCHEMAS
  [ HISTORY ]
  [ LIKE '<pattern>' ]
  [ IN { ACCOUNT | DATABASE [ <db_name> ] | APPLICATION <application_name> | APPLICATION PACKAGE <application_package_name> } ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
  [ WITH PRIVILEGES <object_privilege> [ , <object_privilege> [ , ... ] ] ]
```

## Parameters

`TERSE`
:   Returns output containing only the following columns:

    - `created_on`
    - `name`
    - `kind`
    - `database_name`
    - `schema_name`

    Note that `kind` and `schema_name` always display `NULL` because `kind` is not applicable for schemas and
    `schema_name` is redundant with `name`.

    Default: No value (all columns are included in the output)

`HISTORY`
:   Includes dropped schemas that have not yet been purged (i.e. they are still within their respective Time Travel retention periods).
    If multiple versions of a dropped schema exist, the output displays a row for each version. The output also includes an additional
    `dropped_on` column, which displays:

    - Date and timestamp (for dropped schemas)
    - `NULL` (for active schemas).

    Default: No value (dropped schemas are not included in the output)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN { ACCOUNT | [ DATABASE ] [ db_name ] | APPLICATION application_name | APPLICATION PACKAGE application_package_name }`
:   Specifies the scope of the command, which determines whether the command lists records only for the current/specified database or
    across your entire account.

    The `APPLICATION` and `APPLICATION PACKAGE` keywords are not required, but they specify the scope for the named Snowflake Native App.

    The `DATABASE` keyword is not required; you can set the scope by specifying only the database name. Likewise, the database name
    is not required if the session currently has a database in use.

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

`WITH PRIVILEGES object_privilege [ , object_privilege [ , ... ] ]`
:   Optionally limits rows to objects for which the [active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles) for the current
    user has been granted all of the specified privileges in the list on the object.

    If a CREATE <object> privilege is included in the privileges list, the command excludes objects for which secondary roles have
    been granted privileges. This is because only the primary role has the authorization to create objects. For more information, see
    [Authorization through primary role and secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement).

`OBJECT_VISIBILITY`

> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> This property controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search) in the account,
> enabling users without explicit access privileges to find objects and request access.

## Usage notes

- When you specify the scope to either `APPLICATION` or the database named `SNOWFLAKE`, the `owner` column returns
  `SNOWFLAKE` as the owner for the schema named `LOCAL`. For example:

  Copy code

  ```
  SHOW SCHEMAS IN APPLICATION my_app;
  SHOW SCHEMAS IN DATABASE SNOWFLAKE;
  ```

  The `owner` column returns:

  ```
  +-----+-------+-----+-----------+-----+
  | ... | name  | ... | owner     | ... |
  +-----+-------+-----+-----------+-----+
  | ... | LOCAL | ... | SNOWFLAKE | ... |
  +-----+-------+-----+-----------+-----+
  ```

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

- The `HISTORY` and `WITH PRIVILEGES` parameters are mutually exclusive; they cannot both be used in the same statement.

## Examples

Show all schemas in the current database, `mytestdb`, that you have privileges to view:

Copy code

```
SHOW SCHEMAS;
```

```
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+-----------------+-------------------+
| created_on                      | name               | is_default | is_current | database_name | owner  | comment                                                   | options | retention_time | owner_role_type | object_visibility |
|---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+-----------------+-------------------+
| Fri, 13 May 2016 17:58:37 -0700 | INFORMATION_SCHEMA | N          | N          | MYTESTDB      |        | Views describing the contents of schemas in this database |         |              1 | ROLE            | NULL              |
| Wed, 25 Feb 2015 16:16:54 -0800 | PUBLIC             | N          | Y          | MYTESTDB      | PUBLIC |                                                           |         |              1 | ROLE            | NULL              |
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+-----------------+-------------------+
```

Show all schemas in the current database, `mytestdb`, that you have privileges to view, including dropped schemas (this example
builds on the [DROP SCHEMA](/sql-reference/sql/drop-schema) examples):

Copy code

```
SHOW SCHEMAS HISTORY;
```

```
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+---------------------------------+-----------------+-------------------+
| created_on                      | name               | is_default | is_current | database_name | owner  | comment                                                   | options | retention_time | dropped_on                      | owner_role_type | object_visibility |
|---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+---------------------------------+-----------------+-------------------+
| Fri, 13 May 2016 17:59:50 -0700 | INFORMATION_SCHEMA | N          | N          | MYTESTDB      |        | Views describing the contents of schemas in this database |         |              1 | NULL                            |                 | NULL              |
| Wed, 25 Feb 2015 16:16:54 -0800 | PUBLIC             | N          | Y          | MYTESTDB      | PUBLIC |                                                           |         |              1 | NULL                            | ROLE            | NULL              |
| Tue, 17 Mar 2015 16:42:29 -0700 | MYSCHEMA           | N          | N          | MYTESTDB      | PUBLIC |                                                           |         |              1 | Fri, 13 May 2016 17:25:32 -0700 | ROLE            | NULL              |
+---------------------------------+--------------------+------------+------------+---------------+--------+-----------------------------------------------------------+---------+----------------+---------------------------------+-----------------+-------------------+
```

Show all schemas in the current database that you have been granted the USAGE privilege on:

Copy code

```
SHOW SCHEMAS WITH PRIVILEGES USAGE;
```

```
+-------------------------------+----------------+------------+------------+-----------------------------------------------------------+--------------+---------+---------+----------------+-----------------+-------------------+
| created_on                    | name           | is_default | is_current | database_name                                             | owner        | comment | options | retention_time | owner_role_type | object_visibility |
|-------------------------------+----------------+------------+------------+-----------------------------------------------------------+--------------+---------+---------+----------------+-----------------+-------------------+
| 2023-01-27 15:01:12.940 -0800 | PUBLIC         | N          | N          | BOOKS_DB                                                  | DATA_ADMIN   |         |         | 1              | ROLE            | NULL              |
| 2023-09-15 15:22:51.164 -0700 | PUBLIC         | N          | N          | TEST_DB                                                   | ACCOUNTADMIN |         |         | 4              | ROLE            | NULL              |
| 2023-01-13 10:58:49.584 -0800 | ACCOUNT_USAGE  | N          | N          | SNOWFLAKE                                                 |              |         |         | 1              |                 | NULL              |
+-------------------------------+----------------+------------+------------+-----------------------------------------------------------+--------------+---------+---------+----------------+-----------------+-------------------+
```
