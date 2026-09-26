# Configuring Snowflake for Spark in Qubole

To configure Snowflake for Spark in Qubole, you simply add Snowflake as a Qubole data store. This topic provides step-by-step instructions for performing this task using the Qubole Data Service (QDS) UI.

Note

You can also use the QDS REST API to add Snowflake as a data store. For step-by-step instructions, see
[Adding a Snowflake Data Warehouse as a Data Store](http://docs.qubole.com/en/latest/partner-integration/snowflake-integration/add-a-snowflake-data-warehouse.html) (in the Qubole Documentation).

## Prerequisites

- You must be a QDS system administrator to add a data store.
- You must have a Qubole Enterprise edition account.
- The role used in the connection needs USAGE and CREATE STAGE privileges
  on the schema that contains the table that you will read from or write to
  via Qubole.

## Preparing an External Location for Long-running Queries

If some of your jobs exceed 36 hours in length, consider preparing an
external location to use to exchange data between Snowflake and Spark.
For more information, see [Preparing an External Location For Files](/user-guide/spark-connector-install#label-preparing-external-location-for-spark).

## Adding Snowflake as a Data Store in the QDS UI

1. From the **Home** menu, click **Explore**.
2. In the dropdown list on the **Explore** page, select **+ Add Data Store**.
3. Enter the required information in the following fields:

   - **Data Store Name**: Enter the name of the data store to be created.
   - **Database Type**: Select ‘Snowflake’.
   - **Catalog Name**: Enter the name of the Snowflake catalog.
   - **Database Name**: Enter the name of the database in Snowflake where the data is stored.
   - **Warehouse Name**: Enter the name of the Snowflake virtual warehouse to use for queries.
   - **Host Address**: Enter the base URL of your Snowflake account (e.g.
     `myorganization-myaccount.snowflakecomputing.com`). See [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config) for details on
     specifying your account identifier in this URL.
   - **Username**: Enter the login name for your Snowflake user (used to connect to the host).
   - **Password**: Enter the password for your Snowflake user (used to connect to the host).

   Note that all the values are case-sensitive, except for **Host Address**.
4. Click **Save** to create the data store.

Repeat these steps for each Snowflake database that you want to add as a data store. Or you can edit the data store to change the Snowflake database or any other properties for the data store (e.g.
change the virtual warehouse used for queries).

Note

After adding a Snowflake data store, restart the Spark cluster (if you are using an already-running Spark cluster). Restarting the Spark cluster installs the `.jar` files for the Snowflake
Connector for Spark and the Snowflake JDBC Driver.

## Verifying the Snowflake Data Store in Qubole

To verify that the Snowflake data store was created and has been activated, click on the dropdown list in the upper-left of the **Explore** page. A green dot indicates that the data store has
been activated.

You should also verify that the table explorer widget in the left pane of the **Explore** page displays all of the tables in the Snowflake database specified in the data store.

## Query Pushdown in Qubole

Spark queries benefit from Snowflake’s automatic query pushdown optimization, which improves performance. By default, Snowflake query pushdown is enabled in Qubole.

For supported operations and limitations, see [Query pushdown](/user-guide/spark-connector-use#label-spark-pushdown).
