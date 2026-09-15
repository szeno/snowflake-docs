# Pay for Snowflake Marketplace listings

Learn how to set up billing, understand charges, view and pay Snowflake Marketplace invoices, and manage your paid listings.

**On this page:**

1. [Prerequisites for purchasing paid listings](#label-before-you-begin)
2. [Billing for listings and data products](#label-data-marketplace-consumers-billing)
3. [Set up and manage payment methods](#label-marketplace-payment-methods)
4. [Manage your invoices](#label-manage-invoices)
5. [Manage your purchases](#label-manage-purchases)
6. [Get support or request a refund](#label-contact-provider-support)

## Required roles and privileges

Most tasks on this page require one of the following:

| Access type | Requirement |
| --- | --- |
| Administrator access | ACCOUNTADMIN role |
| Delegated access | PURCHASE DATA EXCHANGE LISTING privilege + IMPORTED PRIVILEGES ([grant privileges](/user-guide/data-exchange-marketplace-privileges#label-granting-imported-privileges-privilege-to-other-roles), [privilege details](/user-guide/data-exchange-marketplace-privileges#label-purchase-data-exchange-listing-account)) |

Expand

Show lessSee more

The PURCHASE DATA EXCHANGE LISTING privilege grants the ability to purchase paid listings and is granted at the account level by an ACCOUNTADMIN. This privilege lets a role create a database from a paid listing and query paid or trial data in the database or application.

To cancel a purchase, you need the ACCOUNTADMIN role or a role with the OWNERSHIP privilege on the database created from the listing.

## 1. Prerequisites for purchasing paid listings

Before your organization purchases a paid Snowflake Marketplace listing, review the following requirements:

- Any organization can pay for listings by using any of the [accepted payment methods](#label-marketplace-payment-methods).
- All purchases are billed in US dollars.
- Taxes are calculated based on your organization’s shipping and billing addresses. This applies even if your organization has multiple locations or is international.
- Snowflake Marketplace invoices are separate from invoices for other Snowflake services, storage, or usage.

### Confirm your billing location is supported

Your organization can access paid listings only if the billing address registered to the account is in a supported country.

Note

Snowflake doesn’t support multiple billing entities for a single organization.

The following countries are supported:

- Australia
- Austria
- Belgium
- Bermuda
- Canada
- Cayman Islands
- Colombia
- Czech Republic
- Denmark
- Finland
- France
- Germany
- India
- Ireland
- Israel
- Italy
- Japan
- Luxembourg
- Mexico
- Netherlands
- New Zealand
- Norway
- Poland
- Portugal
- Saudi Arabia
- Singapore
- South Korea
- Sweden
- Switzerland
- United Arab Emirates
- United Kingdom
- United States

### Accept the combined Snowflake Provider and Consumer Terms

Before purchasing paid listings, an organization administrator must accept the combined
[Snowflake Provider and Consumer Terms](https://other-docs.snowflake.com/en/collaboration/consumer-becoming#label-collaboration-consumer-terms). To learn more about organizations, see [Working with organizations and accounts](/guides-overview-manage).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role** » **ORGADMIN**.
3. Select **Admin** » **Terms**.
4. In the **Snowflake Marketplace** section, select **Review**.
5. If you agree to the terms, select **Accept Terms & Conditions**.

Note

- If your organization intends to access only free listings, and you’ve accepted the [Snowflake Customer-Controlled Data Sharing Functionality Terms](https://www.snowflake.com/legal/data-sharing-terms/), you don’t need to accept the Snowflake Provider and Consumer Terms.
- If you see an error, your user profile might be missing some contact information. If you have an administrator role, see [Add user details to your user profile](/user-guide/ui-snowsight-profile#label-user-details-and-preferences) to update your profile using Snowsight. Otherwise, contact an account administrator to update your user details.

## 2. Billing for listings and data products

### Billing by pricing model

Each listing can have a different pricing model, which determines when and how you’re billed:

| Pricing model | When you’re billed | What triggers charges |
| --- | --- | --- |
| [Usage-based](/collaboration/provider-listings-pricing-model#label-listings-usage-pricing-model) | Monthly, only for months with usage | Queries, billable events, monthly fees, or a combination depending on the listing |
| [Flat-fee](/collaboration/provider-listings-pricing-model#label-listings-subscription-pricing-model) | Upfront at the beginning of the billing term or access period | Access to the listing for the flat-fee term |

Expand

Show lessSee more

Usage-based listings can include per-query charges, billable events, and monthly fees.
Flat-fee listings charge upfront for a specified term and can be recurring or non-recurring.

For more information about pricing models, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model).

### Billing by usage

For usage-based plans, a query can be billable when it accesses paid data, even if the query returns no rows.

| Statement type | Billable? | Example |
| --- | --- | --- |
| SELECT and DML (INSERT, MERGE) | Yes | Querying or modifying paid data |
| DDL that accesses data | Yes | CREATE TABLE AS SELECT on paid data |
| DDL without data access | No | CREATE TABLE, ALTER TABLE |

Expand

Show lessSee more

Usage is tracked daily, so you can [monitor your consumption](#label-monitor-usage). However, billing is processed monthly.
Usage charges are summed up and reflected in the monthly invoice.

## 3. Set up and manage payment methods

Snowflake supports credit card, bank transfer, and Marketplace Capacity Drawdown (MCD) Program funds for paid listings.

| Payment method | How it works | What to know |
| --- | --- | --- |
| MCD funds | Applied automatically when available for a listing. Falls back to another payment method if the listing isn’t MCD-compatible. | [Marketplace Capacity Drawdown details](/collaboration/marketplace-capacity-drawdown). |
| Bank transfer (ACH or wire) | Pay invoices using a virtual bank account number (VBAN) attached to each invoice. | You must include the invoice number in the memo or reference line of the transfer. |
| Credit card | Charged automatically at the interval defined in the payment schedule. | No transaction fees for credit card payments on Snowflake Marketplace. |

Expand

Show lessSee more

### Use Marketplace Capacity Drawdown funds

Marketplace Capacity Drawdown lets eligible organizations use a reserved portion of their committed Snowflake capacity for Snowflake Marketplace purchases. To use this payment method, your organization must be enrolled in the program and the listing must support Marketplace Capacity Drawdown.

If Marketplace Capacity Drawdown is available for a listing, it appears on the purchase page. If it isn’t available, or you don’t want to use it for that purchase, choose another supported payment method.

For more information, see [Marketplace Capacity Drawdown](/collaboration/marketplace-capacity-drawdown).

### Pay by bank transfer or ACH

Each Snowflake Marketplace invoice includes a virtual bank account number (VBAN) confirmation as an attachment to the invoice email. The VBAN is provisioned by Stripe and allows Snowflake to accept bank transfers (ACH or wire) from your organization. Use the VBAN on the invoice to initiate the transfer from your bank.

Important

When paying by bank transfer, always include the **invoice number** (format SM-XXXXX) in the memo or reference line of the payment. Without the invoice number, Snowflake can’t match the transfer to your invoice, which may delay processing and result in overdue notices.

### Pay by credit card

There are no transaction fees for credit card payments.

**To activate your consumer account (first time only):**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Select **Consumer billing**.
5. Select **Activate account**.

**To add a credit card:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Expand **Payment methods** and select **Add credit card**.
5. Enter the card and billing details.
6. Select **Add card**.

   If there are issues with the credit card you added, a status message appears within the tile for the credit card on the **Marketplace billing** tab.

**To delete a credit card:**

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Select **Consumer billing**.
5. Expand **Payment methods** and select a payment method.
6. Select **Delete**, then select **Delete** again to confirm.

## 4. Manage your invoices

To view, download, and pay Snowflake Marketplace invoices, you need the [required roles and privileges](#label-required-roles-and-privileges).

### View all Snowflake Marketplace invoices

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Select **Consumer billing**.

All invoices appear in the **Marketplace invoices** section. You can sort invoices by status, amount, invoice date, and due date.

### View Snowflake Marketplace invoice information

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Select **Consumer billing**.
5. Select an invoice from the **Marketplace invoices** list.
6. Optional: To download a PDF version of the invoice, select **Download PDF**.

### Pay a Snowflake Marketplace invoice

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Select **Admin** » **Billing**.
3. Select the **Marketplace billing** tab.
4. Select **Consumer billing**.
5. Select an invoice from the **Marketplace invoices** list.
6. Select **Make a payment**.

## 5. Manage your purchases

### Control access to a listing

To control access to paid listings, grant the PURCHASE DATA EXCHANGE LISTING privilege. For details, see [Required roles and privileges](#label-required-roles-and-privileges).

### Monitor usage

To monitor usage for paid listings, use the MONETIZED\_USAGE\_DAILY views:

- [MONETIZED\_USAGE\_DAILY (DATA\_SHARING\_USAGE) View](/collaboration/views/monetized-usage-daily-ds) in the
  [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage) schema (account-level usage)
- [MONETIZED\_USAGE\_DAILY (ORGANIZATION\_USAGE) View](/collaboration/views/monetized-usage-daily-org) in the
  [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema (organization-level usage)

### Cancel a purchase

To cancel access to a paid listing, you need the [required privileges](#label-required-roles-and-privileges).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Switch role** » **ACCOUNTADMIN**.
   You can use a custom role if the role has the requisite privileges.
3. Select **Marketplace** » **Snowflake Marketplace**.
4. Select the purchase that you want to cancel.
5. Select **Manage Purchase** » **Cancel Purchase**.
6. Review the cancellation date to verify when your access ends.
7. Confirm your choice to cancel.

## 6. Get support or request a refund

For listing-specific issues, always contact the provider first using the support email listed on the Snowflake Marketplace listing.
This includes:

- Refund requests
- Product issues

If your issue remains unresolved, file a case with Marketplace Operations:
[Report an issue with a Data Marketplace Listing or Provider](https://snowflakecommunity.force.com/s/consumer-reporting).
