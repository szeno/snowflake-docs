# SHOW OBJECTS

Lists the tables and views for which you have access privileges. This command can be used to list the tables and views for a specified
database or schema (or the current database/schema for the session), or your entire account.

## Syntax

Copy code

```
SHOW [ TERSE ] OBJECTS [ LIKE '<pattern>' ]
                       [ IN
                             {
                               ACCOUNT                                         |

                               DATABASE                                        |
                               DATABASE <database_name>                        |

                               SCHEMA                                          |
                               SCHEMA <schema_name>                            |
                               <schema_name>

                               APPLICATION <application_name>                  |
                               APPLICATION PACKAGE <application_package_name>  |
                             }
                       ]
                       [ STARTS WITH '<name_string>' ]
                       [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only a subset of the output columns:

    - `created_on`
    - `name`
    - `kind`
    - `database_name`
    - `schema_name`

    Default: No value (all columns are included in the output).

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns records for the entire account.

    `DATABASE`, `DATABASE db_name`
    :   Returns records for the current database in use or for a specified database (`db_name`).

        If you specify `DATABASE` without `db_name` and no database is in use, the keyword has no effect on the output.

        Note

        Using SHOW commands without an `IN` clause in a database context can result in fewer than expected results.

        Objects with the same name are only displayed once if no `IN` clause is used. For example, if you have table `t1` in
        `schema1` and table `t1` in `schema2`, and they are both in scope of the database context you’ve specified (that is, the database
        you’ve selected is the parent of `schema1` and `schema2`), then SHOW TABLES only displays one of the `t1` tables.

    `SCHEMA`, `SCHEMA schema_name`
    :   Returns records for the current schema in use or a specified schema (`schema_name`).

        `SCHEMA` is optional if a database is in use or if you specify the fully qualified `schema_name` (for example, `db.schema`).

        If no database is in use, specifying `SCHEMA` has no effect on the output.

    `APPLICATION application_name`, `APPLICATION PACKAGE application_package_name`
    :   Returns records for the named Snowflake Native App or application package.

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

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

The command output provides table properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | Date and time when the object was created. |
| name | Name of the object. |
| database\_name | Database in which the object is stored. |
| schema\_name | Schema in which the object is stored. |
| kind | Object type: TABLE, VIEW. |
| comment | Comment for the object. |
| cluster\_by | Column(s) defined as clustering key(s) for the object. |
| rows | Number of rows in the object. |
| bytes | Number of bytes that will be scanned if the entire object is scanned in a query. Note that this number may be different than the number of actual physical bytes (i.e. bytes stored on-disk) for the object. |
| owner | Role that owns the object. |
| retention\_time | Number of days that modified and deleted data is retained for Time Travel. |
| is\_hybrid | `Y` if the object is a hybrid table; `N` otherwise. |
| is\_dynamic | `Y` if the object is a dynamic table; `N` otherwise. |
| is\_iceberg | `Y` if the object is an [Apache Iceberg™ table](/user-guide/tables-iceberg); `N` otherwise. |

Expand

Show lessSee more

## Usage notes

- For a [personal database](/user-guide/personal-databases), the value in the `kind` column is `PERSONAL DATABASE`.
- Personal databases can appear in the output when the command is run by a role with sufficient privileges (for example, ACCOUNTADMIN).
- To view objects in a specific personal database, use:

  Copy code

  ```
  SHOW OBJECTS IN DATABASE "USER$<username>";
  ```
- For materialized views and semantic views, the `kind` column contains `VIEW`.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Show all tables and views whose names start with `HT_` that you have privileges to see in the current database:

Copy code

```
SHOW OBJECTS IN DATABASE STARTS WITH 'HT_';
```

```
+-------------------------------+------------------------+---------------+----------------+-------+---------+------------+---------+-----------+--------------+----------------+-----------------+--------+-----------+------------+
| created_on                    | name                   | database_name | schema_name    | kind  | comment | cluster_by |    rows |     bytes | owner        | retention_time | owner_role_type | budget | is_hybrid | is_dynamic |
|-------------------------------+------------------------+---------------+----------------+-------+---------+------------+---------+-----------+--------------+----------------+-----------------+--------+-----------+------------|
| 2024-05-13 19:08:41.946 -0700 | HT_PRECIP              | HYBRID1_DB    | HYBRID1_SCHEMA | TABLE |         |            |       0 |         0 | HYBRID1_ROLE | 1              | ROLE            | NULL   | Y         | N          |
| 2024-08-23 11:44:13.694 -0700 | HT_SENSOR_DATA_DEVICE1 | HYBRID1_DB    | HYBRID1_SCHEMA | TABLE |         |            | 2678400 | 133920000 | HYBRID1_ROLE | 1              | ROLE            | NULL   | Y         | N          |
| 2024-05-13 16:37:29.217 -0700 | HT_WEATHER             | HYBRID1_DB    | HYBRID1_SCHEMA | TABLE |         |            |      55 |      2985 | HYBRID1_ROLE | 1              | ROLE            | NULL   | Y         | N          |
| 2024-07-18 12:17:27.381 -0700 | HT_WEATHER             | HYBRID1_DB    | PUBLIC         | TABLE |         |            |      55 |      3040 | ACCOUNTADMIN | 1              | ROLE            | NULL   | Y         | N          |
+-------------------------------+------------------------+---------------+----------------+-------+---------+------------+---------+-----------+--------------+----------------+-----------------+--------+-----------+------------+
```
