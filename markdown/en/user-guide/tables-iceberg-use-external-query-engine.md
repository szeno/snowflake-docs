# Use an external query engine with Apache Iceberg™ tables

Snowflake offers the following two options for using an external query engine to query Apache Iceberg™ tables:

- [External query engines through Snowflake Horizon Catalog](#label-tables-iceberg-external-query-engines-horizon)
- [Microsoft Fabric](#label-tables-iceberg-external-query-engines-fabric)

## External query engines through Snowflake Horizon Catalog

Feature — Generally Available

Not available in government regions.

You can access Snowflake-managed Apache Iceberg™ tables by using any
external query engine that supports the open Iceberg REST protocol, such as Apache Spark™. To ensure this interoperability with
external engines, [Apache Polaris™](https://github.com/apache/polaris) is integrated into Horizon Catalog. You can access
these tables in a Snowflake account by using a single Horizon Catalog endpoint and you can use your existing users, roles, policies,
and authentication in Snowflake.

For more information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).

## Microsoft Fabric

To view Snowflake-managed Iceberg tables in [Microsoft Fabric](https://learn.microsoft.com/fabric/), you can connect a standard Snowflake
database to Fabric, which syncs the database with Fabric. You can then view any Snowflake-managed Iceberg tables in the database in Fabric.

For more information, see [Query Snowflake-managed Apache Iceberg™ tables by using Microsoft Fabric](/user-guide/tables-iceberg-query-using-microsoft-fabric).
