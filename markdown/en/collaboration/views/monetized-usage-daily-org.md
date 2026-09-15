Schema:
:   [Organization Usage](/sql-reference/organization-usage)

# MONETIZED\_USAGE\_DAILY View

As a provider of listings, the MONETIZED\_USAGE\_DAILY view in the [Organization Usage](/sql-reference/organization-usage) schema lets you query the history of daily
consumer usage for each listing, including charges accumulated for the usage. For consumer payment information,
query the MARKETPLACE\_DISBURSEMENT\_REPORT view in the ORGANIZATION\_USAGE or DATA\_SHARING\_USAGE schema.

The view includes the history of consumer usage for all accounts in your Snowflake organization.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| REPORT\_DATE | DATETIME | Date when the report was run. |
| USAGE\_DATE | DATE | Usage date. |
| LISTING\_OWNER\_ACCOUNT\_NAME | VARCHAR | Name of the provider account that owns the listing. |
| LISTING\_OWNER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator for the provider account that owns the listing. For more information about account identifiers, see [Account identifiers](/user-guide/admin-account-identifier). |
| LISTING\_NAME | VARCHAR | Identifier for the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name for the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name for the listing. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer account. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Name of the consumer account. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Organization name of the consumer account. |
| CONSUMER\_SNOWFLAKE\_REGION | VARCHAR | Cloud service [region](/user-guide/intro-regions) where the consumer account is hosted. |
| PRICING\_PLAN | JSON | JSON value that includes the specifics of the pricing plan. Only included in the output for paid usage. |
| CHARGE\_TYPE | VARCHAR | Type of charge assessed. For more information about the components of the pricing model for paid listings, see [Paid Listings Pricing Models](https://other-docs.snowflake.com/collaboration/provider-listings-pricing-model).  Possible values:   - `SAMPLE`: No charge. The queries were executed within the trial period for the listing. - `FIXED`: Per-month charges. - `GRACE`: No charge. The queries were counted among the free queries allowed in the calendar month (after the first query)   before the per-query charge is applied. - `VARIABLE`: Per-query charges. - `MAX_VARIABLE_USAGE_REACHED`: No charge. The queries were executed after the maximum total monthly cost for this listing   was reached. - `NON_MONETIZABLE_BILLING_EVENTS`: No charge. These billable events were emitted during trial usage of a data product,   or for billable events not part of a pricing plan on the listing. - `MONETIZABLE_BILLING_EVENTS`: Custom event billing charges. - `MAX_BILLING_EVENT_USAGE_REACHED`: No charge. These billable events were emitted after the maximum total monthly cost for   the listing was reached.   Additional values are part of preview functionality:   - SPCS\_COMPUTE\_POOL\_SURCHARGE: The amount of the SPCS compute pool surcharge. - MAX\_SPCS\_COMPUTE\_POOL\_SURCHARGE\_REACHED: No further charge. When the consumer ran additional   queries, they had already reached the maximum total SPCS compute pool surcharge for this listing. |
| UNITS | VARCHAR | Number of queries included in the charge. For a `FIXED` charge, this value is `1`. |
| UNIT\_PRICE | DECIMAL | Per-month or per-query fee. For free queries or usage after the maximum total charge for the month is reached, the value is `0`. |
| GROSS\_CHARGE | DECIMAL | Total charge for this line item on this day. |
| CURRENCY | VARCHAR | USD |

Expand

Show lessSee more

## Usage Notes

- Latency for the view can be up to 24 hours (1 day).
- The data is retained for 365 days (1 year).

## Examples

Retrieve the total number of queries run and the total gross charges by customer and month. Queries are returned as number of units:

Copy code

```
SELECT
  DATE_TRUNC(MONTH, usage_date) AS usage_month
, consumer_organization_name
, consumer_snowflake_region
, consumer_account_locator
, consumer_account_name
, currency
, SUM(units) AS units
, SUM(gross_charge) AS gross_charge
FROM snowflake.organization_usage.monetized_usage_daily
GROUP BY 1,2,3,4,5,6;
```

Retrieve the total number of queries run and the total gross charges by listing and month:

Copy code

```
SELECT
  DATE_TRUNC(MONTH, usage_date) AS usage_month
, listing_name
, listing_display_name
, listing_global_name
, currency
, SUM(units) AS units
, SUM(gross_charge) AS gross_charge
FROM snowflake.organization_usage.monetized_usage_daily
GROUP BY 1,2,3,4,5;
```

Retrieve the total number of queries run and the total gross charges by charge type, consumer, and month:

Copy code

```
SELECT
  DATE_TRUNC(MONTH, usage_date) AS usage_month
, consumer_organization_name
, consumer_snowflake_region
, consumer_account_locator
, consumer_account_name
, charge_type
, currency
, SUM(units) AS units
, SUM(gross_charge) AS gross_charge
FROM snowflake.organization_usage.monetized_usage_daily
GROUP BY 1,2,3,4,5,6,7;
```
