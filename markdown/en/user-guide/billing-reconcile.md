# Reconcile a billing usage statement

Snowflake generates [billing usage statements](/user-guide/billing-usage-statement) for customers with at least one active contract,
also known as the Snowflake Order Form.

This topic describes how to use queries to reconcile a statement with the usage data found in the billing views of the
[Organization Usage schema](/sql-reference/organization-usage). To execute these queries, you need to do one of the following:

- Sign in to the [organization account](/user-guide/organization-accounts) as a user with the GLOBALORGADMIN role.
- Sign in to an ORGADMIN-enabled account as a user with the ACCOUNTADMIN role.

Note

When executing queries to reconcile usage incurred prior to March 1, 2024, the results of the query might differ slightly from those in
the usage statement. Before this date, some billing views did not round values to match the usage statement. For example, prior to March
1, 2024:

- Usage of $0.001 or -$0.001 were not included in usage statements but were included in the billing views.
- Usage of $1.004 was rounded down to $1.00 in the usage statement but not in the billing views.
- Usage of $1.006 was rounded up to $1.01 in the usage statement but not in the billing views.

Differences between query results and usage statements are small, ranging from a few cents to less than 10 dollars, depending on how long
the contract has been active.

## Reconcile the remaining balance

Snowflake customers with a contract make an upfront financial commitment to pay for a specified amount of usage (that is, a capacity
commitment). As the customer uses Snowflake, the currency spent is deducted from this capacity commitment. The Summary section of each
usage statement identifies the remaining balance on a contract, which is calculated by subtracting the total usage since the start of the
contract from the original capacity commitment.

Use the following query to reconcile the remaining balance shown on a usage statement with data in the
[REMAINING\_BALANCE\_DAILY view](/sql-reference/organization-usage/remaining_balance_daily). Replace the date with the last day of the month shown on the usage
statement.

Copy code

```
SELECT date,
       contract_number,
       (capacity_balance + free_usage_balance + rollover_balance) AS remaining_balance
  FROM snowflake.organization_usage.remaining_balance_daily
  WHERE TRUE
    AND date = LAST_DAY(TO_DATE('2024-01-01'));
```

Note

If the subscription term of a contract has ended, the preceding query correctly returns 0, but the value in the usage statement might
be a number other than zero. This is a known discrepancy that will be addressed in a future update.

## Reconcile total usage for a contract

Snowflake keeps track of how much has been spent on usage since the start of a contract, and classifies this amount as Total Consumed, which
is found in the Summary section of a usage statement. This consumption is tracked in currency spent, not credits consumed.

Use the following query to reconcile the total consumption shown on a usage statement with data in the
[USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily). The total consumption returned by the query does not include usage whose
`balance_source` is `overage`. Replace the date with the last day of the month shown on the usage statement.

Copy code

```
SELECT contract_number,
       SUM(usage_in_currency) AS total_consumed
  FROM snowflake.organization_usage.usage_in_currency_daily
  WHERE TRUE
    AND usage_date <= LAST_DAY(TO_DATE('2024-01-01'))
    AND LOWER(balance_source) != 'overage'
  GROUP BY 1
  ORDER BY 1;
```

## Reconcile total monthly usage by account

The Monthly Usage section of a statement includes a line item for each account in the organization. Each line item shows the total usage in
an account for the month. It shows how many credits were consumed and the amount spent in currency.

Use the following query to reconcile the total monthly usage of each account with the data in the
[USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily). The total usage returned by the query does not include usage whose
`balance_source` is `overage`. Replace the date with the last day of the month shown on the usage statement.

Copy code

```
SELECT contract_number,
       DATE_TRUNC(month, usage_date) AS usage_month,
       CONCAT(account_locator,'-',region) AS account_name,
       SUM(usage_in_currency) AS total_consumed,
  FROM snowflake.organization_usage.usage_in_currency_daily
  WHERE TRUE
    AND usage_month = DATE_TRUNC(month,to_date('2024-01-01'))
    AND LOWER(balance_source) != 'overage'
  GROUP BY 1,2,3
  ORDER BY 1,2,3;
```

Note

There are different naming conventions for regions within Snowflake. The name of the region returned by the preceding query might not
match what you see in the Monthly Usage section of the usage statement, but it refers to the same region. This is a known
discrepancy that will be addressed in a future update.

## Reconcile each type of usage

Snowflake usage can be attributed to different features and [architectural components](/user-guide/intro-key-concepts). The Monthly
Usage section of a statement itemizes usage based on the source of the usage, grouped by the account where the usage occurred. For example,
usage attributed to automatic clustering in account `account_1` appears on a different line than automatic clustering usage in account
`account_2`. Each line shows how many credits were consumed and the amount spent in currency.

Use the following query to reconcile individual categories of usage shown in the statement’s Monthly Usage section with data in the
[USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily). Like the statement, each type of usage is grouped by account in the
query results. Replace the date with the last day of the month shown on the usage statement.

Copy code

```
SELECT contract_number,
       DATE_TRUNC(month, usage_date) AS usage_month,
       CONCAT(account_locator,'-',region) AS account_name,
       usage_type AS usage_category,
       SUM(usage) AS units_consumed,
       SUM(usage_in_currency) AS total_usage
  FROM snowflake.organization_usage.usage_in_currency_daily
  WHERE TRUE
    AND usage_month = DATE_TRUNC(month, TO_DATE('2024-01-01'))
  GROUP BY 1,2,3,4
  ORDER BY 1,2,3,4;
```

Note

There are different naming conventions for regions within Snowflake. The name of the region returned by the preceding query might not
match what you see in the Monthly Usage section of the usage statement, but it refers to the same region. This is a known
discrepancy that will be addressed in a future update.
