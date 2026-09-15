# Unsupported data types

Snowflake doesn’t support the following data types:

| Category | Type | Notes |
| --- | --- | --- |
| LOB (Large Object) | BLOB | BINARY can be used instead; maximum of 67108864 bytes. For more information, see [String & binary data types](/sql-reference/data-types-text). |
| CLOB | VARCHAR can be used instead; maximum of 134217728 bytes (for single-byte). For more information, see [String & binary data types](/sql-reference/data-types-text). |
| Other | ENUM |  |

Expand

Show lessSee more
