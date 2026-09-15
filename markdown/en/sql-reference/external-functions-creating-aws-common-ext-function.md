# Step 5: Create the external function for AWS in Snowflake

This topic provides instructions for creating an external function object in Snowflake. This object stores information about the remote
service, such as the parameters that the remote service accepts. The instructions are the same regardless of whether you are using the
AWS Management Console or the AWS CloudFormation template.

Note

External functions in Snowflake are database objects, meaning they must be created in a schema in a database. To create an external
function, you must have the appropriate privileges on the database and schema where you are creating the function.

For more details, see [Access control privileges](/user-guide/security-access-control-privileges).

## Previous step

[Step 4: Link the API integration for AWS to the proxy service in the Management Console](/sql-reference/external-functions-creating-aws-common-api-integration-proxy-link)

## Create the external function

Return to the Snowflake web interface (where you earlier typed the `CREATE API INTEGRATION` command).

1. Type the `CREATE EXTERNAL FUNCTION` command. It should look similar to the following:

   Copy code

   ```
   CREATE EXTERNAL FUNCTION my_external_function(n INTEGER, v VARCHAR)
    RETURNS VARIANT
    API_INTEGRATION = <api_integration_name>
    AS '<resource_invocation_url>';
   ```

   Customize the command:

   - The `<api_integration_name>` value should contain the name of the API integration that you created earlier.
   - The `<resource_invocation_url>` value should be the `Resource Invocation URL` you recorded in the worksheet.
     Make sure that this URL includes the API Gateway resource name, not just the stage name.
   - You might also want to customize the function name.

   This example passes two arguments (an INTEGER and a VARCHAR ) because those are the arguments that the
   Lambda function expects. When you create your own Lambda function, you must pass
   appropriate arguments for your Lambda function.
2. Record the name of the external function in the `External Function Name` field in your tracking worksheet.
3. If you have not already executed the CREATE EXTERNAL FUNCTION command that you typed above, execute it now.

## Test your external function

You should now be able to call your external function to verify that it works correctly.

For details, see [Calling an external function for AWS](/sql-reference/external-functions-creating-aws-call).

## Next step

None. If you were able to call the function, then you’ve successfully created an external function for AWS.
