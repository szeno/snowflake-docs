# Snowflake SQL API reference

This topic documents the operations, requests, and responses for the SQL API.

## Operations

### `POST /api/v2/statements`

To submit one or more SQL statements for execution, send a POST request to `/api/v2/statements`. You can specify that the
statement should be executed asynchronously.

#### Request syntax

Copy code

```
POST /api/v2/statements
(request body)
```

#### Query parameters

| Parameter | Description |
| --- | --- |
| `requestId` | (Optional) Unique ID (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)) of the API request. See [Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id). |
| `async` | (Optional) Set to `true` to execute the statement asynchronously and return the statement handle.  If the parameter is not specified or is set to false, a statement is executed and the results are returned if the execution is completed in 45 seconds. If the statement execution takes longer to complete, the statement handle is returned. |
| `nullable` | (Optional) Set to `false` to return a SQL NULL value as the string `"null"`, rather than as the value `null`.  Note  You cannot specify this parameter in a GET request.  By default, SQL NULL values are returned as the value `null`:  Copy code  ``` "data" : [ [ null ], ... ] ```  Setting this query parameter to false (e.g. `/api/v2/statements?nullable=false` returns a SQL NULL value as the string `"null"`:  Copy code  ``` "data" : [ [ "null" ], ... ] ``` |

Expand

Show lessSee more

#### Request headers

The request must include the headers listed in [Request headers for all operations](#label-sql-api-reference-request-headers).

#### Request body

(Required) The request body must contain the object specified in [Types of objects in the request body](#label-sql-api-reference-post-statements-request-body).

#### Response

This operation can return the response codes listed below.

| Code | Description |
| --- | --- |
| 200 | The statement was executed successfully.  For this response code, the response can have the following headers:   - [Link](#label-sql-api-reference-response-headers)   **If a single SQL statement was submitted in the request,** the body of the response contains a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object containing the requested data.  Note  If the `code` field in the response is set to `391908`, the result set is too large,   and the response does not include the entire result set.  The following is an example of a response for a single SQL statement in which the results are returned in a single partition. `{handle}` is the statement handle and `{id1}`, `{id2}`, and `{id3}` are uniquely generated request IDs:  Copy code  ``` HTTP/1.1 200 OK Date: Tue, 04 May 2021 18:06:24 GMT Content-Type: application/json Link:   </api/v2/statements/{handle}?requestId={id1}&partition=0>; rel="first",   </api/v2/statements/{handle}?requestId={id2}&partition=0>; rel="last" {   "resultSetMetaData" : {     "numRows" : 4,     "format" : "jsonv2",     "rowType" : [ {       "name" : "COLUMN1",       "database" : "",       "schema" : "",       "table" : "",       "scale" : null,       "precision" : null,       "length" : 4,       "type" : "text",       "nullable" : false,       "byteLength" : 16,       "collation" : null     }, {       "name" : "COLUMN2",       "database" : "",       "schema" : "",       "table" : "\"VALUES\"",       "scale" : 0,       "precision" : 1,       "length" : null,       "type" : "fixed",       "nullable" : false,       "byteLength" : null,       "collation" : null     } ],     "partitionInfo": [{       "rowCount": 4,       "uncompressedSize": 1438,     }]   },   "data" : [ [ "test", "2" ], [ "test", "3" ], [ "test", "4" ], [ "test", "5" ] ],   "code" : "090001",   "statementStatusUrl" : "/api/v2/statements/{handle}?requestId={id3}&partition=0",   "sqlState" : "00000",   "statementHandle" : "{handle}",   "message" : "Statement executed successfully.",   "createdOn" : 1620151584132 } ```  The following is an example of a response for a single SQL statement in which the results need to be returned in multiple partitions, where `{handle}` is the statement handle and `{id1}`, `{id2}`, `{id3}`, and `{id4}` are uniquely generated request IDs:  Copy code  ``` HTTP/1.1 200 OK Date: Tue, 04 May 2021 18:08:15 GMT Content-Type: application/json Link:   </api/v2/statements/{handle}?requestId={id1}&partition=0>; rel="first",   </api/v2/statements/{handle}?requestId={id2}&partition=1>; rel="next",   </api/v2/statements/{handle}?requestId={id3}&partition=1>; rel="last" {   "resultSetMetaData" : {     "numRows" : 56090,     "format" : "jsonv2",     "rowType" : [ {       "name" : "SEQ8()",       "database" : "",       "schema" : "",       "table" : "",       "scale" : 0,       "precision" : 19,       "length" : null,       "type" : "fixed",       "nullable" : false,       "byteLength" : null,       "collation" : null     }, {       "name" : "RANDSTR(1000, RANDOM())",       "database" : "",       "schema" : "",       "table" : "",       "scale" : null,       "precision" : null,       "length" : 16777216,       "type" : "text",       "nullable" : false,       "byteLength" : 16777216,       "collation" : null     } ],     "partitionInfo": [{       "rowCount": 12344,       "uncompressedSize": 14384873,     },{       "rowCount": 43746,       "uncompressedSize": 43748274,       "compressedSize": 746323     }]   },   "data" : [ [ "0", "QqKow2xzdJ....." ],.... [ "98", "ZugTcURrcy...." ] ],   "code" : "090001",   "statementStatusUrl" : "/api/v2/statements/{handle}?requestId={id4}",   "sqlState" : "00000",   "statementHandle" : "{handle}",   "message" : "Statement executed successfully.",   "createdOn" : 1620151693299 } ```  **If multiple SQL statements were submitted in the request,** the body of the response contains a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object with details about the status of the execution of the multiple statements.  In this case, the response does not contain the requested data. Instead, the `data` field just contains the message “Multiple statements executed successfully”.  The response contains the `statementHandles` field, which is an array of statement handles that you can use to [retrieve the results of the individual statements](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements).  The following is an example of a response for a request that specifies multiple SQL statements, where:   - `{handle}` is the statement handle for the set of statements. - `{handle1}`, `{handle2}`, and `{handle3}` are the handles for the individual SQL statements in the request. - `{id1}`, `{id2}`, and `{id3}` are uniquely generated request IDs:   Copy code  ``` HTTP/1.1 200 OK Date: Mon, 31 May 2021 22:50:31 GMT Content-Type: application/json Link:   </api/v2/statements/{handle}?requestId={id1}&partition=0>; rel="first",   </api/v2/statements/{handle}?requestId={id2}&partition=1>; rel="last"  {   "resultSetMetaData" : {   "numRows" : 56090,   "format" : "jsonv2",   "rowType" : [ {       "name" : "multiple statement execution",       "database" : "",       "schema" : "",       "table" : "",       "type" : "text",       "scale" : null,       "precision" : null,       "byteLength" : 16777216,       "nullable" : false,       "collation" : null,       "length" : 16777216     } ],     "partitionInfo": [{       "rowCount": 12344,       "uncompressedSize": 14384873,     },{      "rowCount": 43746,      "uncompressedSize": 43748274,      "compressedSize": 746323     }]   },   "data" : [ [ "Multiple statements executed successfully." ] ],   "code" : "090001",   "statementHandles" : [ "{handle1}", "{handle2}", "{handle3}" ],   "statementStatusUrl" : "/api/v2/statements/{handle}?requestId={id3}",   "sqlState" : "00000",   "statementHandle" : "{handle}",   "message" : "Statement executed successfully.",   "createdOn" : 1622501430333 } ``` |
| 202 | The execution of the statement is still in progress. Use `GET /api/v2/statements/{statementHandle}` to check the status of the statement execution. See [GET /api/v2/statements/{statementHandle}](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements) for details.  The body of the response contains a [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object with details about the status of the statement execution.  The following is an example of a response:  Copy code  ``` HTTP/1.1 202 Accepted Date: Tue, 04 May 2021 18:12:37 GMT Content-Type: application/json Content-Length: 285 {   "code" : "333334",   "message" :       "Asynchronous execution in progress. Use provided query id to perform query monitoring and management.",   "statementHandle" : "019c06a4-0000-df4f-0000-00100006589e",   "statementStatusUrl" : "/api/v2/statements/019c06a4-0000-df4f-0000-00100006589e" } ``` |
| 408 | The execution of the statement exceeded the timeout period. The execution of the statement was cancelled.  The body of the response contains a [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object with details about the cancellation of the statement execution. |
| 422 | An error occurred when executing the statement. Check the error code and error message for details.  The body of the response contains a [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object with details about the error.  The following is an example of a response:  Copy code  ``` HTTP/1.1 422 Unprocessable Entity Date: Tue, 04 May 2021 20:24:11 GMT Content-Type: application/json {   "code" : "000904",   "message" : "SQL compilation error: error line 1 at position 7\ninvalid identifier 'AFAF'",   "sqlState" : "42000",   "statementHandle" : "019c0728-0000-df4f-0000-00100006606e" } ``` |

Expand

Show lessSee more

For the other response codes returned by this operation, see [Response codes for all operations](#label-sql-api-reference-response-codes).

### `GET /api/v2/statements/{statementHandle}`

To check the status of the execution of a statement, send a GET request to `/api/v2/statements/{statementHandle}`. If the
statement has been executed successfully, the body of the response includes a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset)
object containing the requested data.

#### Request syntax

Copy code

```
GET /api/v2/statements/{statementHandle}
```

#### Path parameters

| Parameter | Description |
| --- | --- |
| `statementHandle` | (Required) The handle of the statement that you want to check. You can get this handle from the [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object returned in the response to the [request to execute the statement](#label-sql-api-reference-post-statements). |

Expand

Show lessSee more

#### Query parameters

| `requestId` | (Optional) Unique ID (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)) of the API request. See [Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id). |
| --- | --- |
| `partition` | (Optional) The partition number to return. The size of each partition is determined by Snowflake.  See [Getting the results from the response](/developer-guide/sql-api/handling-responses#label-sql-api-getting-results) for more information. |

Expand

Show lessSee more

#### Request headers

The request must include the headers listed in [Request headers for all operations](#label-sql-api-reference-request-headers).

#### Response

This operation can return the response codes listed below.

| Code | Description |
| --- | --- |
| 200 | The statement was executed successfully.  For this response code, the response can have the following headers:   - [Link](#label-sql-api-reference-response-headers)   The body of the response has a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object containing the requested data.  The following is an example of a response, where `{handle}` is the statement handle and `{id1}`, `{id2}`, `{id3}`, `{id4}`, and `{id5}}` are uniquely generated request IDs:  Copy code  ``` HTTP/1.1 200 OK Date: Tue, 04 May 2021 20:25:46 GMT Content-Type: application/json Link:   </api/v2/statements/{handle}?requestId={id1}&partition=0>; rel="first",   </api/v2/statements/{handle}?requestId={id2}&partition=0>; rel="prev",   </api/v2/statements/{handle}?requestId={id3}&partition=1>; rel="next",   </api/v2/statements/{handle}?requestId={id4}&partition=10>; rel="last" {   "resultSetMetaData" : {     "numRows" : 10000,     "format" : "jsonv2",     "rowType" : [ {       "name" : "SEQ8()",       "database" : "",       "schema" : "",       "table" : "",       "scale" : 0,       "precision" : 19,       "length" : null,       "type" : "fixed",       "nullable" : false,       "byteLength" : null,       "collation" : null     }, {       "name" : "RANDSTR(1000, RANDOM())",       "database" : "",       "schema" : "",       "table" : "",       "scale" : null,       "precision" : null,       "length" : 16777216,       "type" : "text",       "nullable" : false,       "byteLength" : 16777216,       "collation" : null     } ],     "partitionInfo": [{       "rowCount": 12344,       "uncompressedSize": 14384873,     },{       "rowCount": 43746,       "uncompressedSize": 43748274,       "compressedSize": 746323     }]   },   "data" : [ [ "10", "lJPPMTSwps......" ], ... [ "19", "VJKoHmUFJz......" ] ],   "code" : "090001",   "statementStatusUrl" : "/api/v2/statements/{handle}?requestId={id5}&partition=10",   "sqlState" : "00000",   "statementHandle" : "{handle}",   "message" : "Statement executed successfully.",   "createdOn" : 1620151693299 } ``` |
| 202 | The execution of the statement is still in progress. Repeat the request to check the status of the statement execution.  The body of the response contains a [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object with details about the status of the statement execution.  The following is an example of a response:  Copy code  ``` HTTP/1.1 202 Accepted Date: Tue, 04 May 2021 22:31:33 GMT Content-Type: application/json Content-Length: 285 {   "code" : "333334",   "message" :       "Asynchronous execution in progress. Use provided query id to perform query monitoring and management.",   "statementHandle" : "019c07a7-0000-df4f-0000-001000067872",   "statementStatusUrl" : "/api/v2/statements/019c07a7-0000-df4f-0000-001000067872" } ``` |
| 422 | An error occurred when executing the statement. Check the error code and error message for details.  The body of the response contains a [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object with details about the error. |

Expand

Show lessSee more

For the other response codes returned by this operation, see [Response codes for all operations](#label-sql-api-reference-response-codes).

### `POST /api/v2/statements/{statementHandle}/cancel`

To cancel the execution of a statement, send a POST request to `/api/v2/statements/{statementHandle}/cancel`.

#### Request syntax

Copy code

```
POST /api/v2/statements/{statementHandle}/cancel
```

#### Path parameters

| Parameter | Description |
| --- | --- |
| `statementHandle` | (Required) The handle of the statement that you want to check. You can get this handle from the [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object returned in the response to the [request to execute the statement](#label-sql-api-reference-post-statements). |

Expand

Show lessSee more

#### Query parameters

| Parameter | Description |
| --- | --- |
| `requestId` | (Optional) Unique ID (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier)) of the API request. See [Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id). |

Expand

Show lessSee more

#### Request headers

The request must include the headers listed in [Request headers for all operations](#label-sql-api-reference-request-headers).

#### Response

This operation can return the response codes listed below.

| Code | Description |
| --- | --- |
| 200 | Execution of the statement was cancelled successfully.  The body of the response contains a [CancelStatus](#label-sql-api-reference-cancelstatus) object that contains information about the cancellation of the statement.  The following is an example of a response:  Copy code  ``` HTTP/1.1 200 OK Date: Tue, 04 May 2021 22:52:15 GMT Content-Type: application/json Content-Length: 230 {   "code" : "000604",   "sqlState" : "57014",   "message" : "SQL execution canceled",   "statementHandle" : "019c07bc-0000-df4f-0000-001000067c3e",   "statementStatusUrl" : "/api/v2/statements/019c07bc-0000-df4f-0000-001000067c3e" } ``` |
| 422 | An error occurred when executing the statement. Check the error code and error message for details.  The body of the response contains a [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object with details about the error.  The following is an example of a response:  Copy code  ``` HTTP/1.1 422 Unprocessable Entity Date: Tue, 04 May 2021 22:52:49 GMT Content-Type: application/json Content-Length: 183 {   "code" : "000709",   "message" : "Statement 019c07bc-0000-df4f-0000-001000067c3e not found",   "sqlState" : "02000",   "statementHandle" : "019c07bc-0000-df4f-0000-001000067c3e" } ``` |

Expand

Show lessSee more

For the other response codes returned by this operation, see [Response codes for all operations](#label-sql-api-reference-response-codes).

## Request headers for all operations

The following request headers are apply to all operations:

| Header | Required or Optional? | Description |
| --- | --- | --- |
| `Authorization` | Required | Set this to `Bearer`, followed by the token used to authenticate to Snowflake.   - For [key pair authentication](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair), use the generated JWT as the token. - For [OAuth](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-oauth), use the generated OAuth token as the token.   For example:  `Authorization: Bearer token`  See [Authenticating to the server](/developer-guide/sql-api/authenticating#label-sql-api-authenticating). |
| `Accept` | Required | Set this to the list of media types (MIME types) that are acceptable in the body of the response. Include the type `application/json` (or, if all types are acceptable, set this to `*/*`). |
| `Content-Type` | Required | Set this to the media type (MIME type) of the body of the request. Set this to `application/json`. |
| `User-Agent` | Required | Set this to the name and version of your application (e.g. `applicationName/applicationVersion`). You must use a value that complies with [RFC 7231](https://tools.ietf.org/html/rfc7231#section-5.5.3). |
| `X-Snowflake-Authorization-Token-Type` | Optional | Set this to one of the following values:   - `KEYPAIR_JWT`, if you are using [key pair authentication](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair). - `OAUTH`, if you are using [OAuth](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-oauth).   If you omit the `X-Snowflake-Authorization-Token-Type` header, Snowflake determines the token type by examining the token.  Even though this header is optional, you can choose to specify this header. You can set the header to one of the following values:   - `KEYPAIR_JWT` (for key-pair authentication) - `OAUTH` (for OAuth) - `PROGRAMMATIC_ACCESS_TOKEN` (for [programmatic access tokens](/user-guide/programmatic-access-tokens)) |

Expand

Show lessSee more

## Types of objects in the request body

### Body of the `POST` request to `/api/v2/statements/`

The body of a `POST` request to the `/api/v2/statements/` endpoint (see
[Operations](#label-sql-api-reference-post-statements)) is a JSON object that you use to specify the SQL statement to execute, the
statement context, and the format of data in the result set. You use this object in the body of a request to execute a statement.

#### Fields

| Field | Description |
| --- | --- |
| `statement` | (Optional) SQL statement to execute. See [Limitations of the SQL API](/developer-guide/sql-api/intro#label-sql-api-limitations) for the lists of statements that are supported and not supported.  Type: string |
| `timeout` | (Optional) Timeout in seconds for statement execution. If the execution of a statement takes longer than the specified timeout, the execution is automatically canceled. To set the timeout to the maximum value (604800 seconds), set timeout to 0. If this field is not set, the timeout specified by the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) parameter is used.  Type: 64-bit signed integer  Example: `10` |
| `database` | (Optional) Database in which the statement should be executed. The value in this field is case-sensitive.  If you omit this field, the SQL API uses the database from the value of the `DEFAULT_NAMESPACE` [property of the user](/sql-reference/sql/alter-user).  Type: string  Example: `TESTDB` |
| `schema` | (Optional) Schema in which the statement should be executed. The value in this field is case-sensitive.  If you omit this field, the SQL API uses the schema from the value of the `DEFAULT_NAMESPACE` [property of the user](/sql-reference/sql/alter-user).  Type: string  Example: `TESTSCHEMA` |
| `warehouse` | (Optional) Warehouse to use when executing the statement. The value in this field is case-sensitive.  If you omit this field, the SQL API uses the value of the `DEFAULT_WAREHOUSE` [property of the user](/sql-reference/sql/alter-user).  Type: string  Example: `TESTWH` |
| `role` | (Optional) Role to use when executing the statement. The value in this field is case-sensitive.  If you omit this field, the SQL API uses the value of the `DEFAULT_ROLE` [property of the user](/sql-reference/sql/alter-user).  Type: string  Example: `TESTROLE` |
| `bindings` | (Optional) Values of [bind variables](/developer-guide/sql-api/submitting-requests#label-sql-api-bind-variables) in the SQL statement. When executing the statement, Snowflake replaces placeholders (`?` and `:name`) in the statement with these specified values.  Note that the format of this field may change for the GA release of the SQL API.  Type: object  Example:  Copy code  ``` {"1":{"type":"FIXED","value":"123"},"2":{"type":"TEXT","value":"teststring"}} ``` |
| `parameters` | (Optional) [Session parameters](/sql-reference/parameters) that you want to set for this request.  Type: object ([statements\_parameters](/developer-guide/sql-api/reference#label-sql-api-reference-statements-parameters)) |

Expand

Show lessSee more

#### Example

The following is an example of the body object:

Copy code

```
{
  "statement" : "select * from T where c1=?",
  "timeout" : 10,
  "database" : "TESTDB",
  "schema" : "TESTSCHEMA",
  "warehouse" : "TESTWH",
  "role" : "TESTROLE",
  "bindings" : {
    "1" : {
      "type" : "FIXED",
      "value" : "123"
    }
  }
}
```

### `statements_parameters`

`statements_parameters` is a JSON object that you use to specify the [session parameters](/sql-reference/parameters)
that you want to set for this request. This object should be in the `parameters` field of the body of the `POST`
request to the `/api/v2/statements` endpoint (see [Types of objects in the request body](#label-sql-api-reference-post-statements-request-body)).

Note

The SQL API only supports the session parameters listed in the following table.

#### Fields

| Field | Description |
| --- | --- |
| `binary_output_format` | (Optional) Specifies format for VARCHAR values returned as output by BINARY-to-VARCHAR conversion functions. For details, see [BINARY\_OUTPUT\_FORMAT](/sql-reference/parameters#label-binary-output-format).  Type: string  Example: `HEX` |
| `client_result_chunk_size` | (Optional) Specifies the maximum size of each set (or chunk) of query results to download (in MB). For details, see [CLIENT\_RESULT\_CHUNK\_SIZE](/sql-reference/parameters#label-client-result-chunk-size).  Type: integer  Example: `100` |
| `date_output_format` | (Optional) Specifies the display format for the DATE data type. For details, see [DATE\_OUTPUT\_FORMAT](/sql-reference/parameters#label-date-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `YYYY-MM-DD` |
| `multi_statement_count` | (Required when specifying more than one SQL statement in a request) Specifies the number of SQL statements to be submitted in a request when using the multi-statement capability. Valid values are:   - `0`: Indicates that a variable number of statements can be included in the request. - `1`: Indicates that a single SQL statement can be included in the request. This is the default   value used if you do not specify the `MULTI_STATEMENT_COUNT` field. - `> 1`: Indicates the number of SQL statements submitted in the request. This number must match   the number of statements specified in the `statement` field.   Type: string  Example: `2` |
| `query_tag` | (Optional) Query tag that you want to associate with the SQL statement. For details, see [QUERY\_TAG parameter](/sql-reference/parameters#label-query-tag).  Type: string  Example: `tag-1234` |
| `rows_per_resultset` | (Optional) Specifies the maximum number of rows returned in a result set, with 0 (default) meaning no maximum. For details, see [ROWS\_PER\_RESULTSET parameter](/sql-reference/parameters#label-rows-per-resultset).  Type: integer  Example: 200 |
| `time_output_format` | (Optional) Specifies the display format for the TIME data type. For details, see [TIME\_OUTPUT\_FORMAT](/sql-reference/parameters#label-time-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `HH24:MI:SS` |
| `timestamp_ltz_output_format` | (Optional) Specifies the display format for the TIMESTAMP\_LTZ data type. For details, see [TIMESTAMP\_LTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ltz-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `YYYY-MM-DD HH24:MI:SS.FF3` |
| `timestamp_ntz_output_format` | (Optional) Specifies the display format for the TIMESTAMP\_NTZ data type. For details, see [TIMESTAMP\_NTZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-ntz-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `YYYY-MM-DD HH24:MI:SS.FF3` |
| `timestamp_output_format` | (Optional) Specifies the display format for the TIMESTAMP data type alias. For details, see [TIMESTAMP\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `YYYY-MM-DD HH24:MI:SS.FF3 TZHTZM` |
| `timestamp_tz_output_format` | (Optional) Specifies the display format for the TIMESTAMP\_TZ data type. For details, see [TIMESTAMP\_TZ\_OUTPUT\_FORMAT](/sql-reference/parameters#label-timestamp-tz-output-format). See [Formatting the Output of Query Results](/developer-guide/sql-api/handling-responses#label-sql-api-output-format) for details on using parameters to determine the output format of query results.  Type: string  Example: `YYYY-MM-DD HH24:MI:SS.FF3` |
| `timezone` | (Optional) Time zone to use when executing the statement. For details, see [TIMEZONE parameter](/sql-reference/parameters#label-timezone).  Type: string  Example: `america/los_angeles` |
| `use_cached_result` | (Optional) Whether query results can be reused between successive invocations of the same query as long as the original result has not expired. For details, see [USE\_CACHED\_RESULT parameter](/sql-reference/parameters#label-use-cached-result)  Type: string  Example: `true` |

Expand

Show lessSee more

## Response codes for all operations

This section lists the response codes that apply to all operations.

| Code | Description |
| --- | --- |
| 400 | Bad Request.  The request payload is invalid or malformed. This happens if the application didn’t send the correct request payload. The response body may include the error code and message indicating the actual cause. The application must reconstruct the request body for retry.  The following is an example of a response:  Copy code  ``` HTTP/1.1 400 Bad Request Date: Tue, 04 May 2021 22:54:21 GMT Content-Type: application/json {   "code" : "390142",   "message" : "Incoming request does not contain a valid payload." } ``` |
| 401 | Unauthorized.  The request is not authorized. This happens if the attached access token is invalid or missing. The response body may include the error code and message indicating the actual cause, e.g., expired, invalid token. The application must obtain a new access token for retry.  See [Authenticating to the server](/developer-guide/sql-api/authenticating#label-sql-api-authenticating).  The following is an example of a response:  Copy code  ``` HTTP/1.1 401 Unauthorized Date: Tue, 04 May 2021 20:17:57 GMT Content-Type: application/json {   "code" : "390303",   "message" : "Invalid OAuth access token. ...TTTTTTTT" } ``` |
| 403 | Forbidden.  The request is forbidden. This happens if the request is made even if the API is not enabled. |
| 404 | Not Found.  The request endpoint is not valid. This happens if the API endpoint is wrong. For example, if the application requests `/api/v2/hello`, which does not exist, the server returns this code. |
| 405 | Method Not Allowed.  The request method does not match the supported API. This happens, for example, if the application calls the API with the GET method but the endpoint accepts only POST. The application must use a supported method when sending the request.  The following is an example of a response:  Copy code  ``` HTTP/1.1 405 Method Not Allowed Date: Tue, 04 May 2021 22:55:38 GMT Content-Length: 0 ``` |
| 415 | The request header `Content-Type` includes unsupported media type. |
| 422 | The request was well-formed (i.e., syntactically correct) but could not be processed.  The API supports `application/json` only. If no `Content-Type` is specified, the request payload is interpreted as JSON, but if any other media type is specified, this error is returned. |
| 429 | Too many requests.  The number of requests hit the rate limit. The application must reduce the frequency of requests sent to the API endpoints. The application may retry with backoff. Exponentially jittered backoff is recommended.  This response can also occur when the server receives too many concurrent requests. Concurrency limits on the API are determined by the concurrency limits enforced by Snowflake.  The following is an example of a response:  Copy code  ``` HTTP/1.1 429 Too many requests Content-Type: application/json Content-Length: 69 {   "code" : "390505",   "message" : "Too many requests."  } ``` |
| 500 | Internal Server Error.  The server encountered an unrecoverable system error. The response body can include the error code and message for further guidance.  You can retry exponential backoff by setting the `requestId` and `retry` parameters to `true`. For more information, see [Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id). |
| 502 | Bad Gateway.  The server was acting as a gateway or proxy and received an invalid response from the upstream server.  You can retry exponential backoff by setting the `requestId` and `retry` parameters to `true`. For more information, see [Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id). |
| 503 | Service Unavailable.  The request was not processed due to a timeout on the server. The application may retry with backoff. Exponentially jittered backoff is recommended. |
| 504 | Gateway Timeout.  The request was not processed due to a timeout on the server. The application may retry with backoff. Exponentially jittered backoff is recommended. |
| 522 | Invalid SSL Certificate.  The server could not validate the provided SSL certificate. |

Expand

Show lessSee more

## Response headers for all operations

Responses can contain the following headers:

| Header | Description |
| --- | --- |
| `Link` | This header is in the 200 response for a [request to execute the statement](#label-sql-api-reference-post-statements) and a [request to check the status of the execution of a statement](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements).  This header provides links to other partitions of results (e.g. the first partition, the last partition, etc.). The header can include multiple URL entries with different `rel` attribute values that specify the partition to return (`first`, `next`, `prev`, and `last`).  For example:  Copy code  ``` Link: </api/v2/statements/e127cc7c-7812-4e72-9a55-3b4d4f969840?partition=1; rel="last">,       </api/v2/statements/e127cc7c-7812-4e72-9a55-3b4d4f969840?partition=1; rel="next">,       </api/v2/statements/e127cc7c-7812-4e72-9a55-3b4d4f969840?partition=0; rel="first"> ``` |

Expand

Show lessSee more

## Types of objects in the response body

### `CancelStatus`

`CancelStatus` is a JSON object that contains information about the cancellation of the execution of a statement. This
object is returned in the body of the response for a [cancellation request](/developer-guide/sql-api/reference#label-sql-api-reference-post-statements-cancel).

#### Fields

| Field | Description |
| --- | --- |
| `code` | Type: string |
| `sqlState` | Type: string |
| `message`  Example: `successfully cancelled` | Type: string |
| `statementHandle` | Unique identifier for the statement being executed.  Type: string (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier))  Example: `536fad38-b564-4dc5-9892-a4543504df6c` |
| `statementStatusUrl` | URL to get the statement status and result set.  Type: string (a URL)  Example: `/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c` |

Expand

Show lessSee more

#### Example

Copy code

```
{
  "code" : "0",
  "sqlState" : "",
  "message" : "successfully canceled",
  "statementHandle" : "536fad38-b564-4dc5-9892-a4543504df6c",
  "statementStatusUrl" : "/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c"
}
```

### `QueryFailureStatus`

QueryFailureStatus is a JSON object that contains information about a failure to execute a statement. This object is returned in
the body of the 422 response for a [request to execute the statement](#label-sql-api-reference-post-statements).

#### Fields

| Field | Description |
| --- | --- |
| `code` | Type: string  Example: `0` |
| `sqlState` | Type: string |
| `message` | Type: string  Example: `successfully executed` |
| `statementHandle` | Unique identifier for the statement being executed.  Type: string (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier))  Example: `536fad38-b564-4dc5-9892-a4543504df6c` |
| `createdOn` | Timestamp that specifies when the statement execution started. The timestamp is expressed in milliseconds since the epoch.  Type: 64-bit signed integer  Example: `1597090533987` |
| `statementStatusUrl` | URL to get the statement status and result set.  Type: string (a URL)  Example: `/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c` |

Expand

Show lessSee more

#### Example

Copy code

```
{
  "code" : "002139",
  "sqlState" : "42601",
  "message" : "SQL compilation error: Unknown function",
  "statementHandle" : "e4ce975e-f7ff-4b5e-b15e-bf25f59371ae",
  "statementStatusUrl" : "/api/v2/statements/e4ce975e-f7ff-4b5e-b15e-bf25f59371ae"
}
```

### `QueryStatus`

`QueryStatus` is a JSON object that contains information about the status of the execution of a statement. This object is
returned in the following:

- the body of the 202 and 408 response for a [request to execute the statement](#label-sql-api-reference-post-statements).
- the body of a 202 and 422 response for a
  [request to check the status of the execution of a statement](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements).

#### Fields

| Field | Description |
| --- | --- |
| `code` | Type: string  Example: `0` |
| `sqlState` | Type: string |
| `message` | Type: string  Example: `successfully executed` |
| `statementHandle` | Unique identifier for the statement being executed.  Type: string (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier))  Example: `536fad38-b564-4dc5-9892-a4543504df6c` |
| `createdOn` | Timestamp that specifies when the statement execution started. The timestamp is expressed in milliseconds since the epoch.  Type: 64-bit signed integer  Example: `1597090533987` |
| `statementStatusUrl` | URL to get the statement status and result set.  Type: string (a URL)  Example: `/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c` |

Expand

Show lessSee more

#### Example

Copy code

```
{
  "code" : "0",
  "sqlState" : "",
  "message" : "successfully executed",
  "statementHandle" : "e4ce975e-f7ff-4b5e-b15e-bf25f59371ae",
  "statementStatusUrl" : "/api/v2/statements/e4ce975e-f7ff-4b5e-b15e-bf25f59371ae"
}
```

### `ResultSet`

`ResultSet` is a JSON object that contains the results of the execution of a statement. This object is returned in the body
of the 200 response for a [request to execute the statement](#label-sql-api-reference-post-statements) and a
[request to check the status of the execution of a statement](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements).

#### Fields

| Field | Description |
| --- | --- |
| `code` | Type: string  Example: `0` |
| `sqlState` | Type: string |
| `message` | Type: string  Example: `successfully executed` |
| `statementHandle` | Unique identifier for the statement being executed.  If multiple statements were specified in the request, this handle corresponds to the set of those statements. For the handles of the individual statements in the request, see the `statementHandles` field.  Type: string (a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier))  Example: `536fad38-b564-4dc5-9892-a4543504df6c` |
| `statementHandles` | Array of unique identifiers for the statements being executed for this request.  Type: array of strings ([UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier))  Example: `[ "019c9f9a-0502-f25e-0000-438300e0d046", "019c9f9a-0502-f25e-0000-438300e0d04a", "019c9f9a-0502-f25e-0000-438300e0d04e" ]` |
| `createdOn` | Timestamp that specifies when the statement execution started. The timestamp is expressed in milliseconds since the epoch.  Example: `1597090533987` |
| `statementStatusUrl` | URL to get the statement status and result set.  Type: string (a URL)  Example: `/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c` |
| `resultSetMetaData` | Metadata about the result set returned.  Type: object ([ResultSet\_resultSetMetaData](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata)) |
| `data` | **If the request contains a single SQL statement,** this field contains the result set data.  A result set format is an array of arrays in JSON:   - Each array corresponds to a single row. - The elements in a row correspond to the values in the columns for that row. - The data is encoded as JSON strings, regardless of the Snowflake datatype.   Type: array of arrays  Example:  Copy code  ``` [   ["customer1","1234 A Avenue","98765","1565481394123000000"],   ["customer2","987 B Street","98765","1565516712912012345"],   ["customer3","8777 C Blvd","98765","1565605431999999999"],   ["customer4","64646 D Circle","98765","1565661272000000000"] ] ```  **If the request contains multiple SQL statements,** this field just contains the message “Multiple statements executed successfully”. To retrieve the results for each statement in the request, get the handles for these statements from the `statementHandles` field, and [send requests to get the results of each statement](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements). |
| `stats` | For DML statements, this field contains statistics about the number of rows affected by the operation.  Type: object ([ResultSet\_stats](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-stats)) |

Expand

Show lessSee more

### `ResultSet_resultSetMetaData`

`ResultSet_resultSetMetaData` is a JSON object that contains metadata about the results of the execution of a statement.
This object is in the `resultSetMetaData` field of the [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object.

#### Fields

| Field | Description |
| --- | --- |
| `partition` | The index number of the partition that you want to return (where `0` specifies the first partition of data). Snowflake returns data in partitions. Snowflake determines the number of partitions and the size of each partition at runtime. You can get the list of partitions from the `resultSetMetaData` object in the response to the POST request.  See [Getting the results from the response](/developer-guide/sql-api/handling-responses#label-sql-api-getting-results) for more information. |
| `numRows` | The total number of rows of results.  Type: 64-bit signed integer  Example: `100` |
| `format` | Format of the data in the result set.  Type: string |
| `rowType` | Array of [ResultSet\_resultSetMetaData\_rowType](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata-rowtype) objects that describe the columns in the set of results.  Type: array of [ResultSet\_resultSetMetaData\_rowType](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata-rowtype).  Example:  Copy code  ``` [  {"name":"ROWNUM","type":"FIXED","length":0,"precision":38,"scale":0,"nullable":false},  {"name":"ACCOUNT_ID","type":"FIXED","length":0,"precision":38,"scale":0,"nullable":false},  {"name":"ACCOUNT_NAME","type":"TEXT","length":1024,"precision":0,"scale":0,"nullable":false},  {"name":"ADDRESS","type":"TEXT","length":16777216,"precision":0,"scale":0,"nullable":true},  {"name":"ZIP","type":"TEXT","length":100,"precision":0,"scale":0,"nullable":true},  {"name":"CREATED_ON","type":"TIMESTAMP_NTZ","length":0,"precision":0,"scale":3,"nullable":false} ] ``` |

Expand

Show lessSee more

### `ResultSet_resultSetMetaData_rowType`

`ResultSet_resultSetMetaData_rowType` is a JSON object that describes a column in a set of results. An array of these
objects is in the `rowType` field of the [ResultSet\_resultSetMetaData](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata) object.

#### Fields

| Field | Description |
| --- | --- |
| `name` | Name of the column.  Type: string |
| `type` | [Snowflake data type](/sql-reference/intro-summary-data-types) of the column.  Type: string |
| `length` | Length of the column.  Type: 64-bit signed integer |
| `precision` | Precision of the column.  Type: 64-bit signed integer |
| `scale` | Scale of the column.  Type: 64-bit signed integer |
| `nullable` | Specifies whether or not the column is nullable.  Type: boolean |

Expand

Show lessSee more

#### Example

Copy code

```
{
 "name":"ACCOUNT_NAME",
 "type":"TEXT",
 "length":1024,
 "precision":0,
 "scale":0,
 "nullable":false
}
```

### `ResultSet_stats`

`ResultSet_stats` is a JSON object that contains statistics about the execution of a DML statement. This object is in the
`stats` field of the [ResultSet\_resultSetMetaData](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata) object.

#### Fields

| Field | Description |
| --- | --- |
| `numRowsInserted` | Number of rows that were inserted.  Type: 64-bit signed integer  Example: `12` |
| `numRowsUpdated` | Number of rows that were updated.  Type: 64-bit signed integer  Example: `9` |
| `numRowsDeleted` | Number of rows that were deleted.  Type: 64-bit signed integer  Example: `8` |
| `numDuplicateRowsUpdated` | Number of duplicate rows that were updated.  Type: 64-bit signed integer  Example: `20` |

Expand

Show lessSee more
