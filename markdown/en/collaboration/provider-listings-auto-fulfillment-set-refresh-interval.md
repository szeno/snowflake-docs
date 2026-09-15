# Set the account-level refresh interval

If your data product is an application package that is auto-fulfilled to remote regions, updates to your product occur following a refresh
frequency that you set at the account level.

If you have the ACCOUNTADMIN role, you can change the refresh interval for the account using Snowsight or a SQL command.
When you do this, you update the auto-fulfillment refresh interval for every application package published by your account.
This refresh interval does not affect listings with shares attached.

SnowsightSQL

To set the refresh frequency for your application using Snowsight, you must use the ACCOUNTADMIN role and complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio** » **Listings**.
3. Select the row for the listing that you want to manage.
4. From the listing details page, access the Auto-fulfillment settings:

   1. For a listing offered on the Snowflake Marketplace, in the **Region Availability** section, select **Manage**.
   2. For a listing offered to specific consumers, in the **Consumer Accounts** section, select **…**.
5. Select **Update Refresh Frequency** to update the refresh interval and frequency of your data product.
6. Select a frequency at which to refresh your data product, such as every minute or up to once every 8 days.

   The refresh frequency you select affects all application packages published by your account. You can show
   all listings affected by the refresh frequency change before you make the change.

   You can specify the refresh frequency, but the scheduled time when the refresh occurs in a region is based on the date and time that a
   consumer in that region first requests your data product.
7. Select **Update** to save the updated refresh frequency.

To set the refresh frequency for your application using SQL, you must use the ACCOUNTADMIN role and run the following command:

Copy code

```
ALTER ACCOUNT SET LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE = '<schedule>'
```

Where:

`schedule`:
:   The time interval at which to refresh the data product to other regions. Specify a time period in minutes, including the unit
    `MINUTES`.

For example, to set the Auto-fulfillment refresh frequency for every application package published by your account to every hour,
run the following:

Copy code

```
ALTER ACCOUNT SET LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE = '60 MINUTES'
```

Note

The refresh schedule for a data product in a region is based on the date and time that a consumer in that region first requests your
data product. You can also use cron expressions to set listing schedules. For more information, see [LISTING\_AUTO\_FULFILLMENT\_REPLICATION\_REFRESH\_SCHEDULE](/sql-reference/parameters#label-listing-auto-fulfillment-replication-refresh-schedule).
