# Working with privacy budgets

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes how to manage privacy budgets in a privacy policy. For an
introduction to privacy budgets and how they help prevent queries from revealing sensitive information about an entity, see
[Limiting privacy loss](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-loss-budgets).

A privacy budget is created automatically when you define a privacy budget name in the body of the privacy policy. You don’t create a
privacy budget independent of a [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies).

When a query would cause the cumulative privacy loss to exceed the privacy budget limit, the query fails until the privacy budget
refreshes.

To manage a privacy budget, you need OWNERSHIP privilege on the privacy policy that specifies the privacy budget.

## View a privacy budget

Each privacy budget is namespaced to a privacy policy. There can be multiple privacy budgets with the same name, but each is unique to a
privacy policy. Within a privacy policy, a privacy budget is further namespaced to the consumer account incurring
[privacy loss](/user-guide/diff-privacy/differential-privacy-overview#label-diff-privacy-loss-budgets). As a result, multiple accounts can have a privacy budget with the same name and
limit on privacy loss, but Snowflake calculates the cumulative privacy loss for each account separately.

Privacy budget names must be unique within a privacy policy. Multiple accounts can have a privacy budget with the same name
and Snowflake tallies the cumulative privacy loss for each account separately.

View a privacy budget to see its limit on privacy loss as well as the cumulative privacy loss incurred by users associated
with the budget. You can use this information to determine whether the cumulative privacy loss is approaching the privacy budget’s limit.
[See what properties exist in a privacy budget object.](/sql-reference/sql/create-privacy-policy#label-diff-privacy-creation-parameters)

Note

The cumulative privacy loss associated with a privacy budget does not include privacy loss incurred in accounts outside
of the data provider’s account.

You have the following two options for viewing privacy budgets. For both options, a privacy budget appears only if analysts associated with
the privacy budget have incurred privacy loss or if an administrator has [reset the privacy budget](#label-diff-privacy-admin-privacy-budget-reset).

- **To query all privacy budgets in the account,** use the PRIVACY\_BUDGETS view in the Account Usage schema.
  The [PRIVACY\_BUDGETS](/sql-reference/account-usage/privacy_budgets) view in the ACCOUNT USAGE schema contains all privacy budgets
  in the account. You can use it to view privacy budgets associated with all of the privacy policies that you own, and can filter results to
  focus on specific privacy budgets by name. For example, to focus on a specific privacy budget associated with the `patients_policy`
  privacy policy, you might execute the following query:

  Copy code

  ```
  SELECT * FROM snowflake.account_usage.privacy_budgets
    WHERE policy_name='patients_policy' AND budget_name='analyst_budget';
  ```
- **To view the privacy budgets associated with a particular privacy policy,** use the CUMULATIVE\_PRIVACY\_LOSSES table function.
  You can use the [CUMULATIVE\_PRIVACY\_LOSSES](/sql-reference/functions/cumulative_privacy_losses) table function to retrieve privacy budgets associated with a
  particular privacy policy. Unlike the PRIVACY\_BUDGETS view in the ACCOUNT USAGE schema, this function does not have a fixed amount of
  latency and will return the real-time values for the cumulative privacy losses. When calling the function, the name of the privacy policy
  must be fully qualified.

  For example, to view the privacy budgets that are specified in the `my_policy_privacy` policy, execute the following:

  Copy code

  ```
  SELECT *
    FROM TABLE(SNOWFLAKE.DATA_PRIVACY.CUMULATIVE_PRIVACY_LOSSES(
   'my_policy_db.my_policy_schema.my_policy_privacy'));
  ```

## Set privacy settings for a privacy budget

Snowflake lets you adjust the privacy budget’s limit on privacy loss and the maximum amount of privacy budget spent per
aggregate (collectively known as the *epsilon* in differential privacy). You set these controls by specifying the following parameters in
the body of the privacy policy:

- `BUDGET_LIMIT` — Sets the privacy budget’s limit on cumulative privacy loss.
- `MAX_BUDGET_PER_AGGREGATE` – Sets the maximum amount of the privacy budget spend per aggregate (that is, the maximum privacy loss
  incurred by each aggregate function in a query).

For example, to use the [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) command to adjust the privacy controls of an existing privacy budget,
you might execute:

Copy code

```
ALTER PRIVACY POLICY users_policy SET BODY ->
  PRIVACY_BUDGET(BUDGET_NAME=>'analysts',
  BUDGET_LIMIT=>300,
  MAX_BUDGET_PER_AGGREGATE=>0.1);
```

You can also define these controls when executing the [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) command to create the privacy policy.

Caution

When changing the `BUDGET_LIMIT`, `MAX_BUDGET_PER_AGGREGATE`, or `BUDGET_WINDOW` parameter, any
parameter not specified in your ALTER PRIVACY POLICY command reverts back to its default value. So in the previous example,
the `BUDGET_WINDOW` parameter, which determines how often Snowflake resets the privacy budget, will revert to its default value.

For more information about setting privacy controls, see [Adjust privacy controls](/user-guide/diff-privacy/differential-privacy-admin-adjust).

## Privacy budget refresh

### About the refresh period

Snowflake periodically resets the cumulative privacy loss of a privacy budget to 0 to let analysts run a new set of queries. This refresh
period is known as the budget window. This automatic refresh lets analysts access new data as it is added to a table. Theoretically,
the analyst hasn’t learned any information about this new data, so it’s appropriate to let them run more queries.

The default budget window is weekly.

### Modify the refresh period

To modify the privacy budget refresh period, update the `budget_window` value of the privacy policy’s `privacy_budget`. For example:

Copy code

```
ALTER PRIVACY POLICY users_policy SET BODY ->
  PRIVACY_BUDGET(BUDGET_NAME=>'analysts', BUDGET_WINDOW=>'daily');
```

Caution

When changing the `BUDGET_LIMIT`, `MAX_BUDGET_PER_AGGREGATE`, or `BUDGET_WINDOW` parameter, any parameter not specified
in your ALTER PRIVACY POLICY command reverts back to its default value. So in the previous example, `BUDGET_LIMIT` and
`MAX_BUDGET_PER_AGGREGATE` will revert to default values.

## Reset cumulative privacy loss

As analysts execute queries on data protected by a policy, Snowflake tallies the cumulative privacy loss of those queries. You can call
the [RESET\_PRIVACY\_BUDGET](/sql-reference/stored-procedures/reset_privacy_budget) stored procedure to reset the cumulative privacy loss to 0, letting the
analysts execute additional queries.

The RESET\_PRIVACY\_BUDGET stored procedure is intended to reset the budget when analysts inadvertently incur privacy loss and want to
start over. Remember that the privacy loss is automatically set to 0 when the [privacy budget is refreshed](#label-diff-privacy-admin-privacy-budget-refresh).

Only the cumulative privacy loss associated with analysts in the specified account is reset to 0, even if the privacy budget is associated
with analysts in multiple accounts.

Note

When calling RESET\_PRIVACY\_BUDGET, the cumulative privacy loss is not reset
immediately. It is reset the next time a query incurs privacy loss. As a result,
if you view the privacy budget after calling the function but before the first
query incurs privacy loss, the cumulative privacy loss will not be 0.

**Example**

Here’s an example of zeroing out the privacy usage count for all users executing queries in the `companyorg.account_123` account:

Copy code

```
CALL SNOWFLAKE.DATA_PRIVACY.RESET_PRIVACY_BUDGET(
  'my_policy_db.my_policy_schema.my_policy',
  'analyst_budget',
  'companyorg',
  'account_123');
```
