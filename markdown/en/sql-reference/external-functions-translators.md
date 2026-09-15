# Using request and response translators with data for a remote service

With request and response translators, you can change the format of data sent to, and received from, remote services used by
external functions.

## Purpose

When Snowflake sends data to a remote service, Snowflake formats the data according to
[these rules](/sql-reference/external-functions-data-format#label-external-functions-data-format). Similarly, when Snowflake receives data from a remote service,
Snowflake expects the data to be formatted according to the same rules.

Many remote services expect to handle data in a different format. With request and response translators, you can conveniently:

- Convert data from Snowflake’s format to the remote service’s native input format (*request translator*).
- Convert data from the remote service’s native output format to Snowflake’s format (*response translator*).

## SQL implementation

To translate data between Snowflake’s format and the remote service’s native input format, you use JavaScript [UDFs](/developer-guide/udf/udf-overview)
(user-defined functions). You almost always write a pair of UDFs: one to translate the request and one to translate the response.

Snowflake calls these functions as part of each external function call. For example, for a request to a remote service, Snowflake calls the request translator function,
passes it the Snowflake-formatted data, then takes the returned data and sends it to the remote service. When the
remote service returns data, Snowflake calls the response translator function to convert the data back to the format that Snowflake
understands.

From the user perspective, calling an external function when a translator is converting is the same as calling an
external function without a translator. After you specify translators as part of the
[CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) statement, they are called automatically.

An external function can have a maximum of one request translator and one response translator at a time.

The request and response translator UDFs can be [secure UDFs](/developer-guide/secure-udf-procedure).

### Assigning a translator function to an external function

To specify which user-defined function to use as a translator, include `REQUEST_TRANSLATOR` and `RESPONSE_TRANSLATOR`
clauses in the `CREATE EXTERNAL FUNCTION` statement. Each takes the name of the
translator function to use at run time.

For example:

> Copy code
>
> ```
> CREATE EXTERNAL FUNCTION f(...)
>     RETURNS OBJECT
>     ...
>     REQUEST_TRANSLATOR = my_request_translator_udf
>     RESPONSE_TRANSLATOR = my_response_translator_udf
>     ...
>     AS <url_of_proxy_and_resource>;
> ```

The syntax for specifying translators as part of a `CREATE EXTERNAL FUNCTION` statement is shown below:

> Copy code
>
> ```
> CREATE EXTERNAL FUNCTION f(...)
>     RETURNS OBJECT
>     ...
>     [ REQUEST_TRANSLATOR = <request_translator_udf_name> ]
>     [ RESPONSE_TRANSLATOR = <response_translator_udf_name> ]
>     ...
> ```
>
> where:
>
> > `request_translator_udf_name`
> > :   The name of the request translator function.
> >
> > `response_translator_udf_name`
> > :   The name of the response translator function.

The `REQUEST_TRANSLATOR` and `RESPONSE_TRANSLATOR` parameters each take one parameter of type [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).

You can also specify a request or response translator in an [ALTER FUNCTION](/sql-reference/sql/alter-function) command. You can:

- Add a translator if the external function does not already have one.
- Replace an existing translator.
- Remove a translator.

Use the `SET` keyword to add a new translator or to replace an existing translator.

To add or replace a translator:

> Copy code
>
> ```
> ALTER FUNCTION ...
>     SET [REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR] = <udf_name>;
> ```
>
> where
>
> > `udf_name`
> > :   The name of a previously-created JavaScript UDF.

To remove a translator:

> Copy code
>
> ```
> ALTER FUNCTION ...
>     UNSET [REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR];
> ```

### Requirements for the SQL

- The name of the translator function in the `CREATE EXTERNAL FUNCTION` or `ALTER FUNCTION` statement should
  be either:

  - A qualified name (e.g. MyDatabase.MySchema.MyJavaScriptUDF).
  - Defined in the same database and schema as the external function that uses them.
- When the translator is specified in a `CREATE EXTERNAL FUNCTION` or `ALTER FUNCTION` statement, the
  translator UDF must already exist. You can’t specify the name first and create the UDF later – even if you
  don’t call the external function before you create the UDF.
- A UDF used as a translator should not be dropped without first removing it from all external
  functions that use it. (At the time the external function is called, Snowflake fails with an error if the translator does not exist.)
- If the translator UDF is modified (via `ALTER FUNCTION`), it must retain the same interface requirements.
  If it does not retain the interface requirements, an exception is raised before running the external function.

## JavaScript implementation

At run time, SQL passes an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) to the translator UDF. The JavaScript code receives this as a
JavaScript object.

### Implementing a request translator

#### Request translator input properties

A translator UDF receives a JavaScript object named `event`. The object contains the following properties:

- `body`: The format of the `data` field is the same as the existing Snowflake rowset batch (i.e. an array of rows).

  For example,

  Copy code

  ```
  {
    "body": {
         "data": [
                   [0,"cat"],
                   [1,"dog"]
                 ]
         }
  }
  ```

  The existing data is nested under the outer body.
- `serviceUrl`: The external function’s defined URL to call.
- `contextHeaders`: An object that contains all the context-related headers, where the names
  are the field names. For example, the object could contain the field name “SF\_CONTEXT\_CURRENT\_DATABASE”, and the corresponding
  value would be a string containing the current database name.

#### Request translator output properties

The request translator returns an object with fields used to communicate with the external service API gateway. That object has three
optional fields:

- `body`: Defines the actual body to be passed to the service. If this is not defined, there is no body.
  The `body` value should be a string or a JSON object in the format that the remote service expects. If the value is a
  string, that string can contain internal structure (e.g. be JSON-compatible). If the value is a JSON object, that object is
  converted to a string so that it can be included as part of the HTTP POST command string.
- `urlSuffix`: Sets the suffix of the service URL, which is added to the end of the `serviceUrl` value. This suffix
  is also allowed to contain query parameters. Parameter names and values must be URL encoded. For example, if you want to set a parameter named `a`
  to value `my param` you need to do URL encoding of the space character, so the parameter would be `?a=my%20param`.
- `translatorData`: Passed from the request translator to the response translator. This field can pass context information, such as
  the input body, the service URL or suffix, or context headers.

All three fields are optional. However, as a practical matter, most request translators return at least the body data.

### Implementing a response translator

#### Response translator input properties

The input parameter for the response translator function is an object. The example below uses `EVENT`, which contains two properties:

- `body`: The response to be decoded from the external service response.
- `translatorData`: If this field is returned by the request translator, then Snowflake passes it to the response translator.

#### Response translator output properties

The response translator response is returned as an object under the `body` element; the format is the existing
external function format (array of rows). For example:

> Copy code
>
> ```
> {
>   "body": {
>           "data": [
>                     [0, "Life"],
>                     [1, "the universe"],
>                     [2, "and everything"]
>                   ]
>            }
> }
> ```

### Requirements for the translator function

Each translator UDF must meet the following requirements:

- It must be a [JavaScript UDF](/developer-guide/udf/javascript/udf-javascript-introduction).
- It must take exactly one parameter of type [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object), which represents a batch of rows.
- It must return one value of type OBJECT, which also represents a batch of rows.
- It must be a scalar UDF (returning one row for each row (OBJECT) passed in).

  Note

  Although the translator is scalar, the OBJECT passed to the translator can (and
  usually does) have multiple rows embedded inside the JSON in the OBJECT.
- The number and order of the rows (inside the OBJECT) returned by the response translator UDF must be the same as the number and
  order of the rows passed to the request translator UDF (inside the OBJECT).

## Example request translator and response translator

The following example shows a request translator and response translator being used to
convert data into the format required by an external service that does
sentiment analysis, [Amazon Comprehend BatchDetectSentiment](https://docs.aws.amazon.com/comprehend/latest/dg/API_BatchDetectSentiment.html).
The request translator shapes the HTTP request to match the format that
the backend service expects.

To use translators, you’ll need an API gateway. This example uses
an API gateway that is already configured to talk to the sentiment
analysis service. For more information about how to integrate with an Amazon Web Services (AWS) service as the backend, see [Set up an API integration request using
the API Gateway
console](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-method-settings-console.html)
in the AWS documentation.

It is helpful to get your API integration working successfully before
adding translators.

### Setup

Set up a database to hold demo data.

Choose a role that has permission to create external functions:

Copy code

```
USE ROLE ACCOUNTADMIN;
```

Specify which warehouse, database and schema to use:

Copy code

```
USE WAREHOUSE w;
USE DATABASE a;
USE SCHEMA b;
```

Create a table to hold your test sentences:

Copy code

```
CREATE TABLE demo(vc varchar);
INSERT INTO demo VALUES('Today is a good day'),('I am feeling mopey');
```

### Request body before translation

This external function doesn’t have a request translator or response translator:

Copy code

```
CREATE OR REPLACE EXTERNAL FUNCTION ComprehendSentiment(thought varchar)
RETURNS VARIANT
API_INTEGRATION = aws_comprehend_gateway
AS 'https://<MY_GATEWAY>.execute-api.us-east-1.amazonaws.com/test/comprehend_proxy';
```

You can call the external function with your test data from the demo table:

Copy code

```
SELECT ComprehendSentiment(vc), vc FROM demo;
```

The generated request body uses the Snowflake external function
data format:

Copy code

```
{"body":{"data:" [[0, "Today is a good day"],[1,"I am feeling mopey"]]}}
```

However, the external sentiment analysis service expects a different
format that specifies the language and an array of strings:

Copy code

```
{"body": { Language: "en", TextList: [ "Today is a good day", "I am feeling mopey"]}}
```

The next section describes how you can add a request translator to change the request body to the required format.

### Convert the request body

By using a request translator, you can convert the default input described above
(in the Snowflake data format) to the format that the external service requires.

The following SQL creates an `awscomprehendrequest_translator` translator function.

Copy code

```
CREATE OR REPLACE FUNCTION AWSComprehendrequest_translator(EVENT OBJECT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT AS
'
var textlist = []
for(i = 0; i < EVENT.body.data.length; i++) {
   let row = EVENT.body.data[i];
   // row[0] is the row number and row[1] is the input text.
   textlist.push(row[1]); //put text into the textlist
}
// create the request for the service. Also pass the input request as part of the output.
return { "body": { "LanguageCode": "en", "TextList" : textlist }, "translatorData": EVENT.body }
';
```

In the request translator function, the code:

- Loops through each of the input rows. For each row, it adds the string,
  which is in `row[1]`, to the `textlist` array. The
  value at `row[0]` is the row number and it can be ignored.
- Returns a JSON body that has the language code and text
  list that matches the requirements of the external service.
- Returns data via the `translatorData` field. This is
  used by the response translator. In this example, you are sending the
  original input data. You will use the length of the input data in the
  response translator to know how many input requests there were.

You can test the request translator by calling it directly.

Copy code

```
SELECT AWSComprehendrequest_translator(parse_json('{"body":{"data": [[0, "I am so happy we got a sunny day for my birthday."], [1, "$$$$$."], [2, "Today is my last day in the old house."]]}}'));
```

The request translator puts the body into the shape expected by the external
service.

Copy code

```
{"body":{
   "LanguageCode": "en",
   "TextList": [
      "I am so happy we got a sunny day for my birthday.",
      "$$$$$.",
      "Today is my last day in the old house."
               ]
         },
   "translatorData": {
      "data": [[0, "I am so happy we got a sunny day for my birthday."],
               [1, "$$$$$."],
               [2, "Today is my last day in the old house."]]
                     }
}
```

### Response body before adding a response translator

A response body from the external service looks something like this.

Copy code

```
{"body":{
   "ErrorList": [ { "ErrorCode": 57, "ErrorMessage": "Language unknown", "Index": 1} ],
   "ResultList":[ { "Index": 0, "Sentiment": "POSITIVE",
                    "SentimentScore": { "Mixed": 25, "Negative": 5, "Neutral": 1, "Positive": 90 }},
                  { "Index": 2, "Sentiment": "NEGATIVE",
                    "SentimentScore": { "Mixed": 25, "Negative": 75, "Neutral": 30, "Positive": 20 }}
                ]
         }
}
```

### Convert the response body

The response translator processes the results that you get back from the
external service. The results contain a combination of errors in the
`ErrorList` and results in the `ResultList`.

The response translator code combines these results together to make a complete
set that matches the order of the rows that were passed to the external service. The
response translator returns the results in the Snowflake format.

The following SQL creates an `awscomprehendresponse_translator` translator function.

Copy code

```
CREATE OR REPLACE FUNCTION AWSComprehendresponse_translator(EVENT OBJECT)
RETURNS OBJECT
LANGUAGE JAVASCRIPT AS
'
// Combine the scored results and the errors into a single list.
var responses = new Array(EVENT.translatorData.data.length);
// output format: array of {
// "Sentiment": (POSITIVE, NEUTRAL, MIXED, NEGATIVE, or ERROR),
// "SentimentScore": <score>, "ErrorMessage": ErrorMessage }.
// If error, set ErrorMessage; otherwise, set SentimentScore.
// Insert good results into proper position.
for(i = 0; i < EVENT.body.ResultList.length; i++) {
   let row = EVENT.body.ResultList[i];
   let result = [row.Index, {"Sentiment": row.Sentiment, "SentimentScore": row.SentimentScore}]
   responses[row.Index] = result
}
// Insert errors.
for(i = 0; i < EVENT.body.ErrorList.length; i++) {
   let row = EVENT.body.ErrorList[i];
   let result = [row.Index, {"Sentiment": "Error", "ErrorMessage": row.ErrorMessage}]
   responses[row.Index] = result
}
return { "body": { "data" : responses } };
';
```

In the response translator function, the code:

- Initializes an array called `responses` with the size of the input from the
  `translatorData` array length. You sent `translatorData` from the request
  translator to the response translator to pass the original list of test strings.
- Loops through each of the non-error results and puts them into the result list.
- Loops through the error results and puts them into the result list. The result
  list has an index position which tells you what entry it is. The order of the
  produced results must match the input order. The result list also contains
  the sentiment information.

After all of the responses have been gathered, they are returned in a
JSON body in the format that Snowflake expects.

The following direct test will return a JSON body with the correct format.

Copy code

```
SELECT AWSComprehendresponse_translator(
    parse_json('{
        "translatorData": {
            "data": [[0, "I am so happy we got a sunny day for my birthday."],
                    [1, "$$$$$."],
                    [2, "Today is my last day in the old house."]]
                          }
        "body": {
            "ErrorList":  [ { "ErrorCode": 57,  "ErrorMessage": "Language unknown",  "Index": 1 } ],
            "ResultList": [
                            { "Index": 0,  "Sentiment": "POSITIVE",
                              "SentimentScore": { "Mixed": 25,  "Negative": 5,  "Neutral": 1,  "Positive": 90 }
                            },
                            { "Index": 2, "Sentiment": "NEGATIVE",
                              "SentimentScore": { "Mixed": 25,  "Negative": 75,  "Neutral": 30,  "Positive": 20 }
                            }
                          ]
            },
        }'
    )
);
```

### Assign the translators to the external function

To the external function, add the request and response translator functions by
assigning the function names as values to the `request_translator` and `response_translator`
parameters. This way, they’ll be called automatically when the external function runs.

Copy code

```
CREATE OR REPLACE EXTERNAL FUNCTION ComprehendSentiment(thought varchar)
RETURNS VARIANT
API_INTEGRATION = aws_comprehend_gateway
request_translator = db_name.schema_name.AWSComprehendrequest_translator
response_translator = db_name.schema_name.AWSComprehendresponse_translator
AS 'https://<MY_GATEWAY>.execute-api.us-east-1.amazonaws.com/test/comprehend_proxy';
```

You can describe the function to get information about it.

Copy code

```
DESCRIBE FUNCTION ComprehendSentiment(VARCHAR);
```

### Call the external function

Test the external function by calling it with a single sentence.

Copy code

```
SELECT ComprehendSentiment('Today is a good day');
```

You see the sentiment analysis results.

Copy code

```
{"Sentiment": "POSITIVE",
 "SentimentScore":{"Mixed":0.002436627633869648,
                   "Negative":0.0014803812373429537,
                   "Neutral":0.015923455357551575,
                   "Positive": 0.9801595211029053}}
```

Test the external function by calling it with multiple sentences. Use the same `demo` table that you created earlier.

Copy code

```
SELECT ComprehendSentiment(vc), vc FROM demo;
```

The sentiment analysis results are displayed.

[![A table showing the sentiment analysis results.](/static/images/screens/external-functions-serializers.png)](/static/images/screens/external-functions-serializers.png)

When the external function was called, the request translator automatically
converted data into the format required by the external service. Then,
the response translator automatically converted the response from the external
service back into the format required by Snowflake.

## Tips for testing request and response translators

- Test case values are typically OBJECT values (collections of key-value pairs). These should be formatted to meet the
  requirements in [these rules](/sql-reference/external-functions-data-format#label-external-functions-data-format).
- You can start testing your request translator or response translator by passing in an example input converted to a string. For example:

  Copy code

  ```
  select my_request_translator_function(parse_json('{"body": {"data": [ [0,"cat",867], [1,"dog",5309] ] } }'));
  ```

  (The input to `PARSE_JSON()` must be a JSON-formatted string.)
- Test with `NULL` values if appropriate.

  - Include at least one SQL `NULL` value in your test cases.
  - Include at least one [JSON NULL](/user-guide/semistructured-considerations#label-variant-null) value in your test cases.
- Translating a request and translating a response are often converse processes. Conceptually:

  Copy code

  ```
  my_response_translator_udf(my_request_translator_udf(x)) = x
  ```

  You can use this characteristic to help test your request translator and response translator if the data formats match. Create a table with
  good test values, then execute a command similar to:

  Copy code

  ```
  SELECT test_case_column
   FROM test_table
   WHERE my_response_translator_udf(my_request_translator_udf(x)) != x;
  ```

  The query should not return any rows.

  Note that translating a request and translating a response are not always exactly converse. For an example of where they might not be
  converse, see the discussion of converse functions in the “Usage Notes” section of the documentation for the
  [TO\_JSON() function](/sql-reference/functions/to_json).
