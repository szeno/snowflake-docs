# Calling functions and stored procedures in Snowpark Scala

To process data in a DataFrame, you can call system-defined SQL functions, user-defined functions, and stored procedures. This
topic explains how to call these in Snowpark.

## Calling system-defined functions

If you need to call [system-defined SQL functions](/sql-reference-functions), use the equivalent functions in the
[com.snowflake.snowpark.functions object](../reference/scala/com/snowflake/snowpark/functions$.html).

The following example calls the `upper` function in the `functions` object (the equivalent of the system-defined
[UPPER](/sql-reference/functions/upper) function) to return the values in the name column with the letters in uppercase:

Copy code

```
// Import the upper function from the functions object.
import com.snowflake.snowpark.functions._
...
session.table("products").select(upper(col("name"))).show()
```

If a system-defined SQL function is not available in the functions object, you can use one of the following approaches:

- Use the `callBuiltin` function to call the system-defined function.
- Use the `builtin` function to create a function object that you can use to call the system-defined function.

`callBuiltin` and `builtin` are defined in the `com.snowflake.snowpark.functions` object.

For `callBuiltin`, pass the name of the system-defined function as the first argument. If you need
to pass the values of columns to the system-defined function, define and pass
[Column](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-cols-and-expressions) objects as additional arguments to the `callBuiltin` function.

The following example calls the system-defined function [RADIANS](/sql-reference/functions/radians), passing in the value from the
column `col1`:

Copy code

```
// Import the callBuiltin function from the functions object.
import com.snowflake.snowpark.functions._
...
// Call the system-defined function RADIANS() on col1.
val result = df.select(callBuiltin("radians", col("col1"))).collect()
```

The `callBuiltin` function returns a `Column`, which you can pass to the
[DataFrame transformation methods](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-transform) (e.g. filter, select, etc.).

For `builtin`, pass the name of the system-defined function, and use the returned function object to call the
system-defined function. For example:

Copy code

```
// Import the callBuiltin function from the functions object.
import com.snowflake.snowpark.functions._
...
// Create a function object for the system-defined function RADIANS().
val radians = builtin("radians")
// Call the system-defined function RADIANS() on col1.
val result = df.select(radians(col("col1"))).collect()
```

## Calling scalar user-defined functions (UDFs)

The method for calling a UDF depends on how the UDF was created:

- To call [an anonymous UDF](/developer-guide/snowpark/scala/creating-udfs#label-snowpark-udf-inline-anonymous), call the `apply` method of the
  [UserDefinedFunction](../reference/scala/com/snowflake/snowpark/UserDefinedFunction.html) object that was returned when you created the UDF.

  The arguments that you pass to a UDF must be [Column](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-cols-and-expressions) objects. If you need
  to pass in a literal, use `lit()`, as explained in [Using Literals as Column Objects](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-cols-lit).
- To call UDFs that you [registered by name](/developer-guide/snowpark/scala/creating-udfs#label-snowpark-udf-inline-named) and UDFs that you created by executing
  [CREATE FUNCTION](/sql-reference/sql/create-function), use the `callUDF` function in the `com.snowflake.snowpark.functions`
  object.

  Pass the name of the UDF as the first argument and any UDF parameters as additional arguments.

Calling a UDF returns a `Column` object containing the return value of the UDF.

The following example calls the UDF function `myFunction`, passing in the values from the columns `col1` and `col2`. The
example passes the return value from `myFunction` to the `select` method of the DataFrame.

Copy code

```
// Import the callUDF function from the functions object.
import com.snowflake.snowpark.functions._
...
// Runs the scalar function 'myFunction' on col1 and col2 of df.
val result =
    df.select(
        callUDF("myDB.schema.myFunction", col("col1"), col("col2"))
    ).collect()
```

## Calling table functions (system functions and UDTFs)

To call a [table function](/sql-reference/functions-table) or a
[user-defined table function (UDTF)](/developer-guide/udf/udf-overview#label-scalar-vs-tabular-udfs):

1. Construct a [TableFunction](../reference/scala/com/snowflake/snowpark/TableFunction.html) object, passing in the name of the table function.

   If you are creating a UDTF in Snowpark, you can just use the `TableFunction` object returned by the
   `UDTFRegistration.registerTemporary` or `UDTFRegistration.registerPermanent` method. See
   [Creating User-Defined Table Functions (UDTFs)](/developer-guide/snowpark/scala/creating-udfs#label-snowpark-udtf).
2. Call [session.tableFunction](../reference/scala/com/snowflake/snowpark/Session.html#tableFunction(func:com.snowflake.snowpark.TableFunction,args:Map%5BString,com.snowflake.snowpark.Column%5D):com.snowflake.snowpark.DataFrame), passing in the `TableFunction` object and a `Map` of input argument names and
   values.

The `session.tableFunction` method returns a DataFrame that contains the output of the table function.

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
val dfTableFunctionOutput = session.tableFunction(TableFunction("product_by_category_id"), Map("cat_id" -> lit(10)))
dfTableFunctionOutput.show()
```

If you need to join the output of a table function with a DataFrame, call the
[DataFrame.join method that passes in a TableFunction](../reference/scala/com/snowflake/snowpark/DataFrame.html#join(func:com.snowflake.snowpark.TableFunction,args:Map%5BString,com.snowflake.snowpark.Column%5D):com.snowflake.snowpark.DataFrame).

## Calling stored procedures

[Preview Feature](/release-notes/preview-features) — Open

Preview support for this feature is available to all accounts.

You can execute a procedure either on the server side (in the Snowflake environment) or locally. Keep in mind that as the two environments
are different, the conditions and results of procedure execution may differ between them.

You can call a procedure with the Snowpark API in either of the following ways:

- Execute a function locally for testing and debugging using the `SProcRegistration.runLocally` method.
- Execute a procedure in the server-side Snowflake environment using the `Session.storedProcedure` method. This includes a procedure
  scoped to the current session or a permanent procedure stored on Snowflake.

You can also call a permanent stored procedure you create with the Snowpark API from a Snowflake worksheet. For more information, refer
to [Calling a stored procedure](/developer-guide/stored-procedure/stored-procedures-calling).

For more on creating procedures with the Snowpark API, refer to [Creating stored procedures for DataFrames in Scala](/developer-guide/snowpark/scala/creating-sprocs).

### Executing a procedure’s logic locally

You can execute the lambda function for your procedure in your local environment using the `SProcRegistration.runLocally` method.
The method executes the function and returns its result as the type returned by the function.

For example, you can locally call (on the client side) a lambda function that you intend to use in a procedure before registering a
procedure from it on Snowflake. You begin by assigning the lambda code as a value to a variable. You pass that variable to the
`SProcRegistration.runLocally` method to run it on the client side. You can also use the variable to represent the function when
registering the procedure.

Code in the following example assigns the function to the `func` variable. It then tests the function locally by passing the
variable to the `SProcRegistration.runLocally` method with the function’s argument value. The variable is also used to register the
procedure.

Copy code

```
val session = Session.builder.configFile("my_config.properties").create

// Assign the lambda function.
val func = (session: Session, num: Int) => num + 1

// Execute the function locally.
val result = session.sproc.runLocally(func, 1)
print("\nResult: " + result)
```

### Executing a procedure on the server

To execute a procedure in the Snowflake environment on the server, use the `Session.storedProcedure` method. The method returns a
`DataFrame` object.

For example, you can execute:

- A temporary or permanent procedure you [create using the Snowpark API](/developer-guide/snowpark/java/creating-sprocs).
- A procedure [created using a CREATE PROCEDURE statement](/developer-guide/stored-procedure/stored-procedures-creating).

Code in the following example creates a temporary procedure designed to execute on the server, but only last for as long as the current
Snowpark session. It then executes the procedure using both the procedure’s name and the `StoredProcedure` variable representing it.

Copy code

```
val session = Session.builder.configFile("my_config.properties").create

val name: String = "add_two"

val tempSP: StoredProcedure =
  session.sproc.registerTemporary(
    name,
    (session: Session, num: Int) => num + 2
  )

// Execute the procedure on the server by passing the procedure's name.
session.storedProcedure(name, 1).show()

// Execute the procedure on the server by passing a variable
// representing the procedure.
session.storedProcedure(tempSP, 1).show();
```
