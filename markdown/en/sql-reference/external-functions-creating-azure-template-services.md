# Step 2: Use the template to create the remote service (Azure function) and proxy service (API Management service)

This topic provides detailed instructions for using the ARM template provided by Snowflake. The template simplifies the tasks for
creating the Azure Function (to use as the remote service) and API Management service (to use as the proxy service) for your
external function.

## Previous step

[Step 1: Create an Azure AD app for the Azure functions app in the Portal](/sql-reference/external-functions-creating-azure-template-apps)

## Import the template

Before you can use the template, you have to import it into the Azure Portal:

1. If you haven’t already, log into the Azure Portal.
2. In the Azure search bar, search for **Template**.
3. Under **Services**, click on **Deploy a custom template**.
4. Select **Build your own template in the editor**.
5. Select **Load file**.
6. Navigate to the directory on the machine where you downloaded the template, then select that template.
7. Click **Save**.

This takes you to the **Custom deployment** screen.

## Create the Azure function and API Management service

In the **Custom deployment** screen:

1. Select an existing (or create a new) **Resource group**.

   Tip

   If you create a new resource group solely for this demonstration, then you might want to record
   the name so that you can delete it later when you are done with it.
2. Select the appropriate **Region**.
3. Enter an **API Management Service Name**.
4. Record the API Management Service name in the `API Management service name` field in your tracking worksheet.
5. In the **Function App Name** field, enter a unique name.
6. Record the Function App Name in the `Azure Function app name` field in your tracking worksheet.
7. In the **Publisher email** field, enter your email address. Microsoft uses this email to notify you after the API Management
   service has been created.
8. In the **Azuread Application Id** field, enter the ID of the Azure AD application you created earlier. This is the value in the
   `Azure Function AD Application ID` field in your tracking worksheet.
9. Click on **Review + create**.
10. Click on **Create**.

Creating the Azure Functions app and API Management service typically takes approximately half an hour.

## Obtain the required URLs for the API integration and external function

To create the API integration and external function in Snowflake, you need the API Management service’s URL, which you can find by
following the steps below after Azure has finished creating the API Management service.

At this point, the Azure Portal should show the message **Your deployment is complete** and should show the **Deployment name**.

1. Click on **Outputs** in the left-hand column.
2. Record the **api Management URL** in the `API Management URL` field in your tracking worksheet.
3. Record the **azure Function Http Trigger URL** in the `Azure Function HTTP Trigger URL` field in your tracking worksheet.

## Next step

[Step 3: Create the API integration for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-api-integration)
