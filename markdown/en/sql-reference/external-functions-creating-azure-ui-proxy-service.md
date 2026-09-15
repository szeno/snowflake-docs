# Step 2: Create the proxy service (Azure API Management service) in the Portal

Snowflake does not send data (HTTP POST requests) directly to a remote service. Instead, Snowflake sends the data to a proxy service that
relays the data from Snowflake to the remote service (i.e. Azure Function) and back again.

This topic provides instructions for creating and configuring an Azure API Management service for use as the proxy service for your
external function.

## Previous step

[Step 1: Create the remote service (Azure function) in the Portal](/sql-reference/external-functions-creating-azure-ui-remote-service)

## Create the API Management service

The first step is to create the API Management service in the Azure Portal:

1. If you haven’t already, log into the Portal.
2. To create the API Management service, follow the instructions provided in the Microsoft documentation:
   [Create an API Management service](https://docs.microsoft.com/en-us/azure/api-management/get-started-create-service-instance).

   As you perform the tasks described in the instructions, remember to record the API Management service name (which might be titled
   **Resource name**) in the `API Management service name` field in your tracking worksheet.

   Note

   Deploying the API Management service can take 30-40 minutes or more. When deployment completes, you should see a message similar
   to **Your deployment is complete**.
3. After the deployment completes, click the **Go to resource** button.

## Import the API containing the Azure function

After you create the API Management service, the next step is to import and publish the Azure Functions app that contains the APIs
(functions) to call through that API Management service:

1. To import and publish an Azure Function, follow the instructions provided in the Microsoft documentation:
   [Import a function app](https://docs.microsoft.com/en-us/azure/api-management/import-function-app-as-api).

   This document includes instructions for other tasks, as well as importing APIs. For this demonstration, you typically need only the
   instructions for importing an Azure Functions app as a new API.

   As you perform the tasks described in the instructions, remember the following:

   - One of the steps requires that you specify an option for **Product**. For this demonstration, choose **Starter** rather
     than **Unlimited**. For a production system, you might choose differently.
   - Record the **API URL suffix** in the `API Management API URL suffix` field in your tracking worksheet.

   After completing the tasks to import an Azure Functions app, you should be back on the **API Management service** page.
2. Find and click on the **Settings** tab, which is next to the **Design** tab on the panel of the screen
   below your API’s revision number (e.g. **REVISION 1**).
3. If the **Subscription Required** checkbox has a checkmark, then uncheck it unless you want to require a subscription.

   If you do not see the **Subscription** section, scroll down.
4. Click the **Save** button.

Note

Snowflake strongly recommends
[creating a security policy on the Azure API Management service](/sql-reference/external-functions-creating-azure-ui-security-policy).

You can create the security policy now or you can finish creating the external function first and test the external function before
creating the security policy. To simplify debugging, this topic finishes creating and testing the external function before creating
the security policy.

## Next step

[Step 3: Create the API integration for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-api-integration)
