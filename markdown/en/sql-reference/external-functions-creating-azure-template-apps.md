# Step 1: Create an Azure AD app for the Azure functions app in the Portal

This topic provides detailed instructions for creating an Azure AD app for the Azure Functions app.

## Previous step

[Planning an external function for Azure](/sql-reference/external-functions-creating-azure-planning)

## Create an Azure AD app

1. If you haven’t already, log into the Azure Portal.
2. Search for the **App registrations** page.
3. Click on **New registration**, which takes you to the **Register an application** screen.
4. Enter a unique name for your Azure AD app.
5. Record the name of the Azure AD app in the `Azure Function AD app registration name` field in your tracking worksheet.
6. Under **Supported account types**, choose
   **Accounts in this organizational directory only (Default Directory only - Single tenant)**.
7. Click on **Register**.

   This takes you to the **Home** » **App registrations** screen and shows the newly created Azure AD
   app.
8. Record the **Application (client) ID** from the Azure AD app you just created in the `Azure Function AD Application ID` field in
   your tracking worksheet. This ID should be in the form of a UUID.

## Next step

[Step 2: Use the template to create the remote service (Azure function) and proxy service (API Management service)](/sql-reference/external-functions-creating-azure-template-services)
