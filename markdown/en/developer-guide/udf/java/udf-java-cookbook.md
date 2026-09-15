# Java UDF handler examples

This topic includes simple examples of UDF handler code written in Java.

For more on using Java to create a UDF handler, see [Creating a Java UDF handler](/developer-guide/udf/java/udf-java-creating).

## Creating and calling a simple in-line Java UDF

The following statements create and call an in-line Java UDF. This code returns the VARCHAR passed to it.

This function is declared with the optional `CALLED ON NULL INPUT` clause to indicate that the function is
called even if the value of the input is NULL. (This function would return NULL with or without this clause, but
you could modify the code to handle NULL another way, for example, to return an empty string.)

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE JAVA
  CALLED ON NULL INPUT
  HANDLER = 'TestFunc.echoVarchar'
  TARGET_PATH = '@~/testfunc.jar'
  AS
  'class TestFunc {
    public static String echoVarchar(String x) {
      return x;
    }
  }';
```

Call the UDF:

Copy code

```
SELECT echo_varchar('Hello');
+-----------------------+
| ECHO_VARCHAR('HELLO') |
|-----------------------|
| Hello                 |
+-----------------------+
```

### Passing a NULL to an in-line Java UDF

This uses the `echo_varchar()` UDF defined above. The SQL `NULL` value is implicitly converted to
Java `null`, and that Java `null` is returned and implicitly converted back to SQL `NULL`:

Call the UDF:

Copy code

```
SELECT echo_varchar(NULL);
+--------------------+
| ECHO_VARCHAR(NULL) |
|--------------------|
| NULL               |
+--------------------+
```

## Passing array values

Java methods can receive SQL arrays in either of two ways:

- Using Java’s array feature.
- Using Java’s *varargs* (variable number of arguments) feature.

In both cases, your SQL code must pass an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array).

Note

Be sure to use Java types with valid mappings to SQL types. For more information, refer to [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).

### Passing via an ARRAY

Declare the Java parameter as an array. For example, the third parameter in the following method is a String array:

Copy code

```
static int myMethod(int fixedArgument1, int fixedArgument2, String[] stringArray)
```

Below is a complete example:

Create and load the table:

Copy code

```
CREATE TABLE string_array_table(id INTEGER, a ARRAY);
INSERT INTO string_array_table (id, a) SELECT
        1, ARRAY_CONSTRUCT('Hello');
INSERT INTO string_array_table (id, a) SELECT
        2, ARRAY_CONSTRUCT('Hello', 'Jay');
INSERT INTO string_array_table (id, a) SELECT
        3, ARRAY_CONSTRUCT('Hello', 'Jay', 'Smith');
```

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION concat_varchar_2(a ARRAY)
  RETURNS VARCHAR
  LANGUAGE JAVA
  HANDLER = 'TestFunc_2.concatVarchar2'
  TARGET_PATH = '@~/TestFunc_2.jar'
  AS
  $$
  class TestFunc_2 {
      public static String concatVarchar2(String[] strings) {
          return String.join(" ", strings);
      }
  }
  $$;
```

Call the UDF:

Copy code

```
SELECT concat_varchar_2(a)
  FROM string_array_table
  ORDER BY id;
+---------------------+
| CONCAT_VARCHAR_2(A) |
|---------------------|
| Hello               |
| Hello Jay           |
| Hello Jay Smith     |
+---------------------+
```

### Passing via varargs

Using varargs is very similar to using an array.

In your Java code, use Java’s varargs declaration style:

Copy code

```
static int myMethod(int fixedArgument1, int fixedArgument2, String ... stringArray)
```

Below is a complete example. The only significant difference between this example and the preceding example (for arrays) is the
declaration of the parameters to the method.

Create and load the table:

Copy code

```
CREATE TABLE string_array_table(id INTEGER, a ARRAY);
INSERT INTO string_array_table (id, a) SELECT
        1, ARRAY_CONSTRUCT('Hello');
INSERT INTO string_array_table (id, a) SELECT
        2, ARRAY_CONSTRUCT('Hello', 'Jay');
INSERT INTO string_array_table (id, a) SELECT
        3, ARRAY_CONSTRUCT('Hello', 'Jay', 'Smith');
```

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION concat_varchar(a ARRAY)
  RETURNS VARCHAR
  LANGUAGE JAVA
  HANDLER = 'TestFunc.concatVarchar'
  TARGET_PATH = '@~/TestFunc.jar'
  AS
  $$
  class TestFunc {
      public static String concatVarchar(String ... stringArray) {
          return String.join(" ", stringArray);
      }
  }
  $$;
```

Call the UDF:

Copy code

```
SELECT concat_varchar(a)
    FROM string_array_table
    ORDER BY id;
+-------------------+
| CONCAT_VARCHAR(A) |
|-------------------|
| Hello             |
| Hello Jay         |
| Hello Jay Smith   |
+-------------------+
```

## Returning NULL explicitly from an in-line UDF

The following code shows how to return a NULL value explicitly. The Java value `null` is converted to
SQL `NULL`.

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION return_a_null()
  RETURNS VARCHAR
  NULL
  LANGUAGE JAVA
  HANDLER = 'TemporaryTestLibrary.returnNull'
  TARGET_PATH = '@~/TemporaryTestLibrary.jar'
  AS
  $$
  class TemporaryTestLibrary {
    public static String returnNull() {
      return null;
    }
  }
  $$;
```

Call the UDF:

Copy code

```
SELECT return_a_null();
+-----------------+
| RETURN_A_NULL() |
|-----------------|
| NULL            |
+-----------------+
```

## Passing an OBJECT to an in-line Java UDF

The following example uses the SQL [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) data type and the corresponding Java
data type (`Map<String, String>`), and extracts a value from the OBJECT. This example also shows that you
can pass multiple parameters to a Java UDF.

Create and load a table that contains a column of type OBJECT:

Copy code

```
CREATE TABLE objectives (o OBJECT);
INSERT INTO objectives SELECT PARSE_JSON('{"outer_key" : {"inner_key" : "inner_value"} }');
```

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION extract_from_object(x OBJECT, key VARCHAR)
  RETURNS VARIANT
  LANGUAGE JAVA
  HANDLER = 'VariantLibrary.extract'
  TARGET_PATH = '@~/VariantLibrary.jar'
  AS
  $$
  import java.util.Map;
  class VariantLibrary {
    public static String extract(Map<String, String> m, String key) {
      return m.get(key);
    }
  }
  $$;
```

Call the UDF:

Copy code

```
SELECT extract_from_object(o, 'outer_key'),
       extract_from_object(o, 'outer_key')['inner_key'] FROM objectives;
+-------------------------------------+--------------------------------------------------+
| EXTRACT_FROM_OBJECT(O, 'OUTER_KEY') | EXTRACT_FROM_OBJECT(O, 'OUTER_KEY')['INNER_KEY'] |
|-------------------------------------+--------------------------------------------------|
| {                                   | "inner_value"                                    |
|   "inner_key": "inner_value"        |                                                  |
| }                                   |                                                  |
+-------------------------------------+--------------------------------------------------+
```

## Passing a GEOGRAPHY value to an in-line Java UDF

The following example uses the SQL [GEOGRAPHY](/sql-reference/data-types-geospatial) data type.

Create the UDF:

Copy code

```
CREATE OR REPLACE FUNCTION geography_equals(x GEOGRAPHY, y GEOGRAPHY)
  RETURNS BOOLEAN
  LANGUAGE JAVA
  PACKAGES = ('com.snowflake:snowpark:1.2.0')
  HANDLER = 'TestGeography.compute'
  AS
  $$
  import com.snowflake.snowpark_java.types.Geography;

  class TestGeography {
    public static boolean compute(Geography geo1, Geography geo2) {
      return geo1.equals(geo2);
    }
  }
  $$;
```

You can use the PACKAGES clause to specify a Snowflake system package such as
the [Snowpark package](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html).
When you do, you don’t need to also include the Snowpark JAR file as a value of an IMPORTS clause. For more on PACKAGES, see
[CREATE FUNCTION optional parameters](/sql-reference/sql/create-function#label-create-function-optional-parameters).

Create data and call the UDF with that data:

Copy code

```
CREATE TABLE geocache_table (id INTEGER, g1 GEOGRAPHY, g2 GEOGRAPHY);

INSERT INTO geocache_table (id, g1, g2)
  SELECT 1, TO_GEOGRAPHY('POINT(-122.35 37.55)'), TO_GEOGRAPHY('POINT(-122.35 37.55)');
INSERT INTO geocache_table (id, g1, g2)
  SELECT 2, TO_GEOGRAPHY('POINT(-122.35 37.55)'), TO_GEOGRAPHY('POINT(90.0 45.0)');

SELECT id, g1, g2, geography_equals(g1, g2) AS "EQUAL?"
  FROM geocache_table
  ORDER BY id;
```

The output looks similar to:

```
+----+--------------------------------------------------------+---------------------------------------------------------+--------+
| ID | G1                                                     | G2                                                      | EQUAL? |
+----+--------------------------------------------------------|---------------------------------------------------------+--------+
| 1  | { "coordinates": [ -122.35, 37.55 ], "type": "Point" } | { "coordinates": [ -122.35,  37.55 ], "type": "Point" } | TRUE   |
| 2  | { "coordinates": [ -122.35, 37.55 ], "type": "Point" } | { "coordinates": [   90.0,   45.0  ], "type": "Point" } | FALSE  |
+----+--------------------------------------------------------+---------------------------------------------------------+--------+
```

## Passing a VARIANT value to an in-line Java UDF

When you pass a value of the SQL [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) type to a Java UDF, Snowflake can convert the value to the
[Variant](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/com/snowflake/snowpark_java/types/Variant.html) type
provided with the [Snowpark package](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html). Note that
`Variant` is supported from the Snowpark package version 1.4.0 and later.

The Snowpark `Variant` type provides methods for converting values between `Variant` and other types.

To use the Snowpark `Variant` type, use the PACKAGES clause to specify the Snowpark package when creating the UDF. When you do, you
don’t need to also include the Snowpark JAR file as a value of an IMPORTS clause. For more information on PACKAGES, see
[CREATE FUNCTION optional parameters](/sql-reference/sql/create-function#label-create-function-optional-parameters).

Code in the following example receives JSON data stored as the VARIANT type, then uses the `Variant` type in the Snowpark library
to retrieve the `price` value from the JSON. The received JSON has a structure similar to the JSON displayed in
[Sample Data Used in Examples](/user-guide/querying-semistructured#label-sample-data-semistructured-data).

Copy code

```
CREATE OR REPLACE FUNCTION retrieve_price(v VARIANT)
  RETURNS INTEGER
  LANGUAGE JAVA
  PACKAGES = ('com.snowflake:snowpark:1.4.0')
  HANDLER = 'VariantTest.retrievePrice'
  AS
  $$
  import java.util.Map;
  import com.snowflake.snowpark_java.types.Variant;

  public class VariantTest {
    public static Integer retrievePrice(Variant v) throws Exception {
      Map<String, Variant> saleMap = v.asMap();
      int price = saleMap.get("vehicle").asMap().get("price").asInt();
      return price;
    }
  }
  $$;
```

## Reading a file with a Java UDF

You can read the contents of a file with handler code. For example, you might want to read a file to process unstructured data with the
handler. For more information on processing unstructured data, along with example code, refer to [Process unstructured data with UDF and procedure handlers](/user-guide/unstructured-data-java).

The file must be on a Snowflake stage that’s available to your handler.

To read the contents of staged files, your handler can:

- Read a file whose file path is [statically-specified in the IMPORTS clause](#label-reading-file-from-java-udf-imports). At run time,
  your code reads the file from the UDF’s home directory.

  This can be useful when you want to access the file during initialization.
- Read a file from a [directory imported using IMPORTS](#label-java-directory-imports).
- Read a dynamically-specified file by calling methods of either the `SnowflakeFile` class or the `InputStream` class.

  You might do this if you need to access a file specified by the caller. For more information, see the following in this topic:

  - [Reading a dynamically-specified file with](#label-reading-file-from-java-udf-snowflakefile)
  - [Reading a dynamically-specified file with](#label-reading-file-from-java-udf-inputstream)

  `SnowflakeFile` provides features not available with `InputStream`, as described in the following table.

  | Class | Input | Notes |
  | --- | --- | --- |
  | `SnowflakeFile` | URL formats:  - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner. - File URL or string path for files that the UDF owner has access to. The file must be located in a named internal stage or an external stage. | Easily access additional file attributes, such as file size. |
  | `InputStream` | URL formats:  - Scoped URL to reduce the risk of file injection attacks when the function’s caller is not also its owner. The file must be located in an internal or external stage. |  |

  Expand

  Show lessSee more

### Prerequisites

Before your Java handler code can read a file on a stage, you must do the following to make the file available to the code:

1. Create a stage that’s available to your handler.

   You can use an external stage or internal stage. If you use an internal stage, it must be a user or named stage;
   Snowflake does not currently support using a table stage for UDF dependencies. For more on creating a stage, see
   [CREATE STAGE](/sql-reference/sql/create-stage). For more on choosing an internal stage type, see
   [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage).

   Keep in mind that adequate privileges on the stage must be assigned to roles performing SQL actions that read from the stage. For more
   information, see [Granting privileges for user-defined functions](/developer-guide/udf/udf-access-control).
2. To the stage, copy the file that will be read by code.

   You can copy the file from a local drive to a stage by using the PUT command. For command reference, see [PUT](/sql-reference/sql/put).
   For information on staging files with PUT, see [Staging data files from a local file system](/user-guide/data-load-local-file-system-stage).

### Reading a file specified statically in IMPORTS

Your handler can read a file whose stage path has been specified in the IMPORTS clause of the
[CREATE FUNCTION](/sql-reference/sql/create-function) command.

When you specify a file in the IMPORTS clause, Snowflake copies that file from the stage to the UDF’s
*home directory* (also called the *import directory*), which is the directory from which the UDF actually reads the file.

Because imported files are copied to a single directory and must have unique names within that directory, each file in the
IMPORTS clause must have a distinct name, even if the files start out in different stages or different subdirectories within a
stage.

The following example creates and calls a Java UDF that reads a file.

The Java source code below creates a Java method named `readFile`. This UDF uses this method.

Copy code

```
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

class TestReadRelativeFile {
  public static String readFile(String fileName) throws IOException {
    StringBuilder contentBuilder = new StringBuilder();
    String importDirectory = System.getProperty("com.snowflake.import_directory");
    String fPath = importDirectory + fileName;
    Stream<String> stream = Files.lines(Paths.get(fPath), StandardCharsets.UTF_8);
    stream.forEach(s -> contentBuilder.append(s).append("\n"));
    return contentBuilder.toString();
  }
}
```

The following SQL code creates the UDF. This code assumes that the Java source code has been compiled and put into a JAR
file named `TestReadRelativeFile.jar`, which the UDF imports. The second and third imported files,
`my_config_file_1.txt` and `my_config_file_2.txt`, are configuration files that the UDF can read.

Copy code

```
CREATE FUNCTION file_reader(file_name VARCHAR)
  RETURNS VARCHAR
  LANGUAGE JAVA
  IMPORTS = ('@my_stage/my_package/TestReadRelativeFile.jar',
             '@my_stage/my_path/my_config_file_1.txt',
             '@my_stage/my_path/my_config_file_2.txt')
  HANDLER = 'my_package.TestReadRelativeFile.readFile';
```

This code calls the UDF:

Copy code

```
SELECT file_reader('my_config_file_1.txt') ...;
...
SELECT file_reader('my_config_file_2.txt') ...;
```

#### Choosing whether to access a file in compressed or uncompressed format

Files in a stage can be stored in compressed or uncompressed format. Users can compress the file before copying it
to the stage, or can tell the [PUT](/sql-reference/sql/put) command to compress the file.

When Snowflake copies a file compressed in GZIP format from a stage to the UDF home directory, Snowflake can write the copy as-is, or
Snowflake can decompress the content before writing the file.

If the file in the stage is compressed, and if you would like the copy in the UDF home directory to also be compressed, then when
you specify the file name in the IMPORTS clause, simply use the original file name (e.g. “MyData.txt.gz”) in the IMPORTS
clause. For example:

Copy code

```
... IMPORTS = ('@MyStage/MyData.txt.gz', ...)
```

If the file in the stage is GZIP-compressed, but you would like the copy in the UDF home directory to be uncompressed, then when you
specify the file name in the IMPORTS clause, omit the “.gz” extension. For example, if your stage contains “MyData.txt.gz”, but you
want your UDF to read the file in uncompressed format, then specify “MyData.txt” in the IMPORTS clause. If there is not already an
uncompressed file named “MyData.txt”, then Snowflake searches for “MyData.txt.gz” and automatically writes a decompressed copy to
“MyData.txt” in the UDF home directory. Your UDF can then open and read the uncompressed file “MyData.txt”.

Note that smart decompression applies only to the copy in the UDF home directory; the original file in the stage is not changed.

Follow these best practices for handling compressed files:

- Follow proper file naming conventions. If a file is in GZIP-compressed format, then include the extension “.gz” at the end of the file
  name. If a file is not in GZIP-compressed format, then do not end the file name with the “.gz” extension.
- Avoid creating files whose names differ only by the extension “.gz”. For example, do not create both “MyData.txt” and “MyData.txt.gz”
  in the same stage and directory, and do not try to import both “MyData.txt” and “MyData.txt.gz” in the same CREATE FUNCTION command.
- Do not compress files twice. For example, if you compress a file manually, and then you PUT that file without using
  AUTO\_COMPRESS=FALSE, the file will be compressed a second time. Smart decompression will decompress it only once, so the data
  (or JAR) file will still be compressed when it is stored in the UDF home directory.
- In the future, Snowflake might extend smart decompression to compression algorithms other than GZIP. To prevent compatibility issues
  in the future, apply these best practices to files that use any type of compression.

Note

JAR files can also be stored in compressed or uncompressed format in a stage. Snowflake automatically decompresses all compressed
JAR files before making them available to the Java UDF.

### Importing a directory using IMPORTS

You can import a directory using the IMPORTS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) command.

Note

- The import path for a directory must end with a trailing slash (`/`). For example, `IMPORTS = ('@my_stage/my_dir/')`.
- To rename a directory on import, append `/=custom_name/` to the stage path. The custom name must be a single directory name, not a path. For example, `IMPORTS = ('@my_stage/my_dir/=custom_name/')`.
- Directory imports are not supported in Native Apps.

The following example imports a directory called `my_dir` from a stage named `my_stage` and reads the files contained within it.

Copy code

```
CREATE OR REPLACE FUNCTION test_java_udf(fileName STRING)
  RETURNS STRING
  LANGUAGE JAVA
  IMPORTS = ('@my_stage/my_dir/')
  HANDLER = 'TestClass.readFile'
  AS
  $$
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Stream;

class TestClass {
  public static String readFile(String fileName) throws IOException {
    StringBuilder contentBuilder = new StringBuilder();
    String importDirectory = System.getProperty("com.snowflake.import_directory") + "my_dir/";
    String fPath = importDirectory + fileName;
    Stream<String> stream = Files.lines(Paths.get(fPath), StandardCharsets.UTF_8);
    stream.forEach(s -> contentBuilder.append(s).append("\n"));
    return contentBuilder.toString();
  }
}
$$;
SELECT test_java_udf('file.txt');
```

### Reading a dynamically-specified file with `SnowflakeFile`

Using methods of the `SnowflakeFile` class, you can read files from a stage with your Java handler code. The `SnowflakeFile`
class is included on the classpath available to Java UDF handlers on Snowflake.

Note

To make your code resilient to file injection attacks, always use a scoped URL when passing a file’s location to a UDF, particularly
when the function’s caller is not also its owner. You can create a scoped URL in SQL using the built-in function
[BUILD\_SCOPED\_FILE\_URL](/sql-reference/functions/build_scoped_file_url). For more information about what the BUILD\_SCOPED\_FILE\_URL does, see
[Introduction to unstructured data](/user-guide/unstructured-intro).

To develop your UDF code locally, add the Snowpark JAR containing `SnowflakeFile` to your code’s class path. For information about
`snowpark.jar`, see [Setting Up Your Development Environment for Snowpark Java](/developer-guide/snowpark/java/setup). Note that Snowpark client applications cannot use this class.

When you use `SnowflakeFile`, it isn’t necessary to also specify either the staged file or the JAR containing
`SnowflakeFile` with an IMPORTS clause when you create the UDF, as in SQL with a CREATE FUNCTION statement.

Code in the following example uses `SnowflakeFile` to read a file from a specified stage location. Using an
`InputStream` from the `getInputStream` method, it reads the file’s contents into a `String` variable.

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales(file STRING)
  RETURNS INTEGER
  LANGUAGE JAVA
  HANDLER = 'SalesSum.sumTotalSales'
  TARGET_PATH = '@jar_stage/sales_functions2.jar'
  AS
  $$
  import java.io.InputStream;
  import java.io.IOException;
  import java.nio.charset.StandardCharsets;
  import com.snowflake.snowpark_java.types.SnowflakeFile;

  public class SalesSum {

    public static int sumTotalSales(String filePath) throws IOException {
      int total = -1;

      // Use a SnowflakeFile instance to read sales data from a stage.
      SnowflakeFile file = SnowflakeFile.newInstance(filePath);
      InputStream stream = file.getInputStream();
      String contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8);

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total;
    }
  }
  $$;
```

Call the UDF, passing the location of the file in a scoped URL to reduce the likelihood of file injection attacks.

Copy code

```
SELECT sum_total_sales(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```

Note

The UDF owner must have access to any files whose locations are not scoped URLs. You can read these staged files by having the handler
code call the `SnowflakeFile.newInstance` method with a `boolean` value for a new `requireScopedUrl` parameter.

The following example uses `SnowflakeFile.newInstance` while specifying that a scoped URL is not required.

Copy code

```
String filename = "@my_stage/filename.txt";
String sfFile = SnowflakeFile.newInstance(filename, false);
```

### Reading a dynamically-specified file with `InputStream`

You can read file contents directly into a `java.io.InputStream` by making your handler function’s argument an `InputStream`
variable. This can be useful when the function’s caller will want to pass a file path as an argument.

Note

To make your code resilient to file injection attacks, always use a scoped URL when passing a file’s location to a UDF, particularly
when the function’s caller is not also its owner. You can create a scoped URL in SQL using the built-in function
BUILD\_SCOPED\_FILE\_URL. For more information about what the BUILD\_SCOPED\_FILE\_URL does, see
[Introduction to unstructured data](/user-guide/unstructured-intro).

Code in the following example has a handler function `sumTotalSales` that takes an `InputStream` and returns an `int`.
At run time, Snowflake automatically assigns the contents of the file at the `file` variable’s path to the `stream`
argument variable.

Copy code

```
CREATE OR REPLACE FUNCTION sum_total_sales(file STRING)
  RETURNS INTEGER
  LANGUAGE JAVA
  HANDLER = 'SalesSum.sumTotalSales'
  TARGET_PATH = '@jar_stage/sales_functions2.jar'
  AS
  $$
  import java.io.InputStream;
  import java.io.IOException;
  import java.nio.charset.StandardCharsets;

  public class SalesSum {

    public static int sumTotalSales(InputStream stream) throws IOException {
      int total = -1;
      String contents = new String(stream.readAllBytes(), StandardCharsets.UTF_8);

      // Omitted for brevity: code to retrieve sales data from JSON and assign it to the total variable.

      return total;
    }
  }
  $$;
```

Call the UDF, passing the location of the file in a scoped URL to reduce the likelihood of file injection attacks.

Copy code

```
SELECT sum_total_sales(BUILD_SCOPED_FILE_URL('@sales_data_stage', '/car_sales.json'));
```

## Creating and calling a simple staged Java UDF

The following statements create a simple Java UDF. This sample generally follows the file and directory structure
described in [Organizing your files](/developer-guide/udf/java/udf-java-creating#label-udf-java-pre-compiled-organizing-your-files).

### Create and compile the Java handler code

1. In the root directory of your project (here, `my_udf`), create a `src` subdirectory to hold the source .java files and a
   `classes` subdirectory to hold the generated .class files.

   You should have a directory hierarchy similar to the following:

   Copy code

   ```
   my_udf/
   |-- classes/
   |-- src/
   ```
2. In the `src` directory, create a directory called `mypackage` to hold .java files whose classes are in the
   `mypackage` package.
3. In the `mypackage` directory, create a `MyUDFHandler.java` file that contains your source code.

   Copy code

   ```
   package mypackage;

   public class MyUDFHandler {

     public static int decrementValue(int i)
     {
    return i - 1;
     }

     public static void main(String[] argv)
     {
    System.out.println("This main() function won't be called.");
     }
   }
   ```
4. From your project root directory (here, `my_udf`), use the `javac` command to compile the source code.

   The `javac` command in the following example compiles `MyUDFHandler.java` to generate a `MyUDFHandler.class` file in the
   `classes` directory.

   Copy code

   ```
   javac -d classes src/mypackage/MyUDFHandler.java
   ```

   This example includes the following arguments:

   - `-d classes` – Directory into which generated class files should be written.
   - `src/mypackage/MyUDFHandler.java` – Path to the .java file in the form: `source_directory/package_directory/Java_file_name`.

### Package the compiled code into a JAR file

1. Optionally, in the project root directory create a manifest file named `my_udf.manifest` that contains the following attributes:

   Copy code

   ```
   Manifest-Version: 1.0
   Main-Class: mypackage.MyUDFHandler
   ```
2. From your project root directory, run the `jar` command to create a JAR file containing the .class file and manifest.

   The `jar` command in the following example puts the generated `MyUDFHandler.class` file in a `mypackage` package folder
   into a .jar file called `my_udf.jar`. The `-C ./classes` flag specifies the location of the .class files.

   Copy code

   ```
   jar cmf my_udf.manifest my_udf.jar -C ./classes mypackage/MyUDFHandler.class
   ```

   This example includes the following arguments:

   - `cmf` – Command arguments: `c` to create a JAR file, `m` to use the specified .manifest file, and `f` to give the JAR
     file the specified name.
   - `my_udf.manifest` – Manifest file.
   - `my_udf.jar` – Name of the JAR file to create.
   - `-C ./classes` – Directory containing the generated .class files.
   - `mypackage/MyUDFHandler.class` – Package and name of .class file to include in the JAR.

### Upload the JAR file with the compiled handler to a stage

1. In Snowflake, create a stage called `jar_stage` to store the JAR file containing your UDF handler.

   For more information on creating a stage, see [CREATE STAGE](/sql-reference/sql/create-stage).
2. Use the `PUT` command to copy the JAR file from the local file system to a stage.

   Copy code

   ```
   put
    file:///Users/Me/my_udf/my_udf.jar
    @jar_stage
    auto_compress = false
    overwrite = true
    ;
   ```

   You can store the `PUT` command in a script file and then execute that file through [SnowSQL](/user-guide/snowsql).

   The `snowsql` command looks similar to the following:

   Copy code

   ```
   snowsql -a <account_identifier> -w <warehouse> -d <database> -s <schema> -u <user> -f put_command.sql
   ```

   This example assumes that the user’s password is specified in the SNOWSQL\_PWD environment variable.

### Create the UDF with the compiled code as handler

Create the UDF:

Copy code

```
CREATE FUNCTION decrement_value(i NUMERIC(9, 0))
  RETURNS NUMERIC
  LANGUAGE JAVA
  IMPORTS = ('@jar_stage/my_udf.jar')
  HANDLER = 'mypackage.MyUDFHandler.decrementValue'
  ;
```

Call the UDF:

Copy code

```
SELECT decrement_value(-15);
```

```
+----------------------+
| DECREMENT_VALUE(-15) |
|----------------------|
|                  -16 |
+----------------------+
```
