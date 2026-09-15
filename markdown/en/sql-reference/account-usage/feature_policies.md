Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# FEATURE\_POLICIES view

This Account Usage view provides the
[feature policies](/developer-guide/native-apps/ui-consumer-feature-policies) in your account.

Each row in this view corresponds to a different feature policy.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the feature policy. |
| NAME | TEXT | Name of the feature policy. |
| SCHEMA\_ID | TEXT | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | TEXT | Schema to which the feature policy belongs. |
| DATABASE\_ID | TEXT | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | TEXT | Database to which the feature policy belongs. |
| OWNER | TEXT | Name of the role that owns the feature policy. |
| OWNER\_ROLE\_TYPE | TEXT | The type of role that owns the object, for example ROLE. If a Snowflake Native App owns the object, the value is APPLICATION. Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| BLOCKED\_OBJECT\_TYPES\_FOR\_CREATION | TEXT | A comma-separated list of object types that the feature policy blocks for creation. See [Feature Policies](/developer-guide/native-apps/ui-consumer-feature-policies) for more information. |
| COMMENT | TEXT | Comments entered for the feature policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the feature policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the feature policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (two hours).

- The LAST\_ALTERED column is updated when the following operations are performed on an object:
  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
