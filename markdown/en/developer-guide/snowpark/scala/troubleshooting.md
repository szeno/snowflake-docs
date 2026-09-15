# Analyzing Queries and Troubleshooting with Snowpark Scala

This topic provides some guidelines on analyzing queries and troubleshooting problems when working with the Snowpark library.

## Viewing the Execution Plan for a Query in Snowpark

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

> ![Snowpark request in the History page](/static/images/query-tag-snowpark.png)

## Troubleshooting

### Changing the Logging Settings

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

### java.lang.OutOfMemoryError Exceptions

If a `java.lang.OutOfMemoryError` exception is thrown, increase the maximum heap size for the JVM.

If you are using the Scala REPL and you need to increase the maximum heap size, edit the `run.sh` shell script (provided in
the archive file) and add the `-J-Xmxmaximum_size` flag to the `scala` command. The following example increases
the maximum heap size to 4 GB:

> Copy code
>
> ```
> scala -J-Xmx4G ...
> ```
