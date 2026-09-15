# Troubleshooting external functions for AWS

This topic provides troubleshooting information for external functions for AWS.

# Platform-independent Runtime Issues

## Data Type Return Values Do Not Match Expected Return Values

When passing arguments to or from an external function, ensure that the data types are appropriate. If the value
sent can’t fit into the data type being received, the value might be truncated or corrupted in some other way.

For more details, see [Ensure that arguments to the external function correspond to arguments parsed by the remote service](/sql-reference/external-functions-best-practices#label-external-functions-general-ensure-arguments-correspond).

## Error: Row numbers out of order

Possible Causes:
:   The row numbers you return within each batch should be monotonically ascending integers starting at 0. The input row numbers must also
    follow this rule, and each output row should match the corresponding input row. For example, the output in output row 0 should
    correspond to the input in input row 0.

Possible Solutions:
:   Ensure that the row numbers you return are the same as the row numbers you received, and that each output value uses the row number of
    the corresponding input. If this doesn’t work, then the input row numbers may not be correct or you did not return the rows in the
    correct order.

    Next, ensure that the output row numbers start from 0, increase by 1, and are in order.

For more information about data input and output formats, see [Remote service input and output data formats](/sql-reference/external-functions-data-format#label-external-functions-data-format).

## Error: “Error parsing JSON: Invalid response”

Possible Causes:
:   The most likely cause is that the JSON returned by the remote service (e.g. AWS Lambda function) is not constructed correctly.

Possible Solutions:
:   Ensure that the external function returns an array of arrays, with one inner array returned for each input row received. Review the
    description of the output format at [Data format received by Snowflake](/sql-reference/external-functions-data-format#label-format-of-data-to-snowflake).

## Error: Format of the returned value is not JSON

Possible Causes:
:   Your return value includes double quotes inside the value.

Possible Solutions:
:   Although JSON strings are delimited by double quotes, the string itself should not start and end with a quotation mark in most cases.
    If the embedded double quotes are incorrect, remove them.

## Error: Function received the wrong number of rows

Possible Causes:
:   The remote service tried to return more or fewer rows than it received. Even though the function is nominally scalar, it might receive
    multiple rows in the `body` field of the `event` parameter, and should return exactly as many rows as it received.

Possible Solution(s):
:   Ensure that the remote service returns one row for each row that it receives.

## AWS-specific issues

### API Gateway returns error 502 while the endpoint is using Lambda proxy integration

Possible Cause:
:   The Lambda function might have:

    - Timed out.
    - Thrown an exception.
    - Failed in some other way.

Possible Solution:
:   If the Lambda or API Gateway logs are available to you, examine them.

    If the source code of the Lambda function is available to you, then analyze and debug the code in the
    Lambda function. In some cases, you might be able to execute a copy of that code in a simpler context
    (outside AWS) to help debug it.

    Verify that the data sent to the Lambda function is in the format that Lambda function expects.
    You might want to try sending a smaller, simpler data set to see whether that succeeds.

    Verify that you are not sending too much data at a time.

    In some cases, increasing the timeout might solve the problem, especially if the Lambda function requires a
    lot of CPU resources, or if the Lambda function itself calls other remote services and thus requires more time.

### Unable to read the requests body in the HTTP POST method inside the Amazon AWS Lambda function

Possible Cause:
:   You might not have enabled Lambda proxy integration.

Possible Solution:
:   Enable Lambda proxy integration.

    For more details, see the steps in [Create the API Gateway endpoint](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-external-functions-creating-aws-create-and-configure-an-api).

### Error assuming AWS\_ROLE

The full text of the message is:

> Copy code
>
> ```
> SQL execution error: Error assuming AWS_ROLE. Please verify the role and externalId are
> configured correctly in your AWS policy.
> ```

Possible Cause:
:   - In the AWS Trust Relationship Policy for your role, the AWS ARN is incorrect. Possible causes of that include:

      - You did not set it.
      - You set it, but you used the ARN of the AWS role (incorrect) instead of the user ARN, which you
        can see from the DESCRIBE INTEGRATION command in Snowflake. Make sure that you use the value from the
        `API_AWS_IAM_USER_ARN` field of the worksheet rather than the value from the “API\_AWS\_ROLE\_ARN” field.
    - In your AWS Trust Relationship Policy, the **std:ExternalId** is incorrect. Possible causes of that
      include:

      - You did not set it.
      - You re-created the API integration object. Re-creating the API object changes its external ID.

### Error: 403 ‘{“Message”:”User: <ARN> is not authorized to perform: execute-api:Invoke”}’

The full text of the message is:

> Copy code
>
> ```
> Request failed for external function <function_name>.
> Error: 403 '{"Message":"User: <ARN> is not authorized to perform: execute-api:Invoke on resource: <MethodRequestARN>"}'
> ```

Possible Cause:
:   - The API Gateway resource policy has:

      - The wrong IAM Role ARN.
      - The wrong assumed role.
      - The wrong Method Request ARN.
    - The IAM role doesn’t have the right policy attached.

Possible Solution:
:   - Make sure that you followed the resource policy template in
      [Secure your Amazon API Gateway endpoint](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-secure-your-proxy-service-endpoint-aws). Specifically, make sure that your resource policy:

      - Replaced the **<12-digit number>** with the value in the worksheet field named `Your AWS account ID`.
      - Replaced the **<external\_function\_role>** with the value in the `New IAM Role Name` field of the
        worksheet.
      - Replaced the **method\_request\_ARN** in the **Resource** field with the value in the
        `Method Request ARN` field in the worksheet. Make sure there is no slash at the end.
    - If you need to make sure that the IAM role has the correct permissions policy attached, you can find the
      role’s permissions policy list by following the steps below:

      1. In AWS, go to Identity and Access Management (IAM) and select the role.
      2. View the **Summary** for the role.
      3. Click on the **Permissions** tab.
      4. Verify that the required policy is in the **Permissions policies** list.
    - Make sure the endpoint being called is the resource, not the stage, that is set up on the API Gateway.

### Error: 403 ‘{“Message”:”User: anonymous is not authorized to perform: execute-api:Invoke”}’

The full text of the message is:

> Copy code
>
> ```
> Request failed for external function <function_name>.
> Error: 403 '{"Message":"User: anonymous is not authorized to perform: execute-api:Invoke on resource: <MethodRequestARN>"}'
> ```

Possible Cause:
:   One possible cause is that when you were configuring authorization for the API Gateway, you might not have
    specified that the **Method Request** requires **AWS\_IAM** authorization for the resource.

Possible Solution:
:   If you did not follow the instructions in
    [secure the Amazon API Gateway](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-secure-your-proxy-service-endpoint-aws), then please follow them
    now to specify **AWS\_IAM** authorization.

### Error parsing JSON response … Error: top-level JSON object must contain “data” JSON array element

The full text of the message is:

> Copy code
>
> ```
> Error parsing JSON response for external function ... Error: top-level JSON object must contain "data" JSON array element
> ```

Possible Cause:
:   - You might not have specified Lambda proxy integration for the POST command in your API Gateway resource.

Possible Solution:
:   - Specify Lambda proxy integration for your API Gateway resource.

      For more details about Lambda proxy integration, see the steps in
      [Create the API Gateway endpoint](/sql-reference/external-functions-creating-aws-ui-proxy-service#label-external-functions-creating-aws-create-and-configure-an-api).

### Request failed for external function EXT\_FUNC with remote service error: 403 ‘{“message”:”Forbidden”}’;

Possible Cause:
:   The proxy service required an [API key](/sql-reference/external-functions-security#label-external-functions-api-key), typically for
    authentication or billing. The API key is missing or incorrect.

Possible Solution:
:   Use the ALTER API INTEGRATION command to specify the correct API key.

### CloudFormation stack creation fails

This error can occur if you are using an AWS CloudFormation template to create an external function.

Possible Cause:
:   You do not have required permissions for creating the resources specified in the CloudFormation template.

Possible Solution:
:   Check the **Events** tab for the stack to see the error details.

    Also look at the AWS external functions
    [troubleshooting](#label-external-functions-creating-aws-troubleshooting) page for additional
    troubleshooting tips.
