# Snowflake Connector for Microsoft Power Platform: Create a security integration

The *external\_oauth\_audience\_list* parameter of the security integration must
exactly match the Application ID URI that was specified while configuring Microsoft Entra ID.

Create either a Delegated Auth or Service Principal based security integration.

1. Navigate to Snowsight.
2. Open a worksheet.
3. Execute either of the following:

   1. Delegated Auth:

      Using the [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external) command,
      create a security integration with the following parameters:

      Copy code

      ```
      CREATE SECURITY INTEGRATION IF NOT EXISTS external_oauth_azure_1
         TYPE = EXTERNAL_OAUTH
         ENABLED = TRUE
         EXTERNAL_OAUTH_TYPE = AZURE
         EXTERNAL_OAUTH_ISSUER = '{AZURE_AD_ISSUER}'
         EXTERNAL_OAUTH_JWS_KEYS_URL = '{AZURE_AD_JWS_KEY_ENDPOINT}'
         EXTERNAL_OAUTH_AUDIENCE_LIST = ('{SNOWFLAKE_APPLICATION_ID_URI}')
         EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'upn'
         EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' }
      ```

   When using Delegated Authentication, the Snowflake user’s *login\_name* or *email\_address*
   MUST match the Entra email of the user who will run the Power Automate flow.

   For example:

   Copy code

   ```
   ALTER USER SNOWSQL_DELEGATE_USER
   LOGIN_NAME = '{ENTRA-USERID}' or EMAIL_ADDRESS = 'ENTRA-USERID'
   DISPLAY_NAME = 'SnowSQL Delegated User'
   COMMENT = 'A delegate user for SnowSQL client to be used for OAuth based connectivity';
   ```

   **OR**

   - Service Principal Auth:

     Copy code

     ```
     CREATE SECURITY INTEGRATION external_oauth_azure_2
        TYPE = EXTERNAL_OAUTH
        ENABLED = TRUE
        EXTERNAL_OAUTH_TYPE = AZURE
        EXTERNAL_OAUTH_ISSUER = '{AZURE_AD_ISSUER}'
        EXTERNAL_OAUTH_JWS_KEYS_URL = '{AZURE_AD_JWS_KEY_ENDPOINT}'
        EXTERNAL_OAUTH_AUDIENCE_LIST = ('{SNOWFLAKE_APPLICATION_ID_URI}')
        EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'sub'
        EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name';
     ```
4. Create a user for the Service Principal-based connection:

   - The subvalue should be mapped to a user in Snowflake,
     avoiding using high privilege accounts `ACCOUNTADMIN`, `ORGADMIN`, or `SECURITYADMIN`.

   Copy code

   ```
   CREATE OR REPLACE USER SNOWSQL_OAUTH_USER
   LOGIN_NAME = '<subvalue from decoded token>'
   DISPLAY_NAME = 'SnowSQL OAuth User'
   COMMENT = 'A system user for SnowSQL client to be used for OAuth based connectivity';

   CREATE ROLE ANALYST;

   GRANT ROLE ANALYST TO USER SNOWSQL_OAUTH_USER;
   ```

Note

If a Security Integration for Azure AD was previously configured, execute
the [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-external) as described below:

> Copy code
>
> ```
> ALTER SECURITY INTEGRATION external_oauth_azure_1 SET EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = ('sub','upn');
> ```

## Next steps

After completing these procedures, follow the steps in [Snowflake Connector for Microsoft Power Platform: [Optional] Validate Entra authorization setup](/connectors/microsoft/powerapps/validate-entra-auth).
