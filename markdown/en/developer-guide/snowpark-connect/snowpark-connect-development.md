# Developing with Snowpark Connect for Spark

Once your environment is set up, you can build Spark workloads that read, transform, and write data
through Snowflake. Snowpark Connect for Spark translates standard Spark DataFrame operations into SQL, so you can
use familiar APIs while Snowflake handles the compute.

This section covers the following topics:

- [Accessing external data sources](/developer-guide/snowpark-connect/snowpark-connect-external-data-sources),
  including cloud storage, JDBC-accessible databases, and Apache Iceberg tables.
- [Executing Snowflake SQL](/developer-guide/snowpark-connect/snowpark-connect-executing-sql)
  through standard Spark SQL and the SnowflakeSession class.
- [File I/O](/developer-guide/snowpark-connect/snowpark-connect-file-io) for reading and
  writing data using stages, cloud storage locations, and local files.
- [User-defined functions](/developer-guide/snowpark-connect/snowpark-connect-udfs) for
  registering Python, Java, and Scala UDFs and UDTFs when built-in functions aren’t sufficient.
