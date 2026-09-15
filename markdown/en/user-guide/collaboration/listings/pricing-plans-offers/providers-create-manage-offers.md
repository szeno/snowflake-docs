# Create and manage offers

Providers can create both standard and private offers.

- Standard offers are displayed in the pricing section of a listing. With standard offers, providers can allow self-serve purchases or send consumers to their sales team using a **Contact sales** option.
- Private offers are only visible to targeted consumers. With private offers, providers can offer custom discounts and terms.

## Prerequisites

- A provider profile. For more information, see [Set up a provider profile](/collaboration/provider-becoming#label-creating-provider-profile-marketplace).
- A published listing. For more information, see [Create a new listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing).
- An account that allows payment for listings. For more information, see [Set up Stripe to get paid for listings](/collaboration/provider-becoming#label-set-up-stripe-listings).

## Required privileges

- You must use the ACCOUNTADMIN role or a role that has been granted the provider privileges. For more information, see [Privileges required for working with listings](/collaboration/provider-becoming#label-permissions-required-for-working-with-listings-and-shares).

## Working with offers

The **Offers** tab shows a list of both standard and private offers that are available for a listing.

The following details are available for Standard offers:

> - Offer name
> - Status (Draft, Active, Retired)
> - Type (Self-serve or Sales-led)
> - Last updated date
> - Display order

The following details are available for Private offers:

- Offer name
- Status (Draft, Active, Withdrawn, Expired)
- Expiration date
- Target consumer
- Pricing plan terms
- Last updated date

Each row in an **Offers** table includes an action button [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) that you can select to view additional options for managing the offer.

Standard offers provide the following actions:

- View details
- Edit offer
- Display order (not available for **Retired** or **Draft** offers)
- Retire offer (not available for **Retired** or **Draft** offers)

Private offers provide the following actions:

- Copy offer URL
- View details
- Edit offer (not available for **Active** offers)
- Withdraw offer (not available for **Expired** offers)

## Limitations

When providers include a discount in an offer, the discount isn’t automatically applied to the [SYSTEM$CREATE\_BILLING\_EVENT](/sql-reference/functions/system_create_billing_event) charges.

1. To apply the discount, store the discounted price in your app.

   You can also run the [SHOW OFFERS](/sql-reference/sql/show-offers) command to retrieve the discount amount that’s included in an offer.
2. After retrieving the discount, emit the final dollar amount in the [SYSTEM$CREATE\_BILLING\_EVENT](/sql-reference/functions/system_create_billing_event) call.

   Do not send the undiscounted price.

For more information about creating billing events, see [Billable event examples](/developer-guide/native-apps/adding-custom-event-billing#label-native-apps-custom-billing-examples).

## Create a standard offer

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. On the **Offers** tab, **Standard offers** is selected by default. Click **+ Create offer**.
6. In the **Offer details** dialog, specify details for the offer.

   1. Select **Standard offer**.
   2. Select the **Purchase type**:

      - Select **Self-serve** to allow consumers to see the price and purchase the listing directly.
      - Select **Sales-led** to require consumers to contact you to purchase the listing.
   3. Specify a name for the offer.
   4. Select **Next**.
7. In the **Billing and payments** dialog, select a pricing plan to attach to this offer.
8. (Optional) Specify whether to require consumers to include a credit card on file to purchase the listing.
9. Select **Next**.
10. In the **Description** dialog, enter information about the offer that users will see.
11. Specify an offer name to display to consumers.
12. Specify the price to display to consumers.
13. (Optional) Specify a tagline to display to consumers.
14. Specify the text for the button that consumers click to purchase the listing.
15. (Optional) Specify any value propositions for the offer.
16. Select **Next**.
17. Review the offer summary, then click **Create offer**.

1. Create an [offer manifest reference](/user-guide/collaboration/listings/pricing-plans-offers/offer-manifest-reference) named PRICING\_PLAN\_1\_DEFAULT\_OFFER.

   Note

   The offer name must be uppercase.

   Copy code

   ```
   access_start_date_preference: SPECIFIC_DATE
   comment: An internal note
   contract_value: 120.12
   contract_type: LIMITED_TIME
   contract_duration_months: 12
   discount: 0.0
   invoice_start_date_preference: SPECIFIC_DATE
   invoice_start_time: 1731102884579
   is_default: false
   display_name: Display name of the offer
   expiration_time: 1762638884579
   payment_terms:
     payment_type: FULL
   pricing_plan_name: PRICING_PLAN_1
   access_end_time: 1762638884579
   access_start_time: 1731102884579
   state: PUBLISHED
   terms_of_service:
     type: DEFAULT
   ```
2. Create a [listing manifest reference](/progaccess/listing-manifest-reference) that includes the offer.

   Copy code

   ```
   title: my_listing
   subtitle: Subtitle for my_listing
   description: Description for my_listing
   listing_terms:
     type: OFFLINE
   targets:
     regions: PUBLIC.AWS_US_EAST_1
   usage_examples:
     - title: this is a test sql
    description: Simple example
    query: select *
   offers:
     - name: PRICING_PLAN_1_DEFAULT_OFFER
    type: FILE
    path: offers/PRICING_PLAN_1_DEFAULT_OFFER.yaml
   ```
3. Stage the offer and listing manifest reference files.

   Copy code

   ```
   PUT file:///local/path/to/PRICING_PLAN_1_DEFAULT_OFFER.yaml @DB.SCHEMA.STAGE/offers/PRICING_PLAN_1_DEFAULT_OFFER
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

   PUT file:///local/path/to/manifest.yaml @DB.SCHEMA.STAGE/listings/my_manifest
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```
4. Create a listing that uses the manifest files uploaded to the stage.

   Copy code

   ```
   CREATE EXTERNAL LISTING my_listing
     FROM @DB.SCHEMA.STAGE/listings/my_manifest
     REVIEW = TRUE
     PUBLISH = FALSE;
   ```

## Create a private offer based on a pricing plan

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. On the **Offers** tab, select **Private offers**, then click **+ Create offer**.
6. In the **Create private offer** pane, perform the following steps to create a private offer:
   1. On the **Offer details** page, enter the following information:

      1. Select **Private offer** as the offer type.
      2. Specify the [data sharing account identifier](/user-guide/admin-account-identifier) for the consumer that will receive this offer.
      3. Specify a name and expiration date for the offer.
      4. Select **Next**.
      5. On the **Billing and payments** page, select an existing pricing plan and enter the following information.
      6. Review the negotiated price details in the **Plan components** table.

         Optional: Hover on a row in the **Plan components** table and select the **Edit** icon to modify the component details.

         - For usage-based plans, you can edit the monthly access fee or apply a discount. You can also edit the price per query and the monthly limit.
         - For flat-fee plans, you can edit the access fee price or apply a discount percentage.
      7. Specify the contract type:

         - **Limited-time**: This grants access for a fixed period of time, such as 30 days. Consumers can be charged upfront or in installments.
         - **Recurring (Subscription)**: This grants continuous access. Consumers are billed at the chosen frequency for the contract duration, and the subscription auto-renews until the consumer [cancels](/user-guide/collaboration/listings/pricing-plans-offers/consumers-manage-offers#label-pricing-plans-offers-consumer-cancel-purchase) the purchase.

         Note

         You can’t specify a contract type for usage-based pricing plans.
      > 1. Enter a contract duration to indicate the length of time that the offer is valid for.
      >
      >    For flat-fee plans, specifying a contract duration will auto-fill the total contract value based on the pricing plan details.
      > 2. Specify payment options for the offer:
      >
      >    - **Require full payment upfront**: The consumer pays the total contract value (TCV) at the start of the contract.
      >    - **Accept installments**: Allow the consumer to pay in equal monthly installments or specify custom installment amounts.
      >
      >      If you select the **Accept installments** option, you can specify the number of installments and the installment amount.
      >
      >    Note
      >
      >    You can’t specify payment options for usage-based pricing plans.
      > 3. Specify the first invoice date.
      >
      >    The first invoice date is the date when the consumer will be billed for the first time.
      > 4. Select whether to require a credit card to be on file.
      > 5. Select **Next**.
   2. On the **Access and terms** page, specify the access start date and the terms of service for the offer.

      The access start date is the date when the consumer can start using the product. You can set this to **When offer accepted** to allow the consumer to start using the product immediately after accepting the offer, or you can configure a specific start date.
   3. On the **Attachments** page, optionally upload PDF files to include with the offer. For example:

      - Order Form
      - MSA or Terms of Service

      Each offer supports up to 5 PDF attachments, with a maximum size of 5 MB per file. The total size of all attachments across all offers in a listing cannot exceed 50 MB.
   4. Select **Next**.
   5. On the **Summary** page, review the offer details, and then select **Done**.

Upon completion, the offer appears on the **Private offers** tab. The initial status will show **Active**, indicating that the offer is ready to be accepted by the consumer. The consumer can either accept or reject the offer, and the status will be updated accordingly.

1. Create an [offer manifest reference](/user-guide/collaboration/listings/pricing-plans-offers/offer-manifest-reference) named PRIVATE\_OFFER\_PRICING\_PLAN.

   Note

   The offer name must be uppercase.

   Copy code

   ```
   version: V2
   access_start_date_preference: SPECIFIC_DATE
   comment: Private offer for specific consumer
   contract_type: LIMITED_TIME
   contract_duration_months: 12
   discount: 10.0
   invoice_start_date_preference: SPECIFIC_DATE
   invoice_start_time: 1731102884579
   is_default: false
   display_name: Private Offer Display Name
   expiration_time: 1762638884579
   payment_terms:
     payment_type: FULL
   pricing_plan_details:
     type: DEFAULT
     name: PRICING_PLAN_1
   access_end_time: 1762638884579
   access_start_time: 1731102884579
   state: PUBLISHED
   target_consumer: ORGANIZATION_NAME.ACCOUNT_NAME
   terms_of_service:
     type: DEFAULT
   attachments:
     - attachment_path: offers/PRIVATE_OFFER_PRICING_PLAN/attachments/terms_supplement.pdf
   ```
2. Create a [listing manifest reference](/progaccess/listing-manifest-reference) that includes the private offer.

   Copy code

   ```
   title: my_listing
   subtitle: Subtitle for my_listing
   description: Description for my_listing
   listing_terms:
     type: OFFLINE
   targets:
     regions: PUBLIC.AWS_US_EAST_1
   usage_examples:
     - title: this is a test sql
    description: Simple example
    query: select *
   offers:
     - name: PRIVATE_OFFER_PRICING_PLAN
    type: FILE
    path: offers/PRIVATE_OFFER_PRICING_PLAN.yaml
   ```
3. Stage the offer and listing manifest reference files.

   Copy code

   ```
   PUT file:///local/path/to/PRIVATE_OFFER_PRICING_PLAN.yaml @DB.SCHEMA.STAGE/offers/PRIVATE_OFFER_PRICING_PLAN
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

   PUT file:///local/path/to/manifest.yaml @DB.SCHEMA.STAGE/listings/my_manifest
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```
4. Create a listing that uses the manifest files uploaded to the stage.

   Copy code

   ```
   CREATE EXTERNAL LISTING my_listing
     FROM @DB.SCHEMA.STAGE/listings/my_manifest
     REVIEW = TRUE
     PUBLISH = FALSE;
   ```

## Create a one-time pricing offer

One-time pricing plans allow providers to create a private offer that isn’t tied to a pricing plan. When you extend a one-time pricing offer to a consumer, the consumer is charged a single, upfront fee for access to the data product for a specified duration.

The steps below describe how to create a one-time pricing offer.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. On the **Offers** tab, select **Private offers**, then click **+ Create offer**.
6. In the **Create private offer** pane, run the following steps to create a private offer:
   1. On the **Offer details** page, enter the following information:

      1. Select **Private offer** as the offer type.
      2. Specify the [data sharing account identifier](/user-guide/admin-account-identifier) for the consumer that will receive this offer.
      3. Specify a name and expiration date for the offer.
      4. Select **Next**.
      5. On the **Billing and payments** page, select **Apply one-time pricing** and enter the following information.
      6. Specify the total contract value.
      7. Specify the contract type:

         - **Limited-time**: This grants access for a fixed period of time, such as 30 days. Consumers can be charged upfront or in installments.
         - **Recurring (Subscription)**: This grants continuous access. Consumers are billed at the chosen frequency for the contract duration, and the subscription auto-renews until the consumer [cancels](/user-guide/collaboration/listings/pricing-plans-offers/consumers-manage-offers#label-pricing-plans-offers-consumer-cancel-purchase) the purchase.
      8. Enter a contract duration to indicate the length of time that the offer is valid for.
      9. Specify payment options for the offer:

         - **Require full payment upfront**: The consumer pays the total contract value (TCV) at the start of the contract.
         - **Accept installments**: Allow the consumer to pay in equal monthly installments or specify custom installment amounts.

           If you select the **Accept installments** option, you can specify the number of installments and the installment amount.
      10. Specify the first invoice date.

      The first invoice date is the date when the consumer will be billed for the first time.

      11. Select whether to require a credit card to be on file.
      12. Select **Next**.
   2. On the **Access and terms** page, specify the access start date and the terms of service for the offer.

      The access start date is the date when the consumer can start using the product. You can set this to **When offer accepted** to allow the consumer to start using the product immediately after accepting the offer, or you can configure a specific start date.
   3. Select **Next**.
   4. On the **Summary** page, review the offer details, and then select **Done**.

1. Create an [offer manifest reference](/user-guide/collaboration/listings/pricing-plans-offers/offer-manifest-reference) named ONE\_TIME\_PRICING\_OFFER.

   Note

   The offer name must be uppercase.

   Copy code

   ```
   version: V2
   access_start_date_preference: SPECIFIC_DATE
   comment: One-time pricing offer for specific consumer
   contract_type: LIMITED_TIME
   contract_duration_months: 12
   contract_value: 5000.00
   invoice_start_date_preference: SPECIFIC_DATE
   invoice_start_time: 1731102884579
   is_default: false
   display_name: One-Time Pricing Offer
   expiration_time: 1762638884579
   payment_terms:
     payment_type: FULL
   access_end_time: 1762638884579
   access_start_time: 1731102884579
   state: PUBLISHED
   target_consumer: ORGANIZATION_NAME.ACCOUNT_NAME
   terms_of_service:
     type: DEFAULT
   ```
2. Create a [listing manifest reference](/progaccess/listing-manifest-reference) that includes the one-time pricing offer.

   Copy code

   ```
   title: my_listing
   subtitle: Subtitle for my_listing
   description: Description for my_listing
   listing_terms:
     type: OFFLINE
   targets:
     regions: PUBLIC.AWS_US_EAST_1
   usage_examples:
     - title: this is a test sql
    description: Simple example
    query: select *
   offers:
     - name: ONE_TIME_PRICING_OFFER
    type: FILE
    path: offers/ONE_TIME_PRICING_OFFER.yaml
   ```
3. Stage the offer and listing manifest reference files.

   Copy code

   ```
   PUT file:///local/path/to/ONE_TIME_PRICING_OFFER.yaml @DB.SCHEMA.STAGE/offers/ONE_TIME_PRICING_OFFER
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

   PUT file:///local/path/to/manifest.yaml @DB.SCHEMA.STAGE/listings/my_manifest
     SOURCE_COMPRESSION=NONE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```
4. Create a listing that uses the manifest files uploaded to the stage.

   Copy code

   ```
   CREATE EXTERNAL LISTING my_listing
     FROM @DB.SCHEMA.STAGE/listings/my_manifest
     REVIEW = TRUE
     PUBLISH = FALSE;
   ```

## Edit a standard offer

The steps below describe how to edit a standard offer.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. On the **Offers** tab, select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the standard offer you want to edit, and then select **Edit
   offer**.

1. Create a live version of your listing and download the offer manifest reference.

   Copy code

   ```
   ALTER LISTING my_listing ADD LIVE VERSION FROM LAST;
   GET snow://listing/my_listing/versions/live/offers/STANDARD_OFFER.yml file:///Users/my_username/
   ```
2. Edit the offer manifest reference.
3. Upload the offer and listing manifest reference files and commit the change.

   Copy code

   ```
   PUT file:///Users/my_username/STANDARD_OFFER.yaml snow://listing/my_listing/versions/live/offers AUTO_COMPRESS = false;

   ALTER LISTING my_listing COMMIT;
   ```

## Edit a private offer

The steps below describe how to edit a private offer. Only private offers that have the following status can be edited:

- DRAFT
- EXPIRED
- WITHDRAWN

Note

It can take up to 10 minutes for the edits to private offers to be visible to consumers.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. On the **Offers** tab, select **Private offers**, then select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the private offer you want to edit, and then select **Edit**.
6. Edit the private offer, and then click **Edit offer**.

1. Create a live version of your listing and download the offer manifest reference.
2. Edit the offer manifest reference.
3. Upload the offer and listing manifest reference files and commit the change.

   Copy code

   ```
   PUT file:///Users/my_username/PRIVATE_OFFER.yaml snow://listing/my_listing/versions/live/offers AUTO_COMPRESS = false;

   ALTER LISTING my_listing COMMIT;
   ```

## View offer details

You can view details of both standard and private offers.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. Click the **Private Offers** tab.
6. Click the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the offer you want to view and then select **View details**.
7. Review the offer and click **Close** to return to the offers list.

To see details of an offer in your listing, run the [SHOW OFFERS](/sql-reference/sql/show-offers) command.

> Copy code
>
> ```
> SHOW OFFERS IN LISTING my_listing;
> ```

## Retire a standard offer

Retiring an active standard offer makes it unavailable for new purchases. Existing consumers who have already purchased the offer can continue to use it until their contract expires.

Note

This action can’t be undone.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. Click the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the standard offer you want to retire and then select **Retire offer**.
6. A confirmation dialog appears. Click **Retire offer** to confirm.

## Copy a private offer URL

Copy a private offer URL and provide it to consumers so they can review and accept or decline it.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. Click the **Private Offers** tab.
6. Click the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the private offer you want to view and then select **Copy URL**.

## Withdraw a private offer

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select a paid listing in the list.
5. Click the **Private Offers** tab.
6. Click the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the private offer you want to withdraw and then select **Withdraw**.
7. Click **Withdraw offer**.
