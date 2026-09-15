# Summary of data types

Snowflake supports most SQL data types. The following table provides a summary of the supported data types:

| Category | Type | Notes |
| --- | --- | --- |
| [Numeric data types](/sql-reference/data-types-numeric) | NUMBER | Default precision and scale are (38,0). |
| DECIMAL, NUMERIC | Synonymous with NUMBER. |
| INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT | Synonymous with NUMBER, except precision and scale can’t be specified. |
| FLOAT, FLOAT4, FLOAT8 | [1] |
| DOUBLE, DOUBLE PRECISION, REAL | Synonymous with FLOAT. [1] |
| DECFLOAT | Stores numbers exactly, with up to 38 significant digits of precision, and uses a dynamic base-10 exponent. |
| [String & binary data types](/sql-reference/data-types-text) | VARCHAR | Default length is 16777216 bytes. Maximum length is 134217728 bytes. |
| CHAR, CHARACTER | Synonymous with VARCHAR, except the default length is VARCHAR(1). |
| STRING, TEXT | Synonymous with VARCHAR. |
| BINARY |  |
| VARBINARY | Synonymous with BINARY. |
| [Logical data types](/sql-reference/data-types-logical) | BOOLEAN | Currently only supported for accounts provisioned after January 25, 2016. |
| [Date & time data types](/sql-reference/data-types-datetime) | DATE |  |
| DATETIME | Synonymous with TIMESTAMP\_NTZ. |
| TIME |  |
| TIMESTAMP | Alias for one of the TIMESTAMP variations (TIMESTAMP\_NTZ by default). |
| TIMESTAMP\_LTZ | TIMESTAMP with local time zone; time zone, if provided, isn’t stored. |
| TIMESTAMP\_NTZ | TIMESTAMP with no time zone; time zone, if provided, isn’t stored. |
| TIMESTAMP\_TZ | TIMESTAMP with time zone. |
| [Semi-structured data types](/sql-reference/data-types-semistructured) | VARIANT |  |
| OBJECT |  |
| ARRAY |  |
| [Structured data types](/sql-reference/data-types-structured) | ARRAY |  |
| OBJECT |  |
| MAP |  |
| [Unstructured data types](/sql-reference/data-types-unstructured) | FILE | See [Introduction to unstructured data](/user-guide/unstructured-intro). |
| [Geospatial data types](/sql-reference/data-types-geospatial) | GEOGRAPHY |  |
| GEOMETRY |  |
| [UUID data type](/sql-reference/data-types-uuid) | UUID |  |
| [Vector data types](/sql-reference/data-types-vector) | VECTOR |  |
| [UNKNOWN data type](/sql-reference/data-types-unknown) | UNKNOWN | Iceberg v3 type used when a more specific column type isn’t known yet. Supported only in Iceberg tables. Has no storage and always reads as NULL. |
| [User-defined types](/sql-reference/data-types-user-defined) | Not applicable | Defined by the user based on existing Snowflake data types. |

Expand

Show lessSee more

[1] A known issue in Snowflake displays FLOAT, FLOAT4, FLOAT8, REAL, DOUBLE, and DOUBLE PRECISION as FLOAT, even though they are stored as DOUBLE.
