# Snowpark Container Services: Understanding instance families

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## Available Instance Families

An instance family specifies the vCPU, memory, storage, and egress bandwidth
available to nodes in a compute pool. The available instance families vary by
cloud provider. Within each cloud provider, instance families are grouped as
current generation or previous generation. To view the instance
families available in your account and region, use
[SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families).

If you configure backup instance families for a compute pool, choose a backup that is
workload-compatible with the primary: generally a larger size of the same instance
family. On Google Cloud, GEN\_X64\_G1 and CPU\_X64 instance families can’t be backup
instance families for each other. See
[BACKUP\_INSTANCE\_FAMILIES](/sql-reference/sql/create-compute-pool#label-create-compute-pool-backup-instance-families).

For pricing information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

> - [AWS Instance Families](/developer-guide/snowpark-container-services/instance-families-aws)
> - [Azure Instance Families](/developer-guide/snowpark-container-services/instance-families-azure)
> - [Google Cloud Instance Families](/developer-guide/snowpark-container-services/instance-families-gcp)
