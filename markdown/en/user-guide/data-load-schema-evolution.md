# Enable automatic table schema evolution

Semi-structured data tends to evolve over time. Systems that generate data add new columns to accommodate additional information, which requires downstream tables to evolve accordingly.

The structure of tables in Snowflake can evolve automatically to support the structure of new data received from the data sources. Snowflake supports the following:

> - Automatically adding new columns.
> - Automatically dropping the NOT NULL constraint from columns that are missing in new data files.
> - Automatically adding new nested columns as structured columns, and adding fields to existing structured columns (requires the
>   `INFER_NESTED_TYPES` copy option). For more information, see [Detect and evolve structured columns](#label-schema-evolution-structured-types).

To enable table schema evolution, do the following:

> - If you’re creating a new table, set the `ENABLE_SCHEMA_EVOLUTION` parameter to `TRUE` when you use the
>   [CREATE TABLE](/sql-reference/sql/create-table) or [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table-snowflake) command.
> - For an existing table, modify the table using the [ALTER TABLE](/sql-reference/sql/alter-table) or
>   [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table) command and set the `ENABLE_SCHEMA_EVOLUTION` parameter to `TRUE`.

Loading data from files evolves the table columns when all of the following are true:

> - The Snowflake table has the `ENABLE_SCHEMA_EVOLUTION` parameter set to `TRUE`.
> - The [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement uses the `MATCH_BY_COLUMN_NAME` option.
> - The role used to load the data has the `EVOLVE SCHEMA` or `OWNERSHIP` privilege on the table. For Snowpipe, the role that owns
>   the pipe loads the data.

Additionally, for schema evolution with CSV, when used with `MATCH_BY_COLUMN_NAME` and `PARSE_HEADER`, `ERROR_ON_COLUMN_COUNT_MISMATCH` must be set to false.

Schema evolution is a standalone feature but can be used in conjunction with the [schema detection support for retrieving the column definitions](/user-guide/data-load-overview#label-detect-column-definitions-in-semi-structured-data-files) from a set of files in cloud storage. In combination, these features enable continuous data pipelines to create new tables from a set of data files in cloud storage and then modify columns of the tables as the schema of new source data files evolves with column additions or deletions.

## Usage notes

> - This feature supports Apache Avro, Apache Parquet, CSV, JSON, and ORC files.
> - This feature is limited to [COPY INTO <table>](/sql-reference/sql/copy-into-table) statements and Snowpipe data loads. INSERT operations cannot evolve the target table schema automatically.
> - [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) with high-performance architecture supports schema evolution for standard Snowflake tables and Snowflake-managed Iceberg tables. Managed Iceberg support is limited to adding new top-level columns with supported data types. For details, see [Table support and schema](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support). [The Kafka connector with Snowpipe Streaming Classic](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka-schema-detection) also supports schema detection and evolution.
> - By default, this feature is limited to adding a maximum of 100 columns or applying one schema change per `COPY` operation.
>   Snowpipe doesn’t have the one-change limit because it applies each schema change and then continues loading
>   automatically. To request more than 100 added columns or more than one schema change per `COPY` operation, contact
>   [Snowflake Support](/user-guide/contacting-support).
> - There is no limit on dropping NOT NULL column constraints.
> - Schema evolution is tracked by the `SchemaEvolutionRecord` output in the following views and commands: [INFORMATION\_SCHEMA COLUMNS View](/sql-reference/info-schema/columns), [ACCOUNT\_USAGE COLUMNS View](/sql-reference/account-usage/columns), [DESCRIBE TABLE command](/sql-reference/sql/desc-table), and [SHOW COLUMNS command](/sql-reference/sql/show-columns).
>
>   However, for the Kafka connector with Snowpipe Streaming, schema evolution is not tracked by the `SchemaEvolutionRecord` output. The `SchemaEvolutionRecord` output always shows NULL.
> - When a column is manually renamed or modified after a schema evolution, the schema evolution record will be cleared.
> - Schema evolution isn’t supported by [tasks](/user-guide/tasks-intro).
> - These usage notes apply to Snowflake-managed Iceberg tables as well.

## Schema evolution support: Ingestion method comparison

The specific metadata field `SchemaEvolutionRecord` is used to track schema evolution. You can view this field with the [INFORMATION\_SCHEMA.COLUMNS View](/sql-reference/info-schema/columns), [DESCRIBE TABLE command](/sql-reference/sql/desc-table), and [SHOW COLUMNS command](/sql-reference/sql/show-columns).

The following table summarizes schema evolution support and the corresponding `SchemaEvolutionRecord` tracking behavior across different Snowflake ingestion methods:

| Ingestion method | Architecture or context | Schema evolution support status | SchemaEvolutionRecord tracking behavior |
| --- | --- | --- | --- |
| File-based (batch/micro-batch) | [COPY INTO <table>](/sql-reference/sql/copy-into-table) command | Fully supported | Visible in tracking views/commands. |
| File-based (batch/micro-batch) | [Snowpipe](/user-guide/data-load-snowpipe-auto), using automated loading | Fully supported | Visible in tracking views or commands. |
| Streaming at the row level | [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) (High-performance architecture) | Supported, but doesn’t add structured columns or fields. | Visible in tracking views or commands. |
| Streaming at the row level | Snowpipe Streaming with classic architecture; for example, Kafka connector | Only [the classic architecture with Kafka connector](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka-schema-detection) is supported, and tracking is limited. | Always shows NULL in tracking views or commands. |

Expand

Show lessSee more

## Detect and evolve structured columns

With `INFER_NESTED_TYPES => TRUE`, [INFER\_SCHEMA](/sql-reference/functions/infer_schema#label-infer-schema-infer-nested-types)
returns [structured](/sql-reference/data-types-structured) `OBJECT`, `ARRAY`, and `MAP` types for nested data. With the
[INFER\_NESTED\_TYPES](/sql-reference/sql/copy-into-table#label-copy-option-infer-nested-types) copy option set to `TRUE`, schema
evolution adds new nested columns as structured columns instead of semi-structured columns, and adds new fields to existing
structured columns:

Copy code

```
-- A file has a new column, address, with the fields city and zip:
--   Without INFER_NESTED_TYPES:  address VARIANT
--   With INFER_NESTED_TYPES:     address OBJECT(city VARCHAR, zip NUMBER(10,0))

-- A later file adds the field country to address:
--   Before:  address OBJECT(city VARCHAR, zip NUMBER(10,0))
--   After:   address OBJECT(city VARCHAR, zip NUMBER(10,0), country VARCHAR)
```

The `INFER_NESTED_TYPES` copy option works for Parquet, JSON, Avro, and ORC files that you load into standard tables or
Snowflake-managed Iceberg tables with `COPY INTO` or Snowpipe. It can’t be used with `SELECT` transforms, Snowpipe Streaming,
dynamic tables, hybrid tables, or external tables.

Note the following:

- Existing `VARIANT` columns aren’t converted. To move their data, see [Move existing data to structured columns](#label-schema-evolution-structured-types-migrate-variant).
- Schema evolution doesn’t change the types of existing columns or fields, so a record fails to load if a value doesn’t fit.
- Some queries behave differently on structured columns. For example, querying a field that a structured `OBJECT` column doesn’t
  declare returns an error instead of `NULL`, and functions such as `TYPEOF` fail unless you cast the value to `VARIANT`. For more
  information, see [Structured data types](/sql-reference/data-types-structured).
- Field names inside structured columns are case-sensitive, even with `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE`. For example, `zip`
  and `Zip` are added as separate fields.
- By default, a `COPY` operation can add up to 100 fields to structured columns.

### Create a table with structured columns from your files

To create a table with structured columns that evolve as you load files, complete the following steps:

1. Run [INFER\_SCHEMA](/sql-reference/functions/infer_schema#label-infer-schema-infer-nested-types) with
   `INFER_NESTED_TYPES => TRUE` on files that represent the full range of your data, and check the inferred types, as described in
   [Choose column types](#label-schema-evolution-structured-types-review-types).
2. Create the table with `CREATE TABLE ... USING TEMPLATE` or your edited column definitions, and set
   `ENABLE_SCHEMA_EVOLUTION = TRUE`. For a Snowflake-managed Iceberg table, see
   [Create and evolve Snowflake-managed Iceberg tables](#label-schema-evolution-structured-types-iceberg).
3. If a role other than the table owner loads the data, grant that role the `EVOLVE SCHEMA` privilege on the table. For Snowpipe,
   grant the privilege to the role that owns the pipe.
4. Load files with `COPY INTO` or a pipe. In every load into the table, set `MATCH_BY_COLUMN_NAME` and `INFER_NESTED_TYPES = TRUE`.
5. To see the columns and fields that schema evolution added, run [DESCRIBE TABLE](/sql-reference/sql/desc-table). The
   `schema evolution record` column shows `ADD_COLUMN` or `ADD_FIELD` for each column that changed.

For a complete example, see [Add a field to a structured OBJECT column](#label-schema-evolution-structured-types-example).

### Choose column types

`INFER_SCHEMA` infers types from the files that it scans, and schema evolution doesn’t change those types later. Before you create
the table, check for `DATE` or `TIMESTAMP_NTZ` types inferred from JSON strings, and for numeric types sized from the scanned
values (for example, `NUMBER(1, 0)` when every scanned value has one digit). Records with values that don’t fit these types fail
to load.

To change a type, generate the column definitions with [GENERATE\_COLUMN\_DESCRIPTION](/sql-reference/functions/generate_column_description), edit them, and
create the table from the edited list.

For JSON files, schema evolution also sizes new columns and fields from the values in each loaded file. To control a
column’s type, add the column before you load files that contain it.

Structured columns enforce their types, and `VARIANT` columns accept any value. Use a `VARIANT` column for the following data:

- ORC maps, and Parquet maps whose keys aren’t strings or integers. This data can’t be loaded into `MAP` columns.
- JSON objects that use data values, such as customer IDs, as keys. Schema evolution adds a field for each new key, and a load that
  would add more than 100 fields fails.
- Data that a dynamic table selects, because dynamic tables don’t support structured types.

To keep a column as `VARIANT`, declare it as `VARIANT` when you create the table, or add it to the table before you load files that
contain it. ORC `UNION` columns, and Avro `UNION` columns that have more than one non-null type, are always added as `VARIANT`.

### Create and evolve Snowflake-managed Iceberg tables

To create a Snowflake-managed Iceberg table from your files, complete the steps in
[Create a table with structured columns from your files](#label-schema-evolution-structured-types-create) with these changes: set `KIND => 'ICEBERG'` in the `INFER_SCHEMA` calls, and in
step 2, use `CREATE ICEBERG TABLE ... USING TEMPLATE`, as shown in the
[INFER\_SCHEMA example](/sql-reference/functions/infer_schema#label-infer-schema-iceberg-v3-example), and then set
`ENABLE_SCHEMA_EVOLUTION` to `TRUE` with [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table).

Iceberg tables don’t support semi-structured `ARRAY` columns, and Iceberg v2 tables (the default) don’t support `VARIANT` columns.
Loads that would add these columns fail. To use `VARIANT` columns, create an Iceberg v3 table, or
[upgrade the table to Iceberg v3](/user-guide/tables-iceberg-upgrade-version). The upgrade is permanent.

If any column would be `VARIANT`, `INFER_SCHEMA` with `KIND => 'ICEBERG'` fails with
`INFER_SCHEMA cannot produce an Iceberg column definition for type 'VARIANT'`. To create an Iceberg v3 table that has `VARIANT`
columns, run `INFER_SCHEMA` with `KIND => 'STANDARD'`, and create the table from an edited column list, as described in
[Choose column types](#label-schema-evolution-structured-types-review-types). In the edited list, use precision 6 for time types, and precision 6 or 9
for timestamp types.

### Add INFER\_NESTED\_TYPES to an existing load

When you add `INFER_NESTED_TYPES = TRUE` to an existing load, data that’s already loaded doesn’t change. Later loads change in the
following ways:

- New nested columns are added as structured columns. Records whose values don’t fit a structured column’s type fail to load, and
  [Snowpipe skips the files that contain them](#label-schema-evolution-structured-types-troubleshooting). To control a new
  column’s type, or to keep it as `VARIANT`, [add it to the table first](/user-guide/data-load-schema-evolution#label-schema-evolution-variant-columns).
- For Parquet files loaded without `USE_VECTORIZED_SCANNER = TRUE`, new rows store maps in `VARIANT` columns as objects
  (`{"1": "a"}`) instead of `key_value` arrays (`{"key_value": [{"key": 1, "value": "a"}]}`). Queries that read
  `my_map:key_value` return `NULL` for new rows.

If a pipe loads the table, pause the pipe and save its definition first, as described in steps 1 to 3 of
[Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). Then complete the following steps:

1. Update queries that read `my_map:key_value`, if any, so that they handle both layouts.
2. If the load doesn’t set `MATCH_BY_COLUMN_NAME`, set it, and remove any `SELECT` transform. Before you do, check that the
   table’s column names match the column names in the files, because schema evolution adds each unmatched column as a new column.
   To keep loading file metadata, such as `METADATA$FILENAME`, use the `INCLUDE_METADATA`
   [copy option](/sql-reference/sql/copy-into-table#label-copy-into-table-copyoptions).
3. Set `ENABLE_SCHEMA_EVOLUTION = TRUE` on the table. If a role other than the table owner loads the data, grant that role the
   `EVOLVE SCHEMA` privilege on the table. For Snowpipe, grant the privilege to the role that owns the pipe.
4. Set `INFER_NESTED_TYPES = TRUE` in every load into the table. Without it, records that have new fields inside structured
   columns fail to load. If you paused a pipe, complete steps 4 to 9 of
   [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). When you recreate the pipe, include
   `INFER_NESTED_TYPES = TRUE` and any changes that you made in step 2 of this section.

### Move existing data to structured columns

If a pipe loads the original table, pause the pipe and save its definition first, as described in steps 1 to 3 of
[Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps). Then use one of the following methods:

- **Reload the staged files:** If the files are still in the stage, create a table and load the files, as described in
  [Create a table with structured columns from your files](#label-schema-evolution-structured-types-create). Use the same file format as the original load.
- **Copy the rows:** Create a table that has structured columns, as described in steps 2 and 3 of
  [Create a table with structured columns from your files](#label-schema-evolution-structured-types-create), and use `INSERT ... SELECT` with a
  [cast to the structured type](/sql-reference/data-types-structured#label-structured-types-casting-semi-object). The cast fails if
  a value omits a field that the type declares. To store `NULL` for these fields, build each value with
  [OBJECT\_CONSTRUCT\_KEEP\_NULL](/sql-reference/functions/object_construct_keep_null), and list every field:

  Copy code

  ```
  CASE WHEN IS_OBJECT(v)
    THEN OBJECT_CONSTRUCT_KEEP_NULL('a', v:a, 'b', v:b)::OBJECT(a NUMBER, b VARCHAR)
  END
  ```

  The new table has no load metadata for these rows, so a later `COPY INTO` statement from the same stage location might load the
  files again. To load only new files, use the `FILES` or `PATTERN` parameter.

If you paused a pipe, complete steps 4 to 9 of [Recreate a pipe safely](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-recreate-steps)
after the move. When you recreate the pipe, have it load the new table, and include `INFER_NESTED_TYPES = TRUE` and the changes
from step 2 of [Add INFER\_NESTED\_TYPES to an existing load](#label-schema-evolution-structured-types-existing-load).

## Examples

The following examples show how schema evolution changes a table when you load files with `COPY INTO`.

### Add columns and drop NOT NULL constraints

The following example creates a table with column definitions derived from a set of Parquet data. With automatic table schema evolution enabled for the table, further data loads from Parquet files with additional name/value pairs automatically add columns to the table:

Note that the `mystage` stage and `my_parquet_format` file format referenced in the statement must already exist. A set of files must
already be staged in the cloud storage location referenced in the stage definition.

This example builds on an example in the [INFER\_SCHEMA](/sql-reference/functions/infer_schema) topic:

> Copy code
>
> ```
> -- Create table t1 in schema d1.s1, with the column definitions derived from the staged file1.parquet file.
> USE SCHEMA d1.s1;
>
> CREATE OR REPLACE TABLE t1
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(object_construct(*))
>       FROM TABLE(
>         INFER_SCHEMA(
>           LOCATION=>'@mystage/file1.parquet',
>           FILE_FORMAT=>'my_parquet_format'
>         )
>       ));
>
> -- Row data in file1.parquet.
> +------+------+------+
> | COL1 | COL2 | COL3 |
> |------+------+------|
> | a    | b    | c    |
> +------+------+------+
>
> -- Describe the table.
> -- Note that column c2 is required in the Parquet file metadata. Therefore, the NOT NULL constraint is set for the column.
> DESCRIBE TABLE t1;
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
> | name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name |
> |------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------|
> | COL1 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
> | COL2 | VARCHAR(16777216) | COLUMN | N     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
> | COL3 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        |
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+
>
> -- Use the SECURITYADMIN role or another role that has the global MANAGE GRANTS privilege.
> -- Grant the EVOLVE SCHEMA privilege to any other roles that could insert data and evolve table schema in addition to the table owner.
>
> GRANT EVOLVE SCHEMA ON TABLE d1.s1.t1 TO ROLE r1;
>
> -- Enable schema evolution on the table.
> -- Note that the ENABLE_SCHEMA_EVOLUTION property can also be set at table creation with CREATE OR REPLACE TABLE
> ALTER TABLE t1 SET ENABLE_SCHEMA_EVOLUTION = TRUE;
>
> -- Load a new set of data into the table.
> -- The new data drops the NOT NULL constraint on the col2 column.
> -- The new data adds the new column col4.
> COPY INTO t1
>   FROM @mystage/file2.parquet
>   FILE_FORMAT = (type=parquet)
>   MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
>
> -- Row data in file2.parquet.
> +------+------+------+
> | col1 | COL3 | COL4 |
> |------+------+------|
> | d    | e    | f    |
> +------+------+------+
>
> -- Describe the table.
> DESCRIBE TABLE t1;
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> | name | type              | kind   | null? | default | primary key | unique key | check | expression | comment | policy name | schema evolution record                                                                                                                                                                  |
> |------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
> | COL1 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL                                                                                                                                                                                     |
> | COL2 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | {"evolutionType":"DROP_NOT_NULL","evolutionMode":"COPY","fileName":"file2.parquet","triggeringTime":"2024-03-15 23:52:59.514000000Z","queryId":"01b303b8-0808-c9ed-0000-0971491b5932"}   |
> | COL3 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | NULL                                                                                                                                                                                     |
> | COL4 | VARCHAR(16777216) | COLUMN | Y     | NULL    | N           | N          | NULL  | NULL       | NULL    | NULL        | {"evolutionType":"ADD_COLUMN","evolutionMode":"COPY","fileName":"file2.parquet","triggeringTime":"2024-03-15 23:52:59.514000000Z","queryId":"01b303b8-0808-c9ed-0000-0971491b5932"}      |
> +------+-------------------+--------+-------+---------+-------------+------------+-------+------------+---------+-------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
> -- Note that since MATCH_BY_COLUMN_NAME is set as CASE_INSENSITIVE, all column names are retrieved as uppercase letters.
> ```

### Add a field to a structured OBJECT column

The following example creates a table whose `address` column has a `city` field, and then loads a file that adds a `zip` field to
`address`. Like the previous example, it uses the `mystage` stage and the `my_parquet_format` file format:

> Copy code
>
> ```
> -- Create a table with a structured OBJECT column.
> CREATE OR REPLACE TABLE t2
>   USING TEMPLATE (
>     SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
>     WITHIN GROUP (ORDER BY order_id)
>       FROM TABLE(
>         INFER_SCHEMA(
>           LOCATION => '@mystage/file3.parquet',
>           FILE_FORMAT => 'my_parquet_format',
>           INFER_NESTED_TYPES => TRUE
>         )
>       ));
>
> -- file3.parquet contains one row, which this example doesn't load:
> -- name: "Alice", address: {city: "Seattle"}
> -- The column names keep their case from the file, so enclose them in
> -- double quotes in queries, for example, "address".
>
> -- Enable schema evolution.
> ALTER TABLE t2 SET ENABLE_SCHEMA_EVOLUTION = TRUE;
>
> -- Load a new file that contains an additional 'zip' field in 'address'.
> -- file4.parquet row data: name: "Bob", address: {city: "Portland", zip: 97201}
> -- zip is stored as a 32-bit integer in the Parquet file.
> COPY INTO t2
>   FROM @mystage/file4.parquet
>   FILE_FORMAT = (TYPE = PARQUET)
>   MATCH_BY_COLUMN_NAME = CASE_SENSITIVE
>   INFER_NESTED_TYPES = TRUE;
>
> -- The 'address' column now includes the new 'zip' field.
> DESCRIBE TABLE t2;
> +---------+--------------------------------------------------+-----+-----------------------------------+
> | name    | type                                             | ... | schema evolution record           |
> |---------+--------------------------------------------------+-----+-----------------------------------|
> | name    | VARCHAR(16777216)                                | ... | NULL                              |
> | address | OBJECT(city VARCHAR(16777216), zip NUMBER(10,0)) | ... | {"evolutionType":"ADD_FIELD",...} |
> +---------+--------------------------------------------------+-----+-----------------------------------+
> ```

## Troubleshoot schema detection and evolution

The following problems might occur when you create tables from staged files or load files with schema evolution:

- **`template must be a non-null JSON array`:** `INFER_SCHEMA` returned no rows. Run the `INFER_SCHEMA` query by itself to check
  the `LOCATION` and file format. With `INFER_NESTED_TYPES => TRUE`, the function also skips Parquet files that contain maps whose
  keys aren’t strings or integers. For these files, create a table that has a `VARIANT` column for each of these maps, set
  `ENABLE_SCHEMA_EVOLUTION = TRUE`, and load the files with `MATCH_BY_COLUMN_NAME` and `INFER_NESTED_TYPES = TRUE`. Schema
  evolution adds the other columns.
- **A new nested column isn’t added, and Snowflake doesn’t return an error:** Check that the table has
  `ENABLE_SCHEMA_EVOLUTION = TRUE`, that the statement sets `MATCH_BY_COLUMN_NAME`, and that the role that loads the data has the
  `EVOLVE SCHEMA` or `OWNERSHIP` privilege on the table. For Snowpipe, check the role that owns the pipe. Correcting these settings
  affects only later loads. To get the column’s values from files that were already loaded, reload the files into a new table, as
  described in [Move existing data to structured columns](#label-schema-evolution-structured-types-migrate-variant).
- **A new nested column is added as `VARIANT` or semi-structured `ARRAY`:** The load didn’t set `INFER_NESTED_TYPES = TRUE`, or
  the column has `UNION` types that are [always added as VARIANT](/user-guide/data-load-schema-evolution#label-schema-evolution-variant-columns). To move the
  column’s data to a structured column, see [Move existing data to structured columns](#label-schema-evolution-structured-types-migrate-variant).
- **`Typed object schema mismatch in conversion`:** A record doesn’t match a structured column’s type. The error doesn’t identify
  the field. The following causes are common:

  - The record has a new field that schema evolution didn’t add. Check that the statement sets `INFER_NESTED_TYPES = TRUE` and
    meets the requirements in [Create a table with structured columns from your files](#label-schema-evolution-structured-types-create).
  - A value doesn’t fit a field’s type. Create a table with wider types and reload the files. In a Snowflake-managed Iceberg table,
    you can [widen the field](/sql-reference/sql/alter-iceberg-table-alter-column-set-data-type) instead.
  - The record has ORC map data for a `MAP` column, or a new field inside a `MAP` value in a JSON file. Use a `VARIANT` column.

  To find the field, run `INFER_SCHEMA` with `INFER_NESTED_TYPES => TRUE` on the file that failed, and compare the result with the
  output of [DESCRIBE TABLE](/sql-reference/sql/desc-table).
- **`Unsupported data type 'VARIANT' for iceberg tables` or `Unsupported data type 'ARRAY' for iceberg tables`:** A load into a
  Snowflake-managed Iceberg table would add a column type that the table doesn’t support. Set `INFER_NESTED_TYPES = TRUE`. If the
  column must be `VARIANT`, use an Iceberg v3 table. For more information, see [Create and evolve Snowflake-managed Iceberg tables](#label-schema-evolution-structured-types-iceberg).
- **`infer_nested_types is not supported with copy transform`:** The statement combines `INFER_NESTED_TYPES`, set to any value,
  with a `SELECT` transform. Remove the option, or replace the transform with `MATCH_BY_COLUMN_NAME`, as described in
  [Add INFER\_NESTED\_TYPES to an existing load](#label-schema-evolution-structured-types-existing-load).
- **`adding too many structured fields`:** The load would add more than 100 fields, often because JSON objects use data values as
  keys. Create a table that has a `VARIANT` column for the data, and then reload the files. To request a higher limit,
  contact [Snowflake Support](/user-guide/contacting-support).
- **`Schema evolution is incomplete`:** The files in the statement need more than one schema change, and a `COPY` operation applies
  one change by default. Run the statement again until it succeeds. Each run applies one more change, and only the run that
  succeeds loads the files.
- **A `MAP` column contains a single `key_value` entry, or the load fails with `Numeric value 'key_value' is not recognized`:** The
  load sets neither `INFER_NESTED_TYPES = TRUE` nor `USE_VECTORIZED_SCANNER = TRUE`. Set `INFER_NESTED_TYPES = TRUE`. If the load
  uses a `SELECT` transform, set `USE_VECTORIZED_SCANNER = TRUE` instead. Rows that were already loaded don’t change.
- **`Cannot load Parquet MAP field`:** The file has a map whose values are lists. Set the
  [USE\_VECTORIZED\_SCANNER](/sql-reference/sql/copy-into-table#label-use-vectorized-scanner) file format option to `TRUE`.
- **`Invalid Map Key found in parquet file` or `Using a non-primitive Map Key is not supported`:** `MAP` columns can’t store the
  map’s keys. Use a `VARIANT` column: add one before you load the files, or create a table that has one and reload the files. In a
  Snowflake-managed Iceberg table, `VARIANT` columns require Iceberg v3. `INFER_SCHEMA` with `KIND => 'ICEBERG'` returns the same
  errors.
- **Snowpipe doesn’t load a file again after you fix the problem:** With the default `ON_ERROR = SKIP_FILE` setting, Snowpipe
  skips each file that contains a record that fails to load. To find these files, look for the `Load failed` status in the output
  of the [COPY\_HISTORY](/sql-reference/functions/copy_history) function. For files that a pipe skipped before you recreated it, use the
  [COPY\_HISTORY view](/sql-reference/account-usage/copy_history). To load the files, see
  [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).
