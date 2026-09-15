# Snowpark Connect for Spark known differences from Apache Spark

Snowpark Connect for Spark lets you run existing PySpark and Spark Connect workloads on Snowflake without
rewriting code. There are two categories of behavioral differences to be aware of when migrating
workloads:

- **Spark Connect protocol differences**: Snowpark Connect for Spark implements the
  [Spark Connect protocol](https://spark.apache.org/docs/latest/spark-connect-overview.html),
  not the Spark Classic (in-process) execution model. If you’re migrating from Spark Classic, you’ll
  encounter behavioral differences inherent to the protocol itself. These differences apply to
  **all** Spark Connect implementations, not just Snowpark Connect for Spark. See
  [Spark Connect vs Spark Classic](#label-snowpark-connect-spark-connect-vs-classic) on this page.
- **Snowflake execution engine differences**: Because Snowflake is the underlying execution engine
  rather than Apache Spark, there are additional semantic and behavioral differences in data types,
  SQL translation, file I/O, and more.

For detailed API compatibility information, including lists of supported and unsupported APIs,
see [DataFrame support for Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-dataframe-support) and
[Dataset support for Snowpark Connect for Spark (Java/Scala)](/developer-guide/snowpark-connect/snowpark-connect-dataset-support).

## Supported Apache Spark versions

Snowpark Connect for Spark supports **Apache Spark 3.5**. Workloads written against
earlier Spark versions (3.4 and below) or later versions (4.0 and above) aren’t supported and may
produce protocol errors or missing API failures.

## Spark Connect vs Spark Classic

Snowpark Connect for Spark uses the
[Spark Connect protocol](https://spark.apache.org/docs/latest/spark-connect-overview.html),
which introduces a gRPC boundary between the client (where you build DataFrame plans) and the
server (where plans are analyzed and executed). Spark Classic runs everything in a single JVM
process, so the plan is analyzed the moment you construct it. In the Spark Connect architecture,
the client sends **unresolved** plans to the server, and resolution happens only when an action
forces it.

This architectural shift has practical consequences for temporary views, error handling, UDF
behavior, and schema access. If you’re migrating code that was written for Spark Classic, the
issues in this section apply regardless of whether the server is Snowpark Connect for Spark, open-source Spark
Connect, or any other Spark Connect implementation.

### Deferred plan resolution

In Spark Classic, every transformation (`filter`, `select`, `join`) immediately validates
column names, data types, and references against the catalog. An invalid column name raises
`AnalysisException` on the line where it’s used.

With Spark Connect, the client builds a lightweight representation of the plan without contacting
the server. Validation only happens when an action (`.collect()`, `.show()`, `.write()`)
ships the plan to the server. Until then, mistakes in column names or incompatible types go
undetected.

Copy code

```
df = spark.createDataFrame([(1, "a"), (2, "b")], ["id", "value"])

# This line succeeds in Spark Connect even though "bad_col" doesn't exist.
# In Spark Classic, it would raise AnalysisException immediately.
result = df.filter("bad_col > 0").select("id")

# The error surfaces only here, when the plan is sent to the server:
result.show()
```

### Temporary view rebinding

This is the single most common source of subtle bugs when moving from Spark Classic to Spark
Connect.

In Spark Classic, `createOrReplaceTempView("v")` snapshots the DataFrame’s fully resolved plan
into the catalog. Any DataFrame that references `v` already has the plan baked in, so
overwriting or dropping `v` later has no effect on existing DataFrames.

In Spark Connect, the client records only the **name** `"v"` in the DataFrame’s unresolved plan.
The name is looked up on the server at execution time. This has two consequences:

- **Overwriting a view** changes the definition that existing DataFrames see, which can produce
  wrong results or duplicate columns.
- **Dropping a view** causes any DataFrame that still references it by name to fail at execution
  time, even if the DataFrame was created before the view was dropped.

#### Overwriting a view

Consider a pipeline that progressively enriches a dataset:

Copy code

```
# Build a base dataset and register it as a view
base = spark.sql("SELECT order_id, customer_id FROM orders")
base.createOrReplaceTempView("pipeline")

# Enrich with customer data using SELECT *
enriched = spark.sql("""
    SELECT p.*, c.region
    FROM pipeline p
    JOIN customers c ON p.customer_id = c.customer_id
""")

# Overwrite the same view with the enriched version
enriched.createOrReplaceTempView("pipeline")

# In Spark Connect, "enriched" still references "pipeline" by name.
# "pipeline" now contains [order_id, customer_id, region].
# The SELECT * re-expands to all three columns, then adds "region" again.
enriched.columns
# -> ['order_id', 'customer_id', 'region', 'region']  <- duplicate
```

#### Dropping a view

In Spark Classic, you can drop a temporary view as soon as you’ve built a DataFrame from it,
because the plan is already resolved. In Spark Connect, the view must remain available until every
DataFrame that references it has been executed:

Copy code

```
df = spark.sql("SELECT * FROM my_view")

# In Spark Classic this is safe; the plan is already resolved
spark.catalog.dropTempView("my_view")

# In Spark Connect this fails because "my_view" no longer exists
df.show()
```

Defer `dropTempView()` calls until no outstanding DataFrames depend on the view.

#### Workarounds

- **Use distinct view names at each stage.** Append a counter, timestamp, or UUID to avoid
  reusing the same name:

  Copy code

  ```
  import uuid

  def register_view(df):
   name = f"v_{uuid.uuid4().hex[:8]}"
   df.createOrReplaceTempView(name)
   return name

  v1 = register_view(base)
  enriched = spark.sql(f"SELECT p.*, c.region FROM {v1} p JOIN customers c ...")
  ```
- **Re-read from the view** after overwriting it to reset the plan reference:

  Copy code

  ```
  base = spark.sql("SELECT order_id, customer_id FROM orders")
  base.createOrReplaceTempView("pipeline")

  enriched = spark.sql("""
   SELECT p.*, c.region
   FROM pipeline p
   JOIN customers c ON p.customer_id = c.customer_id
  """)

  enriched.createOrReplaceTempView("pipeline")
  enriched = spark.table("pipeline")  # now points to the resolved definition

  enriched.columns
  # -> ['order_id', 'customer_id', 'region']  <- correct
  ```

### UDF serialization timing

In Spark Classic, a Python UDF’s closure (the external variables it captures) is serialized at
registration time. Changing those variables afterward doesn’t affect the UDF.

In Spark Connect, serialization is deferred until the plan is executed. The UDF captures whatever
values the external variables hold at that moment, not at definition time. This can produce
confusing results when variables are mutated between UDF definition and DataFrame evaluation.

Copy code

```
from pyspark.sql.functions import udf

threshold = 50

@udf("boolean")
def above_threshold(val):
    return val > threshold

df = spark.range(100).select(above_threshold("id").alias("result"))

threshold = 0  # mutation after UDF definition

# Spark Classic: uses threshold=50 (serialized at definition)
# Spark Connect: uses threshold=0 (serialized at execution)
df.show()
```

**What to do:** Bind the value at definition time using a factory function:

Copy code

```
def make_threshold_udf(limit):
    @udf("boolean")
    def check(val):
        return val > limit
    return check

above_50 = make_threshold_udf(50)
threshold = 0  # has no effect on above_50
spark.range(100).select(above_50("id")).show()  # uses 50
```

### UDF local dependencies

In Spark Classic, a UDF can import modules from the local file system where the application runs
without any additional setup. Spark Classic loads the entire application context into a single JVM
process, so all files on the driver’s `PYTHONPATH` are automatically available inside UDFs.

Spark Connect separates the client from the server, so local files on the client machine aren’t
automatically available on the server where UDFs execute. You must explicitly upload dependencies
using the `addArtifact` API before the UDF can reference them.

Consider a project with this structure:

Copy code

```
src/
├── main.py
└── library.py
```

In Spark Classic, `main.py` can define a UDF that imports from `library.py` directly:

Copy code

```
@udf(returnType=StringType())
def example_udf(input: int) -> str:
    from library import example_function
    return example_function(input)

# Works in Spark Classic because library.py is on the local path
spark.range(1).select(example_udf("id")).show()
```

In Spark Connect (including Snowpark Connect for Spark), this fails with an unresolved module error. To fix it,
add the dependency as an artifact before registering the UDF:

Copy code

```
spark.addArtifact("library.py", pyfile=True)

@udf(returnType=StringType())
def example_udf(input: int) -> str:
    from library import example_function
    return example_function(input)

# Now works because library.py was uploaded to the server
spark.range(1).select(example_udf("id")).show()
```

### Schema access cost

`df.columns`, `df.schema`, and `df.dtypes` are free in Spark Classic because the plan is
already resolved locally. In Spark Connect, each of these properties sends the unresolved plan to
the server for analysis and waits for the response. A single call is fine, but using these
properties inside a loop that also creates new DataFrames on every iteration multiplies the
round-trips:

Copy code

```
df = spark.table("events")

# Each iteration creates a new DataFrame and checks its schema — N round-trips.
for col_name in new_columns:
    if col_name not in df.columns:
        df = df.withColumn(col_name, lit(None))

# Better: snapshot the column list once, maintain it locally.
known = set(df.columns)
for col_name in new_columns:
    if col_name not in known:
        df = df.withColumn(col_name, lit(None))
        known.add(col_name)
```

**What to do:**

- Read `df.columns` or `df.schema` once, store the result in a local variable, and reuse it.
- When inspecting nested types, access the `StructType` fields from the cached schema rather
  than building intermediate DataFrames just to call `.columns` on them.

### APIs not available in Spark Connect

Spark Connect exposes the DataFrame and SQL APIs over gRPC but doesn’t support low-level Spark
Classic APIs that require direct access to the driver JVM, executors, or the cluster manager.
Code that uses any of the following APIs needs to be rewritten before it can run on Snowpark Connect for Spark
or any other Spark Connect endpoint.

| Spark Classic API | Alternative in Spark Connect |
| --- | --- |
| `spark.sparkContext` / `sc` | Use `SparkSession` methods directly |
| **RDD API** (`sc.parallelize`, `rdd.map`, `rdd.flatMap`) | Rewrite as DataFrame operations (`select`, `explode`, `withColumn`) |
| `sc.broadcast()` | Join against a small DataFrame; the optimizer handles broadcast automatically |
| `sc.accumulator()` | Use DataFrame aggregations or write intermediate counts to a table |
| `sc.addPyFile()` / `sc.addFile()` | Stage files and reference them via `snowpark.connect.udf.imports` |
| `DataFrame.foreach()` / `foreachPartition()` | Use `.write` or a UDTF for side-effect operations |
| `DataFrame.rdd` | Stay in the DataFrame API; use `.collect()` to pull data to the client |
| `DataFrame.toLocalIterator()` | Use `.collect()` or write results to a table and read incrementally |
| `TaskContext` | Not available; use DataFrame-level partitioning instead |
| `MapPartitionsInArrow` with Iterator return type | Return a `RecordBatch` directly; iterators aren’t supported as return types |
| `pyspark.ml` (MLlib) | [Snowpark ML](/developer-guide/snowflake-ml/snowpark-ml) or third-party libraries |
| **Structured Streaming** (`readStream` / `writeStream`) | Not supported |
| `DataStreamReader` / `DataStreamWriter` | Not supported; use batch reads/writes |
| JVM interop (`spark._jvm`, `spark._jsc`) | Not available; use SQL or DataFrame API equivalents |

Expand

Show lessSee more

## Data types and numeric behavior

### Integral type representation

Snowpark Connect for Spark implicitly represents `ByteType`, `ShortType`, and `IntegerType` as `LongType`
in many contexts. While the Spark Connect protocol carries distinct type tags for each integral
width, Snowflake’s storage and compute engine uses `NUMBER(p,0)` internally. Snowpark Connect for Spark maps
Snowflake’s reported precisions back to Spark types via integral emulation
(`snowpark.connect.integralTypesEmulation`), but the mapping is lossy:

- `NUMBER(19,0)` maps to `LongType`, `NUMBER(10,0)` to `IntegerType`, `NUMBER(5,0)` to
  `ShortType`, `NUMBER(3,0)` to `ByteType`.
- Any other precision (for example, `NUMBER(38,0)` from a `COUNT(*)`) becomes
  `DecimalType(p,0)`, not a Spark integral type at all.
- Arithmetic operations, aggregations, and joins can change the Snowflake-side precision, causing
  the returned type to shift unexpectedly.
- `.printSchema()` may show `long` where native Spark shows `integer`, or `double` where
  Spark shows `float`.

**What to do:**

The best solution is to enable `snowpark.connect.integralTypesEmulation`. Otherwise, try:

- Avoid branching on specific integer sub-types (`ByteType` vs `IntegerType` vs `LongType`).
  Treat all integer types as interchangeable where possible.
- If precise integral widths matter, use explicit `.cast()` calls to normalize output types.

### Floating-point precision

`FloatType` and `DoubleType` are maintained as distinct types in the protocol and Arrow
transport, but Snowflake’s `FLOAT` and `DOUBLE` are synonymous internally. Operations that
touch the Snowflake engine may return `DoubleType` where Spark would return `FloatType`.
Additionally, floating-point division and aggregation may produce results at higher or lower
default precision than Spark.

**What to do:**

- Use explicit `round()` calls where exact precision matching is required.
- Avoid relying on exact float equality comparisons across systems.

### Integer overflow

Spark uses fixed-width two’s-complement integers (32-bit `int`, 64-bit `long`). Overflow wraps
silently in non-ANSI mode: adding 1 to `Integer.MAX_VALUE` produces `Integer.MIN_VALUE`.
Snowflake uses arbitrary-precision `NUMBER`, which either succeeds with the mathematically
correct result or errors but never wraps.

By default (`handleIntegralOverflow=false`), Snowpark Connect for Spark doesn’t emulate Spark’s wrapping
semantics. Arithmetic on integral types goes through Snowflake’s `NUMBER` math and is cast to
the target type. This means:

- Operations that would silently wrap in Spark may produce mathematically correct (but
  Spark-incompatible) results, or may error if the cast overflows Snowflake’s internal
  representation.
- `-Long.MIN_VALUE` produces a positive result in Snowflake but wraps back to `Long.MIN_VALUE`
  in Spark.
- `abs(Long.MIN_VALUE)` returns `Long.MIN_VALUE` in Spark (wrapping). In Snowpark Connect for Spark it may
  produce a positive value or error.

You can opt in to overflow emulation:

Copy code

```
spark.conf.set("snowpark.connect.handleIntegralOverflow", "true")
```

With this enabled, Snowpark Connect for Spark emulates two’s-complement wrapping via SQL `MOD` operations on an
offset range. When combined with `spark.sql.ansi.enabled=true`, it raises
`ArithmeticException` on overflow instead of wrapping.

**Trade-offs:**

- Enabling overflow emulation adds SQL complexity to every arithmetic expression (extra
  `WHEN`/`OTHERWISE` clauses), which has a measurable performance cost.
- The overflow wrapping logic is not applied to windowed `SUM` operations. Windowed integral sums
  may produce different results than non-windowed equivalents on the same data when overflow occurs.

## Execution model and performance

### Plan re-execution

Each Spark action (`.collect()`, `.show()`, `.write()`) translates to a separate Snowflake
query. Unlike Spark, intermediate results are **not** automatically cached between actions.
Calling `.show()` followed by `.write()` on the same DataFrame executes the full query plan
twice.

**What to do:**

- Call `df.cache()` on DataFrames that are used by multiple downstream actions. This materializes
  the data as a Snowflake temporary table.
- All Spark storage levels (`MEMORY_ONLY`, `MEMORY_AND_DISK`, and others) map to temp table
  storage. There is no in-memory-only caching.

### Data distribution and parallelism

Snowflake manages query parallelism internally through warehouse sizing. Spark’s distribution APIs
behave differently:

| Spark API | Behavior in Snowpark Connect for Spark |
| --- | --- |
| `repartition(N)` | No effect on query parallelism. For writes, produces N sequential `COPY INTO` statements (slower, not faster). |
| `broadcast(df)` | Ignored. Snowflake’s optimizer determines join strategies. |
| `bucketBy()` / `sortBy()` | Ignored. No Snowflake equivalent. |

Expand

Show lessSee more

## SQL and function compatibility

### SQL dialect

Snowpark Connect for Spark translates Spark SQL to Snowflake SQL. Most standard
SQL works as expected, but some constructs have differences:

- Some correlated subquery forms aren’t supported.
- Multi-column `UNPIVOT` has limitations.
- Window frames require an explicit `ORDER BY` clause for bounded frames. Spark doesn’t always
  enforce this.
- Column resolution in `ORDER BY` after column renames may behave differently.

### Functions with UDF-based implementations

Some Spark built-in functions don’t have a direct Snowflake SQL equivalent. Snowpark Connect for Spark
implements these functions as Python or Java UDFs that are registered automatically on first usage.
You can call them exactly as you would in Spark, and they produce correct results,
but they run slower than native SQL functions because of per-row UDF overhead.

Functions implemented this way include `split` (regex path), `from_csv`, `to_csv`,
`map_concat`, `map_entries`, `posexplode`, `inline`, `xxhash64`, higher-order functions,
and XPath functions, among others.

A smaller set of aggregate functions (`try_sum`, `histogram_numeric`, `percentile`,
`count_min_sketch`) are implemented as Python UDAFs. These are significantly slower than native
aggregates because they serialize and deserialize state for every row.

**What to do:** If you notice slow performance on a query that uses one of these functions, check
whether a fully compatible native equivalent is available.

### Regular expressions

Snowflake uses POSIX Extended Regular Expressions (ERE), while Spark uses Java’s
`java.util.regex`. This affects `rlike`, `regexp_extract`, `regexp_replace`, and the
regex path of `split`:

- Embedded flags (`(?i)`, `(?s)`) aren’t supported.
- Lookaheads and lookbehinds aren’t available.
- Unicode character class support differs.
- Group index behavior differs (empty string vs error on non-matching groups).

This isn’t fixable in Snowpark Connect for Spark because it’s a fundamental engine-level difference.

**What to do:**

- Test regex patterns against Snowflake’s regex engine. Rewrite patterns that rely on Java-specific
  features.
- For case-insensitive matching, use `LOWER()` / `UPPER()` instead of `(?i)`.

## Structured types (ARRAY, MAP, STRUCT)

### STRUCT field ordering

Snowflake alphabetizes STRUCT fields, while Spark preserves definition order. This can affect
hash-based comparisons (for example, SCD type 2 logic) where field sequence matters for
reproducible hash values.

**What to do:**

- Compute hashes on individual fields in a deterministic (for example, alphabetical) order rather
  than hashing the entire STRUCT.
- Define STRUCT fields in alphabetical order in both source and target schemas for consistency.

## Timestamps and timezones

- `cast(..., TimestampType())` behavior depends on Snowflake’s `TIMESTAMP_TYPE_MAPPING` account
  parameter, which Snowpark Connect for Spark doesn’t control. This can silently change semantics across
  Snowflake accounts.
- Spark’s distinction between `TIMESTAMP_NTZ` and `TIMESTAMP_LTZ` maps imperfectly to
  Snowflake’s timestamp types.
- Parquet timestamp rebase modes (pre-Gregorian calendar handling) are unsupported. Pre-Gregorian
  dates may be silently corrupted.
- Session timezone interactions between Spark configs and Snowflake session parameters create
  subtle edge cases.
- Timestamp overflow guards exist for microsecond/millisecond/second conversions (`int64` range),
  but the error behavior differs from Spark’s `ArithmeticException`.

**What to do:**

- Explicitly set the session timezone:
  `spark.conf.set("spark.sql.session.timeZone", "UTC")`
- Use `TIMESTAMP_NTZ` consistently when timezone-awareness isn’t needed.
- Test timestamp-heavy workloads with representative data before production migration.

## Session management

### Session isolation

The Snowpark Connect for Spark package server is designed for single-user use. Each developer or isolated
workload should run its own server process. All Spark Connect client sessions that connect to
the same server process share a single underlying Snowflake session. While per-session state
(configs, temp views, UDF registrations) is tracked separately in memory, the underlying
Snowflake session parameters (warehouse, role, timezone) aren’t isolated per Spark session.

Implications when multiple clients share the same server process:

- Setting a warehouse or role in one session may affect other concurrent sessions.
- Objects created in Snowflake may be visible to, and modified by, other Spark sessions connected to the same server process.

**What to do:**

- Run one Snowpark Connect for Spark server process per user or per isolated workload. See
  [Install Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide-install).
- Avoid changing Snowflake session parameters (warehouse, role) at runtime if multiple clients
  share the same server process.

### Concurrency

The gRPC server uses a `ThreadPoolExecutor` (default 10 workers) to handle concurrent requests.
CPU-bound plan translation holds the Python GIL, which means concurrent requests may serialize
during the translation phase. Query execution on Snowflake is fully parallel.

**What to do:**

- Batch DataFrame operations to reduce the number of server round-trips.
- For high-concurrency deployments, size the server appropriately and consider multiple server
  instances.

## Catalog and metadata

`spark.catalog.*` APIs return Snowflake’s metadata model, which differs structurally from
Spark’s:

- Snowflake tables don’t have Spark-style partition columns. Partition-based operations
  (`recoverPartitions`, `writeTo` with `overwritePartitions`) fail or behave differently.
- `listDatabases`, `listTables`, and `listFunctions` return different metadata structures.
- Schema nullability metadata isn’t preserved.
- `refreshTable` and `refreshByPath` have no Snowflake equivalent.

## Observability and debugging

- `explain()` produces Snowflake execution plans, not Spark logical/physical plans.
- `observe()` / `collect_metrics` are no-ops. Spark’s observability framework has no
  equivalent.
- `interrupt()` for cancelling long-running queries isn’t implemented.
- Error messages originate from Snowflake and may differ in format from Spark’s exceptions.
  Snowflake may redact values in error messages for security.

**What to do:**

- Use Snowflake’s [Query History](/user-guide/ui-snowsight-activity) to monitor and debug
  query execution.
- Set `query_tag` via Spark config to correlate Snowpark Connect for Spark queries with application-level
  context.

## Java and Scala limitations

- Only **Java 11** and **Java 17** are supported.
- Only **Scala 2.12** and **Scala 2.13** are supported.
- **Java/Scala UDTFs and UDAFs** aren’t supported.
- **Interval types** aren’t supported inside user-defined functions (`Interval` inside UDFs).
