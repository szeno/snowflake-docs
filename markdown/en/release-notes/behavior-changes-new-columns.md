# Handling new columns in SHOW command output, Snowflake views, and table functions

Periodically, new columns will be introduced in the output of [SHOW <objects>](/sql-reference/sql/show) commands, in Snowflake views
(such as the views in the [ACCOUNT\_USAGE schema](/sql-reference/account-usage) in the
[SNOWFLAKE database](/sql-reference/snowflake-db) and the views in the
[INFORMATION\_SCHEMA schema](/sql-reference/info-schema)), and in the output of the built-in table functions in the
[ACCOUNT\_USAGE](/sql-reference/account-usage), [ORGANIZATION\_USAGE](/sql-reference/organization-usage),
[READER\_ACCOUNT\_USAGE](/sql-reference/account-usage), and [INFORMATION\_SCHEMA](/sql-reference/info-schema) schemas.

If you have a script or code that depends on the result set including a specific number of columns or that depends on the order
of the columns, the introduction of a new column might affect that script or code.

## Temporarily working around a problem introduced by a new column

If your script or code encounters problems due to the introduction of new columns, your Snowflake administrator (a user who has
been granted the ACCOUNTADMIN role) can change the columns that are returned for executions of a specific SHOW command, SELECT \*
queries of a Snowflake view, or calls to a built-in table function. These columns are referred to as the *default columns*.

- [Overriding the default columns for a SHOW command](#overriding-the-default-columns-for-a-show-command)
- [Resetting the default columns for a SHOW command](#resetting-the-default-columns-for-a-show-command)
- [Getting the list of default columns for a SHOW command](#getting-the-list-of-default-columns-for-a-show-command)
- [Overriding the default columns for a Snowflake view](#overriding-the-default-columns-for-a-snowflake-view)
- [Resetting the default columns for a Snowflake view](#resetting-the-default-columns-for-a-snowflake-view)
- [Getting the list of default columns for a Snowflake view](#getting-the-list-of-default-columns-for-a-snowflake-view)
- [Overriding the default columns for a table function](#overriding-the-default-columns-for-a-table-function)
- [Resetting the default columns for a table function](#resetting-the-default-columns-for-a-table-function)
- [Getting the list of default columns for a table function](#getting-the-list-of-default-columns-for-a-table-function)
- [Getting the list of columns from all previous calls for SHOW commands, Snowflake views, and table functions](#getting-the-list-of-columns-from-all-previous-calls-for-show-commands-snowflake-views-and-table-functions)

### Overriding the default columns for a SHOW command

To exclude newly introduced columns from the output of a SHOW command, call the
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_set_default_columns_override_for_show_command) function, specifying the type of object and
the list of columns that should be returned.

Suppose that a new `direction` column has been introduced in the output of the
[SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations) command. To prevent the new `direction` column from being included in
the output of the command, call SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND, specifying `'NOTIFICATION INTEGRATIONS'`
as the type of object. Pass in a comma-separated list of the columns that should be returned in the output (a list that excludes
`direction`):

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'NOTIFICATION INTEGRATIONS',
  'name, type, category, enabled, comment, created_on'
);
```

When anyone in your account runs the SHOW NOTIFICATION INTEGRATIONS command, the new `direction` column will not be returned in
the output.

Copy code

```
SHOW NOTIFICATION INTEGRATIONS;
```

```
+--------------------------------+---------+--------------+---------+---------+-------------------------------+
| name                           | type    | category     | enabled | comment | created_on                    |
|--------------------------------+---------+--------------+---------+---------+-------------------------------|
| SLACK_NOTIFICATION_INTEGRATION | WEBHOOK | NOTIFICATION | true    | NULL    | 2025-07-02 06:14:53.859 -0700 |
+--------------------------------+---------+--------------+---------+---------+-------------------------------+
```

### Resetting the default columns for a SHOW command

If you need to undo a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND call and return all columns in the SHOW
command for a specific object type, call the
[SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_unset_default_columns_override_for_show_command) function, specifying the type of object.
For example:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'NOTIFICATION INTEGRATIONS'
);
```

### Getting the list of default columns for a SHOW command

If you need to determine if SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was called for a specific object type and you
want the list of columns that will be returned in the output of the command, call the
[SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND](/sql-reference/functions/system_get_default_columns_override_for_show_command) function, specifying the type of object. For
example:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'NOTIFICATION INTEGRATIONS'
);
```

```
+-------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND( |
|   'NOTIFICATION INTEGRATIONS'                         |
| )                                                     |
|-------------------------------------------------------|
| name,type,category,enabled,comment,created_on         |
+-------------------------------------------------------+
```

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was not previously called or if
SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SHOW\_COMMAND was called, the function returns an empty string.

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'NOTIFICATION INTEGRATIONS'
);

SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND(
  'NOTIFICATION INTEGRATIONS'
);
```

```
+-------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SHOW_COMMAND( |
|   'NOTIFICATION INTEGRATIONS'                         |
| )                                                     |
|-------------------------------------------------------|
|                                                       |
+-------------------------------------------------------+
```

### Overriding the default columns for a Snowflake view

To exclude newly introduced columns from the results of a `SELECT *` query of a Snowflake view, call the
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object) function, specifying the type of object, the
database and schema containing the view, the name of the view, and the list of columns that should be returned.

Suppose that a new `replicable_with_failover_groups` column has been introduced in the
[DATABASES view in the ACCOUNT\_USAGE schema](/sql-reference/account-usage/databases). To prevent the new
`replicable_with_failover_groups` column from being returned in the results of a `SELECT *` query of the view,
call SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT, specifying `'VIEW'` as the type of object, `'SNOWFLAKE'` as the
database, `'ACCOUNT_USAGE'` as the schema, and `'DATABASES'` as the view. Pass in a comma-separated list of the columns that
should be returned in the output (a list that excludes `replicable_with_failover_groups`):

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'DATABASES',
  'database_id, database_name, database_owner, is_transient, ' ||
  'comment, created, last_altered, deleted, retention_time, '  ||
  'resource_group, type, owner_role_type, object_visibility'
);
```

The example uses the [||](/sql-reference/functions/concat) operator to construct a string that contains the comma-separated
list of columns.

When anyone in your account performs a `SELECT *` query of the DATABASES view, the new `replicable_with_failover_groups`
column will not be returned in the output.

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES;
```

```
+-------------+---------------+----------------+--------------+---------+-------------------------------+-------------------------------+-------------------------------+----------------+----------------+----------+-----------------+-------------------+
| DATABASE_ID | DATABASE_NAME | DATABASE_OWNER | IS_TRANSIENT | COMMENT | CREATED                       | LAST_ALTERED                  | DELETED                       | RETENTION_TIME | RESOURCE_GROUP | TYPE     | OWNER_ROLE_TYPE | OBJECT_VISIBILITY |
|-------------+---------------+----------------+--------------+---------+-------------------------------+-------------------------------+-------------------------------+----------------+----------------+----------+-----------------+-------------------|
|          55 | MY_DATABASE   | NULL           | NO           | NULL    | 2025-07-16 15:17:55.990 -0700 | 2025-07-17 15:19:52.305 -0700 | 2025-07-16 15:18:32.973 -0700 |              1 | NULL           | STANDARD | NULL            | NULL              |
+-------------+---------------+----------------+--------------+---------+-------------------------------+-------------------------------+-------------------------------+----------------+----------------+----------+-----------------+-------------------+
```

If you need to call this function for an INFORMATION\_SCHEMA view, pass in an empty string for the database name. For example, to
exclude the `replicable_with_failover_groups` column from the results of `SELECT *` queries of the
[DATABASES view in the INFORMATION\_SCHEMA schema](/sql-reference/info-schema/databases):

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  '',
  'INFORMATION_SCHEMA',
  'DATABASES',
  'database_name, database_owner, is_transient, comment, ' ||
  'created, last_altered, retention_time, type, '          ||
  'owner_role_type'
);
```

### Resetting the default columns for a Snowflake view

If you need to undo a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT call and return all columns in a
`SELECT *` query of a Snowflake view, call the
[SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object) function, specifying the type of object,
the database and schema that contain the view, and the name of the view. For example:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'DATABASES'
);
```

If you need to call this function for an INFORMATION\_SCHEMA view, pass in an empty string for the database name. For example:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  '',
  'INFORMATION_SCHEMA',
  'DATABASES'
);
```

### Getting the list of default columns for a Snowflake view

If you need to determine if SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was called for a specific view and you
want the list of columns that will be returned in a `SELECT *` query of that view, call the
[SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_get_default_columns_override_for_system_object) function, specifying the type of object, the
database and schema containing the view, and the name of the view. For example:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'DATABASES'
);
```

```
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(                                                                                                          |
|   'VIEW',                                                                                                                                                       |
|   'SNOWFLAKE',                                                                                                                                                  |
|   'ACCOUNT_USAGE',                                                                                                                                              |
|   'DATABASES'                                                                                                                                                   |
| )                                                                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DATABASE_ID,DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,DELETED,RETENTION_TIME,RESOURCE_GROUP,TYPE,OWNER_ROLE_TYPE,OBJECT_VISIBILITY |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

If you need to call this function for an INFORMATION\_SCHEMA view, pass in an empty string for the database name. For example:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  '',
  'INFORMATION_SCHEMA',
  'DATABASES'
);
```

```
+------------------------------------------------------------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(                                                     |
|   'VIEW',                                                                                                  |
|   '',                                                                                                      |
|   'INFORMATION_SCHEMA',                                                                                    |
|   'DATABASES'                                                                                              |
| )                                                                                                          |
|------------------------------------------------------------------------------------------------------------|
| DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,RETENTION_TIME,TYPE,OWNER_ROLE_TYPE |
+------------------------------------------------------------------------------------------------------------+
```

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was not previously called or if
SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was called, the function returns an empty string.

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'DATABASES'
);

SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'VIEW',
  'SNOWFLAKE',
  'ACCOUNT_USAGE',
  'DATABASES'
);
```

```
+--------------------------------------------------------+
| SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT( |
|   'VIEW',                                              |
|   'SNOWFLAKE',                                         |
|   'ACCOUNT_USAGE',                                     |
|   'DATABASES'                                          |
| )                                                      |
|--------------------------------------------------------|
|                                                        |
+--------------------------------------------------------+
```

### Overriding the default columns for a table function

To exclude newly introduced columns from the output of a built-in table function, call the
[SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_set_default_columns_override_for_system_object) function, specifying `'FUNCTION'` as the type
of object, the database and schema containing the table function, the name of the table function, and the list of columns that
should be returned.

For a table function in the [INFORMATION\_SCHEMA schema](/sql-reference/info-schema), pass in an empty string for the database
name and `'INFORMATION_SCHEMA'` for the schema name.

Suppose that a new `spcs_job_id` column has been introduced in the output of the
[TASK\_HISTORY table function](/sql-reference/functions/task_history). To prevent the new `spcs_job_id` column from being
returned in the output of the table function, call SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT, specifying
`'FUNCTION'` as the type of object, an empty string as the database, `'INFORMATION_SCHEMA'` as the schema, and `'TASK_HISTORY'`
as the table function. Pass in a comma-separated list of the columns that should be returned in the output (a list that excludes
`spcs_job_id`):

Copy code

```
SELECT SYSTEM$SET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'FUNCTION',
  '',
  'INFORMATION_SCHEMA',
  'TASK_HISTORY',
  'query_id, name, database_name, schema_name, query_text, '                    ||
  'condition_text, state, error_code, error_message, scheduled_time, '          ||
  'query_start_time, next_scheduled_time, completed_time, root_task_id, '       ||
  'graph_version, run_id, return_value, scheduled_from, attempt_number, '       ||
  'config, query_hash, query_hash_version, query_parameterized_hash, '          ||
  'query_parameterized_hash_version, graph_run_group_id, backfill_info'
);
```

The example uses the [||](/sql-reference/functions/concat) operator to construct a string that contains the comma-separated
list of columns.

When anyone in your account calls the TASK\_HISTORY table function, the new `spcs_job_id` column will not be returned in the
output.

Copy code

```
SELECT * FROM TABLE(<database_name>.INFORMATION_SCHEMA.TASK_HISTORY());
```

### Resetting the default columns for a table function

If you need to undo a previous SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT call and return all columns in the output
of a table function, call the
[SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_unset_default_columns_override_for_system_object) function, specifying `'FUNCTION'` as the
type of object, an empty string as the database, the schema that contains the table function, and the name of the table
function. For example:

Copy code

```
SELECT SYSTEM$UNSET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'FUNCTION',
  '',
  'INFORMATION_SCHEMA',
  'TASK_HISTORY'
);
```

### Getting the list of default columns for a table function

If you need to determine if SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was called for a specific table function and
you want the list of columns that will be returned in the output of that table function, call the
[SYSTEM$GET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT](/sql-reference/functions/system_get_default_columns_override_for_system_object) function, specifying `'FUNCTION'` as the type
of object, an empty string as the database, the schema that contains the table function, and the name of the table function.
For example:

Copy code

```
SELECT SYSTEM$GET_DEFAULT_COLUMNS_OVERRIDE_FOR_SYSTEM_OBJECT(
  'FUNCTION',
  '',
  'INFORMATION_SCHEMA',
  'TASK_HISTORY'
);
```

If SYSTEM$SET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was not previously called or if
SYSTEM$UNSET\_DEFAULT\_COLUMNS\_OVERRIDE\_FOR\_SYSTEM\_OBJECT was called, the function returns an empty string.

### Getting the list of columns from all previous calls for SHOW commands, Snowflake views, and table functions

To get the list of columns that are overridden for all SHOW commands, Snowflake views, and table functions, call the
[SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides) function. For example:

Copy code

```
SELECT SYSTEM$GET_ALL_DEFAULT_COLUMNS_OVERRIDES();
```

The function returns a string containing a JSON array of objects. Each object represents the list of columns for a specific SHOW
command, Snowflake view, or table function. For example:

```
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SYSTEM$GET_ALL_DEFAULT_COLUMNS_OVERRIDES()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [{"domain":"VIEW","isShowCommand":false,"dbName":"","schemaName":"INFORMATION_SCHEMA","objectName":"DATABASES","serializedDefaultColumns":"DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,RETENTION_TIME,TYPE,OWNER_ROLE_TYPE"},{"domain":"VIEW","isShowCommand":false,"dbName":"SNOWFLAKE","schemaName":"ACCOUNT_USAGE","objectName":"DATABASES","serializedDefaultColumns":"DATABASE_ID,DATABASE_NAME,DATABASE_OWNER,IS_TRANSIENT,COMMENT,CREATED,LAST_ALTERED,DELETED,RETENTION_TIME,RESOURCE_GROUP,TYPE,OWNER_ROLE_TYPE,OBJECT_VISIBILITY"},{"isShowCommand":true,"showCommandType":"NOTIFICATION INTEGRATIONS","serializedDefaultColumns":"name,type,category,enabled,comment,created_on"}] |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

For an explanation of the name/value pairs in each object, see
[SYSTEM$GET\_ALL\_DEFAULT\_COLUMNS\_OVERRIDES](/sql-reference/functions/system_get_all_default_columns_overrides).

## Updating scripts and code to prevent problems when new columns are introduced

To prevent problems from occurring due to the introduction of new columns, your scripts and code should select specific columns
from the output of SHOW commands and when querying Snowflake views and table functions.

To select specific columns from the output of SHOW commands, you can use the
[pipe operator](/sql-reference/operators-flow). See the example in [Select a list of columns for the output of a SHOW command](/sql-reference/operators-flow#label-pipe-operator-example-show).
