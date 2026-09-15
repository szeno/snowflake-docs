# Creating a Java UDF handler

This topic describes how to write the Java handler for a user-defined function (UDF). When you write a Java UDF, you write Java code for
Snowflake to execute as UDF logic. This Java code is the UDF’s handler.

You deploy the UDF with [CREATE FUNCTION](/sql-reference/sql/create-function), giving the UDF a name and specifying the Java method as the handler to use when the
UDF is called. For more information about creating a UDF with SQL, see [Creating a user-defined function](/developer-guide/udf/udf-creating-sql).

For more example code, see [Java UDF handler examples](/developer-guide/udf/java/udf-java-cookbook).

## Writing the UDF handler in Java

Use the following requirements and guidelines when writing your Java UDF handler.

- Define the class as public.
- Inside the class, declare at least one public method to use as a UDF handler.

  For an inline UDF, declare one handler method only. If instead you intend to package
  the class into a JAR as a staged handler, you can declare multiple handler methods, later
  specifying each as a handler with the HANDLER clause of a [CREATE FUNCTION](/sql-reference/sql/create-function) statement.

  For more about the difference between an in-line and staged handler, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

  You can declare other methods, if needed, to be called by the handler method.

  Use the following requirements and guidelines for each handler method:

  - Declare the handler method as public, either static or non-static.

    If the method is non-static, your class must also declare a zero-argument constructor or no constructor at all.

    Snowflake does not pass any arguments to the constructor when it instantiates the class. If the constructor throws an error, the error
    is thrown as a user error, along with the exception message.
  - Specify an appropriate return type.

    The return type must be one of the data types specified in the
    `Java Data Type` column of the [SQL-Java Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings). The return type must be
    compatible with the SQL data type specified in the RETURNS clause of the [CREATE FUNCTION](/sql-reference/sql/create-function) statement.
  - Ensure that each handler method argument (if any) is a data type specified in the `Java Data Type` column of the
    [SQL-Java Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).

    When choosing data types of Java variables, take into account the maximum and minimum possible values of the data that could be sent
    from (and returned to) Snowflake.
  - If you overload a method in a given Java class, keep in mind that Snowflake uses only the *number* of method arguments, not
    their *types*, to differentiate handler methods within a class. Resolving based on data types is impractical because some SQL
    data types can be mapped to more than one Java data type and thus potentially to more than one handler method signature.

    For example, if two Java methods in a class have the same name, the same number of arguments, and different data types,
    calling a UDF that uses one of these methods as a handler generates an error similar to the following:

    ```
    Cannot determine which implementation of handler "handler name" to invoke since there are multiple
    definitions with <number of args> arguments in function <user defined function name> with
    handler <class name>.<handler name>
    ```

    If a warehouse is available, the error is detected at the time that the UDF is created. Otherwise, the error occurs when the
    UDF is called.
  - Comply with the Snowflake-imposed constraints for Java UDFs in each handler method and methods it calls. For more on these
    constraints, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).

## Adding dependencies to the classpath

When your handler code requires classes packaged in external JAR files, you can add these dependencies to the Snowflake-managed classpath
available to your handler. The following describes how to add JAR files to the classpath visible to a Java UDF handler. For more information,
see [Making dependencies available to your code](/developer-guide/upload-dependencies).

## Organizing your files

If you plan to compile the Java code to create the JAR file yourself, you can organize the files as shown below. This example assumes that
you plan to use Java’s package mechanism.

- developmentDirectory
  - packageDirectory

    - class\_file1.java
    - class\_file2.java
  - classDirectory

    - class\_file1.class
    - class\_file2.class
  - manifest\_file.manifest (optional)
  - jar\_file.jar
  - put\_command.sql

`developmentDirectory`
:   This directory contains the project-specific files required to create your Java UDF.

`packageDirectory`
:   This directory contains the .java files to compile and include in the package.

`class_file#.java`
:   These files contain the Java source code of the UDF.

`class_file#.class`
:   These are the .class file(s) created by compiling the .java files.

`manifest_file.manifest`
:   The optional manifest file used when combining the .class files (and optionally, dependency JAR files) into the JAR file.

`jar_file.jar`
:   The JAR file that contains the UDF code.

`put_command.sql`
:   This file contains the SQL [PUT](/sql-reference/sql/put) command to copy the JAR file to a Snowflake
    [stage](/sql-reference/sql/create-stage).

### Compiling the Java code and creating the JAR file

To create a JAR file that contains the compiled Java code:

- Use javac to compile your .java file to a .class file.

  If you use a compiler newer than version 11.x, you can use the “–release” option to specify that the target version is
  version 11.
- Put your .class file into a JAR file. You can package multiple class files (and other JAR files) into your JAR file.

  For example:

  Copy code

  ```
  jar cf ./my_udf.jar MyClass.class
  ```

  A manifest file is required if your handler class is in a package, and optional otherwise. The following example
  uses a manifest file:

  Copy code

  ```
  jar cmf my_udf.manifest ./my_udf.jar example/MyClass.class
  ```

  To build the jar file with all dependencies included, you can use Maven’s `mvn package` command with
  the maven-assembly-plugin. For more information about the maven-assembly-plugin, see the
  [Maven usage page](https://maven.apache.org/plugins/maven-assembly-plugin/usage.html).

  Snowflake automatically supplies the [standard Java libraries](https://docs.oracle.com/en/java/javase/11/docs/api/index.html) (e.g. `java.util`). If your code calls those libraries,
  you do not need to include them in your JAR file.

  The methods that you call in libraries must follow the same Snowflake-imposed constraints as your Java method. For more on these
  constraints, see [Designing Handlers that Stay Within Snowflake-Imposed Constraints](/developer-guide/udf-stored-procedure-constraints).

### Copying the JAR file to your stage

In order for Snowflake to read from the JAR containing your handler method, you need to copy the JAR to one of the following kinds of stage:

- A user or named internal stage.

  Snowflake does not currently support using a table stage to store a JAR file with UDF handlers. For more on internal stages, see
  [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage).
- An external stage.

The stage hosting the JAR file must be readable by the owner of the UDF.

Typically, you upload the JAR to a named internal stage using the [PUT](/sql-reference/sql/put) command. Note that you can’t execute
the `PUT` command through the Snowflake GUI; you can use SnowSQL to execute `PUT`. See the
[Java UDF handler examples](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-examples) section for an example `PUT` command to copy a .jar file to a stage.

For more about creating stages, see [CREATE STAGE](/sql-reference/sql/create-stage).

**Caveats and Best Practices**

If you delete or rename the JAR file, you can no longer call the UDF.

If you need to update your JAR file, then:

- Update it while no calls to the UDF can be made.
- If the old .jar file is still in the stage, the `PUT` command should include the clause `OVERWRITE=TRUE`.

Note

A user performing related to UDFs must have a role that has been assigned permissions required for the action. For more information,
see [Granting privileges for user-defined functions](/developer-guide/udf/udf-access-control).
