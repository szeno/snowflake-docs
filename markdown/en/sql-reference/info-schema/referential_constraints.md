# REFERENTIAL\_CONSTRAINTS view

This Information Schema view displays a row for each FOREIGN KEY constraint that is defined for tables
in the specified (or current) database.

FOREIGN KEY constraints are used to enforce referential integrity. For more information, see
[Constraints](/sql-reference/constraints) and [Referential Integrity Constraints](/user-guide/table-considerations#label-table-considerations-referential-integrity-constraints).

To return information about other constraint types (as well as FOREIGN KEY constraints), query the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints).

See also:
:   [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CONSTRAINT\_CATALOG | VARCHAR | Database that the constraint belongs to |
| CONSTRAINT\_SCHEMA | VARCHAR | Schema that the constraint belongs to |
| CONSTRAINT\_NAME | VARCHAR | Name of the constraint |
| UNIQUE\_CONSTRAINT\_CATALOG | VARCHAR | Database of the unique constraint referenced by the current constraint |
| UNIQUE\_CONSTRAINT\_SCHEMA | VARCHAR | Schema of the unique constraint referenced by the current constraint |
| UNIQUE\_CONSTRAINT\_NAME | VARCHAR | Name of the unique constraint referenced by the current constraint |
| MATCH\_OPTION | VARCHAR | Match option for the constraint |
| UPDATE\_RULE | VARCHAR | Update Rule for the current constraint |
| DELETE\_RULE | VARCHAR | Delete Rule for the current constraint |
| COMMENT | VARCHAR | Comment for this constraint |
| CREATED | TIMESTAMP\_LTZ | Creation time of the constraint |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Return information about all of the FOREIGN KEY constraints in the current database.

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS;
```

```
+--------------------+-------------------+-----------------------------------------------------+---------------------------+--------------------------+-----------------------------------------------------+--------------+-------------+-------------+---------+-------------------------------+-------------------------------+
| CONSTRAINT_CATALOG | CONSTRAINT_SCHEMA | CONSTRAINT_NAME                                     | UNIQUE_CONSTRAINT_CATALOG | UNIQUE_CONSTRAINT_SCHEMA | UNIQUE_CONSTRAINT_NAME                              | MATCH_OPTION | UPDATE_RULE | DELETE_RULE | COMMENT | CREATED                       | LAST_ALTERED                  |
|--------------------+-------------------+-----------------------------------------------------+---------------------------+--------------------------+-----------------------------------------------------+--------------+-------------+-------------+---------+-------------------------------+-------------------------------|
| HTABLES_DB         | HTABLES_SCHEMA    | SYS_CONSTRAINT_51118aaf-1ee6-4548-bc9a-f87e65d92528 | HTABLES_DB                | HTABLES_SCHEMA           | SYS_CONSTRAINT_aad16788-491a-4e68-b0e3-30d48a33a1c1 | FULL         | NO ACTION   | NO ACTION   | NULL    | 2024-09-19 13:51:37.355 -0700 | 2024-09-19 13:51:37.608 -0700 |
| HTABLES_DB         | HTABLES_SCHEMA    | SYS_CONSTRAINT_c97bfe9b-6098-4b8a-b796-e341071db72a | HTABLES_DB                | HTABLES_SCHEMA           | SYS_CONSTRAINT_0bd41d0f-11f7-4366-82a3-f03f31fcce7e | FULL         | NO ACTION   | NO ACTION   | NULL    | 2024-05-28 18:21:43.899 -0700 | 2024-05-28 18:21:44.268 -0700 |
+--------------------+-------------------+-----------------------------------------------------+---------------------------+--------------------------+-----------------------------------------------------+--------------+-------------+-------------+---------+-------------------------------+-------------------------------+
```

Join this view to the [TABLE\_CONSTRAINTS view](/sql-reference/info-schema/table_constraints) to get the names of referencing tables that have FOREIGN KEY constraints:

Copy code

```
SELECT tc.constraint_catalog, tc.constraint_schema, tc.constraint_name, tc.table_name, tc.constraint_type, tc.enforced
  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
    JOIN INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc ON tc.constraint_name=rc.constraint_name;
```

```
+--------------------+-------------------+-----------------------------------------------------+------------+-----------------+----------+
| CONSTRAINT_CATALOG | CONSTRAINT_SCHEMA | CONSTRAINT_NAME                                     | TABLE_NAME | CONSTRAINT_TYPE | ENFORCED |
|--------------------+-------------------+-----------------------------------------------------+------------+-----------------+----------|
| HTABLES_DB         | HTABLES_SCHEMA    | SYS_CONSTRAINT_51118aaf-1ee6-4548-bc9a-f87e65d92528 | HTFK       | FOREIGN KEY     | YES      |
| HTABLES_DB         | HTABLES_SCHEMA    | SYS_CONSTRAINT_c97bfe9b-6098-4b8a-b796-e341071db72a | HT619      | FOREIGN KEY     | YES      |
+--------------------+-------------------+-----------------------------------------------------+------------+-----------------+----------+
```
