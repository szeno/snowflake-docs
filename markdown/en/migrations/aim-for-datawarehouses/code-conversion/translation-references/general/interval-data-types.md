# ANSI SQL - Interval Data Types

## Description

The INTERVAL data type represents a duration or period of time. Many SQL dialects support INTERVAL types in column definitions, literals, and arithmetic expressions. Snowflake supports two families of INTERVAL types: `INTERVAL YEAR TO MONTH` and `INTERVAL DAY TO SECOND`. Learn more from the Snowflake documentation: [INTERVAL Data Type](/sql-reference/data-types-datetime).

Warning

The transformations described on this page require the `--UseIntervalDatatype` flag to be enabled. Without this flag, INTERVAL types are converted to `VARCHAR` as described in each language’s data type reference.

### Snowflake Interval Types

Snowflake supports two interval qualifier families. Mixed qualifiers (combining year-to-month and day-to-second parts) are not allowed.

| Qualifier Family | Supported Qualifiers |
| --- | --- |
| Year-to-Month | `INTERVAL YEAR`, `INTERVAL MONTH`, `INTERVAL YEAR TO MONTH` |
| Day-to-Second | `INTERVAL DAY`, `INTERVAL HOUR`, `INTERVAL MINUTE`, `INTERVAL SECOND`, `INTERVAL DAY TO HOUR`, `INTERVAL DAY TO MINUTE`, `INTERVAL DAY TO SECOND`, `INTERVAL HOUR TO MINUTE`, `INTERVAL HOUR TO SECOND`, `INTERVAL MINUTE TO SECOND` |

Expand

Show lessSee more

### Language Behavior Summary

| Source Language | Qualifier Handling | Notes |
| --- | --- | --- |
| Oracle, Teradata | Source qualifiers preserved | These languages use explicit INTERVAL qualifiers that map directly to Snowflake |
| Redshift, Spark, Databricks, Vertica | Source qualifiers preserved | Same as above |
| BigQuery, PostgreSQL, Greenplum, Netezza | Normalized to `DAY TO SECOND` | Bare `INTERVAL` and mixed qualifiers become `INTERVAL DAY TO SECOND` ([SSC-FDM-0042](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0042)) |
| SQL Server, DB2 | Qualifiers preserved where applicable | Limited native INTERVAL support in source language |

Expand

Show lessSee more

## Interval Column Type Transformations

When the `--UseIntervalDatatype` flag is enabled, INTERVAL columns in `CREATE TABLE` statements are preserved as native Snowflake INTERVAL types.

### Languages with explicit qualifiers

For Oracle, Teradata, Redshift, Spark, Databricks, and Vertica, the source INTERVAL qualifier is preserved directly.

#### Source (Oracle)

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE intervals (
    column1 INTERVAL YEAR TO MONTH,
    column2 INTERVAL DAY TO SECOND,
    column3 INTERVAL YEAR,
    column4 INTERVAL DAY,
    column5 INTERVAL HOUR TO SECOND
);
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE OR REPLACE TABLE intervals (
    column1 INTERVAL YEAR TO MONTH,
    column2 INTERVAL DAY TO SECOND,
    column3 INTERVAL YEAR,
    column4 INTERVAL DAY,
    column5 INTERVAL HOUR TO SECOND
)
;
```

### Languages with unqualified INTERVAL

For BigQuery, PostgreSQL, Greenplum, and Netezza, bare `INTERVAL` is normalized to `INTERVAL DAY TO SECOND` with [SSC-FDM-0042](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0042).

#### Source (BigQuery)

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE intervals (
    COL1 INTERVAL
);
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
CREATE TABLE intervals (
    COL1 INTERVAL DAY TO SECOND /*** SSC-FDM-0042 - INTERVAL QUALIFIER CHANGED TO DAY TO SECOND, SNOWFLAKE DOES NOT SUPPORT MIXING YEAR TO MONTH AND DAY TO SECOND TIME PARTS. ***/
)
;
```

### Without the flag (default behavior)

Without the `--UseIntervalDatatype` flag, INTERVAL columns are converted to `VARCHAR(30)` with [SSC-EWI-0036](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036).

## Interval Literal Transformations

When the flag is enabled, interval literals are normalized to Snowflake-compatible INTERVAL literal syntax. The normalization depends on the source dialect.

### ANSI standard literals

Standard ANSI interval literals with explicit qualifiers are preserved as-is across all languages.

#### Source (Oracle, Teradata, Redshift)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '5-10' YEAR TO MONTH,
  INTERVAL '10 02:30:15.6554' DAY TO SECOND;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '5-10' YEAR TO MONTH,
  INTERVAL '10 02:30:15.6554' DAY TO SECOND;
```

### Verbose syntax normalization

PostgreSQL, Redshift, Vertica, Greenplum, Netezza, and Spark support verbose interval syntax with named units (for example, `WEEK`, `DAY`, `HOUR`). These are normalized to compact Snowflake INTERVAL literals.

#### Source (PostgreSQL)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '5 WEEK 3 DAY 4 HOUR 30 MINUTE 15 SECOND 233 MILLISECOND';
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '38 04:30:15.233' DAY TO SECOND;
```

### ISO 8601 format normalization

PostgreSQL and related languages support ISO 8601 duration format. These are normalized to compact Snowflake literals.

#### Source (PostgreSQL)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL 'P1Y2M3DT4H5M6S',
  INTERVAL 'PT33M16S',
  INTERVAL 'P22-01-05';
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '428 04:05:06' DAY TO SECOND,
  INTERVAL '0 00:33:16' DAY TO SECOND,
  INTERVAL '8065 00:00:00' DAY TO SECOND;
```

### BigQuery expression intervals

BigQuery supports computed interval expressions (`INTERVAL expr unit`). These are transformed to CAST expressions.

#### Source (BigQuery)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL 3 QUARTER,
  INTERVAL 1 + 1 YEAR,
  INTERVAL 3 * 1 DAY,
  INTERVAL 2 * 3 HOUR;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '270 00:00:00' DAY TO SECOND,
  CAST((1 + 1) * 365 AS INTERVAL DAY),
  CAST(3 * 1 AS INTERVAL DAY),
  CAST(2 * 3 AS INTERVAL HOUR);
```

### Overflow normalization

Teradata interval literals with overflowing values are normalized to valid Snowflake intervals.

#### Source (Teradata)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '10 73:80:10' DAY TO SECOND;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '13 02:20:10' DAY TO SECOND;
```

### Negative sign normalization

Teradata places the negative sign outside the literal string. It is normalized inside the string for Snowflake compatibility.

#### Source (Teradata)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL -'10-3' YEAR TO MONTH;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '-10-3' YEAR TO MONTH;
```

### AGO keyword handling

PostgreSQL and related languages support the `AGO` keyword to negate an interval. This is resolved into a negated Snowflake interval literal.

#### Source (PostgreSQL)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '1 DAY -3 MINUTES AGO' DAY TO SECOND,
  INTERVAL '-1 DAY 5 HOURS AGO' DAY TO SECOND;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '-0 23:57:00' DAY TO SECOND,
  INTERVAL '0 19:00:00' DAY TO SECOND;
```

### Spark multi-unit intervals

Spark supports multi-unit interval literals with mixed positive and negative components. These are normalized to compact Snowflake form.

#### Source (Spark)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL -2 HOUR '3' MINUTE 15 SECOND;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '-01:56:45' HOUR TO SECOND;
```

### Vertica named-unit intervals

Vertica supports named-unit interval syntax that is normalized to compact Snowflake form.

#### Source (Vertica)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '4 years 1 month 4 days 14 hours';
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT INTERVAL '1494 14:00:00' DAY TO SECOND;
```

## Interval Arithmetic

When the flag is enabled, datetime subtraction expressions that produce interval results are transformed to use Snowflake’s native interval types.

### Year-to-Month family

Datetime subtraction with `YEAR`, `MONTH`, or `YEAR TO MONTH` qualifiers uses `TIMESTAMPDIFF` and `CAST` to produce a native interval result.

#### Source (Oracle, Teradata)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT (TIMESTAMP '2025-10-12 10:30:15' - TIMESTAMP '2022-01-07 11:00:15') YEAR TO MONTH FROM dual;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  CAST(CAST(TIMESTAMPDIFF(MONTH, TIMESTAMP '2022-01-07 11:00:15', TIMESTAMP '2025-10-12 10:30:15') AS INTERVAL MONTH) AS INTERVAL YEAR TO MONTH) FROM dual;
```

### Day-to-Second family

Datetime subtraction with `DAY`, `HOUR`, `MINUTE`, `SECOND`, or compound qualifiers uses direct timestamp subtraction, producing a native interval result.

#### Source (Oracle, Teradata)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT (TIMESTAMP '2024-12-31 23:59:59' - TIMESTAMP '2024-01-01 00:00:00') DAY TO SECOND FROM dual;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  TIMESTAMP '2024-12-31 23:59:59' - TIMESTAMP '2024-01-01 00:00:00' INTERVAL DAY TO SECOND FROM dual;
```

### DATE operand handling

When DATE operands are used in interval subtraction, they are wrapped with `TIMESTAMP_NTZ_FROM_PARTS` to produce a timestamp suitable for interval subtraction.

#### Source (Oracle)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT (DATE '2024-12-31' - DATE '2024-01-01') DAY TO SECOND FROM dual;
```

#### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  TIMESTAMP_NTZ_FROM_PARTS(DATE '2024-12-31', '00:00:00') - TIMESTAMP_NTZ_FROM_PARTS(DATE '2024-01-01', '00:00:00') INTERVAL DAY TO SECOND FROM dual;
```

## CAST to Interval

CAST expressions targeting interval types are preserved when the flag is enabled.

### Source (Teradata)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  CAST('10-5' AS INTERVAL YEAR TO MONTH),
  CAST(INTERVAL '5 03:30' DAY TO MINUTE AS INTERVAL HOUR(4) TO SECOND);
```

### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  CAST('10-5' AS INTERVAL YEAR TO MONTH),
  CAST(INTERVAL '5 03:30' DAY TO MINUTE AS INTERVAL HOUR(4) TO SECOND);
```

## Interval Arithmetic with Existing Columns

Standard interval arithmetic with columns and literals (addition, subtraction, multiplication, division) is preserved as-is.

### Source (Oracle, Teradata, Redshift)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  date_column + interval_column,
  date_column - interval_column,
  interval_column * 2,
  interval_column / 3,
  DATE '2024-01-01' + INTERVAL '10' DAY,
  TIMESTAMP '2025-01-01 10:30:00' - INTERVAL '5-3' YEAR TO MONTH
FROM datesTable;
```

### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  date_column + interval_column,
  date_column - interval_column,
  interval_column * 2,
  interval_column / 3,
  DATE '2024-01-01' + INTERVAL '10' DAY,
  TIMESTAMP '2025-01-01 10:30:00' - INTERVAL '5-3' YEAR TO MONTH
FROM
  datesTable;
```

## Oracle Precision Zero Handling

Oracle allows `INTERVAL` types with precision `(0)`, which has no equivalent in Snowflake. The zero precision qualifier is removed.

### Source (Oracle)

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '0-5' YEAR(0) TO MONTH,
  INTERVAL '0' DAY(0)
FROM DUAL;
```

### Snowflake

Copy code

```
-- Additional Params: --UseIntervalDatatype
SELECT
  INTERVAL '0-5' YEAR TO MONTH,
  INTERVAL '0' DAY
FROM DUAL;
```

## Known Limitations

The following scenarios produce warnings when the `--UseIntervalDatatype` flag is enabled:

- **Dynamic Tables** ([SSC-EWI-0118](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0118)): Snowflake does not support INTERVAL columns in Dynamic Tables. The Dynamic Table is still generated with a warning.
- **UDFs and Snowflake Scripting** ([SSC-EWI-0117](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0117)): Snowflake does not support the INTERVAL data type in UDF/procedure parameters, return types, or variable declarations.
- **Semi-structured types** ([SSC-EWI-0116](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0116)): Snowflake does not support INTERVAL values inside VARIANT, ARRAY, MAP, or STRUCT columns.
- **Qualifier normalization** ([SSC-FDM-0042](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0042)): For languages with unqualified or mixed INTERVAL types, the qualifier is changed to `DAY TO SECOND`.

## Related EWIs

1. [SSC-EWI-0036](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0036): Data type converted to other data type (INTERVAL to VARCHAR when flag is off).
2. [SSC-EWI-0107](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0107): Interval literal not supported in current scenario.
3. [SSC-EWI-0116](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0116): Snowflake does not support interval values inside semi-structured type columns.
4. [SSC-EWI-0117](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0117): Snowflake does not support interval data type in UDFs or Snowflake Scripting.
5. [SSC-EWI-0118](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0118): Snowflake does not support interval columns in Dynamic Tables.
6. [SSC-EWI-0119](../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0119): Interval type column was converted to VARCHAR.
7. [SSC-FDM-0042](../../issues-and-troubleshooting/functional-difference/generalFDM#ssc-fdm-0042): Interval qualifier changed to DAY TO SECOND.
