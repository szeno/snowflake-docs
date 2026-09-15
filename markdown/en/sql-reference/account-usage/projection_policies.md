Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PROJECTION\_POLICIES view

This Account Usage view provides the projection policies in your account.

Each row in this view corresponds to a different projection policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| POLICY\_NAME | VARCHAR | Name of the projection policy. |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the projection policy. |
| POLICY\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| POLICY\_SCHEMA | VARCHAR | Schema that contains the projection policy. |
| POLICY\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| POLICY\_CATALOG | VARCHAR | Database to which the projection policy belongs. |
| POLICY\_OWNER | VARCHAR | Name of the role that owns the projection policy. |
| POLICY\_SIGNATURE | VARCHAR | Type signature of the projection policy’s arguments. |
| POLICY\_RETURN\_TYPE | VARCHAR | Return value data type. |
| POLICY\_BODY | VARCHAR | Projection policy definition. |
| POLICY\_COMMENT | VARIANT | Comments entered for the projection policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the projection policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the projection policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the projection policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
