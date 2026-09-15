# Executing Snowflake SQL with Snowpark Connect for Spark

To execute SQL commands specific to Snowflake, you can use the `SnowflakeSession` interface. As with the `spark.sql` method,
query results are returned as Spark DataFrames, and you can continue applying or chaining Spark DataFrame transformations and actions on
the resulting data.

With most SQL operations, you can use the `spark.sql` method to execute SQL statements directly and retrieve the results as Spark
DataFrames. However, some parts of Snowflake SQL syntax, including QUALIFY, CONNECT BY, LATERAL FLATTEN, and time travel queries, are
not compatible with Spark SQL. For those, use the `SnowflakeSession` interface instead.

## Using spark.sql() for standard SQL

`spark.sql()` is the standard way to run SQL in a Spark session. Use it for SQL that Spark SQL accepts, including SELECT,
CREATE TABLE, INSERT, and similar statements. Results are returned as DataFrames.

PythonJavaScala

Copy code

```
import snowflake.snowpark_connect

spark = snowflake.snowpark_connect.init_spark_session()

df = spark.sql("SELECT * FROM my_table WHERE value > 10")
df.show()

spark.sql("CREATE TABLE IF NOT EXISTS my_table (id INT, name STRING)")

spark.sql("INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob')")
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

SparkSession spark = SnowparkConnectSession.builder()
    .appName("My App")
    .getOrCreate();

Dataset<Row> df = spark.sql("SELECT * FROM my_table WHERE value > 10");
df.show();

spark.sql("CREATE TABLE IF NOT EXISTS my_table (id INT, name STRING)");

spark.sql("INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob')");
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession

val spark = SnowparkConnectSession.builder()
  .appName("My App")
  .getOrCreate()

val df = spark.sql("SELECT * FROM my_table WHERE value > 10")
df.show()

spark.sql("CREATE TABLE IF NOT EXISTS my_table (id INT, name STRING)")

spark.sql("INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob')")
```

## Using SnowflakeSession for Snowflake-specific SQL

Snowflake-specific SQL syntax, such as CONNECT BY … PRIOR, START WITH, QUALIFY, LATERAL FLATTEN,
time travel queries, and functions like ZEROIFNULL, fails through the standard `spark.sql()` path because the Spark
parser doesn’t recognize it. To execute these statements, use the `SnowflakeSession` interface. Query results are returned as
Spark DataFrames, so you can continue chaining DataFrame transformations and actions on the resulting data.

The following examples show how to use `SnowflakeSession` to execute a Snowflake SQL command
that includes the CONNECT BY clause.

PythonJavaScala

Copy code

```
import snowflake.snowpark_connect
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession

spark = snowflake.snowpark_connect.init_spark_session()
snowflake_session = SnowflakeSession(spark)
result_df = snowflake_session.sql("""
  SELECT
  employee_name,
  manager_name,
  LEVEL
FROM employees
START WITH employee_name = 'Alice'
CONNECT BY PRIOR manager_name = employee_name
""")
result_df.show()
result_df.limit(1).show()
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import com.snowflake.snowpark_connect.client.SnowflakeSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

SparkSession spark = SnowparkConnectSession.builder()
    .appName("My App")
    .getOrCreate();

SnowflakeSession sf = new SnowflakeSession(spark);
Dataset<Row> resultDf = sf.sql(
    "SELECT employee_name, manager_name, LEVEL "
    + "FROM employees "
    + "START WITH employee_name = 'Alice' "
    + "CONNECT BY PRIOR manager_name = employee_name");
resultDf.show();
resultDf.limit(1).show();
```

Copy code

```
import com.snowflake.snowpark_connect.client.{SnowparkConnectSession, SnowflakeSession}

val spark = SnowparkConnectSession.builder()
  .appName("My App")
  .getOrCreate()

val sf = new SnowflakeSession(spark)
val resultDf = sf.sql(
  """SELECT employee_name, manager_name, LEVEL
    |FROM employees
    |START WITH employee_name = 'Alice'
    |CONNECT BY PRIOR manager_name = employee_name""".stripMargin)
resultDf.show()
resultDf.limit(1).show()
```

### Working with SnowflakeSession results

`SnowflakeSession.sql()` executes queries directly against Snowflake, bypassing Spark SQL translation entirely. This has
several implications for how results behave compared to standard `spark.sql()`.

#### Column naming and case sensitivity

Column names in passthrough results follow Snowflake identifier rules:

- Unquoted identifiers are returned in uppercase. For example, `SELECT name` yields a column called `NAME`.
- Quoted identifiers preserve their original casing. For example, `SELECT "myCol"` stays `myCol`.

When `spark.sql.caseSensitive` is `false` (the default), any casing works in downstream DataFrame operations. When
`spark.sql.caseSensitive` is `true`, you must match the exact casing that Snowflake returns. For example,
`df.select("name")` fails if the column was returned as `NAME`, and `df.select("MYVALUE")` fails if the column was
created as `"myValue"`.

For the most forgiving behavior, keep `spark.sql.caseSensitive` at its default `false`. If you must use `true`, use
uppercase column names for unquoted identifiers and match the exact quoted casing for quoted identifiers.

#### Special characters in column names

Passthrough SQL returns column names directly from Snowflake metadata. Unquoted identifiers are
uppercased (for example, `normal_col` becomes `NORMAL_COL`), which is harmless. Columns
created with double quotes in Snowflake (spaces, symbols, or mixed casing) need care when you
build SQL strings from `df.columns`, but work fine in the DataFrame API.

**DataFrame API (no quoting needed)**

The DataFrame API handles quoting automatically, so special-character columns work without extra
steps:

PythonJavaScala

Copy code

```
df = snowflake_session.sql('SELECT 1 AS "col with spaces", 2 AS "another col"')

df.select("col with spaces").show()
df.select(*df.columns).collect()
df.filter(df["`col with spaces`"] > 0).show()
```

Copy code

```
Dataset<Row> df = sf.sql("SELECT 1 AS \"col with spaces\", 2 AS \"another col\"");

df.select("col with spaces").show();
df.select(df.columns()).collectAsList();
df.filter(df.col("col with spaces").gt(0)).show();
```

Copy code

```
val df = sf.sql("""SELECT 1 AS "col with spaces", 2 AS "another col"""")

df.select("col with spaces").show()
df.select(df.columns.map(col): _*).collect()
df.filter(df("`col with spaces`") > 0).show()
```

**Building SQL strings for passthrough**

If you construct follow-up passthrough SQL from `df.columns`, wrap each name in Snowflake
double quotes. Without quoting, column names with spaces cause invalid identifier errors:

PythonJavaScala

Copy code

```
spark.conf.set("snowpark.connect.temporary.views.create_in_snowflake", True)
df.createOrReplaceTempView("my_view")

# Fails: unquoted special-character columns
snowflake_session.sql(f"SELECT {','.join(df.columns)} FROM my_view")

# Works: Snowflake double-quote quoting with uppercase
query_cols = ", ".join(f'"{c.upper()}"' for c in df.columns)
snowflake_session.sql(f"SELECT {query_cols} FROM my_view")
```

Copy code

```
spark.conf().set("snowpark.connect.temporary.views.create_in_snowflake", "true");
df.createOrReplaceTempView("my_view");

// Works: Snowflake double-quote quoting with uppercase
String queryCols = Arrays.stream(df.columns())
    .map(c -> "\"" + c.toUpperCase() + "\"")
    .collect(Collectors.joining(", "));
sf.sql("SELECT " + queryCols + " FROM my_view");
```

Copy code

```
spark.conf.set("snowpark.connect.temporary.views.create_in_snowflake", "true")
df.createOrReplaceTempView("my_view")

// Works: Snowflake double-quote quoting with uppercase
val queryCols = df.columns.map(c => s""""${c.toUpperCase}"""").mkString(", ")
sf.sql(s"SELECT $queryCols FROM my_view")
```

**Building SQL strings for spark.sql()**

When using `spark.sql()` instead of passthrough, column names follow Spark SQL rules and require
backtick quoting:

PythonJavaScala

Copy code

```
query_cols = ", ".join(f"`{c}`" for c in df.columns)
spark.sql(f"SELECT {query_cols} FROM my_view")
```

Copy code

```
String queryCols = Arrays.stream(df.columns())
    .map(c -> "`" + c + "`")
    .collect(Collectors.joining(", "));
spark.sql("SELECT " + queryCols + " FROM my_view");
```

Copy code

```
val queryCols = df.columns.map(c => s"`$c`").mkString(", ")
spark.sql(s"SELECT $queryCols FROM my_view")
```

Columns without special characters (standard unquoted identifiers) don’t need any quoting in
either path.

#### Table-qualified column references

DataFrames from passthrough SQL carry no table qualifier metadata. Using table-qualified column references such as
`df.select("my_table.ID")` raises an exception. Use bare column names instead (for example, `df.select("ID")`). If you
need qualified references, read the table through `spark.table()` instead of passthrough SQL.

#### Temporary views

Passthrough SQL executes directly on Snowflake. Temporary views created with `createOrReplaceTempView()` are local to
Snowpark Connect for Spark by default and invisible to Snowflake-side SQL. To make them available to passthrough queries, set
`snowpark.connect.temporary.views.create_in_snowflake` to `true` before creating the view:

PythonJavaScala

Copy code

```
spark.conf.set("snowpark.connect.temporary.views.create_in_snowflake", "true")
df.createOrReplaceTempView("my_view")

result = snowflake_session.sql("SELECT * FROM my_view")
```

Copy code

```
spark.conf().set("snowpark.connect.temporary.views.create_in_snowflake", "true");
df.createOrReplaceTempView("my_view");

Dataset<Row> result = sf.sql("SELECT * FROM my_view");
```

Copy code

```
spark.conf.set("snowpark.connect.temporary.views.create_in_snowflake", "true")
df.createOrReplaceTempView("my_view")

val result = sf.sql("SELECT * FROM my_view")
```

#### Query execution behavior

Multi-statement SQL separated by semicolons isn’t supported in either `spark.sql()` or `SnowflakeSession.sql()`, which is standard Spark behavior.
Execute multiple statements as separate `spark.sql()` or `SnowflakeSession.sql()` calls.
Only a single trailing semicolon (with optional whitespace) is safely stripped and executed.

#### Portability

`SnowflakeSession.sql()` is not portable to open-source PySpark. It uses internal syntax that the open-source Spark parser
doesn’t recognize. If your code needs to run on both Snowpark Connect for Spark and PySpark, wrap `SnowflakeSession` usage in conditional logic.

## Setting session-level parameters

You can also use the `SnowflakeSession` interface to execute configuration directives specific to Snowflake. These directives
include setting session-level parameters such as the active database, schema, warehouse, and role.

Important

Changing session-level parameters affects all subsequent Spark queries in the same session. For example, calling
`use_database()` changes which database future `spark.sql()` queries resolve table names against. Make sure you
understand the impact before modifying these values mid-session.

The following examples show how to use `SnowflakeSession` to set session-level parameters.

PythonJavaScala

Copy code

```
import snowflake.snowpark_connect
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession

spark = snowflake.snowpark_connect.init_spark_session()
snowflake_session = SnowflakeSession(spark)

snowflake_session.use_database("MY_DATABASE")
snowflake_session.use_schema("MY_SCHEMA")
snowflake_session.use_warehouse("MY_WH")
snowflake_session.use_role("PUBLIC")
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import com.snowflake.snowpark_connect.client.SnowflakeSession;
import org.apache.spark.sql.SparkSession;

SparkSession spark = SnowparkConnectSession.builder()
    .appName("My App")
    .getOrCreate();

SnowflakeSession sf = new SnowflakeSession(spark);

sf.useDatabase("MY_DATABASE");
sf.useSchema("MY_SCHEMA");
sf.useWarehouse("MY_WH");
sf.useRole("PUBLIC");
```

Copy code

```
import com.snowflake.snowpark_connect.client.{SnowparkConnectSession, SnowflakeSession}

val spark = SnowparkConnectSession.builder()
  .appName("My App")
  .getOrCreate()

val sf = new SnowflakeSession(spark)

sf.useDatabase("MY_DATABASE")
sf.useSchema("MY_SCHEMA")
sf.useWarehouse("MY_WH")
sf.useRole("PUBLIC")
```

By default, the DDL helpers pass identifiers unquoted, so Snowflake uppercases them. If the
identifier has mixed or non-standard casing, pass `preserve_case=True` (Python) or
`preserveCase=true` (Java/Scala):

PythonJavaScala

Copy code

```
snowflake_session.use_schema("My_Schema", preserve_case=True)
snowflake_session.use_role("MyCustomRole", preserve_case=True)
```

Copy code

```
sf.useSchema("My_Schema", true);
sf.useRole("MyCustomRole", true);
```

Copy code

```
sf.useSchema("My_Schema", true)
sf.useRole("MyCustomRole", true)
```
