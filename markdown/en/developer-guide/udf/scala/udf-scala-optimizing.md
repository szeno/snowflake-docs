# Controlling global state in scalar Scala UDFs

When designing a UDF and handler that requires access to shared state, you will need to account for the way Snowflake executes UDFs to
process rows.

Most handlers should follow these guidelines:

- If you need to initialize shared state that does not change across rows, initialize it outside the handler function, such as in a
  constructor.
- Write your handler method to be thread safe.
- Avoid storing and sharing dynamic state across rows.

If your UDF cannot follow these guidelines, or if you would like a deeper understanding of the reasons for these guidelines,
please read the next few subsections.

## Sharing state across calls

Snowflake expects scalar UDFs to be processed independently. Relying on state shared between invocations can result in unexpected
behavior. This is because the system can process rows in any order and spread those invocations across several JVMs (for handlers written
in Java or Scala).

UDFs should avoid relying on shared state across calls to the handler method. However, there are two situations in which you might want a
UDF to store shared state:

- Code that contains expensive initialization logic that you do not want to repeat for each row.
- Code that leverages shared state across rows, such as a cache.

If you need to share state across multiple rows, and if that state does not change over time, then use a constructor to create
shared state by setting instance-level variables. The constructor is executed only once per instance, while the handler is called
once per row, so initializing in the constructor is cheaper when a handler processes multiple rows. And because the constructor is
called only once, the constructor does not need to be written to be thread-safe.

If your UDF stores shared state that changes, then your code must be prepared to handle concurrent access to that state.

For more information about parallelism and shared state, refer to [Understanding parallelization](#label-udf-scala-parallelization) and
[Storing JVM state information](#label-udf-scala-storing-state-across-calls) in this topic.

## Understanding parallelization

To improve performance, Snowflake parallelizes both across and within JVMs.

### Parallelizing across JVMs

Snowflake parallelizes across workers in a [warehouse](/user-guide/warehouses-overview). Each worker runs one (or more)
JVMs. This means that there is no global shared state. At most, state can be shared only within a single JVM.

### Parallelizing within JVMs

- Each JVM can execute multiple threads that can call the same instance’s handler method in parallel. This means that each
  handler method needs to be thread-safe.
- If a UDF is IMMUTABLE and a SQL statement calls the UDF more than once with the same arguments for the same row, then the UDF
  returns the same value for each call for that row.

  For example, the following returns the same value twice for each row if the UDF is IMMUTABLE:

  Copy code

  ```
  SELECT my_scala_udf(42), my_scala_udf(42) FROM table1;
  ```

  If you would like multiple calls to return independent values even when passed the same arguments, and if you do not want
  to declare the function VOLATILE, then bind multiple separate UDFs to the same handler method.

  You might do this using the following steps.

  1. Create a JAR file named `@udf_libs/rand.jar` with the following code:

     Copy code

     ```
     class MyClass {

       var x: Double = 0.0

       // Constructor
       def this() = {
         x = Math.random()
       }

       // Handler
       def myHandler(): Double = x
     }
     ```
  2. Create the Scala UDFs as shown below.

     These UDFs have different names, but use the same JAR file and the same handler within that JAR file.

     Scala 2.12Scala 2.13

     Copy code

     ```
     CREATE FUNCTION my_scala_udf_1()
       RETURNS DOUBLE
       LANGUAGE SCALA
       IMPORTS = ('@udf_libs/rand.jar')
       HANDLER = 'MyClass.myHandler';

     CREATE FUNCTION my_scala_udf_2()
       RETURNS DOUBLE
       LANGUAGE SCALA
       IMPORTS = ('@udf_libs/rand.jar')
       HANDLER = 'MyClass.myHandler';
     ```

     Copy code

     ```
     CREATE FUNCTION my_scala_udf_1()
       RETURNS DOUBLE
       LANGUAGE SCALA
       IMPORTS = ('@udf_libs/rand.jar')
       HANDLER = 'MyClass.myHandler';

     CREATE FUNCTION my_scala_udf_2()
       RETURNS DOUBLE
       LANGUAGE SCALA
       IMPORTS = ('@udf_libs/rand.jar')
       HANDLER = 'MyClass.myHandler';
     ```
  3. Use the following code to call both UDFs.

     The UDFs point to the same JAR file and handler. These calls create two instances of the same class. Each instance returns an
     independent value, so the example below returns two independent values, rather than returning the same value twice:

     Copy code

     ```
     SELECT my_scala_udf_1(), my_scala_udf_2() FROM table1;
     ```

## Storing JVM state information

One reason to avoid relying on dynamic shared state is that rows are not necessarily processed in a predictable order. Each time a SQL
statement is executed, Snowflake can vary the number of batches, the order in which batches are processed, and the order of rows within
a batch. If a scalar UDF is designed so that one row affects the return value for a subsequent row, then the UDF can return different
results each time that the UDF is executed.
