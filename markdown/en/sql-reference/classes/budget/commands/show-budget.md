# SHOW BUDGET

*Fully qualified name*: SNOWFLAKE.CORE.BUDGET

Lists budgets for which you have access privileges.

SHOW SNOWFLAKE.CORE.BUDGET INSTANCES is an alias for SHOW SNOWFLAKE.CORE.BUDGET.

See also:
:   [SYSTEM$SHOW\_BUDGETS\_IN\_ACCOUNT](/sql-reference/functions/system_show_budgets_in_account),
    [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget)

## Syntax

Copy code

```
{
  SHOW SNOWFLAKE.CORE.BUDGET           |
  SHOW SNOWFLAKE.CORE.BUDGET INSTANCES
}
  [ LIKE '<pattern>' ]
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
  [ LIMIT <rows> [ FROM '<name_string>' ]
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

## Usage notes

- To refer to this class by its unqualified name, include the database and schema of the class in your
  [search path](/sql-reference/snowflake-db-classes#label-update-search-path).
- The system function [SYSTEM$SHOW\_BUDGETS\_IN\_ACCOUNT](/sql-reference/functions/system_show_budgets_in_account) might execute faster than
  the SHOW command but doesn’t include owner fields in the output.
- The order of results is not guaranteed.

## Output

The command output provides budget properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| created\_on | Date and time when the table was created. |
| name | Name of the budget. |
| database\_name | Name of the database that contains the budget. |
| schema\_name | Name of the schema that contains the budget. |
| current\_version | Version of the BUDGET class used to create the budget instance. |
| comment | Comment for the budget. |
| owner | Role that owns the budget. |
| owner\_role\_type | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Examples

List budgets in the `budget_db.budget_schema` schema:

Copy code

```
SHOW SNOWFLAKE.CORE.BUDGET INSTANCES IN SCHEMA budget_db.budget_schema;
```

List budgets in the `budget_db.budget_schema` schema that include `dept` in the name of the budget:

Copy code

```
SHOW SNOWFLAKE.CORE.BUDGET LIKE '%DEPT%' IN SCHEMA budget_db.budget_schema;
```
