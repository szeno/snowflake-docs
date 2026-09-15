# Making dependencies available to your code

When your user-defined function (UDF) or stored procedure depends on code or files that are external to the UDF or procedure, you can make
the dependency available to the UDF or procedure from a stage or from a Git repository clone in Snowflake from a
[remote Git repository that Snowflake is using](/developer-guide/git/git-overview#label-integrating-git-repository-how-it-works).

For example, you might want your UDF or procedure to have access to the following:

- Python handler code in a module.
- Java or Scala handler code compiled and packaged in a JAR.
- Dependency code written in Java, Python, or Scala.
- Files to be read by your handler code and whose name and location is known when you create the UDF. This can be useful with configuration
  files, for example.

Note

You can also use the PACKAGES clause of [CREATE FUNCTION](/sql-reference/sql/create-function) or [CREATE PROCEDURE](/sql-reference/sql/create-procedure) to
import libraries that are included in Snowflake.

## High-level steps

Follow these steps to make dependencies available to your function or procedure.

1. [Choose or create a stage](#label-dependencies-choose-stage) that’s available to your handler.
2. [Upload the dependency](#label-dependencies-upload-files) to the stage.
3. [Reference the dependency](#label-dependencies-reference-dependency) with IMPORTS when you create the function or procedure.

## Choosing or creating a stage for dependency files

To make your dependency file available to a function or procedure, the file will need to be on a stage where it can be
reached at runtime. The owner of the function or procedure must have the [READ privilege](/user-guide/security-access-control-privileges#label-access-control-privileges-stage)
to the stage.

For more about creating stages, see [CREATE STAGE](/sql-reference/sql/create-stage).

You can also set up Snowflake to
[use a remote Git repository](/developer-guide/git/git-overview#label-integrating-git-repository-how-it-works), creating a Git repository clone with a full clone
of the remote repository’s files.

Note

You can’t execute the `PUT` command through the Snowflake GUI; you can use SnowSQL to execute `PUT`. For an example `PUT` command
to copy a .jar file to a stage, see [Uploading the dependency to the stage](#label-dependencies-upload-files) in this topic.

Choose or create one of the following for your dependency:

- A Git repository clone in Snowflake with files from the remote repository.

  For more information, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).
- A user or named internal stage.

  If you plan to use the `PUT` command to upload the files, use a named internal stage. For more on choosing an internal stage type,
  see [Choosing an internal stage for local files](/user-guide/data-load-local-file-system-create-stage).
- An external stage.

  External stages are locations associated with external storage services, as described in [CREATE STAGE](/sql-reference/sql/create-stage). The
  `PUT` command does not support uploading files to external stages.

If you don’t already have a user stage, named internal stage, or external stage, you can create one by executing
[CREATE STAGE](/sql-reference/sql/create-stage). For example, the following command creates a new internal stage named `mystage`:

Copy code

```
CREATE STAGE mystage;
```

Note

Snowflake does not currently support using a table stage to store handler code.

## Uploading the dependency to the stage

Upload the files required for your stored procedure to a stage.

If your handler is from [a Git repository you’re using with Snowflake](/developer-guide/git/git-overview#label-integrating-git-repository-how-it-works), you might
instead need to [fetch the latest](/developer-guide/git/git-operations#label-git-integration-refreshing-stage) from your remote repository to the Snowflake
Git repository clone.

If you’re using an external stage, use that storage service’s means for uploading files. If you’re using an internal stage, you can copy
the file from a local drive to the stage by using the `PUT` command. For command reference, see [PUT](/sql-reference/sql/put). For
information on staging files with PUT, see [Staging data files from a local file system](/user-guide/data-load-local-file-system-stage).

Use the `PUT` command to upload files to the stage.

Code in the following example uploads `myjar.jar` to a stage called `mystage`, overwriting an existing file of the same
name if it exists.

Copy code

```
PUT file:///Users/MyUserName/MyCompiledJavaCode.jar
  @mystage
  AUTO_COMPRESS = FALSE
  OVERWRITE = TRUE
  ;
```

Note

If you omit `AUTO_COMPRESS = FALSE`, the PUT command automatically compresses the file. The name of the compressed
file on the stage will be `myjar.jar.gz`. Later, when you execute a command such as
[CREATE PROCEDURE](/sql-reference/sql/create-procedure), you will need to specify the filename
with this `.gz` extension in the command’s IMPORTS clause.

Note

The PUT command does not support uploading files to external stages.
To upload files to external stages, use the utilities provided by the cloud service.

## Referencing the dependency

To make a function or procedure you’re creating aware of the dependency’s location, specify the dependency’s location in the IMPORTS
clause of the SQL you use to create the function or procedure.

If you have multiple dependency files, such as when you have third-party libraries on which a handler depends, you can specify the stage
location and file path-and-name of all dependency files as values of the IMPORTS clause.

Code in the following example creates a procedure called `MYPROC`, specifying that the file `MyCompiledJavaCode.jar` (on
the `mystage` stage) should be included in the procedure’s execution environment. In this case, `MyCompiledJavaCode.jar`
contains the procedure’s handler – the compiled code for `MyJavaClass.run`.

Copy code

```
CREATE OR REPLACE PROCEDURE MYPROC(value INT, fromTable STRING, toTable STRING, count INT)
  RETURNS INT
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:latest')
  IMPORTS = ('@mystage/MyCompiledJavaCode.jar')
  HANDLER = 'MyJavaClass.run';
```
