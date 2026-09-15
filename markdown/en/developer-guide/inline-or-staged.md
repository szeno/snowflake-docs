# Keeping handler code in-line or on a stage

When creating a user-defined function (UDF) or stored procedure with SQL, you can specify whether the handler code is in-line with the
SQL that creates it or external to the SQL, such as in a file on a stage. This topic describes the difference.

Not all languages support using either an in-line or staged handler. For the list of supported languages, see language choice for
[stored procedures](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages) or [UDFs](/developer-guide/udf/udf-overview#label-udf-supported-languages).

## Practical differences

### In-line handler advantages

Functions and procedures with in-line handlers may be easier to manage. After using your development tools to verify that your code
works as it should, you can deploy it by copying it into the SQL statement you execute to create the function or procedure. You can
maintain the code there, updating it with a SQL statement (such as with ALTER FUNCTION or ALTER PROCEDURE) without having to maintain the
code elsewhere.

### Staged handler advantages

When using a staged handler, you can do the following:

- Use code you manage separately in a Git repository you’re using from Snowflake.

  For more information, see [How Snowflake works with a remote Git repository](/developer-guide/git/git-overview#label-integrating-git-repository-how-it-works).
- Use previously compiled code, such as when you already have compiled output but don’t have the source.
- Use handler code that might be too large to paste into the SQL statement with which you create the function or procedure.
  In-line code has an upper limit on the source code size.
- Reuse handler code from multiple functions or procedures. Staged code can contain multiple handler functions in which each function can
  be used by a different UDF or procedure. As you create multiple UDFs or procedures, they can each specify the same handler file, but
  specify a different handler function implemented in that file.

  In contrast, the handler for in-line functions or procedures typically contain only one callable function. That callable function can
  call other functions, and those other functions can be defined in the same code file or in another staged code file.
- Use existing testing and debugging tools to do most of the development work. This is particularly true
  if the code is large or complex.

## Using an in-line handler

When you’re using an in-line handler, you include the handler source code in the AS clause of the SQL statement creating the function or
procedure. For example, you would include the handler code in the AS clause of the CREATE FUNCTION or CREATE PROCEDURE statement itself.

Inside the AS clause, you surround the code with single quotes or a pair of dollar signs (`$$`). Using the double dollar signs might be
easier, such as when the source code contains embedded single quotes.

If the in-line handler source code needs to be compiled (such as with a handler written in Java or Scala), Snowflake compiles the source
and stores the output (such as a JAR file) for use later. You can optionally specify a location for a resulting output file with the
TARGET\_PATH clause.

Snowflake manages compiled output in the following ways:

- If the SQL statement (such as CREATE FUNCTION) uses TARGET\_PATH to specify a location for the output file, Snowflake compiles the
  code once and keeps the compiled output for future use.
- If the SQL statement does not specify a location for the file, Snowflake re-compiles the code for each SQL statement that
  calls the function or procedure. Snowflake automatically cleans up the file after the SQL statement finishes.

Note

As a best practice when using an in-line Java or Scala handler, consider specifying a value for the TARGET\_PATH parameter. This can
increase performance because Snowflake will reuse the compiled result of the handler code instead of recompiling the code for each
call to the procedure or UDF.

Attention

When handler code is defined in-line, it will be captured as metadata. If you do not wish to have the code captured as metadata, you can
instead deploy it in other ways, such as by using a [staged handler](#label-inline-stage-using-staged).

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated
data is entered as metadata when using the Snowflake Service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

### In-line example with Java handler

Code in the following example creates a MYPROC stored procedure with an in-line handler in Java. The handler is the `run` method of
the `MyJavaClass` class.

Copy code

```
CREATE OR REPLACE PROCEDURE MYPROC(fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:latest')
  HANDLER = 'MyJavaClass.run'
  AS
  $$
    import com.snowflake.snowpark_java.*;

    public class MyJavaClass {
      public String run(Session session, String fromTable, String toTable, int count) {
        session.table(fromTable).limit(count).write().saveAsTable(toTable);
        return "SUCCESS";
      }
    }
  $$;
```

For CREATE PROCEDURE reference information, refer to [CREATE PROCEDURE](/sql-reference/sql/create-procedure).

## Using a staged handler

When you’re using a staged handler, you use the IMPORTS clause to reference the handler at another location, such as a stage.
For example, you would specify the path to the handler with the IMPORTS clause of a SQL statement such as CREATE PROCEDURE or
CREATE FUNCTION.

When referencing the handler function name with the HANDLER clause, you must qualify the function name with the name of its containing
class or module. This is in contrast with an in-line handler, where you can sometimes simply reference the handler function by its name
alone.

### Staging a handler for use from a function or procedure

The following describes how to add a handler file to the environment in which your function or procedure executes.

1. If necessary, such as with a handler written in Java or Scala, compile and package the handler code for uploading to a stage. For more
   information on build tools, see [Packaging Handler Code](/developer-guide/udf-stored-procedure-building).

   For a handler written in Python, you can use the handler module source.

   When your handler code is written in Java or Scala, build a JAR file that contains all of the dependencies needed for your stored
   procedure. Later, you’ll need to upload the JAR file to a stage and reference the JAR file from your CREATE PROCEDURE statement.
   This process is simpler if you have fewer JAR files to upload and reference.

   - Use Maven to build a JAR file with dependencies.

     If you are using Maven to build and package your code, you can use the
     [Maven Assembly Plugin](https://maven.apache.org/plugins/maven-assembly-plugin/index.html) to create a JAR file that contains
     all of the dependencies. For more information, see [Packaging Java or Scala Handler Code with Maven](/developer-guide/udf-stored-procedure-build-maven).
   - Use other tools to build a JAR file with dependencies.

     If you are not using Maven, see the documentation for your build tool for instructions on building a JAR file with all of
     the dependencies.

     For example, if you are using an IntelliJ IDEA project, see the
     [instructions on setting up an artifact configuration](https://www.jetbrains.com/help/idea/compiling-applications.html#configure_artifact).
2. Upload the handler file to a stage as described in [Making dependencies available to your code](/developer-guide/upload-dependencies).

   If your handler is from [a Git repository you’re using with Snowflake](/developer-guide/git/git-overview#label-integrating-git-repository-how-it-works), you might
   instead need to [fetch the latest](/developer-guide/git/git-operations#label-git-integration-refreshing-stage) from your remote repository to the Snowflake
   Git repository.
3. Reference the handler file when you create the function or procedure.

   You reference the handler file in the IMPORTS clause, as described in [Referencing the dependency](/developer-guide/upload-dependencies#label-dependencies-reference-dependency).

   Code in the following example creates a UDF called `my_udf` whose handler, `MyClass.myFunction` is written in Java. The code’s
   IMPORTS clause specifies that the handler file, called `my_handler.jar`, is at the stage `mystage` in the stage’s
   subdirectory `handlers`. At runtime, Snowflake adds the handler JAR to the classpath.

   Copy code

   ```
   CREATE FUNCTION my_udf(i NUMBER)
     RETURNS NUMBER
     LANGUAGE JAVA
     IMPORTS = ('@mystage/handlers/my_handler.jar')
     HANDLER = 'MyClass.myFunction'
   ```

   For CREATE FUNCTION reference information, see [CREATE FUNCTION](/sql-reference/sql/create-function).

### Caveats and best practices

If you delete or rename the handler file, you can no longer call the function or procedure. If you need to update your handler file, then:

- First ensure that no calls are being made to the function or procedure that uses the handler.
- Use the [PUT](/sql-reference/sql/put) command to upload a new handler file. If the old handler file is still in the stage when you upload the new one,
  use the `PUT` command’s `OVERWRITE=TRUE` clause to overwrite the old handler file.
