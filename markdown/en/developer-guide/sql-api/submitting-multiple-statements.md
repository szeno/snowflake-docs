# Submitting multiple SQL statements in a single request

This topic explains how to submit a request containing multiple statements to the Snowflake SQL API.

Note

Executing multiple statements in a single query requires that a valid warehouse is available in a session.

## Introduction

In some cases, you might need to specify multiple SQL statements in a request. For example, you might need to:

- Define an explicit transaction
- Set and use session variables in statements in a request
- Create and use temporary tables in statements in a request
- Change the database, schema, warehouse, or role for statements in a request

The following sections explain how to submit a request that contains multiple SQL statements.

- [Specifying multiple SQL statements in the request](#label-sql-api-executing-multiple-statements-setting)
- [Getting the results for each SQL statement in the request](#label-sql-api-checking-multiple-statement-status)
- [Handling errors when specifying multiple statements in a request](#label-sql-api-handling-multiple-statement-errors)

## Specifying multiple SQL statements in the request

To submit multiple SQL statements in a single request:

- In the `statement` field, use a semicolon (`;`) between each statement.
- In the `parameters` field, set the `MULTI_STATEMENT_COUNT` field to the number of SQL statements in the request.

For example:

Copy code

```
POST /api/v2/statements HTTP/1.1
Authorization: Bearer <jwt>
Content-Type: application/json
Accept: application/json
User-Agent: myApplication/1.0

{
  "statement": "alter session set QUERY_TAG='mytesttag'; select count(*) from mytable",
  ...
  "parameters": {
      "MULTI_STATEMENT_COUNT": "2"
  }
}
```

In this example `MULTI_STATEMENT_COUNT` is set to `2` which corresponds to the number of SQL statements being submitted.

To submit a variable number of SQL statements in the `statement` field, set `MULTI_STATEMENT_COUNT` to
`0`. This is useful in an application where the number of SQL statements submitted is not known at runtime.

If the value of `MULTI_STATEMENT_COUNT` does not match the number of SQL statements specified in the
`statement` field, the SQL API returns the following error:

Copy code

```
Actual statement count <actual_count> did not match the desired statement count <desired_count>.
```

Where

- `actual_count` is the number of statements specified in the `statement` field.
- `desired_count` is the value of `MULTI_STATEMENT_COUNT`.

If you specify multiple SQL statements in the `statement` field, but do not specify the
`MULTI_STATEMENT_COUNT` field, the SQL API returns the following error:

> Copy code
>
> ```
> Actual statement count 3 did not match the desired statement count 1.
> ```

Note

Snowflake does not currently support variable binding in multi-statement SQL requests.

## Getting the results for each SQL statement in the request

If a request that contains multiple SQL statements is processed successfully, the response does not include the data returned from
executing the individual statements. Instead, the response contains a `statementHandles` field that contains an array of the
handles for the individual statements.

Note

The `statementHandles` field is different from the `statementHandle` field:

- The `statementHandle` field specifies the handle for the set of SQL statements in the request.
- The `statementHandles` field is an array of the handles of the individual SQL statements in the request.

For example, suppose that you send a request that specifies two SQL statements for execution:

Copy code

```
POST /api/v2/statements HTTP/1.1
Authorization: Bearer <jwt>
Content-Type: application/json
Accept: application/json
User-Agent: myApplication/1.0

{
  "statement": "select * from A; select * from B",
  ...
}
```

The response contains a `statementHandles` field that contains an array of the handles for the individual statements.

Copy code

```
HTTP/1.1 200 OK
...
{
  ...
  "statementHandles" : [ "019c9fce-0502-f1fc-0000-438300e02412", "019c9fce-0502-f1fc-0000-438300e02416" ],
  ...
}
```

To check the status and retrieve the data for the individual statements, send a `GET` request to the
`/api/v2/statements/` endpoint and append the handle for each statement to the URL path. See
[Checking the status of the statement execution and retrieving the data](/developer-guide/sql-api/handling-responses#label-sql-api-checking-statement-status) for details.

Copy code

```
GET /api/v2/statements/019c9fce-0502-f1fc-0000-438300e02412
...
```

Copy code

```
GET /api/v2/statements/019c9fce-0502-f1fc-0000-438300e02416
...
```

## Handling errors when specifying multiple statements in a request

If you specified multiple SQL statements in the request and an error occurred when executing any of the statements, Snowflake
returns the HTTP response code 422 with a [QueryFailureStatus](/developer-guide/sql-api/reference#label-sql-api-reference-queryfailurestatus) object.

You can get [details about the error](/developer-guide/sql-api/handling-errors) from this object.

For example, suppose that your request specifies the following statements in which the second INSERT statement contains an error:

Copy code

```
{
  "statement": "create or replace table table1 (i int); insert into table1 (i) values (1); insert into table1 (i) values ('This is not a valid integer.'); insert into table1 (i) values (2); select i from table1 order by i",
  ...
}
```

Snowflake returns a response with the HTTP response code 422 and with a `QueryFailureStatus` object that contains the
details about the error:

Copy code

```
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json
...
{
  "code" : "100132",
  "message" : "JavaScript execution error: Uncaught Execution of multiple statements failed on statement \"insert into table1 (i) values ...\" (at line 1, position 75).\nDML operation to table TABLE1 failed on column I with error: Numeric value 'This is not a valid integer.' is not recognized in SYSTEM$MULTISTMT at '    throw `Execution of multiple statements failed on statement {0} (at line {1}, position {2}).`.replace('{1}', LINES[i])' position 4\nstackstrace: \nSYSTEM$MULTISTMT line: 10",
  "sqlState" : "P0000",
  "statementHandle" : "019d6e97-0502-317e-0000-096d0041f036"
}
```

In the example above, the INSERT statement with the error starts at the character position 75 in the value of the
`statement` field.

The statements before the statement with the error are executed successfully (the CREATE TABLE and first INSERT statement in this
example). The statements after the statement with the error are not executed.
