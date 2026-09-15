# Creating an external function for AWS using an AWS CloudFormation template

These topics provide detailed instructions for using an AWS (Amazon Web Services) CloudFormation template to create an external
function hosted on AWS.

Snowflake provides a sample template that you can start with. This template hides some details of the creation process.
When you are ready to create your own custom external function, you can either customize a copy of the template or you can
[use the AWS Management Console](/sql-reference/external-functions-creating-aws-ui) to create the function.

These topics assume that you are already familiar with the AWS Management Console. They describe the general steps that you need
to complete, but do not describe the Console in detail.

**See also:**

- [Planning an external function for AWS](/sql-reference/external-functions-creating-aws-planning)

**Steps:**

- [Step 1: Use the template to create the remote service (AWS Lambda function) and proxy service (API Gateway)](/sql-reference/external-functions-creating-aws-template-services)
- [Step 2: Record the Amazon API Gateway URL and the new IAM role ARN](/sql-reference/external-functions-creating-aws-template-gateway-url)
- [Step 3: Create the API integration for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-api-integration)
- [Step 4: Link the API integration for AWS to the proxy service in the Management Console](/sql-reference/external-functions-creating-aws-common-api-integration-proxy-link)
- [Step 5: Create the external function for AWS in Snowflake](/sql-reference/external-functions-creating-aws-common-ext-function)
