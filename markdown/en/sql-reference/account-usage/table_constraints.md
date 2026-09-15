Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLE\_CONSTRAINTS view

This Account Usage view displays a row for each table constraint that is defined for the tables in the account.

This view returns information about the following constraint types:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE

For general information about constraints, see [Constraints](/sql-reference/constraints).

See also:
:   [REFERENTIAL\_CONSTRAINTS view](/sql-reference/account-usage/referential_constraints)

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
