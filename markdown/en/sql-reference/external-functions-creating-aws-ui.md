# Creating an external function for AWS using the AWS Management Console

These topics provide detailed instructions for using the AWS Management Console user interface to create an external function
hosted on AWS (Amazon Web Services). You can use these instructions either to create the sample external function provided by
Snowflake or as a guide to create your own external function.

These topics explain how to:

- Create a basic AWS Lambda Function as a remote service and an Amazon API Gateway as a proxy service.
- Create an API integration and the external function itself in Snowflake.
- Link the API integration to the API Management service.
- Secure the API Management service through a security policy.

These topics assume that you are already familiar with the AWS Management Console. They describe the general steps that you need
to complete, but do not describe the Console in detail.

**See also:**

- [Planning an external function for AWS](/sql-reference/external-functions-creating-aws-planning)

**Steps:**

- [Step 1: Create the remote service (AWS Lambda function) in the Management Console](/sql-reference/external-functions-creating-aws-ui-remote-service)
- [Step 2: Create the proxy service (Amazon API Gateway) in the AWS Management Console](/sql-reference/external-functions-creating-aws-ui-proxy-service)
- [Step 3: Create the API integration for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-api-integration)
- [Step 4: Link the API integration for AWS to the proxy service in the Management Console](/sql-reference/external-functions-creating-aws-common-api-integration-proxy-link)
- [Step 5: Create the external function for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-ext-function)
