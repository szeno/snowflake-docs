Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TABLE\_CONSTRAINTS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays a row for each table constraint that is defined for the tables in an account.

This view returns information about the following constraint types:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE

For general information about constraints, see [Constraints](/sql-reference/constraints).

See also:
:   [REFERENTIAL\_CONSTRAINTS view](/sql-reference/organization-usage/referential_constraints)

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
| CONSTRAINT\_ID | NUMBER | Internal/system-generated identifier for the constraint. |
| CONSTRAINT\_NAME | VARCHAR | Name of the constraint. |
| CONSTRAINT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the constraint. |
| CONSTRAINT\_SCHEMA | VARCHAR | Schema that the constraint belongs to. |
| CONSTRAINT\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the constraint. |
| CONSTRAINT\_CATALOG | VARCHAR | Database that the constraint belongs to. |
| TABLE\_ID | NUMBER | Internal/system-generated identifier for the table that the constraint belongs to. |
| TABLE\_NAME | VARCHAR | Name of the current table. |
| TABLE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the current table. |
| TABLE\_SCHEMA | VARCHAR | Name of the schema for the current table. |
| TABLE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the current table. |
| TABLE\_CATALOG | VARCHAR | Name of the database for the current table. |
| CONSTRAINT\_TYPE | VARCHAR | Type of the constraint (`PRIMARY KEY`, `UNIQUE KEY`, or `FOREIGN KEY`). |
| IS\_DEFERRABLE | VARCHAR | Whether evaluation of the constraint can be deferred; by default, always `N`. |
| INITIALLY\_DEFERRED | VARCHAR | Whether evaluation of the constraint is deferrable and initially deferred; by default, always `Y`. |
| ENFORCED | VARCHAR | Whether the constraint is enforced; by default, always `N`. |
| COMMENT | VARCHAR | Comment for the constraint. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the constraint was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the constraint was dropped. |
| RELY | VARCHAR | Whether a constraint in NOVALIDATE mode is taken into account during query rewrite. For details, see [Constraint properties](/sql-reference/sql/create-table-constraint#label-extended-constraint-properties). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
