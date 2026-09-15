# Working with conditional logic

Snowflake Scripting supports the following branching constructs for conditional logic:

- IF-THEN-ELSEIF-ELSE
- CASE

## IF statements

In Snowflake Scripting, you can execute a set of statements if a condition is met by using an
[IF](/sql-reference/snowflake-scripting/if) statement.

The syntax for the IF statement is:

Copy code

```
 IF (<condition>) THEN
   -- Statements to execute if the <condition> is true.

[ ELSEIF ( <condition_2> ) THEN
  -- Statements to execute if the <condition_2> is true.
]

[ ELSE
  -- Statements to execute if none of the conditions are true.
]

  END IF ;
```

In an IF statement:

- If you need to specify additional conditions, add an ELSEIF clause for each condition.
- To specify the statements to execute when none of the conditions evaluate to TRUE, add an ELSE clause.
- The ELSEIF and ELSE clauses are optional.

The following is a simple example of an IF statement:

Copy code

```
BEGIN
  LET count := 1;
  IF (count < 0) THEN
    RETURN 'negative value';
  ELSEIF (count = 0) THEN
    RETURN 'zero';
  ELSE
    RETURN 'positive value';
  END IF;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
BEGIN
  LET count := 1;
  IF (count < 0) THEN
    RETURN 'negative value';
  ELSEIF (count = 0) THEN
    RETURN 'zero';
  ELSE
    RETURN 'positive value';
  END IF;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| positive value  |
+-----------------+
```

For the full syntax and details about IF statements, see [IF (Snowflake Scripting)](/sql-reference/snowflake-scripting/if).

For more examples that use the IF statement, see:

- [Examples for common use cases of Snowflake Scripting](/developer-guide/snowflake-scripting/use-cases) - Execute SQL statements based on IF conditions in loops.
- [BREAK](/sql-reference/snowflake-scripting/break), [LOOP](/sql-reference/snowflake-scripting/loop),
  and [Working with loops](/developer-guide/snowflake-scripting/loops) - Execute BREAK statements to terminate a loop based on IF conditions.
- [EXCEPTION](/sql-reference/snowflake-scripting/exception) - Raise exceptions based on IF conditions.

## CASE statements

A CASE statement behaves similarly to an IF statement but provides a simpler way to specify multiple conditions.

Snowflake Scripting supports two forms of the CASE statement:

- [Simple CASE statements](#label-snowscript-branch-case-simple)
- [Searched CASE statements](#label-snowscript-branch-case-searched)

The next sections explain how to use these different forms.

Note

Snowflake supports other uses of the keyword CASE outside of Snowflake Scripting (e.g. the
conditional expression [CASE](/sql-reference/functions/case)).

### Simple CASE statements

In a simple CASE statement, you define different branches (WHEN clauses) for different possible values of a given expression.

The syntax for the simple CASE statement is:

Copy code

```
CASE ( <expression_to_match> )

    WHEN <value_1_of_expression> THEN
        <statement>;
        [ <statement>; ... ]

    [ WHEN <value_2_of_expression> THEN
        <statement>;
        [ <statement>; ... ]
    ]

    ... -- Additional WHEN clauses for other possible values;

    [ ELSE
        <statement>;
        [ <statement>; ... ]
    ]

END [ CASE ] ;
```

Snowflake executes the first branch for which `value_n_of_expression` matches the value of `expression_to_match`.

For example, suppose that you want to execute different statements, based on the value of the `expression_to_evaluate` variable.
For each possible value of this variable (e.g. `value a`, `value b`, etc.), you can define a WHEN clause that
specifies the statement(s) to execute:

Copy code

```
DECLARE
  expression_to_evaluate VARCHAR DEFAULT 'default value';
BEGIN
  expression_to_evaluate := 'value a';
  CASE (expression_to_evaluate)
    WHEN 'value a' THEN
      RETURN 'x';
    WHEN 'value b' THEN
      RETURN 'y';
    WHEN 'value c' THEN
      RETURN 'z';
    WHEN 'default value' THEN
      RETURN 'default';
    ELSE
      RETURN 'other';
  END;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  expression_to_evaluate VARCHAR DEFAULT 'default value';
BEGIN
  expression_to_evaluate := 'value a';
  CASE (expression_to_evaluate)
    WHEN 'value a' THEN
      RETURN 'x';
    WHEN 'value b' THEN
      RETURN 'y';
    WHEN 'value c' THEN
      RETURN 'z';
    WHEN 'default value' THEN
      RETURN 'default';
    ELSE
      RETURN 'other';
  END;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| x               |
+-----------------+
```

For the full syntax and details about CASE statements, see [CASE (Snowflake Scripting)](/sql-reference/snowflake-scripting/case).

### Searched CASE statements

In the searched CASE statement, you specify different conditions for each branch (WHEN clause). Snowflake
executes the first branch for which the expression evaluates to TRUE.

The syntax for the searched CASE statement is:

Copy code

```
CASE

  WHEN <condition_1> THEN
    <statement>;
    [ <statement>; ... ]

  [ WHEN <condition_2> THEN
    <statement>;
    [ <statement>; ... ]
  ]

  ... -- Additional WHEN clauses for other possible conditions;

  [ ELSE
    <statement>;
    [ <statement>; ... ]
  ]

END [ CASE ] ;
```

For example, when you execute the following CASE statement, the returned value is `a is x` because that branch is the first
branch in which the expression evaluates to TRUE:

Copy code

```
DECLARE
  a VARCHAR DEFAULT 'x';
  b VARCHAR DEFAULT 'y';
  c VARCHAR DEFAULT 'z';
BEGIN
  CASE
    WHEN a = 'x' THEN
      RETURN 'a is x';
    WHEN b = 'y' THEN
      RETURN 'b is y';
    WHEN c = 'z' THEN
      RETURN 'c is z';
    ELSE
      RETURN 'a is not x, b is not y, and c is not z';
  END;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  a VARCHAR DEFAULT 'x';
  b VARCHAR DEFAULT 'y';
  c VARCHAR DEFAULT 'z';
BEGIN
  CASE
    WHEN a = 'x' THEN
      RETURN 'a is x';
    WHEN b = 'y' THEN
      RETURN 'b is y';
    WHEN c = 'z' THEN
      RETURN 'c is z';
    ELSE
      RETURN 'a is not x, b is not y, and c is not z';
  END;
END;
$$
;
```

```
+-----------------+
| anonymous block |
|-----------------|
| a is x          |
+-----------------+
```

For the full syntax and details about CASE statements, see [CASE (Snowflake Scripting)](/sql-reference/snowflake-scripting/case).
