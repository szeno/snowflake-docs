# Setting up data ingestion for your Snowflake Connector for Google Analytics Raw Data

This topic describes how to access Snowflake Connector for Google Analytics Raw Data in your Snowflake account.

Note

Any single property can only be ingested from one GCP project at a time. Changing the project for a previously-configured property currently requires reinstalling the connector. This limitation will be removed in the future.

If you change the export settings for a property, and start exporting it into a different GCP project, you should also manually move data from the previous BigQuery instance, and consolidate it in the newly-configured one.

## Setting up data ingestion using Snowsight

To set up data ingestion using Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for Google Analytics Raw Data, then select the tile for the connector.
4. In the page for the Snowflake Connector for Google Analytics Raw Data, navigate to the **Data Sync** section.

   This displays a list of all the Google Analytics properties.
5. Select the properties you want to ingest:

   1. Search for the property you want to ingest.
   2. Select the checkbox in the **Status** column next to the property you want to select.
   3. Repeat these steps for each property you want to ingest into Snowflake.
6. Select the heading of the **Status** column to see the properties you have currently selected.
7. Select **Start sync** to begin ingesting data into your Snowflake account.

Selected properties appear in the properties list.

**Data Ingestion** status will be displayed in the top right corner of the **Manage data synchronization** section.

Data sync for each property will create two loads:

- Initial load, which ingests historical data. It starts with the current day and runs backward until the first day, for which data is available is reached.
- Present load, which ingests data from the current day and runs forward.

If you wish to only sync current data, you can do so via a worksheet.

Enabling a property using Snowsight will cause the connector to attempt ingestion for all possible export types. If you want to
ingest only specific export types, for example if you only have *events* tables in BigQuery, you can do so by using SQL statements.

Note

Once a property **with** an initial load is enabled, initial load can be disabled. On the other hand,
when a property is enabled **without** an initial load, initial load cannot later be enabled.

### Modifying data ingestion using Snowsight

To modify the Google Analytics tables to be ingested or the synchronization schedule for the tables, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the ACCOUNTADMIN role.
2. In the navigation menu, select **Catalog** » **Apps**.
3. Search for the Snowflake Connector for Google Analytics Raw Data, then select the tile for the connector.
4. In the page for the Snowflake Connector for Google Analytics Raw Data, navigate to the **Data Sync** section.
5. Select **Edit properties**.
6. Modify the tables you want to ingest:

   1. Search for the table you want to ingest.
   2. Select the checkbox in the **Status** column next to the table you want to select or deselect.
7. Select **Update data sync**.

## Setting up data ingestion using SQL statements

To set up data ingestion using SQL statements, do the following:

- [List the properties available for ingestion](#label-gard-connector-listing-properties).
- [Prepare destination database](#label-gard-connector-preparing-destination-database).
- [Enable ingestion of a property](#label-gard-connector-enabling-ingestion).

Note

To configure these settings, use stored procedures that are defined in the PUBLIC schema of
the database that serves as an instance of the connector installation database.

Before calling these stored procedures, select that database as the database to use for the session.

For example, if that database is named `snowflake_connector_for_google_analytics_raw_data`, run the following command:

Copy code

```
USE DATABASE snowflake_connector_for_google_analytics_raw_data;
```

### Listing the properties available for ingestion

To list all the available properties in a given GCP project, call the following stored procedure:

> Copy code
>
> ```
> CALL LIST_GA_PROPERTIES();
> ```

The result displays all the available projects and properties to ingest by an authorized account. If no results are returned please check:

- If the data export from Google Analytics to BigQuery is configured.
- If exported data is visible in BigQuery.
- If proper roles are assigned to the used Service Account / authenticated user.

Please be advised that it can take up to 24 hours between setting up the data export and storing data in BigQuery.
This delay can be a cause for the `LIST_GA_PROPERTIES` procedure producing no results.

Turning the Google Analytics export off does not mean the property is omitted by `LIST_GA_PROPERTIES`.
Even though the export was turned off, data can still persist in BigQuery and can be synchronized by the connector.

### Preparing destination database

Before enabling the ingestion, you need to grant the connector access to creating tables and views inside your destination database and schema.

> Copy code
>
> ```
> GRANT USAGE ON DATABASE <destination database> TO APPLICATION <application name>;
>
> GRANT USAGE ON SCHEMA <destination database>.<destination schema> TO APPLICATION <application name>;
>
> GRANT CREATE TABLE ON SCHEMA <destination database>.<destination schema> TO APPLICATION <application name>;
>
> GRANT CREATE VIEW ON SCHEMA <destination database>.<destination schema> TO APPLICATION <application name>;
> ```

### Enabling or disabling the ingestion of a property

To enable or disable the synchronization of data for a specific property in Google Analytics, call the `ENABLE_PROPERTIES`
stored procedure with the following arguments:

> Copy code
>
> ```
> CALL ENABLE_PROPERTIES('<gcp_project>', ['<properties_to_configure>'], <enable_initial_load>, <exclude_nulls>, <disable_auto_reloads>, <disable_present_load>, <enabled_export_types>);
> ```

Where:

`gcp_project`
:   Specifies the GCP project of the enabled properties.

`properties_to_configure`
:   Specifies a comma-delimited list of Google Analytics property names in single quotation marks.

    Use the property name without the `analytics_` prefix.

`enable_initial_load`
:   A boolean indicating whether to enable or disable the initial data load, which ingests all historical data for a property in parallel to the current sync.

    This is an optional argument and the default value for it is `true`.

    When a property was previously enabled, this flag is ignored, and ingestion will continue from the point when it stopped when the property was disabled.

`exclude_nulls`
:   Optional boolean indicating whether to exclude fields containing null values from the ingested data. Setting this parameter to `true`
    can improve the data ingestion throughput. Default value is `false`.

`disable_auto_reloads`
:   An optional boolean indicating whether to disable automatic reloads. For more information about automatic reload, see [Data ingestion model for the Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-data-ingestion-model).
    Setting this value to `true` can reduce credit consumption, but late data won’t be ingested into Snowflake. This property cannot be set to `true` for the `FRESH_DAILY` export type.
    Default value is `false`.

`disable_present_load`
:   An optional boolean indicating whether to disable scheduled ingestion. For more information about scheduling, see [Data ingestion model for the Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-data-ingestion-model).
    When setting this value to `true`, data will only be ingested into Snowflake if you trigger a reload manually.
    Manual reloads can still trigger automatic reloads unless you also set `disable_auto_reloads` to `true`.
    The initial load still runs unless you set `enable_initial_load` to `false`. The default value of `disable_present_load` is `false`.

`enabled_export_types`
:   An optional list of export types, which connector will try to ingest data for. Possible values are: `DAILY`, `FRESH_DAILY`, `INTRADAY`, `USERS` and `PSEUDONYMOUS_USERS`.
    By default, all export types, except `FRESH_DAILY`, will be enabled.

For example, to enable the synchronization of the properties named `property1`, `property2`, and `property3` in the project `gcp_example_project`, run
the following query:

> Copy code
>
> ```
> CALL ENABLE_PROPERTIES(PROJECT_ID => 'gcp_example_project', PROPERTY_IDS => ['property1','property2','property3']);
> ```

To enable properties without the initial data loading, use the following query:

> Copy code
>
> ```
> CALL ENABLE_PROPERTIES(PROJECT_ID => 'gcp_example_project', PROPERTY_IDS => ['property1','property2','property3'], INITIAL_LOAD => FALSE);
> ```

If you only have daily and user data in BigQuery, you can explicitly omit the intraday export by running the following query:

> Copy code
>
> ```
> CALL ENABLE_PROPERTIES(PROJECT_ID => 'gcp_example_project', PROPERTY_IDS => ['property1'], ENABLED_EXPORT_TYPES => ['DAILY', 'FRESH_DAILY', 'USERS', 'PSEUDONYMOUS_USERS']);
> ```

Snowflake recommends using named arguments so that you can specify the arguments you want and leave the rest unchanged.
For example, to enable properties with the initial load and exclude fields containing null values, run the following query:

> Copy code
>
> ```
>  CALL ENABLE_PROPERTIES(
>     PROJECT_ID => 'gcp_example_project',
>     PROPERTY_IDS => ['property1', 'property2', 'property3'],
>     INITIAL_LOAD => TRUE,
>     EXCLUDE_NULLS => TRUE
> );
> ```

To prevent these properties from being ingested, run the following command:

> Copy code
>
> ```
> CALL DISABLE_PROPERTIES('gcp_example_project', ['property1','property2','property3']);
> ```

Disabling the property stops its synchronization. When the property synchronization is disabled, the whole ingestion that started, but not finished yet is removed from the destination database.

The `ENABLE_PROPERTIES` procedure adds the specified property names to the `ENABLED_PROPERTIES` view.

## Initial load

After enabling a new property, the connector starts ingesting all historical data found in BigQuery in parallel to the current sync responsible for collecting new events.
The initial load runs backwards, starting from the current day until the first day for which data is available is reached.

## Reloading already ingested data

To reload already ingested data, or to load data that has not been ingested at all (e.g. because you enabled property without initial load, or data was absent in BigQuery and now it’s available) you can call one of the following procedures:

> Copy code
>
> ```
> CALL RELOAD_PROPERTY('<property id>');
> ```
>
> This procedure triggers reload of all data (`DAILY`, `FRESH_DAILY`, `INTRADAY`, `USERS` and `PSEUDONYMOUS_USERS`) of a given property, between the earliest table it can find in BigQuery and the last ingested (or terminally marked as `DATA_NOT_FOUND`) table date between the connector.
>
> Copy code
>
> ```
> CALL RELOAD_PROPERTY('<property id>', <first date>, <last date>);
> ```
>
> Triggers reload of all data (`DAILY`, `FRESH_DAILY`, `INTRADAY`, `USERS` and `PSEUDONYMOUS_USERS`) of a given property, between provided dates.
>
> Copy code
>
> ```
> CALL RELOAD_PROPERTY('<property id>', '<export type>', <first date>, <last date>);
> ```
>
> Triggers reload of `DAILY`, `FRESH_DAILY`, `INTRADAY`, `USERS` or `PSEUDONYMOUS_USERS` data of a given property, between provided dates.

Note

- Reload is processed in parallel to main load.
- You can trigger as many reloads of a property, as you want, as long as date ranges do not overlap.
- Data is swapped after downloading each table from BigQuery.
- Reload swaps data only if there is data in BigQuery for a particular day.

Ongoing reloads can be observed via a dedicated view:

> Copy code
>
> ```
> SELECT * FROM PUBLIC.ONGOING_RELOADS;
> ```

To cancel an ongoing reload, execute the following query:

> Copy code
>
> ```
> CALL CANCEL_RELOAD_PROPERTY('<load id>');
> ```
