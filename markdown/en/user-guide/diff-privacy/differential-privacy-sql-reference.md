# Differential privacy SQL reference

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides the following information:

- A reference for the SQL functions that are unique to differential privacy.
- A list of the Snowflake data types, operators, query syntax, and functions that are supported by differential privacy.

## Differential privacy functions

The following functions are unique to differential privacy.

| Function | Description |
| --- | --- |
| [DP\_INTERVAL\_LOW](/sql-reference/functions/dp_interval_low) | Returns the lower bound of the noise interval. |
| [DP\_INTERVAL\_HIGH](/sql-reference/functions/dp_interval_high) | Returns the upper bound of the noise interval. |

Expand

Show lessSee more

## Data types

The following [data types](/sql-reference-data-types) are supported.

| Data type | Notes |
| --- | --- |
| BOOLEAN |  |
| CHAR, CHARACTER |  |
| DATE |  |
| DATETIME |  |
| DECIMAL, NUMERIC |  |
| DOUBLE, DOUBLE PRECISION, REAL |  |
| FLOAT, FLOAT4, FLOAT8 |  |
| INT, INTEGER , BIGINT, SMALLINT, TINYINT, BYTEINT |  |
| NUMBER |  |
| STRING |  |
| TEXT |  |
| TIME |  |
| TIMESTAMP, TIMESTAMP\_NTZ | Time data types with time zones are not supported. Use TIMESTAMP or TIMESTAMP\_NTZ. |
| VARCHAR |  |

Expand

Show lessSee more

## Query syntax

The following elements of the Snowflake [query syntax](/sql-reference/constructs) are supported.

| Syntax | Notes |
| --- | --- |
| SELECT |  |
| SELECT ALL |  |
| FROM |  |
| INNER JOIN ON | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| INNER JOIN USING | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| LEFT OUTER JOIN ON | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| LEFT OUTER JOIN USING | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| RIGHT OUTER JOIN ON | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| RIGHT OUTER JOIN USING | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| FULL OUTER JOIN ON | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| FULL OUTER JOIN USING | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| NATURAL JOIN | See [Supported joins](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-joins-supported). |
| WHERE |  |
| GROUP BY | Aliases are not supported in the GROUP BY clause. For example, `GROUP BY col_a AS column_a` is not supported. |

Expand

Show lessSee more

Limitations on query syntax
:   Quoted identifiers (for example, column, table, schema and database names) are not supported.

## Operators

### Arithmetic operators

The following [arithmetic operators](/sql-reference/operators-arithmetic) are supported.

| Operator | Notes |
| --- | --- |
| `-` (unary) |  |
| `-` |  |
| `+` (unary) | Does not work with strings. |
| `+` |  |
| `*` |  |
| `/` |  |
| `%` |  |

Expand

Show lessSee more

### Comparison operators

The following [comparison operators](/sql-reference/operators-comparison) are supported.

| Operator | Notes |
| --- | --- |
| `=` |  |
| `!=` |  |
| `<` |  |
| `>` |  |
| `<=` |  |
| `>=` |  |

Expand

Show lessSee more

### Logical operators

The following [logical operators](/sql-reference/operators-logical) are supported.

| Operator | Notes |
| --- | --- |
| AND |  |
| NOT |  |
| OR |  |

Expand

Show lessSee more

### Set operators

The following [set operators](/sql-reference/operators-query) are supported.

| Operator | Notes |
| --- | --- |
| UNION [ ALL ] |  |

Expand

Show lessSee more

### Subquery operators

[Subquery operators](/sql-reference/operators-subquery) are not supported.

## Functions

### Aggregate functions

The following [aggregate functions](/sql-reference/functions-aggregation) are supported.

| Function | Notes |
| --- | --- |
| ANY\_VALUE | Supported only as an aggregate for a subquery with a GROUP BY clause. |
| COUNT |  |
| COUNT DISTINCT |  |

Expand

Show lessSee more

### Bitwise expression functions

[Bitwise expression functions](/sql-reference/expressions-byte-bit) are not supported.

### Conditional expression functions

The following [conditional expression functions](/sql-reference/expressions-conditional) are supported.

| Function | Notes |
| --- | --- |
| [ NOT ] IN |  |
| CASE |  |
| COALESCE |  |
| DECODE |  |
| EQUAL\_NULL |  |
| GREATEST |  |
| IFF |  |
| IS [NOT] NULL |  |
| LEAST |  |

Expand

Show lessSee more

### Context functions

[Context functions](/sql-reference/functions-context) are not supported.

### Conversion functions

The following [conversion functions](/sql-reference/functions-conversion) are supported.

| Function | Notes |
| --- | --- |
| CAST, `::` | Columns must be explicitly non-null to be casted. To do this, filter out nulls before casting.  Casting other data types to STRING is not supported. |
| TO\_BOOLEAN |  |
| TO\_CHAR , TO\_VARCHAR |  |
| TO\_DECIMAL , TO\_NUMBER , TO\_NUMERIC |  |
| TO\_DOUBLE |  |
| TRY\_CAST |  |
| TRY\_TO\_BOOLEAN |  |
| TRY\_TO\_DECIMAL, TRY\_TO\_NUMBER, TRY\_TO\_NUMERIC |  |
| TRY\_TO\_DOUBLE |  |

Expand

Show lessSee more

### Data generation functions

[Data generation functions](/sql-reference/functions-data-generation) are not supported.

### Data metric functions

[Data metric functions](/sql-reference/functions-data-metric) are not supported. User-defined DMFs are also not supported.

### Date & time functions

The following [date & time functions](/sql-reference/functions-date-time) are supported.

| Function | Notes |
| --- | --- |
| DATE\_PART | The following date and time parts are not supported: `dayofweek`, `week`, `yearofweek`, `nanosecond`, `epoch_*`, and `timezone_*`. |
| DAYNAME |  |
| EXTRACT | The following date and time parts are not supported: `dayofweek`, `week`, `yearofweek`, `nanosecond`, `epoch_*`, and `timezone_*`. |
| HOUR |  |
| LAST\_DAY |  |
| MINUTE |  |
| SECOND |  |
| TRUNC |  |
| YEAR\* / DAY\* / WEEK\* / MONTH / QUARTER |  |

Expand

Show lessSee more

### Encryption functions

[Encryption functions](/sql-reference/functions-encryption) are not supported.

### File functions

[File functions](/sql-reference/functions-file) are not supported.

### Geospatial functions

[Geospatial functions](/sql-reference/functions-geospatial) are not supported.

### Hash functions

[Hash functions](/sql-reference/functions-hash-scalar) are not supported.

### Metadata functions

[Metadata functions](/sql-reference/functions-metadata) are not supported.

### Numeric functions

The following [numeric functions](/sql-reference/functions-numeric) are supported.

| Function | Notes |
| --- | --- |
| ABS |  |
| CEIL |  |
| FLOOR |  |
| MOD |  |
| SIGN |  |

Expand

Show lessSee more

### Regular expression functions

[Regular expression functions](/sql-reference/functions-regexp) are not supported.

### Semi-structured and structured data functions

[Semi-structured and structured data functions](/sql-reference/functions-semistructured) are not supported.

### String and binary functions

The following [string & binary functions](/sql-reference/functions-string) are supported.

| Function | Notes |
| --- | --- |
| CONTAINS |  |
| LENGTH , LEN |  |
| LOWER |  |
| POSITION |  |
| UPPER |  |

Expand

Show lessSee more

### System functions

[System functions](/sql-reference/functions-system) are not supported.

### Table functions

[Table functions](/sql-reference/functions-table) are not supported.
