# CREATE FUNCTION

Creates a new [UDF (user-defined function)](/developer-guide/udf/udf-overview). Depending on how you configure it, the function can
return either scalar results or tabular results.

When you create a UDF, you specify a handler whose code is written in one of the supported languages. Depending on the handler’s language,
you can either include the handler source code in-line with the CREATE FUNCTION statement or reference the handler’s location from
CREATE FUNCTION, where the handler is precompiled or source code on a stage.

The following table lists each of the supported languages and whether its code may be kept in-line with CREATE FUNCTION or kept on a stage.
For more information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

| Language | Handler Location |
| --- | --- |
| [Java](/developer-guide/udf/java/udf-java-introduction) | In-line or staged |
| [JavaScript](/developer-guide/udf/javascript/udf-javascript-introduction) | In-line |
| [Python](/developer-guide/udf/python/udf-python-introduction) | In-line or staged |
| [Scala](/developer-guide/udf/scala/udf-scala-introduction) | In-line or staged |
| [SQL](/developer-guide/udf/sql/udf-sql-introduction) | In-line |

Expand

Show lessSee more

This command supports the following variants:

- [CREATE OR ALTER FUNCTION](#label-create-or-alter-function-syntax): Creates a function if it doesn’t exist or alters an existing function.

See also:
:   [ALTER FUNCTION](/sql-reference/sql/alter-function), [DROP FUNCTION](/sql-reference/sql/drop-function), [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions), [DESCRIBE FUNCTION](/sql-reference/sql/desc-function)

## Syntax

The syntax for CREATE FUNCTION varies depending on which language you’re using as the UDF handler.

### Java handler

Use the syntax below if the source code is in-line:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVA
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ RUNTIME_VERSION = <java_jdk_version> ]
  [ COMMENT = '<string_literal>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name_and_version>' [ , ... ] ) ]
  HANDLER = '<path_to_method>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  AS '<function_definition>'
```

Use the following syntax if the handler code will be referenced on a stage (such as in a JAR):

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVA
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ RUNTIME_VERSION = <java_jdk_version> ]
  [ COMMENT = '<string_literal>' ]
  IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] )
  HANDLER = '<path_to_method>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
```

### JavaScript handler

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

### Python handler

Use the syntax below if the source code is in-line:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] [ AGGREGATE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE PYTHON
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  RUNTIME_VERSION = <python_version>
  [ COMMENT = '<string_literal>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name>[==<version>]' [ , ... ] ) ]
  [ ARTIFACT_REPOSITORY = '<repository_name>' ]
  HANDLER = '<function_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  AS '<function_definition>'
```

Use the following syntax if the handler code will be referenced on a stage (such as in a module):

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] [ AGGREGATE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  LANGUAGE PYTHON
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  RUNTIME_VERSION = <python_version>
  [ COMMENT = '<string_literal>' ]
  [ ARTIFACT_REPOSITORY = '<repository_name>' ]
  IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] )
  [ PACKAGES = ( '<package_name>[==<version>]' [ , ... ] ) ]
  HANDLER = '<module_file_name>.<function_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
```

### Scala handler

[Preview Feature](/release-notes/preview-features) — Open

Using Scala to write a handler for a user-defined function (UDF) is a preview feature that is available to all accounts. Note that
returning a TABLE is not yet available for Scala UDF handlers.

Use the syntax below if the source code is in-line:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  LANGUAGE SCALA
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ RUNTIME_VERSION = <scala_version> ]
  [ COMMENT = '<string_literal>' ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] ) ]
  [ PACKAGES = ( '<package_name_and_version>' [ , ... ] ) ]
  HANDLER = '<path_to_method>'
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  AS '<function_definition>'
```

Use the following syntax if the handler code will be referenced on a stage (such as in a JAR):

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  LANGUAGE SCALA
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ RUNTIME_VERSION = <scala_version> ]
  [ COMMENT = '<string_literal>' ]
  IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [ , ... ] )
  HANDLER = '<path_to_method>'
```

### SQL handler

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] FUNCTION <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( <col_name> <col_data_type> [ , ... ] ) }
  [ [ NOT ] NULL ]
  [ { VOLATILE | IMMUTABLE } ]
  [ MEMOIZABLE ]
  [ COMMENT = '<string_literal>' ]
  AS '<function_definition>'
```

## Variant syntax

### CREATE OR ALTER FUNCTION

Creates a new function if it doesn’t already exist, or transforms an existing function into the function defined in the statement.
A CREATE OR ALTER FUNCTION statement follows the syntax rules of a CREATE FUNCTION statement and has the same limitations as an
[ALTER FUNCTION](/sql-reference/sql/alter-function) statement.

Supported function alterations include:

- Change function properties and parameters. For example, SECURE, MAX\_BATCH\_ROWS, LOG\_LEVEL, or COMMENT.
- Change function definition. For example, RUNTIME\_VERSION, ARTIFACT\_REPOSITORY (Python), PACKAGES, IMPORTS, return type, and function body.

For more information, see [CREATE OR ALTER FUNCTION usage notes](#label-create-or-alter-function-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE [ OR ALTER ] FUNCTION ...
```

Note

The COPY GRANTS parameter is not supported with this variant syntax.

## Required parameters

### All languages

`name ( [ arg_name arg_data_type [ DEFAULT default_value ] ] [ , ... ] )`
:   Specifies the identifier (`name`), any input arguments, and the default values for any optional arguments for the UDF.

    - For the identifier:

      - The identifier does not need to be unique for the schema in which the function is created because UDFs are
        [identified and resolved by the combination of the name and argument types](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).
      - The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
        identifier string is enclosed in double quotes (for example, “My object”). Identifiers enclosed in double quotes are also
        case-sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).
    - For the input arguments:

      - For `arg_name`, specify the name of the input argument.
      - For `arg_data_type`, use the Snowflake data type that corresponds to the handler language that you are using.

        - For [Java handlers](/developer-guide/udf/java/udf-java-introduction), see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).
        - For [JavaScript handlers](/developer-guide/udf/javascript/udf-javascript-introduction), see [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
        - For [Python handlers](/developer-guide/udf/python/udf-python-introduction), see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
        - For [Scala handlers](/developer-guide/udf/scala/udf-scala-introduction), see [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).
      - To indicate that an argument is optional, use `DEFAULT default_value` to specify the default value of the argument.
        For the default value, you can use a literal or an expression.

        If you specify any optional arguments, you must place these after the required arguments.

        If a function has optional arguments, you cannot define additional functions with the same name and different signatures.

        For details, see [Specify optional arguments](/developer-guide/udf-stored-procedure-arguments#label-procedure-function-arguments-optional).

`RETURNS ...`
:   Specifies the results returned by the UDF, which determines the UDF type:

    > - `result_data_type`: Creates a scalar UDF that returns a single value with the specified data type.
    >
    >   Note
    >
    >   For UDF handlers written in Java, Python, or Scala, the `result_data_type` must be in the `SQL Data Type` column of the
    >   following table corresponding to the handler language:
    >
    >   - [SQL-Java Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings)
    >   - [SQL-Python Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings)
    >   - [SQL-Scala Type Mappings table](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types)
    > - `TABLE ( col_name col_data_type , ... )`: Creates a table UDF that returns tabular results with the specified table column(s)
    >   and column type(s).
    >
    >   Note
    >
    >   For Scala UDFs, the TABLE return type is not supported.

`AS function_definition`
:   Defines the handler code executed when the UDF is called. The `function_definition` value must be source code in one of the
    languages supported for handlers. The code may be:

    - Java. For more information, see [Introduction to Java UDFs](/developer-guide/udf/java/udf-java-introduction).
    - JavaScript. For more information, see [Introduction to JavaScript UDFs](/developer-guide/udf/javascript/udf-javascript-introduction).
    - Python. For more information, see [Introduction to Python UDFs](/developer-guide/udf/python/udf-python-introduction).
    - Scala. For more information, see [Introduction to Scala UDFs](/developer-guide/udf/scala/udf-scala-introduction).
    - A SQL expression or Snowflake Scripting block. For more information, see
      [Introduction to SQL UDFs](/developer-guide/udf/sql/udf-sql-introduction).

    For more information, see [General usage notes](#label-create-function-usage-notes) in this topic.

    Note

    The AS clause is not required when the UDF handler code is referenced on a stage with the IMPORTS clause.

### Java

`LANGUAGE JAVA`
:   Specifies that the code is in the Java language.

`RUNTIME_VERSION = java_jdk_version`
:   Specifies the Java JDK runtime version to use. The supported versions of Java are:

    - 11.x
    - 17.x
    - 21.x

    If RUNTIME\_VERSION is not set, Java JDK 11 is used.

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [ , ... ] )`
:   The location (stage), path, and name of the directory or file(s) to import.

    A file can be a JAR file or another type of file.

    If the file is a JAR file, it can contain one or more .class files and zero or more resource files.

    Java UDFs can also read non-JAR files. For an example, see [Reading a file specified statically in IMPORTS](/developer-guide/udf/java/udf-java-cookbook#label-reading-file-from-java-udf-imports).

    If you plan to copy a file (JAR file or other file) to a stage, then Snowflake recommends using a named internal stage because the
    PUT command supports copying files to named internal stages, and the PUT command is usually the easiest way to move a JAR file
    to a stage.

    External stages are allowed, but are not supported by PUT.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different subdirectories or different stages.

    If both the IMPORTS and TARGET\_PATH clauses are present, the file name in the TARGET\_PATH clause must be different
    from each file name in the IMPORTS clause, even if the files are in different subdirectories or different stages.

    Snowflake returns an error if the TARGET\_PATH matches an existing file; you cannot use TARGET\_PATH to overwrite an existing file.

    For a UDF whose handler is on a stage, the IMPORTS clause is required because it specifies the location of the JAR file that
    contains the UDF.

    For a UDF whose handler code is in-line, the IMPORTS clause is needed only if the in-line UDF needs to access other files, such as
    libraries or text files.

    For Snowflake system packages, such as the [Snowpark package](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html),
    you can specify the package with the PACKAGES clause rather than specifying its JAR file with IMPORTS. When you do, the package
    JAR file need not be included in an IMPORTS value.

    **In-line Java**

    `AS function_definition`
    :   In-line Java UDFs require a [function definition](/sql-reference/sql/create-function#label-create-udf-function-definition).

`HANDLER = handler_name`
:   The name of the handler method or class.

    - If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following
      form: `MyClass.myMethod`.
    - If the handler is for a tabular UDF, the HANDLER value should be the name of a handler class.

### JavaScript

`LANGUAGE JAVASCRIPT`
:   Specifies that the code is in the JavaScript language.

### Python

`LANGUAGE PYTHON`
:   Specifies that the code is in the Python language.

`RUNTIME_VERSION = python_version`
:   Specifies the Python version to use. The supported versions of Python are:

    Generally available versions:

    - 3.9 (deprecated)
    - 3.10
    - 3.11
    - 3.12
    - 3.13
    - 3.14

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [ , ... ] )`
:   The location (stage), path, and name of the directory or file(s) to import.

    A file can be a `.py` file or another type of file.

    Python UDFs can also read non-Python files, such as text files. For an example, see [Reading files and assets](/developer-guide/udf/python/udf-python-examples#label-udf-python-read-files).

    If you plan to copy a file to a stage, then Snowflake recommends using a named internal stage because the
    PUT command supports copying files to named internal stages, and the PUT command is usually the easiest way to move a file
    to a stage.

    External stages are allowed, but are not supported by PUT.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different subdirectories or different stages.

    When the handler code is stored in a stage, you must use the IMPORTS clause to specify the handler code’s location.

    For an in-line Python UDF, the IMPORTS clause is needed only if the UDF handler needs to access other files, such as
    packages or text files.

    For packages included on the Snowflake system, such as [numpy](https://numpy.org/doc/stable/),
    you can specify the package with the PACKAGES clause alone, omitting the package’s source as an IMPORTS value.

`HANDLER = handler_name`
:   The name of the handler function or class.

    - If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a function name. If the handler code
      is in-line with the CREATE FUNCTION statement, you can use the function name alone. When the handler code is referenced at a stage, this
      value should be qualified with the module name, as in the following form: `my_module.my_function`.
    - If the handler is for a tabular UDF, the HANDLER value should be the name of a handler class.

### Scala

`LANGUAGE SCALA`
:   Specifies that the code is in the Scala language.

`RUNTIME_VERSION = scala_version`
:   Specifies the Scala runtime version to use. The supported versions of Scala are:

    - 2.13
    - 2.12

    For more information, see [Writing code to support different Scala versions](/developer-guide/scala-version-differences).

    If RUNTIME\_VERSION is not set, Scala 2.12 is used.

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [ , ... ] )`
:   The location (stage), path, and name of the directory or file(s) to import, such as a JAR or other kind of file.

    - The JAR file might contain handler dependency libraries. It can contain one or more .class files and zero or more resource files.
    - A non-JAR file might be a file read by handler code. For an example, see [Reading a file specified statically in IMPORTS](/developer-guide/udf/java/udf-java-cookbook#label-reading-file-from-java-udf-imports).

    If you plan to copy a file to a stage, then Snowflake recommends using a named internal stage because the PUT command supports
    copying files to named internal stages, and the PUT command is usually the easiest way to move a JAR file to a stage. External
    stages are allowed, but are not supported by PUT.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different stage subdirectories or different stages.

    If both the IMPORTS and TARGET\_PATH clauses are present, the file name in the TARGET\_PATH clause must be different
    from that of any file listed in the IMPORTS clause, even if the files are in different stage subdirectories or different stages.

    For a UDF whose handler is on a stage, the IMPORTS clause is required because it specifies the location of the JAR file that
    contains the UDF.

    For a UDF whose handler code is in-line, the IMPORTS clause is needed only if the in-line UDF needs to access other files, such as
    libraries or text files.

    For Snowflake system packages, such as the [Snowpark package](https://docs.snowflake.com/en/developer-guide/snowpark/reference/java/index.html),
    you can specify the package with the PACKAGES clause rather than specifying its JAR file with IMPORTS. When you do, the package
    JAR file need not be included in an IMPORTS value.

    **In-line Scala**

    `AS function_definition`
    :   UDFs with in-line Scala handler code require a [function definition](/sql-reference/sql/create-function#label-create-udf-function-definition).

`HANDLER = handler_name`
:   The name of the handler method or class.

    - If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following
      form: `MyClass.myMethod`.

## Optional parameters

### All languages

`SECURE`
:   Specifies that the function is secure. For more information about secure functions, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

`{ TEMP | TEMPORARY }`
:   Specifies that the function persists only for the duration of the [session](/user-guide/session-policies) that you created it in. A
    temporary function is dropped at the end of the session.

    Default: No value. If a function is not declared as `TEMPORARY`, the function is permanent.

    You cannot create temporary [user-defined functions](/developer-guide/udf/udf-overview) that have the same name as a function that already
    exists in the schema.

`[ [ NOT ] NULL ]`
:   Specifies whether the function can return NULL values or must return only NON-NULL values. The default is NULL (i.e. the function can
    return NULL).

    Note

    Currently, the `NOT NULL` clause is not enforced for SQL UDFs.
    SQL UDFs declared as `NOT NULL` can return NULL values. Snowflake recommends avoiding `NOT NULL`
    for SQL UDFs unless the code in the function is written to ensure that NULL values are never returned.

`CALLED ON NULL INPUT` or `{ RETURNS NULL ON NULL INPUT | STRICT }`
:   Specifies the behavior of the UDF when called with null inputs. In contrast to system-defined functions, which always return null when any
    input is null, UDFs can handle null inputs, returning non-null values even when an input is null:

    - `CALLED ON NULL INPUT` will always call the UDF with null inputs. It is up to the UDF to handle such values appropriately.
    - `RETURNS NULL ON NULL INPUT` (or its synonym `STRICT`) will not call the UDF if any input is null. Instead, a null value
      will always be returned for that row. Note that the UDF might still return null for non-null inputs.

    Note

    `RETURNS NULL ON NULL INPUT` (`STRICT`) is not supported for SQL UDFs. SQL UDFs effectively use
    `CALLED ON NULL INPUT`. In your SQL UDFs, you must handle null input values.

    Default: `CALLED ON NULL INPUT`

`{ VOLATILE | IMMUTABLE }`
:   Specifies the behavior of the UDF when returning results:

    > - `VOLATILE`: UDF might return different values for different rows, even for the same input (e.g. due to non-determinism and
    >   statefulness).
    > - `IMMUTABLE`: UDF assumes that the function, when called with the same inputs, will always return the same result. This guarantee
    >   is not checked. Specifying `IMMUTABLE` for a UDF that returns different values for the same input will result in undefined
    >   behavior.

    Default: `VOLATILE`

    Note

    IMMUTABLE is not supported on an aggregate function (when you use the AGGREGATE parameter). Therefore, all aggregate functions are
    VOLATILE by default.

`COMMENT = 'string_literal'`
:   Specifies a comment for the UDF, which is displayed in the DESCRIPTION column in the [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions)
    output.

    Default: `user-defined function`

`COPY GRANTS`
:   Specifies to retain the access privileges from the original function when a new function is created using CREATE OR REPLACE FUNCTION.

    The parameter copies all privileges, except OWNERSHIP, from the existing function to the new function. The new function will
    inherit any future grants defined for the object type in the schema. By default, the role that executes the CREATE FUNCTION
    statement owns the new function.

    Note:

    - With [data sharing](/user-guide/data-sharing-gs), if the existing function was shared to another account, the replacement function is
      also shared.
    - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement function lists the grantee for the copied privileges as the
      role that executed the CREATE FUNCTION statement, with the current timestamp when the statement was executed.
    - The operation to copy grants occurs atomically in the CREATE FUNCTION command (i.e. within the same transaction).

### Java

`PACKAGES = ( 'package_name_and_version' [ , ... ] )`
:   The name and version number of Snowflake system packages required as dependencies. The value should be of the form
    `package_name:version_number`, where `package_name` is `snowflake_domain:package`. Note that you can
    specify `latest` as the version number in order to have Snowflake use the latest version available on the system.

    For example:

    Copy code

    ```
    -- Use version 1.2.0 of the Snowpark package.
    PACKAGES=('com.snowflake:snowpark:1.2.0')

    -- Use the latest version of the Snowpark package.
    PACKAGES=('com.snowflake:snowpark:latest')
    ```

    You can discover the list of supported system packages by executing the following SQL in Snowflake:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'java';
    ```

    For a dependency you specify with PACKAGES, you do not need to also specify its JAR file in an IMPORTS clause.

    **In-line Java**

    `TARGET_PATH = stage_path_and_file_name_to_write`
    :   Specifies the location to which Snowflake should write the JAR file containing the result of compiling the handler source code specified
        in the `function_definition`.

        If this clause is included, Snowflake writes the resulting JAR file to the stage location specified by the clause’s value. If this
        clause is omitted, Snowflake re-compiles the source code each time the code is needed. In that case, the JAR file is not stored
        permanently, and the user does not need to clean up the JAR file.

        Snowflake returns an error if the TARGET\_PATH matches an existing file; you cannot use TARGET\_PATH to overwrite an
        existing file.

        The generated JAR file remains until you explicitly delete it, even if you drop the function. When you drop the UDF you should
        separately remove the JAR file because the JAR is no longer needed to support the UDF.

        For example, the following TARGET\_PATH example would result in a `myhandler.jar` file generated and copied to the
        `handlers` stage.

        Copy code

        ```
        TARGET_PATH = '@handlers/myhandler.jar'
        ```

        When you drop this UDF to remove it, you’ll also need to remove its handler JAR file, such as by executing the
        [REMOVE command](/sql-reference/sql/remove).

        Copy code

        ```
        REMOVE @handlers/myhandler.jar;
        ```

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for this
    function’s handler code to access external networks.

    An external access integration specifies [network rules](/sql-reference/sql/create-network-rule) and
    [secrets](/sql-reference/sql/create-secret) that specify external locations and credentials (if any) allowed for use by handler code
    when making requests of an external network, such as an external REST API.

`SECRETS = ( 'secret_variable_name' = secret_name [ , ... ] )`
:   Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from
    secrets in handler code.

    Secrets you specify here must be allowed by the [external access integration](/sql-reference/sql/create-external-access-integration)
    specified as a value of this CREATE FUNCTION command’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter.

    This parameter’s value is a comma-separated list of assignment expressions with the following parts:

    - `secret_name` as the name of the allowed secret.

      You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the
      EXTERNAL\_ACCESS\_INTEGRATIONS parameter.
    - `'secret_variable_name'` as the variable that will be used in handler code when retrieving information from the secret.

    For more information, including an example, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

### Python

`AGGREGATE`
:   Specifies that the function is an aggregate function. For more information about user-defined aggregate functions, see
    [Python user-defined aggregate functions](/developer-guide/udf/python/udf-python-aggregate-functions).

    Note

    IMMUTABLE is not supported on an aggregate function (when you use the AGGREGATE parameter). Therefore, all aggregate functions are
    VOLATILE by default.

`ARTIFACT_REPOSITORY = repository_name`
:   Specifies the name of the repository to use for installing PyPI packages for use by your function.

    Snowflake installs these packages from the artifact repository.

`PACKAGES = ( 'package_name_and_version' [ , ... ] )`
:   The name and version number of packages required as dependencies. The value should be of the form
    `package_name==version_number`. If you omit the version number, Snowflake will use the latest package available on the
    system.

    For example:

    Copy code

    ```
    -- Use version 1.2.2 of the NumPy package.
    PACKAGES=('numpy==1.2.2')

    -- Use the latest version of the NumPy package.
    PACKAGES=('numpy')
    ```

    You can discover the list of supported system packages by executing the following SQL in Snowflake:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'python';
    ```

    For more information about included packages, see [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

    You can specify package versions by using these version
    specifiers: `==`, `<=`, `>=`, `<`, or `>`.

    For example:

    Copy code

    ```
    -- Use version 1.2.3 or higher of the NumPy package.
    PACKAGES=('numpy>=1.2.3')
    ```

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for this
    function’s handler code to access external networks.

    An external access integration specifies [network rules](/sql-reference/sql/create-network-rule) and
    [secrets](/sql-reference/sql/create-secret) that specify external locations and credentials (if any) allowed for use by handler code
    when making requests of an external network, such as an external REST API.

`SECRETS = ( 'secret_variable_name' = secret_name [ , ... ] )`
:   Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from
    secrets in handler code.

    Secrets you specify here must be allowed by the [external access integration](/sql-reference/sql/create-external-access-integration)
    specified as a value of this CREATE FUNCTION command’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter

    This parameter’s value is a comma-separated list of assignment expressions with the following parts:

    - `secret_name` as the name of the allowed secret.

      You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the
      EXTERNAL\_ACCESS\_INTEGRATIONS parameter.
    - `'secret_variable_name'` as the variable that will be used in handler code when retrieving information from the secret.

    For more information, including an example, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

### SQL

`MEMOIZABLE`
:   Specifies that the function is memoizable.

    For more information, see [Memoizable UDFs](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable).

### Scala

`PACKAGES = ( 'package_name_and_version' [ , ... ] )`
:   The name and version number of Snowflake system packages required as dependencies. The value should be of the form
    `package_name:version_number`, where `package_name` is `snowflake_domain:package`. Note that you can
    specify `latest` as the version number in order to have Snowflake use the latest version available on the system.

    For example:

    Copy code

    ```
    -- Use version 1.7.0 of the Snowpark package.
    PACKAGES=('com.snowflake:snowpark:1.7.0')

    -- Use the latest version of the Snowpark package.
    PACKAGES=('com.snowflake:snowpark:latest')
    ```

    You can discover the list of supported system packages by executing the following SQL in Snowflake:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'scala';
    ```

    For a dependency you specify with PACKAGES, you do not need to also specify its JAR file in an IMPORTS clause.

    `TARGET_PATH = stage_path_and_file_name_to_write`
    :   Specifies the location to which Snowflake should write the JAR file containing the result of compiling the handler source code specified
        in the `function_definition`.

        If this clause is included, Snowflake writes the resulting JAR file to the stage location specified by the clause’s value. If this
        clause is omitted, Snowflake re-compiles the source code each time the code is needed. In that case, the JAR file is not stored
        permanently, and the user does not need to clean up the JAR file.

        Snowflake returns an error if the TARGET\_PATH matches an existing file; you cannot use TARGET\_PATH to overwrite an
        existing file.

        The generated JAR file remains until you explicitly delete it, even if you drop the function. When you drop the UDF you should
        separately remove the JAR file because the JAR is no longer needed to support the UDF.

        For example, the following TARGET\_PATH example would result in a `myhandler.jar` file generated and copied to the
        `handlers` stage.

        Copy code

        ```
        TARGET_PATH = '@handlers/myhandler.jar'
        ```

        When you drop this UDF to remove it, you’ll also need to remove its handler JAR file, such as by executing the
        [REMOVE command](/sql-reference/sql/remove).

        Copy code

        ```
        REMOVE @handlers/myhandler.jar;
        ```

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FUNCTION | Schema | The privilege only enables the creation of user-defined functions in the schema.  If you want to enable the creation of data metric functions, the role must have the CREATE DATA METRIC FUNCTION privilege. |
| USAGE | Function | Granting the USAGE privilege on the newly created function to a role allows users with that role to call the function elsewhere in Snowflake (such as masking policy owner role for External Tokenization). |
| USAGE | External access integration | Required on integrations, if any, specified by the EXTERNAL\_ACCESS\_INTEGRATIONS parameter. For more information, see [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration). |
| READ | Secret | Required on secrets, if any, specified by the SECRETS parameter. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |
| USAGE | Schema | Required on schemas containing secrets, if any, specified by the SECRETS parameter. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

# All languages

- The definition for a UDF is limited to 1MB.
- The delimiters around the `function_definition` can be either single quotes or a pair of dollar signs.

  Using `$$` as the delimiter makes it easier to write functions that contain single quotes.

  If the delimiter for the body of the function is the single quote character,
  then any single quotes within `function_definition` (such as string
  literals) must be escaped by single quotes.
- If using a UDF in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the data type of the column, UDF, and masking policy match. For
  more information, see [User-defined functions in a masking policy](/user-guide/security-column-intro#label-security-column-intro-udf-policy).
- If you specify the [CURRENT\_DATABASE](/sql-reference/functions/current_database) or [CURRENT\_SCHEMA](/sql-reference/functions/current_schema) function in the
  handler code of the UDF, the function returns the database or schema that contains the UDF, not the database or schema in use for
  the session.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Setting LOG\_LEVEL or TRACE\_LEVEL as properties in a CREATE FUNCTION statement is not supported. To set these properties
  on a function, use [ALTER FUNCTION](/sql-reference/sql/alter-function) after creating the function, or use
  [CREATE OR ALTER FUNCTION](/sql-reference/sql/create-function#label-create-or-alter-function-syntax).

## Java

- In Java, primitive data types don’t allow NULL values, so passing a NULL for an argument of such a type results in
  an error.
- In the HANDLER clause, the method name is case-sensitive.
- In the IMPORTS and TARGET\_PATH clauses:

  - Package, class, and file name(s) are case-sensitive.
  - Stage name(s) are case-insensitive.
- You can use the PACKAGES clause to specify package names and version numbers for Snowflake system-defined dependencies, such as those
  from Snowpark. For other dependencies, specify dependency JAR files with the IMPORTS clause.
- Snowflake validates that:

  - The JAR file specified in the CREATE FUNCTION statement’s HANDLER exists and contains the specified
    class and method.
  - The input and output types specified in the UDF declaration are compatible with the input and output types
    of the Java method.

  Validation can be done at creation time or execution time, depending on whether you are connected to an active Snowflake warehouse.

  - Creation time — If you are connected to an active Snowflake warehouse at the time the CREATE FUNCTION statement is
    executed, the UDF is validated at creation time.
  - Execution time — If you are not connected to an active Snowflake warehouse, the UDF is created, but is not validated
    immediately, and Snowflake returns the following message:

    `Function name created successfully, but could not be validated since there is no active warehouse`.

## JavaScript

- Snowflake does not validate JavaScript code at UDF creation time. In other words, creation of the UDF succeeds regardless of whether
  the code is valid. If the code is not valid, Snowflake returns errors when the UDF is called at query time.

## Python

- In the HANDLER clause, the handler function name is case-sensitive.
- In the IMPORTS clause:

  - File name(s) are case-sensitive.
  - Stage name(s) are case-insensitive.
- You can use the PACKAGES clause to specify package names and version numbers for dependencies, such as those
  from Snowpark. For other dependencies, specify dependency files with the IMPORTS clause.
- Snowflake validates that:

  - The function or class specified in the CREATE FUNCTION statement’s HANDLER exists.
  - The input and output types specified in the UDF declaration are compatible with the input and output types
    of the handler.

## Scala

- In the HANDLER clause, the method name is case-sensitive.
- In the IMPORTS and TARGET\_PATH clauses:

  - Package, class, and file name(s) are case-sensitive.
  - Stage name(s) are case-insensitive.
- You can use the PACKAGES clause to specify package names and version numbers for Snowflake system-defined dependencies, such as those
  from Snowpark. For other dependencies, specify dependency JAR files with the IMPORTS clause.
- Snowflake validates that:

  - The JAR file specified in the CREATE FUNCTION statement’s HANDLER exists and contains the specified
    class and method.
  - The input and output types specified in the UDF declaration are compatible with the input and output types
    of the Scala method.

  Validation can be done at creation time or execution time, depending on whether you are connected to an active Snowflake warehouse.

  - Creation time — If you are connected to an active Snowflake warehouse at the time the CREATE FUNCTION statement is
    executed, the UDF is validated at creation time.
  - Execution time — If you are not connected to an active Snowflake warehouse, the UDF is created, but is not validated
    immediately, and Snowflake returns the following message:

    `Function name created successfully, but could not be validated since there is no active warehouse`.

## SQL

- Currently, the NOT NULL clause is not enforced for SQL UDFs.

## CREATE OR ALTER FUNCTION usage notes

- All limitations of the [ALTER FUNCTION](/sql-reference/sql/alter-function) command apply.
- You cannot replace or transform a FUNCTION with a PROCEDURE or a PROCEDURE with a FUNCTION.
- You cannot replace or transform a temporary FUNCTION with a non-temporary FUNCTION, or a non-temporary FUNCTION with a temporary FUNCTION.
- You cannot replace or transform a regular FUNCTION with an EXTERNAL FUNCTION, or an EXTERNAL FUNCTION with a regular FUNCTION.
- Changing the LANGUAGE, HANDLER, VOLATILITY, NULL\_HANDLING, TARGET\_PATH properties, and the function input arguments is not supported.
- Setting or unsetting a tag is not supported. Existing tags are not altered by a CREATE OR ALTER FUNCTION statement and remain unchanged.

## Examples

### Java

Here is a basic example of CREATE FUNCTION with an in-line handler:

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE JAVA
  CALLED ON NULL INPUT
  HANDLER = 'TestFunc.echoVarchar'
  TARGET_PATH = '@~/testfunc.jar'
  AS
  'class TestFunc {
    public static String echoVarchar(String x) {
      return x;
    }
  }';
```

Here is a basic example of CREATE FUNCTION with a reference to a staged handler:

Copy code

```
create function my_decrement_udf(i numeric(9, 0))
    returns numeric
    language java
    imports = ('@~/my_decrement_udf_package_dir/my_decrement_udf_jar.jar')
    handler = 'my_decrement_udf_package.my_decrement_udf_class.my_decrement_udf_method'
    ;
```

For more examples of Java UDFs, see [examples](/developer-guide/udf/java/udf-java-cookbook#label-udf-java-examples).

### JavaScript

Create a JavaScript UDF named `js_factorial`:

Copy code

```
CREATE OR REPLACE FUNCTION js_factorial(d double)
  RETURNS double
  LANGUAGE JAVASCRIPT
  STRICT
  AS '
  if (D <= 0) {
    return 1;
  } else {
    var result = 1;
    for (var i = 2; i <= D; i++) {
      result = result * i;
    }
    return result;
  }
  ';
```

### Python

Code in the following example creates a `py_udf` function whose handler code is in-line as `udf`.

Copy code

```
CREATE OR REPLACE FUNCTION py_udf()
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.10'
  PACKAGES = ('numpy','pandas','xgboost==1.5.0')
  HANDLER = 'udf'
AS $$
import numpy as np
import pandas as pd
import xgboost as xgb
def udf():
    return [np.__version__, pd.__version__, xgb.__version__]
$$;
```

Code in the following example creates a `dream` function whose handler is in a `sleepy.py` file located on the
`@my_stage` stage.

Copy code

```
CREATE OR REPLACE FUNCTION dream(i int)
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.10'
  HANDLER = 'sleepy.snore'
  IMPORTS = ('@my_stage/sleepy.py')
```

### Scala

Here is a basic example of CREATE FUNCTION with an in-line handler:

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  HANDLER='Echo.echoVarchar'
  AS
  $$
  class Echo {
    def echoVarchar(x : String): String = {
      return x
    }
  }
  $$;
```

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  HANDLER='Echo.echoVarchar'
  AS
  $$
  class Echo {
    def echoVarchar(x : String): String = {
      return x
    }
  }
  $$;
```

Here is a basic example of CREATE FUNCTION with a reference to a staged handler:

Scala 2.12Scala 2.13

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  IMPORTS = ('@udf_libs/echohandler.jar')
  HANDLER='Echo.echoVarchar';
```

Copy code

```
CREATE OR REPLACE FUNCTION echo_varchar(x VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  IMPORTS = ('@udf_libs/echohandler.jar')
  HANDLER='Echo.echoVarchar';
```

For more examples of Scala UDFs, see [Scala UDF handler examples](/developer-guide/udf/scala/udf-scala-examples).

### SQL

Create a simple SQL scalar UDF that returns a hard-coded approximation of the
mathematical constant pi:

Copy code

```
CREATE FUNCTION pi_udf()
  RETURNS FLOAT
  AS '3.141592654::FLOAT'
  ;
```

Create a simple SQL table UDF that returns hard-coded values:

Copy code

```
CREATE FUNCTION simple_table_function ()
  RETURNS TABLE (x INTEGER, y INTEGER)
  AS
  $$
    SELECT 1, 2
    UNION ALL
    SELECT 3, 4
  $$
  ;
```

Copy code

```
SELECT * FROM TABLE(simple_table_function());
```

Output:

Copy code

```
SELECT * FROM TABLE(simple_table_function());
+---+---+
| X | Y |
|---+---|
| 1 | 2 |
| 3 | 4 |
+---+---+
```

Create a UDF that accepts multiple parameters:

Copy code

```
CREATE FUNCTION multiply1 (a number, b number)
  RETURNS number
  COMMENT='multiply two numbers'
  AS 'a * b';
```

Create a SQL table UDF named `get_countries_for_user` that returns the results of a query:

Copy code

```
CREATE OR REPLACE FUNCTION get_countries_for_user ( id NUMBER )
  RETURNS TABLE (country_code CHAR, country_name VARCHAR)
  AS 'SELECT DISTINCT c.country_code, c.country_name
      FROM user_addresses a, countries c
      WHERE a.user_id = id
      AND c.country_code = a.country_code';
```

### Create and alter a simple function using the CREATE OR ALTER FUNCTION command

Create a function `multiply` that accepts two numbers:

Copy code

```
CREATE OR ALTER FUNCTION multiply(a NUMBER, b NUMBER)
  RETURNS NUMBER
  AS 'a * b';
```

Alter `multiply` to add a comment and make the function secure:

Copy code

```
CREATE OR ALTER SECURE FUNCTION multiply(a NUMBER, b NUMBER)
  RETURNS NUMBER
  COMMENT = 'Multiply two numbers.'
  AS 'a * b';
```
