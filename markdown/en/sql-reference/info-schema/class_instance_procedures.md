# CLASS\_INSTANCE\_PROCEDURES view

This Information Schema view displays a row for each procedure in a
[class](/sql-reference/snowflake-db-classes) instance.

See also:
:   [CLASS\_INSTANCES view](/sql-reference/info-schema/class_instances),
    [CLASS\_INSTANCE\_FUNCTIONS view](/sql-reference/info-schema/class_instance_functions),
    [SHOW PROCEDURES](/sql-reference/sql/show-procedures)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PROCEDURE\_NAME | VARCHAR | Name of the stored procedure. |
| PROCEDURE\_INSTANCE\_NAME | VARCHAR | Name of the class instance to which the procedure belongs. |
| PROCEDURE\_INSTANCE\_SCHEMA | VARCHAR | Name of the schema to which the class instance belongs. |
| PROCEDURE\_INSTANCE\_DATABASE | VARCHAR | Name of the database to which the class instance belongs. |
| PROCEDURE\_OWNER | VARCHAR | Name of the role that owns the stored procedure. |
| ARGUMENT\_SIGNATURE | VARCHAR | Type signature of the stored procedure’s arguments. |
| DATA\_TYPE | VARCHAR | Return value data type. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string return value. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string return value. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric return value. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric return value. |
| NUMERIC\_SCALE | VARCHAR | Scale of numeric return value. |
| PROCEDURE\_LANGUAGE | VARCHAR | Language of the stored procedure. |
| PROCEDURE\_DEFINITION | VARCHAR | Stored procedure definition. |
| CREATED | TIMESTAMP\_LTZ | Date and time the stored procedure was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for the stored procedure. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted
  an instance role with access privileges.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve the procedures for instances in the `mydatabase` database:

Copy code

```
SELECT procedure_name,
       procedure_instance_name,
       argument_signature,
       data_type AS return_value_data_type
    FROM mydatabase.INFORMATION_SCHEMA.CLASS_INSTANCE_PROCEDURES;
```
