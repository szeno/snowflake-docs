# Calling functions and stored procedures in Snowpark Java

To process data in a DataFrame, you can call system-defined SQL functions, user-defined functions, and stored procedures. This
topic explains how to call these in Snowpark.

## Calling system-defined functions

If you need to call [system-defined SQL functions](/sql-reference-functions), use the equivalent static methods in the
[Functions class](../reference/java/com/snowflake/snowpark_java/Functions.html).

The following example calls the `upper` static method in the `Functions` class (the equivalent of the system-defined
[UPPER](/sql-reference/functions/upper) function) to return the values in the name column with the letters in uppercase:

Copy code

```
DataFrame df = session.table("sample_product_data");
df.select(Functions.upper(Functions.col("name"))).show();
```

If a system-defined SQL function is not available in the `Functions` class, you can use the `Functions.callUDF`
static method to call the system-defined function.

For `callUDF`, pass the name of the system-defined function as the first argument. If you need
to pass the values of columns to the system-defined function, define and pass
[Column](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-cols-and-expressions) objects as additional arguments to the `callUDF` method.

The following example calls the system-defined function [RADIANS](/sql-reference/functions/radians), passing in the value from the
column `degrees`:

Copy code

```
// Call the system-defined function RADIANS() on degrees.
DataFrame dfDegrees = session.range(0, 360, 45).rename("degrees", Functions.col("id"));
dfDegrees.select(Functions.col("degrees"), Functions.callUDF("radians", Functions.col("degrees"))).show();
```

The `callUDF` method returns a `Column`, which you can pass to the
[DataFrame transformation methods](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-transform) (e.g. filter, select, etc.).

## Calling scalar user-defined functions (UDFs)

The method for calling a UDF depends on how the UDF was created:

- To call [an anonymous UDF](/developer-guide/snowpark/java/creating-udfs#label-snowpark-java-udf-inline-anonymous), call the `apply` method of the
  [UserDefinedFunction](../reference/scala/com/snowflake/snowpark/UserDefinedFunction.html) object that was returned when you created the UDF.

  The arguments that you pass to a UDF must be [Column](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-cols-and-expressions) objects. If you
  need to pass in a literal, use `Functions.lit()`, as explained in [Using Literals as Column Objects](/developer-guide/snowpark/java/working-with-dataframes#label-snowpark-java-dataframe-cols-lit).
- To call UDFs that you [registered by name](/developer-guide/snowpark/java/creating-udfs#label-snowpark-java-udf-inline-named) and UDFs that you created by executing
  [CREATE FUNCTION](/sql-reference/sql/create-function), use the `Functions.callUDF` static method.

  Pass the name of the UDF as the first argument and any UDF parameters as additional arguments.

Calling a UDF returns a `Column` object containing the return value of the UDF.

The following example calls the UDF function `doubleUdf`, passing in the value from the columns `quantity`. The
example passes the return value from `doubleUdf` to the `select` method of the DataFrame.

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
DataFrame dfWithDoubleQuantity = df.withColumn("doubleQuantity", doubleUdf.apply(Functions.col("quantity")));
dfWithDoubleQuantity.show();
```

## Calling table functions (system functions and UDTFs)

To call a [table function](/sql-reference/functions-table) or a
[user-defined table function (UDTF)](/developer-guide/udf/udf-overview#label-scalar-vs-tabular-udfs):

1. Construct a [TableFunction](../reference/scala/com/snowflake/snowpark/TableFunction.html) object, passing in the name of the table function.
2. Call the [tableFunction method of the Session object](../reference/java/com/snowflake/snowpark_java/Session.html#tableFunction(com.snowflake.snowpark_java.TableFunction,java.util.Map)), passing in the `TableFunction` object and a `Map` of input
   argument names and values.

`table?Function` returns a DataFrame that contains the output of the table function.

For example, suppose that you executed the following command to create a SQL UDTF:

Copy code

```
CREATE OR REPLACE FUNCTION product_by_category_id(cat_id INT)
  RETURNS TABLE(id INT, name VARCHAR)
  AS
  $$
    SELECT id, name
      FROM sample_product_data
      WHERE category_id = cat_id
  $$
  ;
```

The following code calls this UDTF and creates a DataFrame for the output of the UDTF. The example prints the first 10 rows of
output to the console.

Copy code

```
import java.util.HashMap;
import java.util.Map;
...

Map<String, Column> arguments = new HashMap<>();
arguments.put("cat_id", Functions.lit(10));
DataFrame dfTableFunctionOutput = session.tableFunction(new TableFunction("product_by_category_id"), arguments);
dfTableFunctionOutput.show();
```

If you need to join the output of a table function with a DataFrame, call the [join method that passes in a TableFunction](../reference/java/com/snowflake/snowpark_java/DataFrame.html#join(com.snowflake.snowpark_java.TableFunction,java.util.Map)).

## Calling stored procedures

[Preview Feature](/release-notes/preview-features) — Open

Preview support for this feature is available to all accounts.

You can execute a procedure either on the server side (in the Snowflake environment) or locally. Keep in mind that as the two environments
are different, the conditions and results of procedure execution may differ between them.

You can call a procedure with the Snowpark API in either of the following ways:

- Execute a function locally for testing and debugging using the [SProcRegistration.runLocally](../reference/java/com/snowflake/snowpark_java/SProcRegistration.html#runLocally(com.snowflake.snowpark_java.internal.JavaSProc,java.lang.Object...)) method.
- Execute a procedure in the server-side Snowflake environment using one of the [Session.storedProcedure](../reference/java/com/snowflake/snowpark_java/Session.html#storedProcedure(com.snowflake.snowpark_java.StoredProcedure,java.lang.Object...)) methods. This includes a procedure
  scoped to the current session or a permanent procedure stored on Snowflake.

You can also call a permanent stored procedure you create with the Snowpark API from SQL code. For more information, refer
to [Calling a stored procedure](/developer-guide/stored-procedure/stored-procedures-calling).

For more on creating procedures with the Snowpark API, refer to [Creating stored procedures for DataFrames in Java](/developer-guide/snowpark/java/creating-sprocs).

### Executing a procedure’s logic locally

You can execute the lambda function for your procedure in your local environment using the `SProcRegistration.runLocally` method.
The method executes the function and returns its result as the type returned by the function.

For example, you can call a lambda function that you intend to use in a procedure before registering a procedure from it on Snowflake. You
begin by assigning the lambda code as a value to a variable whose type is one of the `com.snowflake.snowpark_java.sproc.JavaSProc`
interfaces. Using that variable, you can test call the function with the `SProcRegistration.runLocally` method. You can also use
the variable to represent the function when registering the procedure.

Code in the following example initializes a `JavaSProc` variable from the lambda function that will be the procedure’s logic. It then
tests the function by passing the variable to the `SProcRegistration.runLocally` method with the function’s argument. The variable
is also used to register the function.

Copy code

```
Session session = Session.builder().configFile("my_config.properties").create();

// Assign the lambda function to a variable.
JavaSProc1<Integer, Integer> func =
  (Session session, Integer num) -> num + 1;

// Execute the function locally.
int result = (Integer)session.sproc().runLocally(func, 1);
System.out.println("\nResult: " + result);

// Register the procedure.
StoredProcedure sp =
  session.sproc().registerTemporary(
    func,
    DataTypes.IntegerType,
    DataTypes.IntegerType
  );

// Execute the procedure on the server.
session.storedProcedure(sp, 1).show();
```

### Executing a procedure on the server

To execute a procedure in the Snowflake environment on the server, use the `Session.storedProcedure` method. The method returns a
`DataFrame` object.

For example, you can execute:

- A temporary or permanent procedure you [create using the Snowpark API](/developer-guide/snowpark/java/creating-sprocs).
- A procedure [created using a CREATE PROCEDURE statement](/developer-guide/stored-procedure/stored-procedures-creating).

Code in the following example creates a temporary procedure designed to execute on the server, but only last for as long as the current
Snowpark session. It then executes the procedure using both the procedure’s name and the [com.snowflake.snowpark\_java.StoredProcedure](../reference/java/com/snowflake/snowpark_java/StoredProcedure.html)
variable representing it.

Copy code

```
Session session = Session.builder().configFile("my_config.properties").create();

String incrementProc = "increment";

// Register the procedure.
StoredProcedure tempSP =
  session.sproc().registerTemporary(
    incrementProc,
    (Session session, Integer num) -> num + 1,
    DataTypes.IntegerType,
    DataTypes.IntegerType
  );

// Execute the procedure on the server by passing the procedure's name.
session.storedProcedure(incrementProc, 1).show();

// Execute the procedure on the server by passing a variable
// representing the procedure.
session.storedProcedure(tempSP, 1).show();
```
