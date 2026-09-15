Categories:
:   [System functions](/sql-reference/functions-system) (Query Information)

# SYSTEM$GET\_RESULTSET\_STATUS

Returns the status of a [RESULTSET](/developer-guide/snowflake-scripting/resultsets) in a Snowflake Scripting
stored procedure.

This function can be useful for getting the status an
[asynchronous child job](/developer-guide/snowflake-scripting/asynchronous-child-jobs)
that is running for a RESULTSET.

## Syntax

Copy code

```
SYSTEM$GET_RESULTSET_STATUS( <resultset_name> )
```

## Arguments

`resultset_name`
:   The name of the RESULTSET.

## Returns

This function returns the status of the RESULTSET in a value of type VARCHAR.
The following status values are possible:

| Status | Description |
| --- | --- |
| RUNNING | The query is still running. |
| SUCCESS | The query finished successfully. |
| ABORTING | The query is in the process of being aborted on the server side. |
| FAILED\_WITH\_ERROR | The query finished unsuccessfully due to an error in the query. |
| FAILED\_WITH\_INCIDENT | The query finished unsuccessfully due to an incident on the server side. |
| ABORTED | The query was aborted on the server side. |
| QUEUED | The query is queued for execution (that is, hasn’t yet started running), typically because it is waiting for resources. |
| DISCONNECTED | The session’s connection is broken. The query’s state will change to FAILED\_WITH\_ERROR soon. |
| RESUMING\_WAREHOUSE | The warehouse is starting up, and the query isn’t yet running. |
| QUEUED\_REPAIRING\_WAREHOUSE | The warehouse is being repaired, and the query is queued for execution. |
| RESTARTED | The query restarted. |
| BLOCKED | The query is waiting on a lock held by another statement. |

Expand

Show lessSee more

## Usage notes

This function can only be called in a [Snowflake Scripting block](/developer-guide/snowflake-scripting/blocks).

## Examples

The following example calls SYSTEM$GET\_RESULTSET\_STATUS twice to return the status of an asynchronous
child job that is running for a RESULTSET. The example calls the function while the asynchronous child job is
running and after it completes.

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  status2 VARCHAR DEFAULT 'invalid';
BEGIN
  LET res RESULTSET := ASYNC (SELECT SYSTEM$WAIT(3));
  LET status VARCHAR := SYSTEM$GET_RESULTSET_STATUS(res);

  AWAIT res;
  status2 := SYSTEM$GET_RESULTSET_STATUS(res);
  RETURN [status, status2];
END;
$$;
```

```
+------------------+
| GET_QUERY_STATUS |
+------------------+
| [                |
|   "RUNNING",     |
|   "SUCCESS"      |
| ]                |
+------------------+
```
