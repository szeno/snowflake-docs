# Auto-fulfillment costs

As a provider, you can enable Cross-Cloud Auto-Fulfillment (auto-fulfillment) for a listing to automatically make your data product available in other Snowflake regions.

When you configure auto-fulfillment for your listing, you don’t have to manage
replicating the data. However, you still incur costs associated with transferring and storing your data product in other Snowflake regions
to support consumers of your listing.

Unlike traditional manual database replication, auto-fulfillment doesn’t require a separate account in each region that you
support. Instead, Snowflake creates one secure share area for an organization to manage auto-fulfillment to a region and
associates billing costs with that area. Because of that, the costs associated with auto-fulfillment are
attributed differently when compared to manual
[database replication costs](/user-guide/account-replication-cost).

In addition, egress cost optimization can reduce the costs of auto-fulfillment.
For an introduction to egress cost optimization, see [Optimizing data transfer costs with Egress Cost Optimizer](/collaboration/provider-listings-auto-fulfillment-eco).

## How auto-fulfillment incurs costs

Auto-fulfillment incurs usage costs in the same way that regular usage of Snowflake does:

Compute resources
:   Auto-fulfillment operations use compute resources to copy data and manage the status of the data in the secure share areas in other regions.

    Snowflake Marketplace calculates compute costs for listing auto-fulfillment to VPS regions by using VPS rates. For details on VPS rates, see [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Storage resources
:   Databases transferred to secure share areas in other regions incur storage costs.

Data transfer resources (egress)
:   The initial database auto-fulfillment and the subsequent synchronization operations transfer data between regions.
    Cloud providers charge for data transferred from one region to another within their own network or a region in another cloud.

    The data transfer rate is determined by the location of the source account (i.e. the account that stores the primary database)
    and the destination region and cloud. For data transfer pricing, see the [pricing guide](https://www.snowflake.com/resource/the-simple-guide-to-snowflake-pricing/) (on the Snowflake website).

    For more information about data transfer billing, refer to [Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

    Egress costs can often be reduced by enabling Egress Cost Optimization (ECO). For more information see [Optimizing data transfer costs with Egress Cost Optimizer](/collaboration/provider-listings-auto-fulfillment-eco).

Attribution to secure share area
:   When you use auto-fulfillment, these usage costs are attributed to one Snowflake-managed secure share area for each region that contains active consumers of your listings. For details about attributing costs, see [View actual costs](/collaboration/provider-listings-auto-fulfillment-monitor-view-costs#label-listings-ccaf-costs-view). For details about the components of costs in Snowflake, see [Understanding overall cost](/user-guide/cost-understanding-overall).

## Factors that affect auto-fulfillment costs

When you configure auto-fulfillment for your listing, the following factors can affect the cost of fulfilling your
listing to other regions:

Compute Resource Factors
:   Queries run by Snowflake to fulfill your listing contribute to compute resources.
    The refresh frequency that you set affects how frequently these queries run.

Storage Resource Factors
:   The size of the database, the rate at which data is appended and updated, and the rate of change in the database affect
    how much data is auto-fulfilled and stored initially and continuously.

Data Transfer Resource Factors
:   The cloud region that the listing is auto-fulfilled to, and the cloud provider of that region affect the cost of data transfer.
    The more regions that consumers request your listing in, the higher the cost to fulfill those listings, due to the data transfer cost.
    For data transfer pricing, see the [pricing guide](https://www.snowflake.com/resource/the-simple-guide-to-snowflake-pricing/) (on the Snowflake website).
