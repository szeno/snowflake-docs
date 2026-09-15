# Tutorials to get started with Snowflake

The tutorials in this topic provide hands-on examples that get you started with Snowflake. To explore these
tutorials, you must have a Snowflake account and a user with the required roles and access to a virtual
warehouse:

- If you have signed up for a [trial account](/user-guide/admin-trial-account), the trial account user has
  the required roles and a virtual warehouse that you can use for several of these tutorials.
- If you use another account to explore these tutorials, you must sign in as a user that has the required
  roles and that can use a virtual warehouse.

Each tutorial describes the prerequisites that must be met before completing its tasks, including the roles required for
the user who performs the tasks. Several tutorials require the ACCOUNTADMIN and SYSADMIN roles.

Note

Snowflake bills a minimal amount for the on-disk storage that you use for any sample data in
these tutorials. Snowflake requires a [virtual warehouse](/user-guide/warehouses) to
load the data and execute queries. A running virtual warehouse consumes Snowflake credits.
After you finish a tutorial, you can drop objects that are created in the tutorial to minimize
costs.

If you are using a [30-day trial account](https://signup.snowflake.com/),
which provides free credits, you won’t incur any costs.

The following sections contain links to tutorials that get you started with Snowflake tasks and features:

- [Tutorial that introduces you to Snowflake](#tutorial-that-introduces-you-to-snowflake)
- [Tutorials to get started with data engineering](#tutorials-to-get-started-with-data-engineering)
- [Tutorial to get started with security](#tutorial-to-get-started-with-security)
- [Other learning resources](#other-learning-resources)

## Tutorial that introduces you to Snowflake

Snowflake provides the following tutorial to introduce you to key concepts and tasks:

[Snowflake in 20 minutes](/user-guide/tutorials/snowflake-in-20minutes)
:   Use SnowSQL, a Snowflake command-line client, to learn about key concepts and tasks.

## Tutorials to get started with data engineering

Snowflake provides the following tutorials to get you started with data engineering:

Note

These tutorials show you how to load data into a table by using the
[COPY INTO <table>](/sql-reference/sql/copy-into-table) command. For information about other options
for loading data, see [Overview of data loading](/user-guide/data-load-overview).

### Load data

[Load and query sample data using SQL](/user-guide/tutorials/tasty-bytes-sql-load)
:   Uses a fictitious food truck brand named Tasty Bytes to show you how to
    [load](/user-guide/data-load-overview) and query data in Snowflake using
    SQL. You can access a pre-loaded
    [Snowsight template](/user-guide/ui-snowsight/snowsight-templates) worksheet
    to complete these tasks.

[Load data from cloud storage: Amazon S3](/user-guide/tutorials/load-from-cloud-tutorial)
:   Shows you how to load data from an Amazon S3 bucket into Snowflake using SQL. You can
    access a pre-loaded Snowsight template worksheet to complete these tasks.

[Load data from cloud storage: Microsoft Azure](/user-guide/tutorials/load-from-cloud-tutorial-azure)
:   Shows you how to load data from Microsoft Azure cloud storage into Snowflake using SQL.
    You can access a pre-loaded Snowsight template worksheet to complete these tasks.

[Load data from cloud storage: Google Cloud Storage](/user-guide/tutorials/load-from-cloud-tutorial-gcs)
:   Shows you how to load data from Google Cloud Storage into Snowflake using SQL.
    You can access a pre-loaded Snowsight template worksheet to complete these tasks.

### Bulk load data

[Bulk load from a local file system using COPY](/user-guide/tutorials/data-load-internal-tutorial)
:   Describes how to [bulk load data](/user-guide/data-load-local-file-system) from files in your
    local file system into a table.

[Bulk load from Amazon S3 using COPY](/user-guide/tutorials/data-load-external-tutorial)
:   Describes how to bulk load data from files in an existing Amazon Simple Storage Service (Amazon S3)
    bucket into a table.

### Work with semi-structured data

[Learn the basics of using JSON with Snowflake](/user-guide/tutorials/json-basics-tutorial)
:   Describes the basics of using [JSON](/user-guide/semistructured-data-formats#label-what-is-json) with Snowflake.

[Load JSON data into a relational table](/user-guide/tutorials/script-data-load-transform-json)
:   Uses a [COPY INTO <table>](/sql-reference/sql/copy-into-table) command with a SELECT statement to load individual
    elements in a staged JSON file into a table.

[Load and unload Parquet data](/user-guide/tutorials/script-data-load-transform-parquet)
:   Describes how you can upload [Parquet](/user-guide/semistructured-data-formats#label-what-is-parquet) data by transforming elements of
    a staged Parquet file directly into table columns using the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command. The
    tutorial also describes how you can use the [COPY INTO <location>](/sql-reference/sql/copy-into-location) command to unload table data
    into a Parquet file.

## Tutorial to get started with security

Snowflake provides the following tutorial to get you started with security:

[Create users and grant roles](/user-guide/tutorials/users-and-roles-tutorial)
:   Shows you how to create a [user](/user-guide/admin-user-management) and grant a role to it
    by using SQL commands. You can access a pre-loaded [Snowsight template](/user-guide/ui-snowsight/snowsight-templates)
    worksheet to complete these tasks.

## Other learning resources

These other learning sources are available:

[Tutorials](https://docs.snowflake.com/tutorials)
:   Explore a large repository of tutorials with hands-on examples that help you learn about Snowflake’s features.

[Snowflake Education Services](https://learn.snowflake.com/en/)
:   Discover instructor-led classes, on-demand courses, and self-directed learning to get you started with Snowflake.

[Snowflake for Developers](https://www.snowflake.com/en/developers/guides/)
:   Discover product quickstarts, industry-specific use cases, administration best practices, and reference architectures
    from Snowflake experts and partners.

[Snowflake Developers YouTube Channel](https://www.youtube.com/@snowflakedevelopers)
:   Discover Snowflake product tips, demos, and tutorials.
