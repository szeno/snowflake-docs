# Analyzing queries and troubleshooting with Snowpark Java

This topic provides some guidelines on analyzing queries and troubleshooting problems when working with the Snowpark library.

## Viewing the execution plan for a query in Snowpark

To inspect the evaluation plan of a DataFrame, call the `explain` method of the DataFrame. This prints the SQL statements
used to evaluate the DataFrame. If there is only one SQL statement, the method also prints the logical plan for the statement.

Copy code

```
----------DATAFRAME EXECUTION PLAN----------
Query List:
0.
SELECT
  "_1" AS "col %",
  "_2" AS "col *"
FROM
  (
    SELECT
      *
    FROM
      (
        VALUES
          (1 :: int, 2 :: int),
          (3 :: int, 4 :: int) AS SN_TEMP_OBJECT_639016133("_1", "_2")
      )
  )
Logical Execution Plan:
 GlobalStats:
    partitionsTotal=0
    partitionsAssigned=0
    bytesAssigned=0
Operations:
1:0     ->Result  SN_TEMP_OBJECT_639016133.COLUMN1, SN_TEMP_OBJECT_639016133.COLUMN2
1:1          ->ValuesClause  (1, 2), (3, 4)

--------------------------------------------
```

After the execution of a DataFrame has been triggered, you can check on the progress of the query in the **Query History**
page in Snowsight.

In the **Query Tag** column, you can find the name of the function and the line number in your code that triggered this query.

> ![Snowpark request in the Query History page](/static/images/query-tag-snowpark.png)

## Changing the logging settings

By default, the Snowpark library logs `INFO` level messages to stdout. To change the logging settings, create a
`simplelogger.properties` file, and configure the logger properties in that file. For example, to set the log level to
`DEBUG`:

Copy code

```
# simplelogger.properties file (a text file)
# Set the default log level for the SimpleLogger to DEBUG.
org.slf4j.simpleLogger.defaultLogLevel=debug
```

Put this file in your classpath. If you are using a Maven directory layout, put the file in the `src/main/resources/`
directory.

## java.lang.OutOfMemoryError exceptions

If a `java.lang.OutOfMemoryError` exception is thrown, increase the maximum heap size for the JVM (e.g. through the
`-J-Xmxmaximum_size` flag).

## Unnamed module error on Java 17

When executing a Snowpark Java or Scala client on Java 17, you might see the following error:

```
java.base does not "opens java.nio" to unnamed module
```

This is because Snowpark uses the [Apache Arrow connector](https://arrow.apache.org/docs/java/install.html#id3), which depends on
internal Java APIs that are not exposed by default after Java 9.

To work around this error, set the following parameter either as a command-line argument when running your application or in your
system’s environment variables.

Copy code

```
--add-opens=java.base/java.nio=ALL-UNNAMED
```

Note

The Snowpark API supports the following versions of Java:

- 11.x
- 17.x
- 21.x

### Setting the argument when running the application

You can set this argument from the command line when running your application.

For example, when calling the `java` command, you can add `--add-opens=java.base/java.nio=ALL-UNNAMED`, as in the following:

Copy code

```
java --add-opens=java.base/java.nio=ALL-UNNAMED -jar my-snowpark-app.jar.
```

If you are also using RSA private key authentication, you will also need to allow `sun.security.util`, as in the following example:

Copy code

```
java --add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/sun.security.util=ALL-UNNAMED -jar my-snowpark-app.jar
```

### Setting the parameter as an environment variable

You can set the parameter in your system’s environment variables. Refer to your operating system’s documentation for
instructions on setting environment variables.

Create or update a `JDK_JAVA_OPTIONS` environment variable, as in the following Unix-based example:

Copy code

```
export JDK_JAVA_OPTIONS="--add-opens=java.base/java.nio=ALL-UNNAMED"
```

If you are also using RSA private key authentication, you will also need to allow `sun.security.util`, as in the following example:

Copy code

```
export JDK_JAVA_OPTIONS="--add-opens=java.base/java.nio=ALL-UNNAMED --add-opens=java.base/sun.security.util=ALL-UNNAMED"
```
