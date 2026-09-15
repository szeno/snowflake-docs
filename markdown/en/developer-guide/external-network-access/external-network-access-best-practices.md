# External network access best practices

This topic provides best practices for accessing external network locations from user-defined functions and procedures.

## Follow applicable best practices from external functions

Follow best practices described for [external functions](/sql-reference/external-functions), including the following:

- [Use a remote service’s batch API if available](/sql-reference/external-functions-best-practices#label-external-functions-best-practices-for-creating)
- [Do not assume that the remote service is passed each row exactly once](/sql-reference/external-functions-best-practices#label-external-function-retries)

Note that, unlike external functions, you are responsible in your handler code for performing retries, sending batch requests from
vectorized UDFs, and managing exceptions.

## Process one row at a time when using external access in a vectorized UDF or UDTF

When your vectorized UDF or UDTF handler code makes requests of an external network, you should process each row independently to
avoid non-deterministic results.

To minimize networking overhead, Snowflake typically batches rows to send to remote services. The number of batches
and the size of each batch can vary.

In addition, the order of batches can vary, and the order of rows within a batch can vary. Even if the query contains
an ORDER BY clause, the ORDER BY is usually applied after the request to the external network location.

Because batch size and row order are not guaranteed, writing a handler code that returns a value for a row
that depends on any other row in this batch or previous batches can produce non-deterministic results.

Snowflake strongly recommends that your code process each row independently.

The return value for each input row should depend on only that input row, not on other input rows. (Currently,
handlers performing external network access do not support [window functions](/sql-reference/functions-window), for example.)

Note also that because batch size is not guaranteed, counting batches is not meaningful.

## Reuse the TCP connection if possible

Snowflake limits the total number of connections that can be made from a UDF. When this limit is reached, you might see the following
error message:

Copy code

```
Cannot assign requested address
```

To avoid running into resource exhaustion issues, you should try to reuse connections as much as possible. You can achieve this by creating
the TCP client or session once during the UDF initialization, then using it in the UDF handler for the rest of the query. For example, for
code written in Python, you can reuse the `Session` object (available from the Python `requests` library) for multiple HTTP
calls.

For more information and an example, refer to [Using the external access integration in a function or procedure](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-using-udf).

## Expect and handle transient errors in code

When you have a long-running query that calls the remote service multiple times, it’s possible for one of the calls to fail with a
transient error. To avoid query failures, your code should execute retries and handle failures on the assumption that failures may
occur.
