description:
:   pyspark.sql.readwriter.DataFrameWriter.options

# Snowpark Migration Accelerator: Issue Codes for Python

## SPRKPY1000

Message: Source project spark-core version is xx.xx:xx.x.x, the spark-core version supported by snowpark is 2.12:3.1.2 so there may be functional differences between the existing mappings.

Category: Warning.

### Description

This issue appears when the Pyspark version of your source code is not supported. This means that there may be functional differences between the existing mappings.

#### Additional recommendations

- The pyspark version scanned by the SMA for compatibility to Snowpark is from 2.12 to 3.1.2. If you are using a version outside this range, the tool may produce inconsistent results. You could alter the version of the source code you are scanning.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](https://snowflakecomputing.atlassian.net/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/371/user-guide/project-overview/configuration-and-settings#report-an-issue).

## SPRKPY1001

Message\*\*:\*\* This code section has parsing errors

Category\*\*:\*\* Parsing error.

### Description

A parsing error is reported by the Snowpark Migration Accelerator (SMA) when it cannot correctly read or understand the code in a file (it cannot correctly “parse” the file). This issue code appears when a file has one or more parsing error(s).

#### Scenario

**Input:** The EWI message appears when the code has invalid syntax, for example:

Copy code

```
def foo():
    x = %%%%%%1###1
```

**Output:** SMA find a parsing error and comment the parsing error adding the corresponding EWI message:

Copy code

```
def foo():
    x
## EWI: SPRKPY1101 => Unrecognized or invalid CODE STATEMENT @(2, 7). Last valid token was 'x' @(2, 5), failed token '=' @(2, 7)
##      = %%%%%%1###1
```

### Additional recommendations

- Check that the file contains valid Python code. (You can use the issues.csv file to find all files with this EWI code to determine which file(s) were not processed by the tool due to parsing error(s).) Many parsing errors occur because only part of the code is input into the tool, so it’s best to ensure that the code will run in the source. If it is valid, report that you encountered a parsing error using the Report an Issue option [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings). Include the line of code that was causing a parsing error in the description when you file this issue.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1002

Message\*\*:\*\* < element > is not supported. Spark element is not supported.

Category\*\*:\*\* Conversion error.

### Description

This issue appears when the tool detects the usage of an element that is not supported in Snowpark, and does not have its own error code associated with it. This is the generic error code used by the SMA for an unsupported element.

#### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It only means that the tool itself cannot find the solution.
- If you have encountered an unsupported element from a pyspark.ml library, consider some alternative approaches. There are additional guides available to walk through issues related to ML such as this one from [Snowflake](https://docs.snowflake.com/en/developer-guide/snowpark/python/snowpark-python-ml).
- Check if the source code has the correct syntax. (You can use the issues.csv file to determine where the conversion error(s) are occurring.) If the syntax is correct, report that you encountered a conversion error on a particular element using the Report an Issue option in the SMA. Include the line of code that was causing the error in the description when you file this issue.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1003

Message\*\*:\*\* An error occurred when loading the symbol table.

Category\*\*:\*\* Conversion error.

### Description

This issue appears when there is an error processing the symbols in the symbol table. The symbol table is part of the underlying architecture of the SMA allowing for more complex conversions. This error could be due to an unexpected statement in the source code.

#### Additional recommendations

- This is unlikely to be an error in the source code itself, but rather is an error in how the tool processes the source code. The best resolution would be to post an issue [in the SMA](https://snowflakecomputing.atlassian.net/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/371/user-guide/project-overview/configuration-and-settings#report-an-issue).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](https://snowflakecomputing.atlassian.net/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/371/user-guide/project-overview/configuration-and-settings#report-an-issue).

## SPRKPY1004

Message\*\*:\*\* The symbol table could not be loaded.

Category\*\*:\*\* Parsing error.

### Description

This issue appears when there is an unexpected error in the tool execution process. Since the symbol table cannot be loaded, the tool cannot start the assessment or conversion process.

#### Additional recommendations

- This is unlikely to be an error in the source code itself, but rather is an error in how the tool processes the source code. The best resolution would be to reach out to [the SMA support team](/migrations/sma-docs/support/contact-us). You can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](https://snowflakecomputing.atlassian.net/o/-MB4z_O8Sl--Tfl3XVml/s/6on4bNAZUZGzMpdEum8X/~/changes/371/user-guide/project-overview/configuration-and-settings#report-an-issue).

## SPRKPY1005

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message\*\*:\*\* pyspark.conf.SparkConf is not required

Category\*\*:\*\* Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.conf.SparkConf](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.html) which is not required.

#### Scenario

**Input**

SparkConf could be called without parameters or with loadDefaults.

Copy code

```
from pyspark import SparkConf

my_conf = SparkConf(loadDefaults=True)
```

**Output**

For both cases (with or without parameters) SMA creates a [Snowpark Session.builder](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.Session.SessionBuilder.configs) object:

Copy code

```
#EWI: SPRKPY1005 => pyspark.conf.SparkConf is not required
#from pyspark import SparkConf
pass

#EWI: SPRKPY1005 => pyspark.conf.SparkConf is not required
my_conf = Session.builder.configs({"user" : "my_user", "password" : "my_password", "account" : "my_account", "role" : "my_role", "warehouse" : "my_warehouse", "database" : "my_database", "schema" : "my_schema"}).create()
```

#### Additional recommendations

- This is an unnecessary parameter being removed with a warning comment being inserted. There should be no additional action from the user.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1006

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message\*\*:\*\* pyspark.context.SparkContext is not required

Category\*\*:\*\* Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.context.SparkContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.html), which is not required in Snowflake.

#### Scenario

**Input**

In this example there are two contexts to create connections to a Spark Cluster

Copy code

```
from pyspark import SparkContext

sql_context1 = SparkContext(my_sc1)
sql_context2 = SparkContext(sparkContext=my_sc2)
```

**Output**

Because there are no clusters on Snowflake the Context is not required, note that the variables my\_sc1 and my\_sc2 that contain Spark properties might not be required or will need to be adapted to fix the code.

Copy code

```
from snowflake.snowpark import Session
#EWI: SPRKPY1006 => pyspark.sql.context.SparkContext is not required
sql_context1 = my_sc1
#EWI: SPRKPY1006 => pyspark.sql.context.SparkContext is not required

sql_context2 = my_sc2
```

#### Additional recommendations

- This is an unnecessary parameter being removed with a warning comment being inserted. There should be no action from the user.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1007

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message\*\*:\*\* pyspark.sql.context.SQLContext is not required

Category\*\*:\*\* Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.context.SQLContext](https://downloads.apache.org/spark/docs/1.6.1/api/python/pyspark.sql.html), which is not required.

#### Scenario

**Input**

Here we have an example with different SparkContext overloads.

Copy code

```
from pyspark import SQLContext
​
my_sc1 = SQLContext(myMaster, myAppName, mySparkHome, myPyFiles, myEnvironment, myBatctSize, mySerializer, my_conf1)
my_sc2 = SQLContext(conf=my_conf2)
my_sc3 = SQLContext()
```

**Output**

The output code has commented the line for pyspark.SQLContext, and replaces the scenarios with a reference to a configuration. Note that the variables my\_sc1 and my\_sc2 that contains Spark properties may be not required or it will to be adapted to fix the code.

Copy code

```
#EWI: SPRKPY1007 => pyspark.sql.context.SQLContext is not required
#from pyspark import SQLContext
pass

#EWI: SPRKPY1007 => pyspark.sql.context.SQLContext is not required
sql_context1 = my_sc1
#EWI: SPRKPY1007 => pyspark.sql.context.SQLContext is not required
sql_context2 = my_sc2
```

#### Additional recommendations

- This is an unnecessary parameter being and is removed with a warning comment inserted into the source code. There should be no action from the user.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1008

Message: pyspark.sql.context.HiveContext is not required

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.context.HiveContext](https://downloads.apache.org/spark/docs/1.6.1/api/python/pyspark.sql.html#pyspark.sql.HiveContext), which is not required.

#### Scenario

**Input**

In this example, there is an example showing how to create a connection to a Hive store.

Copy code

```
from pyspark.sql import HiveContext
hive_context = HiveContext(sc)
df = hive_context.table("myTable")
df.show()
```

**Output**

In Snowflake there are no Hive stores, so the Hive Context is not required. You can still use parquet files on Snowflake please check this [tutorial](https://docs.snowflake.com/en/user-guide/tutorials/script-data-load-transform-parquet) to learn how.

Copy code

```
#EWI: SPRKPY1008 => pyspark.sql.context.HiveContext is not required
hive_context = sc
df = hive_context.table("myTable")
df.show()
```

the sc variable refers to a [Snowpark Session Object](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.Session)

**Recommended fix**

For the output code in the example you should add the [Snowpark Session Object](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.Session) similar to this code:

Copy code

```
## Here manually we can add the Snowpark Session object via a json config file called connection.json
import json
from snowflake.snowpark import Session
jsonFile = open("connection.json")
connection_parameter = json.load(jsonFile)
jsonFile.close()
sc = Session.builder.configs(connection_parameter).getOrCreate()

hive_context = sc
df = hive_context.table("myTable")
df.show()
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1009

Message\*\*:\*\* pyspark.sql.dataframe.DataFrame.approxQuantile has a workaround

Category\*\*:\*\* Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.dataframe.DataFrame.approxQuantile](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.approxQuantile.html) which has a workaround.

#### Scenario

**Input**

It’s important to understand that Pyspark uses two different approxQuantile functions, here we use the [DataFrame approxQuantile](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.approxQuantile.html) version

Copy code

```
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
data = [['Sun', 10],
        ['Mon', 64],
        ['Thr', 12],
        ['Wen', 15],
        ['Thu', 68],
        ['Fri', 14],
        ['Sat', 13]]

columns = ['Day', 'Ammount']
df = spark.createDataFrame(data, columns)
df.approxQuantile('Ammount', [0.25, 0.5, 0.75], 0)
```

**Output**

SMA returns the EWI SPRKPY1009 over the line where approxQuantile is used, so you can use to identify where to fix.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Sun', 10],
        ['Mon', 64],
        ['Thr', 12],
        ['Wen', 15],
        ['Thu', 68],
        ['Fri', 14],
        ['Sat', 13]]

columns = ['Day', 'Ammount']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1009 => pyspark.sql.dataframe.DataFrame.approxQuantile has a workaround, see documentation for more info
df.approxQuantile('Ammount', [0.25, 0.5, 0.75], 0)
```

**Recommended fix**

Use [Snowpark approxQuantile](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrame.approxQuantile) method. Some parameters don’t match so they require some manual adjustments. for the output code’s example a recommended fix could be:

Copy code

```
from snowflake.snowpark import Session
...
df = spark.createDataFrame(data, columns)

df.stat.approx_quantile('Ammount', [0.25, 0.5, 0.75])
```

pyspark.sql.dataframe.DataFrame.approxQuantile’s relativeError parameter doesn’t exist in SnowPark.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1010

Message: pyspark.sql.dataframe.DataFrame.checkpoint has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.dataframe.DataFrame.checkpoint](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.checkpoint.html) which has a workaround.

#### Scenario

**Input**

In PySpark Checkpoints are used to truncate the logical plan of a dataframe, this to avoid the growing of a logical plan.

Copy code

```
import tempfile
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Score']
df = spark.createDataFrame(data, columns)
with tempfile.TemporaryDirectory() as d:
    spark.sparkContext.setCheckpointDir("/tmp/bb")
    df.checkpoint(False)
```

**Output**

SMA returns the EWI SPRKPY1010 over the line where checkpoint is used, so you can use it to identify where to fix. Note that also marks the [setCheckpointDir](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.setCheckpointDir.html) as unsupported, but a checkpointed directory is not required for the fix.

Copy code

```
import tempfile
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Score']
df = spark.createDataFrame(data, columns)
with tempfile.TemporaryDirectory() as d:
    #EWI: SPRKPY1002 => pyspark.context.SparkContext.setCheckpointDir is not supported
    spark.setCheckpointDir("/tmp/bb")
    #EWI: SPRKPY1010 => pyspark.sql.dataframe.DataFrame.checkpoint has a workaround, see documentation for more info
    df.checkpoint(False)
```

**Recommended fix**

Snowpark eliminates the need for explicit checkpoints: this because Snowpark works with SQL-based operations that are optimized by Snowflake query optimization engine eliminating the need for unrequited computations or logical plans that grow out of control.

However there could be scenarios where you would require persist the result of a computation on a dataframe. In this scenarios you can save materialize the results by writing the dataframe on a [Snowflake Table or in a Snowflake Temporary Table](https://docs.snowflake.com/en/user-guide/tables-temp-transient).

- By the use of a permanent table or the computed result can be accessed in any moment even after the session end.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Score']
df = spark.createDataFrame(data, columns)
df.write.save_as_table("my_table", table_type="temporary") # Save the dataframe into Snowflake table "my_table".
df2 = Session.table("my_table") # Now I can access the stored result quering the table "my_table"
```

- An alternative fix, the use of a Temporary table have the advantage that the table is deleted after the session ends:

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Score']
df = spark.createDataFrame(data, columns)
df.write.save_as_table("my_temp_table", table_type="temporary") # Save the dataframe into Snowflake table "my_temp_table".
df2 = Session.table("my_temp_table") # Now I can access the stored result quering the table "my_temp_table"
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1011

Message: pyspark.sql.dataframe.DataFrameStatFunctions.approxQuantile has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.dataframe.DataFrameStatFunctions.approxQuantile](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameStatFunctions.approxQuantile.html#pyspark.sql.DataFrameStatFunctions.approxQuantile) which has a workaround.

#### Scenario

**Input**

It’s important to understand that Pyspark uses two different approxQuantile functions, here we use the [DataFrameStatFunctions approxQuantile](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameStatFunctions.approxQuantile.html#pyspark.sql.DataFrameStatFunctions.approxQuantile) version.

Copy code

```
import tempfile
from pyspark.sql import SparkSession, DataFrameStatFunctions
spark = SparkSession.builder.getOrCreate()
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Gain']
df = spark.createDataFrame(data, columns)
aprox_quantille = DataFrameStatFunctions(df).approxQuantile('Gain', [0.25, 0.5, 0.75], 0)
print(aprox_quantille)
```

**Output**

SMA returns the EWI SPRKPY1011 over the line where approxQuantile is used, so you can use to identify where to fix.

Copy code

```
import tempfile
from snowflake.snowpark import Session, DataFrameStatFunctions
spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 300000],
        ['Q2', 60000],
        ['Q3', 500002],
        ['Q4', 130000]]

columns = ['Quarter', 'Gain']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1011 => pyspark.sql.dataframe.DataFrameStatFunctions.approxQuantile has a workaround, see documentation for more info
aprox_quantille = DataFrameStatFunctions(df).approxQuantile('Gain', [0.25, 0.5, 0.75], 0)
```

**Recommended fix**

You can use [Snowpark approxQuantile](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrame.approxQuantile) method. Some parameters don’t match so they require some manual adjustments. for the output code’s example a recommended fix could be:

Copy code

```
from snowflake.snowpark import Session # remove DataFrameStatFunctions because is not required
...
df = spark.createDataFrame(data, columns)

aprox_quantille = df.stat.approx_quantile('Ammount', [0.25, 0.5, 0.75])
```

pyspark.sql.dataframe.DataFrame.approxQuantile’s relativeError parameter doesn’t exist in SnowPark.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1012

Warning

This issue code has been **deprecated**

Message: pyspark.sql.dataframe.DataFrameStatFunctions.writeTo has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.dataframe.DataFrameStatFunctions.writeTo](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.writeTo.html) which has a workaround.

#### Scenario

**Input**

For this example the dataframe df is written to a Spark table “table”.

Copy code

```
writer = df.writeTo("table")
```

**Output**

SMA returns the EWI SPRKPY1012 over the line where DataFrameStatFunctions.writeTo is used, so you can use to identify where to fix.

Copy code

```
#EWI: SPRKPY1012 => pyspark.sql.dataframe.DataFrameStatFunctions.writeTo has a workaround, see documentation for more info
writer = df.writeTo("table")
```

**Recommended fix**

Use df.write.save\_as\_table() instead.

Copy code

```
import df.write as wt
writer = df.write.save_as_table(table)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1013

Message: pyspark.sql.functions.acosh has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.acosh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.acosh.html) which has a workaround.

#### Scenario

**Input**

On this example pyspark calculates the acosh for a dataframe by using [pyspark.sql.functions.acosh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.acosh.html)

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import acosh
spark = SparkSession.builder.getOrCreate()
data = [['V1', 30],
        ['V2', 60],
        ['V3', 50],
        ['V4', 13]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_with_acosh = df.withColumn("acosh_value", acosh(df["value"]))
```

**Output**

SMA returns the EWI SPRKPY1013 over the line where acosh is used, so you can use to identify where to fix.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 30],
        ['V2', 60],
        ['V3', 50],
        ['V4', 13]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1013 => pyspark.sql.functions.acosh has a workaround, see documentation for more info
df_with_acosh = df.withColumn("acosh_value", acosh(df["value"]))
```

**Recommended fix**

There is no direct “acosh” implementation but “[call\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.3.0/api/snowflake.snowpark.functions.call_function)” can be used instead, using “acosh” as the first parameter, and colName as the second one.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import call_function, col

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 30],
        ['V2', 60],
        ['V3', 50],
        ['V4', 13]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_with_acosh = df.select(call_function('ACOSH', col('value')))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1014

Message: pyspark.sql.functions.asinh has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.asinh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.asinh.html) which has a workaround.

#### Scenario

**Input**

On this example pyspark calculates the asinh for a dataframe by using [pyspark.sql.functions.asinh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.asinh.html).

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import asinh
spark = SparkSession.builder.getOrCreate()
data = [['V1', 3.0],
        ['V2', 60.0],
        ['V3', 14.0],
        ['V4', 3.1]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_result = df.withColumn("asinh_value", asinh(df["value"]))
```

**Output**

SMA returns the EWI SPRKPY1014 over the line where asinh is used, so you can use to identify where to fix.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 3.0],
        ['V2', 60.0],
        ['V3', 14.0],
        ['V4', 3.1]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1014 => pyspark.sql.functions.asinh has a workaround, see documentation for more info
df_result = df.withColumn("asinh_value", asinh(df["value"]))
```

**Recommended fix**

There is no direct “asinh” implementation but “[call\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.3.0/api/snowflake.snowpark.functions.call_function)” can be used instead, using “asinh” as the first parameter, and colName as the second one.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import call_function, col

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 3.0],
        ['V2', 60.0],
        ['V3', 14.0],
        ['V4', 3.1]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_result = df.select(call_function('asinh', col('value')))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1015

Message: pyspark.sql.functions.atanh has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.atanh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.atanh.html) which has a workaround.

#### Scenario

**Input**

On this example pyspark calculates the atanh for a dataframe by using [pyspark.sql.functions.atanh](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.atanh.html).

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import atanh
spark = SparkSession.builder.getOrCreate()
data = [['V1', 0.14],
        ['V2', 0.32],
        ['V3', 0.4],
        ['V4', -0.36]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_result = df.withColumn("atanh_value", atanh(df["value"]))
```

**Output**

SMA returns the EWI SPRKPY1015 over the line where atanh is used, so you can use to identify where to fix.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 0.14],
        ['V2', 0.32],
        ['V3', 0.4],
        ['V4', -0.36]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1015 => pyspark.sql.functions.atanh has a workaround, see documentation for more info
df_result = df.withColumn("atanh_value", atanh(df["value"]))
```

**Recommended fix**

There is no direct “atanh” implementation but “[call\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.3.0/api/snowflake.snowpark.functions.call_function)” can be used instead, using “atanh” as the first parameter, and colName as the second one.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import call_function, col

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['V1', 0.14],
        ['V2', 0.32],
        ['V3', 0.4],
        ['V4', -0.36]]

columns = ['Paremeter', 'value']
df = spark.createDataFrame(data, columns)
df_result = df.select(call_function('atanh', col('value')))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1016

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 0.11.7](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.functions.collect\_set has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.collect\_set](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.collect_set.html) which has a workaround.

#### Scenario

**Input**

Using collect*set to get the elements of \_colname* without duplicates:

Copy code

```
col = collect_set(colName)
```

**Output**

SMA returns the EWI SPRKPY1016 over the line where collect\_set is used, so you can use to identify where to fix.

Copy code

```
#EWI: SPRKPY1016 => pyspark.sql.functions.collect_set has a workaround, see documentation for more info
col = collect_set(colName)
```

**Recommended fix**

Use function array\_agg, and add a second argument with the value True.

Copy code

```
col = array_agg(col, True)
```

#### Additional recommendation

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1017

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

pyspark.sql.functions.date\_add has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.date\_add](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.date_add.html) which has a workaround.

#### Scenario

**Input**

In this example we use date\_add to calculate the date 5 days after the current date for the dataframe df.

Copy code

```
col = df.select(date_add(df.colName, 5))
```

**Output**

SMA returns the EWI SPRKPY1017 over the line where date\_add is used, so you can use to identify where to fix.

Copy code

```
#EWI: SPRKPY1017 => pyspark.sql.functions.date_add has a workaround, see documentation for more info
col = df.select(date_add(df.colName, 5))
```

**Recommended fix**

Import snowflake.snowpark.functions, which contains an implementation for [date\_add](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.date_add) (and alias dateAdd) function.

Copy code

```
from snowflake.snowpark.functions import date_add

col = df.select(date_add(df.dt, 1))
```

#### Additional recommendation

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1018

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.functions.date\_sub has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.date\_sub](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.date_sub.html) which has a workaround.

#### Scenario

**Input**

In this example we use date\_add to calculate the date 5 days before the current date for the dataframe df.

Copy code

```
col = df.select(date_sub(df.colName, 5))
```

**Output**

SMA returns the EWI SPRKPY1018 over the line where date\_sub is used, so you can use to identify where to fix.

Copy code

```
#EWI: SPRKPY1018 => pyspark.sql.functions.date_sub has a workaround, see documentation for more info
col = df.select(date_sub(df.colName, 5))
```

**Recommended fix**

Import snowflake.snowpark.functions, which contains an implementation for [date\_sub](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.date_sub) function.

Copy code

```
from pyspark.sql.functions import date_sub
df.withColumn("date", date_sub(df.colName, 5))
```

#### Additional recommendation

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1019

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.functions.datediff has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.datediff](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.datediff.html) which has a workaround.

#### Scenario

**Input**

In this example we use datediff to calculate the difference in day from ‘today’ and others dates.

Copy code

```
contacts = (contacts
            #days since last event
            .withColumn('daysSinceLastEvent', datediff(lit(today),'lastEvent'))
            #days since deployment
            .withColumn('daysSinceLastDeployment', datediff(lit(today),'lastDeploymentEnd'))
            #days since online training
            .withColumn('daysSinceLastTraining', datediff(lit(today),'lastTraining'))
            #days since last RC login
            .withColumn('daysSinceLastRollCallLogin', datediff(lit(today),'adx_identity_lastsuccessfullogin'))
            #days since last EMS login
            .withColumn('daysSinceLastEMSLogin', datediff(lit(today),'vms_lastuserlogin'))
           )
```

**Output**

SMA returns the EWI SPRKPY1019 over the line where datediff is used, so you can use to identify where to fix.

Copy code

```
from pyspark.sql.functions import datediff
#EWI: SPRKPY1019 => pyspark.sql.functions.datediff has a workaround, see documentation for more info
contacts = (contacts
            #days since last event
            .withColumn('daysSinceLastEvent', datediff(lit(today),'lastEvent'))
            #days since deployment
            .withColumn('daysSinceLastDeployment', datediff(lit(today),'lastDeploymentEnd'))
            #days since online training
            .withColumn('daysSinceLastTraining', datediff(lit(today),'lastTraining'))
            #days since last RC login
            .withColumn('daysSinceLastRollCallLogin', datediff(lit(today),'adx_identity_lastsuccessfullogin'))
            #days since last EMS login
            .withColumn('daysSinceLastEMSLogin', datediff(lit(today),'vms_lastuserlogin'))
           )
```

SMA convert pyspark.sql.functions.datediff onto [snowflake.snowpark.functions.daydiff](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.daydiff) that also calculates the difference in days between two dates.

**Recommended fix**

**datediff(part: string ,end: ColumnOrName, start: ColumnOrName)**

**Action:** Import snowflake.snowpark.functions, which contains an implementation for [datediff](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.daydiff) function that requires an extra parameter for [date time part](https://docs.snowflake.com/en/sql-reference/functions-date-time#label-supported-date-time-parts) and allows more versatility on calculate differences between dates.

Copy code

```
from snowflake.snowpark import Session
from snowflake.snowpark.functions import datediff
contacts = (contacts
            #days since last event
            .withColumn('daysSinceLastEvent', datediff('day', lit(today),'lastEvent'))
            #days since deployment
            .withColumn('daysSinceLastDeployment', datediff('day',lit(today),'lastDeploymentEnd'))
            #days since online training
            .withColumn('daysSinceLastTraining', datediff('day', lit(today),'lastTraining'))
            #days since last RC login
            .withColumn('daysSinceLastRollCallLogin', datediff('day', lit(today),'adx_identity_lastsuccessfullogin'))
            #days since last EMS login
            .withColumn('daysSinceLastEMSLogin', datediff('day', lit(today),'vms_lastuserlogin'))
           )
```

#### Recommendation

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1020

Message: pyspark.sql.functions.instr has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.instr](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.instr.html) which has a workaround.

#### Scenario

**Input**

Here is a basic example of usage of pyspark instr:

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import instr
spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame([('abcd',)], ['test',])
df.select(instr(df.test, 'cd').alias('result')).collect()
```

**Output:**

SMA returns the EWI SPRKPY1020 over the line where instr is used, so you can use to identify where to fix.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
df = spark.createDataFrame([('abcd',)], ['test',])
#EWI: SPRKPY1020 => pyspark.sql.functions.instr has a workaround, see documentation for more info
df.select(instr(df.test, 'cd').alias('result')).collect()
```

**Recommended fix**

Requires a manual change by using the function [charindex](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.charindex) and changing the order of the first two parameters.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import charindex, lit

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
df = spark.createDataFrame([('abcd',)], ['test',])
df.select(charindex(lit('cd'), df.test).as_('result')).show()
```

#### Additional recommendation

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1021

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.last has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.last](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.last.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.last` function that generates this EWI. In this example, the `last` function is used to get the last **value** for each name.

Copy code

```
df = spark.createDataFrame([("Alice", 1), ("Bob", 2), ("Charlie", 3), ("Alice", 4), ("Bob", 5)], ["name", "value"])
df_grouped = df.groupBy("name").agg(last("value").alias("last_value"))
```

**Output**

The SMA adds the EWI `SPRKPY1021` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([("Alice", 1), ("Bob", 2), ("Charlie", 3), ("Alice", 4), ("Bob", 5)], ["name", "value"])
#EWI: SPRKPY1021 => pyspark.sql.functions.last has a workaround, see documentation for more info
df_grouped = df.groupBy("name").agg(last("value").alias("last_value"))
```

**Recommended fix**

As a workaround, you can use the Snowflake [LAST\_VALUE](https://docs.snowflake.com/en/sql-reference/functions/last_value) function. To invoke this function from Snowpark, use the [snowflake.snowpark.functions.call\_builtin](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.call_builtin) function and pass the string `last_value` as the first argument and the corresponding column as the second argument. If you were using the name of the column in the `last` function, you should convert it into a column when calling the `call_builtin` function.

Copy code

```
df = spark.createDataFrame([("Alice", 1), ("Bob", 2), ("Charlie", 3), ("Alice", 4), ("Bob", 5)], ["name", "value"])
df_grouped = df.groupBy("name").agg(call_builtin("last_value", col("value")).alias("last_value"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

---

## SPRKPY1022

Message: pyspark.sql.functions.log10 has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.log10](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.log10.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.log10` function that generates this EWI. In this example, the `log10` function is used to calculate the base-10 logarithm of the **value** column.

Copy code

```
df = spark.createDataFrame([(1,), (10,), (100,), (1000,), (10000,)], ["value"])
df_with_log10 = df.withColumn("log10_value", log10(df["value"]))
```

**Output**

The SMA adds the EWI `SPRKPY1022` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(1,), (10,), (100,), (1000,), (10000,)], ["value"])
#EWI: SPRKPY1022 => pyspark.sql.functions.log10 has a workaround, see documentation for more info
df_with_log10 = df.withColumn("log10_value", log10(df["value"]))
```

**Recommended fix**

As a workaround, you can use the [snowflake.snowpark.functions.log](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.log) function by passing the literal value `10` as the base.

Copy code

```
df = spark.createDataFrame([(1,), (10,), (100,), (1000,), (10000,)], ["value"])
df_with_log10 = df.withColumn("log10_value", log(10, df["value"]))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1023

Message: pyspark.sql.functions.log1p has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.log1p](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.log1p.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.log1p` function that generates this EWI. In this example, the `log1p` function is used to calculate the natural logarithm of the **value** column.

Copy code

```
df = spark.createDataFrame([(0,), (1,), (10,), (100,)], ["value"])
df_with_log1p = df.withColumn("log1p_value", log1p(df["value"]))
```

**Output**

The SMA adds the EWI `SPRKPY1023` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(0,), (1,), (10,), (100,)], ["value"])
#EWI: SPRKPY1023 => pyspark.sql.functions.log1p has a workaround, see documentation for more info
df_with_log1p = df.withColumn("log1p_value", log1p(df["value"]))
```

**Recommended fix**

As a workaround, you can use the [call\_function](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.call_function) function by passing the string `ln` as the first argument and by adding `1` to the second argument.

Copy code

```
df = spark.createDataFrame([(0,), (1,), (10,), (100,)], ["value"])
df_with_log1p = df.withColumn("log1p_value", call_function("ln", lit(1) + df["value"]))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1024

Message: pyspark.sql.functions.log2 has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.log2](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.log2.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.log2` function that generates this EWI. In this example, the `log2` function is used to calculate the base-2 logarithm of the **value** column.

Copy code

```
df = spark.createDataFrame([(1,), (2,), (4,), (8,), (16,)], ["value"])
df_with_log2 = df.withColumn("log2_value", log2(df["value"]))
```

**Output**

The SMA adds the EWI `SPRKPY1024` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(1,), (2,), (4,), (8,), (16,)], ["value"])
#EWI: SPRKPY1024 => pyspark.sql.functions.log2 has a workaround, see documentation for more info
df_with_log2 = df.withColumn("log2_value", log2(df["value"]))
```

**Recommended fix**

As a workaround, you can use the [snowflake.snowpark.functions.log](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.log) function by passing the literal value `2` as the base.

Copy code

```
df = session.createDataFrame([(1,), (2,), (4,), (8,), (16,)], ["value"])
df_with_log2 = df.withColumn("log2_value", log(2, df["value"]))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1025

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.ntile has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.ntile](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.ntile.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.ntile` function that generates this EWI. In this example, the `ntile` function is used to divide the rows into 3 buckets.

Copy code

```
df = spark.createDataFrame([("Alice", 50), ("Bob", 30), ("Charlie", 60), ("David", 90), ("Eve", 70), ("Frank", 40)], ["name", "score"])
windowSpec = Window.orderBy("score")
df_with_ntile = df.withColumn("bucket", ntile(3).over(windowSpec))
```

**Output**

The SMA adds the EWI `SPRKPY1025` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([("Alice", 50), ("Bob", 30), ("Charlie", 60), ("David", 90), ("Eve", 70), ("Frank", 40)], ["name", "score"])
windowSpec = Window.orderBy("score")
#EWI: SPRKPY1025 => pyspark.sql.functions.ntile has a workaround, see documentation for more info
df_with_ntile = df.withColumn("bucket", ntile(3).over(windowSpec))
```

**Recommended fix**

Snowpark has an equivalent [ntile](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.ntile) function, however, the argument pass to it should be a column. As a workaround, you can convert the literal argument into a column using the [snowflake.snowpark.functions.lit](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.lit) function.

Copy code

```
df = spark.createDataFrame([("Alice", 50), ("Bob", 30), ("Charlie", 60), ("David", 90), ("Eve", 70), ("Frank", 40)], ["name", "score"])
windowSpec = Window.orderBy("score")
df_with_ntile = df.withColumn("bucket", ntile(lit(3)).over(windowSpec))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1026

Warning

This issue code has been **deprecated** since [Spark Conversion Core 4.3.2](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.readwriter.DataFrameReader.csv has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.readwriter.DataFrameReader.csv](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.csv.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.readwriter.DataFrameReader.csv` function that generates this EWI. In this example, the `csv` function is used to read multiple `.csv` files with a given schema and uses some extra options such as **encoding**, **header** and **sep** to fine-tune the behavior of reading the files.

Copy code

```
file_paths = [
  "path/to/your/file1.csv",
  "path/to/your/file2.csv",
  "path/to/your/file3.csv",
]

df = session.read.csv(
  file_paths,
  schema=my_schema,
  encoding="UTF-8",
  header=True,
  sep=","
)
```

**Output**

The SMA adds the EWI `SPRKPY1026` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
file_paths = [
  "path/to/your/file1.csv",
  "path/to/your/file2.csv",
  "path/to/your/file3.csv",
]

#EWI: SPRKPY1026 => pyspark.sql.readwriter.DataFrameReader.csv has a workaround, see documentation for more info
df = session.read.csv(
  file_paths,
  schema=my_schema,
  encoding="UTF-8",
  header=True,
  sep=","
)
```

**Recommended fix**

In this section, we explain how to configure the `path` parameter, the `schema` parameter and some `options` to make them work in Snowpark.

**1. path parameter**

Snowpark requires the **path** parameter to be a stage location so, as a workaround, you can create a temporary stage and add each `.csv` file to that stage using the prefix `file://`.

**2. schema parameter**

Snowpark does not allow defining the **schema** as a parameter of the `csv` function. As a workaround, you can use the [snowflake.snowpark.DataFrameReader.schema](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.schema) function.

**3. options parameters**

Snowpark does not allow defining the **extra options** as parameters of the `csv` function. As a workaround, for many of them you can use the [snowflake.snowpark.DataFrameReader.option](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.option) function to specify those parameters as options of the DataFrameReader.

Note

The following options are **not supported** by Snowpark:

- columnNameOfCorruptRecord
- emptyValue
- enforceSchema
- header
- ignoreLeadingWhiteSpace
- ignoreTrailingWhiteSpace
- inferSchema
- locale
- maxCharsPerColumn
- maxColumns
- mode
- multiLine
- nanValue
- negativeInf
- nullValue
- positiveInf
- quoteAll
- samplingRatio
- timestampNTZFormat
- unescapedQuoteHandling

Below is the full example of how the input code should look like after applying the suggestions mentioned above to make it work in Snowpark:

Copy code

```
stage = f'{session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {stage}')

session.file.put(f"file:///path/to/your/file1.csv", f"@{stage}")
session.file.put(f"file:///path/to/your/file2.csv", f"@{stage}")
session.file.put(f"file:///path/to/your/file3.csv", f"@{stage}")

df = session.read.schema(my_schema).option("encoding", "UTF-8").option("sep", ",").csv(stage)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1027

Warning

This issue code has been **deprecated** since [Spark Conversion Core 4.5.2](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.readwriter.DataFrameReader.json has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.readwriter.DataFrameReader.json](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.json.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.readwriter.DataFrameReader.json` function that generates this EWI. In this example, the `json` function is used to read multiple `.json` files with a given schema and uses some extra options such as **primitiveAsString** and **dateFormat** to fine-tune the behavior of reading the files.

Copy code

```
file_paths = [
  "path/to/your/file1.json",
  "path/to/your/file2.json",
  "path/to/your/file3.json",
]

df = session.read.json(
  file_paths,
  schema=my_schema,
  primitiveAsString=True,
  dateFormat="2023-06-20"
)
```

**Output**

The SMA adds the EWI `SPRKPY1027` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
file_paths = [
  "path/to/your/file1.json",
  "path/to/your/file2.json",
  "path/to/your/file3.json",
]

#EWI: SPRKPY1027 => pyspark.sql.readwriter.DataFrameReader.json has a workaround, see documentation for more info
df = session.read.json(
  file_paths,
  schema=my_schema,
  primitiveAsString=True,
  dateFormat="2023-06-20"
)
```

**Recommended fix**

In this section, we explain how to configure the `path` parameter, the `schema` parameter and some `options` to make them work in Snowpark.

**1. path parameter**

Snowpark requires the **path** parameter to be a stage location so, as a workaround, you can create a temporary stage and add each `.json` file to that stage using the prefix `file://`.

**2. schema parameter**

Snowpark does not allow defining the **schema** as a parameter of the `json` function. As a workaround, you can use the [snowflake.snowpark.DataFrameReader.schema](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.schema) function.

**3. options parameters**

Snowpark does not allow defining the **extra options** as parameters of the `json` function. As a workaround, for many of them you can use the [snowflake.snowpark.DataFrameReader.option](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.option) function to specify those parameters as options of the DataFrameReader.

Note

The following options are not supported by Snowpark:

- allowBackslashEscapingAnyCharacter
- allowComments
- allowNonNumericNumbers
- allowNumericLeadingZero
- allowSingleQuotes
- allowUnquotedControlChars
- allowUnquotedFieldNames
- columnNameOfCorruptRecord
- dropFiledIfAllNull
- encoding
- ignoreNullFields
- lineSep
- locale
- mode
- multiline
- prefersDecimal
- primitiveAsString
- samplingRatio
- timestampNTZFormat
- timeZone

Below is the full example of how the input code should look like after applying the suggestions mentioned above to make it work in Snowpark:

Copy code

```
stage = f'{session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {stage}')

session.file.put(f"file:///path/to/your/file1.json", f"@{stage}")
session.file.put(f"file:///path/to/your/file2.json", f"@{stage}")
session.file.put(f"file:///path/to/your/file3.json", f"@{stage}")

df = session.read.schema(my_schema).option("dateFormat", "2023-06-20").json(stage)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1028

Message: pyspark.sql.readwriter.DataFrameReader.orc has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.readwriter.DataFrameReader.orc](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.orc.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.readwriter.DataFrameReader.orc` function that generates this EWI. In this example, the `orc` function is used to read multiple `.orc` files and uses some extra options such as **mergeSchema** and **recursiveFileLookup** to fine-tune the behavior of reading the files.

Copy code

```
file_paths = [
  "path/to/your/file1.orc",
  "path/to/your/file2.orc",
  "path/to/your/file3.orc",
]

df = session.read.orc(
  file_paths,
  mergeSchema="True",
  recursiveFileLookup="True"
)
```

**Output**

The SMA adds the EWI `SPRKPY1028` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
file_paths = [
  "path/to/your/file1.orc",
  "path/to/your/file2.orc",
  "path/to/your/file3.orc",
]

#EWI: SPRKPY1028 => pyspark.sql.readwriter.DataFrameReader.orc has a workaround, see documentation for more info
df = session.read.orc(
  file_paths,
  mergeSchema="True",
  recursiveFileLookup="True"
)
```

**Recommended fix**

In this section, we explain how to configure the `path` parameter and the extra `options` to make them work in Snowpark.

**1. path parameter**

Snowpark requires the **path** parameter to be a stage location so, as a workaround, you can create a temporary stage and add each `.orc` file to that stage using the prefix `file://`.

**2. options parameters**

Snowpark does not allow defining the **extra options** as parameters of the `orc` function. As a workaround, for many of them you can use the [snowflake.snowpark.DataFrameReader.option](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.option) function to specify those parameters as options of the DataFrameReader.

Note

The following options are not supported by Snowpark:

- compression
- mergeSchema

Below is the full example of how the input code should look like after applying the suggestions mentioned above to make it work in Snowpark:

Copy code

```
stage = f'{session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {stage}')

session.file.put(f"file:///path/to/your/file1.orc", f"@{stage}")
session.file.put(f"file:///path/to/your/file2.orc", f"@{stage}")
session.file.put(f"file:///path/to/your/file3.orc", f"@{stage}")

df = session.read.option(recursiveFileLookup, "True").orc(stage)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1029

Message: This issue appears when the tool detects the usage of pyspark.sql.readwriter.DataFrameReader.parquet. This function is supported, but some of the differences between Snowpark and the Spark API might require making some manual changes.

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.readwriter.DataFrameReader.parquet](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.parquet.html) function. This function is supported by Snowpark, however, there are some differences that would require some manual changes.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.readwriter.DataFrameReader.parquet` function that generates this EWI.

Copy code

```
file_paths = [
  "path/to/your/file1.parquet",
  "path/to/your/file2.parquet",
  "path/to/your/file3.parquet",
]

df = session.read.parquet(
  *file_paths,
  mergeSchema="true",
  pathGlobFilter="*file*",
  recursiveFileLookup="true",
  modifiedBefore="2024-12-31T00:00:00",
  modifiedAfter="2023-12-31T00:00:00"
)
```

**Output**

The SMA adds the EWI `SPRKPY1029` to the output code to let you know that this function is supported by Snowpark, but it requires some manual adjustments. Please note that the options supported by Snowpark are transformed into `option` function calls and those that are not supported are removed. This is explained in more detail in the next sections.

Copy code

```
file_paths = [
  "path/to/your/file1.parquet",
  "path/to/your/file2.parquet",
  "path/to/your/file3.parquet"
]

#EWI: SPRKPY1076 => Some of the included parameters are not supported in the parquet function, the supported ones will be added into a option method.
#EWI: SPRKPY1029 => This issue appears when the tool detects the usage of pyspark.sql.readwriter.DataFrameReader.parquet. This function is supported, but some of the differences between Snowpark and the Spark API might require making some manual changes.
df = session.read.option("PATTERN", "*file*").parquet(
  *file_paths
)
```

**Recommended fix**

In this section, we explain how to configure the `paths` and `options` parameters to make them work in Snowpark.

**1. paths parameter**

In Spark, this parameter can be a local or cloud location. Snowpark only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage). So, you can create a temporal stage and add each file into it using the prefix `file://`.

**2. options parameter**

Snowpark does not allow defining the different **options** as parameters of the `parquet` function. As a workaround, you can use the [option](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.option) or [options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.options) functions to specify those parameters as extra options of the DataFrameReader.

Please note that the Snowpark **options** are not exactly the same as the PySpark **options** so some manual changes might be needed. Below is a more detailed explanation of how to configure the most common PySpark options in Snowpark.

**2.1 mergeSchema option**

Parquet supports schema evolution, allowing users to start with a simple schema and gradually add more columns as needed. This can result in multiple parquet files with different but compatible schemas. In Snowflake, thanks to the [infer\_schema](https://docs.snowflake.com/en/sql-reference/functions/infer_schema) capabilities you don’t need to do that and therefore the `mergeSchema` option can just be removed.

**2.2 pathGlobFilter option**

If you want to load only a subset of files from the stage, you can use the `pattern` option to specify a regular expression that matches the files you want to load. The SMA already automates this as you can see in the output of this scenario.

**2.3 recursiveFileLookupstr option**

This option is not supported by Snowpark. The best recommendation is to use a regular expression like with the `pathGlobFilter` option to achieve something similar.

**2.4 modifiedBefore / modifiedAfter option**

You can achieve the same result in Snowflake by using the `metadata` columns.

Note

The following options are not supported by Snowpark:

- compression
- datetimeRebaseMode
- int96RebaseMode
- mergeSchema

Below is the full example of how the input code should be transformed in order to make it work in Snowpark:

Copy code

```
from snowflake.snowpark.column import METADATA_FILE_LAST_MODIFIED, METADATA_FILENAME

temp_stage = f'{session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}')

session.file.put(f"file:///path/to/your/file1.parquet", f"@{temp_stage}")
session.file.put(f"file:///path/to/your/file2.parquet", f"@{temp_stage}")
session.file.put(f"file:///path/to/your/file3.parquet", f"@{temp_stage}")

df = session.read \
  .option("PATTERN", ".*file.*") \
  .with_metadata(METADATA_FILENAME, METADATA_FILE_LAST_MODIFIED) \
  .parquet(temp_stage) \
  .where(METADATA_FILE_LAST_MODIFIED < '2024-12-31T00:00:00') \
  .where(METADATA_FILE_LAST_MODIFIED > '2023-12-31T00:00:00')
```

#### Additional recommendations

- In Snowflake, you can leverage other approaches for parquet data ingestion, such as:

  - Leveraging [native parquet ingestion capabilities](https://docs.snowflake.com/en/user-guide/tutorials/script-data-load-transform-parquet). Consider also [autoingest with snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-auto-s3).
  - Parquet [external tables](https://docs.snowflake.com/en/user-guide/tables-external-intro) which can be pointed directly to cloud file locations.
  - Using [Iceberg tables](https://docs.snowflake.com/LIMITEDACCESS/iceberg/tables-iceberg-parquet-source).
- When doing a migration is a good practice to leverage the SMA reports to try to build an inventory of files and determine after modernization to which stages/tables will the data be mapped.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1030

Warning

This issue code has been **deprecated**

Message: pyspark.sql.session.SparkSession.Builder.appName has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.session.SparkSession.Builder.appName](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.builder.appName.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.session.SparkSession.Builder.appName` function that generates this EWI. In this example, the `appName` function is used to set **MyApp** as the name of the application.

Copy code

```
session = SparkSession.builder.appName("MyApp").getOrCreate()
```

**Output**

The SMA adds the EWI `SPRKPY1030` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
#EWI: SPRKPY1030 => pyspark.sql.session.SparkSession.Builder.appName has a workaround, see documentation for more info
session = Session.builder.appName("MyApp").getOrCreate()
```

**Recommended fix**

As a workaround, you can import the [snowpark\_extensions](https://pypi.org/project/snowpark-extensions/) package which provides an extension for the `appName` function.

Copy code

```
import snowpark_extensions
session = SessionBuilder.appName("MyApp").getOrCreate()
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1031

Warning

This issue code has been **deprecated** since [Spark Conversion Core 2.7.0](/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-python-release-notes/README)

Message: pyspark.sql.column.Column.contains has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.column.Column.contains](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.contains.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.column.Column.contains` function that generates this EWI. In this example, the `contains` function is used to filter the rows where the ‘City’ column contains the substring ‘New’.

Copy code

```
df = spark.createDataFrame([("Alice", "New York"), ("Bob", "Los Angeles"), ("Charlie", "Chicago")], ["Name", "City"])
df_filtered = df.filter(col("City").contains("New"))
```

**Output**

The SMA adds the EWI `SPRKPY1031` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([("Alice", "New York"), ("Bob", "Los Angeles"), ("Charlie", "Chicago")], ["Name", "City"])
#EWI: SPRKPY1031 => pyspark.sql.column.Column.contains has a workaround, see documentation for more info
df_filtered = df.filter(col("City").contains("New"))
```

**Recommended fix**

As a workaround, you can use the [snowflake.snowpark.functions.contains](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.contains) function by passing the column as the first argument and the element to search as the second argument. If the element to search is a literal value then it should be converted into a column expression using the `lit` function.

Copy code

```
from snowflake.snowpark import functions as f
df = spark.createDataFrame([("Alice", "New York"), ("Bob", "Los Angeles"), ("Charlie", "Chicago")], ["Name", "City"])
df_filtered = df.filter(f.contains(col("City"), f.lit("New")))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1032

Message: ***spark element*** is not defined

Category: Conversion error

### Description

This issue appears when the SMA could not determine an appropriate mapping status for the given element. This means, the SMA doesn’t know yet if this element is supported or not by Snowpark. Please note, this is a generic error code used by the SMA for any not defined element.

#### Scenario

**Input**

Below is an example of a function for which the SMA could not determine an appropriate mapping status. In this case, you should assume that `not_defined_function()` is a valid PySpark function and the code runs.

Copy code

```
sc.parallelize(["a", "b", "c", "d", "e"], 3).not_defined_function().collect()
```

**Output**

The SMA adds the EWI `SPRKPY1032` to the output code to let you know that this element is not defined.

Copy code

```
#EWI: SPRKPY1032 => pyspark.rdd.RDD.not_defined_function is not defined
sc.parallelize(["a", "b", "c", "d", "e"], 3).not_defined_function().collect()
```

**Recommended fix**

To try to identify the problem, you can perform the following validations:

- Check if the source code has the correct syntax, and it is spelled correctly.
- Check if you are using a PySpark version supported by the SMA. To know which PySpark version is supported by the SMA at the moment of running the SMA, you can review the first page of the `DetailedReport.docx` file.

If this is a valid PySpark element, please report that you encountered a conversion error on that particular element using the [Report an Issue](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) option of the SMA and include any additional information that you think may be helpful.

Please note that if an element is not defined, it does not mean that it is not supported by Snowpark. You should check the [Snowpark Documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index) to verify if an equivalent element exist.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1033

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.asc has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.asc](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.asc.html) function, which has a workaround.

#### Scenarios

The `pyspark.sql.functions.asc` function takes either a column object or the name of the column as a string as its parameter. Both scenarios are not supported by Snowpark so this EWI is generated.

##### Scenario 1

**Input**

Below is an example of a use of the `pyspark.sql.functions.asc` function that takes a column object as parameter.

Copy code

```
df.orderBy(asc(col))
```

**Output**

The SMA adds the EWI `SPRKPY1033` to the output code to let you know that the `asc` function with a column object parameter is not directly supported by Snowpark, but it has a workaround.

Copy code

```
#EWI: SPRKPY1033 => pyspark.sql.functions.asc has a workaround, see documentation for more info
df.orderBy(asc(col))
```

**Recommended fix**

As a workaround, you can call the [snowflake.snowpark.Column.asc](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Column.asc) function from the column parameter.

Copy code

```
df.orderBy(col.asc())
```

##### Scenario 2

**Input**

Below is an example of a use of the `pyspark.sql.functions.asc` function that takes the name of the column as parameter.

Copy code

```
df.orderBy(asc("colName"))
```

**Output**

The SMA adds the EWI `SPRKPY1033` to the output code to let you know that the `asc` function with a column name parameter is not directly supported by Snowpark, but it has a workaround.

Copy code

```
#EWI: SPRKPY1033 => pyspark.sql.functions.asc has a workaround, see documentation for more info
df.orderBy(asc("colName"))
```

**Recommended fix**

As a workaround, you can convert the string parameter into a column object using the [snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.col) function and then call the [snowflake.snowpark.Column.asc](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Column.asc) function.

Copy code

```
df.orderBy(col("colName").asc())
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1034

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.desc has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.desc](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.desc.html) function, which has a workaround.

#### Scenarios

The `pyspark.sql.functions.desc` function takes either a column object or the name of the column as a string as its parameter. Both scenarios are not supported by Snowpark so this EWI is generated.

##### Scenario 1

**Input**

Below is an example of a use of the `pyspark.sql.functions.desc` function that takes a column object as parameter.

Copy code

```
df.orderBy(desc(col))
```

**Output**

The SMA adds the EWI `SPRKPY1034` to the output code to let you know that the `desc` function with a column object parameter is not directly supported by Snowpark, but it has a workaround.

Copy code

```
#EWI: SPRKPY1034 => pyspark.sql.functions.desc has a workaround, see documentation for more info
df.orderBy(desc(col))
```

**Recommended fix**

As a workaround, you can call the [snowflake.snowpark.Column.desc](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Column.desc) function from the column parameter.

Copy code

```
df.orderBy(col.desc())
```

##### Scenario 2

**Input**

Below is an example of a use of the `pyspark.sql.functions.desc` function that takes the name of the column as parameter.

Copy code

```
df.orderBy(desc("colName"))
```

**Output**

The SMA adds the EWI `SPRKPY1034` to the output code to let you know that the `desc` function with a column name parameter is not directly supported by Snowpark, but it has a workaround.

Copy code

```
#EWI: SPRKPY1034 => pyspark.sql.functions.desc has a workaround, see documentation for more info
df.orderBy(desc("colName"))
```

**Recommended fix**

As a workaround, you can convert the string parameter into a column object using the [snowflake.snowpark.functions.col](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.col) function and then call the [snowflake.snowpark.Column.desc](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Column.desc) function.

Copy code

```
df.orderBy(col("colName").desc())
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1035

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.reverse has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.reverse](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.reverse.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.reverse` function that generates this EWI. In this example, the `reverse` function is used to reverse each string of the **word** column.

Copy code

```
df = spark.createDataFrame([("hello",), ("world",)], ["word"])
df_reversed = df.withColumn("reversed_word", reverse(df["word"]))
df_reversed = df.withColumn("reversed_word", reverse("word"))
```

**Output**

The SMA adds the EWI `SPRKPY1035` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([("hello",), ("world",)], ["word"])
#EWI: SPRKPY1035 => pyspark.sql.functions.reverse has a workaround, see documentation for more info
df_reversed = df.withColumn("reversed_word", reverse(df["word"]))
#EWI: SPRKPY1035 => pyspark.sql.functions.reverse has a workaround, see documentation for more info
df_reversed = df.withColumn("reversed_word", reverse("word"))
```

**Recommended fix**

As a workaround, you can import the [snowpark\_extensions](https://pypi.org/project/snowpark-extensions/) package which provides an extension for the `reverse` function.

Copy code

```
import snowpark_extensions

df = spark.createDataFrame([("hello",), ("world",)], ["word"])
df_reversed = df.withColumn("reversed_word", reverse(df["word"]))
df_reversed = df.withColumn("reversed_word", reverse("word"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1036

Warning

This issue code has been **deprecated**

Message: pyspark.sql.column.Column.getField has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.column.Column.getField](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.getField.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.column.Column.getField` function that generates this EWI. In this example, the `getField` function is used to extract the **name** from the **info** column.

Copy code

```
df = spark.createDataFrame([(1, {"name": "John", "age": 30}), (2, {"name": "Jane", "age": 25})], ["id", "info"])
df_with_name = df.withColumn("name", col("info").getField("name"))
```

**Output**

The SMA adds the EWI `SPRKPY1036` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(1, {"name": "John", "age": 30}), (2, {"name": "Jane", "age": 25})], ["id", "info"])
#EWI: SPRKPY1036 => pyspark.sql.column.Column.getField has a workaround, see documentation for more info
df_with_name = df.withColumn("name", col("info").getField("name"))
```

**Recommended fix**

As a workaround, you can use the [Snowpark column indexer operator](https://docs.snowflake.com/ko/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Column#snowflake.snowpark.Column) with the name of the field as the index.

Copy code

```
df = spark.createDataFrame([(1, {"name": "John", "age": 30}), (2, {"name": "Jane", "age": 25})], ["id", "info"])
df_with_name = df.withColumn("name", col("info")["name"])
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1037

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.sort\_array has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.sort\_array](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.sort_array.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.sort_array` function that generates this EWI. In this example, the `sort_array` function is used to sort the **numbers** array in ascending and descending order.

Copy code

```
df = spark.createDataFrame([(1, [3, 1, 2]), (2, [10, 5, 8]), (3, [6, 4, 7])], ["id", "numbers"])
df_sorted_asc = df.withColumn("sorted_numbers_asc", sort_array("numbers", asc=True))
df_sorted_desc = df.withColumn("sorted_numbers_desc", sort_array("numbers", asc=False))
```

**Output**

The SMA adds the EWI `SPRKPY1037` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(1, [3, 1, 2]), (2, [10, 5, 8]), (3, [6, 4, 7])], ["id", "numbers"])
#EWI: SPRKPY1037 => pyspark.sql.functions.sort_array has a workaround, see documentation for more info
df_sorted_asc = df.withColumn("sorted_numbers_asc", sort_array("numbers", asc=True))
#EWI: SPRKPY1037 => pyspark.sql.functions.sort_array has a workaround, see documentation for more info
df_sorted_desc = df.withColumn("sorted_numbers_desc", sort_array("numbers", asc=False))
```

**Recommended fix**

As a workaround, you can import the [snowpark\_extensions](https://pypi.org/project/snowpark-extensions/) package which provides an extension for the `sort_array` function.

Copy code

```
import snowpark_extensions

df = spark.createDataFrame([(1, [3, 1, 2]), (2, [10, 5, 8]), (3, [6, 4, 7])], ["id", "numbers"])
df_sorted_asc = df.withColumn("sorted_numbers_asc", sort_array("numbers", asc=True))
df_sorted_desc = df.withColumn("sorted_numbers_desc", sort_array("numbers", asc=False))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1038

Message: ***spark element*** is not yet recognized

Category: Conversion error

### Description

This issue appears when there is a PySpark element in your source code that was not recognized by the SMA. This can occur for different reasons, such as:

- An element that does not exist in PySpark.
- An element that was added in a PySpark version that the SMA does not support yet.
- An internal error of the SMA when processing the element.

This is a generic error code used by the SMA for any not recognized element.

#### Scenario

**Input**

Below is an example of a use of a function that could not be recognized by the SMA because it does not exist in PySpark.

Copy code

```
from pyspark.sql import functions as F
F.unrecognized_function()
```

**Output**

The SMA adds the EWI `SPRKPY1038` to the output code to let you know that this element could not be recognized.

Copy code

```
from snowflake.snowpark import functions as F
#EWI: SPRKPY1038 => pyspark.sql.functions.non_existent_function is not yet recognized
F.unrecognized_function()
```

**Recommended fix**

To try to identify the problem, you can perform the following validations:

- Check if the element exists in PySpark.
- Check if the element is spelled correctly.
- Check if you are using a PySpark version supported by the SMA. To know which PySpark version is supported by the SMA at the moment of running the SMA, you can review the first page of the `DetailedReport.docx` file.

If it is a valid PySpark element, please report that you encountered a conversion error on that particular element using the [Report an Issue](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) option of the SMA and include any additional information that you think may be helpful.

Please note that if an element could not be recognized by the SMA, it does not mean that it is not supported by Snowpark. You should check the [Snowpark Documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/index) to verify if an equivalent element exist.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1039

Warning

This issue code has been **deprecated**

Message: pyspark.sql.column.Column.getItem has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.column.Column.getItem](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Column.getItem.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.column.Column.getItem` function that generates this EWI. In this example, the `getItem` function is used to get an item by position and by key.

Copy code

```
df = spark.createDataFrame([(1, ["apple", "banana", "orange"]), (2, ["carrot", "avocado", "banana"])], ["id", "fruits"])
df.withColumn("first_fruit", col("fruits").getItem(0))

df = spark.createDataFrame([(1, {"apple": 10, "banana": 20}), (2, {"carrot": 15, "grape": 25}), (3, {"pear": 30, "apple": 35})], ["id", "fruit_quantities"])
df.withColumn("apple_quantity", col("fruit_quantities").getItem("apple"))
```

**Output**

The SMA adds the EWI `SPRKPY1039` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([(1, ["apple", "banana", "orange"]), (2, ["carrot", "avocado", "banana"])], ["id", "fruits"])
#EWI: SPRKPY1039 => pyspark.sql.column.Column.getItem has a workaround, see documentation for more info
df.withColumn("first_fruit", col("fruits").getItem(0))

df = spark.createDataFrame([(1, {"apple": 10, "banana": 20}), (2, {"carrot": 15, "grape": 25}), (3, {"pear": 30, "apple": 35})], ["id", "fruit_quantities"])
#EWI: SPRKPY1039 => pyspark.sql.column.Column.getItem has a workaround, see documentation for more info
df.withColumn("apple_quantity", col("fruit_quantities").getItem("apple"))
```

**Recommended fix**

As a workaround, you can use the **Snowpark column indexer operator** with the name or position of the field as the index.

Copy code

```
df = spark.createDataFrame([(1, ["apple", "banana", "orange"]), (2, ["carrot", "avocado", "banana"])], ["id", "fruits"])
df.withColumn("first_fruit", col("fruits")[0])

df = spark.createDataFrame([(1, {"apple": 10, "banana": 20}), (2, {"carrot": 15, "grape": 25}), (3, {"pear": 30, "apple": 35})], ["id", "fruit_quantities"])
df.withColumn("apple_quantity", col("fruit_quantities")["apple"])
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1040

Warning

This issue code has been **deprecated**

Message: pyspark.sql.functions.explode has a workaround, see documentation for more info

Category: Warning

### Description

This issue appears when the SMA detects a use of the [pyspark.sql.functions.explode](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.explode.html) function, which has a workaround.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.functions.explode` function that generates this EWI. In this example, the `explode` function is used to generate one row per array item for the **numbers** column.

Copy code

```
df = spark.createDataFrame([("Alice", [1, 2, 3]), ("Bob", [4, 5]), ("Charlie", [6, 7, 8, 9])], ["name", "numbers"])
exploded_df = df.select("name", explode(df.numbers).alias("number"))
```

**Output**

The SMA adds the EWI `SPRKPY1040` to the output code to let you know that this function is not directly supported by Snowpark, but it has a workaround.

Copy code

```
df = spark.createDataFrame([("Alice", [1, 2, 3]), ("Bob", [4, 5]), ("Charlie", [6, 7, 8, 9])], ["name", "numbers"])
#EWI: SPRKPY1040 => pyspark.sql.functions.explode has a workaround, see documentation for more info
exploded_df = df.select("name", explode(df.numbers).alias("number"))
```

**Recommended fix**

As a workaround, you can import the [snowpark\_extensions](https://pypi.org/project/snowpark-extensions/) package which provides an extension for the `explode` function.

Copy code

```
import snowpark_extensions

df = spark.createDataFrame([("Alice", [1, 2, 3]), ("Bob", [4, 5]), ("Charlie", [6, 7, 8, 9])], ["name", "numbers"])
exploded_df = df.select("name", explode(df.numbers).alias("number"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1041

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.9.0](/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-python-release-notes/README)

Message: pyspark.sql.functions.explode\_outer has a workaround

Category: Warning

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.explode\_outer](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.explode_outer.html#pyspark.sql.functions.explode_outer) which has a workaround.

#### Scenario

**Input**

The example shows the use of the method **explode\_outer** in a select call.

Copy code

```
df = spark.createDataFrame(
    [(1, ["foo", "bar"], {"x": 1.0}),
     (2, [], {}),
     (3, None, None)],
    ("id", "an_array", "a_map")
)

df.select("id", "an_array", explode_outer("a_map")).show()
```

**Output**

The tool adds the EWI `SPRKPY1041` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame(
    [(1, ["foo", "bar"], {"x": 1.0}),
     (2, [], {}),
     (3, None, None)],
    ("id", "an_array", "a_map")
)

#EWI: SPRKPY1041 => pyspark.sql.functions.explode_outer has a workaround, see documentation for more info
df.select("id", "an_array", explode_outer("a_map")).show()
```

**Recommended fix**

As a workaround, you can import the snowpark\_extensions package, which contains a helper for the `explode_outer` function.

Copy code

```
import snowpark_extensions

df = spark.createDataFrame(
    [(1, ["foo", "bar"], {"x": 1.0}),
     (2, [], {}),
     (3, None, None)],
    ("id", "an_array", "a_map")
)

df.select("id", "an_array", explode_outer("a_map")).show()
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1042

Message: pyspark.sql.functions.posexplode has a workaround

Category: Warning

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.posexplode](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.posexplode.html?highlight=posexplode) which has a workaround.

#### Scenarios

There are a couple of scenarios that this method can handle depending on the type of column it is passed as a parameter, it can be a `list of values` or a `map/directory (keys/values)`.

##### Scenario 1

**Input**

Below is an example of the usage of `posexplode` passing as a parameter of a **list of values**.

Copy code

```
df = spark.createDataFrame(
    [Row(a=1,
         intlist=[1, 2, 3])])

df.select(posexplode(df.intlist)).collect()
```

**Output**

The tool adds the EWI `SPRKPY1042` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame(
    [Row(a=1,
         intlist=[100, 200, 300])])
#EWI: SPRKPY1042 => pyspark.sql.functions.posexplode has a workaround, see documentation for more info

df.select(posexplode(df.intlist)).show()
```

**Recommended fix**

For having the same behavior, use the method [functions.flatten](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.functions.flatten), drop extra columns, and rename index and value column names.

Copy code

```
df = spark.createDataFrame(
  [Row(a=1,
       intlist=[1, 2, 3])])

df.select(
    flatten(df.intlist))\
    .drop("DATA", "SEQ", "KEY", "PATH", "THIS")\
    .rename({"INDEX": "pos", "VALUE": "col"}).show()
```

##### Scenario 2

**Input**

Below is another example of the usage of `posexplode` passing as a parameter a **map/dictionary (keys/values)**

Copy code

```
df = spark.createDataFrame([
    [1, [1, 2, 3], {"Ashi Garami": "Single Leg X"}, "Kimura"],
    [2, [11, 22], {"Sankaku": "Triangle"}, "Coffee"]
],
schema=["idx", "lists", "maps", "strs"])

df.select(posexplode(df.maps)).show()
```

**Output**

The tool adds the EWI `SPRKPY1042` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame([
    [1, [1, 2, 3], {"Ashi Garami": "Single Leg X"}, "Kimura"],
    [2, [11, 22], {"Sankaku": "Triangle"}, "Coffee"]
],
schema=["idx", "lists", "maps", "strs"])
#EWI: SPRKPY1042 => pyspark.sql.functions.posexplode has a workaround, see documentation for more info

df.select(posexplode(df.maps)).show()
```

**Recommended fix**

As a workaround, you can use [functions.row\_number](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/api/snowflake.snowpark.functions.row_number.html) to get the position and [functions.explode](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.explode) with the name of the field to get the value the key/value for dictionaries.

Copy code

```
df = spark.createDataFrame([
    [10, [1, 2, 3], {"Ashi Garami": "Single Leg X"}, "Kimura"],
    [11, [11, 22], {"Sankaku": "Triangle"}, "Coffee"]
],
    schema=["idx", "lists", "maps", "strs"])

window = Window.orderBy(col("idx").asc())

df.select(
    row_number().over(window).alias("pos"),
    explode(df.maps).alias("key", "value")).show()
```

**Note:** using row\_number is not fully equivalent, because it starts with 1 (not zero as spark method)

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1043

Message: pyspark.sql.functions.posexplode\_outer has a workaround

Category: Warning

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.posexplode\_outer](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.posexplode_outer.html) which has a workaround.

#### Scenarios

There are a couple of scenarios that this method can handle depending on the type of column it is passed as a parameter, it can be a `list of values` or a `map/directory (keys/values)`.

##### Scenario 1

**Input**

Below is an example that shows the usage of `posexplode_outer` passing a **list of values**.

Copy code

```
df = spark.createDataFrame(
    [
        (1, ["foo", "bar"]),
        (2, []),
        (3, None)],
    ("id", "an_array"))

df.select("id", "an_array", posexplode_outer("an_array")).show()
```

**Output**

The tool adds the EWI `SPRKPY1043` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame(
    [
        (1, ["foo", "bar"]),
        (2, []),
        (3, None)],
    ("id", "an_array"))
#EWI: SPRKPY1043 => pyspark.sql.functions.posexplode_outer has a workaround, see documentation for more info

df.select("id", "an_array", posexplode_outer("an_array")).show()
```

**Recommended fix**

For having the same behavior, use the method [functions.flatten](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.functions.flatten) sending the `outer` parameter in True, drop extra columns, and rename index and value column names.

Copy code

```
df = spark.createDataFrame(
    [
        (1, ["foo", "bar"]),
        (2, []),
        (3, None)],
    ("id", "an_array"))

df.select(
    flatten(df.an_array, outer=True))\
    .drop("DATA", "SEQ", "KEY", "PATH", "THIS")\
    .rename({"INDEX": "pos", "VALUE": "col"}).show()
```

##### Scenario 2

**Input**

Below is another example of the usage of posexplode\_outer passing a **map/dictionary (keys/values)**

Copy code

```
df = spark.createDataFrame(
    [
        (1, {"x": 1.0}),
        (2, {}),
        (3, None)],
    ("id", "a_map"))

df.select(posexplode_outer(df.a_map)).show()
```

**Output**

The tool adds the EWI `SPRKPY1043` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame(
    [
        (1, {"x": "Ashi Garami"}),
        (2, {}),
        (3, None)],
    ("id", "a_map"))
#EWI: SPRKPY1043 => pyspark.sql.functions.posexplode_outer has a workaround, see documentation for more info

df.select(posexplode_outer(df.a_map)).show()
```

**Recommended fix**

As a workaround, you can use [functions.row\_number](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/api/snowflake.snowpark.functions.row_number.html) to get the position and [functions.explode\_outer](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.explode_outer) with the name of the field to get the value of the key/value for dictionaries.

Copy code

```
df = spark.createDataFrame(
    [
        (1, {"x": "Ashi Garami"}),
        (2,  {}),
        (3, None)],
    ("id", "a_map"))

window = Window.orderBy(col("id").asc())

df.select(
    row_number().over(window).alias("pos"),
          explode_outer(df.a_map)).show()
```

**Note:** using row\_number is not fully equivalent, because it starts with 1 (not zero as spark method)

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1044

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.4.0](/migrations/sma-docs/general/release-notes/old-version-release-notes/sc-spark-python-release-notes/README)

Message: pyspark.sql.functions.split has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.split](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.split.html) which has a workaround.

#### Scenarios

There are a couple of scenarios depending on the amount of parameters passed to the method.

##### Scenario 1

**Input**

Below is an example when the function `split` has just the *str* and *pattern* parameters

Copy code

```
F.split('col', '\\|')
```

**Output**

The tool shows the EWI `SPRKPY1044` indicating there is a workaround.

Copy code

```
#EWI: SPRKPY1044 => pyspark.sql.functions.split has a workaround, see the documentation for more info
F.split('col', '\\|')
```

**Recommended fix**

As a workaround, you can call the function [snowflake.snowpark.functions.lit](https://docs.snowflake.com/ko/developer-guide/snowpark/reference/python/api/snowflake.snowpark.functions.lit.html) with the pattern parameter and send it into the split.

Copy code

```
F.split('col', lit('\\|'))
## the result of lit will be sent to the split function
```

### Scenario 2

**Input**

Below is another example when the function `split` has the *str, pattern, and limit* parameters.

Copy code

```
F.split('col', '\\|', 2)
```

**Output**

The tool shows the EWI `SPRKPY1044` indicating there is a workaround.

Copy code

```
#EWI: SPRKPY1044 => pyspark.sql.functions.split has a workaround, see the documentation for more info
F.split('col', '\\|', 2)
```

**Recommended fix**

This specific scenario is not supported.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1045

Message: pyspark.sql.functions.map\_values has a workaround

Category: Warning.

### Description

This function is used to extract the list of values from a column that contains a **map/dictionary (keys/values)**.

The issue appears when the tool detects the usage of [pyspark.sql.functions.map\_values](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.map_values.html) which has a workaround.

#### Scenario

**Input**

Below is an example of the usage of the method `map_values`.

Copy code

```
df = spark.createDataFrame(
    [(1, {'Apple': 'Fruit', 'Potato': 'Vegetable'})],
    ("id", "a_map"))

df.select(map_values("a_map")).show()
```

**Output**

The tool adds the EWI `SPRKPY1045` indicating that a workaround can be implemented.

Copy code

```
df = spark.createDataFrame(
    [(1, {'Apple': 'Fruit', 'Potato': 'Vegetable'})],
    ("id", "a_map"))
#EWI: SPRKPY1045 => pyspark.sql.functions.map_values has a workaround, see documentation for more info

df.select(map_values("a_map")).show()
```

**Recommended fix**

As a workaround, you can create an [udf](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.udf) to get the values for a column. The below example shows how to create the udf, then assign it to `F.map_values`, and then make use of it.

Copy code

```
from snowflake.snowpark import functions as F
from snowflake.snowpark.types import ArrayType, MapType

map_values_udf=None

def map_values(map):
    global map_values_udf
    if not map_values_udf:
        def _map_values(map: dict)->list:
            return list(map.values())
        map_values_udf = F.udf(_map_values,return_type=ArrayType(),input_types=[MapType()],name="map_values",is_permanent=False,replace=True)
    return map_values_udf(map)

F.map_values = map_values

df.select(map_values(colDict))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1046

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.1.22](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.functions.monotonically\_increasing\_id has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.monotonically\_increasing\_id](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.monotonically_increasing_id.html) which has a workaround.

#### Scenario

**Input**

Below is an example of the usage of the method `monotonically_increasing_id`.

Copy code

```
from pyspark.sql import functions as F

spark.range(0, 10, 1, 2).select(F.monotonically_increasing_id()).show()
```

**Output**

The tool adds the EWI `SPRKPY1046` indicating that a workaround can be implemented.

Copy code

```
from pyspark.sql import functions as F
#EWI: SPRKPY1046 => pyspark.sql.functions.monotonically_increasing_id has a workaround, see documentation for more info
spark.range(0, 10, 1, 2).select(F.monotonically_increasing_id()).show()
```

**Recommended fix**

Update the tool version.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1047

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 4.6.0](/migrations/sma-docs/general/release-notes/README)

### Description

This issue appears when the tool detects the usage of [pyspark.context.SparkContext.setLogLevel](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.setLogLevel.html?highlight=pyspark%20context%20sparkcontext%20setloglevel#pyspark.SparkContext.setLogLevel) which has a workaround.

#### Scenario

**Input**

Below is an example of the usage of the method `setLogLevel`.

Copy code

```
sparkSession.sparkContext.setLogLevel("WARN")
```

**Output**

The tool adds the EWI `SPRKPY1047` indicating that a workaround can be implemented.

Copy code

```
#EWI: SPRKPY1047 => pyspark.context.SparkContext.setLogLevel has a workaround, see documentation for more info
sparkSession.sparkContext.setLogLevel("WARN")
```

**Recommended fix**

Replace the `setLogLevel` function usage with `logging.basicConfig` that provides a set of convenience functions for simple logging usage. In order to use it, we need to import two modules, “logging” and “sys”, and the level constant should be replaced using the “Level equivalent table”:

Copy code

```
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
```

- Level equivalent table

| Level source parameter | Level target parameter |
| --- | --- |
| “ALL” | *<mark style=”color:red;”>**This has no equivalent**</mark>* |
| “DEBUG” | logging.DEBUG |
| “ERROR” | logging.ERROR |
| “FATAL” | logging.CRITICAL |
| “INFO” | logging.INFO |
| “OFF” | logging.NOTSET |
| “TRACE” | *<mark style=”color:red;”>**This has no equivalent**</mark>* |
| “WARN” | logging.WARNING |

Expand

Show lessSee more

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1048

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.4.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.session.SparkSession.conf has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.session.SparkSession.conf](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.conf.html) which has a workaround.

#### Scenario

**Input**

Below is an example of how to set a configuration into the property `conf` .

Copy code

```
spark.conf.set("spark.sql.crossJoin.enabled", "true")
```

**Output**

The tool adds the EWI `SPRKPY1048` indicating that a workaround can be implemented.

Copy code

```
#EWI: SPRKPY1048 => pyspark.sql.session.SparkSession.conf has a workaround, see documentation for more info
spark.conf.set("spark.sql.crossJoin.enabled", "true")
```

**Recommended fix**

SparkSession.conf is used to pass some specific settings only used by Pyspark and doesn’t apply to Snowpark. You can remove or comment on the code

Copy code

```
#spark.conf.set("spark.sql.crossJoin.enabled", "true")
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1049

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.1.9](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.session.SparkSession.sparkContext has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.session.SparkSession.sparkContext](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.sparkContext.html) which has a workaround.

#### Scenario

**Input**

Below is an example that creates a spark session and then uses the `SparkContext` property to print the appName.

Copy code

```
print("APP Name :"+spark.sparkContext.appName())
```

**Output**

The tool adds the EWI `SPRKPY1049` indicating that a workaround can be implemented.

Copy code

```
#EWI: SPRKPY1049 => pyspark.sql.session.SparkSession.sparkContext has a workaround, see documentation for more info
print("APP Name :"+spark.sparkContext.appName())
```

**Recommended fix**

SparkContext is not supported in SnowPark but you can access the methods and properties from SparkContext directly from the Session instance.

Copy code

```
## Pyspark
print("APP Name :"+spark.sparkContext.appName())
can be used in SnowPark removing the sparkContext as:
#Manual adjustment in SnowPark
print("APP Name :"+spark.appName());
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1050

Message: pyspark.conf.SparkConf.set has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.conf.SparkConf.set](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.set.html) which has a workaround.

#### Scenario

**Input**

Below is an example that sets a variable using `conf.set`.

Copy code

```
conf = SparkConf().setAppName('my_app')

conf.set("spark.storage.memoryFraction", "0.5")
```

**Output**

The tool adds the EWI `SPRKPY1050` indicating that a workaround can be implemented.

Copy code

```
conf = SparkConf().setAppName('my_app')

#EWI: SPRKPY1050 => pyspark.conf.SparkConf.set has a workaround, see documentation for more info
conf.set("spark.storage.memoryFraction", "0.5")
```

**Recommended fix**

SparkConf.set is used to set a configuration setting only used by Pyspark and doesn’t apply to Snowpark. You can remove or comment on the code

Copy code

```
#conf.set("spark.storage.memoryFraction", "0.5")
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1051

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.4.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.session.SparkSession.Builder.master has a workaround

Category: Warning.

### Description

This issue appears when the tool detects [pyspark.sql.session.SparkSession.Builder.master](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.builder.master.html) usage which has a workaround.

#### Scenario

**Input**

Below is an example of the usage of the method `builder.master` to set the Spark Master URL to connect to local using 1 core.

Copy code

```
spark = SparkSession.builder.master("local[1]")
```

**Output**

The tool adds the EWI `SPRKPY1051` indicating that a workaround can be implemented.

Copy code

```
#EWI: SPRKPY1051 => pyspark.sql.session.SparkSession.Builder.master has a workaround, see documentation for more info
spark = Session.builder.master("local[1]")
```

**Recommended fix**

`pyspark.sql.session.SparkSession.Builder.master` is used to set up a Spark Cluster. Snowpark doesn’t use Spark Clusters so you can remove or comment the code.

Copy code

```
## spark = Session.builder.master("local[1]")
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1052

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.8.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.session.SparkSession.Builder.enableHiveSupport has a workaround

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.session.SparkSession.Builder.enableHiveSupport](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.builder.enableHiveSupport.html) which has a workaround.

#### Scenario

**Input**

Below is an example that configures the SparkSession and enables the hive support using the method `enableHiveSupport`.

Copy code

```
spark = Session.builder.appName("Merge_target_table")\
        .config("spark.port.maxRetries","100") \
        .enableHiveSupport().getOrCreate()
```

**Output**

The tool adds the EWI `SPRKPY1052` indicating that a workaround can be implemented.

Copy code

```
#EWI: SPRKPY1052 => pyspark.sql.session.SparkSession.Builder.enableHiveSupport has a workaround, see documentation for more info
spark = Session.builder.appName("Merge_target_table")\
        .config("spark.port.maxRetries","100") \
        .enableHiveSupport().getOrCreate()
```

**Recommended fix**

Remove the use of `enableHiveSupport` function because it is not needed in Snowpark.

Copy code

```
spark = Session.builder.appName("Merge_target_table")\
        .config("spark.port.maxRetries","100") \
        .getOrCreate()
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1053

Message: An error occurred when extracting the dbc files.

Category: Warning.

### Description

This issue appears when a dbc file cannot be extracted. This warning could be caused by one or more of the following reasons: Too heavy, inaccessible, read-only, etc.

#### Additional recommendations

- As a workaround, you can check the size of the file if it is too heavy to be processed. Also, analyze whether the tool can access it to avoid any access issues.
- For more support, you can email us at [snowconvert-info@snowflake.com](mailto:snowconvert-info@snowflake.com). If you have a contract for support with Snowflake, reach out to your sales engineer and they can direct your support needs.

## SPRKPY1080

Message: The value of SparkContext is replaced with ‘session’ variable.

Category: Warning

### Description

Spark context is stored into a variable called session that creates a Snowpark Session.

#### Scenario

**Input**

This snippet describes a SparkContext

Copy code

```
## Input Code
from pyspark import SparkContext
from pyspark.sql import SparkSession

def example1():

    sc = SparkContext("local[*]", "TestApp")

    sc.setLogLevel("ALL")
    sc.setLogLevel("DEBUG")
```

**Output**

In this output code SMA has replaced the PySpark.SparkContext by a SparkSession , Note that SMA also add a template to replace the connection in the “connection.json” file and then load this configuration on the connection\_parameter variable.

Copy code

```
## Output Code
import logging
import sys
import json
from snowflake.snowpark import Session

def example1():
    jsonFile = open("connection.json")
    connection_parameter = json.load(jsonFile)
    jsonFile.close()
    #EWI: SPRKPY1080 => The value of SparkContext is replaced with 'session' variable.
    sc = Session.builder.configs(connection_parameter).getOrCreate()
    sc.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
    logging.basicConfig(stream = sys.stdout, level = logging.NOTSET)
    logging.basicConfig(stream = sys.stdout, level = logging.DEBUG)
```

**Recommended fix**

The configuration file “connection.json” must be updated with the required connection information:

Copy code

```
{
  "user": "my_user",
  "password": "my_password",
  "account": "my_account",
  "role": "my_role",
  "warehouse": "my_warehouse",
  "database": "my_database",
  "schema": "my_schema"
}
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1054

Message: pyspark.sql.readwriter.DataFrameReader.format is not supported.

Category: Warning.

### Description

This issue appears when the [pyspark.sql.readwriter.DataFrameReader.format](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.format.html) has an argument that is not supported by Snowpark.

#### Scenarios

There are some scenarios depending on the type of format you are trying to load. It can be a `supported` , or `non-supported` format.

##### Scenario 1

**Input**

The tool analyzes the type of format that is trying to load, the supported formats are:

- Csv
- JSON
- Parquet
- Orc

The below example shows how the tool transforms the `format` method when passing a `Csv` value.

Copy code

```
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

df1 = spark.read.format('csv').load('/path/to/file')
```

**Output**

The tool transforms the `format` method into a `Csv` method call.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()

df1 = spark.read.csv('/path/to/file')
```

**Recommended fix**

In this case, the tool does not show the EWI, meaning there is no fix necessary.

##### Scenario 2

**Input**

The below example shows how the tool transforms the `format` method when passing a `Jdbc` value.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()

df2 = spark.read.format('jdbc') \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", "jdbc:mysql://localhost:3306/emp") \
    .option("dbtable", "employee") \
    .option("user", "root") \
    .option("password", "root") \
    .load()
```

**Output**

The tool shows the EWI `SPRKPY1054` indicating that the value “jdbc” is not supported.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()

#EWI: SPRKPY1054 => pyspark.sql.readwriter.DataFrameReader.format with argument value "jdbc" is not supported.
#EWI: SPRKPY1002 => pyspark.sql.readwriter.DataFrameReader.load is not supported

df2 = spark.read.format('jdbc') \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", "jdbc:mysql://localhost:3306/emp") \
    .option("dbtable", "employee") \
    .option("user", "root") \
    .option("password", "root") \
    .load()
```

**Recommended fix**

For the `not supported` scenarios, there is no specific fix since it depends on the files that are trying to be read.

##### Scenario 3

**Input**

The below example shows how the tool transforms the `format` method when passing a `CSV`, but using a variable instead.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()

myFormat = 'csv'
df3 = spark.read.format(myFormat).load('/path/to/file')
```

**Output**

Since the tool can’t determine the value of the variable in runtime, shows the EWI `SPRKPY1054` indicating that the value “” is not supported.

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.getOrCreate()

myFormat = 'csv'
#EWI: SPRKPY1054 => pyspark.sql.readwriter.DataFrameReader.format with argument value "" is not supported.
#EWI: SPRKPY1002 => pyspark.sql.readwriter.DataFrameReader.load is not supported
df3 = spark.read.format(myFormat).load('/path/to/file')
```

**Recommended fix**

As a workaround, you can check the value of the variable and add it as a string to the `format` call.

#### Additional recommendations

- The Snowpark location only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
- The documentation of methods supported by Snowpark can be found in the [documentation](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.20.0/snowpark/api/snowflake.snowpark.DataFrameReader#snowflake.snowpark.DataFrameReader)
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1055

Message: pyspark.sql.readwriter.DataFrameReader.option key value is not supported.

Category: Warning.

### Description

This issue appears when the `pyspark.sql.readwriter.DataFrameReader.option` key value is not supported by SnowFlake.

The tool analyzes the option call parameters and depends on the method (CSV or JSON or PARQUET) the key value might have or not have an equivalent in Snowpark, if all the parameters have an equivalent, the tool does not add the EWI, and it replaces the key value for his equivalent, otherwise, the tool adds the EWI.

**List of equivalences:**

- Equivalences for CSV:

| Spark option keys | Snowpark Equivalences |
| --- | --- |
| sep | FIELD\_DELIMITER |
| header | PARSE\_HEADER |
| lineSep | RECORD\_DELIMITER |
| pathGlobFilter | PATTERN |
| quote | FIELD\_OPTIONALLY\_ENCLOSED\_BY |
| nullValue | NULL\_IF |
| dateFormat | DATE\_FORMAT |
| timestampFormat | TIMESTAMP\_FORMAT |
| inferSchema | INFER\_SCHEMA |
| delimiter | FIELD\_DELIMITER |

Expand

Show lessSee more

- Equivalences for JSON:

| Spark option keys | Snowpark Equivalences |
| --- | --- |
| dateFormat | DATE\_FORMAT |
| timestampFormat | TIMESTAMP\_FORMAT |
| pathGlobFilter | PATTERN |

Expand

Show lessSee more

- Equivalences for PARQUET:

| Spark option keys | Snowpark Equivalences |
| --- | --- |
| pathGlobFilter | PATTERN |

Expand

Show lessSee more

Any other key option that’s not in one of the tables above, are not supported or doesn’t have an equivalent in Snowpark. If that’s the case, the tool adds the EWI with the parameter information and removes it from the chain.

#### Scenarios

The below scenarios apply for CSV, JSON, and PARQUET.

There are a couple of scenarios depending on the value of the key used in the `option` method.

##### Scenario 1

**Input**

Below is an example of a `option` call using a `equivalent key`.

Copy code

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

## CSV example:
spark.read.option("header", True).csv(csv_file_path)

## Json example:
spark.read.option("dateFormat", "dd-MM-yyyy").json(json_file_path)

## Parquet example:
spark.read.option("pathGlobFilter", "*.parquet").parquet(parquet_file_path)
```

**Output**

The tool transforms the key with the correct equivalent.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()

## CSV example:
spark.read.option("PARSE_HEADER", True).csv(csv_file_path)

## Json example:
spark.read.option("DATE_FORMAT", "dd-MM-yyyy").json(json_file_path)

## Parquet example:
spark.read.option("PATTERN", "*.parquet").parquet(parquet_file_path)
```

**Recommended fix**

Since the tool transforms the value of the key, there is no necessary fix.

### Scenario 2

**Input**

Below is an example of a `option` call using a `non-equivalent key`.

Copy code

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

## CSV example:
spark.read.option("anotherKeyValue", "myVal").csv(csv_file_path)

## Json example:
spark.read.option("anotherKeyValue", "myVal").json(json_file_path)

## Parquet example:
spark.read.option("anotherKeyValue", "myVal").parquet(parquet_file_path)
```

**Output**

The tool adds the EWI `SPRKPY1055` indicating the key is not supported and removes the `option` call.

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.getOrCreate()

## CSV example:
#EWI: SPRKPY1055 => pyspark.sql.readwriter.DataFrameReader.option with key value "anotherKeyValue" is not supported.
spark.read.csv(csv_file_path)

## Json example:
#EWI: SPRKPY1055 => pyspark.sql.readwriter.DataFrameReader.option with key value "anotherKeyValue" is not supported.
spark.read.json(json_file_path)

## Parquet example:
#EWI: SPRKPY1055 => pyspark.sql.readwriter.DataFrameReader.option with key value "anotherKeyValue" is not supported.
spark.read.parquet(parquet_file_path)
```

**Recommended fix**

It is recommended to check the behavior after the transformation.

### Additional recommendations

- When non-equivalent parameters are present, it is recommended to check the behavior after the transformation.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1056

Warning

This issue code has been **deprecated**

Message: pyspark.sql.readwriter.DataFrameReader.option argument ***<argument\_name>*** is not a literal and can’t be evaluated

Category: Warning

### Description

This issue appears when the argument’s key or value of the [pyspark.sql.readwriter.DataFrameReader.option](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.option.html) function is not a literal value (for example a variable). The SMA does a static analysis of your source code, and therefore it is not possible to evaluate the content of the argument.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.readwriter.DataFrameReader.option` function that generates this EWI.

Copy code

```
my_value = ...
my_option = ...

df1 = spark.read.option("dateFormat", my_value).format("csv").load('filename.csv')
df2 = spark.read.option(my_option, "false").format("csv").load('filename.csv')
```

**Output**

The SMA adds the EWI `SPRKPY1056` to the output code to let you know that the argument of this function is not a literal value, and therefore it could not be evaluated by the SMA.

Copy code

```
my_value = ...
my_option = ...

#EWI: SPRKPY1056 => pyspark.sql.readwriter.DataFrameReader.option argument "dateFormat" is not a literal and can't be evaluated
df1 = spark.read.option("dateFormat", my_value).format("csv").load('filename.csv')
#EWI: SPRKPY1056 => pyspark.sql.readwriter.DataFrameReader.option argument key is not a literal and can't be evaluated
df2 = spark.read.option(my_option, "false").format("csv").load('filename.csv')
```

**Recommended fix**

Even though the SMA was unable to evaluate the argument, it does not mean that it is not supported by Snowpark. Please make sure that the value of the argument is valid and equivalent in Snowpark by checking the [documentation](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameReader.option).

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1057

Warning

This Issue Code has been **deprecated** since [Spark Conversion Core Version 4.8.0](/migrations/sma-docs/general/release-notes/README)

Message: [PySpark Dataframe Option](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.option.html#pyspark.sql.DataFrameReader.option) argument contains a value that is not a literal, therefore cannot be evaluated

Category: Warning.

### Description

This issue code is deprecated. If you are using an older version, please upgrade to the latest.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1058

Message: < method > with < key > Platform specific key is not supported.

Category: ConversionError

### Description

The `get` and `set` methods from [pyspark.sql.conf.RuntimeConfig](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.conf.RuntimeConfig.html#pyspark.sql.conf.RuntimeConfig) are not supported with a Platform specific key.

#### Scenarios

Not all usages of `get` or `set` methods are going to have an EWI in the output code. This EWI appears when the tool detects the usage of these methods with a Platform specific key which is not supported.

##### Scenario 1

**Input**

Below is an example of the `get` or `set` methods with supported keys in Snowpark.

Copy code

```
session.conf.set("use_constant_subquery_alias", False)
spark.conf.set("sql_simplifier_enabled", True)

session.conf.get("use_constant_subquery_alias")
session.conf.get("use_constant_subquery_alias")
```

**Output**

Since the keys are supported in Snowpark the tool does not add the EWI on the output code.

Copy code

```
session.conf.set("use_constant_subquery_alias", True)
session.conf.set("sql_simplifier_enabled", False)

session.conf.get("use_constant_subquery_alias")
session.conf.get("sql_simplifier_enabled")
```

**Recommended fix**

There is no recommended fix for this scenario.

##### Scenario 2

**Input**

Below is an example using not supported keys.

Copy code

```
data =
    [
      ("John", 30, "New York"),
      ("Jane", 25, "San Francisco")
    ]

session.conf.set("spark.sql.shuffle.partitions", "50")
spark.conf.set("spark.yarn.am.memory", "1g")

session.conf.get("spark.sql.shuffle.partitions")
session = spark.conf.get("spark.yarn.am.memory")

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
```

**Output**

The tool adds this EWI `SPRKPY1058` on the output code to let you know that these methods are not supported with a Platform specific key.

Copy code

```
data =
    [
      ("John", 30, "New York"),
      ("Jane", 25, "San Francisco")
    ]

#EWI: SPRKPY1058 => pyspark.sql.conf.RuntimeConfig.set method with this "spark.sql.shuffle.partitions" Platform specific key is not supported.
spark.conf.set("spark.sql.shuffle.partitions", "50")
#EWI: SPRKPY1058 => pyspark.sql.conf.RuntimeConfig.set method with this "spark.yarn.am.memory" Platform specific key is not supported.
spark.conf.set("spark.yarn.am.memory", "1g")

#EWI: SPRKPY1058 => pyspark.sql.conf.RuntimeConfig.get method with this "spark.sql.shuffle.partitions" Platform specific key is not supported.
spark.conf.get("spark.sql.shuffle.partitions")
#EWI: SPRKPY1058 => pyspark.sql.conf.RuntimeConfig.get method with this "spark.yarn.am.memory" Platform specific key is not supported.
spark.conf.get("spark.yarn.am.memory")

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
```

**Recommended fix**

The recommended fix is to remove these methods.

Copy code

```
data =
    [
      ("John", 30, "New York"),
      ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1059

Warning

This issue code has been **deprecated** since [Spark Conversion Core Version 2.45.1](/migrations/sma-docs/general/release-notes/README)

Message: [pyspark.storagelevel.StorageLevel](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.StorageLevel.html) has a workaround, see documentation.

Category: Warning

### Description

Currently, the use of StorageLevel is not required in Snowpark since [Snowflake controls the storage](https://docs.snowflake.com/en/user-guide/intro-key-concepts#database-storage). For more information, you can refer to the EWI [SPRKPY1072](/migrations/sma-docs/issue-analysis/issue-codes-by-source/python/README)

#### Additional recommendations

- Upgrade your application to the latest version.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1060

Message: The authentication mechanism is connection.json (template provided).

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.conf.SparkConf](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.html).

#### Scenario

**Input**

Since the authentication mechanism is different in Snowpark, the tool removes the usages and creates a **connection configuration file (connection.json)** instead.

Copy code

```
from pyspark import SparkConf

my_conf = SparkConf(loadDefaults=True)
```

**Output**

The tool adds the EWI `SPRKPY1060` indicating that the authentication mechanism is different.

Copy code

```
#EWI: SPRKPY1002 => pyspark.conf.SparkConf is not supported
#EWI: SPRKPY1060 => The authentication mechanism is connection.json (template provided).
#my_conf = Session.builder.configs(connection_parameter).getOrCreate()

my_conf = None
```

**Recommended fix**

To create a connection it is necessary that you fill in the information in the `connection.json` file.

Copy code

```
{
  "user": "<USER>",
  "password": "<PASSWORD>",
  "account": "<ACCOUNT>",
  "role": "<ROLE>",
  "warehouse": "<WAREHOUSE>",
  "database": "<DATABASE>",
  "schema": "<SCHEMA>"
}
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1061

Message: Snowpark does not support unix\_timestamp functions

Category: Warning

### Description

In Snowpark, the first parameter is mandatory; the issue appears when the tool detects the usage of [pyspark.sql.functions.unix\_timestamp](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.unix_timestamp.html) with no parameters.

#### Scenario

**Input**

Below an example that calls the `unix_timestamp` method without parameters.

Copy code

```
data = [["2015-04-08", "10"],["2015-04-10", "15"]]

df = spark.createDataFrame(data, ['dt', 'val'])
df.select(unix_timestamp()).show()
```

**Output**

The Snowpark signature for this function `unix_timestamp(e: ColumnOrName, fmt: Optional["Column"] = None)`, as you can notice the first parameter it’s required.

The tool adds this EWI `SPRKPY1061` to let you know that function unix\_timestamp with no parameters it’s not supported in Snowpark.

Copy code

```
data = [["2015-04-08", "10"],["2015-04-10", "15"]]

df = spark.createDataFrame(data, ['dt', 'val'])
#EWI: SPRKPY1061 => Snowpark does not support unix_timestamp functions with no parameters. See documentation for more info.
df.select(unix_timestamp()).show()
```

**Recommended fix**

As a workaround, you can add at least the name or column of the timestamp string.

Copy code

```
data = [["2015-04-08", "10"],["2015-04-10", "15"]]

df = spark.createDataFrame(data, ["dt", "val"])
df.select(unix_timestamp("dt")).show()
```

#### Additional recommendations

- You also can add the [current\_timestamp()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.current_timestamp) as the first parameter.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1062

Message: Snowpark does not support GroupedData.pivot without parameter “values”.

Category: Warning

### Description

This issue appears when the SMA detects the usage of the [pyspark.sql.group.GroupedData.pivot](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.pivot.html) function without the “values” parameter *(the list of values to pivot on)*.

At the moment, the Snowpark Python pivot function requires you to explicitly specify the list of distinct values to pivot on.

#### Scenarios

##### Scenario 1

**Input**

The SMA detects an expression that matches the pattern `dataFrame.groupBy("columnX").pivot("columnY")` and the pivot does not have the **values** parameter.

Copy code

```
df.groupBy("date").pivot("category").sum("amount")
```

**Output**

The SMA adds an EWI message indicating that the pivot function without the “values” parameter is not supported.

In addition, it will add as a second parameter of the pivot function a list comprehension that calculates the list of values that will be translated into columns. Keep in mind that this operation is not efficient for large datasets, and it is advisable to indicate the values explicitly.

Copy code

```
#EWI: SPRKPY1062 => pyspark.sql.group.GroupedData.pivot without parameter 'values' is not supported. See documentation for more info.
df.groupBy("date").pivot("category", [v[0] for v in df.select("category").distinct().limit(10000).collect()]).sum("amount")
```

**Recommended fix**

For this scenario the SMA add a second parameter of the pivot function a list comprehension that calculates the list of values that will be translated into columns, but you can a list of distinct values to pivot on, as follows:

Copy code

```
df = spark.createDataFrame([
      Row(category="Client_ID", date=2012, amount=10000),
      Row(category="Client_name",   date=2012, amount=20000)
  ])

df.groupBy("date").pivot("category", ["dotNET", "Java"]).sum("amount")
```

##### Scenario 2

**Input**

The SMA couldn’t detect an expression that matches the pattern `dataFrame.groupBy("columnX").pivot("columnY")` and the pivot does not have the **values** parameter.

Copy code

```
df1.union(df2).groupBy("date").pivot("category").sum("amount")
```

**Output**

The SMA adds an EWI message indicating that the pivot function without the “values” parameter is not supported.

Copy code

```
#EWI: SPRKPY1062 => pyspark.sql.group.GroupedData.pivot without parameter 'values' is not supported. See documentation for more info.
df1.union(df2).groupBy("date").pivot("category").sum("amount")
```

**Recommended fix**

Add a list of distinct values to pivot on, as follows:

Copy code

```
df = spark.createDataFrame([
      Row(course="dotNET", year=2012, earnings=10000),
      Row(course="Java",   year=2012, earnings=20000)
  ])

df.groupBy("year").pivot("course", ["dotNET", "Java"]).sum("earnings").show()
```

#### Additional recommendations

- Calculating the list of distinct values to pivot on is not an efficient operation on large datasets and could become a blocking call. Please consider indicating the list of distinct values to pivot on explicitly.
- If you don’t want to specify the list of distinct values to pivot on explicitly (not advisable), you can add the following code as the second argument of the pivot function to infer the values at runtime\*

Copy code

```
[v[0] for v in <df>.select(<column>).distinct().limit(<count>).collect()]]
```

**Replace** `<df>` with the corresponding DataFrame, with the column to pivot and with the number of rows to select.

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1063

Message: pyspark.sql.pandas.functions.pandas\_udf has workaround.

Category: Warning

### Description

This issue appears when the tool detects the usage of [pyspark.sql.pandas.functions.pandas\_udf](https://spark.apache.org/docs/3.1.2/api/python/reference/api/pyspark.sql.functions.pandas_udf.html) which has a workaround.

#### Scenario

**Input**

The pandas\_udf function is used to create a user defined functions that works with large amounts of data.

Copy code

```
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def modify_df(pdf):
    return pd.DataFrame({'result': pdf['col1'] + pdf['col2'] + 1})
df = spark.createDataFrame([(1, 2), (3, 4), (1, 1)], ["col1", "col2"])
new_df = df.groupby().apply(modify_df)
```

**Output**

The SMA adds an EWI message indicating that the pandas\_udf has a workaround.

Copy code

```
#EWI: SPRKPY1063 => pyspark.sql.pandas.functions.pandas_udf has a workaround, see documentation for more info
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)

def modify_df(pdf):
    return pd.DataFrame({'result': pdf['col1'] + pdf['col2'] + 1})

df = spark.createDataFrame([(1, 2), (3, 4), (1, 1)], ["col1", "col2"])

new_df = df.groupby().apply(modify_df)
```

**Recommended fix**

Specify explicitly the parameters types as a new parameter `input_types`, and remove `functionType` parameter if applies. Created function must be called inside a select statement.

Copy code

```
@pandas_udf(
    return_type = schema,
    input_types = [PandasDataFrameType([IntegerType(), IntegerType()])]
)

def modify_df(pdf):
    return pd.DataFrame({'result': pdf['col1'] + pdf['col2'] + 1})

df = spark.createDataFrame([(1, 2), (3, 4), (1, 1)], ["col1", "col2"])

new_df = df.groupby().apply(modify_df) # You must modify function call to be a select and not an apply
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1064

Message: The ***Spark element*** does not apply since snowflake uses snowpipe mechanism instead.

Category: Warning

### Description

This issue appears when the tool detects the usage of any element from the pyspark.streaming library:

- [pyspark.streaming.DStream](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.streaming.DStream.html)
- [pyspark.streaming.StreamingContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.streaming.StreamingContext.html)
- pyspark.streaming.listener.StreamingListener.

#### Scenario

**Input**

Below is an example with one of the elements that trigger this EWI.

Copy code

```
from pyspark.streaming.listener import StreamingListener

var = StreamingListener.Java
var.mro()

df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])
df.show()
```

**Output**

The SMA adds the EWI `SPRKPY1064` on the output code to let you know that this function does not apply.

Copy code

```
#EWI: SPRKPY1064 => The element does not apply since snowflake uses snowpipe mechanism instead.

var = StreamingListener.Java
var.mro()

df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])
df.show()
```

**Recommended fix**

The SMA removes the import statement and adds the issue to the *Issues.csv* inventory, remove any usages of the Spark element.

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])
df.show()
```

#### Additional recommendations

- Check the documentation for [Snowpipe](https://docs.snowflake.com/en/user-guide/data-load-snowpipe-intro) to see how it fits to the current scenario.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1065

Message: The pyspark.context.SparkContext.broadcast does not apply since snowflake use data-clustering mechanism to compute the data.

Category: Warning

### Description

This issue appears when the tool detects the usage of element [pyspark.context.SparkContext.broadcast](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.broadcast.html), which is not necessary due to the use of [data-clustering](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions) of Snowflake.

**Input code**

In this example a broadcast variable is created, these variables allows data to be share more efficiently through all nodes.

Copy code

```
sc = SparkContext(conf=conf_spark)

mapping = {1: 10001, 2: 10002}

bc = sc.broadcast(mapping)
```

**Output code**

The SMA adds an EWI message indicating that the broadcast it’s not required.

Copy code

```
sc = conf_spark

mapping = {1: 10001, 2: 10002}
#EWI: SPRKPY1065 => The element does not apply since snowflake use data-clustering mechanism to compute the data.

bc = sc.broadcast(mapping)
```

**Recommended fix**

Remove any usages of pyspark.context.SparkContext.broadcast.

Copy code

```
sc = conf_spark

mapping = {1: 10001, 2: 10002}
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1066

Message: The Spark element does not apply since snowflake use micro-partitioning mechanism are created automatically.

Category: Warning

### Description

This issue appears when the tool detects the usage of elements related to partitions:

- [pyspark.sql.catalog.Catalog.recoverPartitions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.Catalog.recoverPartitions.html)
- [pyspark.sql.dataframe.DataFrame.foreachPartition](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.foreachPartition.html)
- [pyspark.sql.dataframe.DataFrame.sortWithinPartitions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sortWithinPartitions.html)
- [pyspark.sql.functions.spark\_partition\_id](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.spark_partition_id.html)

Those elements do not apply due the use of [micro-partitions](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions) of Snowflake.

**Input code**

In this example [sortWithinPartitions](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.sortWithinPartitions.html) it’s used to create a partition in a DataFrame sorted by the specified column.

Copy code

```
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], schema=["age", "name"])
df.sortWithinPartitions("age", ascending=False)
```

**Output code**

The SMA adds an EWI message indicating that Spark element is not required.

Copy code

```
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], schema=["age", "name"])
#EWI: SPRKPY1066 => The element does not apply since snowflake use micro-partitioning mechanism are created automatically.
df.sortWithinPartitions("age", ascending=False)
```

**Recommended fix**

Remove the usage of the element.

Copy code

```
df = spark.createDataFrame([(2, "Alice"), (5, "Bob")], schema=["age", "name"])
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1067

Message: The pyspark.sql.functions.split has parameters that are not supported in Snowpark.

Category: Warning

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.split](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.split.html) with more than two parameters or a regex pattern as a parameter; both cases are not supported.

#### Scenarios

##### Scenario 1

**Input code**

In this example the split function has more than two parameters.

Copy code

```
df.select(split(columnName, ",", 5))
```

**Output code**

The tool adds this EWI on the output code to let you know that this function is not supported when it has more than two parameters.

Copy code

```
#EWI: SPRKPY1067 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info.
df.select(split(columnName, ",", 5))
```

**Recommended fix**

Keep the split function with only two parameters.

Copy code

```
df.select(split(columnName, ","))
```

##### Scenario 2

**Input code**

In this example the split function has a regex pattern as a parameter.

Copy code

```
df.select(split(columnName, "^([\d]+-[\d]+-[\d])"))
```

**Output code**

The tool adds this EWI on the output code to let you know that this function is not supported when it has a regex pattern as a parameter.

Copy code

```
#EWI: SPRKPY1067 => Snowpark does not support split functions with more than two parameters or containing regex pattern. See documentation for more info.
df.select(split(columnName, "^([\d]+-[\d]+-[\d])"))
```

**Recommended fix**

The spark signature for this method `functions.split(str: ColumnOrName, pattern: str, limit: int = - 1)` not exactly match with the method in Snowpark `functions.split(str: Union[Column, str], pattern: Union[Column, str])` so for now the scenario using regular expression does not have a recommended fix.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1068

Message: toPandas contains columns of type ArrayType that is not supported and has a workaround.

Category: Warning

### Description

[pyspark.sql.DataFrame.toPandas](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.toPandas.html) doesn’t work properly If there are columns of type ArrayType. The workaround for these cases is converting those columns into a Python Dictionary by using json.loads method.

#### Scenario

**Input**

ToPandas returns the data of the original DataFrame as a Pandas DataFrame.

Copy code

```
sparkDF = spark.createDataFrame([
Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0))
])

pandasDF = sparkDF.toPandas()
```

**Output**

The tool adds this EWI to let you know that toPandas is not supported If there are columns of type ArrayType, but has workaround.

Copy code

```
sparkDF = spark.createDataFrame([
Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0))
])
#EWI: SPRKPY1068 => toPandas doesn't work properly If there are columns of type ArrayType. The workaround for these cases is converting those columns into a Python Dictionary by using json.loads method. example: df[colName] = json.loads(df[colName]).
pandasDF = sparkDF.toPandas()
```

**Recommended fix**

Copy code

```
pandas_df = sparkDF.toPandas()​
​
## check/convert all resulting fields from calling toPandas when they are of
## type ArrayType,
## they will be reasigned by converting them into a Python Dictionary
## using json.loads method​
​
for field in pandas_df.schema.fields:
    if isinstance(field.datatype, ArrayType):
        pandas_df[field.name] = pandas_df[field.name].apply(lambda x: json.loads(x) if x is not None else x)
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1069

Message: If partitionBy parameter is a list, Snowpark will throw an error.

Category: Warning

### Description

When there is a usage of [pyspark.sql.readwriter.DataFrameWriter.parquet](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.parquet.html) method where it comes to the parameter `partitionBy`, the tool shows the EWI.

This is because in Snowpark the [DataFrameWriter.parquet](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.parquet) only supports a `ColumnOrSqlExpr` as a partitionBy parameter.

#### Scenarios

##### Scenario 1

**Input code:**

For this scenario the partitionBy parameter is not a list.

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])

df.write.parquet(file_path, partitionBy="age")
```

**Output code:**

The tool adds the EWI `SPRKPY1069` to let you know that Snowpark throws an error if parameter is a list.

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])

#EWI: SPRKPY1069 => If partitionBy parameter is a list, Snowpark will throw an error.
df.write.parquet(file_path, partition_by = "age", format_type_options = dict(compression = "None"))
```

**Recommended fix**

There is not a recommended fix for this scenario because the tool always adds this EWI just in case the partitionBy parameter is a list. Remember that in Snowpark, only accepts cloud locations using a [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])

stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
Session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {stage}').show()
Session.file.put(f"file:///path/to/data/file.parquet", f"@{stage}")

df.write.parquet(stage, partition_by = "age", format_type_options = dict(compression = "None"))
```

##### Scenario 2

**Input code:**

For this scenario the partitionBy parameter is a list.

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])

df.write.parquet(file_path, partitionBy=["age", "name"])
```

**Output code:**

The tool adds the EWI `SPRKPY1069` to let you know that Snowpark throws an error if parameter is a list.

Copy code

```
df = spark.createDataFrame([(25, "Alice", "150"), (30, "Bob", "350")], schema=["age", "name", "value"])

#EWI: SPRKPY1069 => If partitionBy parameter is a list, Snowpark will throw an error.
df.write.parquet(file_path, partition_by = ["age", "name"], format_type_options = dict(compression = "None"))
```

**Recommended fix**

If the value of the parameter is a `list`, then replace it with a `ColumnOrSqlExpr`.

Copy code

```
df.write.parquet(file_path, partition_by = sql_expr("age || name"), format_type_options = dict(compression = "None"))
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1070

Message: The `mode` argument is transformed to `overwrite`, check the variable value and set the corresponding bool value.

Category: Warning

### Description

When there is a usage of:

- [pyspark.sql.readwriter.DataFrameWriter.csv](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.csv.html)
- [pyspark.sql.readwriter.DataFrameWriter.json](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.json.html)
- [pyspark.sql.readwriter.DataFrameWriter.parquet](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.json.html)

The tool analyzes the parameter `mode` to determine if the value is `overwrite`.

#### Scenarios

##### Scenario 1

**Input code**

For this scenario the tool detects that the mode parameter can set the corresponding bool value.

Copy code

```
df.write.csv(file_path, mode="overwrite")
```

**Output code:**

The SMA tool analyzes the mode parameter, determine that the value is `overwrite` and set the corresponding bool value

Copy code

```
df.write.csv(file_path, format_type_options = dict(compression = "None"), overwrite = True)
```

**Recommended fix**

There is not a recommended fix for this scenario because the tool performed the corresponding transformation.

**Scenario 2:**

**Input code**

In this scenario the tool can’t validate the value is `overwrite`.

Copy code

```
df.write.csv(file_path, mode=myVal)
```

**Output code:**

The SMA adds an EWI message indicating that the mode parameter was transformed to ‘overwrite’, but it’s also to let you know that it is better to check the variable value and set the correct bool value.

Copy code

```
#EWI: SPRKPY1070 => The 'mode' argument is transformed to 'overwrite', check the variable value and set the corresponding bool value.
df.write.csv(file_path, format_type_options = dict(compression = "None"), overwrite = myVal)
```

**Recommended fix**

Check for the value of the parameter `mode` and add the correct value for the parameter `overwrite`.

Copy code

```
df.write.csv(file_path, format_type_options = dict(compression = "None"), overwrite = True)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1071

Message: The function pyspark.rdd.RDD.getNumPartitions is not required in Snowpark. So, you should remove all references.

Category: Warning

### Description

This issue appears when the tool finds the use of the [pyspark.rdd.RDD.getNumPartitions](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.getNumPartitions.html) function. Snowflake uses micro-partitioning mechanism, so the use of this function is not required.

#### Scenario

**Input**

The getNumPartitions returns the quantity of partitions on a RDD.

Copy code

```
df = spark.createDataFrame([('2015-04-08',), ('5',), [Row(a=1, b="b")]], ['dt', 'num', 'row'])

print(df.getNumPartitions())
```

**Output**

The tool adds this EWI to let you know that getNumPartitions is not required.

Copy code

```
df = spark.createDataFrame([('2015-04-08',), ('5',), [Row(a=1, b="b")]], ['dt', 'num', 'row'])
#EWI: SPRKPY1071 => The getNumPartitions are not required in Snowpark. So, you should remove all references.

print(df.getNumPartitions())
```

**Recommended fix**

Remove all uses of this function.

Copy code

```
df = spark.createDataFrame([('2015-04-08',), ('5',), [Row(a=1, b="b")]], ['dt', 'num', 'row'])
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1072

Message: The use of StorageLevel is not required in Snowpark.

Category: Warning.

### Description

This issue appears when the tool finds the use of the [StorageLevel](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.StorageLevel.html) class, which works like “flags” to set the storage level. Since Snowflake controls the storage, the use of this function is not required.

#### Additional recommendations

- Remove all uses of this function.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1073

Message: pyspark.sql.functions.udf without parameters or return type parameter are not supported

Category: Warning.

### Description

This issue appears when the tool detects the usage of [pyspark.sql.functions.udf](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html) as function or decorator and is not supported in two specifics cases, when it has no parameters or return type parameter.

#### Scenarios

##### Scenario 1

**Input**

In Pyspark you can create an User Defined Function without input or return type parameters:

Copy code

```
from pyspark.sql import SparkSession, DataFrameStatFunctions
from pyspark.sql.functions import col, udf

spark = SparkSession.builder.getOrCreate()
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)

my_udf = udf(lambda s: len(s))
df.withColumn('Len Value' ,my_udf(col('Value')) ).show()
```

**Output**

Snowpark requires the input and return types for Udf function. Because they are not provided and SMA cannot resolve these parameters.

Copy code

```
from snowflake.snowpark import Session, DataFrameStatFunctions
from snowflake.snowpark.functions import col, udf

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)
#EWI: SPRKPY1073 => pyspark.sql.functions.udf function without the return type parameter is not supported. See documentation for more info.
my_udf = udf(lambda s: len(s))

df.withColumn('Len Value' ,my_udf(col('Value')) ).show()
```

**Recommended fix**

To fix this scenario is required to add the import for the returns types of the input and output, and then the parameters of return*type and input\_types[] on the [udf](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.udf) function \_my\_udf*.

Copy code

```
from snowflake.snowpark import Session, DataFrameStatFunctions
from snowflake.snowpark.functions import col, udf
from snowflake.snowpark.types import IntegerType, StringType

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)

my_udf = udf(lambda s: len(s), return_type=IntegerType(), input_types=[StringType()])

df.with_column("result", my_udf(df.Value)).show()
```

##### Scenario 2

In PySpark you can use a @udf decorator without parameters

**Input**

Copy code

```
from pyspark.sql.functions import col, udf

spark = SparkSession.builder.getOrCreate()
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)

@udf()
def my_udf(str):
    return len(str)

df.withColumn('Len Value' ,my_udf(col('Value')) ).show()
```

**Output**

In Snowpark all the parameters of a [udf](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.udf) decorator are required.

Copy code

```
from snowflake.snowpark.functions import col, udf

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)

#EWI: SPRKPY1073 => pyspark.sql.functions.udf decorator without parameters is not supported. See documentation for more info.

@udf()
def my_udf(str):
    return len(str)

df.withColumn('Len Value' ,my_udf(col('Value')) ).show()
```

**Recommended fix**

To fix this scenario is required to add the import for the returns types of the input and output, and then the parameters of return\_type and input\_types[] on the [udf](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.functions.udf) @udf decorator.

Copy code

```
from snowflake.snowpark.functions import col, udf
from snowflake.snowpark.types import IntegerType, StringType

spark = Session.builder.getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})
data = [['Q1', 'Test 1'],
        ['Q2', 'Test 2'],
        ['Q3', 'Test 1'],
        ['Q4', 'Test 1']]

columns = ['Quadrant', 'Value']
df = spark.createDataFrame(data, columns)

@udf(return_type=IntegerType(), input_types=[StringType()])
def my_udf(str):
    return len(str)

df.withColumn('Len Value' ,my_udf(col('Value')) ).show()
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1074

Message: File has mixed indentation (spaces and tabs).

Category: Parsing error.

### Description

This issue appears when the tool detects the file has a mixed indentation. It means, file has a combination of spaces and tabs to indent code lines.

#### Scenario

**Input**

In Pyspark you can mix spaces and tabs for the indentation level.

Copy code

```
def foo():
    x = 5 # spaces
    y = 6 # tab
```

**Output**

SMA cannot handle mixed indentation markers. When this is detected on a python code file SMA adds the EWI SPRKPY1074 on first line.

Copy code

```
## EWI: SPRKPY1074 => File has mixed indentation (spaces and tabs).
## This file was not converted, so it is expected to still have references to the Spark API
def foo():
    x = 5 # spaces
    y = 6 # tabs
```

**Recommended fix**

The solution is to make all the indentation symbols the same.

Copy code

```
def foo():
  x = 5 # tab
  y = 6 # tab
```

### Additional recommendations

- Useful indent tools [PEP-8](https://peps.python.org/pep-0008/) and [Reindent](https://pypi.org/project/reindent/).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1075

Category

Warning.

### Description

The parse\_json does not apply schema validation, if you need to filter/validate based on schema you might need to introduce some logic.

### Example

**Input**

Copy code

```
df.select(from_json(df.value, Schema))
df.select(from_json(schema=Schema, col=df.value))
df.select(from_json(df.value, Schema, option))
```

**Output**

Copy code

```
#EWI: SPRKPY1075 => The parse_json does not apply schema validation, if you need to filter/validate based on schema you might need to introduce some logic.
df.select(parse_json(df.value))
#EWI: SPRKPY1075 => The parse_json does not apply schema validation, if you need to filter/validate based on schema you might need to introduce some logic.
df.select(parse_json(df.value))
#EWI: SPRKPY1075 => The parse_json does not apply schema validation, if you need to filter/validate based on schema you might need to introduce some logic.
df.select(parse_json(df.value))
```

For the function from\_json the schema is not really passed for inference it is used for validation. See this examples:

Copy code

```
data = [
    ('{"name": "John", "age": 30, "city": "New York"}',),
    ('{"name": "Jane", "age": "25", "city": "San Francisco"}',)
]

df = spark.createDataFrame(data, ["json_str"])
```

**Example 1: Enforce Data Types and Change Column Names:**

Copy code

```
## Parse JSON column with schema
parsed_df = df.withColumn("parsed_json", from_json(col("json_str"), schema))

parsed_df.show(truncate=False)

## +------------------------------------------------------+---------------------------+
## |json_str                                              |parsed_json                |
## +------------------------------------------------------+---------------------------+
## |{"name": "John", "age": 30, "city": "New York"}       |{John, 30, New York}       |
## |{"name": "Jane", "age": "25", "city": "San Francisco"}|{Jane, null, San Francisco}|
## +------------------------------------------------------+---------------------------+
## notice that values outside of the schema were dropped and columns not matched are returned as null
```

**Example 2: Select Specific Columns:**

Copy code

```
## Define a schema with only the columns we want to use
partial_schema = StructType([
    StructField("name", StringType(), True),
    StructField("city", StringType(), True)
])

## Parse JSON column with partial schema
partial_df = df.withColumn("parsed_json", from_json(col("json_str"), partial_schema))

partial_df.show(truncate=False)

## +------------------------------------------------------+---------------------+
## |json_str                                              |parsed_json          |
## +------------------------------------------------------+---------------------+
## |{"name": "John", "age": 30, "city": "New York"}       |{John, New York}     |
## |{"name": "Jane", "age": "25", "city": "San Francisco"}|{Jane, San Francisco}|
## +------------------------------------------------------+---------------------+
## there is also an automatic filtering
```

### Recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). If you have a contract for support with Snowflake, reach out to your sales engineer and they can direct your support needs.
- Useful tools [PEP-8](https://peps.python.org/pep-0008/) and [Reindent](https://pypi.org/project/reindent/).

## SPRKPY1076

Message: Parameters in [pyspark.sql.readwriter.DataFrameReader](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.html) methods are not supported. This applies to CSV, JSON and PARQUET methods.

Category: Warning.

### Description

For the CSV, JSON and PARQUET methods on the [pyspark.sql.readwriter.DataFrameReader](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.html) object, the tool will analyze the parameters and add a transformation according to each case:

- All the parameters match their equivalent name in Snowpark: in this case, the tool will transform the parameter into a .option() call. For this case, the parameter won’t add this EWI.
- Some parameters do not match the equivalent in Snowpark: in this case, the tool will add this EWI with the parameter information and remove it from the method call.

**List of equivalences:**

- Equivalences for CSV:

| Spark keys | Snowpark Equivalences |
| --- | --- |
| sep | FIELD\_DELIMITER |
| header | PARSE\_HEADER |
| lineSep | RECORD\_DELIMITER |
| pathGlobFilter | PATTERN |
| quote | FIELD\_OPTIONALLY\_ENCLOSED\_BY |
| nullValue | NULL\_IF |
| dateFormat | DATE\_FORMAT |
| timestampFormat | TIMESTAMP\_FORMAT |
| inferSchema | INFER\_SCHEMA |
| delimiter | FIELD\_DELIMITER |

Expand

Show lessSee more

- Equivalences for JSON:

| Spark keys | Snowpark Equivalences |
| --- | --- |
| dateFormat | DATE\_FORMAT |
| timestampFormat | TIMESTAMP\_FORMAT |
| pathGlobFilter | PATTERN |

Expand

Show lessSee more

- Equivalences for PARQUET:

| Spark keys | Snowpark Equivalences |
| --- | --- |
| pathGlobFilter | PATTERN |

Expand

Show lessSee more

#### Scenarios

##### Scenario 1

**Input**

For CSV here are some examples:

Copy code

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('myapp').getOrCreate()

spark.read.csv("path3", None,None,None,None,None,None,True).show()
```

**Output**

In the converted code the parameters are added as individual options to the csv function

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.app_name('myapp', True).getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})

#EWI: SPRKPY1076 => Some of the included parameters are not supported in the csv function, the supported ones will be added into a option method.
spark.read.option("FIELD_DELIMITER", None).option("PARSE_HEADER", True).option("FIELD_OPTIONALLY_ENCLOSED_BY", None).csv("path3").show()
```

#### Scenario 2

**Input**

For JSON here are some example:

Copy code

```
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('myapp').getOrCreate()
spark.read.json("/myPath/jsonFile/", dateFormat='YYYY/MM/DD').show()
```

**Output**

In the converted code the parameters are added as individual options to the json function

Copy code

```
from snowflake.snowpark import Session
spark = Session.builder.app_name('myapp', True).getOrCreate()
#EWI: SPRKPY1076 => Some of the included parameters are not supported in the json function, the supported ones will be added into a option method.

spark.read.option("DATE_FORMAT", 'YYYY/MM/DD').json("/myPath/jsonFile/").show()
```

##### Scenario 3

**Input**

For PARQUET here are some examples:

Copy code

```
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('myapp').getOrCreate()

spark.read.parquet("/path/to/my/file.parquet", pathGlobFilter="*.parquet").show()
```

**Output**

In the converted code the parameters are added as individual options to the parquet function

Copy code

```
from snowflake.snowpark import Session

spark = Session.builder.app_name('myapp', True).getOrCreate()
spark.update_query_tag({"origin":"sf_sit","name":"sma","version":{"major":0,"minor":0,"patch":0},"attributes":{"language":"Python"}})

#EWI: SPRKPY1076 => Some of the included parameters are not supported in the parquet function, the supported ones will be added into a option method.
#EWI: SPRKPY1029 => The parquet function require adjustments, in Snowpark the parquet files needs to be located in an stage. See the documentation for more info.

spark.read.option("PATTERN", "*.parquet").parquet("/path/to/my/file.parquet")
```

#### Additional recommendations

- When non-equivalent parameters are present, it is recommended to check the behavior after the transformation.
- Also the documentation could be useful to find a better fit:

  - Options documentation for CSV:
    - [PySpark CSV Options](https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option).
    - [Snowpark CSV Options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-csv).
  - Options documentation for JSON:
    - [PySpark JSON Options](https://spark.apache.org/docs/latest/sql-data-sources-json.html).
    - [Snowpark JSON Options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-json).
  - Options documentation for PARQUET:
    - [Pyspark PARQUET options](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#data-source-option).
    - [SnowPark PARQUET options.](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#type-parquet).
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1077

Message: SQL embedded code cannot be processed.

Category: Warning.

### Description

This issue appears when the tool detects an SQL-embedded code that cannot be converted to Snowpark.

Check the SQL-embedded code section for more information.

#### Scenario

**Input**

In this example the SQL code is embedded on a variable called query that is used as parameter for the Pyspark.sql method.

Copy code

```
query = f"SELECT * from myTable"
spark.sql(query)
```

**Output**

SMA detects that the PySpark.sql parameter is a variable and not a SQL Code, so the EWI SPRKPY1077 message is added to the PySpark.sql line.

Copy code

```
query = f"SELECT * myTable"
#EWI: SPRKPY1077 => SQL embedded code cannot be processed.
spark.sql(query)
```

#### Additional recommendations

- For the transformation of SQL, this code must be directly inside as parameter of the method only as string values and without interpolation. Please check the SQL send to the PySpark.SQL function to validate it’s functionality on Snowflake.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1078

Message: The argument of the pyspark.context.SparkContext.setLogLevel function is not a literal value and therefore could not be evaluated

Category: Warning

### Description

This issue appears when the SMA detects the use of the [pyspark.context.SparkContext.setLogLevel](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.setLogLevel.html) function with an argument that is not a literal value, for example, when the argument is a variable.

The SMA does a static analysis of your source code and therefore it is not possible to evaluate the content of that argument and determine an equivalent in Snowpark.

#### Scenario

**Input**

In this example the logLevel is defined in the variable my\_log\_level, then my\_log\_level used as parameter by the setLogLevel method.

Copy code

```
my_log_level = "WARN"
sparkSession.sparkContext.setLogLevel(my_log_level)
```

**Output**

SMA is unable to evaluate the argument for the log level parameter, so the EWI SPRKPY1078 is added over the line of the transformed logging:

Copy code

```
my_log_level = "WARN"
#EWI: SPRKPY1078 => my_log_level is not a literal value and therefore could not be evaluated. Make sure the value of my_log_level is a valid level in Snowpark. Valid log levels are: logging.CRITICAL, logging.DEBUG, logging.ERROR, logging.INFO, logging.NOTSET, logging.WARNING
logging.basicConfig(stream = sys.stdout, level = my_log_level)
```

**Recommended fix**

Even though the SMA was unable to evaluate the argument, it will transform the `pyspark.context.SparkContext.setLogLevel` function into the Snowpark equivalent. Please make sure the value of the `level` argument in the generated output code is a valid and equivalent log level in Snowpark according to the table below:

| PySpark log level | Snowpark log level equivalent |
| --- | --- |
| ALL | logging.NOTSET |
| DEBUG | logging.DEBUG |
| ERROR | logging.ERROR |
| FATAL | logging.CRITICAL |
| INFO | logging.INFO |
| OFF | logging.WARNING |
| TRACE | logging.NOTSET |
| WARN | logging.WARNING |

Expand

Show lessSee more

Thus the recommended fix will looks like:

Copy code

```
my_log_level = logging.WARNING
logging.basicConfig(stream = sys.stdout, level = my_log_level)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1079

Message: The argument of the pyspark.context.SparkContext.setLogLevel function is not a valid PySpark log level

Category: Warning

### Description

This issue appears when the SMA detects the use of the [pyspark.context.SparkContext.setLogLevel](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.setLogLevel.html) function with an argument that is not a valid log level in PySpark, and therefore an equivalent could not be determined in Snowpark.

#### Scenario

**Input**

here the log level uses “INVALID\_LOG\_LEVEL” that is not a valid Pyspark log level.

Copy code

```
sparkSession.sparkContext.setLogLevel("INVALID_LOG_LEVEL")
```

**Output**

SMA can’t recognize the log level “INVALID\_LOG\_LEVEL”, even though SMA makes the conversion the EWI SPRKPY1079 is added to indicate a possible problem.

Copy code

```
#EWI: SPRKPY1079 => INVALID_LOG_LEVEL is not a valid PySpark log level, therefore an equivalent could not be determined in Snowpark. Valid PySpark log levels are: ALL, DEBUG, ERROR, FATAL, INFO, OFF, TRACE, WARN
logging.basicConfig(stream = sys.stdout, level = logging.INVALID_LOG_LEVEL)
```

**Recommended fix**

Make sure that the log level used in the pyspark.context.SparkContext.setLogLevel function is a valid log level in [PySpark](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.setLogLevel.html) or in [Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/python/troubleshooting) and try again.

Copy code

```
logging.basicConfig(stream = sys.stdout, level = logging.DEBUG)
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1081

This issue code has been **deprecated** since [Spark Conversion Core 4.12.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.readwriter.DataFrameWriter.partitionBy has a workaround.

Category: Warning

### Description

The [Pyspark.sql.readwriter.DataFrameWriter.partitionBy](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.partitionBy.html) function is not supported. The workaround is to use [Snowpark’s copy\_into\_location](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.copy_into_location) instead. See the documentation for more info.

#### Scenario

**Input**

This code will create a separate directories for each unique value in the `FIRST_NAME` column. The data is the same, but it’s going to be stored in different directories based on the column.

Copy code

```
df = session.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]], schema = ["FIRST_NAME", "LAST_NAME"])
df.write.partitionBy("FIRST_NAME").csv("/home/data")
```

This code will create a separate directories for each unique value in the `FIRST_NAME` column. The data is the same, but it’s going to be stored in different directories based on the column.

**Output code**

Copy code

```
df = session.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]], schema = ["FIRST_NAME", "LAST_NAME"])
#EWI: SPRKPY1081 => The partitionBy function is not supported, but you can instead use copy_into_location as workaround. See the documentation for more info.
df.write.partitionBy("FIRST_NAME").csv("/home/data", format_type_options = dict(compression = "None"))
```

**Recommended fix**

In Snowpark, [copy\_into\_location](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.copy_into_location) has a partition\_by parameter that you can use instead of the partitionBy function, but it’s going to require some manual adjustments, as shown in the following example:

**Spark code:**

Copy code

```
df = session.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]], schema = ["FIRST_NAME", "LAST_NAME"])
df.write.partitionBy("FIRST_NAME").csv("/home/data")
```

**Snowpark code manually adjusted:**

Copy code

```
df = session.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]], schema = ["FIRST_NAME", "LAST_NAME"])
df.write.copy_into_location(location=temp_stage, partition_by=col("FIRST_NAME"), file_format_type="csv", format_type_options={"COMPRESSION": "NONE"}, header=True)
```

**copy\_into\_location** has the following parameters

- *location*: The Snowpark location only accepts cloud locations using an [snowflake stage](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).
- *partition\_by*: It can be a Column name or a SQL expression, so you will need to converted to a column or a SQL, using col or sql\_expr.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1082

Message: The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.

Category: Warning

### Description

The [pyspark.sql.readwriter.DataFrameReader.load](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.load.html) function is not supported. The workaround is to use Snowpark DataFrameReader methods instead.

#### Scenarios

The spark signature for this method `DataFrameReader.load(path, format, schema, **options)` does not exist in Snowpark. Therefore, any usage of the load function is going to have an EWI in the output code.

##### Scenario 1

**Input**

Below is an example that tries to load data from a `CSV` source.

Copy code

```
path_csv_file = "/path/to/file.csv"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.load(path_csv_file, "csv").show()
my_session.read.load(path_csv_file, "csv", schema=schemaParam).show()
my_session.read.load(path_csv_file, "csv", schema=schemaParam, lineSep="\r\n", dateFormat="YYYY/MM/DD").show()
```

**Output**

The SMA adds the EWI `SPRKPY1082` to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_csv_file = "/path/to/file.csv"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.

my_session.read.load(path_csv_file, "csv").show()
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_csv_file, "csv", schema=schemaParam).show()
#EWI: The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_csv_file, "csv", schema=schemaParam, lineSep="\r\n", dateFormat="YYYY/MM/DD").show()
```

**Recommended fix**

As a workaround, you can use [Snowpark DataFrameReader](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with `csv` method.
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and puts the file into it, then calls the `CSV` method.

Copy code

```
path_csv_file = "/path/to/file.csv"

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.csv", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.csv"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.csv(stage_file_path).show()
```

- Fixing `schema` parameter:
  - The schema can be set by using the [schema](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.schema) function as follows:

Copy code

```
schemaParam = StructType([
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])

df = my_session.read.schema(schemaParam).csv(temp_stage)
```

- Fixing `options` parameter:

The [options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.options) between spark and snowpark are not the same, in this case `lineSep` and `dateFormat` are replaced with `RECORD_DELIMITER` and `DATE_FORMAT`, the **Additional recommendations** section has a table with all the Equivalences.

Below is an example that creates a dictionary with `RECORD_DELIMITER` and `DATE_FORMAT`, and calls the `options` method with that dictionary.

Copy code

```
optionsParam = {"RECORD_DELIMITER": "\r\n", "DATE_FORMAT": "YYYY/MM/DD"}
df = my_session.read.options(optionsParam).csv(stage)
```

### Scenario 2

**Input**

Below is an example that tries to load data from a `JSON` source.

Copy code

```
path_json_file = "/path/to/file.json"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.load(path_json_file, "json").show()
my_session.read.load(path_json_file, "json", schema=schemaParam).show()
my_session.read.load(path_json_file, "json", schema=schemaParam, dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3").show()
```

**Output**

The SMA adds the EWI `SPRKPY1082` to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_json_file = "/path/to/file.json"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.

my_session.read.load(path_json_file, "json").show()
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_json_file, "json", schema=schemaParam).show()
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_json_file, "json", schema=schemaParam, dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3").show()
```

**Recommended fix**

As a workaround, you can use [Snowpark DataFrameReader](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with `json` method
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and puts the file into it, then calls the `JSON` method.

Copy code

```
path_json_file = "/path/to/file.json"

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.json", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.json"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.json(stage_file_path).show()
```

- Fixing `schema` parameter:
  - The schema can be set by using the [schema](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.schema) function as follows:

Copy code

```
schemaParam = StructType([
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])

df = my_session.read.schema(schemaParam).json(temp_stage)
```

- Fixing `options` parameter:

The [options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.options) between Spark and snowpark are not the same, in this case `dateFormat` and `timestampFormat` are replaced with `DATE_FORMAT` and `TIMESTAMP_FORMAT`, the **Additional recommendations** section has a table with all the Equivalences.

Below is an example that creates a dictionary with `DATE_FORMAT` and `TIMESTAMP_FORMAT`, and calls the `options` method with that dictionary.

Copy code

```
optionsParam = {"DATE_FORMAT": "YYYY/MM/DD", "TIMESTAMP_FORMAT": "YYYY-MM-DD HH24:MI:SS.FF3"}
df = Session.read.options(optionsParam).json(stage)
```

### Scenario 3

**Input**

Below is an example that tries to load data from a `PARQUET` source.

Copy code

```
path_parquet_file = "/path/to/file.parquet"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.load(path_parquet_file, "parquet").show()
my_session.read.load(path_parquet_file, "parquet", schema=schemaParam).show()
my_session.read.load(path_parquet_file, "parquet", schema=schemaParam, pathGlobFilter="*.parquet").show()
```

**Output**

The SMA adds the EWI `SPRKPY1082` to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_parquet_file = "/path/to/file.parquet"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.

my_session.read.load(path_parquet_file, "parquet").show()
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_parquet_file, "parquet", schema=schemaParam).show()
#EWI: SPRKPY1082 => The pyspark.sql.readwriter.DataFrameReader.load function is not supported. A workaround is to use Snowpark DataFrameReader format specific method instead (avro csv, json, orc, parquet). The path parameter should be a stage location.
my_session.read.load(path_parquet_file, "parquet", schema=schemaParam, pathGlobFilter="*.parquet").show()
```

**Recommended fix**

As a workaround, you can use [Snowpark DataFrameReader](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with `parquet` method
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and puts the file into it, then calls the `PARQUET` method.

Copy code

```
path_parquet_file = "/path/to/file.parquet"

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.parquet", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.parquet"

schemaParam = StructType([
        StructField("Name", StringType(), True),
        StructField("Superhero", StringType(), True)
    ])

my_session.read.parquet(stage_file_path).show()
```

- Fixing `schema` parameter:
  - The schema can be set by using the [schema](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.schema) function as follows:

Copy code

```
schemaParam = StructType([
        StructField("name", StringType(), True),
        StructField("city", StringType(), True)
    ])

df = my_session.read.schema(schemaParam).parquet(temp_stage)
```

- Fixing `options` parameter:

The [options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader.options) between Spark and snowpark are not the same, in this case `pathGlobFilter` is replaced with `PATTERN`, the **Additional recommendations** section has a table with all the Equivalences.

Below is an example that creates a dictionary with `PATTERN`, and calls the `options` method with that dictionary.

Copy code

```
optionsParam = {"PATTERN": "*.parquet"}
df = Session.read.options(optionsParam).parquet(stage)
```

### Additional recommendations

- Take into account that the options between spark and snowpark are not the same, but they can be mapped:

| Spark Options | Possible value | Snowpark equivalent | Description |
| --- | --- | --- | --- |
| header | True or False | SKIP\_HEADER = 1 / SKIP\_HEADER = 0 | To use the first line of a file as names of columns. |
| delimiter | Any single/multi character field separator | FIELD\_DELIMITER | To specify single / multiple character(s) as a separator for each column/field. |
| sep | Any single character field separator | FIELD\_DELIMITER | To specify a single character as a separator for each column/field. |
| encoding | UTF-8, UTF-16, etc… | ENCODING | To decode the CSV files by the given encoding type. Default encoding is UTF-8 |
| lineSep | Any single character line separator | RECORD\_DELIMITER | To define the line separator that should be used for file parsing. |
| pathGlobFilter | File pattern | PATTERN | To define a pattern to read files only with filenames matching the pattern. |
| recursiveFileLookup | True or False | N/A | To recursively scan a directory to read files. Default value of this option is False. |
| quote | Single character to be quoted | FIELD\_OPTIONALLY\_ENCLOSED\_BY | To quote fields/columns containing fields where the delimiter / separator can be part of the value. This character To quote all fields when used with quoteAll option. Default value of this option is double quote(“). |
| nullValue | String to replace null | NULL\_IF | To replace null values with the string while reading and writing dataframe. |
| dateFormat | Valid date format | DATE\_FORMAT | To define a string that indicates a date format. Default format is yyyy-MM-dd. |
| timestampFormat | Valid timestamp format | TIMESTAMP\_FORMAT | To define a string that indicates a timestamp format. Default format is yyyy-MM-dd ‘T’HH:mm:ss. |
| escape | Any single character | ESCAPE | To set a single character as escaping character to override default escape character(). |
| inferSchema | True or False | INFER\_SCHEMA | Automatically detects the file schema |
| mergeSchema | True or False | N/A | Not needed in snowflake as this happens whenever the infer\_schema determines the parquet file structure |

Expand

Show lessSee more

- For **modifiedBefore / modifiedAfter** option you can achieve the same result in Snowflake by using the metadata columns and then adding a filter like: `df.filter(METADATA_FILE_LAST_MODIFIED > ‘some_date’)`.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1083

Message: The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy\_into\_location method instead.

Category: Warning

### Description

The [pyspark.sql.readwriter.DataFrameWriter.save](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.save.html) function is not supported. The workaround is to use Snowpark DataFrameWriter methods instead.

#### Scenarios

The spark signature for this method `DataFrameWriter.save(path, format, mode, partitionBy, **options)` does not exists in Snowpark. Therefore, any usage of the load function it’s going to have an EWI in the output code.

##### Scenario 1

**Input code**

Below is an example that tries to save data with `CSV` format.

Copy code

```
path_csv_file = "/path/to/file.csv"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = my_session.createDataFrame(data, schema=["Name", "Age", "City"])

df.write.save(path_csv_file, format="csv")
df.write.save(path_csv_file, format="csv", mode="overwrite")
df.write.save(path_csv_file, format="csv", mode="overwrite", lineSep="\r\n", dateFormat="YYYY/MM/DD")
df.write.save(path_csv_file, format="csv", mode="overwrite", partitionBy="City", lineSep="\r\n", dateFormat="YYYY/MM/DD")
```

**Output code**

The tool adds this EWI `SPRKPY1083` on the output code to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_csv_file = "/path/to/file.csv"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = my_session.createDataFrame(data, schema=["Name", "Age", "City"])

#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_csv_file, format="csv")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_csv_file, format="csv", mode="overwrite")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_csv_file, format="csv", mode="overwrite", lineSep="\r\n", dateFormat="YYYY/MM/DD")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_csv_file, format="csv", mode="overwrite", partitionBy="City", lineSep="\r\n", dateFormat="YYYY/MM/DD")
```

**Recommended fix**

As a workaround you can use [Snowpark DataFrameWriter](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with [csv](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) or [copy\_into\_location](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.copy_into_location) method.
  - If you are using `copy_into_location` method, you need to specify the format with the `file_format_type parameter`.
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and put the file into it, then calls one the methods mentioned above.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.csv", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.csv"

## Using csv method
df.write.csv(stage_file_path)

## Using copy_into_location method
df.write.copy_into_location(stage_file_path, file_format_type="csv")
```

- Fixing `mode` parameter:
  - Use the [mode](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.mode) function from [Snowpark DataFrameWriter](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter), as follows:

Below is an example that adds into the daisy chain the `mode` method with `overwrite` as a parameter.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using csv method
df.write.mode("overwrite").csv(temp_stage)

## Using copy_into_location method
df.write.mode("overwrite").copy_into_location(temp_stage, file_format_type="csv")
```

- Fixing `partitionBy` parameter:
  - Use the [partition\_by](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

Below is an example that used the `partition_by` parameter from the `CSV` method.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using csv method
df.write.csv(temp_stage, partition_by="City")

## Using copy_into_location method
df.write.copy_into_location(temp_stage, file_format_type="csv", partition_by="City")
```

- Fixing `options` parameter:
  - Use the [format\_type\_options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

The options between spark and snowpark are not the same, in this case `lineSep` and `dateFormat` are replaced with `RECORD_DELIMITER` and `DATE_FORMAT`, the **Additional recommendations** section has table with all the Equivalences.

Below is an example that creates a dictionary with `RECORD_DELIMITER` and `DATE_FORMAT`, and calls the `options` method with that dictionary.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
optionsParam = {"RECORD_DELIMITER": "\r\n", "DATE_FORMAT": "YYYY/MM/DD"}

## Using csv method
df.write.csv(stage, format_type_options=optionsParam)

## Using copy_into_location method
df.write.csv(stage, file_format_type="csv", format_type_options=optionsParam)
```

### Scenario 2

**Input code**

Below is an example that tries to save data with `JSON` format.

Copy code

```
path_json_file = "/path/to/file.json"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

df.write.save(path_json_file, format="json")
df.write.save(path_json_file, format="json", mode="overwrite")
df.write.save(path_json_file, format="json", mode="overwrite", dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3")
df.write.save(path_json_file, format="json", mode="overwrite", partitionBy="City", dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3")
```

**Output code**

The tool adds this EWI `SPRKPY1083` on the output code to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_json_file = "/path/to/file.json"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_json_file, format="json")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_json_file, format="json", mode="overwrite")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_json_file, format="json", mode="overwrite", dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_json_file, format="json", mode="overwrite", partitionBy="City", dateFormat="YYYY/MM/DD", timestampFormat="YYYY-MM-DD HH24:MI:SS.FF3")
```

**Recommended fix**

As a workaround you can use [Snowpark DataFrameReader](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with [json](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.json) or [copy\_into\_location](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.copy_into_location) method
  - If you are using `copy_into_location` method, you need to specify the format with the `file_format_type parameter`.
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and put the file into it, then calls one the methods mentioned above.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.json", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.json"

## Using json method
df.write.json(stage_file_path)

## Using copy_into_location method
df.write.copy_into_location(stage_file_path, file_format_type="json")
```

- Fixing `mode` parameter:
  - Use the [mode](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.mode) function from [Snowpark DataFrameWriter](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter), as follows:

Below is an example that adds into the daisy chain the `mode` method with `overwrite` as a parameter.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using json method
df.write.mode("overwrite").json(temp_stage)

## Using copy_into_location method
df.write.mode("overwrite").copy_into_location(temp_stage, file_format_type="json")
```

- Fixing `partitionBy` parameter:
  - Use the [partition\_by](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

Below is an example that used the `partition_by` parameter from the `CSV` method.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using json method
df.write.json(temp_stage, partition_by="City")

## Using copy_into_location method
df.write.copy_into_location(temp_stage, file_format_type="json", partition_by="City")
```

- Fixing `options` parameter:
  - Use the [format\_type\_options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

The options between spark and snowpark are not the same, in this case `dateFormat` and `timestampFormat` are replaced with `DATE_FORMAT` and `TIMESTAMP_FORMAT`, the **Additional recommendations** section has table with all the Equivalences.

Below is an example that creates a dictionary with `DATE_FORMAT` and `TIMESTAMP_FORMAT`, and calls the `options` method with that dictionary.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
optionsParam = {"DATE_FORMAT": "YYYY/MM/DD", "TIMESTAMP_FORMAT": "YYYY-MM-DD HH24:MI:SS.FF3"}

## Using json method
df.write.json(stage, format_type_options=optionsParam)

## Using copy_into_location method
df.write.copy_into_location(stage, file_format_type="json", format_type_options=optionsParam)
```

### Scenario 3

**Input code**

Below is an example that tries to save data with `PARQUET` format.

Copy code

```
path_parquet_file = "/path/to/file.parquet"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

df.write.save(path_parquet_file, format="parquet")
df.write.save(path_parquet_file, format="parquet", mode="overwrite")
df.write.save(path_parquet_file, format="parquet", mode="overwrite", pathGlobFilter="*.parquet")
df.write.save(path_parquet_file, format="parquet", mode="overwrite", partitionBy="City", pathGlobFilter="*.parquet")
```

**Output code**

The tool adds this EWI `SPRKPY1083` on the output code to let you know that this function is not supported by Snowpark, but it has a workaround.

Copy code

```
path_parquet_file = "/path/to/file.parquet"

data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_parquet_file, format="parquet")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_parquet_file, format="parquet", mode="overwrite")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_parquet_file, format="parquet", mode="overwrite", pathGlobFilter="*.parquet")
#EWI: SPRKPY1083 => The pyspark.sql.readwriter.DataFrameWriter.save function is not supported. A workaround is to use Snowpark DataFrameWriter copy_into_location method instead.
df.write.save(path_parquet_file, format="parquet", mode="overwrite", partitionBy="City", pathGlobFilter="*.parquet")
```

**Recommended fix**

As a workaround you can use [Snowpark DataFrameReader](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameReader) methods instead.

- Fixing `path` and `format` parameters:
  - Replace the `load` method with [parquet](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.parquet) or [copy\_into\_location](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/1.23.0/snowpark/api/snowflake.snowpark.DataFrameWriter.copy_into_location) method.
  - If you are using `copy_into_location` method, you need to specify the format with the `file_format_type parameter`.
  - The first parameter `path` must be in a stage to make an equivalence with [Snowpark](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage).

Below is an example that creates a temporal stage and put the file into it, then calls one the methods mentioned above.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Stage creation

temp_stage = f'{Session.get_fully_qualified_current_schema()}.{_generate_prefix("TEMP_STAGE")}'
my_session.sql(f'CREATE TEMPORARY STAGE IF NOT EXISTS {temp_stage}').show()
my_session.file.put(f"file:///path/to/file.parquet", f"@{temp_stage}")
stage_file_path = f"{temp_stage}file.parquet"

## Using parquet method
df.write.parquet(stage_file_path)

## Using copy_into_location method
df.write.copy_into_location(stage, file_format_type="parquet")
```

- Fixing `mode` parameter:
  - Use the [mode](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.mode) function from [Snowpark DataFrameWriter](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter), as follows:

Below is an example that adds into the daisy chain the `mode` method with `overwrite` as a parameter.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using parquet method
df.write.mode("overwrite").parquet(temp_stage)

## Using copy_into_location method
df.write.mode("overwrite").copy_into_location(stage, file_format_type="parquet")
```

- Fixing `partitionBy` parameter:
  - Use the [partition\_by](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

Below is an example that used the `partition_by` parameter from the `parquet` method.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

## Using parquet method
df.write.parquet(temp_stage, partition_by="City")

## Using copy_into_location method
df.write.copy_into_location(stage, file_format_type="parquet", partition_by="City")
```

- Fixing `options` parameter:
  - Use the [format\_type\_options](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.csv) parameter from the `CSV` method, as follows:

The options between spark and snowpark are not the same, in this case `pathGlobFilter` is replaced with `PATTERN`, the **Additional recommendations** section has table with all the Equivalences.

Below is an example that creates a dictionary with `PATTERN`, and calls the `options` method with that dictionary.

Copy code

```
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]
df = spark.createDataFrame(data, schema=["Name", "Age", "City"])
optionsParam = {"PATTERN": "*.parquet"}

## Using parquet method
df.write.parquet(stage, format_type_options=optionsParam)

## Using copy_into_location method
df.write.copy_into_location(stage, file_format_type="parquet", format_type_options=optionsParam)
```

### Additional recommendations

- Take into account the options between spark and snowpark are not the same, but they can be mapped:

| Spark Options | Possible value | Snowpark equivalent | Description |
| --- | --- | --- | --- |
| header | True or False | SKIP\_HEADER = 1 / SKIP\_HEADER = 0 | To use the first line of a file as names of columns. |
| delimiter | Any single/multi character field separator | FIELD\_DELIMITER | To specify single / multiple character(s) as a separator for each column/field. |
| sep | Any single character field separator | FIELD\_DELIMITER | To specify a single character as a separator for each column/field. |
| encoding | UTF-8, UTF-16, etc… | ENCODING | To decode the CSV files by the given encoding type. Default encoding is UTF-8 |
| lineSep | Any single character line separator | RECORD\_DELIMITER | To define the line separator that should be used for file parsing. |
| pathGlobFilter | File pattern | PATTERN | To define a pattern to read files only with filenames matching the pattern. |
| recursiveFileLookup | True or False | N/A | To recursively scan a directory to read files. Default value of this option is False. |
| quote | Single character to be quoted | FIELD\_OPTIONALLY\_ENCLOSED\_BY | To quote fields/columns containing fields where the delimiter / separator can be part of the value. This character To quote all fields when used with quoteAll option. Default value of this option is double quote(“). |
| nullValue | String to replace null | NULL\_IF | To replace null values with the string while reading and writing dataframe. |
| dateFormat | Valid date format | DATE\_FORMAT | To define a string that indicates a date format. Default format is yyyy-MM-dd. |
| timestampFormat | Valid timestamp format | TIMESTAMP\_FORMAT | To define a string that indicates a timestamp format. Default format is yyyy-MM-dd ‘T’HH:mm:ss. |
| escape | Any single character | ESCAPE | To set a single character as escaping character to override default escape character(). |
| inferSchema | True or False | INFER\_SCHEMA | Automatically detects the file schema |
| mergeSchema | True or False | N/A | Not needed in snowflake as this happens whenever the infer\_schema determines the parquet file structure |

Expand

Show lessSee more

- For **modifiedBefore / modifiedAfter** option you can achieve the same result in Snowflake by using the metadata columns and then add a filter like: `df.filter(METADATA_FILE_LAST_MODIFIED > ‘some_date’)`.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1084

This issue code has been **deprecated** since [Spark Conversion Core 4.12.0](/migrations/sma-docs/general/release-notes/README)

Message: pyspark.sql.readwriter.DataFrameWriter.option is not supported.

Category: Warning

### Description

The [pyspark.sql.readwriter.DataFrameWriter.option](https://spark.apache.org/docs/3.5.3/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.option.html) function is not supported.

#### Scenario

**Input code**

Below is an example using the `option` method, this method is used to add additional configurations when writing the data of a DataFrame.

Copy code

```
path_csv_file = "/path/to/file.csv"
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

df.write.option("header", True).csv(csv_file_path)
df.write.option("sep", ";").option("lineSep","-").csv(csv_file_path)
```

**Output code**

The tool adds this EWI `SPRKPY1084` on the output code to let you know that this function is not supported by Snowpark.

Copy code

```
path_csv_file = "/path/to/file.csv"
data = [
        ("John", 30, "New York"),
        ("Jane", 25, "San Francisco")
    ]

df = spark.createDataFrame(data, schema=["Name", "Age", "City"])

#EWI: SPRKPY1084 => The pyspark.sql.readwriter.DataFrameWriter.option function is not supported.

df.write.option("header", True).csv(csv_file_path)
#EWI: SPRKPY1084 => The pyspark.sql.readwriter.DataFrameWriter.option function is not supported.
df.write.option("sep", ";").option("lineSep","-").csv(csv_file_path)
```

**Recommended fix**

The pyspark.sql.readwriter.DataFrameWriter.option method does not have a recommended fix.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1085

Message: pyspark.ml.feature.VectorAssembler is not supported.

Category: Warning

### Description

The [pyspark.ml.feature.VectorAssembler](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.VectorAssembler.html) is not supported.

#### Scenario

**Input code**

VectorAssembler is used to combine several columns into a single vector.

Copy code

```
data = [
        (1, 10.0, 20.0),
        (2, 25.0, 30.0),
        (3, 50.0, 60.0)
    ]

df = SparkSession.createDataFrame(data, schema=["Id", "col1", "col2"])
vector = VectorAssembler(inputCols=["col1", "col2"], output="cols")
```

**Output code**

The tool adds this EWI `SPRKPY1085` on the output code to let you know that this class is not supported by Snowpark.

Copy code

```
data = [
        (1, 10.0, 20.0),
        (2, 25.0, 30.0),
        (3, 50.0, 60.0)
    ]

df = spark.createDataFrame(data, schema=["Id", "col1", "col2"])
#EWI: SPRKPY1085 => The pyspark.ml.feature.VectorAssembler function is not supported.

vector = VectorAssembler(inputCols=["col1", "col2"], output="cols")
```

**Recommended fix**

The pyspark.ml.feature.VectorAssembler does not have a recommended fix.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1086

Message: pyspark.ml.linalg.VectorUDT is not supported.

Category: Warning

### Description

The [pyspark.ml.linalg.VectorUDT](https://spark.apache.org/docs/latest/api/python/_modules/pyspark/ml/linalg.html) is not supported.

#### Scenario

**Input code**

VectorUDT is a data type to represent vector columns in a DataFrame.

Copy code

```
data = [
        (1, Vectors.dense([10.0, 20.0])),
        (2, Vectors.dense([25.0, 30.0])),
        (3, Vectors.dense([50.0, 60.0]))
    ]

schema = StructType([
        StructField("Id", IntegerType(), True),
        StructField("VectorCol", VectorUDT(), True),
    ])

df = SparkSession.createDataFrame(data, schema=schema)
```

**Output code**

The tool adds this EWI `SPRKPY1086` on the output code to let you know that this function is not supported by Snowpark.

Copy code

```
data = [
        (1, Vectors.dense([10.0, 20.0])),
        (2, Vectors.dense([25.0, 30.0])),
        (3, Vectors.dense([50.0, 60.0]))
    ]

#EWI: SPRKPY1086 => The pyspark.ml.linalg.VectorUDT function is not supported.
schema = StructType([
        StructField("Id", IntegerType(), True),
        StructField("VectorCol", VectorUDT(), True),
    ])

df = spark.createDataFrame(data, schema=schema)
```

**Recommended fix**

The pyspark.ml.linalg.VectorUDT does not have a recommended fix.

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1087

Message: The pyspark.sql.dataframe.DataFrame.writeTo function is not supported, but it has a workaround.

Category: Warning.

### Description

The [pyspark.sql.dataframe.DataFrame.writeTo](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.writeTo.html) function is not supported. The workaround is to use Snowpark DataFrameWriter [SaveAsTable](https://docs.snowflake.com/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.DataFrameWriter.saveAsTable) method instead.

#### Scenario

**Input**

Below is an example of a use of the `pyspark.sql.dataframe.DataFrame.writeTo` function, the dataframe `df` is written into a table name `Personal_info`.

Copy code

```
df = spark.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]],
                                 schema=["FIRST_NAME", "LAST_NAME"])

df.writeTo("Personal_info")
```

**Output**

The SMA adds the EWI `SPRKPY1087` to the output code to let you know that this function is not supported, but has a workaround.

Copy code

```
df = spark.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]],
                                 schema=["FIRST_NAME", "LAST_NAME"])

#EWI: SPRKPY1087 => pyspark.sql.dataframe.DataFrame.writeTo is not supported, but it has a workaround.
df.writeTo("Personal_info")
```

**Recommended fix**

The workaround is to use Snowpark DataFrameWriter SaveAsTable method instead.

Copy code

```
df = spark.createDataFrame([["John", "Berry"], ["Rick", "Berry"], ["Anthony", "Davis"]],
                                 schema=["FIRST_NAME", "LAST_NAME"])

df.write.saveAsTable("Personal_info")
```

#### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1088

Message: The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.

Category: Warning

### Description

The [pyspark.sql.readwriter.DataFrameWriter.option](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.option.html) values in Snowpark may be different, so validation might be needed to ensure that the behavior is correct.

#### Scenarios

There are some scenarios depending on the option it is supported or not, or the format used to write the file.

##### Scenario 1

**Input**

Below is an example of the usage of the method option, adding a `sep` option, which is currently `supported`.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])

df.write.option("sep", ",").csv("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1088` indicating that it is required validation.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.option("sep", ",").csv("some_path")
```

**Recommended fix**

The Snowpark API supports this parameter, so the only action can be to check the behavior after the migration. Please refer to the **Equivalences table** to see the supported parameters.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.option("sep", ",").csv("some_path")
```

##### Scenario 2

**Input**

Here the scenario shows the usage of option, but adds a `header` option, which is `not supported`.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])

df.write.option("header", True).csv("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1088` indicating that it is required validation is needed.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.option("header", True).csv("some_path")
```

**Recommended fix**

For this scenario it is recommended to evaluate the Snowpark [format type options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to see if it is possible to change it according to your needs. Also, check the behavior after the change.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.csv("some_path")
```

##### Scenario 3

**Input**

This scenario adds a `sep` option, which is `supported` and uses the `JSON` method.

- Note: this scenario also applies for `PARQUET`.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])

df.write.option("sep", ",").json("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1088` indicating that it is required validation is needed.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.option("sep", ",").json("some_path")
```

**Recommended fix**

The file format `JSON` does not support the parameter `sep`, so it is recommended to evaluate the snowpark [format type options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to see if it is possible to change it according to your needs. Also, check the behavior after the change.

Copy code

```
df = spark.createDataFrame([(100, "myVal")], ["ID", "Value"])
#EWI: SPRKPY1088 => The pyspark.sql.readwriter.DataFrameWriter.option values in Snowpark may be different, so required validation might be needed.
df.write.json("some_path")
```

#### Additional recommendations

- Since there are some `not supported` parameters, it is recommended to check the `table of equivalences` and check the behavior after the transformation.
- **Equivalences table:**

| PySpark Option | SnowFlake Option | Supported File Formats | Description |
| --- | --- | --- | --- |
| SEP | FIELD\_DELIMITER | CSV | One or more single byte or multibyte characters that separate fields in an input file. |
| LINESEP | RECORD\_DELIMITER | CSV | One or more characters that separate records in an input file. |
| QUOTE | FIELD\_OPTIONALLY\_ENCLOSED\_BY | CSV | Character used to enclose strings. |
| NULLVALUE | NULL\_IF | CSV | String used to convert to and from SQL NULL. |
| DATEFORMAT | DATE\_FORMAT | CSV | String that defines the format of date values in the data files to be loaded. |
| TIMESTAMPFORMAT | TIMESTAMP\_FORMAT | CSV | String that defines the format of timestamp values in the data files to be loaded. |

Expand

Show lessSee more

If the parameter used is not in the list, the API throws an error.

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1089

Message: The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.

Category: Warning

### Description

The [pyspark.sql.readwriter.DataFrameWriter.options](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.options.html) values in Snowpark may be different, so validation might be needed to ensure that the behavior is correct.

#### Scenarios

There are some scenarios, depending on whether the options are supported or not, or the format used to write the file.

##### Scenario 1

**Input**

Below is an example of the usage of the method options, adding the options `sep` and `nullValue`, which are currently `supported`.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])

df.write.options(nullValue="myVal", sep=",").csv("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1089` indicating that it is required validation.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.options(nullValue="myVal", sep=",").csv("some_path")
```

**Recommended fix**

The Snowpark API supports these parameters, so the only action can be to check the behavior after the migration. Please refer to the **Equivalences table** to see the supported parameters.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.options(nullValue="myVal", sep=",").csv("some_path")
```

##### Scenario 2

**Input**

Here the scenario shows the usage of options, but adds a `header` option, which is `not supported`.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])

df.write.options(header=True, sep=",").csv("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1089` indicating that it is required validation is needed.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.options(header=True, sep=",").csv("some_path")
```

**Recommended fix**

For this scenario it is recommended to evaluate the Snowpark [format type options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to see if it is possible to change it according to your needs. Also, check the behavior after the change.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.csv("some_path")
```

##### Scenario 3

**Input**

This scenario adds a `sep` option, which is `supported` and uses the `JSON` method.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])

df.write.options(nullValue="myVal", sep=",").json("some_path")
```

**Output**

The tool adds the EWI `SPRKPY1089` indicating that it is required validation is needed.

- Note: this scenario also applies for `PARQUET`.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.options(nullValue="myVal", sep=",").json("some_path")
```

**Recommended fix**

The file format `JSON` does not support the parameter `sep`, so it is recommended to evaluate the snowpark [format type options](https://docs.snowflake.com/en/sql-reference/sql/create-file-format#format-type-options-formattypeoptions) to see if it is possible to change it according to your needs. Also, check the behavior after the change.

Copy code

```
df = spark.createDataFrame([(1, "myVal")], [2, "myVal2"], [None, "myVal3" ])
#EWI: SPRKPY1089 => The pyspark.sql.readwriter.DataFrameWriter.options values in Snowpark may be different, so required validation might be needed.
df.write.json("some_path")
```

#### Additional recommendations

- Since there are some `not supported` parameters, it is recommended to check the `table of equivalences` and check the behavior after the transformation.
- **Equivalences table:**

Snowpark can support a list of **equivalences** for some parameters:

| PySpark Option | SnowFlake Option | Supported File Formats | Description |
| --- | --- | --- | --- |
| SEP | FIELD\_DELIMITER | CSV | One or more single byte or multibyte characters that separate fields in an input file. |
| LINESEP | RECORD\_DELIMITER | CSV | One or more characters that separate records in an input file. |
| QUOTE | FIELD\_OPTIONALLY\_ENCLOSED\_BY | CSV | Character used to enclose strings. |
| NULLVALUE | NULL\_IF | CSV | String used to convert to and from SQL NULL. |
| DATEFORMAT | DATE\_FORMAT | CSV | String that defines the format of date values in the data files to be loaded. |
| TIMESTAMPFORMAT | TIMESTAMP\_FORMAT | CSV | String that defines the format of timestamp values in the data files to be loaded. |

Expand

Show lessSee more

If the parameter used is not in the list, the API throws an error.

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKPY1101

### Category

Parsing error.

#### Description

When the tool recognizes a parsing error, it tries to recover from it and continues the process in the next line. In those cases, it shows the error and comments on the line.

This example shows how a mismatch error between spaces and tabs is handled.

**Input code**

Copy code

```
def foo():
    x = 5 # Spaces
     y = 6 # Tab

def foo2():
    x=6
    y=7
```

**Output code**

Copy code

```
def foo():
    x = 5 # Spaces
## EWI: SPRKPY1101 => Unrecognized or invalid CODE STATEMENT @(3, 2). Last valid token was '5' @(2, 9), failed token 'y' @(3, 2)
## y = 6 # Tab

def foo2():
    x=6
    y=7
```

### Recommendations

- Try fixing the commented line.
- For more support, email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). If you have a support contract with Snowflake, reach out to your sales engineer, who can direct your support needs.
