# Troubleshooting auto-fulfillment

When you use Cross-Cloud Auto-Fulfillment, either by sharing a listing with a consumer account in another region or by setting up the
region availability of your listing on the Snowflake Marketplace, various checks run to determine whether your data product can be auto-fulfilled.

You can use the sections that follow to troubleshoot common issues with auto-fulfillment. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you encounter an issue not listed here.

Note

Some issues described in these sections appear when a compatibility check runs for your data product when you [Set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-setup-steps). For private listings, the compatibility check only runs if you save your listing as a draft before adding consumer accounts, so you might not see the issues when you first publish a private listing.

## Release directive changes don’t take effect in remote regions

For a listing that contains an application package, a release directive change takes effect in a remote
region only after Cross-Cloud Auto-Fulfillment replicates the application package to that region.
When the application package property `LISTING_AUTO_REFRESH` is `TRUE` (the default), Snowflake initiates
replication whenever a release directive changes, without waiting for the auto-fulfillment schedule.

If `LISTING_AUTO_REFRESH` is `FALSE`, [configure a refresh schedule](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval)
or use [SYSTEM$TRIGGER\_LISTING\_REFRESH](/sql-reference/functions/system_trigger_listing_refresh) to trigger an on-demand refresh after
changing the release directive. For more information about `LISTING_AUTO_REFRESH`, see
[ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package).
