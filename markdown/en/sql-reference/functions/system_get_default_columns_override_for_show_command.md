Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND

Returns the list of columns that were set by a previous call to
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command).

For more information, see [Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) ,
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) ,
    [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides)

## Syntax

Copy code

```
SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  '<object_type>'
)
```

## Arguments

`'object_type'`
:   Type of object for the SHOW command. For example, for the SHOW TABLES command, specify `'TABLES'`. For the SHOW NOTIFICATION
    INTEGRATIONS command, specify `'NOTIFICATION INTEGRATIONS'`.

## Returns

Returns a VARCHAR value containing a comma-separated list of the columns specified by the previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND. The column names are in lowercase.

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was not called or if
[SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) was called to clear the list of columns, the function returns an
empty string.

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Examples

The following example returns the list of columns specified by a previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND for the SHOW TABLES command:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'TABLES'
);
```

```
+-------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND( |
|   'TABLES'                                            |
| )                                                     |
|-------------------------------------------------------|
| name,database_name,kind,comment                       |
+-------------------------------------------------------+
```

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was not called or if
SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was called to clear the list, the function returns an empty string:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'TABLES'
);

SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'TABLES'
);
```

```
+-------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND( |
|   'TABLES'                                            |
| )                                                     |
|-------------------------------------------------------|
|                                                       |
+-------------------------------------------------------+
```
