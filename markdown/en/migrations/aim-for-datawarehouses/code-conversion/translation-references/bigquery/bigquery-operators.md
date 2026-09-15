# BigQuery - Operators

## IS operators

IS operators return `TRUE` or `FALSE` for the condition they are testing. They never return `NULL`, even for `NULL` inputs. ([BigQuery SQL Language Reference IS operators](https://cloud.google.com/bigquery/docs/reference/standard-sql/operators?hl=en#is_operators))

| BigQuery | Snowflake |
| --- | --- |
| `X IS TRUE` | `NVL(X, FALSE)` |
| `X IS NOT TRUE` | `NVL(NOT X, TRUE)` |
| `X IS FALSE` | `NVL(NOT X, FALSE)` |
| `X IS NOT FALSE` | `NVL(X, TRUE)` |
| `X IS NULL` | `X IS NULL` |
| `X IS NOT NULL` | `X IS NOT NULL` |
| `X IS UNKNOWN` | `X IS NULL` |
| `X IS NOT UNKNOWN` | `X IS NOT NULL` |

Expand

Show lessSee more

## UNNEST operator

The UNNEST operator takes an array and returns a table with one row for each element in the array. ([BigQuery SQL Language Reference UNNEST operator](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#unnest_operator)).

This operator will be emulated using the [FLATTEN](/sql-reference/functions/flatten) function, the `VALUE` and `INDEX` columns returned by the function will be renamed accordingly to match the UNNEST operator aliases

| BigQuery | Snowflake |
| --- | --- |
| `UNNEST(arrayExpr)` | `FLATTEN(INPUT => arrayExpr) AS F0_(SEQ, KEY, PATH, INDEX, F0_, THIS)` |
| `UNNEST(arrayExpr) AS alias` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, INDEX, alias, THIS)` |
| `UNNEST(arrayExpr) AS alias WITH OFFSET` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, OFFSET, alias, THIS)` |
| `UNNEST(arrayExpr) AS alias WITH OFFSET AS offsetAlias` | `FLATTEN(INPUT => arrayExpr) AS alias(SEQ, KEY, PATH, offsetAlias, alias, THIS)` |

Expand

Show lessSee more

### SELECT \* with UNNEST

When the UNNEST operator is used inside a SELECT \* statement the `EXCLUDE` keyword will be used to remove the unnecessary FLATTEN columns.

Input:

Copy code

```
SELECT * FROM UNNEST ([10,20,30]) AS numbers WITH OFFSET position;
```

Generated code:

Copy code

```
 SELECT
* EXCLUDE(SEQ, KEY, PATH, THIS)
FROM
TABLE(FLATTEN(INPUT => [10,20,30])) AS numbers (
SEQ,
KEY,
PATH,
position,
numbers,
THIS
);
```

## PIVOT operator

The PIVOT operator rotates rows into columns by aggregating values for each distinct pivot value. ([BigQuery SQL Language Reference PIVOT operator](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#pivot_operator)).

Snowflake supports the same syntax directly, including the optional `IN`-list aliasing form (`'Q1' AS first`), per the [Snowflake PIVOT documentation](https://docs.snowflake.com/en/sql-reference/constructs/pivot). Single-aggregate PIVOT operators are passed through unchanged.

Because the two engines can name the resulting columns differently, [`SSC-FDM-BQ0013`](../../issues-and-troubleshooting/functional-difference/bigqueryFDM#ssc-fdm-bq0013) is emitted when the column names may diverge — that is, when at least one `IN`-list value is unaliased, or the aggregate function is aliased. The marker is suppressed when every `IN`-list value is aliased and the aggregate has no alias, since both engines then produce identical column names.

Input:

Copy code

```
SELECT * FROM sales PIVOT(SUM(amount) FOR quarter IN ('Q1', 'Q2', 'Q3', 'Q4'));
```

Generated code:

Copy code

```
SELECT
  *
FROM
  sales
  --** SSC-FDM-BQ0013 - BIGQUERY PIVOT OUTPUT COLUMN NAMES MAY DIFFER FROM SNOWFLAKE; DOWNSTREAM QUERIES THAT REFERENCE PIVOT OUTPUT COLUMNS MAY NEED UPDATES **
  PIVOT(
    SUM(amount)
    FOR quarter
    IN ('Q1', 'Q2', 'Q3', 'Q4')
  );
```

**Note:** Multi-aggregate PIVOT (`PIVOT(agg1, agg2 FOR ...)`) is not supported in Snowflake. The multi-aggregate form is currently passed through unchanged; a dedicated EWI is planned as follow-up work.
