# Scala UDF handler project and packaging

You can make handler code projects easier to maintain by using a well-organized project hierarchy and popular build tools. These are
useful when you intend to copy handler code to a Snowflake stage, then refer to it from functions and procedures.

To build and package handler code, you can use popular tools such as sbt, Maven, and Gradle. For more information, refer to the
following topics:

- [Packaging Scala Handler Code with sbt](/developer-guide/udf-stored-procedure-build-sbt)
- [Packaging Java or Scala Handler Code with Maven](/developer-guide/udf-stored-procedure-build-maven)

Once you’ve packaged handler code, you can add it to a stage as described in [Making dependencies available to your code](/developer-guide/upload-dependencies).

For more information on choosing whether to keep your handler in-line or on a stage, refer to [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

## Organize your files

If you intend to package your handler in a JAR file and put it on a Snowflake stage, you might find it useful to use a project
hierarchy that organizes Snowflake handler code. This section suggests a hierarchy for organizing files.

For a GitHub template you can use to create a project hierarchy like this one, refer to the
[Snowflake-Labs GitHub repository](https://github.com/Snowflake-Labs/snowpark-scala-template/tree/v1.0.0).

Copy code

```
SnowflakeProject
|-- project
|   |-- plugins.sbt
|-- src
|   |-- main / scala / org / example
|   |   |-- function
|   |   |   |-- FunctionHandler.scala
|   |   |-- procedure
|   |   |-- utils
|   |-- test / scala / org / example
|   |   |-- function
|   |   |-- procedure
|-- build.sbt
|-- pom.xml
```

The following table describes the sections of the hierarchy.

| Directory/File | Description |
| --- | --- |
| `project` directory | Contains files used by sbt to guide build and packaging of code.   - `plugins.sbt` file specifies plugins used by sbt. To build code for use in Snowflake, add a plugin to help create a JAR with   your handler’s dependencies. For more information, refer to [Packaging Scala Handler Code with sbt](/developer-guide/udf-stored-procedure-build-sbt). |
| `src / main / scala / org / example` directory | Contains handler code source files.   - Use the `function` directory to hold handler source for user-defined functions (UDFs). - Use the `procedure` directory to hold handler source for stored procedures. - Use the `utils` directory to hold handler source required for both. |
| `src / test / scala / org / example` directory | Contains handler test source files.   - Use the `function` directory to hold tests for user-defined functions (UDFs). - Use the `procedure` directory to hold tests for stored procedures. |
| `build.sbt` file | Specifies the build definition used by sbt, including name and version of the built output, dependencies, and so on. For more information, refer to [Packaging Scala Handler Code with sbt](/developer-guide/udf-stored-procedure-build-sbt). |
| `pom.xml` file | Specifies the build definition used by Maven. For more information, refer to [Packaging Java or Scala Handler Code with Maven](/developer-guide/udf-stored-procedure-build-maven). |

Expand

Show lessSee more
