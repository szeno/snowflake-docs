# Private connectivity with external functions: Azure Portal

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up outbound private connectivity to an external service by calling an external function
for Snowflake accounts on Microsoft Azure as follows:

- Use the Azure Portal user interface to configure resources in Microsoft Azure.
- Create an API integration and external function in Snowflake.
- Call the external function in Snowflake to validate private connectivity to the external service.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Process overview

The following is a general overview of the configuration process. Steps in Snowflake must be done by a user with the ACCOUNTADMIN role.
Steps in the Azure Portal are done by a user with rights to use the corresponding resources unless otherwise specified.

The following steps are the same as using external functions with the public Internet:

1. Complete the prerequisite steps for external functions on Microsoft Azure.
2. In the Azure Portal, create the remote service.
3. In the Azure Portal, create the proxy service.

However, you might want to create new resources to fully differentiate your private connectivity needs from your public Internet needs.
Consult with your internal security administrators to determine the best approach for your needs.

These steps are unique to external functions that use private connectivity for an external service:

1. In Snowflake, create a private endpoint.

   Snowflake stores the private IP address for the private endpoint internally.
2. In the Azure Portal, approve the private endpoint.

   This action is done by the owner of the Azure API Management resource (external service).
3. In Snowflake, create a new API integration.

   You need a dedicated API integration to support private connectivity to the external service.
4. In Snowflake, create an external function. The private connectivity URL is the value for the invocation URL in the external function.
5. In Snowflake, call the external function to enable Snowflake to connect to the external service using private connectivity.
6. Deprovision any private connectivity endpoints that are not necessary.

## Configuration

Complete these steps in the Azure Portal:

1. If you already have the Azure API Management resource set up and you want to reuse the remote service and proxy service, skip to the
   private connectivity steps. Otherwise, complete these steps:
2. Complete the [prerequisites](/sql-reference/external-functions-creating-azure-planning) for external functions on Microsoft Azure.
3. In the Azure Portal, [create the remote service](/sql-reference/external-functions-creating-azure-ui-remote-service).
4. In the Azure Portal, [create the proxy service](/sql-reference/external-functions-creating-azure-ui-proxy-service).

Complete these steps to configure private connectivity:

1. In Snowflake, run the [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) command to create a new API integration to support private
   connectivity to the external service. Update the property values to align with your Microsoft Azure subscription:

   Copy code

   ```
   CREATE API INTEGRATION external_api_integration_azure_private
     API_PROVIDER = azure_private_api_management
     AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
     AZURE_AD_APPLICATION_ID = 'dv3421nq-1g4s-4ap4-x89c-xrf28hna7m2o'
     API_ALLOWED_PREFIXES = ('https://aztest1-external-function-api.azure.net')
     ENABLED = TRUE
     COMMENT = 'API integration for private connectivity to an external service with external functions on Azure.';
   ```
2. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to create the private
   endpoint. Update the argument values to align with your Microsoft Azure subscription:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     '/subscriptions/f4b00c5f-f6bf-41d6-806b-e1cac4f1f36f/resourceGroups/aztest1-external-function-rg/providers/Microsoft.ApiManagement/service/aztest1-external-function-api',
     'aztest1-external-function-api.azure.net',
     'Gateway'
     );
   ```
3. In the Azure Portal and as the owner of the Azure API Management resource, approve the private endpoint. For details, see the [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).
4. [Link the API Integration for Azure to the proxy service](/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link) to enable Snowflake to send API requests to the Azure API Management
   service.
5. You can choose to block public access to the Azure API Management resource. For more information, see
   `Secure access to the Azure API Management resource`\_ (in this topic).
6. In Snowflake, if you already have a database and schema to store the external function and want to use these objects, be sure these
   objects are [in use](/sql-reference/sql/use) or select them in Snowsight. Otherwise, create a database and schema to
   store the external the external function for use with private connectivity to an external service:

   Copy code

   ```
   CREATE DATABASE private_external_service_db;
   CREATE SCHEMA private_ext_functions;
   ```
7. In Snowflake, run the [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) command to create the external function to use with
   private connectivity to the external service. Be sure to update the invocation URL with the external service private connectivity URL:

   Copy code

   ```
   CREATE OR REPLACE SECURE EXTERNAL FUNCTION private_ext_function_azure_portal(
     a INTEGER , b VARCHAR)
     RETURNS VARIANT
     API_INTEGRATION = external_api_integration_azure_private
     AS 'https://aztest1-external-function-api.azure.net/my-api-url-suffix/http-function-name';
   ```

   The URL format depends on whether you are creating an external function using the Azure Portal or the Azure ARM template. For
   details, see [invocation URL format](/sql-reference/external-functions-creating-azure-common-ext-function#label-external-function-invocation-url-format).
8. In Snowflake, call the external function to test private connectivity to the external service:

   Copy code

   ```
   SELECT private_ext_function_azure(66, 'Mario');
   ```

   ```
   [0, 66, 'Mario']
   ```

If the output of the function returns the result that matches the configuration of the remote service at the beginning of the procedure,
then you confirmed that private connectivity to the external service is working as expected.

## Secure access to the Azure API Management resource

You can secure the access to the Azure API Management resource that is associated with the private endpoint for use with external functions.
From the perspective of the Azure API Management resource, Snowflake is an inbound connection. By securing the access, you reduce the
likelihood of attacks that might compromise your use of external functions.

For example, you might want to run this Azure CLI
[apim command](https://learn.microsoft.com/en-us/cli/azure/apim?view=azure-cli-latest#az-apim-update) to block public access:

Copy code

```
az apim update --name <api-name> --resource-group <resource group name> --public-network-access false
```

Update the placeholder values with the values that correspond to the name of the API Management resource and the name of the resource group.

For details and options, see these topics:

- [Use a virtual network to secure inbound and outbound traffic for Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/virtual-network-concepts?tabs=stv2).
- [Connect privately to API Management using an inbound private endpoint](https://learn.microsoft.com/en-us/azure/api-management/private-endpoint).
