# Snowflake Connector for Spark

The Snowflake Connector for Spark (“Spark connector”) brings Snowflake into the Apache Spark ecosystem, enabling Spark to read
data from, and write data to, Snowflake.
From Spark’s perspective, Snowflake looks similar to other Spark data sources (PostgreSQL, HDFS, S3, etc.).

Note

You can also use [Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-apache-spark) as an alternative to the Snowflake Connector for Spark.

Snowflake supports multiple versions of the Spark connector:

> - Spark Connector 2.x: Spark versions 3.2, 3.3, and 3.4.
>
>   - There’s a separate version of the Snowflake connector for each version of Spark. Use the correct version of the connector for your version of Spark.
> - Spark Connector 3.x: Spark versions 3.2, 3.3, 3.4, 3.5, 4.0, and 4.1.
>
>   - Each Spark Connector 3 package supports most versions of Spark.

The connector runs as a Spark plugin and is provided as a Spark package (`spark-snowflake`).

## Enforce data protection policies on Apache Iceberg tables accessed from Spark

Snowflake supports enforcing row access and data masking policies on Apache Iceberg tables that you query from Apache Spark™ through
Snowflake Horizon Catalog. To enable this enforcement, you must install 3.1.6 or a later version of the Spark connector. The Spark connector
connects Spark to Snowflake to evaluate policies that are configured on the Iceberg tables.
For more information, see [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies).

**Next Topics:**

- [Overview of the Spark Connector](/user-guide/spark-connector-overview)
- [Installing and Configuring the Spark Connector](/user-guide/spark-connector-install)
- [Configuring Snowflake for Spark in Databricks](/user-guide/spark-connector-databricks)
- [Configuring Snowflake for Spark in Qubole](/user-guide/spark-connector-qubole)
- [Using the Spark Connector](/user-guide/spark-connector-use)
