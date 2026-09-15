Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TYPES view

This Account Usage view displays a row for each [user-defined type](/sql-reference/data-types-user-defined)
defined in the account.

See also:
:   [TYPES view](/sql-reference/info-schema/types) (Information Schema) ,
    [TYPES view](/sql-reference/organization-usage/types) (Organization Usage)

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| TYPE\_ID | NUMBER | Internal/system-generated identifier for the type. |
| TYPE\_NAME | VARCHAR | Name of the type. |
| TYPE\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema that contains the type. |
| TYPE\_SCHEMA | VARCHAR | Schema that contains the type. |
| TYPE\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database that contains the type. |
| TYPE\_CATALOG | VARCHAR | Database that contains the type. |
| TYPE\_OWNER | VARCHAR | Name of the role that owns the type. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
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
| CREATED | TIMESTAMP\_LTZ | Date and time when the type was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the type was dropped. |
| COMMENT | VARCHAR | Comment for this type. |

Expand

Show lessSee more

## Usage notes

- Latency for the view might be up to 120 minutes (2 hours).
- The view only displays objects for which the current role for the session has been granted access privileges.
- The view doesn’t recognize the MANAGE GRANTS privilege and consequently might show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

## Examples

Retrieve all user-defined types in the account:

Copy code

```
SELECT type_name, type_catalog, type_schema, type_owner, base_data_type
  FROM SNOWFLAKE.ACCOUNT_USAGE.TYPES
  ORDER BY created DESC;
```

Retrieve user-defined types that have been dropped:

Copy code

```
SELECT type_name, type_catalog, type_schema, deleted
  FROM SNOWFLAKE.ACCOUNT_USAGE.TYPES
  WHERE deleted IS NOT NULL
  ORDER BY deleted DESC;
```
