# About the Openflow Connector for Google BigQuery

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

The Openflow Connector for Google BigQuery connects a Google BigQuery project to Snowflake and replicates data from selected datasets, tables, and views on a schedule. The connector performs an initial full load for each table, followed by incremental updates using BigQuery’s native change-tracking functionality. Views are replicated using a truncate and load strategy.

## Use cases

The connector supports the following use cases:

- **Replication to Snowflake:** Continuously mirror datasets from BigQuery into Snowflake for downstream analytics and modeling. Incremental changes arrive on a schedule with a 10 minute delay window.
- **Selective replication:** Define which regions, datasets, tables, and views to include using names or regex filters for broad coverage with control.
- **Migration and change capture:** Perform a one-time snapshot load for migrations, then run incremental syncs using BigQuery’s change history to keep tables in sync.
- **View replication:** Replicate standard and materialized BigQuery views to Snowflake using a truncate and load strategy on a configurable schedule.

## The table replication lifecycle

A table’s replication cycle begins with schema discovery and an initial snapshot load of
the data. The cycle transitions to incremental synchronization after data has been ingested into Snowflake.

1. **Schema Introspection:** The connector discovers the source table’s schema, validates its data types, and creates a corresponding destination schema and table in Snowflake.
2. **Snapshot Load:** After creating schema and table, the connector performs a full copy of all existing data from the BigQuery table to Snowflake. This process runs sequentially for each table in the configuration.
3. **Incremental Sync:** Once the initial load is complete, the table enters a scheduled incremental synchronization mode. On each run, the connector uses BigQuery’s CHANGES function to read the journal of row-level changes (inserts, updates, deletes) that occurred since the last synchronization. These changes are then fetched and merged into the destination table in Snowflake.

## Openflow requirements

The minimum runtime size must be `Medium`. Use a larger runtime and multi-node Openflow setup if you
are replicating large data volumes.

## Limitations

- BigQuery guarantees that data streams used to fetch source data remain
  valid for at least 6 hours. As a result, the process of reading the
  source table must be completed in less than 6 hours to prevent the data
  streams from expiring. You must use a larger, multi-node runtime when
  ingesting tables with data volumes that are larger than 100GB.
- BigQuery’s BIGNUMERIC type supports a higher precision (up to 76 digits) than Snowflake’s
  NUMBER type (38 digits). The connector cannot ingest values from
  BIGNUMERIC columns that exceed the Snowflake limit.
- The connector does not support replication of external tables.
- View replication uses a truncate and load strategy only. Incremental
  synchronization (CDC) is not supported for views.
- Incremental syncs require a primary key to correctly handle updates
  and deletes. For tables without a primary key, the connector does not
  support deletes and treats updates as new inserts.

  Note

  You must ensure that the primary key constraints are met. If the
  field marked as the primary key is not unique, data inconsistency
  can occur during incremental mode.
- The connector uses the [BigQuery’s CHANGES](https://cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions#changes) function for incremental updates.
  Because this function cannot query the last ten minutes of table
  history, replicated data in incremental mode has a minimum 10-minute
  lag behind the source.
- The incremental sync process is limited to a maximum 24-hour data
  window due to the BigQuery CHANGES function. If the replication lag
  for a table exceeds this period, the connector truncates the change
  window to 24 hours to proceed with the sync. This truncation can
  result in data loss.
- The connector inherits all other limitations of the BigQuery CHANGES
  function. For more information, see the
  [BigQuery CHANGES function documentation](https://cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions#changes).

## View replication

The connector supports replication of standard views and materialized views from BigQuery to Snowflake. Unlike table replication, views do not support incremental synchronization (CDC). Instead, the connector uses a **truncate and load** strategy: on each synchronization cycle, the connector fully replaces the data in the Snowflake destination table with the current contents of the source view.

The view synchronization frequency is configured separately from table incremental sync frequency using the **View Sync Frequency** parameter. Runs do not overlap. If a cycle takes longer than the configured interval, the next run waits for the previous run to finish.

You can filter which views to replicate using the **Included View Names** and **Included View Names Regex** parameters. These filters apply across all datasets selected for replication.

The connector creates temporary tables in BigQuery during view ingestion. Use the **Temporary Table Dataset** parameter to specify a dedicated dataset for these temporary tables. Snowflake recommends using a separate dataset for temporary tables and not using the ingested dataset for this purpose.

## Data type mapping

The connector maps BigQuery data types to the corresponding Snowflake data types.

| BigQuery Data Type | Snowflake Data Type |
| --- | --- |
| BIGNUMERIC | NUMBER |
| NUMERIC | NUMBER |
| GEOGRAPHY | VARCHAR |
| DATETIME | TIMESTAMP\_NTZ |
| JSON | OBJECT |
| STRUCT | OBJECT |
| RANGE | OBJECT |
| INTERVAL | OBJECT |
| TIMESTAMP | TIMESTAMP\_NTZ |
| DATE | DATE |
| TIME | TIME |
| INT64 / INTEGER | NUMBER |
| FLOAT64 | FLOAT |
| BOOL / BOOLEAN | BOOLEAN |
| STRING | VARCHAR |
| BYTES | BINARY |
| ARRAY | ARRAY |

Expand

Show lessSee more

## Track data changes in Google BigQuery

The connector’s incremental sync functionality is built on [BigQuery’s native CHANGES function](https://cloud.google.com/bigquery/docs/reference/standard-sql/time-series-functions#changes). When you enable change history on a source table, BigQuery maintains an internal journal of all row-level modifications (inserts, updates, and deletes).

The connector queries this journal on a configured incremental sync frequency schedule to retrieve a feed of changes. The connector materializes these changes into a journal table within the same BigQuery dataset. This journal table follows a consistent naming convention: `<sourceTableName>_<incremental_number>_<hash>_journal`

These journal tables are managed entirely by the connector during the replication process and are used to merge data into the final destination table in Snowflake.

Warning

Do not modify the journal tables in any way. Modifying journal tables can disrupt the synchronization process and lead to data integrity issues.

The merge operation handles changes differently for tables with a Primary Key (PK) and tables without one.

### Tables with a Primary Key

For tables with a primary key, the connector handles data changes as follows:

Inserts and Updates:
:   Rows identified as `INSERT` or `UPDATE` are “upserted” into the corresponding Snowflake table.

Deletes:
:   To preserve data history, the connector uses a soft-delete strategy. Instead of physically removing a deleted row from Snowflake, the connector performs an `UPDATE` on the target row, setting the `_SNOWFLAKE_DELETED` column to `TRUE`.

### Tables without a Primary Key

For tables without a primary key, the connector handles data changes as follows:

Inserts and Updates:
:   Rows identified as `INSERT` or `UPDATE` are treated the same way and are inserted into the corresponding Snowflake table.

Deletes:
:   Not supported.

Note

The connector automatically adds the `_SNOWFLAKE_DELETED` (BOOLEAN) column to the destination table schema when it is created.

### Configured synchronization frequency schedule vs actual synchronization frequency

The Incremental Sync Frequency schedule determines the table synchronization frequency. If the schedule
you specified is more frequent than the actual time required to synchronize the table, the system does not follow
the schedule you specified. This occurs because incremental cycles must execute sequentially and cannot overlap.

## Schema Evolution

The connector supports several common schema changes in the source BigQuery table. The following
schema changes are detected and propagated to the Snowflake destination table:

Column Addition:
:   New columns added in BigQuery are automatically added to the corresponding Snowflake table.

Column Deletion (Soft Delete):
:   When a column is dropped in BigQuery, the connector performs a “soft delete” in
    Snowflake. The column is not dropped from the destination table. Instead, it is renamed by adding the
    `_SNOWFLAKE_DELETED` suffix to the end of the column name. For example `my_column` becomes `my_column_SNOWFLAKE_DELETED`. This preserves historical data in Snowflake.

Column Rename:
:   A column rename operation is a two-step process:

    1. The original column is “soft deleted” and renamed with the `_SNOWFLAKE_DELETED` suffix added.
    2. A new column with the new name is added to the Snowflake table.

Primary Key Modification:
:   Adding, removing and changing primary keys is supported.

Data Type Changes:
:   Only changes that widen the existing type are tolerated. Any change that narrows a column’s type or converts it to an incompatible type is not supported and will cause replication for that table to fail.

## Next steps

For information on how to set up the connector, see the following topic:

- [Setting Up the Openflow Connector for Google BigQuery](/user-guide/data-integration/openflow/connectors/google-big-query/setup)
