# Writing code to support different Scala versions

You can write code to support different versions of Scala. For some Snowflake features, you’ll need to account for the Scala version you’re
using. For example, when you’re declaring a stored procedure with SQL, you’ll need to reference the Snowpark package with a name that ends
with the Scala version you’re using.

For Scala code differences between the versions, please see Scala documentation.

## Referencing Snowpark packages

When you reference the Snowpark package in your code, such as when you’re declaring a stored procedure with SQL, the package name will
depend on the following:

- The version of the Snowpark package you’re using.
- The version of Scala you’re using.

The following describes how to reference the Snowpark package for different Scala versions.

### Names for Snowpark package versions 1.16 and earlier

When referencing Snowpark package version 1.16 and earlier, you reference the package with the name `com.snowflake:snowpark` – in
other words, without the Scala version suffix.

- Scala 2.12: `com.snowflake:snowpark:1.16`
- Scala 2.13: `com.snowflake:snowpark:1.16`

### Names for Snowpark package versions 1.17 and later

When referencing the Snowpark package 1.17 and later, you reference the package with the name `com.snowflake:snowpark_<scala_version>`.

- Scala 2.12: `com.snowflake:snowpark_2.12:latest`
- Scala 2.13: `com.snowflake:snowpark_2.13:latest`

### Examples

The following examples show how to reference the Snowpark package versions 1.17 and later.

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE PROCEDURE MYPROC(value INT, fromTable STRING, toTable STRING, count INT)
  RETURNS INT
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.12'
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  IMPORTS = ('@mystage/MyCompiledJavaCode.jar')
  HANDLER = 'MyJavaClass.run';
```

Copy code

```
CREATE OR REPLACE PROCEDURE MYPROC(value INT, fromTable STRING, toTable STRING, count INT)
  RETURNS INT
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.13'
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  IMPORTS = ('@mystage/MyCompiledJavaCode.jar')
  HANDLER = 'MyJavaClass.run';
```
