# AWAIT (Snowflake Scripting)

Waits for all [asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs)
that are running to finish or for a specific asynchronous child job that is running for a
[RESULTSET](/developer-guide/snowflake-scripting/resultsets) to finish, then returns
when the all jobs have finished or the specific job has finished, respectively.

AWAIT is a blocking call. You can use an AWAIT statement to block other code from running until
the AWAIT call completes.

Note

This [Snowflake Scripting](/developer-guide/snowflake-scripting/index) construct is valid only within a
[Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

See also:
:   [CANCEL](/sql-reference/snowflake-scripting/cancel)

## Syntax

Copy code

```
AWAIT { ALL | <result_set_name> };
```

Where:

> `ALL`
> :   The stored procedure waits for all asynchronous child jobs that were started before the AWAIT call.
>
> `result_set_name`
> :   The stored procedure waits for the asynchronous child job that is running for the specified RESULTSET
>     to finish.

## Usage notes

- An asynchronous child job is created when the ASYNC keyword is specified for a query.
  For more information, see [Working with asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs).
- When the ASYNC keyword is specified for a query, the stored procedure can’t access the query results
  until an AWAIT statement returns the results.
- When you run an asynchronous child job, “fire and forget” isn’t supported. Therefore, if the stored
  procedure runs a child job that is still running when the stored procedure completes, the child job
  is canceled automatically.
- Snowflake Scripting supports built-in variables that you can use in the code for stored procedures.

  These variables behave in the following ways for asynchronous child jobs:

  - The [SQLID](/developer-guide/snowflake-scripting/query-id) variable is available for the query
    specified for an asynchronous child job immediately after the asynchronous child job is created.
  - The following [built-in variables for exception handling](/developer-guide/snowflake-scripting/exceptions#label-snowscript-exception-handling)
    are available after the AWAIT or AWAIT ALL statement associated with the asynchronous child job that
    caused the error runs:

    - SQLCODE
    - SQLERRM
    - SQLSTATE

    When an AWAIT ALL statement is associated with multiple asynchronous child jobs, these built-in variables
    capture information about the first failing asynchronous child job.
  - The following built-in variables related to
    [the number of rows affected by DML commands](/developer-guide/snowflake-scripting/dml-status)
    are available after the AWAIT statement associated with the asynchronous child job for a
    RESULTSET runs:

    - SQLROWCOUNT
    - SQLFOUND
    - SQLNOTFOUND

    These variables aren’t available when an AWAIT ALL statement runs.
- If an asynchronous child job fails, the AWAIT or AWAIT ALL statement associated with the asynchronous job
  fails with an error, and execution of the stored procedure stops. For example, the following stored procedure
  fails and returns an error when execution reaches the AWAIT statement:

  Copy code

  ```
  BEGIN
    LET res RESULTSET := ASYNC (SELECT * FROM invalid_table);
    AWAIT res;
  END;
  ```

  ```
  002003 (42S02): Uncaught exception of type 'STATEMENT_ERROR' on line 2 at position 4 : SQL compilation error:
  Table 'INVALID_TABLE' does not exist or not authorized.
  ```

## Examples

Wait for all asynchronous child jobs to complete:

Copy code

```
AWAIT ALL;
```

Wait for an asynchronous child job that is running for a RESULTSET to complete:

Copy code

```
AWAIT my_result_set;
```

For more examples, see [Examples of using asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs#label-snowscript-asynchronous-child-jobs-examples).
