# CANCEL (Snowflake Scripting)

Cancels an [asynchronous child job](/developer-guide/snowflake-scripting/asynchronous-child-jobs)
that is running for a [RESULTSET](/developer-guide/snowflake-scripting/resultsets).

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [AWAIT](/sql-reference/snowflake-scripting/await)

## Syntax

Copy code

```
CANCEL <result_set_name> ;
```

Where:

> `result_set_name`
> :   The name of the RESULTSET.

## Usage notes

- An asynchronous child job is created for a RESULTSET when the ASYNC keyword is specified for the query
  that is associated with the RESULTSET.
- If the child job for the RESULTSET has already completed, the CANCEL statement has no effect.

## Examples

Copy code

```
CANCEL my_result_set;
```
