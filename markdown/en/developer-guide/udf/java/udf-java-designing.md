# Designing Java UDFs

This topic helps you design Java UDFs.

## Choosing your data types

Before you write your code:

- Choose the data types your function should accept as arguments and the data
  type your function should return.
- Take into account time-zone related issues.
- Decide how to handle NULL values.

### SQL-Java data type mappings for parameters and return types

For information on how Snowflake converts between Java and SQL data types, see
[Data Type Mappings Between SQL and Handler Languages](/developer-guide/udf-stored-procedure-data-type-mapping).

### TIMESTAMP\_LTZ values and time zones

A Java UDF is largely isolated from the environment in which it is called. However, the timezone is inherited from
the calling environment. If the caller’s session set a default time zone before calling the Java UDF, then the Java
UDF has the same default time zone. Java UDF uses the same [IANA Time Zone Database](https://www.iana.org/time-zones) data as the native [TIMEZONE](/sql-reference/parameters#label-timezone)
Snowflake SQL uses (i.e. data from release 2025b of the Time Zone Database).

### NULL values

Snowflake supports two distinct NULL values: SQL `NULL` and VARIANT’s JSON `null`. (For information about Snowflake
VARIANT NULL, see [NULL values](/user-guide/semistructured-considerations#label-variant-null).)

Java supports one `null` value, which is only for non-primitive data types.

A SQL `NULL` argument to a Java UDF translates to the Java `null` value, but only for Java data types that
support `null`.

A returned Java `null` value translates back to SQL `NULL`.

### Arrays and variable number of arguments

Java UDFs can receive arrays of any of the following Java data types:

- String
- boolean
- double
- float
- int
- long
- short

The data type of the SQL values passed must be compatible with the corresponding Java data type. For details about data type compatibility,
see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).

The following additional rules apply for each of the specified Java data types:

- boolean: The Snowflake ARRAY must contain only BOOLEAN elements, and must not contain any NULL values.
- int/short/long: The Snowflake ARRAY must contain only [fixed-point](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) elements with a
  scale of 0, and must not contain any NULL values.
- float/double: The Snowflake ARRAY must contain either:

  - [FLOAT](/sql-reference/data-types-numeric#label-data-types-for-floating-point-numbers) elements.
  - [Fixed-point](/sql-reference/data-types-numeric#label-data-types-for-fixed-point-numbers) elements (with any scale).

  The ARRAY must not contain any NULL values.

Java methods can receive these arrays in either of two ways:

- Using Java’s array feature.
- Using Java’s *varargs* (variable number of arguments) feature.

In both cases, your SQL code must pass an [ARRAY](/sql-reference/data-types-semistructured).

#### Passing via an ARRAY

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

#### Passing via varargs

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

## Designing Java UDFs that stay within Snowflake-imposed constraints

For information on designing handler code that runs well on Snowflake, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).

## Designing the class

When a SQL statement calls your Java UDF, Snowflake calls a Java method you have written. Your Java method is called a
“handler method”, or “handler” for short.

As with any Java method, your method must be declared as part of a class. Your handler method can be a static method or an instance
method of the class. If your handler is an instance method, and your class defines a zero-argument constructor, then Snowflake
invokes your constructor at initialization time to create an instance of your class. If
your handler is a static method, your class is not required to have a constructor.

The handler is called once for each row passed to the Java UDF. (Note: a new instance of the class is not created for each row;
Snowflake can call the same instance’s handler method more than once, or call the same static method more than once.)

To optimize execution of your code, Snowflake assumes that initialization might be slow, while execution of the handler method
is fast. Snowflake sets a longer timeout for executing initialization (including the time to load your UDF and the time
to call the constructor of the handler method’s containing class, if a constructor is defined) than for executing the handler
(the time to call your handler with one row of input).

Additional information about designing the class is in [Creating a Java UDF handler](/developer-guide/udf/java/udf-java-creating).

## Optimizing initialization and controlling global state in scalar UDFs

Most function and procedure handlers should follow the guidelines below:

- If you need to initialize shared state that does not change across rows, initialize it outside the handler function, such as in the
  module or constructor.
- Write your handler function or method to be thread safe.
- Avoid storing and sharing dynamic state across rows.

If your UDF cannot follow these guidelines, or if you would like a deeper understanding of the reasons for these guidelines,
please read the next few subsections.

### Sharing state across calls

Snowflake expects scalar UDFs to be processed independently. Relying on state shared between invocations can result in unexpected
behavior. This is because the system can process rows in any order and spread those invocations across several JVMs (for handlers written
in Java or Scala) or instances (for handlers written in Python).

UDFs should avoid relying on shared state across calls to the handler method. However, there are two situations in which you might want a
UDF to store shared state:

- Code that contains expensive initialization logic that you do not want to repeat for each row.
- Code that leverages shared state across rows, such as a cache.

If you need to share state across multiple rows, and if that state does not change over time, then use a constructor to create
shared state by setting instance-level variables. The constructor is executed only once per instance, while the handler is called
once per row, so initializing in the constructor is cheaper when a handler processes multiple rows. And because the constructor is
called only once, the constructor does not need to be written to be thread-safe.

If your UDF stores shared state that changes, then your code must be prepared to handle concurrent access to that state.
The next two sections provide more information about parallelism and shared state.

### Understanding Java UDF parallelization

To improve performance, Snowflake parallelizes both across and within JVMs.

- Across JVMs:

  Snowflake parallelizes across workers in a [warehouse](/user-guide/warehouses-overview). Each worker runs one (or more)
  JVMs. This means that there is no global shared state. At most, state can be shared only within a single JVM.
- Within JVMs:

  - Each JVM can execute multiple threads that can call the same instance’s handler method in parallel. This means that each
    handler method needs to be thread-safe.
  - If a UDF is IMMUTABLE and a SQL statement calls the UDF more than once with the same arguments for the same row, then the UDF
    returns the same value for each call for that row. For example, the following returns the same value twice for each row
    if the UDF is IMMUTABLE:

    Copy code

    ```
    SELECT
        my_java_udf(42),
        my_java_udf(42)
      FROM table1;
    ```

    If you would like multiple calls to return independent values even when passed the same arguments, and if you do not want
    to declare the function VOLATILE, then bind multiple separate UDFs to the same handler method. For example:

    1. Create a JAR file named `@java_udf_stage/rand.jar` with code:

       Copy code

       ```
       class MyClass {

         private double x;

         // Constructor
         public MyClass()  {
           x = Math.random();
         }

         // Handler
         public double myHandler() {
           return x;
         }
       }
       ```
    2. Create the Java UDFs as shown below. These UDFs have different names, but use the same JAR file and the same handler
       within that JAR file.

       Copy code

       ```
       CREATE FUNCTION my_java_udf_1()
         RETURNS DOUBLE
         LANGUAGE JAVA
         IMPORTS = ('@java_udf_stage/rand.jar')
         HANDLER = 'MyClass.myHandler';

       CREATE FUNCTION my_java_udf_2()
         RETURNS DOUBLE
         LANGUAGE JAVA
         IMPORTS = ('@java_udf_stage/rand.jar')
         HANDLER = 'MyClass.myHandler';
       ```
    3. The following code calls both UDFs. The UDFs point to the same JAR file and handler. These calls create two
       instances of the same class. Each instance returns an independent value, so the example below returns two independent
       values, rather than returning the same value twice:

       Copy code

       ```
       SELECT
           my_java_udf_1(),
           my_java_udf_2()
         FROM table1;
       ```

### Storing JVM state information

One reason to avoid relying on dynamic shared state is that rows are not necessarily processed in a predictable order.
Each time a SQL statement is executed, Snowflake can vary the number of batches, the order in which batches are
processed, and the order of rows within a batch. If a scalar UDF is designed so that one row affects the return value for a
subsequent row, then the UDF can return different results each time that the UDF is executed.

## Handling errors

A Java method used as a UDF can use the normal Java exception-handling techniques to catch errors within the
method.

If an exception occurs inside the method and is not caught by the method, Snowflake raises an error that includes the stack trace for the
exception. When [logging of unhandled exceptions](/developer-guide/logging-tracing/unhandled-exception-messages) is enabled,
Snowflake logs data about unhandled exceptions in an event table.

You can explicitly throw an exception without catching it in order to end the query and produce a SQL error. For
example:

Copy code

```
if (x < 0) {
  throw new IllegalArgumentException("x must be non-negative.");
}
```

When debugging, you can include values in the SQL error message text. To do so, place an entire Java method body in a
try-catch block; append argument values to the caught error’s message; and throw an exception with the extended
message. To avoid revealing sensitive data, remove argument values prior to deploying JAR files to a production
environment.

## Following best practices

- Write platform-independent code.

  - Avoid code that assumes a specific CPU architecture (e.g. x86).
  - Avoid code that assumes a specific operating system.
- If you need to execute initialization code and do not want to include it in the method that you call, you can put
  the initialization code into a static initialization block.
- Whenever possible when using an in-line handler, specify a value for the [CREATE FUNCTION](/sql-reference/sql/create-function) or
  [CREATE PROCEDURE](/sql-reference/sql/create-procedure) TARGET\_PATH parameter. This will prompt Snowflake to reuse previously-generated
  handler code output rather than recompiling for each call. For more information, see [Using an in-line handler](/developer-guide/inline-or-staged#label-inline-stage-using-inline).

See also:

- [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints)
- [Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices)

## Following good security practices

To help ensure that your handler functions in a secure way, see the best practices described in
[Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices).
