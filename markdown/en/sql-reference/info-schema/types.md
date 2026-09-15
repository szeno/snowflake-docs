# TYPES view

This Information Schema view displays a row for each [user-defined type](/sql-reference/data-types-user-defined)
defined in the specified or current database.

See also:
:   [TYPES view](/sql-reference/account-usage/types) (Account Usage) ,
    [TYPES view](/sql-reference/organization-usage/types) (Organization Usage)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| TYPE\_CATALOG | VARCHAR | Database that contains the type. |
| TYPE\_SCHEMA | VARCHAR | Schema that contains the type. |
| TYPE\_NAME | VARCHAR | Name of the type. |
| TYPE\_OWNER | VARCHAR | Name of the role that owns the type. |
| BASE\_DATA\_TYPE | VARCHAR | Underlying data type of the user-defined type. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters for VARCHAR types. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes for VARCHAR types. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision for NUMBER types. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of the numeric precision for NUMBER types. |
| NUMERIC\_SCALE | NUMBER | Numeric scale for NUMBER types. |
| DATETIME\_PRECISION | NUMBER | Fractional seconds precision for TIMESTAMP types. |
| CHECK\_EXPRESSION | VARCHAR | Not applicable for Snowflake. |
| DEFAULT\_EXPRESSION | VARCHAR | Not applicable for Snowflake. |
| IS\_NULLABLE\_DEFAULT | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_NAME | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the type. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| COMMENT | VARCHAR | Comment for this type. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view doesn’t
  honor the MANAGE GRANTS privilege and consequently might show less information compared to a SHOW command when both are executed
  by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve all user-defined types in the `mydb` database:

Copy code

```
SELECT type_name, type_owner, base_data_type
  FROM mydb.INFORMATION_SCHEMA.TYPES;
```

Retrieve all user-defined types in a specific schema:

Copy code

```
SELECT type_name, type_owner, base_data_type
  FROM mydb.INFORMATION_SCHEMA.TYPES
  WHERE type_schema = 'MY_SCHEMA';
```
