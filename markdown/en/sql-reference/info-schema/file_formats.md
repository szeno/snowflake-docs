# FILE\_FORMATS view

This Information Schema view displays a row for each file format defined in the specified (or current) database.

File formats are named objects that can be used for loading/unloading data. For more information, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FILE\_FORMAT\_CATALOG | VARCHAR | Database that the file format belongs to |
| FILE\_FORMAT\_SCHEMA | VARCHAR | Schema that the file format belongs to |
| FILE\_FORMAT\_NAME | VARCHAR | Name of the file format |
| FILE\_FORMAT\_OWNER | VARCHAR | Name of the role that owns the file format |
| FILE\_FORMAT\_TYPE | VARCHAR | Type of the file format |
| RECORD\_DELIMITER | VARCHAR | Character that separates records |
| FIELD\_DELIMITER | VARCHAR | Character that separates fields |
| SKIP\_HEADER | NUMBER | Number of lines skipped at the start of the file |
| DATE\_FORMAT | VARCHAR | Date format |
| TIME\_FORMAT | VARCHAR | Time format |
| TIMESTAMP\_FORMAT | VARCHAR | Timestamp format |
| BINARY\_FORMAT | VARCHAR | Binary format |
| ESCAPE | VARCHAR | String used as the escape character for any field values |
| ESCAPE\_UNENCLOSED\_FIELD | VARCHAR | String used as the escape character for unenclosed field values |
| TRIM\_SPACE | VARCHAR | Whether whitespace is removed from fields |
| FIELD\_OPTIONALLY\_ENCLOSED\_BY | VARCHAR | Character used to enclose strings |
| NULL\_IF | VARCHAR | A list of strings to be replaced by null |
| COMPRESSION | VARCHAR | Compression method for the data file |
| ERROR\_ON\_COLUMN\_COUNT\_MISMATCH | VARCHAR | Whether to generate a parsing error if the number of fields in an input file does not match the number of columns in the corresponding table |
| CREATED | TIMESTAMP\_LTZ | Creation time of the file format |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| COMMENT | VARCHAR | Comment for this file format |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
