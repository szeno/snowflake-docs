# Creating User-Defined Functions (UDFs) for DataFrames in Scala

The Snowpark API provides methods that you can use to create a user-defined function from a lambda or function in Scala. This
topic explains how to create these types of functions.

## Introduction

You can call Snowpark APIs to create user-defined functions (UDFs) for your custom lambdas and functions in Scala, and you can
call these UDFs to process the data in your DataFrame.

When you use the Snowpark API to create a UDF, the Snowpark library serializes and uploads the code for your UDF to an internal
stage. When you call the UDF, the Snowpark library executes your function on the server, where the data is located. As a result,
the data doesn’t need to be transferred to the client in order for the function to process the data.

In your custom code, you can also call code that is packaged in JAR files (for example, Java classes for a third-party library).

You can create a UDF for your custom code in one of two ways:

- You can [create an anonymous UDF](#label-snowpark-udf-inline-anonymous) and assign the function to a variable. As long as
  this variable is in scope, you can use this variable to call the UDF.

  Copy code

  ```
  // Create and register an anonymous UDF (doubleUdf).
  val doubleUdf = udf((x: Int) => x + x)
  // Call the anonymous UDF.
  val dfWithDoubleNum = df.withColumn("doubleNum", doubleUdf(col("num")))
  ```
- You can [create a named UDF](#label-snowpark-udf-inline-named) and call the UDF by name. You can use this if, for example,
  you need to call a UDF by name or use the UDF in a subsequent session.

  Copy code

  ```
  // Create and register a permanent named UDF ("doubleUdf").
  session.udf.registerPermanent("doubleUdf", (x: Int) => x + x, "mystage")
  // Call the named UDF.
  val dfWithDoubleNum = df.withColumn("doubleNum", callUDF("doubleUdf", col("num")))
  ```

The next sections provide important information about creating UDFs in Snowpark:

- [Data Types Supported for Arguments and Return Values](#label-snowpark-udf-data-types)
- [Caveat About Creating UDFs in an Object With the App Trait](#label-snowpark-udf-inline-scala-app-trait)

The rest of this topic explains how to create UDFs.

Note

If you defined a UDF by running the `CREATE FUNCTION` command, you can call that UDF in Snowpark.

For details, see [Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/scala/calling-functions#label-snowpark-udfs-calling).

### Data Types Supported for Arguments and Return Values

In order to create a UDF for a Scala function or lambda, you must use the supported data types listed below for the arguments and
return value of your function or lambda:

| SQL Data Type | Scala Data Type | Notes |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | The following types are supported:   - `Short` or `Option[Short]` - `Int` or `Option[Int]` - `Long` or `Option[Long]` - `java.math.BigDecimal` |  |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `Float` or `Option[Float]` |  |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `Double` or `Option[Double]` |  |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `String` or `java.lang.String` |  |
| [BOOLEAN](/sql-reference/data-types-logical) | `Boolean` or `Option[Boolean]` |  |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` |  |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` |  |
| [BINARY](/sql-reference/data-types-text) | `Array[Byte]` |  |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark.types.Variant](../reference/scala/com/snowflake/snowpark/types/Variant.html) |  |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Array[String]` or `Array[Variant]` |  |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map[String, String]` or `Map[String, Variant]` | Mutable maps of the following types are supported:   - `scala.collection.mutable.Map[String, String]` - `scala.collection.mutable.Map[String, Variant]` |
| [GEOGRAPHY](/sql-reference/data-types-geospatial) | [com.snowflake.snowpark.types.Geography](../reference/scala/com/snowflake/snowpark/types/Geography.html) |  |

Expand

Show lessSee more

### Caveat About Creating UDFs in an Object With the App Trait

Scala provides an [App](https://www.scala-lang.org/api/2.12.11/scala/App.html) trait that you can extend in order to turn your
Scala object into an executable program. The `App` trait provides a `main` method that automatically executes all the
code in the body of your object definition. (The code in your object definition effectively becomes the `main` method.)

One effect of extending the `App` trait is that the fields in your object won’t be initialized until the `main` method
is called. If your object extends `App` and you define a UDF that uses an object field that you initialized earlier, the UDF
definition uploaded to the server won’t include the initialized value of the object field.

For example, suppose that you define and initialize a field named `myConst` in the object and use that field in a UDF:

Copy code

```
object Main extends App {
  ...
  // Initialize a field.
  val myConst = "Prefix "
  // Use the field in a UDF.
  // Because the App trait delays the initialization of the object fields,
  // myConst in the UDF definition resolves to null.
  val myUdf = udf((s : String) =>  myConst + s )
  ...
}
```

When Snowpark serializes and uploads the UDF definition to Snowflake, `myConst` is not initialized and resolves to `null`.
As a result, calling the UDF returns `null` for `myConst`.

To work around this, change your object so that it does not extend the `App` trait, and implement a separate `main`
method for your code:

Copy code

```
object Main {
  ...
  def main(args: Array[String]): Unit = {
    ... // Your code ...
  }
  ...
}
```

## Specifying Dependencies for a UDF

In order to define a UDF through the Snowpark API, you must call `Session.addDependency()` for any files that contain any
classes and resources that your UDF depends on (e.g. JAR files, resource files, etc.). (For details on reading resources from a
UDF, see [Reading Files from a UDF](#label-snowpark-udf-read-files).)

The Snowpark library uploads these files to an internal stage and adds the files to the classpath when executing your UDF.

Tip

If you don’t want the library to upload the file every time you run your application, upload the file to a stage. When calling
`addDependency`, pass the path to the file in the stage.

If you are using the Scala REPL, you must add the
[directory of classes generated by the REPL](/developer-guide/snowpark/scala/quickstart-scala-repl) as a dependency. For example, if you used the
`run.sh` script to start the REPL, call the following method, which adds the `repl_classes` directory created by the
script:

Copy code

```
// If you used the run.sh script to start the Scala REPL, call this to add the REPL classes directory as a dependency.
session.addDependency("<path_to_directory_where_you_ran_run.sh>/repl_classes/")
```

The following example demonstrates how to add a JAR file in a stage as a dependency:

Copy code

```
// Add a JAR file that you uploaded to a stage.
session.addDependency("@my_stage/<path>/my-library.jar")
```

The following examples demonstrate how to add dependencies for JAR files and resource files:

Copy code

```
// Add a JAR file on your local machine.
session.addDependency("/<path>/my-library.jar")

// Add a directory of resource files.
session.addDependency("/<path>/my-resource-dir/")

// Add a resource file.
session.addDependency("/<path>/my-resource.xml")
```

You should not need to specify the following dependencies:

> - **Your Scala runtime libraries.**
>
>   These libraries are already available in the runtime environment on the server where your UDFs are executed.
> - **The Snowpark JAR file.**
>
>   The Snowpark library automatically attempts to detect and upload the Snowpark JAR file to the server.
>
>   To prevent the library from repeatedly uploading the Snowpark JAR file to the server:
>
>   1. Upload the Snowpark JAR file to a stage.
>
>      For example, the following command uploads the Snowpark JAR file to the stage `@mystage`. The PUT command compresses the
>      JAR file and names the resulting file snowpark\_2.12-1.18.0.jar.gz.
>
>      ```
>      -- Put the Snowpark JAR file in a stage.
>      PUT file:///<path>/snowpark_2.12-1.18.0.jar @mystage
>      ```
>   2. Call `addDependency` to add the Snowpark JAR file in the stage as a dependency.
>
>      For example, to add the Snowpark JAR file uploaded by the previous command:
>
>      ```
>      // Add the Snowpark JAR file that you uploaded to a stage.
>      session.addDependency("@mystage/snowpark_2.12-1.18.0.jar.gz")
>      ```
>
>      Note that the specified path to the JAR file includes the `.gz` filename extension, which was added by the PUT command.
> - **The JAR file or directory with the currently running application.**
>
>   The Snowpark library automatically attempts to detect and upload these dependencies.
>
>   If the Snowpark library is unable to detect these dependencies automatically, the library reports an error, and you must call
>   `addDependency` to add these dependencies manually.

If it takes too long for the dependencies to be uploaded to the stage, the Snowpark library reports a timeout exception. To
configure the maximum amount of time that the Snowpark library should wait, set the
[snowpark\_request\_timeout\_in\_seconds](/developer-guide/snowpark/scala/creating-session#label-snowpark-request-timeout-in-seconds) property when creating the session.

## Creating an Anonymous UDF

To create an anonymous UDF, you can either:

- Call the `udf` function in the `com.snowflake.snowpark.functions` object, passing in the definition of the anonymous
  function.
- Call the `registerTemporary` method in the `UDFRegistration` class, passing in the definition of the anonymous
  function. Because you are registering an anonymous UDF, you must use the method signatures that don’t have a `name`
  parameter.

Note

When writing multi-threaded code (e.g. when using parallel collections), use the `registerTemporary` method to register
UDFs, rather than using the `udf` function. This can prevent errors in which the default Snowflake `Session` object
cannot be found.

These methods return a `UserDefinedFunction` object, which you can use to call the UDF. (See
[Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/scala/calling-functions#label-snowpark-udfs-calling).)

The following example creates an anonymous UDF:

Copy code

```
// Create and register an anonymous UDF.
val doubleUdf = udf((x: Int) => x + x)
// Call the anonymous UDF, passing in the "num" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleNum".
val dfWithDoubleNum = df.withColumn("doubleNum", doubleUdf(col("num")))
```

Note

If you are creating a UDF in a Jupyter notebook, you must set up the notebook to work with Snowpark (see
[Setting Up a Jupyter Notebook for Snowpark Scala](/developer-guide/snowpark/scala/quickstart-jupyter)) and follow the guidelines for writing UDFs in a notebook (see
[Creating UDFs in Jupyter Notebooks](#label-snowpark-udf-jupyter)).

The following example creates an anonymous UDF that passes in an `Array` of `String` values and appends the string
`x` to each value:

Copy code

```
// Create and register an anonymous UDF.
val appendUdf = udf((x: Array[String]) => x.map(a => a + " x"))
// Call the anonymous UDF, passing in the "a" column, which holds an ARRAY.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "appended".
val dfWithXAppended = df.withColumn("appended", appendUdf(col("a")))
```

The following example creates an anonymous UDF that uses a custom class (`LanguageDetector`, which detects the language used
in text). The example calls the anonymous UDF to detect the language in the `text_data` column in a DataFrame and creates a new
DataFrame that includes an additional `lang` column with the language used.

Copy code

```
// Import the udf function from the functions object.
import com.snowflake.snowpark.functions._

// Import the package for your custom code.
// The custom code in this example detects the language of textual data.
import com.mycompany.LanguageDetector

// If the custom code is packaged in a JAR file, add that JAR file as
// a dependency.
session.addDependency("$HOME/language-detector.jar")

// Create a detector
val detector = new LanguageDetector()

// Create an anonymous UDF that takes a string of text and returns the language used in that string.
// Note that this captures the detector object created above.
// Assign the UDF to the langUdf variable, which will be used to call the UDF.
val langUdf = udf((s: String) =>
     Option(detector.detect(s)).getOrElse("UNKNOWN"))

// Create a new DataFrame that contains an additional "lang" column that contains the language
// detected by the UDF.
val dfEmailsWithLangCol =
    dfEmails.withColumn("lang", langUdf(col("text_data")))
```

## Creating and Registering a Named UDF

If you want to call a UDF by name (e.g. by using the `callUDF` function in the `functions` object) or if you need to
use a UDF in subsequent sessions, you can create and register a named UDF. To do this, use one of the following methods in the
`UDFRegistration` class:

- `registerTemporary`, if you just plan to use the UDF in the current session
- `registerPermanent`, if you plan to use the UDF in subsequent sessions

To access an object of the `UDFRegistration` class, call the `udf` method of the `Session` class.

`registerTemporary` creates a temporary UDF that you can use in the current session.

Copy code

```
// Create and register a temporary named UDF.
session.udf.registerTemporary("doubleUdf", (x: Int) => x + x)
// Call the named UDF, passing in the "num" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleNum".
val dfWithDoubleNum = df.withColumn("doubleNum", callUDF("doubleUdf", col("num")))
```

`registerPermanent` creates a UDF that you can use in the current and subsequent sessions. When you call
`registerPermanent`, you must also specify a location in an internal stage location where the JAR files for the UDF and its
dependencies will be uploaded.

Note

`registerPermanent` does not support external stages.

For example:

Copy code

```
// Create and register a permanent named UDF.
// Specify that the UDF and dependent JAR files should be uploaded to
// the internal stage named mystage.
session.udf.registerPermanent("doubleUdf", (x: Int) => x + x, "mystage")
// Call the named UDF, passing in the "num" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleNum".
val dfWithDoubleNum = df.withColumn("doubleNum", callUDF("doubleUdf", col("num")))
```

Note

If you are creating a UDF in a Jupyter notebook, you must set up the notebook to work with Snowpark (see
[Setting Up a Jupyter Notebook for Snowpark Scala](/developer-guide/snowpark/scala/quickstart-jupyter)) and follow the guidelines for writing UDFs in a notebook (see
[Creating UDFs in Jupyter Notebooks](#label-snowpark-udf-jupyter)).

## Creating UDFs in Jupyter Notebooks

If you are creating UDFs in a [Jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html), you must
follow these additional steps:

- [Setting Up a Jupyter Notebook for Snowpark Scala](/developer-guide/snowpark/scala/quickstart-jupyter) (if you haven’t already set up the notebook to work with Snowpark)
- [Writing the Implementation of a UDF](#label-snowpark-udf-jupyter-serializable-class)
- [Accessing a Variable Defined in Another Cell](#label-snowpark-udf-jupyter-access-var)

### Writing the Implementation of a UDF

Define the implementation of your function in a class that extends `Serializable`. For example:

Copy code

```
// Class containing a function that implements your UDF.
class MyUDFCode( ... ) extends Serializable {
  val myUserDefinedFunc = (s: String) => {
    ...
  }
}
val myUdf = udf((new MyUDFCode(resourceName)).myUserDefinedFunc)
```

### Accessing a Variable Defined in Another Cell

If you need to use a variable defined in another cell in your UDF, you must pass the variable as an argument to the class
constructor. For example, suppose that in cell 1, you’ve defined a variable:

Copy code

```
In [1]:
```

Copy code

```
val prefix = "Hello"
```

and you want to use that variable in a UDF that you’ve defined in cell 2. In the class constructor for the UDF, add an argument
for this variable. Then, when calling the class constructor to create the UDF, pass in the variable defined in cell 1:

Copy code

```
In [2]:
```

Copy code

```
// resourceName is the argument for the variable defined in another cell.
class UDFCode(var prefix: String) extends Serializable {
  val prependPrefixFunc = (s: String) => {
    s"$prefix $s"
  }
}

// When constructing UDFCode, pass in the variable (resourceName) that is defined in another cell.
val prependPrefixUdf = udf((new UDFCode(prefix)).prependPrefixFunc)
val myDf = session.sql("select 'Raymond' NAME")
myDf.withColumn("CONCAT", prependPrefixUdf(col("NAME"))).show()
```

## Using Objects That Are Not Serializable

When you create a UDF for a lambda or function, the Snowpark library serializes the lambda closure and sends it to the server for
execution.

If an object captured by the lambda closure is not serializable, the Snowpark library throws an
`java.io.NotSerializableException` exception.

Copy code

```
Exception in thread "main" java.io.NotSerializableException: <YourObjectName>
```

If this occurs, you can either:

- Make the object serializable, or
- Declare the object as a `lazy val` or use the `@transient` annotation to avoid serializing the object.

  For example:

  Copy code

  ```
  // Declare the detector object as lazy.
  lazy val detector = new LanguageDetector("en")
  // The detector object is not serialized but is instead reconstructed on the server.
  val langUdf = udf((s: String) =>
    Option(detector.detect(s)).getOrElse("UNKNOWN"))
  ```

## Writing Initialization Code for a UDF

If your UDF requires initialization code or context, you can provide this through values captured as part of the UDF closure.

The following example uses a separate class to initialize the context needed by three UDFs.

- The first UDF creates a new instance of the class within the lambda, so the initialization is performed every time the UDF is
  invoked.
- The second UDF captures an instance of the class generated in your client program. The context generated on the client is
  serialized and is used by the UDF. Note that the context class must be serializable for this approach to work.
- The third UDF captures a `lazy val`, so the context is instantiated lazily on the first UDF invocation and is reused in
  subsequent invocations. This approach works even when the context is not serializable. However, there is no guarantee that
  ALL UDF invocations within a dataframe will use the same lazily generated context.

Copy code

```
import com.snowflake.snowpark._
import com.snowflake.snowpark.functions._
import scala.util.Random

// Context needed for a UDF.
class Context {
  val randomInt = Random.nextInt
}

// Serializable context needed for the UDF.
class SerContext extends Serializable {
  val randomInt = Random.nextInt
}

object TestUdf {
  def main(args: Array[String]): Unit = {
    // Create the session.
    val session = Session.builder.configFile("/<path>/profile.properties").create
    import session.implicits._
    session.range(1, 10, 2).show()

    // Create a DataFrame with two columns ("c" and "d").
    val dummy = session.createDataFrame(Seq((1, 1), (2, 2), (3, 3))).toDF("c", "d")
    dummy.show()

    // Initialize the context once per invocation.
    val udfRepeatedInit = udf((i: Int) => (new Context).randomInt)
    dummy.select(udfRepeatedInit('c)).show()

    // Initialize the serializable context only once,
    // regardless of the number of times that the UDF is invoked.
    val sC = new SerContext
    val udfOnceInit = udf((i: Int) => sC.randomInt)
    dummy.select(udfOnceInit('c)).show()

    // Initialize the non-serializable context only once,
    // regardless of the number of times that the UDF is invoked.
    lazy val unserC = new Context
    val udfOnceInitU = udf((i: Int) => unserC.randomInt)
    dummy.select(udfOnceInitU('c)).show()
  }
}
```

## Reading Files from a UDF

As mentioned earlier, the Snowpark library uploads and executes UDFs on the server. If your UDF needs to read data from a file,
you must ensure that the file is uploaded with the UDF.

In addition, if the content of the file remains the same between calls to the UDF, you can write your code to load the file once
during the first call and not on subsequent calls. This can improve the performance of your UDF calls.

To set up a UDF to read a file:

1. Add the file to a JAR file.

   For example, if your UDF needs to use a file in a `data/` subdirectory (`data/hello.txt`), run the `jar` command to
   add this file to a JAR file:

   Copy code

   ```
   # Create a new JAR file containing data/hello.txt.
   $ jar cvf <path>/myJar.jar data/hello.txt
   ```
2. Specify that the JAR file is a dependency, which uploads the file to the server and adds the file to the classpath. See
   [Specifying Dependencies for a UDF](#label-snowpark-udf-inline-dependencies).

   For example:

   Copy code

   ```
   // Specify that myJar.jar contains files that your UDF depends on.
   session.addDependency("<path>/myJar.jar")
   ```
3. In the UDF, call `Class.getResourceAsStream` to find the file in the classpath and read the file.

   To avoid adding a dependency on `this`, you can use `classOf[com.snowflake.snowpark.DataFrame]` (rather than
   `getClass`) to get the `Class` object.

   For example, to read the `data/hello.txt` file:

   Copy code

   ```
   // Read data/hello.txt from myJar.jar.
   val resourceName = "/data/hello.txt"
   val inputStream = classOf[com.snowflake.snowpark.DataFrame].getResourceAsStream(resourceName)
   ```

   In this example, the resource name starts with a `/`, which indicates that this is the full path of the file in the JAR file.
   (In this case, the location of the file is not relative to the package of the class.)

> Note
>
> If you don’t expect the content of the file to change between UDF calls, read the file into a `lazy val`. This causes
> the file loading code to execute only on the first call to the UDF and not on subsequent calls.

The following example defines an object (`UDFCode`) with a function that will be used as a UDF (`readFileFunc`). The function
reads the file `data/hello.txt`, which is expected to contain the string `hello,`. The function prepends this string to the
string passed in as an argument.

Copy code

```
// Create a function object that reads a file.
object UDFCode extends Serializable {

  // The code in this block reads the file. To prevent this code from executing each time that the UDF is called,
  // the code is used in the definition of a lazy val. The code for a lazy val is executed only once when the variable is
  // first accessed.
  lazy val prefix = {
    import java.io._
    val resourceName = "/data/hello.txt"
    val inputStream = classOf[com.snowflake.snowpark.DataFrame]
      .getResourceAsStream(resourceName)
    if (inputStream == null) {
      throw new Exception("Can't find file " + resourceName)
    }
    scala.io.Source.fromInputStream(inputStream).mkString
  }

  val readFileFunc = (s: String) => prefix + " : " + s
}
```

The next part of the example registers the function as an anonymous UDF. The example calls the UDF on the `NAME` column in a
DataFrame. The example assumes that the `data/hello.txt` file is packaged in the JAR file `myJar.jar`.

Copy code

```
// Add the JAR file as a dependency.
session.addDependency("<path>/myJar.jar")

// Create a new DataFrame with one column (NAME)
// that contains the name "Raymond".
val myDf = session.sql("select 'Raymond' NAME")

// Register the function that you defined earlier as an anonymous UDF.
val readFileUdf = udf(UDFCode.readFileFunc)

// Call UDF for the values in the NAME column of the DataFrame.
myDf.withColumn("CONCAT", readFileUdf(col("NAME"))).show()
```

## Creating User-Defined Table Functions (UDTFs)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

To create and register a UDTF in Snowpark, you must:

- [Define a class for the UDTF](#label-snowpark-udtf-define-class).
- [Create an instance of that class, and register that instance as a UDTF](#label-snowpark-udtf-register).

The next sections describe these steps in more detail.

For information on calling a UDTF, see [Calling a UDTF](#label-snowpark-udtf-call).

### Defining the UDTF Class

Define a class that inherits from one of the `UDTFn` classes (e.g. `UDTF0`, `UDTF1`, etc.) in the
[com.snowflake.snowpark.udtf package](../reference/scala/com/snowflake/snowpark/udtf/index.html), where `n` specifies the number of input arguments for your UDTF. For example, if
your UDTF passes in 2 input arguments, extend the `UDTF2` class.

In your class, override the following methods:

- [outputSchema()](#label-snowpark-udtf-define-class-output-schema), which returns a `types.StructType` object that
  describes the names and types of the fields in the returned rows (the “schema” of the output).
- [process()](#label-snowpark-udtf-define-class-process), which is called once for each row in the input partition
  (see the note below).
- [endPartition()](#label-snowpark-udtf-define-class-end-partition), which is called once for each partition after all rows
  have been passed to `process()`.

When a UDTF is called, the rows are grouped into partitions before they are passed to the UDTF:

- If the statement that calls the UDTF specifies the PARTITION clause (explicit partitions), that clause determines how the rows
  are partitioned.
- If the statement does not specify the PARTITION clause (implicit partitions), Snowflake determines how best to partition the
  rows.

For an explanation of partitions, see [Table functions and partitions](/developer-guide/udf/udf-calling-sql#label-udf-java-partitions).

For an example of a UDTF class, see [Example of a UDTF Class](#label-snowpark-udtf-define-class-example).

#### Overriding the outputSchema() Method

Override the `outputSchema()` method to define the names and data types of the fields (the “output schema”) of the rows
returned by the `process()` and `endPartition()` methods.

> Copy code
>
> ```
> def outputSchema(): StructType
> ```

In this method, construct and return a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object that uses an `Array` of [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects to specify the
Snowflake data type of each field in a returned row. Snowflake supports the following type objects for the output schema for a
UDTF:

| SQL Data Type | Scala Type | `com.snowflake.snowpark.types` Type |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `Short` or `Option[Short]` | `ShortType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `Int` or `Option[Int]` | `IntType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `Long` or `Option[Long]` | `LongType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.math.BigDecimal` | `DecimalType` |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `Float` or `Option[Float]` | `FloatType` |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `Double` or `Option[Double]` | `DoubleType` |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `String` or `java.lang.String` | `StringType` |
| [BOOLEAN](/sql-reference/data-types-logical) | `Boolean` or `Option[Boolean]` | `BooleanType` |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` | `DateType` |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` | `TimestampType` |
| [BINARY](/sql-reference/data-types-text) | `Array[Byte]` | `BinaryType` |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark.types.Variant](../reference/scala/com/snowflake/snowpark/types/Variant.html) | `VariantType` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Array[String]` | `ArrayType(StringType)` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Array[Variant]` | `ArrayType(VariantType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map[String, String]` | `MapType(StringType, StringType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map[String, Variant]` | `MapType(StringType, VariantType)` |

Expand

Show lessSee more

For example, if your UDTF returns a row with a single integer field:

> Copy code
>
> ```
> override def outputSchema(): StructType = StructType(StructField("C1", IntegerType))
> ```

#### Overriding the process() Method

In your UDTF class, override the `process()` method:

> Copy code
>
> ```
> def process(arg0: A0, ... arg<n> A<n>): Iterable[Row]
> ```

where `n` is the number of arguments passed to your UDTF.

The number of arguments in the signature corresponds to the class that you extended. For example, if your UDTF passes in 2 input
arguments and you are extending the `UDTF2` class, the `process()` method has this signature:

> Copy code
>
> ```
> def process(arg0: A0, arg1: A1): Iterable[Row]
> ```

This method is invoked once for each row in the input partition.

##### Choosing the Types of the Arguments

For the type of each argument in the `process()` method, use the Scala type that corresponds to the Snowflake data type of
the argument passed to the UDTF.

Snowflake supports the following data types for the arguments for a UDTF:

| SQL Data Type | Scala Data Type | Notes |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | The following types are supported:   - `Short` or `Option[Short]` - `Int` or `Option[Int]` - `Long` or `Option[Long]` - `java.math.BigDecimal` |  |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `Float` or `Option[Float]` |  |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `Double` or `Option[Double]` |  |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `String` or `java.lang.String` |  |
| [BOOLEAN](/sql-reference/data-types-logical) | `Boolean` or `Option[Boolean]` |  |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` |  |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` |  |
| [BINARY](/sql-reference/data-types-text) | `Array[Byte]` |  |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark.types.Variant](../reference/scala/com/snowflake/snowpark/types/Variant.html) |  |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Array[String]` or `Array[Variant]` |  |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map[String, String]` or `Map[String, Variant]` | Mutable maps of the following types are supported:   - `scala.collection.mutable.Map[String, String]` - `scala.collection.mutable.Map[String, Variant]` |

Expand

Show lessSee more

##### Returning Rows

In the `process()` method, construct and return an `Iterable` of `Row` objects that contain the data to be
returned by the UDTF for the given input values. The fields in the row must use the types that you specified in the
`outputSchema` method. (See [Overriding the outputSchema() Method](#label-snowpark-udtf-define-class-output-schema).)

For example, if your UDTF generates rows, construct and return an `Iterable` of `Row` objects for the generated rows:

> Copy code
>
> ```
> override def process(start: Int, count: Int): Iterable[Row] =
>     (start until (start + count)).map(Row(_))
> ```

#### Overriding the endPartition() Method

Override the `endPartition` method and add code that should be executed after all rows in the input partition have been
passed to the `process` method. The `endPartition` method is invoked once for each input partition.

> Copy code
>
> ```
> def endPartition(): Iterable[Row]
> ```

You can use this method if you need to perform any work after all of the rows in the partition have been processed. For example,
you can:

- Return rows based on state information that you capture in each `process` method call.
- Return rows that are not tied to a specific input row.
- Return rows that summarize the output rows that have been generated by the `process` method.

The fields in the rows that you return must match the types that you specified in the `outputSchema` method. (See
[Overriding the outputSchema() Method](#label-snowpark-udtf-define-class-output-schema).)

If you do not need to return additional rows at the end of each partition, return an empty `Iterable` of `Row`
objects. for example:

> Copy code
>
> ```
> override def endPartition(): Iterable[Row] = Array.empty[Row]
> ```

Note

While Snowflake supports large partitions with timeouts tuned to process them successfully, especially large partitions can cause
processing to time out (such as when `endPartition` takes too long to complete). Please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need the
timeout threshold adjusted for specific usage scenarios.

#### Example of a UDTF Class

The following is an example of a UDTF class that generates a range of rows.

- Because the UDTF passes in 2 arguments, the class extends `UDTF2`.
- The arguments `start` and `count` specify the starting number for the row and the number of rows to generate.

Copy code

```
class MyRangeUdtf extends UDTF2[Int, Int] {
  override def process(start: Int, count: Int): Iterable[Row] =
    (start until (start + count)).map(Row(_))
  override def endPartition(): Iterable[Row] = Array.empty[Row]
  override def outputSchema(): StructType = StructType(StructField("C1", IntegerType))
}
```

### Registering the UDTF

Next, create an instance of the new class, and register the class by calling one of the [UDTFRegistration](../reference/scala/com/snowflake/snowpark/UDTFRegistration.html) methods. You can
register a [temporary](#label-snowpark-udtf-register-name-temporary) or
[permanent UDTF](#label-snowpark-udtf-register-name-permanent).

#### Registering a Temporary UDTF

To register a temporary UDTF, call `UDTFRegistration.registerTemporary`:

- If you do not need to call the UDTF by name, you can register an anonymous UDTF by passing in an instance of the class:

  Copy code

  ```
  // Register the MyRangeUdtf class that was defined in the previous example.
  val tableFunction = session.udtf.registerTemporary(new MyRangeUdtf())
  // Use the returned TableFunction object to call the UDTF.
  session.tableFunction(tableFunction, lit(10), lit(5)).show
  ```
- If you need to call the UDTF by name, pass in a name of the UDTF as well:

  Copy code

  ```
  // Register the MyRangeUdtf class that was defined in the previous example.
  val tableFunction = session.udtf.registerTemporary("myUdtf", new MyRangeUdtf())
  // Call the UDTF by name.
  session.tableFunction(TableFunction("myUdtf"), lit(10), lit(5)).show()
  ```

#### Registering a Permanent UDTF

If you need to use the UDTF in subsequent sessions, call `UDTFRegistration.registerPermanent` to register a permanent UDTF.

When registering a permanent UDTF, you must specify a stage where the registration method will upload the JAR files for the UDTF
and its dependencies. For example:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> val tableFunction = session.udtf.registerPermanent("myUdtf", new MyRangeUdtf(), "@mystage")
> // Call the UDTF by name.
> session.tableFunction(TableFunction("myUdtf"), lit(10), lit(5)).show()
> ```

### Calling a UDTF

After registering the UDTF, you can call the UDTF by passing the returned `TableFunction` object to the
`tableFunction` method of the `Session` object:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> val tableFunction = session.udtf.registerTemporary(new MyRangeUdtf())
> // Use the returned TableFunction object to call the UDTF.
> session.tableFunction(tableFunction, lit(10), lit(5)).show()
> ```

To call a UDTF by name, construct a `TableFunction` object with that name, and pass that to the `tableFunction`
method:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> val tableFunction = session.udtf.registerTemporary("myUdtf", new MyRangeUdtf())
> // Call the UDTF by name.
> session.tableFunction(TableFunction("myUdtf"), lit(10), lit(5)).show()
> ```

You can also call a UDTF through a SELECT statement directly:

> Copy code
>
> ```
> session.sql("select * from table(myUdtf(10, 5))")
> ```
