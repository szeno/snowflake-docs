Schema:
:   [Data Sharing Usage](/sql-reference/data-sharing-usage)

# MARKETPLACE\_LISTING\_INVOICE\_STATUS view

The MARKETPLACE\_LISTING\_INVOICE\_STATUS view in the [Data Sharing Usage](/sql-reference/data-sharing-usage) schema lets providers of paid Snowflake Marketplace listings track each invoice’s full billing lifecycle: what was billed, collected, and disbursed. Rows are at line-item grain (one invoice can span multiple rows, for example installments), and the view is visible only to providers of paid listings, showing only their own data.

Use this view for the following tasks:

- **Cash-flow forecasting:** See whether each invoice is unpaid, collected but not yet disbursed, or disbursed, and when the payout was made.
- **Collections and aging:** Find open invoices by due date, and see the amount billed, the Marketplace Capacity Drawdown (MCD) amount applied, and the balance remaining after MCD.
- **Payout reconciliation:** Compare the expected payout with the amount disbursed, and tie disbursements to bank deposits by date.
- **Invoice and offer details:** Review subtotals, sales tax, fees, billing periods, installment numbers, and the offer name and type for each line item.
- **Consumer and jurisdiction details:** Get the consumer’s billing and shipping addresses, the additional recipients selected at checkout, and the billing email address on file, for example to confirm tax jurisdiction or contact a consumer about an overdue invoice.
- **Revenue reporting:** Summarize billed and disbursed amounts by month, listing, or consumer.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| STRIPE\_DISPLAY\_NUMBER | VARCHAR | The Snowflake Marketplace invoice number. This column has the same value as `INVOICE_NUMBER` today. Use `INVOICE_NUMBER` for joins. `STRIPE_DISPLAY_NUMBER` is a legacy column. |
| INVOICE\_DATE | DATE | The date the consumer was billed for the product subscription. |
| USAGE\_MONTH | DATE | The first month for which the invoice is generated, as the first day of that month (`YYYY-MM-01`). For example, if the consumer purchases the listing on 12-MAR-2024, then the date in this field is `2024-03-01`. |
| INVOICE\_STATUS | VARCHAR | Status of the invoice. Possible values: `open` (not yet paid), `closed` (paid, credited, or written off; paid invoices are disbursed to providers within 30 days), `void` (canceled), and `rebilled` (replaced by a new invoice). |
| PO\_NUMBER | VARCHAR | Purchase order (PO) number specified by the consumer to buy a listing. The PO number is manually entered by the consumer. |
| CURRENCY | VARCHAR | Currency of the transaction. Always USD. |
| TOTAL\_BILLED\_AMOUNT | DECIMAL | Total amount billed to the consumer in USD. This amount includes the consumer’s taxes and provider fees. |
| FEE | DECIMAL | Provider fees owed to Snowflake. Snowflake subtracts the fees from the total billed amount. |
| SALES\_TAX\_AMOUNT | DECIMAL | The sales tax in USD payable by the consumer. This amount is included in the `TOTAL_BILLED_AMOUNT` column. |
| EXPECTED\_PAYOUT\_AMOUNT | DECIMAL | The total expected payout to the provider in USD. Calculated as `TOTAL_BILLED_AMOUNT` - `SALES_TAX_AMOUNT` - `FEE`. |
| LISTING\_DISPLAY\_NAME | VARCHAR | Title of the listing product. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | Name of the consumer organization. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account name of the consumer. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer. |
| CONSUMER\_COMPANY\_NAME | VARCHAR | Company name of the consumer. |
| CONSUMER\_BILLING\_EMAIL\_ADDRESS | VARCHAR | The Snowflake Marketplace billing email address on file. |
| INVOICE\_NUMBER | VARCHAR | Snowflake Marketplace invoice number. This is the invoice identifier to use for joins. It has the same value as `STRIPE_DISPLAY_NUMBER` today. |
| PURCHASER\_EMAILS | ARRAY | Email addresses that the consumer selected as **Additional Recipients** during checkout. |
| CONSUMER\_BILL\_TO | OBJECT | Consumer bill-to address, with the keys `city`, `state`, `country`, and `postal_code`. |
| CONSUMER\_SHIP\_TO | OBJECT | Consumer ship-to address, with the keys `city`, `state`, `country`, and `postal_code`. |
| OFFER\_NAME | VARCHAR | The seller-defined name of the offer. |
| OFFER\_TYPE | VARCHAR | Whether the offer is standard or private. Possible values: `STANDARD`, `PRIVATE`. |
| SUBTOTAL\_AMOUNT | DECIMAL | The list price of the offer or listing in USD, before sales tax. Calculated as `TOTAL_BILLED_AMOUNT` - `SALES_TAX_AMOUNT`. |
| BILLING\_PERIOD\_START\_DATE | DATE | The start date of the billing period for the invoice. |
| BILLING\_PERIOD\_END\_DATE | DATE | The end date of the billing period for the invoice. |
| INSTALLMENT\_NUMBER | NUMBER | Installment number. NULL if the invoice isn’t part of an installment plan. |
| DUE\_DATE | DATE | The payment due date. |
| MCD\_APPLIED\_AMOUNT | DECIMAL | [Marketplace Capacity Drawdown (MCD)](/collaboration/marketplace-capacity-drawdown) amount applied to the line item. |
| BALANCE\_AFTER\_MCD | DECIMAL | The balance remaining after MCD is applied. Calculated as `TOTAL_BILLED_AMOUNT` - `MCD_APPLIED_AMOUNT`. This value reflects MCD only. It doesn’t include other payments, so it isn’t the outstanding balance. |
| CONSUMER\_PAID\_IN\_FULL\_DATE | DATE | The date the consumer paid Snowflake in full. This isn’t the provider payout date. For the payout date, see `DISBURSEMENT_DATE`. NULL if the invoice isn’t paid in full, including when the status is `open`, or when the invoice is written off, voided, or rebilled. |
| DISBURSEMENT\_STATUS | VARCHAR | Indicates whether funds have been disbursed to the provider’s bank account. Possible values: `Disbursed`, `Not disbursed`. NULL if the invoice is open or otherwise isn’t eligible for disbursement, or if the payment event has a net amount of zero. |
| DISBURSEMENT\_DATE | DATE | Date when the payout was disbursed to the provider’s bank account. Corresponds to `EVENT_DATE` in the [MARKETPLACE\_DISBURSEMENT\_REPORT view](/collaboration/views/marketplace-disbursement-report-ds) where `EVENT_TYPE` is `payment`. |
| DISBURSEMENT\_AMOUNT | DECIMAL | Actual amount paid to the provider in USD. Corresponds to `NET_AMOUNT` in the [MARKETPLACE\_DISBURSEMENT\_REPORT view](/collaboration/views/marketplace-disbursement-report-ds), calculated as `GROSS` - `FEES` - `TAXES`. |
| PROVIDER\_SALES\_TAX\_AMOUNT | DECIMAL | Sales tax on the fees, owed to Snowflake by the provider. Corresponds to `TAXES` in the [MARKETPLACE\_DISBURSEMENT\_REPORT view](/collaboration/views/marketplace-disbursement-report-ds). |

Expand

Show lessSee more

## Usage Notes

- Latency for the view can be up to 24 hours.
- The data is retained for 7 years.

## Examples

Note

- Each row is one line item. An invoice can span multiple rows, for example when it is billed in installments, so aggregate amounts rather than assume one row per invoice.
- In example 2, **Compare disbursed and open amounts**, uncomment the optional date filter to limit results to your reporting period. `disbursement_date` is NULL until an invoice is disbursed.

### 1. Open accounts receivable and aging

Retrieve unpaid invoices, oldest overdue first, with the consumer contacts to follow up with and the line-item balance after Marketplace Capacity Drawdown (MCD) is applied. `days_overdue` is negative for invoices that aren’t due yet. To see only past-due invoices, uncomment the optional filter.

`balance_after_mcd` reflects MCD only, at line-item grain. It isn’t a true outstanding balance, and it doesn’t account for payments that aren’t MCD or for partial payments.

Copy code

```
SELECT
  invoice_number,
  invoice_status,
  due_date,
  DATEDIFF('day', due_date, CURRENT_DATE()) AS days_overdue,
  listing_display_name,
  installment_number,
  consumer_account_name,
  consumer_company_name,
  consumer_billing_email_address,
  purchaser_emails,
  subtotal_amount,
  total_billed_amount,
  mcd_applied_amount,
  balance_after_mcd
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE invoice_status = 'open'
  -- Optional: uncomment to show only past-due invoices.
  -- AND due_date < CURRENT_DATE()
ORDER BY due_date;
```

### 2. Compare disbursed and open amounts

For each line item, open items first, see whether it has been disbursed to you, how much was disbursed and when, and how much is still open, meaning not yet disbursed.

Copy code

```
SELECT
  invoice_number,
  invoice_date,
  due_date,
  listing_display_name,
  installment_number,
  consumer_account_name,
  invoice_status,
  IFF(disbursement_status = 'Disbursed', 'Disbursed', 'Open') AS payout_status,
  expected_payout_amount,
  IFF(disbursement_status = 'Disbursed', disbursement_amount, 0) AS disbursed_amount,
  IFF(disbursement_status = 'Disbursed', 0, expected_payout_amount) AS open_amount,
  disbursement_date
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE invoice_status IN ('open', 'closed')
  -- Optional: uncomment and edit to limit results to a reporting period.
  -- AND invoice_date BETWEEN '2026-01-01' AND '2026-03-31'
ORDER BY payout_status DESC, invoice_number, installment_number;
```

### 3. Summarize monthly payouts

Retrieve the total amount disbursed in each month.

Copy code

```
SELECT
  DATE_TRUNC('month', disbursement_date) AS disbursement_month,
  SUM(disbursement_amount) AS total_disbursed
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE disbursement_status = 'Disbursed'
GROUP BY ALL
ORDER BY disbursement_month;
```

### 4. Forecast cash flow by payment stage

List each line item with its payment stage, based on whether the consumer has paid in full (`consumer_paid_in_full_date`) and whether you’ve been paid out (`disbursement_status`):

- **Disbursed:** Snowflake has paid you.
- **Collected, not disbursed:** the consumer paid in full, or MCD covered the full amount, but you haven’t been paid out yet.
- **Billed, Partially paid:** MCD covered part of the amount, so `balance_after_mcd` is less than `total_billed_amount`.
- **Billed, not paid:** the invoice is open and nothing has been paid.
- **Closed, payment not applicable:** the invoice was closed without any payment being due, for example because it was credited or written off.

Rows are sorted by stage, starting with billed but unpaid, with the dates that show where each line item is in the cycle. Voided and rebilled rows are excluded so that canceled invoices aren’t counted.

Copy code

```
SELECT
  CASE
    WHEN disbursement_status = 'Disbursed' THEN 'Disbursed'
    WHEN consumer_paid_in_full_date IS NOT NULL OR balance_after_mcd = 0 THEN 'Collected, not disbursed'
    WHEN balance_after_mcd <> total_billed_amount THEN 'Billed, Partially paid'
    WHEN invoice_status = 'open' THEN 'Billed, not paid'
    ELSE 'Closed, payment not applicable'
  END AS payment_stage,
  invoice_number,
  listing_display_name,
  installment_number,
  consumer_account_name,
  invoice_date,
  due_date,
  consumer_paid_in_full_date,
  disbursement_date,
  total_billed_amount,
  balance_after_mcd,
  expected_payout_amount,
  disbursement_amount
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE invoice_status IN ('open', 'closed')
ORDER BY
  CASE payment_stage
    WHEN 'Billed, not paid' THEN 1
    WHEN 'Billed, Partially paid' THEN 2
    WHEN 'Collected, not disbursed' THEN 3
    WHEN 'Disbursed' THEN 4
    ELSE 5
  END,
  due_date,
  invoice_number,
  installment_number;
```

### 5. Total each invoice across line items

Combine line items into one row per invoice, with the listings on the invoice, billed amount, sales tax, fees, MCD applied, and expected payout. Voided and rebilled rows are excluded so that canceled invoices aren’t counted.

Copy code

```
SELECT
  invoice_number,
  ANY_VALUE(consumer_account_name) AS consumer_account_name,
  LISTAGG(DISTINCT listing_display_name, ', ') AS listings,
  MIN(due_date) AS first_due_date,
  SUM(subtotal_amount) AS subtotal,
  SUM(sales_tax_amount) AS sales_tax,
  SUM(fee) AS fee,
  SUM(total_billed_amount) AS total_billed,
  SUM(mcd_applied_amount) AS mcd_applied,
  SUM(expected_payout_amount) AS expected_payout
FROM snowflake.data_sharing_usage.marketplace_listing_invoice_status
WHERE invoice_status IN ('open', 'closed')
GROUP BY invoice_number
ORDER BY invoice_number;
```
