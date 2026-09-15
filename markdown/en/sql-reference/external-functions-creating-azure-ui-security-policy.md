# Step 6: Create the Azure security policy for the proxy service in the Portal

The previous steps allow your imported APIs (and Azure Function) to be called by Snowflake, as well as other authenticated clients, such
as applications that are in your Azure AD tenant or have a service principal in your Azure AD tenant.

If you want to allow only Snowflake to call the Azure Function, you must implement token validation. With token validation, when Snowflake
tries to access the API Management service, Snowflake presents a JWT (JSON Web Token) access token obtained from Azure AD. The API Management service can
either validate the JWT or pass it through without validation.

This topic provides instructions for creating a security policy for the API Management service by adding a validate-JWT policy that
defines the rules for validating the token.

Important

Snowflake strongly recommends creating a security policy for the API Management service. After completing this step, only Snowflake
is allowed to call your Azure Function through the API Management service.

If you prefer to use role-based validation in your validate-JWT policy, see the Microsoft Service Principal documentation for assigning
a role to a service principal:
[New-AzureADServiceAppRoleAssignment](https://docs.microsoft.com/en-us/powershell/module/azuread/new-azureadserviceapproleassignment).

## Previous step

[Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function)

## Create a validate-JWT policy that allows Snowflake to call the Azure function

This section shows how to specify a policy for validating a JSON Web Token (JWT) that authorizes Snowflake to call your Azure Function.
The validation policy (“validate-JWT policy”) validates the following two claims in the JWT:

- The Snowflake service principal application ID.
- The target application App ID (the “audience ID” or just “aud”) of the Azure Function.

For more information about claims in JSON Web Tokens (JWTs) issued by Azure Active Directory, see the Microsoft documentation:
[access tokens](https://docs.microsoft.com/en-us/azure/active-directory/develop/access-tokens#claims-in-access-tokens).

The following steps configure the imported API to use a JSON Web Token:

1. If you haven’t already, log into the Azure Portal.
2. Go to the **API Management service** screen.
3. Select your API Management service.
4. Find the **APIs** section in the left-hand column, then click on the **APIs** option under that.
5. In the column that contains **All APIs**, click on the name of the API for which you want to add a security
   policy.
6. Look for **In-bound Processing**:

   1. Click on **+ Add policy**.
   2. Click on **validate-jwt**.
   3. Fill in the **Header name** with the value `Authorization`.
   4. Add validation for the JWT (JSON Web Token) provided by Snowflake for accessing the Azure Function:

      1. Look for **Required claims** and click on **+ Add claim**.
      2. Fill in the **Name** field with `aud` (short for “audience”).
      3. Within the required claim, Look for **Values** and click on **+Add value**.

         Add the UUID that you copied to the azure\_ad\_application\_id field in the CREATE API INTEGRATION command. This is recorded in
         the `Azure Function App AD Application ID` field of your tracking worksheet.
   5. Add a separate “claim” for Snowflake:

      1. Click on **+ Add claim** again:
      2. Fill in the **Name** field with the literal string `appid`.
      3. Within the claim, click on **+ Add value** and add the Snowflake Application ID in the **Values** field.

         If you do not already have the Snowflake Application ID, you can get it by performing the following steps
         (the Snowflake Application ID is in the **Application ID** field):

         > 1. In the worksheet, find the AZURE\_MULTI\_TENANT\_APP\_NAME that you filled in earlier.
         > 2. In the Azure Portal search box, look for **Enterprise Applications**.
         >
         >    This takes you to the **Enterprise applications | All applications** screen.
         > 3. In that screen, search for the AZURE\_MULTI\_TENANT\_APP\_NAME.
         >
         >    The enterprise applications search box does not have a label. Look for a wide field immediately
         >    above the list of enterprise applications. The box might say something similar to
         >    **First 50 shown, to search all of your applications, enter a display name or the application ID**.
         >
         >    If you do not find an exact match for the AZURE\_MULTI\_TENANT\_APP\_NAME, then search again using only
         >    the first several characters of this name (if the name contains an underscore, then do not include the
         >    underscore or any characters after the underscore).
         > 4. Find the **Application ID** value for the AZURE\_MULTI\_TENANT\_APP\_NAME.
7. Paste the following into **Open ID URLs**:

   `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration`

   Replace the `<tenant_id>` with your Azure AD Tenant ID (as described in the
   [Prerequisites](/sql-reference/external-functions-creating-azure-planning#label-preparing-to-create-an-external-function-on-azure) section for planning an external function).
8. Click on **Save**.

## Test your external function

To make sure that your external function works correctly with the new security policy, call your external function again.

For details, see [Calling an external function for Azure](/sql-reference/external-functions-creating-azure-call).

## Restrict the IP addresses that accept Azure functions calls (optional)

In addition to specifying a validate-JWT policy (or using role-based validation), you can implement additional security by restricting IP
addresses. This ensures that only the API Management service’s IP address is allowed to access the Azure Functions app containing your Azure
Function.

For more information about restricting IP addresses, see the Microsoft documentation:
[In-bound IP address restrictions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options#inbound-ip-restrictions).

## Next step

None. You’ve successfully created an external function for Azure.
