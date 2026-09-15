# Understanding data transfer cost

Data transfer is the process of moving data into (ingress) and out of (egress) Snowflake.

Snowflake charges a per-byte fee for data egress when users transfer data from a Snowflake account into a different region on the same
cloud platform or into a completely different cloud platform. Data transfers within the same region are free.

The per-byte rate for transferring data out of a region depends on where your Snowflake account is hosted. For data transfer pricing, see
the [pricing guide](https://www.snowflake.com/pricing/pricing-guide/).

Note

Snowflake does not charge *data ingress* fees. However, a cloud storage provider might charge a data egress fee for transferring
data from the provider to your Snowflake account.

Contact your cloud storage provider (Amazon S3, Google Cloud Storage, or Microsoft Azure) to determine whether they apply data egress
charges to transfer data from their network and region of origin to the cloud provider’s network and region where your Snowflake
account is hosted.

## Snowflake features that incur transfer costs

Snowflake features that transfer data from a Snowflake account into a different region on the same cloud platform or into a completely
different cloud platform incur data transfer costs. For example, the following actions incur data transfer costs:

- [Unloading data](/user-guide/data-unload-overview) - Unloading data from Snowflake to Amazon, Google Cloud Storage, or Microsoft Azure.

  Typically this involves the use of [COPY INTO <location>](/sql-reference/sql/copy-into-location) to unload data to cloud storage in a region or cloud
  platform different from where your Snowflake account is hosted.
  In addition, unloading data typically involves a stage, with its associated costs.
- [Replicating Data](/user-guide/account-replication-intro) - Replication of databases, creating a snapshot of the database to a
  secondary database.

  Typically this involves replicating data to a Snowflake account in a region or cloud platform different from where your primary (origin)
  Snowflake account is hosted. See also [Replication Billing](/user-guide/account-replication-cost).
- [External network access](/developer-guide/external-network-access/external-network-access-overview) - Accessing network locations
  external to Snowflake from procedure or UDF handler code using external access. See also
  [Costs of external network access](/developer-guide/external-network-access/external-network-access-billing).
- [Copy files](/sql-reference/sql/copy-files) - Copy files from a source stage to an output stage. For example, with [Writing files from Snowpark Python UDFs and UDTFs](/developer-guide/snowpark/python/creating-udfs#label-snowpark-python-udf-write-files), you can copy files to an external stage that is on a different region/cloud.
- [Writing external functions](/sql-reference/external-functions) - Use of external functions to transfer data from your Snowflake account to AWS, Microsoft
  Azure, or Google Public cloud. See also [External Functions Billing](/sql-reference/external-functions-introduction#label-external-functions-billing).
- [Cross-Cloud Auto-Fulfillment](/collaboration/provider-understand-cost-auto-fulfillment) -
  Using auto-fulfillment to offer listings to consumers in other cloud regions.
- [FileOperation.put](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.FileOperation.put) - PUT calls to external stages from Snowpark stored procedures.
- [Cross-region/cross-cloud Iceberg writes](/user-guide/tables-iceberg#label-tables-iceberg-cross-cloud-support) - When you [use Snowflake as the catalog](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog),
  writing new data into the Iceberg table incurs costs for data transfer usage if the active storage location is in a different region or
  with another cloud provider. However, data transfers within the same region are free.
- Cross-region/cross-cloud reads from an Iceberg table created with Snowflake Storage - When you create an Iceberg table
  using [Snowflake Storage](/user-guide/tables-iceberg-internal-storage#label-tables-iceberg-internal-storage-data-transfer-cost), reading existing data through the
  Snowflake Horizon Catalog incurs costs for data transfer usage if the client is in a different region or with another cloud provider.

Note

Snowflake does not apply data egress charges when a Snowflake client or driver retrieves query results across regions within
the same cloud platform or across different cloud platforms.

**Next Topic**

> - [Exploring data transfer cost](/user-guide/cost-exploring-data-transfer)
