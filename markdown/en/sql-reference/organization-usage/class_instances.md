Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# CLASS\_INSTANCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each instance of a class defined in the account.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

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
SELECT ACCOUNT_NAME, NAME, DATABASE_NAME, SCHEMA_NAME, CLASS_NAME
  FROM snowflake.organization_usage.class_instances
  WHERE CLASS_NAME = 'ANOMALY_DETECTION';
```

The following example joins this view with [TABLES view](/sql-reference/organization-usage/tables) on the INSTANCE\_ID column to find the tables
that belong to each instance:

Copy code

```
SELECT a.TABLE_NAME,
       b.NAME AS instance_name,
       b.CLASS_NAME
  FROM SNOWFLAKE.ORGANIZATION_USAGE.TABLES a
  JOIN SNOWFLAKE.ORGANIZATION_USAGE.CLASS_INSTANCES b
  ON a.INSTANCE_ID = b.ID
  WHERE b.DELETED IS NULL;
```
