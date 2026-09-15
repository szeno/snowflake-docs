Categories:
:   [System functions](/sql-reference/functions-system) (Control)

# SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND

Clears the list of columns specified by a previous call to
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) for a type of object.

For more information, see [Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) ,
    [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_get_default_columns_override_for_show_command) ,
    [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides)

## Syntax

Copy code

```
SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  '<object_type>'
)
```

## Arguments

`'object_type'`
:   Type of object for the SHOW command. For example, for the SHOW TABLES command, specify `'TABLES'`. For the SHOW NOTIFICATION
    INTEGRATIONS command, specify `'NOTIFICATION INTEGRATIONS'`.

## Returns

Returns TRUE if the operation was successful.

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Examples

The following example clears the list of columns set by a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND call for
the [SHOW TABLES](/sql-reference/sql/show-tables) command:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'TABLES'
);
```
