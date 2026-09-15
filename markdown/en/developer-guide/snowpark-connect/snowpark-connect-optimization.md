# Optimizing Snowpark Connect for Spark workloads

This page describes strategies for improving the performance of your Snowpark Connect for Spark workloads.
The recommendations are organized from high-level principles to specific, actionable techniques
for reading, transforming, caching, and writing data.

## How Snowpark Connect for Spark executes your code

Understanding how Snowpark Connect for Spark processes your Spark code is the foundation for effective
optimization.

Your Spark code runs on a local machine, a Snowflake Notebook, or in
Snowpark Container Services. Snowpark Connect for Spark translates DataFrame operations into SQL and sends them
to a Snowflake warehouse for execution. The warehouse handles all compute, storage I/O, and
parallelism.

Evaluation is **lazy**: transformations like `filter`, `select`, and `join` are deferred until
a terminal action (`show`, `collect`, `write`, `count`) triggers execution. At that point,
Snowpark Connect for Spark compiles the full transformation chain into one or more SQL statements and submits them
to the warehouse.

Each action on an **uncached** DataFrame triggers a full re-execution of the plan. If you call
`show()` and then `count()` on the same DataFrame, the underlying query runs twice. See
[Caching and materialization](#label-spconnect-caching) for how to avoid this.

The Snowflake query optimizer controls execution strategy automatically. Hints like
`broadcast` don’t affect how queries run on Snowflake.
Similarly `repartition` doesn’t control query parallelism, but it does affect the statement result.

## General principles

The following principles apply broadly across all Snowpark Connect for Spark workloads.

### UDFs significantly impact performance

Most of the operations that stay in the DataFrame API run natively on the Snowflake engine. User-defined
functions cross a sandbox boundary, adding serialization overhead and preventing the query
optimizer from inlining the logic. Replace simple UDFs with built-in Spark functions (`lower`,
`trim`, `date_format`, `when`) whenever possible.

### Filter and project early

Push filters and column selections before joins, aggregations, sorts, and UDFs. The fewer rows and columns
in the pipeline, the less data Snowflake processes and the less data crosses the gRPC boundary
between the client and Snowflake.

Copy code

```
# Preferred: filter and select before the join
orders = orders.filter(col("status") == "active").select("order_id", "customer_id", "amount")
result = orders.join(customers, "customer_id")

# Avoid: joining first, then filtering
result = orders.join(customers, "customer_id").filter(col("status") == "active")
```

### Provide explicit schemas

Schema inference (`inferSchema=True`) samples each file to determine column types. This applies
to CSV, JSON, and Parquet formats. For repeated reads, infer the schema once and reuse it:

Copy code

```
# Infer once
schema = spark.read.option("inferSchema", "true").csv("@stage/sample.csv").schema

# Reuse for all subsequent reads
for path in file_paths:
    df = spark.read.schema(schema).csv(path)
```

If your data is uniform, you can improve performance by reducing the per-file sample size with
`rowsToInferSchema`. This option is available for CSV, JSON, and Parquet:

Copy code

```
df = spark.read.option("rowsToInferSchema", "100").csv("@stage/data.csv", inferSchema=True)
df = spark.read.option("rowsToInferSchema", "50").json("@stage/data.json")
```

## Reading data efficiently

### Use external tables for partitioned reads

When reading Hive-style partitioned Parquet from an external stage, partition pruning at the storage
layer requires an external table. Without one, Snowpark Connect for Spark reads all files and applies filters after
loading.

The most reliable approach is to create and manage the external table yourself using
[CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) with the `PARTITION_TYPE = HIVE` option. This gives you full control over refresh scheduling, column definitions, and access
grants. Once the table exists, read it directly:

Copy code

```
df = spark.table("my_external_table")
df = df.filter(col("date") == "2026-01-15")  # Only reads matching partitions
```

Alternatively, Snowpark Connect for Spark can create a temporary external table automatically. Set the
`snowpark.connect.sql.partition.external_table_location` configuration to the stage path:

Copy code

```
spark.conf.set("snowpark.connect.sql.partition.external_table_location", "@my_ext_stage")

df = spark.read.parquet("@my_ext_stage/data/")
df = df.filter(col("date") == "2026-01-15")  # Only reads matching partitions
```

This automatic option applies when all of the following are true:

- Data is on an **external stage** (S3, Azure Blob Storage, GCS).
- Files are in **Parquet** format.
- Directories follow Hive-style `key=value` partitioning.

Providing an explicit schema avoids inference overhead and is recommended for large datasets.

### Follow file layout best practices

How your data files are organized affects read performance:

- **Use fewer, larger files** (100-500 MB each). Many small files incur per-file overhead
  from listing, opening, and processing each file individually.
- **Prefer Parquet** for analytical workloads. Parquet supports columnar pruning and built-in
  compression, reducing both I/O and storage costs.
- **Prefer directory paths over individual file lists** when reading multiple files.
  Reading a directory or glob pattern is more efficient than listing files individually.

## Transformations and query generation

### Supply explicit pivot values

When you call `pivot()` without specifying values, Snowpark Connect for Spark runs a `SELECT DISTINCT` query
followed by `collect()` to discover the unique pivot values before executing the actual pivot.
This adds a full extra round trip to Snowflake.

Copy code

```
# Slow: triggers an extra query to discover pivot values
df.groupBy("region").pivot("quarter").sum("revenue")

# Fast: skip the discovery query
df.groupBy("region").pivot("quarter", ["Q1", "Q2", "Q3", "Q4"]).sum("revenue")
```

This matters especially for high-cardinality pivot columns.

### Use literal window frame boundaries

Non-literal window frame boundaries (computed from expressions) require Snowpark Connect for Spark to execute an
extra Snowflake query to evaluate the boundary value. Prefer literal integers:

Copy code

```
from pyspark.sql.window import Window

# Fast: literal boundaries
w = Window.partitionBy("dept").orderBy("salary").rowsBetween(-3, 3)

# Slower: expression boundary triggers an extra query per window spec
w = Window.partitionBy("dept").orderBy("salary").rowsBetween(-some_col, some_col)
```

For window functions in general, choose low-to-medium cardinality partition keys and ensure order
keys align with table clustering when possible.

### Prefer union over unionByName

`union()` requires DataFrames to have identical schemas in the same column order and produces
minimal overhead. `unionByName()` inspects both schemas, renames columns to align by name, and
resolves common types, adding overhead.

Use `union()` when you control the schema and column order. Use `unionByName()` only when
schemas might differ.

### Prefer literal regex patterns

Snowpark Connect for Spark translates Spark’s `rlike` to Snowflake’s `REGEXP_INSTR` with null and empty-string
handling. When the pattern is a **column expression** instead of a literal string,
it requires an additional runtime conditional to handle edge cases, which can degrade performance.
Use literal patterns when possible:

Copy code

```
# Fast: literal pattern
df.filter(col("name").rlike("^John.*"))

# Slower: column-based pattern adds runtime conditionals
df.filter(col("name").rlike(col("pattern_column")))
```

### Avoid expensive anti-patterns

The following patterns are common sources of performance problems:

**Avoid** `collect()` **on large DataFrames**
:   `collect()` pulls all rows to the client over gRPC. Use `.limit()` to sample, or write
    results to a table and query them there.

**Avoid** `count()` **for existence checks**
:   `count()` scans the entire dataset. To check whether data exists, use `df.head(1)` or
    `df.limit(1).collect()` instead.

**Avoid chaining** `withColumns` **calls**
:   Although Snowpark Connect for Spark applies some flattening to reduce nesting from chained `withColumn`
    calls, using `select()` to add multiple columns in a single operation produces cleaner SQL.
    In complex pipelines with many transformations, excessive nesting can still contribute to longer
    SQL compilation times.

    Copy code

    ```
    # Preferred: batch column additions
    df = df.select(
        "*",
        (col("price") * col("quantity")).alias("total"),
        upper(col("name")).alias("name_upper"),
    )

    # Avoid: chained withColumn calls
    df = df.withColumn("total", col("price") * col("quantity"))
    df = df.withColumn("name_upper", upper(col("name")))
    ```

**Avoid** `toPandas()` **on large datasets**
:   `toPandas()` transfers all data to the client and converts it to a Pandas DataFrame. Process
    data in Snowflake and export only the final, reduced result.

**Avoid** `offset()` **and** `tail()` **on large DataFrames**
:   `offset()` without `limit()` triggers a hidden `count()` on the full DataFrame.
    `tail(n)` also calls `count()` internally. Prefer sorting in reverse with `limit()`:

    Copy code

    ```
    # Avoid: hidden full-table count()
    result = df.offset(1000)
    last_rows = df.tail(10)

    # Preferred
    last_rows = df.orderBy(col("id").desc()).limit(10).collect()
    ```

**Avoid repeated DataFrame references without caching**
:   Each action on an uncached DataFrame re-executes the full query plan. This causes exponential
    SQL growth and can trigger compilation timeouts. Use `persist()` or `cache()` to break the
    dependency chain. See [Caching and materialization](#label-spconnect-caching).

## Caching and materialization

### How caching works

Unlike Spark, which caches data in executor memory, Snowpark Connect for Spark materializes cached DataFrames as
Snowflake temporary tables. Explicitly modifying the Spark storage level doesn’t change the behavior.
The temporary table persists for the session duration.

Each action (`collect()`, `show()`, `write()`) on an **uncached** DataFrame triggers a full
re-execution of the query plan. If you need multiple actions on the same expensive DataFrame,
caching avoids redundant computation:

Copy code

```
# Without cache: the filter + join runs TWICE
expensive_df = large_df.join(other_df, "key").filter(col("x") > 100)
expensive_df.show()       # executes full plan
expensive_df.count()      # executes full plan AGAIN

# With cache: filter + join runs once, temp table is reused
expensive_df = large_df.join(other_df, "key").filter(col("x") > 100).cache()
expensive_df.show()       # materializes temp table, then reads
expensive_df.count()      # reads from temp table
expensive_df.unpersist()  # clean up when done
```

### When not to cache

Caching isn’t beneficial if you use a DataFrame only once or don’t reuse the cached data,
because creating the temporary table adds overhead.

### Describe cache

Snowpark Connect for Spark caches schema metadata to avoid repeated `DESCRIBE` queries against Snowflake.
The `snowpark.connect.describe_cache_ttl_seconds` property controls the cache lifetime
(default: 300 seconds).

- Increase for stable schemas to reduce metadata query overhead.
- Decrease or set to `0` for rapidly evolving schemas during development.
- A longer TTL can visibly boost performance for short workloads.

### Temporary views

The `snowpark.connect.temporary.views.create_in_snowflake` property controls whether temporary
views are created as Snowflake objects. Creating them in Snowflake can improve query compilation time,
but if the view has a long definition, it can fail due to Snowflake view size limits.

## UDF and UDTF performance

When you need custom logic that can’t be expressed with built-in functions, follow these guidelines
to minimize UDF overhead:

- **Prefer native Spark functions** (`lower`, `trim`, `date_format`, `regexp_replace`)
  over equivalent UDF implementations.
- **Minimize the package count** in your UDF dependencies. Each additional package increases
  cold-start resolution time. Pin package versions to avoid unexpected resolution delays.
- **Reuse UDF objects** instead of redefining them. Snowpark Connect for Spark caches UDF registrations by
  hashing the definition. Reusing the same UDF object avoids re-registration:

  Copy code

  ```
  # Good: define once, reuse across DataFrames
  my_udf = udf(my_func, returnType=StringType())
  df1.select(my_udf(col("a")))
  df2.select(my_udf(col("b")))

  # Avoid: redefining identical UDFs in a loop
  for table in tables:
   local_udf = udf(my_func, returnType=StringType())  # re-registers each time
   spark.table(table).select(local_udf(col("a")))
  ```
- **Align your Python version** with the Snowflake server’s Python version. If the client and
  server Python minor versions differ, UDFs might require additional processing before they’re
  created, which adds overhead.

For more details, see [User-defined functions with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-udfs).

## Warehouse sizing and Spark no-ops

Warehouse size directly affects query execution time. Use larger warehouses for data-intensive
ETL jobs and batch workloads. Right-size to smaller warehouses for iterative development and
testing.

Many Spark settings related to executors, memory, shuffle partitions, and optimizer hints are
accepted silently for compatibility but have no effect in Snowpark Connect for Spark. Properties like
`spark.executor.memory`, `spark.driver.memory`, and `spark.sql.shuffle.partitions` are
no-ops. Snowflake manages all compute resources, memory allocation, and parallelism internally.

For a complete list of supported properties, see
[Snowpark Connect for Spark properties](/developer-guide/snowpark-connect/snowpark-connect-parameters).
