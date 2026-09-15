Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# REMAINING\_BALANCE\_DAILY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The REMAINING\_BALANCE\_DAILY view in the ORGANIZATION\_USAGE schema can be used to return the daily remaining balance and on demand
consumption daily for an organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| CONTRACT\_NUMBER | VARCHAR | Contract number for the organization. |
| DATE | DATE | The date of the FREE\_USAGE\_BALANCE or CAPACITY\_BALANCE in the UTC time zone. |
| CURRENCY | VARCHAR | The currency of the FREE\_USAGE\_BALANCE or CAPACITY\_BALANCE or ON\_DEMAND\_CONSUMPTION\_BALANCE. |
| FREE\_USAGE\_BALANCE | NUMBER (38,2) | The amount of free usage in currency that is available for use as of the date. This is the end of day balance. |
| CAPACITY\_BALANCE | NUMBER (38,2) | The amount of capacity in currency that is available for use as of the date. This is the end of day balance. |
| ON\_DEMAND\_CONSUMPTION\_BALANCE | NUMBER (38,2) | The amount of consumption at on demand prices that will be invoiced given that all the free usage and capacity balances have been exhausted. This is a negative value (e.g. -250) until the invoice is paid. This is the end of day balance. |
| ROLLOVER\_BALANCE | NUMBER (38,2) | The amount of rollover balance in currency that is available for use at the end of the date. At the end of a contract term, it is calculated as sum(AMOUNT) from the CONTRACT\_ITEMS view - sum(USAGE\_IN\_CURRENCY) from the USAGE\_IN\_CURRENCY\_DAILY view. |
| MARKETPLACE\_CAPACITY\_DRAWDOWN\_BALANCE | NUMBER(38,2) | Amount of CAPACITY\_BALANCE that is available for purchases in the Snowflake Marketplace. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 72 hours.
- If multiple organizations draw down from the same capacity contract, only the primary organization can access this view. The primary
  organization is also known as the funding organization.
- On demand consumption balance resets after month close (typically on the 3rd or 4th day of the next month) after it is invoiced and paid.
- Until month close, data for a given day in a month can change to account for any end-of-month adjustments/credits or contract amendments
  between Snowflake organizations.
- Customers who signed a contract through a Snowflake reseller cannot access data in this view.
- Data is retained indefinitely.
- This view does not include data generated prior to June 2020. To obtain data before this date, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
