# Snowpipe REST API reference

You interact with a pipe by making calls to REST endpoints. This topic describes the Snowpipe REST API for defining the list of files to ingest and fetching reports of the load history. For an overview of how the API works, including authentication and an example, see [Load data with the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview).

Snowflake also provides the [Snowflake Ingest SDKs for Java and Python](/user-guide/data-load-snowpipe-rest-load), which simplify working with the Snowpipe REST API.

## Data file ingestion

The Snowpipe API provides a REST endpoint for defining the list of files to ingest.

### Endpoint: `insertFiles`

Informs Snowflake about the files to be ingested into a table. A successful response from this endpoint means that Snowflake has recorded the list of files to add to the table. It does not necessarily mean the files have been ingested. For more details, see the response codes below.

In most cases, Snowflake inserts fresh data into the target table within a few minutes.

**Method:** `POST`

**POST URL:**

> `https://{account}.snowflakecomputing.com/v1/data/pipes/{pipeName}/insertFiles?requestId={requestId}`

**URL Parameters:**

- `account` (Required): Account identifier for your Snowflake account.
- `pipeName` (Required): Fully qualified pipe name. Unquoted parts of the name aren’t case-sensitive; double-quoted parts are. For example, `MYDB.MYSCHEMA.MYPIPE`.
- `requestId` (Optional): String used to track requests through the system. We recommend providing a random string with each request, for example, a UUID. Append it to the URL like this: `?requestId=<your_uuid>`.
- `showSkippedFiles` (Optional): Set to `true` to include a `skippedFiles` array in the response. The array lists paths that the pipe already received in the last 14 days and therefore skipped. The default is `false`.

**Request Headers**

- `Content-Type:`:

  - `text/plain`: For a plain text list of file paths and filenames, one per line. The size parameter is not allowed in this format.
  - `application/json`: For a JSON object containing a list of files with optional size information.
- `Authorization`: `Bearer <jwt_token>` for key pair authentication, or `Bearer WIF.<provider>.<token>` for [workload identity federation](/user-guide/workload-identity-federation).

**Request Body (for application/json Content-Type)**

The request body must be a JSON object with a single key named “files”. The value associated with this key is an array of JSON objects, where each object represents a file to be ingested.

Copy code

```
{
  "files":[
    {
      "path":"filePath/file1.csv",
      "size":100
    },
    {
      "path":"filePath/file2.csv",
      "size":100
    }
   ]
}
```

Each element in the “files” array is a JSON object with the following attributes:

- `path` (Required): The path and filename of the staged file, relative to the location in the pipe’s `COPY INTO` statement. If that statement names only the stage, the path is relative to the root of the stage, which is the stage URL for an external stage. If the statement includes a path, such as `@mystage/2026/`, the path in the request is relative to `2026/`. Include the full path under that location when you partition files into directories.
- `size` (Optional, but recommended for better performance): The size of the file in bytes.

**Request Body (for text/plain Content-Type)**

The request body should be a plain text list of file paths and filenames, with one entry per line.

```
filePath/file_a.csv
another/path/file_b.json
yet/another/file_c.txt
```

Note

The request can contain at most 5,000 files. Each file path can be at most 1,024 bytes long when encoded as UTF-8.

**Response Body**

> Response Codes:
>
> - 200: Success. Snowflake added the files to the ingest queue. Files that the pipe already received in the last 14 days are skipped.
> - 400: Failure. The request is invalid. For example, the request has no files, a file path is too long, or the pipe is in the `STOPPED_CLONED` state.
> - 401: Failure. The token (a key pair JWT or a workload identity federation token) is invalid or expired.
> - 403: Failure. The role used when calling the endpoint has privileges on the pipe, but not the `OPERATE` privilege.
> - 404: Failure. `pipeName` isn’t recognized, or the role has no privileges on the pipe or on the database and schema that contain it. For more information, see [Grant access privileges](/user-guide/data-load-snowpipe-rest-gs#label-snowpipe-rest-endpoints-access-control).
> - 415: Failure. The `Content-Type` header isn’t `application/json` or `text/plain`.
> - 429: Failure. Snowflake limited the rate of requests or of submitted files, or the request contains more than 5,000 files.
> - 500: Failure. An internal error occurred, or the request body couldn’t be parsed.
>
> For more information about handling these codes, see [Handle errors and retries](/user-guide/data-load-snowpipe-rest-overview#label-snowpipe-rest-errors).
>
> Response Payload:
>
> > With a successful API request (code 200), the response payload contains the `requestId` and `responseCode` elements in JSON format. The `requestId` element is included only if you specified the `requestId` parameter. If an error occurs, the response payload might contain details about the error.
> >
> > The following example shows a successful response:
> >
> > Copy code
> >
> > ```
> > {
> >   "requestId": "your_request_uuid",
> >   "responseCode": "SUCCESS"
> > }
> > ```
> >
> > If the [COPY INTO <table>](/sql-reference/sql/copy-into-table) statement in the pipe definition includes the `PATTERN` copy option, the `unmatchedPatternFiles` attribute lists any submitted files that didn’t match the regular expression and were therefore skipped. If you set `showSkippedFiles` to `true`, the `skippedFiles` attribute lists paths that the pipe already received in the last 14 days.
> >
> > The following example shows a response that lists unmatched files:
> >
> > > Copy code
> > >
> > > ```
> > > {
> > >   "requestId": "your_request_uuid",
> > >   "responseCode": "SUCCESS",
> > >   "unmatchedPatternFiles": ["some_file.txt", "another_file.dat"]
> > > }
> > > ```

## Load history reports

The Snowpipe API provides REST endpoints for fetching load reports.

### Endpoint: `insertReport`

Retrieves a report of files submitted via `insertFiles` whose contents were recently ingested into a table. Note that for large files, this may only be part of the file.

Note the following limitations for this endpoint:

- The 10,000 most recent events are retained.
- Events are retained for a maximum of 10 minutes.

An event occurs when data from a file submitted via `insertFiles` has been committed to the table and is available to queries. The `insertReport` endpoint can be thought of like the UNIX command tail. By calling this command repeatedly, it is possible to see the full history of events on a pipe over time. Note that the command must be called often enough to not miss events. How often depends on the rate files are sent to `insertFiles`.

**Method:** `GET`

**GET URL:**

> `https://<account_identifier>.snowflakecomputing.com/v1/data/pipes/<pipeName>/insertReport?requestId=<requestId>&beginMark=<beginMark>`

**URL Parameters:**

- `account_identifier` (Required): Your unique Snowflake account identifier. The preferred format is `organization_name-account_name`. For alternative formats (account locator with region and cloud platform), see [Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).
- `pipeName` (Required): Fully qualified pipe name. Unquoted parts of the name aren’t case-sensitive; double-quoted parts are. For example, `MYDB.MYSCHEMA.MYPIPE`.
- `requestId` (Optional): A string you can provide to track this specific request through Snowflake’s system. Using a random string like a UUID is highly recommended for easier debugging and monitoring. Append this to the URL like so: `?requestId=<your_uuid>`.
- `beginMark` (Optional): A marker value returned in the `nextBeginMark` field of a previous `insertReport` response. Including this marker helps optimize subsequent calls by potentially reducing the number of duplicate events returned. Note: While `beginMark` is intended as a hint to avoid duplicates, occasional repetition of events might still occur. If `beginMark` is not specified, the report will show the ingestion history from the last 10 minutes. Append this to the URL like so: `?beginMark=<previous_nextBeginMark>`.

**Request Headers:**

- `Accept`: `application/json`. The endpoint always returns the report in JSON format.
- `Authorization`: Your Snowflake authentication token. Use the format `Bearer <jwt_token>` for key pair authentication, or `Bearer WIF.<provider>.<token>` for workload identity federation.

**Request Body:**

This endpoint does not accept a request body for GET requests. The necessary parameters are provided in the URL and headers.

**Response Body:**

> Response Codes:
>
> - 200: Success. Snowflake returned the report.
> - 400: Failure. The request is invalid. For example, the pipe is in the `STOPPED_CLONED` state.
> - 401: Failure. The token (a key pair JWT or a workload identity federation token) is invalid or expired.
> - 403: Failure. The role used when calling the endpoint has privileges on the pipe, but not `MONITOR` on the pipe or `MONITOR EXECUTION` on the account.
> - 404: Failure. `pipeName` isn’t recognized, or the role has no privileges on the pipe or on the database and schema that contain it. For more information, see [Grant access privileges](/user-guide/data-load-snowpipe-rest-gs#label-snowpipe-rest-endpoints-access-control).
> - 429: Failure. Snowflake limited the request rate.
> - 500: Failure. An internal error occurred.
>
> Response Payload:
>
> > A success response (200) contains information about files that have recently been added to the table. Note that this report may only represent a portion of a large file.
> >
> > For example:
> >
> > > Copy code
> > >
> > > ```
> > > {
> > >   "pipe": "TESTDB.TESTSCHEMA.pipe2",
> > >   "completeResult": true,
> > >   "nextBeginMark": "1_39",
> > >   "files": [
> > >     {
> > >       "path": "data2859002086815673867.csv",
> > >       "stageLocation": "s3://mybucket/",
> > >       "fileSize": 57,
> > >       "timeReceived": "2017-06-21T04:47:41.453Z",
> > >       "lastInsertTime": "2017-06-21T04:48:28.575Z",
> > >       "rowsInserted": 1,
> > >       "rowsParsed": 1,
> > >       "errorsSeen": 0,
> > >       "errorLimit": 1,
> > >       "complete": true,
> > >       "status": "LOADED"
> > >     }
> > >   ]
> > > }
> > > ```
>
> Response Fields:
>
> > | Field | Type | Description |
> > | --- | --- | --- |
> > | `pipe` | String | The fully-qualified name of the pipe. |
> > | `completeResult` | Boolean | `false` if an event was missed between the supplied `beginMark` and the first event in this report history. Otherwise, `true`. |
> > | `nextBeginMark` | String | `beginMark` to use on the next request to avoid seeing duplicate records. Note that this value is a hint. Duplicates can still occasionally occur. |
> > | `files` | Array | An array of JSON objects, one object for each file that is part of the history response. |
> > | `path` | String | The file path relative to the location in the pipe’s `COPY INTO` statement. |
> > | `stageLocation` | String | The location that `path` is relative to: the stage’s location plus any path in the pipe’s `FROM` clause. For an external stage, this is a cloud storage location, such as `s3://mybucket/orders/`. For an internal stage, it starts with a path prefix that Snowflake uses for the stage, such as `stages/<uuid>/`, not the stage name. |
> > | `fileSize` | Long | File size, in bytes. |
> > | `timeReceived` | String | Time that this file was received for processing. Format is ISO-8601 in UTC time zone. |
> > | `lastInsertTime` | String | Time that data from this file was last inserted into the table. Format is ISO-8601 in UTC time zone. |
> > | `rowsInserted` | Long | Number of rows inserted into the target table from the file. |
> > | `rowsParsed` | Long | Number of rows parsed from the file. Rows with errors may be skipped. |
> > | `errorsSeen` | Integer | Number of errors seen in the file |
> > | `errorLimit` | Integer | Number of errors allowed in the file before it is considered failed (based on ON\_ERROR copy option). |
> > | `firstError` [1] | String | Error message for the first error encountered in this file. |
> > | `firstErrorLineNum` [1] | Long | Line number of the first error. |
> > | `firstErrorCharacterPos` [1] | Long | Character position of the first error. |
> > | `firstErrorColumnName` [1] | String | Column name where the first error occurred. |
> > | `systemError` [1] | String | General error describing why the file was not processed. |
> > | `complete` | Boolean | Indicates whether the file was completely processed successfully. |
> > | `status` | String | Load status for the file: |
> > |  |  | - LOAD\_IN\_PROGRESS: Part of the file has been loaded into the table, but the load process has not completed yet. |
> > |  |  | - LOADED: The entire file has been loaded into the table. |
> > |  |  | - LOAD\_FAILED: The file load failed. |
> > |  |  | - PARTIALLY\_LOADED: Some rows from this file were loaded successfully, but others were not loaded due to errors. Processing of this file is completed. |
> > | [1] Values are only supplied for these fields when files include errors. |  |  |
> >
> > Expand
> >
> > Show lessSee more

### Endpoint: `loadHistoryScan`

Fetches a report about ingested files whose contents have been added to table. Note that for large files, this may only be part of the file. This endpoint differs from `insertReport` in that it views the history between two points in time. There is a maximum of 10,000 items returned, but multiple calls can be issued to cover the desired time range.

Important

This endpoint is rate limited to avoid excessive calls. To help avoid exceeding the rate limit (error code 429), we recommend relying more heavily on `insertReport` than `loadHistoryScan`. When calling `loadHistoryScan`, specify the most narrow time range that includes a set of data loads. For example, reading the last 10 minutes of history every 8 minutes would work well. Trying to read the last 24 hours of history every minute will result in 429 errors indicating a rate limit has been reached. The rate limits are designed to allow each history record to be read a handful of times.

For a more comprehensive view, without these limits, Snowflake provides an Information Schema table function, [COPY\_HISTORY](/sql-reference/functions/copy_history), that returns the load history of a pipe or table.

**Method:** `GET`

**GET URL:**

> `https://{account}.snowflakecomputing.com/v1/data/pipes/{pipeName}/loadHistoryScan?startTimeInclusive=<startTime>&endTimeExclusive=<endTime>&requestId=<requestId>`

**URL Parameters:**

- `account` (Required): Your unique Snowflake account identifier.
- `pipeName` (Required): Fully qualified pipe name. Unquoted parts of the name aren’t case-sensitive; double-quoted parts are. For example, `MYDB.MYSCHEMA.MYPIPE`.
- `startTimeInclusive` (Required): The beginning of the time range for retrieving load history data, specified as a timestamp in ISO-8601 format (for example, 2023-10-26T10:00:00Z). This timestamp marks the inclusive lower bound of the query. The endpoint returns load history from the last 14 days only.
- `endTimeExclusive` (Optional): The end of the time range for retrieving load history data, specified as a timestamp in ISO-8601 format (for example, 2023-10-26T10:15:00Z). This timestamp marks the exclusive upper bound of the query. If this parameter is omitted, the current server timestamp (CURRENT\_TIMESTAMP()) will be used as the end of the time range.
- `requestId` (Optional): A string you can provide to track this specific request through Snowflake’s system. We recommend using a random string like a UUID for easier debugging and monitoring. Append this to the URL like so: `?requestId=<your_uuid>`.

**Request Headers:**

- `Accept`: `application/json`. The endpoint always returns the report in JSON format.
- `Authorization`: Your Snowflake authentication token. Use the format `Bearer <jwt_token>` for key pair authentication, or `Bearer WIF.<provider>.<token>` for workload identity federation.

**Request Body:**

This endpoint does not accept a request body for `GET` requests. All necessary parameters are provided in the URL and headers.

**Response Body:**

> Response Codes:
>
> - 200: Success. Snowflake returned the load history.
> - 400: Failure. The request is invalid. For example, `startTimeInclusive` is missing or isn’t a valid ISO-8601 timestamp, or the pipe is in the `STOPPED_CLONED` state.
> - 401: Failure. The token (a key pair JWT or a workload identity federation token) is invalid or expired.
> - 403: Failure. The role used when calling the endpoint has privileges on the pipe, but not `MONITOR` on the pipe or `MONITOR EXECUTION` on the account.
> - 404: Failure. `pipeName` isn’t recognized, or the role has no privileges on the pipe or on the database and schema that contain it. For more information, see [Grant access privileges](/user-guide/data-load-snowpipe-rest-gs#label-snowpipe-rest-endpoints-access-control).
> - 429: Failure. Snowflake limited the request rate.
> - 500: Failure. An internal error occurred.
>
> Response Payload:
>
> > A success response (200) contains information about files that have recently been added to the table. Note that this report may only represent a portion of a large file.
> >
> > For example:
> >
> > > Copy code
> > >
> > > ```
> > > {
> > >   "pipe": "TESTDB.TESTSCHEMA.pipe2",
> > >   "completeResult": "true",
> > >   "startTimeInclusive": "2017-08-25T18:42:31.081Z",
> > >   "endTimeExclusive":"2017-08-25T22:43:45.552Z",
> > >   "rangeStartTime":"2017-08-25T22:43:45.383Z",
> > >   "rangeEndTime":"2017-08-25T22:43:45.383Z",
> > >   "files": [
> > >     {
> > >       "path": "data2859002086815673867.csv",
> > >       "stageLocation": "s3://mystage/",
> > >       "fileSize": 57,
> > >       "timeReceived": "2017-08-25T22:43:45.383Z",
> > >       "lastInsertTime": "2017-08-25T22:43:45.383Z",
> > >       "rowsInserted": 1,
> > >       "rowsParsed": 1,
> > >       "errorsSeen": 0,
> > >       "errorLimit": 1,
> > >       "complete": true,
> > >       "status": "LOADED"
> > >     }
> > >   ]
> > > }
> > > ```
>
> Response Fields:
>
> | Field | Type | Description |
> | --- | --- | --- |
> | `pipe` | String | Fully-qualified name of the pipe. |
> | `completeResult` | String | `"false"` if the report is incomplete because the number of entries in the specified time range exceeds the 10,000-entry limit. The value is a string, either `"true"` or `"false"`. If the value is `"false"`, specify the current `rangeEndTime` value as the `startTimeInclusive` value for the next request to get the next set of entries. |
> | `startTimeInclusive` | String | Starting timestamp (in ISO-8601 format) provided in the request. |
> | `endTimeExclusive` | String | Ending timestamp (in ISO-8601 format) provided in the request. |
> | `rangeStartTime` | String | Timestamp (in ISO-8601 format) of the oldest entry in the files included in the response. |
> | `rangeEndTime` | String | Timestamp (in ISO-8601 format) of the latest entry in the files included in the response. |
> | `files` | Array | An array of JSON objects, one object for each file that is part of the history response. Within the array, the response fields are the same as those returned in the `insertReport` response. |
>
> Expand
>
> Show lessSee more
