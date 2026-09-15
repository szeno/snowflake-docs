# Creating User-Defined Functions (UDFs) for DataFrames in Java

The Snowpark API provides methods that you can use to create a user-defined function from a lambda expression in Java.
This topic explains how to create these types of functions.

## Introduction

You can call Snowpark APIs to create user-defined functions (UDFs) for lambda expressions in Java, and you can call
these UDFs to process the data in your DataFrame.

When you use the Snowpark API to create a UDF, the Snowpark library serializes and uploads the code for your UDF to a stage. When you call the UDF, the Snowpark library executes your function on the server, where the data is located. As a result,
the data doesn’t need to be transferred to the client in order for the function to process the data.

In your custom code, you can also call code that is packaged in JAR files (for example, Java classes for a third-party library).

You can create a UDF for your custom code in one of two ways:

- You can [create an anonymous UDF](#label-snowpark-java-udf-inline-anonymous) and assign the function to a variable. As long
  as this variable is in scope, you can use this variable to call the UDF.

  Copy code

  ```
  import com.snowflake.snowpark_java.types.*;
  ...

  // Create and register an anonymous UDF (doubleUdf)
  // that takes in an integer argument and returns an integer value.
  UserDefinedFunction doubleUdf =
    Functions.udf((Integer x) -> x + x, DataTypes.IntegerType, DataTypes.IntegerType);
  // Call the anonymous UDF.
  DataFrame df = session.table("sample_product_data");
  DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", doubleUdf.apply(Functions.col("quantity")));
  dfWithDoubleQuantity.show();
  ```
- You can [create a named UDF](#label-snowpark-java-udf-inline-named) and call the UDF by name. You can use this if, for
  example, you need to call a UDF by name or use the UDF in a subsequent session.

  Copy code

  ```
  import com.snowflake.snowpark_java.types.*;
  ...

  // Create and register a permanent named UDF ("doubleUdf")
  // that takes in an integer argument and returns an integer value.
  UserDefinedFunction doubleUdf =
    session
   .udf()
   .registerPermanent(
     "doubleUdf",
     (Integer x) -> x + x,
     DataTypes.IntegerType,
     DataTypes.IntegerType,
     "mystage");
  // Call the named UDF.
  DataFrame df = session.table("sample_product_data");
  DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", Functions.callUDF("doubleUdf", Functions.col("quantity")));
  dfWithDoubleQuantity.show();
  ```

The rest of this topic explains how to create UDFs.

Note

If you defined a UDF by running the `CREATE FUNCTION` command, you can call that UDF in Snowpark.

For details, see [Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/java/calling-functions#label-snowpark-java-udfs-calling).

## Data Types Supported for Arguments and Return Values

In order to create a UDF for a Java lambda, you must use the supported data types listed below for the arguments and return value
of your method:

| SQL Data Type | Java Data Type | Notes |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | The following types are supported:   - `Integer` - `Long` - `java.math.BigDecimal` or `java.math.BigInteger` |  |
| [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) | `Float` |  |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) | `Double` |  |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `String` |  |
| [BOOLEAN](/sql-reference/data-types-logical) | `Boolean` |  |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` |  |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` |  |
| [BINARY](/sql-reference/data-types-text) | `Byte[]` |  |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark\_java.types.Variant](../reference/java/com/snowflake/snowpark_java/types/Variant.html) |  |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `String[]` or `Variant[]` |  |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map<String, String>` or `Map<String, Variant>` |  |
| [GEOGRAPHY](/sql-reference/data-types-geospatial) | [com.snowflake.snowpark\_java.types.Geography](../reference/java/com/snowflake/snowpark_java/types/Geography.html) |  |

Expand

Show lessSee more

## Specifying Dependencies for a UDF

In order to define a UDF through the Snowpark API, you must call `Session.addDependency()` for any files that contain any
classes and resources that your UDF depends on (e.g. JAR files, resource files, etc.). (For details on reading resources from a
UDF, see [Reading Files from a UDF](#label-snowpark-java-udf-read-files).)

The Snowpark library uploads these files to an internal stage and adds the files to the classpath when executing your UDF.

Tip

If you don’t want the library to upload the file every time you run your application, upload the file to a stage. When calling
`addDependency`, pass the path to the file in the stage.

The following example demonstrates how to add a JAR file in a stage as a dependency:

Copy code

```
// Add a JAR file that you uploaded to a stage.
session.addDependency("@my_stage/<path>/my-library.jar");
```

The following examples demonstrate how to add dependencies for JAR files and resource files:

Copy code

```
// Add a JAR file on your local machine.
session.addDependency("/<path>/my-library.jar");

// Add a directory of resource files.
session.addDependency("/<path>/my-resource-dir/");

// Add a resource file.
session.addDependency("/<path>/my-resource.xml");
```

You should not need to specify the following dependencies:

> - **Your Java runtime libraries.**
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
>      session.addDependency("@mystage/snowpark_2.12-1.18.0.jar.gz");
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
[snowpark\_request\_timeout\_in\_seconds](/developer-guide/snowpark/java/creating-session#label-snowpark-java-request-timeout-in-seconds) property when creating the session.

## Creating an Anonymous UDF

To create an anonymous UDF, you can either:

- Call the `Functions.udf` static method, passing in the lambda expression and the [DataTypes](../reference/java/com/snowflake/snowpark_java/types/DataTypes.html) fields (or objects
  constructed by the methods of that class) representing the data types of the inputs and output.
- Call the `registerTemporary` method in the `UDFRegistration` class, passing in the lambda expression and the
  [DataTypes](../reference/java/com/snowflake/snowpark_java/types/DataTypes.html) fields (or objects constructed by the methods of that class) representing the data types of the inputs and output.

  You can access an instance of the `UDFRegistration` class by calling the `udf` method of the `Session` object.

  When calling `registerTemporary`, use a method signature that does not have a `name` parameter. (Because you are
  creating an anonymous UDF, you do not specify a name for the UDF.)

Note

When writing multi-threaded code (e.g. when using parallel collections), use the `registerTemporary` method to register
UDFs, rather than using the `udf` method. This can prevent errors in which the default Snowflake `Session` object
cannot be found.

These methods return a `UserDefinedFunction` object, which you can use to call the UDF. (See
[Calling scalar user-defined functions (UDFs)](/developer-guide/snowpark/java/calling-functions#label-snowpark-java-udfs-calling).)

The following example creates an anonymous UDF:

Copy code

```
import com.snowflake.snowpark_java.types.*;
...

// Create and register an anonymous UDF
// that takes in an integer argument and returns an integer value.
UserDefinedFunction doubleUdf =
  Functions.udf((Integer x) -> x + x, DataTypes.IntegerType, DataTypes.IntegerType);
// Call the anonymous UDF, passing in the "quantity" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleQuantity".
DataFrame df = session.table("sample_product_data");
DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", doubleUdf.apply(Functions.col("quantity")));
dfWithDoubleQuantity.show();
```

The following example creates an anonymous UDF that uses a custom class (`LanguageDetector`, which detects the language used
in text). The example calls the anonymous UDF to detect the language in the `text_data` column in a DataFrame and creates a new
DataFrame that includes an additional `lang` column with the language used.

Copy code

```
import com.snowflake.snowpark_java.types.*;

// Import the package for your custom code.
// The custom code in this example detects the language of textual data.
import com.mycompany.LanguageDetector;

// If the custom code is packaged in a JAR file, add that JAR file as
// a dependency.
session.addDependency("$HOME/language-detector.jar");

// Create a detector
LanguageDetector detector = new LanguageDetector();

// Create an anonymous UDF that takes a string of text and returns the language used in that string.
// Note that this captures the detector object created above.
// Assign the UDF to the langUdf variable, which will be used to call the UDF.
UserDefinedFunction langUdf =
  Functions.udf(
    (String s) -> java.util.Optional.ofNullable(detector.detect(s)).orElse("UNKNOWN"),
    DataTypes.StringType,
    DataTypes.StringType);

// Create a new DataFrame that contains an additional "lang" column that contains the language
// detected by the UDF.
DataFrame dfEmailsWithLangCol =
    dfEmails.withColumn("lang", langUdf.apply(Functions.col("text_data")));
```

## Creating and Registering a Named UDF

If you want to call a UDF by name (e.g. by using the `Functions.callUDF` static method) or if you need to use a UDF in
subsequent sessions, you can create and register a named UDF. To do this, use one of the following methods in the
`UDFRegistration` class:

- `registerTemporary`, if you just plan to use the UDF in the current session
- `registerPermanent`, if you plan to use the UDF in subsequent sessions

To access an object of the `UDFRegistration` class, call the `udf` method of the `Session` object.

When calling `registerTemporary` or `registerPermanent` method, pass in the lambda expression and the [DataTypes](../reference/java/com/snowflake/snowpark_java/types/DataTypes.html)
fields (or objects constructed by the methods of that class) representing the data types of the inputs and output.

For example:

Copy code

```
import com.snowflake.snowpark_java.types.*;
...
// Create and register a temporary named UDF
// that takes in an integer argument and returns an integer value.
UserDefinedFunction doubleUdf =
  session
    .udf()
    .registerTemporary(
      "doubleUdf",
      (Integer x) -> x + x,
      DataTypes.IntegerType,
      DataTypes.IntegerType);
// Call the named UDF, passing in the "quantity" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleQuantity".
DataFrame df = session.table("sample_product_data");
DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", Functions.callUDF("doubleUdf", Functions.col("quantity")));
dfWithDoubleQuantity.show();
```

`registerPermanent` creates a UDF that you can use in the current and subsequent sessions. When you call
`registerPermanent`, you must also specify a location in an internal stage location where the JAR files for the UDF and its
dependencies will be uploaded.

Note

`registerPermanent` does not support external stages.

For example:

Copy code

```
import com.snowflake.snowpark_java.types.*;
...

// Create and register a permanent named UDF
// that takes in an integer argument and returns an integer value.
// Specify that the UDF and dependent JAR files should be uploaded to
// the internal stage named mystage.
UserDefinedFunction doubleUdf =
  session
    .udf()
    .registerPermanent(
      "doubleUdf",
      (Integer x) -> x + x,
      DataTypes.IntegerType,
      DataTypes.IntegerType,
      "mystage");
// Call the named UDF, passing in the "quantity" column.
// The example uses withColumn to return a DataFrame containing
// the UDF result in a new column named "doubleQuantity".
DataFrame df = session.table("sample_product_data");
DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", Functions.callUDF("doubleUdf", Functions.col("quantity")));
dfWithDoubleQuantity.show();
```

## Using Objects That Are Not Serializable

When you create a UDF for a lambda expression, the Snowpark library serializes the lambda closure and sends it to the server for
execution.

If an object captured by the lambda closure is not serializable, the Snowpark library throws a
`java.io.NotSerializableException` exception.

Copy code

```
Exception in thread "main" java.io.NotSerializableException: <YourObjectName>
```

If this occurs, you must make the object serializable.

## Writing Initialization Code for a UDF

If your UDF requires initialization code or context, you can provide this through values captured as part of the UDF closure.

The following example uses a separate class to initialize the context needed by two UDFs.

- The first UDF creates a new instance of the class within the lambda, so the initialization is performed every time the UDF is
  invoked.
- The second UDF captures an instance of the class generated in your client program. The context generated on the client is
  serialized and is used by the UDF. Note that the context class must be serializable for this approach to work.

Copy code

```
import com.snowflake.snowpark_java.*;
import com.snowflake.snowpark_java.types.*;
import java.io.Serializable;

// Context needed for a UDF.
class Context {
  double randomInt = Math.random();
}

// Serializable context needed for the UDF.
class SerContext implements Serializable {
  double randomInt = Math.random();
}

class TestUdf {
  public static void main(String[] args) {
    // Create the session.
    Session session = Session.builder().configFile("/<path>/profile.properties").create();
    session.range(1, 10, 2).show();

    // Create a DataFrame with two columns ("c" and "d").
    DataFrame dummy =
      session.createDataFrame(
        new Row[]{
          Row.create(1, 1),
          Row.create(2, 2),
          Row.create(3, 3)
        },
        StructType.create(
          new StructField("c", DataTypes.IntegerType),
          new StructField("d", DataTypes.IntegerType))
        );
    dummy.show();

    // Initialize the context once per invocation.
    UserDefinedFunction udfRepeatedInit =
      Functions.udf(
        (Integer i) -> new Context().randomInt,
        DataTypes.IntegerType,
        DataTypes.DoubleType
      );
    dummy.select(udfRepeatedInit.apply(dummy.col("c"))).show();

    // Initialize the serializable context only once,
    // regardless of the number of times that the UDF is invoked.
    SerContext sC = new SerContext();
    UserDefinedFunction udfOnceInit =
      Functions.udf(
        (Integer i) -> sC.randomInt,
        DataTypes.IntegerType,
        DataTypes.DoubleType
      );
    dummy.select(udfOnceInit.apply(dummy.col("c"))).show();
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
   [Specifying Dependencies for a UDF](#label-snowpark-java-udf-inline-dependencies).

   For example:

   Copy code

   ```
   // Specify that myJar.jar contains files that your UDF depends on.
   session.addDependency("<path>/myJar.jar");
   ```
3. In the UDF, call `Class.forName().getResourceAsStream()` to find the file in the classpath and read the file.

   To avoid adding a dependency on `this`, you can use `Class.forName("com.snowflake.snowpark_java.DataFrame")`
   (rather than `getClass()`) to get the `Class` object.

   For example, to read the `data/hello.txt` file:

   Copy code

   ```
   // Read data/hello.txt from myJar.jar.
   String resourceName = "/data/hello.txt";
   InputStream inputStream = Class.forName("com.snowflake.snowpark_java.DataFrame").getResourceAsStream(resourceName);
   ```

   In this example, the resource name starts with a `/`, which indicates that this is the full path of the file in the JAR file.
   (In this case, the location of the file is not relative to the package of the class.)

> Note
>
> If you don’t expect the content of the file to change between UDF calls, read the file into a static field of your class,
> and read the file only if the field is not set.

The following example defines an object (`UDFCode`) with a function that will be used as a UDF (`readFileFunc`). The function
reads the file `data/hello.txt`, which is expected to contain the string `hello,`. The function prepends this string to the
string passed in as an argument.

Copy code

```
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

// Create a function class that reads a file.
class UDFCode {
  private static String fileContent = null;
  // The code in this block reads the file. To prevent this code from executing each time that the UDF is called,
  // The file content is cached in 'fileContent'.
  public static String readFile() {
    if (fileContent == null) {
      try {
        String resourceName = "/data/hello.txt";
        InputStream inputStream = Class.forName("com.snowflake.snowpark_java.DataFrame")
          .getResourceAsStream(resourceName);
        fileContent = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
      } catch (Exception e) {
        fileContent = "Error while reading file";
      }
    }
    return fileContent;
  }
}
```

The next part of the example registers the function as an anonymous UDF. The example calls the UDF on the `NAME` column in a
DataFrame. The example assumes that the `data/hello.txt` file is packaged in the JAR file `myJar.jar`.

Copy code

```
import com.snowflake.snowpark_java.types.*;

// Add the JAR file as a dependency.
session.addDependency("<path>/myJar.jar");

// Create a new DataFrame with one column (NAME)
// that contains the name "Raymond".
DataFrame myDf = session.sql("select 'Raymond' NAME");

// Register the function that you defined earlier as an anonymous UDF.
UserDefinedFunction readFileUdf = session.udf().registerTemporary(
  (String s) -> UDFCode.readFile() + " : " + s, DataTypes.StringType, DataTypes.StringType);

// Call UDF for the values in the NAME column of the DataFrame.
myDf.withColumn("CONCAT", readFileUdf.apply(Functions.col("NAME"))).show();
```

## Creating User-Defined Table Functions (UDTFs)

To create and register a UDTF in Snowpark, you must:

- [Define a class for the UDTF](#label-snowpark-java-udtf-define-class).
- [Create an instance of that class, and register that instance as a UDTF](#label-snowpark-java-udtf-register).

The next sections describe these steps in more detail.

For information on calling a UDTF, see [Calling a UDTF](#label-snowpark-java-udtf-call).

### Defining the UDTF Class

Define a class that implements one of the `JavaUDTFn` interfaces (e.g. `JavaUDTF0`, `JavaUDTF1`, etc.) in the
[com.snowflake.snowpark\_java.udtf package](../reference/java/com/snowflake/snowpark_java/udtf/package-summary.html), where `n` specifies the number of input arguments for your UDTF. For example,
if your UDTF passes in 2 input arguments, implement the `JavaUDTF2` interface.

In your class, implement the following methods:

- [outputSchema()](#label-snowpark-java-udtf-define-class-output-schema), which returns a `types.StructType` object
  that describes the names and types of the fields in the returned rows (the “schema” of the output).
- [process()](#label-snowpark-java-udtf-define-class-process), which is called once for each row in the
  input partition (see the note below).
- [inputSchema()](#label-snowpark-java-udtf-define-class-input-schema), which returns a `types.StructType` object that
  describes the types of the input parameters.

  If your `process()` method passes in `Map` arguments, you must implement the `inputSchema()` method.
  Otherwise, implementing this method is optional.
- [endPartition()](#label-snowpark-java-udtf-define-class-end-partition), which is called once for each partition after all
  rows have been passed to `process()`.

When a UDTF is called, the rows are grouped into partitions before they are passed to the UDTF:

- If the statement that calls the UDTF specifies the PARTITION clause (explicit partitions), that clause determines how the rows
  are partitioned.
- If the statement does not specify the PARTITION clause (implicit partitions), Snowflake determines how best to partition the
  rows.

For an explanation of partitions, see [Table functions and partitions](/developer-guide/udf/udf-calling-sql#label-udf-java-partitions).

For an example of a UDTF class, see [Example of a UDTF Class](#label-snowpark-java-udtf-define-class-example).

#### Implementing the outputSchema() Method

Implement the `outputSchema()` method to define the names and data types of the fields (the “output schema”) of the rows
returned by the `process()` and `endPartition()` methods.

> Copy code
>
> ```
> public StructType outputSchema()
> ```

In this method, construct and return a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object that contains [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects representing the Snowflake data
type of each field in a returned row. Snowflake supports the following type objects for the output schema for a UDTF:

| SQL Data Type | Java Type | `com.snowflake.snowpark_java.types` Type |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Short` | `ShortType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Integer` | `IntType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Long` | `LongType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.math.BigDecimal` | `DecimalType` |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `java.lang.Float` | `FloatType` |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `java.lang.Double` | `DoubleType` |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `java.lang.String` | `StringType` |
| [BOOLEAN](/sql-reference/data-types-logical) | `java.lang.Boolean` | `BooleanType` |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` | `DateType` |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` | `TimestampType` |
| [BINARY](/sql-reference/data-types-text) | `byte[]` | `BinaryType` |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark\_java.types.Variant](../reference/java/com/snowflake/snowpark_java/types/Variant.html) | `VariantType` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `String[]` | `ArrayType(StringType)` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Variant[]` | `ArrayType(VariantType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `java.util.Map<String, String>` | `MapType(StringType, StringType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `java.util.Map<String, Variant>` | `MapType(StringType, VariantType)` |

Expand

Show lessSee more

For example, if your UDTF returns a row with a single integer field:

> Copy code
>
> ```
> public StructType outputSchema() {
>   return StructType.create(new StructField("C1", DataTypes.IntegerType));
> }
> ```

#### Implementing the process() Method

In your UDTF class, implement the `process()` method:

> Copy code
>
> ```
> Stream<Row> process(A0 arg0, ... A<n> arg<n>)
> ```

where `n` is the number of arguments passed to your UDTF.

The number of arguments in the signature corresponds to the interface that you implemented. For example, if your UDTF passes in 2
input arguments and you are implementing the `JavaUDTF2` interface, the `process()` method has this signature:

> Copy code
>
> ```
> Stream<Row> process(A0 arg0, A1 arg1)
> ```

This method is invoked once for each row in the input partition.

##### Choosing the Types of the Arguments

For the type of each argument in the `process()` method, use the Java type that corresponds to the Snowflake data type of
the argument passed to the UDTF.

Snowflake supports the following data types for the arguments for a UDTF:

| SQL Data Type | Java Data Type | Notes |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | The following types are supported:   - `java.lang.Short` - `java.lang.Integer` - `java.lang.Long` - `java.math.BigDecimal` |  |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `java.lang.Float` |  |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `java.lang.Double` |  |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `java.lang.String` |  |
| [BOOLEAN](/sql-reference/data-types-logical) | `java.lang.Boolean` |  |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` |  |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` |  |
| [BINARY](/sql-reference/data-types-text) | `byte[]` |  |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark\_java.types.Variant](../reference/java/com/snowflake/snowpark_java/types/Variant.html) |  |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `String[]` or `Variant[]` |  |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `Map<String, String>` or `Map<String, Variant>` |  |

Expand

Show lessSee more

Note

If you pass in `java.util.Map` arguments, you must implement the `inputSchema` method to describe the types of those
arguments. See [Implementing the inputSchema() Method](#label-snowpark-java-udtf-define-class-input-schema).

##### Returning Rows

In the `process()` method, build and return a [java.util.stream.Stream](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/stream/Stream.html) of `Row` objects that contain the data to be
returned by the UDTF for the given input values. The fields in the row must use the types that you specified in the
`outputSchema` method. (See [Implementing the outputSchema() Method](#label-snowpark-java-udtf-define-class-output-schema).)

For example, if your UDTF generates rows, construct and return an `Iterable` of `Row` objects for the generated rows:

> Copy code
>
> ```
> import java.util.stream.Stream;
> ...
>
> public Stream<Row> process(Integer start, Integer count) {
>   Stream.Builder<Row> builder = Stream.builder();
>   for (int i = start; i < start + count ; i++) {
>     builder.add(Row.create(i));
>   }
>   return builder.build();
> }
> ```

#### Implementing the inputSchema() Method

If the [process()](#label-snowpark-java-udtf-define-class-process) method passes in a `java.util.Map` argument, you
must implement the `inputSchema()` method to describe the types of the input arguments.

Note

If the `process()` method does not pass in `Map` arguments, you do not need to implement the `inputSchema()`
method.

In this method, construct and return a [StructType](../reference/scala/com/snowflake/snowpark/types/StructType$.html) object that contains [StructField](../reference/scala/com/snowflake/snowpark/types/StructField$.html) objects representing the Snowflake data
type of each argument passed in to the `process()` method. Snowflake supports the following type objects for the input
schema for a UDTF:

| SQL Data Type | Java Type | `com.snowflake.snowpark_java.types` Type |
| --- | --- | --- |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Short` | `ShortType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Integer` | `IntType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.lang.Long` | `LongType` |
| [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) | `java.math.BigDecimal` | `DecimalType` |
| [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | `java.lang.Float` | `FloatType` |
| [DOUBLE](/sql-reference/data-types-numeric#label-data-type-double-precision) | `java.lang.Double` | `DoubleType` |
| [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | `java.lang.String` | `StringType` |
| [BOOLEAN](/sql-reference/data-types-logical) | `java.lang.Boolean` | `BooleanType` |
| [DATE](/sql-reference/data-types-datetime#label-datatypes-date) | `java.sql.Date` | `DateType` |
| [TIMESTAMP](/sql-reference/data-types-datetime#label-datatypes-timestamp) | `java.sql.Timestamp` | `TimestampType` |
| [BINARY](/sql-reference/data-types-text) | `byte[]` | `BinaryType` |
| [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | [com.snowflake.snowpark\_java.types.Variant](../reference/java/com/snowflake/snowpark_java/types/Variant.html) | `VariantType` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `String[]` | `ArrayType(StringType)` |
| [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) | `Variant[]` | `ArrayType(VariantType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `java.util.Map<String, String>` | `MapType(StringType, StringType)` |
| [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | `java.util.Map<String, Variant>` | `MapType(StringType, VariantType)` |

Expand

Show lessSee more

For example, suppose that your `process()` method passes in a `Map<String, String>` argument and a
`Map<String, Variant>` argument:

Copy code

```
import java.util.Map;
import com.snowflake.snowpark_java.*;
import com.snowflake.snowpark_java.types.*;
...

public Stream<Row> process(Map<String, String> stringMap, Map<String, Variant> varMap) {
  ...
}
```

You must implement the `inputSchema()` method to return a `StructType` object that describes the types of these input
arguments:

Copy code

```
import java.util.Map;
import com.snowflake.snowpark_java.types.*;
...

public StructType inputSchema() {
  return StructType.create(
      new StructField(
          "string_map",
          DataTypes.createMapType(DataTypes.StringType, DataTypes.StringType)),
      new StructField(
          "variant_map",
          DataTypes.createMapType(DataTypes.StringType, DataTypes.VariantType)));
}
```

#### Implementing the endPartition() Method

Implement the `endPartition` method and add code that should be executed after all rows in the input partition have been
passed to the `process` method. The `endPartition` method is invoked once for each input partition.

> Copy code
>
> ```
> public Stream<Row> endPartition()
> ```

You can use this method if you need to perform any work after all of the rows in the partition have been processed. For example,
you can:

- Return rows based on state information that you capture in each `process` method call.
- Return rows that are not tied to a specific input row.
- Return rows that summarize the output rows that have been generated by the `process` method.

The fields in the rows that you return must match the types that you specified in the `outputSchema` method. (See
[Implementing the outputSchema() Method](#label-snowpark-java-udtf-define-class-output-schema).)

If you do not need to return additional rows at the end of each partition, return an empty `Stream`. For example:

> Copy code
>
> ```
> public Stream<Row> endPartition() {
>   return Stream.empty();
> }
> ```

Note

While Snowflake supports large partitions with timeouts tuned to process them successfully, especially large partitions can cause
processing to time out (such as when `endPartition` takes too long to complete). Please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need the
timeout threshold adjusted for specific usage scenarios.

#### Example of a UDTF Class

The following is an example of a UDTF class that generates a range of rows.

- Because the UDTF passes in 2 arguments, the class implements `JavaUDTF2`.
- The arguments `start` and `count` specify the starting number for the row and the number of rows to generate.

Copy code

```
import java.util.stream.Stream;
import com.snowflake.snowpark_java.types.*;
import com.snowflake.snowpark_java.udtf.*;

class MyRangeUdtf implements JavaUDTF2<Integer, Integer> {
  public StructType outputSchema() {
    return StructType.create(new StructField("C1", DataTypes.IntegerType));
  }

  // Because the process() method in this example does not pass in Map arguments,
  // implementing the inputSchema() method is optional.
  public StructType inputSchema() {
    return StructType.create(
            new StructField("start_value", DataTypes.IntegerType),
            new StructField("value_count", DataTypes.IntegerType));
  }

  public Stream<Row> endPartition() {
    return Stream.empty();
  }

  public Stream<Row> process(Integer start, Integer count) {
    Stream.Builder<Row> builder = Stream.builder();
    for (int i = start; i < start + count ; i++) {
      builder.add(Row.create(i));
    }
    return builder.build();
  }
}
```

### Registering the UDTF

Next, create an instance of the new class, and register the class by calling one of the [UDTFRegistration](../reference/scala/com/snowflake/snowpark/UDTFRegistration.html) methods. You can
register a [temporary](#label-snowpark-java-udtf-register-name-temporary) or
[permanent UDTF](#label-snowpark-java-udtf-register-name-permanent).

#### Registering a Temporary UDTF

To register a temporary UDTF, call `UDTFRegistration.registerTemporary`:

- If you do not need to call the UDTF by name, you can register an anonymous UDTF by passing in an instance of the class:

  Copy code

  ```
  // Register the MyRangeUdtf class that was defined in the previous example.
  TableFunction tableFunction = session.udtf().registerTemporary(new MyRangeUdtf());
  // Use the returned TableFunction object to call the UDTF.
  session.tableFunction(tableFunction, Functions.lit(10), Functions.lit(5)).show();
  ```
- If you need to call the UDTF by name, pass in a name of the UDTF as well:

  Copy code

  ```
  // Register the MyRangeUdtf class that was defined in the previous example.
  TableFunction tableFunction = session.udtf().registerTemporary("myUdtf", new MyRangeUdtf());
  // Call the UDTF by name.
  session.tableFunction(new TableFunction("myUdtf"), Functions.lit(10), Functions.lit(5)).show();
  ```

#### Registering a Permanent UDTF

If you need to use the UDTF in subsequent sessions, call `UDTFRegistration.registerPermanent` to register a permanent UDTF.

When registering a permanent UDTF, you must specify a stage where the registration method will upload the JAR files for the UDTF
and its dependencies. For example:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> TableFunction tableFunction = session.udtf().registerPermanent("myUdtf", new MyRangeUdtf(), "@myStage");
> // Call the UDTF by name.
> session.tableFunction(new TableFunction("myUdtf"), Functions.lit(10), Functions.lit(5)).show();
> ```

### Calling a UDTF

After registering the UDTF, you can call the UDTF by passing the returned `TableFunction` object to the
`tableFunction` method of the `Session` object:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> TableFunction tableFunction = session.udtf().registerTemporary(new MyRangeUdtf());
> // Use the returned TableFunction object to call the UDTF.
> session.tableFunction(tableFunction, Functions.lit(10), Functions.lit(5)).show();
> ```

To call a UDTF by name, construct a `TableFunction` object with that name, and pass that to the `tableFunction`
method:

> Copy code
>
> ```
> // Register the MyRangeUdtf class that was defined in the previous example.
> TableFunction tableFunction = session.udtf().registerTemporary("myUdtf", new MyRangeUdtf());
> // Call the UDTF by name.
> session.tableFunction(new TableFunction("myUdtf"), Functions.lit(10), Functions.lit(5)).show();
> ```

You can also call a UDTF through a SELECT statement directly:

> Copy code
>
> ```
> session.sql("select * from table(myUdtf(10, 5))");
> ```
