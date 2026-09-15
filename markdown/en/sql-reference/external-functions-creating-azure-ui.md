# Creating an external function for Azure using the Azure Portal

These topics provide detailed instructions for using the Azure Portal user interface to create an external function hosted on
Microsoft Azure. You can use these instructions either to create the sample external function provided by Snowflake or as a guide to
create your own external function.

In these topics, you will learn how to:

- Create a basic Azure Function as a remote service and an Azure API Management service as a proxy service.
- Create an API integration and the external function itself in Snowflake.
- Link the API integration to the API Management service.
- Secure the API Management service through a security policy.

These topics assume that you are already familiar with the Azure Portal. They describe the general steps that you need to complete,
but do not describe the Portal in detail.

**See also:**

- [Planning an external function for Azure](/sql-reference/external-functions-creating-azure-planning)

**Steps:**

- [Step 1: Create the remote service (Azure function) in the Portal](/sql-reference/external-functions-creating-azure-ui-remote-service)
- [Step 2: Create the proxy service (Azure API Management service) in the Portal](/sql-reference/external-functions-creating-azure-ui-proxy-service)
- [Step 3: Create the API integration for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-api-integration)
- [Step 4: Link the API integration for Azure to the proxy service in the Portal](/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link)
- [Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function)
- [Step 6: Create the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-ui-security-policy)
