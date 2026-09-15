# Snowpark Library for Python release notes for 2025

This article contains the release notes for the [Snowpark Library for Python](/developer-guide/snowpark/python/index), including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for [Snowpark Library for Python](/developer-guide/snowpark/python/index) updates.

See [Snowpark Developer Guide for Python](/developer-guide/snowpark/python/index) for documentation.

Warning

Because Python 3.8 has reached its [End of Life](https://devguide.python.org/versions/), deprecation warnings will be triggered when you use snowpark-python with Python 3.8. For more information, see [Snowflake Python Runtime Support](/developer-guide/python-runtime-support-policy). Snowpark Python 1.24.0 will be the last client and server version to support Python 3.8, in accordance with [Anaconda’s policy](https://forum.anaconda.com/t/python-3-8-reaches-end-of-life/87265). Upgrade your existing Python 3.8 objects to Python 3.9 or later.

## Version 1.44.0: Dec 15, 2025

### New features

- Added support for targeted delete-insert via the `overwrite_condition` parameter in `DataFrameWriter.save_as_table`.

### Improvements

- Improved `DataFrameReader` to return columns in deterministic order when using `INFER_SCHEMA`.
- Added a dependency on `protobuf<6.34` (was `<6.32`).

## Version 1.43.0: Dec 03, 2025

### New features

- Added support for `DataFrame.lateral_join`
- Added support for Private Preview feature `Session.client_telemetry`.
- Added support for `Session.udf_profiler`.
- Added support for `functions.ai_translate`.
- Added support for the following `iceberg_config` options in `DataFrameWriter.save_as_table` and `DataFrame.copy_into_table`:

  - `target_file_size`
  - `partition_by`
- Added support for the following functions in `functions.py`:

  - String and Binary functions:

    - `base64_decode_binary`
    - `bucket`
    - `compress`
    - `day`
    - `decompress_binary`
    - `decompress_string`
    - `md5_binary`
    - `md5_number_lower64`
    - `md5_number_upper64`
    - `sha1_binary`
    - `sha2_binary`
    - `soundex_p123`
    - `strtok`
    - `truncate`
    - `try_base64_decode_binary`
    - `try_base64_decode_string`
    - `try_hex_decode_binary`
    - `try_hex_decode_string`
    - `unicode`
    - `uuid_string`
  - Conditional expressions:

    - `booland_agg`
    - `boolxor_agg`
    - `regr_valy`
    - `zeroifnull`
  - Numeric expressions:

    - `cot`
    - `mod`
    - `pi`
    - `square`
    - `width_bucket`

### Bug fixes

- Fixed a bug where automatically-generated temporary objects were not properly cleaned up.
- Fixed a bug in SQL generation when joining two `DataFrames` created using `DataFrame.alias` and CTE optimization is enabled.
- Fixed a bug in `XMLReader` where finding the start position of a row tag could return an incorrect file position.

### Improvements

- Enhanced `DataFrame.sort()` to support ORDER BY ALL when no columns are specified.
- Removed experimental warning from `Session.cte_optimization_enabled`.

### Snowpark pandas API updates

#### New features

- Added support for `DataFrame.groupby.rolling()`.
- Added support for mapping `np.percentile` with DataFrame and Series inputs to `Series.quantile`.
- Added support for setting the `random_state` parameter to an integer when calling `DataFrame.sample` or `Series.sample`.
- Added support for the following `iceberg_config` options in `to_iceberg`:
  - `target_file_size`
  - `partition_by`

#### Improvements

- Enhanced autoswitching functionality from Snowflake to native pandas for methods with unsupported argument combinations:

  - `shift()` with `suffix` or non-integer `periods` parameters
  - `sort_index()` with `axis=1` or `key` parameters
  - `sort_values()` with `axis=1`
  - `melt()` with `col_level` parameter
  - `apply()` with `result_type` parameter for DataFrame
  - `pivot_table()` with `sort=True`, non-string `index` list, non-string `columns` list, non-string `values` list, or `aggfunc` dict with non-string values
  - `fillna()` with `downcast` parameter or using `limit` together with `value`
  - `dropna()` with `axis=1`
  - `asfreq()` with `how` parameter, `fill_value` parameter, `normalize=True`, or `freq` parameter being week, month, quarter, or year
  - `groupby()` with `axis=1`, `by!=None and level!=None`, or by containing any non-pandas hashable labels.
  - `groupby_fillna()` with `downcast` parameter
  - `groupby_first()` with `min_count>1`
  - `groupby_last()` with `min_count>1`
  - `groupby_shift()` with `freq` parameter
- Slightly improved the performance of `agg`, `nunique`, `describe`, and related methods on 1-column DataFrame and Series objects.
- Add support for the following in faster pandas:

  - `groupby.apply`
  - `groupby.nunique`
  - `groupby.size`
  - `concat`
  - `copy`
  - `str.isdigit`
  - `str.islower`
  - `str.isupper`
  - `str.istitle`
  - `str.lower`
  - `str.upper`
  - `str.title`
  - `str.match`
  - `str.capitalize`
  - `str.__getitem__`
  - `str.center`
  - `str.count`
  - `str.get`
  - `str.pad`
  - `str.len`
  - `str.ljust`
  - `str.rjust`
  - `str.split`
  - `str.replace`
  - `str.strip`
  - `str.lstrip`
  - `str.rstrip`
  - `str.translate`
  - `dt.tz_localize`
  - `dt.tz_convert`
  - `dt.ceil`
  - `dt.round`
  - `dt.floor`
  - `dt.normalize`
  - `dt.month_name`
  - `dt.day_name`
  - `dt.strftime`
  - `dt.dayofweek`
  - `dt.weekday`
  - `dt.dayofyear`
  - `dt.isocalendar`
  - `rolling.min`
  - `rolling.max`
  - `rolling.count`
  - `rolling.sum`
  - `rolling.mean`
  - `rolling.std`
  - `rolling.var`
  - `rolling.sem`
  - `rolling.corr`
  - `expanding.min`
  - `expanding.max`
  - `expanding.count`
  - `expanding.sum`
  - `expanding.mean`
  - `expanding.std`
  - `expanding.var`
  - `expanding.sem`
  - `cumsum`
  - `cummin`
  - `cummax`
  - `groupby.groups`
  - `groupby.indices`
  - `groupby.first`
  - `groupby.last`
  - `groupby.rank`
  - `groupby.shift`
  - `groupby.cumcount`
  - `groupby.cumsum`
  - `groupby.cummin`
  - `groupby.cummax`
  - `groupby.any`
  - `groupby.all`
  - `groupby.unique`
  - `groupby.get_group`
  - `groupby.rolling`
  - `groupby.resample`
  - `to_snowflake`
  - `to_snowpark`
  - `resample.min`
  - `resample.max`
  - `resample.count`
  - `resample.sum`
  - `resample.mean`
  - `resample.median`
  - `resample.std`
  - `resample.var`
  - `resample.size`
  - `resample.first`
  - `resample.last`
  - `resample.quantile`
  - `resample.nunique`
- Make faster pandas disabled by default (opt-in instead of opt-out).
- Improve performance of `drop_duplicates` by avoiding joins when `keep!=False` in faster pandas.

#### Bug fixes

- Fixed a bug in `DataFrameGroupBy.agg` where func is a list of tuples used to set the names of the output columns.
- Fixed a bug where converting a modin datetime index with a timezone to a numpy array with `np.asarray` would cause a `TypeError`.
- Fixed a bug where `Series.isin` with a Series argument matched index labels instead of the row position.

## Version 1.42.0: Oct 29, 2025

### New features

- Snowpark Python DB-API is now generally available.

  To access this feature, use `DataFrameReader.dbapi()` to read data from a database table or query into a DataFrame using a DB-API connection.

## Version 1.41.0: Oct 23, 2025

### New features

- Added a new function `service` in `snowflake.snowpark.functions` that allows users to create a callable representing a Snowpark Container Services (SPCS) service.
- Added a new function `group_by_all()` to the `DataFrame` class.
- Added `connection_parameters` parameter to `DataFrameReader.dbapi()` (Public Preview) method to allow passing keyword arguments to the `create_connection` callable.
- Added support for `Session.begin_transaction`, `Session.commit`, and `Session.rollback`.
- Added support for the following functions in `functions.py`:

  - Geospatial functions:
    - `st_interpolate`
    - `st_intersection`
    - `st_intersection_agg`
    - `st_intersects`
    - `st_isvalid`
    - `st_length`
    - `st_makegeompoint`
    - `st_makeline`
    - `st_makepolygon`
    - `st_makepolygonoriented`
    - `st_disjoint`
    - `st_distance`
    - `st_dwithin`
    - `st_endpoint`
    - `st_envelope`
    - `st_geohash`
    - `st_geomfromgeohash`
    - `st_geompointfromgeohash`
    - `st_hausdorffdistance`
    - `st_makepoint`
    - `st_npoints`
    - `st_perimeter`
    - `st_pointn`
    - `st_setsrid`
    - `st_simplify`
    - `st_srid`
    - `st_startpoint`
    - `st_symdifference`
    - `st_transform`
    - `st_union`
    - `st_union_agg`
    - `st_within`
    - `st_x`
    - `st_xmax`
    - `st_xmin`
    - `st_y`
    - `st_ymax`
    - `st_ymin`
    - `st_geogfromgeohash`
    - `st_geogpointfromgeohash`
    - `st_geographyfromwkb`
    - `st_geographyfromwkt`
    - `st_geometryfromwkb`
    - `st_geometryfromwkt`
    - `try_to_geography`
    - `try_to_geometry`
- Added a parameter to enable and disable automatic column name aliasing for `interval_day_time_from_parts` and `interval_year_month_from_parts` functions.

### Bug fixes

- Fixed a bug that `DataFrameReader.xml` fails to parse XML files with undeclared namespaces when `ignoreNamespace` is `True`.
- Added a fix for floating point precision discrepancies in `interval_day_time_from_parts`.
- Fixed a bug where writing Snowpark pandas DataFrames on the pandas backend with a column multiindex to Snowflake with `to_snowflake` would raise `KeyError`.
- Fixed a bug that `DataFrameReader.dbapi` (Public Preview) is not compatible with oracledb 3.4.0.
- Fixed a bug where `modin` would unintentionally be imported during session initialization in some scenarios.
- Fixed a bug where `session.udf%udtf%udaf|sproc.register` failed when an extra session argument was passed. These methods do not expect a session argument; please remove it if provided.

### Improvements

- The default maximum length for inferred StringType columns during schema inference in `DataFrameReader.dbapi` is now increased from 16 MB to 128 MB in parquet file–based ingestion.

### Dependency updates

- Updated dependency of `snowflake-connector-python>=3.17,<5.0.0`.

### Snowpark pandas API updates

#### New features

- Added support for the `dtypes` parameter of `pd.get_dummies`.
- Added support for `nunique` in `df.pivot_table`, `df.agg`, and other places where aggregate functions can be used.
- Added support for `DataFrame.interpolate` and `Series.interpolate` with the “linear”, “ffill”/”pad”, and “backfill”/bfill” methods. These use the SQL `INTERPOLATE_LINEAR`, `INTERPOLATE_FFILL`, and `INTERPOLATE_BFILL` functions (Public Preview).

#### Improvements

- Improved performance of `Series.to_snowflake` and `pd.to_snowflake(series)` for large data by uploading data via a parquet file. You can control the dataset size at which Snowpark pandas switches to parquet with the variable `modin.config.PandasToSnowflakeParquetThresholdBytes`.
- Enhanced autoswitching functionality from Snowflake to native pandas for methods with unsupported argument combinations:

  - `get_dummies()` with `dummy_na=True`, `drop_first=True`, or custom `dtype` parameters
  - `cumsum()`, `cummin()`, `cummax()` with `axis=1` (column-wise operations)
  - `skew()` with `axis=1` or `numeric_only=False` parameters
  - `round()` with `decimals` parameter as a Series
  - `corr()` with `method!=pearson` parameter
- Set `cte_optimization_enabled` to True for all Snowpark pandas sessions.
- Add support for the following in faster pandas:

  - `isin`
  - `isna`
  - `isnull`
  - `notna`
  - `notnull`
  - `str.contains`
  - `str.startswith`
  - `str.endswith`
  - `str.slice`
  - `dt.date`
  - `dt.time`
  - `dt.hour`
  - `dt.minute`
  - `dt.second`
  - `dt.microsecond`
  - `dt.nanosecond`
  - `dt.year`
  - `dt.month`
  - `dt.day`
  - `dt.quarter`
  - `dt.is_month_start`
  - `dt.is_month_end`
  - `dt.is_quarter_start`
  - `dt.is_quarter_end`
  - `dt.is_year_start`
  - `dt.is_year_end`
  - `dt.is_leap_year`
  - `dt.days_in_month`
  - `dt.daysinmonth`
  - `sort_values`
  - `loc` (setting columns)
  - `to_datetime`
  - `drop`
  - `invert`
  - `duplicated`
  - `iloc`
  - `head`
  - `columns` (e.g., df.columns = [“A”, “B”])
  - `agg`
  - `min`
  - `max`
  - `count`
  - `sum`
  - `mean`
  - `median`
  - `std`
  - `var`
  - `groupby.agg`
  - `groupby.min`
  - `groupby.max`
  - `groupby.count`
  - `groupby.sum`
  - `groupby.mean`
  - `groupby.median`
  - `groupby.std`
  - `groupby.var`
  - `drop_duplicates`
- Reuse row count from the relaxed query compiler in `get_axis_len`.

#### Bug fixes

- Fixed a bug where the row count was not cached in the ordered DataFrame each time `count_rows()` was called.

## Version 1.40.0: October 6, 2025

### New features

- Added a new module `snowflake.snowpark.secrets` that provides Python wrappers for accessing Snowflake Secrets within Python UDFs and stored procedures that execute inside Snowflake.

  - `get_generic_secret_string`
  - `get_oauth_access_token`
  - `get_secret_type`
  - `get_username_password`
  - `get_cloud_provider_token`
- Added support for the following scalar functions in `functions.py`:

  - Conditional expression functions:

    - `booland`
    - `boolnot`
    - `boolor`
    - `boolxor`
    - `boolor_agg`
    - `decode`
    - `greatest_ignore_nulls`
    - `least_ignore_nulls`
    - `nullif`
    - `nvl2`
    - `regr_valx`
  - Semi-structured and structured date functions:

    - `array_remove_at`
    - `as_boolean`
    - `map_delete`
    - `map_insert`
    - `map_pick`
    - `map_size`
  - String & binary functions:

    - `chr`
    - `hex_decode_binary`
  - Numeric functions:

    - `div0null`
  - Differential privacy functions:

    - `dp_interval_high`
    - `dp_interval_low`
  - Context functions:

    - `last_query_id`
    - `last_transaction`
  - Geospatial functions:

    - `h3_cell_to_boundary`
    - `h3_cell_to_children`
    - `h3_cell_to_children_string`
    - `h3_cell_to_parent`
    - `h3_cell_to_point`
    - `h3_compact_cells`
    - `h3_compact_cells_strings`
    - `h3_coverage`
    - `h3_coverage_strings`
    - `h3_get_resolution`
    - `h3_grid_disk`
    - `h3_grid_distance`
    - `h3_int_to_string`
    - `h3_polygon_to_cells`
    - `h3_polygon_to_cells_strings`
    - `h3_string_to_int`
    - `h3_try_grid_path`
    - `h3_try_polygon_to_cells`
    - `h3_try_polygon_to_cells_strings`
    - `h3_uncompact_cells`
    - `h3_uncompact_cells_strings`
    - `haversine`
    - `h3_grid_path`
    - `h3_is_pentagon`
    - `h3_is_valid_cell`
    - `h3_latlng_to_cell`
    - `h3_latlng_to_cell_string`
    - `h3_point_to_cell`
    - `h3_point_to_cell_string`
    - `h3_try_coverage`
    - `h3_try_coverage_strings`
    - `h3_try_grid_distance`
    - `st_area`
    - `st_asewkb`
    - `st_asewkt`
    - `st_asgeojson`
    - `st_aswkb`
    - `st_aswkt`
    - `st_azimuth`
    - `st_buffer`
    - `st_centroid`
    - `st_collect`
    - `st_contains`
    - `st_coveredby`
    - `st_covers`
    - `st_difference`
    - `st_dimension`

### Bug fixes

- Fixed a bug that caused `DataFrame.limit()` to fail if the executed SQL contained parameter binding when used in non-stored-procedure/udxf environments.
- Added an experimental fix for a bug in schema query generation that could cause invalid sql to be generated when using nested structured types.
- Fixed multiple bugs in `DataFrameReader.dbapi` (Public Preview):

  - Fixed UDTF ingestion failure with `pyodbc` driver caused by unprocessed row data.
  - Fixed SQL Server query input failure due to incorrect select query generation.
  - Fixed UDTF ingestion not preserving column nullability in the output schema.
  - Fixed an issue that caused the program to hang during multithreaded Parquet based ingestion when a data fetching error occurred.
  - Fixed a bug in schema parsing when custom schema strings used upper-cased data type names (`NUMERIC`, `NUMBER`, `DECIMAL`, `VARCHAR`, `STRING`, `TEXT`).
- Fixed a bug in `Session.create_dataframe` where schema string parsing failed when using upper-cased data type names (e.g., `NUMERIC`, `NUMBER`, `DECIMAL`, `VARCHAR`, `STRING`, `TEXT`).

### Improvements

- Improved `DataFrameReader.dbapi` (Public Preview) so it doesn’t retry on non-retryable errors, such as SQL syntax error on external data source query.
- Removed unnecessary warnings about local package version mismatch when using `session.read.option('rowTag', <tag_name>).xml(<stage_file_path>)` or `xpath` functions.
- Improved `DataFrameReader.dbapi` (Public Preview) reading performance by setting the default `fetch_size` parameter value to 100000.
- Improved error message for XSD validation failure when reading XML files using `session.read.option('rowValidationXSDPath', <xsd_path>).xml(<stage_file_path>)`.

### Snowpark pandas API updates

#### Dependency updates

- Updated the supported `modin` versions to >=0.36.0 and <0.38.0 (was >= 0.35.0 and <0.37.0).

#### New features

- Added support for `DataFrame.query` for DataFrames with single-level indexes.
- Added support for `DataFrameGroupby.__len__` and `SeriesGroupBy.__len__`.

#### Improvements

- Hybrid execution mode is now enabled by default. Certain operations on smaller data now automatically execute in native pandas in-memory. Use `from modin.config import AutoSwitchBackend; AutoSwitchBackend.disable()` to turn this off and force all execution to occur in Snowflake.
- Added a session parameter `pandas_hybrid_execution_enabled` to enable/disable hybrid execution as an alternative to using `AutoSwitchBackend`.
- Removed an unnecessary `SHOW OBJECTS` query issued from `read_snowflake` under certain conditions.
- When hybrid execution is enabled, `pd.merge`, `pd.concat`, `DataFrame.merge`, and `DataFrame.join` can now move arguments to backends other than those among the function arguments.
- Improved performance of `DataFrame.to_snowflake` and `pd.to_snowflake(dataframe)` for large data by uploading data via a parquet file. You can control the dataset size at which Snowpark pandas switches to parquet with the variable `modin.config.PandasToSnowflakeParquetThresholdBytes`.

## Version 1.39.1: September 25, 2025

### Bug fixes

- Added an experimental fix for a bug in schema query generation that could cause invalid SQL to be generated when using nested structured types.

## Version 1.39.0: September 17, 2025

### New features

- Downgraded to level `logging.DEBUG - 1` the log message saying that the
  Snowpark `DataFrame` reference of an internal `DataFrameReference` object
  has changed.
- Eliminate duplicate parameter check queries for casing status when retrieving the session.
- Retrieve DataFrame row counts through object metadata to avoid a COUNT(\*) query (performance)
- Added support for applying the Snowflake Cortex function `Complete`.
- Introduce faster pandas: Improved performance by deferring row position computation.

  - The following operations are currently supported and can benefit from the optimization: `read_snowflake`, `repr`, `loc`, `reset_index`, `merge`, and binary operations.
  - If a lazy object (e.g., DataFrame or Series) depends on a mix of supported and unsupported operations, the optimization will not be used.
- Updated the error message for when Snowpark pandas is referenced within `apply`.
- Added a session parameter `dummy_row_pos_optimization_enabled` to enable/disable dummy row position optimization in faster pandas.

### Dependency updates

- Updated the supported `modin` versions to >=0.35.0 and <0.37.0 (was previously >= 0.34.0 and <0.36.0).

### Bug fixes

- Fixed an issue with `drop_duplicates` where the same data source could be read multiple times in the same query but in a different order each time, resulting in missing rows in the final result. The fix ensures that the data source is read only once.
- Fixed a bug with hybrid execution mode where an `AssertionError` was unexpectedly raised by certain indexing operations.

### Snowpark local testing updates

#### New features

- Added support to allow patching `functions.ai_complete`.

## Version 1.38.0: September 4, 2025

### New features

- Added support for the following AI-powered functions in `functions.py`:

  - `ai_extract`
  - `ai_parse_document`
  - `ai_transcribe`
- Added time travel support for querying historical data:

  - `Session.table()` now supports time travel parameters:

    - `time_travel_mode`
    - `statement`
    - `offset`
    - `timestamp`
    - `timestamp_type`
    - `stream`
  - `DataFrameReader.table()` supports the same time travel parameters as direct arguments.
  - `DataFrameReader` supports time travel via option chaining (e.g., `session.read.option("time_travel_mode", "at").option("offset", -60).table("my_table")`).
- Added support for specifying the following parameters to `DataFrameWriter.copy_into_location` for validation and writing data to external locations:

  - `validation_mode`
  - `storage_integration`
  - `credentials`
  - `encryption`
- Added support for `Session.directory` and `Session.read.directory` to retrieve the list of all files on a stage with metadata.
- Added support for `DataFrameReader.jdbc(Private Preview)` that allows the JDBC driver to ingest external data sources.
- Added support for `FileOperation.copy_files` to copy files from a source location to an output stage.
- Added support for the following scalar functions in `functions.py`:

  - `all_user_names`
  - `bitand`
  - `bitand_agg`
  - `bitor`
  - `bitor_agg`
  - `bitxor`
  - `bitxor_agg`
  - `current_account_name`
  - `current_client`
  - `current_ip_address`
  - `current_role_type`
  - `current_organization_name`
  - `current_organization_user`
  - `current_secondary_roles`
  - `current_transaction`
  - `getbit`

### Bug fixes

- Fixed the `_repr_` of `TimestampType` to match the actual subtype it represents.
- Fixed a bug in `DataFrameReader.dbapi` that `UDTF` ingestion does not work in stored procedures.
- Fixed a bug in schema inference that caused incorrect stage prefixes to be used.

### Improvements

- Enhanced error handling in `DataFrameReader.dbapi` thread-based ingestion to prevent unnecessary operations, which improves resource efficiency.
- Bumped cloudpickle dependency to also support `cloudpickle==3.1.1` in addition to previous versions.
- Improved `DataFrameReader.dbapi` (Public Preview) ingestion performance for PostgreSQL and MySQL by using a server-side cursor to fetch data.

### Snowpark pandas API Updates

### New features

- Completed support for the following functions on the “Pandas” and “Ray” backends:

  - `pd.read_snowflake()`
  - `pd.to_iceberg()`
  - `pd.to_pandas()`
  - `pd.to_snowpark()`
  - `pd.to_snowflake()`
  - `DataFrame.to_iceberg()`
  - `DataFrame.to_pandas()`
  - `DataFrame.to_snowpark()`
  - `DataFrame.to_snowflake()`
  - `Series.to_iceberg()`
  - `Series.to_pandas()`
  - `Series.to_snowpark()`
  - `Series.to_snowflake()`

    on the “Pandas” and “Ray” backends. Previously, only some of these functions and methods were supported on the Pandas backend.
- Added support for `Index.get_level_values()`.

### Improvements

- Set the default transfer limit in hybrid execution for data leaving Snowflake to 100k, which can be overridden with the `SnowflakePandasTransferThreshold` environment variable. This configuration is appropriate for scenarios with two available engines, “pandas” and “Snowflake,” on relational workloads.
- Improved the import error message by adding `--upgrade` to `pip install "snowflake-snowpark-python[modin]"` in the message.
- Reduced the telemetry messages from the modin client by pre-aggregating into five-second windows and only keeping a narrow band of metrics that are useful for tracking hybrid execution and native pandas performance.
- Set the initial row count only when hybrid execution is enabled, which reduces the number of queries issued for many workloads.
- Added a new test parameter for integration tests to enable hybrid execution.

### Bug fixes

- Raised `NotImplementedError` instead of `AttributeError` on attempting to call
  Snowflake extension functions/methods `to_dynamic_table()`, `cache_result()`,
  `to_view()`, `create_or_replace_dynamic_table()`, and
  `create_or_replace_view()` on DataFrames or series using the pandas or ray
  backends.

## Version 1.37.0: August 18, 2025

### New features

- Added support for the following `xpath` functions in `functions.py`:

  - `xpath`
  - `xpath_string`
  - `xpath_boolean`
  - `xpath_int`
  - `xpath_float`
  - `xpath_double`
  - `xpath_long`
  - `xpath_short`
- Added support for the `use_vectorized_scanner` parameter in the `Session.write_arrow()` function.
- DataFrame profiler adds the following information about each query: `describe query time`, `execution time`, and `sql query text`. To view this information, call `session.dataframe_profiler.enable()` and call `get_execution_profile` on a DataFrame.
- Added support for `DataFrame.col_ilike`.
- Added support for non-blocking stored procedure calls that return `AsyncJob` objects.

  - Added the `block: bool = True` parameter to `Session.call()`. When `block=False`, returns an `AsyncJob` instead of blocking until completion.
  - Added the `block: bool = True` parameter to `StoredProcedure.__call__()` for async support across both named and anonymous stored procedures.
  - Added `Session.call_nowait()` that is equivalent to `Session.call(block=False)`.

### Bug fixes

- Fixed a bug in CTE optimization stage where `deepcopy` of internal plans would cause a memory spike when a DataFrame is created locally using `session.create_dataframe()` using large input data.
- Fixed a bug in `DataFrameReader.parquet` where the `ignore_case` option in the `infer_schema_options` was not respected.
- Fixed a bug where `to_pandas()` had a different format of column name when the query result format is set to `JSON` and `ARROW`.

### Deprecations

- Deprecated `pkg_resources`.

### Dependency updates

- Added a dependency on `protobuf<6.32`

### Snowpark pandas API Updates

### New features

- Added support for efficient transfer of data between Snowflake and [<Ray](https://www.ray.io/) with the `DataFrame.set_backend` method. The installed version of `modin` must be at least 0.35.0, and `ray` must be installed.

### Dependency updates

- Updated the supported modin versions to >=0.34.0 and <0.36.0 (was previously >= 0.33.0 and <0.35.0).
- Added support for pandas 2.3 when the installed modin version is 0.35.0 or greater.

### Bug fixes

- Fixed an issue in hybrid execution mode (Private Preview) where `pd.to_datetime` and `pd.to_timedelta` would unexpectedly raise `IndexError`.
- Fixed a bug where `pd.explain_switch` would raise `IndexError` or return `None` if called before any potential switch operations were performed.

## Version 1.36.0: August 5, 2025

### New features

- `Session.create_dataframe` now accepts keyword arguments that are forwarded in the internal call to `Session.write_pandas` or `Session.write_arrow` when creating a DataFrame from a pandas DataFrame or a `pyarrow` table.
- Added new APIs for AsyncJob:

  - `AsyncJob.is_failed()` returns a bool indicating whether a job has failed. Can be used in combination with `AsyncJob.is_done()` to determine if a job is finished and erred.
  - `AsyncJob.status()` returns a string representing the current query status (such as, “RUNNING”, “SUCCESS”, “FAILED\_WITH\_ERROR”) for detailed monitoring without calling `result()`.
- Added a DataFrame profiler. To use, you can call `get_execution_profile()` on your desired DataFrame. This profiler reports the queries executed to evaluate a DataFrame and statistics about each of the query operators. Currently an experimental feature.
- Added support for the following functions in `functions.py`:

  - `ai_sentiment`
- Updated the interface for the `context.configure_development_features` experimental feature. All development features are disabled by default unless explicitly enabled by the user.

### Improvements

- Hybrid execution row estimate improvements and a reduction of eager calls.
- Added a new configuration variable to control transfer costs out of Snowflake when using hybrid execution.
- Added support for creating permanent and immutable UDFs/UDTFs with DataFrame/Series/GroupBy.apply, map, and transform by passing the `snowflake_udf_params` keyword argument.
- Added support for `mapping np.unique` to DataFrame and Series inputs using `pd.unique`.

### Bug fixes

- Fixed an issue where the Snowpark pandas plugin would unconditionally disable `AutoSwitchBackend` even when users have explicitly configured it programmatically or with environment variables.

## Version 1.35.0: July 24, 2025

### New features

- Added support for the following functions in `functions.py`:
  - `ai_embed`
  - `try_parse_json`

### Improvements

- Improved `query` parameter in `DataFrameReader.dbapi` (Private Preview) so that parentheses aren’t needed around the query.
- Improved error experience in `DataFrameReader.dbapi` (Private Preview) for exceptions raised when inferring the schema of the target data source.

### Bug fixes

- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) that fails `dbapi` with process exit code 1 in a Python stored procedure.
- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) where `custom_schema` accepts an illegal schema.
- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) where `custom_schema` doesn’t work when connecting to Postgres and MySQL.
- Fixed a bug in schema inference that causes it to fail for external stages.

### Snowpark local testing updates

#### New features

- Added local testing support for reading files with `SnowflakeFile`. The testing support uses local file paths, the Snow URL semantic (`snow://...`), local testing framework stages, and Snowflake stages (`@stage/file_path`).

## Version 1.34.0: Jul 14, 2025

### New features

- Added a new option `TRY_CAST` to `DataFrameReader`. When `TRY_CAST` is `True`, columns are wrapped in a `TRY_CAST` statement instead of a hard cast when loading data.
- Added a new option `USE_RELAXED_TYPES` to the `INFER_SCHEMA_OPTIONS` of `DataFrameReader`. When set to `True`, this option casts all strings to max length strings and all numeric types to `DoubleType`.
- Added debuggability improvements to eagerly validate dataframe schema metadata. Enable it using `snowflake.snowpark.context.configure_development_features()`.
- Added a new function `snowflake.snowpark.dataframe.map_in_pandas` that allows users to map a function across a dataframe. The mapping function takes an iterator of pandas DataFrames as input and provides one as output.
- Added a `ttl cache` to describe queries. Repeated queries in a 15-second interval use the cached value rather than requery Snowflake.
- Added a parameter `fetch_with_process` to `DataFrameReader.dbapi` (PrPr) to enable multiprocessing for parallel data fetching in local ingestion. By default, local ingestion uses multithreading. Multiprocessing can improve performance for CPU-bound tasks like Parquet file generation.
- Added a new function `snowflake.snowpark.functions.model` that allows users to call methods of a model.

### Improvements

- Added support for row validation using XSD schema using `rowValidationXSDPath` option when reading XML files with a row tag using `rowTag` option.
- Improved SQL generation for `session.table().sample()` to generate a flat SQL statement.
- Added support for complex column expression as input for `functions.explode`.
- Added debuggability improvements to show which Python lines a SQL compilation error corresponds to. Enable it using `snowflake.snowpark.context.configure_development_features()`. This feature also depends on AST collections to be enabled in the session, which can be done using `session.ast_enabled = True`.
- Set `enforce_ordering=True` when calling `to_snowpark_pandas()` from a Snowpark DataFrame containing DML/DDL queries instead of throwing a `NotImplementedError`.

### Bug fixes

- Fixed a bug caused by redundant validation when creating an iceberg table.
- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) where closing the cursor or connection could unexpectedly raise an error and terminate the program.
- Fixed ambiguous column errors when using table functions in `DataFrame.select()` that have output columns matching the input DataFrame’s columns. This improvement works when DataFrame columns are provided as `Column` objects.
- Fixed a bug where having a NULL in a column with DecimalTypes would cast the column to FloatTypes instead and lead to precision loss.

### Snowpark Local testing Updates

- Fixed a bug when processing windowed functions that lead to incorrect indexing in results.
- When a scalar numeric is passed to `fillna`, Snowflake will ignore non-numeric columns instead of producing an error.

### Snowpark pandas API Updates

#### New features

- Added support for `DataFrame.to_excel` and `Series.to_excel`.
- Added support for `pd.read_feather`, `pd.read_orc`, and `pd.read_stata`.
- Added support for `pd.explain_switch()` to return debugging information on hybrid execution decisions.
- Support `pd.read_snowflake` when the global modin backend is `Pandas`.
- Added support for `pd.to_dynamic_table`, `pd.to_iceberg`, and `pd.to_view`.

#### Improvements

- Added modin telemetry on API calls and hybrid engine switches.
- Show more helpful error messages to Snowflake Notebook users when the `modin` or `pandas` version does not match our requirements.
- Added a data type guard to the cost functions for hybrid execution mode (Private Preview) that checks for data type compatibility.
- Added automatic switching to the pandas backend in hybrid execution mode (Private Preview) for many methods that are not directly implemented in pandas on Snowflake.
- Set the `type` and other standard fields for pandas on Snowflake telemetry.

#### Dependency updates

- Added `tqdm` and `ipywidgets` as dependencies so that progress bars appear when the user switches between modin backends.
- Updated the supported `modin` versions to >=0.33.0 and <0.35.0 (was previously >= 0.32.0 and <0.34.0).

#### Bug fixes

- Fixed a bug in Hybrid Execution mode (Private Preview) where certain series operations would raise `TypeError: numpy.ndarray object is not callable`.
- Fixed a bug in hybrid execution mode (Private Preview) where calling `numpy` operations like `np.where` on modin objects with the Pandas backend would raise an `AttributeError`. This fix requires `modin` version 0.34.0 or later.
- Fixed an issue in `df.melt` where the resulting values have an additional suffix applied.

## Version 1.33.0 (2025-06-19)

### New features

- Added support for MySQL in `DataFrameWriter.dbapi` (Private Preview) for both Parquet and UDTF-based ingestion.
- Added support for PostgreSQL in `DataFrameReader.dbapi` (Private Preview) for both Parquet and UDTF-based ingestion.
- Added support for Databricks in `DataFrameWriter.dbapi` (Private Preview) for UDTF-based ingestion, consolidating with other mentions of Databricks support.
- Added support to `DataFrameReader` to enable use of `PATTERN` when reading files with `INFER_SCHEMA` enabled.
- Added support for the following AI-powered functions in `functions.py`:

  - `ai_complete`
  - `ai_similarity`
  - `ai_summarize_agg` (originally `summarize_agg`)
  - different config options for `ai_classify`
- Added support for more options when reading XML files with a row tag using `rowTag` option:

  - Added support for removing namespace prefixes from column names using `ignoreNamespace` option.
  - Added support for specifying the prefix for the attribute column in the result table using `attributePrefix` option.
  - Added support for excluding attributes from the XML element using `excludeAttributes` option.
  - Added support for specifying the column name for the value when there are attributes in an element that has no child elements using `valueTag` option.
  - Added support for specifying the value to treat as a null value using `nullValue` option.
  - Added support for specifying the character encoding of the XML file using `charset` option.
  - Added support for ignoring surrounding whitespace in the XML element using `ignoreSurroundingWhitespace` option.
- Added support for parameter `return_dataframe` in `Session.call`, which can be used to set the return type of the functions to a `DataFrame` object.
- Added a new argument to `Dataframe.describe` called `strings_include_math_stats` that triggers `stddev` and `mean` to be calculated for String columns.
- Added support for retrieving `Edge.properties` when retrieving lineage from `DGQL` in `DataFrame.lineage.trace`.
- Added a parameter `table_exists` to `DataFrameWriter.save_as_table` that allows specifying if a table already exists. This allows skipping a table lookup that can be expensive.

### Bug fixes

- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) where the `create_connection` defined as local function was incompatible with multiprocessing.
- Fixed a bug in `DataFrameReader.dbapi` (Private Preview) where Databricks `TIMESTAMP` type was converted to Snowflake `TIMESTAMP_NTZ` type which should be `TIMESTAMP_LTZ` type.
- Fixed a bug in `DataFrameReader.json` where repeated reads with the same reader object would create incorrectly quoted columns.
- Fixed a bug in `DataFrame.to_pandas()` that would drop column names when converting a DataFrame that did not originate from a select statement.
- Fixed a bug where `DataFrame.create_or_replace_dynamic_table` raises an error when the DataFrame contains a UDTF and `SELECT *` in the UDTF is not parsed correctly.
- Fixed a bug where casted columns could not be used in the values clause of functions.

### Improvements

- Improved the error message for `Session.write_pandas()` and `Session.create_dataframe()` when the input pandas DataFrame does not have a column.
- Improved `DataFrame.select` when the arguments contain a table function with output columns that collide with columns of current DataFrame. With the improvement, if user provides non-colliding columns in `df.select("col1", "col2", table_func(...))` as string arguments, then the query generated by Snowpark client will not raise ambiguous column error.
- Improved `DataFrameReader.dbapi` (Private Preview) to use in-memory Parquet-based ingestion for better performance and security.
- Improved `DataFrameReader.dbapi` (Private Preview) to use `MATCH_BY_COLUMN_NAME=CASE_SENSITIVE` in copy into table operation.

### Snowpark Local testing Updates

#### New features

- Added support for snow URLs (`snow://`) in local file testing.

#### Bug fixes

- Fixed a bug in `Column.isin` that would cause incorrect filtering on joined or previously filtered data.
- Fixed a bug in `snowflake.snowpark.functions.concat_ws` that would cause results to have an incorrect index.

### Snowpark pandas API Updates

#### Dependency updates

- Updated `modin` dependency constraint from 0.32.0 to >=0.32.0, <0.34.0. The latest version tested with Snowpark pandas is `modin` 0.33.1.

#### New features

- Added support for **Hybrid Execution (Private Preview)**. By running `from modin.config import AutoSwitchBackend; AutoSwitchBackend.enable()`, pandas on Snowflake automatically chooses whether to run certain pandas operations locally or on Snowflake. This feature is disabled by default.

#### Improvements

- Set the default value of the `index` parameter to `False` for `DataFrame.to_view`, `Series.to_view`, `DataFrame.to_dynamic_table`, and `Series.to_dynamic_table`.
- Added `iceberg_version` option to table creation functions.
- Reduced query count for many operations, including `insert`, `repr`, and `groupby`, that previously issued a query to retrieve the input data’s size.

#### Bug fixes

- Fixed a bug in `Series.where` when the `other` parameter is an unnamed `Series`.

## Version 1.32.0 (2025-05-15)

### Improvements

- Invoking Snowflake system procedures does not invoke an additional `describe procedure` call to check the return type of the procedure.
- Added support for `Session.create_dataframe()` with the stage URL and `FILE` data type.
- Added support for different modes for dealing with corrupt XML records when reading an XML file using *session.read.option(‘mode’, <mode>), option(‘rowTag’, <tag\_name>).xml(<stage\_file\_path>)*. Currently `PERMISSIVE`, `DROPMALFORMED` and `FAILFAST` are supported.
- Improved the error message of the XML reader when the specified `ROWTAG` is not found in the file.
- Improved query generation for `Dataframe.drop` to use `SELECT * EXCLUDE ()` to exclude the dropped columns. To enable this feature, set `session.conf.set("use_simplified_query_generation", True)`.
- Added support for `VariantType` to `StructType.from_json`.

### Bug fixes

- Fixed a bug in `DataFrameWriter.dbapi` (Private preview) where unicode or double-quoted column names in external databases cause errors because they are not quoted correctly.
- Fixed a bug where named fields in nested `OBJECT` data could cause errors when containing spaces.

### Snowpark local testing updates

#### Bug fixes

- Fixed a bug in `snowflake.snowpark.functions.rank` that would not respect sort direction.
- Fixed a bug in `snowflake.snowpark.functions.to_timestamp_*` that would cause incorrect results on filtered data.

### Snowpark pandas API Updates

#### New features

- Added support for dict values in `Series.str.get`, `Series.str.slice`, and `Series.str.__getitem__` (*Series.str[…]*).
- Added support for `DataFrame.to_html`.
- Added support for `DataFrame.to_string` and `Series.to_string`.
- Added support for reading files from S3 buckets using `pd.read_csv`.

#### Improvements

- Make `iceberg_config` a required parameter for `DataFrame.to_iceberg` and `Series.to_iceberg`.

## Version 1.31.0 (2025-04-24)

### New features

- Added support for the `restricted caller` permission of `execute_as` argument in `StoredProcedure.register()`.
- Added support for non-select statements in `DataFrame.to_pandas()`.
- Added support for the `artifact_repository` parameter to `Session.add_packages`, `Session.add_requirements`, `Session.get_packages`, `Session.remove_package`, and `Session.clear_packages`.
- Added support for reading an XML file using a row tag by `session.read.option('rowTag', <tag_name>).xml(<stage_file_path>)` (experimental).

  - Each XML record is extracted as a separate row.
  - Each field within that record becomes a separate column of type `VARIANT`, which can be further queried using the dot notation, such as `col(a.b.c)`.
- Added updates to `DataFrameReader.dbapi` (PrPr):

  - Added the `fetch_merge_count` parameter for optimizing performance by merging multiple fetched data into a single Parquet file.
  - Added support for Databricks.
  - Added support for ingestion with Snowflake UDTF.
- Added support for the following AI-powered functions in `functions.py` (Private Preview):

  - `prompt`
  - `ai_filter` (added support for `prompt()` function and image files, and changed the second argument name from *expr* to *file*)
  - *ai\_classify*

#### Improvements

- Renamed the `relaxed_ordering` param into `enforce_ordering` for `DataFrame.to_snowpark_pandas`. Also the new default values is `enforce_ordering=False` which has the opposite effect of the previous default value, `relaxed_ordering=False`.
- Improved `DataFrameReader.dbapi` (PrPr) reading performance by setting the default `fetch_size` parameter value to 1000.
- Improve the error message for invalid identifier SQL error by suggesting the potentially matching identifiers.
- Reduced the number of describe queries issued when creating a DataFrame from a Snowflake table using `session.table`.
- Improved performance and accuracy of `DataFrameAnalyticsFunctions.time_series_agg()`.

#### Bug fixes

- Fixed a bug in `DataFrame.group_by().pivot().agg` when the pivot column and aggregate column are the same.
- Fixed a bug in `DataFrameReader.dbapi` (PrPr) where a `TypeError` was raised when `create_connection` returned a connection object of an unsupported driver type.
- Fixed a bug where `df.limit(0)` call would not properly apply.
- Fixed a bug in `DataFrameWriter.save_as_table` that caused reserved names to throw errors when using append mode.

#### Deprecations

- Deprecated support for Python3.8.
- Deprecated argument `sliding_interval` in `DataFrameAnalyticsFunctions.time_series_agg()`.

### Snowpark local testing updates

#### New features

- Added support for Interval expression to `Window.range_between`.
- Added support for `array_construct` function.

#### Bug fixes

- Fixed a bug in local testing where transient `__pycache__` directory was unintentionally copied during stored procedure execution via import.
- Fixed a bug in local testing that created incorrect result for `Column.like` calls.
- Fixed a bug in local testing that caused `Column.getItem` and `snowpark.snowflake.functions.get` to raise `IndexError` rather than return `null`.
- Fixed a bug in local testing where `df.limit(0)` call would not properly apply.
- Fixed a bug in local testing where a `Table.merge` into an empty table would cause an exception.

### Snowpark pandas API updates

#### Dependency updates

- Updated `modin` from 0.30.1 to 0.32.0.
- Added support for `numpy` 2.0 and above.

#### New features

- Added support for `DataFrame.create_or_replace_view` and `Series.create_or_replace_view`.
- Added support for `DataFrame.create_or_replace_dynamic_table` and `Series.create_or_replace_dynamic_table`.
- Added support for `DataFrame.to_view` and `Series.to_view`.
- Added support for `DataFrame.to_dynamic_table` and `Series.to_dynamic_table`.
- Added support for `DataFrame.groupby.resample` for aggregations `max`, `mean`, `median`, `min`, and `sum`.
- Added support for reading stage files using:

  - `pd.read_excel`
  - `pd.read_html`
  - `pd.read_pickle`
  - `pd.read_sas`
  - `pd.read_xml`
- Added support for `DataFrame.to_iceberg` and `Series.to_iceberg`.
- Added support for dict values in `Series.str.len`.

#### Improvements

- Improve the performance of `DataFrame.groupby.apply` and `Series.groupby.apply` by avoiding expensive pivot step.
- Added an estimate for the row count upper bound to `OrderedDataFrame` to enable better engine switching. This could potentially result in increased query counts.
- Renamed the `relaxed_ordering` parameter in `enforce_ordering` with `pd.read_snowflake`. Also the new default value is `enforce_ordering=False` which has the opposite effect of the previous default value, `relaxed_ordering=False`.

#### Bug fixes

- Fixed a bug for `pd.read_snowflake` when reading iceberg tables and `enforce_ordering=True`.

## Version 1.30.0 (2025-03-27)

### New features

- Added Support for relaxed consistency and ordering guarantees in `Dataframe.to_snowpark_pandas` by introducing the `relaxed_ordering` parameter.
- `DataFrameReader.dbapi` (preview) now accepts a list of strings for the `session_init_statement` parameter, allowing multiple SQL statements to be executed during session initialization.

### Improvements

- Improved query generation for `Dataframe.stat.sample_by` to generate a single flat query that scales well with large `fractions` dictionary compared to older method of creating a UNION ALL subquery for each key in `fractions`. To enable this feature, set `session.conf.set("use_simplified_query_generation", True)`.
- Improved the performance of `DataFrameReader.dbapi` by enabling the vectorized option when copying a parquet file into a table.
- Improved query generation for `DataFrame.random_split` in the following ways. They can be enabled by setting `session.conf.set("use_simplified_query_generation", True)`:

  - Removed the need to `cache_result` in the internal implementation of the input dataframe resulting in a pure lazy dataframe operation.
  - The `seed` argument now behaves as expected with repeatable results across multiple calls and sessions.
- `DataFrame.fillna` and `DataFrame.replace` now both support fitting `int` and `float` into `Decimal` columns if `include_decimal` is set to `True`.
- Added documentation for the following UDF and stored procedure functions in `files.py` as a result of their General Availability.

  - `SnowflakeFile.write`
  - `SnowflakeFile.writelines`
  - `SnowflakeFile.writeable`
- Minor documentation changes for `SnowflakeFile` and `SnowflakeFile.open()`.

### Bug fixes

- Fixed a bug for the following functions that raised errors. `.cast()` is applied to their output:
  - `from_json`
  - `size`

### Snowpark local testing updates

#### Bug fixes

- Fixed a bug in aggregation that caused empty groups to still produce rows.
- Fixed a bug in `Dataframe.except_` that would cause rows to be incorrectly dropped.
- Fixed a bug that caused `to_timestamp` to fail when casting filtered columns.

### Snowpark pandas API updates

#### New features

- Added support for list values in `Series.str.__getitem__` (`Series.str[...]`).
- Added support for `pd.Grouper` objects in GROUP BY operations. When `freq` is specified, the default values of the `sort`, `closed`, `label`, and `convention` arguments are supported; `origin` is supported when it is `start` or `start_day`.
- Added support for relaxed consistency and ordering guarantees in `pd.read_snowflake` for both named data sources (for example, tables and views) and query data sources by introducing the new parameter `relaxed_ordering`.

#### Improvements

- Raise a warning whenever `QUOTED_IDENTIFIERS_IGNORE_CASE` is found to be set, ask user to unset it.
- Improved how a missing `index_label` in `DataFrame.to_snowflake` and `Series.to_snowflake` is handled when `index=True`. Instead of raising a `ValueError`, system-defined labels are used for the index columns.
- Improved the error message for `groupby`, `DataFrame`, or `Series.agg` when the function name is not supported.

### Snowpark local testing updates

#### Improvements

- Raise a warning whenever `QUOTED_IDENTIFIERS_IGNORE_CASE` is found to be set, ask user to unset it.
- Improved how a missing `index_label` in `DataFrame.to_snowflake` and `Series.to_snowflake` is handled when `index=True`. Instead of raising a `ValueError`, system-defined labels are used for the index columns.
- Improved error message for `groupby or DataFrame or Series.agg` when the function name is not supported.

## Version 1.29.1 (2025-03-12)

### Bug fixes

- Fixed a bug in `DataFrameReader.dbapi` (private preview) that prevents usage in stored procedures and Snowbooks.

## Version 1.29.0 (2025-03-05)

### New features

- Added support for the following AI-powered functions in `functions.py` (Private Preview):
  - `ai_filter`
  - `ai_agg`
  - `summarize_agg`

> - Added support for the new FILE SQL type, with the following related functions in `functions.py` (Private Preview):
>
>   - `fl_get_content_type`
>   - `fl_get_etag`
>   - `fl_get_file_type`
>   - `fl_get_last_modified`
>   - `fl_get_relative_path`
>   - `fl_get_scoped_file_url`
>   - `fl_get_size`
>   - `fl_get_stage`
>   - `fl_get_stage_file_url`
>   - `fl_is_audio`
>   - `fl_is_compressed`
>   - `fl_is_document`
>   - `fl_is_image`
>   - `fl_is_video`
> - Added support for importing third-party packages from PyPi using Artifact Repository (Private Preview):
>
>   - Use keyword arguments `artifact_repository` and `packages` to specify your artifact repository and packages respectively when registering stored procedures or user defined functions.
>   - Supported APIs are:
>     - `Session.sproc.register`
>     - `Session.udf.register`
>     - `Session.udaf.register`
>     - `Session.udtf.register`
>     - `functions.sproc`
>     - `functions.udf`
>     - `functions.udaf`
>     - `functions.udtf`
>     - `functions.pandas_udf`
>     - `functions.pandas_udtf`

### Improvements

> - Improved version validation warnings for `snowflake-snowpark-python` package compatibility when registering stored procedures. Now, warnings are only triggered if the major or minor version does not match, while bugfix version differences no longer generate warnings.
> - Bumped cloudpickle dependency to also support `cloudpickle==3.0.0` in addition to previous versions.

### Bug fixes

> - Fixed a bug where creating a Dataframe with large number of values raised `Unsupported feature 'SCOPED_TEMPORARY'.` error if thread-safe session was disabled.
> - Fixed a bug where `df.describe` raised internal SQL execution error when the DataFrame is created from reading a stage file and CTE optimization is enabled.
> - Fixed a bug where `df.order_by(A).select(B).distinct()` would generate invalid SQL when simplified query generation was enabled using `session.conf.set("use_simplified_query_generation", True)`.
>   - Disabled simplified query generation by default.

### Snowpark pandas API updates

#### Improvements

> - Improve error message for `pd.to_snowflake`, `DataFrame.to_snowflake`, and `Series.to_snowflake` when the table does not exist.
> - Improve readability of docstring for the `if_exists` parameter in `pd.to_snowflake`, `DataFrame.to_snowflake`, and `Series.to_snowflake`.
> - Improve error message for all pandas functions that use UDFs with Snowpark objects.

#### Bug fixes

> - Fixed a bug in `Series.rename_axis` where an `AttributeError` was being raised.
> - Fixed a bug where `pd.get_dummies` didn’t ignore NULL/NaN values by default.
> - Fixed a bug where repeated calls to `pd.get_dummies` results in ‘Duplicated column name error’.
> - Fixed a bug in `pd.get_dummies` where passing list of columns generated incorrect column labels in output DataFrame.
> - Update `pd.get_dummies` to return bool values instead of int.

### Snowpark local testing updates

#### New features

- Added support for literal values to `range_between` window function.

## Version 1.28.0 (2025-02-20)

### New features

- Added support for the following functions in `functions.py`

  - `normal`
  - `randn`
- Added support for `allow_missing_columns` parameter to `Dataframe.union_by_name` and `Dataframe.union_all_by_name`.

### Improvements

- Improved random object name generation to avoid collisions.
- Improved query generation for `Dataframe.distinct` to generate SELECT DISTINCT instead of SELECT with GROUP BY all columns. To disable this feature, set `session.conf.set("use_simplified_query_generation", False)`.

### Deprecations

- Deprecated Snowpark Python function `snowflake_cortex_summarize`. Users can install `snowflake-ml-python` and use the `snowflake.cortex.summarize` function instead.
- Deprecated Snowpark Python function `snowflake_cortex_sentiment`. Users can install `snowflake-ml-python` and use the `snowflake.cortex.sentiment` function instead.

### Bug fixes

- Fixed a bug where session-level query tag was overwritten by a stack trace for DataFrames that generate multiple queries. Now, the query tag will only be set to the stacktrace if `session.conf.set("collect_stacktrace_in_query_tag", True)`.
- Fixed a bug in `Session._write_pandas` where it was erroneously passing `use_logical_type` parameter to `Session._write_modin_pandas_helper` when writing a Snowpark pandas object.
- Fixed a bug in options SQL generation that could cause multiple values to be formatted incorrectly.
- Fixed a bug in `Session.catalog` where empty strings for database or schema were not handled correctly and were generating erroneous SQL statements.

### Experimental Features

- Added support for writing pyarrow Tables to Snowflake tables.

### Snowpark pandas API updates

#### New features

- Added support for applying Snowflake Cortex functions `Summarize` and `Sentiment`.
- Added support for list values in `Series.str.get`.

### Bug fixes

- Fixed a bug in `apply` where kwargs were not being correctly passed into the applied function.

### Snowpark local testing updates

#### New features

- Added support for the following functions
  :   - `hour`
      - `minute`
- Added support for NULL\_IF parameter to CSV reader.
- Added support for `date_format`, `datetime_format`, and `timestamp_format` options when loading CSVs.

### Bug fixes

- Fixed a bug in `DataFrame.join` that caused columns to have incorrect typing.
- Fixed a bug in `when` statements that caused incorrect results in the `otherwise` clause.

## Version 1.27.0 (2025-02-05)

### New features

Added support for the following functions in `functions.py`:

- `array_reverse`
- `divnull`
- `map_cat`
- `map_contains_key`
- `map_keys`
- `nullifzero`
- `snowflake_cortex_sentiment`
- `acosh`
- `asinh`
- `atanh`
- `bit_length`
- `bitmap_bit_position`
- `bitmap_bucket_number`
- `bitmap_construct_agg`
- `cbrt`
- `equal_null`
- `from_json`
- `ifnull`
- `localtimestamp`
- `max_by`
- `min_by`
- `nth_value`
- `nvl`
- `octet_length`
- `position`
- `regr_avgx`
- `regr_avgy`
- `regr_count`
- `regr_intercept`
- `regr_r2`
- `regr_slope`
- `regr_sxx`
- `regr_sxy`
- `regr_syy`
- `try_to_binary`
- `base64`
- `base64_decode_string`
- `base64_encode`
- `editdistance`
- `hex`
- `hex_encode`
- `instr`
- `log1p`
- `log2`
- `log10`
- `percentile_approx`
- `unbase64`
- Added support for specifying a schema string (including implicit struct syntax) when calling `DataFrame.create_dataframe`.
- Added support for `DataFrameWriter.insert_into/insertInto`. This method also supports local testing mode.
- Added support for `DataFrame.create_temp_view` to create a temporary view. It will fail if the view already exists.
- Added support for multiple columns in the functions `map_cat` and `map_concat`.
- Added an option `keep_column_order` for keeping original column order in `DataFrame.with_column` and `DataFrame.with_columns`.
- Added options to column casts that allow renaming or adding fields in `StructType` columns.
- Added support for `contains_null parameter` to `ArrayType`.
- Added support for creating a temporary view via `DataFrame.create_or_replace_temp_view` from a DataFrame created by reading a file from a stage.
- Added support for `value_contains_null` parameter to `MapType`.
- Added interactive to telemetry that indicates whether the current environment is an interactive one.
- Allow `session.file.get` in a Native App to read file paths starting with / from the current version
- Added support for multiple aggregation functions after `DataFrame.pivot`.

### Experimental features

- Added `Session.catalog` class to manage Snowflake objects. It can be accessed via `Session.catalog`.

  - `snowflake.core` is a dependency required for this feature.
- Allow user input schema or user input schemas when reading JSON file on stage.
- Added support for specifying a schema string (including implicit struct syntax) when calling `DataFrame.create_dataframe`.

### Improvements

- Updated `README.md` to include instructions on how to verify package signatures using `cosign`.

### Bug fixes

- Fixed a bug in local testing mode that caused a column to contain None when it should contain 0.
- Fixed a bug in `StructField.from_json` that prevented `TimestampTypes` with `tzinfo` from being parsed correctly.
- Fixed a bug in `function date_format` that caused an error when the input column was date type or timestamp type.
- Fixed a bug in DataFrame that allowed null values to be inserted in a non-nullable column.
- Fixed a bug in functions `replace` and `lit` which raised type hint assertion error when passing Column expression objects.
- Fixed a bug in `pandas_udf` and `pandas_udtf` where session parameters were erroneously ignored.
- Fixed a bug that raised an incorrect type conversion error for system function called through `session.call`.

### Snowpark pandas API updates

#### New features

- Added support for `Series.str.ljust` and `Series.str.rjust`.
- Added support for `Series.str.center`.
- Added support for `Series.str.pad`.
- Added support for applying the Snowpark Python function `snowflake_cortex_sentiment`.
- Added support for `DataFrame.map`.
- Added support for `DataFrame.from_dict` and `DataFrame.from_records`.
- Added support for mixed case field names in struct type columns.
- Added support for `SeriesGroupBy.unique`
- Added support for `Series.dt.strftime` with the following directives:

  - %d: Day of the month as a zero-padded decimal number.
  - %m: Month as a zero-padded decimal number.
  - %Y: Year with century as a decimal number.
  - %H: Hour (24-hour clock) as a zero-padded decimal number.
  - %M: Minute as a zero-padded decimal number.
  - %S: Second as a zero-padded decimal number.
  - %f: Microsecond as a decimal number, zero-padded to 6 digits.
  - %j: Day of the year as a zero-padded decimal number.
  - %X: Locale’s appropriate time representation.
  - %%: A literal ‘%’ character.
- Added support for `Series.between`.
- Added support for `include_groups=False` in `DataFrameGroupBy.apply`.
- Added support for `expand=True` in `Series.str.split`.
- Added support for `DataFrame.pop` and `Series.pop`.
- Added support for `first` and `last` in `DataFrameGroupBy.agg` and `SeriesGroupBy.agg`.
- Added support for `Index.drop_duplicates`.
- Added support for aggregations `"count"`, `"median"`, `np.median`,
  `"skew"`, `"std"`, `np.std` `"var"`, and `np.var` in
  `pd.pivot_table()`, `DataFrame.pivot_table()`, and `pd.crosstab()`.

#### Improvements

- Improved performance of `DataFrame.map`, `Series.apply` and `Series.map` methods by mapping numpy functions to Snowpark functions if possible.
- Added documentation for `DataFrame.map`.
- Improved performance of `DataFrame.apply` by mapping numpy functions to Snowpark functions if possible.
- Added documentation on the extent of Snowpark pandas interoperability with scikit-learn.
- Infer return type of functions in `Series.map`, `Series.apply` and `DataFrame.map` if type-hint is not provided.
- Added `call_count` to telemetry that counts method calls including interchange protocol calls.
