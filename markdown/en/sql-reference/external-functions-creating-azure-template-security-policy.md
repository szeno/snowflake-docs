# Step 6: Update the Azure security policy for the proxy service in the Portal

The ARM template provided by Snowflake creates a security policy to validate a JWT (JSON Web Token) that authorizes Snowflake to
call your Azure Function.

However, the security policy is missing one field, which you need to fill in to ensure the policy provides the necessary level of security.

Important

Snowflake strongly recommends updating the security policy for the API Management service. After completing this step, only Snowflake
is allowed to call your Azure Function through the API Management service.

## Previous step

[Step 5: Create the external function for Azure in Snowflake](/sql-reference/external-functions-creating-azure-common-ext-function)

## Update the security policy in the Azure API Management service

To update the policy:

1. If you haven’t already, log into the Azure Portal.
2. Select **API Management Services**.
3. Find the API Management service instance that you created. The name of this instance is recorded in the `API Management service name`
   field in your tracking worksheet.
4. Click on the API Management service instance name.
5. Select **APIs** » **APIs**.
6. Under **All APIs**, select **ext-func-api**.
7. Select **POST echo**.
8. Click on the **validate-JWT** button, which is in the **Inbound processing** box.

   If you do not see this button, please scroll down.
9. Search for “SNOWFLAKE\_SERVICE\_PRINCIPAL\_ID”, and replace it with the Snowflake app ID.

   If you do not already have the Snowflake app ID, you can get it by performing the following steps:

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
10. Click **Save**.

## Test your external function

To make sure that your external function works correctly with the updated security policy, call your external function again.

For details, see [Calling an external function for Azure](/sql-reference/external-functions-creating-azure-call).

## Next step

None. You’ve successfully created an external function for Azure.
