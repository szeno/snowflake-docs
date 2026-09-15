# Planning an external function for Azure

This topic helps you prepare to create an external function for Microsoft Azure using either the Azure Portal or an ARM (Azure Resource
Manager) template provided by Snowflake.

## Prerequisites

These instructions assume that you are an experienced Azure Portal user.

To create an external function for Azure, you must have the following:

- An Azure AD (Active Directory) tenant.
- An account in that Azure AD tenant. The account must have privileges to:

  - Create an Azure Functions app.
  - Create a service endpoint using Azure API Management service.
  - Register an Azure AD Application.
- A Snowflake account in which you have the ACCOUNTADMIN role or a role with the CREATE INTEGRATION privilege.

In addition, you should already have an Azure AD Tenant ID.

The Azure AD Tenant ID is a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) , which typically is formatted to look
similar to `12345678-abcd-1234-efab-123456789012`, where each non-dash character is a hexadecimal digit.

If you do not already know your Azure AD tenant ID, you can find it using the following procedure:

1. Log into the Azure Portal (<http://portal.azure.com>).
2. In the **Azure services** icons near the top of the page, click on **Azure Active Directory**.
3. In the menu on the left-hand side, look for the section titled **Manage**, then click on **Properties** under that.

The Azure AD tenant ID is displayed in the **Tenant ID** field.

## Public Internet or private connectivity

When you call an external function, the connectivity from Snowflake to the external service can go through the public Internet or use
[Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview) (Microsoft documentation). The choice to
use Azure Private Link depends on your security requirements in terms of how you need to connect to the external service. Using Azure
Private Link can help you meet your security requirements.

If you choose to use the public Internet, finish the remainder of this topic and follow the numbered topics for creating an external
function on Azure using the Azure Portal or the ARM template.

If you choose to use Azure Private Link, the configuration process requires using the ACCOUNTADMIN role and a Snowflake account that is
Business Critical Edition (or higher). There is an additional billing charge to use Azure Private Link. Finish the remainder of this topic and review these topics for more information:

- [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound)
- [Manage private connectivity endpoints: Azure](/user-guide/private-manage-endpoints-azure)
- [Private connectivity with external functions: Azure ARM template](/sql-reference/external-functions-creating-azure-template-private-connect) (includes billing section)
- [Private connectivity with external functions: Azure Portal](/sql-reference/external-functions-creating-azure-ui-private-connect) (includes billing section)

## Choosing the method for creating the external function

Snowflake provides instructions for two ways to create an external function on Azure:

- Azure Portal web interface
- ARM (Azure Resource Manager) template provided by Snowflake

### Azure portal

You can use the [Azure Portal](https://azure.microsoft.com/en-us/features/azure-portal/) to create an Azure Function (as the remote
service) and an API Management service instance (as the proxy service). If you choose this method, you also use the Azure Portal to
configure security-related settings.

The instructions for creating an external function using the Azure Portal include a sample Azure Function and details for creating a basic
API Management service instance:

- First-time users can use the instructions and sample Azure Function with little or no modification.
- Experienced users can use the instructions and sample Azure Function as a starting point for creating a custom Azure Function and a
  custom-configured API Management service instance.

### ARM (Azure Resource Manager) template

An [ARM template](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/overview) uses [JSON](https://www.json.org/) to describe
configuration information about an Azure Function (as the remote service) and an Azure API Management service instance (as the proxy
service).

Snowflake provides a sample ARM template that includes the following:

- Sample Azure Function.
- Most of the configuration information for a sample API Management service. You must enter some additional information if you wish to
  customize the sample API Management service.
- Code to create a storage account needed by the Azure Functions service.
- Code to add a validate-JWT (JSON Web Token) Policy to the API Management instance in order to increase security of the Azure API
  Management service. However, you must manually update the validate-JWT policy before using it.

ARM templates can be useful for both first-time and experienced users:

- First-time users might want to start with the Snowflake sample template because it reduces the number of steps required to create the
  Azure Function and the API Management service instance.

  Note that although the template-based instructions help you create your first external function quickly, they skip steps that
  most users need when creating customized external functions.
- Experienced users might want to use ARM templates because templates can be used to automate deployment. This can be useful if you are
  developing an Azure Function and API Management service iteratively.

For more information about configuring Azure Functions using ARM templates, see the Microsoft documentation:
[resource deployment](https://docs.microsoft.com/en-us/azure/azure-functions/functions-infrastructure-as-code) .

## Preparing to use the Azure portal

These sections help you prepare to use the Azure Portal to create an external function on Microsoft Azure.

### Choose the pricing plan for your Azure function

In Microsoft Azure, an Azure Function (remote service) can run on a Linux host or Windows host. At this time, Azure offers different
combinations of pricing and authentication options for Linux and Windows hosts.

If you plan to run your Azure Function on Linux, then you must choose a valid combination of Azure pricing plan and authentication:

- If you use the Premium or App Service pricing plan:

  - Create the Azure AD (Active Directory) application from the **Authentication/Authorization** tab on the **Azure Functions**
    screen in the Azure Portal.
  - Use Azure AD for authentication with the Azure Functions service.

  Additional details and links are provided later in the
  [instructions for creating a remote service](/sql-reference/external-functions-creating-azure-ui-remote-service#label-set-authorization-requirements-for-azure-function-app).
- If you use the Consumption pricing plan:

  - Manually create the Azure AD application in the Azure Portal. Additional details are provided later in the
    [instructions for creating a remote service](/sql-reference/external-functions-creating-azure-ui-remote-service#label-set-authorization-requirements-for-azure-function-app).
  - Set a validate-JWT policy for the API Management instance. For details, see [Step 6: Create the Azure security policy for the proxy service in the Portal](/sql-reference/external-functions-creating-azure-ui-security-policy).
  - Use IP address restrictions to limit the remote service to accept connections only from the API Management service instance. For
    details, see [Restrict the IP addresses that accept Azure functions calls (optional)](/sql-reference/external-functions-creating-azure-ui-security-policy#label-restrict-ip-addresses-that-call-the-remote-service).

### Create a worksheet for tracking required information

As you complete the tasks to create an external function in the Azure Portal, you are required to enter specific values
(e.g. API Management service name) during each step in the process. Often, the values you enter are required in subsequent steps.

To facilitate recording/tracking this information, we’ve provided a worksheet with fields for each of the required values:

Copy code

```
================================================================================
======================= Tracking Worksheet: Azure Portal =======================
================================================================================

****** Step 1: Azure Function (Remote Service) Info ****************************

Azure Function app name: _______________________________________________________
HTTP-Triggered Function name: __________________________________________________
Azure Function AD app registration name: _______________________________________
Azure Function App AD Application ID: __________________________________________

    (The value for the Azure Function App AD Application ID above is the
    "Application (client) ID" of the Azure AD app registration for the
    Azure Function. The value is used to fill in the "azure_ad_application_id"
    field in the CREATE API INTEGRATION command. This value is in the form of a
    UUID (universally unique identifier), which contains hexadecimal digits and
    dashes.)

****** Step 2: Azure API Management Service (Proxy Service) Info ***************

API Management service name: ___________________________________________________
API Management API URL suffix: _________________________________________________

****** Steps 3-5: API Integration & External Function Info *********************

API Integration Name: __________________________________________________________
AZURE_MULTI_TENANT_APP_NAME: ___________________________________________________
AZURE_CONSENT_URL: _____________________________________________________________

External Function Name: ________________________________________________________
```

## Preparing to use the ARM template

These sections help you prepare to use the ARM template provided by Snowflake to create an external function on Microsoft Azure.

### Download the template

The template is available to download from the
[Snowflake repository in GitHub](https://github.com/Snowflake-Labs/sfguide-external-functions-examples/tree/main/DeploymentTemplates/azure/BasicSetup.json).

Before you can use the template, you must import it into the Azure Portal. Details for importing the template are included later in the
topic that describes using the template.

### Choose the pricing plan for your Azure function

In Microsoft Azure, an Azure Function (remote service) can run on a Linux host or Windows host. At this time, Azure offers different
combinations of pricing and authentication options for Linux and Windows hosts.

The Snowflake-provided ARM template defaults to using the following pricing plan and authentication information:

- Defaults to using a Windows host for the Azure Function.
- Defaults to the “Consumption” pricing tier.
- Creates an Azure Functions app, and configures that app to require AD (Active Directory) authentication.
- Creates a security policy to validate a JWT (JSON Web Token) that authorizes Snowflake to call your
  Azure Function.

  Note that this security policy is missing one field; instructions provided later tell you how to fill in this field.

If you plan to run your Azure API management instance or Azure Function with a different configuration, you must update the
template. For information about updating the template, see the Microsoft documentation:

- [Automating resource deployment](https://docs.microsoft.com/en-us/azure/azure-functions/functions-infrastructure-as-code)
  (for your function app in Azure Functions)

### Create a worksheet for tracking required information

As you complete the tasks to create an external function using the ARM template provided by Snowflake, you are required to enter specific
values (e.g. API Management service name) during each step in the process. Often, the values you enter are required in subsequent steps.

To facilitate recording/tracking this information, we’ve provided a worksheet with fields for each of the required values:

Note

For information hard-coded in the ARM template, the values have already been filled in.

Copy code

```
================================================================================
======================= Tracking Worksheet: ARM Template =======================
================================================================================

****** Step 1: Azure Function (Remote Service) Info ****************************

HTTP-Triggered Function name: __________________ echo __________________________
Azure Function AD Application ID: ______________________________________________

    (The value for the Azure Function AD Application ID above is the
    "Application (client) ID" of the Azure AD app registration for the
    Azure Function. The value is used to fill in the "azure_ad_application_id"
    field in the CREATE API INTEGRATION command. This value is in the form of a
    UUID (universally unique identifier), which contains hexadecimal digits and
    dashes.)

****** Step 2: Azure API Management Service (Proxy Service) Info ***************

API Management service name: ___________________________________________________
API Management URL: ____________________________________________________________
Azure Function HTTP Trigger URL: _______________________________________________
API Management API URL suffix: _________________________________________________

****** Steps 3-5: API Integration & External Function Info *********************

API Integration Name: __________________________________________________________
AZURE_MULTI_TENANT_APP_NAME: ___________________________________________________
AZURE_CONSENT_URL: _____________________________________________________________

External Function Name: ________________________________________________________
```

## Next step

Azure Portal:
:   [Step 1: Create the remote service (Azure function) in the Portal](/sql-reference/external-functions-creating-azure-ui-remote-service)

ARM template:
:   [Step 1: Create an Azure AD app for the Azure functions app in the Portal](/sql-reference/external-functions-creating-azure-template-apps)
