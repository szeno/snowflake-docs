# Snowpark Migration Accelerator: Snowpark Connect Issue Codes for Python

## SPRKCNTPY1000

**Message** The element < **element** > is not supported for Snowpark Connect

**Category** Conversion Error

### Description

This issue appears when the tool detects the usage of an element that is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for an unsupported element.

### Scenario

#### Input

The tool found an unidentified element of the pyspark library.

Copy code

```
from pyspark import NotSupportedElement
sc.addFile("data.txt")
print(NotSupportedElement.get("data.txt"))
```

#### Output

The tool adds the comment to the statement pointing to the unsupported element.

Copy code

```
from pyspark import NotSupportedElement
sc.addFile("data.txt")
# EWI SPRKCNTPY1000: The element 'NotSupportedElement' is not supported for Snowpark Connect
print(NotSupportedElement.get("data.txt"))
```

### Recommended fix

Since this is a generic error code that applies to a range of unsupported functions, there is not a single and specific fix. The appropriate action will depend on the particular element in use.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is some kind of workaround, please report that you encountered a conversion error on that particular element using the [Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY1001

`SparkSession` has been replaced with `Session` in Snowpark Connect.

**Message** The `SparkSession` creation has been transformed to use a Snowpark `Session` equivalent.

**Category** Warning.

### Description

This issue appears when the SMA detects the creation of a `SparkSession` object in the input code. Snowpark Connect uses a different object, called `Session`, to manage the connection to Snowflake and to create DataFrames.

When the SMA encounters the creation of a `SparkSession`, it adds this EWI to inform you that it has transformed the code to use a Snowpark Session instead.

### Scenario

#### Input

Below is an example of a Python `SparkSession` initialization which will be replaced for a Snowpark Connect `Session` initialization, and therefore it generates this EWI.

Copy code

```
spark = SparkSession.builder.getOrCreate()
```

#### Output

The SMA adds the EWI `SPRKCNTPY1001` to the output code to let you know that your `SparkSession` initialization has been replaced for a Snowpark Connect `Session` initialization.

Copy code

```
#EWI: SPRKCNTPY1001 => The creation of the SparkSession has been replaced with the creation of an equivalent Snowpark Connect Session.
spark = snowpark_connect.server.init_spark_session()
```

### Additional recommendations

- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). If you have a contract for support with Snowflake, reach out to your sales engineer, and they can direct your support needs.

## SPRKCNTPY1500

**Message** The element < **element** > of the library RDD is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of an RDD element is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for RDD unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `pyspark.rdd` library.

Copy code

```
from pyspark import SparkContext

sc = SparkContext("local", "Simple App")
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)
result = rdd.NotSupportedElement(withReplacement=False, fraction=0.5).collect()
print(result)
```

#### Output

The SMA adds the EWI `SPRKCNTPY1500` to the output code to let you know that this RDD element is not supported by Snowpark Connect.

Copy code

```
from pyspark import SparkContext

sc = SparkContext("local", "Simple App")
data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)
# EWI SPRKCNTPY1500: The element 'NotSupportedElement' of the library RDD is not supported for Snowpark Connect
result = rdd.NotSupportedElement(withReplacement=False, fraction=0.5).collect()
print(result)
```

### Recommended fix

- Convert RDD operations to DataFrame operations.

  Copy code

  ```
  # PySpark RDD approach (NOT supported)
  rdd = spark.sparkContext.parallelize(data)
  result = rdd.map(lambda x: x * 2).collect()

  # Snowpark DataFrame approach (Supported)
  df = session.create_dataframe(data, schema=["value"])
  result = df.select(col("value") * 2).collect()
  ```
- Process data locally before sending it to Snowflake if the RDD operations are simple.
- Use pandas DataFrames for local processing, then convert to Snowpark DataFrames.
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action will depend on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY2000

**Message** The element < **element** > of the library Streaming is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of a Streaming element is not supported in Snowpark Connect and does not have its own error code associated with it. This is the generic error code used by the SMA for Streaming unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `pyspark.streaming` library.

Copy code

```
from pyspark import SparkContext
from pyspark.streaming import NotSupportedElement

sc = SparkContext("local[2]", "NetworkWordCount")
ssc = NotSupportedElement(sc, 1)
```

#### Output

The SMA adds the EWI `SPRKCNTPY2000` to the output code to let you know that this Streaming element is not supported by Snowpark Connect.

Copy code

```
from pyspark import SparkContext
from pyspark.streaming import NotSupportedElement

sc = SparkContext("local[2]", "NetworkWordCount")
# EWI SPRKCNTPY2000: The element 'NotSupportedElement' of the library Streaming is not supported for Snowpark Connect
ssc = NotSupportedElement(sc, 1)
```

### Recommended fix

- Use Snowflake Streams to capture table changes.
- Process changes with Snowpark Connect in scheduled jobs.
- Ideal for maintaining derived tables.
- Since this is a generic error code that applies to a range of unsupported functions, there no single and specific fix. The appropriate action will depend on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY2500

**Message** The element < **element** > of the library ML is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines the usage instance of an ML element that is not supported in Snowpark Connect and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `pyspark.ml` library.

Copy code

```
from pyspark.ml.classification import NotSupportedElement

lr = NotSupportedElement(maxIter=10, regParam=0.01)
model = lr.fit(trainingData)
```

#### Output

The SMA adds the EWI `SPRKCNTPY2500` to the output code to let you know that this ML element is not supported by Snowpark Connect.

Copy code

```
from pyspark.ml.classification import NotSupportedElement

# EWI SPRKCNTPY2500: The element 'NotSupportedElement' of the library ML is not supported for Snowpark Connect
lr = NotSupportedElement(maxIter=10, regParam=0.01)
model = lr.fit(trainingData)
```

### Recommended fix

- Use the Snowpark ML library.

  Copy code

  ```
  # Instead of PySpark ML
  from snowflake.ml.modeling.linear_model import LinearRegression
  from snowflake.ml.modeling.ensemble import RandomForestRegressor

  # Snowpark ML approach
  model = LinearRegression()
  model.fit(train_df)
  predictions = model.predict(test_df)
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action will depend on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is some kind of workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY3000

**Message** The element < **element** > of the library MLLIB is not supported for Snowpark Connect

**Category** Conversion Error

### Description

This issue appears when the tool determines the usage instance of an MLLIB element that is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `pyspark.mllib` library.

Copy code

```
from pyspark.mllib.recommendation import NotSupportedElement, Rating
ratings = [
    Rating(0, 0, 4.0),
    Rating(0, 1, 2.0),
    Rating(1, 1, 5.0)
]
model = NotSupportedElement.train(ratings, 10)
```

#### Output

The SMA adds the EWI `SPRKCNTPY3000` to the output code to let you know that this MLLIB element is not supported by Snowpark Connect.

Copy code

```
from pyspark.mllib.recommendation import NotSupportedElement, Rating

# EWI SPRKCNTPY3000: The element 'NotSupportedElement' of the library MLLIB is not supported for Snowpark Connect
ratings = [
    Rating(0, 0, 4.0),
    Rating(0, 1, 2.0),
    Rating(1, 1, 5.0)
]
model = NotSupportedElement.train(ratings, 10)
```

### Recommended fix

- Use the Snowpark ML library.

  Copy code

  ```
  # Instead of MLlib's LinearRegressionWithSGD
  from snowflake.ml.modeling.linear_model import LinearRegression

  # MLlib approach (NOT supported)
  # from pyspark.mllib.regression import LinearRegressionWithSGD
  # model = LinearRegressionWithSGD.train(rdd_data)

  # Snowpark ML approach
  model = LinearRegression(input_cols=['feature1', 'feature2'], label_cols=['target'])
  model.fit(train_df)
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action will depend on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY3500

**Message** The element < **element** > of the library Spark Session is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of a Spark Session element is not supported in Snowpark Connect and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `pyspark.SparkSession` library.

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.SparkSession import NotSupportedElement

spark = SparkSession.builder.appName("Example").getOrCreate()
new_spark = spark.NotSupportedElement()
```

#### Output

The SMA adds the EWI `SPRKCNTPY3500` to the output code to let you know that this Spark Session element is not supported by Snowpark Connect.

Copy code

```
from pyspark.sql import SparkSession
from pyspark.sql.SparkSession import NotSupportedElement

spark = SparkSession.builder.appName("Example").getOrCreate()
# EWI SPRKCNTPY3500: The element 'NotSupportedElement' of the library Spark Session is not supported for Snowpark Connect
new_spark = spark.NotSupportedElement()
```

### Recommended fix

- The key is to replace `SparkSession` patterns with equivalent Snowpark `Session` operations while leveraging Snowflake’s unique capabilities like warehouses, stages, and native SQL functions.

  Copy code

  ```
  # PySpark SparkSession
  from pyspark.sql import SparkSession
  spark = SparkSession.builder.appName("MyApp").getOrCreate()

  # Snowpark Session
  from snowflake.snowpark import Session
  session = Session.builder.configs({
   "account": "your_account",
   "user": "your_user",
   "password": "your_password",
   "role": "your_role",
   "warehouse": "your_warehouse",
   "database": "your_database",
   "schema": "your_schema"
  }).create()
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action will depend on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is some kind of workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY3501

The `AppName` method of `pyspark.sql.session.SparkSession.Builder` has been replaced with the `SetName` function to provide equivalent functionality in Snowpark Connect when creating a session.

**Message** The `AppName` method of `pyspark.sql.session.SparkSession.Builder` has been replaced with the `SetName` function to provide equivalent functionality in Snowpark Connect.

**Category** Warning.

### Description

This issue occurs when the SMA detects the use of `AppName` Spark function while creating a `SparkSession` instance. The tool replaces this function with Snowpark initialization statements to achieve equivalent functionality.

### Scenario

#### Input

Below is an example of a Python `AppName` Spark function that will be replaced by the `SetAppName` Snowpark Connect function, and therefore it will add this EWI.

Copy code

```
spark = (
  SparkSession
    .builder
    .appName("MyApp")
    .getOrCreate()
)
```

#### Output

The SMA adds the EWI `SPRKCNTPY3501` to the output code to let you know that this element has been transformed.

Copy code

```
conf = SparkConf()
conf.setAppName("MyApp")
#EWI: SPRKCNTPY3501 => The AppName method of pyspark.sql.session.SparkSession.Builder has been replaced with the SetAppName function to provide equivalent functionality in Snowpark Connect

spark = ( snowpark_connect.server.init_spark_session(conf = conf)
)
```

### Recommended fix

Review the output code and ensure that the Snowpark Connect session is configured correctly with the desired application name.

### Additional recommendations

- Please review the Snowpark Connect documentation to understand how to configure and use Snowpark Connect sessions effectively.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). If you have a contract for support with Snowflake, reach out to your sales engineer, and they can direct your support needs.

## SPRKCNTPY3502

The `Master` method of `pyspark.sql.session.SparkSession.Builder` has been replaced with the `SetName` function to provide equivalent functionality in Snowpark Connect when creating a session.

**Message** The `Master` method of `pyspark.sql.session.SparkSession.Builder` has been replaced with the `SetName` function to provide equivalent functionality in Snowpark Connect.

**Category** Warning.

### Description

This issue occurs when the SMA detects the use of `Master` Spark function while creating a `SparkSession` instance. The tool replaces this function with Snowpark initialization statements to achieve equivalent functionality.

### Scenario

#### Input

Below is an example of a Python `Master` Spark function that will be replaced by the `SetAppName` Snowpark Connect function, and therefore it will add this EWI.

Copy code

```
spark = (
  SparkSession
    .builder
    .master("local[1]")
    .getOrCreate()
)
```

#### Output

The SMA adds the EWI `SPRKCNTPY3502` to the output code to let you know that this element has been transformed.

Copy code

```
conf = SparkConf()
conf.setMaster("local[1]")
#EWI: SPRKCNTPY3502 => The Master method of pyspark.sql.session.SparkSession.Builder has been replaced with the SetMaster function to provide equivalent functionality in Snowpark Connect

spark = ( snowpark_connect.server.init_spark_session(conf = conf)
)
```

### Recommended fix

Review the output code and ensure that the Snowpark Connect session is configured correctly with the desired master setting.

### Additional recommendations

- Please review the Snowpark Connect documentation to understand how to configure and use Snowpark Connect sessions effectively.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). If you have a contract for support with Snowflake, reach out to your sales engineer, and they can direct your support needs.

## SPRKCNTPY4000

SparkContext element is not supported by Snowpark Connect.

**Message** The element **<element full name>** of the library `SparkContext` is not supported by Snowpark Connect.

**Category** Conversion error

### Description

This issue appears when the SMA detects an usage of a Python `SparkContext` element that is not supported by Snowpark Connect and does not have its own specific error code associated with it. This is a generic error code used by the SMA for unsupported `SparkContext` elements.

### Scenario

#### Input

Below is an example of an usage of a `SparkContext` element that triggers this EWI:

Copy code

```
from pyspark import SparkContext

sc = SparkContext()
sc.not_supported_element()
```

#### Output

The SMA adds the EWI `SPRKCNTPY4000` indicating that the `SparkContext` element is not supported by Snowpark Connect.

Copy code

```
from pyspark import SparkContext

sc = SparkContext()
#EWI: SPRKCNTPY4000 => The element 'pyspark.context.SparkContext.not_supported_element' of the library SparkContext is not supported by Snowpark Connect
sc.not_supported_element()
```

### Recommended fix

Snowpark Connect uses a DataFrame-based architecture and doesn’t support `SparkContext` or RDD operations. As a workaround, you could refactor your code to use Snowpark Connect `Session` and `DataFrame` APIs instead.

### Additional recommendations

- Consult the [Snowpark Connect documentation](/developer-guide/snowpark-connect/snowpark-connect-apache-spark) for available alternatives to your specific use case.
- Note that some SparkContext functionality has no direct equivalent and may require application redesign.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTPY4001

**Message** `SparkContext` instantiation has been converted to a Snowpark Connect session.

**Category** Warning

### Description

This issue appears when the SMA detects [pyspark.context.SparkContext](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkContext.html) constructor calls in your code. The SMA automatically transforms these instantiations into equivalent Snowpark Connect session calls, enabling your Spark applications to run on Snowflake’s infrastructure.

The transformation process involves the following steps:

- Replacing `SparkContext` instantiation with `snowpark_connect.server.init_spark_session()`
- Preserving any existing `SparkConf` configuration parameters

> **Important**: Before running the converted code, you **must** configure your connection details in a `connections.toml` or `config.toml` file. This configuration file should contain your Snowflake account credentials, warehouse information, and other connection parameters required for Snowpark Connect to establish a connection to your Snowflake account.
>
> For comprehensive setup instructions, please refer to the [official Snowpark Connect documentation](/developer-guide/snowpark-connect/snowpark-connect-local-ide).

### Scenarios

#### Scenario 1

##### Input code

`SparkContext` instantiated with default parameters:

Copy code

```
sc = SparkContext()
```

##### Output code

The SMA sets the environment variable, starts the Snowpark Connect session, and retrieves the session without additional configuration:

Copy code

```
#EWI: SPRKCNTPY4001 => SparkContext instantiation has been converted to a Snowpark Connect session
sc = snowpark_connect.server.init_spark_session()
```

#### Scenario 2

##### Input code

SparkContext instantiated with master and `appName` parameters:

Copy code

```
sc = SparkContext(master="local[*]", appName="MyApp")
# or
sc = SparkContext("local[*]", "MyApp")
```

##### Output code

The SMA sets the environment variable, starts the Snowpark Connect session, and passes the parameters via a `SparkConf` object:

Copy code

```
conf = SparkConf()
conf.setAppName("MyApp")
conf.setMaster("local[*]")
#EWI: SPRKCNTPY4001 => SparkContext instantiation has been converted to a Snowpark Connect session
sc = snowpark_connect.server.init_spark_session(conf = conf)
```

#### Scenario 3

##### Input code

`SparkContext` instantiated using an existing `SparkConf` object.

Copy code

```
my_conf = SparkConf()
sc = SparkContext(conf=my_conf)
```

##### Output code

The SMA preserves the existing `SparkConf` object and passes it directly to the `snowpark_connect.server.init_spark_session()` method:

Copy code

```
my_conf = SparkConf()
#EWI: SPRKCNTPY4001 => SparkContext instantiation has been converted to a Snowpark Connect session
sc = snowpark_connect.server.init_spark_session(conf = my_conf)
```

### Additional Recommendations

- While the SMA preserves your `SparkConf` settings, not all Spark configurations may be supported in Snowpark Connect. Review your configurations to ensure compatibility.
- Ensure that downstream operations using the `SparkContext` object are compatible with Snowpark Connect, as some Spark-specific functionalities may not have direct equivalents.
- For more support, you can email us at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).
