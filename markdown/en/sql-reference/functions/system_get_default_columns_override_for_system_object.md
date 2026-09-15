Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT

Returns the list of columns that were set by a previous call to
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object) for the specified Snowflake view (for
example, for a specific [ACCOUNT\_USAGE](/sql-reference/account-usage), [ORGANIZATION\_USAGE](/sql-reference/organization-usage),
[READER\_ACCOUNT\_USAGE](/sql-reference/account-usage), or [INFORMATION\_SCHEMA](/sql-reference/info-schema) view) or for a
built-in table function in one of these schemas.

For more information, see [Handling new columns in SHOW command output, Snowflake views, and table functions](/release-notes/behavior-changes-new-columns).

See also:
:   [SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object),
    [SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object),
    [SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides)

## Syntax

Copy code

```
SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  '<object_type>',
  '<database_name>',
  '<schema_name>',
  '<object_name>'
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

## Returns

Returns a VARCHAR value containing a comma-separated list of the columns specified by the previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT. The column names are in uppercase.

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was not called or if
[SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object) was called to clear the list of columns, the function returns an
empty string.

## Access control requirements

Only account administrators (users who have been granted the ACCOUNTADMIN role) can call this function.

## Usage notes

- You must have a database in use (for example, by running [USE DATABASE](/sql-reference/sql/use-database)) in order to call this function.
  If no database is in use, the function call fails.

## Examples

The following example returns the list of columns specified by a previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT for the
[TABLES view in the ACCOUNT\_USAGE schema](/sql-reference/account-usage/tables):

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'TABLES'
);
```

```
+--------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT( |
|   'VIEW',                                              |
|   'SNOWFLAKE',                                         |
|   'ACCOUNT_USAGE',                                     |
|   'TABLES'                                             |
| )                                                      |
|--------------------------------------------------------|
| TABLE_NAME,TABLE_SCHEMA,TABLE_TYPE                     |
+--------------------------------------------------------+
```

The following example returns the list of columns specified by a previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT for the
[TABLES view in the INFORMATION\_SCHEMA schema](/sql-reference/info-schema/tables):

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  '',
  'ACCOUNT_USAGE',
  'TABLES'
);
```

```
+--------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT( |
|   'VIEW',                                              |
|   '',                                                  |
|   'INFORMATION_SCHEMA',                                |
|   'TABLES'                                             |
| )                                                      |
|--------------------------------------------------------|
| TABLE_NAME,TABLE_SCHEMA,TABLE_TYPE                     |
+--------------------------------------------------------+
```

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was not called or if
SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was called to clear the list, the function returns an empty string:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'TABLES'
);

SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'TABLES'
);
```

```
+--------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT( |
|   'VIEW',                                              |
|   'SNOWFLAKE',                                         |
|   'ACCOUNT_USAGE',                                     |
|   'TABLES'                                             |
| )                                                      |
|--------------------------------------------------------|
```

The following example returns the list of columns specified by a previous call to
SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT for the [TASK\_HISTORY](/sql-reference/functions/task_history) table function in the
INFORMATION\_SCHEMA schema:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'FUNCTION',
  '',
  'INFORMATION_SCHEMA',
  'TASK_HISTORY'
);
```
