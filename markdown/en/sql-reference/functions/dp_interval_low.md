Categories:
:   [Differential privacy functions](/sql-reference/functions-differential-privacy)

# DP\_INTERVAL\_LOW

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the lower bound of the [noise interval](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-understand-results), which is used by differential privacy to help
analysts determine how much noise has been introduced into query results.

By default, there is a 95% confidence level that the actual value is equal to or larger than the lower bound.

See also:
:   [DP\_INTERVAL\_HIGH](/sql-reference/functions/dp_interval_high)

## Syntax

Copy code

```
DP_INTERVAL_LOW( <aggregated_column> )
```

## Arguments

`aggregated_column`
:   Alias of a column that has been aggregated by the query.

## Returns

Returns an integer that is the lower bound of the noise interval.

If the table is not protected by differential privacy, returns NULL.

## Examples

To return the lower bound of the noise interval for the aggregation of the column `num_claims`:

Copy code

```
SELECT SUM(num_claims) AS sum_claims,
  DP_INTERVAL_LOW(sum_claims)
  FROM t1;
```
