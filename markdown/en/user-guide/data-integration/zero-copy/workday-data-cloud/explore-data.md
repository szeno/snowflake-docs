# Explore and query Workday Data Cloud data

This topic describes how to mount the Workday Data Cloud catalog as a catalog-linked database, discover the Workday tables, and query them in Snowflake.

The Zerocopy Connector must be in `CONNECTED` state before performing any of the steps in this topic. See [Set up the Workday Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/workday-data-cloud/setup).

## List available shares

To see what the connector makes available to mount, call `SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES`:

Copy code

```
SELECT SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES('my_db.my_schema.my_workday_connector');
```

The function returns a JSON array of the namespaces that the Workday catalog exposes. Snowsight calls the same function to populate the connector page.

## Create a catalog-linked database

Snowflake mounts the whole Workday catalog, so you name only the connector.

You can mount using the Snowsight UI or SQL.

### Using Snowsight

1. In Snowsight, select **Ingestion** » **Zero-Copy**.
2. Select your Workday connector to open the connector page.
3. Select **Mount all schemas**.

The catalog-linked database and its schemas are listed on the connector page.

### Using SQL

Create the catalog-linked database using the `LINKED_ZEROCOPY_CONNECTOR` clause. The role requires `CREATE DATABASE` on the account and `USAGE` on the connector. The owner of the catalog-linked database can be different from the owner of the connector.

Copy code

```
CREATE DATABASE my_workday_db
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_workday_connector',
    SYNC_INTERVAL_SECONDS = 86400  -- optional
  );
```

The database is created immediately and populated in the background, so the schemas and tables might not all be visible in the first few moments after the statement returns.

To confirm the database was created, use [SHOW DATABASES](/sql-reference/sql/show-databases):

Copy code

```
SHOW DATABASES LIKE 'MY_WORKDAY_DB%';
```

### Sync interval

`SYNC_INTERVAL_SECONDS` is optional. Use it to control how often Snowflake discovers structural changes in the Workday catalog, such as a new namespace or table. The value can range from 30 to 86400 seconds (1 day).

For Workday Data Cloud, Snowflake recommends 86400 seconds (1 day). The structure of the Workday catalog changes far less often than the data inside it, so a long discovery interval avoids polling that rarely finds anything new. The interval doesn’t affect the freshness of your query results, because Snowflake contacts Workday on each `SELECT`. For details, see [Refresh intervals](/user-guide/data-integration/zero-copy/workday-data-cloud/setup#label-workday-refresh-intervals).

To change the interval on an existing catalog-linked database, use `ALTER DATABASE ... UPDATE LINKED_ZEROCOPY_CONNECTOR`:

Copy code

```
ALTER DATABASE my_workday_db
  UPDATE LINKED_ZEROCOPY_CONNECTOR SET SYNC_INTERVAL_SECONDS = 86400;
```

Note

`UPDATE LINKED_ZEROCOPY_CONNECTOR` applies only to catalog-linked databases created from a Zerocopy Connector. Catalog-linked databases created from a catalog integration use `UPDATE LINKED_CATALOG` instead. The two forms are mutually exclusive.

## Explore the data

### Data model overview

Snowflake mirrors the structure of the Workday catalog. Each Workday namespace becomes a **schema** in the catalog-linked database, and each Workday table becomes a **table** in that schema.

### Discover schemas and tables

Copy code

```
SHOW SCHEMAS IN DATABASE my_workday_db;
```

To list the tables that Snowflake discovered in a schema:

Copy code

```
SHOW TABLES IN SCHEMA my_workday_db.my_schema;

SHOW ICEBERG TABLES IN SCHEMA my_workday_db.my_schema;
```

Inspect the columns of a table before querying it:

Copy code

```
SHOW COLUMNS IN TABLE my_workday_db.my_schema.my_table;
```

## Query the data

Query the tables exactly as you would any other Snowflake table. Snowflake contacts Workday on each `SELECT`, so every query is served fresh data from your Workday tenant rather than a cached copy.

Copy code

```
SELECT * FROM my_workday_db.my_schema.my_table LIMIT 10;

SELECT COUNT(*) FROM my_workday_db.my_schema.my_table;
```

Joins, views, and any other read query work normally, including joining Workday data to your own Snowflake tables:

Copy code

```
SELECT
  w.worker_id,
  w.job_profile,
  h.headcount_target
FROM my_workday_db.my_schema.workers w
JOIN my_planning_db.my_schema.headcount_plan h
  ON w.cost_center = h.cost_center;
```

Replace `my_workday_db`, the schema, and the table and column names with the actual values returned by `SHOW SCHEMAS` and `SHOW TABLES` in your environment.

Note

Catalog-linked databases are read-only. `INSERT`, `UPDATE`, `DELETE`, and DDL statements against these tables are rejected. Workday remains the system of record.

## Create table as select (CTAS)

To persist query results as a native Snowflake table for use in dashboards, ML models, or data sharing:

Copy code

```
CREATE DATABASE IF NOT EXISTS my_ctas_db;
USE DATABASE my_ctas_db;

-- Snapshot a Workday table into a native Snowflake table
CREATE OR REPLACE TABLE worker_snapshot AS
SELECT *
FROM my_workday_db.my_schema.workers;

SELECT * FROM worker_snapshot LIMIT 10;
```

Unlike the mounted tables, a table created this way is a copy. It doesn’t reflect later changes in Workday until you re-create or refresh it.

## Drop a catalog-linked database

The catalog-linked database must be dropped before you can disconnect or drop the connector. Catalog-linked databases don’t support `UNDROP`.

Copy code

```
DROP DATABASE my_workday_db;
```

For the full teardown sequence, see [Remove the integration](/user-guide/data-integration/zero-copy/workday-data-cloud/setup#label-workday-remove-integration).
