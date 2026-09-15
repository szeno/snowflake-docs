# General Scala UDF handler coding guidelines

This topic describes general guidelines for writing handler code in Scala. For information specific to scalar function handlers, refer to
[Writing a scalar UDF in Scala](/developer-guide/udf/scala/udf-scala-scalar).

For suggestions on structuring your project, packaging your code, and managing dependencies, refer to
[Scala UDF handler project and packaging](/developer-guide/udf/scala/udf-scala-packaging).

## Best practices

- Write platform-independent code.

  - Avoid code that assumes a specific CPU architecture (e.g. x86).
  - Avoid code that assumes a specific operating system.
- If you need to execute initialization code and do not want to include it in the method that you call, you can put
  the initialization code into a companion object of your handler class.
- Whenever possible when using an in-line handler, specify a value for the [CREATE FUNCTION](/sql-reference/sql/create-function) or
  [CREATE PROCEDURE](/sql-reference/sql/create-procedure) TARGET\_PATH parameter. This will prompt Snowflake to reuse previously-generated
  handler code output rather than recompiling for each call. For more information, see [Using an in-line handler](/developer-guide/inline-or-staged#label-inline-stage-using-inline).

## Writing a handler

You can write a scalar UDF with a handler written in Scala.

The handler is called once for each row passed to the Scala UDF. A new instance of the class is not created for each row;
Snowflake can call the same instance’s handler method more than once.

To optimize execution of your code, Snowflake timeout thresholds differ between the time it takes to initialize your handler class or
object, and the time it takes to execute its handler method. Snowflake allows more time to initialize the handler class or object on the
assumption that initialization might take longer. This includes the time to load your UDF and the time
to call the constructor of the handler method’s containing class, if a constructor is defined.

## Handling errors

You can handle exceptions with common exception-handling techniques to catch errors within the handler method.

If an exception occurs inside the method and is not caught by the method, Snowflake raises an error that includes the stack trace for the
exception.

You can explicitly throw an exception without catching it in order to end the query and produce a SQL error. For example:

Copy code

```
if (x < 0) throw new IllegalArgumentException("x must be non-negative.")
```

When debugging, you can include values in the SQL error message text. To do so:

- Place an entire Scala method body in a try-catch block;
- Append argument values to the caught error’s message; and
- Throw an exception with the extended message.

To avoid revealing sensitive data, remove argument values prior to deploying JAR files to a production environment.

## Choosing data types

When writing your handler, you’ll need to declare parameter and return data types (from the handler’s language) that map well with the
UDF’s parameter and return data types (from SQL).

When the UDF is called, Snowflake converts the UDF’s arguments from the SQL parameter types to the handler’s parameter types. When
returning a value, Snowflake converts the return value from the handler’s return type to the UDF’s return type.

Snowflake converts values between types according to supported mappings between SQL types and Scala types. For more about those mappings,
refer to [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).

When choosing data types of Scala variables, take into account the maximum and minimum possible values of the data that could be sent
from (and returned to) Snowflake.

## Creating the UDF with `CREATE FUNCTION`

You create a UDF in SQL using the CREATE FUNCTION command, specifying the code you wrote as the handler. For the command reference, see
[CREATE FUNCTION](/sql-reference/sql/create-function).

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION <name> ( [ <arguments> ] )
  RETURNS <type>
  LANGUAGE SCALA
  [ IMPORTS = ( '<imports>' ) ]
  RUNTIME_VERSION = 2.12
  [ PACKAGES = ( '<package_name>' [, '<package_name>' . . .] ) ]
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  HANDLER = '<handler_class>.<handler_method>'
  [ AS '<scala_code>' ]
```

Copy code

```
CREATE OR REPLACE FUNCTION <name> ( [ <arguments> ] )
  RETURNS <type>
  LANGUAGE SCALA
  [ IMPORTS = ( '<imports>' ) ]
  RUNTIME_VERSION = 2.13
  [ PACKAGES = ( '<package_name>' [, '<package_name>' . . .] ) ]
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  HANDLER = '<handler_class>.<handler_method>'
  [ AS '<scala_code>' ]
```

To associate the handler code you’ve written with the UDF, you do the following when executing CREATE FUNCTION:

- Set LANGUAGE to SCALA.
- Set the IMPORTS clause value to the path and name of the handler class if the class is in an external location, such as on a stage.
- Set RUNTIME\_VERSION to the version of the Scala runtime that your code requires.
- Set the PACKAGES clause value to the name of one or more packages, if any, required by the handler class.
- Set the HANDLER clause value to the name of the handler object and method.
- The `AS '<scala_code>'` clause is required if the handler code is specified in-line with CREATE FUNCTION.
