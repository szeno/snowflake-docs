# Step 2: Record the Amazon API Gateway URL and the new IAM role ARN

## Previous step

[Step 1: Use the template to create the remote service (AWS Lambda function) and proxy service (API Gateway)](/sql-reference/external-functions-creating-aws-template-services)

## Get the API Gateway URL and the new IAM role ARN

In the next few steps, you create the API integration and the external function.
In order to create these, you need the API Gateway URL and the New IAM Role ARN, which you can find by following the steps below.

1. You should be in the AWS Management Console. You should be on the **Events** tab for the stack you created in the
   previous step.
2. Click on the **Outputs** tab.
3. Copy the value for **resourceInvocationUrl** to the tracking worksheet field titled `Resource Invocation URL`.
4. Copy the value for **awsRoleArn** to the tracking worksheet field titled `New IAM Role ARN`.

## Next step

[Step 3: Create the API integration for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-api-integration)
