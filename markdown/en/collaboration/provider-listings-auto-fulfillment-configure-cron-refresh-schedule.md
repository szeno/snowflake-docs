# Configure a cron refresh schedule

If you have the MANAGE LISTING AUTO FULFILLMENT privilege, you can use Snowsight or SQL to configure a [cron](https://en.wikipedia.org/wiki/Cron) refresh schedule for an account or for a database.

## Account-level refresh schedules

If your data product is an application package that is auto-fulfilled to remote regions, updates to your product occur based on a schedule that you set at the account level. This is important for providers who need to offer a predictable timestamp for when refreshes are available to all consumers.

When you create a refresh schedule for an account, you update the auto-fulfillment refresh schedule for every application package published by your account. This refresh schedule doesn’t affect listings with shares attached.

Note

Account-level schedules are used by Snowflake Native Apps. For other shares, the schedule is per database. Listings that use different databases can have different schedules.

## Database-level refresh schedules

If you’re a provider with multiple listings in a database, you can create a refresh schedule for that database. All listings within that database will refresh based on that schedule.

If your listings are in different databases, you can create different schedules for each database.

## Set the refresh schedule for a listing

SnowsightSQL

To set a cron refresh schedule using Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. On the **Listings** tab, select the row for the listing that you want to manage.
4. On the listing details page, scroll down to the **Cloud region availability** section.
   The current refresh schedule is displayed here.
5. Select **Cloud region availability** » **Update refresh frequency**.
6. In the **Data product refresh** menu, select **Scheduled time**.
7. Specify the frequency and time for this schedule; for example, **Daily at 1:00 AM (UTC-7:00) (Local time) Pacific time**.
8. To save the updated refresh schedule, select **Update**.

You can set up cron refresh schedules when you [create](/sql-reference/sql/create-listing) or [alter](/sql-reference/sql/alter-listing) a listing. The cron expression for configuring a cron refresh schedule consists of the following fields:

```
# __________ minute (0-59)
# | ________ hour (0-23)
# | | ______ day of month (1-31, or L)
# | | | ____ month (1-12, JAN-DEC)
# | | | | __ day of week (0-6, SUN-SAT, or L)
# | | | | |
# | | | | |
  * * * * *
```

For more information about using SQL to manage data refreshing for auto-fulfillment, see [auto\_fulfillment](/progaccess/listing-manifest-reference#label-listing-api-manifest-auto-fulfillment).

The following example sets the cron refresh schedule for a listing to occur Monday through Friday at 5:00 p.m. London (UTC) time:

Copy code

```
ALTER LISTING shared_listing
  $$
    auto-fulfillment:
      refresh_schedule: "USING CRON  0 17 * * MON-FRI Europe/London"
      refresh_type: "SUB_DATABASE"
  $$
PUBLISH=TRUE;
```
