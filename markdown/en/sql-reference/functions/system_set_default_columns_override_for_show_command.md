Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND

Controls the columns that should be returned when the specified [SHOW <objects>](/sql-reference/sql/show) command is executed.

You can call this function if the introduction of new columns in a SHOW COMMAND introduces a problem with a script or code that
depends on a fixed number or order of columns in the results. See [Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_get_default_columns_override_for_show_command) ,
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) ,
    [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides)

## Syntax

Copy code

```
SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  '<object_type>',
  '<list_of_columns>'
)
```

## Arguments

`'object_type'`
:   Type of object for the SHOW command. For example, for the SHOW TABLES command, specify `'TABLES'`. For the SHOW NOTIFICATION
    INTEGRATIONS command, specify `'NOTIFICATION INTEGRATIONS'`.

`list_of_columns`
:   Comma-separated list of columns that should be returned in the output of the SHOW command.

    You can specify the column names in uppercase, lowercase, or mixed case.

    To return all columns, specify an empty string or call
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command).

## Returns

Returns TRUE if the operation was successful.

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Examples

The following example configures the [SHOW TABLES](/sql-reference/sql/show-tables) command to return only the `name`, `database_name`,
`kind`, and `comment` columns:

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'TABLES',
  'name, database_name, kind, comment'
);
```

Executing the SHOW TABLES command returns only the specified columns:

Copy code

```
SHOW TABLES;
```

```
+------------------+---------------+-------+---------+
| name             | database_name | kind  | comment |
|------------------+---------------+-------+---------|
| DEPARTMENT_TABLE | MY_DB         | TABLE |         |
| EMPLOYEE_TABLE   | MY_DB         | TABLE |         |
+------------------+---------------+-------+---------+
```

Executing the SHOW TERSE TABLES command returns only the specified columns except for `comment`, which isn’t normally returned
when you specify TERSE:

Copy code

```
SHOW TERSE TABLES;
```

```
+------------------+-------+---------------+
| name             | kind  | database_name |
|------------------+-------+---------------|
| DEPARTMENT_TABLE | TABLE | MY_DB         |
| EMPLOYEE_TABLE   | TABLE | MY_DB         |
+------------------+-------+---------------+
```
