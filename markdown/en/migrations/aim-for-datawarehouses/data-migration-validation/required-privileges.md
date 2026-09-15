# Required privileges

AIM DMV needs privileges in two places: your Snowflake account (the target) and [each source platform it reads from](#source-platform-privileges). This page lists both, so you can share the Snowflake grants with your account administrator and the source grants with your source platform’s database administrator, and request the access up front.

On the Snowflake side, grant the privileges once to a dedicated role, then use that role for the Orchestrator and Worker connections in your `config.toml` or `connections.toml`. See [Connecting to Snowflake with a PAT](./overview#connecting-to-snowflake-with-a-pat) for how those connections authenticate. For the source side, see [Source platform privileges](#source-platform-privileges).

Note

The Snowflake AIM Agent for Data Warehouses and the SnowConvert AI CLI create most Snowflake objects for you at runtime (schemas, stages, pipes, file formats, and stored procedures). The connection role still needs the privileges below so it can create and operate those objects.

## Where AIM DMV needs access

In Snowflake, a workflow touches three main areas, plus a few optional ones depending on how you deploy and where migrated data lands.

| Area | Object | Purpose |
| --- | --- | --- |
| Metadata database | `SNOWCONVERT_AI` (default) | Task queue, workflow state, migration and validation metadata, internal stage, and stored procedures. |
| Target database | User-specified | Where migrated tables are created and loaded. |
| Warehouse | User-specified | Runs `COPY INTO`, `MERGE`, DDL, and metadata queries. |
| External stage (optional) | Storage integration and stage | Loading from S3, Azure Blob, or GCS instead of an internal stage. |
| Iceberg target (optional) | External volume and catalog integration | Migrating into Iceberg tables. |
| SPCS deployment (optional) | Secret and external access integration | Running Workers in Snowpark Container Services. |

Expand

Show lessSee more

On the source side, Workers connect to each source platform to read table metadata and data. Those grants are platform-specific: see [Source platform privileges](#source-platform-privileges).

## Metadata database privileges

By default AIM DMV stores workflow and result metadata in the `SNOWCONVERT_AI` database, across the `DATA_MIGRATION`, `DATA_VALIDATION`, `COMMON`, and `TEMP` schemas. For what each schema holds, see [The SNOWCONVERT\_AI database](./snowconvert-ai-database).

If you let the Orchestrator create the database on startup, the role needs `CREATE DATABASE` on the account. If your account requires the database to be pre-created, an administrator creates it and grants `USAGE` and `CREATE SCHEMA` on it instead.

Copy code

```
-- Database level
GRANT USAGE ON DATABASE SNOWCONVERT_AI TO ROLE <migration_role>;
GRANT CREATE SCHEMA ON DATABASE SNOWCONVERT_AI TO ROLE <migration_role>;

-- Schema level (grant after the first run creates the schemas,
-- or pre-create the schemas and grant before the first run)
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.DATA_VALIDATION TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.COMMON TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;

-- Future objects, so dynamically created tables, pipes, and procedures stay accessible
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA SNOWCONVERT_AI.DATA_VALIDATION TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA SNOWCONVERT_AI.COMMON TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
GRANT ALL PRIVILEGES ON FUTURE PROCEDURES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;

-- Internal stage used for task results
GRANT READ, WRITE ON STAGE SNOWCONVERT_AI.DATA_MIGRATION.TASK_RESULTS TO ROLE <migration_role>;
```

### Granular alternative

If `ALL PRIVILEGES` is too broad for your account’s policies, grant the specific object-creation and DML privileges the schemas need instead. Repeat the pattern for `DATA_VALIDATION`, `COMMON`, and `TEMP`, keeping the object types relevant to each schema (for example, `TEMP` needs `CREATE PIPE`, `CREATE STAGE`, and `CREATE TABLE` for validation result ingestion).

Copy code

```
GRANT USAGE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT CREATE TABLE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT CREATE STAGE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT CREATE PIPE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT CREATE PROCEDURE ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT CREATE FILE FORMAT ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;
GRANT USAGE ON ALL PROCEDURES IN SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE <migration_role>;

-- TEMP schema (data validation result ingestion)
GRANT CREATE PIPE ON SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
GRANT CREATE STAGE ON SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
GRANT CREATE TABLE ON SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
```

## Target database privileges

The target database and schema are where migrated tables are created and loaded.

Copy code

```
-- Database level
GRANT USAGE ON DATABASE <target_db> TO ROLE <migration_role>;
GRANT CREATE SCHEMA ON DATABASE <target_db> TO ROLE <migration_role>;

-- Schema level
GRANT USAGE ON SCHEMA <target_db>.<target_schema> TO ROLE <migration_role>;
GRANT CREATE TABLE ON SCHEMA <target_db>.<target_schema> TO ROLE <migration_role>;

-- Table-level DML for COPY INTO, MERGE, DELETE, and TRUNCATE during migration
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA <target_db>.<target_schema> TO ROLE <migration_role>;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA <target_db>.<target_schema> TO ROLE <migration_role>;
```

These privileges cover the operations AIM DMV performs on the target during a workflow:

| Operation | SQL issued | Why |
| --- | --- | --- |
| Create target tables | `CREATE TABLE IF NOT EXISTS <table> (...)` | Auto-creates tables from the source schema. |
| Load data | `COPY INTO <table> FROM @stage/...` | Bulk loads from Parquet or CSV. |
| Upsert and dedup | `MERGE INTO <table>` and `DELETE FROM <table>` | Watermark sync and incremental deduplication. |
| Preflight schema | `CREATE TRANSIENT SCHEMA IF NOT EXISTS PREFLIGHT_<id>` | Dry-run validation before the real load. |
| Preflight cleanup | `DROP SCHEMA IF EXISTS PREFLIGHT_<id> CASCADE` | Removes the transient schema after the workflow. |
| Staging tables | `CREATE OR REPLACE TRANSIENT TABLE <stg> LIKE <tgt>` | Intermediate staging for upserts. |
| Staging cleanup | `DROP TABLE IF EXISTS <staging_table>` | Removes the staging table after the merge. |
| Schema introspection | `SELECT ... FROM INFORMATION_SCHEMA.TABLES` or `COLUMNS` | Validates the target structure. |

Expand

Show lessSee more

## Warehouse privileges

Copy code

```
GRANT USAGE ON WAREHOUSE <warehouse_name> TO ROLE <migration_role>;
GRANT OPERATE ON WAREHOUSE <warehouse_name> TO ROLE <migration_role>;
GRANT MONITOR ON WAREHOUSE <warehouse_name> TO ROLE <migration_role>;
```

| Privilege | Reason |
| --- | --- |
| `USAGE` | Executes queries (`COPY INTO`, `MERGE`, DDL, and metadata reads). |
| `OPERATE` | Resumes the warehouse if it auto-suspends. |
| `MONITOR` | Reads query history for task tracking. |

Expand

Show lessSee more

## Optional privileges

Grant these only when your deployment or target uses the corresponding feature.

### External stage and storage integration

Required when you load from external cloud storage (S3, Azure Blob, or GCS) instead of Snowflake’s internal stage.

Copy code

```
GRANT USAGE ON INTEGRATION <storage_integration_name> TO ROLE <migration_role>;
GRANT USAGE ON STAGE <db>.<schema>.<external_stage> TO ROLE <migration_role>;
GRANT READ ON STAGE <db>.<schema>.<external_stage> TO ROLE <migration_role>;
```

### Iceberg table targets

Required when you migrate into Iceberg tables.

Copy code

```
GRANT CREATE ICEBERG TABLE ON SCHEMA <target_db>.<target_schema> TO ROLE <migration_role>;
GRANT USAGE ON EXTERNAL VOLUME <external_volume_name> TO ROLE <migration_role>;
GRANT USAGE ON INTEGRATION <catalog_integration_name> TO ROLE <migration_role>;
```

The Iceberg strategy you choose determines which additional privileges apply:

| Strategy | Additional privileges |
| --- | --- |
| `catalog_link` | `USAGE` on the catalog integration. |
| `convert_to_managed` | `USAGE` on the catalog integration, plus `OWNERSHIP` or `ALTER` on the Iceberg table. |
| `copy_files` | `USAGE` on the source data stage. |

Expand

Show lessSee more

### Snowpipe monitoring

AIM DMV creates and drops Snowpipes in the `TEMP` schema to ingest data-validation results. `CREATE PIPE` on `TEMP` (granted above) covers creation. To also monitor pipe status, add:

Copy code

```
GRANT MONITOR ON ALL PIPES IN SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
GRANT MONITOR ON FUTURE PIPES IN SCHEMA SNOWCONVERT_AI.TEMP TO ROLE <migration_role>;
```

### Workers on Snowpark Container Services

Required when you run Workers in SPCS, which reads source credentials from a secret and reaches the source system through an external access integration. For the full SPCS setup, see [Deploying workers](./deploy-workers).

Copy code

```
-- Source credential secret
GRANT USAGE ON SECRET <db>.<schema>.<secret_name> TO ROLE <migration_role>;

-- External access integration for network egress to the source database
GRANT USAGE ON INTEGRATION <eai_name> TO ROLE <migration_role>;
```

## Quick-start role setup

Copy this script and replace the placeholders (`<wh>`, `<target_db>`, `<target_schema>`, `<migration_user>`, and the optional integrations) for your environment. Uncomment the external stage and Iceberg sections only if you use them.

Copy code

```
-- 1. Create a dedicated role
CREATE ROLE IF NOT EXISTS DMV_MIGRATION_ROLE;

-- 2. Warehouse
GRANT USAGE, OPERATE, MONITOR ON WAREHOUSE <wh> TO ROLE DMV_MIGRATION_ROLE;

-- 3. Metadata database
GRANT USAGE, CREATE SCHEMA ON DATABASE SNOWCONVERT_AI TO ROLE DMV_MIGRATION_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.DATA_MIGRATION TO ROLE DMV_MIGRATION_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.DATA_VALIDATION TO ROLE DMV_MIGRATION_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.COMMON TO ROLE DMV_MIGRATION_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA SNOWCONVERT_AI.TEMP TO ROLE DMV_MIGRATION_ROLE;

-- 4. Target database
GRANT USAGE, CREATE SCHEMA ON DATABASE <target_db> TO ROLE DMV_MIGRATION_ROLE;
GRANT ALL PRIVILEGES ON SCHEMA <target_db>.<target_schema> TO ROLE DMV_MIGRATION_ROLE;
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON FUTURE TABLES IN SCHEMA <target_db>.<target_schema> TO ROLE DMV_MIGRATION_ROLE;

-- 5. External stage integration (optional)
-- GRANT USAGE ON INTEGRATION <storage_integration> TO ROLE DMV_MIGRATION_ROLE;

-- 6. Iceberg target (optional)
-- GRANT CREATE ICEBERG TABLE ON SCHEMA <target_db>.<target_schema> TO ROLE DMV_MIGRATION_ROLE;
-- GRANT USAGE ON EXTERNAL VOLUME <external_volume> TO ROLE DMV_MIGRATION_ROLE;
-- GRANT USAGE ON INTEGRATION <catalog_integration> TO ROLE DMV_MIGRATION_ROLE;

-- 7. Assign the role to the connection user
GRANT ROLE DMV_MIGRATION_ROLE TO USER <migration_user>;
ALTER USER <migration_user> SET DEFAULT_ROLE = DMV_MIGRATION_ROLE;
```

## Objects created at runtime

AIM DMV creates objects as workflows run. This is why the metadata and target grants include `FUTURE` objects: without them, the role can’t operate objects it creates after the initial grant.

| Object | Location | Lifecycle |
| --- | --- | --- |
| `TASK_QUEUE`, `WORKFLOW`, `TABLE_METADATA`, `PARTITION_METADATA`, `SCHEMA_MIGRATION` | `SNOWCONVERT_AI.DATA_MIGRATION` | Persistent. |
| `TASK_RESULTS` (internal stage) | `SNOWCONVERT_AI.DATA_MIGRATION` | Persistent. |
| `PARQUET_FILE_FORMAT`, `CSV_FILE_FORMAT`, and stored procedures | `SNOWCONVERT_AI.DATA_MIGRATION` | Persistent. |
| Validation result Snowpipes | `SNOWCONVERT_AI.TEMP` | Per-workflow, auto-cleaned. |
| Target tables | `<target_db>.<target_schema>` | Persistent. |
| `PREFLIGHT_<id>` schema | `<target_db>` | Per-workflow, dropped when the workflow ends unless `preflightKeepSchema` is `true`. See [Preflight: a bounded dry run](../manual-migration/data-migration-configuration-reference#preflight-bounded-dry-run). |
| Transient staging tables | `<target_db>.<target_schema>` | Per-partition, auto-dropped. |
| Staged intermediate files | `TASK_RESULTS` stage, and external stages used by server-side extraction | Per-workflow, governed by `cleanUpTransientResources`. See [Cleaning up transient resources](../manual-migration/data-migration-configuration-reference#cleaning-up-transient-resources). |

Expand

Show lessSee more

If a workflow fails or is canceled, its staged files stay behind when `cleanUpTransientResources` is `on-success` (the default). That’s deliberate, so you can inspect them. Set the property to `always` when you’d rather not accumulate them.

## Customizing metadata database and schema names

You can change the default metadata database and schema names with environment variables on the Orchestrator. If you override any of these, adjust the `GRANT` statements above to reference your custom names.

| Environment variable | Default | Controls |
| --- | --- | --- |
| `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA` | `SNOWCONVERT_AI` | Metadata database name. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA` | `DATA_MIGRATION` | Migration schema name. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA` | `DATA_VALIDATION` | Validation schema name. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_COMMON_METADATA` | `COMMON` | Common schema name. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_TEMP_METADATA` | `TEMP` | Temp and pipe schema name. |

Expand

Show lessSee more

Workers need matching values in their own configuration, because they read these locations from Worker TOML rather than from the Orchestrator’s environment. See [Matching metadata locations between the Orchestrator and Workers](../manual-migration/data-migration-configuration-reference#matching-metadata-locations).

For the other environment variables AIM DMV reads, including metadata storage mode, secret resolution, and Teradata TPT paths, see [Environment variables](../manual-migration/data-migration-configuration-reference#environment-variables).

## Source platform privileges

AIM DMV Workers connect to your source platform to read table metadata, infer keys, estimate sizes, and extract data. Grant the privileges below to the source database user the Workers connect as (the user configured in `connections.source.<platform>`). Share this section with your source platform’s database administrator.

The requirements differ by platform, but the pattern is the same everywhere: read access to the tables being migrated, plus visibility into the platform’s system catalog. Row-level data validation (L3) sometimes needs an extra hashing privilege.

The following table summarizes the requirements. Each platform’s grants and details follow.

| Platform | Primary requirement | Catalog access | Data validation (L3) extra |
| --- | --- | --- | --- |
| Oracle | `SELECT` on source tables | Automatic (`ALL_*` views) | `EXECUTE ON DBMS_CRYPTO` (LOB columns only) |
| SQL Server | `SELECT` on source schema and `VIEW DATABASE STATE` | `VIEW DEFINITION` | None |
| Azure Synapse | Same as SQL Server | Same as SQL Server | CETAS extraction needs `CREATE EXTERNAL TABLE` |
| Amazon Redshift | `SELECT` on source tables and `USAGE` on schema | Automatic (`information_schema`) | None |
| Teradata | `SELECT` on source database and `SELECT` on `DBC` | Explicit `SELECT` on `DBC.*V` views | `HASH_MD5` UDF and `EXECUTE FUNCTION` |
| PostgreSQL | `SELECT` on source tables and `USAGE` on schema | Automatic (`pg_catalog`, `information_schema`) | None |

Expand

Show lessSee more

### Oracle

AIM DMV connects to Oracle to extract table metadata, infer keys, and read data. It queries Oracle’s `ALL_*` dictionary views rather than the `DBA_*` views, so the connected user only needs visibility into the objects granted to it.

#### Dictionary views queried

| View | Purpose |
| --- | --- |
| `ALL_TAB_COLUMNS` | Column metadata (name, data type, precision, scale, nullability, ordinal). |
| `ALL_TABLES` | Table existence check. `NUM_ROWS` isn’t relied on; `COUNT(*)` is used instead. |
| `ALL_OBJECTS` | Object type detection (table compared to view). |
| `ALL_CONSTRAINTS` | Primary key (`P`), unique (`U`), and foreign key (`R`) constraint discovery. |
| `ALL_CONS_COLUMNS` | Constraint column membership and ordering. |
| `USER_SEGMENTS` | Table size estimation, only when the owner matches the session user. |

Expand

Show lessSee more

#### Required grants

Copy code

```
-- Run as SYS, SYSTEM, or a DBA-privileged user.
-- Replace <source_user> with the Oracle user the Workers connect as.
-- Replace <source_schema> and <table_name> with the objects being migrated.

-- Read access to the tables being migrated
GRANT SELECT ON <source_schema>.<table_name> TO <source_user>;

-- Data validation (L3) with LOB columns (CLOB, NCLOB, BLOB)
GRANT EXECUTE ON DBMS_CRYPTO TO <source_user>;

-- DBMS_CLOUD-based extraction (Oracle Cloud), optional
-- GRANT EXECUTE ON DBMS_CLOUD TO <source_user>;
-- GRANT CREATE CREDENTIAL TO <source_user>;
```

The `ALL_*` dictionary views need no explicit grant. They automatically show any object the user can `SELECT` from.

#### Key points

- The `DBA_*` views aren’t required. AIM DMV uses only `ALL_*` views, which show the objects the user can access.
- `SELECT` on the source tables is the primary requirement. The `ALL_*` views populate automatically once the user has object access.
- `USER_SEGMENTS` is used for size estimation when the table owner matches the connected user. For cross-schema tables, size defaults to 0 and partitioning falls back to `COUNT(*)`.
- `COUNT(*)` runs on each source table for accurate row counts (used for partitioning), which requires `SELECT` on the table.

#### Queries executed on source tables

| Operation | Query | Privilege needed |
| --- | --- | --- |
| Row count (metadata) | `SELECT COUNT(*) FROM <owner>.<table>` | `SELECT` on table |
| Schema discovery | `SELECT ... FROM ALL_TAB_COLUMNS WHERE owner = ... AND table_name = ...` | Automatic with `SELECT` on the object |
| Object type detection | `SELECT ... FROM ALL_OBJECTS WHERE owner = ... AND object_name = ...` | Automatic |
| Primary key inference | `SELECT ... FROM ALL_CONSTRAINTS JOIN ALL_CONS_COLUMNS ... WHERE constraint_type = 'P'` | Automatic |
| Unique key inference | Same as above with `constraint_type = 'U'` | Automatic |
| Foreign key discovery | Same as above with `constraint_type = 'R'` | Automatic |
| Table size | `SELECT ... FROM USER_SEGMENTS WHERE segment_name = ...` | Own schema only; otherwise returns 0 |
| Data extraction | `SELECT <columns> FROM <owner>.<table> [WHERE ...]` | `SELECT` on table |
| L3 row hashing (validation) | `SELECT RAWTOHEX(DBMS_CRYPTO.HASH(col, 2)) ...` | `SELECT` and `EXECUTE ON DBMS_CRYPTO` (LOBs only) |

Expand

Show lessSee more

#### Data validation requirements

For L3 row validation with LOB columns:

| Requirement | Detail |
| --- | --- |
| `EXECUTE ON DBMS_CRYPTO` | Required only for tables with `CLOB`, `NCLOB`, or `BLOB` columns. |
| Purpose | Hashes the full LOB content on the source for row-level comparison. |
| Without the grant | Row-level validation fails for LOB columns. |
| Non-LOB tables | Don’t need this grant. |

Expand

Show lessSee more

#### Identifier handling

AIM DMV maps workflow JSON names to Oracle data-dictionary spelling:

- Unquoted names (all-upper or all-lower in the workflow JSON) become uppercase in catalog queries.
- Mixed-case or quoted names keep their exact spelling in catalog filters.

If `ALL_TAB_COLUMNS` returns no rows for a table, verify that the schema and table names match Oracle’s dictionary casing.

#### Connection methods

| Method | Config keys | Notes |
| --- | --- | --- |
| EZ Connect (thin mode) | `host`, `port`, `service_name` | Default; no Oracle Client needed. |
| TNS alias | `tns_alias`, `tns_admin` | Uses `tnsnames.ora`. |
| Oracle Wallet (ATP/ADW) | `wallet_directory`, `wallet_password` | For Autonomous Database. |
| Thick mode (legacy) | `oracle_thick_mode = true` | For 10g password verifiers. |
| ODBC fallback | `odbc_driver` | Only when the `oracledb` package isn’t installed. |

Expand

Show lessSee more

#### Quick-start grants

Copy code

```
-- Minimal grants for a full-schema Oracle migration.
-- Run as a DBA or the schema owner with GRANT OPTION.

-- Grant SELECT on every table in the source schema
BEGIN
  FOR t IN (SELECT table_name FROM all_tables WHERE owner = '<source_schema>') LOOP
    EXECUTE IMMEDIATE 'GRANT SELECT ON <source_schema>.' || t.table_name || ' TO <source_user>';
  END LOOP;
END;
/

-- For L3 validation with LOB columns
GRANT EXECUTE ON DBMS_CRYPTO TO <source_user>;
```

### SQL Server

#### System views queried

| View or object | Purpose |
| --- | --- |
| `INFORMATION_SCHEMA.COLUMNS` | Column metadata (name, data type, precision, scale, nullability, ordinal). |
| `sys.tables` | Table existence and metadata joins. |
| `sys.schemas` | Schema name resolution. |
| `sys.indexes` | Index metadata for key inference (clustered, unique). |
| `sys.index_columns` | Index column membership. |
| `sys.partitions` | Row count (`SUM(p.rows)`). |
| `sys.allocation_units` | Table size (`SUM(total_pages)`). |
| `sys.objects` | Object type detection (table compared to view). |
| `sys.columns` | Column metadata (user-defined types, vector metadata). |
| `sys.types` | User-defined type resolution. |
| `information_schema.table_constraints` | Primary key constraint discovery. |
| `information_schema.key_column_usage` | Constraint column membership. |

Expand

Show lessSee more

#### Required grants

Copy code

```
-- Replace <source_user> with the login or user the Workers connect as.
-- Replace <source_db> and <source_schema> with the source objects.

USE <source_db>;

-- Read access to the tables being migrated
GRANT SELECT ON SCHEMA::<source_schema> TO <source_user>;

-- System catalog access for metadata queries
GRANT VIEW DEFINITION ON SCHEMA::<source_schema> TO <source_user>;

-- Row count and size (sys.partitions, sys.allocation_units)
GRANT VIEW DATABASE STATE TO <source_user>;

-- Alternative: db_datareader includes SELECT on all tables plus catalog access
-- ALTER ROLE db_datareader ADD MEMBER <source_user>;

-- CETAS extraction, optional
GRANT CREATE EXTERNAL TABLE TO <source_user>;
GRANT ALTER ON SCHEMA::<source_schema> TO <source_user>;
```

#### Key points

- `VIEW DEFINITION` is needed for `sys.indexes`, `sys.index_columns`, `sys.columns`, and `sys.types` to be visible for the schema.
- `VIEW DATABASE STATE` enables access to `sys.dm_db_partition_stats` and `sys.allocation_units` for row count and size.
- `INFORMATION_SCHEMA` views are visible to any user with `SELECT` on the underlying objects.
- The connection is database-scoped. Azure SQL Database doesn’t support `USE` statements, so set the database in the connection string.
- CETAS extraction also requires access to pre-created external data source and Parquet external file format objects. Azure SQL Database doesn’t support CETAS; use `cloud_direct` instead.

#### Operations performed

| Operation | Query | Privilege |
| --- | --- | --- |
| Row count and size | `SELECT SUM(p.rows), SUM(a.total_pages) FROM sys.tables JOIN sys.partitions ...` | `VIEW DATABASE STATE` |
| Schema discovery | `SELECT ... FROM INFORMATION_SCHEMA.COLUMNS` | `SELECT` on table |
| Object type | `SELECT ... FROM sys.objects JOIN sys.schemas WHERE type IN ('U','V')` | `VIEW DEFINITION` |
| Key inference | `SELECT ... FROM sys.indexes JOIN sys.index_columns ...` | `VIEW DEFINITION` |
| Data extraction | `SELECT <columns> FROM [schema].[table] ...` | `SELECT` on table |
| CETAS extraction | `CREATE EXTERNAL TABLE ... AS SELECT ...` | `CREATE EXTERNAL TABLE`, `ALTER` on the source CETAS export schema, and access to the external data source and file format |
| L3 row hashing (validation) | `SELECT HASHBYTES('MD5', ...) FROM ...` | `SELECT` on table |

Expand

Show lessSee more

### Azure Synapse

Azure Synapse (Dedicated SQL Pool and Serverless SQL Pool) uses the same T-SQL system views as SQL Server, but connects through its own `connections.source.azure_synapse` configuration. Apply the SQL Server grants above, with these differences:

- Dedicated Pool: same as SQL Server, using `sys.indexes`, `sys.index_columns`, and `INFORMATION_SCHEMA.COLUMNS`.
- Serverless Pool: `INFORMATION_SCHEMA.COLUMNS` is used for schema discovery, and `sys` views can have limited availability.
- CETAS extraction (optional): when you use the `CREATE EXTERNAL TABLE AS SELECT` extraction strategy, the user also needs the grants below, plus access to pre-created external data source and external file format objects.

Copy code

```
GRANT CREATE EXTERNAL TABLE TO <source_user>;
GRANT ALTER ON SCHEMA::<source_schema> TO <source_user>;
```

### Amazon Redshift

#### System views queried

| View | Purpose |
| --- | --- |
| `SVV_TABLE_INFO` | Row count (`tbl_rows`) and table size (`size`, in MB). |
| `information_schema.columns` | Column metadata (name, data type, precision, scale, nullability, ordinal). |
| `information_schema.tables` | Object type detection (table compared to view). |
| `information_schema.table_constraints` | Primary key constraint discovery. |
| `information_schema.key_column_usage` | Constraint column membership. |
| `SVV_EXTERNAL_COLUMNS` | Schema for external (Spectrum or Iceberg) tables. |
| `SVV_EXTERNAL_TABLES` | Detection of external tables. |

Expand

Show lessSee more

#### Required grants

Copy code

```
-- Replace <source_user> with the Redshift user the Workers connect as.
-- Replace <source_schema> with the schema being migrated.

-- Read access to the tables being migrated
GRANT USAGE ON SCHEMA <source_schema> TO <source_user>;
GRANT SELECT ON ALL TABLES IN SCHEMA <source_schema> TO <source_user>;

-- External tables (Spectrum or Iceberg)
GRANT USAGE ON SCHEMA <external_schema> TO <source_user>;
GRANT SELECT ON ALL TABLES IN SCHEMA <external_schema> TO <source_user>;
```

#### Key points

- `SVV_TABLE_INFO` shows only the tables the user owns, or all tables for a superuser. If the row count returns NULL, AIM DMV falls back to `COUNT(*)`.
- `information_schema` views are visible when the user has `SELECT` on the underlying tables.
- `UNLOAD` to S3 requires `SELECT` on the source table. Redshift grants `UNLOAD` implicitly with `SELECT`.
- External tables (Spectrum or Iceberg) use `SVV_EXTERNAL_COLUMNS` and `SVV_EXTERNAL_TABLES`, and require `USAGE` on the external schema.

### Teradata

#### System views queried

| View or command | Purpose |
| --- | --- |
| `DBC.TablesV` | Object type detection (table compared to view, via `TableKind`). |
| `DBC.ColumnsV` | Column metadata (name, data type, precision, nullability). |
| `DBC.ColumnsQV` | Full view column metadata for L1 schema validation. |
| `DBC.TableStatsV` | Row count (`RowCount` from collected statistics). |
| `DBC.TableSizeV` | Table size (`CurrentPerm`, in bytes). |
| `DBC.Indices` | Primary and unique index discovery for key inference. |
| `HELP COLUMN <table>` | Basic view column metadata when `DBC.ColumnsQV` isn’t available. |

Expand

Show lessSee more

#### Required grants

Copy code

```
-- Replace <source_user> with the Teradata user the Workers connect as.
-- Replace <source_db> with the source database.

-- Read access to the tables being migrated
GRANT SELECT ON <source_db> TO <source_user>;

-- DBC dictionary access for metadata queries
GRANT SELECT ON DBC.TablesV TO <source_user>;
GRANT SELECT ON DBC.ColumnsV TO <source_user>;
GRANT SELECT ON DBC.ColumnsQV TO <source_user>;
GRANT SELECT ON DBC.TableStatsV TO <source_user>;
GRANT SELECT ON DBC.TableSizeV TO <source_user>;
GRANT SELECT ON DBC.Indices TO <source_user>;

-- Data validation (L3): HASH_MD5 UDF, installed in the same database as
-- connections.source.teradata.database
GRANT EXECUTE FUNCTION ON <source_db>.HASH_MD5 TO <source_user>;

-- WRITE_NOS extraction to S3, Azure, or GCS, optional
-- GRANT EXECUTE ON SYSLIB.WRITE_NOS TO <source_user>;
```

#### Key points

- `DBC` views require explicit `SELECT` grants on Teradata, unlike Oracle’s `ALL_*` views.
- `DBC.TableStatsV.RowCount` depends on collected statistics. If it’s stale or NULL, AIM DMV falls back to `COUNT(*)`.
- `HASH_MD5` isn’t a built-in function. A DBA must install it in the same database the Worker uses as its default, or row-level validation fails.
- `DBC.ColumnsQV` provides full metadata for view schema validation. If it’s unavailable, AIM DMV falls back to `HELP COLUMN` and compares only column names and data types.
- Teradata identifiers are case-insensitive by default; AIM DMV normalizes them to the `DBC` spelling.

#### Data validation requirements

| Requirement | Detail |
| --- | --- |
| `HASH_MD5` UDF | Must exist in the Worker’s default database; used for L3 row-hash validation. |
| `EXECUTE FUNCTION` privilege | Granted on the `HASH_MD5` UDF. |
| Not built-in | A DBA must install the `HASH_MD5` UDF before row-level validation can run. |

Expand

Show lessSee more

### PostgreSQL

#### System views queried

| View | Purpose |
| --- | --- |
| `information_schema.columns` | Column metadata (name, data type, precision, scale, nullability, ordinal). |
| `information_schema.tables` | Object type detection (table compared to view). |
| `information_schema.table_constraints` | Primary key constraint discovery. |
| `information_schema.key_column_usage` | Constraint column membership. |
| `pg_catalog.pg_class` | Object type detection and table metadata. |
| `pg_catalog.pg_namespace` | Schema resolution. |
| `pg_catalog.pg_index` | Index-based key inference. |
| `pg_catalog.pg_attribute` | Index column membership. |

Expand

Show lessSee more

#### Required grants

Copy code

```
-- Replace <source_user> with the PostgreSQL user the Workers connect as.
-- Replace <source_schema> with the schema being migrated.

-- Read access to the tables being migrated
GRANT USAGE ON SCHEMA <source_schema> TO <source_user>;
GRANT SELECT ON ALL TABLES IN SCHEMA <source_schema> TO <source_user>;

-- Read access to tables created later in the schema
ALTER DEFAULT PRIVILEGES IN SCHEMA <source_schema>
    GRANT SELECT ON TABLES TO <source_user>;
```

#### Key points

- `pg_catalog` views are readable by all PostgreSQL users by default, so they need no explicit grant.
- `information_schema` shows the objects the user can access, the same as Oracle’s `ALL_*` behavior.
- `USAGE` on the schema is required before any object within it is accessible.
- Row count uses `COUNT(*)`, because PostgreSQL doesn’t keep a reliable pre-computed row count.
- PostgreSQL folds unquoted identifiers to lowercase, the opposite of Oracle; AIM DMV normalizes accordingly.

## Related content

- [Data Migration & Validation overview](./overview)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Deploying workers](./deploy-workers)
- [Data migration](./data-migration)
- [Data validation](./data-validation)
