# Mar 05, 2026: Preventing a semantic view metric from being aggregated across specific dimensions

If a metric should not be aggregated across specific dimensions, you can now specify those dimensions in the NON ADDITIVE BY
clause of the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command.

For example, to prevent the metric from being aggregated by some date dimensions:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW bank_accounts_sv
  TABLES (
    bank_accounts
  )
  DIMENSIONS (
    bank_accounts.customer_id_dim AS bank_accounts.customer_id,
    bank_accounts.account_type_dim AS bank_accounts.account_type,
    bank_accounts.year_dim AS bank_accounts.year,
    bank_accounts.month_dim AS bank_accounts.month,
    bank_accounts.day_dim AS bank_accounts.day
  )
  METRICS (
    bank_accounts.m_account_balance
      NON ADDITIVE BY (year_dim, month_dim, day_dim)
      AS SUM(balance)
  );
```

For more information, see [Identifying the dimensions that should be non-additive for a metric](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive).
