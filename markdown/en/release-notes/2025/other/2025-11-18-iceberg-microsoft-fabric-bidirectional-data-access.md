# Nov 18, 2025: Apache Iceberg™ tables: Support for bi-directional data access with Microsoft Fabric (*Preview*)

You can now query Apache Iceberg™ tables between Snowflake and Microsoft Fabric in both directions by using a REST API endpoint:

- Query Snowflake-managed Iceberg tables from Fabric. To query Snowflake-managed Iceberg tables in Fabric, connect a
  Snowflake database to Fabric. You can select an existing database or create a new one. After connecting, Fabric creates an item that lets
  you access your Snowflake-managed tables. For more information, see [Query Snowflake-managed Apache Iceberg™ tables by using Microsoft Fabric](/user-guide/tables-iceberg-query-using-microsoft-fabric).
- Query OneLake tables with Iceberg metadata from Snowflake. To query Fabric Iceberg tables registered in Snowflake, configure a REST
  catalog integration for OneLake table APIs, which provides table information from Fabric.

  For more information, see the following topics:

  - [Configure a catalog integration for OneLake REST](/user-guide/tables-iceberg-configure-catalog-integration-rest-onelake)
  - [Overview of OneLake table APIs](https://learn.microsoft.com/fabric/onelake/table-apis/table-apis-overview) in the Microsoft Fabric documentation
  - [Getting started with OneLake table APIs for Iceberg](https://learn.microsoft.com/en-us/fabric/onelake/table-apis/iceberg-table-apis-get-started#snowflake)
    in the Microsoft Fabric documentation
