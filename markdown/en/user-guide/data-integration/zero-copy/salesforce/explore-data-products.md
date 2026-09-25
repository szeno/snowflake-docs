# Explore data products from Salesforce Data Cloud

This topic describes how to list available Salesforce data products, mount them as catalog-linked databases, and query the shared data in Snowflake.

Before performing the steps in this topic:

- The Zerocopy Connector must be in `CONNECTED` state. See [Set up the Salesforce Data Cloud Zerocopy Connector](/user-guide/data-integration/zero-copy/salesforce/setup).
- Your Salesforce administrator must have created and linked at least one Data Share to the connector. See [Set up Salesforce Data Cloud for Zero-Copy](/user-guide/data-integration/zero-copy/salesforce/setup-salesforce).

## List shared data products

After your Salesforce administrator links a Data Share to the Snowflake V2 Data Share Target, call `SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES` to see what’s available:

Copy code

```
SELECT SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES('my_db.my_schema.my_sfdc_connector');
```

The function returns a JSON array. Each element represents one shared data product. The `name` field is the value you pass as `SHARE_NAME` or `SHARE_NAME_FILTER` when creating a catalog-linked database.

```
[
  {
    "name": "contact_v1",
    "status": "UNMOUNTED",
    "catalog_linked_databases": []
  },
  {
    "name": "opportunity_v1",
    "status": "MOUNTED",
    "catalog_linked_databases": [ { "name": "MARKETINGSHARE" } ]
  }
]
```

The `status` field indicates whether the data share is available to mount or already mounted:

| Status | Description |
| --- | --- |
| `UNMOUNTED` | Shared by Salesforce Data Cloud. No catalog-linked database has been created yet. |
| `MOUNTED` | A catalog-linked database exists for this share. |

Expand

Show lessSee more

To parse the output into a tabular format:

Copy code

```
WITH raw AS (
  SELECT PARSE_JSON(
    SYSTEM$ZEROCOPY_CONNECTOR_LIST_SHARES('my_db.my_schema.my_sfdc_connector')
  ) AS json_data
)
SELECT
  f.value:name::STRING                                              AS share_name,
  f.value:status::STRING                                           AS status,
  CASE
    WHEN ARRAY_SIZE(f.value:catalog_linked_databases) > 0
    THEN f.value:catalog_linked_databases[0]:name::STRING
    ELSE NULL
  END                                                              AS mounted_database
FROM raw,
LATERAL FLATTEN(INPUT => json_data) f;
```

## Create a catalog-linked database

Mounting a share creates a catalog-linked database that contains the shared data as queryable schemas. Snowflake automatically creates views on top of them.

You can mount using the Snowsight UI or SQL.

### Using Snowsight

1. In Snowsight, navigate to **Ingestion** » **Zero-Copy**.
2. Select the **Available connectors** tab and click your Salesforce connector.
3. On the **Catalog linked databases** tab, click **Mount all data shares**.

The catalog-linked database is created immediately.

### Using SQL

Copy code

```
-- (Recommended) Mount all shares — each share becomes a schema
CREATE DATABASE my_sfdc_db
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_sfdc_connector',
    ALL_SHARES = TRUE
  );

-- Mount a filtered set of shares
CREATE DATABASE my_sfdc_db
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_sfdc_connector',
    SHARE_NAME_FILTER = ('share1', 'share2')
  );

-- Mount a single share
CREATE DATABASE my_sfdc_db
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_sfdc_connector',
    SHARE_NAME = 'my_share'
  );

-- Mount all shares, setting the optional properties
CREATE DATABASE my_sfdc_db
  LINKED_ZEROCOPY_CONNECTOR = (
    CONNECTOR_NAME = 'my_db.my_schema.my_sfdc_connector',
    ALL_SHARES = TRUE,
    SYNC_INTERVAL_SECONDS = 300,
    LEGACY_SALESFORCE_SCHEMA_ALIAS = FALSE,
    SALESFORCE_USER_FRIENDLY_NAME = TRUE
  );
```

`LEGACY_SALESFORCE_SCHEMA_ALIAS` and `SALESFORCE_USER_FRIENDLY_NAME` apply only
to a Salesforce connector, and you can set them only when you create the
database.

The following properties are all optional:

| Property | Default | Description |
| --- | --- | --- |
| `SYNC_INTERVAL_SECONDS` | `300` (5 minutes) for a Salesforce connector | How often automatic table discovery looks for structural changes in the Salesforce catalog, such as a new data share. The value can range from 30 to 86400 seconds (1 day). Unlike the other two properties, you can change this one after creation with `ALTER DATABASE <cld_name> UPDATE LINKED_ZEROCOPY_CONNECTOR SET SYNC_INTERVAL_SECONDS = <seconds>`. |
| `LEGACY_SALESFORCE_SCHEMA_ALIAS` | `FALSE` | If `TRUE`, also exposes each mounted share under its Data Cloud V1 schema name, `schema_<share_name>`, so that a three-part reference written against the database created from the legacy target still resolves after you swap in the catalog-linked database. For more information, see [Migrate from the legacy Snowflake data share target](/user-guide/data-integration/zero-copy/salesforce/migrate-legacy-share). |
| `SALESFORCE_USER_FRIENDLY_NAME` | `TRUE` | If `TRUE`, also exposes a short-named view for each object, with the object-type suffix (`__dll`, `__dlm`, or `__cio`) removed from the view name and the `__c` suffix removed from the column names. For example, `Case_Home__dll` is also available as `Case_Home`, and its `AccountId__c` column as `AccountId`. |

Expand

Show lessSee more

To confirm the database was created:

Copy code

```
SHOW DATABASES LIKE 'MY_SFDC_DB%';
```

## Explore the data

### Data model overview

When you mount a share, each data share appears as a **schema** within the catalog-linked database. Within each schema, Salesforce data objects are exposed as **views**.

### Discover schemas and views

Copy code

```
-- Data shares are mounted as schemas in the catalog-linked database
SHOW SCHEMAS IN DATABASE my_sfdc_db;

-- Views are the queryable layer — use these for all queries
SHOW VIEWS IN SCHEMA my_sfdc_db.my_share_schema;

-- Inspect columns before querying
SHOW COLUMNS IN VIEW my_sfdc_db.my_share_schema.ssot__Account__dlm;
```

Note

Views are created shortly after the catalog-linked database is mounted. If `SHOW VIEWS` returns no results immediately, wait for 1 minute and try again.

### Query the data

Query Salesforce data via the views in each schema. The view names are determined by what your Salesforce administrator included in the Data Share.

Copy code

```
-- Query a Data Lake Object (DLO)
SELECT * FROM my_sfdc_db.my_share_schema.Case_Home__dll LIMIT 10;

-- Query a Data Model Object (DMO)
SELECT * FROM my_sfdc_db.my_share_schema.ssot__PriceBook__dlm LIMIT 10;

-- Query a Calculated Insights Object (CIO)
SELECT * FROM my_sfdc_db.my_share_schema.Product_Sku_Aggregation__cio LIMIT 10;
```

Replace `my_sfdc_db`, `my_share_schema`, and the view names with the actual values returned by `SHOW SCHEMAS` and `SHOW VIEWS` in your environment.

## Create table as select (CTAS)

To persist query results as a native Snowflake table for use in dashboards, ML models, or data sharing:

Copy code

```
CREATE DATABASE IF NOT EXISTS my_ctas_db;
USE DATABASE my_ctas_db;

-- Snapshot a Salesforce data model object into a native Snowflake table
CREATE OR REPLACE TABLE account_snapshot AS
SELECT *
FROM my_sfdc_db.my_share_schema.ssot__Account__dlm;

SELECT * FROM account_snapshot LIMIT 10;
```

## Drop a catalog-linked database

All catalog-linked databases must be dropped before you can disconnect or drop the connector.
Catalog-linked databases do not support `UNDROP`.

Copy code

```
DROP DATABASE my_sfdc_db;
```
