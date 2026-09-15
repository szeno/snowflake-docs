# CASE (Snowflake Scripting)

A `CASE` statement provides a way to specify multiple conditions.

For more information on branching constructs, see [Working with conditional logic](/developer-guide/snowflake-scripting/branch).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

## Syntax

**Simple CASE statement:**

> Copy code
>
> ```
> CASE ( <expression_to_match> )
>     WHEN <expression> THEN
>         <statement>;
>         [ <statement>; ... ]
>     [ WHEN ... ]
>     [ ELSE
>         <statement>;
>         [ <statement>; ... ]
>     ]
> END [ CASE ] ;
> ```

Where:

> `expression_to_match`
> :   The expression to match.
>
> `expression`
> :   If the value of this expression matches the value of `expression_to_match`, then the statements in this clause
>     are executed.
>
> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).

**Searched CASE statement:**

> Copy code
>
> ```
> CASE
>     WHEN <boolean_expression> THEN
>         <statement>;
>         [ <statement>; ... ]
>     [ WHEN ... ]
>     [ ELSE
>         <statement>;
>         [ <statement>; ... ]
>     ]
> END [ CASE ] ;
> ```

Where:

> `boolean_expression`
> :   If this expression evaluates to TRUE, then the statements in this clause are executed.
>
> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).

## Usage notes

- If more than one branch of the `CASE` would match the expression, only the first is used.
- When you compare expressions, NULL does not match NULL. If you wish to test explicitly for NULL values, use
  [IS [ NOT ] NULL](/sql-reference/functions/is-null).

## Examples

This example demonstrates a simple `CASE` statement:

> Copy code
>
> ```
> CREATE PROCEDURE case_demo_01(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
>   BEGIN
>     CASE (v)
>       WHEN 'first choice' THEN
>         RETURN 'one';
>       WHEN 'second choice' THEN
>         RETURN 'two';
>       ELSE
>         RETURN 'unexpected choice';
>     END;
>   END;
> ```
>
> Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
> `execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
> code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):
>
> Copy code
>
> ```
> CREATE PROCEDURE case_demo_01(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     BEGIN
>         CASE (v)
>             WHEN 'first choice' THEN
>                 RETURN 'one';
>             WHEN 'second choice' THEN
>                 RETURN 'two';
>             ELSE
>                 RETURN 'unexpected choice';
>        END CASE;
>     END;
> $$
> ;
> ```

When you call this stored procedure, the procedure produces the following output:

> Copy code
>
> ```
> CALL case_demo_01('second choice');
> +--------------+
> | CASE_DEMO_01 |
> |--------------|
> | two          |
> +--------------+
> ```

This example demonstrates a searched `CASE` statement:

> Copy code
>
> ```
> CREATE PROCEDURE case_demo_2(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
>   BEGIN
>     CASE
>       WHEN v = 'first choice' THEN
>         RETURN 'one';
>       WHEN v = 'second choice' THEN
>         RETURN 'two';
>       ELSE
>         RETURN 'unexpected choice';
>     END;
>   END;
> ```
>
> Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
> `execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
> code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):
>
> Copy code
>
> ```
> CREATE PROCEDURE case_demo_2(v VARCHAR)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     BEGIN
>         CASE 
>             WHEN v = 'first choice' THEN
>                 RETURN 'one';
>             WHEN v = 'second choice' THEN
>                 RETURN 'two';
>             ELSE
>                 RETURN 'unexpected choice';
>        END CASE;
>     END;
> $$
> ;
> ```

When you call this stored procedure, the procedure produces the following output:

> Copy code
>
> ```
> CALL case_demo_2('none of the above');
> +-------------------+
> | CASE_DEMO_2       |
> |-------------------|
> | unexpected choice |
> +-------------------+
> ```
