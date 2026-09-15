# Scala UDF handler examples

This topic includes simple examples of UDF handler code written in Scala.

For information on using Scala to create a scalar UDF handler, refer to [Writing a scalar UDF in Scala](/developer-guide/udf/scala/udf-scala-scalar). For general
coding guidelines, refer to [General Scala UDF handler coding guidelines](/developer-guide/udf/scala/udf-scala-general).

## Creating and calling a simple in-line Scala UDF

The following statements create and call an in-line Scala UDF. This code returns the VARCHAR passed to it.

This function is declared with the optional `CALLED ON NULL INPUT` clause to indicate that the function is
called even if the value of the input is NULL. (This function would return NULL with or without this clause, but
you could modify the code to handle NULL another way, for example, to return an empty string.)

### Create the UDF

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  CALLED ON NULL INPUT
  RUNTIME_VERSION = 2.12
  HANDLER='Echo.echoVarchar'
  AS
  $$
  class Echo {
    def echoVarchar(x : String): String = {
      return x
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  CALLED ON NULL INPUT
  RUNTIME_VERSION = 2.13
  HANDLER='Echo.echoVarchar'
  AS
  $$
  class Echo {
    def echoVarchar(x : String): String = {
      return x
    }
  }
  $$;
```

### Call the UDF

Copy code

```
SELECT echo_varchar('Hello');
```

### Passing a NULL to an in-line Scala UDF

This uses the `echo_varchar()` UDF defined above. The SQL `NULL` value is implicitly converted to
Scala [Null](https://www.scala-lang.org/api/2.12.17/scala/Null.html), and that Scala `Null` is returned and implicitly converted
back to SQL `NULL`:

Call the UDF:

Copy code

```
SELECT echo_varchar(NULL);
```

## Returning NULL explicitly from an in-line UDF

The following code shows how to return a NULL value explicitly. The Scala value `Null` is converted to
SQL `NULL`.

### Create the UDF

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION return_a_null()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER='TemporaryTestLibrary.returnNull'
  AS
  $$
  class TemporaryTestLibrary {
    def returnNull(): String = {
      return null
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION return_a_null()
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  HANDLER='TemporaryTestLibrary.returnNull'
  AS
  $$
  class TemporaryTestLibrary {
    def returnNull(): String = {
      return null
    }
  }
  $$;
```

### Call the UDF

Copy code

```
SELECT return_a_null();
```

## Passing an OBJECT to an in-line Scala UDF

The following example uses the SQL [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) data type and the corresponding Scala
data type (`Map[String, String]`), and extracts a value from the OBJECT. This example also shows that you
can pass multiple parameters to a Scala UDF.

Create and load a table that contains a column of type OBJECT:

Copy code

```
CREATE TABLE objectives (o OBJECT);
INSERT INTO objectives SELECT PARSE_JSON('{"outer_key" : {"inner_key" : "inner_value"} }');
```

### Create the UDF

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION extract_from_object(x OBJECT, key VARCHAR)
  RETURNS VARIANT
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER='VariantLibrary.extract'
  AS
  $$
  import scala.collection.immutable.Map

  class VariantLibrary {
    def extract(m: Map[String, String], key: String): String = {
      return m(key)
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION extract_from_object(x OBJECT, key VARCHAR)
  RETURNS VARIANT
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  HANDLER='VariantLibrary.extract'
  AS
  $$
  import scala.collection.immutable.Map

  class VariantLibrary {
    def extract(m: Map[String, String], key: String): String = {
      return m(key)
    }
  }
  $$;
```

### Call the UDF

Copy code

```
SELECT extract_from_object(o, 'outer_key'),
  extract_from_object(o, 'outer_key')['inner_key'] FROM OBJECTIVES;
```

## Passing an ARRAY to an in-line Scala UDF

The following example uses the SQL [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) data type.

### Create the UDF

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION generate_greeting(greeting_words ARRAY)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER='StringHandler.handleStrings'
  AS
  $$
  class StringHandler {
    def handleStrings(strings: Array[String]): String = {
      return concatenate(strings)
    }
    private def concatenate(strings: Array[String]): String = {
      var concatenated : String = ""
      for (newString <- strings)  {
          concatenated = concatenated + " " + newString
      }
      return concatenated
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION generate_greeting(greeting_words ARRAY)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  HANDLER='StringHandler.handleStrings'
  AS
  $$
  class StringHandler {
    def handleStrings(strings: Array[String]): String = {
      return concatenate(strings)
    }
    private def concatenate(strings: Array[String]): String = {
      var concatenated : String = ""
      for (newString <- strings)  {
          concatenated = concatenated + " " + newString
      }
      return concatenated
    }
  }
  $$;
```

## Reading a file with a Scala UDF

You can read the contents of a file or directory with handler code. For example, you might want to read a file to process unstructured data with the
handler.

The file must be on a Snowflake stage that’s available to your handler.

To read the contents of staged files, your handler can:

- Read a file from a [directory imported using IMPORTS](#label-scala-directory-imports).
- Read a dynamically-specified file by calling methods of either the
  `SnowflakeFile` class or the `InputStream` class.

  You might do this if you need to access a file specified by the caller. For more information, see the following in this topic:

  - [Reading a dynamically-specified file with](#label-reading-file-from-scala-udf-snowflakefile)
  - [Reading a dynamically-specified file with](#label-reading-file-from-scala-udf-inputstream)

`SnowflakeFile` provides features not available with `InputStream`, as described in the following table.

| Class | Input | Notes |
| --- | --- | --- |
| `SnowflakeFile` | URL formats:   - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner. - File URL or string path for files that the UDF owner has access to.   The file must be located in a named internal stage or an external stage. | Easily access additional file attributes, such as file size. |
| `InputStream` | URL formats:   - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner.   The file must be located in a named internal stage or an external stage. |  |

Expand

Show lessSee more

Note

The UDF owner must have access to any files whose locations are not scoped URLs. You can read these staged files by having the handler
code call the `SnowflakeFile.newInstance` method with a `boolean` value for a new `requireScopedUrl` parameter.

The following example uses `SnowflakeFile.newInstance` while specifying that a scoped URL is not required.

Copy code

```
var filename = "@my_stage/filename.txt"
var sfFile = SnowflakeFile.newInstance(filename, false)
```

### Importing a directory using IMPORTS

You can import a directory using the IMPORTS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command.

Note

- The import path for a directory must end with a trailing slash (`/`). For example, `IMPORTS = ('@my_stage/my_dir/')`.
- To rename a directory on import, append `/=custom_name/` to the stage path. The custom name must be a single directory name, not a path. For example, `IMPORTS = ('@my_stage/my_dir/=custom_name/')`.
- Directory imports are not supported in Native Apps.

The following example imports a directory called `my_dir` from a stage named `my_stage` and reads the files contained within it.

Copy code

```
CREATE OR REPLACE FUNCTION scala_udf(fileName STRING)
  RETURNS STRING
LANGUAGE SCALA
RUNTIME_VERSION = '2.12'
IMPORTS = ('@my_stage/my_dir/')
HANDLER = 'FileReader.compute'
AS $$
import java.io._
import java.nio.file.{Paths, Files}
import scala.io.Source

class FileReader {
  def compute(fileName: String): String = {
    // Get the base import directory
    val importDir = System.getProperty("com.snowflake.import_directory")

    // Construct the path
    val filePath = Paths.get(importDir, "/", "my_dir", "/", fileName)

    // Read the file using Scala Source
    if (Files.exists(filePath)) {
      val source = Source.fromFile(filePath.toFile)
      try {
        source.getLines().mkString("\n")
      } finally {
        source.close()
      }
    } else {
      s"File not found: $fileName"
    }
  }
}
$$;
SELECT scala_udf('file.txt');
```

### Reading a dynamically-specified file with `SnowflakeFile`

Using methods of the `SnowflakeFile` class, you can read files from a stage with your handler code. The `SnowflakeFile`
class is included on the classpath available to Scala UDF handlers on Snowflake.

Note

To make your code resilient to file injection attacks, always use a scoped URL when passing a file’s location to a UDF, particularly
when the function’s caller is not also its owner. You can create a scoped URL in SQL using the built-in function
[BUILD\_SCOPED\_FILE\_URL](/sql-reference/functions/build_scoped_file_url). For more information about what the BUILD\_SCOPED\_FILE\_URL does, see
[Introduction to unstructured data](/user-guide/unstructured-intro).

To develop your UDF code locally, add the Snowpark JAR containing `SnowflakeFile` to your code’s class path. For information about
`snowpark.jar`, see [Setting Up Your Development Environment for Snowpark Scala](/developer-guide/snowpark/scala/setup). Note that Snowpark client applications cannot use this class.

When you use `SnowflakeFile`, it isn’t necessary to also specify either the staged file or the JAR containing
`SnowflakeFile` with an IMPORTS clause when you create the UDF, as in SQL with a CREATE FUNCTION statement.

### Create the UDF

Code in the following example uses `SnowflakeFile` to read a file from a specified stage location. Using an
`InputStream` from the `getInputStream` method, it reads the file’s contents into a `String` variable.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales_snowflake_file(file STRING)
  RETURNS INTEGER
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES=('com.snowflake:snowpark_2.12:latest')
  HANDLER='SalesSum.sumTotalSales'
  AS
  $$
  import java.io.InputStream
  import java.io.IOException
  import java.nio.charset.StandardCharsets
  import com.snowflake.snowpark_java.types.SnowflakeFile

  object SalesSum {
    @throws(classOf[IOException])
    def sumTotalSales(filePath: String): Int = {
      var total = -1

      // Use a SnowflakeFile instance to read sales data from a stage.
      val file = SnowflakeFile.newInstance(filePath)
      val stream = file.getInputStream()
      val contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8)

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales_snowflake_file(file STRING)
  RETURNS INTEGER
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES=('com.snowflake:snowpark_2.13:latest')
  HANDLER='SalesSum.sumTotalSales'
  AS
  $$
  import java.io.InputStream
  import java.io.IOException
  import java.nio.charset.StandardCharsets
  import com.snowflake.snowpark_java.types.SnowflakeFile

  object SalesSum {
    @throws(classOf[IOException])
    def sumTotalSales(filePath: String): Int = {
      var total = -1

      // Use a SnowflakeFile instance to read sales data from a stage.
      val file = SnowflakeFile.newInstance(filePath)
      val stream = file.getInputStream()
      val contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8)

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total
    }
  }
  $$;
```

### Call the UDF

Copy code

```
SELECT sum_total_sales_input_stream(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```

### Reading a dynamically-specified file with `InputStream`

You can read file contents directly into a `java.io.InputStream` by making your handler function’s argument an `InputStream`
variable. This can be useful when the function’s caller will want to pass a file path as an argument.

Note

To make your code resilient to file injection attacks scoped URLs are required when passing a file’s location to a UDF. You can create a
scoped URL in SQL using the built-in function BUILD\_SCOPED\_FILE\_URL. For more information about what the BUILD\_SCOPED\_FILE\_URL does,
see [Introduction to unstructured data](/user-guide/unstructured-intro).

### Create the UDF

Code in the following example has a handler function `sumTotalSales` that takes an `InputStream` and returns an `Int`.
At run time, Snowflake automatically assigns the contents of the file at the `file` variable’s path to the `stream`
argument variable.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales_input_stream(file STRING)
  RETURNS NUMBER
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER = 'SalesSum.sumTotalSales'
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  AS $$
  import com.snowflake.snowpark.types.Variant
  import java.io.InputStream
  import java.io.IOException
  import java.nio.charset.StandardCharsets
  object SalesSum {
    @throws(classOf[IOException])
    def sumTotalSales(stream: InputStream): Int = {
      val total = -1
      val contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8)

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales_input_stream(file STRING)
  RETURNS NUMBER
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  HANDLER = 'SalesSum.sumTotalSales'
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  AS $$
  import com.snowflake.snowpark.types.Variant
  import java.io.InputStream
  import java.io.IOException
  import java.nio.charset.StandardCharsets
  object SalesSum {
    @throws(classOf[IOException])
    def sumTotalSales(stream: InputStream): Int = {
      val total = -1
      val contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8)

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total
    }
  }
  $$;
```

### Call the UDF

Copy code

```
SELECT sum_total_sales_input_stream(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```
