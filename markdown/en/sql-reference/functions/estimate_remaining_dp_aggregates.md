Categories:
:   [Differential privacy functions](/sql-reference/functions-differential-privacy) , [Table functions](/sql-reference/functions-table)

# ESTIMATE\_REMAINING\_DP\_AGGREGATES

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the estimated number of aggregation functions that can be run before the limit of a privacy budget is reached. The number of
remaining aggregates is *estimated*. The actual number of aggregate functions allowed before reaching the privacy budget limit might vary in
practice, depending on various factors.

This function is useful for both implementing differential privacy and querying privacy-protected tables:

- Analysts can use this function to estimate roughly how much privacy budget they have left in a budget window.
- Privacy policy owners can use this function to
  [fine-tune their privacy budget settings](/user-guide/diff-privacy/differential-privacy-admin-adjust#label-diff-privacy-admin-adjust-privacy-budget) so the limit of a privacy budget is
  appropriate for every user.

The privacy budget is calculated per aggregate function, not per query. So the query
`SELECT SUM(age), COUNT(age) FROM T GROUP BY STATE;` incurs twice as much privacy loss as the query `SELECT SUM(age) FROM T;` (that is,
the query ‘costs’ twice as much). In general, all aggregate functions cost the same: the value of the `MAX_BUDGET_PER_AGGREGATE`
parameter in the body of the privacy policy. Note that a GROUP BY clause is *not* considered an aggregation function, and does not incur
privacy loss.

The function also returns the budget spent (that is, the current cumulative privacy loss), but Snowflake recommends using the function to
focus on the estimated remaining budget rather than the budget spent. The budget spent is not a linear function (number of aggregations \*
cost per aggregation), but rather a *sub-linear* function. This means that the total cost of additional aggregations decreases with use
during a budget window. This is why the estimated number of remaining aggregates is larger than the formula (remaining budget of privacy
loss) / (privacy loss per function).

## Syntax

Copy code

```
SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('<table_name>')
```

## Arguments

`table_name`
:   The name of the table protected by a differential privacy policy. The function returns privacy budget data based on the queries that you
    have run against this table since the last budget refresh.

## Output

The function returns a table with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `NUMBER_OF_REMAINING_DP_AGGREGATES` | INT | The estimated number of remaining aggregate functions that an analyst can call before exceeding the privacy budget limit. |
| `BUDGET_LIMIT` | DECIMAL | The current limit of the privacy budget protecting the specified table, as defined in the privacy policy.  To adjust the privacy budget limit, see [Set privacy settings for a privacy budget](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-adjust-budget). |
| `BUDGET_WINDOW` | STRING | The refresh period of the privacy budget, that is, how often the cumulative privacy loss is reset to 0. Defined in the privacy policy protecting the table.  To adjust the budget window, see [Modify the refresh period](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-refresh-period). |
| `BUDGET_SPENT` | DECIMAL | The cumulative privacy loss incurred by the current user using the current role during the current budget window. |

Expand

Show lessSee more

## Access control privileges

You need the following privileges to run this function:

- SELECT privilege on the specified table.
- USAGE privilege on the database and schema of the specified table.

## Usage notes

- Estimates are based on the queries run by the user who is executing the function. A query is associated with a privacy budget based on
  several conditions, so be sure the environment you use to execute this function is exactly the same as the one used to execute the queries
  (for example, user, role, and account).
- If you’re running a query that uses multiple tables, you should run ESTIMATE\_REMAINING\_DP\_AGGREGATES once per table, then use the lowest
  `NUMBER_OF_REMAINING_DP_AGGREGATES` value as the estimated usage cap.
- Empty output indicates that the table is not protected by differential privacy (that is, does not have a privacy policy assigned to it).

## Examples

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.DATA_PRIVACY.ESTIMATE_REMAINING_DP_AGGREGATES('my_table'));
```

```
+-----------------------------------+--------------+---------------+--------------+
| NUMBER_OF_REMAINING_DP_AGGREGATES | BUDGET_LIMIT | BUDGET_WINDOW | BUDGET_SPENT |
|-----------------------------------+--------------+---------------+--------------|
|                 994               |     233      |     WEEKLY    |     1.8      |
+-----------------------------------+--------------+---------------+--------------+
```

For an extended example that shows how to use the ESTIMATE\_REMAINING\_DP\_AGGREGATES function to see the effects of queries, see
[Tracking privacy budget spending](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-analyst-budget).
