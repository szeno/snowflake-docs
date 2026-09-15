# Snowpark Library for Python release notes for 2026

This article contains the release notes for the [Snowpark Library for Python](/developer-guide/snowpark/python/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for [Snowpark Library for Python](/developer-guide/snowpark/python/index) updates.

See [Snowpark Developer Guide for Python](/developer-guide/snowpark/python/index) for documentation.

Warning

Because Python 3.8 has reached its [End of Life](https://devguide.python.org/versions/), deprecation warnings will be triggered when you use `snowpark-python` with Python 3.8. For more information, see [Snowflake Python Runtime Support](/developer-guide/python-runtime-support-policy). Snowpark Python 1.24.0 will be the last client and server version to support Python 3.8, in accordance with [Anaconda’s policy](https://forum.anaconda.com/t/python-3-8-reaches-end-of-life/87265). Upgrade your existing Python 3.8 objects to Python 3.9 or later.

## Version 1.54.0: Jul 29, 2026

### New features

- Added the `ai_count_tokens` function to `snowflake.snowpark.functions` to estimate token counts for AI function calls.
- Added the `ai_multi_embed` function to `snowflake.snowpark.functions` to generate multimodal embeddings from text, images, audio, or video files.
- Added the `ai_redact` function to `snowflake.snowpark.functions` to detect and redact personally identifiable information (PII) from text.
- Added the `DataFrame.ai.multi_embed` method to generate multimodal embeddings via the DataFrame API.
- Added the `DataFrame.ai.redact` method to detect and redact PII from text columns via the DataFrame API.
- Added the `DataFrame.ai.translate` method to translate text columns between languages via the DataFrame API.

### Improvements

- Removed the `experimental` tag from all AI SQL functions in `DataFrameAIFunctions` (`complete`, `filter`, `agg`, `classify`, `similarity`, `sentiment`, `embed`, `summarize_agg`, `transcribe`, `parse_document`, `extract`, `count_tokens`, `split_text_markdown_header`, `split_text_recursive_character`) and `RelationalGroupedDataFrame.ai_agg`.
- Updated `DataFrame.ai.count_tokens` to match the standalone `ai_count_tokens` function: `function_name` is now the required first parameter, and `model` is optional. This method also adds `options` and `return_error_details` parameters.

### Bug fixes

- Fixed a bug where `DataFrame.ai.count_tokens` called the deprecated `SNOWFLAKE.CORTEX.COUNT_TOKENS` function instead of the `AI_COUNT_TOKENS` SQL function. Token counts may differ slightly due to the updated tokenizer.
- Reverted the change introduced in 1.53.0 that eliminated unnecessary `SELECT *` from joins, which was causing performance regressions. This has no functional impact.

## Version 1.53.1: Jul 14, 2026

No user-facing changes in this release.

## Version 1.53.0: Jul 09, 2026

### New features

- Added the `udf_init_once` decorator in `snowflake.snowpark.functions` for marking functions to be executed once during pre-fork initialization on Snowflake workers, matching the server-side `_snowflake.udf_init_once` API.

### Bug fixes

- Fixed a bug where stage paths and file format names that contain single quotes were not consistently escaped when generating SQL, which could produce malformed statements. This affects `INFER_SCHEMA` (used by `DataFrameReader.csv`/`json`/`parquet`/`orc`/`avro`) and `COPY FILES` (used by `FileOperation.copy_files`).
- Fixed a bug where single quotes and backslashes in stage/file paths were not correctly escaped when generating `COPY INTO` / `PUT` / `GET` SQL, which could produce malformed statements. This affects `DataFrame.write.csv`/`copy_into_location` and the Snowpark-pandas `DataFrame.to_csv` stage path.
- Fixed a bug where column names containing quote characters returned by an external database were not correctly escaped when generating the `SELECT` query for `DataFrameReader.dbapi`, which could produce malformed SQL. Embedded quote characters in identifiers are now doubled (backticks for Databricks/MySQL, double quotes for Oracle/PostgreSQL/SQL Server).
- Fixed a bug where the destination passed to `DataFrameWriter.copy_into_location` (and `csv`/`json`/`parquet`/`save`) was embedded into the generated `COPY INTO` statement without quoting, which could produce malformed SQL for locations containing single quotes. The location is now consistently quoted and escaped, and a string that merely starts and ends with a single quote but contains unescaped interior quotes is no longer treated as an already-quoted literal; it is fully escaped so it stays a single SQL string literal.
- Fixed a bug where UDF default argument values reconstructed from a source file in `register_from_file` were evaluated with `eval()`; they are now evaluated only against the documented set of supported default-value types, and unsupported expressions are ignored.
- Fixed a bug where `object_name`, `object_domain`, or `object_version` values containing single quotes or backslashes in `session.lineage.trace()` caused incorrect SQL generation. These values are now properly escaped before being embedded in the `SYSTEM$DGQL` call.
- Fixed a bug where single quotes and backslashes in `comment` (`create_or_replace_view` / dynamic table / `save_as_table`), collation specs (`Column.collate`), VARIANT/OBJECT subfield keys (`Column[...]`), and `DataFrame`/`Session.flatten` paths were not correctly escaped when generating SQL, which could produce malformed statements. Backslash sequences (for example, `\t`, `\n`) in these values are now applied literally rather than interpreted.
- Fixed a bug where string values in the AI functions (`ai_extract`, `ai_classify`, `ai_similarity`, `ai_parse_document`, `ai_transcribe`, `ai_complete`) configuration and `response_format` were not correctly escaped when generating the SQL object literal, which could produce malformed statements when a value contained single quotes or backslashes (for example, an apostrophe in a natural-language question).

### Dependency updates

- Lifted `protobuf` restriction for Python 3.14 from `==5.29.3` to `>=5.29.3,<6.34`.
- Capped `pandas` to `<3.0.0` for the `[pandas]` install extra, as Snowpark Python pandas-related features may not be fully compatible with pandas 3.0 or later.

## Version 1.52.0: Jun 10, 2026

### New features

- Added `get_wif_token` to `snowflake.snowpark.secrets` for workload identity federation tokens on the Snowflake server (not available in SPCS file-based secret environments).

### Bug fixes

- Fixed a bug where copying a `DataFrame` via `copy.copy()` lost post-aggregate state, causing subsequent `.limit()` or `.sort()` to generate incorrect SQL.
- Fixed a bug where calling `DataFrame.alias()` twice on the same DataFrame (for example, for a self-join) caused both aliases to share the same internal column-mapping dictionary. This made `col("R", "col")` resolve to the same column as `col("L", "col")`, producing incorrect join conditions and filter expressions.
- Fixed a bug where `cloudpickle` could not be resolved when registering a Python stored procedure or UDF with `runtime_version='3.13'`.

### Improvements

- Improved CTE optimization to deduplicate identical subtrees in self-joins, which were previously emitted as repeated subqueries.
- Reduced the size of generated query text for repeated join operations.

### Deprecations

- Removed support for Python 3.9.

## Version 1.51.1: May 28, 2026

### Documentation

- Clarified that the JDBC driver JAR referenced via `udtf_configs.imports` in `DataFrameReader.jdbc()` must be downloaded from the database vendor and uploaded to a Snowflake stage.

## Version 1.51.0: May 18, 2026

### Bug fixes

- Fixed a bug where `AsyncJob.result("no_result")` sometimes silently returned without raising an error for failed queries.
- Fixed a bug where `INTERVAL YEAR TO MONTH` values with zero months were displayed incorrectly (for example, `INTERVAL '0-4' YEAR TO MONTH` instead of `INTERVAL '4-0' YEAR TO MONTH`) when using `snowflake-connector-python>=4.3.0`.

### Improvements

- When `Session.reduce_describe_query_enabled` is enabled, fewer DESCRIBE queries are issued when the outer query only projects or renames columns from an inner subquery whose column types are already known.

## Version 1.50.1: May 06, 2026

### Bug fixes

- Fixed a bug where using parameter bindings for `CALL` queries issued through `session.sql` would raise an error.
- Fixed a bug where `StringType` columns from Iceberg tables were not recognized as max-size strings.
- Improved the `FileNotFoundError` message raised when `INFER_SCHEMA` returns zero rows so it also points to file format options (`PARSE_HEADER`, `SKIP_HEADER`, `ON_ERROR=CONTINUE`) that can silently filter everything out, instead of only suggesting a missing path.

## Version 1.50.0: Apr 23, 2026

### New features

- Added `artifact_repository` support to `udtf_configs` in `session.read.dbapi()`, enabling users to specify a custom artifact repository (for example, PyPI) for packages used by the internal UDTF during distributed ingestion.

### Bug fixes

- Fixed a bug where the `TRY_CAST` reader option was ignored when calling `DataFrameReader.schema().csv()`.
- Fixed a bug where `event_table_telemetry` was using incorrect resource attributes.
- Fixed a bug where `value_contains_null` was not propagated for `MapType` in `_as_nested` function.
- Fixed a bug where CTE optimization incorrectly deduplicated subtrees containing non-deterministic data generation functions (for example, `uuid_string()`).
- Fixed a bug where vectorized UDFs using non-Anaconda package repositories did not specify the pandas package by default.

### Snowpark pandas API updates

#### Dependency updates

- Updated the supported `pandas` versions to <=2.4 (was previously <=2.3.1).

## Version 1.49.0: Apr 13, 2026

### New features

- Allow a user-specified schema when reading Parquet files from a stage.

### Improvements

- Restored the following query improvements that were reverted in 1.47.0 due to bugs:
  - Reduced the size of queries generated by certain `DataFrame.join` operations.
  - Removed redundant aliases in generated queries (for example, `SELECT "A" AS "A"` is now always simplified to `SELECT "A"`).
- Removed warning that `DataFrameReader.dbapi` feature was in private preview.

### Bug fixes

- Fixed a bug where `Session.create_dataframe` raised `TypeError` when a `StringType` column was given a non-string Python value (for example, `int`, `float`, `bool`, `Decimal`) for a small local relation (below the array bind threshold); `VALUES` SQL generation now coerces these types to string literals, consistent with the large-data bind-parameter path.
- Fixed a bug where `DataFrame.approxQuantile` did not accept a `Column` for the `col` parameter.

### Snowpark Local Testing updates

#### Bug fixes

- Fixed a bug where `concat` produced extra NaN rows and mismatched values after a `filter` operation in local testing.
- Fixed a bug where `dense_rank()` would fail with `ValueError` on NULL partition values.
- Fixed a bug where `collect()` raised `KeyError` after `save_as_table(column_order="name")` when the source DataFrame omitted columns with types `VariantType`, `MapType`, or `ArrayType` that were present in the target table schema in local testing.

## Version 1.48.1: Mar 31, 2026

### Bug fixes

- Fixed a bug where chained `DataFrame.filter()` calls with raw SQL text containing `OR` produced incorrect results.
- Fixed a Snowflake platform compatibility issue where `concat(lit('"'), ...)` could lose the leading quote through chained set-operation plans.
- Fixed a bug for XML schema inference session resolution in Spark-compatible mode.

## Version 1.48.0: Mar 23, 2026

### New features

- Added support for DIRECTED JOIN.
- Added support for the `INCLUDE_METADATA` copy option in `DataFrame.copy_into_table`, allowing users to include file metadata columns in the target table.

### Bug fixes

- Fixed a bug in `Session.client_telemetry` where traces did not include a Snowflake-style trace ID.
- Fixed a bug where saving a Snowpark DataFrame into an Iceberg table in overwrite mode raised an error because `StringType` was saved with the wrong length.
- Fixed a bug in `ai_complete` where `model_parameters` and `response_format` values containing single quotes would generate malformed SQL.
- Fixed a bug in `DataFrameReader.xml()` where reading XML with a custom schema whose field names contain colons (for example, `px:name`) raised a `SnowparkColumnException`.
- Fixed a bug in `Session.read.json` that caused SQL compilation errors when `INFER_SCHEMA` was set to True and the `USE_RELAXED_TYPES` field of `INFER_SCHEMA_OPTIONS` was also set to True.
- Fixed a bug where passing a DataFrame created from a SQL `SET` command to Streamlit’s `st.write` method would raise an exception.
- Fixed a bug where the account-level default artifact repository setting was not reflected in creation of stored procedures/UDFs.

### Improvements

- Use internal describe to get return type when executing a stored procedure.

## Version 1.47.0: Mar 05, 2026

### New features

- Added support for the `array_union_agg` function in the `snowflake.snowpark.functions` module.

### Bug fixes

- Fixed a bug where `Session.udf.register_from_file` did not properly process the `strict` and `secure` parameters.
- Fixed a bug where an error was raised on a string value in a `DecimalType` column when creating a DataFrame with small data (< array binding threshold).
- Reverted the following improvements introduced in 1.46.0 as they caused unintended breaking changes in some query patterns:
  - Reduced the size of queries generated by certain `DataFrame.join` operations.
  - Removed redundant aliases in generated queries (for example, `SELECT "A" AS "A"` is now always simplified to `SELECT "A"`).

## Version 1.46.0: Feb 25, 2026

### New features

- Added support for the `DECFLOAT` data type that allows users to represent decimal numbers exactly with 38 digits of precision and a dynamic base-10 exponent.
- Added support for the `DEFAULT_PYTHON_ARTIFACT_REPOSITORY` parameter that allows users to configure the default artifact repository at the account, database, and schema level.

### Bug fixes

- Fixed a bug where `cloudpickle` was not automatically added to the package list when using `artifact_repository` with custom packages, causing `ModuleNotFoundError` at runtime.
- Fixed a bug when reading XML with a custom schema that resulted in element attributes being included when a column was not of the `StructType` type.
- Fixed a bug where `Session.udf.register_from_file` did not properly process the `strict` and `secure` parameters.

### Improvements

- Reduced the size of queries generated by certain `DataFrame.join` operations.
- Removed redundant aliases in generated queries (for example, `SELECT "A" AS "A"` is now always simplified to `SELECT "A"`).

## Version 1.45.0: Jan 26, 2026

### New features

- Allow user input schema when reading an XML file on a stage.
- Added support for the following functions in `functions.py`:

  - `hex_decode_string`
  - `jarowinkler_similarity`
  - `parse_url`
  - `regexp_instr`
  - `regexp_like`
  - `regexp_substr`
  - `regexp_substr_all`
  - `rtrimmed_length`
  - `space`
  - `split_part`
- Added the `preserve_parameter_names` flag to stored procedure, UDF, UDTF, and UDAF creation.

### Bug fixes

- Fixed a bug where `opentelemetry` was not correctly imported when using `Session.client_telemetry.enable_event_table_telemetry_collection`.

### Improvements

- `snowflake.snowpark.context.configure_development_features` is effective for multiple sessions including newly created sessions after the configuration. There is no longer a duplicate experimental warning.
- Removed the experimental warning from `DataFrame.to_arrow` and `DataFrame.to_arrow_batches`.
- When both `Session.reduce_describe_query_enabled` and `Session.cte_optimization_enabled` are enabled, fewer `DESCRIBE` queries are issued when resolving a table schema.
