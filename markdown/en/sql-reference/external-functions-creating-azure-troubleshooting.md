# Troubleshooting external functions for Azure

This topic provides troubleshooting information for external functions for Azure.

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

## Azure-specific issues

### Unable to modify settings during creation of the Azure function

Possible Causes:
:   When creating your Azure Function, you may not be able to modify settings for the function under the
    **Authentication/Authorization** menu.

    This problem can occur if all of the following are true:

    - Your Azure Function is running on Linux rather than Microsoft Windows.
    - You plan to use Azure AD authentication/authorization for your Azure Function.
    - You are using Azure’s “consumption” pricing tier rather than the “premium” pricing tier.

    Azure AD authentication is not available on the Linux Consumption plan for Azure Functions. You must use an App Service plan or
    Premium plan in order to authenticate with Azure AD.

Possible Solutions:
:   - Recreate the Azure Function and specify that it will run on Microsoft Windows rather than Linux.
    - Skip Azure AD authentication/authorization for the Azure Function; instead, perform the following tasks:

      - Set a validate-JWT (JSON Web Token) Policy for the API Management instance as documented in
        [Step 6: Create the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-ui-security-policy).
      - Use IP address restrictions to limit the remote service to accept connections only from the API Management
        service instance.

      If you choose this solution, you must create the Azure AD application manually. For details, see the Microsoft documentation:

      [app registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app) .

      If you create the Azure AD application manually, record the `Azure Function AD app registration name` and
      the `Azure Function App AD Application ID` in your tracking worksheet.
    - Switch from consumption pricing to premium pricing or use an App Service plan. For more details, see the Microsoft documentation:
      [configuring an authentication provider](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-aad)

### External function times out

Possible Causes:
:   There are many possible causes of timeouts. On Azure, one of the possible causes is that the Azure Functions app was not written to scale
    properly.

Possible Solutions:
:   Ensure that you are following the
    [Azure guidelines for writing scalable functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices#scalability-best-practices) .

For more information about troubleshooting scalability and performance issues, see
[Troubleshooting scalability and performance issues](/sql-reference/external-functions-implementation#label-external-functions-troubleshooting-scalability) .

### Error: Failed to obtain Azure active directory access token.

Possible Solutions:
:   Try the following steps:

    - Verify that the Snowflake service principal has access to your Azure AD tenant.
    - Verify that the tenant ID and the Azure AD application ID are correct.

      Note that whitespace, including leading and trailing whitespace (e.g. blanks), is significant in ID fields. Check for incorrect
      leading or trailing whitespace.

### Error: 401 ‘{ “statusCode”: 401, “message”: “Access denied due to missing subscription key…” }’

Full error message text:

Copy code

```
Request failed for external function <function_name>. Error: 401 '{ "statusCode": 401, "message":
"Access denied due to missing subscription key. Make sure to include subscription key when making requests to an API." }'
```

Possible Causes:
:   The API Management service’s subscription requirement might be on.

Possible Solutions:
:   You might need to turn off the subscription requirement for the API Management service.

### Error: 401 ‘{ “statusCode”: 401, “message”: “Access denied due to missing subscription key.” }

Possible Causes:
:   The proxy service requires an [API key](/sql-reference/external-functions-security#label-external-functions-api-key) (aka “subscription key”), typically for authentication
    or billing. However, no API key was supplied in the API\_KEY clause of the CREATE API INTEGRATION command.

Possible Solutions:
:   Use the ALTER API INTEGRATION command to update the API integration with a valid API key.

### Error: 401 ‘{ “statusCode”: 401, “message”: “Access denied due to invalid subscription key.” }’

Possible Causes:
:   The proxy service requires an [API key](/sql-reference/external-functions-security#label-external-functions-api-key) (aka “subscription key”), typically for authentication
    or billing. However, the API key supplied in the API\_KEY clause of the CREATE API INTEGRATION command was not valid.

Possible Solutions:
:   Use the ALTER API INTEGRATION command to update the API integration with a valid API key.

### Error: 401 ‘{ “statusCode”: 401, “message”: “Invalid JWT.” }’

Full error message text:

Copy code

```
Request failed for external function <function_name>. Error: 401 '{ "statusCode": 401, "message": "Invalid JWT." }'
```

Possible Causes:
:   - You might not have finished setting the security policy on the Azure API Management service. For example, you might have:

      - Created, but not edited, the JWT (JSON Web Token).
      - Omitted one or more of the required claims/values. For example, you might have specified the claim for Snowflake but not the
      - remote service (Azure Function), or vice versa.
    - You might have used an invalid open ID URL.

Possible Solutions:
:   - Finish setting the security policy on the Azure API Management service. For example, review the JWT and verify that you included the
      required claims/values, including the claim for Snowflake and the claim for the remote service (Azure Function).
    - Verify that you used a valid open ID URL.

### Error (remote service): 401 ‘{ “statusCode”: 401, “message”: “Invalid JWT.” }’

Full error message text:

Copy code

```
Request failed for external function <function_name> with remote service error: 401 '{ "statusCode": 401, "message": "Invalid JWT." }'
```

Possible Causes:
:   If you used the ARM template, you might not have updated the JWT (JSON Web Token) that the template created for you.

Possible Solutions:
:   Update the JWT as documented in [Step 6: Update the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-template-security-policy).

### Error: 500 …

Possible Causes:
:   You might have chosen the wrong option for your Azure AD app:

    - Incorrect option:
      **Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)**
    - Correct option: **Accounts in this organizational directory only (Default Directory only - Single tenant)**
