Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CLASS\_INSTANCES view

This Account Usage view displays a row for each instance of a class defined in the account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the instance. |
| NAME | VARCHAR | Name of the instance. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the instance. |
| SCHEMA\_NAME | VARCHAR | Name of the schema the instance belongs to. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the instance. |
| DATABASE\_NAME | VARCHAR | Name of the database the instance belongs to. |
| CLASS\_ID | NUMBER | Internal/system-generated identifier for the class the instance is instantiated from. |
| CLASS\_NAME | VARCHAR | Name of the class the instance is instantiated from. |
| CLASS\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the class the instance is instantiated from. |
| CLASS\_SCHEMA\_NAME | VARCHAR | Name of the schema of the class the instance is instantiated from. |
| CLASS\_DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the class the instance is instantiated from. |
| CLASS\_DATABASE\_NAME | VARCHAR | Name of the database of the class the instance is instantiated from. |
| OWNER\_NAME | VARCHAR | Name of the role that owns the instance. |
| OWNER\_ROLE\_TYPE | VARCHAR | The internal/system-generated identifier of the role that owns the instance of the class. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the instance was created. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the instance was deleted. |
| COMMENT | VARCHAR | Comment for the instance. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays the instances for which the current role for the session has been granted access privileges.

## Examples

The following example finds all instances of the [ANOMALY\_DETECTION](/sql-reference/classes/anomaly_detection) class:

Copy code

```
SELECT NAME, DATABASE_NAME, SCHEMA_NAME, CLASS_NAME
  FROM SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES
  WHERE CLASS_NAME = 'ANOMALY_DETECTION';
```

The following example joins this view with [TABLES view](/sql-reference/account-usage/tables) on the INSTANCE\_ID column to find the tables
that belong to each instance:

Copy code

```
SELECT a.TABLE_NAME,
       b.NAME AS instance_name,
       b.CLASS_NAME
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES a
  JOIN SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES b
  ON a.INSTANCE_ID = b.ID
  WHERE b.DELETED IS NULL;
```
