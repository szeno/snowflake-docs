# Quick reference: Snowpark Java APIs for SQL commands

This topic provides a quick reference of some of the Snowpark APIs that correspond to SQL commands.

(Note that this is not a complete list of the APIs that correspond to SQL commands.)

## Performing queries

### Selecting columns

To select specific columns, use [select](../reference/java/com/snowflake/snowpark_java/DataFrame.html#select(com.snowflake.snowpark_java.Column...)).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT id, name FROM sample_product_data; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfSelectedCols = df.select(Functions.col("id"), Functions.col("name"));  dfSelectedCols.show(); ``` |

Expand

Show lessSee more

### Renaming columns

To rename a column, use [as](../reference/java/com/snowflake/snowpark_java/Column.html#as(java.lang.String)) or [alias](../reference/java/com/snowflake/snowpark_java/Column.html#alias(java.lang.String)).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT id AS item_id FROM sample_product_data; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfRenamedCol = df.select(Functions.col("id").as("item_id"));  dfRenamedCol.show(); ``` |
|  | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfRenamedCol = df.select(Functions.col("id").alias("item_id"));  dfRenamedCol.show(); ``` |

Expand

Show lessSee more

### Filtering data

To filter data, use [filter](../reference/java/com/snowflake/snowpark_java/DataFrame.html#filter(com.snowflake.snowpark_java.Column)) or [where](../reference/java/com/snowflake/snowpark_java/DataFrame.html#where(com.snowflake.snowpark_java.Column)).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data WHERE id = 1; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfFilteredRows = df.filter(Functions.col("id").equal_to(Functions.lit(1)));  dfFilteredRows.show(); ``` |
|  | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfFilteredRows = df.where(Functions.col("id").equal_to(Functions.lit(1)));  dfFilteredRows.show(); ``` |

Expand

Show lessSee more

### Sorting data

To sort data, use [sort](../reference/java/com/snowflake/snowpark_java/DataFrame.html#sort(com.snowflake.snowpark_java.Column...)).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data ORDER BY category_id; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfSorted = df.sort(Functions.col("category_id"));  dfSorted.show(); ``` |

Expand

Show lessSee more

### Limiting the number of rows returned

To limit the number of rows returned, use [limit](../reference/java/com/snowflake/snowpark_java/DataFrame.html#limit(int)). See [Limiting the Number of Rows in a DataFrame](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-limit).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_product_data   ORDER BY category_id LIMIT 2; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfSorted = df.sort(Functions.col("category_id")).limit(2);  Row[] arrayRows = dfSorted.collect(); ``` |

Expand

Show lessSee more

### Performing joins

To perform a join, use [join](../reference/java/com/snowflake/snowpark_java/DataFrame.html#join(com.snowflake.snowpark_java.DataFrame,com.snowflake.snowpark_java.Column,java.lang.String)) or [naturalJoin](../reference/java/com/snowflake/snowpark_java/DataFrame.html#naturalJoin(com.snowflake.snowpark_java.DataFrame)). See [Joining DataFrames](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-joining).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT * FROM sample_a   INNER JOIN sample_b   on sample_a.id_a = sample_b.id_a; ``` | Copy code  ``` DataFrame dfLhs = session.table("sample_a");  DataFrame dfRhs = session.table("sample_b");  DataFrame dfJoined =   dfLhs.join(dfRhs, dfLhs.col("id_a").equal_to(dfRhs.col("id_a")));  dfJoined.show(); ``` |
| Copy code  ``` SELECT * FROM sample_a NATURAL JOIN sample_b; ``` | Copy code  ``` DataFrame dfLhs = session.table("sample_a");  DataFrame dfRhs = session.table("sample_b");  DataFrame dfJoined = dfLhs.naturalJoin(dfRhs);  dfJoined.show(); ``` |

Expand

Show lessSee more

### Querying semi-structured data

To traverse semi-structured data, use [subField(“<field\_name>”)](../reference/java/com/snowflake/snowpark_java/Column.html#subField(java.lang.String)) and [subField(<index>)](../reference/java/com/snowflake/snowpark_java/Column.html#subField(int)). See
[Working with Semi-Structured Data](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-semistructured).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT src:salesperson.name FROM car_sales; ``` | Copy code  ``` DataFrame df = session.table("car_sales");  DataFrame dfJsonField =   df.select(Functions.col("src").subField("salesperson").subField("name"));  dfJsonField.show(); ``` |

Expand

Show lessSee more

### Grouping and aggregating data

To group data, use [groupBy](../reference/java/com/snowflake/snowpark_java/DataFrame.html#groupBy(com.snowflake.snowpark_java.Column...)). This returns a [RelationalGroupedDataFrame](../reference/scala/com/snowflake/snowpark/RelationalGroupedDataFrame.html) object, which you can use to perform the aggregations.

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT category_id, count(*)   FROM sample_product_data GROUP BY category_id; ``` | Copy code  ``` DataFrame df = session.table("sample_product_data");  DataFrame dfCountPerCategory = df.groupBy(Functions.col("category_id")).count();  dfCountPerCategory.show(); ``` |

Expand

Show lessSee more

### Calling window functions

To call a [window function](/user-guide/functions-window-using), use the [Window](../reference/scala/com/snowflake/snowpark/Window$.html) object methods to build a [WindowSpec](../reference/scala/com/snowflake/snowpark/WindowSpec.html)
object, which in turn you can use for windowing functions (similar to using ‘<function> OVER … PARTITION BY … ORDER BY’).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` SELECT category_id, id, SUM(amount) OVER   (PARTITION BY category_id ORDER BY product_date)   FROM sample_product_data ORDER BY product_date; ``` | Copy code  ``` WindowSpec window = Window.partitionBy(   Functions.col("category_id")).orderBy(Functions.col("product_date"));  DataFrame df = session.table("sample_product_data");  DataFrame dfCumulativePrices = df.select(   Functions.col("category_id"), Functions.col("product_date"),   Functions.sum(Functions.col("amount")).over(window)).sort(Functions.col("product_date"));  dfCumulativePrices.show(); ``` |

Expand

Show lessSee more

## Updating, deleting, and merging rows

To update, delete, and merge rows in a table, use [Updatable](../reference/scala/com/snowflake/snowpark/Updatable.html). See [Updating, Deleting, and Merging Rows in a Table](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-updatable).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` UPDATE sample_product_data   SET serial_number = 'xyz' WHERE id = 12; ``` | Copy code  ``` import java.util.HashMap; import java.util.Map; ...  Map<Column, Column> assignments = new HashMap<>();  assignments.put(Functions.col("serial_number"), Functions.lit("xyz"));  Updatable updatableDf = session.table("sample_product_data");  UpdateResult updateResult =   updatableDf.update(     assignments,     Functions.col("id").equal_to(Functions.lit(12)));  System.out.println("Number of rows updated: " + updateResult.getRowsUpdated()); ``` |
| Copy code  ``` DELETE FROM sample_product_data   WHERE category_id = 50; ``` | Copy code  ``` Updatable updatableDf = session.table("sample_product_data");  DeleteResult deleteResult =   updatableDf.delete(updatableDf.col("category_id").equal_to(Functions.lit(50)));  System.out.println("Number of rows deleted: " + deleteResult.getRowsDeleted()); ``` |
| Copy code  ``` MERGE  INTO target_table USING source_table   ON target_table.id = source_table.id   WHEN MATCHED THEN     UPDATE SET target_table.description =       source_table.description; ``` | Copy code  ``` import java.util.HashMap; import java.util.Map;  Map<String, Column> assignments = new HashMap<>(); assignments.put("description", source.col("description")); MergeResult mergeResult =   target.merge(source, target.col("id").equal_to(source.col("id")))   .whenMatched().updateColumn(assignments)   .collect(); ``` |

Expand

Show lessSee more

## Working with stages

For more information on working with stages, see [Working With Files in a Stage](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages).

### Uploading and Downloading Files from a Stage

To upload and download files from a stage, use [FileOperation](../reference/scala/com/snowflake/snowpark/FileOperation.html). See [Uploading and Downloading Files in a Stage](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-file-operation).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` PUT file:///tmp/*.csv @myStage OVERWRITE = TRUE; ``` | Copy code  ``` import java.util.HashMap; import java.util.Map; ... Map<String, String> putOptions = new HashMap<>();  putOptions.put("OVERWRITE", "TRUE");  PutResult[] putResults = session.file().put(   "file:///tmp/*.csv", "@myStage", putOptions);  for (PutResult result : putResults) {   System.out.println(result.getSourceFileName() + ": " + result.getStatus()); } ``` |
| Copy code  ``` GET @myStage file:///tmp PATTERN = '.*.csv.gz'; ``` | Copy code  ``` import java.util.HashMap; import java.util.Map; ... Map<String, String> getOptions = new HashMap<>();  getOptions.put("PATTERN", "'.*.csv.gz'");  GetResult[] getResults = session.file().get( "@myStage", "file:///tmp", getOptions);  for (GetResult result : getResults) {   System.out.println(result.getFileName() + ": " + result.getStatus()); } ``` |

Expand

Show lessSee more

### Reading data from files in a stage

To read data from files in a stage, use [DataFrameReader](../reference/scala/com/snowflake/snowpark/DataFrameReader.html) to create a DataFrame for the data. See
[Setting Up a DataFrame for Files in a Stage](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-query).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE FILE FORMAT snowpark_temp_format TYPE = JSON;  SELECT "$1"[0]['salesperson']['name'] FROM (   SELECT $1::VARIANT AS "$1" FROM @mystage/car_sales.json(     FILE_FORMAT => 'snowpark_temp_format')) LIMIT 10;  DROP FILE FORMAT snowpark_temp_format; ``` | Copy code  ``` DataFrame df = session.read().json(   "@mystage/car_sales.json").select(     Functions.col("$1").subField(0).subField("salesperson").subField("name"));  df.show(); ``` |

Expand

Show lessSee more

### Copying data from files in a stage to a table

To copy data from files in a stage to a table, use [DataFrameReader](../reference/scala/com/snowflake/snowpark/DataFrameReader.html) to create a [CopyableDataFrame](../reference/scala/com/snowflake/snowpark/CopyableDataFrame.html) for the data, and use the
[copyInto](../reference/java/com/snowflake/snowpark_java/CopyableDataFrame.html#copyInto(java.lang.String)) method to copy the data to the table. See [Copying Data from Files into a Table](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-copy-into-table).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` COPY INTO new_car_sales   FROM @mystage/car_sales.json   FILE_FORMAT = (TYPE = JSON); ``` | Copy code  ``` CopyableDataFrame dfCopyableDf = session.read().json("@mystage/car_sales.json"); dfCopyableDf.copyInto("new_car_sales"); ``` |

Expand

Show lessSee more

### Saving a DataFrame to files on a stage

To save a DataFrame to files on a stage, use the [DataFrameWriter](../reference/scala/com/snowflake/snowpark/DataFrameWriter.html) method named after the format of the files that you want to
use. See [Saving a DataFrame to Files on a Stage](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-stages-copy-into-location).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` COPY INTO @mystage/saved_data.json   FROM (  SELECT  *  FROM (car_sales) )   FILE_FORMAT = ( TYPE = JSON COMPRESSION = 'none' )   OVERWRITE = TRUE   DETAILED_OUTPUT = TRUE ``` | Copy code  ``` DataFrame df = session.table("car_sales");  WriteFileResult writeFileResult = df.write().mode(   SaveMode.Overwrite).option(   "DETAILED_OUTPUT", "TRUE").option(   "compression", "none").json(   "@mystage/saved_data.json"); ``` |

Expand

Show lessSee more

## Creating and calling user-defined functions (UDFs)

To create an anonymous UDF, use [Functions.udf](../reference/java/com/snowflake/snowpark_java/Functions.html#udf(com.snowflake.snowpark_java.udf.JavaUDF0,com.snowflake.snowpark_java.types.DataType)).

To create a temporary or permanent UDF that you can call by name, use [UDFRegistration.registerTemporary](../reference/scala/com/snowflake/snowpark/UDFRegistration.html#registerTemporary%5BRT,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22%5D(name:String,func:(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)=%3ERT)(implicitevidence$530:reflect.runtime.universe.TypeTag%5BRT%5D,implicitevidence$531:reflect.runtime.universe.TypeTag%5BA1%5D,implicitevidence$532:reflect.runtime.universe.TypeTag%5BA2%5D,implicitevidence$533:reflect.runtime.universe.TypeTag%5BA3%5D,implicitevidence$534:reflect.runtime.universe.TypeTag%5BA4%5D,implicitevidence$535:reflect.runtime.universe.TypeTag%5BA5%5D,implicitevidence$536:reflect.runtime.universe.TypeTag%5BA6%5D,implicitevidence$537:reflect.runtime.universe.TypeTag%5BA7%5D,implicitevidence$538:reflect.runtime.universe.TypeTag%5BA8%5D,implicitevidence$539:reflect.runtime.universe.TypeTag%5BA9%5D,implicitevidence$540:reflect.runtime.universe.TypeTag%5BA10%5D,implicitevidence$541:reflect.runtime.universe.TypeTag%5BA11%5D,implicitevidence$542:reflect.runtime.universe.TypeTag%5BA12%5D,implicitevidence$543:reflect.runtime.universe.TypeTag%5BA13%5D,implicitevidence$544:reflect.runtime.universe.TypeTag%5BA14%5D,implicitevidence$545:reflect.runtime.universe.TypeTag%5BA15%5D,implicitevidence$546:reflect.runtime.universe.TypeTag%5BA16%5D,implicitevidence$547:reflect.runtime.universe.TypeTag%5BA17%5D,implicitevidence$548:reflect.runtime.universe.TypeTag%5BA18%5D,implicitevidence$549:reflect.runtime.universe.TypeTag%5BA19%5D,implicitevidence$550:reflect.runtime.universe.TypeTag%5BA20%5D,implicitevidence$551:reflect.runtime.universe.TypeTag%5BA21%5D,implicitevidence$552:reflect.runtime.universe.TypeTag%5BA22%5D):com.snowflake.snowpark.UserDefinedFunction) or
[UDFRegistration.registerPermanent](../reference/scala/com/snowflake/snowpark/UDFRegistration.html#registerPermanent%5BRT,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22%5D(name:String,func:(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)=%3ERT,stageLocation:String)(implicitevidence$806:reflect.runtime.universe.TypeTag%5BRT%5D,implicitevidence$807:reflect.runtime.universe.TypeTag%5BA1%5D,implicitevidence$808:reflect.runtime.universe.TypeTag%5BA2%5D,implicitevidence$809:reflect.runtime.universe.TypeTag%5BA3%5D,implicitevidence$810:reflect.runtime.universe.TypeTag%5BA4%5D,implicitevidence$811:reflect.runtime.universe.TypeTag%5BA5%5D,implicitevidence$812:reflect.runtime.universe.TypeTag%5BA6%5D,implicitevidence$813:reflect.runtime.universe.TypeTag%5BA7%5D,implicitevidence$814:reflect.runtime.universe.TypeTag%5BA8%5D,implicitevidence$815:reflect.runtime.universe.TypeTag%5BA9%5D,implicitevidence$816:reflect.runtime.universe.TypeTag%5BA10%5D,implicitevidence$817:reflect.runtime.universe.TypeTag%5BA11%5D,implicitevidence$818:reflect.runtime.universe.TypeTag%5BA12%5D,implicitevidence$819:reflect.runtime.universe.TypeTag%5BA13%5D,implicitevidence$820:reflect.runtime.universe.TypeTag%5BA14%5D,implicitevidence$821:reflect.runtime.universe.TypeTag%5BA15%5D,implicitevidence$822:reflect.runtime.universe.TypeTag%5BA16%5D,implicitevidence$823:reflect.runtime.universe.TypeTag%5BA17%5D,implicitevidence$824:reflect.runtime.universe.TypeTag%5BA18%5D,implicitevidence$825:reflect.runtime.universe.TypeTag%5BA19%5D,implicitevidence$826:reflect.runtime.universe.TypeTag%5BA20%5D,implicitevidence$827:reflect.runtime.universe.TypeTag%5BA21%5D,implicitevidence$828:reflect.runtime.universe.TypeTag%5BA22%5D):com.snowflake.snowpark.UserDefinedFunction).

To call a permanent UDF by name, use [Functions.callUDF](../reference/java/com/snowflake/snowpark_java/Functions.html#callUDF(java.lang.String,com.snowflake.snowpark_java.Column...)).

For details, see [Creating User-Defined Functions (UDFs) for DataFrames in Java](/developer-guide/snowpark/java/creating-udfs) and [Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/java/calling-functions#label-snowpark-java-udfs-calling).

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE FUNCTION <temp_function_name>   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   <temp_function_name>(quantity) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` UserDefinedFunction doubleUdf =   Functions.udf(     (Integer x) -> x + x,     DataTypes.IntegerType,     DataTypes.IntegerType);  DataFrame df = session.table("sample_product_data");  DataFrame dfWithDoubleNum =   df.withColumn("doubleNum",     doubleUdf.apply(Functions.col("quantity")));  dfWithDoubleNum.show(); ``` |
| Copy code  ``` CREATE FUNCTION <temp_function_name>   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   <temp_function_name>(quantity) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` UserDefinedFunction doubleUdf =   session     .udf()     .registerTemporary(       "doubleUdf",       (Integer x) -> x + x,       DataTypes.IntegerType,       DataTypes.IntegerType);  DataFrame df = session.table("sample_product_data");  DataFrame dfWithDoubleNum =   df.withColumn("doubleNum",     Functions.callUDF("doubleUdf", Functions.col("quantity"))); dfWithDoubleNum.show(); ``` |
| Copy code  ``` CREATE FUNCTION doubleUdf(arg1 INT)   RETURNS INT   LANGUAGE JAVA   ...   AS   ...;  SELECT ...,   doubleUdf(quantity) AS doublenum   FROM sample_product_data; ``` | Copy code  ``` UserDefinedFunction doubleUdf =   session     .udf()     .registerPermanent(       "doubleUdf",       (Integer x) -> x + x,       DataTypes.IntegerType,       DataTypes.IntegerType,       "mystage");  DataFrame df = session.table("sample_product_data");  DataFrame dfWithDoubleNum =   df.withColumn("doubleNum",     Functions.callUDF("doubleUdf", Functions.col("quantity"))); dfWithDoubleNum.show(); ``` |

Expand

Show lessSee more

## Creating and calling stored procedures

For a guide on creating stored procedures with Snowpark, see [Creating stored procedures for DataFrames in Java](/developer-guide/snowpark/java/creating-sprocs).

- To create an anonymous or named temporary procedure, use a `registerTemporary` method of [com.snowflake.snowpark\_java.SProcRegistration](../reference/java/com/snowflake/snowpark_java/SProcRegistration.html).
- To create a named permanent procedure, use a `registerPermanent` method of the [com.snowflake.snowpark\_java.SProcRegistration](../reference/java/com/snowflake/snowpark_java/SProcRegistration.html) class.
- To call a procedure, use the `storedProcedure` method of the [com.snowflake.snowpark\_java.Session](../reference/java/com/snowflake/snowpark_java/Session.html) class.

| Example of a SQL Statement | Example of Snowpark Code |
| --- | --- |
| Copy code  ``` CREATE PROCEDURE <temp_procedure_name>(x INTEGER, y INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN     RETURN x + y;   END   $$   ;  CALL <temp_procedure_name>(2, 3); ``` | Copy code  ``` StoredProcedure sp =   session.sproc().registerTemporary((Session session, Integer x, Integer y) -> x + y,     new DataType[] {DataTypes.IntegerType, DataTypes.IntegerType},     DataTypes.IntegerType);    session.storedProcedure(sp, 2, 3).show(); ``` |
| Copy code  ``` CREATE PROCEDURE sproc(x INTEGER, y INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN    RETURN x + y;   END   $$   ;  CALL sproc(2, 3); ``` | Copy code  ``` String name = "sproc";  StoredProcedure sp =   session.sproc().registerTemporary(name,     (Session session, Integer x, Integer y) -> x + y,     new DataType[] {DataTypes.IntegerType, DataTypes.IntegerType},     DataTypes.IntegerType);    session.storedProcedure(name, 2, 3).show(); ``` |
| Copy code  ``` CREATE PROCEDURE add_hundred(x INTEGER)   RETURNS INTEGER   LANGUAGE JAVA   ...   AS   $$   BEGIN    RETURN x + 100;   END   $$   ;  CALL add_hundred(3); ``` | Copy code  ``` String name = "add_hundred"; String stageName = "sproc_libs";  StoredProcedure sp =   session.sproc().registerPermanent(     name,     (Session session, Integer x) -> x + 100,     DataTypes.IntegerType,     DataTypes.IntegerType,     stageName,     true);    session.storedProcedure(name, 3).show(); ``` |

Expand

Show lessSee more
