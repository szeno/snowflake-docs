# Submitting a request to execute SQL statements

This topic explains how to submit a request to the SQL API.

To submit SQL statements for execution, send a `POST` request to the `/api/v2/statements/` endpoint. See
[Operations](/developer-guide/sql-api/reference#label-sql-api-reference-post-statements) for details.

Copy code

```
POST /api/v2/statements HTTP/1.1
(request body)
```

## Setting up the request

In the request URL, you can set query parameters to:

- [Specify a request ID that distinguishes this request from other requests](#label-sql-api-generating-request-id).
- Execute the statement asynchronously.

Note

Your code must be able to handle async query executions. It is not guaranteed that your query will always be executed synchronously if you don’t specify the explicit `async=true` property. For more information, see the [response workflow](/developer-guide/sql-api/handling-responses#label-sql-api-checking-statement-status-responses).

For the [body of the request](/developer-guide/sql-api/reference#label-sql-api-reference-post-statements-request-body), set the following fields:

- Set the `statement` field to the SQL statement that you want to execute. For example:

  Copy code

  ```
  {
    "statement": "select * from my_table",
    ...
  }
  ```

  If you want to submit multiple statements in a single request, use a semicolon (`;`) between statements.
  See [Submitting multiple SQL statements in a single request](/developer-guide/sql-api/submitting-multiple-statements) for details.
- If you include bind variables (`?` placeholders) in the statement, set the `bindings` field to an object that specifies
  the corresponding Snowflake data types and values for each variable.

  For details, see [Using bind variables in a statement](#label-sql-api-bind-variables).
- To specify the warehouse, database, schema, and role to use, set the `warehouse`, `database`, `schema`, and
  `role` fields.

  The values in these fields are case-sensitive and must match the case of the field returned by a SQL SHOW command.
  For example, suppose you create a database using the following SQL command:

  Copy code

  ```
  CREATE OR REPLACE DATABASE Xpto;
  ```

  In this example, [the object identifier is not quoted, so it will be created with uppercase by default](/sql-reference/identifiers-syntax).

  If the [SHOW DATABASES](/sql-reference/sql/show-databases) command returns `XPTO` in uppercase for the name of the database, you must specify `XPTO` in uppercase for the field value.

  If you omit these fields, the SQL API uses the values of the corresponding properties for the user (i.e. the
  `DEFAULT_WAREHOUSE`, `DEFAULT_NAMESPACE`, and `DEFAULT_ROLE`
  [properties of the user](/sql-reference/sql/alter-user)).
- To set a timeout for the statement execution, set the `timeout` field to the maximum number of seconds to wait.
  If the `timeout` field is not set, the timeout specified by the [STATEMENT\_TIMEOUT\_IN\_SECONDS](/sql-reference/parameters#label-statement-timeout-in-seconds) parameter is
  used.

## Example of a request

For example, the following `curl` command sends a SQL statement for execution. The example uses the file
`request-body.json` to specify the body of the request.

Copy code

```
curl -i -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <jwt>" \
    -H "Accept: application/json" \
    -H "User-Agent: myApplicationName/1.0" \
    -d "@request-body.json" \
    "https://<account_identifier>.snowflakecomputing.com/api/v2/statements"
```

where:

- `jwt` is the [JWT that you generated for authentication](/developer-guide/sql-api/authenticating#label-sql-api-authenticating-key-pair).
- `myApplicationName` is an example of an identifier for your application.
- `account_identifier` is your [account identifier](/user-guide/admin-account-identifier).

In this example, `request-body.json` contains the
[body of the request](/developer-guide/sql-api/reference#label-sql-api-reference-post-statements-request-body):

Copy code

```
{
  "statement": "select * from T where c1=?",
  "timeout": 60,
  "database": "TESTDB",
  "schema": "TESTSCHEMA",
  "warehouse": "TESTWH",
  "role": "TESTROLE",
  "bindings": {
    "1": {
      "type": "FIXED",
      "value": "123"
    }
  }
}
```

In the body of the request in the example above:

- The `statement` field specifies the SQL statement to execute.

  The statement includes a [bind variable](#label-sql-api-bind-variables) (the question mark in `"cl=?"`), which
  evaluates to the first binding (`"1"`) specified in the `bindings` field.
- The `timeout` field specifies that the server allows 60 seconds for the statement to be executed.
- The `database`, `schema`, `warehouse`, and `role` fields specify that the `TESTDB` database,
  `TESTSCHEMA` schema, `TESTWH` warehouse, and `TESTROLE` role should be used when executing the statement.

## Using bind variables in a statement

If you want to use bind variables (`?` placeholders) in the statement, use the `bindings` field to specify the values that
should be inserted.

Set this field to a JSON object that specifies the [Snowflake data type](/sql-reference/intro-summary-data-types) and value
for each bind variable.

Copy code

```
...
"statement": "select * from T where c1=?",
...
"bindings": {
  "1": {
    "type": "FIXED",
    "value": "123"
  }
},
...
```

Choose the binding type that corresponds to the type of the value that you are binding. For example, if the value is a
string representing a date (e.g. `2021-04-15`) and you want to insert the value into a DATE column, use the
`TEXT` binding type.

The following table specifies the values of the `type` field that you can use to bind to different
[Snowflake data types](/sql-reference-data-types).

- The first column on the left specifies the binding types that you can use.
- The rest of the columns specify the Snowflake data type of the column where you plan to insert the data.
- Each cell specifies the type of value that you can use with a binding type to insert data into a column of a particular
  Snowflake data type.

  If the cell for a binding type and Snowflake data type is empty, you cannot use the specified binding type to insert data into
  a column of that Snowflake data type.

**Binding types supported for different Snowflake data types**

| Snowflake Data Types | INT / NUMBER | FLOAT | DECFLOAT | VARCHAR | BINARY | BOOLEAN | DATE | TIME | TIMESTAMP\_TZ | TIMESTAMP\_LTZ | TIMESTAMP\_NTZ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Binding Types |  |  |  |  |  |  |  |  |  |  |  |
| FIXED | integer | integer | integer | integer |  | 0 (false) / nonzero (true) |  |  |  |  |  |
| REAL | integer | int or float | int or float | int or float |  | 0/non-0 |  |  |  |  |  |
| DECFLOAT | integer | int or float | int or float (see notes below) | int or float |  | 0/non-0 |  |  |  |  |  |
| TEXT | integer | int or float | int or float (see notes below) | any text | hexdec | `"true"`/ `"false"` | see notes below | see notes below | see notes below | see notes below | see notes below |
| BINARY |  |  |  | hexdec |  |  |  |  |  |  |  |
| BOOLEAN |  |  |  | true/false, 0/1 |  | true/false |  |  |  |  |  |
| DATE |  |  |  | epoch (ms) |  |  | epoch (ms) |  | epoch (ms) | epoch (ms) | epoch (ms) |
| TIME |  |  |  | epoch (nano) |  |  |  | epoch (nano) |  |  |  |
| TIMESTAMP\_TZ |  |  |  | epoch (nano) |  |  | epoch (nano) | epoch (nano) | epoch (nano) |  |  |
| TIMESTAMP\_LTZ |  |  |  | epoch (nano) |  |  | epoch (nano) | epoch (nano) | epoch (nano) | epoch (nano) | epoch (nano) |
| TIMESTAMP\_NTZ |  |  |  | epoch (nano) |  |  | epoch (nano) | epoch (nano) | epoch (nano) | epoch (nano) | epoch (nano) |

Expand

Show lessSee more

Note the following:

- The values of the bind variables must be strings (e.g. `"1.0"` for the value 1.0).
- When using the DECFLOAT or TEXT binding type, to insert data into a DECFLOAT column, you can specify the value in scientific notation (e.g. `"1.23e-40"`).
- When using the DATE binding type, specify the number of milliseconds since the epoch.
- When using the TIME or TIMESTAMP\* binding type, specify the number of nanoseconds since the epoch.
- When using the TIMESTAMP\_TZ binding type, specify the number of nanoseconds since the epoch followed by a space and the
  timezone offset in minutes (e.g. `1616173619000000000 960`).
- When using the `TEXT` binding type:
  - To insert data into a DATE column, you can use any [date format](/sql-reference/date-time-input-output#label-date-time-input-output-date-formats) that is
    supported by AUTO detection.
  - To insert data into a TIME column, you can use any [time format](/sql-reference/date-time-input-output#label-time-formats) that is supported by AUTO
    detection.
  - To insert data into a TIMEZONE\* column, you can use any
    [date-time format](/sql-reference/date-time-input-output#label-date-time-input-output-timestamp-formats) that is supported by AUTO detection.

If the value is in a format not supported by Snowflake, the API returns an error:

Copy code

```
{
  code: "100037",
  message: "<bind type> value '<value>' is not recognized",
  sqlState: "22018",
  statementHandle: "<ID>"
}
```

Note

Snowflake does not currently support variable binding in multi-statement SQL requests.

## Submitting concurrent requests

The Snowflake SQL API supports sending concurrent requests to the server. Concurrency limits on the API are determined by the concurrency limits enforced by Snowflake.

Depending on the current server load, you might receive an HTTP 429 error which indicates that the server is currently
receiving too many requests.

To ensure that your application correctly handles 429 errors, wrap concurrent requests within retry logic.

## Resubmitting a request to execute SQL statements

In some cases, it might not be clear if Snowflake executed the SQL statement in an API request (e.g. due to a network error or a
timeout). You might choose to resubmit the same request to Snowflake again, in case Snowflake did not execute the statement.

However, if Snowflake already executed the statement in the initial request and you resubmit the request again, the statement is
executed twice. For some types of requests, repeatedly executing the same statement can have unintended consequences (e.g.
inserting duplicate data into a table).

To prevent Snowflake from executing the same statement twice when you resubmit a request, you can use a request ID to distinguish
your request from other requests. If you specify the same request ID in the initial request along with the `retry=true` parameter in the resubmitted request, Snowflake does not execute the statement again if the statement has already been executed successfully.

To specify a request ID, generate a
[universally unique identifier (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier). You can then include this identifier in the `requestId` query parameter. You must also specify the `retry=true` parameter as part of the request as shown in the following example.

Copy code

```
POST /api/v2/statements?requestId=ea7b46ed-bdc1-8c32-d593-764fcad64e83&retry=true HTTP/1.1
```

If Snowflake fails to process a request, you can submit the same request again with the same request ID. Using the same request ID
indicates to the server that you are submitting the same request again.

Note

The `retry=true` parameter adds overhead to processing the SQL statement because Snowflake must scan and match a
statement in the statement history. Use this parameter only when retrying the statement is required.
