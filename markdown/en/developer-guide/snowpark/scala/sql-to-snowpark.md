# Quick reference: Snowpark Scala APIs for SQL commands

This topic provides a quick reference of some of the Snowpark APIs that correspond to SQL commands.

(Note that this is not a complete list of the APIs that correspond to SQL commands.)

## Performing queries

### Selecting columns

To select specific columns, use [DataFrame.select](../reference/scala/com/snowflake/snowpark/DataFrame.html#select(first:com.snowflake.snowpark.Column,remaining:com.snowflake.snowpark.Column*):com.snowflake.snowpark.DataFrame).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT id, name FROM sample_product_data; ``` | Copy code  ``` val dfSelectedCols = df.select(col("id"), col("name")) dfSelectedCols.show() ``` |

Expand

Show lessSee more

### Renaming columns

To rename a column, use [Column.as](../reference/scala/com/snowflake/snowpark/Column.html#as(alias:String):com.snowflake.snowpark.Column), [Column.alias](../reference/scala/com/snowflake/snowpark/Column.html#alias(alias:String):com.snowflake.snowpark.Column), or [Column.name](../reference/scala/com/snowflake/snowpark/Column.html#name(alias:String):com.snowflake.snowpark.Column).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT id AS item_id FROM sample_product_data; ``` | Copy code  ``` val dfRenamedCol = df.select(col("id").as("item_id")) dfRenamedCol.show() ``` |
|  | Copy code  ``` val dfRenamedCol = df.select(col("id").alias("item_id")) dfRenamedCol.show() ``` |
|  | Copy code  ``` val dfRenamedCol = df.select(col("id").name("item_id")) dfRenamedCol.show() ``` |

Expand

Show lessSee more

### Filtering data

To filter data, use [DataFrame.filter](../reference/scala/com/snowflake/snowpark/DataFrame.html#filter(condition:com.snowflake.snowpark.Column):com.snowflake.snowpark.DataFrame) or [DataFrame.where](../reference/scala/com/snowflake/snowpark/DataFrame.html#where(condition:com.snowflake.snowpark.Column):com.snowflake.snowpark.DataFrame).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data WHERE id = 1; ``` | Copy code  ``` val dfFilteredRows = df.filter((col("id") === 1)) dfFilteredRows.show() ``` |
|  | Copy code  ``` val dfFilteredRows = df.where((col("id") === 1)) dfFilteredRows.show() ``` |

Expand

Show lessSee more

### Sorting data

To sort data, use [DataFrame.sort](../reference/scala/com/snowflake/snowpark/DataFrame.html#sort(first:com.snowflake.snowpark.Column,remaining:com.snowflake.snowpark.Column*):com.snowflake.snowpark.DataFrame).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data ORDER BY category_id; ``` | Copy code  ``` val dfSorted = df.sort(col("category_id")) dfSorted.show() ``` |

Expand

Show lessSee more

### Limiting the number of rows returned

To limit the number of rows returned, use [DataFrame.limit](../reference/scala/com/snowflake/snowpark/DataFrame.html#limit(n:Int):com.snowflake.snowpark.DataFrame). See [Limiting the Number of Rows in a DataFrame](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-limit).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data   ORDER BY category_id LIMIT 2; ``` | Copy code  ``` val dfSorted = df.sort(col("category_id")).limit(2); val arrayRows = dfSorted.collect() ``` |

Expand

Show lessSee more

### Performing joins

To perform a join, use [DataFrame.join](../reference/scala/com/snowflake/snowpark/DataFrame.html#join(right:com.snowflake.snowpark.DataFrame,joinExprs:com.snowflake.snowpark.Column,joinType:String):com.snowflake.snowpark.DataFrame) or [DataFrame.naturalJoin](../reference/scala/com/snowflake/snowpark/DataFrame.html#naturalJoin(right:com.snowflake.snowpark.DataFrame):com.snowflake.snowpark.DataFrame). See [Joining DataFrames](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-joining).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_a   INNER JOIN sample_b   on sample_a.id_a = sample_b.id_a; ``` | Copy code  ``` val dfJoined =   dfLhs.join(dfRhs, dfLhs.col("id_a") === dfRhs.col("id_a")) dfJoined.show() ``` |
| Copy code  ``` SELECT * FROM sample_a NATURAL JOIN sample_b; ``` | Copy code  ``` val dfJoined = dfLhs.naturalJoin(dfRhs) dfJoined.show() ``` |

Expand

Show lessSee more

### Querying semi-structured data

To traverse semi-structured data, use [Column.apply(“<field\_name>”)](../reference/scala/com/snowflake/snowpark/Column.html#apply(field:String):com.snowflake.snowpark.Column) and [Column.apply(<index>)](../reference/scala/com/snowflake/snowpark/Column.html#apply(idx:Int):com.snowflake.snowpark.Column). See
[Working with Semi-Structured Data](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-semistructured).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT src:salesperson.name FROM car_sales; ``` | Copy code  ``` dfJsonField =   df.select(col("src")("salesperson")("name")) dfJsonField.show() ``` |

Expand

Show lessSee more

### Grouping and aggregating data

To group data, use [DataFrame.groupBy](../reference/scala/com/snowflake/snowpark/DataFrame.html#groupBy(first:com.snowflake.snowpark.Column,remaining:com.snowflake.snowpark.Column*):com.snowflake.snowpark.RelationalGroupedDataFrame). This returns a [RelationalGroupedDataFrame](../reference/scala/com/snowflake/snowpark/RelationalGroupedDataFrame.html) object, which you can use to perform the
aggregations.

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT category_id, count(*)   FROM sample_product_data GROUP BY category_id; ``` | Copy code  ``` val dfCountPerCategory = df.groupBy(col("category")).count() dfCountPerCategory.show() ``` |

Expand

Show lessSee more

### Calling window functions

To call a [window function](/user-guide/functions-window-using), use the [Window](../reference/scala/com/snowflake/snowpark/Window$.html) object methods to build a [WindowSpec](../reference/scala/com/snowflake/snowpark/WindowSpec.html)
object, which in turn you can use for windowing functions (similar to using ‘<function> OVER … PARTITION BY … ORDER BY’).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT category_id, price_date, SUM(amount) OVER   (PARTITION BY category_id ORDER BY price_date)   FROM prices ORDER BY price_date; ``` | Copy code  ``` val window = Window.partitionBy(   col("category")).orderBy(col("price_date")) val dfCumulativePrices = dfPrices.select(   col("category"), col("price_date"),   sum(col("amount")).over(window)).sort(col("price_date")) dfCumulativePrices.show() ``` |

Expand

Show lessSee more

## Updating, deleting, and merging rows

To update, delete, and merge rows in a table, use [Updatable](../reference/scala/com/snowflake/snowpark/Updatable.html). See [Updating, Deleting, and Merging Rows in a Table](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-updatable).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` UPDATE sample_product_data   SET serial_number = 'xyz' WHERE id = 12; ``` | Copy code  ``` val updateResult =   updatableDf.update(     Map("serial_number" -> lit("xyz")),     col("id") === 12) ``` |
| Copy code  ``` DELETE FROM sample_product_data   WHERE category_id = 50; ``` | Copy code  ``` val deleteResult =   updatableDf.delete(updatableDf("category_id") === 50) ``` |
| Copy code  ``` MERGE  INTO target_table USING source_table   ON target_table.id = source_table.id   WHEN MATCHED THEN     UPDATE SET target_table.description =       source_table.description; ``` | Copy code  ``` val mergeResult =    target.merge(source, target("id") === source("id"))   .whenMatched.update(Map("description" -> source("description")))   .collect() ``` |

Expand

Show lessSee more

## Working with stages

For more information on working with stages, see [Working With Files in a Stage](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages).

### Uploading and downloading files from a stage

To upload and download files from a stage, use [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html). See [Uploading and Downloading Files in a Stage](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-file-operation).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` PUT file:///tmp/*.csv @myStage OVERWRITE = TRUE; ``` | Copy code  ``` val putOptions = Map("OVERWRITE" -> "TRUE") val putResults = session.file.put(   "file:///tmp/*.csv", "@myStage", putOptions) ``` |
| Copy code  ``` GET @myStage file:///tmp PATTERN = '.*.csv.gz'; ``` | Copy code  ``` val getOptions = Map("PATTERN" -> s"'.*.csv.gz'") val getResults = session.file.get(  "@myStage", "file:///tmp", getOptions) ``` |

Expand

Show lessSee more

### Reading data from files in a stage

To read data from files in a stage, use [DataFrameReader](../reference/scala/com/snowflake/snowpark/DataFrameReader.html) to create a DataFrame for the data. See
[Setting Up a DataFrame for Files in a Stage](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-query).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE FILE FORMAT snowpark_temp_format TYPE = JSON; SELECT "$1"[0]['salesperson']['name'] FROM (   SELECT $1::VARIANT AS "$1" FROM @mystage/car_sales.json(     FILE_FORMAT => 'snowpark_temp_format')) LIMIT 10; DROP FILE FORMAT snowpark_temp_format; ``` | Copy code  ``` val df = session.read.json(   "@mystage/car_sales.json").select(     col("$1")(0)("salesperson")("name")) df.show(); ``` |

Expand

Show lessSee more

### Copying data from files in a stage to a table

To copy data from files in a stage to a table, use [DataFrameReader](../reference/scala/com/snowflake/snowpark/DataFrameReader.html) to create a [CopyableDataFrame](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html) for the data, and use the
[CopyableDataFrame.copyInto](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html#copyInto(tableName:String):Unit) method to copy the data to the table. See [Copying Data from Files into a Table](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-copy-into-table).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` COPY INTO new_car_sales   FROM @mystage/car_sales.json   FILE_FORMAT = (TYPE = JSON); ``` | Copy code  ``` val dfCopyableDf = session.read.json("@mystage/car_sales.json") dfCopyableDf.copyInto("new_car_sales") ``` |

Expand

Show lessSee more

### Saving a DataFrame to files on a stage

To save a DataFrame to files on a stage, use the [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) method named after the format of the files that you want to
use. See [Saving a DataFrame to Files on a Stage](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-stages-copy-into-location).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` COPY INTO @mystage/saved_data.json   FROM (  SELECT  *  FROM (car_sales) )   FILE_FORMAT = ( TYPE = JSON COMPRESSION = 'none' )   OVERWRITE = TRUE   DETAILED_OUTPUT = TRUE ``` | Copy code  ``` val df = session.table("car_sales") val writeFileResult = df.write.mode(   SaveMode.Overwrite).option(   "DETAILED_OUTPUT", "TRUE").option(   "compression", "none").json(   "@mystage/saved_data.json") ``` |

Expand

Show lessSee more

## Creating and calling user-defined functions (UDFs)

To create a Scala function that serves as a UDF (an anonymous UDF), use [udf](../reference/scala/com/snowflake/snowpark/functions$.html#udf%5BRT,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22%5D(func:(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)=%3ERT)(implicitevidence$255:reflect.runtime.universe.TypeTag%5BRT%5D,implicitevidence$256:reflect.runtime.universe.TypeTag%5BA1%5D,implicitevidence$257:reflect.runtime.universe.TypeTag%5BA2%5D,implicitevidence$258:reflect.runtime.universe.TypeTag%5BA3%5D,implicitevidence$259:reflect.runtime.universe.TypeTag%5BA4%5D,implicitevidence$260:reflect.runtime.universe.TypeTag%5BA5%5D,implicitevidence$261:reflect.runtime.universe.TypeTag%5BA6%5D,implicitevidence$262:reflect.runtime.universe.TypeTag%5BA7%5D,implicitevidence$263:reflect.runtime.universe.TypeTag%5BA8%5D,implicitevidence$264:reflect.runtime.universe.TypeTag%5BA9%5D,implicitevidence$265:reflect.runtime.universe.TypeTag%5BA10%5D,implicitevidence$266:reflect.runtime.universe.TypeTag%5BA11%5D,implicitevidence$267:reflect.runtime.universe.TypeTag%5BA12%5D,implicitevidence$268:reflect.runtime.universe.TypeTag%5BA13%5D,implicitevidence$269:reflect.runtime.universe.TypeTag%5BA14%5D,implicitevidence$270:reflect.runtime.universe.TypeTag%5BA15%5D,implicitevidence$271:reflect.runtime.universe.TypeTag%5BA16%5D,implicitevidence$272:reflect.runtime.universe.TypeTag%5BA17%5D,implicitevidence$273:reflect.runtime.universe.TypeTag%5BA18%5D,implicitevidence$274:reflect.runtime.universe.TypeTag%5BA19%5D,implicitevidence$275:reflect.runtime.universe.TypeTag%5BA20%5D,implicitevidence$276:reflect.runtime.universe.TypeTag%5BA21%5D,implicitevidence$277:reflect.runtime.universe.TypeTag%5BA22%5D):com.snowflake.snowpark.UserDefinedFunction).

To create a temporary or permanent UDF that you can call by name, use [UDFRegistration.registerTemporary](../reference/scala/com/snowflake/snowpark/UDFRegistration.html#registerTemporary%5BRT,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22%5D(name:String,func:(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)=%3ERT)(implicitevidence$530:reflect.runtime.universe.TypeTag%5BRT%5D,implicitevidence$531:reflect.runtime.universe.TypeTag%5BA1%5D,implicitevidence$532:reflect.runtime.universe.TypeTag%5BA2%5D,implicitevidence$533:reflect.runtime.universe.TypeTag%5BA3%5D,implicitevidence$534:reflect.runtime.universe.TypeTag%5BA4%5D,implicitevidence$535:reflect.runtime.universe.TypeTag%5BA5%5D,implicitevidence$536:reflect.runtime.universe.TypeTag%5BA6%5D,implicitevidence$537:reflect.runtime.universe.TypeTag%5BA7%5D,implicitevidence$538:reflect.runtime.universe.TypeTag%5BA8%5D,implicitevidence$539:reflect.runtime.universe.TypeTag%5BA9%5D,implicitevidence$540:reflect.runtime.universe.TypeTag%5BA10%5D,implicitevidence$541:reflect.runtime.universe.TypeTag%5BA11%5D,implicitevidence$542:reflect.runtime.universe.TypeTag%5BA12%5D,implicitevidence$543:reflect.runtime.universe.TypeTag%5BA13%5D,implicitevidence$544:reflect.runtime.universe.TypeTag%5BA14%5D,implicitevidence$545:reflect.runtime.universe.TypeTag%5BA15%5D,implicitevidence$546:reflect.runtime.universe.TypeTag%5BA16%5D,implicitevidence$547:reflect.runtime.universe.TypeTag%5BA17%5D,implicitevidence$548:reflect.runtime.universe.TypeTag%5BA18%5D,implicitevidence$549:reflect.runtime.universe.TypeTag%5BA19%5D,implicitevidence$550:reflect.runtime.universe.TypeTag%5BA20%5D,implicitevidence$551:reflect.runtime.universe.TypeTag%5BA21%5D,implicitevidence$552:reflect.runtime.universe.TypeTag%5BA22%5D):com.snowflake.snowpark.UserDefinedFunction) or
[UDFRegistration.registerPermanent](../reference/scala/com/snowflake/snowpark/UDFRegistration.html#registerPermanent%5BRT,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22%5D(name:String,func:(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)=%3ERT,stageLocation:String)(implicitevidence$806:reflect.runtime.universe.TypeTag%5BRT%5D,implicitevidence$807:reflect.runtime.universe.TypeTag%5BA1%5D,implicitevidence$808:reflect.runtime.universe.TypeTag%5BA2%5D,implicitevidence$809:reflect.runtime.universe.TypeTag%5BA3%5D,implicitevidence$810:reflect.runtime.universe.TypeTag%5BA4%5D,implicitevidence$811:reflect.runtime.universe.TypeTag%5BA5%5D,implicitevidence$812:reflect.runtime.universe.TypeTag%5BA6%5D,implicitevidence$813:reflect.runtime.universe.TypeTag%5BA7%5D,implicitevidence$814:reflect.runtime.universe.TypeTag%5BA8%5D,implicitevidence$815:reflect.runtime.universe.TypeTag%5BA9%5D,implicitevidence$816:reflect.runtime.universe.TypeTag%5BA10%5D,implicitevidence$817:reflect.runtime.universe.TypeTag%5BA11%5D,implicitevidence$818:reflect.runtime.universe.TypeTag%5BA12%5D,implicitevidence$819:reflect.runtime.universe.TypeTag%5BA13%5D,implicitevidence$820:reflect.runtime.universe.TypeTag%5BA14%5D,implicitevidence$821:reflect.runtime.universe.TypeTag%5BA15%5D,implicitevidence$822:reflect.runtime.universe.TypeTag%5BA16%5D,implicitevidence$823:reflect.runtime.universe.TypeTag%5BA17%5D,implicitevidence$824:reflect.runtime.universe.TypeTag%5BA18%5D,implicitevidence$825:reflect.runtime.universe.TypeTag%5BA19%5D,implicitevidence$826:reflect.runtime.universe.TypeTag%5BA20%5D,implicitevidence$827:reflect.runtime.universe.TypeTag%5BA21%5D,implicitevidence$828:reflect.runtime.universe.TypeTag%5BA22%5D):com.snowflake.snowpark.UserDefinedFunction).

To call a permanent UDF by name, use [callUDF](../reference/scala/com/snowflake/snowpark/functions$.html#callUDF(udfName:String,cols:Any*):com.snowflake.snowpark.Column).

For details, see [Creating User-Defined Functions (UDFs) for DataFrames in Scala](/developer-guide/snowpark/scala/creating-udfs) and [Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/scala/calling-functions#label-snowpark-udfs-calling).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE FUNCTION <temp_function_name>   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   <temp_function_name>(amount) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` val doubleUdf = udf((x: Int) => x + x) val dfWithDoubleNum = df.withColumn(  "doubleNum", doubleUdf(col("amount"))) dfWithDoubleNum.show() ``` |
| Copy code  ``` CREATE FUNCTION <temp_function_name>   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   <temp_function_name>(amount) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` session.udf.registerTemporary(   "doubleUdf", (x: Int) => x + x) val dfWithDoubleNum = df.withColumn(  "doubleNum", callUDF("doubleUdf", (col("amount")))) dfWithDoubleNum.show() ``` |
| Copy code  ``` CREATE FUNCTION doubleUdf(arg1 INT)   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   doubleUdf(amount) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` session.udf.registerPermanent(   "doubleUdf", (x: Int) => x + x, "mystage") val dfWithDoubleNum = df.withColumn(  "doubleNum", callUDF("doubleUdf", (col("amount")))) dfWithDoubleNum.show() ``` |

Expand

Show lessSee more

## Creating and calling stored procedures

For a guide on creating stored procedures with Snowpark, see [Creating stored procedures for DataFrames in Scala](/developer-guide/snowpark/scala/creating-sprocs).

- To create an anonymous or named temporary procedure, use a `registerTemporary` methods of [com.snowflake.snowpark.SProcRegistration](../reference/scala/com/snowflake/snowpark/SProcRegistration.html).
- To create a named permanent procedure, use a `registerPermanent` method of the [com.snowflake.snowpark.SProcRegistration](../reference/scala/com/snowflake/snowpark/SProcRegistration.html) class.
- To call a procedure, use the `storedProcedure` method of the [com.snowflake.snowpark.Session](../reference/scala/com/snowflake/snowpark/Session.html) class.

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE PROCEDURE <temp_procedure_name>(x INTEGER, y INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN    RETURN x + y;   END   $$   ;  CALL <temp_procedure_name>(2, 3); ``` | Copy code  ``` val sp: StoredProcedure =   session.sproc.registerTemporary(     (session: Session, x: Int, y: Int) => x + y   )  session.storedProcedure(sp, 2, 3).show() ``` |
| Copy code  ``` CREATE PROCEDURE sproc(x INTEGER, y INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN    RETURN x + y;   END   $$   ;  CALL sproc(2, 3); ``` | Copy code  ``` val name: String = "sproc" val sp: StoredProcedure =   session.sproc.registerTemporary(     name,     (session: Session, x: Int, y: Int) => x + y   )  session.storedProcedure(name, 2, 3).show() ``` |
| Copy code  ``` CREATE PROCEDURE add_hundred(x INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN    RETURN x + 100;   END   $$   ;  CALL add_hundred(3); ``` | Copy code  ``` val name: String = "add_hundred" val stageName: String = "sproc_libs"  val sp: StoredProcedure =   session.sproc.registerPermanent(     name,     (session: Session, x: Int) => x + 100,     stageName,     true   )  session.storedProcedure(name, 3).show ``` |

Expand

Show lessSee more
