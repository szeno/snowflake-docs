# Handling responses

This topic explains how to handle a response from the SQL API.

## Understanding the flow of execution

By default, Snowflake executes the statement synchronously and returns one of the response codes shown in the flow chart below:

> ![Flow chart for submitting a statement for execution](/static/images/sql-api-flow-chart-submit.png)

As shown in the flow chart above:

- If you submitted a single statement that was executed successfully, Snowflake returns the HTTP response code 200 and the
  rows from the results in a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object.

  Use the `ResultSet` object to [retrieve the results](#label-sql-api-getting-results).
- If you submitted [multiple statements in a single request](/developer-guide/sql-api/submitting-multiple-statements) and the request
  was processed successfully, Snowflake returns the HTTP response code 200 and a
  [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object.

  The `ResultSet` object does not contain any rows from the results. Instead, the `data` field just contains the
  message “Multiple statements executed successfully.”

  To retrieve the data, you must get the handles of the individual statements in the request from the `statementHandles`
  field. For each statement handle, send a request to check the status of the execution of the statement. See
  [Checking the status of the statement execution and retrieving the data](#label-sql-api-checking-statement-status).

  For more information about the process of handling a response for a request that specifies multiple SQL statements, see
  [Getting the results for each SQL statement in the request](/developer-guide/sql-api/submitting-multiple-statements#label-sql-api-checking-multiple-statement-status).
- If the statement takes longer than 45 seconds to execute or if you specified that the statement should be executed
  asynchronously, Snowflake returns the HTTP response code 202 with a
  [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object.

  You can send a request to the endpoint specified by the `statementStatusUrl` field in the `QueryStatus` object to
  check the status of the execution of the statement. See
  [Checking the status of the statement execution and retrieving the data](#label-sql-api-checking-statement-status).

  If you want to cancel the execution of the statement, you can send a request to the
  `/api/v2/statements/statementHandle/cancel`, using the statement handle from the `statementHandle` field in the
  `QueryStatus` object. See [Canceling the execution of a SQL statement](/developer-guide/sql-api/cancelling-requests).

## Checking the status of the statement execution and retrieving the data

In some cases, you need to send a request to check the status of the execution of a statement:

- When you [submit a SQL statement for execution](/developer-guide/sql-api/submitting-requests), Snowflake returns a 202 response code
  if the execution of the statement has not yet completed or if you submitted an asynchronous query.

  To check if the statement has finished executing, you must send a request to check the status of the statement.
- If you [submitted multiple SQL statements in a single request](/developer-guide/sql-api/submitting-multiple-statements), you get the
  results of each individual statement by sending a request to check the status of the statement.

In both of these cases, you send a `GET` request to the `/api/v2/statements/` endpoint and append the statement handle to
the end of the URL path as a path parameter. See [GET /api/v2/statements/{statementHandle}](/developer-guide/sql-api/reference#label-sql-api-reference-get-statements) for details.

Copy code

```
GET /api/v2/statements/{statementHandle}
```

`{statementHandle}` is the handle of the statement that you want to check. To get the statement handle:

- If you received response with a 202 response code, the body of the response includes a
  [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object. You can get the statement handle from the
  `statementHandle` field of this object.

  Note that you can also get the full URL for the request from the `statementStatusUrl` field of this object.

  Copy code

  ```
  {
    "code": "090001",
    "sqlState": "00000",
    "message": "successfully executed",
    "statementHandle": "e4ce975e-f7ff-4b5e-b15e-bf25f59371ae",
    "statementStatusUrl": "/api/v2/statements/e4ce975e-f7ff-4b5e-b15e-bf25f59371ae"
  }
  ```
- If you submitted a request containing multiple SQL statements, the body of the response includes a `ResultSet` object that
  contains a `statementHandles` field. You can get the handles for the individual statements from this field.

  Copy code

  ```
  {
    ...
    "statementHandles" : [ "019c9fce-0502-f1fc-0000-438300e02412", "019c9fce-0502-f1fc-0000-438300e02416" ],
    ...
  }
  ```

For example, the following `curl` command checks that status of the statement with the handle
`e4ce975e-f7ff-4b5e-b15e-bf25f59371ae`:

Copy code

```
curl -i -X GET \
    -H "Authorization: Bearer <jwt>" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -H "User-Agent: myApplicationName/1.0" \
    "https://<account_identifier>.snowflakecomputing.com/api/v2/statements/e4ce975e-f7ff-4b5e-b15e-bf25f59371ae"
```

where:

- `jwt` is the [JWT that you generated for authentication](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair).
- `myApplicationName` is an example of an identifier for your application.
- `account_identifier` is your [account identifier](/user-guide/admin-account-identifier).

When you send a request to check the status, Snowflake returns one of the response codes shown in the flow chart below:

![Flow chart for submitting a statement for execution](/static/images/sql-api-flow-chart-async.png)

As shown in the flow chart above:

- If the statement has finished executing successfully, Snowflake returns the HTTP response code 200 and the rows from the results
  in a [ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object.

  Use the `ResultSet` object to [retrieve the results](#label-sql-api-getting-results).
- If the statement has not finished executing, Snowflake returns the HTTP response code 202 or 429 with a
  [QueryStatus](/developer-guide/sql-api/reference#label-sql-api-reference-querystatus) object.

  Use this object to [check the status of the execution of the statement](#label-sql-api-checking-statement-status).
- If an error occurred when executing the statement, Snowflake returns the HTTP response code 422 with a
  [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object.

  You can get [details about the error](/developer-guide/sql-api/handling-errors) from this object.

## Getting the results from the response

Note

Snowflake version 5.40 introduces changes to the way data returned by the Snowflake SQL API is handled, among other changes.

This section describes how to get the results from a response using newer functionality of the Snowflake SQL API.
For information on using the older, deprecated behavior see [Deprecated functionality](/developer-guide/sql-api/sql-api-old#label-sql-api-old).

If you [submit a SQL statement for execution](/developer-guide/sql-api/submitting-requests) or
[check the status of statement execution](#label-sql-api-checking-statement-status), Snowflake returns a
[ResultSet](/developer-guide/sql-api/reference#label-sql-api-reference-resultset) object in the body of the response if the statement was executed
successfully.

The Snowflake API returns data in partitions. Snowflake determines the number of partitions and the size of each
partition that is returned. The size of a partition is variable and is based on the amount of data returned by Snowflake for
a particular SQL query.

When you submit a request, the body of this response includes a `partitionInfo` field. This field contains an array of objects, each of which describes a partition of data. This first object describes the partition of data returned in this response.
The rest of the objects describe the additional partitions that you can retrieve by submitting subsequent requests with `partition=partition_number`.

Each object in the array specifies the number of rows and size of a partition. Your application can use this partition metadata to determine how to handle the partitions returned for subsequent requests.

The following shows an example of part of the response:

Copy code

```
{
  "code": "090001",
  "statementHandle": "536fad38-b564-4dc5-9892-a4543504df6c",
  "sqlState": "00000",
  "message": "successfully executed",
  "createdOn": 1597090533987,
  "statementStatusUrl": "/api/v2/statements/536fad38-b564-4dc5-9892-a4543504df6c",
  "resultSetMetaData" : {
    "numRows" : 50000,
    "format" : "jsonv2",
    "partitionInfo" : [ {
      "rowCount" : 12288,
      "uncompressedSize" : 124067,
      "compressedSize" : 29591
    }, {
      "rowCount" : 37712,
      "uncompressedSize" : 414841,
      "compressedSize" : 84469
    }],
  },
  "data": [
    ["customer1", "1234 A Avenue", "98765", "2021-01-20
    12:34:56.03459878"],
    ["customer2", "987 B Street", "98765", "2020-05-31
    01:15:43.765432134"],
    ["customer3", "8777 C Blvd", "98765", "2019-07-01
    23:12:55.123467865"],
    ["customer4", "64646 D Circle", "98765", "2021-08-03
    13:43:23.0"]
  ]
}
```

## Getting metadata about the results

In the `ResultSet` object returned in the response, the `resultSetMetaData` field contains a
[ResultSet\_resultSetMetaData](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata) object that describes the
result set (for example, the format of the results, the number of partitions returned, etc.).

### Getting metadata about the columns returned in the `ResultSet` object

The `resultSetMetaData` field contains information about the columns returned in the `ResultSet` object.

In the example below, the `rowType` field contains an array of
[ResultSet\_resultSetMetaData\_rowType](/developer-guide/sql-api/reference#label-sql-api-reference-resultset-resultsetmetadata-rowtype)
objects. Each object describes a column in the results. The `type` field specifies the Snowflake data type of the
column.

Copy code

```
{
 "resultSetMetaData": {
  "numRows": 1300,
  "rowType": [
   {
    "name":"ROWNUM",
    "type":"FIXED",
    "length":0,
    "precision":38,
    "scale":0,
    "nullable":false
   }, {
    "name":"ACCOUNT_NAME",
    "type":"TEXT",
    "length":1024,
    "precision":0,
    "scale":0,
    "nullable":false
   }, {
    "name":"ADDRESS",
    "type":"TEXT",
    "length":16777216,
    "precision":0,
    "scale":0,
    "nullable":true
   }, {
    "name":"ZIP",
    "type":"TEXT",
    "length":100,
    "precision":0,
    "scale":0,
    "nullable":true
   }, {
    "name":"CREATED_ON",
    "type":"TIMESTAMP_NTZ",
    "length":0,
    "precision":0,
    "scale":3,
    "nullable":false
   }],
  "partitionInfo": [{
    ... // Partition metadata
  }]
 }
}
```

### Getting metadata about the partitions returned by the `ResultSet` object

When you submit a request to execute a query, the response includes metadata that describes how the data is partitioned across responses as well as the first partition of data.

The `resultSetMetaData` field contains a `partitionInfo` field. This field contain an array of objects, each of which
describes a partition of data. This first object describes the partition of data returned in this response. The rest of the objects
describe the additional partitions that you can retrieve by submitting subsequent requests with `partition=partition_number`.

The following shows an example of part of the response:

Copy code

```
  {
    "resultSetMetaData": {
    "numRows: 103477,
    "format": "jsonv2"
    "rowType": {
      ... // Column metadata.
    },
    "partitionInfo": [{
        "rowCount": 12344,
        "uncompressedSize": 14384873,
      },{
        "rowCount": 47387,
        "uncompressedSize": 76483423,
        "compressedSize": 4342748
      },{
        "rowCount": 43746,
        "uncompressedSize": 43748274,
        "compressedSize": 746323
    }]
  },
  ...
}
```

In this example, the first object in the `partitionInfo` field describes the partition of data in the data field of this response.

The second object describes the second partition of data, which contains 47387 rows and which you can retrieve by sending the request

`GET /api/v2/statements/handle?partition=1`.

The third object describes the third partition of data, which contains 43746 rows and which you can retrieve by sending the request

`GET /api/v2/statements/handle?partition=2`.

## Getting the data from the results

In the `ResultSet` object in the response, the results are in the `data` field. The `data` field
contains an array of an array of strings in JSON. For example:

Copy code

```
{
  ...
  "data": [
    ["customer1", "1234 A Avenue", "98765", "2021-01-20 12:34:56.03459878"],
    ["customer2", "987 B Street", "98765", "2020-05-31 01:15:43.765432134"],
    ["customer3", "8777 C Blvd", "98765", "2019-07-01 23:12:55.123467865"],
    ["customer4", "64646 D Circle", "98765", "2021-08-03 13:43:23.0"]
  ],
  ...
}
```

Each array within the array contains the data for a row. The elements in each array represent the data in a row.

The data in the result set is encoded in JSON expressed as strings, regardless of the Snowflake data type of the column.

For example, the value `1.0` in a `NUMBER` column is returned as the string `"1.0"`. As another example, timestamps
are returned as the number of nanoseconds since the epoch. For example, the timestamp for Thursday, January 28, 2021
10:09:37.123456789 PM is returned as `"1611871777123456789"`.

You are responsible for converting the strings to the appropriate data types.

Snowflake returns the values as strings in the following formats (if no
[output format parameter](#label-sql-api-output-format) is specified in the POST submit statement request), depending on the
[Snowflake data type](/sql-reference-data-types):

> INT / NUMBER:
> :   Decimal number in a string.
>
> FLOAT:
> :   Integer or float in a string.
>
> DECFLOAT:
> :   Integer or float in a string. If the number of significant digits is less than or equal to 38, the value is returned in plain format. Otherwise, the value is returned in scientific notation.
>
> VARCHAR:
> :   String.
>
> BINARY:
> :   Hexadecimal number in a string.
>
> BOOLEAN:
> :   “false” or “true” in a string.
>
> DATE:
> :   Integer value (in a string) of the number of days since the epoch (e.g. `18262`).
>
> TIME, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ:
> :   Float value (with 9 decimal places) of the number of seconds since the epoch (e.g.
>     `82919.000000000`).
>
> TIMESTAMP\_TZ:
> :   Float value (with 9 decimal places) of the number of seconds since the epoch, followed by a space and the timezone offset in minutes (for example, `1616173619.000000000 1500`). The offset value is a positive integer ranging from 720 (-12) to 2160 (+12), so `timezone_in_minutes = offset - 1440`. To calculate the timezone, you must subtract 1440 from the offset value (1500, in this example), which equals +60 minutes for a +0100 timezone.

## Retrieving additional partitions

The Snowflake SQL API returns data in partitions. The first partition is returned in JSON format and contains metadata about all of the partitions returned for a specific query. Your application can use this partition metadata to determine how to handle the partitions returned for subsequent requests.

After receiving the response containing the first partition of data, you can get the rest of the partitions by submitting requests with `partition=partition_number`, where `partition_number` identifies the partition of data to return. The partition number `0` identifies the first partition of data, which is returned in the initial request.

For example, after receiving the first partition of data, you can get the second partition of data by submitting a request with the partition parameter set to `1`:

Copy code

```
GET /api/v2/statements/<handle>?partition=1
```

In the response for a `GET /api/v2/statements/<handle>?partition=partition_number` request, the body contains JSON data in compressed form (using gzip).

The response includes the HTTP header `Content-Encoding: gzip`, which indicates that the body of the response is compressed.

These responses do not contain any metadata. Metadata for all partitions is provided in the first partition.

## Returning SQL NULL values as strings

By default, SQL NULL values are returned as the value `null`:

Copy code

```
"data" : [ [ null ], ... ]
```

If you want these values returned as the string `"null"` instead, set the `nullable` query parameter to `false`
in the [POST request to submit the SQL statement for execution](/developer-guide/sql-api/submitting-requests). For example:

Copy code

```
POST /api/v2/statements?nullable=false
```

This returns SQL NULL values as `"null"`:

Copy code

```
"data" : [ [ "null" ], ... ]
```

Note

You cannot specify the `nullable` parameter in
[GET requests to check the statement status](#label-sql-api-checking-statement-status).

## Formatting the output of query results

The Snowflake SQL API supports parameters for formatting output (e.g. [Session parameters for dates, times, and timestamps](/sql-reference/date-time-input-output#label-session-parameters-for-dates-times-timestamps)).

For example, by default, a DATE value like 2019-03-27 is returned as “17982” (2019-03-27 is 17982 days after the epoch). If you specify that the DATE\_OUTPUT\_FORMAT should be “MM/DD/YY” in the request:

Copy code

```
{
  "statement": "select date_column from mytable",
  "resultSetMetaData": {
    "format": "jsonv2",
  },
  "parameters": {
    "DATE_OUTPUT_FORMAT": "MM/DD/YYYY"
  }
  ...
}
```

The DATE value is returned as “03/27/2019”.

In the `parameters` field in the body of the request, you can set the following parameters that determine the output format of
the data:

- BINARY\_OUTPUT\_FORMAT
- DATE\_OUTPUT\_FORMAT
- TIME\_OUTPUT\_FORMAT
- TIMESTAMP\_LTZ\_OUTPUT\_FORMAT
- TIMESTAMP\_NTZ\_OUTPUT\_FORMAT
- TIMESTAMP\_TZ\_OUTPUT\_FORMAT
- TIMESTAMP\_OUTPUT\_FORMAT
- TIMEZONE

Note

Snowflake ignores the account-level and user-level settings for these parameters. In order to change the format of the values in SQL API results, you must set these output parameters in the body of the request.

## Including row numbers in the `resultSet` object

Row numbers are not returned in the result set. To include row numbers in the response, call the SEQUENCE or ROW\_NUMBER window function in your query to generate the row numbers.
