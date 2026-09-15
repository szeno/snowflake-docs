# View consumer invoices for your listings

Snowflake issues invoices to consumers for Snowflake Marketplace provider paid listings. A consumer invoice lists the purchases and the billed amount for the invoicing period.

To access consumer invoices in Snowsight, you must have been granted the ACCOUNTADMIN role.

To view consumer invoices in Provider Studio across all your listings:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Invoices** tab.

To view consumer invoices for a specific listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, select the **Listings** tab.
4. Select a paid listing.
5. Select the **Invoices** tab.

To view consumer invoices from the Billing module:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. Select **Marketplace Billing**.
4. Select the **Provider** tab.

## Cancel a consumer invoice

You can request cancellation of a consumer invoice directly from the invoices table. To cancel an invoice:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select the **Invoices** tab.
4. In the row for the invoice you want to cancel, select [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) and then select **Cancel invoice**.
5. In the dialog that opens, follow the instructions to confirm the cancellation.

The cancellation process depends on the invoice amount:

- **Under $33,000 USD**: Snowflake processes the cancellation directly. It usually completes within 30 minutes.
- **$33,000 USD or more**: The dialog directs you to open a [provider onboarding case](https://snowforce.my.site.com/s/provider-onboarding-case). The Snowflake internal team reviews and processes your cancellation request.
