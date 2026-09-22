# Openflow Connector for Salesforce Bulk API: Iceberg table destinations

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Openflow Connector for Salesforce Bulk API supports writing to Snowflake-managed Apache Apache Iceberg™ tables as an opt-in destination format. The connector supports Iceberg v2 and v3. Existing connectors that write to standard Snowflake tables aren’t affected.

To use Iceberg table destinations, configure the Snowflake destination database with Iceberg defaults, then set the connector’s **Table Storage Format** parameter to `ICEBERG` and choose an **Iceberg Version** before the connector creates destination tables.

## Prerequisites

Before you begin:

- Complete the steps in [Openflow Connector for Salesforce Bulk API: Set up Snowflake](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-snowflake).
- Choose either Snowflake storage or an external volume in your cloud storage for the Iceberg table files.

## Configure the destination database

Configure the destination database with Iceberg defaults before starting the connector. The connector reads the database defaults for the external volume and storage serialization policy when it creates Iceberg tables.

### Option A: Snowflake storage

To use [Snowflake storage for Apache Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage), configure the database with `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`:

Copy code

```
ALTER DATABASE <my_salesforce_db> SET
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

With Snowflake storage, Snowflake stores and manages the Iceberg table files. You don’t need to configure external cloud storage or grant access to an external volume.

### Option B: External volume in your cloud storage

To store the Iceberg table files in your cloud storage, configure the database with the external volume:

Copy code

```
ALTER DATABASE <my_salesforce_db> SET
  EXTERNAL_VOLUME = '<external_volume>'
  STORAGE_SERIALIZATION_POLICY = <COMPATIBLE|OPTIMIZED>;
```

`COMPATIBLE` produces Parquet files readable by external engines. `OPTIMIZED` enables Snowflake-specific query optimizations. Choose based on your data query needs. For more information, see [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#storage-serialization-policy).

Grant the execute-as role (which your service user also holds under `KEY_PAIR` authentication)
`USAGE` on the external volume:

Copy code

```
GRANT USAGE ON EXTERNAL VOLUME <external_volume> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

This grant isn’t required when you use Snowflake storage (`EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'`).

Note

`CATALOG = 'SNOWFLAKE'` is set automatically by the connector when it creates Iceberg tables. Don’t set it at the database level.

## Configure the connector

Set the following destination parameters before the connector creates destination tables:

- **Table Storage Format**: Set to `ICEBERG`. The default is `STANDARD`.
- **Iceberg Version**: Set to `2` or `3`. The default is `3`.

Don’t change **Table Storage Format** or **Iceberg Version** after ingestion begins. To switch between standard and Iceberg destinations, or between Iceberg v2 and v3, recreate the connector and perform a fresh load into new destination tables.

For the full connector configuration workflow, see [Openflow Connector for Salesforce Bulk API: Configure the connector](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/configure-connector).

## Verify Iceberg table creation

After the initial load completes, verify that the destination tables were created as Iceberg tables:

Copy code

```
SELECT GET_DDL('TABLE', '<my_salesforce_db>.<my_salesforce_schema>.<object_table>');
```

The returned DDL should include `ICEBERG TABLE`.

You can also verify the database-level Iceberg defaults:

Copy code

```
SHOW PARAMETERS LIKE 'EXTERNAL_VOLUME' IN DATABASE <my_salesforce_db>;
SHOW PARAMETERS LIKE 'STORAGE_SERIALIZATION_POLICY' IN DATABASE <my_salesforce_db>;
```

## Limitations and behavior

- **Tri-Secret Secure accounts and Snowflake storage**: Accounts with Tri-Secret Secure (TSS) enabled may be unable to create new Snowflake-managed Iceberg tables that use [Snowflake storage for Apache Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage). For details, see [Encryption](/user-guide/tables-iceberg-internal-storage#encryption).
- **Collation isn’t supported on Iceberg tables**: When **Table Storage Format** is set to `ICEBERG`, the connector doesn’t include `DEFAULT_DDL_COLLATION` in table creation parameters.
- **Salesforce time fields use microsecond precision**: Salesforce fields of type `time` are created as `TIME(6)` on Iceberg tables.
- **Formula views can be created over Iceberg tables**: When **Enable Views Creation** is set to `true`, the connector can create formula views over Iceberg base tables. The formula field limitations described in [Openflow Connector for Salesforce Bulk API: Salesforce formula fields](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/formula-fields) still apply.
- **Hard deletes aren’t supported**: The connector still represents deleted Salesforce records with the `isDeleted` column rather than hard-deleting rows from the destination table.
