# Monitor resources and view costs

This section describes how to monitor auto-fulfillment resources and view estimated and actual costs associated with auto-fulfillment.

## Monitor resources

If you want to minimize costs associated with auto-fulfillment, review the usage of your listings and learn more
about preparing your data for auto-fulfillment:

Monitor Compute Resources
:   Identify the queries run by Snowflake and review the refresh frequency interval for your listings.

    Refer to the [LISTING\_AUTO\_FULFILLMENT\_REFRESH\_DAILY view](/sql-reference/data-sharing-usage/listing-auto-fulfillment-refresh-daily) to identify the listings and databases contributing to compute cost.

    To identify the queries run by Snowflake to support auto-fulfillment, review the **Query History** and filter on
    **Client generated statements**. Refer to the [Query History Page](/user-guide/ui-snowsight-activity#label-snowsight-activity-query-history).

    Review the refresh frequency interval that you set for the listing. Refer to [Set the account-level refresh interval](/collaboration/provider-listings-auto-fulfillment-set-refresh-interval).

Monitor Storage Resources
:   Determine what data to put in your listing and how to structure your data to minimize the amount that needs to be auto-fulfilled.
    Refer to [Prepare data for a listing](/collaboration/provider-listings-preparing).
    Cross-Cloud Auto-Fulfillment does not support secure views that reference data stored in other databases.

    Refer to the [LISTING\_AUTO\_FULFILLMENT\_DATABASE\_STORAGE\_DAILY view](/sql-reference/data-sharing-usage/listing-auto-fulfillment-database-storage-daily) to identify listings and databases contributing to storage cost.

Monitor Data Transfer Resources
:   Identify the regions in which secure share areas have been created. Run the [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) command.

Monitor ECO costs
:   Monitor the ECO costs across your organization. Run the [USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily) in the [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema of the SNOWFLAKE database. In the SERVICE\_TYPE column, review the EGRESS\_COST\_OPTIMIZER value.

## View estimated costs

SQL

To view estimated costs for all secure share areas associated with the provider accounts in your organization, use the
[LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) in the [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema of the SNOWFLAKE database.

To view actual costs for accounts in your organization, use other views in the [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema of the SNOWFLAKE database.

## View actual costs

You can use the [ORGANIZATION\_USAGE](/sql-reference/organization-usage) view or the Snowsight **Usage** dashboard to view costs associated with Cross-Cloud
Auto-Fulfillment and attribute costs associated with fulfilling listings to specific regions. Use the accounts prefixed with
**SNOWFLAKE\_MANAGED$** and **AUTO\_FULFILLMENT\_AREA$** to attribute cost to specific regions.

You must be an account administrator (use the ACCOUNTADMIN role) or use the [ORGANIZATION\_USAGE\_VIEWER](/sql-reference/snowflake-db-roles#label-db-roles-organization-usage-schema) database role to view usage data for Snowflake.

SnowsightSQL

To view actual costs in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**, and then select **Consumption**.
3. Select a warehouse to use to view the usage data.
4. Using the accounts filter, select the accounts titled **SNOWFLAKE\_MANAGED$PUBLIC\_<region\_name>** or **AUTO\_FULFILLMENT\_AREA$-<region\_name>** to filter on the secure share areas used by auto-fulfillment.
   For example, select **SNOWFLAKE\_MANAGED$PUBLIC\_AWS\_EU\_WEST\_2** to view the costs associated with using auto-fulfilling data to the AWS region eu\_west\_2.
5. Use the filters to view all usage types, or focus on compute, storage, or data transfer costs.

To view estimated costs using SQL, you can query the [LISTING\_AUTO\_FULFILLMENT\_USAGE\_HISTORY view](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) in the [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schema. To view actual costs, refer to the other views in the ORGANIZATION\_USAGE schema. For more details on viewing costs, see [Exploring overall cost](/user-guide/cost-exploring-overall).

The costs that you see reflect all listings shared to a particular region by any account in your organization. To identify which listings
are being consumed in which regions and contributing to the costs in a specific region, see [Monitor listing use](/collaboration/provider-listings-monitor-studio).
