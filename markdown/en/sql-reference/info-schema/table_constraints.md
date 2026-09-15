# TABLE\_CONSTRAINTS view

This Information Schema view displays a row for each table constraint that is defined in the specified (or current) database.
This view returns information about the following constraint types:

- PRIMARY KEY
- FOREIGN KEY
- UNIQUE

For general information about constraints, see [Constraints](/sql-reference/constraints).

See also:
:   [REFERENTIAL\_CONSTRAINTS view](/sql-reference/info-schema/referential_constraints)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CONSTRAINT\_CATALOG | VARCHAR | Database that the constraint belongs to |
| CONSTRAINT\_SCHEMA | VARCHAR | Schema that the constraint belongs to |
| CONSTRAINT\_NAME | VARCHAR | Name of the constraint |
| TABLE\_CATALOG | VARCHAR | Name of the database of the current table |
| TABLE\_SCHEMA | VARCHAR | Name of the schema of the current table |
| TABLE\_NAME | VARCHAR | Name of the current table |
| CONSTRAINT\_TYPE | VARCHAR | Type of the constraint |
| IS\_DEFERRABLE | VARCHAR | Whether evaluation of the constraint can be deferred |
| INITIALLY\_DEFERRED | VARCHAR | Whether evaluation of the constraint is deferrable and initially deferred |
| ENFORCED | VARCHAR | Whether the constraint is enforced |
| COMMENT | VARCHAR | Comment for this constraint |
| CREATED | TIMESTAMP\_LTZ | Creation time of the constraint |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| RELY | VARCHAR | Whether a constraint in NOVALIDATE mode is taken into account during query rewrite. For details, see [Constraint properties](/sql-reference/sql/create-table-constraint#label-extended-constraint-properties). |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Example

Create a hybrid table with a multi-column PRIMARY KEY constraint and a comment on the constraint. Query the view to get information about the constraint.

Copy code

```
CREATE OR REPLACE HYBRID TABLE HT2PK
  (col1 NUMBER(38,0) NOT NULL,
  col2 NUMBER(38,0) NOT NULL,
  col3 VARCHAR(16777216),
  CONSTRAINT PKEY_2 PRIMARY KEY (col1, col2) COMMENT 'Primary key on two columns');

SELECT constraint_name, table_name, constraint_type, enforced, comment
  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
  WHERE COMMENT IS NOT NULL;
```

```
+-----------------+------------+-----------------+----------+----------------------------+
| CONSTRAINT_NAME | TABLE_NAME | CONSTRAINT_TYPE | ENFORCED | COMMENT                    |
|-----------------+------------+-----------------+----------+----------------------------|
| PKEY_2          | HT2PK      | PRIMARY KEY     | YES      | Primary key on two columns |
+-----------------+------------+-----------------+----------+----------------------------+
```

Return a list of constraints on all tables that have names beginning with `HT`:

Copy code

```
SELECT constraint_name, table_name, constraint_type, enforced, comment
  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
  WHERE table_name LIKE 'HT%'
  ORDER BY table_name;
```

```
+-----------------------------------------------------+------------------------+-----------------+----------+----------------------------+
| CONSTRAINT_NAME                                     | TABLE_NAME             | CONSTRAINT_TYPE | ENFORCED | COMMENT                    |
|-----------------------------------------------------+------------------------+-----------------+----------+----------------------------|
| SYS_CONSTRAINT_da2e8533-5501-4862-ae42-0a7798d578eb | HT01                   | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_5b3c6d13-f607-4ef6-a147-0026bae98c71 | HT1                    | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_d5887706-0e3b-4d5b-8787-e3327cdf4851 | HT100                  | PRIMARY KEY     | YES      | NULL                       |
| PK1                                                 | HT1PK                  | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_f1d1e153-cc32-477c-9a24-5c049e40ca0a | HT239                  | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_fe27c4f3-23f6-4091-92c4-5acd53cc5029 | HT239                  | UNIQUE          | YES      | NULL                       |
| PKEY_2                                              | HT2PK                  | PRIMARY KEY     | YES      | Primary key on two columns |
| SYS_CONSTRAINT_0bd41d0f-11f7-4366-82a3-f03f31fcce7e | HT616                  | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_6124310b-5f50-4009-a5c0-dc1b5a89b0bc | HT616                  | UNIQUE          | YES      | NULL                       |
| SYS_CONSTRAINT_bf3d76ba-de1e-4227-954f-9f53de777ed4 | HT619                  | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_c97bfe9b-6098-4b8a-b796-e341071db72a | HT619                  | FOREIGN KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_6e02d776-1759-449e-aece-467aaaefcfc8 | HTFK                   | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_51118aaf-1ee6-4548-bc9a-f87e65d92528 | HTFK                   | FOREIGN KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_fe27c4f3-23f6-4091-92c4-5acd53cc5029 | HTLIKE                 | UNIQUE          | YES      | NULL                       |
| SYS_CONSTRAINT_f1d1e153-cc32-477c-9a24-5c049e40ca0a | HTLIKE                 | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_aad16788-491a-4e68-b0e3-30d48a33a1c1 | HTPK                   | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_0bdff17e-e90a-4929-99c5-98e3597e3069 | HTT1                   | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_39e9110f-7a72-454e-bfe2-0a26eca97e7c | HT_PRECIP              | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_6acd8274-04e7-4b22-b9ae-29185b979219 | HT_SENSOR_DATA_DEVICE1 | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_39e9110f-7a72-454e-bfe2-0a26eca97e7c | HT_WEATHER             | PRIMARY KEY     | YES      | NULL                       |
| SYS_CONSTRAINT_843d828a-900d-409e-a57d-8f27b602eccf | HT_WEATHER             | PRIMARY KEY     | YES      | NULL                       |
+-----------------------------------------------------+------------------------+-----------------+----------+----------------------------+
```
