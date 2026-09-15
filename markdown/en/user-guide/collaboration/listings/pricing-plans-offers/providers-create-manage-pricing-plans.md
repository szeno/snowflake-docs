# Create and manage pricing plans

## Prerequisites

- A provider profile. See [Set up a provider profile](/collaboration/provider-becoming#label-creating-provider-profile-marketplace).
- A published listing. See [Create a new listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing).
- An account that allows payment for listings. See [Set up Stripe to get paid for listings](/collaboration/provider-becoming#label-set-up-stripe-listings).

## Required privileges

- You must use the ACCOUNTADMIN role or a role that has been granted the provider privileges. See [Privileges required for working with listings](https://other-docs.snowflake.com/collaboration/provider-becoming#label-permissions-required-for-working-with-listings-and-shares).

## Create a pricing plan

Follow the steps below to create a new listing with a pricing plan.

SnowsightSQL

1. Follow the steps for [sharing data on the Snowflake Marketplace](/collaboration/provider-listings-creating-publishing#label-listing-marketplace-create).
2. After you add a data product to your share, in the **Access type** dropdown, select **Paid listing**.

   A **Pricing** section and a **Trial (optional)** section are added to the listing page.
3. In the **Pricing** section, select **Add pricing plans**.

   The **Create pricing plan** page opens.
4. On the **Settings** page, specify a name for the plan, then select **Next**.

   You can optionally specify a product SKU for the pricing plan.
5. On the **Pricing details** page, select a pricing model for the plan:

   - If you select **Flat-fee**, specify the access fee price and the billing frequency (monthly or annually) for the plan.
   - If you select **Usage-based**, specify the monthly access fee, the price per query, and the maximum monthly charge.
6. Select **Next**.
7. Review the pricing plan summary, and then select **Done**.
8. Optional: To add another pricing plan, select **Add pricing plan**, and then repeat the previous steps.
9. Select **Submit for approval** » **Publish once approved** to publish the listing. Only published listings can be offered to consumers.

If you want to create additional pricing plans for a specific listing, select the listing, select the **Pricing plans** tab, and then select **+ Create pricing plan**.

1. Create a [pricing plan manifest reference](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plan-manifest-reference) named PRICING\_PLAN\_1.

   Note

   The pricing plan name must be uppercase.

   Copy code

   ```
   display_name: Default pricing plan display name
   currency: USD
   pricing_model: FLAT_FEE
   base_fee: 100.0
   billing_duration_months: 1
   sales_motion: SELF_SERVE
   comment: Comment for the pricing plan
   metadata:
     description: Pricing plan description
     price: $100 / unit
     button_text: Buy Now
     value_propositions:
    - val 1
    - val 2
     visibility: VISIBLE
     contract_type: LIMITED_TIME
     contract_duration_months: 12
     state: PUBLISHED
   ```
2. Create a [listing manifest reference](/progaccess/listing-manifest-reference) that includes the pricing plan.

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
   pricing_plans:
     - name: PRICING_PLAN_1
    type: FILE
    path: pricingPlans/PRICING_PLAN_1.yaml
   ```
3. Stage the pricing plan and listing manifest reference files.

   Copy code

   ```
   PUT file:///local/path/to/PRICING_PLAN_1.yaml @DB.SCHEMA.STAGE/pricingPlans/PRICING_PLAN_1
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

## Add a pricing plan to a paid listing

The steps below add a pricing plan to an existing listing.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, click the **Listings** tab.
4. Select the paid listing that you want to attach a pricing plan to.

   The **Pricing plans** tab for the listing opens.
5. Click **+ Create pricing plan**.
6. On the **Settings** page, specify a name for the plan, then select **Next**.

   You can optionally specify a product SKU for the pricing plan.
7. Click **Next**.
8. On the **Pricing details** page, select a pricing model for the plan:

   - If you select **Flat-fee**, specify the access fee price and the billing frequency (monthly or annually) for the plan.
   - If you select **Usage-based**, specify the monthly access fee, the price per query, and the maximum monthly charge.
9. Select **Next**.
10. Review the pricing plan summary, and then select **Done**.
11. Optional: To add another pricing plan, select **Add pricing plan**, and then repeat the previous steps.

1. Create a pricing plan manifest reference file and save it as PRICING\_PLAN\_1.yaml.

   Copy code

   ```
   display_name: Default pricing plan display name
   currency: USD
   pricing_model: FLAT_FEE
   base_fee: 100.0
   billing_duration_months: 1
   sales_motion: SELF_SERVE
   comment: Comment for the pricing plan
   metadata:
     description: Pricing plan description
     price: $100 / unit
     button_text: Buy Now
     value_propositions:
    - val 1
    - val 2
     visibility: VISIBLE
     contract_type: LIMITED_TIME
     contract_duration_months: 12
     state: PUBLISHED
   ```
2. Create a live version of your listing and download the listing manifest reference.

   Copy code

   ```
   ALTER LISTING my_listing ADD LIVE VERSION FROM LAST;
   GET snow://listing/my_listing/versions/live/manifest.yml file:///Users/my_username/
   ```
3. Add the pricing plan to the listing manifest reference.

   Note

   The pricing plan name must be uppercase.

   Copy code

   ```
   pricing_plans:
     - name: PRICING_PLAN_1
    type: FILE
    path: pricingPlans/PRICING_PLAN_1.yaml
   ```
4. Upload the pricing plan and listing manifest reference files and commit the change.

   Copy code

   ```
   PUT file:///Users/my_username/PRICING_PLAN_1.yaml snow://listing/my_listing/versions/live/pricingPlans AUTO_COMPRESS = false;

   PUT file:///Users/my_username/manifest.yml snow://listing/my_listing/versions/live AUTO_COMPRESS = false;

   ALTER LISTING my_listing COMMIT;
   ```
5. To see the pricing plan in your listing, run the [SHOW PRICING PLANS](/sql-reference/sql/show-pricing-plans) command.

   Copy code

   ```
   SHOW PRICING PLANS IN LISTING my_listing;
   ```

## Edit a pricing plan

To edit an existing pricing plan, follow the steps below:

Note

It can take up to 10 minutes for pricing plan edits to be visible to consumers.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, select the **Listings** tab.
4. On the **Listings** page, select a paid listing.
5. Select the **Pricing plans** tab.
6. Select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) button for the pricing plan you want to edit, and then select **Edit plan**.
7. Edit the pricing plan, and then click **Done**.

1. Create a live version of your listing and download the pricing plan manifest reference.

   Copy code

   ```
   ALTER LISTING my_listing ADD LIVE VERSION FROM LAST;
   GET snow://listing/my_listing/versions/live/pricingPlans/PRICING_PLAN_1.yml file:///Users/my_username/
   ```
2. Edit the pricing plan manifest reference.
3. Upload the pricing plan and listing manifest reference files and commit the change.

   Copy code

   ```
   PUT file:///Users/my_username/PRICING_PLAN_1.yaml snow://listing/my_listing/versions/live/pricingPlans AUTO_COMPRESS = false;

   ALTER LISTING my_listing COMMIT;
   ```

## View pricing plan details

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the right pane, select the **Listings** tab.
4. On the **Listings** page, select a paid listing.
5. Select the **Pricing** tab.
6. Select **Options** for the pricing plan you want to view, and then select **See details**.
7. Review the pricing plan and click **Edit** to edit the pricing plan, or click **Close**.

To see details of the pricing plan in your listing, run the [SHOW PRICING PLANS](/sql-reference/sql/show-pricing-plans) command.

Copy code

```
SHOW PRICING PLANS IN LISTING my_listing;
```
