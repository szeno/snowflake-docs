# Step 3: Create the API integration for Azure in Snowflake

This topic provides instructions for creating an API integration object in Snowflake to work with your proxy service (i.e. Azure API
Management service). The instructions are the same regardless of whether you are using the Azure Portal or ARM template.

## Previous step

Azure Portal:
:   [Step 2: Create the proxy service (Azure API Management service) in the Portal](/sql-reference/external-functions-creating-azure-ui-proxy-service)

ARM template:
:   [Step 2: Use the template to create the remote service (Azure function) and proxy service (API Management service)](/sql-reference/external-functions-creating-azure-template-services)

## Required information

You need the following information to create the API integration for Azure in Snowflake:

- `Azure Function App AD Application ID` (from your tracking worksheet)
- Azure AD Tenant ID (as described in the [Prerequisites](/sql-reference/external-functions-creating-azure-planning#label-preparing-to-create-an-external-function-on-azure) section for planning an external
  function)

## Create the API integration object

Use the [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) command to create the API integration object:

1. Open a Snowflake session, typically a Snowflake web interface session.
2. Execute the USE ROLE command to use the ACCOUNTADMIN role or a role with the CREATE INTEGRATION privilege. For example:

   Copy code

   ```
   use role has_accountadmin_privileges;
   ```
3. Enter a CREATE API INTEGRATION statement. The statement should look similar to the following:

   Copy code

   ```
   create or replace api integration <integration_name>
    api_provider = azure_api_management
    azure_tenant_id = '<tenant_id>'
    azure_ad_application_id = '<azure_application_id>'
    api_allowed_prefixes = ('<url>')
    enabled = true;
   ```

   In the statement:

   1. Replace `<integration_name>` with a unique integration name (e.g. `my_api_integration_name`). The name must follow the rules for
      [Object identifiers](/sql-reference/identifiers).

      In addition, record the integration name in the `API Integration Name` field in your tracking worksheet. You will need the name when
      you execute the CREATE EXTERNAL FUNCTION command later in the creation process.
   2. Replace `<tenant_id>` with your Azure AD Tenant ID.

      As an alternative, you can use your domain (e.g. `my_company.onmicrosoft.com`).
   3. Replace `<azure_application_id>` with the value from the `Azure Function App AD Application ID` field in your tracking worksheet.
   4. For `api_allowed_prefixes`, replace `<url>` with the appropriate URL.

      Usually, this is the URL of the proxy service (i.e. Azure API Management service), in the following format:

      Copy code

      ```
      https://<api_management_service_name>.azure-api.net
      ```

      However, you can restrict the URLs to which this API integration can be applied by appending an appropriate suffix, in which case
      the URL has the following format:

      Copy code

      ```
      https://<api_management_service_name>.azure-api.net/<api_url_suffix>
      ```

      The URL you enter depends on whether you are using the Azure Portal or ARM template to create your external function:

      Azure Portal:
      :   Use the values from the `API Management service name` and `API Management API URL suffix` fields in your
          tracking worksheet. For example, your URL should look similar to:

          Copy code

          ```
          https://my-api-management-svc.azure-api.net/my-api-url-suffix
          ```

          This should match the base URL and suffix from the API Management service **Settings** tab for your imported API. If
          convenient, you can copy the value from the tab instead.

      ARM template:
      :   Use the value from the `API Management URL` field in your tracking worksheet.
4. If you haven’t already, execute the CREATE API INTEGRATION statement you entered.

## Next step

[Step 4: Link the API integration for Azure to the proxy service in the Portal](/sql-reference/external-functions-creating-azure-common-api-integration-proxy-link)
