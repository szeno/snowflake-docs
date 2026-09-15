Schema:
:   [Organization Usage](/sql-reference/organization-usage)

# MARKETPLACE\_PAID\_USAGE\_DAILY View

You can use the MARKETPLACE\_PAID\_USAGE\_DAILY view in the [Organization Usage](/sql-reference/organization-usage) schema to query the daily history of your usage of paid
listings. Retrieve the count of queries executed by users in your account on individual listings, with the charges for the usage.

The view includes this history for all accounts in your Snowflake organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REPORT\_DATE | DATETIME | Date when the report was run. |
| USAGE\_DATE | DATETIME | Usage date. |
| PROVIDER\_NAME | VARCHAR | Provider display name from listing. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Account name of the provider. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the provider account. For more information about account identifiers, see [Account identifiers](/user-guide/admin-account-identifier). |
| PROVIDER\_ORGANIZATION\_NAME | VARCHAR | Organization name for the provider. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Name of the consumer account. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer account. For more information about account identifiers, see [Account identifiers](/user-guide/admin-account-identifier). |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. |
| DATABASE\_NAME | VARCHAR | Name of the database associated with this listing. |
| PO\_NUMBER | VARCHAR | Purchase order number associated with this listing. |
| PRICING\_PLAN | VARIANT | JSON value that includes the specifics of the pricing plan. Only included in the output for paid usage. |
| CHARGE\_TYPE | VARCHAR | Type of charge assessed. For more information about the components of the pricing model for paid listings, see [Paid Listings Pricing Models](https://other-docs.snowflake.com/collaboration/provider-listings-pricing-model).  Possible values:   - `SAMPLE`: No charge. The queries were executed within the trial period for the listing. - `FIXED`: Per-month charges. - `GRACE`: No charge. The queries were counted among the free queries allowed in the calendar month (after the first query)   before the per-query charge is applied. - `VARIABLE`: Per-query charges. - `MAX_VARIABLE_USAGE_REACHED`: No charge. The queries were executed after the maximum total monthly cost for this listing   was reached. - `NON_MONETIZABLE_BILLING_EVENTS`: No charge. These billable events were emitted during trial usage of a data product,   or for billable events not part of a pricing plan on the listing. - `MONETIZABLE_BILLING_EVENTS`: Custom event billing charges. - `MAX_BILLING_EVENT_USAGE_REACHED`: No charge. These billable events were emitted after the maximum total monthly cost for   the listing was reached.   Additional values are part of preview functionality:   - SPCS\_COMPUTE\_POOL\_SURCHARGE: The amount of the SPCS compute pool surcharge. - MAX\_SPCS\_COMPUTE\_POOL\_SURCHARGE\_REACHED: No further charge. When the consumer ran additional   queries, they had already reached the maximum total SPCS compute pool surcharge for this listing. |
| UNITS | VARCHAR | Number of queries included in the charge. For a `FIXED` charge, this value is `1`. |
| UNIT\_PRICE | DECIMAL | Per-month or per-query fee. For sample data, the value is `0`. |
| CHARGE | DECIMAL | Total charge for this line item on this day (without tax). |
| CURRENCY | VARCHAR | USD |

Expand

Show lessSee more

## Usage Notes

- Latency for the view can be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).

## Examples

Retrieve the total amount charged per month and listing:

Copy code

```
SELECT
  DATE_TRUNC(MONTH, usage_date) AS usage_month
, listing_display_name
, listing_global_name
, SUM(charge) AS charge
FROM snowflake.organization_usage.marketplace_paid_usage_daily
GROUP BY 1,2,3;
```

Retrieve the total amount charged per month, listing, and consumer account:

Copy code

```
SELECT
  DATE_TRUNC(MONTH, usage_date) AS usage_month
, consumer_account_name
, consumer_account_locator
, listing_display_name
, listing_global_name
, SUM(charge) AS charge
FROM snowflake.organization_usage.marketplace_paid_usage_daily
GROUP BY 1,2,3,4,5;
```
