Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# REFERENTIAL\_CONSTRAINTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each FOREIGN KEY constraint that is defined for tables in each account.

FOREIGN KEY constraints are used to enforce referential integrity. For more information, see
[Constraints](/sql-reference/constraints) and [Referential Integrity Constraints](/user-guide/table-considerations#label-table-considerations-referential-integrity-constraints).

To return information about other constraint types (as well as FOREIGN KEY constraints), query the [TABLE\_CONSTRAINTS view](/sql-reference/organization-usage/table_constraints).

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
| CONSTRAINT\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the constraint. |
| CONSTRAINT\_CATALOG | VARCHAR | Database that the constraint belongs to |
| CONSTRAINT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the constraint. |
| CONSTRAINT\_SCHEMA | VARCHAR | Schema that the constraint belongs to |
| CONSTRAINT\_NAME | VARCHAR | Name of the constraint |
| UNIQUE\_CONSTRAINT\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the current constraint. |
| UNIQUE\_CONSTRAINT\_CATALOG | VARCHAR | Database of the unique constraint referenced by the current constraint. |
| UNIQUE\_CONSTRAINT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the constraint. |
| UNIQUE\_CONSTRAINT\_SCHEMA | VARCHAR | Schema of the unique constraint referenced by the current constraint. |
| UNIQUE\_CONSTRAINT\_NAME | VARCHAR | Name of the unique constraint referenced by the current constraint. |
| MATCH\_OPTION | VARCHAR | Match option for the constraint. |
| UPDATE\_RULE | VARCHAR | Update Rule for the current constraint. |
| DELETE\_RULE | VARCHAR | Delete Rule for the current constraint. |
| COMMENT | VARCHAR | Comment for the constraint. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the constraint was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the constraint was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
