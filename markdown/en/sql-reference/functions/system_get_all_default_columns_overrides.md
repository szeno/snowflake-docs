Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES

Returns the list of columns that were set by previous calls to
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) and
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object).

For more information, see [Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) ,
    [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_get_default_columns_override_for_show_command) ,
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) ,
    [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object) ,
    [SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_get_default_columns_override_for_system_object) ,
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object)

## Syntax

Copy code

```
SYSTEM$GET_ALL_DEFAULT_COLUMNS_OVERRIDES()
```

## Arguments

None.

## Returns

Returns a VARCHAR value (a string) in JSON format. The string is a JSON array that contains an object for each SHOW command,
Snowflake view, and built-in table function that has an overridden list of columns.

If the object represents the overridden list of default columns for a SHOW command, the object contains the following name/value
pairs:

| Name | Description |
| --- | --- |
| `isShowCommand` | Indicates if the object represents the list of columns for a SHOW command. In this case, the value is `true`. |
| `showCommandType` | Type of the object for the SHOW command. For example, for SHOW NOTIFICATION INTEGRATIONS, the value is `"NOTIFICATION INTEGRATIONS"`. |
| `serializedDefaultColumns` | Comma-separated list of columns specified in a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND call. The column names are in uppercase. |

Expand

Show lessSee more

If the object represents the overridden list of default columns for a Snowflake view or built-in table function, the object
contains the following name/value pairs:

| Name | Description |
| --- | --- |
| `domain` | Type of the object. The value is `"VIEW"` for a Snowflake view or `"FUNCTION"` for a built-in table function. |
| `isShowCommand` | Indicates if the object represents the list of columns for a SHOW command. In this case, the value is `false`. |
| `dbName` | Name of the database containing the object. For INFORMATION\_SCHEMA views and table functions, the value is an empty string (`""`). |
| `schemaName` | Name of the schema containing the object. |
| `objectName` | Name of the view or table function. |
| `serializedDefaultColumns` | Comma-separated list of columns specified in a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT call. The column names are in uppercase. |

Expand

Show lessSee more

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Examples

The following example returns the list of columns specified by previous calls to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND and SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT:

Copy code

```
SELECT SYSTEM$GET_ALL_DEFAULT_COLUMNS_OVERRIDES();
```

```
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SYSTEM$GET_ALL_DEFAULT_COLUMNS_OVERRIDES()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [{"domain":"VIEW","isShowCommand":false,"dbName":"","schemaName":"INFORMATION_SCHEMA","objectName":"DATABASES","serializedDefaultColumns":"DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,RETENTION_TIME,TYPE,OWNER_ROLE_TYPE"},{"domain":"VIEW","isShowCommand":false,"dbName":"SNOWFLAKE","schemaName":"ACCOUNT_USAGE","objectName":"DATABASES","serializedDefaultColumns":"DATABASE_ID,DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,DELETED,RETENTION_TIME,RESOURCE_GROUP,TYPE,OWNER_ROLE_TYPE,OBJECT_VISIBILITY"},{"isShowCommand":true,"showCommandType":"NOTIFICATION INTEGRATIONS","serializedDefaultColumns":"name,type,category,enabled,comment,created_on"}] |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
