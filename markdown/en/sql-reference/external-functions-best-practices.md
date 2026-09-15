# External functions best practices

This topic documents best practices that will improve efficiency and prevent unexpected results that could occur
if a remote service is not designed to be compatible with Snowflake.

You can find additional best practices in the following documents:

- [Optimize the performance and reliability of Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices)

  (Although this is a Microsoft Azure document, much of the advice in it applies to remote services on
  any cloud platform.)

## Use a remote service’s batch API if available

Some remote services offer both batch mode and single-row mode. If the queries that use an external function are
expected to send multiple rows, then Snowflake recommends using the batch mode of the remote service to improve
performance.

This rule does not necessarily apply if:

- Each row is very large (e.g. hundreds of kilobytes or more).
- The remote service processes rows differently if they are received in batches than if they are received
  individually. (For details, see [Process one row at a time](#label-external-functions-process-one-row-at-a-time).)

## Process one row at a time

To minimize networking overhead, Snowflake typically batches rows to send to remote services. The number of batches
and the size of each batch can vary.

In addition, the order of batches can vary, and the order of rows within a batch can vary. Even if the query contains
an ORDER BY clause, the ORDER BY is usually applied after the external function(s) have been called.

Because batch size and row order are not guaranteed, writing a function that returns a value for a row
that depends upon any other row in this batch or previous batches can produce non-deterministic results.

Snowflake strongly recommends that the remote service process each row independently.
The return value for each input row should depend on only that input row, not on other input rows. (Currently,
external functions do not support [window functions](/sql-reference/functions-window), for example.)

Note also that because batch size is not guaranteed, counting batches is not meaningful.

See also [Ensure your external function is stateless](#label-external-functions-should-be-stateless).

## Do not assume that the remote service is passed each row exactly once

If Snowflake calls a remote service, and the remote service receives the request and returns a result, but Snowflake
does not receive the result due to a temporary network problem, Snowflake might repeat the request. If Snowflake
retries, the remote service might see the same row twice (or more).

This can cause unexpected effects. For example, because the remote service might get called more than once for the
same value, a remote service that assigns unique IDs might have gaps in the sequence of those IDs. In some cases,
such effects can be reduced by tracking the batch ID in the `sf-external-function-query-batch-id` field of the
request header to determine whether a particular batch of rows has been processed previously. When Snowflake retries a
request for a specific batch, Snowflake uses the same batch ID as it used earlier for the same batch.

Snowflake retries when it receives the following errors:

- All transient network transport errors.
- All requests that fail with 429 status code.
- All requests that fail with 5XX status code.

Requests are retried until a total retry timeout is reached. The total retry timeout is not user-configurable.
Snowflake might adjust this limit in the future.

When the total retry timeout is reached without a successful retry, the query fails.

If your external function call times out when the remote service is working, and all the elements between Snowflake
and the remote service seem to be working, you can try a smaller batch size to see if that reduces the timeout errors.

To learn how to set the maximum batch size, see [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

## Ensure your external function is stateless

In general, an external function (including the remote service) should avoid storing state information, both:

- Internal state (state that the remote service stores internally).
- External state (state stored outside the remote service, for example state information sent to and/or read from
  another remote service that itself retains state).

If the remote service changes state information and then uses that information to affect future outputs, the function
might return different values than expected.

For example, consider a simple remote service that contains an internal counter and returns the number of rows
received since the remote service first started. If there is a temporary network problem, and Snowflake repeats
a request with the same data, the remote service will count the re-sent rows twice (or more).

For an example involving external state, see [Avoid side-effects](#label-external-functions-should-avoid-side-effects).

In the rare cases where a function is not stateless, the documentation for callers should say clearly that the
function is not stateless, and the function should be marked volatile.

If a remote service handles requests
[asynchronously](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous), then the remote service
author must write the remote service to store and manage some state temporarily. For example, the remote service must
store the HTTP POST request’s batch ID so that if an HTTP GET is received with the same batch ID, the remote service
can return HTTP code 202 when the specified batch is still being processed.

Note that a query can be aborted for various reasons, which means that there is no guarantee that a final GET will
arrive after the remote service has finished generating a result. Remote services that store state for asynchronous
requests should eventually time out and clean up that internal state. The optimal timeout might change in the future,
but currently Snowflake recommends preserving information about asynchronous requests for at least 10 minutes
and preferably 12 hours before deleting it.

## Avoid side-effects

An external function (including the remote service) should avoid side effects, such as changing external
state (information stored outside the remote service).

For example, if the remote service reports out-of-range values to a government agency, that is a side effect.

Side-effects can be useful, but the side-effects of calling an external function are not always predictable.
For example, suppose that you call a remote service that analyzes an anonymized health record and returns a diagnosis.
Suppose also that if the diagnosis is that the patient has a contagious disease, then the diagnosis is reported to an
agency that keeps count of the number of cases of that disease. This is a useful side effect. However, it is
vulnerable to problems such as:

- If an external function call is inside a transaction that is rolled back, the side effects are not rolled back.
- If the remote service is called more than once with the same row (e.g. due to temporary network failures and
  retries), the side-effect could occur more than once. For example, an infected patient might be counted twice
  in the statistics.

There are also situations in which rows could be undercounted rather than overcounted.

In the very rare cases where a function has side effects, the documentation for callers should say clearly what the
side effects are, and the function should be marked volatile.

## Categorize your function as volatile or immutable

Functions can be categorized as volatile or immutable. (The [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function)
statement allows the user to specify whether the function is volatile or immutable.)

For an external function to be considered immutable, it should meet the following criteria:

- If given the same input value, the function returns the same output value. (For example, the SQRT function returns
  the same output when given the same input, but the CURRENT\_TIMESTAMP function does not necessarily return the same
  output when given the same input.)
- The function has no side effects. (For details, see [Avoid side-effects](#label-external-functions-should-avoid-side-effects).)

If a function meets these two criteria, then Snowflake can use certain types of optimizations to reduce the number
of rows or batches sent to the remote service. (These optimizations might evolve over time, and are not described in
detail here.)

Snowflake cannot detect or enforce immutability, or factors that affect immutability (for example,
side effects). The writer of a remote service should document whether the remote service meets the criteria
to be labeled immutable. If a remote service has side effects, then the external function that calls that remote
service should be marked volatile, even if the function call returns the same output value for the same input value.
If you are not certain that a remote service is immutable, then any external function that calls that remote service
should be labeled volatile.

## Account for timeout errors

An external function call involves Snowflake, a remote service, a proxy service, and potentially other elements
in the chain. None of these elements know how long a particular function call should take, so none know exactly
when to stop waiting and return a timeout error. Each step might have its own independent timeout. For more
information about timeouts and retries, see [Account for timeout errors](#label-external-function-timeouts) and [retries](#label-external-function-retries).

## Minimize latency

To minimize latency and improve performance of external function calls, Snowflake recommends doing the following
when practical:

- Put the API Gateway in the same cloud platform and region as Snowflake instances that call it most frequently (or
  with the largest amount of data).
- If you wrote the remote service (rather than using an existing service), deploy that remote service in
  the same cloud platform and region as it is called from.
- Send as little data as possible. For example, if the remote service will examine inputs values and
  operate on only a subset of them, then it is usually more efficient to filter in SQL and send only the
  relevant rows to the remote service, rather than send all rows to the remote service and let it filter.

  As another example, if you are processing a column that contains large semi-structured
  data values, and the remote service will operate on only a small piece of each of those data values, it is
  usually more efficient to extract the relevant piece using Snowflake SQL and send only that piece, rather
  than send the entire column and have the remote service do the extraction of the small piece before processing.

## Develop and test external functions one step at a time

Snowflake recommends that you test without Snowflake before testing with Snowflake.

During the early stages of developing an external function, use the cloud platform proxy service console (e.g. the
Amazon API Gateway console) and remote service development console (e.g. the AWS Lambda console) to help develop
and test the proxy service and remote service.

For example, if you have developed a Lambda function, you might want to test it extensively through the Lambda console
before testing it by calling it from Snowflake.

Testing through the proxy service console and remote service console usually has the following advantages:

- It can make diagnosing the problem easier because there are fewer places to look for the cause of the problem.
- Viewing the data payload might provide useful debugging information. Snowflake does not show any portion of
  the data payload in error messages; although this enhances security, it can slow debugging.
- Snowflake auto-retries HTTP 5xx errors, which can make debugging slower or more difficult in some situations.
- Testing through Snowflake consumes Snowflake credits in addition to cloud platform credits.

Of course, after you’ve tested the remote service and the proxy service as much as you can without Snowflake, you
should test them with Snowflake. The advantages of testing with Snowflake include:

- You’re testing all the steps involved in the external function.
- Using a Snowflake table as the data source makes it easy to test with large volumes of data to get a realistic
  estimate of the performance of the external function.

Consider the following test cases:

- NULL values.
- “Empty” values (for example, empty strings, empty semi-structured data types).
- Very long VARCHAR and BINARY values, if appropriate.

## Make your remote service asynchronous

If you are writing a remote service, and if your remote service might not return results within the expected timeout,
then consider making your remote service
[asynchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous).
For details, see [Asynchronous vs. Synchronous remote services](/sql-reference/external-functions-implementation#label-external-functions-synchronous-vs-asynchronous-remote-services).

## Ensure that arguments to the external function correspond to arguments parsed by the remote service

When passing arguments to or from an external function, ensure that the data types are appropriate. If the value
sent can’t fit into the data type being received, the value might be truncated or corrupted, or the remote service
call might fail.

For example, because some Snowflake SQL numeric data types can store larger values than commonly-used JavaScript
data types, de-serializing large numbers from JSON is particularly sensitive in JavaScript.

If you change the number, data types, or order of the arguments to the remote
service, remember to make the corresponding changes to the external function. Currently, the ALTER FUNCTION
command does not have an option to change parameters, so you must drop and re-create the external function to change
the arguments.
