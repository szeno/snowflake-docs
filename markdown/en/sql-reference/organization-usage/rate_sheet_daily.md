Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# RATE\_SHEET\_DAILY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The RATE\_SHEET\_DAILY view in the ORGANIZATION\_USAGE schema returns the effective rates used for calculating usage in the organization
currency based on credits used for all Snowflake accounts in your organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATE | DATE | Date (in the UTC time zone) for the effective price. |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| CONTRACT\_NUMBER | VARCHAR | Snowflake contract number for the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the account. |
| ACCOUNT\_LOCATOR | VARCHAR | Locator for the account. |
| REGION | VARCHAR | Name of the region where the account is located. |
| SERVICE\_LEVEL | VARCHAR | Service level of the Snowflake account (Standard, Enterprise, Business Critical, etc.). |
| USAGE\_TYPE | VARCHAR | Corresponds to the Usage Category column in a billing statement, which exists for backward compatibility only. Use the BILLING\_TYPE, RATING\_TYPE, SERVICE\_TYPE, and IS\_ADJUSTMENT columns for billing reconciliation. |
| CURRENCY | VARCHAR | The currency of the EFFECTIVE\_RATE. |
| EFFECTIVE\_RATE | NUMBER(38, 2) | The rate after applying any applicable discounts per the contract for the organization. |
| SERVICE\_TYPE | VARCHAR | Type of usage, for example, `snowpipe` for usage related to the Snowpipe feature. |
| RATING\_TYPE | VARCHAR | Indicates how the usage in the record is rated, or priced. Possible values include:   - `compute` - `storage` - `other` |
| BILLING\_TYPE | VARCHAR | Indicates what is being charged or credited. Possible billing types include:   - `consumption` — Usage associated with compute credits, storage costs, and data transfer costs. - `rebate` — Usage covered by the credits awarded to the organization when it shared data with another organization. - `priority support` — Charges for priority support services. This charge is associated with a stipulation in a contract, not with an account. - `vps_deployment_fee` — Charges for a [Virtual Private Snowflake](/user-guide/intro-editions#label-snowflake-editions-vps) deployment. - `support_credit` — Snowflake Support credited the account to reverse charges attributed to an issue in Snowflake. |
| IS\_ADJUSTMENT | BOOLEAN | Indicates whether the record is an adjustment to usage. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- Until month close, data for a given day in a month can change to account for any end-of-month adjustments/credits, mid-month contract amendments, or Snowflake account transfers from one organization to another.
- Customers who signed a contract through a Snowflake reseller cannot access data in this view.
- Data is retained indefinitely.
- This view does not include data generated prior to June 2020. To obtain data before this date, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
