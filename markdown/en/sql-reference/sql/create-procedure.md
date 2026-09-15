# CREATE PROCEDURE

Creates a new [stored procedure](/developer-guide/stored-procedure/stored-procedures-usage).

A procedure can be written in one of the following languages:

- [Java (using Snowpark)](/developer-guide/stored-procedure/java/procedure-java-overview)
- [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript)
- [Python (using Snowpark)](/developer-guide/stored-procedure/python/procedure-python-overview)
- [Scala (using Snowpark)](/developer-guide/stored-procedure/scala/procedure-scala-overview)
- [Snowflake Scripting](/developer-guide/snowflake-scripting/index)

Note

When you want to create and call a procedure that is anonymous (rather than stored), use [CALL (with anonymous procedure)](/sql-reference/sql/call-with).
Creating an anonymous procedure does not require a role with CREATE PROCEDURE schema privileges.

This command supports the following variants:

- [CREATE OR ALTER PROCEDURE](#label-create-or-alter-procedure-syntax): Creates a new procedure if it doesn’t exist or alters an existing procedure.

See also:
:   [ALTER PROCEDURE](/sql-reference/sql/alter-procedure), [DROP PROCEDURE](/sql-reference/sql/drop-procedure), [SHOW PROCEDURES](/sql-reference/sql/show-procedures), [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure), [CALL](/sql-reference/sql/call),
    [SHOW USER PROCEDURES](/sql-reference/sql/show-user-procedures)

## Syntax

### Java handler

You can create a stored procedure that either includes its handler code in-line, or refers to its handler code in a JAR file. For more
information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

For examples of Java stored procedures, see [Writing Java handlers for stored procedures created with SQL](/developer-guide/stored-procedure/java/procedure-java-overview).

[Preview Feature](/release-notes/preview-features) — Open

Using tabular stored procedures with a [Java handler](/developer-guide/stored-procedure/java/procedure-java-tabular-data) is a preview feature
that is available to all accounts.

For in-line stored procedures, use the following syntax:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE JAVA
  RUNTIME_VERSION = '<java_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
  AS '<procedure_definition>'
```

For a stored procedure that uses a precompiled handler, use the following syntax.

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE JAVA
  RUNTIME_VERSION = '<java_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
```

### JavaScript handler

For examples of JavaScript stored procedures, see [Writing stored procedures in JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript).

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS <result_data_type> [ NOT NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
  AS '<procedure_definition>'
```

Important

JavaScript is case-sensitive, whereas SQL is not. See [Case-sensitivity in JavaScript arguments](/developer-guide/stored-procedure/stored-procedures-javascript#label-considerations-for-case-sensitivity-in-stored-procedures) for
important information about using stored procedure argument names in the JavaScript code.

### Python handler

For examples of Python stored procedures, see [Writing stored procedures with SQL and Python](/developer-guide/stored-procedure/python/procedure-python-overview).

For in-line stored procedures, use the following syntax:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<python_version>'
  [ ARTIFACT_REPOSITORY = `<repository_name>` ]
  [ PACKAGES = ( '<package_name>' [ , ... ] ) ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<function_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER }]
  AS '<procedure_definition>'
```

For a stored procedure in which the code is in a file on a stage, use the following syntax:

Copy code

```
CREATE [ OR REPLACE ] [ { TEMP | TEMPORARY } ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<python_version>'
  [ ARTIFACT_REPOSITORY = `<repository_name>` ]
  [ PACKAGES = ( '<package_name>' [ , ... ] ) ]
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<module_file_name>.<function_name>'
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <name_of_integration> [ , ... ] ) ]
  [ SECRETS = ('<secret_variable_name>' = <secret_name> [ , ... ] ) ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
```

### Scala handler

You can create a stored procedure that either includes its handler code in-line, or refers to its handler code in a JAR file. For more
information, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

For examples of Scala stored procedures, see [Writing Scala handlers for stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-overview).

[Preview Feature](/release-notes/preview-features) — Open

Using tabular stored procedures with a [Scala handler](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data) via `RETURNS TABLE(...)`
is a preview feature that is available to all accounts.

For in-line stored procedures, use the following syntax:

Copy code

```
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE SCALA
  RUNTIME_VERSION = '<scala_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark_<scala_version>:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ TARGET_PATH = '<stage_path_and_file_name_to_write>' ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
  AS '<procedure_definition>'
```

For a stored procedure that uses a precompiled handler, use the following syntax.

Copy code

```
CREATE [ OR REPLACE ] [ SECURE ] PROCEDURE <name> (
    [ <arg_name> <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE SCALA
  RUNTIME_VERSION = '<scala_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark_<scala_version>:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ VOLATILE | IMMUTABLE ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
```

### Snowflake Scripting handler

For examples of Snowflake Scripting stored procedures, see [Writing stored procedures in Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting).

Copy code

```
CREATE [ OR REPLACE ] PROCEDURE <name> (
    [ <arg_name> [ { IN | INPUT | OUT | OUTPUT } ] <arg_data_type> [ DEFAULT <default_value> ] ] [ , ... ] )
  [ COPY GRANTS ]
  RETURNS { <result_data_type> | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  [ NOT NULL ]
  LANGUAGE SQL
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ] -- Note: VOLATILE and IMMUTABLE are deprecated.
  [ COMMENT = '<string_literal>' ]
  [ EXECUTE AS { OWNER | CALLER | RESTRICTED CALLER } ]
  AS <procedure_definition>
```

### Procedure-scoped temporary tables (Snowflake Scripting)

Inside the body of a Snowflake Scripting stored procedure (`LANGUAGE SQL`), you can create a temporary table that exists only for the
current procedure execution by running the following statement:

Copy code

```
CREATE [ OR REPLACE ] PROCEDURE SCOPED { TEMP | TEMPORARY } TABLE <table_name> ( <col_name> <col_data_type> [ , ... ] ) ;
```

Although this statement begins with `CREATE PROCEDURE`, it does not define a nested stored procedure. It declares a
[procedure-scoped temporary table](/user-guide/tables-temp-transient#label-tables-temp-procedure-scoped) named `table_name` with the defined columns.

The table is visible only within the same procedure execution and is dropped automatically when that execution finishes. It is not the same as a
[session-scoped temporary table](/user-guide/tables-temp-transient#label-table-type-temporary) created with [CREATE TEMPORARY TABLE](/sql-reference/sql/create-table), which persists for the
remainder of the [session](/user-guide/session-policies).

You can run this form of `CREATE PROCEDURE` more than once in a procedure body to declare additional procedure-scoped temporary tables. Each
`table_name` must be unique among procedure-scoped temporary tables in that procedure.

For an example, see [procedure-scoped temporary table example](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedures-snowscript-scoped-temp-table).

Note

If you are creating a Snowflake Scripting procedure in SnowSQL or Snowsight, you must
use [string literal delimiters](/sql-reference/data-types-text#label-quoted-string-constants) (`'` or `$$`) around
`{procedure definition}`. See [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

## Variant syntax

### CREATE OR ALTER PROCEDURE

Creates a new procedure if it doesn’t already exist, or transforms an existing procedure into the procedure defined in the
statement. A CREATE OR ALTER PROCEDURE statement follows the syntax rules of a CREATE PROCEDURE statement and has the same
limitations as an [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) statement.

Alterations to the following are supported:

- LOG\_LEVEL, TRACE\_LEVEL, COMMENT, SECURE, return type, and the procedure body.
- SECRETS, EXTERNAL\_ACCESS\_INTEGRATIONS, RUNTIME\_VERSION, IMPORTS, and PACKAGES for Python, Scala, and Java stored procedures; also ARTIFACT\_REPOSITORY for Python stored procedures.
- Execution privileges (EXECUTE AS CALLER or EXECUTE AS OWNER)

For more information, see [CREATE OR ALTER PROCEDURE usage notes](#label-create-or-alter-procedure-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE [ OR ALTER ] PROCEDURE ...
```

## Required parameters

### All languages

`name ( [ arg_name [ { IN | INPUT | OUT | OUTPUT } ] arg_data_type` *[ DEFAULT {default\_value} ] ] [ , … ] )*
:   Specifies the identifier (`name`), any arguments, and the default values for any optional arguments for the
    stored procedure.

    - For the identifier:

      - The identifier does not need to be unique for the schema in which the procedure is created because stored procedures are
        [identified and resolved by the combination of the name and argument types](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).
      - The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
        identifier string is enclosed in double quotes (e.g. “My object”). Identifiers enclosed in double quotes are also
        case-sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).
    - For the arguments:

      - For `arg_name`, specify the name of the argument.
      - For `{ IN | INPUT | OUT | OUTPUT }`, specify the type of the argument (input or output). The type specification is only valid
        for a Snowflake Scripting stored procedure. For more information, see [Using arguments passed to a stored procedure](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-arguments).
      - For `arg_data_type`, use the Snowflake data type that corresponds to the language that you are using.

        - For [Java stored procedures](/developer-guide/stored-procedure/java/procedure-java-overview), see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).
        - For [JavaScript stored procedures](/developer-guide/stored-procedure/stored-procedures-javascript), see
          [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
        - For [Python stored procedures](/developer-guide/stored-procedure/python/procedure-python-overview), see
          [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
        - For [Scala stored procedures](/developer-guide/stored-procedure/scala/procedure-scala-overview), see [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).

        - For Snowflake Scripting, a [SQL data type](/sql-reference-data-types).

        Note

        For stored procedures you write in Java, Python, or Scala (which use Snowpark APIs), omit the argument for the Snowpark
        `Session` object.

        The `Session` argument is not a formal parameter that you specify in CREATE PROCEDURE or CALL. When you call your
        stored procedure, Snowflake automatically creates a `Session` object and passes it to the handler function for your
        stored procedure.
      - To indicate that an argument is optional, use `DEFAULT default_value` to specify the default value of the argument.
        For the default value, you can use a literal or an expression.

        If you specify any optional arguments, you must place these after the required arguments.

        If a procedure has optional arguments, you cannot define additional procedures with the same name and different signatures.

        For details, see [Specify optional arguments](/developer-guide/udf-stored-procedure-arguments#label-procedure-function-arguments-optional).

`RETURNS { result_data_type [ [ NOT ] NULL ] | TABLE ( [ col_name col_data_type [ , ... ] ] ) }`
:   Specifies the type of the result returned by the stored procedure.

    - For `result_data_type`, use the Snowflake data type that corresponds to the type of the language that you are using.

      - For [Java stored procedures](/developer-guide/stored-procedure/java/procedure-java-overview), see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).
      - For [JavaScript stored procedures](/developer-guide/stored-procedure/stored-procedures-javascript), see
        [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
      - For [Python stored procedures](/developer-guide/stored-procedure/python/procedure-python-overview), see
        [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
      - For [Scala stored procedures](/developer-guide/stored-procedure/scala/procedure-scala-overview), see [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).

      - For Snowflake Scripting, a [SQL data type](/sql-reference-data-types).

      Note

      Stored procedures you write in Snowpark (Java or Scala) must have a return value. In Snowpark (Python), when a stored procedure
      returns no value, it is considered to be returning `None`. Note that every CREATE PROCEDURE statement must include a RETURNS
      clause that defines a return type, even if the procedure does not explicitly return anything.
    - For `RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )`, if you know the
      [Snowflake data types](/sql-reference-data-types) of the columns in the returned table, specify the column names and
      types:

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE get_top_sales()
        RETURNS TABLE (sales_date DATE, quantity NUMBER)
      ...
      ```

      Otherwise (for example, if you are determining the column types during run time), you can omit the column names and types:

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE get_top_sales()
        RETURNS TABLE ()
      ```

      Note

      Currently, in the `RETURNS TABLE(...)` clause, you can’t specify GEOGRAPHY as a column type. This
      applies whether you are creating a stored or anonymous procedure.

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
        RETURNS TABLE(g GEOGRAPHY)
        ...
      ```

      Copy code

      ```
      WITH test_return_geography_table_1() AS PROCEDURE
        RETURNS TABLE(g GEOGRAPHY)
        ...
      CALL test_return_geography_table_1();
      ```

      If you attempt to specify GEOGRAPHY as a column type, calling the stored procedure results in the error:

      Copy code

      ```
      Stored procedure execution error: data type of returned table does not match expected returned table type
      ```

      To work around this issue, you can omit the column arguments and types in `RETURNS TABLE()`.

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE test_return_geography_table_1()
        RETURNS TABLE()
        ...
      ```

      Copy code

      ```
      WITH test_return_geography_table_1() AS PROCEDURE
        RETURNS TABLE()
        ...
      CALL test_return_geography_table_1();
      ```

      RETURNS TABLE(…) is supported only when the handler is written in the following languages:

      - [Java](/developer-guide/stored-procedure/java/procedure-java-tabular-data)
      - [Python](/developer-guide/stored-procedure/python/procedure-python-tabular-data)
      - [Scala](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data)
      - [Snowflake Scripting](/sql-reference/snowflake-scripting/return)

    As a practical matter, outside of a [Snowflake Scripting block](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-call-sp-return-value),
    [the returned value cannot be used because the call cannot be part of an expression](/developer-guide/stored-procedures-vs-udfs#label-sp-udf-using-values).

`LANGUAGE language`
:   Specifies the language of the stored procedure code. Note that this is optional for stored procedures written with
    [Snowflake Scripting](/developer-guide/snowflake-scripting/index).

    Currently, the supported values for `language` include:

    - `JAVA` (for [Java](/developer-guide/stored-procedure/java/procedure-java-overview))
    - `JAVASCRIPT` (for [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript))
    - `PYTHON` (for [Python](/developer-guide/stored-procedure/python/procedure-python-overview))
    - `SCALA` (for [Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview))
    - `SQL` (for [Snowflake Scripting](/developer-guide/snowflake-scripting/index))

    Default: `SQL`.

`AS procedure_definition`
:   Defines the code executed by the stored procedure. The definition can consist of any valid code.

    Note the following:

    - For stored procedures for which the code is not in-line, omit the AS clause. This includes stored procedures with staged handlers.

      Instead, use the IMPORTS clause to specify the location of the file containing the code for the stored procedure. For
      details, see:

      - [Writing stored procedures with SQL and Python](/developer-guide/stored-procedure/python/procedure-python-overview)
      - [Writing Java handlers for stored procedures created with SQL](/developer-guide/stored-procedure/java/procedure-java-overview)
      - [Writing Scala handlers for stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-overview)

      For more information on in-line and staged handlers, see [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).
    - You must use [string literal delimiters](/sql-reference/data-types-text#label-quoted-string-constants) (`'` or `$$`) around
      `{procedure definition}` if:

      - You are using a language other than Snowflake Scripting.
      - You are creating a Snowflake Scripting procedure in SnowSQL or Snowsight. See
        [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).
    - For stored procedures in JavaScript, if you are writing a string that contains newlines, you can use
      backquotes (also called “backticks”) around the string.

      The following example of a JavaScript stored procedure uses `$$` and backquotes because the body of the stored procedure
      contains single quotes and double quotes:

      > Copy code
      >
      > ```
      > CREATE OR REPLACE TABLE table1 ("column 1" VARCHAR);
      > ```
      >
      > Copy code
      >
      > ```
      > CREATE or replace PROCEDURE proc3()
      >   RETURNS VARCHAR
      >   LANGUAGE javascript
      >   AS
      >   $$
      >   var rs = snowflake.execute( { sqlText: 
      >    `INSERT INTO table1 ("column 1") 
      >         SELECT 'value 1' AS "column 1" ;`
      >     } );
      >   return 'Done.';
      >   $$;
      > ```
    - Snowflake does not completely validate the code when you execute the CREATE PROCEDURE command.

      For example, for Snowpark (Scala) stored procedures, the number and types of arguments are validated, but the body of
      the function is not validated. If the number or types do not match (e.g. if the Snowflake data type NUMBER is used when the
      argument is a non-numeric type), executing the CREATE PROCEDURE command causes an error.

      If the code is not valid, the CREATE PROCEDURE command will succeed, and errors will be returned when the stored procedure is
      called.

    For more details about stored procedures, see [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

### Java

`RUNTIME_VERSION = 'language_runtime_version'`
:   The language runtime version to use. Currently, the supported versions are:

    - 11.x
    - 17.x
    - 21.x

`PACKAGES = ( 'snowpark_package_name' [, 'package_name' ...] )`
:   A comma-separated list of the names of packages deployed in Snowflake that should be included in the handler code’s
    execution environment. The Snowpark package is required for stored procedures, so it must always be referenced in the PACKAGES clause.
    For more information about Snowpark, see [Snowpark API](/developer-guide/snowpark/index).

    By default, the environment in which Snowflake runs stored procedures includes a selected set of packages for supported languages.
    When you reference these packages in the PACKAGES clause, it is not necessary to reference a file containing the package in the IMPORTS
    clause because the package is already available in Snowflake. You can also specify the package version.

    For the list of supported packages and versions for Java, query the
    [INFORMATION\_SCHEMA.PACKAGES view](/sql-reference/info-schema/packages) for rows, specifying the language. For example:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'java';
    ```

    To specify the package name and version number, use the following form:

    Copy code

    ```
    domain:package_name:version
    ```

    To specify the latest version, specify `latest` for `version`.

    For example, to include a package from the latest Snowpark library in Snowflake, use the following:

    Copy code

    ```
    PACKAGES = ('com.snowflake:snowpark:latest')
    ```

    When specifying a package from the Snowpark library, you must specify version 1.3.0 or later.

`HANDLER = 'fully_qualified_method_name'`
:   Use the fully qualified name of the method or function for the stored procedure. This is typically in the
    following form:

    Copy code

    ```
    com.my_company.my_package.MyClass.myMethod
    ```

    where:

    Copy code

    ```
    com.my_company.my_package
    ```

    corresponds to the package containing the object or class:

    Copy code

    ```
    package com.my_company.my_package;
    ```

### Python

`RUNTIME_VERSION = 'language_runtime_version'`
:   The language runtime version to use. Currently, the supported versions are:

    > Generally available versions:
    >
    > - 3.9 (deprecated)
    > - 3.10
    > - 3.11
    > - 3.12
    > - 3.13
    > - 3.14

`PACKAGES = ( 'snowpark_package_name' [, 'package_name' ...] )`
:   A comma-separated list of the names of packages deployed in Snowflake that should be included in the handler code’s
    execution environment. The Snowpark package is required for stored procedures, so it must always be referenced in the PACKAGES clause.
    For more information about Snowpark, see [Snowpark API](/developer-guide/snowpark/index).

    By default, the environment in which Snowflake runs stored procedures includes a selected set of packages for supported languages.
    When you reference these packages in the PACKAGES clause, it is not necessary to reference a file containing the package in the IMPORTS
    clause because the package is already available in Snowflake. You can also specify the package version.

    For the list of supported packages and versions for Python, query the
    [INFORMATION\_SCHEMA.PACKAGES view](/sql-reference/info-schema/packages) for rows, specifying the language. For example:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'python';
    ```

    Snowflake includes a large number of packages available through Anaconda; for more information, see
    [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

    To specify the package name and version number, use the following form:

    Copy code

    ```
    package_name[==version]
    ```

    To specify the latest version, omit the version number.

    For example, to include the spacy package version 2.3.5 (along with the latest version of the required Snowpark package), use the
    following:

    Copy code

    ```
    PACKAGES = ('snowflake-snowpark-python', 'spacy==2.3.5')
    ```

    When specifying a package from the Snowpark library, you must specify version 0.4.0 or later. Omit the version number to use the
    latest version available in Snowflake.

    [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Specifying a range of Python package versions is available as a preview feature to all accounts.

    You can specify package versions by using these version
    specifiers: `==`, `<=`, `>=`, `<`,or `>`.

    For example:

    Copy code

    ```
    -- Use version 1.2.3 or higher of the NumPy package.
    PACKAGES=('numpy>=1.2.3')
    ```

`HANDLER = 'fully_qualified_method_name'`
:   Use the name of the stored procedure’s function or method. This can differ depending on whether the code is in-line or
    referenced at a stage.

    - When the code is in-line, you can specify just the function name, as in the following example:

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE MYPROC(from_table STRING, to_table STRING, count INT)
        ...
        HANDLER = 'run'
      AS
      $$
      def run(session, from_table, to_table, count):
        ...
      $$;
      ```
    - When the code is imported from a stage, specify the fully qualified handler function name as `<module_name>.<function_name>`.

      Copy code

      ```
      CREATE OR REPLACE PROCEDURE MYPROC(from_table STRING, to_table STRING, count INT)
        ...
        IMPORTS = ('@mystage/my_py_file.py')
        HANDLER = 'my_py_file.run';
      ```

### Scala

`RUNTIME_VERSION = 'language_runtime_version'`
> Specifies the Scala runtime version to use. The supported versions of Scala are:
>
> - 2.13
> - 2.12
>
> For more information, see [Writing code to support different Scala versions](/developer-guide/scala-version-differences).

`PACKAGES = ( 'snowpark_package_name' [, 'package_name' ...] )`
:   A comma-separated list of the names of packages deployed in Snowflake that should be included in the handler code’s
    execution environment. The Snowpark package is required for stored procedures, so it must always be referenced in the PACKAGES clause.
    For more information about Snowpark, see [Snowpark API](/developer-guide/snowpark/index).

    By default, the environment in which Snowflake runs stored procedures includes a selected set of packages for supported languages.
    When you reference these packages in the PACKAGES clause, it is not necessary to reference a file containing the package in the IMPORTS
    clause because the package is already available in Snowflake. You can also specify the package version.

    For the list of supported packages and versions for Scala, query the
    [INFORMATION\_SCHEMA.PACKAGES view](/sql-reference/info-schema/packages) for rows, specifying the language. For example:

    Copy code

    ```
    SELECT * FROM INFORMATION_SCHEMA.PACKAGES WHERE LANGUAGE = 'scala';
    ```

    To specify the package name and version number, use the following form:

    Copy code

    ```
    domain:package_name:version
    ```

    To specify the latest version, specify `latest` for `version`.

    For example, to include a package from the latest Snowpark library in Snowflake, use the following:

    Copy code

    ```
    PACKAGES = ('com.snowflake:snowpark:latest')
    ```

    Snowflake supports using Snowpark version 0.9.0 or later in a Scala stored procedure. Note, however, that these versions have
    limitations. For example, versions prior to 1.1.0 do not support the use of transactions in a stored procedure.

`HANDLER = 'fully_qualified_method_name'`
:   Use the fully qualified name of the method or function for the stored procedure. This is typically in the following form:

    Copy code

    ```
    com.my_company.my_package.MyClass.myMethod
    ```

    where:

    Copy code

    ```
    com.my_company.my_package
    ```

    corresponds to the package containing the object or class:

    Copy code

    ```
    package com.my_company.my_package;
    ```

## Optional parameters

### All languages

`SECURE`
:   Specifies that the procedure is secure. For more information about secure procedures, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

`{ TEMP | TEMPORARY }`
:   Specifies that the procedure persists for only the duration of the [session](/user-guide/session-policies) in which you created it.
    A temporary procedure is dropped at the end of the session.

    Default: No value. If a procedure is not declared as `TEMPORARY`, it is permanent.

    You cannot create temporary [procedures](/developer-guide/stored-procedure/stored-procedures-overview) that have the same name as
    a procedure that already exists in the schema.

    Note that creating a temporary procedure does not require the CREATE PROCEDURE privilege on the schema in which the object is created.

    For more information about creating temporary procedures, see [Temporary procedures](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-overview-temporary).

`[ [ NOT ] NULL ]`
:   Specifies whether the stored procedure can return NULL values or must return only NON-NULL values.

    The default is NULL (i.e. the stored procedure can return NULL).

`CALLED ON NULL INPUT` or `{ RETURNS NULL ON NULL INPUT | STRICT }`
:   Specifies the behavior of the stored procedure when called with null inputs. In contrast to system-defined functions, which
    always return null when any input is null, stored procedures can handle null inputs, returning non-null values even when an
    input is null:

    - `CALLED ON NULL INPUT` will always call the stored procedure with null inputs. It is up to the procedure to handle such
      values appropriately.
    - `RETURNS NULL ON NULL INPUT` (or its synonym `STRICT`) will not call the stored procedure if any input is null,
      so the statements inside the stored procedure will not be executed. Instead, a null value will always be returned. Note that
      the procedure might still return null for non-null inputs.

    Default: `CALLED ON NULL INPUT`

`{ VOLATILE | IMMUTABLE }`
:   Deprecated

    Attention

    These keywords are deprecated for stored procedures. These keywords are not intended to apply to stored procedures. In a
    future release, these keywords will be removed from the documentation.

`COMMENT = 'string_literal'`
:   Specifies a comment for the stored procedure, which is displayed in the DESCRIPTION column in the [SHOW PROCEDURES](/sql-reference/sql/show-procedures) output.

    Default: `stored procedure`

`EXECUTE AS OWNER` or `EXECUTE AS CALLER` or `EXECUTE AS RESTRICTED CALLER`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Restricted caller’s rights (`EXECUTE AS RESTRICTED CALLER`) is a preview feature available to all accounts.

    Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with
    the privileges of the caller (a “caller’s rights” stored procedure):

    - If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure.
    - If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a
      caller’s rights procedure.
    - If you execute the statement CREATE PROCEDURE … EXECUTE AS RESTRICTED CALLER, then in the future the procedure will execute as a
      caller’s rights procedure, but might not be able to run with all of the caller’s privileges. For more information, see
      [Restricted caller’s rights](/developer-guide/restricted-callers-rights).

    If `EXECUTE AS ...` isn’t specified, the procedure runs as an owner’s rights stored procedure. Owner’s rights stored
    procedures have less access to the caller’s environment (for example, the caller’s session variables), and Snowflake defaults to this
    higher level of privacy and security.

    For more information, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

    Default: `OWNER`

`COPY GRANTS`
:   Specifies to retain the access privileges from the original procedure when a new procedure is created using CREATE OR REPLACE PROCEDURE.

    The parameter copies all privileges, except OWNERSHIP, from the existing procedure to the new procedure. The new procedure will
    inherit any future grants defined for the object type in the schema. By default, the role that executes the CREATE PROCEDURE
    statement owns the new procedure.

    Note:

    - The [SHOW GRANTS](/sql-reference/sql/show-grants) output for the replacement procedure lists the grantee for the copied privileges as the
      role that executed the CREATE PROCEDURE statement, with the current timestamp when the statement was executed.
    - The operation to copy grants occurs atomically in the CREATE PROCEDURE command (i.e. within the same transaction).

### Java

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [, 'stage_path_and_directory_or_file_name_to_read' ...] )`
:   The location (stage), path, and name of the directory or file(s) to import. You must set the IMPORTS clause to include any files that
    your stored procedure depends on:

    - If you are writing an in-line stored procedure, you can omit this clause, unless your code depends on classes defined outside
      the stored procedure or resource files.
    - If you are writing a stored procedure with a staged handler, you must also include a path to the JAR file containing the
      stored procedure’s handler code.
    - The IMPORTS definition cannot reference variables from arguments that are passed into the stored procedure.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different subdirectories or different stages.

`TARGET_PATH = stage_path_and_file_name_to_write`
:   Specifies the location to which Snowflake should write the JAR file containing the result of compiling the handler source code specified
    in the `procedure_definition`.

    If this clause is included, Snowflake writes the resulting JAR file to the stage location specified by the clause’s value. If this
    clause is omitted, Snowflake re-compiles the source code each time the code is needed. In that case, the JAR file is not stored
    permanently, and the user does not need to clean up the JAR file.

    Snowflake returns an error if the TARGET\_PATH matches an existing file; you cannot use TARGET\_PATH to overwrite an
    existing file.

    If you specify both the IMPORTS and TARGET\_PATH clauses, the file name in the TARGET\_PATH clause must
    be different from each file name in the IMPORTS clause, even if the files are in different subdirectories or different
    stages.

    The generated JAR file remains until you explicitly delete it, even if you drop the procedure. When you drop the procedure you should
    separately remove the JAR file because the JAR is no longer needed to support the procedure.

    For example, the following TARGET\_PATH example would result in a `myhandler.jar` file generated and copied to the
    `handlers` stage.

    Copy code

    ```
    TARGET_PATH = '@handlers/myhandler.jar'
    ```

    When you drop this procedure to remove it, you’ll also need to remove its handler JAR file, such as by executing the
    [REMOVE command](/sql-reference/sql/remove).

    Copy code

    ```
    REMOVE @handlers/myhandler.jar;
    ```

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for this
    procedure’s handler code to access external networks.

    An external access integration specifies [network rules](/sql-reference/sql/create-network-rule) and
    [secrets](/sql-reference/sql/create-secret) that specify external locations and credentials (if any) allowed for use by handler code
    when making requests of an external network, such as an external REST API.

`SECRETS = ( 'secret_variable_name' = secret_name [ , ... ] )`
:   Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from
    secrets in handler code.

    Secrets you specify here must be allowed by the [external access integration](/sql-reference/sql/create-external-access-integration)
    specified as a value of this CREATE PROCEDURE command’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter.

    This parameter’s value is a comma-separated list of assignment expressions with the following parts:

    - `secret_name` as the name of the allowed secret.

      You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the
      EXTERNAL\_ACCESS\_INTEGRATIONS parameter.
    - `'secret_variable_name'` as the variable that will be used in handler code when retrieving information from the secret.

    For more information, including an example, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

### Python

`ARTIFACT_REPOSITORY = artifact_repository`

Specifies the name of the repository to use for installing PyPI packages for use by your procedure.

Set this to `snowflake.snowpark.pypi_shared_repository`, which is the default artifact repository provided by Snowflake.

`PACKAGES = ( 'package_name' [ , ... ] )`

Specify a list of the names of the packages that you want to install and use in your procedure. Snowflake installs these packages from the artifact repository.

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [, 'stage_path_and_directory_or_file_name_to_read' ...] )`
:   The location (stage), path, and name of the directory or file(s) to import. You must set the IMPORTS clause to include any files that
    your stored procedure depends on:

    - If you are writing an in-line stored procedure, you can omit this clause, unless your code depends on classes defined outside
      the stored procedure or resource files.
    - If your stored procedure’s code will be on a stage, you must also include a path to the module file your code is in.
    - The IMPORTS definition cannot reference variables from arguments that are passed into the stored procedure.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different subdirectories or different stages.

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for this
    procedure’s handler code to access external networks.

    An external access integration specifies [network rules](/sql-reference/sql/create-network-rule) and
    [secrets](/sql-reference/sql/create-secret) that specify external locations and credentials (if any) allowed for use by handler code
    when making requests of an external network, such as an external REST API.

`SECRETS = ( 'secret_variable_name' = secret_name [ , ... ] )`
:   Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from
    secrets in handler code.

    Secrets you specify here must be allowed by the [external access integration](/sql-reference/sql/create-external-access-integration)
    specified as a value of this CREATE PROCEDURE command’s EXTERNAL\_ACCESS\_INTEGRATIONS parameter.

    This parameter’s value is a comma-separated list of assignment expressions with the following parts:

    - `secret_name` as the name of the allowed secret.

      You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the
      EXTERNAL\_ACCESS\_INTEGRATIONS parameter.
    - `'secret_variable_name'` as the variable that will be used in handler code when retrieving information from the secret.

    For more information, including an example, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

### Scala

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [, 'stage_path_and_directory_or_file_name_to_read' ...] )`
:   The location (stage), path, and name of the directory or file(s) to import. You must set the IMPORTS clause to include any files that
    your stored procedure depends on:

    - If you are writing an in-line stored procedure, you can omit this clause, unless your code depends on classes defined outside
      the stored procedure or resource files.
    - If you are writing a stored procedure with a staged handler, you must also include a path to the JAR file containing the
      stored procedure’s handler code.
    - The IMPORTS definition cannot reference variables from arguments that are passed into the stored procedure.

    Each file in the IMPORTS clause must have a unique name, even if the files are in different subdirectories or different stages.

`TARGET_PATH = stage_path_and_file_name_to_write`
:   Specifies the location to which Snowflake should write the JAR file containing the result of compiling the handler source code specified
    in the `procedure_definition`.

    If this clause is included, Snowflake writes the resulting JAR file to the stage location specified by the clause’s value. If this
    clause is omitted, Snowflake re-compiles the source code each time the code is needed. In that case, the JAR file is not stored
    permanently, and the user does not need to clean up the JAR file.

    Snowflake returns an error if the TARGET\_PATH matches an existing file; you cannot use TARGET\_PATH to overwrite an
    existing file.

    If you specify both the IMPORTS and TARGET\_PATH clauses, the file name in the TARGET\_PATH clause must
    be different from each file name in the IMPORTS clause, even if the files are in different subdirectories or different
    stages.

    The generated JAR file remains until you explicitly delete it, even if you drop the procedure. When you drop the procedure you should
    separately remove the JAR file because the JAR is no longer needed to support the procedure.

    For example, the following TARGET\_PATH example would result in a `myhandler.jar` file generated and copied to the
    `handlers` stage.

    Copy code

    ```
    TARGET_PATH = '@handlers/myhandler.jar'
    ```

    When you drop this procedure to remove it, you’ll also need to remove its handler JAR file, such as by executing the
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
| CREATE PROCEDURE | Schema | Required to create a permanent stored procedure. Not required when creating a temporary procedure that persists for only the duration of the session in which the procedure was created. |
| USAGE | Procedure | Granting the USAGE privilege on the newly created procedure to a role allows users with that role to call the procedure elsewhere in Snowflake. |
| USAGE | External access integration | Required on integrations, if any, specified when creating the procedure. For more information, see [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration). |
| READ | Secret | Required on secrets, if any, specified when creating the procedure. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |
| USAGE | Schema | Required on schemas containing secrets, if any, specified when creating the procedure. For more information, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret) and [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

For additional usage notes, see the following.

# All handler languages

- The definition for a stored procedure is limited to 1MB.
- Stored procedures support [overloading](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading). Two procedures can have the same
  name if they have a different number of parameters or different data types for their parameters.
- Stored procedures are not atomic; if one statement in a stored procedure fails, the other statements in the stored
  procedure are not necessarily rolled back. For information about stored procedures and transactions, see
  [Transaction management](/developer-guide/stored-procedure/stored-procedures-usage#label-stored-procedures-usage-transaction-management).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

Tip

If your organization uses a mix of caller’s rights and owner’s rights stored procedures, you might want to use a
naming convention for your stored procedures to indicate whether an individual stored procedure is a caller’s
rights stored procedure or an owner’s rights stored procedure.

- Setting LOG\_LEVEL or TRACE\_LEVEL as properties in a CREATE PROCEDURE statement is not supported. To set these properties
  on a procedure, use [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) after creating the procedure, or use
  [CREATE OR ALTER PROCEDURE](/sql-reference/sql/create-procedure#label-create-or-alter-procedure-syntax).

## Java

See the [known limitations](/developer-guide/stored-procedure/java/procedure-java-limitations).

## Javascript

A JavaScript stored procedure can return only a single value, such as a string (for example, a success/failure indicator)
or a number (for example, an error code). If you need to return more extensive information, you can return a
VARCHAR that contains values separated by a delimiter (such as a comma), or a semi-structured data type, such
as [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).

## Python

See the [known limitations](/developer-guide/stored-procedure/python/procedure-python-limitations).

## Scala

See the [known limitations](/developer-guide/stored-procedure/scala/procedure-scala-limitations).

## CREATE OR ALTER PROCEDURE usage notes

- All limitations of the [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) command apply.
- All limitations described in [CREATE OR ALTER FUNCTION usage notes](/sql-reference/sql/create-function#label-create-or-alter-function-usage-notes) apply.

## Examples

This creates a trivial stored procedure that returns a hard-coded value. This is unrealistic, but shows the basic
SQL syntax with minimal JavaScript code:

Copy code

```
CREATE OR REPLACE PROCEDURE sp_pi()
    RETURNS FLOAT NOT NULL
    LANGUAGE JAVASCRIPT
    AS
    $$
    return 3.1415926;
    $$
    ;
```

This shows a more realistic example that includes a call to the JavaScript API. A more extensive version of this
procedure could allow a user to insert data into a table that the user didn’t have privileges to insert into directly.
JavaScript statements could check the input parameters and execute the SQL `INSERT` only if certain requirements
were met.

Copy code

```
CREATE OR REPLACE PROCEDURE stproc1(FLOAT_PARAM1 FLOAT)
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
    var sql_command = 
     "INSERT INTO stproc_test_table1 (num_col1) VALUES (" + FLOAT_PARAM1 + ")";
    try {
        snowflake.execute (
            {sqlText: sql_command}
            );
        return "Succeeded.";   // Return a success/error indicator.
        }
    catch (err)  {
        return "Failed: " + err;   // Return a success/error indicator.
        }
    $$
    ;
```

For more examples, see [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

### In-line handler

Code in the following example creates a procedure called `my_proc` with an in-line Python handler function `run`. Through
the PACKAGES clause, the code references the included Snowpark library for Python, whose `Session` is required when Python
is the procedure handler language.

Copy code

```
CREATE OR REPLACE PROCEDURE my_proc(from_table STRING, to_table STRING, count INT)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.9'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
AS
$$
def run(session, from_table, to_table, count):
  session.table(from_table).limit(count).write.save_as_table(to_table)
  return "SUCCESS"
$$;
```

### Staged handler

Code in the following example creates a procedure called `my_proc` with a staged Java handler method `MyClass.myMethod`.
Through the PACKAGES clause, the code references the included Snowpark library for Java, whose `Session` is required when Java
is the procedure handler language. With the IMPORTS clause, the code references the staged JAR file containing the handler code.

Copy code

```
CREATE OR REPLACE PROCEDURE my_proc(fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE JAVA
  RUNTIME_VERSION = '11'
  PACKAGES = ('com.snowflake:snowpark:latest')
  IMPORTS = ('@mystage/myjar.jar')
  HANDLER = 'MyClass.myMethod';
```

## Create and alter a procedure using the CREATE OR ALTER PROCEDURE command

Create an owner’s rights Python stored procedure with external access integrations and default OWNER privileges.

Copy code

```
CREATE OR ALTER PROCEDURE python_add1(A NUMBER)
  RETURNS NUMBER
  LANGUAGE PYTHON
  HANDLER='main'
  RUNTIME_VERSION = '3.10'
  EXTERNAL_ACCESS_INTEGRATIONS=(example_integration)
  PACKAGES = ('snowflake-snowpark-python')
  EXECUTE AS OWNER
  AS
$$
def main(session, a):
    return a+1
$$;
```

Alter the stored procedure’s secrets and change the stored procedure to a caller’s rights procedure:

Copy code

```
CREATE OR ALTER PROCEDURE python_add1(A NUMBER)
  RETURNS NUMBER
  LANGUAGE PYTHON
  HANDLER='main'
  RUNTIME_VERSION = '3.10'
  EXTERNAL_ACCESS_INTEGRATIONS=(example_integration)
  SECRETS = ('secret_variable_name' = secret_name)
  PACKAGES = ('snowflake-snowpark-python')
  EXECUTE AS CALLER
  AS
$$
def main(session, a):
    return a+1
$$;
```
