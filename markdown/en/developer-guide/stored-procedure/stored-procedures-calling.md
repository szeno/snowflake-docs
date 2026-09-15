# Calling a stored procedure

You can call a stored procedure in one of several ways.

## Tools for calling procedures

Choose the tool for calling the procedure.

| Language | Approach |
| --- | --- |
| **SQL**  Execute a SQL command, such as by using Snowsight. | [Execute the SQL CALL command](#label-call-procedure-arguments) to call a procedure. |
| **Java, Python, or Scala with Snowpark**  Write code locally in one of the supported languages, having the call execute in Snowflake. | Execute client code that uses Snowpark APIs in one of the following languages.   - [Java](/developer-guide/snowpark/java/creating-sprocs) - [Python](/developer-guide/snowpark/python/creating-sprocs) - [Scala](/developer-guide/snowpark/scala/creating-sprocs) |
| **Command line**  Create and manage Snowflake entities by executing commands from the command line. | Execute commands of the [Snowflake CLI](/developer-guide/snowflake-cli/index):   - [To execute SQL commands](/developer-guide/snowflake-cli/command-reference/sql-commands/sql). - [To execute Snowpark commands](/developer-guide/snowflake-cli/command-reference/snowpark-commands/execute). |
| **Python**  On the client, write code that executes management operations on Snowflake. | Execute code that uses the [Snowflake Python API](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-call-procedure). |
| **RESTful APIs** (language-agnostic)  Make requests of RESTful endpoints to create and manage Snowflake entities. | Make a request to create a procedure using the [Snowflake REST API](/developer-guide/snowflake-rest-api/procedure/procedure-introduction) |

Expand

Show lessSee more

Once you have the privileges to call the stored procedure, you can use a CALL statement to call the stored procedure.

Note

To both create and call an anonymous procedure, use [CALL (with anonymous procedure)](/sql-reference/sql/call-with). Creating and calling an anonymous procedure does
not require a role with CREATE PROCEDURE schema privileges.

## Usage notes

- Procedure names are not necessarily unique within the schema; stored procedures are identified and resolved by their arguments types as well
  as their names (that is, stored procedures can be overloaded).
- Outside of a [Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks), the value returned by the stored
  procedure cannot be used, because the call cannot be part of an expression.

  In a Snowflake Scripting block, you can specify `INTO :snowflake_scripting_variable` to capture the return value from
  the stored procedure in a Snowflake Scripting variable.
- Stored procedures are not atomic; if one statement in a stored procedure fails, the other statements in the stored
  procedure are not necessarily rolled back. For information about stored procedures and transactions, see
  [Transaction management](/developer-guide/stored-procedure/stored-procedures-usage#label-stored-procedures-usage-transaction-management).
- You can also create and call an anonymous procedure using [CALL (with anonymous procedure)](/sql-reference/sql/call-with).

## Calling a stored procedure with SQL

If the stored procedure has arguments, you can specify those arguments by name or by position.

For example, the following stored procedure accepts three arguments:

Copy code

```
CREATE OR REPLACE PROCEDURE sp_concatenate_strings(
    first_arg VARCHAR,
    second_arg VARCHAR,
    third_arg VARCHAR)
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
  BEGIN
    RETURN first_arg || second_arg || third_arg;
  END;
  $$;
```

When calling the procedure, you can specify the arguments by name:

Copy code

```
CALL sp_concatenate_strings(
  first_arg => 'one',
  second_arg => 'two',
  third_arg => 'three');
```

```
+------------------------+
| SP_CONCATENATE_STRINGS |
|------------------------|
| onetwothree            |
+------------------------+
```

If you specify the arguments by name, you do not need to specify the arguments in any particular order:

Copy code

```
CALL sp_concatenate_strings(
  third_arg => 'three',
  first_arg => 'one',
  second_arg => 'two');
```

```
+------------------------+
| SP_CONCATENATE_STRINGS |
|------------------------|
| onetwothree            |
+------------------------+
```

You can also specify the arguments by position:

Copy code

```
CALL sp_concatenate_strings(
  'one',
  'two',
  'three');
```

```
+------------------------+
| SP_CONCATENATE_STRINGS |
|------------------------|
| onetwothree            |
+------------------------+
```

Note

- You must either specify all arguments by name or by position. You can’t specify some of the arguments by name and other
  arguments by position.
- When you specify an argument by name, you can’t use double quotes around the argument name.
- If two procedures have the same name but different argument types, you can use the argument names to specify
  which procedure to execute, if the argument names are different. For more information, see
  [Overloading procedures and functions](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).

### Specifying optional arguments

If the stored procedure has [optional arguments](/developer-guide/udf-stored-procedure-arguments#label-procedure-function-arguments-optional), you can omit the optional
arguments in the call. Each optional argument has a default value that is used when the argument is omitted.

For example, the following stored procedure has one required argument and two optional arguments. Each optional argument has a
default value.

Copy code

```
CREATE OR REPLACE PROCEDURE build_string_proc(
    word VARCHAR,
    prefix VARCHAR DEFAULT 'pre-',
    suffix VARCHAR DEFAULT '-post'
  )
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
    BEGIN
      RETURN prefix || word || suffix;
    END;
  $$
  ;
```

You can omit any of the optional arguments in the call. When you omit an argument, the default value of the argument is used.

Copy code

```
CALL build_string_proc('hello');
```

```
+-------------------+
| BUILD_STRING_PROC |
|-------------------|
| pre-hello-post    |
+-------------------+
```

Copy code

```
CALL build_string_proc('hello', 'before-');
```

```
+-------------------+
| BUILD_STRING_PROC |
|-------------------|
| before-hello-post |
+-------------------+
```

If you need to omit an optional argument and specify another optional argument that appears after the omitted argument in the
signature, use named arguments, rather than positional arguments.

For example, suppose that you want to omit the `prefix` argument and specify the `suffix` argument. The `suffix` argument
appears after the `prefix` in the signature, so you must specify the arguments by name:

Copy code

```
CALL build_string_proc(word => 'hello', suffix => '-after');
```

```
+-------------------+
| BUILD_STRING_PROC |
|-------------------|
| pre-hello-after   |
+-------------------+
```
