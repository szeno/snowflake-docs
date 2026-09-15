# Configuring Snowflake for Spark in Databricks

The Databricks version 4.2 native Snowflake Connector allows your Databricks account
to read data from and write data to Snowflake without importing any libraries.
Older versions of Databricks required importing the libraries for the Spark connector into your Databricks clusters.

The connector automatically distributes processing across Spark and Snowflake,
without requiring the user to specify the parts of the processing that should be
done on each system. Queries also benefit from Snowflake’s automatic query
pushdown optimization.

## Prerequisites

- You must have a Databricks account, and you must be using the Databricks Runtime version 4.2 or later. In addition:

  - You should have already set your Snowflake user login name and password in your Databricks secret manager; you will read the login and password back by calling `dbutils.secrets.get(...)`. For more details about the Databricks secret manager, see <https://docs.databricks.com/user-guide/secrets/index.html>
- You must have a Snowflake account. To read or write from this account, you need the following information:

  - URL for your Snowflake account.
  - Login name and password for the user who connects to the account.
  - Default database and schema to use for the session after connecting.
  - Default virtual warehouse to use for the session after connecting.
- The role used in the connection needs USAGE and CREATE STAGE privileges
  on the schema that contains the table that you will read from or write to
  via Databricks.

## Accessing Databricks Snowflake Connector Documentation

The primary documentation for the Databricks Snowflake Connector is available on the Databricks web site. That documentation includes examples showing the commands
a Scala or Python notebook uses to send data from Spark to Snowflake or vice versa.

For more details, see [Data Sources — Snowflake](https://docs.databricks.com/spark/latest/data-sources/snowflake.html).

## Preparing an External Location for Long-running Queries

If some of your jobs exceed 36 hours in length, consider preparing an
external location to use to exchange data between Snowflake and Spark.
For more information, see [Preparing an External Location For Files](/user-guide/spark-connector-install#label-preparing-external-location-for-spark).

## Query Pushdown in Databricks

Spark queries benefit from Snowflake’s automatic query pushdown optimization, which improves performance. By default, Snowflake query pushdown is enabled in Databricks.

For more details about query pushdown, see [Pushing Spark Query Processing to Snowflake](https://www.snowflake.com/snowflake-spark-part-2-pushing-query-processing/) (Snowflake Blog).
