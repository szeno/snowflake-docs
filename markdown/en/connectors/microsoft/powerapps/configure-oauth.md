# Snowflake Connector for Microsoft Power Platform: Configure the OAuth resource in Microsoft Entra ID

The process for configuring OAuth in Microsoft Entra includes the following steps:

1. Navigate to the [Microsoft Azure Portal](https://portal.azure.com/) and authenticate.
2. Navigate to **Microsoft Entra ID**.
3. Select **App Registrations**.
4. Select **New Registration**.
5. Enter ‘Snowflake OAuth Resource’, or similar value as the **Name**.
6. Verify the **Supported account types** are set to **Single Tenant**.
7. Select **Register**.
8. Select **Expose an API**.
9. Select the link next to **Application ID URI** to add the Application ID URI. The Application ID URI will be in the format *Application ID URI <api://9xxxxxxxxxxxxxxxxxx>*
10. **For Delegated Auth** or **For Service Principal Auth**
11. **For Delegated Auth Only**

    1. Select **Add a Scope** to add a scope representing the Snowflake role.
    2. Select who can consent.
    3. Add a description.
    4. Click **Add Scope** to save.
       Example: *session:scope:analyst* to restrict users having specific roles, and *session:role-any* to allow users of any role.
12. **For Service Principal Auth Only**

    To add a Snowflake role as a role for OAuth flows where the programmatic client requests an access token for itself, follow these steps:

    1. Select **App Roles**.
    2. Select **+Create app role**.
    3. Check **Applications** as “Allowed member types”.
    4. For value enter

       Example: *session:role:analyst* to connect to a specific role, or *session:role-any* for any role which the service user is mapped to.

       Avoid high-privilege roles such as *ACCOUNTADMIN*, *SECURITYADMIN* or *ORGADMIN*.
13. [Optional] If a security integration is already being used in Snowflake with another Microsoft product
    such as PowerBI and with a different claim mapping, the manifest will need to be modified.
    The manifest will need to emit tokens using a different issuer, so that a separate
    security integration in Snowflake with the unique claim mapping can be created.
14. Select **Manifest**.
15. Find the attribute `requestedAccessTokenVersion` and set the value to “2”.

    - When *requestedAccessTokenVersion* is set to “2”, the Access Token is going to have an issuer of format: `https://login.microsoftonline.com/<Tenant-ID>/v2.0`
    - When *requestedAccessTokenVersion* is set to “1”, the Access Token is going to have an issuer of format: `https://sts.windows.net/<tenant-ID>/`
16. Select **Save**.

## Next steps

After completing these procedures, follow the steps in [Snowflake Connector for Microsoft Power Platform: Create OAuth client in Microsoft Entra ID](/connectors/microsoft/powerapps/create-oauth-client).
