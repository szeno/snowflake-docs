# Getting details about an error

If the statement does not execute successfully, Snowflake returns one of the following response codes, as shown in the flow chart
below:

![Flow chart for handling errors during statement execution](/static/images/sql-api-flow-chart-error.png)

As shown in this flow chart:

- If the statement execution takes longer than the timeout period specified by the `timeout` field in the request (or the
  timeout specified by the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) parameter, if the `timeout` field is not set),
  Snowflake returns the HTTP response code 408 with a [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object.

  Use this object to get [details about the cancellation of the statement execution](/developer-guide/sql-api/handling-responses#label-sql-api-getting-results).
- If an error occurred when executing the statement, Snowflake returns the HTTP response code 422 with a
  [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object.

  You can get details about the error from this object.
