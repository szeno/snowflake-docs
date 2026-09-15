Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CLASSES view

This Account Usage view displays a row for each [class](/sql-reference/snowflake-db-classes)
in the account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the class. |
| NAME | VARCHAR | Name of the class. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the class. |
| SCHEMA\_NAME | VARCHAR | Name of the schema the class belongs to. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the class. |
| DATABASE\_NAME | VARCHAR | Name of the database the class belongs to. |
| OWNER\_NAME | VARCHAR | Name of the role that owns the class. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the class was created. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the class was deleted. |
| COMMENT | VARCHAR | Comment for the class. |

Expand

Show lessSee more

## Usage notes

Latency for the view may be up to 180 minutes (3 hours).

## Examples

The following example finds all classes in the account:

Copy code

```
SELECT name, database_name, schema_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.CLASSES;
```
