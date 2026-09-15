# Snowpark Connect for Spark properties

Snowpark Connect for Spark supports custom configuration in a way that’s similar to standard Spark. You can modify configuration properties only
through the session’s `set` method by using a key-value pair. Note that Snowpark Connect for Spark recognizes only a limited set of properties that
influence execution. Any unsupported properties are silently ignored without raising an exception.

## Supported Spark properties

Snowpark Connect for Spark supports a subset of Spark properties.

| Property Name | Default | Meaning | Since |
| --- | --- | --- | --- |
| `spark.app.name` | (none) | Application name set as Snowflake `query_tag` (`Spark-Connect-App-Name={name}`) for query tracking. | 1.0.0 |
| `spark.Catalog.databaseFilterInformationSchema` | `false` | When `true`, filters out `INFORMATION_SCHEMA` from database listings in catalog operations. | 1.0.0 |
| `spark.hadoop.fs.s3a.access.key` | (none) | AWS access key ID for S3 authentication when reading or writing to S3 locations. | 1.0.0 |
| `spark.hadoop.fs.s3a.assumed.role.arn` | (none) | AWS IAM role ARN with S3 access when using role-based authentication. | 1.0.0 |
| `spark.hadoop.fs.s3a.secret.key` | (none) | AWS secret access key for S3 authentication when reading or writing to S3 locations. | 1.0.0 |
| `spark.hadoop.fs.s3a.server-side-encryption.key` | (none) | AWS KMS key ID for server-side encryption when using the `AWS_SSE_KMS` encryption type. | 1.0.0 |
| `spark.hadoop.fs.s3a.session.token` | (none) | AWS session token for temporary S3 credentials when using STS. | 1.0.0 |
| `spark.sql.ansi.enabled` | `false` | Enables ANSI SQL mode for stricter type checking and error handling. When `true`, arithmetic overflows and invalid casts raise errors instead of returning `NULL`. | 1.0.0 |
| `spark.sql.caseSensitive` | `false` | Controls case sensitivity for identifiers. When `false`, column and table names are case-insensitive (auto-uppercased in Snowflake). | 1.0.0 |
| `spark.sql.crossJoin.enabled` | `true` | Enables or disables implicit cross joins. When `false`, a missing or trivial join condition results in an error. | 1.0.0 |
| `spark.sql.execution.pythonUDTF.arrow.enabled` | `false` | When `true`, enables Apache Arrow optimization for Python UDTF serialization/deserialization. | 1.0.0 |
| `spark.sql.globalTempDatabase` | `global_temp` | Schema name for global temporary views; created automatically if it does not exist. | 1.0.0 |
| `spark.sql.legacy.allowHashOnMapType` | `false` | When `true`, allows hashing MAP type columns. By default, MAP types cannot be hashed for consistency with Spark behavior. | 1.0.0 |
| `spark.sql.legacy.dataset.nameNonStructGroupingKeyAsValue` | `false` | Legacy behavior for dataset grouping key naming. | 1.6.0 |
| `spark.sql.mapKeyDedupPolicy` | `EXCEPTION` | Controls behavior when duplicate keys are found in map creation. Values: `EXCEPTION` (raise error) or `LAST_WIN` (keep last value). | 1.0.0 |
| `spark.sql.parser.quotedRegexColumnNames` | `false` | When `true`, enables regex pattern matching in quoted column names in SQL queries (for example `SELECT '(col1|col2)' FROM table`). | 1.0.0 |
| `spark.sql.parquet.inferTimestampNTZ.enabled` | `true` | When `true`, infers `TimestampNTZType` from Parquet files instead of mapping all timestamps to `TimestampType`. | 1.15.0 |
| `spark.sql.parquet.outputTimestampType` | `TIMESTAMP_MILLIS` | Controls Parquet output timestamp type. Supports `TIMESTAMP_MILLIS` or `TIMESTAMP_MICROS`. | 1.7.0 |
| `spark.sql.pyspark.inferNestedDictAsStruct.enabled` | `false` | When `true`, infers nested Python dictionaries as `StructType` instead of `MapType` during DataFrame creation. | 1.0.0 |
| `spark.sql.pyspark.legacy.inferArrayTypeFromFirstElement.enabled` | `false` | When `true`, infers array element type from first element only instead of sampling all elements. | 1.0.0 |
| `spark.sql.repl.eagerEval.enabled` | `false` | When `true`, enables eager evaluation in REPL showing DataFrame results automatically without calling `show()`. | 1.0.0 |
| `spark.sql.repl.eagerEval.maxNumRows` | `20` | Maximum number of rows to display in REPL eager evaluation mode. | 1.0.0 |
| `spark.sql.repl.eagerEval.truncate` | `20` | Maximum width for column values in REPL eager evaluation display before truncation. | 1.0.0 |
| `spark.sql.session.localRelationCacheThreshold` | `2147483647` | Byte threshold for caching local relations. Relations larger than this are cached to improve performance. | 1.0.0 |
| `spark.sql.session.timeZone` | *<system\_local\_timezone>* | Session timezone used for timestamp operations. Synced with Snowflake session via `ALTER SESSION SET TIMEZONE`. | 1.0.0 |
| `spark.sql.sources.default` | `parquet` | Default data source format for read/write operations when format is not explicitly specified. | 1.0.0 |
| `spark.sql.storeAssignmentPolicy` | `LEGACY` | Sets how strictly types are checked when inserting data into a table. `LEGACY` allows most casts. `ANSI` blocks risky casts and fails on overflow. `STRICT` also blocks casts that lose precision. | 1.27.0 |
| `spark.sql.timestampType` | `TIMESTAMP_LTZ` | Default timestamp type for timestamp operations. Values: `TIMESTAMP_LTZ` (with local timezone) or `TIMESTAMP_NTZ` (no timezone). | 1.0.0 |
| `spark.sql.tvf.allowMultipleTableArguments.enabled` | `true` | When `true`, allows table-valued functions to accept multiple table arguments. | 1.0.0 |

Expand

Show lessSee more

## Supported Snowpark Connect for Spark properties

Custom configuration properties specific to Snowpark Connect for Spark.

| Property Name | Default | Meaning | Since |
| --- | --- | --- | --- |
| `fs.azure.sas.<container>.<account>.blob.core.windows.net` | (none) | Azure SAS token for Blob Storage authentication. Used when reading or writing to Azure Blob Storage locations. | 1.0.0 |
| `fs.azure.sas.fixed.token.<account>.dfs.core.windows.net` | (none) | Azure SAS token for ADLS Gen2 (Data Lake Storage) authentication. Used when reading or writing to Azure Data Lake Storage Gen2 locations. | 1.0.0 |
| `mapreduce.fileoutputcommitter.marksuccessfuljobs` | `false` | When `true`, generates `_SUCCESS` file after successful write operations for compatibility with Hadoop/Spark workflows. | 1.0.0 |
| `parquet.enable.summary-metadata` | `false` | Alternative config for generating Parquet summary metadata files. Either this or `spark.sql.parquet.enable.summary-metadata` enables the feature. | 1.4.0 |
| `snowflake.repartition.for.writes` | `false` | When `true`, forces `DataFrame.repartition(n)` to split output into `n` files during writes. Matches Spark behavior but adds overhead. | 1.0.0 |
| `snowpark.connect.csv.continueOnError` | `false` | When `true`, continues processing when errors are encountered while reading CSV files instead of failing immediately. Malformed rows are skipped and remaining valid rows are returned. | 1.16.0 |
| `snowpark.connect.cte.optimization_enabled` | `false` | When `true`, enables Common Table Expression (CTE) optimization in Snowpark sessions for improved query performance. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-cte-optimization-enabled) | 1.0.0 |
| `snowpark.connect.describe_cache_ttl_seconds` | `300` | Time-to-live in seconds for query cache entries. Reduces repeated schema lookups. | 1.0.0 |
| `snowpark.connect.enable_snowflake_extension_behavior` | `false` | When `true`, enables Snowflake-specific extensions that can differ from Spark behavior (such as hash on MAP types or MD5 return type). [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-enable-snowflake-extension-behavior) | 1.0.0 |
| `snowpark.connect.handleIntegralOverflow` | `false` | When `true`, integral overflow behavior is aligned with the Spark approach. | 1.7.0 |
| `snowpark.connect.iceberg.external_volume` | (none) | Snowflake external volume name for Iceberg table operations. | 1.0.0 |
| `snowpark.connect.integralTypesEmulation` | `client_default` | Controls conversion of decimal to integral types. Values: `client_default`, `enabled`, `disabled` [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-integral-types-emulation) | 1.7.0 |
| `snowpark.connect.parquet.useLogicalType` | `false` | When `true`, enables proper handling of Parquet logical types such as TIMESTAMP, DATE, and DECIMAL. Instead of reading these columns as their physical types (for example, INT64 or FIXED\_LEN\_BYTE\_ARRAY), Snowpark Connect for Spark maps them to the corresponding Spark logical types. | 1.6.0 |
| `snowpark.connect.scala.version` | `2.12` | Controls the Scala version used (supports `2.12` or `2.13`) | 1.7.0 |
| `snowpark.connect.sql.partition.external_table_location` | (none) | External table location path for partitioned writes. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-sql-partition-external-table-location) | 1.4.0 |
| `snowpark.connect.temporary.views.create_in_snowflake` | `false` | When `true`, creates temporary views directly in Snowflake instead of managing them locally. | 1.0.1 |
| `snowpark.connect.udf.imports [DEPRECATED 1.7.0]` | (none) | Comma-separated list of files or modules to import for UDF execution. Triggers UDF recreation when changed. | 1.0.0 |
| `snowpark.connect.udf.python.imports` | (none) | Comma-separated list of files/modules to import for Python UDF execution. Triggers UDF recreation when changed. | 1.7.0 |
| `snowpark.connect.udf.java.imports` | (none) | Comma-separated list of files or modules to import for Java UDF execution. Triggers UDF recreation when changed. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-udf-java-imports) | 1.7.0 |
| `snowpark.connect.udf.packages` | (none) | Comma-separated list of Python packages to include when registering UDFs. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-udf-packages) | 1.0.0 |
| `snowpark.connect.udtf.compatibility_mode` | `false` | When `true`, enables Spark-compatible UDTF behavior for improved compatibility with Spark UDTF semantics. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-udtf-compatibility-mode) | 1.0.0 |
| `snowpark.connect.version` | `<current_version>` | Read-only. Returns the current Snowpark Connect for Spark version. | 1.0.0 |
| `snowpark.connect.views.duplicate_column_names_handling_mode` | `rename` | How to handle duplicate column names in views. Values: `rename` (add suffix) `fail` (raise error) or `drop` (remove duplicates). [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-views-duplicate-column-names-handling-mode) | 1.0.0 |
| `spark.sql.parquet.enable.summary-metadata` | `false` | When `true`, generates Parquet summary metadata files (`_metadata`, `_common_metadata`) during Parquet writes. | 1.4.0 |
| `snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables` | `false` | When `true`, allows partition overwrites on Snowflake tables in Spark SQL (`INSERT OVERWRITE <table> PARTITION(<partition spec>)`). [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-sql-emulate-partition-overwrites) | 1.12.3 |
| `snowpark.connect.sql.returnDmlMetadata` | `false` | When `true`, DML operations (INSERT, UPDATE, DELETE, MERGE) return a DataFrame with row count metadata instead of an empty result. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-sql-return-dml-metadata) | 1.20.0 |
| `snowpark.connect.artifact_repository` | (none) | Specifies the name of a Snowflake artifact repository for UDF/UDTF package resolution. When set, packages are resolved from the specified repository instead of Anaconda. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-artifact-repository) | 1.14.0 |
| `snowpark.connect.udf.resource_constraint.architecture` | (none) | When set to `x86`, UDFs, UDTFs, and `applyInPandas` operations are created with an x86 architecture constraint. Requires a warehouse with an x86 resource constraint. [More](/developer-guide/snowpark-connect/snowpark-connect-parameters#label-spconnect-udf-resource-constraint-architecture) | 1.13.0 |

Expand

Show lessSee more

### `snowpark.connect.cte.optimization_enabled`

Specify `true` to enable Common Table Expression (CTE) optimization in the Snowpark session for query performance.

Default: `false`

Since: 1.0.0

#### Comments

Configuration that enables [Snowflake Common Table Expressions (CTEs)](/user-guide/queries-cte). This configuration optimizes the
Snowflake queries in which there are a lot of repetitive code blocks. This modification will lead to improvements in both query compilation and
execution performance.

### `snowpark.connect.enable_snowflake_extension_behavior`

Specify `true` to enable Snowflake-specific extensions that can differ from Spark behavior (such as a hash on MAP types or MD5 return type).

Default: `false`

Since: 1.0.0

#### Comments

When set to `true`, changes the behavior of certain operations:

> - `bit_get/getbit` — Explicit use of [Snowflake getbit function](/sql-reference/functions/getbit)
> - `hash` — Explicit use of [Snowflake hash function](/sql-reference/functions/hash)
> - `md5` — Explicit use of [Snowflake md5 function](/sql-reference/functions/md5)
> - Renaming table columns — Allows for altering table columns

### `snowpark.connect.integralTypesEmulation`

Specifies how to convert decimal to integral types. Values: `client_default`, `enabled`, `disabled`

Default: `client_default`

Since: 1.7.0

#### Comments

By default, Snowpark Connect for Spark treats all integral types as `Long` types. This is caused by the way [numbers are represented in Snowflake](/sql-reference/data-types-numeric#label-data-type-number). Integral types emulation allows for an exact mapping between Snowpark and Spark types when reading from datasources.

The default option `client_default` activates the emulation only when the script is executed from the Scala client. Integral types are mapped based on the following precisions:

| Precision | Spark Type |
| --- | --- |
| 19 | `LongType` |
| 10 | `IntegerType` |
| 5 | `ShortType` |
| 3 | `ByteType` |
| Other | `DecimalType(precision, 0)` |

Expand

Show lessSee more

When other precisions are found, the final type is mapped to the *DecimalType*.

### `snowpark.connect.sql.partition.external_table_location`

Specifies the external table location path for partitioned writes.

Default: (none)

Since: 1.4.0

#### Comments

To read only an exact subset of partitioned files from the provided directory, additional configuration is required. This feature is only available for files stored on [external stages](/sql-reference/sql/create-stage). To prune the read files, Snowpark Connect for Spark uses [external tables](/sql-reference/sql/create-external-table).

This feature is enabled when the configuration `snowpark.connect.sql.partition.external_table_location` is set. It should contain existing database and schema names where external tables will be created.

Reading parquet files that are stored on external stages will create an external table; for files on internal stages, it will not be created. Providing the schema will reduce the execution time, eliminating the cost of inferring it from sources.

For best performance, filter according to the [Snowflake External Tables filtering limitations](/user-guide/tables-external-intro#label-tables-external-intro-filtering-records-in-parquet-files).

##### Example

Copy code

```
spark.conf.set("snowpark.connect.sql.partition.external_table_location", "<database-name>.<schema-name>")

spark.read.parquet("@external-stage/example").filter(col("x") > lit(1)).show()

schema = StructType([StructField("x",IntegerType()),StructField("y",DoubleType())])

spark.read.schema(schema).parquet("@external-stage/example").filter(col("x") > lit(1)).show()
```

### `snowpark.connect.udf.java.imports`

Specifies a comma-separated list of files and modules to import for Java UDF execution. Triggers UDF recreation when changed.

Default: (none)

Since: 1.7.0

#### Comments

This configuration works very similarly to the `snowpark.connect.udf.python.imports`. With it, you can specify external libraries and files for Java UDFs created using [registerJavaFunction](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.UDFRegistration.registerJavaFunction.html). Configurations are mutually exclusive to prevent unnecessary dependency mixing.

To include external libraries and files, you provide stage paths to the files as the value of the configuration setting `snowpark.connect.udf.java.imports`. The configuration value should be an array of stage paths to the files, where the paths are separated by commas.

##### Example

Code in the following example includes two files in the UDF’s execution context. The UDF imports functions from these files and uses them in its logic.

Copy code

```
# Files need to be previously staged

spark.conf.set("snowpark.connect.udf.java.imports", "[@stage/library.jar]")

spark.registerJavaFunction("javaFunction", "com.example.ExampleFunction")

spark.sql("SELECT javaFunction('arg')").show()
```

You can use the `snowpark.connect.udf.java.imports` setting to include other kinds of files as well, such as those with data your code needs to read. Note that when you do this, your code should only read from the included files; any writes to such files will be lost after the function’s execution ends.

### `snowpark.connect.udf.packages`

Specifies a comma-separated list of Python packages to include when registering UDFs.

Default: (none)

Since: 1.0.0

#### Comments

You can use this to define additional packages to be available in Python UDFs. The value is a comma-separated list of dependencies.

You can discover the list of supported packages by executing the following SQL in Snowflake:

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'python';
```

##### Example

Copy code

```
spark.conf.set("snowpark.connect.udf.packages", "[numpy]")

@udtf(returnType="val: int")

class Powers:

  def eval(self, x: int):
      import numpy as np

      for v in np.power(np.array([x, x, x]), [0, 1, 2]):
          yield (int(v),)

spark.udtf.register(name="powers", f=Powers)

spark.sql("SELECT * FROM powers(10)").show()
```

For more information, see [Python](/sql-reference/sql/create-function#label-create-function-python-packages).

### `snowpark.connect.udtf.compatibility_mode`

Specify `true` to enable Spark-compatible UDTF behavior for improved compatibility with Spark UDTF semantics.

Default: `false`

Since: 1.0.0

#### Comments

This property determines whether UDTFs should use Spark-compatible behavior or the default Snowpark behavior. When set to `true`, it applies a compatibility wrapper that mimics Spark’s output type coercion and error handling patterns.

When enabled, UDTFs use a compatibility wrapper that applies Spark-style automatic type coercion (for example, string “true” to boolean, boolean to integer) and error handling. The wrapper also converts table arguments to Row-like objects for both positional and named access, and properly handles SQL null values to match Spark’s behavior patterns.

### `snowpark.connect.views.duplicate_column_names_handling_mode`

Specifies how to handle duplicate column names in views. Allowed values include `rename` (add suffix), `fail` (raise error), or `drop` (remove duplicates).

Default: `rename`

Since: 1.0.0

#### Comments

Snowflake does not support duplicate column names.

##### Example

The following code fails at the view creation step with the following SQL compilation error: “duplicate column name ‘foo’”.

Copy code

```
df = spark.createDataFrame([
(1, 1),
(2, 2)
], ["foo", "foo"])

df.show() # works

df.createTempView("df_view") # Fails with SQL compilation error: duplicate column name 'foo'
```

To work around this, set the `snowpark.connect.views.duplicate_column_names_handling_mode` configuration option to one of the following values:

- `rename`: A suffix such as `_dedup_1`, `_dedup_2`, and so on will be appended to all of the duplicate column names after the first one.
- `drop`: All of the duplicate columns except one will be dropped. If the columns have different values, this might lead to incorrect results.

### `snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables`

When `true`, allows partition overwrites on Snowflake tables in Spark SQL (`INSERT OVERWRITE <table> PARTITION(<partition spec>)`).

Default: `false`

Since: 1.12.3

#### Comments

Snowflake tables do not support user-defined partitioning, and by default, partition overwrites will result in an error. Enabling this option allows using `INSERT OVERWRITE <table> PARTITION(<partition spec>)` syntax to perform overwrites.

The `<partition spec>` will accept any columns that exist in the target table.

##### Example

Code in the following example overwrites all rows in the students table that have a student\_id of 222222.

Copy code

```
spark.conf.set("snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables", True)

# create the students and persons tables as standard Snowflake tables
students_data = [
  ("Ashua Hill", "456 Erica Ct, Cupertino", 111111),
  ("Brian Reed", "723 Kern Ave, Palo Alto", 222222)
]

students_df = spark.createDataFrame(students_data, ["name", "address", "student_id"])
students_df.write.mode("overwrite").saveAsTable("students")

persons_data = [
    ("Dora Williams", "134 Forest Ave, Menlo Park", 123456789),
    ("Eddie Davis", "245 Market St, Milpitas", 345678901)
]

persons_df = spark.createDataFrame(persons_data, ["name", "address", "ssn"])
persons_df.write.mode("overwrite").saveAsTable("persons")

# overwrites all rows in the students table that have a student_id of 222222
spark.sql("""
    INSERT OVERWRITE students PARTITION (student_id = 222222)
    SELECT name, address FROM persons WHERE name = 'Dora Williams'
""").collect()
```

### `snowpark.connect.sql.returnDmlMetadata`

When `true`, DML statements executed through `spark.sql()` return a single-row DataFrame
containing row count metadata instead of an empty result. This applies to INSERT, UPDATE, DELETE,
and MERGE operations.

Default: `false`

Since: 1.20.0

#### Comments

By default, DML statements return an empty DataFrame with no columns. Enabling this property causes
each DML operation to return a DataFrame with metadata columns that describe how many rows were
affected:

| DML operation | Returned columns |
| --- | --- |
| INSERT / INSERT OVERWRITE | `num_affected_rows`, `num_inserted_rows` |
| UPDATE | `num_affected_rows` |
| DELETE | `num_affected_rows` |
| MERGE | `num_affected_rows`, `num_updated_rows`, `num_deleted_rows`, `num_inserted_rows` |

Expand

Show lessSee more

Note

DML row count metadata is a Snowpark Connect for Spark extension. Apache Spark does not natively return row counts
from DML operations. Code that relies on this feature isn’t portable to open-source Spark.

This property does not affect DML statements executed through
[Snowflake SQL pass-through](/developer-guide/snowpark-connect/snowpark-connect-executing-sql).
When SQL pass-through is enabled, Snowflake returns its own result format regardless of this setting.

##### Example

Copy code

```
spark.conf.set("snowpark.connect.sql.returnDmlMetadata", "true")

# INSERT returns num_affected_rows and num_inserted_rows
result = spark.sql("INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob')")
result.show()
# +-----------------+-----------------+
# %num_affected_rows%num_inserted_rows|
# +-----------------+-----------------+
# |                2|                2|
# +-----------------+-----------------+

# UPDATE returns num_affected_rows
result = spark.sql("UPDATE my_table SET name = 'Robert' WHERE id = 2")
result.show()
# +-----------------+
# %num_affected_rows%
# +-----------------+
# |                1|
# +-----------------+

# DELETE returns num_affected_rows
result = spark.sql("DELETE FROM my_table WHERE id = 1")
result.show()
# +-----------------+
# %num_affected_rows%
# +-----------------+
# |                1|
# +-----------------+

# MERGE returns all metadata columns
result = spark.sql("""
    MERGE INTO target t
    USING source s ON t.id = s.id
    WHEN MATCHED THEN UPDATE SET t.name = s.name
    WHEN NOT MATCHED THEN INSERT (id, name) VALUES (s.id, s.name)
""")
result.show()
# +-----------------+----------------+----------------+-----------------+
# %num_affected_rows%num_updated_rows%num_deleted_rows%num_inserted_rows|
# +-----------------+----------------+----------------+-----------------+
# |                3|               2|               0|                1|
# +-----------------+----------------+----------------+-----------------+
```

### `snowpark.connect.artifact_repository`

Specifies the name of a Snowflake [artifact repository](/developer-guide/udf/python/udf-python-packages) to use for package resolution when registering UDFs, UDTFs, `applyInPandas`, `mapInArrow`, and `cogroup` operations. When set, packages specified via `snowpark.connect.udf.packages` are resolved from the specified artifact repository instead of Anaconda.

Default: (none)

Since: 1.14.0

#### Comments

By default, Snowpark Connect for Spark resolves Python packages from Snowflake’s curated Anaconda channel. Setting this configuration to an artifact repository name allows resolving packages from PyPI or other configured sources, enabling the use of packages that are not available in the Anaconda channel.

For information on how to create and configure an artifact repository in Snowflake, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

Changing this configuration invalidates cached UDFs and UDTFs, causing them to be recreated with the new repository on next invocation.

This configuration applies to the following operations:

- UDFs registered via `@udf` decorator or `spark.udf.register()`
- UDTFs registered via `@udtf` decorator or `spark.udtf.register()`
- `applyInPandas` via `groupBy().applyInPandas()`
- `mapInArrow` via `DataFrame.mapInArrow()`
- `cogroup` via `groupBy().cogroup().applyInPandas()`

##### Example

The following example configures the artifact repository, then defines a UDF that uses `pykalman`, a package available from the artifact repository, to apply Kalman filter smoothing.

Copy code

```
spark.conf.set("snowpark.connect.artifact_repository", "my_pypi_repo")
spark.conf.set("snowpark.connect.udf.packages", "[pykalman]")

@udf(returnType=DoubleType())
def kalman_smooth_value(value: float) -> float:
    import numpy as np
    from pykalman import KalmanFilter

    kf = KalmanFilter(
        transition_matrices=[1],
        observation_matrices=[1],
        initial_state_mean=0,
        initial_state_covariance=1,
        observation_covariance=1,
        transition_covariance=0.1,
    )
    observations = np.array([value, value, value])
    smoothed_state_means, _ = kf.smooth(observations)
    return float(smoothed_state_means[-1][0])

df = spark.createDataFrame([(1, 10.0), (2, 20.0), (3, 30.0)], ["id", "value"])
df.select("id", kalman_smooth_value("value").alias("smoothed")).show()
```

For more information on artifact repositories and available packages, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

### `snowpark.connect.udf.resource_constraint.architecture`

When set to `x86`, UDFs, UDTFs, and `applyInPandas` operations are created with an x86 architecture constraint. This requires a warehouse configured with an x86 resource constraint for execution.

Default: (none)

Since: 1.13.0

#### Comments

Some third-party Python packages (such as TensorFlow, XGBoost, and certain scientific libraries) are built only for the x86 CPU architecture. Setting this configuration to `x86` adds `RESOURCE_CONSTRAINT=(architecture='x86')` to the `CREATE FUNCTION` statement generated by Snowpark Connect for Spark, ensuring the UDF runs on x86-compatible infrastructure.

To use this configuration, you must execute your workload on a warehouse that has been created with an x86 resource constraint. The following resource constraint values support x86:

- `MEMORY_1X_x86` (minimum warehouse size: XSMALL)
- `MEMORY_16X_x86` (minimum warehouse size: MEDIUM)
- `MEMORY_64X_x86` (minimum warehouse size: LARGE)

If the warehouse does not have an x86 resource constraint, UDF execution will fail.

This configuration applies to the following operations:

- UDFs registered via `@udf` decorator or `spark.udf.register()`
- UDTFs registered via `@udtf` decorator or `spark.udtf.register()`
- `applyInPandas` via `groupBy().applyInPandas()`

##### Example

The following example creates a warehouse with an x86 resource constraint, then configures Snowpark Connect for Spark to use x86 architecture for UDFs.

Copy code

```
CREATE WAREHOUSE my_x86_warehouse WITH
  WAREHOUSE_SIZE = 'MEDIUM'
  WAREHOUSE_TYPE = 'SNOWPARK-OPTIMIZED'
  RESOURCE_CONSTRAINT = 'MEMORY_16X_x86';

USE WAREHOUSE my_x86_warehouse;
```

Copy code

```
spark.conf.set("snowpark.connect.udf.resource_constraint.architecture", "x86")

@udf(returnType=IntegerType())
def add_one(x: int) -> int:
    return x + 1

df = spark.createDataFrame([(1,), (2,), (3,)], ["value"])
df.select(add_one(df["value"]).alias("result")).show()
```

For more information on warehouses and resource constraints, see [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).
