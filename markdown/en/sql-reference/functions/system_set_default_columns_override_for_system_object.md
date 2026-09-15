Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT

Controls the columns that should be returned when you select all columns (`SELECT *`) from the specified Snowflake view (for
example, from a specific [ACCOUNT\_USAGE](/sql-reference/account-usage), [ORGANIZATION\_USAGE](/sql-reference/organization-usage),
[READER\_ACCOUNT\_USAGE](/sql-reference/account-usage), or [INFORMATION\_SCHEMA](/sql-reference/info-schema) view) or from the
output of a built-in table function in one of these schemas.

Note

This function does not affect queries that select specific columns from the view or table function output.

You can call this function if the introduction of new columns in a Snowflake view or table function introduces a problem with a
script or code that selects all columns and depends on a fixed number or order of columns in the results. See
[Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_get_default_columns_override_for_system_object),
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object),
    [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides)

## Syntax

Copy code

```
SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  '<object_type>',
  '<database_name>',
  '<schema_name>',
  '<object_name>',
  '<list_of_columns>'
)
```

## Arguments

`'object_type'`
:   Type of the object. Specify `'VIEW'` for a Snowflake view or `'FUNCTION'` for a built-in table function.

`'database_name'`
:   Name of the database that contains the object. For a view, specify `'SNOWFLAKE'` or, for an INFORMATION\_SCHEMA view, an empty
    string. For a table function, specify an empty string for an INFORMATION\_SCHEMA table function, or `'SNOWFLAKE'` for an
    ACCOUNT\_USAGE, ORGANIZATION\_USAGE, or READER\_ACCOUNT\_USAGE table function.

`'schema_name'`
:   Name of the schema that contains the object. For a view, specify the name of a schema in the
    [SNOWFLAKE database](/sql-reference/snowflake-db) or `'INFORMATION_SCHEMA'`. For a table function, specify the name of the
    schema that contains it, such as `'INFORMATION_SCHEMA'`, `'ACCOUNT_USAGE'`, `'ORGANIZATION_USAGE'`, or
    `'READER_ACCOUNT_USAGE'`.

`'object_name'`
:   Name of the object.

`list_of_columns`
:   Comma-separated list of columns that should be returned when you select all columns from this view or from the output of this
    table function.

    You can specify the column names in uppercase, lowercase, or mixed case. The columns are returned in their default order,
    regardless of the order in which you list them.

    To return all columns, specify an empty string or call SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT.

## Returns

Returns TRUE if the operation was successful.

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Usage notes

- You must have a database in use (for example, by running [USE DATABASE](/sql-reference/sql/use-database)) in order to call this function.
  If no database is in use, the function call fails.

## Examples

The following example configures queries that select all columns from the [TABLES view](/sql-reference/account-usage/tables) view in the
ACCOUNT\_USAGE schema to return only the `table_name`, `table_schema`, and `table_type` columns:

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'TABLES',
  'table_name, table_schema, table_type'
);
```

Selecting all columns from that view returns only the specified columns:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES;
```

```
+------------+---------------------+------------+
| TABLE_NAME | TABLE_SCHEMA        | TABLE_TYPE |
|------------+---------------------+------------|
| MY_TABLE   | MY_SCHEMA           | BASE TABLE |
+------------+---------------------+------------+
```

The following example configures queries that select all columns from the [TABLES view](/sql-reference/info-schema/tables) view in the
INFORMATION\_SCHEMA schema to return only the `table_name`, `table_schema`, and `table_type` columns:

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  '',
  'INFORMATION_SCHEMA',
  'TABLES',
  'table_name, table_schema, table_type'
);
```

Selecting all columns from that view returns only the specified columns:

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.TABLES;
```

```
+--------------+------------+------------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE |
|--------------+------------+------------|
| MY_SCHEMA    | MY_TABLE   | BASE TABLE |
+--------------+------------+------------+
```

To configure the columns returned by a built-in table function in the INFORMATION\_SCHEMA schema, specify `'FUNCTION'` as the
object type, an empty string as the database name, and `'INFORMATION_SCHEMA'` as the schema name. The following example
configures the [TASK\_HISTORY](/sql-reference/functions/task_history) table function to return only the `name`, `state`, and
`scheduled_time` columns:

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'FUNCTION',
  '',
  'INFORMATION_SCHEMA',
  'TASK_HISTORY',
  'name, state, scheduled_time'
);
```
