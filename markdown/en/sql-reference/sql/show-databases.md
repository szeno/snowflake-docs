# SHOW DATABASES

Lists the databases for which you have access privileges across your entire account, including dropped databases that are still within
the Time Travel retention period and, therefore, can be undropped.

The output returns database metadata and properties, ordered lexicographically by database name. This is important to note if you wish
to filter the results using the provided filters.

See also:
:   [CREATE DATABASE](/sql-reference/sql/create-database) , [ALTER DATABASE](/sql-reference/sql/alter-database) , [DESCRIBE DATABASE](/sql-reference/sql/desc-database) , [DROP DATABASE](/sql-reference/sql/drop-database) , [UNDROP DATABASE](/sql-reference/sql/undrop-database)

    [DATABASES view](/sql-reference/info-schema/databases) (Information Schema)

## Syntax

Copy code

```
SHOW [ TERSE ] DATABASES [ HISTORY ] [ LIKE '<pattern>' ]
                                     [ STARTS WITH '<name_string>' ]
                                     [ LIMIT <rows> [ FROM '<name_string>' ] ]
                                     [ WITH PRIVILEGES <object_privilege> [ , <object_privilege> [ , ... ] ] ]
```

## Parameters

`TERSE`
:   Optionally returns output containing only the following columns:

    - `created_on`
    - `name`
    - `kind`
    - `database_name`
    - `schema_name`

    Note that `kind`, `database_name`, and `schema_name` always display `NULL` because the columns are not
    applicable for databases.

    Default: No value (all columns are included in the output)

`HISTORY`
:   Optionally includes dropped databases that have not yet been purged (i.e. they are still within their respective Time Travel
    retention periods). If multiple versions of a dropped database exist, the output displays a row for each version. The output also
    includes an additional `dropped_on` column, which displays:

    - Date and timestamp (for dropped databases).
    - `NULL` (for active databases).

    Default: No value (dropped databases are not included in the output)

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

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

- The `HISTORY` and `WITH PRIVILEGES` parameters are mutually exclusive; they cannot both be used in the same statement.
- For a [personal database](/user-guide/personal-databases), the value in the `kind` column is `PERSONAL DATABASE`.
- For [catalog-linked databases](/user-guide/tables-iceberg-catalog-linked-database), the `kind` column is `CATALOG-LINKED DATABASE`.
- The `resharing_settings` column returns an OBJECT that describes the resharing configuration of an imported database. It is populated
  only for imported databases (`kind` is `IMPORTED DATABASE`) and is `NULL` for local databases. The object
  includes the `enabled` field, which is `true` when the database can be reshared, and `only_within_organization`, which is `true` when
  resharing is restricted to accounts within your organization. For details on using this column to confirm that an imported database
  can be reshared, see [Reshare incoming data as a resharer](/collaboration/resharing-as-resharer).

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

Show all databases that you have privileges to view in your account:

Copy code

```
SHOW DATABASES;
```

```
+---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+----------+-----------------+-------------------+-------------------------------------+
| created_on                      | name      | is_default | is_current | origin | owner  | comment | options | retention_time | kind     | owner_role_type | object_visibility | data_quality_monitoring_settings    |
|---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+----------|-----------------|-------------------|-------------------------------------|
| Tue, 17 Mar 2015 16:57:04 -0700 | MYTESTDB  | N          | Y          |        | PUBLIC |         |         | 1              | STANDARD | ROLE            | NULL              | NULL                                |
| Wed, 25 Feb 2015 17:30:04 -0800 | SALES1    | N          | N          |        | PUBLIC |         |         | 1              | STANDARD | ROLE            | NULL              | NULL                                |
| Fri, 13 Feb 2015 19:21:49 -0800 | DEMO1     | N          | N          |        | PUBLIC |         |         | 1              | STANDARD | ROLE            | NULL              | NULL                                |
+---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+----------+-----------------+-------------------+-------------------------------------+
```

Show all databases that you have privileges to view in the system, including dropped databases (this example builds on the
[DROP DATABASE](/sql-reference/sql/drop-database) examples):

Copy code

```
SHOW DATABASES HISTORY;
```

```
+---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------+----------+-----------------+-------------------+-------------------------------------+
| created_on                      | name      | is_default | is_current | origin | owner  | comment | options | retention_time | dropped_on                      | kind     | owner_role_type | object_visibility | data_quality_monitoring_settings    |
|---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------|----------|-----------------|-------------------|-------------------------------------|
| Tue, 17 Mar 2015 16:57:04 -0700 | MYTESTDB  | N          | Y          |        | PUBLIC |         |         | 1              | [NULL]                          | STANDARD | ROLE            | NULL              | NULL                                |
| Wed, 25 Feb 2015 17:30:04 -0800 | SALES1    | N          | N          |        | PUBLIC |         |         | 1              | [NULL]                          | STANDARD | ROLE            | NULL              | NULL                                |
| Fri, 13 Feb 2015 19:21:49 -0800 | DEMO1     | N          | N          |        | PUBLIC |         |         | 1              | [NULL]                          | STANDARD | ROLE            | NULL              | NULL                                |
| Wed, 25 Feb 2015 16:16:54 -0800 | MYTESTDB2 | N          | N          |        | PUBLIC |         |         | 1              | Fri, 13 May 2016 17:35:09 -0700 | STANDARD | ROLE            | NULL              | NULL                                |
+---------------------------------+-----------+------------+------------+--------+--------+---------+---------+----------------+---------------------------------+----------+-----------------+-------------------+-------------------------------------+
```

Show all databases that you have been granted the USAGE and MODIFY privileges on:

Copy code

```
SHOW DATABASES WITH PRIVILEGES USAGE, MODIFY;
```

```
+-------------------------------+------------+------------+------------+---------------------------+--------------+---------+---------+----------------+-------------------+-----------------+-------------------+-------------------------------------+
| created_on                    | name       | is_default | is_current | origin                    | owner        | comment | options | retention_time | kind              | owner_role_type | object_visibility | data_quality_monitoring_settings    |
|-------------------------------+------------+------------+------------+---------------------------+--------------+---------+---------+----------------+-------------------+-----------------|-------------------|-------------------------------------|
| 2023-01-27 14:33:11.417 -0800 | BOOKS_DB   | N          | N          |                           | DATA_ADMIN   |         |         | 1              | STANDARD          | ROLE            | NULL              | NULL                                |
| 2023-09-15 15:22:51.111 -0700 | TEST_DB    | N          | N          |                           | ACCOUNTADMIN |         |         | 4              | STANDARD          | ROLE            | NULL              | NULL                                |
| 2023-08-18 13:33:01.024 -0700 | SNOWFLAKE  | N          | N          | SNOWFLAKE.ACCOUNT_USAGE   |              |         |         | 0              | APPLICATION       |                 | NULL              | NULL                                |
+-------------------------------+------------+------------+------------+---------------------------+--------------+---------+---------+----------------+-------------------+-----------------+-------------------+-------------------------------------+
```
