# Sample asynchronous remote service for AWS

This topic contains a sample asynchronous AWS Lambda Function (remote service). You can create this sample function by following
the same steps described in [Step 1: Create the remote service (AWS Lambda function) in the Management Console](/sql-reference/external-functions-creating-aws-ui-remote-service).

## Overview of the code

This section of the documentation provides information about creating an asynchronous external function on AWS.
(Before implementing your first asynchronous external function, you might want to read the
[conceptual overview](/sql-reference/external-functions-implementation#label-external-functions-implementation-asynchronous-remote-service) of asynchronous
external functions.)

On AWS, asynchronous remote services must overcome the following restrictions:

- Because the HTTP POST and GET are separate requests, the remote service must keep information about the workflow
  launched by the POST request so that the state can later be queried by the GET request.

  Typically, each HTTP POST and HTTP GET invokes a separate instance of the handler function(s) in a separate
  process or thread. The separate instances do not share memory. In order for the GET handler to read the
  status or the processed data, the GET handler must access a shared storage resource that
  is available on AWS.
- The only way for the POST handler to send the initial HTTP 202 response code is via a `return` statement (or
  equivalent), which terminates the execution of the handler. Therefore, prior to returning HTTP 202, the POST handler
  must launch an independent process (or thread) to do the actual data
  processing work of the remote service. This independent process typically needs access to the storage that is visible
  to the GET handler.

One way for an asynchronous remote service to overcome these restrictions is to use 3 processes (or threads) and shared storage:

![Illustration of processes for an Asynchronous Remote Service](/static/images/asynchronous-external-functions-lambdas-05.png)

In this model, the processes have the following responsibilities:

- The HTTP POST handler:

  - Reads the input data. In a Lambda Function, this is read from the body of the handler function’s `event` input
    parameter.
  - Reads the batch ID. In a Lambda Function, this is read from the header of the `event` input parameter.
  - Starts the data processing process, and passes it the data and the batch ID. The data is usually passed
    during the call, but could be passed by writing it to external storage.
  - Records the batch ID in shared storage that both the data processing process and
    the HTTP GET handler process can access.
  - If needed, records that the processing of this batch has not yet finished.
  - Returns HTTP 202 if no error was detected.
- The data processing code:

  - Reads the input data.
  - Processes the data.
  - Makes the result available to the GET handler (either by writing the result data to shared storage, or by
    providing an API through which to query the results).
  - Typically, updates this batch’s status (e.g. from `IN_PROGRESS` to `SUCCESS`) to indicate that the
    results are ready to be read.
  - Exits. Optionally, this process can return an error indicator. Snowflake does not see this directly
    (Snowflake sees only the HTTP return codes from the POST handler and GET handler), but returning an
    error indicator from the data processing process might help during debugging.
- The GET handler:

  - Reads the batch ID. In a Lambda Function, this is read from the header of the `event` input parameter.
  - Reads the storage to get the current status of this batch (e.g. `IN_PROGRESS` or `SUCCESS`).
  - If the processing is still in progress, then return 202.
  - If the processing has finished successfully, then:

    - Read the results.
    - Clean up storage.
    - Return the results along with HTTP code 200.
  - If the stored status indicates an error, then:

    - Clean up storage.
    - Return an error code.

  Note that the GET handler might be called multiple times for a batch if the processing takes long
  enough that multiple HTTP GET requests are sent.

There are many possible variations on this model. For example:

- The batch ID and status could be written at the start of the data processing process rather than at the end of
  the POST process.
- The data processing could be done in a separate function (e.g. a separate Lambda function) or even as a
  completely separate service.
- The data processing code does not necessarily need to write to shared storage. Instead, the processed data could
  be made available another way. For example, an API could accept the batch ID as a parameter and return the data.

The implementation code should take into account the possibility that the processing will take too long
or will fail, and therefore any partial results must be cleaned up to avoid wasting storage space.

The storage mechanism must be sharable across multiple processes (or threads). Possible storage mechanisms include:

- Storage mechanisms provided by AWS, such as:

  - Disk space (e.g. [Amazon Elastic File System (EFS)](https://aws.amazon.com/efs/) ).
  - A local database server available through AWS (e.g. [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) ).
- Storage that is outside AWS but accessible from AWS.

The code for each of the 3 processes above can be written as 3 separate Lambda Functions (one for the POST handler,
one for the data processing function, and one for the GET handler), or as a single function that can be invoked in
different ways.

The sample Python code below is a single Lambda Function that can be called separately for the POST, the
data processing, and the GET processes.

## Sample code

This code shows a sample query with output.
The focus in this example is on the three processes and how they interact, not on the shared storage mechanism
(DynamoDB) or data transformation (sentiment analysis). The code is structured to make it easy to replace the
example storage mechanism and data transformation with different ones.

For simplicity, this example:

- Hard-codes some important values (e.g. the AWS region).
- Assumes the existence of some resources (e.g. the Jobs table in Dynamo).

Copy code

```
import json
import time
import boto3

HTTP_METHOD_STRING = "httpMethod"
HEADERS_STRING = "headers"
BATCH_ID_STRING = "sf-external-function-query-batch-id"
DATA_STRING = "data"
REGION_NAME = "us-east-2"

TABLE_NAME = "Jobs"
IN_PROGRESS_STATUS = "IN_PROGRESS"
SUCCESS_STATUS = "SUCCESS"

def lambda_handler(event, context):
    # this is called from either the GET or POST
    if (HTTP_METHOD_STRING in event):
        method = event[HTTP_METHOD_STRING]
        if method == "POST":
            return initiate(event, context)
        elif method == "GET":
            return poll(event, context)
        else:
            return create_response(400, "Function called from invalid method")

    # if not called from GET or POST, then this lambda was called to
    # process data
    else:
        return process_data(event, context)

# Reads batch_ID and data from the request, marks the batch_ID as being processed, and
# starts the processing service.
def initiate(event, context):
    batch_id = event[HEADERS_STRING][BATCH_ID_STRING]
    data = json.loads(event["body"])[DATA_STRING]

    lambda_name = context.function_name

    write_to_storage(batch_id, IN_PROGRESS_STATUS, "NULL")
    lambda_response = invoke_process_lambda(batch_id, data, lambda_name)

    # lambda response returns 202, because we are invoking it with
    # InvocationType = 'Event'
    if lambda_response["StatusCode"] != 202:
        response = create_response(400, "Error in initiate: processing lambda not started")
    else:
        response = {
            'statusCode': lambda_response["StatusCode"]
        }

    return response

# Processes the data passed to it from the POST handler. In this example,
# the processing is to perform sentiment analysis on text.
def process_data(event, context):
    data = event[DATA_STRING]
    batch_id = event[BATCH_ID_STRING]

    def process_data_impl(data):
        comprehend = boto3.client(service_name='comprehend', region_name=REGION_NAME)
        # create return rows
        ret = []
        for i in range(len(data)):
            text = data[i][1]
            sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            sentiment_score = json.dumps(sentiment_response['SentimentScore'])
            ret.append([i, sentiment_score])
        return ret

    processed_data = process_data_impl(data)
    write_to_storage(batch_id, SUCCESS_STATUS, processed_data)

    return create_response(200, "No errors in process")

# Repeatedly checks on the status of the batch_ID, and returns the result after the
# processing has been completed.
def poll(event, context):
    batch_id = event[HEADERS_STRING][BATCH_ID_STRING]
    processed_data = read_data_from_storage(batch_id)

    def parse_processed_data(response):
        # in this case, the response is the response from DynamoDB
        response_metadata = response['ResponseMetadata']
        status_code = response_metadata['HTTPStatusCode']

        # Take action depending on item status
        item = response['Item']
        job_status = item['status']
        if job_status == SUCCESS_STATUS:
            # the row number is stored at index 0 as a Decimal object,
            # we need to convert it into a normal int to be serialized to JSON
            data = [[int(row[0]), row[1]] for row in item['data']]
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'data': data
                })
            }
        elif job_status == IN_PROGRESS_STATUS:
            return {
                'statusCode': 202,
                "body": "{}"
            }
        else:
            return create_response(500, "Error in poll: Unknown item status.")

    return parse_processed_data(processed_data)

def create_response(code, msg):
    return {
        'statusCode': code,
        'body': msg
    }

def invoke_process_lambda(batch_id, data, lambda_name):
    # Create payload to be sent to processing lambda
    invoke_payload = json.dumps({
        BATCH_ID_STRING: batch_id,
        DATA_STRING: data
    })

    # Invoke processing lambda asynchronously by using InvocationType='Event'.
    # This allows the processing to continue while the POST handler returns HTTP 202.
    lambda_client = boto3.client('lambda', region_name=REGION_NAME,)
    lambda_response = lambda_client.invoke(
        FunctionName=lambda_name,
        InvocationType='Event',
        Payload=invoke_payload
    )
    # returns 202 on success if InvocationType = 'Event'
    return lambda_response

def write_to_storage(batch_id, status, data):
    # we assume that the table has already been created
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)

    # Put in progress item in table
    item_to_store = {
        'batch_id': batch_id,
        'status': status,
        'data': data,
        'timestamp': "{}".format(time.time())
    }
    db_response = table.put_item(
        Item=item_to_store
    )

def read_data_from_storage(batch_id):
    # we assume that the table has already been created
    client = boto3.resource('dynamodb')
    table = client.Table(TABLE_NAME)

    response = table.get_item(Key={'batch_id': batch_id},
                          ConsistentRead=True)
    return response
```

## Sample call and output

Here is a sample call to the asynchronous external function, along with sample output, including the sentiment
analysis results:

Copy code

```
create table test_tb(a string);
insert into test_tb values
    ('hello world'),
    ('I am happy');
select ext_func_async(a) from test_tb;

Row | EXT_FUNC_ASYNC(A)
0   | {"Positive": 0.47589144110679626, "Negative": 0.07314028590917587, "Neutral": 0.4493273198604584, "Mixed": 0.0016409909585490823}
1   | {"Positive": 0.9954453706741333, "Negative": 0.00039307220140472054, "Neutral": 0.002452891319990158, "Mixed": 0.0017087293090298772}
```

## Notes about the sample code

- The data processing function is invoked by calling:

  Copy code

  ```
  lambda_response = lambda_client.invoke(
   ...
   InvocationType='Event',
   ...
  )
  ```

  The InvocationType should be ‘Event’, as shown above, because the 2nd process (or thread) must be asynchronous and
  `Event` is the only type of non-blocking call available through the `invoke()` method.
- The data processing function returns an HTTP 200 code. However, this HTTP 200 code is not returned directly to
  Snowflake. Snowflake does not see any HTTP 200 until a GET polls the status and sees that the data processing
  function finished processing this batch successfully.
