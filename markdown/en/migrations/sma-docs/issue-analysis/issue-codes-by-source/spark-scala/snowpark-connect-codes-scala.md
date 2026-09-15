# Snowpark Migration Accelerator: Snowpark Connect Issue Codes for Scala

## SPRKCNTSCL1000

**Message** The element < **element** > is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool detects the usage of an element that is not supported in Snowpark Connect and does not have its own error code associated with it. This is the generic error code used by the SMA for an unsupported element.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark` library.

Copy code

```
import org.apache.spark.NotSupportedElement
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

val conf = new SparkConf().setAppName("GraphXExample").setMaster("local")
val sc = new SparkContext(conf)
val vertices: RDD[(VertexId, String)] = sc.parallelize(Seq((1L, "A"), (2L, "B")))
val edges: RDD[Edge[String]] = sc.parallelize(Seq(Edge(1L, 2L, "edge")))
val graph = NotSupportedElement(vertices, edges)
```

#### Output

The tool adds the comment to the statement pointing to the unsupported element.

Copy code

```
import org.apache.spark.NotSupportedElement
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkConf, SparkContext}

val conf = new SparkConf().setAppName("GraphXExample").setMaster("local")
val sc = new SparkContext(conf)
val vertices: RDD[(VertexId, String)] = sc.parallelize(Seq((1L, "A"), (2L, "B")))
val edges: RDD[Edge[String]] = sc.parallelize(Seq(Edge(1L, 2L, "edge")))
// EWI SPRKCNTSCL1000: The element 'NotSupportedElement' is not supported for Snowpark Connect
val graph = NotSupportedElement(vertices, edges)
```

### Recommended fix

Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTSCL1500

**Message** The element < **element** > of the library RDD is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of an RDD element is not supported in Snowpark Connect and does not have its own error code associated with it. This is the generic error code used by the SMA for RDD unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark.rdd` library.

Copy code

```
import org.apache.spark.rdd.RDD

val rdd: RDD[Int] = ???
rdd.NotSupportedElement()
```

#### Output

The SMA adds the EWI `SPRKCNTSCL1500` to the output code to let you know that this RDD element is not supported by Snowpark Connect.

Copy code

```
import snowflake.snowpark.snowpark_connect
import org.apache.spark.rdd.RDD

val rdd: RDD[Int] = ???
/*EWI: SPRKCNTSCL1500 => The element 'org.apache.spark.rdd.RDD.NotSupportedElement' of the library RDD is not supported for Snowpark Connect*/
rdd.NotSupportedElement()
```

### Recommended fix

- Convert RDD operations to DataFrame operations.
- The key recommendation is to completely abandon RDD patterns and redesign your data processing logic using Snowpark’s DataFrame API and SQL capabilities, leveraging Snowflake’s distributed computing architecture rather than trying to replicate RDD functionality.
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTSCL2000

**Message** The element < **element** > of the library Streaming is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of a Streaming element is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for Streaming unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark.streaming` library.

Copy code

```
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, NotSupportedElement}

val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
val ssc = new NotSupportedElement(conf, Seconds(1))
```

#### Output

The SMA adds the EWI `SPRKCNTSCL2000` to the output code to let you know that this Streaming element is not supported by Snowpark Connect.

Copy code

```
import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, NotSupportedElement}

val conf = new SparkConf().setAppName("NetworkWordCount").setMaster("local[2]")
// EWI SPRKCNTSCL2000: The element 'NotSupportedElement' of the library Streaming is not supported for Snowpark Connect
val ssc = new NotSupportedElement(conf, Seconds(1))
```

### Recommended fix

- The key recommendation is to completely redesign streaming architecture to use external streaming platforms for real-time processing combined with Snowpark Connect for analytical batch processing, rather than trying to replicate Spark Streaming functionality.
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTSCL2500

**Message** The element < **element** > of the library ML is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of an ML element is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark.ml` library.

Copy code

```
import org.apache.spark.ml.feature.NotSupportedElement
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder.appName("Example").getOrCreate()
val data = spark.read.format("libsvm").load("data.txt")
val scaler = new NotSupportedElement().setInputCol("features").setOutputCol("scaledFeatures")
```

#### Output

The SMA adds the EWI `SPRKCNTSCL2500` to the output code to let you know that this ML element is not supported by Snowpark Connect.

Copy code

```
import org.apache.spark.ml.feature.NotSupportedElement
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder.appName("Example").getOrCreate()
val data = spark.read.format("libsvm").load("data.txt")
// EWI SPRKCNTSCL2500: The element 'NotSupportedElement' of the library ML is not supported for Snowpark Connect
val scaler = new NotSupportedElement().setInputCol("features").setOutputCol("scaledFeatures")
```

### Recommended fix

- Use the Snowpark ML library.

  Copy code

  ```
  // Spark ML Pipeline (NOT supported)
  import org.apache.spark.ml.Pipeline
  import org.apache.spark.ml.classification.LogisticRegression
  import org.apache.spark.ml.feature.{HashingTF, Tokenizer}

  // Snowpark ML equivalent
  import com.snowflake.snowpark.ml.modeling.linear_model.LogisticRegression
  import com.snowflake.snowpark.ml.preprocessing.StandardScaler

  val lr = new LogisticRegression()
   .setInputCols(Array("feature1", "feature2"))
   .setLabelCols(Array("label"))
  val model = lr.fit(trainingData)
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTSCL3000

**Message** The element < **element** > of the library MLLIB is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines the the usage instance of an MLLIB element is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark.mllib` library.

Copy code

```
import org.apache.spark.mllib.recommendation.NotSupportedElement
import org.apache.spark.mllib.recommendation.Rating
import org.apache.spark.{SparkConf, SparkContext}

val conf = new SparkConf().setAppName("ALSExample").setMaster("local")
val sc = new SparkContext(conf)
val data = sc.textFile("data.txt")
val ratings = data.map(_.split(',') match { case Array(user, item, rate) =>
  Rating(user.toInt, item.toInt, rate.toDouble)
})
val model = NotSupportedElement.train(ratings, 10, 10, 0.01)
```

#### Output

The SMA adds the EWI `SPRKCNTSCL3000` to the output code to let you know that this MLLIB element is not supported by Snowpark Connect.

Copy code

```
import org.apache.spark.mllib.recommendation.NotSupportedElement
import org.apache.spark.mllib.recommendation.Rating
import org.apache.spark.{SparkConf, SparkContext}

val conf = new SparkConf().setAppName("ALSExample").setMaster("local")
val sc = new SparkContext(conf)
val data = sc.textFile("data.txt")
val ratings = data.map(_.split(',') match { case Array(user, item, rate) =>
  Rating(user.toInt, item.toInt, rate.toDouble)
})
// EWI SPRKCNTSCL3000: The element 'NotSupportedElement' of the library MLLIB is not supported for Snowpark Connect
val model = NotSupportedElement.train(ratings, 10, 10, 0.01)
```

### Recommended fix

- The key recommendation is to completely abandon MLlib patterns and redesign machine learning workflows using Snowpark ML, SQL-based ML functions, or hybrid approaches that leverage Snowflake distributed architecture rather than trying to replicate RDD-based MLlib functionality.

  Copy code

  ```
  // MLlib approach (NOT supported)
  import org.apache.spark.mllib.classification.LogisticRegressionWithSGD
  import org.apache.spark.mllib.regression.LabeledPoint

  val training = rdd.map { line =>
   val parts = line.split(',')
   LabeledPoint(parts(0).toDouble, Vectors.dense(parts(1).split(' ').map(_.toDouble)))
  }
  val model = LogisticRegressionWithSGD.train(training, numIterations)

  // Snowpark ML equivalent
  import com.snowflake.snowpark.ml.modeling.linear_model.LogisticRegression

  val model = new LogisticRegression()
   .setInputCols(Array("feature1", "feature2", "feature3"))
   .setLabelCols(Array("target"))
  val trainedModel = model.fit(trainingDataFrame)
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).

## SPRKCNTSCL3500

**Message** The element < **element** > of the library Spark Session is not supported for Snowpark Connect.

**Category** Conversion Error

### Description

This issue appears when the tool determines that the usage instance of a Spark Session element is not supported in Snowpark Connect, and does not have its own error code associated with it. This is the generic error code used by the SMA for ML unsupported elements.

### Scenario

#### Input

The tool found an unidentified element of the `org.apache.spark.sql.SparkSession` library.

Copy code

```
import org.apache.spark.sql.SparkSession.NotSupportedElement

val spark = SparkSession.builder.appName("Example").getOrCreate()
SparkSession.NotSupportedElement()
```

#### Output

The SMA adds the EWI `SPRKCNTSCL3500` to the output code to let you know that this Spark Session element is not supported by Snowpark Connect.

Copy code

```
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder.appName("Example").getOrCreate()
// EWI SPRKCNTSCL3500: The element 'NotSupportedElement' of the library Spark Session is not supported for Snowpark Connect
SparkSession.NotSupportedElement()
```

### Recommended fix

- The key is to replace `SparkSession` patterns with equivalent Snowpark `Session` operations while leveraging Snowflake’s unique capabilities like warehouses, stages, and native SQL functions.

  Copy code

  ```
  // Spark SparkSession
  import org.apache.spark.sql.SparkSession

  val spark = SparkSession.builder()
   .appName("MySparkApp")
   .master("local[*]")
   .getOrCreate()

  // Snowpark Session
  import com.snowflake.snowpark.Session

  val session = Session.builder
   .configs(Map(
       "URL" -> "https://account.snowflakecomputing.com",
       "USER" -> "username",
       "PASSWORD" -> "password",
       "ROLE" -> "role_name",
       "WAREHOUSE" -> "warehouse_name",
       "DB" -> "database_name",
       "SCHEMA" -> "schema_name"
   ))
   .create
  ```
- Since this is a generic error code that applies to a range of unsupported functions, there is no single and specific fix. The appropriate action depends on the particular element in use.
- Please note that even though the element is not supported, it does not necessarily mean that a solution or workaround cannot be found. It means only that the SMA itself cannot find the solution.

### Additional recommendations

- Even though the option or the element on the message is not supported, this does not mean that a solution cannot be found. It means only that the tool itself cannot find the solution.
- If you believe that Snowpark Connect already supports this element or that there is a workaround, please report that you encountered a conversion error on that particular element using [the Report an Issue option](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings) in the SMA and include any additional information that you think may be helpful.
- For more support, email support at [sma-support@snowflake.com](mailto:sma-support@snowflake.com) or post an issue [in the SMA](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings).
