# Tutorials and Other Resources

This topic provides links to assorted “how to” tutorials/labs and “best practices” for using Snowflake.

## Tutorials

Snowflake provides several tutorials for getting started.

You will need a Snowflake account to explore these tutorials. If you sign up for a trial account,
the trial account has a user with necessary roles (ACCOUNTADMIN and SYSADMIN) and a virtual warehouse (COMPUTE\_WH)
needed to explore this tutorial. If you use any other account to explore this tutorial, then make sure your user is
granted these roles and the account has the virtual warehouse.

For new users, we recommend you start with these tutorials:

- [Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes) — A simple tutorial using SnowSQL, the Snowflake command-line client, to introduce key concepts and tasks.
- [Getting Started with Snowflake - Zero to Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake/index.html) — A comprehensive tutorial that uses both SnowSQL and [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) covers data loading,
  querying, working with semi-structured data, accessing
  historical data using Snowflake’s Time Travel feature, sharing, and so on.
- [Getting Started with Python](https://quickstarts.snowflake.com/guide/getting_started_with_python/index.html) — A tutorial in which you set up the Python Connector and then explore the basic operations you can do with it.

For tutorials on bulk loading, see:

- [Bulk Loading from a Local File System](/user-guide/tutorials/data-load-internal-tutorial)
- [Bulk Loading from Amazon S3](/user-guide/tutorials/data-load-external-tutorial)

In addition, you might explore the following pages that introduce important concepts about semi-structured data:

- [JSON Basics](/user-guide/tutorials/json-basics-tutorial)
- [Loading JSON Data into a Relational Table](/user-guide/tutorials/script-data-load-transform-json)
- [Loading and Unloading Parquet Data](/user-guide/tutorials/script-data-load-transform-parquet)

![](/static/images/video-play-bn.png)
![](/static/images/vid-thumb-d-generic.png)

![](/static/images/vid-thumb-gs-key-concepts.png)
![](/static/images/vid-thumb-gs-intro-snowflake.png)
![](/static/images/vid-thumb-gs-intro-virtual-warehouses.png)
![](/static/images/vid-thumb-gs-intro-db-query.png)
![](/static/images/vid-thumb-gs-intro-data-loading.png)

![](/static/images/vid-thumb-d-accel-bi-queries.png)
![](/static/images/vid-thumb-d-easily-load-analyze-semi-struct.png)
![](/static/images/vid-thumb-d-elim-conc-issues.png)
![](/static/images/vid-thumb-d-protect-data-time-travel.png)
![](/static/images/vid-thumb-d-quick-look-zero-copy-cloning.png)
![](/static/images/vid-thumb-d-easy-data-sharing.png)
![](/static/images/vid-thumb-d-query-mult-databases.png)
![](/static/images/vid-thumb-d-tackle-high-concurrency.png)
![](/static/images/vid-thumb-d-snowpipe.png)

## Best Practices

Snowflake best practices are provided throughout the documentation. The following are
links to important practices related to Snowflake features:

- [Roles and Access Control](/user-guide/security-access-control-considerations)
- [Virtual Warehouses](/user-guide/warehouses-considerations)
- [Table Design](/user-guide/table-considerations)
- [Data Storage](/user-guide/tables-storage-considerations)
- [Data Loading](/user-guide/data-load-considerations)
- [Data Unloading](/user-guide/data-unload-considerations)
- [Semi-structured Data](/user-guide/semistructured-considerations)

## Sample Data Sets

The following benchmarking datasets are available for all Snowflake accounts:

- [TPC-DS](/user-guide/sample-data-tpcds)
- [TPC-H](/user-guide/sample-data-tpch)

In addition, [Snowflake Marketplace](https://app.snowflake.com/marketplace?pricing=free) is where you can
find additional data sets, provided by third-parties, for use with Snowflake. For related documentation, refer to
[Introduction to the Snowflake Marketplace](https://other-docs.snowflake.com/en/marketplace/intro.html).
