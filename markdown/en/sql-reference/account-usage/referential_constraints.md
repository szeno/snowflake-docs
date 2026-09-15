Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# REFERENTIAL\_CONSTRAINTS view

This Account Usage view displays a row for each FOREIGN KEY constraint that is defined for tables in the account.

FOREIGN KEY constraints are used to enforce referential integrity. For more information, see
[Constraints](/sql-reference/constraints) and [Referential Integrity Constraints](/user-guide/table-considerations#label-table-considerations-referential-integrity-constraints).

To return information about other constraint types (as well as FOREIGN KEY constraints), query the [TABLE\_CONSTRAINTS view](/sql-reference/account-usage/table_constraints).

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
