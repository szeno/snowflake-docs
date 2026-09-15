# Snowpark Connect for Apache Spark

With Snowpark Connect for Apache Spark™, you can connect your existing Spark workloads directly to Snowflake and run them on the
Snowflake compute engine. Snowpark Connect for Spark supports the
[Spark DataFrame API](https://spark.apache.org/docs/latest/sql-programming-guide.html) on Snowflake. All
workloads run on a Snowflake warehouse, so you can run your PySpark DataFrame code with all the benefits of
the Snowflake engine.

In Apache Spark™ version 3.4, the Apache Spark community introduced Spark Connect. Its decoupled client-server
architecture separates the user’s code from the Spark cluster where the work is done. This architecture makes
it possible for Snowflake to power Spark jobs.

Snowpark Connect for Spark offers the following benefits:

- Decouples client and server, so that Spark code can run remotely against the Snowflake compute engine
  without your needing to manage a Spark cluster.
- Lets your team use their existing ecosystem to author and orchestrate Spark workloads, for example,
  Jupyter notebooks, VS Code, and Airflow.
- Allows you to reuse open-source Spark DataFrames and Spark SQL code with minimal migration or changes.
- Offers a streamlined way to integrate Snowflake governance, security, and scalability into Spark-based
  workflows, supporting a familiar PySpark experience with pushdown optimizations into Snowflake.
- Supports multiple languages, including Python, Java, Scala, and Spark SQL.

## Develop and run Spark workloads on Snowflake

You can use familiar development tools to develop Spark workloads that run on Snowflake, and then run those
workloads in batches using the Snowpark Submit command-line tool.

- **Interactive development**: Use tools such as Snowflake Notebooks, VS Code, or IntelliJ IDEA to develop
  Spark workloads. You can authenticate with Snowflake, start a Spark session, and run PySpark or Java/Scala
  code to load, transform, and analyze data. For more information, see
  [Environment setup for Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-environment-setup).
- **Batch workloads**: Run asynchronous Spark workloads directly on Snowflake’s infrastructure while using
  familiar Spark semantics. Use Snowpark Submit to submit production-ready Spark applications using a simple CLI
  interface and tools like Airflow. For more information, see
  [Orchestrating Snowpark Connect for Spark workloads](/developer-guide/snowpark-connect/snowpark-connect-orchestration).

## Next steps

- [Getting started](/developer-guide/snowpark-connect/snowpark-connect-getting-started): Set up your
  environment, run the tutorial, or migrate existing workloads.
- [Development](/developer-guide/snowpark-connect/snowpark-connect-development): Learn about accessing
  external data, executing SQL, file I/O, and user-defined functions.
- [Orchestration](/developer-guide/snowpark-connect/snowpark-connect-orchestration): Run batch
  workloads asynchronously with Snowpark Submit.
- [Monitoring](/developer-guide/snowpark-connect/snowpark-connect-monitoring): Track query execution
  and resource usage.
- [Troubleshooting](/developer-guide/snowpark-connect/snowpark-connect-troubleshooting): Diagnose
  common issues, including limitations.
- [Optimization](/developer-guide/snowpark-connect/snowpark-connect-optimization): Improve the
  performance of your Snowpark Connect for Spark workloads.
- [Reference](/developer-guide/snowpark-connect/snowpark-connect-reference-overview): Explore API
  support, parameters, and client library references.
- [Samples](/developer-guide/snowpark-connect/snowpark-connect-samples): End-to-end examples for
  common scenarios.
