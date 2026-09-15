# NULL (Snowflake Scripting)

NULL can be used as a “no-op” (no operation) statement.

Note

Using NULL as a statement is uncommon. NULL is usually used as a *value*, rather than as a *statement*.

As a value, NULL means “no value.” For more information, see
[the Wikipedia article on SQL NULL](https://en.wikipedia.org/wiki/Null_(SQL)).

When working with [semi-structured data types](/sql-reference/data-types-semistructured),
such as [JSON](/user-guide/tutorials/json-basics-tutorial), you might need to
[distinguish between NULL as an SQL value and NULL as a JSON value (also called “VARIANT NULL”)](/user-guide/semistructured-considerations#label-variant-null).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

## Syntax

Copy code

```
NULL;
```

## Usage notes

- The NULL statement can be executed only inside [Snowflake Scripting](/developer-guide/snowflake-scripting/index) code.
- A NULL statement in an exception handler ensures that the code continues executing rather than aborting if there is no
  higher-level handler.
- A NULL statement in a branch does nothing; however, it communicates to the reader that the author of the code explicitly
  considered the condition for which the branch would execute. In other words, the NULL shows that the branch condition wasn’t
  overlooked or accidentally omitted.
- Before using the NULL statement, consider alternatives.

  For example, suppose you are writing a stored procedure with an exception handler. In most stored procedures, if each
  non-exception code path should return a value, then each code path involving an exception handler should also return a value.
  In that case, avoid executing a NULL statement. Instead, consider explicitly returning NULL, an empty result set, or an
  error indicator.

  You can also use a CONTINUE handler to run statements in the exception block and continues with the statement
  immediately following the one that caused the error. For more information, see [Handling an exception in Snowflake Scripting](/developer-guide/snowflake-scripting/exceptions#label-snowscript-exception-handling).

## Examples

The following code uses a NULL statement in an exception handler to ensure that the exception is caught (rather than passed
up to the caller), but no specific action is taken:

Copy code

```
CREATE PROCEDURE null_as_statement()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  SELECT 1 / 0;
  RETURN 'If you see this, the exception was not thrown/caught properly.';
EXCEPTION
  WHEN OTHER THEN
      NULL;
END;
$$
;
```

Call the stored procedure:

Copy code

```
CALL null_as_statement();
```

```
+-------------------+
| NULL_AS_STATEMENT |
|-------------------|
| NULL              |
+-------------------+
```

Note

The NULL value returned by the CALL statement isn’t directly due to the NULL statement in the exception. Instead, the return
value is NULL because the stored procedure didn’t execute an explicit RETURN statement.

Snowflake recommends that stored procedures explicitly return a value, including in each branch of the exception handler.
