# Set up auto-fulfillment

This section describes how to set up Cross-Cloud Auto-Fulfillment (auto-fulfillment) for secure share data products and application package data products. It also describes how to set up object-level auto-fulfillment for a listing.

You must add a data product to your listing before you can set up auto-fulfillment. Also, the steps to set up auto-fulfillment differ depending on the data product you offer and how you make your listing available.

## Set up auto-fulfillment for a secure share data product shared on the Snowflake Marketplace

If your data product is a secure share that you publish to the Snowflake Marketplace using a listing, use the following steps to
set up auto-fulfillment:

Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Select the listing for which you want to set up auto-fulfillment.
4. Select **Region Availability** » **Edit**.
5. For **Region availability**, choose your desired availability.

   - By default, **All regions** is selected. This ensures the availability of your listing in any future regions added by Snowflake.
   - If your listing has specific regional limitations, change the region availability to **Custom regions** and select the regions in which you want to offer your data product. When you choose custom regions, your listing is visible in all current Snowflake Marketplace regions, but consumers can only get your data product in the regions you specify. Your listing will not be available in any new regions automatically.
   - For paid listings, **Custom regions** is selected by default. Paid listings are only available in [supported regions](https://other-docs.snowflake.com/en/collaboration/consumer-listings-paying#label-monetization-consumer-region-support) and any future supported regions added by Snowflake.
6. For **Fulfillment method**, **Automatic** fulfillment is the default selection. With Cross-Cloud Auto-Fulfillment, your data product is automatically fulfilled to a region and you incur costs only when there is consumer demand in that region.
   If you can’t use auto-fulfillment and the option is available, select **Manual** to manually replicate your data product. See [Manually replicate data to fulfill a listing request](https://other-docs.snowflake.com/en/collaboration/provider-listings-managing#label-manually-replicate-listing).
7. If you select **Automatic** for auto-fulfillment:

   1. Select a refresh interval from the drop-down list, then enter a value. You must select a refresh interval of at least 8 days.
   2. If you don’t have a default warehouse set, select a warehouse to use for auto-fulfillment.
   3. When you add a data product to your listing, Snowflake performs a compatibility check to validate that your data product can be auto-fulfilled to other regions. If the check returns any incompatibilities, you might need to update your data product. See [Troubleshooting auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-troubleshooting).
   4. Select **Save and Enable Fulfillment**.

      Auto-fulfillment for the listing is now enabled, but the data product attached to the listing is not fulfilled to any regions
      until the listing is published and a consumer requests the data product. See [How auto-fulfillment works](/collaboration/provider-listings-auto-fulfillment#label-how-auto-fulfillment-works).
8. If you chose to manually fulfill the listing, select **Save**. Before publishing the listing, you must replicate data to each of the available regions you select. See [Manually replicate data to fulfill a listing request](https://other-docs.snowflake.com/en/collaboration/provider-listings-managing#label-manually-replicate-listing).

## Set up auto-fulfillment for an application package data product shared on the Snowflake Marketplace

If your data product is an application package that you publish to the Snowflake Marketplace with a listing, use the following steps to
set up auto-fulfillment:

Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Select the listing for which you want to set up auto-fulfillment.
4. Select **Region Availability** » **Edit**.
5. For **Region availability**, choose your desired availability.

   - By default, **All regions** is selected. Choosing all regions ensures the availability of your listing in any future regions added by Snowflake.
   - If your listing has specific regional limitations, change the region availability to **Custom regions** and select the regions in which you want to offer your data product. When you choose custom regions, your listing is visible in all current Snowflake Marketplace regions, but consumers can only get your data product in the regions you specify. Your listing will also not become automatically available in any new regions.
   - For paid listings, **Custom regions** is selected by default. Paid listings are only available in [supported regions](https://other-docs.snowflake.com/en/collaboration/consumer-listings-paying#label-monetization-consumer-region-support) and any future supported regions added by Snowflake.
6. Review the refresh interval configured at the account level. If you need to use a different refresh interval, see [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).
7. If you don’t have a default warehouse set, select a warehouse to use for auto-fulfillment.
8. Select **Save and Enable Fulfillment**.

   Auto-fulfillment for the listing is now enabled, but the data product attached to the listing is not fulfilled to any regions until the listing is published and a consumer requests the data product. See [How auto-fulfillment works](/collaboration/provider-listings-auto-fulfillment#label-how-auto-fulfillment-works).

## Set up object-level auto-fulfillment

You can configure auto-fulfillment to automatically transfer the data product associated with your listing to other Snowflake regions. You also can use SUB\_DATABASE auto-fulfillment and choose to fulfill only the tables and views in a data product to a remote region using auto-fulfillment. This can help reduce costs and ease the manageability burden of your auto-fulfilled data product.

The steps below describe how to set up object-level auto-fulfillment for a listing. As part of a typical workflow, you set up object-level auto-fulfillment when you set up the region availability (for a listing published on the Snowflake Marketplace) or when you add a consumer located in another region (for a listing shared privately).

Snowsight

1. Create a listing. See [Create a new listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing).
2. Add a data product that contains only supported objects.
3. Set up regions or accounts to share with to start setting up auto-fulfillment:

   For a listing published to the Snowflake Marketplace:

   1. Locate the **Region Availability** section and select **Add**.
   2. For **Region availability**, keep the default of **All regions** or select **Custom regions** for your listing.

   For a listing shared privately, add a consumer account in a remote region.
4. Select your preferred refresh interval for updating the data product in remote regions.
5. Publish your listing or save it as a draft.

## Set up auto-fulfillment for a listing that spans databases

Providers can create a single listing that spans databases, eliminating the need to create one combined database per listing. In this case, all listings associated with a database are auto-fulfilled together.

### Workflow

1. A provider has a database (main database) that they want to share. They also have views in that database that reference objects in another database (referenced database).
2. The provider creates a share in the main database.
3. Using [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share), the provider grants the following required privileges to the share:

   1. The provider grants the USAGE privilege on the main database that contains the view to the share.
   2. The provider grants the REFERENCE\_USAGE privilege on the referenced database to the share.

      Note

      Setting the auto-fulfillment refresh type to `FULL_DATABASE` is deprecated and isn’t supported for reference usage grants.
   3. The provider grants the USAGE privilege on the schema that contains the view to the share.
   4. The provider grants the SELECT privilege on the view to the share.![Diagram showing the privileges granted to a share for a listing that spans databases](/static/images/laf-listings-span-dbs-privileges.png)
4. The provider creates a listing with the share and enables [auto-fulfillment](/collaboration/provider-listings-auto-fulfillment) for cross-region cross-cloud consumers.

For more information, see [Share data from multiple databases](/user-guide/data-sharing-multiple-db).

### Supported reference types

When REFERENCE\_USAGE is granted on a database to a share, the following reference types are supported:

- A view referencing a table or view in another database.
- Tables or views with policies when these policies are stored in another database.
- Tables or views with tags when these tags are stored in another database.

  Note

  A tag without an attached policy in a different database will only be replicated if reference usage is granted. Otherwise, replication will be skipped. See [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) for more information. If the tag is used in tag-based masking, then the share is treated as a table or view with row-access policies.

### Limitations

- Snowflake groups listings together when refreshing the data. Setting up listings that span multiple databases can change the way listings are grouped. As a result, the following might be affected:

  - The listing refresh history can be missing or incorrect after update the auto-fulfillment schedule.
  - Setting the *refresh\_schedule\_override* option may be required. When this option is missing, a resulting error message will include the list of listings that were affected by the change in the order that the listings were grouped.
- Setting the auto-fulfillment refresh type to `FULL_DATABASE` is deprecated and isn’t supported for reference usage grants.

### Usage notes

When setting up auto-fulfillment, if the selected and referenced databases include existing listings, then the values in the **Data product refresh** section default to the existing refresh schedule. As a result, changes to the auto-fulfillment refresh schedule apply to all other listings associated with this database and with the referenced database.

### Examples

For examples on how to create a secure view that references objects and other views in one or more databases, see the [Share data from multiple databases examples](/user-guide/data-sharing-multiple-db#label-share-multi-db-examples).

After you create a secure view, you can create a listing that includes the secure view and [set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-setup-steps) on the listing. For examples on how to create listings on the Snowflake Marketplace, see [Create and publish a listing](https://other-docs.snowflake.com/en/collaboration/provider-listings-creating-publishing).
