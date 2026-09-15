# Packaging Scala Handler Code with sbt

You can use the Scala build tool (sbt) to build and package your code as an assembly JAR. You can use the
[sbt-assembly plugin](https://github.com/sbt/sbt-assembly/blob/develop/README.md) to create a JAR file containing all of the
dependencies.

Once you have a JAR file, you can upload the file to a Snowflake stage, then reference it in the IMPORTS parameter in the
[CREATE FUNCTION](/sql-reference/sql/create-function) or [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement that you use to create the function or
procedure . For more information on uploading JAR files, refer to [Making dependencies available to your code](/developer-guide/upload-dependencies). For more
information on choosing whether to have code inline or on a stage, refer to [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

To create an assembly JAR file with your handler code, use the following steps.

1. In the directory containing your `build.sbt` file, in the `project/` subdirectory, create a file named `plugins.sbt`.

   For example, if the directory containing your `build.sbt` file is `hello-snowpark/`, create the file
   `hello-snowpark/project/plugins.sbt`:

   Copy code

   ```
   hello-snowpark/
   |-- build.sbt
    |-- project/
        |-- plugins.sbt
   ```
2. In the `plugins.sbt` file, add the following line:

   Copy code

   ```
   addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "1.1.0")
   ```

   This adds the [sbt-assembly plugin](https://github.com/sbt/sbt-assembly/blob/develop/README.md) to your project.
3. If your project requires multiple versions of the same library (e.g. if your project depends on two libraries that require
   different versions of a third library), define a merge strategy in your `build.sbt` file to resolve the dependencies. See
   [Merge Strategy](https://github.com/sbt/sbt-assembly/blob/develop/README.md#merge-strategy) for details.
4. If your project requires the Snowpark library, refer to it in your `build.sbt` file with `libraryDependencies`, as shown below.
   Be sure to use at least the [minimum version required](/developer-guide/stored-procedure/scala/procedure-scala-overview#label-stored-proc-scala-prerequisites).

   Because the Snowpark library is included on Snowflake, exclude it from the JAR file by specifying that the dependency is
   `"provided"`.

   Copy code

   ```
   libraryDependencies += "com.snowflake" % "snowpark" % "1.1.0" % "provided"
   ```
5. Change to the directory for your project (e.g. `hello-snowpark`), and run the following command:

   Copy code

   ```
   sbt assembly
   ```

   Note

   If you encounter the error `Not a valid command: assembly`, `Not a valid project ID: assembly`, or
   `Not a valid key: assembly`, make sure that the `plugins.sbt` file is in the subdirectory named `project/` (as
   mentioned in step 1).

   This command creates a JAR file in the following location:

   Copy code

   ```
   target/scala-<version>/<project-name>-assembly-1.0.jar
   ```
