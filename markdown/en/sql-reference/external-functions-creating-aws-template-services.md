# Step 1: Use the template to create the remote service (AWS Lambda function) and proxy service (API Gateway)

This topic provides detailed instructions for using the AWS CloudFormation template provided by Snowflake. The template simplifies
the tasks for creating the AWS Lambda Function (to use as the remote service) and the Amazon API Gateway (to use as the proxy
service) for your external function.

This document shows how to create a sample external function on AWS by using a CloudFormation template.

Snowflake provides a template you can start with. This template hides some details of the creation process and
hard-codes some names (for example, the stage name) and functionality. When you are ready to create your own custom external
function, you can either customize a copy of the template, or you can follow the more flexible instructions at
[Creating external functions on AWS](/sql-reference/external-functions-creating-aws).

If you would like to customize the template, you can read more about
[AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-whatis-concepts.html).

Note

These instructions assume that you are already familiar with AWS administration. These instructions
describe the general steps that you need to execute, but do not describe the user interface in
detail because the interface could change.

## Previous step

[Planning an external function for AWS](/sql-reference/external-functions-creating-aws-planning)

## Upload the template

1. Go to the AWS Management Console.
2. In the top search bar, search for **CloudFormation**.
3. Under Services, click on **CloudFormation**.
4. Click on **Create stack**.

   If given a choice between **With new resources (standard)** or
   **With existing resources (import resources)**, then choose **With new resources (standard)**.
5. On the **Create stack** page, under **Prepare template**, select **Template is ready**.
6. Select **Upload a template file**.
7. Select **Choose file**.
8. Navigate to the directory that contains your copy of the template, then select that template.
9. Click **Next** to reach the page on which you enter names for roles, etc.

   Note

   The template uses default names for some resources. You can change the names.

## Configure your options

The template contains default values for most fields. However, you need to enter a few values, such as whether you want a
regional endpoint or a private endpoint.

1. Enter a name for the stack.
2. Enter the type of endpoint that you want to use: “REGIONAL” or “PRIVATE”.

   If you are unsure which type to use, choose “REGIONAL”.

   If you choose “PRIVATE”, then update the VPC ID (labeled “sourceVpcId” in the template).
   (For instructions on finding your VPC ID, see [Planning an external function for AWS](/sql-reference/external-functions-creating-aws-planning).)

   For more information about endpoints, including a description of the different types of endpoints, see
   [AWS endpoints](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html)
   and [Choosing your endpoint type: Regional endpoint vs. Private endpoint](/sql-reference/external-functions-creating-aws-planning#label-external-functions-aws-endpoint-type).
3. Enter a name for the API Gateway IAM role (parameter **apiGatewayIAMRoleName**). This is the role assumed
   by Snowflake for authorizing with the API Gateway.
   Make sure this role does not already exist because the template will try to update the role if it exists.

   Record the role name in the tracking worksheet field titled `New IAM Role Name`.
4. Enter a name for the Lambda Execution role (parameter **lambdaExecutionRoleName**). This role is used by the
   Lambda service for adding CloudWatch logs.
   Make sure this role does not already exist because the template will try to update the role if it exists.
5. Click **Next**.

   This page has some advanced options for template deployment.

   1. Optionally, set advanced options, such as stack policy. (These are not needed when creating the sample function
      using the template supplied by Snowflake. However, if you use template-based deployment for functions that you have
      customized, then you might need to customize the advanced options at this point.)
   2. Click **Next**.
6. On the review page, scroll down to the end and acknowledge that the CloudFormation template might create IAM
   resources with custom names. This is needed because the template creates two IAM roles as part of the deployment.
7. Click on **Create stack**.

The deployment will take a few seconds. After the deployment is complete, you should be on the **Events** tab for
the newly created stack. The created resources will be listed under the **Resources** tab.

## Next step

[Step 2: Record the Amazon API Gateway URL and the new IAM role ARN](/sql-reference/external-functions-creating-aws-template-gateway-url)
