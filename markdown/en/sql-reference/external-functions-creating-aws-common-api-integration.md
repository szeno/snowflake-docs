# Step 3: Create the API integration for AWS in Snowflake

This topic provides instructions for creating an API integration object in Snowflake to work with your proxy service (i.e.
Amazon API Gateway). The instructions are the same regardless of whether you are using the Management Console or the
CloudFormation template.

## Previous step

AWS Management Console:
:   [Step 2: Create the proxy service (Amazon API Gateway) in the AWS Management Console](/sql-reference/external-functions-creating-aws-ui-proxy-service)

AWS CloudFormation template:
:   [Step 2: Record the Amazon API Gateway URL and the new IAM role ARN](/sql-reference/external-functions-creating-aws-template-gateway-url)

## Prerequisites

You need the following information to create the API integration for AWS in Snowflake:

> - The `New IAM Role ARN` (from your tracking worksheet).
> - The `Resource Invocation URL` (from your tracking worksheet).

## Create the API integration object

1. Open a Snowflake session, typically a Snowflake web interface session.
2. Use a Snowflake role with ACCOUNTADMIN privileges or the CREATE INTEGRATION privilege, for example:

   Copy code

   ```
   use role <has_accountadmin_privileges>;
   ```
3. Type the [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) command to create an API integration. The command should
   look similar to the following:

   Copy code

   ```
   CREATE OR REPLACE API INTEGRATION my_api_integration_01
     api_provider = aws_api_gateway
     api_aws_role_arn = '<new_IAM_role_ARN>'
     api_allowed_prefixes = ('https://')
     enabled = true;
   ```

   Customize the command:

   - The `api_provider` clause should be set based on the type of endpoint:

     - If you are using a private endpoint, the **api\_provider** clause should be set to
       `aws_private_api_gateway`.
     - If you are using a U.S. government GovCloud endpoint, the **api\_provider** clause should be set to
       `aws_gov_api_gateway` or `aws_gov_private_api_gateway`.
     - For most other users, the **api\_provider** clause should be set to `aws_api_gateway`.
   - The `<new_IAM_role_ARN>` should be the value in the `New IAM Role ARN` field in the tracking worksheet.
   - The **api\_allowed\_prefixes** field should contain the resource invocation URL that you recorded earlier.

   Below is an example of a complete CREATE API INTEGRATION statement:

   Copy code

   ```
   create or replace api integration demonstration_external_api_integration_01
    api_provider=aws_api_gateway
    api_aws_role_arn='arn:aws:iam::123456789012:role/my_cloud_account_role'
    api_allowed_prefixes=('https://xyz.execute-api.us-west-2.amazonaws.com/production/')
    enabled=true;
   ```
4. In the tracking worksheet field titled `API Integration Name`, record the name of the API integration
   that you created. You need the API integration name when you execute the
   CREATE EXTERNAL FUNCTION command later.
5. Execute the CREATE API INTEGRATION command you typed above.

## Record the API\_AWS\_IAM\_USER\_ARN and API\_AWS\_EXTERNAL\_ID

1. Execute the DESCRIBE INTEGRATION command.

   Copy code

   ```
   DESCRIBE INTEGRATION <my_integration_name>;
   ```

   For example:

   Copy code

   ```
   DESCRIBE INTEGRATION my_api_integration_01;
   ```
2. Look for the property named **API\_AWS\_IAM\_USER\_ARN** and then record that property’s **property\_value** in the
   tracking worksheet.
3. Find the property named **API\_AWS\_EXTERNAL\_ID** and record that property’s **property\_value** in the tracking worksheet.

   Note that the **property\_value** of the **API\_AWS\_EXTERNAL\_ID** often ends with an equals sign (“=”). That equals sign is
   part of the value; make sure that you cut and paste it along with the rest of the **property\_value**.

For the next few steps, you return to your AWS administration window. Do not close your Snowflake
administration window now; you must return to it later.

## Next step

[Step 4: Link the API integration for AWS to the proxy service in the Management Console](/sql-reference/external-functions-creating-aws-common-api-integration-proxy-link)
