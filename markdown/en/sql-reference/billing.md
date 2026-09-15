# BILLING schema

In the SNOWFLAKE database, the BILLING schema contains views that display billing information for customers of Snowflake resellers and
distributors, as well as FOCUS-compliant cost and usage data for org-enabled accounts.

## BILLING views

The BILLING schema contains the following views:

| View | Latency | Notes |
| --- | --- | --- |
| [COLLABORATION\_REBATE\_CONTRIBUTION](/sql-reference/billing/collaboration_rebate_contribution) | 24 hours |  |
| [FOCUS\_COST\_USAGE\_V1\_3](/sql-reference/billing/focus_cost_usage_v1_3) | 72 hours |  |
| [PARTNER\_CONTRACT\_ITEMS](/sql-reference/billing/partner_contract_items) | 24 hours |  |
| [PARTNER\_RATE\_SHEET\_DAILY](/sql-reference/billing/partner_rate_sheet_daily) | 24 hours |  |
| [PARTNER\_REMAINING\_BALANCE\_DAILY](/sql-reference/billing/partner_remaining_balance_daily) | 24 hours |  |
| [PARTNER\_USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/billing/partner_usage_in_currency_daily) | 24 hours |  |

Expand

Show lessSee more

## Accessing the BILLING schema

The BILLING schema is available in the [organization account](/user-guide/organization-accounts) and a regular account that has the
[ORGADMIN role enabled](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

You must use the ACCOUNTADMIN role to access the views in the schema.
