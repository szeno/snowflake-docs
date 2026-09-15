# Accessing data ingested by Snowflake Connector for Google Analytics Raw Data

This topic describes how to access raw data in Google Analytics from your Snowflake account.

For each property in BigQuery that is configured for synchronization, the Snowflake Connector for Google Analytics Raw Data creates:

- The `ANALYTICS_propertyId` table with the same name as the property name. This table contains the raw daily data. Each record in the table is stored in a separate row and the Google Analytics event data is saved into a single column of type VARIANT.
- The `ANALYTICS_propertyId__VIEW` view that maps the event data from the table above into separate columns.
- The `ANALYTICS_INTRADAY_propertyId` table with the same name as the property name. This table contains the raw intraday data.
- The `ANALYTICS_INTRADAY_propertyId__VIEW` view that maps the intraday event data from the table above into separate columns.
- The `USERS_propertyId` table with the same name as the property name. This table contains the raw users data.
- The `USERS_propertyId__VIEW` view that maps the users data from the table above into separate columns.
- The `PSEUDONYMOUS_USERS_propertyId` table with the same name as the property name. This table contains the raw pseudonymous users data.
- The `PSEUDONYMOUS_USERS_propertyId__VIEW` view that maps the users data from the table above into separate columns.

The temporary owner of the tables and views above is the Snowflake Connector for Google Analytics Raw Data. The ownership should be transferred during the Connector uninstallation, for details see [Uninstalling and reinstalling the Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-uninstalling-and-reinstalling).

The following sections explain how to grant the privileges to access this data and how to access the data from these tables and views.

## Granting privileges for accessing the Google Analytics data in Snowflake

After the Snowflake Connector for Google Analytics Raw Data synchronizes the data with Snowflake, you can use `data_owner_role` to access the data or any other role if it meets both of the following conditions:

- Has USAGE privilege on the database and schema that contain the data ingested by Snowflake Connector for Google Analytics Raw Data.
- Is granted with the DATA\_READER application role, which has SELECT privilege on tables or views within this schema.

For example, if you configured the Snowflake Connector for Google Analytics Raw Data to store the data in the `dest_db` database and
`dest_schema` schema, you can create the `google_analytics_raw_data_reader_role` role and grant the privileges
for accessing the data to that role.

The following example shows how to grant these privileges:

> Copy code
>
> ```
> CREATE ROLE google_analytics_raw_data_reader_role;
> GRANT USAGE ON DATABASE dest_db TO ROLE google_analytics_raw_data_reader_role;
> GRANT USAGE ON SCHEMA dest_db.dest_schema TO ROLE google_analytics_raw_data_reader_role;
> GRANT APPLICATION ROLE SNOWFLAKE_CONNECTOR_FOR_GOOGLE_ANALYTICS_RAW_DATA.DATA_READER TO ROLE google_analytics_raw_data_reader_role;
> ```

## Accessing the raw data

For each BigQuery table that you synchronize, the Snowflake Connector for Google Analytics Raw Data creates a new table with
the same name in the Snowflake database and schema used to store the Snowflake Connector for Google Analytics Raw Data.

For example, if you configured the connector to store data in the `dest_db` database and
`dest_schema` schema and access data via role `my_role`,
and if you configured the connector to synchronize the `analytics_12345` table in
BigQuery, the connector creates the table named `dest_db.dest_schema.analytics_12345`.

This table contains raw data ingested from BigQuery. The table contains the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| `raw` | VARIANT | The data for the record in raw form. |
| `run_id` | VARIANT | The id of the asynchronous process that ingested the data. |
| `source_table_date` | DATE | The name of the daily table from which the connector ingested the data to the table. |
| `ingestion_complete` | BOOLEAN | True if the connector ingested all the data from the daily table, false if some of the data is still being downloaded. |

Expand

Show lessSee more

The following is an example of the output for a SELECT statement that retrieves the data for the
`dest_db.dest_schema.analytics_12345` table:

> Copy code
>
> ```
> SELECT * FROM DEST_DB.DEST_SCHEMA.ANALYTICS_12345 LIMIT 5;
>
> +---------------------------+--------------------------------------+--------------------+--------------------+
> | RAW                       | RUN_ID                               |  SOURCE_TABLE_DATE | INGESTION_COMPLETE |
> +---------------------------+--------------------------------------+--------------------+--------------------+
> | { "app_info": null, ... } | f8edbf0e-1d0d-4ff5-9e5c-0e114b1fc44a |  2023-06-13        |  TRUE              |
> | { "app_info": null, ... } | f8edbf0e-1d0d-4ff5-9e5c-0e114b1fc44a |  2023-06-13        |  TRUE              |
> | { "app_info": null, ... } | f8edbf0e-1d0d-4ff5-9e5c-0e114b1fc44a |  2023-06-13        |  TRUE              |
> | { "app_info": null, ... } | d949ab70-6a7e-47a5-b876-d7e33d701b0d |  2023-06-14        |  FALSE             |
> | { "app_info": null, ... } | d949ab70-6a7e-47a5-b876-d7e33d701b0d |  2023-06-14        |  FALSE             |
> +---------------------------+--------------------------------------+--------------------+--------------------+
> ```

## Accessing the flattened data

For each table that contains data, the connector asynchronously creates a flattened view of the raw data, and refreshes it daily.
The name of the view is the name of the table with the suffix `__view`.
For example, for the table named `analytics_12345`, the connector creates
the `dest_db.dest_schema.analytics_12345__view` view.

Note

- There are no views for rows where `ingestion_complete` is `FALSE` .
- If the BigQuery column type changes, for the previously existing view, the view column is changed to type `VARIANT`.

The following is an example of the output for a SELECT statement that retrieves the data from the
`dest_db.dest_schema.analytics_12345__view` view. In this example, the `analytics_12345` table has `VARIANT` column `raw`
with values named `EVENT_DATE`, `EVENT_TIMESTAMP`, `EVENT_NAME`, and `EVENT_PREVIOUS_TIMESTAMP`.

> Copy code
>
> ```
> USE ROLE MY_ROLE;
> SELECT EVENT_DATE, EVENT_TIMESTAMP, EVENT_NAME, EVENT_PREVIOUS_TIMESTAMP
> FROM DEST_DB.DEST_SCHEMA.ANALYTICS_12345__VIEW LIMIT 5;
>
> +------------+--------------------------+-------------------+--------------------------+
> | EVENT_DATE | EVENT_TIMESTAMP          | EVENT_NAME        | EVENT_PREVIOUS_TIMESTAMP |
> +------------+--------------------------+-------------------+--------------------------+
> | 2023-06-13 | 2023-06-13 18:27:20.775  | "page_view"       | null                     |
> | 2023-06-13 | 2023-06-13 18:27:25.960  | "user_engagement" | null                     |
> | 2023-06-13 | 2023-06-13 19:26:49.130  | "scroll"          | null                     |
> | 2023-06-13 | 2023-06-13 18:27:51.135  | "page_view"       | null                     |
> | 2023-06-13 | 2023-06-13 18:27:56.343  | "user_engagement" | null                     |
> +------------+--------------------------+-------------------+--------------------------+
> ```
