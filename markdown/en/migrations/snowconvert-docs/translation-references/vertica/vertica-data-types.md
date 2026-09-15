# Vertica - Data types

Snowflake supports most basic [SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

## Binary Data Type

| Vertica | Snowflake |
| --- | --- |
| [BINARY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/binary-data-types-binary-and-varbinary/) | [BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary) |
| [VARBINARY (synonyms: BYTEA, RAW, BINARY VARYING)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/binary-data-types-binary-and-varbinary/) | [BINARY (synonyms: VARBINARY, BINARY VARYING)](https://docs.snowflake.com/en/sql-reference/data-types-text#binary) |
| [LONG VARBINARY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/long-data-types/) | [BINARY](https://docs.snowflake.com/en/sql-reference/data-types-text#binary)    *Notes: Vertica’s `LONG VARBINARY` supports up to 32,000,000 bytes (**~30.5MB)**, while Snowflake’s `BINARY` is limited to (8,388,608 bytes) **8MB**. This size difference means you might need an alternative solution for mapping larger `LONG VARBINARY` data.* |

Expand

Show lessSee more

## Boolean Data Type

| Vertica | Snowflake |
| --- | --- |
| [BOOLEAN](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/boolean-data-type/) | [BOOLEAN](https://docs.snowflake.com/en/sql-reference/data-types-logical#boolean) |

Expand

Show lessSee more

## Character Data Type

| Vertica | Snowflake |
| --- | --- |
| [CHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/character-data-types-char-and-varchar/) | [CHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#char-character-nchar) |
| [VARCHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/character-data-types-char-and-varchar/) | [VARCHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar) |
| [LONG VARCHAR](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/long-data-types/) | [VARCHAR](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar)    *Notes: Vertica’s `LONG VARCHAR` supports up to 32,000,000 bytes (**~30.5MB)**, while Snowflake’s `VARCHAR` is limited to 16,777,216 bytes (**16MB)**. This size difference means you might need an alternative solution for mapping larger `LONG VARCHAR` data.* |

Expand

Show lessSee more

## Date/Time Data Type

| Vertica | Snowflake |
| --- | --- |
| [DATE](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/date/) | [DATE](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-date)    *Notes: Be aware of* [*Snowflake’s*](https://docs.snowflake.com/en/sql-reference/data-types-datetime#data-types) *recommended year range (1582-9999).* |
| [TIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timetimetz/) | [TIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-time) |
| [TIME WITH TIMEZONE (TIMETZ)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#label-datatypes-time)    *Notes: TIME data type in Snowflake does not persist this timezone attribute.* [*`SSC-FDM-0005`*](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0005) *is added.* |
| [TIMESTAMP](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp) |
| [DATETIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/datetime/) | [DATETIME](https://docs.snowflake.com/en/sql-reference/data-types-datetime#datetime) |
| [SMALLDATETIME](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/smalldatetime/) | [TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |
| [TIMESTAMP WITH TIMEZONE (TIMESTAMPTZ)](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP\_TZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |
| [TIMESTAMP WITHOUT TIME ZONE](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/datetime-data-types/timestamptimestamptz/) | [TIMESTAMP\_NTZ](https://docs.snowflake.com/en/sql-reference/data-types-datetime#timestamp-ltz-timestamp-ntz-timestamp-tz) |

Expand

Show lessSee more

## Approximate Numeric Data Type

| Vertica | Snowflake |
| --- | --- |
| [DOUBLE PRECISION](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [DOUBLE PRECISION](https://docs.snowflake.com/en/sql-reference/data-types-numeric#double-double-precision-real) |
| [FLOAT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [FLOAT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#float-float4-float8) |
| [FLOAT8](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [FLOAT8](https://docs.snowflake.com/en/sql-reference/data-types-numeric#float-float4-float8) |
| [REAL](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/double-precision-float/) | [REAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#double-double-precision-real) |

Expand

Show lessSee more

## Exact Numeric Data Type

| Vertica | Snowflake |
| --- | --- |
| [INTEGER](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INTEGER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [INT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [BIGINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [BIGINT](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [INT8](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [INTEGER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#int-integer-bigint-smallint-tinyint-byteint) |
| [SMALLINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [SMALLINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) |
| [TINYINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) | [TINYINT](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/integer/) |
| [DECIMAL](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [DECIMAL](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |
| [NUMERIC](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |
| [NUMBER](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMBER](https://docs.snowflake.com/en/sql-reference/data-types-numeric#number) |
| [MONEY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/numeric-data-types/numeric/) | [NUMERIC](https://docs.snowflake.com/en/sql-reference/data-types-numeric#decimal-dec-numeric) |

Expand

Show lessSee more

## Spatial Data Type

| Vertica | Snowflake |
| --- | --- |
| [GEOMETRY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/spatial-data-types/) | [GEOMETRY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#label-data-types-geometry) |
| [GEOGRAPHY](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/spatial-data-types/) | [GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial#label-data-types-geography) |

Expand

Show lessSee more

## UUID Data Type

| Vertica | Snowflake |
| --- | --- |
| [UUID](https://docs.vertica.com/25.1.x/en/sql-reference/data-types/uuid-data-type/) | [VARCHAR(36)](https://docs.snowflake.com/en/sql-reference/data-types-text#varchar)    *Notes: Snowflake doesn’t have a native UUID data type. Instead, UUIDs are usually stored as either **VARCHAR(36)** (for string format) or **BINARY(16)** (for raw byte format).*  *You can generate RFC 4122-compliant UUIDs in Snowflake using the built-in* [***`UUID_STRING()`***](https://docs.snowflake.com/en/sql-reference/functions/uuid_string) *function.* |

Expand

Show lessSee more
