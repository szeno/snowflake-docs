Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# FILE\_FORMATS view

This Account Usage view displays a row for each file format defined in the account.

File formats are named objects that can be used for loading/unloading data. For more information, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| FILE\_FORMAT\_ID | NUMBER | Internal/system-generated identifier for the file format. |
| FILE\_FORMAT\_NAME | VARCHAR | Name of the file format, |
| FILE\_FORMAT\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the file format. |
| FILE\_FORMAT\_SCHEMA | VARCHAR | Schema that the file format belongs to. |
| FILE\_FORMAT\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the file format. |
| FILE\_FORMAT\_CATALOG | VARCHAR | Database that the file format belongs to. |
| FILE\_FORMAT\_OWNER | VARCHAR | Name of the role that owns the file format. |
| FILE\_FORMAT\_TYPE | VARCHAR | File format type of the file format (`CSV`, `JSON`, etc.). |
| RECORD\_DELIMITER | VARCHAR | Character that separates records. |
| FIELD\_DELIMITER | VARCHAR | Character that separates fields. |
| SKIP\_HEADER | NUMBER | Number of lines skipped at the start of the file. |
| DATE\_FORMAT | VARCHAR | Date format. |
| TIME\_FORMAT | VARCHAR | Time format. |
| TIMESTAMP\_FORMAT | VARCHAR | Timestamp format. |
| BINARY\_FORMAT | VARCHAR | Binary format. |
| ESCAPE | VARCHAR | String used as the escape character for any field values. |
| ESCAPE\_UNENCLOSED\_FIELD | VARCHAR | String used as the escape character for unenclosed field values. |
| TRIM\_SPACE | BOOLEAN | Whether whitespace is removed from fields. |
| FIELD\_OPTIONALLY\_ENCLOSED\_BY | VARCHAR | Character used to enclose strings. |
| NULL\_IF | VARCHAR | A list of strings to be replaced by null. |
| COMPRESSION | VARCHAR | Compression method for the data file. |
| ERROR\_ON\_COLUMN\_COUNT\_MISMATCH | VARCHAR | Whether to generate a parsing error if the number of fields in an input file does not match the number of columns in the corresponding table. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the file format was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the file format was dropped. |
| COMMENT | VARCHAR | Comment for the file format. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
