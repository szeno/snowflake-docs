# CLASS\_INSTANCES view

This Information Schema view displays a row for each [class](/sql-reference/snowflake-db-classes)
instance in a database.

See also:
:   [CLASS\_INSTANCE\_FUNCTIONS view](/sql-reference/info-schema/class_instance_functions),
    [CLASS\_INSTANCE\_PROCEDURES view](/sql-reference/info-schema/class_instance_procedures)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the instance. |
| SCHEMA\_NAME | VARCHAR | Name of the schema the instance belongs to. |
| DATABASE\_NAME | VARCHAR | Name of the database the instance belongs to. |
| CLASS\_NAME | VARCHAR | Name of the class the instance is instantiated from. |
| CLASS\_SCHEMA\_NAME | VARCHAR | Name of the schema of the class the instance is instantiated from. |
| CLASS\_DATABASE\_NAME | VARCHAR | Name of the database of the class the instance is instantiated from. |
| VERSION | VARCHAR | Current version of the instance. |
| OWNER | VARCHAR | Name of the role that owns the instance. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the instance was created. |
| COMMENT | VARCHAR | Comment for the instance. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not include instances that have been dropped. To view dropped instances, use
  the Account Usage [CLASS\_INSTANCES view](/sql-reference/account-usage/class_instances) instead.

## Examples

Retrieve the names of all instances, and the class they were instantiated from, in the `mydatabase` database:

Copy code

```
SELECT name, class_name, class_schema_name, class_database_name
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCES;
```
