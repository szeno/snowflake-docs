# Manage offers in Snowsight

## View and accept an offer

Consumers can view offers in the following ways:

- For offers on the **Data sharing** » **External sharing** page, the **Shared with you** tab shows offers that have been
  shared privately with you outside of Snowflake Marketplace.
- For offers on Snowflake Marketplace, you can access an offer by doing the following:
  - Copy and paste the URL that the provider shared with you into the search bar.
  - Search for or browse to the listing you want to access that includes the offer.

To accept an offer, follow these steps:

1. Navigate to the listing you want to access that includes the offer, and then open the offer.

   This opens the **Review offer** page for a standard offer, or the **Review Private offer** page for a private offer.
2. Review the offer details, including the pricing plan, contract duration, terms of service, and any attachments the provider has included.
3. Select **Continue to checkout**.

   This opens the **Complete your purchase** page. For details about the sections on this page, see the following sections:

   - [View and accept a private offer](#label-consumers-manage-offers-private-flat-fee-checkout)
   - [View and accept a standard offer](#label-consumers-manage-offers-standard-checkout)

Note

If you can’t complete the purchase, for example because your current role doesn’t have the required privileges, the review page shows a message that explains the issue, and **Continue to checkout** is unavailable. Resolve the issue, and then try again.

After you accept an offer, that offer’s access start date controls when you can start using the product, and its first invoice date controls when you’re billed the first time.

## View and accept a private offer

The following steps describe the checkout experience for consumers who accept a private offer:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. On the **Shared with you** tab, select the listing that includes the offer, and then open the offer.

   This opens the **Review Private offer** page.
4. Review the offer details, and then select **Continue to checkout**.

   This opens the **Complete your purchase** page, which includes the following sections:

   - **Product details**: Review the provider and listing information.
   - **Pricing details**: Review the total contract value. If Snowflake collects sales tax in your location, this section also shows the estimated tax and the total amount.
   - **Payment schedule**: Review the amount due, due date, and status of each payment.

     The amounts shown in the payment schedule don’t include sales tax.
   - **Payment methods**: Select a payment method.

     You must select a payment method to complete the purchase. You can pay by credit card or be invoiced for the amount due. To add a credit card, select **Add new payment method**.

     If your organization is enrolled in the [Marketplace Capacity Drawdown (MCD)](/collaboration/marketplace-capacity-drawdown) program and the listing supports MCD, this section shows your available MCD balance. To use MCD funds for this purchase, select **Use Marketplace Capacity Drawdown (MCD)**, and then choose how much to apply:

     - **Apply all available MCD**: Apply your available MCD funds to the invoices for this purchase. This is the default option.
     - **Limit MCD for this purchase**: Enter the maximum amount of MCD funds, in US dollars and including tax, to apply to this purchase. Snowflake applies MCD funds to the invoices for this purchase until the total reaches this amount, and bills the rest to your payment method.

       If the offer is a subscription that renews automatically, you can also select **Apply this limit to renewals** to use the same limit for each renewal.

     When you use MCD funds, you must also select a payment method as a backup. To change these MCD settings after the purchase, see [Update MCD allocation for a purchase](#label-consumers-manage-offers-update-mcd-limit).

     Note

     The MCD balance shown can be delayed by up to 2 hours. If you purchase multiple listings in a short amount of time and use MCD funds, this value might not be up to date. Your invoices are generated based on your actual MCD balance.
   - **Billing notifications**: Review who receives the invoices for this purchase:

     - **Marketplace consumer billing contacts**: These contacts receive all Snowflake Marketplace invoices for your organization. To change them, a user with the `ORGADMIN` role updates the billing contacts. For more information, see [Update billing contact information](/user-guide/billing-contacts).
     - **Additional recipients**: To send the invoices for this purchase to other people, select **Add recipients**, enter one or more email addresses separated by commas, and then select **Add recipients**. Additional recipients receive invoices for this purchase only. You can add up to 10 additional recipients.

     To change the additional recipients after the purchase, see [Update invoice email recipients for a purchase](#label-consumers-manage-offers-update-invoice-recipients).
   - **Installation details**: For a listing that creates a database or an application, review the name of the database or application that’s created. To grant access to roles in addition to `ACCOUNTADMIN`, select **Show optional settings**.
   - **Terms of service**: Select that you’ve read the terms of service, privacy policy, and privacy notice.

     You must select all checkboxes to complete the purchase.
   - **PO number**: Optionally, add a purchase order number that identifies this purchase for your records.
   - **Payment summary**: Review the amount due now, including any MCD funds applied, the amount billed to your payment method, and any applicable sales taxes.

     Note

     - Taxes shown at checkout are estimates. The final taxes on your invoice might differ.
     - If your organization has a sales tax exemption on file with Snowflake, the estimated taxes reflect the exemption.
     - Snowflake collects sales tax only for consumers in the U.S. and Canada. In other locations, the provider collects any applicable sales tax directly.

   Note

   For a usage-based offer, the checkout experience differs as follows:

   - **Pricing details**: Shows the usage-based charges, such as a monthly base fee, the price per unit, and charges for billable events, instead of the total contract value. If the plan includes free units each month, this section shows how many.
   - **Billing cadence**: Replaces the payment schedule. Usage-based offers are billed monthly, on the 1st of the month, instead of on a fixed payment schedule.
   - **Payment methods**: If you use MCD funds, Snowflake applies them to your future usage charges, starting with your first monthly invoice. You can’t limit the amount of MCD funds applied to a usage-based purchase.
   - **Billing notifications**: You can’t add additional recipients for an individual usage-based purchase.
   - **Payment summary**: Shows the monthly base fee and estimated taxes, any MCD funds applied, and the amount due today, instead of the total amount due now. If the plan has a spending limit, the summary also shows the most you can be billed each month. You’re billed monthly based on your actual usage, pricing, and applicable taxes until you cancel your subscription.
5. Select **Complete purchase** to purchase a flat-fee listing, or **Start subscription** to start a usage-based subscription.

## View and accept a standard offer

Standard offers are displayed in the pricing section of a listing on Snowflake Marketplace. The following steps describe the checkout experience for consumers who purchase a self-serve standard offer:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace**, and then search for or browse to the listing that you want to purchase.
3. In the pricing section of the listing page, select the standard offer.

   This opens the **Review offer** page.
4. Review the offer details, including the pricing plan, contract duration, and terms of service, and then select **Continue to checkout**.

   This opens the **Complete your purchase** page. The sections on this page match the checkout for a private offer with the same pricing model. For details, see [View and accept a private offer](#label-consumers-manage-offers-private-flat-fee-checkout).
5. Select **Complete purchase** for a flat-fee offer, or **Start subscription** for a usage-based offer.

## Update a paid listing payment method

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. In the right pane, select a paid listing.
4. Select **Manage Purchase**.
5. Select **Update payment method**.
6. Select **Add payment method**, complete the mandatory fields, and then click **Add**.
7. Select **Return to Snowflake Inc. (Snowflake Marketplace)**.

## Update invoice email recipients for a purchase

You can add or remove the additional recipients who receive the invoices for a specific purchase. Additional recipients receive invoices for that purchase only, in addition to your organization’s Marketplace consumer billing contacts. Changes apply to invoices sent after you save the change.

Additional recipients are available for purchases of flat-fee offers, both private and standard. They aren’t available for usage-based offers.

To update the additional recipients for a purchase, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the paid listing.
4. Select **Manage Purchase**.
5. In the **Additional recipients** section, do one or both of the following:

   - To add recipients, select **Add recipients**, enter one or more email addresses separated by commas, and then select **Add**. You can add up to 10 additional recipients.
   - To remove a recipient, select the remove icon next to the email address.

   Snowflake saves each change when you make it.

To change the Marketplace consumer billing contacts that receive all Snowflake Marketplace invoices for your organization, see [Update billing contact information](/user-guide/billing-contacts).

## Update MCD allocation for a purchase

For purchases of flat-fee offers, you can change how much of your [Marketplace Capacity Drawdown (MCD)](/collaboration/marketplace-capacity-drawdown) balance Snowflake applies to the purchase at any time after checkout. Changes apply to invoices that haven’t been generated yet.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **External sharing**.
3. Select the paid listing.
4. Select **Manage Purchase**.
5. Make sure that **Use Marketplace Capacity Drawdown (MCD)** is selected, and then choose one of the following options:

   - **Apply all available MCD**: Apply your available MCD funds to the invoices for this purchase.
   - **Limit MCD for this purchase**: Enter the maximum amount of MCD funds, in US dollars and including tax, to apply to this purchase. If the offer is a subscription that renews automatically, you can also select **Apply this limit to renewals**.

   Snowflake saves your changes when you move to another part of the dialog or close it.

If you lower the limit below the amount of MCD funds already applied to the purchase, Snowflake doesn’t apply any more MCD funds to the purchase.

## View paid listing invoices

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. In the right pane, select a paid listing.
4. Select **Manage Purchase**.
5. Select **View Invoices on Stripe**.
6. Select an invoice in the **INVOICE HISTORY** list.
7. Select **Return to Snowflake Inc. (Snowflake Marketplace)**.

## Add a purchase order to the next generated invoice

Note

You can’t add a purchase order to a historical invoice.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. In the right pane, select a paid listing.
4. Select **Manage Purchase**.
5. Select **Edit** next to **PO Number**.
6. Enter the purchase order number and click **Save**.
7. Select **X (Close)** to close the dialog.

## Cancel a paid listing purchase

When you cancel a paid listing purchase, auto-renewal stops, but the cancellation is not immediate, and you do not receive a refund. To request the cancellation of a paid listing, or request a refund, contact [Snowflake Marketplace Operations](https://snowforce.my.site.com/s/consumer-reporting).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Data sharing** » **Internal sharing**.
3. In the right pane, select a paid listing.
4. Select **Manage Purchase**.
5. Select **Cancel Purchase**.
6. Select **Cancel Purchase** to confirm purchase cancellation.

## Track orders and private offers in Consumer Hub

Consumer Hub is a central place in Snowsight where you can track your Snowflake Marketplace orders and review the private offers that providers send you.

To open Consumer Hub, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), and then in the navigation menu, select **Marketplace** » **Consumer Hub**.

Consumer Hub has the following tabs:

- **Your orders**: Your Snowflake Marketplace orders, including the listing, provider, pricing, payment method, and access start and end dates. To switch between current and previous orders, select **Active orders** or **Past orders**.
- **Private offers**: The private offers that providers have sent you and the status of each offer, such as **Pending**, **Accepted**, **Active**, or **Expired**.
- **Contact sales requests**: The contact sales requests that you’ve submitted to providers.

To find a specific order or offer, search by listing name or provider name.

### View private offer details in Consumer Hub

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Consumer Hub**.
3. Select the **Private offers** tab.
4. Find the offer, and then do one of the following:
   - For a pending offer, select **Review offer**. This opens the offer on the listing page, where you can review and accept the offer.
   - For any other offer, select **View details**. This opens the **Private offer details** panel.

The **Private offer details** panel includes the following sections:

- **Offer details**: The product name, the deadline to accept the offer, and the accounts included in the offer.
- **Billing and payments**: The price, contract type, contract duration, payment options, payment terms, and the date of the first invoice. For accepted offers that you pay for in installments, this section also includes the payment schedule. For more information, see [View the installment payment schedule for a private offer](#label-consumers-manage-offers-consumer-hub-payment-schedule).
- **Access and terms**: The access start date and the terms of service.
- **Attachments**: PDF documents that the provider attached to the offer, such as order forms or master service agreements. To view an attachment, select **Open**. This section appears only if the provider attached documents to the offer.

### View the installment payment schedule for a private offer

When you accept a private offer that you pay for in installments, the **Billing and payments** section of the **Private offer details** panel includes a **Payment schedule**. The payment schedule lists the number, amount, and due date of each installment, so you can see how much you owe for the purchase and when each payment is due.

If the schedule has more than six installments, Consumer Hub shows only the number of installments. To see every installment, select **Show details**. To collapse the schedule, select **Hide details**.

Note

Installment amounts don’t include taxes. If the provider set an installment amount of zero, that installment still appears in the payment schedule.
