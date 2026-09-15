# Compute pool surcharges in Snowflake Native Apps with containers

This preview lets Snowflake Marketplace providers bill based on usage
of compute pools managed by a Snowflake Native App with Snowpark Container Services (SPCS).

Note

Compute pool surcharges apply only to Snowflake Native Apps with Snowpark Container Services. The app must be attached to a paid listing on Snowflake Marketplace.

## About billing for compute pools

If you have a paid listing on Snowflake Marketplace for Snowflake Native Apps with Snowpark Container Services (also called an app with containers), then you can add a surcharge for SPCS compute pool (CP) resources created by the app during setup. During this preview, we support combining SPCS CP surcharges with a base charge *only*.

The Marketplace invoice for a provider is itemized by listing, displaying a total usage-based amount per month. The consumer receives a detailed report on usage-based charges.

The surcharge pricing model is available only if all of the following conditions apply:

- The app must use at least one SPCS container with compute pools.
- The app must automatically create its compute pools during installation.
- The app must automatically request privileges during installation.
- You must be participating in the open preview for Snowflake Native Apps with Snowpark Container Services (introduced June 2024).
  For more information on this preview, see [Add a compute pool to an app with containers](/developer-guide/native-apps/container-compute-pool).
- The app must be available on the Snowflake Marketplace as a paid listing
  before you can configure surcharges.

## Developing a Native App’s compute pools for surcharging

To update your app code so that it correctly creates compute pools for surcharging, refer to the following information:

1. Add the CREATE COMPUTE POOL command to the setup script.
2. Request the CREATE COMPUTE POOL privilege in the manifest file.

To be surcharged, compute pool names must be unique and should describe the purpose, usage, owner role, and/or associated app of the compute pool.

If any compute pools are added after setup (for example, by the consumer), the listing prevents the app from running.

Note

Consumer-created compute pools cannot run an app with containers from a listing.

## How to add a compute pool surcharge using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Navigate to the listing you want to work with, or create a new listing.
4. Add the data product, if it isn’t already attached.
5. To configure pricing, click **Pricing & Trial** » **Add**, located in
   the **Data Product** » **Access & Pricing** section of the screen.
6. If **Usage-based** is not already selected at the top,
   click on it to display the relevant options.
7. To start configuring charges for computing resources, click **+ Compute Pool Surcharge** in
   the **Snowpark Container Services Compute Pool Surcharge** section.

   For each compute pool that you want to display or charge for:

   1. Enter the pre-configured name of the compute pool.
      This name must be the same name as in the app.
   2. Add an amount to bill per credit (in USD). For compute pools that should be displayed
      but have no surcharge, set this amount to $0.
   3. If you have more compute pools to add, click **+ Compute Pool Surcharge** again.
   4. Continue until you have entered all the compute pools you want to display or charge for.
8. (Optional) To set an optional maximum on the charges billed to per month,
   add the amount in **Maximum Monthly Charge** in the **Charging Limit** section.
9. To save your work, click **Save**. To exit without saving, click **Cancel**.

## View pricing selections

Pricing selections are displayed on your view of the listing page. To view them,
select **Preview** on the listing page. To view
pricing selections as they appear to the consumer, on the **Preview** page, select **Buy**.

Note

You should test to ensure that the surcharge is configured properly.

## Reporting

To report on usage, use the following views in the [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage) schema:

- [MARKETPLACE\_PAID\_USAGE\_DAILY View](/collaboration/views/marketplace-paid-usage-daily-ds)
- [MARKETPLACE\_PROVIDER\_SPCS\_USAGE View](/collaboration/views/marketplace-provider-spcs-usage-ds)
- [MONETIZED\_USAGE\_DAILY View](/collaboration/views/monetized-usage-daily-ds)

This preview adds new values to the CHARGE\_TYPE field in the [MARKETPLACE\_PAID\_USAGE\_DAILY View](/collaboration/views/marketplace-paid-usage-daily-ds)
and the [MONETIZED\_USAGE\_DAILY View](/collaboration/views/monetized-usage-daily-ds):

- SPCS\_COMPUTE\_POOL\_SURCHARGE - The amount of the SPCS compute pool surcharge.
- MAX\_SPCS\_COMPUTE\_POOL\_SURCHARGE\_REACHED - No further charge. When the consumer ran additional
  queries, they had already reached the maximum total SPCS compute pool surcharge for this listing.

Copy code

```
SELECT listing_global_name,
   listing_display_name,
   charge_type,
   charge
FROM SNOWFLAKE.DATA_SHARING_USAGE.MARKETPLACE_PAID_USAGE_DAILY
WHERE charge_type='SPCS_COMPUTE_POOL_SURCHARGE';
```

Copy code

```
SELECT
  usage_date,
  listing_display_name,
  consumer_account_name,
  consumer_organization_name,
  charge_type,
  gross_charge
FROM SNOWFLAKE.DATA_SHARING_USAGE.MONETIZED_USAGE_DAILY
WHERE charge_type='SPCS_COMPUTE_POOL_SURCHARGE';
```

## Limitations

- You can combine compute pool surcharges with a base charge, but not with any other
  usage-based pricing model. If you have both a base charge and compute pool surcharges, the base charge won’t be reflected in MONETIZED\_DAILY\_USAGE views or the MARKETPLACE\_DISBURSEMENT\_REPORT views. However, both the base charge and the surcharge appear on the invoice.
- Compute pool surcharges can’t be combined with subscription-based pricing.
- Compute pool surcharges are calculated per day, not per hour.
- Compute pool surcharges are only calculated in US dollars.
- Time-based trials are supported. Other types of trials (usage-based or limited functionality)
  are not supported.

## Frequently asked questions

**How often is usage metered for compute pool surcharges?**

Usage is metered every 5 minutes.
