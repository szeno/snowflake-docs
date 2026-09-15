# SHOW SNOWFLAKE.ML.TOP\_INSIGHTS

Lists all Top Insights class instances.

SHOW SNOWFLAKE.ML.TOP\_INSIGHTS INSTANCES is an alias for SHOW SNOWFLAKE.ML.TOP\_INSIGHTS.

## Syntax

Copy code

```
{
  SHOW SNOWFLAKE.ML.TOP_INSIGHTS           |
  SHOW SNOWFLAKE.ML.TOP_INSIGHTS INSTANCES
}
  [ LIKE <pattern> ]
  [ IN
      {
        ACCOUNT                  |

        DATABASE                 |
        DATABASE <database_name> |

        SCHEMA                   |
        SCHEMA <schema_name>     |
        <schema_name>
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

    If you omit `IN ...`, the scope of the command depends on whether the session currently has a database in use:

    - If a database is currently in use, the command returns the objects you have privileges to view in the database. This has the
      same effect as specifying `IN DATABASE`.
    - If no database is currently in use, the command returns the objects you have privileges to view in your account. This has the
      same effect as specifying `IN ACCOUNT`.

## Usage notes

The order of results is not guaranteed.

## Output

The command output provides instance properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | Date and time when the instance was created |
| name | Name of the instance |
| database\_name | Database in which the instance is stored |
| schema\_name | Schema in which the instance is stored |
| current\_version | The version of the instance |
| comment | Comment for the instance |
| owner | The role that owns the instance |

Expand

Show lessSee more
