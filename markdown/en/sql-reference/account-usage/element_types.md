Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# ELEMENT\_TYPES view

This Account Usage view displays a row for each [structured ARRAY type](/sql-reference/data-types-structured) in an
object (a column in a table) in the account.

Each row describes the type of the element in the structured ARRAY.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| COLLECTION\_TYPE\_IDENTIFIER | VARCHAR | Type identifier. Use this to join on:   - The DTD\_IDENTIFIER column in the [COLUMNS view](/sql-reference/info-schema/columns). - The DTD\_IDENTIFIER column in this view (for nested types). - The DTD\_IDENTIFIER column in the [FIELDS view](/sql-reference/info-schema/fields#label-info-schema-fields-view) (for nested types). |
| OBJECT\_ID | VARCHAR | Internal/system-generated identifier for the object that uses this ARRAY type (e.g. name of a table). |
| OBJECT\_NAME | VARCHAR | Name of the object that uses this ARRAY type (e.g. name of a table). |
| OBJECT\_TYPE | VARCHAR | Type of the object that uses this ARRAY type:   - TABLE (if used by a column) |
| OBJECT\_SCHEMA\_ID | VARCHAR | Internal/system-generated identifier for the schema of the object that uses this ARRAY type. |
| OBJECT\_SCHEMA | VARCHAR | Schema that contains the object that uses this ARRAY type. |
| OBJECT\_CATALOG\_ID | VARCHAR | Internal/system-generated identifier for the database of the object that uses this ARRAY type. |
| OBJECT\_CATALOG | VARCHAR | Database that contains the object that uses this ARRAY type. |
| DATA\_TYPE | VARCHAR | Data type of the element. |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string elements. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string elements. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric elements. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric elements. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric elements. |
| DATETIME\_PRECISION | NUMBER | Not applicable for Snowflake. |
| INTERVAL\_TYPE | VARCHAR | Not applicable for Snowflake. |
| INTERVAL\_PRECISION | NUMBER | Not applicable for Snowflake. |
| CHARACTER\_SET\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| CHARACTER\_SET\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| CHARACTER\_SET\_NAME | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_NAME | VARCHAR | The collation specification for this element |
| UDT\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| UDT\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| UDT\_NAME | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_NAME | VARCHAR | Not applicable for Snowflake. |
| MAXIMUM\_CARDINALITY | NUMBER | Maximum cardinality. Currently, this is always set to NULL. |
| DTD\_IDENTIFIER | VARCHAR | Nested type identifier. Use this to join on:   - The COLLECTION\_TYPE\_IDENTIFIER column in this view. - The ROW\_IDENTIFIER column in the [FIELDS view](/sql-reference/info-schema/fields#label-info-schema-fields-view) (for nested types). |
| IS\_NULLABLE | VARCHAR | `Y` if the structured ARRAY allows NULL values; `N` otherwise. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the object was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 90 minutes.

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not honor the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
