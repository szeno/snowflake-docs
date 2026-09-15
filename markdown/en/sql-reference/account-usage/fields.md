Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# FIELDS view

This Account Usage view displays a row for each field in a [structured OBJECT type](/sql-reference/data-types-structured)
and a row for the key and value in a [MAP](/sql-reference/data-types-structured) in an object (a column in a table) in the
account.

For MAPs, the view contains separate rows for the key and value.

Each row describes the type of the element in the structured ARRAY.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ROW\_IDENTIFIER | VARCHAR | Type identifier. Use this to join on:   - The DTD\_IDENTIFIER column in the [COLUMNS view](/sql-reference/info-schema/columns). - The DTD\_IDENTIFIER column in the [ELEMENT\_TYPES view](/sql-reference/info-schema/element_types#label-info-schema-element-types-view) (for nested types). - The DTD\_IDENTIFIER column in this view (for nested types). |
| FIELD\_NAME | VARCHAR | One of the following values:   - For structured OBJECTs, the name of the key. - For MAPs, KEY for the key or VALUE for the value. |
| OBJECT\_ID | VARCHAR | Internal/system-generated identifier for the object that uses this OBJECT or MAP type (e.g. name of a table). |
| OBJECT\_NAME | VARCHAR | Name of the object that uses this OBJECT or MAP type (e.g. name of a table). |
| OBJECT\_TYPE | VARCHAR | Type of the object that uses this OBJECT or MAP type:   - TABLE (if used by a column) |
| OBJECT\_SCHEMA\_ID | VARCHAR | Internal/system-generated identifier for the schema for the object that uses this OBJECT or MAP type. |
| OBJECT\_SCHEMA | VARCHAR | Schema that contains the object that uses this OBJECT or MAP type. |
| OBJECT\_CATALOG\_ID | VARCHAR | Internal/system-generated identifier for the database for the object that uses this OBJECT or MAP type. |
| OBJECT\_CATALOG | VARCHAR | Database that contains the object that uses this OBJECT or MAP type. |
| ORDINAL\_POSITION | NUMBER | The ordinal position of the key in the OBJECT or MAP. The position is 1-based.  For MAPs, the ordinal position of the key is 1, and the ordinal position of the value is 2. |
| DATA\_TYPE | VARCHAR | Data type of the value (for OBJECTs) or the key or value (for MAPs). |
| CHARACTER\_MAXIMUM\_LENGTH | NUMBER | Maximum length in characters of string keys or values. |
| CHARACTER\_OCTET\_LENGTH | NUMBER | Maximum length in bytes of string keys or values. |
| NUMERIC\_PRECISION | NUMBER | Numeric precision of numeric keys or values. |
| NUMERIC\_PRECISION\_RADIX | NUMBER | Radix of precision of numeric keys or values. |
| NUMERIC\_SCALE | NUMBER | Scale of numeric keys or values. |
| DATETIME\_PRECISION | NUMBER | Not applicable for Snowflake. |
| INTERVAL\_TYPE | VARCHAR | Not applicable for Snowflake. |
| INTERVAL\_PRECISION | NUMBER | Not applicable for Snowflake. |
| CHARACTER\_SET\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| CHARACTER\_SET\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| CHARACTER\_SET\_NAME | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| COLLATION\_NAME | VARCHAR | The collation specification for this keys or values. |
| UDT\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| UDT\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| UDT\_NAME | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| SCOPE\_NAME | VARCHAR | Not applicable for Snowflake. |
| MAXIMUM\_CARDINALITY | NUMBER | Maximum cardinality. Currently, this is always set to NULL. |
| DTD\_IDENTIFIER | VARCHAR | Nested type identifier. Use this to join on:   - The COLLECTION\_TYPE\_IDENTIFIER column in the [ELEMENT\_TYPES view](/sql-reference/info-schema/element_types#label-info-schema-element-types-view). - The ROW\_IDENTIFIER column in this view (for nested types). |
| IS\_NULLABLE | VARCHAR | `Y` if the structured OBJECT or MAP allows NULL values; `N` otherwise. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the object was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 90 minutes.

- The view only displays objects for which the current role for the session has been granted access privileges.
- The view does not honor the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command
  executed by a user who holds the MANAGE GRANTS privilege.
