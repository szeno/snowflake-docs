# Manage regions and replication

To manage or monitor additional auto-fulfillment settings for your listing, do the following:

Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Select the row for the listing that you want to manage.
4. From the listing details page, access the auto-fulfillment settings:

   1. For a listing offered on the Snowflake Marketplace, in the **Region Availability** section, select **Manage**.
   2. For a listing offered to specific consumers, in the **Consumer Accounts** section, select **…**.
5. Select **Manage Regions & Replication** to see the regions where the listing is fulfilled and the status of auto-fulfillment. You can add or remove availability for a particular region or check the status. Select a region to see the timestamp of the last sync and how many consumers are accessing the data.

   - If no consumers have accessed your listing’s product in a region, you can select **Remove Region**.
   - If a consumer has accessed your listing’s product in a region, you cannot remove the region. Instead, if you want to remove your data product from that region, all consumers using the product must drop the database or application first, or you must delete the listing.

For more details about modifying listings, see [Modify published listings](https://other-docs.snowflake.com/collaboration/provider-listings-modifying).
