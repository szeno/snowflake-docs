# Paid listings pricing models

For a consumer, the pricing model of a listing depends on what the provider of a listing selects from the options provided by Snowflake.
A provider can attach a single pricing plan to a listing.

This topic outlines the pricing models available for providers to choose for their listings.
You can choose from a usage-based plan or a subscription-based plan:

| Pricing model | Charge components | Billing timing |
| --- | --- | --- |
| [Usage-based](#label-listings-usage-pricing-model) | Providers charge for any combination:   - For billable events - Per query - Monthly fee | Consumers are billed in arrears in months where usage occurs. |
| [Subscription-based](#label-listings-subscription-pricing-model) | Providers charge for a specified term, with optional recurring billing. | Consumers are billed upfront. |

Expand

Show lessSee more

As a provider, you cannot remove a pricing plan from a listing. Any update to a pricing plan for a listing offered publicly on the
Snowflake Marketplace is subject to approval. See [Modify published listings](/collaboration/provider-listings-modifying) for more.

After receiving payment from consumers, Stripe pays providers. If consumers use their Capacity commitment to purchase listings,
Snowflake pays providers.

## Usage-based pricing models

You can add a usage-based pricing plan to your paid listing. The options available to you depend on what you choose to share with
a listing and how you choose to bill.

| Content being shared | Pricing model options |
| --- | --- |
| Application | Usage-based models where providers charge for any combination:   - For billable events - Per query - Monthly fee |
| Data | Usage-based models where providers charge for any combination:   - Per query - Monthly fee |

Expand

Show lessSee more

### Components of usage-based pricing models

Usage-based plans charge consumers on a monthly basis according to their usage of your data product. If you choose a usage-based plan,
you can charge for any combination of the following options:

Billable events:
:   Only listings that share an application can use Custom Event Billing, which charges based on billable events.

    With Custom Event Billing, you can charge a price for specific types of usage of your application. For example, you can charge:

    - Per row of data modified by the application
    - Per procedure call made by the application
    - Per row of data used by the application
    - Per unique row of data updated in a month by your application (monthly active rows)

    You can also charge for other events that you define in your application code.

Per-query charge:
:   Pay a fixed price for each query run that accesses paid data.

    If the pricing model includes a per-month charge, the per-query amount is charged in addition to the per-month charge.

Monthly fee:
:   Pay a fixed price per calendar month in which at least one executed query references a Snowflake Native App, or a paid listing data share. For Snowflake Native App with Snowpark Container Services, a one-time monthly fee is charged when the compute pool runs. Your organization isn’t charged a monthly fee if the Snowflake Native App with Snowpark Container Services compute pool isn’t run, or a query isn’t executed on the Snowflake Native App or the data share within the calendar month.

    A billing cycle is the period of time that starts on the first day of the calendar month and ends on the last day of the month. The per-month price is charged regardless of when during the month the first query was run against paid data. The per-month charge is a fixed price and is not prorated.

For usage-based plans with dynamic charges, such as per-query plans or Custom Event Billing, your pricing plan must include additional
components:

Maximum total charge per month:
:   The maximum total monthly cost that can be charged for a listing as defined by the listing provider. This maximum total charge includes
    all usage-based charges included in the pricing plan for the listing. When this maximum monthly charge is reached, subsequent usage, such
    as queries, is free.

Number of free queries:
:   For pricing plans that include per-query charges, the first query in a calendar month is always charged.
    You can also specify a number of free queries allowed after the first query, and then resume charging a per-query price.

    The first query in each calendar month incurs the per-month charge, the per-query charge, or both, depending on the pricing plan for the listing.

### Configure your listing for custom event billing

After you [create a listing](/collaboration/provider-listings-creating-publishing), you can configure your listing to add a Custom Event Billing
usage-based pricing plan.

#### Add Custom Event Billing to your listing

Note

Before you can add Custom Event Billing to your listing, you must configure your application to emit billable events. You must
know each `class` and corresponding `billing_quantity` used to calculate the `base_charge` in the application to add
Custom Event Billing to your application.
Refer to [Add billable events to an application package](/developer-guide/native-apps/adding-custom-event-billing).

After you [create a listing](/collaboration/provider-listings-creating-publishing), do the following to add a Custom Event Billing pricing plan to your listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, and then select the draft listing you want to configure.
4. In the **Data Product** section, for **Pricing & Trial**, select **Add**.

   If you do not see a **Pricing & Trial** section, you must add your application package to the listing.
5. Select the **Usage-based** pricing plan.
6. (Optional) To charge for billable events and a monthly fee, select **+ Monthly Fee**, and then add a monthly fee
   in US dollars.
7. For **Billable Events**, select **+ Billable Event** to add a new billable event.

   Note

   You are paid only for billable events that you add to your listing, even if additional types of events are emitted by your application.
   The billable event details that you specify in the listing must exactly match the billable events emitted by your application.
8. For each billable event that you add, do the following:

   - Enter a **Class** that exactly matches the `class` defined in the system function for your application.
   - Enter an **Event Display Name** to describe the billable event. For example, **Row Modified**.
   - Enter a **Billing Quantity** to define how much you want to charge for each billable event. For example, **0.01** to charge $1.00
     for 100 modified rows. This value must match the `billing_quantity` variable used to calculate the `base_charge` in your
     application code.
   - Enter a **Unit Name** to describe the units of the billable event being charged for. For example, **row**.
9. If desired, add another billable event. You can charge for up to eight (8) billable events.
10. Enter a **Description** to describe how your application bills consumers. For example, “Charges one cent for each row of data modified
    as a result of actions performed in the application.”
11. Optionally select **+ Per Query Charge** to add charges for each query performed in addition to the charges associated with billable events.
12. If you add per-query charges, add a **Cost per Query** in US dollars.
13. Enter a number of free **Included Queries** for the pricing plan. For example, enter **200** to start
    charging consumers when they run the 202nd query against the application database, because the first query is always charged.
14. For **Charging Limit**, specify a **Maximum Monthly Charge** in US dollars.
15. Select whether to offer a free trial, and if so, select the length of the trial.
    Trials are required for listings offered publicly on the Snowflake Marketplace.
16. Select **Save**.

Before you publish your application to specific consumers or publicly on the Snowflake Marketplace, test your application to make sure the
charges are being made as you expect.
See [Add billable events to an application package](/developer-guide/native-apps/adding-custom-event-billing).

Note

If you share your application with other consumer accounts in your organization and want to charge for their usage,
[contact Snowflake Support](/user-guide/contacting-support). By default, usage within your organization is not billed to allow for testing.

### Configure your listing for a per-query usage plan

After you [create a listing](/collaboration/provider-listings-creating-publishing), you can configure your listing to add a per-query usage-based pricing plan.

With a per-query usage-based plan for your application, you charge a price for each query performed against the shared content.

As with any usage-based plan, you must set a maximum monthly charge for usage to avoid unexpected overages for consumers.

To add a per-query usage-based plan to your listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, and then select the draft listing you want to configure.
4. In the **Data Product** section, for **Pricing & Trial**, select **Add**.

   If you do not see a **Pricing & Trial** section, you must add a data product to the listing.
5. Select the **Usage-based** pricing plan.
6. Optionally select **+ Monthly Fee** to also charge a monthly fee for months in which a consumer uses your listing.
7. For **Queries**, select **+ Per Query Charge**.
8. Add a **Cost per Query** in US dollars.
9. Optionally enter a number of queries included in the pricing plan for free. For example, enter **200** to start
   charging consumers when they run the 202nd query against the application database, because the first query is always charged.
10. For **Charging Limit**, specify a **Maximum Monthly Charge** in US dollars.
11. Select whether to offer a free trial, and if so, select the length and type of the trial.
    Trials are required for listings offered publicly on the Snowflake Marketplace.
12. Select **Save**.

### Configure your listing for a monthly fee usage plan

After you [create a listing](/collaboration/provider-listings-creating-publishing), you can configure it to add a monthly fee usage-based pricing plan.

With a monthly fee usage-based plan, you charge a fixed price for each month in which a consumer
ran a query against a database included in the data product. For listings with applications, you can combine monthly fee usage charges
with Custom Event Billing.

If you want to charge a monthly fee whether or not consumers use your data product, add a subscription-based plan instead.
See [Subscription-based pricing models](#label-listings-subscription-pricing-model).

To add a monthly fee usage-based plan to your listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, and then select the draft listing you want to configure.
4. In the **Data Product** section, for **Pricing & Trial**, select **Add**.

   If you do not see a **Pricing & Trial** section, you must add a data product to the listing.
5. Select the **Usage-based** pricing plan.
6. For **Monthly Fee**, select **+ Monthly Fee**.
7. Enter a **Monthly fee** in US dollars.
8. Select whether to offer a free trial, and if so, select the length and type of the trial.
   Trials are required for listings offered publicly on the Snowflake Marketplace.
9. Select **Save**.

### Usage-based pricing plan examples

The following examples describe possible usage-based pricing plans that a provider might set up for a listing that shares a data product
privately or publicly on the Snowflake Marketplace.

#### Monthly fee only plan

The following diagram shows the costs associated with a pricing plan composed only of a monthly fee charge.

For each month in which users in an account query paid data in the listing, the provider charges only the fixed price of $100 USD.

![Diagram showing different volumes of queries being run in January and February, but the per month charge for each month remains $100.](/static/images/marketplace-consumers-pricing-plan-fixed-only.png)

#### Per-query only plan

The following diagram shows example costs associated with a pricing plan composed only of a per-query charge.

For each month in which users query paid data from a listing, the provider charges a per-query fee of $0.01 USD. The plan includes 1,000 free queries against paid data (after the first query) per billing cycle. This example plan also includes a maximum monthly charge of $200.

In this diagram, the January invoice bills the consumer $20 for a total of 3,000 queries that were run against the listing.

In the February billing cycle, the fixed maximum monthly price of $200 was reached partway through the month. Queries run against the paid
data during the remainder of the billing cycle were free.

![Diagram showing query patterns for the per-query charge listing. The January invoice bills the consumer $20 for a total of 3000 queries that were run against the listing, 1000 of which were free. The February invoice bills the consumer for a total of 21,000 queries, where 1,000 were included in the free queries and 20,000 queries hit the maximum monthly price of $200. The consumer ran additional queries after the monthly maximum was met, but those queries were also free.](/static/images/marketplace-consumers-pricing-plan-usage-only.png)

#### Per-month plus per-query plan

The following diagram shows example costs associated with a pricing plan composed of combined per-month and per-query charges.

For each month in which users in this account query paid data in the listing, the provider charges a fixed price of $100
in addition to a $0.01 fee per query.

This example pricing plan includes 1,000 free queries against paid data (after the first query) per billing cycle.
This example plan also includes a maximum monthly charge of $200.

In this diagram, the January invoice bills the consumer $20 for a total of 3,000 queries that were run against the listing,
as well as the fixed monthly charge of $100.

In the February billing cycle, the fixed maximum monthly price of $200 was reached partway through the month. The consumer paid for
10,000 queries against the data in addition to the $100 fixed monthly charge. An additional 1,000 queries were free as part of the free
monthly queries, and any queries made after the first 11,000 were also free because the maximum charge was reached.

![Diagram showing query patterns for the per-query charge and per-monthly charge listing. The January invoice bills the consumer $120. $100 for the fixed monthly charge, and then $20 for a total of 3000 queries that were run against the listing, 1000 of which were free. The February invoice bills the consumer for a total of 11,000 queries, where 1,000 were included in the free queries and 10,000 queries cost $100. Combined with the $100 fixed monthly charge, the consumer hit the monthly maximum charge of $200. The consumer ran additional queries after the monthly maximum was met, but those queries were also free.](/static/images/marketplace-consumers-pricing-plan-fixed-usage.png)

## Subscription-based pricing models

Choose a subscription-based pricing model to charge an upfront fee for a specified term, with optional recurring billing for your listing.

### Configure your listing for a subscription-based plan

After you [create a listing](/collaboration/provider-listings-creating-publishing), you can configure it to add a subscription-based plan.

For this pricing plan, consumers are charged upfront for access to the data product for a specified term.
You can choose to offer the listing with recurring billing for a subscription that auto-renews, or non-recurring billing for
access for a fixed term.

### Add a recurring subscription-based plan

To add a recurring subscription-based plan to your listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then select the draft listing you want to configure.
4. For the **Data Product** section, for **Pricing & Trial**, select **Add**.

   If you do not see a **Pricing & Trial** section, you must add a data product to the listing.
5. Select **Subscription-based**.
6. For **Billing and access**, select **Recurring** to charge consumers upfront at the beginning of the recurring term.
7. Specify a term from 1–36 months for the **Billing period** for the listing.
8. Specify the total price to be paid upfront, in US dollars.
9. Select whether to offer a free trial, and if so, select the type and length of the trial.
   Trials are required for listings offered publicly on the Snowflake Marketplace.
10. Select **Save**.

### Add a non-recurring subscription-based plan

You can add a non-recurring subscription-based plan to charge consumers once upfront for access to your listing. Listings with this plan
cannot be repurchased by consumers. If you want consumers to be able to repurchase your listing, choose a recurring subscription-based plan.

To add a non-recurring subscription-based plan to your listing, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. Select **Listings**, then select the draft listing you want to configure.
4. For the **Data Product** section, for **Pricing & Trial**, select **Add**.

   If you do not see a **Pricing & Trial** section, you must add a data product to the listing.
5. Select **Subscription-based**.
6. If **Billing and access** is shown, select **One time** to charge consumers once upfront with no option to renew or repurchase the listing.
7. Specify an **Access period** from 1–36 months for the listing.
8. Specify the total price to be paid upfront, in US dollars.
9. Select whether to offer a free trial, and if so, select the type and length of the trial.
   Trials are required for listings offered publicly on the Snowflake Marketplace.
10. Select **Save**.

## Installment plan pricing models

Choose an installment plan pricing model to divide the total price into portions
so the consumer can pay one portion at a time rather than pay the entire amount
in one lump sum.

- Provide consumers the flexibility to make periodic payments by splitting total
  cost into multiple smaller payments.
- Allow providers to define installment payments, including the ability to
  specify larger or smaller payment amounts earlier or later in the
  subscription term. Providers may also define zero value payments, allowing
  consumers to skip payments.

### Configure listings to bill consumers using installments

You must have OWNERSHIP or MODIFY privilege on the listing to configure
installments. For a complete set of privileges for working with listings
see [Privileges required for working with listings](/collaboration/provider-becoming#label-permissions-required-for-working-with-listings-and-shares).

To configure listings for installment payments:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Find and select the listing where you want to configure for installments.
4. In the **Access & Pricing** section, select the pencil icon
   next to **Listing Access**.
5. Select **Subscription-based**.
6. Select **Consumer must pay in installments**.
7. Configure the installment for the listing:

   1. Select **Access period**.
   2. Specify **Total price**.
   3. Select **Installment Type**, one of:
      - **Use equal amounts for all installments**.
      - **Set custom amount per installment**.

        When using a custom amount you can specify multiple payments and amount
        per payment, including zero payments.
8. Select **Save** to save the changes.

### Limitations

Price changes to existing subscription pricing, such as by changing
non-recurring subscriptions to recurring, and/or by adding installments to
an existing plan, is not supported. Instead, make a new listing.

### Grant consumers early access to your listing

Early access:

- Grants consumers access to subscription-based listings without requiring
  upfront payment.
- Allows providers to specify early access and set terms such as NET 30, or
  to specify sharing an invoice directly with the consumer.

Note

The provider is expected to inform the consumer of the desired payment terms.

You must have OWNERSHIP or MODIFY privilege on the listing to configure early
access.

To enable early access:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Find and select the listing that you want to configure for early access.
4. Select **Subscription-based pricing** plan for paid listings.
5. Select **Allow early access** in the
   **Access the listing without payment** section.
6. Select **Save** to save the changes.

Note

Snowflake only recommends early access for paid private listings.

Consumers are able to access the paid listing without payment, even if
they are late or delinquent.
