# Writing a scalar UDF in Scala

You can write a scalar user-defined function (UDF) in Scala. The Scala handler code executes when the UDF is called. This topic describes how
to write a handler in Scala and create the UDF.

A UDF is a user-defined function that returns scalar results – meaning a single value rather than multiple rows. For more general
information about UDFs, see [User-defined functions overview](/developer-guide/udf/udf-overview).

When you create a UDF, you do the following:

1. Write a Scala object or class with a method that Snowflake will invoke when the UDF is called.

   For more information, see [Implementing a handler](#label-udf-scala-writing-your-scala-code) in this topic.
2. Create the UDF in SQL with the CREATE FUNCTION command, specifying your object or class and method as the handler. When you create the
   UDF, you specify:

   - Data types of UDF input parameters.
   - Data type of the UDF return value.
   - Code to execute as a handler when the UDF is called.
   - The language in which the handler is written.

   For more about CREATE FUNCTION syntax, see [Creating the UDF with `CREATE FUNCTION`](/developer-guide/udf/scala/udf-scala-general#label-udf-scala-create-function).

You can call a UDF as described in [Executing a UDF](/developer-guide/udf/udf-calling-sql).

## Implementing a handler

You implement an object or class with a handler method to process UDF argument values into the UDF’s return value.

When writing a handler, you:

- Write a public class with a public method to specify as the handler.

  This will be the method that Snowflake invokes when the UDF is called in SQL.

  You can define multiple other methods in the same object or class, then use each as the handler for a different UDF. For example, you
  might want to do this when you intend to keep the compiled handler code on a stage and reference it from multiple functions.

  For more information on a staged handler, refer to [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
- Optionally write a zero-argument constructor for Snowflake to invoke to initialize the handler.

Note

Be sure to write your handler in keeping with the Snowflake-imposed constraints in each handler method and methods it calls.
For more on these constraints, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).

## Handler example

Code in the following example includes a `MyHandler.echoVarchar` handler method that receives and returns string. The value received
by the UDF – a VARCHAR – is mapped by Snowflake to the handler method’s parameter type – a String.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER='MyHandler.echoVarchar'
  AS
  $$
  class MyHandler {
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
  RUNTIME_VERSION = 2.13
  HANDLER='MyHandler.echoVarchar'
  AS
  $$
  class MyHandler {
    def echoVarchar(x : String): String = {
      return x
    }
  }
  $$;
```

Call the UDF

Copy code

```
SELECT echo_varchar('Hello');
```

## Initializing the handler

You can optionally initialize your handler by adding a zero-argument constructor.

If the constructor throws an error, the error is thrown as a user error, along with the exception message.

Copy code

```
def this() = {
  // Initialize here.
}
```

## Processing function arguments

To process data passed to the UDF as arguments, implement a public method that Snowflake will invoke when the UDF is called in SQL code.
When you create the UDF with a CREATE FUNCTION command, you’ll use the HANDLER clause to specify the method as the handler.

When declaring a handler method, you:

- Declare the handler method as public.

  You can optionally include a zero-argument constructor to initialize the handler. For more information, refer to
  [Initializing the handler](#label-udf-scala-handler-initializing) in this topic.

  If you intend to package the class into a JAR as a staged handler, you can declare multiple handler methods, later specifying each as a
  handler with the HANDLER clause of a CREATE FUNCTION statement. For more information on a staged handler, refer to
  [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
- Specify handler method parameter and return types that map to the SQL types specified by the UDF declaration.

  For more information, refer to [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).
- Optionally declare additional methods to support the handler method’s processing, such as methods to be called from the handler method.

  Code in the following example features a `handleStrings` handler method that calls a non-handler method `concatenate` to
  help process the array received as an argument.

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

  The following calls the `generate_greeting` function.

  Copy code

  ```
  SELECT generate_greeting(['Hello', 'world']);
  ```

  The following illustrates the output from calling `generate_greeting` with the values above.

  ```
  Hello world
  ```

## Overloading handler methods

You can overload handler methods in the same class or object as long as they have different numbers of parameters.

For Scala UDFs, Snowflake uses only the *number* of method arguments, not their *types*, to differentiate handler methods.
Resolving based on data types is impractical because some SQL data types can be mapped to more than one Scala or Java data type and
thus potentially to more than one handler method signature.

For example, if two Scala methods have the same name and the same number of arguments, but different data types, then calling a UDF using
one of those methods as a handler generates an error similar to the following:

Copy code

```
Cannot determine which implementation of handler "handler name" to invoke since there are multiple
definitions with <number of args> arguments in function <user defined function name> with
handler <class name>.<handler name>
```

If a warehouse is available, the error is detected at the time that the UDF is created. Otherwise, the error occurs when the UDF is
called.
