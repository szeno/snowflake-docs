# External data sources with Snowpark Connect for Spark

With Snowpark Connect for Spark, you can work with data outside Snowflake through cloud object storage, relational databases, and Apache Iceberg
tables.

Cloud storage
:   Read and write files (CSV, JSON, Parquet, and more) on Amazon S3, Azure Blob Storage, and Google Cloud Storage using Snowflake
    external stages or direct cloud paths. See [Cloud storage with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-cloud-storage).

JDBC databases
:   Read from and write to external relational databases such as MySQL and PostgreSQL using the JDBC data source API. See
    [JDBC data sources for Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-jdbc).

Apache Iceberg tables
:   Read and write Snowflake-managed and externally managed Apache Iceberg tables through the standard Spark DataFrame APIs. See
    [Apache Iceberg tables with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-iceberg).
