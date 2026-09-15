# Virtual warehouses

A virtual warehouse, often referred to simply as a “warehouse”, is a cluster of compute resources in Snowflake. A virtual warehouse is
available in two types:

- Standard
- Snowpark-optimized

A warehouse provides the required resources, such as CPU, memory, and temporary storage, to
perform the following operations in a Snowflake session:

- Executing SQL [SELECT](/sql-reference/sql/select) statements that require compute resources (for example, retrieving rows from tables and views).
- Performing DML operations, such as:
  - Updating rows in tables ([DELETE](/sql-reference/sql/delete) , [INSERT](/sql-reference/sql/insert) , [UPDATE](/sql-reference/sql/update)).
  - Loading data into tables ([COPY INTO <table>](/sql-reference/sql/copy-into-table)).
  - Unloading data from tables ([COPY INTO <location>](/sql-reference/sql/copy-into-location)).

Note

To perform these operations, a warehouse must be running and in use for the session. While a warehouse is running, it consumes Snowflake
credits.

[Overview of warehouses](/user-guide/warehouses-overview)
:   Warehouses are required for queries, as well as all DML operations, including loading data into tables.
    In addition to being defined by its type as either Standard or Snowpark-optimized, a warehouse is defined by its size,
    as well as the other properties that can be set to help control and automate warehouse activity.

[Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized)
:   Snowpark workloads can be run on both Standard and Snowpark-optimized warehouses. Snowpark-optimized warehouses are recommended for workloads that have large memory requirements such as ML training use cases.

[Warehouse considerations](/user-guide/warehouses-considerations)
:   Best practices and general guidelines for using virtual warehouses in Snowflake to process queries.

[Multi-cluster warehouses](/user-guide/warehouses-multicluster)
:   Multi-cluster warehouses enable you to scale compute resources to manage your user and query concurrency needs as they change, such as during peak and off hours.

[Working with warehouses](/user-guide/warehouses-tasks)
:   Learn how to create, stop, start and otherwise manage Snowflake warehouses.

[Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service)
:   The query acceleration service can accelerate parts of the query workload in a warehouse.
    When enabled for a warehouse, query acceleration can improve overall warehouse performance by reducing the impact of outlier queries
    (i.e. queries which use more resources than typical queries).

[Monitoring warehouse load](/user-guide/warehouses-load-monitoring)
:   Warehouse query load measures the average number of queries that were running or queued within a specific interval.

- [Overview of warehouses](/user-guide/warehouses-overview)
- [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized)
- [Warehouse considerations](/user-guide/warehouses-considerations)
- [Multi-cluster warehouses](/user-guide/warehouses-multicluster)
- [Working with warehouses](/user-guide/warehouses-tasks)
- [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service)
- [Monitoring warehouse load](/user-guide/warehouses-load-monitoring)
