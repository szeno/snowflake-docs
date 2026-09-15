# Adjust privacy controls

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes techniques the data owner can use to adjust the privacy controls that Snowflake uses to introduce noise into results.
Snowflake recommends trying these options in the order in which they’re presented in this topic.

Snowflake provides parameters to adjust both the privacy budget’s limit on privacy loss and the maximum amount of privacy budget used per
aggregate (collectively known as the *epsilon* in differential privacy literature).

## Step 1: Adjust privacy domains

Before adjusting the privacy budget, you should consider adjusting the privacy domain set on the columns of the privacy-protected table.
Snowflake introduces enough noise to obscure all values in a column, so the wider the range of values, the more noise that must be introduced.
Follow these guidelines:

- If you want to increase the noise, broaden the range to include values that are greater or less than the actual values. Remember, the
  privacy domain defines all *possible* values, not actual values.
- If you want to decrease the noise, narrow the privacy domain to exclude or clamp values outside a useful range. For information about how
  values outside the privacy domain are treated, see [Values outside a privacy domain](/user-guide/diff-privacy/differential-privacy-privacy-domains#label-diff-privacy-privacy-domains-excluded-values).

Note

The analyst can also narrow a privacy domain to decrease noise. For more information, see
[Narrowing a privacy domain to improve results](/user-guide/diff-privacy/differential-privacy-privacy-domains-analyst#label-diff-privacy-analyst-privacy-domains-improve-results)

## Step 2: Adjust MAX\_BUDGET\_PER\_AGGREGATE parameter

If you’ve adjusted the privacy domain, but still need to fine-tune your privacy controls, you can start modifying settings that affect the
privacy budget. Adjusting the `MAX_BUDGET_PER_AGGREGATE` parameter in the body of a privacy policy controls how much of a privacy
budget can be spent on each aggregate in a query (that is, how much privacy loss an aggregate can incur). Adjusting this parameter changes
the amount of noise added to each aggregate query, as well as the number of aggregates that can be executed before the privacy budget
limit is reached.

The parameter sets the level for each aggregate, not each query. As an example, the query `SELECT COUNT(*), AVG(a) ...` has two
aggregates: `COUNT(*)` and `AVG(a)`.

To adjust the maximum privacy loss incurred by each aggregate in a query, use the [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) command to
set a new value for the `MAX_BUDGET_PER_AGGREGATE` parameter. For example:

Copy code

```
ALTER PRIVACY POLICY users_policy SET BODY ->
  PRIVACY_BUDGET(BUDGET_NAME=>'analysts', MAX_BUDGET_PER_AGGREGATE=>0.1);
```

## Step 3: Adjust limit of the privacy budget

If adjusting other privacy controls doesn’t give you the results you’re looking for, you can adjust the privacy budget’s limit on privacy
loss. While the other privacy controls affect the amount of noise in query results, adjusting the budget limit affects how many queries an
analyst can run.

Each time an analyst runs a query with aggregate functions against a privacy-protected table, the analyst’s cumulative privacy loss is
incremented, and the estimated number of remaining aggregates is decremented. When the cumulative privacy loss reaches the privacy budget’s
limit, the analysts cannot run another query. If you want to maximize the usefulness of your data to the analyst, you can base your budget
limit on how many queries you think analysts will run during each budget window.

Note

Remember that cumulative privacy loss is reset to 0 on a fixed schedule, as defined by the [budget window](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-privacy-budget-refresh-definition). When the privacy budget is reset, the analyst can run a fresh set of
queries even if they reached the budget limit during the previous budget window.

The [ESTIMATE\_REMAINING\_DP\_AGGREGATES](/sql-reference/functions/estimate_remaining_dp_aggregates) function helps estimate the number of queries remaining for a privacy
budget. In general, this number is based on the number of aggregates in each query and the value of the `MAX_BUDGET_PER_AGGREGATE`
parameter that you specified in the body of the privacy policy. For an extended example of using the ESTIMATE\_REMAINING\_DP\_AGGREGATES
function to see the effects of queries on the privacy budget, see [Tracking privacy budget spending](/user-guide/diff-privacy/differential-privacy-analyst#label-diff-privacy-analyst-budget).

After you have used the ESTIMATE\_REMAINING\_DP\_AGGREGATES function to get an idea of how much privacy budget is spent on a series of queries,
you can adjust the `BUDGET_LIMIT` parameter in the body of the privacy policy to set a new privacy budget limit. For example:

Copy code

```
ALTER PRIVACY POLICY users_policy SET BODY ->
  PRIVACY_BUDGET(BUDGET_NAME=>'analysts',
  BUDGET_LIMIT=>300,
  MAX_BUDGET_PER_AGGREGATE=>0.1);
```

Important

Note that this command includes the `MAX_BUDGET_PER_AGGREGATE` parameter that was set previously. If you don’t include a parameter
in the ALTER PRIVACY POLICY statement, it resets to its default value.
