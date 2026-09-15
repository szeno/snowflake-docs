# FOR (Snowflake Scripting)

A `FOR` loop repeats a sequence of steps a specific number of times. The number of times might be specified by the
user, or might be specified by the number of rows in a [cursor](/developer-guide/snowflake-scripting/cursors). The syntax
of these two types of `FOR` loops is slightly different.

For more information on loops, see [Working with loops](/developer-guide/snowflake-scripting/loops).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [BREAK](/sql-reference/snowflake-scripting/break), [CONTINUE](/sql-reference/snowflake-scripting/continue)

## Syntax

To loop over all rows in a [cursor](/developer-guide/snowflake-scripting/cursors), use:

> Copy code
>
> ```
> FOR <row_variable> IN <cursor_name> DO
>     <statement>;
>     [ <statement>; ... ]
> END FOR [ <label> ] ;
> ```

To loop a specified number of times, use:

> Copy code
>
> ```
> FOR <counter_variable> IN [ REVERSE ] <start> TO <end> { DO | LOOP }
>     <statement>;
>     [ <statement>; ... ]
> END { FOR | LOOP } [ <label> ] ;
> ```

Where:

> `row_variable`
> :   Specify a variable name that follows the rules for [Object identifiers](/sql-reference/identifiers).
>
>     Do not add a declaration for this variable in the DECLARE or BEGIN … END sections.
>     The name should not already be defined in the scope of the local block.
>
>     The name is valid inside the `FOR` loop, but not outside the `FOR` loop.
>
>     The `row_variable` holds one row from the cursor. Fields within that row are accessed using dot notation. For example:
>
>     > `my_row_variable.my_column_name`
>
>     A more complete example is included in the examples below.
>
> `counter_variable`
> :   Specify a variable name that follows the rules for [Object identifiers](/sql-reference/identifiers).
>
>     The name of the `counter_variable` is valid only inside the `FOR` loop.
>     If a variable with the same name is declared outside the loop, the outer variable and the loop variable are separate. Inside the
>     loop, references to that name are resolved to the loop variable.
>
>     The code inside the `FOR` loop is allowed to read the value of the counter variable, but should not change it. For
>     example, do not increment the counter variable manually to change the step size.
>
> `start`
> :   This is the initial value of `counter_variable`.
>
>     The starting value should be an INTEGER or an expression that evaluates to an INTEGER.
>
> `end`
> :   This is the final value of `counter_variable`, after the `counter_variable` has been incremented as you loop.
>
>     The ending value should be an INTEGER or an expression that evaluates to an INTEGER.
>
>     The `end` value should be greater than or equal to the `start` value. If `end` is less than
>     `start`, the loop executes 0 times (even if the `REVERSE` keyword is used).
>
> `statement`
> :   A statement can be any of the following:
>
>     - A single SQL statement (including CALL).
>     - A control-flow statement (for example, a [looping](/developer-guide/snowflake-scripting/loops) or
>       [branching](/developer-guide/snowflake-scripting/branch) statement).
>     - A nested [block](/developer-guide/snowflake-scripting/blocks).
>
> `cursor_name`
> :   The name of the cursor to iterate through.
>
> `label`
> :   An optional label. Such a label can be a jump target for a [BREAK (Snowflake Scripting)](/sql-reference/snowflake-scripting/break) or
>     [CONTINUE (Snowflake Scripting)](/sql-reference/snowflake-scripting/continue) statement. A label must follow the naming rules for
>     [Object identifiers](/sql-reference/identifiers).

## Usage notes

- The loop iterates up to and including the `end` point.

  For example, `FOR i IN 1 TO 10` loops 10 times, and during the final iteration the value of `i` is 10.

  If you use the `REVERSE` keyword, then the loop iterates backwards down to and including the `start` value.
- A loop can contain multiple statements. You can use, but are not required to use, a [BEGIN … END (Snowflake Scripting)](/sql-reference/snowflake-scripting/begin)
  [block](/developer-guide/snowflake-scripting/blocks) to contain those statements.
- The optional keyword `REVERSE` causes Snowflake to start with the `end` value and decrement down to the `start` value.
- Although you can change the value of the `counter_variable` inside the loop, Snowflake recommends that you avoid doing this.
  Changing the value makes the code more difficult to understand.
- If you use the keyword `DO`, then use `END FOR` at the end of the `FOR` loop. If you use the keyword `LOOP`, then use
  `END LOOP` at the end of the `FOR` loop.

## Examples

The following sections contain examples of different kinds of FOR loops:

- [Cursor-based FOR loops](#cursor-based-for-loops)
- [Counter-based FOR loops](#counter-based-for-loops)

Note

For more examples, see [FOR loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for).

### Cursor-based FOR loops

This example shows how to use a [cursor](/developer-guide/snowflake-scripting/cursors) to sum the values in the `price`
column of all the rows returned by a query. This stored procedure behaves somewhat like an aggregate function.

> Copy code
>
> ```
> CREATE or replace TABLE invoices (price NUMBER(12, 2));
> INSERT INTO invoices (price) VALUES
>     (11.11),
>     (22.22);
> ```
>
> Copy code
>
> ```
> CREATE OR REPLACE PROCEDURE for_loop_over_cursor()
> RETURNS FLOAT
> LANGUAGE SQL
> AS
> $$
> DECLARE
>     total_price FLOAT;
>     c1 CURSOR FOR SELECT price FROM invoices;
> BEGIN
>     total_price := 0.0;
>     OPEN c1;
>     FOR rec IN c1 DO
>         total_price := total_price + rec.price;
>     END FOR;
>     CLOSE c1;
>     RETURN total_price;
> END;
> $$
> ;
> ```
>
> Here is the output of the stored procedure:
>
> Copy code
>
> ```
> CALL for_loop_over_cursor();
> +----------------------+
> | FOR_LOOP_OVER_CURSOR |
> |----------------------|
> |                33.33 |
> +----------------------+
> ```

### Counter-based FOR loops

This example shows how to use a `FOR` loop to iterate a specified number of times:

> Copy code
>
> ```
> CREATE PROCEDURE simple_for(iteration_limit INTEGER)
> RETURNS INTEGER
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         counter INTEGER DEFAULT 0;
>     BEGIN
>         FOR i IN 1 TO iteration_limit DO
>             counter := counter + 1;
>         END FOR;
>         RETURN counter;
>     END;
> $$;
> ```
>
> Here is the output of the stored procedure:
>
> Copy code
>
> ```
> CALL simple_for(3);
> +------------+
> | SIMPLE_FOR |
> |------------|
> |          3 |
> +------------+
> ```

The following example shows how to use the `REVERSE` keyword to count backwards.

> Copy code
>
> ```
> CREATE PROCEDURE reverse_loop(iteration_limit INTEGER)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         values_of_i VARCHAR DEFAULT '';
>     BEGIN
>         FOR i IN REVERSE 1 TO iteration_limit DO
>             values_of_i := values_of_i || ' ' || i::varchar;
>         END FOR;
>         RETURN values_of_i;
>     END;
> $$;
> ```
>
> Here is the output of the stored procedure:
>
> Copy code
>
> ```
> CALL reverse_loop(3);
> +--------------+
> | REVERSE_LOOP |
> |--------------|
> |  3 2 1       |
> +--------------+
> ```

The following example shows the behavior when the loop counter variable has the same name (`i`) as a variable that was already
declared. Within the `FOR` loop, references to `i` resolve to the loop counter variable (not to the variable declared outside of
the loop).

> Copy code
>
> ```
> CREATE PROCEDURE p(iteration_limit INTEGER)
> RETURNS VARCHAR
> LANGUAGE SQL
> AS
> $$
>     DECLARE
>         counter INTEGER DEFAULT 0;
>         i INTEGER DEFAULT -999;
>         return_value VARCHAR DEFAULT '';
>     BEGIN
>         FOR i IN 1 TO iteration_limit DO
>             counter := counter + 1;
>         END FOR;
>         return_value := 'counter: ' || counter::varchar || '\n';
>         return_value := return_value || 'i: ' || i::VARCHAR;
>         RETURN return_value;
>     END;
> $$;
> ```
>
> Here is the output of the stored procedure:
>
> Copy code
>
> ```
> CALL p(3);
> +------------+
> | P          |
> |------------|
> | counter: 3 |
> | i: -999    |
> +------------+
> ```
