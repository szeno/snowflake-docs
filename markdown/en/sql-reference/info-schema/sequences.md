# SEQUENCES view

This Information Schema view displays a row for each sequence defined in the specified (or current) database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SEQUENCE\_CATALOG | VARCHAR | Database that the sequence belongs to |
| SEQUENCE\_SCHEMA | VARCHAR | Schema that the sequence belongs to |
| SEQUENCE\_NAME | VARCHAR | Name of the sequence |
| SEQUENCE\_OWNER | VARCHAR | Name of the role that owns the sequence |
| DATA\_TYPE | VARCHAR | Data type of the sequence |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of the data type of the sequence |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of the numeric precision of the data type of the sequence |
| NUMERIC\_SCALE | NUMBER | Scale of the data type of the sequence |
| START\_VALUE | VARCHAR | Initial value of the sequence |
| MINIMUM\_VALUE | VARCHAR | Not applicable for Snowflake. |
| MAXIMUM\_VALUE | VARCHAR | Not applicable for Snowflake. |
| NEXT\_VALUE | VARCHAR | Next value that the sequence will produce |
| INCREMENT | VARCHAR | Increment of the sequence generator |
| CYCLE\_OPTION | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the sequence |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| ORDERED | VARCHAR | If `YES`, the sequence has the ORDER property. If `NO`, the sequence has the NOORDER property. |
| COMMENT | VARCHAR | Comment for this sequence |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
