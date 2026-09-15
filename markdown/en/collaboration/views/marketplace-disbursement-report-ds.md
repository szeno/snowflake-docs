Schema:
:   [Data Sharing Usage](/sql-reference/data-sharing-usage)

# MARKETPLACE\_DISBURSEMENT\_REPORT View

The MARKETPLACE\_DISBURSEMENT\_REPORT view in the [Data Sharing Usage](/sql-reference/data-sharing-usage) schema lets you query the history of your earnings from
paid listings in the Snowflake Marketplace.

The view includes the history for a specific listing. Only visible to providers of paid listings, this view includes the history of payment statuses per invoice for purchased listings.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| STRIPE\_DISPLAY\_NUMBER | VARCHAR | The Stripe invoice or display number. |
| EVENT\_DATE | DATE | Date when the payment event occurred. |
| EVENT\_TYPE | VARCHAR | Type of event (payment). |
| INVOICE\_DATE | DATE | Date of the invoice. |
| LISTING\_NAME | VARCHAR | Identifier for the listing. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name for the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. |
| CHARGE\_TYPE | VARCHAR | Type of charge assessed. For more information about the components of the pricing model for paid listings, see [Paid Listings Pricing Models](https://other-docs.snowflake.com/collaboration/provider-listings-pricing-model). Possible values: `FIXED`: Per-month charges. Also includes per-query charges if included by the provider in the pricing plan for the listing. `VARIABLE`: Per-query charges only. |
| GROSS | DECIMAL | Gross amount billed to the consumer. |
| FEES | DECIMAL | Pre-tax fees, owed to Snowflake by the provider. Snowflake subtracts the fees from the gross amount. |
| TAXES | DECIMAL | Sales tax (on the fees), owed to Snowflake by the provider. Snowflake subtracts the taxes from the gross amount. |
| NET\_AMOUNT | DECIMAL | Actual amount to be paid to the provider. The equation for this is: `NET_AMOUNT` = `GROSS` - `FEES` - `TAXES`. |
| CURRENCY | VARCHAR | USD |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Name of the consumer account. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator for the consumer account. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Name of the consumer organization. |

Expand

Show lessSee more

## Usage Notes

- Latency for the view can be up to 48 hours (2 days).
- The data is retained for 365 days (1 year).

## Examples

Retrieve the total amount disbursed to a provider’s bank account for each month for each listing:

Copy code

```
SELECT
  event_date
, listing_name
, listing_display_name
, listing_global_name
, currency
, SUM(net_amount) AS net_amount
FROM snowflake.data_sharing_usage.marketplace_disbursement_report
WHERE event_type = 'payment'
GROUP BY 1,2,3,4,5;
```

Retrieve the total amount that has been disbursed for each invoice period, grouped by listing and charge type. Note that the invoice period
could be spread out over multiple report dates:

Copy code

```
SELECT
  invoice_date
, listing_name
, listing_display_name
, listing_global_name
, charge_type
, currency
, SUM(gross) AS gross
, SUM(fees) AS fees
, SUM(taxes) AS taxes
, SUM(net_amount) AS net_amount
FROM snowflake.data_sharing_usage.marketplace_disbursement_report
WHERE event_type = 'payment'
GROUP BY 1,2,3,4,5,6;
```
