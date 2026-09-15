# Creating an external function for Azure using an ARM template

These topics provide detailed instructions for using an ARM (Azure Resource Manager) template to create an external function hosted on
Microsoft Azure.

Snowflake provides a sample template that you can start with. This template hides some details of the creation process and hard-codes
some names (e.g. trigger name) and functionality. When you are ready to create your own custom external function, you can either customize
a copy of the template or you can [use the Azure Portal](/sql-reference/external-functions-creating-azure-ui) to create the function.

These topics assume that you are already familiar with the Azure Portal. They describe the general steps that you need to complete,
but do not describe the Portal in detail.

**See also:**

- [Planning an external function for Azure](/sql-reference/external-functions-creating-azure-planning)

**Steps:**

- [Step 1: Create an Azure AD app for the Azure functions app in the Portal](/sql-reference/external-functions-creating-azure-template-apps)
- [Step 2: Use the template to create the remote service (Azure function) and proxy service (API Management service)](/sql-reference/external-functions-creating-azure-template-services)
- [Step 3: Create the API integration for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-api-integration)
- [Step 4: Link the API integration for Azure to the proxy service in the Portal](/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link)
- [Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function)
- [Step 6: Update the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-template-security-policy)
