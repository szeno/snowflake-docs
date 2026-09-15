# Using Snowflake

These topics describe the concepts and tasks associated with using Snowflake.

- [Snowsight: The Snowflake web interface](/user-guide/ui-snowsight) — Learn how to use Snowsight for your Snowflake operations:

  - [Snowsight quick tour](/user-guide/ui-snowsight-quick-tour)
  - [Getting started with Snowsight](/user-guide/ui-snowsight-gs)
  - [Work with worksheets in Snowsight](/user-guide/ui-snowsight-worksheets)
  - [Workspaces](/user-guide/ui-snowsight/workspaces)
  - [About Legacy Snowflake Notebooks](/user-guide/ui-snowsight/notebooks)
  - [Using Snowflake Copilot](/user-guide/snowflake-copilot)
  - [Visualizing data with dashboards](/user-guide/ui-snowsight-dashboards)
  - [Explore and manage database objects in Snowsight](/user-guide/ui-snowsight-data)
  - [Monitor query activity with Query History](/user-guide/ui-snowsight-activity)
  - [Evaluating and monitoring account security in the Trust Center](/user-guide/trust-center/overview)
  - [Manage Snowflake Support cases](/user-guide/ui-support)
  - [Set up and manage notification contacts for Snowflake](/user-guide/ui-snowsight-contacts)
- [Virtual warehouses](/user-guide/warehouses) — Key concepts and tasks for creating and using virtual warehouses to execute queries and perform DML operations, such as loading and unloading data:

  - [Overview of warehouses](/user-guide/warehouses-overview)
  - [Multi-cluster warehouses](/user-guide/warehouses-multicluster)
  - [Warehouse considerations](/user-guide/warehouses-considerations)
  - [Working with warehouses](/user-guide/warehouses-tasks)
  - [Using the Query Acceleration Service (QAS)](/user-guide/query-acceleration-service)
  - [Monitoring warehouse load](/user-guide/warehouses-load-monitoring)
- [Databases, Tables & Views](/user-guide/databases) — Key concepts and tasks related to understanding and working with Snowflake databases and tables:

  - [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions)
  - [Working with Temporary and Transient Tables](/user-guide/tables-temp-transient)
  - [Introduction to external tables](/user-guide/tables-external-intro)
  - [Overview of Views](/user-guide/views-introduction)
  - [Working with Secure Views](/user-guide/views-secure)
  - [Working with Materialized Views](/user-guide/views-materialized)
  - [Table Design Considerations](/user-guide/table-considerations)
  - [Cloning considerations](/user-guide/object-clone)
  - [Data storage considerations](/user-guide/tables-storage-considerations)
- [Query Data in Snowflake](/guides-overview-queries) — Key concepts and tasks for executing queries in Snowflake:

  - [Working with joins](/user-guide/querying-joins)
  - [Understanding How Snowflake Can Eliminate Redundant Joins](/user-guide/join-elimination)
  - [Working with Subqueries](/user-guide/querying-subqueries)
  - [Querying Hierarchical Data](/user-guide/queries-hierarchical)
  - [Working with CTEs (Common Table Expressions)](/user-guide/queries-cte)
  - [Querying Semi-structured Data](/user-guide/querying-semistructured)
  - [Analyzing data with window functions](/user-guide/functions-window-using)
  - [Identifying Sequences of Rows That Match a Pattern](/user-guide/match-recognize-introduction)
  - [Using Sequences](/user-guide/querying-sequences)
  - [Using Persisted Query Results](/user-guide/querying-persisted-results)
  - [Computing the Number of Distinct Values](/user-guide/querying-distinct-counts)
  - [Estimating Similarity of Two or More Sets](/user-guide/querying-approximate-similarity)
  - [Estimating Frequent Values](/user-guide/querying-approximate-frequent-values)
  - [Estimating Percentile Values](/user-guide/querying-approximate-percentile-values)
  - [Querying data using worksheets](/user-guide/ui-snowsight-query)
  - [Canceling Statements](/user-guide/querying-cancel-statements)
- [Introduction to loading semi-structured data](/user-guide/semistructured-intro) — Key concepts and tasks for working with JSON and other types of semi-structured data:

  - [Supported formats for semi-structured data](/user-guide/semistructured-data-formats)
  - [Considerations for semi-structured data stored in VARIANT](/user-guide/semistructured-considerations)
  - [Tutorial: JSON basics for Snowflake](/user-guide/tutorials/json-basics-tutorial)
- [Introduction to unstructured data](/user-guide/unstructured-intro) — Key concepts and tasks for working with unstructured data:

  - [Directory tables](/user-guide/data-load-dirtables)
  - [REST API for unstructured data support](/user-guide/data-load-unstructured-rest-api)
  - [Share unstructured data with a secure view](/user-guide/unstructured-data-sharing)
  - [Troubleshooting processing of unstructured data](/user-guide/unstructured-ts)
- [Snowflake Time Travel & Fail-safe](/user-guide/data-availability) — Key concepts and tasks for understanding how Snowflake maintains access to deleted and modified data, and also how Snowflake enables data recovery in the
  event of loss:

  - [Understanding & using Time Travel](/user-guide/data-time-travel)
  - [Understanding and viewing Fail-safe](/user-guide/data-failsafe)
  - [Storage costs for Time Travel and Fail-safe](/user-guide/data-cdp-storage-costs)
- [Introduction to streams and tasks](/user-guide/data-pipelines-intro) — Key concepts and tasks for transforming and optimizing loaded data for analysis:

  - [Introduction to streams](/user-guide/streams-intro)
  - [Introduction to tasks](/user-guide/tasks-intro)
- [Introduction to business continuity & disaster recovery](/user-guide/replication-intro) — Key concepts and tasks for replicating and failing over databases across multiple Snowflake accounts, as well as redirecting client connections, for business continuity and disaster recovery:

  - [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro)
  - [Redirecting client connections](/user-guide/client-redirect)
- [Sample data sets](/user-guide/sample-data) — Key concepts and tasks for using the sample data sets provided with Snowflake:

  - [Use the sample database](/user-guide/sample-data-using)
  - [Sample data: TPC-H](/user-guide/sample-data-tpch)
  - [Sample Data: OpenWeatherMap — Deprecated](/user-guide/sample-data-openweathermap)
- [Alerts and Notifications](/guides-overview-alerts) — Key concepts and tasks for sending email notifications in SQL (e.g. from a
  stored procedure, task, etc.) and setting up alerts to perform actions or send notifications when data in Snowflake meets
  certain conditions.

  - [Setting up alerts based on data in Snowflake](/user-guide/alerts)
  - [Notifications in Snowflake](/user-guide/notifications/about-notifications)
- [Snowflake Postgres](/user-guide/snowflake-postgres/about) — Create, manage, and use Postgres instances directly from Snowflake:

  - [Creating a Snowflake Postgres Instance](/user-guide/snowflake-postgres/postgres-create-instance)
  - [Connecting to Snowflake Postgres](/user-guide/snowflake-postgres/connecting-to-snowflakepg)
  - [Snowflake Postgres Roles](/user-guide/snowflake-postgres/postgres-roles)
  - [Snowflake Postgres Connection Pooling](/user-guide/snowflake-postgres/postgres-connection-pooling)
  - [Snowflake Postgres Maintenance](/user-guide/snowflake-postgres/postgres-maintenance)
  - [Snowflake Postgres Read Replicas](/user-guide/snowflake-postgres/postgres-create-replica)
  - [Snowflake Postgres High Availability](/user-guide/snowflake-postgres/high-availability)
  - [Snowflake Postgres Cost Evaluation](/user-guide/snowflake-postgres/postgres-cost)
  - [Snowflake Postgres Insights](/user-guide/snowflake-postgres/insights)
  - [Snowflake Postgres logging](/user-guide/snowflake-postgres/postgres-logging)
  - [Using Cortex Code CLI with Snowflake Postgres](/user-guide/snowflake-postgres/postgres-cortex-code)
  - [Snowflake Postgres networking](/user-guide/snowflake-postgres/postgres-network)
  - [Snowflake Postgres Instance Sizes](/user-guide/snowflake-postgres/postgres-instance-sizes)
  - [Snowflake Postgres Extensions](/user-guide/snowflake-postgres/postgres-extensions)
  - [Snowflake Postgres Server Settings](/user-guide/snowflake-postgres/postgres-server-settings)
