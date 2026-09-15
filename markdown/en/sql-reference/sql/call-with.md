# CALL (with anonymous procedure)

Creates and calls an anonymous procedure that is like a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview) but is not
stored for later use.

With this command, you both create an anonymous procedure defined by parameters in the WITH clause and call that procedure.

You need not have a role with CREATE PROCEDURE schema privileges for this command.

The procedure runs with [caller’s rights](/developer-guide/stored-procedure/stored-procedures-rights), which means that the procedure runs with
the privileges of the caller, uses the current session context, and has access to the caller’s session variables and parameters.

See also:
:   [CREATE PROCEDURE](/sql-reference/sql/create-procedure) , [CALL](/sql-reference/sql/call).

## Syntax

### Java

[Preview Feature](/release-notes/preview-features) — Open

Using tabular stored procedures with a [Java handler](/developer-guide/stored-procedure/java/procedure-java-tabular-data)
via `RETURNS TABLE(...)` is a preview feature that is available to all accounts.

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE { JAVA }
  RUNTIME_VERSION = '<scala_or_java_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ AS '<procedure_definition>' ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

For Java procedures with [staged handlers](/developer-guide/inline-or-staged), use the following syntax:

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE { JAVA }
  RUNTIME_VERSION = '<scala_or_java_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

### JavaScript

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS <result_data_type> [ [ NOT ] NULL ]
  LANGUAGE JAVASCRIPT
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  AS '<procedure_definition>'
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

### Python

For in-line procedures, use the following syntax:

Copy code

```
WITH <name> AS PROCEDURE ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<python_version>'
  PACKAGES = ( 'snowflake-snowpark-python[==<version>]'[, '<package_name>[==<version>]' ... ])
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<function_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
  AS '<procedure_definition>'
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

For a procedure in which the code is in a file on a stage, use the following syntax:

Copy code

```
WITH <name> AS PROCEDURE ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE PYTHON
  RUNTIME_VERSION = '<python_version>'
  PACKAGES = ( 'snowflake-snowpark-python[==<version>]'[, '<package_name>[==<version>]' ... ])
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<module_file_name>.<function_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

### Scala

[Preview Feature](/release-notes/preview-features) — Open

Using tabular stored procedures with a [Scala handler](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data)
via `RETURNS TABLE(...)` is a preview feature that is available to all accounts.

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE { SCALA }
  RUNTIME_VERSION = '<scala_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark_<scala_version>:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ AS '<procedure_definition>' ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

For Scala procedures with [staged handlers](/developer-guide/inline-or-staged), use the following syntax:

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS { <result_data_type> [ [ NOT ] NULL ] | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE { SCALA }
  RUNTIME_VERSION = '<scala_or_java_runtime_version>'
  PACKAGES = ( 'com.snowflake:snowpark_<scala_version>:<version>' [, '<package_name_and_version>' ...] )
  [ IMPORTS = ( '<stage_path_and_directory_or_file_name_to_read>' [, '<stage_path_and_directory_or_file_name_to_read>' ...] ) ]
  HANDLER = '<fully_qualified_method_name>'
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

### Snowflake Scripting

Copy code

```
WITH <name> AS PROCEDURE ([ <arg_name> <arg_data_type> ]) [ , ... ] )
  RETURNS { <result_data_type> | TABLE ( [ <col_name> <col_data_type> [ , ... ] ] ) }
  LANGUAGE SQL
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  AS '<procedure_definition>'
  [ , <cte_nameN> [ ( <cte_column_list> ) ] AS ( SELECT ...  ) ]
CALL <name> ( [ [ <arg_name> => ] <arg> , ... ] )
  [ INTO :<snowflake_scripting_variable> ]
```

## Required parameters

### All languages

`WITH name AS PROCEDURE ( [ arg_name arg_data_type ] [ , ... ] )`
:   Specifies the identifier (`name`) and any input arguments for the procedure.

    - For the identifier:

      - The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
        identifier string is enclosed in double quotes (e.g. “My object”). Identifiers enclosed in double quotes are also
        case-sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).
    - For the input arguments:

      - For `arg_name`, specify the name of the input argument.
      - For `arg_data_type`, use the Snowflake data type that corresponds to the handler language that you are using.

        - For [Java procedures](/developer-guide/stored-procedure/java/procedure-java-overview), see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).
        - For [JavaScript procedures](/developer-guide/stored-procedure/stored-procedures-javascript), see
          [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
        - For [Python procedures](/developer-guide/stored-procedure/python/procedure-python-overview), see
          [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
        - For [Scala procedures](/developer-guide/stored-procedure/scala/procedure-scala-overview), see [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).

        - For Snowflake Scripting, a [SQL data type](/sql-reference-data-types).

        Note

        For procedures you write in Java, Python, or Scala (which use Snowpark APIs), omit the argument for the Snowpark
        `Session` object.

        The `Session` argument is not a formal parameter that you specify. When you execute this command, Snowflake automatically
        creates a `Session` object and passes it to the handler function for your procedure.

`RETURNS result_data_type [ [ NOT ] NULL ]`
:   Specifies the type of the result returned by the procedure.

    Use NOT NULL to specify that the procedure must return only non-null values; the default is NULL, meaning that the procedure
    can return NULL.

    - For `result_data_type`, use the Snowflake data type that corresponds to the type of the language that you are using.

      - For [Java procedures](/developer-guide/stored-procedure/java/procedure-java-overview), see [SQL-Java Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-java-data-type-mappings).
      - For [JavaScript procedures](/developer-guide/stored-procedure/stored-procedures-javascript), see
        [SQL and JavaScript data type mapping](/developer-guide/stored-procedure/stored-procedures-javascript#label-stored-procedure-data-type-mapping).
      - For [Python procedures](/developer-guide/stored-procedure/python/procedure-python-overview), see
        [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
      - For [Scala procedures](/developer-guide/stored-procedure/scala/procedure-scala-overview), see [SQL-Scala Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-types-to-scala-types).

      - For Snowflake Scripting, a [SQL data type](/sql-reference-data-types).

      Note

      Procedures you write in Java or Scala must have a return value. In Python, when a procedure returns no value, it is considered to be
      returning `None`.

      Note that regardless of handler language, the WITH clause for this command must include a RETURNS clause that defines a return type,
      even if the procedure does not explicitly return anything.
    - For `RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )`, if you know the
      [Snowflake data types](/sql-reference-data-types) of the columns in the returned table, specify the column names and
      types:

      Copy code

      ```
      WITH get_top_sales() AS PROCEDURE
        RETURNS TABLE (sales_date DATE, quantity NUMBER)
        ...
      CALL get_top_sales();
      ```

      Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types:

      Copy code

      ```
      WITH get_top_sales() AS PROCEDURE
        ...
        RETURNS TABLE ()
      CALL get_top_sales();
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

      `RETURNS TABLE(...)` is supported only when the handler is written in the following languages:

      - [Java](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data)
      - [Python](/developer-guide/stored-procedure/python/procedure-python-tabular-data)
      - [Scala](/developer-guide/stored-procedure/scala/procedure-scala-tabular-data)
      - [Snowflake Scripting](/sql-reference/snowflake-scripting/return)

    As a practical matter, outside of a [Snowflake Scripting block](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting#label-stored-procedure-snowscript-call-sp-return-value),
    [the returned value cannot be used because the call cannot be part of an expression](/developer-guide/stored-procedures-vs-udfs#label-sp-udf-using-values).

`LANGUAGE language`
:   Specifies the language of the procedure’s handler code.

    Currently, the supported values for `language` include:

    - `JAVA` (for [Java](/developer-guide/stored-procedure/java/procedure-java-overview))
    - `JAVASCRIPT` (for [JavaScript](/developer-guide/stored-procedure/stored-procedures-javascript))
    - `PYTHON` (for [Python](/developer-guide/stored-procedure/python/procedure-python-overview))
    - `SCALA` (for [Scala](/developer-guide/stored-procedure/scala/procedure-scala-overview))
    - `SQL` (for [Snowflake Scripting](/developer-guide/snowflake-scripting/index))

`AS procedure_definition`
:   Defines the code executed by the procedure. The definition can consist of any valid code.

    Note the following:

    - For procedures for which the code is not in-line, omit the AS clause. This includes procedures whose
      [handlers are on a stage](/developer-guide/inline-or-staged).

      Instead, use the IMPORTS clause to specify the location of the file containing the code for the procedure. For
      details, see:

      - [Writing stored procedures with SQL and Python](/developer-guide/stored-procedure/python/procedure-python-overview)
      - [Writing Java handlers for stored procedures created with SQL](/developer-guide/stored-procedure/java/procedure-java-overview)
      - [Writing Scala handlers for stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-overview)
    - You must use [string literal delimiters](/sql-reference/data-types-text#label-quoted-string-constants) (`'` or `$$`) around
      `{procedure definition}`, even in Snowflake Scripting.
    - For procedures in JavaScript, if you are writing a string that contains newlines, you can use
      backquotes (also called “backticks”) around the string.

      The following example of a JavaScript procedure uses `$$` and backquotes because the body of the procedure
      contains single quotes and double quotes:

      Copy code

      ```
      WITH proc3 AS PROCEDURE ()
        RETURNS VARCHAR
        LANGUAGE javascript
        AS
        $$
        var rs = snowflake.execute( { sqlText:
         `INSERT INTO table1 ("column 1")
             SELECT 'value 1' AS "column 1" ;`
         } );
        return 'Done.';
        $$
      CALL proc3();
      ```
    - Snowflake does not validate the handler code. However, invalid handler code will result in errors when you execute the command.

    For more details about stored procedures, see [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).

`CALL name ( [ [ arg_name => ] arg , ... ] )`
:   Specifies the identifier (`name`) for the procedure to call and any input arguments.

    You can either specify the input arguments by name (`arg_name => arg`) or by position (`arg`).

    Note

    - You must either specify all arguments by name or by position. You can’t specify some of the arguments by name and other
      arguments by position.
    - When you specify an argument by name, you can’t use double quotes around the argument name.
    - If two procedures have the same name but different argument types, you can use the argument names to specify
      which procedure to execute, if the argument names are different. For more information, see
      [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

### Java, Python, or Scala

`RUNTIME_VERSION = 'language_runtime_version'`
:   The language runtime version to use. Currently, the supported versions are:

    - Java: 11
    - Python:

      Generally available versions:

      - 3.9 (deprecated)
      - 3.10
      - 3.11
      - 3.12
      - 3.13
      - 3.14
    - Scala: 2.12

`PACKAGES = ( 'snowpark_package_name' [, 'package_name' ...] )`
:   A comma-separated list of the names of packages deployed in Snowflake that should be included in the handler code’s
    execution environment. The Snowpark package is required for procedures, so it must always be referenced in the PACKAGES clause.
    For more information about Snowpark, see [Snowpark API](/developer-guide/snowpark/index).

    By default, the environment in which Snowflake runs procedures includes a selected set of packages for supported languages.
    When you reference these packages in the PACKAGES clause, it is not necessary to reference a file containing the package in the IMPORTS
    clause because the package is already available in Snowflake.

    For the list of supported packages and versions for a given language, query the
    [INFORMATION\_SCHEMA.PACKAGES view](/sql-reference/info-schema/packages), specifying the language. For example:

    Copy code

    ```
    SELECT * FROM information_schema.packages WHERE language = '<language>';
    ```

    where `language` is `java`, `python`, or `scala`.

    The syntax for referring to a package in the PACKAGES clause varies by the package’s language, as described below.

    - Java

      Specify the package name and version number using the following form:

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
    - Python

      Snowflake includes a large number of packages available through Anaconda; for more information, see
      [Using third-party packages](/developer-guide/udf/python/udf-python-packages).

      Specify the package name and version number using the following form:

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
    - Scala

      Specify the package name and version number using the following form:

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

      Snowflake supports using Snowpark version 0.9.0 or later in a Scala procedure. Note, however, that these versions have limitations.
      For example, versions prior to 1.1.0 do not support the use of transactions in a procedure.

`HANDLER = 'fully_qualified_method_name'`
:   - Python

      Use the name of the procedure’s function or method. This can differ depending on whether the code is in-line or
      referenced at a stage.

      - When the code is in-line, you can specify just the function name, as in the following example:

        Copy code

        ```
        WITH myproc AS PROCEDURE()
          ...
          HANDLER = 'run'
          AS
          $$
          def run(session):
            ...
          $$
        CALL myproc();
        ```
      - When the code is imported from a stage, specify the fully-qualified handler function name as `<module_name>.<function_name>`.

        Copy code

        ```
        WITH myproc AS PROCEDURE()
          ...
          IMPORTS = ('@mystage/my_py_file.py')
          HANDLER = 'my_py_file.run'
        CALL myproc();
        ```
    - Java and Scala

      Use the fully-qualified name of the method or function for the procedure. This is typically in the
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

## Optional parameters

### All languages

`CALLED ON NULL INPUT` or `RETURNS NULL ON NULL INPUT | STRICT`
:   Specifies the behavior of the procedure when called with null inputs. In contrast to system-defined functions, which
    always return null when any input is null, procedures can handle null inputs, returning non-null values even when an
    input is null:

    - `CALLED ON NULL INPUT` will always call the procedure with null inputs. It is up to the procedure to handle such
      values appropriately.
    - `RETURNS NULL ON NULL INPUT` (or its synonym `STRICT`) will not call the procedure if any input is null,
      so the statements inside the procedure will not be executed. Instead, a null value will always be returned. Note that
      the procedure might still return null for non-null inputs.

    Default: `CALLED ON NULL INPUT`

`INTO :snowflake_scripting_variable`
:   Sets the specified [Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables) to the return value of
    the stored procedure.

### Java, Python, or Scala

`IMPORTS = ( 'stage_path_and_directory_or_file_name_to_read' [, 'stage_path_and_directory_or_file_name_to_read' ...] )`
:   The location (stage), path, and name of the directory or file(s) to import. You must set the `IMPORTS` clause to include any files that
    your procedure depends on:

    - If you are writing an in-line procedure, you can omit this clause, unless your code depends on classes defined outside
      the procedure or resource files.
    - Java or Scala: If you are writing a procedure whose handler will be compiled code, you must also include a path to the JAR file
      containing the procedure’s handler.
    - Python: If your procedure’s code will be on a stage, you must also include a path to the module file your code is in.

    Each file in the `IMPORTS` clause must have a unique name, even if the files are in different subdirectories or different
    stages.

## Usage notes

### General usage

- Procedures are not atomic; if one statement in a procedure fails, the other statements in the
  procedure are not necessarily rolled back. For information about procedures and transactions, see
  [Transaction management](/developer-guide/stored-procedure/stored-procedures-usage#label-stored-procedures-usage-transaction-management).
- A procedure can return only a single value, such as a string (for example, a success/failure indicator)
  or a number (for example, an error code). If you need to return more extensive information, you can return a
  VARCHAR that contains values separated by a delimiter (such as a comma), or a semi-structured data type, such
  as [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

### Syntax

- Similar to when a [WITH](/sql-reference/constructs/with) clause is used with a SELECT statement, a WITH clause used with CALL supports
  specifying multiple CTEs separated by commas, in addition to the procedure definition. However, it is not possible to pass tabular
  values produced by a WITH clause to the CALL clause.

  It is, however, possible to specify a simple variable whose value is assigned in the WITH clause.
- The CALL clause must occur last in the syntax.

### Privileges

- Creating and calling a procedure with this command does not require a role with CREATE PROCEDURE schema privileges.
- The procedure’s handler code will be able to perform only actions permitted for the role assigned to the person who ran this command.

### Language-specific

- For Java procedures, see the [known limitations](/developer-guide/stored-procedure/java/procedure-java-limitations).
- For Python procedures, see the [known limitations](/developer-guide/stored-procedure/python/procedure-python-limitations).
- For Scala procedures, see the [known limitations](/developer-guide/stored-procedure/scala/procedure-scala-limitations).

## Examples

The following example creates and calls a procedure, specifying the arguments by position:

Scala 2.12Scala 2.13

Copy code

```
WITH copy_to_table AS PROCEDURE (fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.12
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'DataCopy.copyBetweenTables'
  AS
  $$
    object DataCopy
    {
      def copyBetweenTables(session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =
      {
        session.table(fromTable).limit(count).write.saveAsTable(toTable)
        return "Success"
      }
    }
  $$
```

Copy code

```
WITH copy_to_table AS PROCEDURE (fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = 2.13
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'DataCopy.copyBetweenTables'
  AS
  $$
    object DataCopy
    {
      def copyBetweenTables(session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =
      {
        session.table(fromTable).limit(count).write.saveAsTable(toTable)
        return "Success"
      }
    }
  $$
```

Copy code

```
CALL copy_to_table('table_a', 'table_b', 5);
```

The following example creates and calls a procedure, specifying the arguments by name:

Scala 2.12Scala 2.13

Copy code

```
WITH copy_to_table AS PROCEDURE (fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.12'
  PACKAGES = ('com.snowflake:snowpark_2.12:latest')
  HANDLER = 'DataCopy.copyBetweenTables'
  AS
  $$
    object DataCopy
    {
      def copyBetweenTables(session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =
      {
        session.table(fromTable).limit(count).write.saveAsTable(toTable)
        return "Success"
      }
    }
  $$
```

Copy code

```
WITH copy_to_table AS PROCEDURE (fromTable STRING, toTable STRING, count INT)
  RETURNS STRING
  LANGUAGE SCALA
  RUNTIME_VERSION = '2.13'
  PACKAGES = ('com.snowflake:snowpark_2.13:latest')
  HANDLER = 'DataCopy.copyBetweenTables'
  AS
  $$
    object DataCopy
    {
      def copyBetweenTables(session: com.snowflake.snowpark.Session, fromTable: String, toTable: String, count: Int): String =
      {
        session.table(fromTable).limit(count).write.saveAsTable(toTable)
        return "Success"
      }
    }
  $$
```

Call the procedure:

Copy code

```
CALL copy_to_table(
  toTable => 'table_b',
  count => 5,
  fromTable => 'table_a');
```

For additional examples, refer to the following topics:

- For examples of Java procedures, see [Writing Java handlers for stored procedures created with SQL](/developer-guide/stored-procedure/java/procedure-java-overview).
- For examples of Python procedures, see [Writing stored procedures with SQL and Python](/developer-guide/stored-procedure/python/procedure-python-overview).
- For examples of Scala procedures, see [Writing Scala handlers for stored procedures created with SQL](/developer-guide/stored-procedure/scala/procedure-scala-overview).
- For examples of Snowflake Scripting stored procedures, see [Writing stored procedures in Snowflake Scripting](/developer-guide/stored-procedure/stored-procedures-snowflake-scripting).

For procedure examples, see [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage).
