# Writing stored procedures in Snowflake Scripting

This topic provides an introduction to writing a stored procedure in SQL by using Snowflake Scripting.
For more information about Snowflake Scripting, see the [Snowflake Scripting Developer Guide](/developer-guide/snowflake-scripting/index).

## Introduction

To write a stored procedure that uses Snowflake Scripting:

- Use the [CREATE PROCEDURE](/sql-reference/sql/create-procedure) or [WITH … CALL …](/sql-reference/sql/call-with) command with
  LANGUAGE SQL.
- In the body of the stored procedure (the AS clause), you use a
  [Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

  Note

  If you are creating a Snowflake Scripting procedure in [SnowSQL](/user-guide/snowsql) or [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), you must use
  [string literal delimiters](/sql-reference/data-types-text#label-quoted-string-constants) (`'` or `$$`) around the body of the stored procedure.

  For details, see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples).

Snowflake limits the maximum size of the source code in the body of a Snowflake Scripting stored procedure. Snowflake
recommends limiting the size to 100 KB. (The code is stored in a compressed form, and the exact limit depends on the
compressibility of the code.)

You can capture log and trace data as your handler code executes. For more information, see
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

Note

- The same rules around [caller’s rights vs. owner’s rights](/developer-guide/stored-procedure/stored-procedures-rights) apply to these stored procedures.
- The same considerations and guidelines in [Working with stored procedures](/developer-guide/stored-procedure/stored-procedures-usage) apply to Snowflake Scripting stored procedures.

The following is an example of a simple stored procedure that returns the value of the argument that is passed in:

Copy code

```
CREATE OR REPLACE PROCEDURE output_message(message VARCHAR)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
BEGIN
  RETURN message;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE output_message(message VARCHAR)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
$$
BEGIN
  RETURN message;
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL output_message('Hello World');
```

The following is an example of a stored procedure that creates a [procedure-scoped temporary table](/user-guide/tables-temp-transient#label-tables-temp-procedure-scoped) from
inside the procedure body. The `CREATE OR REPLACE PROCEDURE SCOPED TEMP TABLE` statement defines the table `inner_scratch` for the current
execution only. The procedure inserts rows into that table and returns the row count.

Copy code

```
CREATE OR REPLACE PROCEDURE proc_scoped_temp_table()
  RETURNS VARCHAR
  LANGUAGE SQL
  AS $$
DECLARE
    row_count INTEGER;
BEGIN
    CREATE OR REPLACE PROCEDURE SCOPED TEMP TABLE inner_scratch (val INTEGER);
    INSERT INTO inner_scratch VALUES (100), (200);

    row_count := (SELECT COUNT(*) FROM inner_scratch);

    RETURN 'count=' || row_count::VARCHAR;
END;
$$;
```

The following is an example of creating and calling an anonymous stored procedure by using the
[WITH … CALL …](/sql-reference/sql/call-with) command:

Copy code

```
WITH anonymous_output_message AS PROCEDURE (message VARCHAR)
  RETURNS VARCHAR NOT NULL
  LANGUAGE SQL
  AS
  $$
  BEGIN
    RETURN message;
  END;
  $$
CALL anonymous_output_message('Hello World');
```

Note that in an anonymous stored procedure, you must use [string literal delimiters](/sql-reference/data-types-text#label-quoted-string-constants) (`'`
or `$$`) around the body of the procedure.

## Using arguments passed to a stored procedure

If you pass in any arguments to your stored procedure, you can refer to those arguments by name in any Snowflake Scripting
expression. Snowflake Scripting stored procedures support input (IN) and output (OUT) arguments.

When you specify an output argument in the definition of a Snowflake Scripting stored procedure, the stored procedure
can return the current value of the output argument to a calling program, such as an anonymous block or a different
stored procedure. The stored procedure takes an initial value for the output argument, saves the value to
a variable in the procedure body, and optionally performs operations to change the value of the variable, before
returning the updated value to the calling program.

For example, a salesperson’s user identifier and a sales quarter can be passed to a stored procedure named
`emp_quarter_calling_sp_demo`. This stored procedure calls a different stored procedure named
`sales_total_out_sp_demo`. The `sales_total_out_sp_demo` stored procedure has an output argument that
performs operations to return the salesperson’s total sales for the quarter to the calling stored procedure
`emp_quarter_calling_sp_demo`. For an example of this scenario, see
[Using an output argument to return the total sales for an employee in a quarter](#label-snowflake-scripting-out-arguments-total-sales).

When there is a mismatch between the data type of the value being passed in and the data type of the output argument,
supported coercions are performed automatically. For an example, see [Using an output argument with a different data type than the input value from a calling procedure](#label-snowflake-scripting-out-arguments-coercion).
For information about which coercions Snowflake can perform automatically, see [Data types that can be cast](/sql-reference/data-type-conversion#label-valid-casting-and-coercions).

The [GET\_DDL](/sql-reference/functions/get_ddl) function and the [SHOW PROCEDURES](/sql-reference/sql/show-procedures) command show the
type (either `IN` or `OUT`) of a stored procedure’s arguments in output. Other commands and views that show
metadata about stored procedures don’t show the type of the arguments, such as the [DESCRIBE PROCEDURE](/sql-reference/sql/desc-procedure)
command, the Information Schema [PROCEDURES view](/sql-reference/info-schema/procedures), and the Account Usage
[PROCEDURES view](/sql-reference/account-usage/procedures).

A stored procedure can’t be overloaded by specifying different argument types in the signature. For example, assume a stored
procedure has this signature:

Copy code

```
CREATE PROCEDURE test_overloading(a IN NUMBER)
```

The following CREATE PROCEDURE command fails with an error stating that the procedure already exists, because it tries to create
a new stored procedure that differs from the previous example only in the argument type:

Copy code

```
CREATE PROCEDURE test_overloading(a OUT NUMBER)
```

### Syntax

Use the following syntax to specify an argument in a Snowflake Scripting stored procedure definition:

Copy code

```
<arg_name> [ { IN | INPUT | OUT | OUTPUT } ] <arg_data_type>
```

Where:

`arg_name`
:   The name of the argument. The name must follow the naming rules for [Object identifiers](/sql-reference/identifiers).

`{ IN | INPUT | OUT | OUTPUT }`
:   Optional keyword that specifies whether the argument is an input argument or an output argument.

    - `IN` or `INPUT` - The argument is initialized with the supplied value, and this value is assigned to a stored procedure
      variable. The variable can be modified in the stored procedure body, but its final value can’t be passed to a calling
      program.

      `IN` and `INPUT` are synonymous.
    - `OUT` or `OUTPUT` - The argument is initialized with the supplied value, and this value is assigned to a stored procedure
      variable. The variable can be modified in the stored procedure body, and its final value can be passed to a calling
      program. In a stored procedure body, output arguments can only be assigned values by using variables.

      Output arguments can also be passed uninitialized variables. When the associated variable is unassigned, the output
      argument returns NULL.

      `OUT` and `OUTPUT` are synonymous.

    Default: `IN`

`arg_data_type`
> A [SQL data type](/sql-reference-data-types).

### Limitations

- Output arguments must be specified in a stored procedure’s definition.
- Output arguments can’t be specified as [optional arguments](/developer-guide/udf-stored-procedure-arguments#label-procedure-function-arguments-optional). That is,
  output arguments can’t be specified using the DEFAULT keyword.
- In the body of a stored procedure, variables must be used to assign values to output arguments.
- The same variable can’t be used for multiple output arguments.
- Session variables can’t be passed to output arguments.
- User-defined functions (UDFs) don’t support output arguments.
- Stored procedures written in languages other than SQL don’t support output arguments.
- Output arguments can’t be used in [asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs).
- Stored procedures are limited to 500 arguments, including both input and output arguments.

### Examples

- [Simple example of using arguments passed to a stored procedure](#label-stored-procedure-snowscript-arguments-simple)
- [Using an argument in a SQL statement (binding)](#label-stored-procedure-snowscript-arguments-binding)
- [Using an argument as an object identifier](#label-stored-procedure-snowscript-arguments-identifier)
- [Using an argument when building a string for a SQL statement](#label-stored-procedure-snowscript-arguments-string)
- [Using an output argument to return a single value](#label-snowflake-scripting-out-arguments-single-value)
- [Using output arguments to return several values for multiple calls to a stored procedure](#label-snowflake-scripting-out-arguments-multiple-values)
- [Using an output argument with a different data type than the input value from a calling procedure](#label-snowflake-scripting-out-arguments-coercion)
- [Using an output argument to return the total sales for an employee in a quarter](#label-snowflake-scripting-out-arguments-total-sales)

#### Simple example of using arguments passed to a stored procedure

The following stored procedure uses the values of the arguments in [IF](/sql-reference/snowflake-scripting/if) and
[RETURN](/sql-reference/snowflake-scripting/return) statements.

Copy code

```
CREATE OR REPLACE PROCEDURE return_greater(number_1 INTEGER, number_2 INTEGER)
RETURNS INTEGER NOT NULL
LANGUAGE SQL
AS
BEGIN
  IF (number_1 > number_2) THEN
    RETURN number_1;
  ELSE
    RETURN number_2;
  END IF;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE return_greater(number_1 INTEGER, number_2 INTEGER)
RETURNS INTEGER NOT NULL
LANGUAGE SQL
AS
$$
BEGIN
  IF (number_1 > number_2) THEN
    RETURN number_1;
  ELSE
    RETURN number_2;
  END IF;
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL return_greater(2, 3);
```

#### Using an argument in a SQL statement (binding)

As is the case with Snowflake Scripting variables, if you need to use an argument in a SQL statement, put a colon (`:`) in front
of the argument name. For more information, see [Using a variable in a SQL statement (binding)](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-binding).

The following sections contain examples that use bind variables in stored procedures:

- [Example that uses a bind variable in a WHERE clause](#label-stored-procedure-snowscript-arguments-binding-example-where)
- [Example of using a bind variable to set the value of a property](#label-stored-procedure-snowscript-arguments-binding-example-comment)
- [Example that uses bind variables to set parameters in a command](#label-stored-procedure-snowscript-arguments-binding-example-stage)
- [Examples that use a bind variable for an array](#label-stored-procedure-snowscript-arguments-binding-examples-array)

##### Example that uses a bind variable in a WHERE clause

The following stored procedure uses the `id` argument in the WHERE clause of a SELECT statement. In the WHERE
clause, the argument is specified as `:id`.

Copy code

```
CREATE OR REPLACE PROCEDURE find_invoice_by_id(id VARCHAR)
RETURNS TABLE (id INTEGER, price NUMBER(12,2))
LANGUAGE SQL
AS
DECLARE
  res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
BEGIN
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE find_invoice_by_id(id VARCHAR)
RETURNS TABLE (id INTEGER, price NUMBER(12,2))
LANGUAGE SQL
AS
$$
DECLARE
  res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
BEGIN
  RETURN TABLE(res);
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL find_invoice_by_id('2');
```

In addition, the [TO\_QUERY](/sql-reference/functions/to_query) function provides a simple syntax for accepting a SQL string
directly in the FROM clause of a SELECT statement. For a comparison of the TO\_QUERY function with dynamic SQL,
see [Constructing SQL at runtime](/user-guide/querying-construct-at-runtime).

##### Example of using a bind variable to set the value of a property

The following stored procedure uses the `comment` argument to add a comment for a table in a
CREATE TABLE statement. In the statement, the argument is specified as `:comment`.

Copy code

```
CREATE OR REPLACE PROCEDURE test_bind_comment(comment VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
BEGIN
  CREATE OR REPLACE TABLE test_table_with_comment(a VARCHAR, n NUMBER) COMMENT = :comment;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_bind_comment(comment VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
  CREATE OR REPLACE TABLE test_table_with_comment(a VARCHAR, n NUMBER) COMMENT = :comment;
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL test_bind_comment('My Test Table');
```

View the comment for the table by querying the [TABLES view](/sql-reference/info-schema/tables)
in the INFORMATION\_SCHEMA:

Copy code

```
SELECT comment FROM information_schema.tables WHERE table_name='TEST_TABLE_WITH_COMMENT';
```

```
+---------------+
| COMMENT       |
%---------------%
| My Test Table |
+---------------+
```

You can also view the comment by running a [SHOW TABLES](/sql-reference/sql/show-tables) command.

##### Example that uses bind variables to set parameters in a command

Assume you have a stage named `st` with CSV files:

Copy code

```
CREATE OR REPLACE STAGE st;
PUT file://good_data.csv @st;
PUT file://errors_data.csv @st;
```

You want to load the data in the CSV files into a table named `test_bind_stage_and_load`:

Copy code

```
CREATE OR REPLACE TABLE test_bind_stage_and_load (a VARCHAR, b VARCHAR, c VARCHAR);
```

The following stored procedure uses the FROM, ON\_ERROR, and VALIDATION\_MODE parameters in
a [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement. In the statement, the parameter values are specified as
`:my_stage_name`, `:on_error`, and `:valid_mode`, respectively.

Copy code

```
CREATE OR REPLACE PROCEDURE test_copy_files_validate(
  my_stage_name VARCHAR,
  on_error VARCHAR,
  valid_mode VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
BEGIN
  COPY INTO test_bind_stage_and_load
    FROM :my_stage_name
    ON_ERROR=:on_error
    FILE_FORMAT=(type='csv')
    VALIDATION_MODE=:valid_mode;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_copy_files_validate(
  my_stage_name VARCHAR,
  on_error VARCHAR,
  valid_mode VARCHAR)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
  COPY INTO test_bind_stage_and_load
    FROM :my_stage_name
    ON_ERROR=:on_error
    FILE_FORMAT=(type='csv')
    VALIDATION_MODE=:valid_mode;
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL test_copy_files_validate('@st', 'skip_file', 'return_all_errors');
```

##### Examples that use a bind variable for an array

You can expand a bind variable that represents an [array](/sql-reference/data-types-semistructured#label-data-type-array) into a list of individual values
by using the spread operator (`**`). For more information and examples, see [Expansion operators](/sql-reference/operators-expansion).

#### Using an argument as an object identifier

If you need to use an argument to refer to an object (for example, a table name in the FROM clause of a SELECT statement), use the
[IDENTIFIER](/sql-reference/identifier-literal) keyword to indicate that the argument represents an object identifier. For
example:

Copy code

```
CREATE OR REPLACE PROCEDURE get_row_count(table_name VARCHAR)
RETURNS INTEGER NOT NULL
LANGUAGE SQL
AS
DECLARE
  row_count INTEGER DEFAULT 0;
  res RESULTSET DEFAULT (SELECT COUNT(*) AS COUNT FROM IDENTIFIER(:table_name));
  c1 CURSOR FOR res;
BEGIN
  FOR row_variable IN c1 DO
    row_count := row_variable.count;
  END FOR;
  RETURN row_count;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE get_row_count(table_name VARCHAR)
RETURNS INTEGER NOT NULL
LANGUAGE SQL
AS
$$
DECLARE
  row_count INTEGER DEFAULT 0;
  res RESULTSET DEFAULT (SELECT COUNT(*) AS COUNT FROM IDENTIFIER(:table_name));
  c1 CURSOR FOR res;
BEGIN
  FOR row_variable IN c1 DO
    row_count := row_variable.count;
  END FOR;
  RETURN row_count;
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL get_row_count('invoices');
```

The following example executes a CREATE TABLE … AS SELECT (CTAS) statement in a stored procedure based on
the table names provided in arguments.

Copy code

```
CREATE OR REPLACE PROCEDURE ctas_sp(existing_table VARCHAR, new_table VARCHAR)
  RETURNS TEXT
  LANGUAGE SQL
AS
BEGIN
  CREATE OR REPLACE TABLE IDENTIFIER(:new_table) AS
    SELECT * FROM IDENTIFIER(:existing_table);
  RETURN 'Table created';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE ctas_sp(existing_table VARCHAR, new_table VARCHAR)
  RETURNS TEXT
  LANGUAGE SQL
AS
$$
BEGIN
  CREATE OR REPLACE TABLE IDENTIFIER(:new_table) AS
    SELECT * FROM IDENTIFIER(:existing_table);
  RETURN 'Table created';
END;
$$
;
```

Before calling the procedure, create a simple table and insert data:

Copy code

```
CREATE OR REPLACE TABLE test_table_for_ctas_sp (
  id NUMBER(2),
  v  VARCHAR(2))
AS SELECT
  column1,
  column2,
FROM
  VALUES
    (1, 'a'),
    (2, 'b'),
    (3, 'c');
```

Call the stored procedure to create a new table that is based on this table:

Copy code

```
CALL ctas_sp('test_table_for_ctas_sp', 'test_table_for_ctas_sp_backup');
```

#### Using an argument when building a string for a SQL statement

Note that if you are building a SQL statement as a string to be passed to
[EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) (see [Assigning a query to a declared RESULTSET](/developer-guide/snowflake-scripting/resultsets#label-snowscript-resultsets-assign)), do not prefix the argument with a
colon. For example:

Copy code

```
CREATE OR REPLACE PROCEDURE find_invoice_by_id_via_execute_immediate(id VARCHAR)
RETURNS TABLE (id INTEGER, price NUMBER(12,2))
LANGUAGE SQL
AS
DECLARE
  select_statement VARCHAR;
  res RESULTSET;
BEGIN
  select_statement := 'SELECT * FROM invoices WHERE id = ' || id;
  res := (EXECUTE IMMEDIATE :select_statement);
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE find_invoice_by_id_via_execute_immediate(id VARCHAR)
RETURNS TABLE (id INTEGER, price NUMBER(12,2))
LANGUAGE SQL
AS
$$
DECLARE
  select_statement VARCHAR;
  res RESULTSET;
BEGIN
  select_statement := 'SELECT * FROM invoices WHERE id = ' || id;
  res := (EXECUTE IMMEDIATE :select_statement);
  RETURN TABLE(res);
END;
$$
;
```

#### Using an output argument to return a single value

The following example creates the stored procedure `simple_out_sp_demo` with the output argument `xout` in
its definition. The stored procedure sets the value of `xout` to `2`.

Copy code

```
CREATE OR REPLACE PROCEDURE simple_out_sp_demo(xout OUT NUMBER)
  RETURNS STRING
  LANGUAGE SQL
AS
BEGIN
  xout := 2;
  RETURN 'Done';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE simple_out_sp_demo(xout OUT NUMBER)
  RETURNS STRING
  LANGUAGE SQL
AS
$$
BEGIN
  xout := 2;
  RETURN 'Done';
END;
$$
;
```

The following anonymous block sets the value of the `x` variable to `1`. Then, it calls the `simple_out_sp_demo`
stored procedure and specifies the variable as the argument.

Copy code

```
BEGIN
  LET x := 1;
  CALL simple_out_sp_demo(:x);
  RETURN x;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE
$$
BEGIN
  LET x := 1;
  CALL simple_out_sp_demo(:x);
  RETURN x;
END;
$$
;
```

The output shows that the `simple_out_sp_demo` stored procedure performed an operation to set the value of the
output argument to `2` and then returned this value to the anonymous block.

```
+-----------------+
| anonymous block |
%-----------------%
|               2 |
+-----------------+
```

The following anonymous block calls `simple_out_sp_demo` stored procedure and returns an error, because it tries to
assign a value to the output argument using an expression instead of a variable.

Copy code

```
BEGIN
  LET x := 1;
  CALL simple_out_sp_demo(:x + 2);
  RETURN x;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE
$$
BEGIN
  LET x := 1;
  CALL simple_out_sp_demo(:x + 2);
  RETURN x;
END;
$$
;
```

#### Using output arguments to return several values for multiple calls to a stored procedure

The following example demonstrates the following behavior related to stored procedures and
input and output arguments:

- A stored procedure can have several input and output arguments in its definition.
- A program can call a stored procedure with output arguments multiple times, and the values of the
  output arguments are preserved after each call.
- Input arguments don’t return values to the calling program.

Create the stored procedure `multiple_out_sp_demo` with multiple input and output arguments in its
definition. The stored procedure performs the same operations on the equivalent input and output arguments.
For example, the stored procedure adds `1` to the `p1_in` input argument and to the `p1_out` output
argument.

Copy code

```
CREATE OR REPLACE PROCEDURE multiple_out_sp_demo(
    p1_in NUMBER,
    p1_out OUT NUMBER,
    p2_in VARCHAR(100),
    p2_out OUT VARCHAR(100),
    p3_in BOOLEAN,
    p3_out OUT BOOLEAN)
  RETURNS NUMBER
  LANGUAGE SQL
AS
BEGIN
  p1_in := p1_in + 1;
  p1_out := p1_out + 1;
  p2_in := p2_in || ' hi ';
  p2_out := p2_out || ' hi ';
  p3_in := (NOT p3_in);
  p3_out := (NOT p3_out);
  RETURN 1;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE multiple_out_sp_demo(
    p1_in NUMBER,
    p1_out OUT NUMBER,
    p2_in VARCHAR(100),
    p2_out OUT VARCHAR(100),
    p3_in BOOLEAN,
    p3_out OUT BOOLEAN)
  RETURNS NUMBER
  LANGUAGE SQL
AS
$$
BEGIN
  p1_in := p1_in + 1;
  p1_out := p1_out + 1;
  p2_in := p2_in || ' hi ';
  p2_out := p2_out || ' hi ';
  p3_in := (NOT p3_in);
  p3_out := (NOT p3_out);
  RETURN 1;
END;
$$
;
```

The following anonymous block assigns values to the variables that correspond to the arguments of the
`multiple_out_sp_demo` stored procedure and then calls the stored procedure multiple times. The first
call uses the variable values specified in the anonymous block, but each subsequent call uses the values
returned by the output arguments in the `multiple_out_sp_demo` stored procedure.

Copy code

```
BEGIN
  LET x_in INT := 1;
  LET x_out INT := 1;
  LET y_in VARCHAR(100) := 'hello';
  LET y_out VARCHAR(100) := 'hello';
  LET z_in BOOLEAN := true;
  LET z_out BOOLEAN := true;

  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  RETURN [x_in, x_out, y_in, y_out, z_in, z_out];
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE
$$
BEGIN
  LET x_in INT := 1;
  LET x_out INT := 1;
  LET y_in VARCHAR(100) := 'hello';
  LET y_out VARCHAR(100) := 'hello';
  LET z_in BOOLEAN := true;
  LET z_out BOOLEAN := true;

  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  CALL multiple_out_sp_demo(:x_in, :x_out, :y_in, :y_out, :z_in, :z_out);
  RETURN [x_in, x_out, y_in, y_out, z_in, z_out];
END;
$$
;
```

```
+------------------------+
| anonymous block        |
%------------------------%
| [                      |
|   1,                   |
|   4,                   |
|   "hello",             |
|   "hello hi  hi  hi ", |
|   true,                |
|   false                |
| ]                      |
+------------------------+
```

#### Using an output argument with a different data type than the input value from a calling procedure

For some use cases, there might be a mismatch between the data type of the value being passed in to a stored
procedure and the data type of the procedure’s output argument. In these cases,
[supported coercions](/sql-reference/data-type-conversion#label-valid-casting-and-coercions) are performed automatically.

Note

Although coercion is supported in some cases, it isn’t recommended.

This example demonstrates automatic conversion of a FLOAT value that is passed to an output argument with
a NUMBER data type. The FLOAT value is automatically converted to a NUMBER value and then passed back to the
calling anonymous block.

Create the `sp_out_coercion` stored procedure, which takes an output argument of type NUMBER:

Copy code

```
CREATE OR REPLACE PROCEDURE sp_out_coercion(x OUT NUMBER)
  RETURNS STRING
  LANGUAGE SQL
AS
BEGIN
  x := x * 2;
  RETURN 'Done';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE sp_out_coercion(x OUT NUMBER)
  RETURNS STRING
  LANGUAGE SQL
AS
$$
BEGIN
  x := x * 2;
  RETURN 'Done';
END;
$$
;
```

Execute an anonymous block that passes a FLOAT value to the `sp_out_coercion` stored procedure:

Copy code

```
BEGIN
  LET a FLOAT := 500.662;
  CALL sp_out_coercion(:a);
  RETURN a || ' (Type ' || SYSTEM$TYPEOF(a) || ')';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE
$$
BEGIN
  LET a FLOAT := 500.662;
  CALL sp_out_coercion(:a);
  RETURN a || ' (Type ' || SYSTEM$TYPEOF(a) || ')';
END;
$$
;
```

The output shows both the returned value and the data type of the returned value, by calling the
[SYSTEM$TYPEOF](/sql-reference/functions/system_typeof) function. Note that the value is coerced from a
NUMBER value back to a FLOAT value after it is returned from the stored procedure:

```
+---------------------------+
| anonymous block           |
%---------------------------%
| 1002 (Type FLOAT[DOUBLE]) |
+---------------------------+
```

#### Using an output argument to return the total sales for an employee in a quarter

This example uses the following `quarterly_sales` table:

Copy code

```
CREATE OR REPLACE TABLE quarterly_sales(
  empid INT,
  amount INT,
  quarter TEXT)
  AS SELECT * FROM VALUES
    (1, 10000, '2023_Q1'),
    (1, 400, '2023_Q1'),
    (2, 4500, '2023_Q1'),
    (2, 35000, '2023_Q1'),
    (1, 5000, '2023_Q2'),
    (1, 3000, '2023_Q2'),
    (2, 200, '2023_Q2'),
    (2, 90500, '2023_Q2'),
    (1, 6000, '2023_Q3'),
    (1, 5000, '2023_Q3'),
    (2, 2500, '2023_Q3'),
    (2, 9500, '2023_Q3'),
    (3, 2700, '2023_Q3'),
    (1, 8000, '2023_Q4'),
    (1, 10000, '2023_Q4'),
    (2, 800, '2023_Q4'),
    (2, 4500, '2023_Q4'),
    (3, 2700, '2023_Q4'),
    (3, 16000, '2023_Q4'),
    (3, 10200, '2023_Q4');
```

Create the stored procedure `sales_total_out_sp_demo` that takes two input arguments for the
employee identifier and quarter, and one output argument to calculate the sales total for the
given employee and quarter.

Copy code

```
CREATE OR REPLACE PROCEDURE sales_total_out_sp_demo(
    id INT,
    quarter VARCHAR(20),
    total_sales OUT NUMBER(38,0))
  RETURNS STRING
  LANGUAGE SQL
AS
$$
BEGIN
  SELECT SUM(amount) INTO total_sales FROM quarterly_sales
    WHERE empid = :id AND
          quarter = :quarter;
  RETURN 'Done';
END;
$$
;
```

Create the stored procedure `emp_quarter_calling_sp_demo` that calls the `sales_total_out_sp_demo`
stored procedure. This stored procedure also takes two input arguments for the employee identifier and quarter.

Copy code

```
CREATE OR REPLACE PROCEDURE emp_quarter_calling_sp_demo(
    id INT,
    quarter VARCHAR(20))
  RETURNS STRING
  LANGUAGE SQL
AS
BEGIN
  LET x NUMBER(38,0);
  CALL sales_total_out_sp_demo(:id, :quarter, :x);
  RETURN 'Total sales for employee ' || id || ' in quarter ' || quarter || ': ' || x;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE emp_quarter_calling_sp_demo(
    id INT,
    quarter VARCHAR(20))
  RETURNS STRING
  LANGUAGE SQL
AS
$$
BEGIN
  LET x NUMBER(38,0);
  CALL sales_total_out_sp_demo(:id, :quarter, :x);
  RETURN 'Total sales for employee ' || id || ' in quarter ' || quarter || ': ' || x;
END;
$$
;
```

Call the `emp_quarter_calling_sp_demo` with the arguments `2` (for the employee identifier) and
`'2023_Q4'` (for the quarter).

Copy code

```
CALL emp_quarter_calling_sp_demo(2, '2023_Q4');
```

```
+-----------------------------------------------------+
| emp_quarter_calling_sp_demo                         |
%-----------------------------------------------------%
| Total sales for employee 2 in quarter 2023_Q4: 5300 |
+-----------------------------------------------------+
```

## Returning tabular data

If you need to return tabular data (for example, data from a RESULTSET) from your stored procedure, specify
RETURNS TABLE(…) in your [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement.

If you know the [Snowflake data types](/sql-reference-data-types) of the columns in the returned table, specify the column
names and types in the RETURNS TABLE().

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
...
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

If you need to return the data in a RESULTSET, use TABLE() in your
[RETURN](/sql-reference/snowflake-scripting/return) statement.

For example:

Copy code

```
CREATE OR REPLACE PROCEDURE get_top_sales()
RETURNS TABLE (sales_date DATE, quantity NUMBER)
LANGUAGE SQL
AS
DECLARE
  res RESULTSET DEFAULT (SELECT sales_date, quantity FROM sales ORDER BY quantity DESC LIMIT 10);
BEGIN
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE get_top_sales()
RETURNS TABLE (sales_date DATE, quantity NUMBER)
LANGUAGE SQL
AS
$$
DECLARE
  res RESULTSET DEFAULT (SELECT sales_date, quantity FROM sales ORDER BY quantity DESC LIMIT 10);
BEGIN
  RETURN TABLE(res);
END;
$$
;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL get_top_sales();
```

## Calling a stored procedure from another stored procedure

In a stored procedure, if you need to call another stored procedure, use one of the following approaches:

- [Calling a stored procedure without using the returned value](#label-stored-procedure-snowscript-call-sp-no-return-value)
- [Using the value returned from a stored procedure call](#label-stored-procedure-snowscript-call-sp-return-value)
- [Passing output argument values from a stored procedure to a calling stored procedure](#label-stored-procedure-snowscript-call-sp-output-argument-values)

### Calling a stored procedure without using the returned value

Use a [CALL](/sql-reference/sql/call) statement to call the stored procedure (as you normally would).

If you need to pass in any variables or arguments as input arguments in the CALL statement, remember to use a colon (`:`) in
front of the variable name. (See [Using a variable in a SQL statement (binding)](/developer-guide/snowflake-scripting/variables#label-snowscript-variables-binding).)

The following is an example of a stored procedure that calls another stored procedure but does not depend on the return value.

First, create a table for use in the example:

Copy code

```
-- Create a table for use in the example.
CREATE OR REPLACE TABLE int_table (value INTEGER);
```

Then, create the stored procedure that you will call from another stored procedure:

Copy code

```
-- Create a stored procedure to be called from another stored procedure.
CREATE OR REPLACE PROCEDURE insert_value(value INTEGER)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
BEGIN
  INSERT INTO int_table VALUES (:value);
  RETURN 'Rows inserted: ' || SQLROWCOUNT;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
-- Create a stored procedure to be called from another stored procedure.
CREATE OR REPLACE PROCEDURE insert_value(value INTEGER)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
$$
BEGIN
  INSERT INTO int_table VALUES (:value);
  RETURN 'Rows inserted: ' || SQLROWCOUNT;
END;
$$
;
```

Next, create a second stored procedure that calls the first stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE insert_two_values(value1 INTEGER, value2 INTEGER)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
BEGIN
  CALL insert_value(:value1);
  CALL insert_value(:value2);
  RETURN 'Finished calling stored procedures';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE insert_two_values(value1 INTEGER, value2 INTEGER)
RETURNS VARCHAR NOT NULL
LANGUAGE SQL
AS
$$
BEGIN
  CALL insert_value(:value1);
  CALL insert_value(:value2);
  RETURN 'Finished calling stored procedures';
END;
$$
;
```

Finally, call the second stored procedure:

Copy code

```
CALL insert_two_values(4, 5);
```

### Using the value returned from a stored procedure call

If you are calling a stored procedure that returns a scalar value, and you need to access that value, use the
`INTO :snowflake_scripting_variable` clause in the [CALL](/sql-reference/sql/call) statement to capture the value in a
[Snowflake Scripting variable](/developer-guide/snowflake-scripting/variables).

The following example calls the `get_row_count` stored procedure that was defined in
[Using an argument as an object identifier](#label-stored-procedure-snowscript-arguments-identifier).

Copy code

```
CREATE OR REPLACE PROCEDURE count_greater_than(table_name VARCHAR, maximum_count INTEGER)
  RETURNS BOOLEAN NOT NULL
  LANGUAGE SQL
  AS
  DECLARE
    count1 NUMBER;
  BEGIN
    CALL get_row_count(:table_name) INTO :count1;
    IF (:count1 > maximum_count) THEN
      RETURN TRUE;
    ELSE
      RETURN FALSE;
    END IF;
  END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE count_greater_than(table_name VARCHAR, maximum_count INTEGER)
  RETURNS BOOLEAN NOT NULL
  LANGUAGE SQL
  AS
  $$
  DECLARE
    count1 NUMBER;
  BEGIN
    CALL get_row_count(:table_name) INTO :count1;
    IF (:count1 > maximum_count) THEN
      RETURN TRUE;
    ELSE
      RETURN FALSE;
    END IF;
  END;
  $$
  ;
```

The following is an example of calling the stored procedure:

Copy code

```
CALL count_greater_than('invoices', 3);
```

If the stored procedure returns a table, you can capture the return value by setting a
[RESULTSET](/developer-guide/snowflake-scripting/resultsets) to a string containing the CALL statement. (See
[Assigning a query to a declared RESULTSET](/developer-guide/snowflake-scripting/resultsets#label-snowscript-resultsets-assign).)

To retrieve the return value from the call, you can use a
[CURSOR for the RESULTSET](/developer-guide/snowflake-scripting/resultsets#label-snowscript-resultsets-use-cursor). For example:

Copy code

```
DECLARE
  res1 RESULTSET;
BEGIN
res1 := (CALL my_procedure());
LET c1 CURSOR FOR res1;
FOR row_variable IN c1 DO
  IF (row_variable.col1 > 0) THEN
    ...;
  ELSE
    ...;
  END IF;
END FOR;
...
```

### Passing output argument values from a stored procedure to a calling stored procedure

When an output argument is specified in the definition of a Snowflake Scripting stored procedure, the stored procedure
can return the current value of the output argument to a calling stored procedure. The stored procedure takes an initial value
for the output argument, saves the value to a variable in the procedure body, and optionally performs operations to change the
value of the variable. The stored procedure then returns the updated value to the calling stored procedure.

For an example, see [Using an output argument to return the total sales for an employee in a quarter](#label-snowflake-scripting-out-arguments-total-sales).

## Using nested stored procedures

A *nested stored procedure* is a stored procedure that’s defined within the scope of an anonymous block or
a block in another stored procedure (the *parent stored procedure*).

You declare a nested stored procedure in the [DECLARE](/sql-reference/snowflake-scripting/declare) section
of a block, which can be part of a [CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement. The following example
shows a nested stored procedure declaration:

Copy code

```
DECLARE
  <nested_stored_procedure_name> PROCEDURE (<arguments>)
     RETURNS <data_type>
     AS
     BEGIN
       <nested_procedure_procedure_statements>
     END;
BEGIN
  <statements>
END;
```

For information about the declaration syntax of a nested stored procedure, see
[Nested stored procedure declaration syntax](/sql-reference/snowflake-scripting/declare#label-snowscript-declare-syntax-nested-stored-procedure).

A nested stored procedure only exists within the scope of its [block](/developer-guide/snowflake-scripting/blocks).
It can be called from any section of its block (DECLARE, BEGIN … END, and EXCEPTION). A single block can contain
multiple nested stored procedures, and one nested stored procedure can call another nested stored procedure in the
same block. A nested procedure can’t be called or accessed from outside of its block.

A nested stored procedure operates in the same security context as the block that defines it. When a nested stored
procedure is defined in a parent stored procedure, it automatically runs with the same privileges as the parent
stored procedure.

Note

Both a nested stored procedure declaration and the [CALL WITH](/sql-reference/sql/call-with) command
create a temporary stored procedure with limited scope. They differ in the following ways:

- A CALL WITH statement can appear anywhere that a SQL statement can, including within a stored procedure, but a
  nested stored procedure declaration must be in a Snowflake Scripting block.
- A CALL WITH stored procedure only exists in the scope of its statement, but a nested stored procedure exists in
  the scope of its Snowflake Scripting block.

### Benefits of nested stored procedures

Nested stored procedures provide the following benefits:

- They can enhance and simplify security by encapsulating logic inside an anonymous block or parent stored procedure,
  which prevents access to it from outside the block or parent.
- They keep code modular by splitting it logically into smaller chunks, which can make it easier to maintain and
  debug.
- They improve maintainability by reducing the need for global variables or additional arguments, because a nested stored
  procedure can directly access the local variables of its block.

### Usage notes for calling nested stored procedures

The following usage notes apply to calling a nested stored procedure:

- To pass arguments to a nested stored procedure, a block can use constant values,
  [Snowflake Scripting variables](/developer-guide/snowflake-scripting/variables),
  [bind variables](/sql-reference/bind-variables), [SQL (session) variables](/sql-reference/session-variables),
  and calls to [user-defined functions](/developer-guide/udf/udf-overview).
- When there is a mismatch between the data type of the value being passed in and the data type of an argument,
  Snowflake performs supported coercions automatically. For information about which coercions Snowflake can perform
  automatically, see [Data type conversion](/sql-reference/data-type-conversion).

### Usage notes for variables in a nested stored procedure

The following usage notes apply to variables in a nested stored procedure:

- A nested stored procedure can reference variables from its block that were declared before the nested
  stored procedure declaration in the DECLARE section of its block. It can’t reference variables declared
  after it in the DECLARE section.
- A nested stored procedure can’t access variables declared in a LET statement in the BEGIN … END
  section of a block.
- The value of a referenced variable reflects its value at the time when the nested stored procedure is called.
- A nested stored procedure can modify a referenced variable value, and the modified value persists in the block
  and across multiple invocations of the same nested procedure in a single execution
  of its anonymous block or in a single call to its parent stored procedure.
- The value of a variable that was declared before a nested stored procedure call can be passed as an argument to
  the nested stored procedure. The variable value can be passed as an argument in a call even if the variable
  was declared after the nested stored procedure declaration or in a LET statement.

For example, the following stored procedure declares several variables:

Copy code

```
CREATE OR REPLACE PROCEDURE outer_sp ()
RETURNS NUMBER
LANGUAGE SQL
AS
$$
DECLARE
  var_before_nested_proc NUMBER DEFAULT 1;
  test_nested_variables PROCEDURE(arg1 NUMBER)
    -- <nested_sp_logic>
  var_after_nested_proc NUMBER DEFAULT 2;
BEGIN
  LET var_let_before_call NUMBER DEFAULT 3;
  LET result := CALL nested_proc(:<var_name>);
  LET var_let_after_call NUMBER DEFAULT 3;
  RETURN result;
END;
$$;
```

In this example, only `var_before_nested_proc` can be referenced in `nested_sp_logic`.

In the nested stored procedure call, the value of any of the following variables can be passed to the nested stored
procedure as an argument in `var_name`:

- `var_before_nested_proc`
- `var_after_nested_proc`
- `var_let_before_call`

The value of `var_let_after_call` can’t be passed to the nested stored procedure as an argument.

### Limitations for nested stored procedures

The following limitations apply to defining nested stored procedures:

- They can’t be defined inside other nested stored procedures or inside control structures, such as
  FOR or WHILE loops.
- Each nested stored procedure must have a unique name in its block. That is, nested stored procedures can’t
  be overloaded.
- They don’t support output (OUT) arguments.
- They don’t support optional arguments with default values.

The following limitations apply to calling nested stored procedures:

- They can’t be called in an [EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) statement.
- They can’t be called in [asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs).
- They don’t support named input arguments (`arg_name => arg`). Arguments must be
  specified by position. For more information, see [CALL](/sql-reference/sql/call).

### Examples of nested stored procedures

The following examples use nested stored procedures:

- [Define a nested stored procedure that returns tabular data](#label-stored-procedure-snowscript-nested-stored-procedures-example-table)
- [Define a nested stored procedure that returns a scalar value](#label-stored-procedure-snowscript-nested-stored-procedures-example-scalar)
- [Define a nested stored procedure in an anonymous block](#label-stored-procedure-snowscript-nested-stored-procedures-example-anonymous-block)
- [Define a nested stored procedure that is passed arguments](#label-stored-procedure-snowscript-nested-stored-procedures-example-arguments)
- [Define a nested stored procedure that calls another nested stored procedure](#label-stored-procedure-snowscript-nested-stored-procedures-example-call-from-nested)

#### Define a nested stored procedure that returns tabular data

The following example defines a nested stored procedure that returns a tabular data. The example creates a
parent stored procedure called `nested_procedure_example_table` with a nested stored procedure
called `nested_return_table`. The code includes the following logic:

- Declares a variable called `res` of type RESULTSET.
- Includes the following logic in the nested stored procedure:

  - Declares a variable called `res2`.
  - Inserts values into a table called `nested_table`.
  - Sets the `res2` variable to the results of a SELECT on the table.
  - Returns the tabular data in the result set.
- Creates the table `nested_table` in the parent stored procedure.
- Calls the nested stored procedure `nested_return_table` and sets the `res` variable to the results of the call
  to the nested stored procedure.
- Returns the tabular results in the `res` variable.

Copy code

```
CREATE OR REPLACE PROCEDURE nested_procedure_example_table()
RETURNS TABLE()
LANGUAGE SQL
AS
$$
DECLARE
  res RESULTSET;
  nested_return_table PROCEDURE()
    RETURNS TABLE()
    AS
    DECLARE
      res2 RESULTSET;
    BEGIN
      INSERT INTO nested_table VALUES(1);
      INSERT INTO nested_table VALUES(2);
      res2 := (SELECT * FROM nested_table);
      RETURN TABLE(res2);
    END;
BEGIN
  CREATE OR REPLACE TABLE nested_table(col1 INT);
  res := (CALL nested_return_table());
  RETURN TABLE(res);
END;
$$;
```

Call the stored procedure:

Copy code

```
CALL nested_procedure_example_table();
```

```
+------+
| COL1 |
%------%
|    1 |
|    2 |
+------+
```

#### Define a nested stored procedure that returns a scalar value

The following example defines a nested stored procedure that returns a scalar value. The example creates a
parent stored procedure called `nested_procedure_example_scalar` with a nested stored procedure
called `simple_counter`. The code includes the following logic:

- Declares a variable called `counter` of type NUMBER, and sets the value of this variable to `0`.
- Specifies that the nested stored procedure adds `1` to the current value of the `counter` variable.
- Calls the nested stored procedure three times in the parent stored procedure. The value of the `counter`
  variable is carried over between invocations of the nested stored procedure.
- Returns the value of the `counter` variable, which is `3`.

Copy code

```
CREATE OR REPLACE PROCEDURE nested_procedure_example_scalar()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
  counter NUMBER := 0;
  simple_counter PROCEDURE()
    RETURNS VARCHAR
    AS
    BEGIN
      counter := counter + 1;
      RETURN counter;
    END;
BEGIN
  CALL simple_counter();
  CALL simple_counter();
  CALL simple_counter();
  RETURN counter;
END;
$$;
```

Call the stored procedure:

Copy code

```
CALL nested_procedure_example_scalar();
```

```
+---------------------------------+
| NESTED_PROCEDURE_EXAMPLE_SCALAR |
%---------------------------------%
| 3                               |
+---------------------------------+
```

#### Define a nested stored procedure in an anonymous block

The following example is the same as the example in [Define a nested stored procedure that returns a scalar value](#label-stored-procedure-snowscript-nested-stored-procedures-example-scalar),
except that it defines a nested stored procedure in an anonymous block instead of a stored procedure:

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  counter NUMBER := 0;
  simple_counter PROCEDURE()
    RETURNS VARCHAR
    AS
    BEGIN
      counter := counter + 1;
      RETURN counter;
    END;
BEGIN
  CALL simple_counter();
  CALL simple_counter();
  CALL simple_counter();
  RETURN counter;
END;
$$;
```

```
+-----------------+
| anonymous block |
%-----------------%
|               3 |
+-----------------+
```

#### Define a nested stored procedure that is passed arguments

The following example defines a nested stored procedure that is passed arguments. In the example, the nested
stored procedure inserts values into the following table:

Copy code

```
CREATE OR REPLACE TABLE log_nested_values(col1 INT, col2 INT);
```

The example creates a parent stored procedure called `nested_procedure_example_arguments` with a nested stored procedure
called `log_and_multiply_numbers`. The nested stored procedure takes two arguments of type NUMBER. The code includes the
following logic:

- Declares variables `a`, `b`, and `x` of type NUMBER.
- Includes a nested stored procedure that performs the following actions:

  - Inserts the two number values passed to it by the parent stored procedure into the `log_nested_values` table
    using bind variables.
  - Sets the value of variable `x` to the result of multiplying the two argument values.
  - Returns the value of `x` to the parent stored procedure.
- Sets the value of variable `a` to `5` and variable `b` to `10`.
- Calls the nested stored procedure.
- Returns the value of the `x` variable, which was set in the nested stored procedure.

Copy code

```
CREATE OR REPLACE PROCEDURE nested_procedure_example_arguments()
RETURNS NUMBER
LANGUAGE SQL
AS
$$
DECLARE
  a NUMBER;
  b NUMBER;
  x NUMBER;
  log_and_multiply_numbers PROCEDURE(num1 NUMBER, num2 NUMBER)
    RETURNS NUMBER
    AS
    BEGIN
      INSERT INTO log_nested_values VALUES(:num1, :num2);
      x := :num1 * :num2;
      RETURN x;
    END;
BEGIN
  a := 5;
  b := 10;
  CALL log_and_multiply_numbers(:a, :b);
  RETURN x;
END;
$$;
```

Call the stored procedure:

Copy code

```
CALL nested_procedure_example_arguments();
```

```
+------------------------------------+
| NESTED_PROCEDURE_EXAMPLE_ARGUMENTS |
%------------------------------------%
|                                 50 |
+------------------------------------+
```

Query the `log_nested_values` table to confirm that the nested stored procedure inserted the
values passed to it:

Copy code

```
SELECT * FROM log_nested_values;
```

```
+------+------+
| COL1 | COL2 |
|------+------|
|    5 |   10 |
+------+------+
```

#### Define a nested stored procedure that calls another nested stored procedure

The following example defines a nested stored procedure that calls another nested stored procedure. The example creates a
parent stored procedure called `nested_procedure_example_call_from_nested` with two nested stored procedures
called `counter_nested_proc` and `call_counter_nested_proc`. The code includes the following logic:

- Declares a variable called `counter` of type NUMBER, and sets the value of this variable to `0`.
- Includes the nested stored procedure `counter_nested_proc` that adds `10` to the value of `counter`.
- Includes the nested stored procedure `call_counter_nested_proc` that adds `15` to the value of `counter`
  and also calls `counter_nested_proc` (which adds another `10` to the value of `counter`).
- Calls both nested stored procedures in the parent stored procedure.
- Returns the value of the `counter` variable, which is `35`.

Copy code

```
CREATE OR REPLACE PROCEDURE nested_procedure_example_call_from_nested()
RETURNS NUMBER
LANGUAGE SQL
AS
$$
DECLARE
  counter NUMBER := 0;
  counter_nested_proc PROCEDURE()
    RETURNS NUMBER
    AS
    DECLARE
      var1 NUMBER := 10;
    BEGIN
      counter := counter + var1;
    END;
  call_counter_nested_proc PROCEDURE()
    RETURNS NUMBER
    AS
    DECLARE
      var2 NUMBER := 15;
    BEGIN
      counter := counter + var2;
      CALL counter_nested_proc();
    END;
BEGIN
  counter := 0;
  CALL counter_nested_proc();
  CALL call_counter_nested_proc();
  RETURN counter;
END;
$$;
```

Call the stored procedure:

Copy code

```
CALL nested_procedure_example_call_from_nested();
```

```
+-------------------------------------------+
| NESTED_PROCEDURE_EXAMPLE_CALL_FROM_NESTED |
%-------------------------------------------%
|                                        35 |
+-------------------------------------------+
```

## Using and setting SQL variables in a stored procedure

By default, Snowflake Scripting stored procedures run with owner’s rights. When a
stored procedure runs with owner’s rights, it can’t access
[SQL (or session) variables](/sql-reference/session-variables).

However, a caller’s rights stored procedure can read the caller’s session variables and use
them in the logic of the stored procedure. For example, a caller’s rights stored procedure
can use the value in a SQL variable in a query. To create a stored procedure that runs with
caller’s rights, specify the `EXECUTE AS CALLER` parameter in the
[CREATE PROCEDURE](/sql-reference/sql/create-procedure) statement.

These examples illustrate this key difference between caller’s rights and owner’s rights stored
procedures. They attempt to use SQL variables in two ways:

- Set a SQL variable before calling the stored procedure, then use the SQL variable inside the stored
  procedure.
- Set a SQL variable inside the stored procedure, then use the SQL variable after returning from the stored
  procedure.

Both using the SQL variable and setting the SQL variable work correctly in a caller’s rights stored procedure.
Both fail when using an owner’s rights stored procedure, even if the caller is the owner.

For more information about owner’s rights and caller’s rights, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).

### Using a SQL variable in a stored procedure

The following example uses a SQL variable in a stored procedure.

First, set a SQL variable in a session:

Copy code

```
SET example_use_variable = 2;
```

Create a simple stored procedure that runs with caller’s rights and uses this SQL variable:

Copy code

```
CREATE OR REPLACE PROCEDURE use_sql_variable_proc()
RETURNS NUMBER
LANGUAGE SQL
EXECUTE AS CALLER
AS
DECLARE
  sess_var_x_2 NUMBER;
BEGIN
  sess_var_x_2 := 2 * $example_use_variable;
  RETURN sess_var_x_2;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE use_sql_variable_proc()
RETURNS NUMBER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  sess_var_x_2 NUMBER;
BEGIN
  sess_var_x_2 := 2 * $example_use_variable;
  RETURN sess_var_x_2;
END;
$$
;
```

Call the stored procedure:

Copy code

```
CALL use_sql_variable_proc();
```

```
+-----------------------+
| USE_SQL_VARIABLE_PROC |
%-----------------------%
|                     4 |
+-----------------------+
```

Set the SQL variable to a different value:

Copy code

```
SET example_use_variable = 9;
```

Call the procedure again to see that the returned value has changed:

Copy code

```
CALL use_sql_variable_proc();
```

```
+-----------------------+
| USE_SQL_VARIABLE_PROC |
%-----------------------%
|                    18 |
+-----------------------+
```

### Setting a SQL variable in a stored procedure

You can set a SQL variable in a stored procedure that’s running with caller’s rights. For
more information, including guidelines for using SQL variables in stored procedures, see
[Caller’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-caller).

Note

Although you can set a SQL variable inside a stored procedure and leave it set after the end of the procedure,
Snowflake does not recommend doing this.

The following example sets a SQL variable in a stored procedure.

First, set a SQL variable in a session:

Copy code

```
SET example_set_variable = 55;
```

Confirm the value of the SQL variable:

Copy code

```
SHOW VARIABLES LIKE 'example_set_variable';
```

```
+----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
|     session_id | created_on                    | updated_on                    | name                 | value | type  | comment |
|----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------|
| 10363782631910 | 2024-11-27 08:18:32.007 -0800 | 2024-11-27 08:20:17.255 -0800 | EXAMPLE_SET_VARIABLE | 55    | fixed |         |
+----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
```

For example, the following stored procedure sets the SQL variable `example_set_variable`
to a new value and returns the new value:

Copy code

```
CREATE OR REPLACE PROCEDURE set_sql_variable_proc()
RETURNS NUMBER
LANGUAGE SQL
EXECUTE AS CALLER
AS
BEGIN
  SET example_set_variable = $example_set_variable - 3;
  RETURN $example_set_variable;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE set_sql_variable_proc()
RETURNS NUMBER
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
  SET example_set_variable = $example_set_variable - 3;
  RETURN $example_set_variable;
END;
$$
;
```

Call the stored procedure:

Copy code

```
CALL set_sql_variable_proc();
```

```
+-----------------------+
| SET_SQL_VARIABLE_PROC |
%-----------------------%
|                    52 |
+-----------------------+
```

Confirm the new value of the SQL variable:

Copy code

```
SHOW VARIABLES LIKE 'example_set_variable';
```

```
+----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
|     session_id | created_on                    | updated_on                    | name                 | value | type  | comment |
|----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------|
| 10363782631910 | 2024-11-27 08:18:32.007 -0800 | 2024-11-27 08:24:04.027 -0800 | EXAMPLE_SET_VARIABLE | 52    | fixed |         |
+----------------+-------------------------------+-------------------------------+----------------------+-------+-------+---------+
```
