# Bulk load files with CoCo

Tell [CoCo](/user-guide/cortex-code/cortex-code) which files to load and where, and CoCo loads them into a Snowflake table with a one-time [COPY INTO <table>](/sql-reference/sql/copy-into-table). CoCo inspects your files, creates or reuses a file format with options that match your data, and creates a table from the inferred schema or uses one you already have. CoCo then runs `COPY INTO` on your warehouse and checks the results.

Loading files by hand means choosing file format options, writing table DDL that matches the files, and tracking down errors when a column or data type doesn’t line up. With CoCo, you describe the load in plain language and review the SQL instead of writing it. CoCo shows each statement and waits for your approval before it creates or changes objects or loads data, in every approval mode, including when you bypass approvals.

## Choose between a one-time load and continuous ingestion

Use a bulk load when the files are already in place and you want to load them now, such as for a backfill, a migration, or a file delivery that you load on demand. A bulk load doesn’t pick up files that arrive later.

If new files keep arriving and you want each one loaded automatically, set up Snowpipe instead. CoCo can set up Snowpipe for you. For more information, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco).

If your request names files or a location but doesn’t say whether the load is one-time or continuous, CoCo asks before it starts.

## Before you begin

You need:

- [CoCo](/user-guide/cortex-code/cortex-code) connected to your Snowflake account. You can use [CoCo CLI](/user-guide/cortex-code/cortex-code-cli), [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop), or [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight). For CoCo in Snowsight, your role also needs the [access that CoCo requires](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).
- At least one file in one of the following sources. CoCo samples the files to detect the format and infer the schema.
  - A named internal or external stage.
  - A cloud storage path in Amazon S3, Google Cloud Storage, or Microsoft Azure Blob Storage. CoCo reuses a [storage integration](/sql-reference/sql/create-storage-integration) that allows the path, or helps you create one.
  - Files on your computer. In CoCo CLI or CoCo Desktop, CoCo uploads them to an internal stage with [PUT](/sql-reference/sql/put). In Snowsight, first [stage the files](/user-guide/data-load-local-file-system-stage-ui), and then ask CoCo to load them from the stage.
- A warehouse. `COPY INTO` runs on the warehouse, so size it for the number and size of your files.
- A role with `USAGE` on the warehouse, database, and schema, and the privileges for the objects that CoCo creates or uses:
  - `CREATE FILE FORMAT` on the schema.
  - `CREATE TABLE` on the schema for a new table, or `INSERT` and `SELECT` on an existing table.
  - `CREATE STAGE` on the schema, if CoCo creates a stage.
  - `USAGE` on an existing external stage, or `READ` on an existing internal stage. To upload files to an existing internal stage, you also need `WRITE` on the stage.
  - `USAGE` on an existing storage integration or file format that CoCo reuses.
  - The global `CREATE INTEGRATION` privilege, if CoCo creates a storage integration. An administrator can create the integration for you.
  - `EVOLVE SCHEMA` or `OWNERSHIP` on the table, for schema evolution. To enable schema evolution on an existing table, the role needs `OWNERSHIP` on the table.
  - `CREATE ICEBERG TABLE` on the schema, for a new Apache Iceberg™ table, and `CREATE EXTERNAL VOLUME` on the account or `USAGE` on an existing external volume if the table uses an external volume.

CoCo is billed based on token consumption. For more information, see [CoCo costs](/user-guide/cortex-code/cortex-code#cost). The `COPY INTO` statement and the queries that CoCo uses to inspect your files run on your warehouse and consume warehouse credits. For more information, see [Understanding compute cost](/user-guide/cost-understanding-compute).

Supported formats are CSV and TSV, JSON (including NDJSON and JSONL), Parquet, Avro, ORC, and XML. You can load into a standard Snowflake table or a Snowflake-managed [Iceberg table](/user-guide/tables-iceberg-load).

## Load your files

### Step 1: Describe what you want to load

In CoCo, describe the files and where to load them. You don’t need to select a skill or write SQL. Say that it’s a one-time load so that CoCo doesn’t need to ask. For example:

```
Load the CSV files on @mydb.public.orders_stage into a new table ORDERS. This is a one-time load.
```

CoCo uses the warehouse, database, and schema from your session and asks for any that aren’t set. If your request doesn’t say whether to load into an existing table or a new one, CoCo asks.

### Step 2: Confirm the file format

CoCo lists the files at the source and detects the format and compression from the file names. It asks only about details it can’t detect, such as whether CSV fields contain line breaks or JSON objects span more than one line. If the source has no files yet, CoCo stops and asks you to add at least one sample file.

If a compatible file format already exists in the schema, CoCo offers to reuse it. Otherwise, CoCo shows the `CREATE FILE FORMAT` statement and creates the file format after you approve. If the load needs a new stage or storage integration, or an upload of files from your computer, CoCo also shows those statements and runs them after you approve. For the options that CoCo sets, see [What CoCo configures for you](#label-bulk-coco-optimizations).

Important

Before you approve the file format, check that these options suit your files:

- **`MULTI_LINE = FALSE` for CSV and JSON files:** For uncompressed CSV files, this option lets Snowflake split large files and scan them in parallel. However, Snowflake treats each CSV record that has a line break inside a field, and each JSON object that spans more than one line, as an error. With CoCo’s default error handling, that error stops the load. CoCo asks about these line breaks and sets `MULTI_LINE = TRUE` only if you say that your files have them. For more information, see `MULTI_LINE` for [CSV](/sql-reference/sql/copy-into-table#label-multi-line-csv) and [JSON](/sql-reference/sql/copy-into-table#label-multi-line-json).
- **`USE_VECTORIZED_SCANNER = TRUE` for Parquet files:** This option can significantly reduce the time that it takes to load Parquet files. However, the vectorized scanner handles some data differently than the default scanner. For example, it always treats `BINARY_AS_TEXT` as `FALSE`, and it loads map types, `NULL` values in nested data, and time and timestamp values differently. Iceberg loads that use `LOAD_MODE = ADD_FILES_COPY` require this option. For the full list of differences, see [USE\_VECTORIZED\_SCANNER](/sql-reference/sql/copy-into-table#label-use-vectorized-scanner).

### Step 3: Review the table

For a new table, CoCo infers the columns and data types from your files with [INFER\_SCHEMA](/sql-reference/functions/infer_schema) and creates the table with [schema evolution](/user-guide/data-load-schema-evolution) enabled. For an existing table, CoCo checks whether schema evolution is enabled and asks before turning it on. If you decline, CoCo leaves the table unchanged and still matches columns by name, but columns in your files that aren’t in the table aren’t loaded.

For XML files and CSV files without a header row, CoCo doesn’t infer the schema with `INFER_SCHEMA`, so it asks you for the column definitions.

Before CoCo creates or changes a table, it shows the DDL and waits for your approval.

### Step 4: Run the load

CoCo shows the `COPY INTO` statement and runs it after you approve.

### Step 5: Check the results

After the load, CoCo checks the `COPY INTO` results and [COPY\_HISTORY](/sql-reference/functions/copy_history), and counts the rows in the table. If the load stops on an error or any files fail to load, CoCo shows the error, suggests a fix to the file format or error handling, and explains what it plans to retry before it runs the load again.

## What CoCo configures for you

CoCo creates a named file format and sets options that follow Snowflake’s recommendations for loading performance:

| Your files | File format options |
| --- | --- |
| CSV with a header row | `PARSE_HEADER = TRUE`, without `SKIP_HEADER`, so that Snowflake reads column names from the header, and `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE`, so that columns can be matched by name. |
| CSV with no line breaks inside fields | `MULTI_LINE = FALSE`, and `COMPRESSION = NONE` for uncompressed files, so that Snowflake can split large files and scan them in parallel. |
| JSON with one object per line (NDJSON or JSONL) | `MULTI_LINE = FALSE`, without `STRIP_OUTER_ARRAY`. |
| JSON with a single top-level array | `STRIP_OUTER_ARRAY = TRUE`, so that each array element loads as a row. |
| Parquet | `USE_VECTORIZED_SCANNER = TRUE` for faster reads, and `USE_LOGICAL_TYPE = TRUE` so that timestamps and decimals from Spark or pandas keep their types. |
| Parquet, Avro, or ORC | Automatic compression detection, because these formats record their compression inside the file. |

Expand

Show lessSee more

In the `COPY INTO` statement, CoCo also:

- References the named file format instead of inline format options.
- Matches columns by name with `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` for Parquet, Avro, ORC, JSON, and CSV with a header row, so the column order in your files doesn’t need to match the table, and schema evolution can add new columns. For Iceberg loads with `LOAD_MODE = ADD_FILES_COPY`, CoCo uses `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE` instead.
- Uses `ON_ERROR = ABORT_STATEMENT`, so the load stops at the first error, unless you ask CoCo to skip files or continue on errors.
- Doesn’t reload files that were already loaded into the table, unless you ask.

## Adapt the load to your files

### Load from a cloud storage path

```
Load the Parquet files in s3://my-bucket/exports/2026/ into RAW.PUBLIC.EXPORTS once.
```

CoCo reuses a stage and storage integration that already cover the path. If no stage covers the path, CoCo proposes a new one and, if no storage integration allows the path, helps you create one.

### Load files from your computer

In CoCo CLI or CoCo Desktop:

```
Upload ./data/customers.csv and load it into a new table CUSTOMERS. This is a one-time load.
```

CoCo creates or reuses an internal stage and uploads the files with `PUT` after you approve. In Snowsight, [stage the files](/user-guide/data-load-local-file-system-stage-ui) first, and then ask CoCo to load them from the stage.

### Load into an existing table

```
Load the CSV files on @mydb.public.orders_stage into the existing ORDERS table, one time.
```

CoCo maps the file columns to the table columns by name and asks before it enables schema evolution on the table.

### Load newline-delimited JSON

```
Load the NDJSON files on @mydb.public.events_stage into EVENTS as a one-time copy.
Each line is one JSON object.
```

CoCo creates a JSON file format without `STRIP_OUTER_ARRAY`, so each line loads as a row.

### Load Parquet written by Spark or pandas

```
One-time load from @mydb.public.data_stage into table DATA.
The Parquet files were written by Spark. Keep timestamps and decimals as their original types.
```

CoCo sets `USE_LOGICAL_TYPE = TRUE` on the file format, so timestamps and decimals keep their original types.

### Load into an Iceberg table

```
Load the Parquet files on @mydb.public.sales_stage into a Snowflake-managed Iceberg table
named SALES, one time. The files were written with pandas, not an Iceberg writer.
```

Mention Iceberg in your request, and CoCo loads into a Snowflake-managed Iceberg table, which it helps you create if needed. For Parquet files, CoCo asks whether an Iceberg writer produced them, unless your request already says how they were written. CoCo uses `LOAD_MODE = ADD_FILES_COPY` only for Parquet files from an Iceberg writer. For other Parquet files, and for CSV, JSON, Avro, and ORC files, it uses `LOAD_MODE = FULL_INGEST`. For table and storage requirements, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load).

## Limitations and considerations

- For XML files and CSV files without a header row, you provide the column definitions. Headerless CSV files load by column position, without matching by name or schema evolution.
- Snowflake skips files that it has already loaded into the same table, based on load metadata that it keeps for 64 days. To reload files, ask CoCo explicitly. Reloading files can duplicate rows. For more information, see [Load metadata](/user-guide/data-load-considerations-load#label-copy-load-metadata).
- Uploading files from your computer requires CoCo CLI or CoCo Desktop.
- For Iceberg tables, CoCo loads only into Snowflake-managed Iceberg tables, not tables that use an external catalog.

## What’s next

- To load new files automatically as they arrive, see [Set up continuous file ingestion with CoCo](/user-guide/data-load-snowpipe-auto-coco).
- To monitor loads, see [Monitor data loading activity by using Copy History](/user-guide/data-load-monitor).
- To prepare files for faster loads, see [Preparing your data files](/user-guide/data-load-considerations-prepare).
- To transform data while you load it, see [Transform data during a load](/user-guide/data-load-transform).
