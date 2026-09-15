# Tutorial: Get started with Snowpark Connect for Spark

This tutorial walks you through a complete Snowpark Connect for Spark workflow using a local IDE. You’ll create a
source table, read data into a Spark DataFrame, apply transformations with user-defined functions,
save results to a table and a file, and verify the output using the `SnowflakeSession` class.

Choose the tab for your language in each step to follow along in Python, Java, or Scala.

Note

Each step builds on the previous one to form a single end-to-end example. Pick one language tab
and follow it through all steps. For Python, you can run each step individually in a REPL or
notebook. For Java or Scala, combine all steps into one `Tutorial.java` or `Tutorial.scala`
file before running.

## Prerequisites

Complete the
[environment setup](/developer-guide/snowpark-connect/snowpark-connect-environment-setup)
for your language before starting this tutorial. You need a Snowflake account with access to
Snowpark Connect for Spark and a database and schema to work in.

## Step 1: Connect and create a source table

Start a session and create a table with sample sales data.

PythonJavaScala

Copy code

```
import snowflake.snowpark_connect
from snowflake.snowpark_connect.snowflake_session import SnowflakeSession
from pyspark.sql.connect.functions import udf
from pyspark.sql.functions import col, upper
from pyspark.sql.types import DoubleType

spark = snowflake.snowpark_connect.init_spark_session()

spark.sql("CREATE OR REPLACE TABLE sales (product STRING, region STRING, amount DOUBLE)")
spark.sql("""
    INSERT INTO sales VALUES
        ('Widget', 'north', 120.50),
        ('Gadget', 'south', 85.00),
        ('Widget', 'south', 200.75),
        ('Gizmo', 'north', 45.30),
        ('Gadget', 'north', 150.00),
        ('Gizmo', 'south', 60.00)
""")
```

Copy code

```
import com.snowflake.snowpark_connect.client.SnowparkConnectSession;
import com.snowflake.snowpark_connect.client.SnowflakeSession;
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.*;
import org.apache.spark.sql.connect.client.REPLClassDirMonitor;
import static org.apache.spark.sql.functions.*;

public class Tutorial {
    public static void main(String[] args) {
        SparkSession spark = SnowparkConnectSession.builder()
            .appName("Tutorial")
            .getOrCreate();

        // Register a class finder so Spark can discover compiled UDF classes
        REPLClassDirMonitor classFinder = new REPLClassDirMonitor("/path/to/target/classes");
        spark.registerClassFinder(classFinder);

        spark.sql("CREATE OR REPLACE TABLE sales (product STRING, region STRING, amount DOUBLE)");
        spark.sql("INSERT INTO sales VALUES "
            + "('Widget', 'north', 120.50), "
            + "('Gadget', 'south', 85.00), "
            + "('Widget', 'south', 200.75), "
            + "('Gizmo', 'north', 45.30), "
            + "('Gadget', 'north', 150.00), "
            + "('Gizmo', 'south', 60.00)");
```

Copy code

```
import com.snowflake.snowpark_connect.client.{SnowparkConnectSession, SnowflakeSession}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.DoubleType
import org.apache.spark.sql.connect.client.REPLClassDirMonitor

object Tutorial {
  def main(args: Array[String]): Unit = {
    val spark = SnowparkConnectSession.builder()
      .appName("Tutorial")
      .getOrCreate()

    // Register a class finder so Spark can discover compiled UDF classes
    val classFinder = new REPLClassDirMonitor("/path/to/target/scala-2.12/classes")
    spark.registerClassFinder(classFinder)

    spark.sql("CREATE OR REPLACE TABLE sales (product STRING, region STRING, amount DOUBLE)")
    spark.sql("""INSERT INTO sales VALUES
        ('Widget', 'north', 120.50),
        ('Gadget', 'south', 85.00),
        ('Widget', 'south', 200.75),
        ('Gizmo', 'north', 45.30),
        ('Gadget', 'north', 150.00),
        ('Gizmo', 'south', 60.00)""")
```

## Step 2: Read from the table and apply transformations

Read the data into a DataFrame, normalize the `region` column to uppercase, and apply a tiered
tax rate based on the sale amount. Orders under $50 are taxed at 5%, orders between $50 and $150
at 10%, and orders over $150 at 15%. This kind of multi-bracket business logic is a natural fit for
a UDF. The Python example registers a UDF, while Java and Scala use typed Dataset `map` operations.

PythonJavaScala

Copy code

```
@udf(returnType=DoubleType())
def apply_tiered_tax(amount: float) -> float:
    if amount < 50:
        rate = 0.05
    elif amount <= 150:
        rate = 0.10
    else:
        rate = 0.15
    return round(amount * (1 + rate), 2)

df = spark.table("sales")

result = df.withColumn("region", upper(col("region"))) \
           .withColumn("amount_with_tax", apply_tiered_tax(col("amount")))

result.show()
```

Copy code

```
import org.apache.spark.api.java.function.MapFunction;

// POJO that mirrors the source table schema.
// Encoders.bean() maps DataFrame columns to getter/setter pairs,
// giving you a typed Dataset<Sale> instead of raw Row objects.
public static class Sale implements java.io.Serializable {
    private String product;
    private String region;
    private double amount;

    public Sale() {}
    public String getProduct() { return product; }
    public void setProduct(String p) { this.product = p; }
    public String getRegion() { return region; }
    public void setRegion(String r) { this.region = r; }
    public double getAmount() { return amount; }
    public void setAmount(double a) { this.amount = a; }
}

// Output POJO with the computed column. A separate class lets the
// encoder infer the result schema automatically from the bean fields.
public static class SaleWithTax implements java.io.Serializable {
    private String product;
    private String region;
    private double amount;
    private double amount_with_tax;

    public SaleWithTax() {}
    public String getProduct() { return product; }
    public void setProduct(String p) { this.product = p; }
    public String getRegion() { return region; }
    public void setRegion(String r) { this.region = r; }
    public double getAmount() { return amount; }
    public void setAmount(double a) { this.amount = a; }
    public double getAmount_with_tax() { return amount_with_tax; }
    public void setAmount_with_tax(double v) { this.amount_with_tax = v; }
}

static double applyTieredTax(double amount) {
    double rate = amount < 50 ? 0.05 : amount <= 150 ? 0.10 : 0.15;
    return Math.round(amount * (1 + rate) * 100.0) / 100.0;
}

Dataset<Sale> sales = spark.table("sales").as(Encoders.bean(Sale.class));

Dataset<Row> result = sales
    .map((MapFunction<Sale, SaleWithTax>) s -> {
        SaleWithTax out = new SaleWithTax();
        out.setProduct(s.getProduct());
        out.setRegion(s.getRegion().toUpperCase());
        out.setAmount(s.getAmount());
        out.setAmount_with_tax(applyTieredTax(s.getAmount()));
        return out;
    }, Encoders.bean(SaleWithTax.class))
    .toDF();

result.show();
```

Copy code

```
import spark.implicits._

case class Sale(product: String, region: String, amount: Double)
case class SaleWithTax(product: String, region: String, amount: Double, amount_with_tax: Double)

def applyTieredTax(amount: Double): Double = {
  val rate = if (amount < 50) 0.05 else if (amount <= 150) 0.10 else 0.15
  Math.round(amount * (1 + rate) * 100.0) / 100.0
}

val result = spark.table("sales").as[Sale]
  .map(s => SaleWithTax(
    s.product,
    s.region.toUpperCase,
    s.amount,
    applyTieredTax(s.amount)
  ))
  .toDF()

result.show()
```

The output looks like this:

```
+-------+------+------+---------------+
%product%region%amount%amount_with_tax|
+-------+------+------+---------------+
| Widget| NORTH|120.50|         132.55|
| Gadget| SOUTH| 85.00|          93.50|
| Widget| SOUTH|200.75|         230.86|
|  Gizmo| NORTH| 45.30|          47.57|
| Gadget| NORTH|150.00|         165.00|
|  Gizmo| SOUTH| 60.00|          66.00|
+-------+------+------+---------------+
```

## Step 3: Save results to a table and a file

Write the transformed data to a new Snowflake table and export it to a Parquet file on an internal
stage.

PythonJavaScala

Copy code

```
result.write.mode("overwrite").saveAsTable("sales_with_tax")

result.write.mode("overwrite").parquet("@~/tutorial_output/sales_with_tax")
```

Copy code

```
result.write().mode("overwrite").saveAsTable("sales_with_tax");

result.write().mode("overwrite").parquet("@~/tutorial_output/sales_with_tax");
```

Copy code

```
result.write.mode("overwrite").saveAsTable("sales_with_tax")

result.write.mode("overwrite").parquet("@~/tutorial_output/sales_with_tax")
```

## Step 4: Verify with the SnowflakeSession class

Use `SnowflakeSession` to run a Snowflake-native aggregation query against the output table and
list the staged Parquet files written in Step 3. This verifies that both outputs were created and
demonstrates how to use `SnowflakeSession` for Snowflake-specific SQL.

PythonJavaScala

Copy code

```
sf = SnowflakeSession(spark)

totals = sf.sql("""
    SELECT product,
           SUM(amount_with_tax) AS total_with_tax,
           COUNT(*) AS num_sales
    FROM sales_with_tax
    GROUP BY product
    ORDER BY total_with_tax DESC
""")
totals.show()

staged_files = sf.sql("LIST @~/tutorial_output/sales_with_tax")
staged_files.show(truncate=False)

spark.stop()
```

Copy code

```
        SnowflakeSession sf = new SnowflakeSession(spark);

        Dataset<Row> totals = sf.sql(
            "SELECT product, "
            + "SUM(amount_with_tax) AS total_with_tax, "
            + "COUNT(*) AS num_sales "
            + "FROM sales_with_tax "
            + "GROUP BY product "
            + "ORDER BY total_with_tax DESC");
        totals.show();

        Dataset<Row> stagedFiles = sf.sql(
            "LIST @~/tutorial_output/sales_with_tax");
        stagedFiles.show(false);

        spark.stop();
    }
}
```

Copy code

```
    val sf = new SnowflakeSession(spark)

    val totals = sf.sql(
      """SELECT product,
        |       SUM(amount_with_tax) AS total_with_tax,
        |       COUNT(*) AS num_sales
        |FROM sales_with_tax
        |GROUP BY product
        |ORDER BY total_with_tax DESC""".stripMargin)
    totals.show()

    val stagedFiles = sf.sql("LIST @~/tutorial_output/sales_with_tax")
    stagedFiles.show(truncate = false)

    spark.stop()
  }
}
```

The staged file listing shows the Parquet files written to the stage:

```
+--------------------------------------------------------------------------------------------------------+----+--------------------------------+-----------------------------+
|name                                                                                                    |size|md5                             |last_modified                |
+--------------------------------------------------------------------------------------------------------+----+--------------------------------+-----------------------------+
|tutorial_output/sales_with_tax/part-00000-...-c000_0_2_0.snappy.parquet                                 |976 |694064b6ca5a43c9...             |Mon, 01 Jan 2024 00:00:00 GMT|
|tutorial_output/sales_with_tax/part-00000-...-c000_0_3_0.snappy.parquet                                 |976 |a41ee22852932...                |Mon, 01 Jan 2024 00:00:00 GMT|
|tutorial_output/sales_with_tax/part-00000-...-c000_0_4_0.snappy.parquet                                 |976 |abdc796ac22cb...                |Mon, 01 Jan 2024 00:00:00 GMT|
|tutorial_output/sales_with_tax/part-00000-...-c000_0_5_0.snappy.parquet                                 |976 |6efec381920c9...                |Mon, 01 Jan 2024 00:00:00 GMT|
|tutorial_output/sales_with_tax/part-00000-...-c000_0_6_0.snappy.parquet                                 |976 |a63c1fabd8b41...                |Mon, 01 Jan 2024 00:00:00 GMT|
|tutorial_output/sales_with_tax/part-00000-...-c000_0_7_0.snappy.parquet                                 |976 |22825d9f598b4...                |Mon, 01 Jan 2024 00:00:00 GMT|
+--------------------------------------------------------------------------------------------------------+----+--------------------------------+-----------------------------+
```

The table aggregation output looks like this:

```
+-------+--------------+---------+
%PRODUCT%TOTAL_WITH_TAX%NUM_SALES%
+-------+--------------+---------+
| Widget|        363.41|        2|
| Gadget|         258.5|        2|
|  Gizmo|        113.56|        2|
+-------+--------------+---------+
```

## Step 5: Run the tutorial

PythonJavaScala

Copy code

```
python tutorial.py
```

Copy code

```
mvn compile exec:java -Dexec.mainClass="Tutorial"
```

Copy code

```
sbt "runMain Tutorial"
```

## Clean up

Remove the tables and stage files created during this tutorial:

Copy code

```
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS sales_with_tax;
REMOVE @~/tutorial_output/;
```

## Next steps

- Learn more about [executing Snowflake SQL](/developer-guide/snowpark-connect/snowpark-connect-executing-sql),
  including `SnowflakeSession` for Snowflake-specific syntax.
- Explore [user-defined functions](/developer-guide/snowpark-connect/snowpark-connect-udfs) for Python, Java,
  and Scala UDFs and UDTFs.
- Read and write files with [File I/O](/developer-guide/snowpark-connect/snowpark-connect-file-io).
- Configure session behavior with [parameters](/developer-guide/snowpark-connect/snowpark-connect-parameters).
