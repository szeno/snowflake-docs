# Accessing fetched Google Analytics data

## Overview

For each report that is configured for synchronization, the connector creates the following table and view
in the destination database and destination schema:

- `report_name__RAW`: A table that contains data in a raw form, where each row contains a Google Analytics
  record in a single VARIANT column.
- `report_name`: A view that contains flattened data, where each row contains a Google Analytics
  dimension or metric in a separate column.

## Accessing the raw data

For each synchronized Google Analytics report, the connector creates a new table
with the `report_name__RAW` name in the Snowflake database and schema used to store the Google Analytics data.

For example, if you configure the connector to store the Google Analytics data in the `dest_db` database
and `dest_schema` schema and to synchronize the `my_report` report, the connector
creates the table `dest_db.dest_schema.my_report__raw`.

This table contains raw data ingested from Google Analytics in the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `DATE` | DATE | The value of the `date` dimension for a record from Google Analytics |
| `RAW` | VARIANT | The data for a record from Google Analytics in raw form |
| `LAST_UPDATE_DATE` | TIMESTAMP\_NTZ | The last time a record was updated in Snowflake |

Expand

Show lessSee more

The following example SELECT statement retrieves data from the `dest_db.dest_schema.my_report__raw` table:

> Copy code
>
> ```
> SELECT * FROM DEST_DB.DEST_SCHEMA.MY_REPORT__RAW;
> ```

## Accessing the flattened data

In addition, for each table that contains data, the connector creates a flattened view of the raw data.
The name of the view is the name of the table without the `__RAW` suffix. For example, for the table
named `dest_db.dest_schema.my_report__raw`, the connector creates the view named `dest_db.dest_schema.my_report`.

The view contains flattened records from Google Analytics, where each dimension and metric is stored in a separate column.

The following is an example of a SELECT statement that retrieves data from the `dest_db.dest_schema.my_report` view:

> Copy code
>
> ```
> SELECT * FROM DEST_DB.DEST_SCHEMA.MY_REPORT;
> ```

Note

The flattened view is created only after an entire dataset is fetched from the GA API.
Larger reports might take more time.
