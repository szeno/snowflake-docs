# Snowflake Catalog SDK

The Snowflake Catalog SDK is available for Apache Iceberg™ versions 1.2.0 or later.

With the Snowflake Catalog SDK, you can query [Iceberg tables](/user-guide/tables-iceberg) using a third-party engine
such as Apache Spark™ or Trino.

## Supported catalog operations

The SDK supports the following commands for browsing Iceberg metadata in Snowflake:

- SHOW NAMESPACES
- USE NAMESPACE
- SHOW TABLES
- USE DATABASE
- USE SCHEMA

The SDK currently supports read operations (SELECT statements) only.

## Install and connect

To install the Snowflake Catalog SDK,
download the [latest version of the Iceberg libraries](https://iceberg.apache.org/releases/).

Before you can use the Snowflake Catalog SDK, you need a Snowflake database
with one or more Iceberg tables.
To create an Iceberg table, see [Create an Apache Iceberg™ table in Snowflake](/user-guide/tables-iceberg-create).

After you establish a connection and the SDK confirms that Iceberg metadata is present,
Snowflake accesses your Parquet data using the external volume that is associated with your Iceberg table(s).

## Examples using Spark

Note

To learn about using Trino with the Snowflake Catalog SDK, see the
[Trino documentation](https://trino.io/docs/current/object-storage/metastores.html#iceberg-snowflake-catalog).

To read table data with the SDK, start by configuring the following properties for your Spark cluster:

Copy code

```
spark-shell --packages org.apache.iceberg:iceberg-spark-runtime-3.3_2.13:1.2.0,net.snowflake:snowflake-jdbc:3.13.28
# Configure a catalog named "snowflake_catalog" using the standard Iceberg SparkCatalog adapter
--conf spark.sql.catalog.snowflake_catalog=org.apache.iceberg.spark.SparkCatalog
# Specify the implementation of the named catalog to be Snowflake's Catalog implementation
--conf spark.sql.catalog.snowflake_catalog.catalog-impl=org.apache.iceberg.snowflake.SnowflakeCatalog
# Provide a Snowflake JDBC URI with which the Snowflake Catalog will perform low-level communication with Snowflake services
--conf spark.sql.catalog.snowflake_catalog.uri='jdbc:snowflake://<account_identifier>.snowflakecomputing.com'
# Configure the Snowflake user on whose behalf to perform Iceberg metadata lookups
--conf spark.sql.catalog.snowflake_catalog.jdbc.user=<user_name>
# Provide the user password. To configure the credentials, you can provide either password or private_key_file.
--conf spark.sql.catalog.snowflake_catalog.jdbc.password=<password>
# Configure the private_key_file to use when connecting to Snowflake services; additional connection options can be found at https://docs.snowflake.com/en/user-guide/jdbc-configure.html
--conf spark.sql.catalog.snowflake_catalog.jdbc.private_key_file=<location of the private key>
```

Note

You can use any Snowflake-supported [JDBC driver connection parameter](/developer-guide//jdbc/jdbc-parameters)
in your configuration by using the following syntax: `--conf spark.sql.catalog.snowflake_catalog.jdbc.property-name=property-value`

After you configure your Spark cluster, you can check which tables are available to query. For example:

Copy code

```
spark.sessionState.catalogManager.setCurrentCatalog("snowflake_catalog");
spark.sql("SHOW NAMESPACES").show()
spark.sql("SHOW NAMESPACES IN my_database").show()
spark.sql("USE my_database.my_schema").show()
spark.sql("SHOW TABLES").show()
```

Then you can select a table to query.

Copy code

```
spark.sql("SELECT * FROM my_database.my_schema.my_table WHERE ").show()
```

You can use the `DataFrame` structure with languages like Python and Scala to query data.

Copy code

```
df = spark.table("my_database.my_schema.my_table")
df.show()
```

Note

If you receive vectorized read errors while running queries, you can disable the vectorized reads for your session
by configuring: `spark.sql.iceberg.vectorization.enabled=false`. To keep using vectorized reads,
you can set the [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#label-storage-serialization-policy) parameter.

## Query caching

When you issue a query, Snowflake caches the result within a certain time frame (90 seconds by default).
You might experience latency up to that duration. If you plan to access data programmatically for comparison purposes,
you can set the `spark.sql.catalog.cache-enabled` property to `false` to disable caching.

If your application is designed to tolerate a specific amount of latency, you can use the following property
to specify the latency period: `spark.sql.catalog.cache.expiration-interval-ms`.

## Limitations

The following limitations apply to the Snowflake Catalog SDK and are subject to change:

> - The SDK currently supports read operations (SELECT statements) only.
> - Only Apache Spark and Trino are supported for reading Iceberg tables.
> - You cannot use the SDK to access non-Iceberg Snowflake tables.
