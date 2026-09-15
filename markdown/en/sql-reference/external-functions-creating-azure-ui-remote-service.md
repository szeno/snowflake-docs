# Step 1: Create the remote service (Azure function) in the Portal

This topic provides detailed instructions for creating an Azure Function for use as the remote service for your external function.

## Previous step

[Planning an external function for Azure](/sql-reference/external-functions-creating-azure-planning)

## Create the Azure functions app

There are multiple possible ways to create a remote service. This section shows how to create a remote service that is implemented
as a JavaScript function.

This external function is [synchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-synchronous).
For information about creating an
[asynchronous](/sql-reference/external-functions-implementation#label-external-functions-introduction-miniglossary-asynchronous) external function, see
[Creating an Asynchronous Function on Azure](/sql-reference/external-functions-creating-azure-asynchronous#label-creating-an-asynchronous-function-on-azure).

Create an Azure Functions app to serve as a container for the function(s) that you create later:

1. If you haven’t already, log into the Azure Portal.
2. Create the Azure Functions app by following the instructions in the Microsoft documentation:
   [Azure Functions App](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal).

   As you follow the instructions, remember the following:

   - When you enter a name in the **Function App Name** field, also record the name in the `Azure Function app name` field in
     your tracking worksheet.
   - When asked to choose how to **Publish**, choose **Code**.
   - Some restrictions apply when creating multiple apps in the same resource group. For details, see the Microsoft documentation:
     [Azure app service](https://docs.microsoft.com/en-us/azure/app-service/containers/app-service-linux-intro#limitations).

   Snowflake provides a sample “echo” function in Node.js. To use this sample function to get started:

   - When asked for the `Runtime stack`, select Node.js.
   - When asked for the version of Node.js, select version 12.
   - When asked which OS to run the function on, choose “Windows” or “Linux”.
     - If you are only creating a demo function, Snowflake recommends selecting “Windows”.

       Linux Function Apps cannot be edited in the Azure Portal. Users must publish the code through the Visual Studio Code interface.
     - If you want to run your Azure Function on Linux rather than Microsoft Windows, see the Microsoft documentation:
       [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-vs-code?pivots=programming-language-javascript).

       Azure AD authentication is not available on Linux when using the “Consumption” pricing plan for Azure Functions.
       You must use an “App Service” pricing plan or “Premium” pricing plan in order to authenticate with Azure AD.

       For more details, see the Microsoft documentation:
       [Azure AD](https://docs.microsoft.com/en-us/azure/app-service/configure-authentication-provider-aad).

## Create an HTTP-triggered Azure function

After you create your Azure Functions app (container), you need to create an Azure Function in the container. This function acts as the
remote service.

Microsoft allows Azure Functions to be called (“triggered”) different ways. A Snowflake external function invokes a remote service via an
HTTP POST command, so the Azure Function you create must be an “HTTP-triggered function”.

Tip

You can use the instructions provided by Microsoft to create the HTTP-triggered function:

> - [Create an app portal](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal)
> - [Create an Azure function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function#create-function)

However, Snowflake provides custom instructions that include additional details and sample code, and suggest a different authorization
level than Microsoft. We suggest using the custom instructions in place of Microsoft’s instructions.

### Create the function

To perform the tasks described in this section, you should be in the **Function App** screen in the Azure Portal. The name of your
Azure Functions app should be displayed, typically near the upper left corner of the screen.

To create the HTTP-triggered function:

1. In the left-hand side menu tree, look for the section titled **Functions**. In that section, click on the item
   labeled **Functions** to add a function.
2. Click on the **+ Add** button.
3. Select **HTTP trigger** from the list of potential triggers on the right.
4. Enter the name to use for your HTTP-triggered function.

   Record this name in the `HTTP-Triggered Function name` field in your tracking worksheet.
5. Enter the **Authorization level**.

   Snowflake recommends choosing **Function** as the authorization level.

   For more information about possible authorization levels, see the Microsoft documentation:
   [HTTP-triggered functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=csharp#configuration).
6. Click on the button titled **Add**.

   This takes you to a screen that shows the function name and, below that, the word **Function**.
7. In the tree menu on the left-hand side, click on **Code + Test**.
8. Replace the default code with your own code.

   Sample code for a JavaScript “echo” function is provided below.

   The function reads each row, then copies the row to the output (results). The row number is also included in the output. The output is
   returned as part of a multi-level dictionary.

   This function accepts and returns data in the same format (JSON) that Snowflake sends and reads. For more details about data
   formats, see [Remote Service Input and Output Data Formats](/sql-reference/external-functions-data-format#label-external-functions-data-format).

   Normally, the function returns HTTP code 200. If no rows are passed to the function (that is, if the request body is empty), the function
   returns error code 400.

   Copy code

   ```
   module.exports = async function(context, request) {
    context.log('JavaScript HTTP trigger function processed a request.');

    if (request.body) {
        var rows = request.body.data;
        var results = [];
        rows.forEach(row => {
            results.push([row[0], row]);
        });

        results = {data: results}
        context.res = {
            status: 200,
            body: JSON.stringify(results)
        };
   }
   else {
       context.res = {
           status: 400,
           body: "Please pass data in the request body."
       };
   }
   };
   ```
9. Click on the **Save** button above the code.

### Test the function

To test the HTTP-triggered Azure Function you just created, paste the following sample data into the **Body** field and click on
the **Test/Run** button:

> Copy code
>
> ```
> {
>     "data": [ [ 0, 43, "page" ], [ 1, 42, "life, the universe, and everything" ] ]
> }
> ```

The content of the output should be similar to the following:

> Copy code
>
> ```
> { "data":
>     [
>         [ 0, [ 0, 43, "page" ] ],
>         [ 1, [ 1, 42, "life, the universe, and everything" ]  ]
>     ]
> }
> ```

Note that the formatting might be different from what is shown above.

## Set the authorization requirements for the Azure functions app

When an external function is called, Snowflake sends an HTTP POST command to the proxy service (for example, the Azure API Management service),
which relays the POST to the remote service (for example, the Azure Function).

Each of these two steps should have authorization requirements, so you typically specify:

- The authorization needed to call the API Management service.
- The authorization needed to call functions in the Azure Functions app that contains your Azure Function.

This section describes how to require authorization for your Azure Functions app. The API Management service is created later, so its
authorization requirements are also specified later.

When Snowflake authenticates with your Azure Functions app, Snowflake uses OAuth client credential grant flow with Azure AD.

For more details about the client credential grant flow, see the Microsoft documentation:
[client credential](https://docs.microsoft.com/en-us/azure/active-directory/azuread-dev/v1-oauth2-client-creds-grant-flow).

This client credential flow requires an Azure AD app registration that represents the Azure Functions app.

This section includes instructions for creating the Azure AD app registration for the Azure Functions app. For example, you can set your
Azure Functions app to require Azure AD authentication. To configure authorization via Azure AD, you must:

- Create an Azure AD app registration, which is an Azure AD-based entity that represents
  an identity or resource identifier (that is, what you want to protect).
- Associate the Azure AD app registration with the Azure Functions app for which you want to require authentication.

Note

For Azure Functions, the fastest way to create an Azure AD app registration is by enabling Azure AD Authentication for the service, as
documented below. If you are using a remote service other than an Azure Function, use the **App registrations** page to create
a new Azure AD app registration for your remote service.

For more details about app registration, see the Microsoft documentation:

> [app registration documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

### Enable app service authentication for the Azure functions app

Before you execute the steps below, you should be on the **Function App** screen for your Azure Functions app.

1. In the left-hand menu pane, look for the section named **Settings** and click on **Authentication**.

   If the left-hand margin shows the **Developer** menu (with **Code + Test**, **Integration**, etc.), if you have a scroll
   bar at the bottom of your screen, try sliding the scroll bar to the left to return to the **Function App**
   or **App Service** section, and then look for **Settings**.
2. Click the **Add identity provider** button.
3. In the **Identity provider** drop-down menu, select **Microsoft**.
4. For **App registration type**, select **Create new app registration**.
5. In the **Name** field, type the name of your app.
6. For **Supported account types**, select **Current tenant - Single tenant**.
7. For **Restrict access**, select **Require authentication**.
8. For **Unauthenticated requests**, select **HTTP 401 Unauthorized**.
9. Click **Next: Permissions**. Review the permissions.
10. Click **Add**. A new Azure AD application is created and the application page is displayed.
11. Click the link that shows your application’s name to go to your Azure AD application’s page.
12. Find the **Application (client) ID** field.

Record this ID in the **Azure Function App AD Application ID** field in your tracking worksheet.

Important

Make sure you copy the ID, not the Azure AD application name. The ID should contain a UUID.

## Next step

[Step 2: Create the proxy service (Azure API Management service) in the Portal](/sql-reference/external-functions-creating-azure-ui-proxy-service)
