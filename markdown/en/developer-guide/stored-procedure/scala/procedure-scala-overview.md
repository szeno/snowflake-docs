# Writing Scala handlers for stored procedures created with SQL

You can create a stored procedure whose handler is written in Scala. You can use the Snowpark library within your stored procedure to
perform queries, updates, and other work on tables in Snowflake.

With stored procedures, you can build and run your data pipeline within Snowflake, using a Snowflake warehouse as the
compute framework. For the code for your data pipeline, you use the Snowpark API for Scala to write stored procedures. To schedule
the execution of these stored procedures, you use [tasks](/user-guide/tasks-intro).

You can capture log and trace data as your handler code executes. For more information, refer to
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

## Write a Scala handler for a stored procedure

1. Make sure your environment meets the [prerequisites](#label-stored-proc-scala-prerequisites).
2. If you’re developing locally, [set up your environment to use Snowpark](#label-stored-proc-scala-setup).
3. Choose whether to deploy your handler [inline or on a stage](/developer-guide/inline-or-staged).
4. Follow guidelines for the handler [class or object](#label-stored-proc-scala-writing-class),
   [method or function](#label-stored-proc-scala-writing-method),
   and [performance](#label-stored-proc-scala-planning).
5. Implement support for features such as [data access](/developer-guide/stored-procedure/scala/procedure-scala-access-data),
   [file reading](/developer-guide/stored-procedure/scala/procedure-scala-read-files),
   [returning tabular data](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data), and
   [logging and tracing](/developer-guide/logging-tracing/logging-scala).
6. Make your code’s [dependencies available on Snowflake](#label-stored-proc-scala-writing-access-jars).
7. Include your handler code inline or imported from a stage when you
   [create the stored procedure](/developer-guide/stored-procedure/stored-procedures-creating).

Note

To both create and call an anonymous procedure, use [CALL (with anonymous procedure)](/sql-reference/sql/call-with). Creating and calling an anonymous procedure does
not require a role with CREATE PROCEDURE schema privileges.

## Meet prerequisites

Snowflake currently supports the following versions of Scala:

- 2.13
- 2.12

For more information, see [Writing code to support different Scala versions](/developer-guide/scala-version-differences).

You must use version 1.1.0 or a more recent version of the Snowpark library.

If you are writing a stored procedure whose handler code will be copied to a stage, you must compile your classes to run in one of
the following Java versions:

- 11.x
- 17.x
- 21.x

## Set up your development environment for Snowpark

If you’re developing your code locally, set up your development environment to use the Snowpark library. See
[Setting Up Your Development Environment for Snowpark Scala](/developer-guide/snowpark/scala/setup).

### Structure and building handler code

You can keep handler source code inline with the SQL that creates the procedure or keep the handler’s compiled results in a separate location
and reference it from the SQL. For more information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

For more on building handler source code for use with a procedure, see [Packaging Handler Code](/developer-guide/udf-stored-procedure-building).

## Guidelines for the handler class or object

When writing the handler class or object, note the following:

- The class (or object) and method must not be protected or private.
- If the method is not static and you want to define a constructor, define a zero-argument constructor for the class.
  Snowflake invokes this zero-argument constructor at initialization time to create an instance of your class.
- You can define different methods for different stored procedures in the same class or object.

## Guidelines for the handler method or function

When writing the method or function for a stored procedure, note the following:

- Specify the Snowpark `Session` object as the first argument of your method or function.

  When you call your stored procedure, Snowflake automatically creates a `Session` object and passes it to your stored
  procedure. (You cannot create the `Session` object yourself.)
- For the rest of the arguments and for the return value, use the [Scala types](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types) that
  correspond to [Snowflake data types](/sql-reference-data-types).
- Your method or function must return a value.
- Stored procedure execution times out unless the timer is reset by the code’s activity. In particular, the timeout timer is reset
  by the code’s interactions with data, including file operations, queries, and iterating through a result set.
- When you run an [asynchronous child job](/developer-guide/snowpark/scala/working-with-dataframes#label-snowpark-dataframe-action-method-async) from within a procedure’s handler, “fire
  and forget” is not supported.

  In other words, if the handler issues a child query that is still running when the parent procedure job completes, the child job is
  canceled automatically.

## Guidelines for handler performance and security

To ensure that your code runs well on Snowflake, follow these guidelines:

- Limit the amount of memory consumed.

  Snowflake places limits on a method in terms of the amount of memory needed. For more information on how to avoid consuming too much,
  see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).
- Write thread-safe code.

  Make sure that your handler method or function is thread safe.
- Understand the security restrictions.

  Your handler code runs within a restricted engine, so be sure to follow the rules described in
  [Security Practices for UDFs and Procedures](/developer-guide/udf-stored-procedure-security-practices).
- Decide on using owner’s rights or caller’s rights.

  When planning to write your stored procedure, consider whether you want the stored procedure to run with
  [caller’s rights or owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights).
- Keep in mind the timeout behavior for stored procedures.

  Stored procedure execution times out unless the timer is reset by the code’s activity. In particular, the timeout timer is reset
  by the code’s interactions with data, including file operations, queries, and iterating through a result set.

## Make dependencies available to your code

If your handler code depends on code defined outside the handler itself (such as classes in a JAR file) or on resource files, you can make
those dependencies available to your code by uploading them to a stage. When
[creating the procedure](/developer-guide/stored-procedure/stored-procedures-creating), you can reference these dependencies using the IMPORTS
clause.

For more information, see [Making dependencies available to your code](/developer-guide/upload-dependencies).
