# Snowpark Migration Accelerator: Issue Codes for Spark - Scala

## SPRKSCL1126

Message: org.apache.spark.sql.functions.covar\_pop has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.covar\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

**Input**

Below is an example of the `org.apache.spark.sql.functions.covar_pop` function, first used with column names as the arguments and then with column objects.

Copy code

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

val result1 = df.select(covar_pop("column1", "column2").as("covariance_pop"))
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

**Output**

The SMA adds the EWI `SPRKSCL1126` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

/*EWI: SPRKSCL1126 => org.apache.spark.sql.functions.covar_pop has a workaround, see documentation for more info*/
val result1 = df.select(covar_pop("column1", "column2").as("covariance_pop"))
/*EWI: SPRKSCL1126 => org.apache.spark.sql.functions.covar_pop has a workaround, see documentation for more info*/
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

**Recommended fix**

Snowpark has an equivalent [covar\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html#covar_pop(column1:com.snowflake.snowpark.Column,column2:com.snowflake.snowpark.Column):com.snowflake.snowpark.Column) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html#col(colName:String):com.snowflake.snowpark.Column) function as a workaround.

Copy code

```
val df = Seq(
  (10.0, 100.0),
  (20.0, 150.0),
  (30.0, 200.0),
  (40.0, 250.0),
  (50.0, 300.0)
).toDF("column1", "column2")

val result1 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
val result2 = df.select(covar_pop(col("column1"), col("column2")).as("covariance_pop"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1112

Message: ***spark element*** is not supported

Category: Conversion error

### Description

This issue appears when the SMA detects the use of a Spark element that is not supported by Snowpark, and it does not have its own error code associated with it. This is a generic error code used by the SMA for any unsupported Spark element.

#### Scenario

**Input**

Below is an example of a Spark element that is not supported by Snowpark, and therefore it generates this EWI.

Copy code

```
val df = session.range(10)
val result = df.isLocal
```

**Output**

The SMA adds the EWI `SPRKSCL1112` to the output code to let you know that this element is not supported by Snowpark.

Copy code

```
val df = session.range(10)
/*EWI: SPRKSCL1112 => org.apache.spark.sql.Dataset.isLocal is not supported*/
val result = df.isLocal
```

**Recommended fix**

Since this is a generic error code that applies to a range of unsupported functions, there is not a single and specific fix. The appropriate action will depend on the particular element in use.

Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It only means that the SMA itself cannot find the solution.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1143

Message: An error occurred when loading the symbol table

Category: Conversion error

### Description

This issue appears when there is an error loading the symbols of the SMA symbol table. The symbol table is part of the underlying architecture of the SMA allowing for more complex conversions.

#### Additional recommendations

- This is unlikely to be an error in the source code itself, but rather is an error in how the SMA processes the source code. The best resolution would be to post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1153

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.3.2](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.max has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.max](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.max` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
val result1 = df.select(max("value"))
val result2 = df.select(max(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1153` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
/*EWI: SPRKSCL1153 => org.apache.spark.sql.functions.max has a workaround, see documentation for more info*/
val result1 = df.select(max("value"))
/*EWI: SPRKSCL1153 => org.apache.spark.sql.functions.max has a workaround, see documentation for more info*/
val result2 = df.select(max(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [max](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(10, 12, 20, 15, 18).toDF("value")
val result1 = df.select(max(col("value")))
val result2 = df.select(max(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1102

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](/migrations/sma-docs/general/release-notes/README)

Message:Explode is not supported

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.explode](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which is not supported by Snowpark.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.explode` function used to get the consolidated information of the array fields of the dataset.

Copy code

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

    dfExplode.select(explode(dfExplode("Translation").alias("exploded")))
```

**Output**

The SMA adds the EWI `SPRKSCL1102` to the output code to let you know that this function is not supported by Snowpark.

Copy code

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

    /*EWI: SPRKSCL1102 => Explode is not supported */
    dfExplode.select(explode(dfExplode("Translation").alias("exploded")))
```

**Recommended Fix**

Since explode is not supported by Snowpark, the function [flatten](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/DataFrame.html) could be used as a substitute.

The following fix creates flatten of the dfExplode dataframe, then makes the query to replicate the result in Spark.

Copy code

```
    val explodeData = Seq(
      Row("Cat", Array("Gato","Chat")),
      Row("Dog", Array("Perro","Chien")),
      Row("Bird", Array("Ave","Oiseau"))
    )

    val explodeSchema = StructType(
      List(
        StructField("Animal", StringType),
        StructField("Translation", ArrayType(StringType))
      )
    )

    val rddExplode = session.sparkContext.parallelize(explodeData)

    val dfExplode = session.createDataFrame(rddExplode, explodeSchema)

     var dfFlatten = dfExplode.flatten(col("Translation")).alias("exploded")
                              .select(col("exploded.value").alias("Translation"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1136

Warning

This issue code is **deprecated** since [Spark Conversion Core 4.3.2](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.min has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.min](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.min` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(min("value"))
val result2 = df.select(min(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1136` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
/*EWI: SPRKSCL1136 => org.apache.spark.sql.functions.min has a workaround, see documentation for more info*/
val result1 = df.select(min("value"))
/*EWI: SPRKSCL1136 => org.apache.spark.sql.functions.min has a workaround, see documentation for more info*/
val result2 = df.select(min(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [min](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that takes a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(min(col("value")))
val result2 = df.select(min(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1167

Message: Project file not found on input folder

Category: Warning

### Description

This issue appears when the SMA detects that input folder does not have any project configuration file. The project configuration files supported by the SMA are:

- build.sbt
- build.gradle
- pom.xml

#### Additional recommendations

- Include a configuration project file on input folder.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1147

Message: org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.tanh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.tanh` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
val result1 = df.withColumn("tanh_value", tanh("value"))
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1147` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
/*EWI: SPRKSCL1147 => org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info*/
val result1 = df.withColumn("tanh_value", tanh("value"))
/*EWI: SPRKSCL1147 => org.apache.spark.sql.functions.tanh has a workaround, see documentation for more info*/
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [tanh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(-1.0, 0.5, 1.0, 2.0).toDF("value")
val result1 = df.withColumn("tanh_value", tanh(col("value")))
val result2 = df.withColumn("tanh_value", tanh(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1116

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.40.1](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.split has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.split](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI.

Copy code

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
val result1 = df.withColumn("split_values", split(col("values"), ","))
val result2 = df.withColumn("split_values", split(col("values"), ",", 0))
```

**Output**

The SMA adds the EWI `SPRKSCL1116` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
/*EWI: SPRKSCL1116 => org.apache.spark.sql.functions.split has a workaround, see documentation for more info*/
val result1 = df.withColumn("split_values", split(col("values"), ","))
/*EWI: SPRKSCL1116 => org.apache.spark.sql.functions.split has a workaround, see documentation for more info*/
val result2 = df.withColumn("split_values", split(col("values"), ",", 0))
```

**Recommended fix**

For the Spark overload that receives two arguments, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

The overload that receives three arguments is not yet supported by Snowpark and there is no workaround.

Copy code

```
val df = Seq("apple,banana,orange", "grape,lemon,lime", "cherry,blueberry,strawberry").toDF("values")
val result1 = df.withColumn("split_values", split(col("values"), lit(",")))
val result2 = df.withColumn("split_values", split(col("values"), ",", 0)) // This overload is not supported yet
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1122

Message: org.apache.spark.sql.functions.corr has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.corr](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.corr` function, first used with column names as the arguments and then with column objects.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

val result1 = df.select(corr("col1", "col2"))
val result2 = df.select(corr(col("col1"), col("col2")))
```

**Output**

The SMA adds the EWI `SPRKSCL1122` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

/*EWI: SPRKSCL1122 => org.apache.spark.sql.functions.corr has a workaround, see documentation for more info*/
val result1 = df.select(corr("col1", "col2"))
/*EWI: SPRKSCL1122 => org.apache.spark.sql.functions.corr has a workaround, see documentation for more info*/
val result2 = df.select(corr(col("col1"), col("col2")))
```

**Recommended fix**

Snowpark has an equivalent [corr](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives two column objects as arguments. For that reason, the Spark overload that receives column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (20.0, 40.0),
  (30.0, 60.0)
).toDF("col1", "col2")

val result1 = df.select(corr(col("col1"), col("col2")))
val result2 = df.select(corr(col("col1"), col("col2")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1173

Message: SQL embedded code cannot be processed.

Category: Warning.

### Description

This issue appears when the SMA detects a SQL-embedded code that can’t be processed. Then, the SQL-embedded code can’t be converted to Snowflake.

#### Scenario

**Input**

Below is an example of a SQL-embedded code that can’t be processed.

Copy code

```
spark.sql("CREATE VIEW IF EXISTS My View" + "AS Select * From my Table WHERE date < current_date()")
```

**Output**

The SMA adds the EWI `SPRKSCL1173` to the output code to let you know that the SQL-embedded code can’t be processed.

Copy code

```
/*EWI: SPRKSCL1173 => SQL embedded code cannot be processed.*/
spark.sql("CREATE VIEW IF EXISTS My View" + "AS Select * From my Table WHERE date < current_date()")
```

**Recommended fix**

Make sure that the SQL-embedded code is a string without interpolations, variables or string concatenations.

#### Additional recommendations

- You can find more information about SQL-embedded [here](/migrations/sma-docs/translation-reference/sql-embedded-code).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1163

Message: The element is not a literal and can’t be evaluated.

Category: Conversion error.

### Description

This issue occurs when the current processing element is not a literal, then it can’t be evaluated by SMA.

#### Scenario

**Input**

Below is an example when element to process is not a literal and it can’t be evaluated by SMA.

Copy code

```
val format_type = "csv"
spark.read.format(format_type).load(path)
```

**Output**

The SMA adds the EWI `SPRKSCL1163` to the output code to let you know that `format_type` parameter is not a literal and it can’t be evaluated by the SMA.

Copy code

```
/*EWI: SPRKSCL1163 => format_type is not a literal and can't be evaluated*/
val format_type = "csv"
spark.read.format(format_type).load(path)
```

**Recommended fix**

- Make sure that a value of the variable is a valid one in order to avoid unexpected behaviors.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1132

Message: org.apache.spark.sql.functions.grouping\_id has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.grouping\_id](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.grouping_id` function, first used with multiple column name as arguments and then with column objects.

Copy code

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id("store", "product"))
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

**Output**

The SMA adds the EWI `SPRKSCL1132` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

/*EWI: SPRKSCL1132 => org.apache.spark.sql.functions.grouping_id has a workaround, see documentation for more info*/
val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id("store", "product"))
/*EWI: SPRKSCL1132 => org.apache.spark.sql.functions.grouping_id has a workaround, see documentation for more info*/
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

**Recommended fix**

Snowpark has an equivalent [grouping\_id](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives multiple column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("Store1", "Product1", 100),
  ("Store1", "Product2", 150),
  ("Store2", "Product1", 200),
  ("Store2", "Product2", 250)
).toDF("store", "product", "amount")

val result1 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
val result2 = df.cube("store", "product").agg(sum("amount"), grouping_id(col("store"), col("product")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1106

Warning

This issue code has been **deprecated**

Message: Writer option is not supported.

Category: Conversion error.

### Description

This issue appears when the tool detects, in writer statement, the usage of an option not supported by Snowpark.

#### Scenario

**Input**

Below is an example of the [org.apache.spark.sql.DataFrameWriter.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html) used to add options to a writer statement.

Copy code

```
df.write.format("net.snowflake.spark.snowflake").option("dbtable", tablename)
```

**Output**

The SMA adds the EWI `SPRKSCL1106` to the output code to let you know that the option method is not supported by Snowpark.

Copy code

```
df.write.saveAsTable(tablename)
/*EWI: SPRKSCL1106 => Writer option is not supported .option("dbtable", tablename)*/
```

**Recommended fix**

There is no recommended fix for this scenario

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1157

Message: org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.kurtosis](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.kurtosis` function that generates this EWI. In this example, the `kurtosis` function is used to calculate the kurtosis of selected column.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = kurtosis(col("elements"))
val result2 = kurtosis("elements")
```

**Output**

The SMA adds the EWI `SPRKSCL1157` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
/*EWI: SPRKSCL1157 => org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info*/
val result1 = kurtosis(col("elements"))
/*EWI: SPRKSCL1157 => org.apache.spark.sql.functions.kurtosis has a workaround, see documentation for more info*/
val result2 = kurtosis("elements")
```

**Recommended fix**

Snowpark has an equivalent [kurtosis](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = kurtosis(col("elements"))
val result2 = kurtosis(col("elements"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1146

Message: org.apache.spark.sql.functions.tan has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.tan](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.tan` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
val result1 = df.withColumn("tan_value", tan("angle"))
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

**Output**

The SMA adds the EWI `SPRKSCL1146` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
/*EWI: SPRKSCL1146 => org.apache.spark.sql.functions.tan has a workaround, see documentation for more info*/
val result1 = df.withColumn("tan_value", tan("angle"))
/*EWI: SPRKSCL1146 => org.apache.spark.sql.functions.tan has a workaround, see documentation for more info*/
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

**Recommended fix**

Snowpark has an equivalent [tan](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(math.Pi / 4, math.Pi / 3, math.Pi / 6).toDF("angle")
val result1 = df.withColumn("tan_value", tan(col("angle")))
val result2 = df.withColumn("tan_value", tan(col("angle")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1117

Warning

This issue code is **deprecated** since [Spark Conversion Core 2.40.1](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.translate has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.translate](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.translate` function that generates this EWI. In this example, the `translate` function is used to replace the characters **‘a’**, **‘e’** and **‘o’** in each word with **’1’**, **’2’** and **’3’**, respectively.

Copy code

```
val df = Seq("hello", "world", "scala").toDF("word")
val result = df.withColumn("translated_word", translate(col("word"), "aeo", "123"))
```

**Output**

The SMA adds the EWI `SPRKSCL1117` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("hello", "world", "scala").toDF("word")
/*EWI: SPRKSCL1117 => org.apache.spark.sql.functions.translate has a workaround, see documentation for more info*/
val result = df.withColumn("translated_word", translate(col("word"), "aeo", "123"))
```

**Recommended fix**

As a workaround, you can convert the second and third argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq("hello", "world", "scala").toDF("word")
val result = df.withColumn("translated_word", translate(col("word"), lit("aeo"), lit("123")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1123

Message: org.apache.spark.sql.functions.cos has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.cos](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.cos` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
val result1 = df.withColumn("cosine_value", cos("angle_radians"))
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

**Output**

The SMA adds the EWI `SPRKSCL1123` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
/*EWI: SPRKSCL1123 => org.apache.spark.sql.functions.cos has a workaround, see documentation for more info*/
val result1 = df.withColumn("cosine_value", cos("angle_radians"))
/*EWI: SPRKSCL1123 => org.apache.spark.sql.functions.cos has a workaround, see documentation for more info*/
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

**Recommended fix**

Snowpark has an equivalent [cos](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(0.0, Math.PI / 4, Math.PI / 2, Math.PI).toDF("angle_radians")
val result1 = df.withColumn("cosine_value", cos(col("angle_radians")))
val result2 = df.withColumn("cosine_value", cos(col("angle_radians")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1172

Message: Snowpark does not support StructField with metadata parameter.

Category: Warning

### Description

This issue appears when the SMA detects that [org.apache.spark.sql.types.StructField.apply](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/StructField.html) with [org.apache.spark.sql.types.Metadata](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/Metadata.html) as parameter. This is because Snowpark does not support the metadata parameter.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.types.StructField.apply` function that generates this EWI. In this example, the `apply` function is used to generate an instance of StructField.

Copy code

```
val result = StructField("f1", StringType(), True, metadata)
```

**Output**

The SMA adds the EWI `SPRKSCL1172` to the output code to let you know that metadata parameter is not supported by Snowflake.

Copy code

```
/*EWI: SPRKSCL1172 => Snowpark does not support StructField with metadata parameter.*/
val result = StructField("f1", StringType(), True, metadata)
```

**Recommended fix**

Snowpark has an equivalent [com.snowflake.snowpark.types.StructField.apply](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/types/StructField$.html) function that receives three parameters. Then, as workaround, you can try to remove the metadata argument.

Copy code

```
val result = StructField("f1", StringType(), True, metadata)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1162

Note

This issue code has been **deprecated**

Message: An error occurred when extracting the dbc files.

Category: Warning.

### Description

This issue appears when a dbc file cannot be extracted. This warning could be caused by one or more of the following reasons: Too heavy, inaccessible, read-only, etc.

#### Additional recommendations

- As a workaround, you can check the size of the file if it is too heavy to be processed. Also, analyze whether the tool can access it to avoid any access issues.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1133

Message: org.apache.spark.sql.functions.least has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.least](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.least` function, first used with multiple column name as arguments and then with column objects.

Copy code

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
val result1 = df.withColumn("least", least("value1", "value2", "value3"))
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

**Output**

The SMA adds the EWI `SPRKSCL1133` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
/*EWI: SPRKSCL1133 => org.apache.spark.sql.functions.least has a workaround, see documentation for more info*/
val result1 = df.withColumn("least", least("value1", "value2", "value3"))
/*EWI: SPRKSCL1133 => org.apache.spark.sql.functions.least has a workaround, see documentation for more info*/
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

**Recommended fix**

Snowpark has an equivalent [least](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives multiple column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq((10, 20, 5), (15, 25, 30), (7, 14, 3)).toDF("value1", "value2", "value3")
val result1 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
val result2 = df.withColumn("least", least(col("value1"), col("value2"), col("value3")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1107

Warning

This issue code has been **deprecated**

Message: Writer save is not supported.

Category: Conversion error.

### Description

This issue appears when the tool detects, in writer statement, the usage of a writer save method that is not supported by Snowpark.

#### Scenario

**Input**

Below is an example of the [org.apache.spark.sql.DataFrameWriter.save](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html) used to save the DataFrame content.

Copy code

```
df.write.format("net.snowflake.spark.snowflake").save()
```

**Output**

The SMA adds the EWI `SPRKSCL1107` to the output code to let you know that the save method is not supported by Snowpark.

Copy code

```
df.write.saveAsTable(tablename)
/*EWI: SPRKSCL1107 => Writer method is not supported .save()*/
```

**Recommended fix**

There is no recommended fix for this scenario

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1156

Message: org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.degrees](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.degrees` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
val result1 = df.withColumn("degrees", degrees("radians"))
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

**Output**

The SMA adds the EWI `SPRKSCL1156` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
/*EWI: SPRKSCL1156 => org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info*/
val result1 = df.withColumn("degrees", degrees("radians"))
/*EWI: SPRKSCL1156 => org.apache.spark.sql.functions.degrees has a workaround, see documentation for more info*/
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

**Recommended fix**

Snowpark has an equivalent [degrees](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(math.Pi, math.Pi / 2, math.Pi / 4, math.Pi / 6).toDF("radians")
val result1 = df.withColumn("degrees", degrees(col("radians")))
val result2 = df.withColumn("degrees", degrees(col("radians")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1127

Message: org.apache.spark.sql.functions.covar\_samp has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.covar\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.covar_samp` function, first used with column names as the arguments and then with column objects.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

val result1 = df.select(covar_samp("value1", "value2").as("sample_covariance"))
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

**Output**

The SMA adds the EWI `SPRKSCL1127` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

/*EWI: SPRKSCL1127 => org.apache.spark.sql.functions.covar_samp has a workaround, see documentation for more info*/
val result1 = df.select(covar_samp("value1", "value2").as("sample_covariance"))
/*EWI: SPRKSCL1127 => org.apache.spark.sql.functions.covar_samp has a workaround, see documentation for more info*/
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

**Recommended fix**

Snowpark has an equivalent [covar\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives two string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  (10.0, 20.0),
  (15.0, 25.0),
  (20.0, 30.0),
  (25.0, 35.0),
  (30.0, 40.0)
).toDF("value1", "value2")

val result1 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
val result2 = df.select(covar_samp(col("value1"), col("value2")).as("sample_covariance"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1113

Message: org.apache.spark.sql.functions.next\_day has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.next\_day](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.next_day` function, first used with a string as the second argument and then with a column object.

Copy code

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
val result1 = df.withColumn("next_monday", next_day(col("date"), "Mon"))
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

**Output**

The SMA adds the EWI `SPRKSCL1113` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
/*EWI: SPRKSCL1113 => org.apache.spark.sql.functions.next_day has a workaround, see documentation for more info*/
val result1 = df.withColumn("next_monday", next_day(col("date"), "Mon"))
/*EWI: SPRKSCL1113 => org.apache.spark.sql.functions.next_day has a workaround, see documentation for more info*/
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

**Recommended fix**

Snowpark has an equivalent [next\_day](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives two column objects as arguments. For that reason, the Spark overload that receives two column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives a column object and a string, you can convert the string into a column object using the [com.snowflake.snowpark.functions.lit](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function as a workaround.

Copy code

```
val df = Seq("2024-11-06", "2024-11-13", "2024-11-20").toDF("date")
val result1 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
val result2 = df.withColumn("next_monday", next_day(col("date"), lit("Mon")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1002

Message: This code section has recovery from parsing errors ***statement***

Category: Parsing error.

### Description

This issue appears when the SMA detects some statement that it cannot correctly read or understand in the code of a file — this is called a **parsing error**. However, the SMA can recover from that parsing error and continue analyzing the code of the file. In this case, the SMA is able to process the code of the file without errors.

#### Scenario

**Input**

Below is an example of invalid Scala code where the SMA can recovery.

Copy code

```
Class myClass {

    def function1() & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

**Output**

The SMA adds the EWI `SPRKSCL1002` to the output code to let you know that the code of the file has parsing errors, however the SMA can recovery from that error and continue analyzing the code of the file.

Copy code

```
class myClass {

    def function1();//EWI: SPRKSCL1002 => Unexpected end of declaration. Failed token: '&' @(3,21).
    & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

**Recommended fix**

Since the message pinpoint the error in the statement you can try to identify the invalid syntax and remove it or comment out that statement to avoid the parsing error.

Copy code

```
Class myClass {

    def function1() = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

Copy code

```
Class myClass {

    // def function1() & = { 1 }

    def function2() = { 2 }

    def function3() = { 3 }

}
```

#### Additional recommendations

- Check that the code of the file is a valid Scala code.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1142

Message: ***spark element*** is not defined

Category: Conversion error

### Description

This issue appears when the SMA could not determine an appropriate mapping status for the given element. This means, the SMA doesn’t know yet if this element is supported or not by Snowpark. Please note, this is a generic error code used by the SMA for any not defined element.

#### Scenario

**Input**

Below is an example of a function for which the SMA could not determine an appropriate mapping status, and therefore it generated this EWI. In this case, you should assume that `notDefinedFunction()` is a valid Spark function and the code runs.

Copy code

```
val df = session.range(10)
val result = df.notDefinedFunction()
```

**Output**

The SMA adds the EWI `SPRKSCL1142` to the output code to let you know that this element is not defined.

Copy code

```
val df = session.range(10)
/*EWI: SPRKSCL1142 => org.apache.spark.sql.DataFrame.notDefinedFunction is not defined*/
val result = df.notDefinedFunction()
```

**Recommended fix**

To try to identify the problem, you can perform the following validations:

- Check if it is a valid Spark element.
- Check if the element has the correct syntax and it is spelled correctly.
- Check if you are using a Spark version supported by the SMA.

If this is a valid Spark element, please report that you encountered a conversion error on that particular element using the [Report an Issue](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) option of the SMA and include any additional information that you think may be helpful.

Please note that if an element is not defined by the SMA, it does not mean necessarily that it is not supported by Snowpark. You should check the [Snowpark Documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/index.html) to verify if an equivalent element exist.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1152

Message: org.apache.spark.sql.functions.variance has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.variance](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.variance` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
val result1 = df.select(variance("value"))
val result2 = df.select(variance(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1152` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
/*EWI: SPRKSCL1152 => org.apache.spark.sql.functions.variance has a workaround, see documentation for more info*/
val result1 = df.select(variance("value"))
/*EWI: SPRKSCL1152 => org.apache.spark.sql.functions.variance has a workaround, see documentation for more info*/
val result2 = df.select(variance(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [variance](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(10, 20, 30, 40, 50).toDF("value")
val result1 = df.select(variance(col("value")))
val result2 = df.select(variance(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1103

This issue code has been **deprecated**

Message: SparkBuilder method is not supported ***method name***

Category: Conversion Error

### Description

This issue appears when the SMA detects a method that is not supported by Snowflake in the SparkBuilder method chaining. Therefore, it might affect the migration of the reader statement.

The following are the not supported SparkBuilder methods:

- master
- appName
- enableHiveSupport
- withExtensions

#### Scenario

**Input**

Below is an example of a SparkBuilder method chaining with many methods are not supported by Snowflake.

Copy code

```
val spark = SparkSession.builder()
           .master("local")
           .appName("testApp")
           .config("spark.sql.broadcastTimeout", "3600")
           .enableHiveSupport()
           .getOrCreate()
```

**Output**

The SMA adds the EWI `SPRKSCL1103` to the output code to let you know that master, appName and enableHiveSupport methods are not supported by Snowpark. Then, it might affect the migration of the Spark Session statement.

Copy code

```
val spark = Session.builder.configFile("connection.properties")
/*EWI: SPRKSCL1103 => SparkBuilder Method is not supported .master("local")*/
/*EWI: SPRKSCL1103 => SparkBuilder Method is not supported .appName("testApp")*/
/*EWI: SPRKSCL1103 => SparkBuilder method is not supported .enableHiveSupport()*/
.create
```

**Recommended fix**

To create the session is required to add the proper Snowflake Snowpark configuration.

In this example a configs variable is used.

Copy code

```
    val configs = Map (
      "URL" -> "https://<myAccount>.snowflakecomputing.com:<port>",
      "USER" -> <myUserName>,
      "PASSWORD" -> <myPassword>,
      "ROLE" -> <myRole>,
      "WAREHOUSE" -> <myWarehouse>,
      "DB" -> <myDatabase>,
      "SCHEMA" -> <mySchema>
    )
    val session = Session.builder.configs(configs).create
```

Also is recommended the use of a configFile (profile.properties) with the connection information:

Copy code

```
## profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

And with the `Session.builder.configFile` the session can be created:

Copy code

```
val session = Session.builder.configFile("/path/to/properties/file").create
```

### Additional recommendations

- [Developer guide for create a session.](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-session)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1137

Message: org.apache.spark.sql.functions.sin has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sin](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.sin` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
val result1 = df.withColumn("sin_value", sin("angle"))
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

**Output**

The SMA adds the EWI `SPRKSCL1137` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
/*EWI: SPRKSCL1137 => org.apache.spark.sql.functions.sin has a workaround, see documentation for more info*/
val result1 = df.withColumn("sin_value", sin("angle"))
/*EWI: SPRKSCL1137 => org.apache.spark.sql.functions.sin has a workaround, see documentation for more info*/
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

**Recommended fix**

Snowpark has an equivalent [sin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(Math.PI / 2, Math.PI, Math.PI / 6).toDF("angle")
val result1 = df.withColumn("sin_value", sin(col("angle")))
val result2 = df.withColumn("sin_value", sin(col("angle")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1166

Note

This issue code has been **deprecated**

Message: org.apache.spark.sql.DataFrameReader.format is not supported.

Category: Warning.

### Description

This issue appears when the [org.apache.spark.sql.DataFrameReader.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html) has an argument that is not supported by Snowpark.

#### Scenarios

There are some scenarios depending on the type of format you are trying to load. It can be a `supported`, or `non-supported` format.

##### Scenario 1

**Input**

The tool analyzes the type of format that is trying to load, the supported formats are:

- `csv`
- `json`
- `orc`
- `parquet`
- `text`

The below example shows how the tool transforms the `format` method when passing a `csv` value.

Copy code

```
spark.read.format("csv").load(path)
```

**Output**

The tool transforms the `format` method into a `csv` method call when load function has one parameter.

Copy code

```
spark.read.csv(path)
```

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

Copy code

```
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

**Output**

The tool shows the EWI `SPRKSCL1166` indicating that the value `net.snowflake.spark.snowflake` is not supported.

Copy code

```
/*EWI: SPRKSCL1166 => The parameter net.snowflake.spark.snowflake is not supported for org.apache.spark.sql.DataFrameReader.format
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

Copy code

```
val myFormat = "csv"
spark.read.format(myFormat).load(path)
```

**Output**

Since the tool can’t determine the value of the variable in runtime, shows the EWI `SPRKSCL1163` indicating that the value is not supported.

Copy code

```
/*EWI: SPRKSCL1163 => myFormat is not a literal and can't be evaluated
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format(myFormat).load(path)
```

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations

- The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
- The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/DataFrameReader.html)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1118

Message: org.apache.spark.sql.functions.trunc has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.trunc](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.trunc` function that generates this EWI.

Copy code

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

val result = df.withColumn("truncated", trunc(col("date"), "month"))
```

**Output**

The SMA adds the EWI `SPRKSCL1118` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

/*EWI: SPRKSCL1118 => org.apache.spark.sql.functions.trunc has a workaround, see documentation for more info*/
val result = df.withColumn("truncated", trunc(col("date"), "month"))
```

**Recommended fix**

As a workaround, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq(
  Date.valueOf("2024-10-28"),
  Date.valueOf("2023-05-15"),
  Date.valueOf("2022-11-20"),
).toDF("date")

val result = df.withColumn("truncated", trunc(col("date"), lit("month")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1149

Message: org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.toRadians](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.toRadians` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
val result1 = df.withColumn("radians", toRadians("degrees"))
val result2 = df.withColumn("radians", toRadians(col("degrees")))
```

**Output**

The SMA adds the EWI `SPRKSCL1149` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
/*EWI: SPRKSCL1149 => org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info*/
val result1 = df.withColumn("radians", toRadians("degrees"))
/*EWI: SPRKSCL1149 => org.apache.spark.sql.functions.toRadians has a workaround, see documentation for more info*/
val result2 = df.withColumn("radians", toRadians(col("degrees")))
```

**Recommended fix**

As a workaround, you can use the [radians](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq(0, 45, 90, 180, 270).toDF("degrees")
val result1 = df.withColumn("radians", radians(col("degrees")))
val result2 = df.withColumn("radians", radians(col("degrees")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1159

Message: org.apache.spark.sql.functions.stddev\_samp has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.stddev_samp` function that generates this EWI. In this example, the `stddev_samp` function is used to calculate the sample standard deviation of selected column.

Copy code

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
val result1 = stddev_samp(col("elements"))
val result2 = stddev_samp("elements")
```

**Output**

The SMA adds the EWI `SPRKSCL1159` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
/*EWI: SPRKSCL1159 => org.apache.spark.sql.functions.stddev_samp has a workaround, see documentation for more info*/
val result1 = stddev_samp(col("elements"))
/*EWI: SPRKSCL1159 => org.apache.spark.sql.functions.stddev_samp has a workaround, see documentation for more info*/
val result2 = stddev_samp("elements")
```

**Recommended fix**

Snowpark has an equivalent [stddev\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq("1.7", "2.1", "3.0", "4.4", "5.2").toDF("elements")
val result1 = stddev_samp(col("elements"))
val result2 = stddev_samp(col("elements"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1108

Note

This issue code has been **deprecated.**

Message: org.apache.spark.sql.DataFrameReader.format is not supported.

Category: Warning.

### Description

This issue appears when the [org.apache.spark.sql.DataFrameReader.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html) has an argument that is not supported by Snowpark.

#### Scenarios

There are some scenarios depending on the type of format you are trying to load. It can be a `supported`, or `non-supported` format.

##### Scenario 1

**Input**

The tool analyzes the type of format that is trying to load, the supported formats are:

- `csv`
- `json`
- `orc`
- `parquet`
- `text`

The below example shows how the tool transforms the `format` method when passing a `csv` value.

Copy code

```
spark.read.format("csv").load(path)
```

**Output**

The tool transforms the `format` method into a `csv` method call when load function has one parameter.

Copy code

```
spark.read.csv(path)
```

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

Copy code

```
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

**Output**

The tool shows the EWI `SPRKSCL1108` indicating that the value `net.snowflake.spark.snowflake` is not supported.

Copy code

```
/*EWI: SPRKSCL1108 => The parameter net.snowflake.spark.snowflake is not supported for org.apache.spark.sql.DataFrameReader.format
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format("net.snowflake.spark.snowflake").load(path)
```

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

Copy code

```
val myFormat = "csv"
spark.read.format(myFormat).load(path)
```

**Output**

Since the tool can’t determine the value of the variable in runtime, shows the EWI `SPRKSCL1108` indicating that the value is not supported.

Copy code

```
/*EWI: SPRKSCL1108 => myFormat is not a literal and can't be evaluated
  EWI: SPRKSCL1112 => org.apache.spark.sql.DataFrameReader.load(scala.String) is not supported*/
spark.read.format(myFormat).load(path)
```

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations

- The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
- The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/DataFrameReader.html)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1128

Message: org.apache.spark.sql.functions.exp has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.exp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.exp` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("exp_value", exp("value"))
val result2 = df.withColumn("exp_value", exp(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1128` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
/*EWI: SPRKSCL1128 => org.apache.spark.sql.functions.exp has a workaround, see documentation for more info*/
val result1 = df.withColumn("exp_value", exp("value"))
/*EWI: SPRKSCL1128 => org.apache.spark.sql.functions.exp has a workaround, see documentation for more info*/
val result2 = df.withColumn("exp_value", exp(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [exp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("exp_value", exp(col("value")))
val result2 = df.withColumn("exp_value", exp(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1169

Message: ***Spark element*** is missing on the method chaining.

Category: Warning.

### Description

This issue appears when the SMA detects that a Spark element call is missing on the method chaining. SMA needs to know that Spark element to analyze the statement.

#### Scenario

**Input**

Below is an example where load function call is missing on the method chaining.

Copy code

```
val reader = spark.read.format("json")
val df = reader.load(path)
```

**Output**

The SMA adds the EWI `SPRKSCL1169` to the output code to let you know that load function call is missing on the method chaining and SMA can’t analyze the statement.

Copy code

```
/*EWI: SPRKSCL1169 => Function 'org.apache.spark.sql.DataFrameReader.load' is missing on the method chaining*/
val reader = spark.read.format("json")
val df = reader.load(path)
```

**Recommended fix**

Make sure that all function calls of the method chaining are in the same statement.

Copy code

```
val reader = spark.read.format("json").load(path)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1138

Message: org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sinh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.sinh` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("sinh_value", sinh("value"))
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1138` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
/*EWI: SPRKSCL1138 => org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info*/
val result1 = df.withColumn("sinh_value", sinh("value"))
/*EWI: SPRKSCL1138 => org.apache.spark.sql.functions.sinh has a workaround, see documentation for more info*/
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [sinh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, 3.0).toDF("value")
val result1 = df.withColumn("sinh_value", sinh(col("value")))
val result2 = df.withColumn("sinh_value", sinh(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1129

Message: org.apache.spark.sql.functions.floor has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.floor](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.floor` function, first used with a column name as an argument, then with a column object and finally with two column objects.

Copy code

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
val result1 = df.withColumn("floor_value", floor("value"))
val result2 = df.withColumn("floor_value", floor(col("value")))
val result3 = df.withColumn("floor_value", floor(col("value"), lit(1)))
```

**Output**

The SMA adds the EWI `SPRKSCL1129` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result1 = df.withColumn("floor_value", floor("value"))
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result2 = df.withColumn("floor_value", floor(col("value")))
/*EWI: SPRKSCL1129 => org.apache.spark.sql.functions.floor has a workaround, see documentation for more info*/
val result3 = df.withColumn("floor_value", floor(col("value"), lit(1)))
```

**Recommended fix**

Snowpark has an equivalent [floor](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

For the overload that receives a column object and a scale, you can use the [callBuiltin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function to invoke the Snowflake builtin [FLOOR](https://docs.snowflake.com/en/sql-reference/functions/floor) function. To use it, you should pass the string **“floor”** as the first argument, the column as the second argument and the scale as the third argument.

Copy code

```
val df = Seq(4.75, 6.22, 9.99).toDF("value")
val result1 = df.withColumn("floor_value", floor(col("value")))
val result2 = df.withColumn("floor_value", floor(col("value")))
val result3 = df.withColumn("floor_value", callBuiltin("floor", col("value"), lit(1)))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1168

Message: ***Spark element*** with argument(s) value(s) ***given arguments*** is not supported.

Category: Warning.

### Description

This issue appears when the SMA detects that Spark element with the given parameters is not supported.

#### Scenario

**Input**

Below is an example of Spark element which parameter is not supported.

Copy code

```
spark.read.format("text").load(path)
```

**Output**

The SMA adds the EWI `SPRKSCL1168` to the output code to let you know that Spark element with the given parameter is not supported.

Copy code

```
/*EWI: SPRKSCL1168 => org.apache.spark.sql.DataFrameReader.format(scala.String) with argument(s) value(s) (spark.format) is not supported*/
spark.read.format("text").load(path)
```

**Recommended fix**

For this scenario there is no specific fix.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1139

Message: org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sqrt](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.sqrt` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
val result1 = df.withColumn("sqrt_value", sqrt("value"))
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1139` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
/*EWI: SPRKSCL1139 => org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info*/
val result1 = df.withColumn("sqrt_value", sqrt("value"))
/*EWI: SPRKSCL1139 => org.apache.spark.sql.functions.sqrt has a workaround, see documentation for more info*/
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [sqrt](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(4.0, 16.0, 25.0, 36.0).toDF("value")
val result1 = df.withColumn("sqrt_value", sqrt(col("value")))
val result2 = df.withColumn("sqrt_value", sqrt(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1119

Message: org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.Column.endsWith](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Column.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.Column.endsWith` function, first used with a literal string argument and then with a column object argument.

Copy code

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
val result1 = df1.filter(col("email").endsWith(".com"))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
val result2 = df2.filter(col("email").endsWith(col("suffix")))
```

**Output**

The SMA adds the EWI `SPRKSCL1119` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
/*EWI: SPRKSCL1119 => org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info*/
val result1 = df1.filter(col("email").endsWith(".com"))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
/*EWI: SPRKSCL1119 => org.apache.spark.sql.Column.endsWith has a workaround, see documentation for more info*/
val result2 = df2.filter(col("email").endsWith(col("suffix")))
```

**Recommended fix**

As a workaround, you can use the [com.snowflake.snowpark.functions.endswith](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function, where the first argument would be the column whose values will be checked and the second argument the suffix to check against the column values. Please note that if the argument of the Spark’s `endswith` function is a literal string, you should convert it into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df1 = Seq(
  ("Alice", "alice@example.com"),
  ("Bob", "bob@example.org"),
  ("David", "david@example.com")
).toDF("name", "email")
val result1 = df1.filter(endswith(col("email"), lit(".com")))

val df2 = Seq(
  ("Alice", "alice@example.com", ".com"),
  ("Bob", "bob@example.org", ".org"),
  ("David", "david@example.org", ".com")
).toDF("name", "email", "suffix")
val result2 = df2.filter(endswith(col("email"), col("suffix")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1148

Message: org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.toDegrees](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.toDegrees` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
val result1 = df.withColumn("angle_in_degrees", toDegrees("angle_in_radians"))
val result2 = df.withColumn("angle_in_degrees", toDegrees(col("angle_in_radians")))
```

**Output**

The SMA adds the EWI `SPRKSCL1148` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
/*EWI: SPRKSCL1148 => org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info*/
val result1 = df.withColumn("angle_in_degrees", toDegrees("angle_in_radians"))
/*EWI: SPRKSCL1148 => org.apache.spark.sql.functions.toDegrees has a workaround, see documentation for more info*/
val result2 = df.withColumn("angle_in_degrees", toDegrees(col("angle_in_radians")))
```

**Recommended fix**

As a workaround, you can use the [degrees](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq(Math.PI, Math.PI / 2, Math.PI / 4).toDF("angle_in_radians")
val result1 = df.withColumn("angle_in_degrees", degrees(col("angle_in_radians")))
val result2 = df.withColumn("angle_in_degrees", degrees(col("angle_in_radians")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1158

Message: org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.skewness](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.skewness` function that generates this EWI. In this example, the `skewness` function is used to calculate the skewness of selected column.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = skewness(col("elements"))
val result2 = skewness("elements")
```

**Output**

The SMA adds the EWI `SPRKSCL1158` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
/*EWI: SPRKSCL1158 => org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info*/
val result1 = skewness(col("elements"))
/*EWI: SPRKSCL1158 => org.apache.spark.sql.functions.skewness has a workaround, see documentation for more info*/
val result2 = skewness("elements")
```

**Recommended fix**

Snowpark has an equivalent [skew](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq("1", "2", "3").toDF("elements")
val result1 = skew(col("elements"))
val result2 = skew(col("elements"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1109

Note

This issue code has been **deprecated**

Message: The parameter is not defined for org.apache.spark.sql.DataFrameReader.option

Category: Warning

### Description

This issue appears when the SMA detects that giving parameter of [org.apache.spark.sql.DataFrameReader.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html) is not defined.

#### Scenario

**Input**

Below is an example of undefined parameter for `org.apache.spark.sql.DataFrameReader.option` function.

Copy code

```
spark.read.option("header", True).json(path)
```

**Output**

The SMA adds the EWI `SPRKSCL1109` to the output code to let you know that giving parameter to the org.apache.spark.sql.DataFrameReader.option function is not defined.

Copy code

```
/*EWI: SPRKSCL1109 => The parameter header=True is not supported for org.apache.spark.sql.DataFrameReader.option*/
spark.read.option("header", True).json(path)
```

**Recommended fix**

Check the Snowpark documentation for reader format option [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions), in order to identify the defined options.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1114

Message: org.apache.spark.sql.functions.repeat has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.repeat](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.repeat` function that generates this EWI.

Copy code

```
val df = Seq("Hello", "World").toDF("word")
val result = df.withColumn("repeated_word", repeat(col("word"), 3))
```

**Output**

The SMA adds the EWI `SPRKSCL1114` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("Hello", "World").toDF("word")
/*EWI: SPRKSCL1114 => org.apache.spark.sql.functions.repeat has a workaround, see documentation for more info*/
val result = df.withColumn("repeated_word", repeat(col("word"), 3))
```

**Recommended fix**

As a workaround, you can convert the second argument into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq("Hello", "World").toDF("word")
val result = df.withColumn("repeated_word", repeat(col("word"), lit(3)))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1145

Message: org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sumDistinct](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.sumDistinct` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

val result1 = df.groupBy("name").agg(sumDistinct("value"))
val result2 = df.groupBy("name").agg(sumDistinct(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1145` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

/*EWI: SPRKSCL1145 => org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info*/
val result1 = df.groupBy("name").agg(sumDistinct("value"))
/*EWI: SPRKSCL1145 => org.apache.spark.sql.functions.sumDistinct has a workaround, see documentation for more info*/
val result2 = df.groupBy("name").agg(sumDistinct(col("value")))
```

**Recommended fix**

As a workaround, you can use the [sum\_distinct](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function. For the Spark overload that receives a string argument, you additionally have to convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Alice", 10),
  ("Alice", 20),
  ("Bob", 15)
).toDF("name", "value")

val result1 = df.groupBy("name").agg(sum_distinct(col("value")))
val result2 = df.groupBy("name").agg(sum_distinct(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1171

Message: Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info.

Category: Warning.

### Description

This issue appears when the SMA detects that [org.apache.spark.sql.functions.split](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) has more than two parameters or containing regex pattern.

#### Scenarios

The `split` function is used to separate the given column around matches of the given pattern. This Spark function has three overloads.

##### Scenario 1

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has two parameters and the second argument is a string, not a regex pattern.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), "Snow"))
```

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result = df.select(split(col("words"), "Snow"))
```

**Recommended fix**

Snowpark has an equivalent [split](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as a second argument. For that reason, the Spark overload that receives a string argument in the second argument, but it is not a regex pattern, can convert the string into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), lit("Snow")))
```

##### Scenario 2

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has two parameters and the second argument is a regex pattern.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(col("words"), "^([\\d]+-[\\d]+-[\\d])"))
```

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark because regex patterns are not supported by Snowflake.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result = df.select(split(col("words"), "^([\\d]+-[\\d]+-[\\d])"))
```

**Recommended fix**

Since Snowflake does not support regex patterns, try to replace the pattern by a not regex pattern string.

##### Scenario 3

**Input**

Below is an example of the `org.apache.spark.sql.functions.split` function that generates this EWI. In this example, the `split` function has more than two parameters.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
val result = df.select(split(df("words"), "Snow", 3))
```

**Output**

The SMA adds the EWI `SPRKSCL1171` to the output code to let you know that this function is not fully supported by Snowpark, because Snowflake does not have a split function with more than two parameters.

Copy code

```
val df = Seq("Snowflake", "Snowpark", "Snow", "Spark").toDF("words")
/* EWI: SPRKSCL1171 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info. */
val result3 = df.select(split(df("words"), "Snow", 3))
```

**Recommended fix**

Since Snowflake does not support split function with more than two parameters, try to use the split function supported by Snowflake.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1120

Message: org.apache.spark.sql.functions.asin has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.asin](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.asin` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
val result1 = df.select(col("value"), asin("value").as("asin_value"))
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

**Output**

The SMA adds the EWI `SPRKSCL1120` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
/*EWI: SPRKSCL1120 => org.apache.spark.sql.functions.asin has a workaround, see documentation for more info*/
val result1 = df.select(col("value"), asin("value").as("asin_value"))
/*EWI: SPRKSCL1120 => org.apache.spark.sql.functions.asin has a workaround, see documentation for more info*/
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

**Recommended fix**

Snowpark has an equivalent [asin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(0.5, 0.6, -0.5).toDF("value")
val result1 = df.select(col("value"), asin(col("value")).as("asin_value"))
val result2 = df.select(col("value"), asin(col("value")).as("asin_value"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1130

Message: org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.greatest](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.greatest` function, first used with multiple column names as arguments and then with multiple column objects.

Copy code

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

val result1 = df.withColumn("greatest", greatest("value1", "value2", "value3"))
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

**Output**

The SMA adds the EWI `SPRKSCL1130` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

/*EWI: SPRKSCL1130 => org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info*/
val result1 = df.withColumn("greatest", greatest("value1", "value2", "value3"))
/*EWI: SPRKSCL1130 => org.apache.spark.sql.functions.greatest has a workaround, see documentation for more info*/
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

**Recommended fix**

Snowpark has an equivalent [greatest](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives multiple column objects as arguments. For that reason, the Spark overload that receives column objects as arguments is directly supported by Snowpark and does not require any changes.

For the overload that receives multiple string arguments, you can convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("apple", 10, 20, 15),
  ("banana", 5, 25, 18),
  ("mango", 12, 8, 30)
).toDF("fruit", "value1", "value2", "value3")

val result1 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
val result2 = df.withColumn("greatest", greatest(col("value1"), col("value2"), col("value3")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

---

## SPRKSCL1161

Message: Failed to add dependencies.

Category: Conversion error.

### Description

This issue occurs when the SMA detects a Spark version in the project configuration file that is not supported by the SMA, therefore SMA could not add the Snowpark and Snowpark Extensions dependencies to the corresponding project configuration file. If Snowpark dependencies are not added, the migrated code will not compile.

#### Scenarios

There are three possible scenarios: sbt, gradle and pom.xml. The SMA tries to process the project configuration file by removing Spark dependencies and adding Snowpark and Snowpark Extensions dependencies.

##### Scenario 1

**Input**

Below is an example of the `dependencies` section of a `sbt` project configuration file.

Copy code

```
...
libraryDependencies += "org.apache.spark" % "spark-core_2.13" % "3.5.3"
libraryDependencies += "org.apache.spark" % "spark-sql_2.13" % "3.5.3"
...
```

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

Copy code

```
...
libraryDependencies += "org.apache.spark" % "spark-core_2.13" % "3.5.3"
libraryDependencies += "org.apache.spark" % "spark-sql_2.13" % "3.5.3"
...
```

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `sbt` project configuration file.

Copy code

```
...
libraryDependencies += "com.snowflake" % "snowpark" % "1.14.0"
libraryDependencies += "net.mobilize.snowpark-extensions" % "snowparkextensions" % "0.0.18"
...
```

Make sure to use the Snowpark version that best meets your project’s requirements.

##### Scenario 2

**Input**

Below is an example of the `dependencies` section of a `gradle` project configuration file.

Copy code

```
dependencies {
    implementation group: 'org.apache.spark', name: 'spark-core_2.13', version: '3.5.3'
    implementation group: 'org.apache.spark', name: 'spark-sql_2.13', version: '3.5.3'
    ...
}
```

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

Copy code

```
dependencies {
    implementation group: 'org.apache.spark', name: 'spark-core_2.13', version: '3.5.3'
    implementation group: 'org.apache.spark', name: 'spark-sql_2.13', version: '3.5.3'
    ...
}
```

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `gradle` project configuration file.

Copy code

```
dependencies {
    implementation 'com.snowflake:snowpark:1.14.2'
    implementation 'net.mobilize.snowpark-extensions:snowparkextensions:0.0.18'
    ...
}
```

Make sure that dependencies version are according to your project needs.

##### Scenario 3

**Input**

Below is an example of the `dependencies` section of a `pom.xml` project configuration file.

Copy code

```
<dependencies>
  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.13</artifactId>
    <version>3.5.3</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-sql_2.13</artifactId>
    <version>3.5.3</version>
    <scope>compile</scope>
  </dependency>
  ...
</dependencies>
```

**Output**

The SMA adds the EWI `SPRKSCL1161` to the issues inventory since the Spark version is not supported and keeps the output the same.

Copy code

```
<dependencies>
  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.13</artifactId>
    <version>3.5.3</version>
  </dependency>

  <dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-sql_2.13</artifactId>
    <version>3.5.3</version>
    <scope>compile</scope>
  </dependency>
  ...
</dependencies>
```

**Recommended fix**

Manually, remove the Spark dependencies and add Snowpark and Snowpark Extensions dependencies to the `gradle` project configuration file.

Copy code

```
<dependencies>
  <dependency>
    <groupId>com.snowflake</groupId>
    <artifactId>snowpark</artifactId>
    <version>1.14.2</version>
  </dependency>

  <dependency>
    <groupId>net.mobilize.snowpark-extensions</groupId>
    <artifactId>snowparkextensions</artifactId>
    <version>0.0.18</version>
  </dependency>
  ...
</dependencies>
```

Make sure that dependencies version are according to your project needs.

#### Additional recommendations

- Make sure that input has a project configuration file:

  - build.sbt
  - build.gradle
  - pom.xml
- Spark version supported by the SMA is 2.12:3.1.2
- You can check the latest Snowpark version [here](https://github.com/snowflakedb/snowpark-java-scala/releases/latest).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1155

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.3.2](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.countDistinct](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.countDistinct` function, first used with column names as arguments and then with column objects.

Copy code

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

val result1 = df.select(countDistinct("name", "value"))
val result2 = df.select(countDistinct(col("name"), col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1155` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

/*EWI: SPRKSCL1155 => org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info*/
val result1 = df.select(countDistinct("name", "value"))
/*EWI: SPRKSCL1155 => org.apache.spark.sql.functions.countDistinct has a workaround, see documentation for more info*/
val result2 = df.select(countDistinct(col("name"), col("value")))
```

**Recommended fix**

As a workaround, you can use the [count\_distinct](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function. For the Spark overload that receives string arguments, you additionally have to convert the strings into column objects using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val df = Seq(
  ("Alice", 1),
  ("Bob", 2),
  ("Alice", 3),
  ("Bob", 4),
  ("Alice", 1),
  ("Charlie", 5)
).toDF("name", "value")

val result1 = df.select(count_distinct(col("name"), col("value")))
val result2 = df.select(count_distinct(col("name"), col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1104

This issue code has been **deprecated**

Message: Spark Session builder option is not supported.

Category: Conversion Error.

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.SparkSession.Builder.config](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/SparkSession$$Builder.html) function, which is setting an option of the Spark Session and it is not supported by Snowpark.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.SparkSession.Builder.config` function used to set an option in the Spark Session.

Copy code

```
val spark = SparkSession.builder()
           .master("local")
           .appName("testApp")
           .config("spark.sql.broadcastTimeout", "3600")
           .getOrCreate()
```

**Output**

The SMA adds the EWI `SPRKSCL1104` to the output code to let you know config method is not supported by Snowpark. Then, it is not possible to set options in the Spark Session via config function and it might affect the migration of the Spark Session statement.

Copy code

```
val spark = Session.builder.configFile("connection.properties")
/*EWI: SPRKSCL1104 => SparkBuilder Option is not supported .config("spark.sql.broadcastTimeout", "3600")*/
.create()
```

**Recommended fix**

To create the session is required to add the proper Snowflake Snowpark configuration.

In this example a configs variable is used.

Copy code

```
    val configs = Map (
      "URL" -> "https://<myAccount>.snowflakecomputing.com:<port>",
      "USER" -> <myUserName>,
      "PASSWORD" -> <myPassword>,
      "ROLE" -> <myRole>,
      "WAREHOUSE" -> <myWarehouse>,
      "DB" -> <myDatabase>,
      "SCHEMA" -> <mySchema>
    )
    val session = Session.builder.configs(configs).create
```

Also is recommended the use of a configFile (profile.properties) with the connection information:

Copy code

```
## profile.properties file (a text file)
URL = https://<account_identifier>.snowflakecomputing.com
USER = <username>
PRIVATEKEY = <unencrypted_private_key_from_the_private_key_file>
ROLE = <role_name>
WAREHOUSE = <warehouse_name>
DB = <database_name>
SCHEMA = <schema_name>
```

And with the `Session.builder.configFile` the session can be created:

Copy code

```
val session = Session.builder.configFile("/path/to/properties/file").create
```

### Additional recommendations

- [Developer guide for create a session.](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-session)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1124

Message: org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.cosh](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.cosh` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
val result1 = df.withColumn("cosh_value", cosh("value"))
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1124` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
/*EWI: SPRKSCL1124 => org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info*/
val result1 = df.withColumn("cosh_value", cosh("value"))
/*EWI: SPRKSCL1124 => org.apache.spark.sql.functions.cosh has a workaround, see documentation for more info*/
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [cosh](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(0.0, 1.0, 2.0, -1.0).toDF("value")
val result1 = df.withColumn("cosh_value", cosh(col("value")))
val result2 = df.withColumn("cosh_value", cosh(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1175

Message: The two-parameter `udf` function is not supported in Snowpark. It should be converted into a single-parameter `udf` function. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.

Category: Conversion error.

### Description

This issue appears when the SMA detects an use of the two-parameter [org.apache.spark.sql.functions.udf](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function in the source code, because Snowpark does not have an equivalent two-parameter `udf` function, then the output code might not compile.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.udf` function that generates this EWI. In this example, the `udf` function has two parameters.

Copy code

```
val myFuncUdf = udf(new UDF1[String, Integer] {
  override def call(s: String): Integer = s.length()
}, IntegerType)
```

**Output**

The SMA adds the EWI `SPRKSCL1175` to the output code to let you know that the `udf` function is not supported, because it has two parameters.

Copy code

```
/*EWI: SPRKSCL1175 => The two-parameter udf function is not supported in Snowpark. It should be converted into a single-parameter udf function. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
val myFuncUdf = udf(new UDF1[String, Integer] {
  override def call(s: String): Integer = s.length()
}, IntegerType)
```

**Recommended fix**

Snowpark only supports the single-parameter `udf` function (without the return type parameter), so you should convert your two-parameter `udf` function into a single-parameter `udf` function in order to make it work in Snowpark.

For example, for the sample code mentioned above, you would have to manually convert it into this:

Copy code

```
val myFuncUdf = udf((s: String) => s.length())
```

Please note that there are some caveats about creating `udf` in Snowpark that might require you to make some additional manual changes to your code. Please check these other recommendations related to creating single-parameter `udf` functions in Snowpark for more details.

#### Additional recommendations

- To learn more about how to create user-defined functions in Snowpark, please refer to the following documentation: [Creating User-Defined Functions (UDFs) for DataFrames in Scala](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1001

Message: This code section has parsing errors. The parsing error was found at: line ***line number***, column ***column number***. When trying to parse ***statement***. This file was not converted, so it is expected to still have references to the Spark API.

Category: Parsing error.

### Description

This issue appears when the SMA detects some statement that it cannot correctly read or understand in the code of a file — this is called a **parsing error**. Besides, this issue appears when a file has one or more parsing error(s).

#### Scenario

**Input**

Below is an example of invalid Scala code.

Copy code

```
/#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

**Output**

The SMA adds the EWI `SPRKSCL1001` to the output code to let you know that the code of the file has parsing errors. Therefore, SMA is not able to process a file with this error.

Copy code

```
// **********************************************************************************************************************
// EWI: SPRKSCL1001 => This code section has parsing errors
// The parsing error was found at: line 0, column 0. When trying to parse ''.
// This file was not converted, so it is expected to still have references to the Spark API
// **********************************************************************************************************************
/#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

**Recommended fix**

Since the message pinpoint the error statement you can try to identify the invalid syntax and remove it or comment out that statement to avoid the parsing error.

Copy code

```
Class myClass {

    def function1() = { 1 }

}
```

Copy code

```
// /#/(%$"$%

Class myClass {

    def function1() = { 1 }

}
```

#### Additional recommendations

- Check that the code of the file is a valid Scala code.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1141

Message: org.apache.spark.sql.functions.stddev\_pop has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

Below is an example of the `org.apache.spark.sql.functions.stddev_pop` function, first used with a column name as an argument and then with a column object.

**Input**

Copy code

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

val result1 = df.select(stddev_pop("age"))
val result2 = df.select(stddev_pop(col("age")))
```

**Output**

The SMA adds the EWI `SPRKSCL1141` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

/*EWI: SPRKSCL1141 => org.apache.spark.sql.functions.stddev_pop has a workaround, see documentation for more info*/
val result1 = df.select(stddev_pop("age"))
/*EWI: SPRKSCL1141 => org.apache.spark.sql.functions.stddev_pop has a workaround, see documentation for more info*/
val result2 = df.select(stddev_pop(col("age")))
```

**Recommended fix**

Snowpark has an equivalent [stddev\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("Alice", 23),
  ("Bob", 30),
  ("Carol", 27),
  ("David", 25),
).toDF("name", "age")

val result1 = df.select(stddev_pop(col("age")))
val result2 = df.select(stddev_pop(col("age")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1110

Note

This issue code has been **deprecated**

Message: Reader method not supported ***method name***.

Category: Warning

### Description

This issue appears when the SMA detects a method that is not supported by Snowflake in the DataFrameReader method chaining. Then, it might affect the migration of the reader statement.

#### Scenario

**Input**

Below is an example of a DataFrameReader method chaining where load method is not supported by Snowflake.

Copy code

```
spark.read.
    format("net.snowflake.spark.snowflake").
    option("query", s"select * from $tablename")
    load()
```

**Output**

The SMA adds the EWI `SPRKSCL1110` to the output code to let you know that load method is not supported by Snowpark. Then, it might affect the migration of the reader statement.

Copy code

```
session.sql(s"select * from $tablename")
/*EWI: SPRKSCL1110 => Reader method not supported .load()*/
```

**Recommended fix**

Check the Snowpark documentation for reader [here](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/DataFrameReader.html), in order to know the supported methods by Snowflake.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1100

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](/migrations/sma-docs/general/release-notes/README)

Message: Repartition is not supported.

Category: Parsing error.

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.DataFrame.repartition](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Dataset.html) function, which is not supported by Snowpark. Snowflake manages the storage and the workload on the clusters making repartition operation inapplicable.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.DataFrame.repartition` function used to return a new `DataFrame` partitioned by the given partitioning expressions.

Copy code

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    val dfRepartitionByExpresion = dfName.repartition($"name")

    val dfRepartitionByNumber = dfJob.repartition(3)

    val dfRepartitionByBoth = dfAge.repartition(3, $"age")

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

**Output**

The SMA adds the EWI `SPRKSCL1100` to the output code to let you know that this function is not supported by Snowpark.

Copy code

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByExpresion = dfName.repartition($"name")

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByNumber = dfJob.repartition(3)

    /*EWI: SPRKSCL1100 => Repartition is not supported*/
    val dfRepartitionByBoth = dfAge.repartition(3, $"age")

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

**Recommended Fix**

Since Snowflake manages the storage and the workload on the clusters making repartition operation inapplicable. This means that the use of repartition before the join is not required at all.

Copy code

```
    var nameData = Seq("James", "Sarah", "Dylan", "Leila, "Laura", "Peter")
    var jobData = Seq("Police", "Doctor", "Actor", "Teacher, "Dentist", "Fireman")
    var ageData = Seq(40, 38, 34, 27, 29, 55)

    val dfName = nameData.toDF("name")
    val dfJob = jobData.toDF("job")
    val dfAge = ageData.toDF("age")

    val dfRepartitionByExpresion = dfName

    val dfRepartitionByNumber = dfJob

    val dfRepartitionByBoth = dfAge

    val joinedDf = dfRepartitionByExpresion.join(dfRepartitionByNumber)
```

#### Additional recommendations

- The [Snowflake’s architecture guide](https://docs.snowflake.com/en/user-guide/intro-key-concepts) provides insight about Snowflake storage management.
- Snowpark [Dataframe reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/dataframe) could be useful in how to adapt a particular scenario without the need of repartition.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1151

Message: org.apache.spark.sql.functions.var\_samp has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.var\_samp](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.var_samp` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

val result1 = df.groupBy("category").agg(var_samp("value"))
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1151` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

/*EWI: SPRKSCL1151 => org.apache.spark.sql.functions.var_samp has a workaround, see documentation for more info*/
val result1 = df.groupBy("category").agg(var_samp("value"))
/*EWI: SPRKSCL1151 => org.apache.spark.sql.functions.var_samp has a workaround, see documentation for more info*/
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [var\_samp](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("A", 10),
  ("A", 20),
  ("A", 30),
  ("B", 40),
  ("B", 50),
  ("B", 60)
).toDF("category", "value")

val result1 = df.groupBy("category").agg(var_samp(col("value")))
val result2 = df.groupBy("category").agg(var_samp(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

---

## SPRKSCL1165

Message: Reader format on DataFrameReader method chaining can’t be defined

Category: Warning

### Description

This issue appears when the SMA detects that `format` of the reader in DataFrameReader method chaining is not one of the following supported for Snowpark: `avro`, `csv`, `json`, `orc`, `parquet` and `xml`. Therefore, the SMA can’t determine if setting options are defined or not.

#### Scenario

**Input**

Below is an example of DataFrameReader method chaining where SMA can determine the format of reader.

Copy code

```
spark.read.format("net.snowflake.spark.snowflake")
                 .option("query", s"select * from $tableName")
                 .load()
```

**Output**

The SMA adds the EWI `SPRKSCL1165` to the output code to let you know that `format` of the reader can’t be determine in the giving DataFrameReader method chaining.

Copy code

```
/*EWI: SPRKSCL1165 => Reader format on DataFrameReader method chaining can't be defined*/
spark.read.option("query", s"select * from $tableName")
                 .load()
```

**Recommended fix**

Check the Snowpark documentation [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to get more information about format of the reader.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1134

Message: org.apache.spark.sql.functions.log has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.log](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.log` function that generates this EWI.

Copy code

```
val df = Seq(10.0, 20.0, 30.0, 40.0).toDF("value")
val result1 = df.withColumn("log_value", log(10, "value"))
val result2 = df.withColumn("log_value", log(10, col("value")))
val result3 = df.withColumn("log_value", log("value"))
val result4 = df.withColumn("log_value", log(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1134` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(10.0, 20.0, 30.0, 40.0).toDF("value")
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result1 = df.withColumn("log_value", log(10, "value"))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result2 = df.withColumn("log_value", log(10, col("value")))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result3 = df.withColumn("log_value", log("value"))
/*EWI: SPRKSCL1134 => org.apache.spark.sql.functions.log has a workaround, see documentation for more info*/
val result4 = df.withColumn("log_value", log(col("value")))
```

**Recommended fix**

Below are the different workarounds for all the overloads of the `log` function.

**1. def log(base: Double, columnName: String): Column**

You can convert the base into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function and convert the column name into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val result1 = df.withColumn("log_value", log(lit(10), col("value")))
```

**2. def log(base: Double, a: Column): Column**

You can convert the base into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function.

Copy code

```
val result2 = df.withColumn("log_value", log(lit(10), col("value")))
```

**3.def log(columnName: String): Column**

You can pass `lit(Math.E)` as the first argument and convert the column name into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function and pass it as the second argument.

Copy code

```
val result3 = df.withColumn("log_value", log(lit(Math.E), col("value")))
```

**4. def log(e: Column): Column**

You can pass `lit(Math.E)` as the first argument and the column object as the second argument.

Copy code

```
val result4 = df.withColumn("log_value", log(lit(Math.E), col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1125

Warning

This issue code is **deprecated** since [Spark Conversion Core 2.9.0](/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-scala-release-notes/README)

Message: org.apache.spark.sql.functions.count has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.count](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.count` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

val result1 = df.groupBy("name").agg(count("subject").as("subject_count"))
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

**Output**

The SMA adds the EWI `SPRKSCL1125` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

/*EWI: SPRKSCL1125 => org.apache.spark.sql.functions.count has a workaround, see documentation for more info*/
val result1 = df.groupBy("name").agg(count("subject").as("subject_count"))
/*EWI: SPRKSCL1125 => org.apache.spark.sql.functions.count has a workaround, see documentation for more info*/
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

**Recommended fix**

Snowpark has an equivalent [count](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("Alice", "Math"),
  ("Bob", "Science"),
  ("Alice", "Science"),
  ("Bob", null)
).toDF("name", "subject")

val result1 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
val result2 = df.groupBy("name").agg(count(col("subject")).as("subject_count"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1174

Message: The single-parameter `udf` function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.

Category: Warning.

### Description

This issue appears when the SMA detects an use of the single-parameter [org.apache.spark.sql.functions.udf](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function in the code. Then, it might require a manual intervention.

The Snowpark API provides an equivalent [com.snowflake.snowpark.functions.udf](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that allows you to create a user-defined function from a lambda or function in Scala, however, there are some caveats about creating `udf` in Snowpark that might require you to make some manual changes to your code in order to make it work properly.

#### Scenarios

The Snowpark `udf` function should work as intended for a wide range of cases without requiring manual intervention. However, there are some scenarios that would require you to manually modify your code in order to get it work in Snowpark. Some of those scenarios are listed below:

##### Scenario 1

**Input**

Below is an example of creating UDFs in an object with the App Trait.

The Scala’s `App` trait simplifies creating executable programs by providing a `main` method that automatically runs the code within the object definition. Extending `App` delays the initialization of the fields until the `main` method is executed, which can affect the UDFs definitions if they rely on initialized fields. This means that if an object extends `App` and the `udf` references an object field, the `udf` definition uploaded to Snowflake will not include the initialized value of the field. This can result in `null` values being returned by the `udf`.

For example, in the following code the variable myValue will resolve to `null` in the `udf` definition:

Copy code

```
object Main extends App {
  ...
  val myValue = 10
  val myUdf = udf((x: Int) => x + myValue) // myValue in the `udf` definition will resolve to null
  ...
}
```

**Output**

The SMA adds the EWI `SPRKSCL1174` to the output code to let you know that the single-parameter `udf` function is supported in Snowpark but it requires manual intervention.

Copy code

```
object Main extends App {
  ...
  val myValue = 10
  /*EWI: SPRKSCL1174 => The single-parameter udf function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
  val myUdf = udf((x: Int) => x + myValue) // myValue in the `udf` definition will resolve to null
  ...
}
```

**Recommended fix**

To avoid this issue, it is recommended to not extend `App` and implement a separate `main` method for your code. This ensure that object fields are initialized before `udf` definitions are created and uploaded to Snowflake.

Copy code

```
object Main {
  ...
  def main(args: Array[String]): Unit = {
    val myValue = 10
    val myUdf = udf((x: Int) => x + myValue)
  }
  ...
}
```

For more details about this topic, see [Caveat About Creating UDFs in an Object With the App Trait](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs#caveat-about-creating-udfs-in-an-object-with-the-app-trait).

##### Scenario 2

**Input**

Below is an example of creating UDFs in Jupyter Notebooks.

Copy code

```
def myFunc(s: String): String = {
  ...
}

val myFuncUdf = udf((x: String) => myFunc(x))
df1.select(myFuncUdf(col("name"))).show()
```

**Output**

The SMA adds the EWI `SPRKSCL1174` to the output code to let you know that the single-parameter `udf` function is supported in Snowpark but it requires manual intervention.

Copy code

```
def myFunc(s: String): String = {
  ...
}

/*EWI: SPRKSCL1174 => The single-parameter udf function is supported in Snowpark but it might require manual intervention. Please check the documentation to learn how to manually modify the code to make it work in Snowpark.*/
val myFuncUdf = udf((x: String) => myFunc(x))
df1.select(myFuncUdf(col("name"))).show()
```

**Recommended fix**

To create a `udf` in a Jupyter Notebook, you should define the implementation of your function in a class that extends `Serializable`. For example, you should manually convert it into this:

Copy code

```
object ConvertedUdfFuncs extends Serializable {
  def myFunc(s: String): String = {
    ...
  }

  val myFuncAsLambda = ((x: String) => ConvertedUdfFuncs.myFunc(x))
}

val myFuncUdf = udf(ConvertedUdfFuncs.myFuncAsLambda)
df1.select(myFuncUdf(col("name"))).show()
```

For more details about how to create UDFs in Jupyter Notebooks, see [Creating UDFs in Jupyter Notebooks](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs#creating-udfs-in-jupyter-notebooks).

#### Additional recommendations

- To learn more about how to create user-defined functions in Snowpark, please refer to the following documentation: [Creating User-Defined Functions (UDFs) for DataFrames in Scala](https://docs.snowflake.com/en/developer-guide/snowpark/scala/creating-udfs)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1000

Message: Source project spark-core version is ***version number***, the spark-core version supported by snowpark is 2.12:3.1.2 so there may be functional differences between the existing mappings

Category: Warning

### Description

This issue appears when the SMA detects a version of the `spark-core` that is not supported by SMA. Therefore, there may be functional differences between the existing mappings and the output might have unexpected behaviors.

#### Additional recommendations

- The spark-core version supported by SMA is 2.12:3.1.2. Consider changing the version of your source code.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1140

Message: org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.stddev](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.stddev` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

val result1 = df.select(stddev("score"))
val result2 = df.select(stddev(col("score")))
```

**Output**

The SMA adds the EWI `SPRKSCL1140` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

/*EWI: SPRKSCL1140 => org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info*/
val result1 = df.select(stddev("score"))
/*EWI: SPRKSCL1140 => org.apache.spark.sql.functions.stddev has a workaround, see documentation for more info*/
val result2 = df.select(stddev(col("score")))
```

**Recommended fix**

Snowpark has an equivalent [stddev](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("Alice", 10),
  ("Bob", 15),
  ("Charlie", 20),
  ("David", 25),
).toDF("name", "score")

val result1 = df.select(stddev(col("score")))
val result2 = df.select(stddev(col("score")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1111

Note

This issue code has been **deprecated**

Message: CreateDecimalType is not supported.

Category: Conversion error.

### Description

This issue appears when the SMA detects a usage [org.apache.spark.sql.types.DataTypes.CreateDecimalType](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/types/DecimalType.html) function.

#### Scenario

**Input**

Below is an example of usage of org.apache.spark.sql.types.DataTypes.CreateDecimalType function.

Copy code

```
var result = DataTypes.createDecimalType(18, 8)
```

**Output**

The SMA adds the EWI `SPRKSCL1111` to the output code to let you know that CreateDecimalType function is not supported by Snowpark.

Copy code

```
/*EWI: SPRKSCL1111 => CreateDecimalType is not supported*/
var result = createDecimalType(18, 8)
```

**Recommended fix**

There is not a recommended fix yet.

## SPRKSCL1101

This issue code has been **deprecated** since [Spark Conversion Core 2.3.22](/migrations/sma-docs/general/release-notes/README)

Message: Broadcast is not supported

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.broadcast](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which is not supported by Snowpark. This function is not supported because Snowflake does not support [broadcast variables](https://spark.apache.org/docs/latest/api/java/org/apache/spark/broadcast/Broadcast.html).

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.broadcast` function used to create a broadcast object to use on each Spark cluster:

Copy code

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      broadcast(dfCollege),
      Seq("CollegeName")
    )
```

**Output**

The SMA adds the EWI `SPRKSCL1101` to the output code to let you know that this function is not supported by Snowpark.

Copy code

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      /*EWI: SPRKSCL1101 => Broadcast is not supported*/
      broadcast(dfCollege),
      Seq("CollegeName")
    )
```

**Recommended fix**

Since Snowflake manages the storage and the workload on the clusters making broadcast objects inapplicable. This means that the use of broadcast could not be required at all, but each case should require further analysis.

The recommended approach is replace a Spark dataframe broadcast by a Snowpark regular dataframe or by using a dataframe method as [Join](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrame.join).

For the proposed input the fix is to adapt the join to use directly the dataframe `collegeDF` without the use of broadcast for the dataframe.

Copy code

```
    var studentData = Seq(
      ("James", "Orozco", "Science"),
      ("Andrea", "Larson", "Bussiness"),
    )

    var collegeData = Seq(
      ("Arts", 1),
      ("Bussiness", 2),
      ("Science", 3)
    )

    val dfStudent = studentData.toDF("FirstName", "LastName", "CollegeName")
    val dfCollege = collegeData.toDF("CollegeName", "CollegeCode")

    dfStudent.join(
      dfCollege,
      Seq("CollegeName")
    ).show()
```

#### Additional recommendations

- The [Snowflake’s architecture guide](https://docs.snowflake.com/en/user-guide/intro-key-concepts) provides insight about Snowflake storage management.
- Snowpark [Dataframe reference](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/dataframe) could be useful in how to adapt a particular broadcast scenario.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1150

Message: org.apache.spark.sql.functions.var\_pop has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.var\_pop](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.var_pop` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

val result1 = df.groupBy("group").agg(var_pop("value"))
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1150` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

/*EWI: SPRKSCL1150 => org.apache.spark.sql.functions.var_pop has a workaround, see documentation for more info*/
val result1 = df.groupBy("group").agg(var_pop("value"))
/*EWI: SPRKSCL1150 => org.apache.spark.sql.functions.var_pop has a workaround, see documentation for more info*/
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [var\_pop](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(
  ("A", 10.0),
  ("A", 20.0),
  ("A", 30.0),
  ("B", 40.0),
  ("B", 50.0),
  ("B", 60.0)
).toDF("group", "value")

val result1 = df.groupBy("group").agg(var_pop(col("value")))
val result2 = df.groupBy("group").agg(var_pop(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

---

## SPRKSCL1164

Note

This issue code has been **deprecated**

Message: The parameter is not defined for org.apache.spark.sql.DataFrameReader.option

Category: Warning

### Description

This issue appears when the SMA detects that giving parameter of [org.apache.spark.sql.DataFrameReader.option](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameReader.html) is not defined.

#### Scenario

**Input**

Below is an example of undefined parameter for `org.apache.spark.sql.DataFrameReader.option` function.

Copy code

```
spark.read.option("header", True).json(path)
```

**Output**

The SMA adds the EWI `SPRKSCL1164` to the output code to let you know that giving parameter to the org.apache.spark.sql.DataFrameReader.option function is not defined.

Copy code

```
/*EWI: SPRKSCL1164 => The parameter header=True is not supported for org.apache.spark.sql.DataFrameReader.option*/
spark.read.option("header", True).json(path)
```

**Recommended fix**

Check the Snowpark documentation for reader format option [here](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions), in order to identify the defined options.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1135

Warning

This issue code is **deprecated** since [Spark Conversion Core 4.3.2](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.mean has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.mean](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.mean` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(mean("value"))
val result2 = df.select(mean(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1135` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
/*EWI: SPRKSCL1135 => org.apache.spark.sql.functions.mean has a workaround, see documentation for more info*/
val result1 = df.select(mean("value"))
/*EWI: SPRKSCL1135 => org.apache.spark.sql.functions.mean has a workaround, see documentation for more info*/
val result2 = df.select(mean(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [mean](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(1, 3, 10, 1, 3).toDF("value")
val result1 = df.select(mean(col("value")))
val result2 = df.select(mean(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1115

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.6.0](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.round has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.round](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.round` function that generates this EWI.

Copy code

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
val result1 = df.withColumn("rounded_value", round(col("value")))
val result2 = df.withColumn("rounded_value", round(col("value"), 2))
```

**Output**

The SMA adds the EWI `SPRKSCL1115` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
/*EWI: SPRKSCL1115 => org.apache.spark.sql.functions.round has a workaround, see documentation for more info*/
val result1 = df.withColumn("rounded_value", round(col("value")))
/*EWI: SPRKSCL1115 => org.apache.spark.sql.functions.round has a workaround, see documentation for more info*/
val result2 = df.withColumn("rounded_value", round(col("value"), 2))
```

**Recommended fix**

Snowpark has an equivalent [round](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a column object and a scale, you can convert the scale into a column object using the [com.snowflake.snowpark.functions.lit](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(3.9876, 5.673, 8.1234).toDF("value")
val result1 = df.withColumn("rounded_value", round(col("value")))
val result2 = df.withColumn("rounded_value", round(col("value"), lit(2)))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1144

Message: The symbol table could not be loaded

Category: Parsing error

### Description

This issue appears when there is a critical error in the SMA execution process. Since the symbol table cannot be loaded, the SMA cannot start the assessment or conversion process.

#### Additional recommendations

- This is unlikely to be an error in the source code itself, but rather is an error in how the SMA processes the source code. The best resolution would be to post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1170

Note

This issue code has been **deprecated**

Message: sparkConfig member key is not supported with platform specific key.

Category: Conversion error

### Description

If you are using an older version, please upgrade to the latest.

#### Additional recommendations

- Upgrade your application to the latest version.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1121

Message: org.apache.spark.sql.functions.atan has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.atan](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.atan` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
val result1 = df.withColumn("atan_value", atan("value"))
val result2 = df.withColumn("atan_value", atan(col("value")))
```

**Output**

The SMA adds the EWI `SPRKSCL1121` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
/*EWI: SPRKSCL1121 => org.apache.spark.sql.functions.atan has a workaround, see documentation for more info*/
val result1 = df.withColumn("atan_value", atan("value"))
/*EWI: SPRKSCL1121 => org.apache.spark.sql.functions.atan has a workaround, see documentation for more info*/
val result2 = df.withColumn("atan_value", atan(col("value")))
```

**Recommended fix**

Snowpark has an equivalent [atan](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(1.0, 0.5, -1.0).toDF("value")
val result1 = df.withColumn("atan_value", atan(col("value")))
val result2 = df.withColumn("atan_value", atan(col("value")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1131

Message: org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.grouping](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.grouping` function, first used with a column name as an argument and then with a column object.

Copy code

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
val result1 = df.cube("name").agg(grouping("name"), sum("age"))
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

**Output**

The SMA adds the EWI `SPRKSCL1131` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
/*EWI: SPRKSCL1131 => org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info*/
val result1 = df.cube("name").agg(grouping("name"), sum("age"))
/*EWI: SPRKSCL1131 => org.apache.spark.sql.functions.grouping has a workaround, see documentation for more info*/
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

**Recommended fix**

Snowpark has an equivalent [grouping](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq(("Alice", 2), ("Bob", 5)).toDF("name", "age")
val result1 = df.cube("name").agg(grouping(col("name")), sum("age"))
val result2 = df.cube("name").agg(grouping(col("name")), sum("age"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1160

Note

This issue code has been **deprecated** since [Spark Conversion Core 4.1.0](/migrations/sma-docs/general/release-notes/README)

Message: org.apache.spark.sql.functions.sum has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.sum](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.sum` function that generates this EWI. In this example, the `sum` function is used to calculate the sum of selected column.

Copy code

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
val result1 = sum(col("elements"))
val result2 = sum("elements")
```

**Output**

The SMA adds the EWI `SPRKSCL1160` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
/*EWI: SPRKSCL1160 => org.apache.spark.sql.functions.sum has a workaround, see documentation for more info*/
val result1 = sum(col("elements"))
/*EWI: SPRKSCL1160 => org.apache.spark.sql.functions.sum has a workaround, see documentation for more info*/
val result2 = sum("elements")
```

**Recommended fix**

Snowpark has an equivalent [sum](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

Copy code

```
val df = Seq("1", "2", "3", "4", "5").toDF("elements")
val result1 = sum(col("elements"))
val result2 = sum(col("elements"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1154

Message: org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [org.apache.spark.sql.functions.ceil](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of the `org.apache.spark.sql.functions.ceil` function, first used with a column name as an argument, then with a column object and finally with a column object and a scale.

Copy code

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
val result1 = df.withColumn("ceil", ceil("value"))
val result2 = df.withColumn("ceil", ceil(col("value")))
val result3 = df.withColumn("ceil", ceil(col("value"), lit(1)))
```

**Output**

The SMA adds the EWI `SPRKSCL1154` to the output code to let you know that this function is not fully supported by Snowpark, but it has a workaround.

Copy code

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result1 = df.withColumn("ceil", ceil("value"))
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result2 = df.withColumn("ceil", ceil(col("value")))
/*EWI: SPRKSCL1154 => org.apache.spark.sql.functions.ceil has a workaround, see documentation for more info*/
val result3 = df.withColumn("ceil", ceil(col("value"), lit(1)))
```

**Recommended fix**

Snowpark has an equivalent [ceil](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function that receives a column object as an argument. For that reason, the Spark overload that receives a column object as an argument is directly supported by Snowpark and does not require any changes.

For the overload that receives a string argument, you can convert the string into a column object using the [com.snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function as a workaround.

For the overload that receives a column object and a scale, you can use the [callBuiltin](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/functions$.html) function to invoke the Snowflake builtin [CEIL](https://docs.snowflake.com/en/sql-reference/functions/ceil) function. To use it, you should pass the string **“ceil”** as the first argument, the column as the second argument and the scale as the third argument.

Copy code

```
val df = Seq(2.33, 3.88, 4.11, 5.99).toDF("value")
val result1 = df.withColumn("ceil", ceil(col("value")))
val result2 = df.withColumn("ceil", ceil(col("value")))
val result3 = df.withColumn("ceil", callBuiltin("ceil", col("value"), lit(1)))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKSCL1105

This issue code has been **deprecated**

Message: Writer format value is not supported.

Category: Conversion Error

### Description

This issue appears when the [org.apache.spark.sql.DataFrameWriter.format](https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/DataFrameWriter.html) has an argument that is not supported by Snowpark.

#### Scenarios

There are some scenarios depending on the type of format you are trying to save. It can be a `supported`, or `non-supported` format.

##### Scenario 1

**Input**

The tool analyzes the type of format that is trying to save, the supported formats are:

- `csv`
- `json`
- `orc`
- `parquet`
- `text`

Copy code

```
    dfWrite.write.format("csv").save(path)
```

**Output**

The tool transforms the `format` method into a `csv` method call when save function has one parameter.

Copy code

```
    dfWrite.write.csv(path)
```

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2

**Input**

The below example shows how the tool transforms the `format` method when passing a `net.snowflake.spark.snowflake` value.

Copy code

```
dfWrite.write.format("net.snowflake.spark.snowflake").save(path)
```

**Output**

The tool shows the EWI `SPRKSCL1105` indicating that the value `net.snowflake.spark.snowflake` is not supported.

Copy code

```
/*EWI: SPRKSCL1105 => Writer format value is not supported .format("net.snowflake.spark.snowflake")*/
dfWrite.write.format("net.snowflake.spark.snowflake").save(path)
```

**Recommended fix**

For the `not supported` scenarios there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3

**Input**

The below example shows how the tool transforms the `format` method when passing a `csv`, but using a variable instead.

Copy code

```
val myFormat = "csv"
dfWrite.write.format(myFormat).save(path)
```

**Output**

Since the tool can’t determine the value of the variable in runtime, shows the EWI `SPRKSCL1163` indicating that the value is not supported.

Copy code

```
val myFormat = "csv"
/*EWI: SPRKSCL1163 => myFormat is not a literal and can't be evaluated*/
dfWrite.write.format(myFormat).save(path)
```

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations

- The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
- The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/scala/2.12/com/snowflake/snowpark/DataFrameWriter.html)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).
