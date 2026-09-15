# Snowflake Connector for Microsoft Power Platform: Create OAuth client in Microsoft Entra ID

To create an OAuth client in Microsoft Entra ID, follow these steps:

1. Navigate to the [Microsoft Azure Portal](https://portal.azure.com/) and authenticate.
2. Navigate to Azure Active Directory.
3. Select **App Registrations**.
4. Select **New Registration**.
5. Enter a name for the client such as `Snowflake OAuth Client`.
6. Verify the Supported account types are set to `Single Tenant`.
7. Click **Register**.
8. In the **Overview** section, copy the *ClientID* from the **Application (client) ID** field.

   This will be known as the *<OAUTH\_CLIENT\_ID>* in the following steps.
9. Select **Certificates & secrets** » **New client secret**.
10. Add a description of the secret.
11. For testing purposes, select *long-living secrets*.

For Production environments, follow necessary security policies.

12. Select **Add** and copy the secret. This will be known as the *<OAUTH\_CLIENT\_SECRET>* in the following steps.
13. For **Delegated Auth** or **Service Principal Auth**

> 1. For **Delegated Auth**:
>    1. Select **Manage** » **API Permissions**.
>    2. Select **Add Permission**.
>    3. Select **My APIs**.
>    4. Select the **Snowflake OAuth Resource** that was created in [Snowflake Connector for Microsoft Power Platform: Configure the OAuth resource in Microsoft Entra ID](/connectors/microsoft/powerapps/configure-oauth).
>    5. Select the **Delegated Permissions** box.
>    6. Confirm the **Permission** related to the Scopes manually defined in the Application that are to be granted to this client.
>    7. Click **Add Permissions**.
>    8. Click **Grant Admin Consent** to grant the permissions to the client.
>
>       Note
>
>       This method should only be used for testing purposes.
>       In production environments, granting permissions in this manner is not recommended.
>    9. Click **Yes**.
>    10. Click **Manage** » **Authentication**,
>        **add a platform** » **Web and enter Redirect URI’s**
>        `https://global.consent.azure-apim.net/redirect/snowflakev2`

1. For **Service Principal Auth**:
   1. Select **Manage** » **API Permissions**.
   2. Select **Add Permission**.
   3. Select **My APIs**.
   4. Select the **Snowflake OAuth Resource** that was created in [Snowflake Connector for Microsoft Power Platform: Configure the OAuth resource in Microsoft Entra ID](/connectors/microsoft/powerapps/configure-oauth)
   5. Select the **Application Permissions** box.
   6. Confirm the Permission related to the Roles manually defined in the Manifest of the Application that are to be granted to this client.
   7. Select **Add Permissions**.
   8. Click **Grant Admin Consent** to grant the permissions to the client.
      Note that for testing purposes, permissions are configured this way.
      However, in a production environment, granting permissions in this manner is not advisable.
   9. Click **Yes**.

## Next steps

After completing these procedures, follow the steps in [Snowflake Connector for Microsoft Power Platform: Collect Azure AD information for Snowflake](/connectors/microsoft/powerapps/collect-azure-ad-info).
