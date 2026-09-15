Schema:
:   [BILLING](/sql-reference/billing)

# PARTNER\_RATE\_SHEET\_DAILY view

The PARTNER\_RATE\_SHEET\_DAILY view in the BILLING schema returns the effective rates used for calculating usage in the organization currency. This usage is based on credits used for all Snowflake accounts in the organization of a reseller’s customer.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the reseller’s organization. |
| SOLD\_TO\_ORGANIZATION\_NAME | VARCHAR | Name of the organization of the reseller’s customer. |
| SOLD\_TO\_CUSTOMER\_NAME | VARCHAR | Name of the reseller’s customer. |
| SOLD\_TO\_PO\_NUMBER | VARCHAR | Purchase order number associated with the reseller’s sale to the customer. |
| SOLD\_TO\_CONTRACT\_NUMBER | VARCHAR | Number associated with the customer’s contract with the reseller. |
| DATE | DATE | Date (in UTC) for the effective price. |
| ACCOUNT\_NAME | VARCHAR | Name of the customer’s account. |
| ACCOUNT\_LOCATOR | VARCHAR | Locator of the customer’s account, which is used in the [legacy account identifier](/user-guide/admin-account-identifier#label-account-locator). |
| REGION | VARCHAR | Name of the region where the customer’s account is located. |
| SERVICE\_LEVEL | VARCHAR | Service level of the customer’s Snowflake account (Standard, Enterprise, Business Critical, etc.). |
| USAGE\_TYPE | VARCHAR | Type of usage, which can be one of Compute, Storage, Data Transfer, Materialized Views, etc. |
| BILLING\_TYPE | VARCHAR | Indicates what is being charged or credited. Possible billing types include:   - `consumption` — Usage associated with compute credits, storage costs, and data transfer costs. - `rebate` — Usage covered by the credits awarded to the organization when it shared data with another organization. - `priority support` — Charges for priority support services. This charge is associated with a stipulation in a contract, not with an account. - `vps_deployment_fee` — Charges for a [Virtual Private Snowflake](/user-guide/intro-editions#label-snowflake-editions-vps) deployment. - `support_credit` — Snowflake Support credited the account to reverse charges attributed to an issue in Snowflake. |
| RATING\_TYPE | VARCHAR | Indicates how the usage in the record is rated, or priced. Possible values include:   - `compute` - `storage` - `other` |
| SERVICE\_TYPE | VARCHAR | Type of usage, for example, `snowpipe` for usage related to the Snowpipe feature. |
| IS\_ADJUSTMENT | BOOLEAN | Indicates whether the record is an adjustment to usage. |
| CURRENCY | VARCHAR | Currency of the EFFECTIVE\_RATE. |
| EFFECTIVE\_RATE | NUMBER(38, 2) | Rate after applying any applicable discounts. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 24 hours.
- Until month close, data for a given day in a month can change to account for any end-of-month adjustments, mid-month contract amendments, or Snowflake account transfers from one organization to another.
