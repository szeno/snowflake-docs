Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# GRANTS\_TO\_SHARES view

This Account Usage view can be used to query access control privileges that have been granted to a share. The information in this view could have a latency of up to 3 hours.

## Columns

The following table provides definitions for the GRANTS\_TO\_SHARES view columns.

| Column | Data type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | The date and time when the privilege was granted to the share. |
| MODIFIED\_ON | TIMESTAMP\_LTZ | The date and time when the privilege was last updated. |
| DELETED\_ON | TIMESTAMP\_LTZ | The date and time when the privilege was revoked from the share. This value is null if the privilege hasn’t been revoked. |
| PRIVILEGE | VARCHAR | The name of the privilege granted on the object. |
| GRANTED\_ON | VARCHAR | The kind of the object on which the privilege was granted. |
| OBJECT\_NAME | VARCHAR | The name of the object on which the privilege was granted. |
| OBJECT\_DATABASE | VARCHAR | The database that contains the object on which the privilege was granted. A null value indicates that the object is not database-scoped. |
| OBJECT\_SCHEMA | VARCHAR | The schema that contains the object on which the privilege was granted. A null value indicates that the object is not schema-scoped. |
| SHARE\_NAME | VARCHAR | The name of the share to which the privilege was granted. |
| GRANTED\_BY | VARCHAR | The role that granted the privilege. A null value indicates that the privilege is a system grant. |
| GRANTED\_BY\_ROLE\_TYPE | VARCHAR | The type of role that granted the privilege. Values are `ROLE` and `DATABASE_ROLE`. |

Expand

Show lessSee more

## Usage notes

- This view doesn’t include access control privileges to the shares that have been dropped.
- This view records current grants and historical grants, including grants that were revoked or granted again.
- This view supports common data object types that can be granted to a share, including Database, Schema, Table, View, Function, Database
  Role, and so on.
