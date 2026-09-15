# Step 4: Create the external function for GCP in Snowflake

This topic provides instructions for creating an external function object in Snowflake. This object stores information about the remote
service, such as the parameters that the remote service accepts.

Note

External functions in Snowflake are database objects, meaning they must be created in a schema in a database. To create an external
function, you must have the appropriate privileges on the database and schema where you are creating the function.

For more details, see [Access control privileges](/user-guide/security-access-control-privileges).

## Previous step

[Step 3: Create the API integration for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-api-integration)

## Create the external function object

This task assumes you are in the **Worksheets** [![Worksheet tab](/static/images/screens/ui-navigation-worksheet-icon.svg)](/static/images/screens/ui-navigation-worksheet-icon.svg) page in the Classic Console:

1. Enter a [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) statement. The statement should look similar to the following:

   > Copy code
   >
   > ```
   > create or replace external function <external_function_name>(<parameters>)
   >  returns variant
   >  api_integration = <api_integration_name>
   >  as '<function_url>';
   > ```
2. Replace `external_function_name` with a unique function name (e.g. `echo`). This name must follow the rules for
   [Object identifiers](/sql-reference/identifiers).

   In addition, record the function name in the “External Function Name” field in your tracking worksheet.
3. Replace `parameters` with the names and SQL data types of the parameters for the function, if any. For example:

   > Copy code
   >
   > ```
   > a integer, b varchar
   > ```

   The parameters must correspond to the parameters expected by the remote service. The parameter names do not need to match, but the
   data types need to be compatible.

   In addition, record the parameter names and data types in the “External Function Name” field in your tracking worksheet.
4. Replace `api_integration_name` with the value from the “API Integration Name” field in your tracking worksheet.

1. Replace `<function_URL>` with the values from the `Gateway Base URL` and `Path Suffix` fields, separated by a forward slash (`/`).

   The URL should look similar to:

   Copy code

   ```
   https://<gateway-base-url>/<path-suffix>
   ```
2. If you haven’t already, execute the CREATE EXTERNAL FUNCTION command that you entered.

## Test your external function

You should now be able to call your external function to verify that it works correctly.

Note

If you added a security definition to the configuration file to secure your gateway in [Step 2: Create the proxy service (Google Cloud API Gateway) in the console](/sql-reference/external-functions-creating-gcp-ui-proxy-service)
of this tutorial, you will not be able to test your external function until you update the security definitions in the configuration file
in [Step 5: Create a GCP security policy for the proxy service in the console](/sql-reference/external-functions-creating-gcp-ui-security-policy) of this tutorial.

For details, see [Calling an external function for GCP](/sql-reference/external-functions-creating-gcp-call).

## Next step

[Step 5: Create a GCP security policy for the proxy service in the console](/sql-reference/external-functions-creating-gcp-ui-security-policy)
