Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SEQUENCES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each sequence defined in an account.

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
| SEQUENCE\_ID | NUMBER | Internal/system-generated identifier for the sequence. |
| SEQUENCE\_NAME | VARCHAR | Name of the sequence. |
| SEQUENCE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the sequence. |
| SEQUENCE\_SCHEMA | VARCHAR | Schema that the sequence belongs to. |
| SEQUENCE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the sequence. |
| SEQUENCE\_CATALOG | VARCHAR | Database that the sequence belongs to. |
| SEQUENCE\_OWNER | VARCHAR | Name of the role that owns the sequence. |
| DATA\_TYPE | VARCHAR | Data type of the sequence. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of the data type of the sequence. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of the numeric precision of the data type of the sequence. |
| NUMERIC\_SCALE | NUMBER | Scale of the data type of the sequence. |
| START\_VALUE | VARCHAR | Initial value of the sequence. |
| MINIMUM\_VALUE | VARCHAR | Not applicable for Snowflake. |
| MAXIMUM\_VALUE | VARCHAR | Not applicable for Snowflake. |
| NEXT\_VALUE | VARCHAR | Next value that the sequence will produce. |
| INCREMENT | VARCHAR | Increment of the sequence generator. |
| CYCLE\_OPTION | VARCHAR | Not applicable for Snowflake. |
| ORDERED | VARCHAR | If `YES`, the sequence has the ORDER property. If `NO`, the sequence has the NOORDER property. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the sequence was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the sequence was dropped. |
| COMMENT | VARCHAR | Comment for the sequence. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
