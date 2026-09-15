Note

The Snowflake Connector for ServiceNow® is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms).

# Tutorial: Snowflake ServiceNow® data ingestion connector installation

## Introduction

Use this tutorial to configure and understand the Snowflake Connector for
ServiceNow® using the Snowsight wizard, select some tables, ingest data, and run an example query.

This tutorial is not meant to be exhaustive. Please review
[About the Snowflake Connector for ServiceNow®](/connectors/servicenow/about) for full functionality and limitations.

Note

This tutorial assumes you do not have a ServiceNow® account, so it guides you through
the steps of creating a developer account. If you do have a Servicenow® account,
feel free to try it out, with the caveat that the Snowflake connector for ServiceNow®
is subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms).

### Prerequisites

Before beginning this tutorial please ensure that you have met the following requirements:

- `ORGADMIN` rights to Accept the Terms of Service in the Snowflake Marketplace.
- `ACCOUNTADMIN` rights on the Snowflake account where you want to install the connector.

### What you’ll learn

In this tutorial you’ll learn how to:

- How to set up the Snowflake Connector for ServiceNow®.
- How to ingest ServiceNow® data into Snowflake
- How to stop the connector to avoid unnecessary costs in a development environment.

### What you’ll need

- [A Snowflake account](https://snowflake.com/)
- [A ServiceNow® developer account](https://developer.servicenow.com/dev.do/)

### What you’ll build

A ServiceNow® to Snowflake ingestion data flow.

## Set up the ServiceNow® developer instance

If you do not want to test this connector on your ServiceNow® account, you can use a
developer instance. This section describes how to set up a developer instance.

1. Go to the [ServiceNow® developer website](https://developer.servicenow.com), and create a developer user.
2. Log on to the developer website with your newly created user and select **Create an Instance**.
3. Choose an instance type. You’ll receive an email with your instance URL, and your user and password.

Deployment is usually pretty quick, around five minutes. But, while you wait, let’s go to the next step and configure Snowflake!

## Create and set up the Snowflake account

### Create a Snowflake account

If you do not have a Snowflake account, you can get a free trial at [snowflake.com](https://www.snowflake.com/en/).
Select **Start for Free** and follow the instructions.

### Accept the Terms & Conditions

1. Log on to your Snowflake account through the Snowsight web interface and change to the `ORGADMIN` role.
2. In the navigation menu, select **Admin** » **Terms**.
3. In the **Snowflake Marketplace** section, review the Consumer Terms of Service.
4. If you agree to the terms, select **Accept Terms & Conditions**.

### Set up a virtual warehouse

Connectors require a virtual warehouse. To create the required warehouse perform the following:

Change to the `ACCOUNTADMIN` role.

1. Navigate to **Admin -> Warehouses** and select **+ Warehouse**.
2. Specify `CONNECTOR_UI_WH` as warehouse name, size XS, and, and leaving all other the defaults.
3. Select **Create Warehouse**.

### Install the ServiceNow® connector

The connector is delivered through the Snowflake Marketplace, and is available to all Snowflake customers.
Once chosen, it is installed into your account as an application with several views and stored procedures.

1. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
2. In the search window, enter `ServiceNow` and select the tile.
3. Review the business needs and usage samples.
4. Select **Get**.
5. Select the warehouse previously created, `CONNECTOR_UI_WH`.
6. Select **Options**.
7. For this tutorial, accept the default name for the installation database, `Snowflake_Connector_for_ServiceNow`. Do not select any additional roles.
8. Select **Get**. `Snowflake Connector for ServiceNow` will display indicating the connector is now ready to use.
9. Select **Done**. Manage options will be specified it in the next section.

Next, check that the connector was installed. From Snowsight, go to **Data Products -> Apps**. You should see a new installed application with the name **Snowflake\_Connector\_for\_ServiceNow**.

Navigate to the public schema in **Data -> Databases**, and examine the newly available views and procedures.

## Complete all the prerequisites

Launch the Snowflake Connector for ServiceNow® from the **Data Products -> Apps -> Snowflake Connector for ServiceNow**.
You will be presented with a list of tasks that need to be completed before the connector can start data ingestion.
Please read the following descriptions carefully and complete each.

One of the final steps asks you to create an application registry if you want to
enable OAuth2 authentication. The next several steps will focus on this.

For the next section, we suggest you open two browser tabs so that you can copy certain data from Snowflake to ServiceNow®:

- From the Snowflake, use the connector to generate the redirect URL which will be pasted into the Application Registry.
- From the ServiceNow®, you’ll need the Application Registry to provide the Client ID and secret, which you then paste into Snowflake.

### On Snowflake

1. Copy the redirect URL. You will need it in the next section.
2. Open a new tab in your browser (without closing the above) and follow the steps in the next section.

### On ServiceNow®

1. Log in to your ServiceNow® developer instance.
2. From the main page, select **All** and search **Application Registry**.
3. Select **New** in the upper right-hand side of the window.
4. Select **Create an OAuth API endpoint for external clients**.
5. Give the endpoint a name, such as **Snowflake\_connector**. Leave the client secret blank, as the value populates automatically later in the procedure.
6. Paste in the redirect URL that was generated on the Snowflake side.
7. Select **Submit**. The window closes.
8. Select the registry you just created to re-open it.
   Note that the **Client ID** and **Client secret** are auto-generated.

   Don’t close the ServiceNow® browser tab or store the **Client ID** and **Client secret** in some safe place, they will be needed later.

   Return to the Snowflake configuration tab.

## Configure the connector

1. Select **Start configuration**.
   This Configure screen displays. By default, the fields are set to the names of objects that were created when you configured the connector.
   You can also use existing objects. The virtual warehouse selected will be used by the connector for background data ingestion.
2. Review [Configure the Snowflake Connector for ServiceNow®](/connectors/servicenow/installing-snowsight#label-servicenow-connector-configuring-snc-v2) for more information.
3. Select **Configure**.

Note that it can take a few minutes for the configuration process to complete.

Note

This step created a Large warehouse with its auto suspension set to ten minutes.
If you set to refresh every hour, the Large warehouse (8 credits/hour) will
wake up for a minimum of 10 minutes every hour. For this tutorial, this is not
needed. In the navigation menu, select **Compute** » **Warehouses** » **SERVICENOW\_WAREHOUSE** » **…** » **Edit**,
and change this to an XSMALL, and the auto timeout to one minute. In a real-life
use case, a Large warehouse size is often needed.

Note

You should attach a resource monitor to the `SERVICENOW_WAREHOUSE`. To attach
a resource monitor, In the navigation menu, select **Admin** » **Cost management**, and then select **Resource Monitors**.
Create a warehouse resource monitor.

## Set up the Snowflake to ServiceNow® OAuth2 hand-shake

1. Select **OAuth2** as an authentication method.
2. Fill in the ServiceNow® instance details. This is the first part of the ServiceNow® URL for your ServiceNow® account, **without** `https://*` protocol and the trailing `service-now.com`.
3. Paste the **Client id** and the **Client secret** from ServiceNow® into the Snowflake wizard.
4. Select **Connect**. Your ServiceNow® accounts pops up and requests to connect to Snowflake.
5. Select **Allow**. The connection is established between the two systems.

To verify the connection, select the three dots […] and **View Details**. At the top of the pop-up you will see the date **ServiceNow** authenticated.

Note

If you are having issues, perhaps the Client secret wasn’t copied. Unlock the password field and copy and paste the text.

## Configure deletions sync

If you want not only inserts and updates, but also deletes to be synchronized to Snowflake, you have to provide name of the journal table.
By default ServiceNow® uses `sys_audit_delete` table to store information about deleted records so feel free to provide this name.
If you don’t care about deletes, you can leave this field empty.

Select **Validate** to check if the connector is able to connect to the source system and has access to all the required tables.
It can take a few minutes for the process to complete.
When it’s done, select **Define data to sync** to select tables for the ingestion.

## Select ServiceNow® tables

Note

Be aware that:

- The connector can only ingest tables with `sys_id` columns present.
- ServiceNow® views are not supported. Instead of ingesting these views, you should synchronize all tables for the underlying view and join the synchronized tables in Snowflake.
- Incremental updates occur only for tables with `sys_updated_on` or `sys_created_on` columns.
- For tables that do not have `sys_updated_on` or `sys_created_on` columns, the connector uses `truncate and load` mode. In this mode, the table is always ingested using the initial load approach, and newly ingested data replaces the old data.

1. In the **Snowflake Connector for ServiceNow** window, on the top bar, select **Data Sync**.
2. To be able to run our test query later, we need to ingest a couple of tables. From the search window enter **incident** and check the box next to it and choose a 30 minute sync time.
3. To choose other tables, clear the search, put the table name and select the checkbox. Do this at least for the `task` table.

> Note
>
> Hint: Clear the search fields, and then select the title **Status** to sort and show all the tables you selected.

1. Select **Start Sync**. The select window closes and you get the message **Syncing Data** from the main Connector window. In addition to the tables you choose, three system tables will also be loaded. These are necessary to build the views on the raw data: `sys_dictionary`, `sys_db_object`, and `sys_glide_object`.

You receive a message indicating success. It appears once at least one table has been fully ingested.

Note

Don’t stop the ingest prematurely. Ensure that views are built in the destination database first.

## Connector Monitoring

Open a worksheet to examine the connector status.
Here are some examples of SQL queries you can execute to get monitoring
information:

Copy code

```
// Return general information about all ingestions
SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.public.connector_stats;
// Search for information about particular table ingestions
SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.public.connector_stats WHERE table_name = '<table_name>';
// Examine connector configuration
SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.public.connector_configuration;
// Calculate ingested data volume
SELECT
    table_name,
    sum(ingested_rows) AS row_count
FROM SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.public.connector_stats
GROUP BY table_name
ORDER BY table_name;
// General connector statistics
SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.public.connector_overview;
```

## Configuring access to the ingested data

The connector exposes the `DATA_READER` application role. This role has read access to all the ingested data in the destination schema.
It’s automatically granted to the role provided during the **Configure** step of the installation process.
It was named `SERVICE_NOW_RESOURCES_PROVIDER` in the screenshot earlier in this guide.
You can grant either application role or account role further if needed.

## Query the data

Examine the tables that the connector has created under the destination schema of the destination database.
For each table in ServiceNow® that is configured for synchronization, the connector creates the following table and views:

- A table with the same name that contains the data in raw form, where each record is contained in a single `VARIANT` column.
- A view named `table_name__view` that contains the data in flattened form, where the view
  contains a column for each column in the original table and a row for each record that is present in the original table.

Note

After you start the connector, it takes some time for the views to be created. The creation
of the views relies on data in the ServiceNow® `sys_db_object`, `sys_dictionary`
and `sys_glide_object` tables. The connector loads metadata from these ServiceNow®
tables after you enable any table for synchronization. It can take some time for the connector
to load this metadata. Do not stop the warehouse while views are being created.

- A view named `table_name__view_with_deleted` that contains the same
  data as `table_name__view` as well as rows for records that have been deleted in ServiceNow®.
- A table `table_name__event_log` that contains the history of changes fetched by the connector from ServiceNow®.

> To query from the raw data, review [Access the raw data](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-raw-v2). To
> query the views (recommended), review [Access the flattened data](/connectors/servicenow/accessing-data#label-servicenow-connector-accessing-data-flattened-v2).

### Query to identify number of incidents raised by month and priority

Here’s a test query to identify the number of incidents raised by
month and priority. Other example queries are provided on the Snowflake Connector
for ServiceNow® page in the Marketplace.

Copy code

```
USE ROLE SERVICE_NOW_RESOURCES_PROVIDER;
USE DATABASE SERVICENOW_DEST_DB;
USE SCHEMA DEST_SCHEMA;
WITH T1 AS (
    SELECT
    DISTINCT
        T.NUMBER AS TICKET_NUMBER,
        T.SHORT_DESCRIPTION,
        T.DESCRIPTION,
        T.PRIORITY,
        T.SYS_CREATED_ON AS CREATED_ON,
        T.SYS_UPDATED_ON AS UPDATED_ON,
        T.CLOSED_AT
    FROM TASK__VIEW T
    LEFT JOIN INCIDENT__VIEW I
        ON I.SYS_ID = T.SYS_ID -- ADDITIONAL INCIDENT DETAIL
   WHERE I.SYS_ID IS NOT NULL -- THIS CONDITION HELPS KEEP JUST THE INCIDENT TICKETS
)
SELECT
 YEAR(CREATED_ON) AS YEAR_CREATED,
 MONTH(CREATED_ON) AS MONTH_CREATED,
 PRIORITY,
 COUNT(DISTINCT TICKET_NUMBER) AS NUM_INCIDENTS
FROM T1
GROUP BY
    YEAR_CREATED,
    MONTH_CREATED,
    PRIORITY
ORDER BY
    YEAR_CREATED,
    MONTH_CREATED,
    PRIORITY
;
```

## Granting access to the connector

The connector exposes two application roles beyond the one used to access the data in destination database:

- The `VIEWER` role has read only access to the connector configuration and state
- The `ADMIN` role that can modify connector configuration and enable/disable ingestion

To monitor errors, run stats, examine connector stats, and examine enabled tables, you
can set up a ServiceNow® monitoring role that allows access to the views and read
only procedures in the connector database.

For example, run the following in a worksheet (and then use the role):

Copy code

```
USE ROLE accountadmin;
CREATE ROLE IF NOT EXISTS servicenow_monitor_role;
GRANT APPLICATION ROLE SNOWFLAKE_CONNECTOR_FOR_SERVICENOW.viewer TO ROLE servicenow_monitor_role;
GRANT USAGE ON WAREHOUSE SERVICENOW_WAREHOUSE TO ROLE servicenow_monitor_role;
```

## Stop the Ingestion

During this tutorial, we’re only ingesting the data, so it makes sense to stop the ingestion
after that initial load. However, in a production environment, you would not stop the connector.

Note

If you do not stop the connector, it will wake up the virtual warehouse at the specified time interval and consume credits.

1. In Snowsight, select the **Snowflake Connector for ServiceNow** tile.
2. In the **Snowflake Connector for ServiceNow** window, select **Pause Connector**.

## Uninstall the connector (but not the data)

If you have completed the tutorial or for any reason no longer need the connector you can easily uninstall it via the Snowflake Marketplace.

1. Select **Data Products** and then **Apps**.
2. Select three dots icon in the item on the list representing the connector app.
3. Select **Uninstall**.
4. Decide if you want to delete the objects owned by the application (tables and views with ingested data in the destination schema) or transfer ownership of them to another role.
5. Select **Uninstall**.

## Conclusion And Resources

Congratulations! You’ve successfully installed and configured the Snowflake Connector
for ServiceNow®, ingested data and ran a query to gather insights on incidents and priority.

What you learned

- How to set up the Snowflake Connector for ServiceNow®.
- How to ingest ServiceNow® data into Snowflake.
- How to stop the connector to avoid unnecessary costs in a development environment.

### Related Resources

- [Introducing the Snowflake Native Application Framework](https://www.snowflake.com/blog/introducing-snowflake-native-application-framework/)
- [About the Snowflake Connector for ServiceNow®](/connectors/servicenow/about)
