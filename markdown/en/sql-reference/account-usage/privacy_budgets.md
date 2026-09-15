Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PRIVACY\_BUDGETS view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view lets you retrieve the privacy budgets associated with
[privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) in an account.

For more information about viewing privacy budgets, see [View a privacy budget](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-privacy-budget-view).

## Columns

| Column | Data type | Description |
| --- | --- | --- |
| `database_name` | VARCHAR | Database that contains the privacy policy. |
| `schema_name` | VARCHAR | Schema that contains the privacy policy. |
| `policy_name` | VARCHAR | Name of the privacy policy. |
| `budget_name` | VARCHAR | Name of the privacy budget in the privacy policy. |
| `consumer_id` | VARCHAR | Organization and account where users executed queries that incurred privacy loss. |
| `budget_spent` | FLOAT | Cumulative privacy loss since the last time the [privacy budget was refreshed](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-privacy-budget-refresh). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- A privacy budget only appears if analysts associated with the privacy budget have incurred privacy loss or if an administrator has
  [reset the privacy budget](/user-guide/diff-privacy/differential-privacy-admin-privacy-budgets#label-diff-privacy-admin-privacy-budget-reset).
