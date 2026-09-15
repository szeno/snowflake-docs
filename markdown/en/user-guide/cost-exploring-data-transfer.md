# Exploring data transfer cost

Snowflake does not charge a data ingress fee to bring data into your account, but does charge a per-byte fee to transfer data from a
Snowflake account into another region on the same cloud platform or into a different cloud platform.

This topic describes how to gain insight into historical data transfer costs using [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), or by writing queries against
views in the [ACCOUNT\_USAGE](/sql-reference/account-usage) and [ORGANIZATION\_USAGE](/sql-reference/organization-usage) schemas.
Snowsight allows you to quickly and easily obtain information about cost from a visual dashboard. Queries against the usage views
allow you to drill down into cost data and can help generate custom reports and dashboards.

To gain a better understanding of how data transfer fees accrue, see [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

## Viewing the data transfer history

Users can use Snowsight to view the amount of data transferred from your Snowflake account to
a different cloud provider or region within a specified date range. The unit of measure is bytes.

To explore data transfer costs:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with [access to cost-related features](/user-guide/cost-access-control).
3. In the navigation menu, select **Admin** » **Cost management**.
4. Select a warehouse to use to view the usage data. Snowflake recommends using an XS warehouse for this purpose.
5. Select **Consumption**.
6. Select **Data Transfer** from the Usage Type drop-down.

For usage notes related to the **Consumption** page, see [Usage notes](/user-guide/cost-exploring-overall#label-cost-exploring-consumption-page-notes).

## Querying data for data transfer cost

Snowflake provides two schemas, [ORGANIZATION\_USAGE](/sql-reference/organization-usage) and
[ACCOUNT\_USAGE](/sql-reference/account-usage), that contain data related to usage and cost. The ORGANIZATION\_USAGE schema provides
cost information for all of the accounts in the organization while the ACCOUNT\_USAGE schema provides similar information for a single
account. Views in these schemas provide granular, analytics-ready usage data to build custom reports or dashboards.

Most views in the ORGANIZATION\_USAGE and ACCOUNT\_USAGE schemas contain the cost of data transfers in terms of the volume of data
transferred. To view cost in currency rather than volume, write queries against the
[USAGE\_IN\_CURRENCY\_DAILY view](/sql-reference/organization-usage/usage_in_currency_daily). This view converts the volume of data transferred into cost in currency
using the daily price of transferring a TB.

The following views provide usage and cost information related to transferring data from your Snowflake account to a different cloud
provider or region.

| View | Description | Schema |
| --- | --- | --- |
| DATA\_TRANSFER\_DAILY\_HISTORY | Number of bytes transferred on a given day. For more detailed data, use the DATA\_TRANSFER\_HISTORY view instead. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage/data_transfer_daily_history) |
| DATA\_TRANSFER\_HISTORY | Number of bytes transferred, including the source cloud and region, target cloud and region, and type of transfer. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage/data_transfer_history) [ACCOUNT\_USAGE](/sql-reference/account-usage/data_transfer_history) |
| DATABASE\_REPLICATION\_USAGE\_HISTORY | Number of bytes transferred and credit consumed during database replication. | [ACCOUNT\_USAGE](/sql-reference/account-usage/database_replication_usage_history) |
| LISTING\_AUTO\_FULFILLMENT\_ USAGE\_HISTORY | Estimated usage associated with fulfilling data products to other regions by using Cross-Cloud Auto-Fulfillment. Refer to the SERVICE\_TYPE of DATA\_TRANSFER. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage/listing_auto_fulfillment_usage_history) |
| REPLICATION\_USAGE\_HISTORY | Number of bytes transferred and credits consumed during database replication. If possible, use the [DATABASE\_REPLICATION\_USAGE\_HISTORY view](/sql-reference/account-usage/database_replication_usage_history) instead. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage/replication_usage_history) [ACCOUNT\_USAGE](/sql-reference/account-usage/replication_usage_history) |
| REPLICATION\_GROUP\_USAGE\_HISTORY | Number of bytes transferred and credits consumed during replication for a specific replication group. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage) [ACCOUNT\_USAGE](/sql-reference/account-usage/replication_group_usage_history) |
| USAGE\_IN\_CURRENCY\_DAILY | Daily data transfer in TB along with the cost of that usage in the organization’s currency. | [ORGANIZATION\_USAGE](/sql-reference/organization-usage/usage_in_currency_daily) |

Expand

Show lessSee more

Note

The views and table functions of the [Snowflake Information Schema](/sql-reference/info-schema) also provide usage data related to cost. Though
the ACCOUNT\_USAGE schema is preferred, the Information Schema can be faster in some circumstances.
