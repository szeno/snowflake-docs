# CLASSES view

This Information Schema view displays a row for each [class](/sql-reference/snowflake-db-classes)
in the database.

See also:
:   [CLASSES view](/sql-reference/account-usage/classes),
    [CLASS\_INSTANCES view](/sql-reference/info-schema/class_instances)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the instance. |
| SCHEMA\_NAME | VARCHAR | Name of the schema the instance belongs to. |
| DATABASE\_NAME | VARCHAR | Name of the database the instance belongs to. |
| VERSION | VARCHAR | Version of the class that is currently active in this account. |
| OWNER | VARCHAR | Name of the role that owns the instance. |
| OWNER\_ROLE\_TYPE | VARCHAR | The internal/system-generated identifier of the role that owns the instance of the class. |
| IS\_SERVICE\_CLASS | VARCHAR | TRUE if the class is a SERVICE class. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the instance was created. |
| COMMENT | VARCHAR | Comment for the instance. |

Expand

Show lessSee more

## Usage notes

The view only displays objects for which the current role for the session has been granted access privileges.

## Examples

Retrieve all classes in the SNOWFLAKE database:

Copy code

```
SELECT name, schema_name, database_name, version
    FROM SNOWFLAKE.INFORMATION_SCHEMA.CLASSES;
```
