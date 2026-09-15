# Informatica PowerCenter - Data types

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

Note

This reference applies to both output formats, **dbt** and **Snowflake Scripting**.

This page describes how Informatica PowerCenter data types are mapped to Snowflake data types. The mapping is the same regardless of the output format (dbt or Snowflake Scripting), because both produce the same Snowflake types.

## Type mapping

The following type mappings are used:

| Informatica PowerCenter | Snowflake | Notes |
| --- | --- | --- |
| string | [VARCHAR](/sql-reference/data-types-text#varchar) |  |
| nstring | [VARCHAR](/sql-reference/data-types-text#varchar) | National strings map to `VARCHAR`, which stores Unicode in Snowflake. |
| text | [TEXT](/sql-reference/data-types-text#varchar) | `TEXT` is a synonym for `VARCHAR`. |
| integer | [NUMBER](/sql-reference/data-types-numeric#number) |  |
| small integer | [NUMBER](/sql-reference/data-types-numeric#number) |  |
| bigint | [NUMBER](/sql-reference/data-types-numeric#number) | Snowflake `NUMBER` covers the full Informatica integer range. |
| decimal | [NUMBER](/sql-reference/data-types-numeric#number) |  |
| double | [FLOAT](/sql-reference/data-types-numeric#float-float4-float8) |  |
| real | [FLOAT](/sql-reference/data-types-numeric#float-float4-float8) |  |
| date | [DATE](/sql-reference/data-types-datetime#date) |  |
| date/time | [TIMESTAMP](/sql-reference/data-types-datetime#timestamp) |  |
| datetime | [TIMESTAMP](/sql-reference/data-types-datetime#timestamp) |  |
| timestamp | [TIMESTAMP](/sql-reference/data-types-datetime#timestamp) |  |
| time | [TIME](/sql-reference/data-types-datetime#time) |  |
| binary | [BINARY](/sql-reference/data-types-text#binary) |  |
| varbinary | [BINARY](/sql-reference/data-types-text#binary) |  |

Expand

Show lessSee more

## Default type

When a source type is not in the table above, it is mapped to `VARCHAR`. Review any such columns after migration to confirm `VARCHAR` is the correct type.

## Precision and scale

For Informatica variable and parameter definitions, precision and scale are not carried over to the generated Snowflake type. For example, an Informatica `decimal` variable maps to `NUMBER` with Snowflake’s default precision and scale rather than to `NUMBER(p, s)`. Set an explicit precision and scale in Snowflake where your data requires it.

Note

Snowflake `NUMBER` stores both integers and fixed-point decimals, so the Informatica integer types and `decimal` all map to `NUMBER`. The default is `NUMBER(38, 0)`. See the Snowflake [numeric data types](/sql-reference/data-types-numeric) reference for the full range.
