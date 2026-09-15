Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SESSION\_POLICIES view

This Account Usage view provides the [session policies](/user-guide/session-policies) in your account.

Each row in this view corresponds to a different session policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the session policy. |
| NAME | VARCHAR | Name of the session policy. |
| SCHEMA\_ID | VARCHAR | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | VARCHAR | Schema to which the session policy belongs. |
| DATABASE\_ID | VARCHAR | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | VARCHAR | Database to which the session policy belongs. |
| OWNER | VARCHAR | Name of the role that owns the session policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| SESSION\_IDLE\_TIMEOUT\_MINS | NUMBER | Session idle timeout in minutes for the policy. |
| SESSION\_UI\_IDLE\_TIMEOUT\_MINS | NUMBER | UI session idle timeout in minutes for the policy. |
| SESSION\_MAX\_LIFESPAN\_MINS | NUMBER | Maximum session lifespan in minutes for the policy. |
| SESSION\_UI\_MAX\_LIFESPAN\_MINS | NUMBER | Maximum UI session lifespan in minutes for the policy. |
| COMMENT | VARCHAR | Comments entered for the session policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the session policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the session policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
