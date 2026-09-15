# Step 1: Create the remote service (AWS Lambda function) in the Management Console

This topic provides detailed instructions for creating an AWS Lambda Function for use as the remote service for your external
function.

This topic includes code for a sample Lambda Function that you can use as-is to create your first external function, or that
you can use as a starting point for a custom Lambda Function.

## Previous step

[Planning an external function for AWS](/sql-reference/external-functions-creating-aws-planning)

## Introduction

There are multiple ways to create a remote service on AWS. This topic shows one way, which is to create a Lambda Function
to be used as the remote service.

This tutorial describes two sample Lambda Functions, each of which is written in Python.

More details are provided in [Snowflake Sample Functions](#label-snowflake-sample-functions-aws) (in this topic).

## Understanding Lambda function input and output

In order for Snowflake to send data to and receive data from your remote service, your remote service must accept
and return data in JSON format.

Platform-independent information about remote service input and output is in
[Remote Service Input and Output Data Formats](/sql-reference/external-functions-data-format#label-external-functions-data-format) .

This section provides details that are specific to AWS Lambda Functions.

### Language-independent input and output via JSON

The information in this section applies to all Lambda Functions used as remote services for Snowflake external functions.
For platform-specific information about external function input and output, see the sub-section(s) below.

On AWS, the convention for an HTTP-compatible service is to return the body inside a JSON object that also includes the HTTP status
code. The JSON for a typical return value from an AWS Lambda function looks like the following:

> Copy code
>
> ```
> {
> "statusCode": <http_status_code>,
> "body":
>         {
>             "data":
>                   [
>                       [ 0, <value> ],
>                       [ 1, <value> ]
>                       ...
>                   ]
>         }
> }
> ```

The structure of the JSON input is similar to the preceding, but includes additional key-value pairs that you are unlikely to
need, and excludes the `statusCode`.

### Python-specific Lambda function input

The following material applies to Snowflake-compatible Python-language Lambda Functions, including the sample Lambda Functions
in this tutorial. This information is in addition to the
[language-independent rules for input and output](#label-aws-language-independent-input-and-output).

A Snowflake-compatible Python-Language Lambda Function receives two parameters, `event` and `context`. Simple
external functions typically need only the `event` parameter.

The `event` parameter includes many sub-fields, one of which is `body`. The body is a JSON-compatible string that
contains a dictionary.

The dictionary includes a key named `data`; the corresponding value for `data` is an array. That array contains
the rows passed by Snowflake.

Each row is represented by an array that is nested inside the `data` array.

(Because AWS Lambda conveniently processes the HTTP POST request sent by Snowflake, extracts the body, and passes the body inside
the event parameter, the example functions provided by Snowflake do not need to parse the entire HTTP POST request.)

The [Sample synchronous Lambda function](/sql-reference/external-functions-creating-aws-sample-synchronous) includes code showing how to read the `event` parameter.

## Choose the code for the Lambda function

### Snowflake sample functions

Snowflake supplies two sample functions:

- The shorter example is [synchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-synchronous). If you are new to
  external functions or Lambda Functions, Snowflake recommends that you use this to create your first sample external function.

  Experienced users can also copy and modify it to use as a starting point for custom remote services.

  The code is available in [sample synchronous Lambda Function](/sql-reference/external-functions-creating-aws-sample-synchronous).
- The other example is [asynchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous).

  This sample is intended primarily as a sample for building customized asynchronous remote services.

  The code is available in [sample asynchronous Lambda Function](/sql-reference/external-functions-creating-aws-sample-asynchronous).

### Custom Lambda function

You can write your own Lambda Function from scratch, or you can use one of the functions described in
[Choose the code for the Lambda function](#label-snowflake-sample-functions-aws) (in this topic) as a starting point.

If you have an existing remote service that you want to use, then you can skip most of the instructions in this step of the
tutorial. Instead, do the following:

1. Record your AWS Account ID in the `Your AWS Account ID` field in the tracking worksheet.
2. Record the remote service’s Lambda Function name in the `Lambda Function Name` field in the tracking worksheet.
3. Go to [Step 2: Create the proxy service (Amazon API Gateway) in the AWS Management Console](/sql-reference/external-functions-creating-aws-ui-proxy-service).

## Create a Lambda function

To create an AWS Lambda Function, follow the steps below.

Note

Although these steps show you how to create the sample remote services provided by Snowflake, you can use these steps as a model
for creating your own customized remote service. If you create a custom Lambda Function, then modify the steps below as
appropriate (e.g. choose the appropriate programming language for your remote service’s code).

1. Log into the AWS Management Console, if you haven’t already.
2. If you have not already recorded your AWS account ID in the worksheet field named `Your AWS Account ID`, record it now.

   If you need to look up your AWS account ID, follow the
   [AWS instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html#FindingYourAWSId).
3. Select **Lambda**.
4. Select **Create function**.
5. Enter a function name.

   Record this name in the `Lambda Function Name` field in the worksheet.
6. Select the programming language to use. If you are using one of the sample Python functions provided by Snowflake,
   then choose **Python 3.10**.
7. Choose or create an execution role for this function.

   Select the appropriate option(s), typically **Create a new role with basic Lambda permissions**.

   (This role is separate from your cloud account role and separate from your Snowflake role(s).)
8. Click on the **Create Function** button.
9. In the **lambda\_function** tab, enter the code for the function.

   If you have not already written your own function, you can use the following example provided by Snowflake:

   [sample synchronous code](/sql-reference/external-functions-creating-aws-sample-synchronous#label-sample-synchronous-lambda-function) or the

   Tip

   If you cannot paste into the edit window, try double-clicking on the function’s file name to enable editing.
10. Click on the **Deploy** button to deploy the function.

## Test the Lambda function

Click the down-arrow beside the **Test** button and select **Configure test event**. In the **Event name** field, type **test**.

For the sample synchronous Python function provided by Snowflake, use the following test data (replace any default
data with the data below):

> Copy code
>
> ```
> {
>   "body":
>     "{ \"data\": [ [ 0, 43, \"page\" ], [ 1, 42, \"life, the universe, and everything\" ] ] }"
> }
> ```

Click **Create**, and then click **Test**.

The execution results should be similar to:

> Copy code
>
> ```
> {
>   "statusCode": 200,
>   "body": "{\"data\": [[0, [\"Echoing inputs:\", 43, \"page\"]], [1, [\"Echoing inputs:\", 42, \"life, the universe, and everything\"]]]}"
> }
> ```

You now have an AWS Lambda function that you can use as the remote service for your external function.

## Next step

[Step 2: Create the proxy service (Amazon API Gateway) in the AWS Management Console](/sql-reference/external-functions-creating-aws-ui-proxy-service)
