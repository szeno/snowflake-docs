# Step 5: Create the external function for Azure in Snowflake

This topic provides instructions for creating an external function object in Snowflake. This object stores information about the remote
service, such as the parameters that the remote service accepts. The instructions are the same regardless of whether you are using the
Azure Portal or ARM template.

Note

External functions in Snowflake are database objects, meaning they must be created in a schema in a database. To create an external
function, you must have the appropriate privileges on the database and schema where you are creating the function.

For more details, see [Access control privileges](/user-guide/security-access-control-privileges).

## Previous step

[Step 4: Link the API integration for Azure to the proxy service in the Portal](/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link)

## Create the external function

This task assumes you are in the **Worksheets** [![Worksheet tab](/static/images/screens/ui-navigation-worksheet-icon.svg)](/static/images/screens/ui-navigation-worksheet-icon.svg) page in Snowsight:

1. Enter a [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) statement. The statement should look similar to the following:

   Copy code

   ```
   create or replace external function <external_function_name>(<parameters>)
    returns variant
    api_integration = <api_integration_name>
    as '<invocation_url>';
   ```
2. Replace `<external_function_name>` with a unique function name (e.g. `echo`). This name must follow the rules for
   [Object identifiers](/sql-reference/identifiers).

   In addition, record the function name in the `External Function Name` field in your tracking worksheet.
3. Replace `<parameters>` with the names and SQL data types of the parameters for the function, if any.

   The parameters must correspond to the parameters expected by the remote service. The parameter names do not need to match, but the
   data types need to be compatible.

   If your Azure Function uses the sample JavaScript code provided in Step 1, then the parameters are an INTEGER and a VARCHAR. For
   example:

   Copy code

   ```
   a integer, b varchar
   ```

   In addition, record the parameter names and data types in the `External Function Name` field in your tracking worksheet.
4. Replace `<api_integration_name>` with the value from the `API Integration Name` field in your tracking worksheet.
5. Replace `<invocation_url>` with the appropriate URL. This is the URL to which Snowflake sends the HTTP POST command in order to
   call the remote service and has the following format:

   Copy code

   ```
   https://<api_management_service_name>.azure-api.net/<api_url_suffix>/<http_triggered_function_name>
   ```

   The URL you use depends on whether you are using the Azure Portal or ARM template to create your external function:

   Azure Portal:
   :   Use the values from the `API Management service name`, `API Management API URL suffix`, and
       `HTTP-Triggered Function name` fields in your tracking worksheet. For example, your URL should look similar to:

       Copy code

       ```
       https://my-api-management-svc.azure-api.net/my-api-url-suffix/my_http_function
       ```

   ARM template:
   :   Use the value from the `Azure Function HTTP Trigger URL` field in your tracking worksheet.
6. If you haven’t already, execute the CREATE EXTERNAL FUNCTION command that you entered.

## Test your external function

You should now be able to call your external function to verify that it works correctly.

For details, see [Calling an external function for Azure](/sql-reference/external-functions-creating-azure-call).

## Next step

Azure Portal:
:   [Step 6: Create the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-ui-security-policy)

ARM template:
:   [Step 6: Update the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-template-security-policy)
