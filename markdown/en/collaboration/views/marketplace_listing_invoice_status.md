Schema:
:   [Data Sharing Usage](/sql-reference/data-sharing-usage)

# MARKETPLACE\_LISTING\_INVOICE\_STATUS view

The MARKETPLACE\_LISTING\_INVOICE\_STATUS view in the [Data Sharing Usage](/sql-reference/data-sharing-usage) schema lets you query the history of invoices related to paid listings in the Snowflake Marketplace.

Only visible to providers of paid listings, this view includes the history of payment statuses per invoice for purchased listings.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| STRIPE\_DISPLAY\_NUMBER | VARCHAR | The Stripe invoice or display number. |
| INVOICE\_DATE | DATE | Date of invoice. |
| USAGE\_MONTH | VARCHAR | The first month when an invoice is generated, in `YYYY-MM-01` format. For example, if the consumer purchases the listing on 12-MAR-2024, then the date in this field is `2024-03-01`. |
| INVOICE\_STATUS | VARCHAR | Status of the invoice. Possible values: `closed` Paid to Snowflake; paid to providers within 30 days. `open` Not yet paid. `void` Canceled. `rebilled` Indicates that a voided invoice was rebilled to make an adjustment. If an invoice is canceled and rebilled, there are two rows for that invoice number: one `void` and one `rebilled`; the invoice created to bill the consumer again has a new number and is `open`. |
| PO\_NUMBER | VARCHAR | Purchase order (PO) number specified by the consumer to buy a listing. The PO number is manually entered by the consumer. |
| CURRENCY | VARCHAR | Always USD (alternate currencies are not supported in this view). |
| TOTAL\_BILLED\_AMOUNT | DECIMAL | Total amount billed to the consumer in USD. This amount includes consumer’s taxes. that apply to the consumer and provider fees. |
| SALES\_TAX\_AMOUNT | DECIMAL | The sales tax in USD payable by the consumer. This amount is included in the `TOTAL_BILLED_AMOUNT` column amount. |
| FEES | DECIMAL | Provider fees. This amount is included in the `TOTAL_BILLED_AMOUNT` column amount. |
| EXPECTED\_PAYOUT\_AMOUNT | DECIMAL | The total expected payout to the provider in USD. This value is calculated by subtracting `SALES_TAX_AMOUNT` and `FEES` from `TOTAL_BILLED_AMOUNT`. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Display name of the listing. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Organization name of the consumer. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account name of the consumer. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer. |
| CONSUMER\_COMPANY\_NAME | VARCHAR | Company name of the consumer. |
| CONSUMER\_BILLING\_EMAIL\_ADDRESS | VARCHAR | Email address associated with billing for the consumer. |

Expand

Show lessSee more

## Usage Notes

- Latency for the view can be up to 48 hours (2 days).
- The data is retained for 365 days (1 year).

## Examples

Retrieve billing information for export.

Copy code

```
SELECT
  stripe_display_number AS snowflake_mp_invoice_number,
  invoice_date,
  usage_month AS first_billing_month,
  invoice_status,
  po_number,
  currency,
  total_billed_amount,
  listing_display_name,
  listing_global_name,
  consumer_organization_name,
  consumer_account_name,
  consumer_account_locator,
  consumer_company_name,
  consumer_billing_email_address
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status;
```

Retrieve details of unpaid invoices by consumer.

Copy code

```
SELECT
  consumer_account_name,
  consumer_account_locator,
  SUM( total_billed_amount ) AS total_outstanding
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE invoice_status IN ('open')
GROUP BY ALL;
```
