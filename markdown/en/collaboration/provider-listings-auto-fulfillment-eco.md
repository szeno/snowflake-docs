# Optimizing data transfer costs with Egress Cost Optimizer

Egress Cost Optimizer (ECO) is a capability of auto-fulfillment that minimizes egress costs when sharing data or apps to multiple regions,
helping providers on Snowflake (of both public and private listings) to reduce costs of sharing and cost of service, and as a result, maximize their return on investment (ROI).

Note

- By default, Egress Cost Optimizer is unavailable to customers using [Virtual Private Snowflake (VPS)](/user-guide/intro-editions#label-snowflake-editions-vps), using [Business Critical Edition](/user-guide/intro-editions#label-snowflake-editions-business-critical), or on a [government cloud](/user-guide/intro-regions#label-us-gov-regions). If you’re a BCE, VPS or Gov customer, you can reach out to your Snowflake account executive for more information about ECO enablement.
- Providers can enable ECO in a primary account in any commercial region and create listings targeted to any other region, including VPS, BCE, and Gov.

## How Egress Cost Optimizer works

Egress Cost Optimizer analyzes your listing configuration in terms of the number
of regions and cloud providers where the listing is available, and delivers the most cost-efficient auto-fulfillment for database replication.
For example, if you’re replicating data to multiple cloud regions and incurring repeated egress costs on the same dataset,
it intelligently routes the data through a Snowflake-managed ECO cache.
In this way, customers end up paying zero additional egress costs to expand to new regions, reducing the data transfer costs.

In another example, if you’re only replicating to 1-2 regions within the same cloud provider, the ECO doesn’t use the ECO cache because your data transfer costs are already optimized.
As a result, by turning on ECO, you’re ensuring minimum data transfer costs under any data sharing scenario.
For more information on costs, benefits, and limits of ECO see [Benefits and costs of egress cost optimization](#label-listing-auto-fulfillment-egress-cost-opt-benefits) and [Limitations of ECO](/collaboration/provider-listings-auto-fulfillment-eco#label-listing-auto-fulfillment-egress-cost-opt-limitations).

Still another example to consider is whether you’re replicating tables rather than an entire database. ECO only uses the cloud cache if the overall costs are getting optimized at the database level. So if you have one table in a database, and that table is being replicated to 10 regions while the database is only getting replicated to a single region, then replication won’t use the cache.

![Without Egress Cost Optimizer: Egress costs compound as data is shared across 30+ regions](/static/images/collaboration/ccauto-wo-eco.png)

Without Egress Cost Optimizer: Egress costs compound as data is shared across 30+ regions.

![With Egress Cost Optimizer: Egress cost is minimized to one-time of moving data into the cloud cache](/static/images/collaboration/ccauto-with-eco.png)

With Egress Cost Optimizer: Egress cost is reduced to a one-time movement of data into the ECO cache.

ECO doesn’t impact existing security, features, and performance commitments of listings,
such as support for data encryption in transit and rest through Snowflake Tri-Secret Secure (TSS), or
existing cross-cloud auto fulfillment features (for example object-level replication, listing refresh cron schedule, and listing refresh history).

You can learn more about the Snowflake supported third-party sub-processors that are leveraged in connection with Cloud Cache by visiting our
[Sub-processor](https://www.snowflake.com/en/legal/privacy/snowflake-sub-processors/) site.

When using ECO, your data will be hosted in the following regions,
in addition to the regions where you make the data available to your consumers:

**North and South America**

| Local region | Local cloud | Local region ID | Snowflake-managed ECO cache region |
| --- | --- | --- | --- |
| Canada (Central) | AWS | `ca-central-1` | Eastern North America |
| South America (Sao Paulo) | AWS | `sa-east-1` | Eastern North America |
| US West (Oregon) | AWS | `us-west-2` | Western North America |
| US East (Ohio) | AWS | `us-east-2` | Eastern North America |
| US East (N. Virginia) | AWS | `us-east-1` | Eastern North America |
| US Central1 (Iowa) | GCP | `us-central1` | Eastern North America |
| US East4 (N. Virginia) | GCP | `us-east4` | Eastern North America |
| Canada Central (Toronto) | Azure | `canadacentral` | Eastern North America |
| Central US (Iowa) | Azure | `centralus` | Eastern North America |
| East US 2 (Virginia) | Azure | `eastus2` | Eastern North America |
| South Central US (Texas) | Azure | `southcentralus` | Eastern North America |
| West US 2 (Washington) | Azure | `westus2` | Western North America |

Expand

Show lessSee more

**Europe and Middle East**

| Local region | Local cloud | Local region ID | Snowflake-managed ECO cache region |
| --- | --- | --- | --- |
| EU (Frankfurt) | AWS | `eu-central-1` | European Union |
| EU (Zurich) | AWS | `eu-central-2` | European Union |
| EU (Stockholm) | AWS | `eu-north-1` | European Union |
| EU (Ireland) | AWS | `eu-west-1` | European Union |
| Europe (London) | AWS | `eu-west-2` | European Union |
| EU (Paris) | AWS | `eu-west-3` | European Union |
| Middle East Central2 (Dammam) | GCP | `me-central2` | European Union |
| Europe West2 (London) | GCP | `europe-west-2` | European Union |
| Europe West3 (Frankfurt) | GCP | `europe-west-3` | European Union |
| Europe West4 (Netherlands) | GCP | `europe-west-4` | European Union |
| North Europe (Ireland) | Azure | `northeurope` | European Union |
| Switzerland North (Zurich) | Azure | `switzerlandnorth` | European Union |
| West Europe (Netherlands) | Azure | `westeurope` | European Union |
| UAE North (Dubai) | Azure | `uaenorth` | European Union |
| UK South (London) | Azure | `uksouth` | European Union |

Expand

Show lessSee more

**Asia Pacific and China**

| Local region | Local cloud | Local region ID | Snowflake-managed ECO cache region |
| --- | --- | --- | --- |
| Asia Pacific (Tokyo) | AWS | `ap-northeast-1` | Asia-Pacific |
| Asia Pacific (Seoul) | AWS | `ap-northeast-2` | Asia-Pacific |
| Asia Pacific (Osaka) | AWS | `ap-northeast-3` | Asia-Pacific |
| Asia Pacific (Mumbai) | AWS | `ap-south-1` | Asia-Pacific |
| Asia Pacific (Singapore) | AWS | `ap-southeast-1` | Asia-Pacific |
| Asia Pacific (Sydney) | AWS | `ap-southeast-2` | Asia-Pacific |
| Asia Pacific (Jakarta) | AWS | `ap-southeast-3` | Asia-Pacific |
| Australia East (New South Wales) | Azure | `australiaeast` | Oceania |
| Central India (Pune) | Azure | `centralindia` | Asia-Pacific |
| Japan East (Tokyo) | Azure | `japaneast` | Asia-Pacific |
| Southeast Asia (Singapore) | Azure | `southeastasia` | Asia-Pacific |

Expand

Show lessSee more

ECO ensures that under any circumstance, you’re only paying cross-cloud egress cost once.
As a result, the more cloud regions that you replicate to, the more the potential egress cost savings.

Note

This feature is only available for Cross-Cloud Auto-Fulfillment and not for manual replication.

## Benefits and costs of egress cost optimization

Egress cost optimization can be used to reduce and control listing auto-fulfillment costs.

Initial costs:
:   The first time data is auto-fulfilled using the egress cost
    optimizer, the data is cached in Snowflake-managed S3-compatible storage with zero-egress costs,
    and you are charged for the initial egress of all the data in each listing to this storage location.
    Thereafter, egress is charged only for data updates.

Incremental data loading vs full data reloading:
:   If you regularly replace tables, or truncate and reload tables,
    be aware that this fresh data will be treated as a new table. Using
    these processes causes those tables to be re-cached, which incurs a
    higher cost than modifying the data by using less resource-intensive methods.

Greater savings with many regions or clouds:
:   Sharing data across more regions increases your savings on total egress costs.
    The more regions where data is shared, the greater the savings with the egress cost optimizer.

Database level, not listing level:
:   Where an auto-fulfillment schedule is set on the account level,
    rather than on the listing level, the egress cost optimizer will be
    enabled on all the listings that follow the account schedule. After the
    cost optimizer is enabled on a database, all subsequent auto-fulfillment
    involving that database will use it.

Cache storage costs:
:   Cache storage costs are incurred only while the listing is active. For example, if you have a listing that’s cached, and you drop that listing after 10 days, you are only charged for 10 days of cache storage.

For more information about pricing for egress between source and target regions or clouds, see the Snowflake [pricing guide](https://www.snowflake.com/resource/the-simple-guide-to-snowflake-pricing/) and the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

# ECO FAQs

When does ECO use the zero-egress cache?
:   ECO uses a heuristic-based algorithm to decide when to use the ECO cache. For example, if you’re replicating to only one or two regions within the same cloud provider, ECO doesn’t use the zero-egress cost cache because your data transfer costs are already optimized. The algorithm calculates the effective data transfer cost at the listing level.

How do I measure changes in data transfer?
:   When your listing uses the ECO cloud cache, the cache updates the `bytesSkipped` parameter in the [LISTING\_REFRESH\_HISTORY](/sql-reference/functions/listing_refresh_history). If you don’t see the cache being used, then your data transfer is already optimized. Please reach out to Snowflake support for any questions.

How much does it cost to use ECO?
:   The cost to use the ECO cache is described in Table 3(d) of the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) (on the Snowflake website). ECO stores the data for 15 days, and you’re charged only for the number of days that the cache is used. For example, you create a listing on Day 1 and enable ECO. The listing uses the cache for cross-cloud replication to target customers. Then you delete the listing on Day 10. In this case, you’re charged for 10 days of ECO cache storage.

# Limitations of ECO

- Incremental data ingestion is required for the cloud cache to be fully used by the egress cost optimizer.
- The cloud cache is only used by the egress cost optimizer for refreshes made by auto-fulfillment.
- Egress cost optimizer will only use the cloud cache if the overall egress costs for all listings on the same database are getting optimized. The optimizer algorithm measures the size of the listings at a database level and not at a table level.
- ECO is not supported for listings that include a [Cortex Knowledge Extension (CKE)](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview).

  Providers should be aware of the cost implications for replication with listings that have a CKE.

  If a CKE is added to a listing that has ECO enabled, ECO will be automatically turned off, and the provider will be notified by email. With ECO turned off, costs associated with the listing can increase.

  Similarly, if a CKE is added to a listing that’s part of a replication group, then ECO will be turned off for all listings within that replication group. An email notification will be sent to the provider indicating that the ECO was turned off.
