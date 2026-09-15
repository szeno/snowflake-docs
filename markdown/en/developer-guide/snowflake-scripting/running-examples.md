# Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector

This topic explains how to run the Snowflake Scripting examples in [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), and the [Python Connector](/developer-guide/python-connector/python-connector).

Note

If you are using other clients and interfaces, such as [Snowflake CLI](/developer-guide/snowflake-cli/index) or the
[JDBC driver](/developer-guide/jdbc/jdbc), you can skip this topic and refer to
[Snowflake Scripting blocks](/developer-guide/snowflake-scripting/blocks).

## Introduction

Currently, the following interfaces do not correctly parse Snowflake Scripting blocks:

- [Snowflake CLI](/developer-guide/snowflake-cli/index)
- [SnowSQL](/user-guide/snowsql)
- The `execute_stream()` and `execute_string()` methods in
  [Python Connector](/developer-guide/python-connector/python-connector) code

  Note

  The other Python Connector methods parse Snowflake Scripting blocks correctly.

Entering and running a Snowflake Scripting block can result in the following error:

Copy code

```
SQL compilation error: syntax error line 2 at position 25 unexpected '<EOF>'
```

To work around this, use delimiters around the start and end of a Snowflake Scripting block if you are using
these interfaces.

The following sections explain how to do this:

- [Using string constant delimiters around a block in a stored procedure](#label-snowscript-stored-procedure-delimiter-workaround)
- [Passing a block as a string literal to EXECUTE IMMEDIATE](#label-snowscript-anonymous-block-delimiter-workaround)

## Using string constant delimiters around a block in a stored procedure

If you are creating a stored procedure, enclose the Snowflake Scripting block in
[single quotes or double dollar signs](/sql-reference/data-types-text#label-quoted-string-constants). For example:

Copy code

```
CREATE OR REPLACE PROCEDURE myprocedure()
  RETURNS VARCHAR
  LANGUAGE SQL
  AS
  $$
    -- Snowflake Scripting code
    DECLARE
      radius_of_circle FLOAT;
      area_of_circle FLOAT;
    BEGIN
      radius_of_circle := 3;
      area_of_circle := pi() * radius_of_circle * radius_of_circle;
      RETURN area_of_circle;
    END;
  $$
  ;
```

Note

When specifying the scripting block directly on the Snowflake CLI command line, the `$$` delimiters might not work for some shells because they interpret that delimiter as something else. For example, the bash and zsh shells interpret it as the process ID (PID). To address this limitation, you can use the following alternatives:

- If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
- You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f filename` command.

## Passing a block as a string literal to EXECUTE IMMEDIATE

If you are writing an [anonymous block](/developer-guide/snowflake-scripting/blocks#label-snowscript-block-anonymous), pass the block as a string literal to the
[EXECUTE IMMEDIATE](/sql-reference/sql/execute-immediate) command. To delimit the string literal, use
[single quotes or double dollar signs](/sql-reference/data-types-text#label-quoted-string-constants).

For example:

Copy code

```
EXECUTE IMMEDIATE $$
-- Snowflake Scripting code
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := pi() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
$$
;
```

As an alternative, you can define a [session variable](/sql-reference/session-variables) that is a string literal
containing the block, and you can pass that session variable to the EXECUTE IMMEDIATE command. For example:

Copy code

```
SET stmt =
$$
DECLARE
    radius_of_circle FLOAT;
    area_of_circle FLOAT;
BEGIN
    radius_of_circle := 3;
    area_of_circle := pi() * radius_of_circle * radius_of_circle;
    RETURN area_of_circle;
END;
$$
;

EXECUTE IMMEDIATE $stmt;
```

Note

When specifying the scripting block directly on the Snowflake CLI command line, the `$$` delimiters might not work for some shells because they interpret that delimiter as something else. For example, the bash and zsh shells interpret it as the process ID (PID). To address this limitation, you can use the following alternatives:

- If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
- You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f filename` command.
