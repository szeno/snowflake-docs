# Remote service input and output data formats

When Snowflake sends data to a remote service, or receives data from a remote
service, the data must be formatted correctly. This topic provides information
about the proper data formats. Data received from and returned to Snowflake must
also be of an [appropriate data type](/sql-reference/external-functions-best-practices#label-external-functions-general-ensure-arguments-correspond).

When executing an external function, for example, Snowflake sends and expects data in the
format described here. It sends the data to a proxy service, not directly to the
remote service (for more, see [Introduction to external functions](/sql-reference/external-functions-introduction)). Therefore, the proxy service must receive
(and return) data in a Snowflake-compatible format. Although
typically the proxy service passes data through unchanged, the proxy can reformat data (both
sending and receiving) to meet the needs of both the remote service and Snowflake.

For simplicity, and to help illustrate the formats that Snowflake expects to send and receive, most of the examples
in this section assume that the remote service reads and writes data in the same format as Snowflake expects, and
the proxy service passes data through unchanged in both directions.

## Data format sent by Snowflake

Each HTTP request from Snowflake is a POST or a GET.

- A POST request contains headers and a request body. The request body
  includes a [batch](/sql-reference/external-functions-introduction#label-external-functions-introduction-miniglossary-batch) of rows.
- A GET contains only headers, and is used only for polling when the remote
  service returns results [asynchronously](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous).

### Body format

The body of the POST request contains the data, serialized in JSON format.

The schema for the JSON is:

- The top-level is a JSON object (a set of name/value pairs, also called a “dictionary”).
- Currently, there is exactly one item in that object; the key for that item is named “data”.
- That “data” item’s value is a JSON array, in which:

  - Each element is one row of data.
  - Each row of data is a JSON array of one or more columns.
  - The first column is always the row number (i.e. the 0-based index of the row within the batch).
  - The remaining columns contain the arguments to the function.
- Data types are serialized as follows:

  - Numbers are serialized as JSON numbers.
  - Booleans are serialized as JSON booleans.
  - Strings are serialized as JSON strings.
  - Objects are serialized as JSON objects.
  - All other supported data types are serialized as JSON strings.

    - Dates, times, and timestamps are serialized as strings. For details about formatting these data types as
      strings, see [Date and time input and output formats](/sql-reference/date-time-input-output) and [Date and time formats in conversion functions](/sql-reference/functions-conversion#label-date-time-format-conversion).
    - Binary columns are serialized as strings. For details, see
      [Overview of supported binary formats](/sql-reference/binary-input-output#label-overview-of-supported-binary-formats).
  - NULL is serialized as JSON null.

For examples of extracting data in a remote service on each platform, see:

- AWS: [Create the Remote Service (Lambda Function on AWS)](/sql-reference/external-functions-creating-aws-ui-remote-service#label-external-functions-creating-aws-create-remote-service) .
- Azure: [Create the Remote Service (Azure Function)](/sql-reference/external-functions-creating-azure-ui-remote-service#label-external-functions-creating-azure-create-remote-service) .

Optionally, the JSON can be compressed for transmission over the network. Compression is
documented in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

#### Body example

Here’s an example of a serialized request for an external function with the signature
`f(integer, varchar, timestamp)`. The first column is the row number within the batch, and the
next three values are the arguments to the external function.

> Copy code
>
> ```
> {
>     "data": [
>                 [0, 10, "Alex", "2014-01-01 16:00:00"],
>                 [1, 20, "Steve", "2015-01-01 16:00:00"],
>                 [2, 30, "Alice", "2016-01-01 16:00:00"],
>                 [3, 40, "Adrian", "2017-01-01 16:00:00"]
>             ]
> }
> ```

### Header format

The header information is generally available to the remote service as a set of
key/value pairs. The header information includes:

- The following HTTP headers:

  - Headers that describe how data is serialized in the request body:

    - “sf-external-function-format”: This is currently always set to “json”.
    - “sf-external-function-format-version”: This is currently always set to “1.0”.
  - “sf-external-function-current-query-id”: This contains the query ID of the query that called this external
    function. You can use this to correlate Snowflake queries to calls of the remote service, for example to help
    debug issues.
  - “sf-external-function-query-batch-id”: The batch ID uniquely identifies the specific batch of
    rows processed with this request. The remote service can use this ID to track the status of a batch that is being
    processed. The ID can also be used as an idempotency token if requests are retried due to an error.
    The ID can also be used for logging/tracing of requests by the remote service.

    The batch ID in a GET is the same as the batch ID in the corresponding POST.

    The batch ID is an opaque value generated by Snowflake. The format could change in future releases, so remote
    services should not rely on a specific format or try to interpret the value.
  - Headers that describe the signature (name and argument types) and return type of the external function that
    was called in the SQL query. These values can have characters that are not standard characters for Snowflake
    [identifiers](/sql-reference/identifiers-syntax), so base64 versions of the information are included,
    and non-standard characters are replaced with a blank in the non-base64 versions.

    The specific headers are:

    - sf-external-function-name
    - sf-external-function-name-base64
    - sf-external-function-signature
    - sf-external-function-signature-base64
    - sf-external-function-return-type
    - sf-external-function-return-type-base64

    For example, the headers sent for the function `ext_func(n integer) returns varchar` are:

    - sf-external-function-name: ext\_func
    - sf-external-function-name-base64: <base64 value>
    - sf-external-function-signature: (N NUMBER)
    - sf-external-function-signature-base64: <base64 value>
    - sf-external-function-return-type: VARCHAR(134217728)
    - sf-external-function-return-type-base64: <base64 value>

    Because SQL INTEGER values are treated as SQL NUMBER, the SQL argument declared as type `INTEGER` is
    described as type `NUMBER`.
- Additional optional metadata described in the “headers” and “context\_headers” properties of
  [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

#### Header access example

To extract the “sf-external-function-signature” header from inside an AWS Lambda function written in
Python, which receives the headers as a Python dictionary, execute the following:

> Copy code
>
> ```
> def handler(event, context):
>
>     request_headers = event["headers"]
>     signature = request_headers["sf-external-function-signature"]
> ```

The details will be different for other languages and on other cloud platforms.

For remote services developed on AWS, more information about headers and lambda proxy integration is available in
the [AWS API Gateway documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format) .

## Data format received by Snowflake

### Body format

When a remote service finishes processing a batch, the remote service should
send data back to Snowflake in a JSON format similar to the format of the data
sent by Snowflake.

The JSON response returned to Snowflake should contain one row for each row sent by Snowflake. Each returned row
contains two values:

- The row number (i.e. the 0-based index of the row within the batch).
- The value returned from the function for that row. The value can be a compound value (for example, an OBJECT), but
  it must be exactly one value because all scalar Snowflake functions (external or otherwise) return a single value.

So that Snowflake can correlate the response with the request, the row numbers in the returned data
must correspond to the row numbers in the data that Snowflake sent and must be
returned in the same order as they were received.

#### Body access example

The following JSON example shows two rows containing an OBJECT value, each
preceded by a row number:

Copy code

```
{
    "data":
        [
            [ 0, { "City" : "Warsaw",  "latitude" : 52.23, "longitude" :  21.01 } ],
            [ 1, { "City" : "Toronto", "latitude" : 43.65, "longitude" : -79.38 } ]
        ]
}
```

To compose one of these returned rows with Python, you might use the following code:

Copy code

```
...
row_number = 0
output_value = {}

output_value["city"] = "Warsaw"
output_value["latitude"] = 21.01
output_value["longitude"] = 52.23
row_to_return = [row_number, output_value]
...
```

To access the OBJECT value of a returned row with SQL, use the notation described in
[Traversing Semi-structured Data](/user-guide/querying-semistructured#label-traversing-semistructured-data). For example:

Copy code

```
select val:city, val:latitude, val:longitude
    from (select ext_func_city_lat_long(city_name) as val from table_of_city_names);
```

### Header format

The response can also contain the following optional HTTP headers:

- Content-MD5: Snowflake uses the optional Content-MD5 header to check the integrity of the response. If this header
  is included in the response, Snowflake computes an MD5 checksum on the response body to ensure that it matches
  the corresponding checksum in the returned header. If the values do not match, the SQL query fails. The checksum
  should be encoded in a base64 representation before being returned in the header. See the example code below.

Optionally, the JSON can be compressed for transmission over the network. Compression is
documented in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

For information about timeouts and retries, see [Account for timeout errors](/sql-reference/external-functions-best-practices#label-external-function-timeouts) and
[Do not assume that the remote service is passed each row exactly once](/sql-reference/external-functions-best-practices#label-external-function-retries).

### Status code

The response also contains an HTTP status code. Snowflake recognizes the following HTTP status codes:

| Code | Description |
| --- | --- |
| 200 | Batch processed successfully. |
| 202 | Batch received and still being processed. |

Expand

Show lessSee more

Other values are treated as errors.

### Response creation example

The example Python code below returns a proper response, including the HTTP response code, the processed data, and an
MD5 header (which is optional).

This example is based on an AWS Lambda function. Some code might need customization for different platforms.

Copy code

```
import json
import hashlib
import base64

def handler(event, context):

    # The return value should contain an array of arrays (one inner array
    # per input row for a scalar function).
    array_of_rows_to_return = [ ]

    ...

    json_compatible_string_to_return = json.dumps({"data" : array_of_rows_to_return})

    # Calculate MD5 checksum for the response
    md5digest = hashlib.md5(json_compatible_string_to_return.encode('utf-8')).digest()
    response_headers = {
        'Content-MD5' : base64.b64encode(md5digest)
    }

    # Return the HTTP status code, the processed data, and the headers
    # (including the Content-MD5 header).
    return {
        'statusCode': 200,
        'body': json_compatible_string_to_return,
        'headers': response_headers
    }
```
