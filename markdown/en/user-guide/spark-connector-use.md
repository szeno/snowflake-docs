# Using the Spark Connector

The connector adheres to the standard Spark API, but with the addition of Snowflake-specific options, which are described in this topic.

In this topic, the term COPY refers to both:

- [COPY INTO <table>](/sql-reference/sql/copy-into-table) (used to transfer data from an internal or external stage into a table).
- [COPY INTO <location>](/sql-reference/sql/copy-into-location) (used to transfer data from a table into an internal or external stage).

## Verifying the network connection to Snowflake

To test a connection to Snowflake, use the `snow connection test` command in Snowflake CLI. For connection setup and diagnostic options, see [Test and diagnose a connection](/developer-guide/snowflake-cli/connecting/configure-connections#test-and-diagnose-a-connection).

Run the test from the environment whose network connectivity you want to check. A successful CLI connection test doesn’t verify the Spark Connector’s configuration or connectivity from other Spark nodes.

## Pushdown

The Spark Connector applies predicate and query pushdown by capturing and analyzing the Spark logical plans for SQL operations. When the data source is Snowflake, the operations are translated into a SQL query and then executed in Snowflake to improve performance.

However, because this translation requires almost a one-to-one translation of Spark SQL operators to Snowflake expressions, not all of Spark SQL operators can be pushed down. When pushdown fails, the connector falls back to a less-optimized execution plan. The unsupported operations are instead performed in Spark.

Note

If you need pushdown for all operations, consider writing your code to use [Snowpark API](/developer-guide/snowpark/index) instead.

Below is a list of supported operations for pushdown (all functions below use their Spark names). If a function is not in this list, a Spark plan that utilizes it might be executed on Spark rather than pushed down into Snowflake.

- Aggregation Functions

  - Average
  - Corr
  - CovPopulation
  - CovSample
  - Count
  - Max
  - Min
  - StddevPop
  - StddevSamp
  - Sum
  - VariancePop
  - VarianceSamp
- Boolean Operators

  - And
  - Between
  - Contains
  - EndsWith
  - EqualTo
  - GreaterThan
  - GreaterThanOrEqual
  - In
  - IsNull
  - IsNotNull
  - LessThan
  - LessThanOrEqual
  - Not
  - Or
  - StartsWith
- Date, Time, and Timestamp Functions

  - DateAdd
  - DateSub
  - Month
  - Quarter
  - TruncDate
  - TruncTimestamp
  - Year
- Mathematical Functions

  - Arithmetic operators ‘+’ (addition), ‘-’ (subtraction), ‘\*’ (multiplication), ‘/’ (division), and ‘-’ (unary negation).
  - Abs
  - Acos
  - Asin
  - Atan
  - Ceil
  - CheckOverflow
  - Cos
  - Cosh
  - Exp
  - Floor
  - Greatest
  - Least
  - Log
  - Pi
  - Pow
  - PromotePrecision
  - Rand
  - Round
  - Sin
  - Sinh
  - Sqrt
  - Tan
  - Tanh
- Miscellaneous Operators

  - Alias (AS expressions)
  - BitwiseAnd
  - BitwiseNot
  - BitwiseOr
  - BitwiseXor
  - CaseWhen
  - Cast(child, t, \_)
  - Coalesce
  - If
  - MakeDecimal
  - ScalarSubquery
  - ShiftLeft
  - ShiftRight
  - SortOrder
  - UnscaledValue
- Relational Operators

  - Aggregate functions and group-by clauses
  - Distinct
  - Filters
  - In
  - InSet
  - Joins
  - Limits
  - Projections
  - Sorts (ORDER BY)
  - Union and Union All
  - Window functions and windowing-clauses
- String Functions

  - Ascii
  - Concat(children)
  - Length
  - Like
  - Lower
  - StringLPad
  - StringRPad
  - StringTranslate
  - StringTrim
  - StringTrimLeft
  - StringTrimRight
  - Substring
  - Upper
- Window Functions (note: these do not work with Spark 2.2)

  - DenseRank
  - Rank
  - RowNumber

## Using the Connector in Scala

### Specifying the Data Source Class Name

To use Snowflake as a data source in Spark, use the `.format` option to provide the Snowflake connector class name that defines the data source.

> `net.snowflake.spark.snowflake`

To ensure a compile-time check of the class name, Snowflake highly recommends defining a variable for the class name. For example:

Copy code

```
val SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
```

Also, for convenience, the `Utils` class provides the variable, which can be imported as follows:

Copy code

```
import net.snowflake.spark.snowflake.Utils.SNOWFLAKE_SOURCE_NAME
```

Note

All examples in this topic use `SNOWFLAKE_SOURCE_NAME` as the class definition.

### Enabling/Disabling Pushdown in a Session

Version 2.1.0 (and higher) of the connector supports query pushdown, which can significantly improve performance by pushing query processing to Snowflake when Snowflake is the Spark data source.

By default, pushdown is enabled.

To disable pushdown within a Spark session for a given DataFrame:

1. After instantiating a `SparkSession` object, call the `SnowflakeConnectorUtils.disablePushdownSession` static
   method, passing in the `SparkSession` object. For example:

   Copy code

   ```
   SnowflakeConnectorUtils.disablePushdownSession(spark)
   ```

   Where `spark` is your `SparkSession` object.
2. Create a DataFrame with the [autopushdown](/user-guide/spark-connector-use#label-spark-options-autopushdown) option set to `off`. For example:

   Copy code

   ```
   val df = sparkSession.read.format(SNOWFLAKE_SOURCE_NAME)
     .options(sfOptions)
     .option("query", query)
     .option("autopushdown", "off")
     .load()
   ```

   Note that you can also set the `autopushdown` option in a `Map` that you pass to the `options` method (e.g.
   in `sfOptions` in the example above).

To enable pushdown again after disabling it, call the `SnowflakeConnectorUtils.enablePushdownSession` static method
(passing in the `SparkSession` object), and create a DataFrame with `autopushdown` enabled.

### Moving Data from Snowflake to Spark

Note

When using DataFrames, the Snowflake connector supports SELECT queries only.

To read data from Snowflake into a Spark DataFrame:

1. Use the `read()` method of the `SqlContext` object to construct a `DataFrameReader`.
2. Specify `SNOWFLAKE_SOURCE_NAME` using the `format()` method. For the definition, see [Using the Connector in Scala](#label-spark-data-source) (in this topic).
3. Specify the connector options using either the `option()` or `options()` method. For more information, see [Setting Configuration Options for the Connector](#label-spark-options) (in this topic).
4. Specify one of the following options for the table data to be read:
   - `dbtable`: The name of the table to be read. All columns and records are retrieved (i.e. it is equivalent to `SELECT * FROM db_table`).
   - `query`: The exact query (SELECT statement) to run.

#### Usage Notes

- Currently, the connector does not support other types of queries (e.g. SHOW or DESC, or DML statements) when using DataFrames.
- There is an upper limit to the size of an individual row. For more details, see [Limits on Query Text Size](/user-guide/query-size-limits).

#### Performance Considerations

When transferring data between Snowflake and Spark, use the following methods to analyze/improve performance:

- Use the `net.snowflake.spark.snowflake.Utils.getLastSelect()` method to see the actual query issued when moving data from Snowflake to Spark.
- If you use the `filter` or `where` functionality of the Spark DataFrame, check that the respective filters are present in the issued SQL query. The Snowflake connector tries to translate all the
  filters requested by Spark to SQL.

  However, there are forms of filters that the Spark infrastructure today does not pass to the Snowflake connector. As a result, in some situations, a large number of unnecessary records are requested from
  Snowflake.
- If you need only a subset of columns, make sure the reflect the subset in the SQL query.
- In general, if the SQL query issued does not match what you expect based on the DataFrame operations, use the `query` option to provide the exact SQL syntax you want.

#### Examples

Read an entire table:

> Copy code
>
> ```
> val df: DataFrame = sqlContext.read
>     .format(SNOWFLAKE_SOURCE_NAME)
>     .options(sfOptions)
>     .option("dbtable", "t1")
>     .load()
> ```

Read the results of a query:

> Copy code
>
> ```
> val df: DataFrame = sqlContext.read
>     .format(SNOWFLAKE_SOURCE_NAME)
>     .options(sfOptions)
>     .option("query", "SELECT DEPT, SUM(SALARY) AS SUM_SALARY FROM T1")
>     .load()
> ```

### Moving Data from Spark to Snowflake

The steps for saving the contents of a DataFrame to a Snowflake table are similar to writing from Snowflake to Spark:

1. Use the `write()` method of the `DataFrame` to construct a `DataFrameWriter`.
2. Specify `SNOWFLAKE_SOURCE_NAME` using the `format()` method. For the definition, see [Using the Connector in Scala](#label-spark-data-source) (in this topic).
3. Specify the connector options using either the `option()` or `options()` method. For more information, see [Setting Configuration Options for the Connector](#label-spark-options) (in this topic).
4. Use the `dbtable` option to specify the table to which data is written.
5. Use the `mode()` method to specify the save mode for the content.

   For more information, see [SaveMode](https://spark.apache.org/docs/1.6.0/api/java/org/apache/spark/sql/SaveMode.html) (Spark documentation).

#### Examples

> Copy code
>
> ```
> df.write
>     .format(SNOWFLAKE_SOURCE_NAME)
>     .options(sfOptions)
>     .option("dbtable", "t2")
>     .mode(SaveMode.Overwrite)
>     .save()
> ```

### Exporting JSON from Spark to Snowflake

Spark DataFrames can contain JSON objects, serialized as strings. The following code provides an example of converting a regular DataFrame to a DataFrame containing JSON data:

> Copy code
>
> ```
> val rdd = myDataFrame.toJSON
> val schema = new StructType(Array(StructField("JSON", StringType)))
> val jsonDataFrame = sqlContext.createDataFrame(
>             rdd.map(s => Row(s)), schema)
> ```

Note that the resulting `jsonDataFrame` contains a single column of type `StringType`. As a result, when this DataFrame is exported to Snowflake with the common `SaveMode.Overwrite` mode, a new table in Snowflake is created with a single column of type `VARCHAR`.

To load `jsonDataFrame` into a `VARIANT` column:

1. Create a Snowflake table (connecting to Snowflake in Java using the Snowflake JDBC Driver). For explanations of the
   connection parameters used in the example, see [JDBC Driver connection parameter reference](/developer-guide/jdbc/jdbc-parameters).

   Copy code

   ```
   import java.sql.Connection;
   import java.sql.DriverManager;
   import java.sql.ResultSet;
   import java.sql.ResultSetMetaData;
   import java.sql.SQLException;
   import java.sql.Statement;
   import java.util.Properties;
   public class SnowflakeJDBCExample {
     public static void main(String[] args) throws Exception {
    String jdbcUrl = "jdbc:snowflake://myorganization-myaccount.snowflakecomputing.com/";

    Properties properties = new Properties();
    properties.put("user", "peter");
    properties.put("password", "test");
    properties.put("account", "myorganization-myaccount");
    properties.put("warehouse", "mywh");
    properties.put("db", "mydb");
    properties.put("schema", "public");

    // get connection
    System.out.println("Create JDBC connection");
    Connection connection = DriverManager.getConnection(jdbcUrl, properties);
    System.out.println("Done creating JDBC connection\n");
    // create statement
    System.out.println("Create JDBC statement");
    Statement statement = connection.createStatement();
    System.out.println("Done creating JDBC statement\n");
    // create a table
    System.out.println("Create my_variant_table table");
    statement.executeUpdate("create or replace table my_variant_table(json VARIANT)");
    statement.close();
    System.out.println("Done creating demo table\n");

    connection.close();
    System.out.println("Close connection\n");
     }
   }
   ```
2. Instead of using `SaveMode.Overwrite`, use `SaveMode.Append`, to reuse the existing table. When the string value representing JSON is loaded into Snowflake, because the target column is of type VARIANT, it is parsed as JSON. For example:

   Copy code

   ```
   df.write
    .format(SNOWFLAKE_SOURCE_NAME)
    .options(sfOptions)
    .option("dbtable", "my_variant_table")
    .mode(SaveMode.Append)
    .save()
   ```

### Executing DDL/DML SQL Statements

Use the `runQuery()` method of the `Utils` object to execute DDL/DML SQL statements, in addition to queries, for example:

Copy code

```
var sfOptions = Map(
    "sfURL" -> "<account_identifier>.snowflakecomputing.com",
    "sfUser" -> "<user_name>",
    "sfPassword" -> "<password>",
    "sfDatabase" -> "<database>",
    "sfSchema" -> "<schema>",
    "sfWarehouse" -> "<warehouse>"
    )
Utils.runQuery(sfOptions, "CREATE TABLE MY_TABLE(A INTEGER)")
```

where `sfOptions` is the parameters map used to read/write DataFrames.

The `runQuery` method returns only TRUE or FALSE. It is intended for statements that do not return a result set,
for example DDL statements like `CREATE TABLE` and DML statements like `INSERT`, `UPDATE`, and `DELETE`.
It is not useful for statements that return a result set, such as `SELECT` or `SHOW`.

### Working with Timestamps and Time Zones

Spark provides only one type of timestamp, equivalent to the Scala/Java Timestamp type. It is almost identical in behavior to the TIMESTAMP\_LTZ (local time zone) data type in Snowflake. As such, when transferring data between Spark and Snowflake, Snowflake recommends using the following approaches to preserve time correctly, relative to time zones:

- Use only the TIMESTAMP\_LTZ data type in Snowflake.

  Note

  The default timestamp data type mapping is TIMESTAMP\_NTZ (no time zone), so you must explicitly set the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) parameter to use TIMESTAMP\_LTZ.
- Set the Spark time zone to `UTC` and use this time zone in Snowflake (i.e. don’t set the `sfTimezone` option for the connector, and don’t explicitly set a time zone in Snowflake). In this scenario, TIMESTAMP\_LTZ and TIMESTAMP\_NTZ are effectively equivalent.

  To set the time zone, add the following line to your Spark code:

  Copy code

  ```
  java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"))
  ```

If you don’t implement either of these approaches, undesired time modifications might occur. For example, consider the following scenario:

- The time zone in Spark is set to `America/New_York`.
- The time zone in Snowflake is set to `Europe/Warsaw`, which can happen by either:

  - Setting `sfTimezone` to `Europe/Warsaw` for the connector.
  - Setting `sfTimezone` to `snowflake` for the connector and setting the [TIMEZONE](/sql-reference/parameters#label-timezone) session
    parameter in Snowflake to `Europe/Warsaw`.
- Both TIMESTAMP\_NTZ and TIMESTAMP\_LTZ are in use in Snowflake.

In this scenario:

1. If a value representing `12:00:00` in a TIMESTAMP\_NTZ column in Snowflake is sent to Spark, this value doesn’t carry any time zone information. Spark treats the value as `12:00:00` in New York.
2. If Spark sends this value `12:00:00` (in New York) back to Snowflake to be loaded into a TIMESTAMP\_LTZ column, it is automatically converted and loaded as `18:00:00` (for the Warsaw time zone).
3. If this value is then converted to TIMESTAMP\_NTZ in Snowflake, the user sees `18:00:00`, which is different from the original value, `12:00:00`.

To summarize, Snowflake recommends strictly following at least one of these rules:

- Use the same time zone, ideally `UTC`, for both Spark and Snowflake.
- Use only the TIMESTAMP\_LTZ data type for transferring data between Spark and Snowflake.

### Sample Scala Program

Important

This sample program assumes you are using version 2.2.0 (or higher) of the connector, which uses a Snowflake internal stage for storing temporary data and, therefore, does not require an S3 location for
storing temporary data. If you are using an earlier version, you must have an existing S3 location and include values for `tempdir`, `awsAccessKey`, `awsSecretKey` for `sfOptions`.
For more details, see [AWS Options for External Data Transfer](#label-s3-options) (in this topic).

The following Scala program provides a full use case for the Snowflake Connector for Spark. Before using the code, replace the following strings with the appropriate values, as described in
[Setting Configuration Options for the Connector](#label-spark-options) (in this topic):

- `<account_identifier>`: Your [account identifier](/user-guide/gen-conn-config).
- `<user_name>` , `<password>`: Login credentials for the Snowflake user.
- `<database>` , `<schema>` , `<warehouse>`: Defaults for the Snowflake session.

The sample Scala program uses basic authentication (i.e. username and password). If you wish to authenticate with OAuth, see [Using External OAuth](#using-external-oauth) (in this topic).

Copy code

```
import org.apache.spark.sql._

//
// Configure your Snowflake environment
//
var sfOptions = Map(
    "sfURL" -> "<account_identifier>.snowflakecomputing.com",
    "sfUser" -> "<user_name>",
    "sfPassword" -> "<password>",
    "sfDatabase" -> "<database>",
    "sfSchema" -> "<schema>",
    "sfWarehouse" -> "<warehouse>"
)

//
// Create a DataFrame from a Snowflake table
//
val df: DataFrame = sqlContext.read
    .format(SNOWFLAKE_SOURCE_NAME)
    .options(sfOptions)
    .option("dbtable", "t1")
    .load()

//
// DataFrames can also be populated via a SQL query
//
val df: DataFrame = sqlContext.read
    .format(SNOWFLAKE_SOURCE_NAME)
    .options(sfOptions)
    .option("query", "select c1, count(*) from t1 group by c1")
    .load()

//
// Join, augment, aggregate, etc. the data in Spark and then use the
// Data Source API to write the data back to a table in Snowflake
//
df.write
    .format(SNOWFLAKE_SOURCE_NAME)
    .options(sfOptions)
    .option("dbtable", "t2")
    .mode(SaveMode.Overwrite)
    .save()
```

## Using the Connector with Python

Using the connector with Python is very similar to the Scala usage.

We recommend using the `bin/pyspark` script included in the Spark distribution.

### Configuring the `pyspark` Script

The `pyspark` script must be configured similarly to the `spark-shell` script, using the `--packages` or `--jars` options. For example:

> Copy code
>
> ```
> bin/pyspark --packages net.snowflake:snowflake-jdbc:3.13.22,net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.3
> ```

Don’t forget to include the Snowflake Spark Connector and JDBC Connector .jar
files in your CLASSPATH environment variable.

For more information about configuring the `spark-shell` script, see [Step 4: Configure the Local Spark Cluster or Amazon EMR-hosted Spark Environment](/user-guide/spark-connector-install#label-spark-cluster-setup).

### Enabling/Disabling Pushdown in a Session

Version 2.1.0 (and higher) of the connector supports query pushdown, which can significantly improve performance by pushing query processing to Snowflake when Snowflake is the Spark data source.

By default, pushdown is enabled.

To disable pushdown within a Spark session for a given DataFrame:

1. After instantiating a `SparkSession` object, call the `SnowflakeConnectorUtils.disablePushdownSession` static
   method, passing in the `SparkSession` object. For example:

   Copy code

   ```
   sc._jvm.net.snowflake.spark.snowflake.SnowflakeConnectorUtils.disablePushdownSession(sc._jvm.org.apache.spark.sql.SparkSession.builder().getOrCreate())
   ```
2. Create a DataFrame with the [autopushdown](/user-guide/spark-connector-use#label-spark-options-autopushdown) option set to `off`. For example:

   Copy code

   ```
   df = spark.read.format(SNOWFLAKE_SOURCE_NAME) \
     .options(**sfOptions) \
     .option("query",  query) \
     .option("autopushdown", "off") \
     .load()
   ```

   Note that you can also set the `autopushdown` option in a `Dictionary` that you pass to the `options` method
   (e.g. in `sfOptions` in the example above).

To enable pushdown again after disabling it, call the `SnowflakeConnectorUtils.enablePushdownSession` static method
(passing in the `SparkSession` object), and create a DataFrame with `autopushdown` enabled.

### Sample Python Script

Important

This sample script assumes you are using version 2.2.0 (or higher) of the connector, which uses a Snowflake internal stage for storing temporary data and, therefore, does not require an S3 location for
storing this data. If you are using an earlier version, you must have an existing S3 location and include values for `tempdir`, `awsAccessKey`, `awsSecretKey` for `sfOptions`. For more
details, see [AWS Options for External Data Transfer](#label-s3-options) (in this topic).

Once the `pyspark` script has been configured, you can perform SQL queries and other operations. Here’s an example Python script that performs a simple SQL query. This script illustrates basic connector
usage. Most of the Scala examples in this document can be adapted with minimal effort/changes for use with Python.

The sample Python script uses basic authentication (i.e. username and password). If you wish to authenticate with OAuth, see [Using External OAuth](#using-external-oauth) (in this topic).

Copy code

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").appName("Simple App").getOrCreate()

# You might need to set these
sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", "<AWS_KEY>")
sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", "<AWS_SECRET>")

# Set options below
sfOptions = {
  "sfURL" : "<account_identifier>.snowflakecomputing.com",
  "sfUser" : "<user_name>",
  "sfPassword" : "<password>",
  "sfDatabase" : "<database>",
  "sfSchema" : "<schema>",
  "sfWarehouse" : "<warehouse>",
  "sfRole" : "Accountadmin"
}

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

df = spark.read.format(SNOWFLAKE_SOURCE_NAME) \
  .options(**sfOptions) \
  .option("query",  "select 1 as my_num union all select 2 as my_num") \
  .load()

df.show()
```

Tip

Note the usage of `sfOptions` and `SNOWFLAKE_SOURCE_NAME`. This simplifies the code and reduces the chance of errors.

For details about the supported options for `sfOptions`, see [Setting Configuration Options for the Connector](#label-spark-options) (in this topic).

## Data Type Mappings

The Spark Connector supports converting between many common data types.

### From Spark SQL to Snowflake

> | Spark Data Type | Snowflake Data Type |
> | --- | --- |
> | `ArrayType` | VARIANT |
> | `BinaryType` | Not supported |
> | `BooleanType` | BOOLEAN |
> | `ByteType` | INTEGER. Snowflake does not support the BYTE type. |
> | `DateType` | DATE |
> | `DecimalType` | DECIMAL |
> | `DoubleType` | DOUBLE |
> | `FloatType` | FLOAT |
> | `IntegerType` | INTEGER |
> | `LongType` | INTEGER |
> | `MapType` | VARIANT |
> | `ShortType` | INTEGER |
> | `StringType` | If length is specified, VARCHAR(N); otherwise, VARCHAR |
> | `StructType` | VARIANT |
> | `TimestampType` | TIMESTAMP |
>
> Expand
>
> Show lessSee more

### From Snowflake to Spark SQL

> | Snowflake Data Type | Spark Data Type |
> | --- | --- |
> | ARRAY | `StringType` |
> | BIGINT | `DecimalType(38, 0)` |
> | BINARY | Not supported |
> | BLOB | Not supported |
> | BOOLEAN | `BooleanType` |
> | CHAR | `StringType` |
> | CLOB | `StringType` |
> | DATE | `DateType` |
> | DECIMAL | `DecimalType` |
> | DOUBLE | `DoubleType` |
> | FLOAT | `DoubleType` |
> | INTEGER | `DecimalType(38, 0)` |
> | OBJECT | `StringType` |
> | TIMESTAMP | `TimestampType` |
> | TIME | `StringType` (Spark Connector Version 2.4.14 or later) |
> | VARIANT | `StringType` |
>
> Expand
>
> Show lessSee more

## Calling the DataFrame.show Method

If you are calling the `DataFrame.show` method and passing in a number that is less than the number of rows in the
DataFrame, construct a DataFrame that just contains the rows to show in a sorted order.

To do this:

1. Call the `sort` method first to return a DataFrame that contains sorted rows.
2. Call the `limit` method on that DataFrame to return a DataFrame that just contains the rows that you want to show.
3. Call the `show` method on the returned DataFrame.

For example, if you want to show 5 rows and want the results sorted by the column `my_col`:

> Copy code
>
> ```
> val dfWithRowsToShow = originalDf.sort("my_col").limit(5)
> dfWithRowsToShow.show(5)
> ```

Otherwise, if you call `show` to display a subset of rows in the DataFrame, different executions of the code might result in
different rows being shown.

## Setting Configuration Options for the Connector

The following sections list the options that you set to configure the behavior of the connector:

- [Required Connection Options](#label-spark-options-required-section)
- [Required Context Options](#label-spark-options-required-context-section)
- [Additional Context Options](#label-spark-options-additional-context-section)
- [Proxy Options](#label-spark-options-proxy-section)
- [Additional Options](#label-spark-options-additional-section)

To set these options, call the `.option(<key>, <value>)` or `.options(<map>)` method of the
[Spark DataframeReader](https://spark.apache.org/docs/1.6.0/api/java/org/apache/spark/sql/DataFrameReader.html) class.

Tip

To facilitate using the options, Snowflake recommends specifying the options in a single `Map` object and calling
`.options(<map>)` to set the options.

### Required Connection Options

The following options are required for connecting to Snowflake:

`sfUrl`
:   Specifies the *hostname* for your account in the following format:

    `account_identifier.snowflakecomputing.com`

    `account_identifier` is your [account identifier](/user-guide/gen-conn-config).

`sfUser`
:   Login name for the Snowflake user.

You must also use one of the following options to authenticate:

- `sfPassword`

  Password for the Snowflake user.
- `pem_private_key`

  Private key (in PEM format) for key pair authentication. For instructions, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
- `sfAuthenticator`

  Specifies the authentication method. Set the value to one of the following:

  - `oauth` to use [External OAuth](/user-guide/oauth-ext-overview) to authenticate to Snowflake. Using External OAuth requires setting the `sfToken` parameter.
  - `WORKLOAD_IDENTITY` (Recommended) to use [workload identity federation](/user-guide/workload-identity-federation) to authenticate to Snowflake. Using workload identity federation requires setting the `sfWorkloadIdentityProvider` parameter. For more information, see [Using workload identity federation (WIF)](#label-spark-auth-wif) (in this topic).

`sfToken`
:   (Required if using External OAuth) Set the value to your External OAuth access token.

    This connection parameter requires setting the `sfAuthenticator` parameter value to `oauth`.

    Default is none.

`sfWorkloadIdentityProvider`
:   (Required if using workload identity federation) Specifies the workload identity provider. Set the value to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on the platform where your workload runs.

    This connection parameter requires setting the `sfAuthenticator` parameter value to `WORKLOAD_IDENTITY`.

    Default is none.

### Required Context Options

The following options are required for setting the database and schema context for the session:

`sfDatabase`
:   The database to use for the session after connecting.

`sfSchema`
:   The schema to use for the session after connecting.

### Additional Context Options

The options listed in this section are not required.

`sfAccount`
:   Account identifier (e.g. `myorganization-myaccount`). This option is no longer required because the account identifier is specified in `sfUrl`. It is documented here only for backward compatibility.

`sfWarehouse`
:   The default virtual warehouse to use for the session after connecting.

`sfRole`
:   The default security role to use for the session after connecting.

### Proxy Options

The options listed in this section are not required.

`use_proxy`
:   Specifies whether the connector should use a proxy:

    - `true` specifies that the connector should use a proxy.
    - `false` specifies that the connector should not use a proxy.

    The default value is `false`.

`proxy_host`
:   (Required if `use_proxy` is `true`) Specifies the hostname of the proxy server to use.

`proxy_port`
:   (Required if `use_proxy` is `true`) Specifies the port number of the proxy server to use.

`proxy_protocol`
:   Specifies the protocol used to connect to the proxy server. You can specify one of the following values:

    - `http`
    - `https`

    The default value is `http`.

    This is only supported for Snowflake on AWS.

    This option was added in version 2.11.1 of the Spark Connector.

`proxy_user`
:   Specifies the user name for authenticating to the proxy server. Set this if the proxy server requires authentication.

    This is only supported for Snowflake on AWS.

`proxy_password`
:   Specifies the password of `proxy_user` for authenticating to the proxy server. Set this if the proxy server requires
    authentication.

    This is only supported for Snowflake on AWS.

`non_proxy_hosts`
:   Specifies the list of hosts that the connector should connect to directly, bypassing the proxy server.

    Separate the hostnames with a URL-escaped pipe symbol (`%7C`). You can also use an asterisk (`*`) as a wildcard

    This is only supported for Snowflake on AWS.

### Additional Options

The options listed in this section are not required.

`sfTimezone`
:   The time zone to be used by Snowflake when working with Spark. Note that the parameter only sets the time zone in Snowflake; the Spark environment remains unmodified. The supported values are:

    - `spark`: Use the time zone from Spark (default).
    - `snowflake`: Use the current time zone for Snowflake.
    - `sf_default`: Use the default time zone for the Snowflake user who is connecting.
    - `time_zone`: Use a specific time zone (e.g. `America/New_York`), if valid.

      For more information about the impact of setting this option, see [Working with Timestamps and Time Zones](#label-spark-timestamps) (in this topic).

`sfCompress`
:   If set to `on` (default), the data passed between Snowflake and Spark is compressed.

`s3MaxFileSize`
:   The size of the file used when moving data from Snowflake to Spark. The default is 10MB.

`preactions`
:   A semicolon-separated list of SQL commands that are executed before data is transferred between Spark and Snowflake.

    If a SQL command contains `%s`, the `%s` is replaced with the table name referenced for the operation.

`postactions`
:   A semicolon-separated list of SQL commands that are executed after data is transferred between Spark and Snowflake.

    If a SQL command contains `%s`, it is replaced with the table name referenced for the operation.

`truncate_columns`
:   If set to `on` (default), a COPY command automatically truncates text strings that exceed the target column length. If set to `off`, the command produces an error if a loaded string exceeds the target column length.

`truncate_table`
:   This parameter controls whether Snowflake retains the schema of a Snowflake
    target table when overwriting that table.

    By default, when a target table in Snowflake is overwritten, the schema of
    that target table is also overwritten; the new schema is based on the schema
    of the source table (the Spark dataframe).

    However, sometimes the schema of the source is not ideal. For example,
    a user might want a Snowflake target table to be able to store FLOAT
    values in the future even though the data type of the initial source column
    is INTEGER. In that case, the Snowflake table’s schema should not be
    overwritten; the Snowflake table should merely be truncated and then
    reused with its current schema.

    The possible values of this parameter are:

    - `on`
    - `off`

    If this parameter is `on`, the original schema of the target table is kept.
    If this parameter is `off`, then the old schema of the table is ignored,
    and a new schema is generated based on the schema of the source.

    This parameter is optional.

    The default value of this parameter is `off` (i.e. by default
    the original table schema is overwritten).

    For details about mapping Spark data types to Snowflake data types (and
    vice versa), see: [Data Type Mappings](#label-spark-data-type-mappings) (in this topic).

`continue_on_error`
:   This variable controls whether the COPY command aborts if the user enters
    invalid data (for example, invalid JSON format for a variant data type column).

    The possible values are:

    - `on`
    - `off`

    The value `on` means continue even if an error occurs. The value `off`
    means abort if an error is hit.

    This parameter is optional.

    The default value of this parameter is `off`.

    Turning this option on is not recommended. If any errors are reported
    while COPYing into Snowflake with the Spark connector, then this is likely
    to result in missing data.

    Note

    If rows are rejected or missing, and those rows are not clearly faulty
    in the input source, please report it to Snowflake.

`usestagingtable`
:   This parameter controls whether data loading uses a staging table.

    A staging table is a normal table (with a temporary name) that is created
    by the connector; if the data loading operation is successful, the original
    target table is dropped and the staging table is renamed to the original
    target table’s name. If the data loading operation fails, the staging table
    is dropped and the target table is left with the data that it had
    immediately prior to the operation. Thus the staging table allows the original
    target table data to be retained if the operation fails. For safety, Snowflake
    strongly recommends using a staging table in most circumstances.

    In order for the connector to create a staging table, the user executing the
    COPY via the Spark connector must have sufficient privileges to
    create a table. Direct loading (i.e. loading without using a staging table)
    is useful if the user does not have permission to create a table.

    The possible values of this parameter are:

    - `on`
    - `off`

    If the parameter is `on`, a staging table is used. If this parameter
    is `off`, then the data is loaded directly into the target table.

    This parameter is optional.

    The default value of this parameter is `on` (i.e. use a staging table).

`autopushdown`
:   This parameter controls whether automatic query pushdown is enabled.

    If pushdown is enabled, then when a query is run on Spark, if part of the
    query can be “pushed down” to the Snowflake server, it is pushed down.
    This improves performance of some queries.

    This parameter is optional.

    The default value is `on` if the connector is plugged into a compatible
    version of Spark. Otherwise, the default value is `off`.

    If the connector is plugged into a different version of Spark than the
    connector is intended for (e.g. if version 3.2 of the connector is
    plugged into version 3.3 of Spark), then auto-pushdown is disabled
    even if this parameter is set to `on`.

`purge`
:   If this is set to `on`, then the connector deletes temporary files created
    when transferring from Spark to Snowflake via external data transfer.
    If this parameter is set to `off`, then those files are not automatically
    deleted by the connector.

    Purging works only for transfers from Spark to Snowflake, not for transfers
    from Snowflake to Spark.

    The possible values are

    - `on`
    - `off`

    The default value is `off`.

`columnmap`
:   This parameter is useful when writing data from Spark to Snowflake
    and the column names in the Snowflake table do not match the column names
    in the Spark table. You can create a map that indicates which Spark
    source column corresponds to each Snowflake destination column.

    The parameter is a single string literal, in the form of:

    > `"Map(col_2 -> col_b, col_3 -> col_a)"`

    For example, consider the following scenario:

    - A Dataframe named `df` in Spark has three columns:
      `col_1` , `col_2` , `col_3`
    - A table named `tb` in Snowflake has two columns:
      `col_a` , `col_b`
    - You wish to copy the following values:

      - From `df.col_2` to `tb.col_b`.
      - From `df.col_3` to `tb.col_a`.

    The value of the `columnmap` parameter would be:

    > `Map(col_2 -> col_b, col_3 -> col_a)`

    You can generate this value by executing the following Scala code:

    > `Map("col_2"->"col_b","col_3"->"col_a").toString()`

    The default value of this parameter is null. In other words, by default,
    column names in the source and destination tables should match.

    This parameter is used only when writing from Spark to Snowflake;
    it does not apply when writing from Snowflake to Spark.

`keep_column_case`
:   When writing a table from Spark to Snowflake, the Spark connector defaults
    to shifting the letters in column names to uppercase, unless the column
    names are in double quotes.

    When writing a table from Snowflake to Spark, the Spark connector defaults
    to adding double quotes around any column name that contains any characters
    except uppercase letters, underscores, and digits.

    If you set keep\_column\_case to `on`, then the Spark connector will not
    make these changes.

    The possible values are:

    - `on`
    - `off`

    The default value is `off`.

`column_mapping`
:   The connector must map columns from the Spark data frame to the Snowflake table. This can be done based on column
    names (regardless of order), or based on column order (i.e. the first column in the data frame is mapped to the first
    column in the table, regardless of column name).

    By default, the mapping is done based on order. You can override that by setting this parameter to `name`,
    which tells the connector to map columns based on column names. (The name mapping is case-insensitive.)

    The possible values of this parameter are:

    - `order`
    - `name`

    The default value is `order`.

`column_mismatch_behavior`
:   This parameter applies only when the `column_mapping` parameter is set to `name`.

    If the column names in the Spark data frame and the Snowflake table do not match, then:

    - If `column_mismatch_behavior` is `error`, then the Spark Connector reports an error.
    - If `column_mismatch_behavior` is `ignore`, then the Spark Connector ignores the error.
      - The driver discards any column in the Spark data frame that does not have a corresponding column in the
        Snowflake table.
      - The driver inserts NULLs into any column in the Snowflake table that does not have a corresponding column
        in the Spark data frame.

    Potential errors include:

    - The Spark data frame could contain columns that are identical except for case (uppercase/lowercase). Because
      column name mapping is case-insensitive, it is not possible to determine the correct mapping from the data frame
      to the table.
    - The Snowflake table could contain columns that are identical except for case (uppercase/lowercase). Because
      column name mapping is case-insensitive, it is not possible to determine the correct mapping from the data frame
      to the table.
    - The Spark data frame and the Snowflake table might have no column names in common. In theory, the Spark Connector
      could insert NULLs into every column of every row, but this is usually pointless, so the connector throws an
      error even if the `column_mismatch_behavior` is set to `ignore`.

    The possible values of this parameter are:

    - `error`
    - `ignore`

    The default value is `error`.

`time_output_format`
:   This parameter allows the user to specify the format for `TIME` data returned.

    The possible values of this parameter are the possible values for time formats specified at [Time formats](/sql-reference/date-time-input-output#label-time-formats).

    This parameter affects only output, not input.

`timestamp_ntz_output_format`, `timestamp_ltz_output_format`, `timestamp_tz_output_format`
:   These options specify the output format for timestamp values. The default values of these options are:

    | Configuration Option | Default Value |
    | --- | --- |
    | `timestamp_ntz_output_format` | `"YYYY-MM-DD HH24:MI:SS.FF3"` |
    | `timestamp_ltz_output_format` | `"TZHTZM YYYY-MM-DD HH24:MI:SS.FF3"` |
    | `timestamp_tz_output_format` | `"TZHTZM YYYY-MM-DD HH24:MI:SS.FF3"` |

    Expand

    Show lessSee more

    If these options are set to `"sf_current"`, the connector uses the formats specified for the session.

`partition_size_in_mb`
:   This parameter is used when the query result set is very large and needs to be split into multiple DataFrame
    partitions. This parameter specifies the recommended uncompressed size for each DataFrame partition. To reduce the
    number of partitions, make this size larger.

    This size is used as a recommended size; the actual size of partitions could be smaller or larger.

    This option applies only when the [use\_copy\_unload](/user-guide/spark-connector-use#label-use-copy-unload) parameter is FALSE.

    This parameter is optional.

    The default value is `100` (MB).

`use_copy_unload`
:   If this is `FALSE`, Snowflake uses the Arrow data format when SELECTing data. If this is set to `TRUE`,
    then Snowflake reverts to the old behavior of using the `COPY UNLOAD` command to transmit selected data.

    This parameter is optional.

    The default value is `FALSE`.

`treat_decimal_as_long`
:   If `TRUE`, configures the Spark Connector to return `Long` values (rather than `BigDecimal` values) for queries
    that return the type `Decimal(precision, 0)`.

    The default value is `FALSE`.

    This option was added in version 2.11.1 of the Spark Connector.

`s3_stage_vpce_dns_name`
:   Specifies the DNS name of your VPC Endpoint for access to internal stages.

    This option was added in version 2.11.1 of the Spark Connector.

`support_share_connection`
:   If `FALSE`, configures the Spark Connector to create a new JDBC connection for each job or action that uses the same Spark
    Connector options to access Snowflake.

    The default value is `TRUE`, which means that the different jobs and actions share the same JDBC connection if they use the
    same Spark Connector options to access Snowflake.

    If you need to enable or disable this setting programmatically, use the following global static functions:

    - `SparkConnectorContext.disableSharedConnection()`
    - `SparkConnectorContext.enableSharingJDBCConnection()`

    Note

    In the following special cases, the Spark Connector does not use a shared JDBC connection:

    - If preactions or postactions are set, and those preactions or postactions are not CREATE TABLE, DROP TABLE, or MERGE INTO,
      the Spark Connector does not use the shared connection.
    - Utility functions in Utils such as `Utils.runQuery()` and `Utils.getJDBCConnection()` do not use the shared
      connection.

    This option was added in version 2.11.2 of the Spark Connector.

`force_skip_pre_post_action_check_for_shared_session`
:   If `TRUE`, configures the Spark Connector to disable the validation of preactions and postactions for session sharing.

    The default value is `FALSE`.

    Important

    Before setting this option, make sure that the queries in preactions and postactions don’t affect the session settings.
    Otherwise, you may encounter issues with results.

    This option was added in version 2.11.3 of the Spark Connector.

### Using Key Pair Authentication & Key Pair Rotation

The Spark connector supports key pair authentication and key rotation.

1. To start, complete the initial configuration for key pair authentication as shown in [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
2. Send an unencrypted copy of the private key using the `pem_private_key` connection option.

Attention

For security reasons, rather than hard-coding the `pem_private_key` in your application, you should set the parameter dynamically after reading the key from a secure source. If the key is encrypted, then decrypt it and send the decrypted version.

In the Python example, note that the `pem_private_key` file, `rsa_key.p8`, is:

- Being read directly from a password-protected file, using the environment variable `PRIVATE_KEY_PASSPHRASE`.
- Using the expression `pkb` in the `sfOptions` string.

To connect, you can save the Python example to a file (i.e. `<file.py>`) and then execute the following command:

Copy code

```
spark-submit --packages net.snowflake:snowflake-jdbc:3.13.22,net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.3 <file.py>
```

**Python**

Copy code

```
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import re
import os

with open("<path>/rsa_key.p8", "rb") as key_file:
  p_key = serialization.load_pem_private_key(
    key_file.read(),
    password = os.environ['PRIVATE_KEY_PASSPHRASE'].encode(),
    backend = default_backend()
    )

pkb = p_key.private_bytes(
  encoding = serialization.Encoding.PEM,
  format = serialization.PrivateFormat.PKCS8,
  encryption_algorithm = serialization.NoEncryption()
  )

pkb = pkb.decode("UTF-8")
pkb = re.sub("-*(BEGIN|END) PRIVATE KEY-*\n","",pkb).replace("\n","")

sc = SparkContext("local", "Simple App")
spark = SQLContext(sc)
spark_conf = SparkConf().setMaster('local').setAppName('Simple App')

sfOptions = {
  "sfURL" : "<account_identifier>.snowflakecomputing.com",
  "sfUser" : "<user_name>",
  "pem_private_key" : pkb,
  "sfDatabase" : "<database>",
  "sfSchema" : "schema",
  "sfWarehouse" : "<warehouse>"
}

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

df = spark.read.format(SNOWFLAKE_SOURCE_NAME) \
    .options(**sfOptions) \
    .option("query", "COLORS") \
    .load()

df.show()
```

### Using External OAuth

Starting with Spark Connector version 2.7.0, you can use [External OAuth](/user-guide/oauth-ext-overview) to authenticate to Snowflake using either the sample Scala program or the sample Python script.

Before using External OAuth and the Spark Connector to authenticate to Snowflake, configure an External OAuth security integration for one of the supported External OAuth authorization servers or an External OAuth [custom client](/user-guide/oauth-ext-custom).

In the Scala and Python examples, note the replacement of the `sfPassword` parameter with the `sfAuthenticator` and `sfToken` parameters.

**Scala:**

> Copy code
>
> ```
> // spark connector version
>
> val SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
> import net.snowflake.spark.snowflake2.Utils.SNOWFLAKE_SOURCE_NAME
> import org.apache.spark.sql.DataFrame
>
> var sfOptions = Map(
>     "sfURL" -> "<account_identifier>.snowflakecomputing.com",
>     "sfUser" -> "<username>",
>     "sfAuthenticator" -> "oauth",
>     "sfToken" -> "<external_oauth_access_token>",
>     "sfDatabase" -> "<database>",
>     "sfSchema" -> "<schema>",
>     "sfWarehouse" -> "<warehouse>"
> )
>
> //
> // Create a DataFrame from a Snowflake table
> //
> val df: DataFrame = sqlContext.read
>     .format(SNOWFLAKE_SOURCE_NAME)
>     .options(sfOptions)
>     .option("dbtable", "region")
>     .load()
>
> //
> // Join, augment, aggregate, etc. the data in Spark and then use the
> // Data Source API to write the data back to a table in Snowflake
> //
> df.write
>     .format(SNOWFLAKE_SOURCE_NAME)
>     .options(sfOptions)
>     .option("dbtable", "t2")
>     .mode(SaveMode.Overwrite)
>     .save()
> ```

**Python:**

> Copy code
>
> ```
> from pyspark import SparkConf, SparkContext
> from pyspark.sql import SQLContext
> from pyspark.sql.types import *
>
> sc = SparkContext("local", "Simple App")
> spark = SQLContext(sc)
> spark_conf = SparkConf().setMaster('local').setAppName('<APP_NAME>')
>
> # You might need to set these
> sc._jsc.hadoopConfiguration().set("fs.s3n.awsAccessKeyId", "<AWS_KEY>")
> sc._jsc.hadoopConfiguration().set("fs.s3n.awsSecretAccessKey", "<AWS_SECRET>")
>
> # Set options below
> sfOptions = {
>   "sfURL" : "<account_identifier>.snowflakecomputing.com",
>   "sfUser" : "<user_name>",
>   "sfAuthenticator" : "oauth",
>   "sfToken" : "<external_oauth_access_token>",
>   "sfDatabase" : "<database>",
>   "sfSchema" : "<schema>",
>   "sfWarehouse" : "<warehouse>"
> }
>
> SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"
>
> df = spark.read.format(SNOWFLAKE_SOURCE_NAME) \
>   .options(**sfOptions) \
>   .option("query",  "select 1 as my_num union all select 2 as my_num") \
>   .load()
>
> df.show()
> ```

### Using workload identity federation (WIF)

[Workload identity federation](/user-guide/workload-identity-federation) provides a service-to-service authentication method for Snowflake. This method enables applications, services, or containers to authenticate with Snowflake by leveraging their cloud provider’s native identity system, such as AWS IAM, Microsoft Entra ID, or Google Cloud service accounts. This approach eliminates the need for managing long-lived credentials and simplifies credential acquisition compared to other methods like External OAuth. Snowflake connectors are designed to automatically obtain short-lived credentials from the platform’s identity provider.

Starting with Spark Connector version 3.1.7, you can use workload identity federation to authenticate to Snowflake. This version of the connector is certified with the Snowflake JDBC driver 3.28.0.

To enable the workload identity federation authenticator, do the following:

1. Set the `sfAuthenticator` connection parameter to `WORKLOAD_IDENTITY`.
2. Set the `sfWorkloadIdentityProvider` connection parameter to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on your platform.
3. For OpenID Connect (OIDC), specify the `sfToken` connection parameter.

### AWS Options for External Data Transfer

These options are used to specify the Amazon S3 location where temporary data is stored and provide authentication details for accessing the location. They are required only if you are doing an external data transfer. External data transfers are required if either of the following is true:

- You are using version 2.1.x or lower of the Spark Connector (which
  does not support internal transfers), or
- Your transfer is likely to take 36 hours or more (internal transfers
  use temporary credentials that expire after 36 hours).

`tempDir`
:   The S3 location where intermediate data is stored (e.g. `s3n://xy12345-bucket/spark-snowflake-tmp/`).

    If `tempDir` is specified, you must also specify either:

    - `awsAccessKey` , `awsSecretKey`   
       or
    - `temporary_aws_access_key_id` , `temporary_aws_secret_access_key`, `temporary_aws_session_token`

`awsAccessKey` , `awsSecretKey`
:   These are standard AWS credentials that allow access to the location
    specified in `tempDir`. Note that both of these options must be set
    together.

    If they are set, they can be retrieved from the existing `SparkContext` object.

    If you specify these variables, you must also specify `tempDir`.

    These credentials should also be set for the Hadoop cluster.

`temporary_aws_access_key_id` , `temporary_aws_secret_access_key`, `temporary_aws_session_token`
:   These are temporary AWS credentials that allow access to the location
    specified in `tempDir`. Note that all three of these options must be
    set together.

    Also, if these options are set, they take precedence over the `awsAccessKey` and `awsSecretKey` options.

    If you specify `temporary_aws_access_key_id` , `temporary_aws_secret_access_key`, and `temporary_aws_session_token` , you must also specify `tempDir`. Otherwise, these parameters are ignored.

`check_bucket_configuration`
:   If set to `on` (default), the connector checks if the bucket used for data transfer has a lifecycle policy configured (see [Preparing an AWS External S3 Bucket](/user-guide/spark-connector-install#label-spark-s3-setup) for more information). If there is no lifecycle
    policy present, a warning is logged.

    Disabling this option (by setting to `off`) skips this check. This can be useful if a user can access the bucket data operations, but not the bucket lifecycle policies. Disabling the option can also
    speed up query execution times slightly.

For details, see [Authenticating S3 for Data Exchange](#label-spark-auth) (in this topic).

### Azure Options for External Data Transfer

This section describes the parameters that apply to Azure Blob storage when
doing external data transfers. External data transfers are required if either
of the following is true:

- You are using version 2.1.x or lower of the Spark Connector (which
  does not support internal transfers), or
- Your transfer is likely to take 36 hours or more (internal transfers
  use temporary credentials that expire after 36 hours).

When using an external transfer with Azure Blob storage, you specify the location of the
Azure container and the SAS (shared-access signature) for that container using
the parameters described below.

`tempDir`
:   The Azure Blob storage container where intermediate data is stored.
    This is in the form of a URL, for example:

    > `wasb://<azure_container>@<azure_account>.<azure_endpoint>/`

`temporary_azure_sas_token`
:   Specify the SAS token for Azure Blob storage.

For details, see [Authenticating Azure for Data Exchange](#label-spark-azure-auth) (in this topic).

#### Specifying Azure Information for Temporary Storage in Spark

When using Azure Blob storage to provide temporary storage to transfer data
between Spark and Snowflake, you must provide Spark, as well as the Snowflake Spark Connector,
with the location and credentials for the temporary storage.

To provide Spark with the temporary storage location, execute commands similar to the following
on your Spark cluster:

> Copy code
>
> ```
> sc.hadoopConfiguration.set("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
> sc.hadoopConfiguration.set("fs.AbstractFileSystem.wasb.impl", "org.apache.hadoop.fs.azure.Wasb")
> sc.hadoopConfiguration.set("fs.azure.sas.<container>.<account>.<azure_endpoint>", <azure_sas>)
> ```

Note that the last command contains the following variables:

- `<container>` and `<account>`: These are the container and account name for your Azure deployment.
- `<azure_endpoint>`: This is the endpoint for your Azure deployment location. For example, if you are using an Azure US deployment, the endpoint is likely to be `blob.core.windows.net`.
- `<azure_sas>`: This is the Shared Access Signature security token.

Replace each of these variables with the proper information for your Azure Blob Storage account.

## Passing Snowflake Session Parameters as Options for the Connector

The Snowflake Connector for Spark supports sending arbitrary session-level parameters to Snowflake (see [Session parameters](/sql-reference/parameters#label-session-parameters) for more info). This can be achieved by adding a
`("<key>" -> "<value>")` pair to the `options` object, where `<key>` is the session parameter name and `<value>` is the value.

Note

The `<value>` should be a string enclosed in double quotes, even for parameters that accept numbers or Boolean values (e.g. `"1"` or `"true"`).

For example, the following code sample passes the [USE\_CACHED\_RESULT](/sql-reference/parameters#label-use-cached-result) session parameter with a value of `"false"`, which disables using the results of previously-executed queries:

Copy code

```
// ... assuming sfOptions contains Snowflake connector options

// Add to the options request to keep connection alive
sfOptions += ("USE_CACHED_RESULT" -> "false")

// ... now use sfOptions with the .options() method
```

## Security Considerations

Customers should ensure that in a multi-node Spark system, communications between the nodes are secure. The Spark
master sends Snowflake credentials to Spark workers so that those workers can access Snowflake stages. If
communications between the Spark master and Spark workers are not secure, the credentials could be read by an
unauthorized third party.

## Authenticating S3 for Data Exchange

This section describes how to authenticate when using S3 for data exchange.

This task is required only in either of the following circumstances:

- The Snowflake Connector for Spark version is 2.1.x (or lower). Starting with v2.2.0, the connector uses a Snowflake internal temporary stage for data exchange. If you are not currently using version 2.2.0 (or higher) of the connector, Snowflake strongly recommends upgrading to the latest version.
- The Snowflake Connector for Spark version is 2.2.0 (or higher), but your jobs regularly exceed 36 hours in length. This is the maximum duration for the AWS token used by the connector to access the internal stage for data exchange.

If you are using an older version of the connector, you need to prepare an S3 location that the connector can use to exchange data between Snowflake and Spark.

To allow access to the S3 bucket/directory used to exchange data between Spark and Snowflake (as specified for `tempDir`), two authentication methods are supported:

- Permanent AWS credentials (also used to configure Hadoop/Spark authentication for accessing S3)
- Temporary AWS credentials

### Using Permanent AWS Credentials

This is the standard AWS authentication method. It requires a pair of `awsAccessKey` and `awsSecretKey` values.

Note

These values should also be used to configure Hadoop/Spark for accessing S3. For more information, including examples, see [Authenticating Hadoop/Spark Using S3A or S3N](#label-spark-s3a-s3n) (in this topic).

For example:

> Copy code
>
> ```
> sc.hadoopConfiguration.set("fs.s3n.awsAccessKeyId", "<access_key>")
> sc.hadoopConfiguration.set("fs.s3n.awsSecretAccessKey", "<secret_key>")
>
> // Then, configure your Snowflake environment
> //
> var sfOptions = Map(
>     "sfURL" -> "<account_identifier>.snowflakecomputing.com",
>     "sfUser" -> "<user_name>",
>     "sfPassword" -> "<password>",
>     "sfDatabase" -> "<database>",
>     "sfSchema" -> "<schema>",
>     "sfWarehouse" -> "<warehouse>",
>     "awsAccessKey" -> sc.hadoopConfiguration.get("fs.s3n.awsAccessKeyId"),
>     "awsSecretKey" -> sc.hadoopConfiguration.get("fs.s3n.awsSecretAccessKey"),
>     "tempdir" -> "s3n://<temp-bucket-name>"
> )
> ```

For details about the options supported by `sfOptions`, see [AWS Options for External Data Transfer](#label-s3-options) (in this topic).

#### Authenticating Hadoop/Spark Using S3A or S3N

Hadoop/Spark ecosystems support 2 URI schemes for [accessing S3](https://wiki.apache.org/hadoop/AmazonS3/):

`s3a://`
:   **New, recommended method (for Hadoop 2.7 and higher)**

    To use this method, modify the Scala examples in this topic to add the following Hadoop configuration options:

    > Copy code
    >
    > ```
    > val hadoopConf = sc.hadoopConfiguration
    > hadoopConf.set("fs.s3a.access.key", <accessKey>)
    > hadoopConf.set("fs.s3a.secret.key", <secretKey>)
    > ```

    Make sure the `tempdir` option uses `s3a://` as well.

`s3n://`
:   **Older method (for Hadoop 2.6 and lower)**

    In some systems, it is necessary to specify it explicitly as shown in the following Scala example:

    > Copy code
    >
    > ```
    > val hadoopConf = sc.hadoopConfiguration
    > hadoopConf.set("fs.s3.impl", "org.apache.hadoop.fs.s3native.NativeS3FileSystem")
    > hadoopConf.set("fs.s3.awsAccessKeyId", <accessKey>)
    > hadoopConf.set("fs.s3.awsSecretAccessKey", <secretKey>)
    > ```

### Using Temporary AWS Credentials

This method uses the `temporary_aws_access_key_id`, `temporary_aws_secret_access_key`, and `temporary_aws_session_token` configuration options for the connector.

This method allows additional security by providing Snowflake with only temporary access to the S3 bucket/directory used for data exchange.

Note

Temporary credentials can only be used to configure the S3 authentication for the connector; they cannot be used to configure Hadoop/Spark authentication.

Also, if you provide temporary credentials, they take precedence over any permanent credentials that have been provided.

The following Scala code sample provides an example of authenticating using temporary credentials:

> Copy code
>
> ```
> import com.amazonaws.services.securitytoken.AWSSecurityTokenServiceClient
> import com.amazonaws.services.securitytoken.model.GetSessionTokenRequest
>
> import net.snowflake.spark.snowflake.Parameters
>
> // ...
>
> val sts_client = new AWSSecurityTokenServiceClient()
> val session_token_request = new GetSessionTokenRequest()
>
> // Set the token duration to 2 hours.
>
> session_token_request.setDurationSeconds(7200)
> val session_token_result = sts_client.getSessionToken(session_token_request)
> val session_creds = session_token_result.getCredentials()
>
> // Create a new set of Snowflake connector options, based on the existing
> // sfOptions definition, with additional temporary credential options that override
> // the credential options in sfOptions.
> // Note that constants from Parameters are used to guarantee correct
> // key names, but literal values, such as temporary_aws_access_key_id are, of course,
> // also allowed.
>
> var sfOptions2 = collection.mutable.Map[String, String]() ++= sfOptions
> sfOptions2 += (Parameters.PARAM_TEMP_KEY_ID -> session_creds.getAccessKeyId())
> sfOptions2 += (Parameters.PARAM_TEMP_KEY_SECRET -> session_creds.getSecretAccessKey())
> sfOptions2 += (Parameters.PARAM_TEMP_SESSION_TOKEN -> session_creds.getSessionToken())
> ```

`sfOptions2` can now be used with the `options()` DataFrame method.

## Authenticating Azure for Data Exchange

This section describes how to authenticate when using Azure Blob storage for data exchange.

Authenticating this way is required only in either of the following circumstances:

- The Snowflake Connector for Spark version is 2.1.x (or lower). Starting with
  v2.2.0, the connector uses a Snowflake internal temporary stage for data
  exchange. If you are not currently using version 2.2.0 (or higher) of the
  connector, Snowflake strongly recommends upgrading to the latest version.
- The Snowflake Connector for Spark version is 2.2.0 (or higher), but your
  jobs regularly exceed 36 hours in length. This is the maximum duration for
  the Azure token used by the connector to access the internal stage for
  data exchange.

You need to prepare an Azure Blob storage container that the connector can use to
exchange data between Snowflake and Spark.

### Using Azure Credentials

This is the standard Azure Blob storage authentication method. It requires a pair of
values: `tempDir` (a URL) and `temporary_azure_sas_token` values.

Note

These values should also be used to configure Hadoop/Spark for accessing Azure Blob storage. For more information, including examples, see [Authenticating Hadoop/Spark Using Azure](#label-spark-azure) (in this topic).

For example:

> Copy code
>
> ```
> sc.hadoopConfiguration.set("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
> sc.hadoopConfiguration.set("fs.AbstractFileSystem.wasb.impl", "org.apache.hadoop.fs.azure.Wasb")
> sc.hadoopConfiguration.set("fs.azure.sas.<container>.<account>.<azure_endpoint>", <azure_sas>)
>
> // Then, configure your Snowflake environment
> //
> val sfOptions = Map(
>   "sfURL" -> "<account_identifier>.snowflakecomputing.com",
>   "sfUser" -> "<user_name>",
>   "sfPassword" -> "<password>",
>   "sfDatabase" -> "<database_name>",
>   "sfSchema" -> "<schema_name>",
>   "sfWarehouse" -> "<warehouse_name>",
>   "sfCompress" -> "on",
>   "sfSSL" -> "on",
>   "tempdir" -> "wasb://<azure_container>@<azure_account>.<Azure_endpoint>/",
>   "temporary_azure_sas_token" -> "<azure_sas>"
> )
> ```

For details about the options supported by `sfOptions`, see [Azure Options for External Data Transfer](#label-azure-options) (in this topic).

#### Authenticating Hadoop/Spark Using Azure

To use this method, modify the Scala examples in this topic to add the following Hadoop configuration options:

> Copy code
>
> ```
> val hadoopConf = sc.hadoopConfiguration
> sc.hadoopConfiguration.set("fs.azure", "org.apache.hadoop.fs.azure.NativeAzureFileSystem")
> sc.hadoopConfiguration.set("fs.AbstractFileSystem.wasb.impl", "org.apache.hadoop.fs.azure.Wasb")
> sc.hadoopConfiguration.set("fs.azure.sas.<container>.<account>.<azure_endpoint>", <azure_sas>)
> ```

Make sure the `tempdir` option uses `wasb://` as well.

## Authenticating Through a Browser is Not Supported

When using the Spark Connector, it is impractical to use any form of authentication that would open a browser
window to ask the user for credentials. The window would not necessarily appear on the client machine. Therefore, the
Spark Connector does not support any type of authentication, including MFA (Multi-Factor Authentication) or SSO
(Single Sign-On), that would invoke a browser window.
