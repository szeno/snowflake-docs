# Update the refresh frequency

To update the refresh interval and frequency of your data product, do the following:

Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Select the row for the listing that you want to manage.
4. From the listing details page, access the auto-fulfillment settings:

   - For a listing offered on the Snowflake Marketplace, in the **Cloud region availability** section, select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) menu, and then select **Update Refresh Frequency**.
   - For a listing offered to specific consumers, in the **Who can access** section, select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) menu, and then select **Update Refresh Frequency**.
5. In the **Update Refresh Frequency** pane, you can configure a trigger-based, interval-based, or schedule-based refresh. See [How auto-fulfillment refreshes data](/collaboration/provider-listings-auto-fulfillment#label-how-auto-fulfillment-refreshes-data) for details.

> - The refresh interval of an application package must be set at the account level. See [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).
> - The refresh interval for a share is set at the listing level, but you can only specify one schedule for each database. If you have multiple shares attached to multiple listings that contain objects from the same database, updating the refresh interval for one of the listings updates the refresh interval for all other listings that use the same database.

For more details about modifying listings, see [Modify published listings](https://other-docs.snowflake.com/collaboration/provider-listings-modifying).
