# Step 4: Link the API integration for Azure to the proxy service in the Portal

When an external function is called, Snowflake sends an HTTP POST command to the proxy service (i.e. Azure API Management service), which
relays the POST to the remote service (i.e. Azure Functions). A service principal in your Azure AD tenant allows Snowflake to
authenticate with Azure AD when calling the API Management service in your tenant.

This topic provides instructions for creating a service principal to link the API integration you created in the previous step with
your Azure API Management service. The instructions are the same regardless of whether you are using the Azure Portal or ARM template.

For more information about service principals, see the Microsoft documentation:
[Applications and service principals](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals#service-principal-object).

## Previous step

[Step 3: Create the API integration for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-api-integration)

## Obtain the app name and consent URL for the API integration

Before you create a service principal, you need some information about the API integration:

1. If you haven’t already, log into the Snowflake web interface.
2. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command for the API integration you created in the previous step:

   Copy code

   ```
   describe api integration <integration_name>;
   ```
3. From the DESCRIBE results:

   - Record the app name (from the AZURE\_MULTI\_TENANT\_APP\_NAME column) in the corresponding field in your tracking worksheet.
   - Record the consent URL (from the AZURE\_CONSENT\_URL column) in the corresponding field in your tracking worksheet.

     The URL looks similar to the following:

     Copy code

     ```
     https://login.microsoftonline.com/<tenant_id>/oauth2/authorize?client_id=<snowflake_application_id>&response_type=code
     ```

## Grant Snowflake access to your Azure tenancy

To grant Snowflake access to your Azure tenancy, you need the AZURE\_CONSENT\_URL that you recorded earlier:

1. Paste the URL into your browser. When your browser resolves this URL, Azure automatically creates a service principal that represents
   Snowflake in the tenant.

   Note that you only need to create a service principal for Snowflake once per tenancy. After Snowflake has been granted access, access
   does not need to be granted again. In other words, you do not need to grant access again for each new external function you create for
   Azure.

   If Snowflake has already been granted access to your Azure tenancy, you should see the Snowflake web site, which should show something
   similar to **SNOWFLAKE THE CLOUD DATA PLATFORM**. You can then skip the remaining tasks and proceed to
   [Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function).

   If Snowflake has not yet been granted access, you should see a Microsoft **Permissions requested** page, and you should continue
   to the next task.
2. Click the **Accept** button. This allows the Azure service principal created for your Snowflake account to obtain an access token
   on any resource inside your Azure AD tenant.

At this point, you have finished creating a service principal in your tenant to represent Snowflake.

However, to enhance security, you should ensure that only authorized clients can access your Azure Function. Instructions for controlling
access are provided in the final step of the creation process.

## Next step

[Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function)
