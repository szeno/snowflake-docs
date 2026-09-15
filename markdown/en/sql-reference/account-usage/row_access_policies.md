Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# ROW\_ACCESS\_POLICIES view

This Account Usage view displays a row for each row access policy defined in your account.

Each row corresponds to a different row access policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| POLICY\_NAME | VARCHAR | Name of the row access policy. |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the row access policy. |
| POLICY\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| POLICY\_SCHEMA | VARCHAR | Schema to which the row access policy belongs. |
| POLICY\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| POLICY\_CATALOG | VARCHAR | Database to which the row access policy belongs. |
| POLICY\_OWNER | VARCHAR | Name of the role that owns the row access policy. |
| POLICY\_SIGNATURE | VARCHAR | Type signature of the row access policy’s arguments. |
| POLICY\_RETURN\_TYPE | VARCHAR | Return value data type. |
| POLICY\_BODY | VARCHAR | Row access policy definition. |
| POLICY\_COMMENT | VARIANT | Comments entered for the row access policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the row access policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the row access policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| OPTIONS | VARIANT | The value for the EXEMPT\_OTHER\_POLICIES property in the policy. If set to `TRUE`, the column returns `{ "EXEMPT_OTHER_POLICIES: "TRUE" }`. If the property is set to `FALSE` or not set at all, the column returns NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only returns rows if at least one row access policy has been created.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Example

Obtain all of the row access policies created in your account, ordered by the timestamp on which the policy was created:

> Copy code
>
> ```
> select policy_name, policy_signature, created
> from row_access_policies
> order by created
> ;
> ```
