Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# MASKING\_POLICIES view

This Account Usage view provides the masking policies in your account.

Each row in this view corresponds to a different masking policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| POLICY\_NAME | VARCHAR | Name of the masking policy. |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the masking policy. |
| POLICY\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| POLICY\_SCHEMA | VARCHAR | Schema to which the masking policy belongs. |
| POLICY\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| POLICY\_CATALOG | VARCHAR | Database to which the masking policy belongs. |
| POLICY\_OWNER | VARCHAR | Name of the role that owns the masking policy. |
| POLICY\_SIGNATURE | VARCHAR | Type signature of the masking policy’s arguments. |
| POLICY\_RETURN\_TYPE | VARCHAR | Return value data type. |
| POLICY\_BODY | VARCHAR | Masking policy definition. |
| POLICY\_COMMENT | VARIANT | Comments entered for the masking policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the masking policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the masking policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| OPTIONS | VARIANT | The value for the EXEMPT\_OTHER\_POLICIES property in the policy. If set to `TRUE`, the column returns `{ "EXEMPT_OTHER_POLICIES: "TRUE" }`. If the property is set to `FALSE` or not set at all, the column returns NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
