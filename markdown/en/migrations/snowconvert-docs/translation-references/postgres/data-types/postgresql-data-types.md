# PostgreSQL - Data types

Current Data types conversion for PostgreSQL to Snowflake.

## Applies to

- PostgreSQL
- Greenplum
- Netezza

Snowflake supports most basic [SQL data types](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types) (with some restrictions) for use in columns, local variables, expressions, parameters, and any other appropriate/suitable locations.

## Numeric Data Types

| PostgreSQL | Snowflake |
| --- | --- |
| INT | INT |
| INT2 | SMALLINT |
| INT4 | INTEGER |
| INT8 | INTEGER |
| INTEGER | INTEGER |
| BIGINT | BIGINT |
| DECIMAL | DECIMAL |
| DOUBLE PRECISION | DOUBLE PRECISION |
| NUMERIC​ | NUMERIC |
| SMALLINT | SMALLINT |
| FLOAT | FLOAT |
| FLOAT4 | FLOAT4 |
| FLOAT8 | FLOAT8 |
| REAL | REAL​ |
| BIGSERIAL/SERIAL8 | INTEGER  *Note: Snowflake supports defining columns as IDENTITY, which automatically generates sequential values. This is the more concise and often preferred approach in Snowflake.* |

Expand

Show lessSee more

## Character Types

| PostgreSQL | Snowflake |
| --- | --- |
| VARCHAR | VARCHAR  *Note: VARCHAR holds Unicode UTF-8 characters. If no length is specified, the default is the maximum allowed length (16,777,216).* |
| CHAR | CHAR |
| CHARACTER | CHARACTER  *Note:* Snowflake’s CHARACTER is an alias for VARCHAR. |
| NCHAR | NCHAR |
| BPCHAR | VARCHAR  *Note: BPCHAR data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-FDM-PG0002*](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0002)*.* |
| CHARACTER VARYING | CHARACTER VARYING |
| NATIONAL CHARACTER | NCHAR |
| NATIONAL CHARACTER VARYING | NCHAR VARYING |
| TEXT | TEXT |
| [NAME](https://www.postgresql.org/docs/current/datatype-character.html) (Special character type) | VARCHAR |

Expand

Show lessSee more

## Boolean Types

| PostgreSQL | Snowflake |
| --- | --- |
| BOOL/BOOLEAN | BOOLEAN |

Expand

Show lessSee more

## Binary Types

| PostgreSQL | Snowflake |
| --- | --- |
| BYTEA | BINARY |

Expand

Show lessSee more

## Bit String Types

| PostgreSQL | Snowflake |
| --- | --- |
| BIT | CHARACTER |
| BIT VARYING | CHARACTER VARYING |
| VARBIT | CHARACTER VARYING |

Expand

Show lessSee more

## Date & Time Data

| PostgreSQL | Snowflake |
| --- | --- |
| DATE | DATE |
| TIME | TIME |
| TIME WITH TIME ZONE | TIME  *Note: Time zone not supported for time data type. For more information, please refer to* [*SSC-FDM-0005*](../../../issues-and-troubleshooting/functional-difference/generalFDM.md#ssc-fdm-0005)*.* |
| TIME WITHOUT TIME ZONE | TIME |
| TIMESTAMP | TIMESTAMP |
| TIMESTAMPTZ | TIMESTAMP\_TZ |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP\_TZ |
| TIMESTAMP WITHOUT TIME ZONE | TIMESTAMP\_NTZ |
| INTERVAL YEAR TO MONTH | VARCHAR  *Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*. With the `--UseIntervalDatatype` preview flag, maps to `INTERVAL DAY TO SECOND`. See [Interval Data Types](../../general/interval-data-types).* |
| INTERVAL DAY TO SECOND | VARCHAR  *Note: Data type is **not supported** in Snowflake. VARCHAR is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*. With the `--UseIntervalDatatype` preview flag, maps to `INTERVAL DAY TO SECOND`. See [Interval Data Types](../../general/interval-data-types).* |

Expand

Show lessSee more

## Pseudo Types

| PostgreSQL | Snowflake |
| --- | --- |
| UNKNOWN | TEXT  *Note: Data type is **not supported** in Snowflake. TEXT is used instead. For more information please refer to* [*SSC-EWI-0036*](../../../issues-and-troubleshooting/conversion-issues/generalEWI.md#ssc-ewi-0036)*.* |

Expand

Show lessSee more

## Array Types

| PostgreSQL | Snowflake |
| --- | --- |
| type [] | ARRAY  *Note: Strongly typed array transformed to ARRAY without type checking. For more information please refer to* [*SSC-FDM-PG0016*](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM.md#ssc-fdm-pg0016)*.* |

Expand

Show lessSee more

## Related EWIs

1. [SSC-FDM-PG0002](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0002): Bpchar converted to varchar.
2. [SSC-FDM-PG0003](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0003): Bytea Converted To Binary
3. [SSC-FDM-PG0014](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0014): Unknown Pseudotype transformed to Text Type
4. [SSC-FDM-0005](../../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0005): TIME ZONE not supported for time data type.
5. [SSC-EWI-0036](../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to another data type.
6. [SSC-EWI-PG0016](../../../issues-and-troubleshooting/conversion-issues/postgresqlEWI#ssc-ewi-pg0016): Bit String Type converted to Varchar Type.
7. [SSC-FDM-PG0016](../../../issues-and-troubleshooting/functional-difference/postgresqlFDM#ssc-fdm-pg0016): *Strongly typed array transformed to ARRAY without type checking*.
