# SHOW MATERIALIZED VIEWS

[Enterprise Edition Feature](/user-guide/intro-editions)

Materialized views require Enterprise Edition. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists the materialized views that you have privileges to access.

For more information about materialized views, see [Working with Materialized Views](/user-guide/views-materialized).

See also:
:   [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view) , [ALTER MATERIALIZED VIEW](/sql-reference/sql/alter-materialized-view) , [DROP MATERIALIZED VIEW](/sql-reference/sql/drop-materialized-view) , [DESCRIBE MATERIALIZED VIEW](/sql-reference/sql/desc-materialized-view)

## Syntax

Copy code

```
SHOW MATERIALIZED VIEWS [ LIKE '<pattern>' ]
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
```

## Parameters

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

## Usage notes

- The output columns are similar to the output columns for [SHOW TABLES](/sql-reference/sql/show-tables), but includes the following additional columns:

  - refreshed\_on: time of the last DML operation on the base table that was processed by a
    [“refresh” operation](/user-guide/views-materialized#label-working-with-a-materialized-view).
  - compacted\_on: time of the last DML operation on the base table that was processed by a
    [“compaction” operation](/user-guide/views-materialized#label-working-with-a-materialized-view).
  - behind\_by: If the background process that updates the materialized view
    with changes from the base table has not yet brought the materialized view
    up to date, then this column shows approximately how many seconds the
    materialized view is “behind” the base table. Note that even if this shows
    that the materialized view is not up to date, any queries on the
    materialized view will still return up-to-date results (they just might
    take a little longer as extra information is retrieved from the base table).
- The command SHOW VIEWS also shows information about materialized views.

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

## Output

The command output provides materialized view properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | The timestamp at which the materialized view was created. |
| name | The name of the materialized view. |
| reserved | Reserved for future use. |
| database\_name | The name of the database in which the materialized view exists. |
| schema\_name | The name of the schema in which the materialized view exists. |
| cluster\_by | Information about the clustering columns (if the materialized view is clustered). |
| rows | The number of rows in the materialized view. |
| bytes | The number of bytes of data in the materialized view. |
| source\_database\_name | The name of the database in which the materialized view’s base table exists. |
| source\_schema\_name | The name of the schema in which the materialized view’s base table exists. |
| source\_table\_name | The name of the materialized view’s base table. |
| refreshed\_on | The timestamp of the last DML operation on the base table that was processed by a [“refresh” operation](/user-guide/views-materialized#label-working-with-a-materialized-view). |
| compacted\_on | The timestamp of the last DML operation on the base table that was processed by a [“compaction” operation](/user-guide/views-materialized#label-working-with-a-materialized-view). |
| owner | The owner of the materialized view. |
| invalid | True if the materialized view is currently invalid (for example, if the base table dropped a column that the view used); false otherwise. |
| invalid\_reason | The reason (if any) that the materialized view is currently invalid. |
| behind\_by | How far the updates of the materialized view are behind the updates of the base table. |
| comment | Optional comment. |
| text | The text of the command that created this materialized view (e.g. CREATE MATERIALIZED VIEW …). |
| is\_secure | True if the materialized view is a secure view; false otherwise. |
| automatic\_clustering | True if the view is clustered and the clustering is automatic. |
| owner\_role\_type | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Examples

Show all materialized views:

> Copy code
>
> ```
> SHOW MATERIALIZED VIEWS;
> ```

Show only materialized views with names matching the specified regular expression:

> Copy code
>
> ```
> SHOW MATERIALIZED VIEWS LIKE 'mv1%';
>
> +-------------------------------+------+----------+---------------+-------------+------------+------+-------+----------------------+--------------------+-------------------+-------------------------------+--------------+----------+---------+----------------+-----------+---------+--------------------------------------------+-----------+----------------------+-----------------+
> | created_on                    | name | reserved | database_name | schema_name | cluster_by | rows | bytes | source_database_name | source_schema_name | source_table_name | refreshed_on                  | compacted_on | owner    | invalid | invalid_reason | behind_by | comment | text                                       | is_secure | automatic_clustering | owner_role_type |
> |-------------------------------+------+----------+---------------+-------------+------------+------+-------+----------------------+--------------------+-------------------+-------------------------------+--------------+----------+---------+----------------+-----------+---------+--------------------------------------------+-----------|----------------------+-----------------|
> | 2018-10-05 17:13:17.579 -0700 | MV1  |          | TEST_DB1      | PUBLIC      |            |    0 |     0 | TEST_DB1             | PUBLIC             | INVENTORY         | 2018-10-05 17:13:50.373 -0700 | NULL         | SYSADMIN | false   | NULL           | 0s        |         | CREATE OR REPLACE MATERIALIZED VIEW mv1 AS | false     | OFF                  | ROLE            |
> |                               |      |          |               |             |            |      |       |                      |                    |                   |                               |              |          |         |                |           |         |       SELECT ID, price FROM inventory;     |           |                      |                 |          |
> +-------------------------------+------+----------+---------------+-------------+------------+------+-------+----------------------+--------------------+-------------------+-------------------------------+--------------+----------+---------+----------------+-----------+---------+--------------------------------------------+-----------+----------------------+-----------------+
> ```
