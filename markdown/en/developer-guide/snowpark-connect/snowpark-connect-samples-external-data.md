# Samples: External data sources with Snowpark Connect for Spark

This page provides end-to-end ETL examples that ingest data from external cloud storage into
Snowflake tables using the standard Spark API.

These examples assume you’ve completed the
[local IDE setup](/developer-guide/snowpark-connect/snowpark-connect-local-ide) and have a
`~/.snowflake/connections.toml` entry configured. Each external source requires appropriate
credentials or a storage integration, as shown in the inline comments.

## Example 1: AWS S3 (CSV to table)

Ingest pipe-delimited CSV files from an S3 bucket, apply data-quality rules, and land the result
in a Snowflake table. Snowpark Connect for Spark transparently creates a temporary external Snowflake stage
pointing at the S3 bucket so the standard `spark.read.csv()` API works unchanged.

PythonJavaScala

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from pyspark.sql.types import (
    DecimalType, LongType, StringType, StructField, StructType,
)
from pyspark.sql.functions import (
    coalesce, col, current_timestamp, lit, to_date, trim, upper, when,
)

spark = init_spark_session()

spark.conf.set("spark.hadoop.fs.s3a.access.key", "YOUR_ACCESS_KEY")
spark.conf.set("spark.hadoop.fs.s3a.secret.key", "YOUR_SECRET_KEY")
spark.conf.set("spark.hadoop.fs.s3a.session.token", "YOUR_SESSION_TOKEN")

orders_schema = StructType([
    StructField("order_id", LongType(), False),
    StructField("customer_name", StringType(), True),
    StructField("amount", DecimalType(10, 2), True),
    StructField("order_date", StringType(), True),
    StructField("region", StringType(), True),
])

raw = (
    spark.read.format("csv")
    .option("header", "true")
    .option("sep", "|")
    .option("quote", '"')
    .option("escape", '"')
    .option("nullValue", "NA")
    .option("multiLine", "true")
    .schema(orders_schema)
    .load("s3://your-bucket/landing/orders/")
)

cleaned = (
    raw
    .withColumn("region", upper(trim(col("region"))))
    .withColumn("customer_name", coalesce(col("customer_name"), lit("UNKNOWN")))
    .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
    .withColumn("amount", when(col("amount") <= 0, None).otherwise(col("amount")))
    .filter(col("amount").isNotNull())
    .filter(col("region").isNotNull())
    .dropDuplicates(["order_id"])
    .withColumn("loaded_at", current_timestamp())
)

cleaned.show(truncate=False)

cleaned.write.mode("overwrite").saveAsTable("orders_curated")

result = spark.table("orders_curated")
print(f"orders_curated row count: {result.count()}")
result.show(truncate=False)

spark.sql("DROP TABLE IF EXISTS orders_curated")
spark.stop()
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.types.*;
import static org.apache.spark.sql.functions.*;

public class S3CsvToTable {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("S3 CSV to Table").getOrCreate();

        spark.conf().set("spark.hadoop.fs.s3a.access.key", "YOUR_ACCESS_KEY");
        spark.conf().set("spark.hadoop.fs.s3a.secret.key", "YOUR_SECRET_KEY");
        spark.conf().set("spark.hadoop.fs.s3a.session.token", "YOUR_SESSION_TOKEN");

        StructType ordersSchema = new StructType(new StructField[]{
            new StructField("order_id", DataTypes.LongType, false, Metadata.empty()),
            new StructField("customer_name", DataTypes.StringType, true, Metadata.empty()),
            new StructField("amount", DataTypes.createDecimalType(10, 2), true, Metadata.empty()),
            new StructField("order_date", DataTypes.StringType, true, Metadata.empty()),
            new StructField("region", DataTypes.StringType, true, Metadata.empty()),
        });

        Dataset<Row> raw = spark.read().format("csv")
            .option("header", "true")
            .option("sep", "|")
            .option("quote", "\"")
            .option("escape", "\"")
            .option("nullValue", "NA")
            .option("multiLine", "true")
            .schema(ordersSchema)
            .load("s3://your-bucket/landing/orders/");

        Dataset<Row> cleaned = raw
            .withColumn("region", upper(trim(col("region"))))
            .withColumn("customer_name", coalesce(col("customer_name"), lit("UNKNOWN")))
            .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
            .withColumn("amount",
                when(col("amount").leq(0), lit(null)).otherwise(col("amount")))
            .filter(col("amount").isNotNull())
            .filter(col("region").isNotNull())
            .dropDuplicates(new String[]{"order_id"})
            .withColumn("loaded_at", current_timestamp());

        cleaned.show(false);

        cleaned.write().mode("overwrite").saveAsTable("orders_curated");

        Dataset<Row> result = spark.table("orders_curated");
        System.out.println("orders_curated row count: " + result.count());
        result.show(false);

        spark.sql("DROP TABLE IF EXISTS orders_curated");
        spark.stop();
    }
}
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object S3CsvToTable {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("S3 CSV to Table").getOrCreate()

    spark.conf.set("spark.hadoop.fs.s3a.access.key", "YOUR_ACCESS_KEY")
    spark.conf.set("spark.hadoop.fs.s3a.secret.key", "YOUR_SECRET_KEY")
    spark.conf.set("spark.hadoop.fs.s3a.session.token", "YOUR_SESSION_TOKEN")

    val ordersSchema = StructType(Seq(
      StructField("order_id", LongType, nullable = false),
      StructField("customer_name", StringType, nullable = true),
      StructField("amount", DecimalType(10, 2), nullable = true),
      StructField("order_date", StringType, nullable = true),
      StructField("region", StringType, nullable = true),
    ))

    val raw = spark.read.format("csv")
      .option("header", "true")
      .option("sep", "|")
      .option("quote", "\"")
      .option("escape", "\"")
      .option("nullValue", "NA")
      .option("multiLine", "true")
      .schema(ordersSchema)
      .load("s3://your-bucket/landing/orders/")

    val cleaned = raw
      .withColumn("region", upper(trim(col("region"))))
      .withColumn("customer_name", coalesce(col("customer_name"), lit("UNKNOWN")))
      .withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
      .withColumn("amount",
        when(col("amount") <= 0, lit(null)).otherwise(col("amount")))
      .filter(col("amount").isNotNull)
      .filter(col("region").isNotNull)
      .dropDuplicates(Seq("order_id"))
      .withColumn("loaded_at", current_timestamp())

    cleaned.show(truncate = false)

    cleaned.write.mode("overwrite").saveAsTable("orders_curated")

    val result = spark.table("orders_curated")
    println(s"orders_curated row count: ${result.count()}")
    result.show(truncate = false)

    spark.sql("DROP TABLE IF EXISTS orders_curated")
    spark.stop()
  }
}
```

## Example 2: Azure Blob Storage (Parquet to table)

Read sales Parquet files from Azure Blob Storage, compute derived columns with NULL-safe
arithmetic, and write the enriched result to a Snowflake table. For supported Azure URL schemes and
credential configuration, see
[Cloud storage with Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-cloud-storage).

PythonJavaScala

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from pyspark.sql.types import (
    DecimalType, DoubleType, IntegerType, LongType, StringType,
    StructField, StructType, TimestampType,
)
from pyspark.sql.functions import (
    coalesce, col, current_timestamp, lit, regexp_replace, when,
)

spark = init_spark_session()

account = "myaccount"
container = "mycontainer"
spark.conf.set(
    f"fs.azure.sas.{container}.{account}.blob.core.windows.net",
    "YOUR_SAS_TOKEN",
)

sales_schema = StructType([
    StructField("transaction_id", LongType(), False),
    StructField("product_name", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DecimalType(12, 4), True),
    StructField("discount_pct", DoubleType(), True),
    StructField("sold_at", TimestampType(), True),
])

raw = spark.read.schema(sales_schema).parquet(
    f"azure://{account}.blob.core.windows.net/{container}/sales/2024/"
)

enriched = (
    raw
    .withColumn("discount_pct", coalesce(col("discount_pct"), lit(0.0)))
    .withColumn("net_amount",
                (col("unit_price") * col("quantity")
                 * (1 - col("discount_pct"))).cast(DecimalType(14, 2)))
    .withColumn("product_name",
                regexp_replace(col("product_name"), r"[^\w\s\-]", ""))
    .withColumn("margin_flag",
                when(col("discount_pct") > 0.3, lit("deep_discount"))
                .when(col("discount_pct") > 0, lit("discounted"))
                .otherwise(lit("full_price")))
    .withColumn("loaded_at", current_timestamp())
)

enriched.show(truncate=False)

enriched.write.mode("overwrite").saveAsTable("sales_enriched")

result = spark.table("sales_enriched")
print(f"sales_enriched row count: {result.count()}")
result.show(truncate=False)

spark.sql("DROP TABLE IF EXISTS sales_enriched")
spark.stop()
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.types.*;
import static org.apache.spark.sql.functions.*;

public class AzureParquetToTable {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("Azure Parquet to Table").getOrCreate();

        String account = "myaccount";
        String container = "mycontainer";
        spark.conf().set(
            "fs.azure.sas." + container + "." + account + ".blob.core.windows.net",
            "YOUR_SAS_TOKEN");

        StructType salesSchema = new StructType(new StructField[]{
            new StructField("transaction_id", DataTypes.LongType, false, Metadata.empty()),
            new StructField("product_name", DataTypes.StringType, true, Metadata.empty()),
            new StructField("quantity", DataTypes.IntegerType, true, Metadata.empty()),
            new StructField("unit_price", DataTypes.createDecimalType(12, 4), true,
                Metadata.empty()),
            new StructField("discount_pct", DataTypes.DoubleType, true, Metadata.empty()),
            new StructField("sold_at", DataTypes.TimestampType, true, Metadata.empty()),
        });

        Dataset<Row> raw = spark.read().schema(salesSchema).parquet(
            "azure://" + account + ".blob.core.windows.net/" + container + "/sales/2024/");

        Dataset<Row> enriched = raw
            .withColumn("discount_pct", coalesce(col("discount_pct"), lit(0.0)))
            .withColumn("net_amount",
                col("unit_price").multiply(col("quantity"))
                    .multiply(lit(1).minus(col("discount_pct")))
                    .cast(DataTypes.createDecimalType(14, 2)))
            .withColumn("product_name",
                regexp_replace(col("product_name"), "[^\\w\\s\\-]", ""))
            .withColumn("margin_flag",
                when(col("discount_pct").gt(0.3), lit("deep_discount"))
                    .when(col("discount_pct").gt(0), lit("discounted"))
                    .otherwise(lit("full_price")))
            .withColumn("loaded_at", current_timestamp());

        enriched.show(false);

        enriched.write().mode("overwrite").saveAsTable("sales_enriched");

        Dataset<Row> result = spark.table("sales_enriched");
        System.out.println("sales_enriched row count: " + result.count());
        result.show(false);

        spark.sql("DROP TABLE IF EXISTS sales_enriched");
        spark.stop();
    }
}
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object AzureParquetToTable {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("Azure Parquet to Table").getOrCreate()

    val account = "myaccount"
    val container = "mycontainer"
    spark.conf.set(
      s"fs.azure.sas.$container.$account.blob.core.windows.net",
      "YOUR_SAS_TOKEN")

    val salesSchema = StructType(Seq(
      StructField("transaction_id", LongType, nullable = false),
      StructField("product_name", StringType, nullable = true),
      StructField("quantity", IntegerType, nullable = true),
      StructField("unit_price", DecimalType(12, 4), nullable = true),
      StructField("discount_pct", DoubleType, nullable = true),
      StructField("sold_at", TimestampType, nullable = true),
    ))

    val raw = spark.read.schema(salesSchema).parquet(
      s"azure://$account.blob.core.windows.net/$container/sales/2024/")

    val enriched = raw
      .withColumn("discount_pct", coalesce(col("discount_pct"), lit(0.0)))
      .withColumn("net_amount",
        (col("unit_price") * col("quantity") * (lit(1) - col("discount_pct")))
          .cast(DecimalType(14, 2)))
      .withColumn("product_name",
        regexp_replace(col("product_name"), "[^\\w\\s\\-]", ""))
      .withColumn("margin_flag",
        when(col("discount_pct") > 0.3, lit("deep_discount"))
          .when(col("discount_pct") > 0, lit("discounted"))
          .otherwise(lit("full_price")))
      .withColumn("loaded_at", current_timestamp())

    enriched.show(truncate = false)

    enriched.write.mode("overwrite").saveAsTable("sales_enriched")

    val result = spark.table("sales_enriched")
    println(s"sales_enriched row count: ${result.count()}")
    result.show(truncate = false)

    spark.sql("DROP TABLE IF EXISTS sales_enriched")
    spark.stop()
  }
}
```

## Example 3: GCS via named stage (JSON to table)

Read JSON event data from Google Cloud Storage using a pre-created named Snowflake external stage,
normalize it, and load into a Snowflake table.

Important

Direct GCS URLs (`gs://`, `gcs://`) aren’t supported for I/O. You must create a named
external stage backed by a storage integration first (see the setup SQL below).

**One-time setup (run once in Snowflake):**

Copy code

```
CREATE STORAGE INTEGRATION gcs_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'GCS'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('gcs://your-gcs-bucket/');

CREATE STAGE my_gcs_stage
  URL = 'gcs://your-gcs-bucket/events/'
  STORAGE_INTEGRATION = gcs_int;
```

PythonJavaScala

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from pyspark.sql.functions import col, current_timestamp, lit, lower, trim, when
from pyspark.sql.types import DoubleType, LongType

spark = init_spark_session()

events = (
    spark.read.format("json")
    .option("multiLine", "true")
    .load("@my_gcs_stage/2024/01/")
)

events.printSchema()

normalized = (
    events
    .withColumn("event_type", lower(trim(col("event_type"))))
    .withColumn("user_id", col("user_id").cast(LongType()))
    .withColumn("event_value",
                when(col("event_value").isNull(), lit(0.0))
                .otherwise(col("event_value").cast(DoubleType())))
    .filter(col("event_type").isNotNull())
    .withColumn("loaded_at", current_timestamp())
)

normalized.show(truncate=False)

normalized.write.mode("overwrite").saveAsTable("events_normalized")

result = spark.table("events_normalized")
print(f"events_normalized row count: {result.count()}")
result.show(truncate=False)

spark.sql("DROP TABLE IF EXISTS events_normalized")
spark.stop()
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.types.DataTypes;
import static org.apache.spark.sql.functions.*;

public class GcsJsonToTable {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("GCS JSON to Table").getOrCreate();

        Dataset<Row> events = spark.read().format("json")
            .option("multiLine", "true")
            .load("@my_gcs_stage/2024/01/");

        events.printSchema();

        Dataset<Row> normalized = events
            .withColumn("event_type", lower(trim(col("event_type"))))
            .withColumn("user_id", col("user_id").cast(DataTypes.LongType))
            .withColumn("event_value",
                when(col("event_value").isNull(), lit(0.0))
                    .otherwise(col("event_value").cast(DataTypes.DoubleType)))
            .filter(col("event_type").isNotNull())
            .withColumn("loaded_at", current_timestamp());

        normalized.show(false);

        normalized.write().mode("overwrite").saveAsTable("events_normalized");

        Dataset<Row> result = spark.table("events_normalized");
        System.out.println("events_normalized row count: " + result.count());
        result.show(false);

        spark.sql("DROP TABLE IF EXISTS events_normalized");
        spark.stop();
    }
}
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DoubleType, LongType}

object GcsJsonToTable {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("GCS JSON to Table").getOrCreate()

    val events = spark.read.format("json")
      .option("multiLine", "true")
      .load("@my_gcs_stage/2024/01/")

    events.printSchema()

    val normalized = events
      .withColumn("event_type", lower(trim(col("event_type"))))
      .withColumn("user_id", col("user_id").cast(LongType))
      .withColumn("event_value",
        when(col("event_value").isNull, lit(0.0))
          .otherwise(col("event_value").cast(DoubleType)))
      .filter(col("event_type").isNotNull)
      .withColumn("loaded_at", current_timestamp())

    normalized.show(truncate = false)

    normalized.write.mode("overwrite").saveAsTable("events_normalized")

    val result = spark.table("events_normalized")
    println(s"events_normalized row count: ${result.count()}")
    result.show(truncate = false)

    spark.sql("DROP TABLE IF EXISTS events_normalized")
    spark.stop()
  }
}
```

## Example 4: Internal stage multi-format ingest to table

End-to-end ETL using only Snowflake internal stages. Works on any cloud (AWS, Azure, GCP) without
external credentials. The pipeline builds sample data with tricky values (quotes, commas, newlines,
NULLs), writes it to a stage in CSV and JSON formats, reads each back to verify data integrity, then
applies ETL transformations and lands the curated result in a Snowflake table.

PythonJavaScala

Copy code

```
from snowflake.snowpark_connect import init_spark_session
from pyspark.sql.types import (
    DoubleType, IntegerType, StringType, StructField, StructType,
)
from pyspark.sql.functions import (
    coalesce, col, current_timestamp, lit, to_timestamp, trim, upper, when,
)

spark = init_spark_session()

spark.sql("CREATE OR REPLACE TEMP STAGE etl_example_stage")

schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("created_at", StringType(), True),
    StructField("region", StringType(), True),
])

data = [
    (1, "Alice O'Brien",     1500.50, "2024-01-15 10:30:00", "us-east-1"),
    (2, 'Bob "The Builder"',  0.01,   "2024-02-28 23:59:59", "eu-west-1"),
    (3, "Charlie, Jr.",       None,   "2024-03-01 00:00:00", "ap-south-1"),
    (4, "",                   99999.99,"2024-12-31 12:00:00", None),
    (5, "Eve\nNewline",       42.00,  "2024-06-15 06:15:00", "us-west-2"),
]

source = spark.createDataFrame(data, schema)
source.show(truncate=False)

# CSV round-trip
source.write.mode("overwrite") \
    .option("header", "true").option("quote", '"').option("escape", '"') \
    .csv("@etl_example_stage/csv/")

csv_df = spark.read.format("csv") \
    .option("header", "true").option("inferSchema", "true") \
    .option("quote", '"').option("escape", '"').option("multiLine", "true") \
    .load("@etl_example_stage/csv/")
csv_df.orderBy("id").show(truncate=False)

# JSON round-trip
source.write.mode("overwrite").json("@etl_example_stage/json/")

json_df = spark.read.format("json") \
    .option("inferSchema", "true").load("@etl_example_stage/json/")
json_df.orderBy("id").show(truncate=False)

# Transform and load to table
curated = (
    source
    .withColumn("name", when(trim(col("name")) == "", None).otherwise(col("name")))
    .withColumn("name", coalesce(col("name"), lit("N/A")))
    .withColumn("amount", coalesce(col("amount"), lit(0.0)))
    .withColumn("region", coalesce(upper(trim(col("region"))), lit("UNKNOWN")))
    .withColumn("created_at", to_timestamp(col("created_at"), "yyyy-MM-dd HH:mm:ss"))
    .withColumn("amount_bucket",
                when(col("amount") >= 10000, lit("high"))
                .when(col("amount") >= 100, lit("medium"))
                .otherwise(lit("low")))
    .withColumn("loaded_at", current_timestamp())
)

curated.write.mode("overwrite").saveAsTable("etl_curated")

result = spark.table("etl_curated")
result.orderBy("id").show(truncate=False)
print(f"etl_curated row count: {result.count()}")

spark.sql("DROP TABLE IF EXISTS etl_curated")
spark.sql("DROP STAGE IF EXISTS etl_example_stage")
spark.stop()
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.types.*;
import static org.apache.spark.sql.functions.*;
import java.util.Arrays;

public class InternalStageToTable {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("Internal Stage to Table").getOrCreate();

        spark.sql("CREATE OR REPLACE TEMP STAGE etl_example_stage");

        StructType schema = new StructType(new StructField[]{
            new StructField("id", DataTypes.IntegerType, false, Metadata.empty()),
            new StructField("name", DataTypes.StringType, true, Metadata.empty()),
            new StructField("amount", DataTypes.DoubleType, true, Metadata.empty()),
            new StructField("created_at", DataTypes.StringType, true, Metadata.empty()),
            new StructField("region", DataTypes.StringType, true, Metadata.empty()),
        });

        Dataset<Row> source = spark.createDataFrame(Arrays.asList(
            RowFactory.create(1, "Alice O'Brien",       1500.50, "2024-01-15 10:30:00", "us-east-1"),
            RowFactory.create(2, "Bob \"The Builder\"",  0.01,   "2024-02-28 23:59:59", "eu-west-1"),
            RowFactory.create(3, "Charlie, Jr.",         null,   "2024-03-01 00:00:00", "ap-south-1"),
            RowFactory.create(4, "",                     99999.99,"2024-12-31 12:00:00", null),
            RowFactory.create(5, "Eve\nNewline",         42.00,  "2024-06-15 06:15:00", "us-west-2")
        ), schema);

        source.show(false);

        // CSV round-trip
        source.write().mode("overwrite")
            .option("header", "true").option("quote", "\"").option("escape", "\"")
            .csv("@etl_example_stage/csv/");

        Dataset<Row> csvDf = spark.read().format("csv")
            .option("header", "true").option("inferSchema", "true")
            .option("quote", "\"").option("escape", "\"").option("multiLine", "true")
            .load("@etl_example_stage/csv/");
        csvDf.orderBy("id").show(false);

        // JSON round-trip
        source.write().mode("overwrite").json("@etl_example_stage/json/");

        Dataset<Row> jsonDf = spark.read().format("json")
            .option("inferSchema", "true").load("@etl_example_stage/json/");
        jsonDf.orderBy("id").show(false);

        // Transform and load to table
        Dataset<Row> curated = source
            .withColumn("name",
                when(trim(col("name")).equalTo(""), lit(null)).otherwise(col("name")))
            .withColumn("name", coalesce(col("name"), lit("N/A")))
            .withColumn("amount", coalesce(col("amount"), lit(0.0)))
            .withColumn("region", coalesce(upper(trim(col("region"))), lit("UNKNOWN")))
            .withColumn("created_at",
                to_timestamp(col("created_at"), "yyyy-MM-dd HH:mm:ss"))
            .withColumn("amount_bucket",
                when(col("amount").geq(10000), lit("high"))
                    .when(col("amount").geq(100), lit("medium"))
                    .otherwise(lit("low")))
            .withColumn("loaded_at", current_timestamp());

        curated.write().mode("overwrite").saveAsTable("etl_curated");

        Dataset<Row> result = spark.table("etl_curated");
        result.orderBy("id").show(false);
        System.out.println("etl_curated row count: " + result.count());

        spark.sql("DROP TABLE IF EXISTS etl_curated");
        spark.sql("DROP STAGE IF EXISTS etl_example_stage");
        spark.stop();
    }
}
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._
import org.apache.spark.sql.Row

object InternalStageToTable {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("Internal Stage to Table").getOrCreate()

    spark.sql("CREATE OR REPLACE TEMP STAGE etl_example_stage")

    val schema = StructType(Seq(
      StructField("id", IntegerType, nullable = false),
      StructField("name", StringType, nullable = true),
      StructField("amount", DoubleType, nullable = true),
      StructField("created_at", StringType, nullable = true),
      StructField("region", StringType, nullable = true),
    ))

    import spark.implicits._

    val source = Seq(
      (1, Some("Alice O'Brien"),       Some(1500.50), "2024-01-15 10:30:00", Some("us-east-1")),
      (2, Some("Bob \"The Builder\""), Some(0.01),    "2024-02-28 23:59:59", Some("eu-west-1")),
      (3, Some("Charlie, Jr."),        None,          "2024-03-01 00:00:00", Some("ap-south-1")),
      (4, Some(""),                    Some(99999.99),"2024-12-31 12:00:00", None),
      (5, Some("Eve\nNewline"),        Some(42.00),   "2024-06-15 06:15:00", Some("us-west-2"))
    ).toDF("id", "name", "amount", "created_at", "region")

    source.show(truncate = false)

    // CSV round-trip
    source.write.mode("overwrite")
      .option("header", "true").option("quote", "\"").option("escape", "\"")
      .csv("@etl_example_stage/csv/")

    val csvDf = spark.read.format("csv")
      .option("header", "true").option("inferSchema", "true")
      .option("quote", "\"").option("escape", "\"").option("multiLine", "true")
      .load("@etl_example_stage/csv/")
    csvDf.orderBy("id").show(truncate = false)

    // JSON round-trip
    source.write.mode("overwrite").json("@etl_example_stage/json/")

    val jsonDf = spark.read.format("json")
      .option("inferSchema", "true").load("@etl_example_stage/json/")
    jsonDf.orderBy("id").show(truncate = false)

    // Transform and load to table
    val curated = source
      .withColumn("name",
        when(trim(col("name")) === "", lit(null)).otherwise(col("name")))
      .withColumn("name", coalesce(col("name"), lit("N/A")))
      .withColumn("amount", coalesce(col("amount"), lit(0.0)))
      .withColumn("region", coalesce(upper(trim(col("region"))), lit("UNKNOWN")))
      .withColumn("created_at",
        to_timestamp(col("created_at"), "yyyy-MM-dd HH:mm:ss"))
      .withColumn("amount_bucket",
        when(col("amount") >= 10000, lit("high"))
          .when(col("amount") >= 100, lit("medium"))
          .otherwise(lit("low")))
      .withColumn("loaded_at", current_timestamp())

    curated.write.mode("overwrite").saveAsTable("etl_curated")

    val result = spark.table("etl_curated")
    result.orderBy("id").show(truncate = false)
    println(s"etl_curated row count: ${result.count()}")

    spark.sql("DROP TABLE IF EXISTS etl_curated")
    spark.sql("DROP STAGE IF EXISTS etl_example_stage")
    spark.stop()
  }
}
```
