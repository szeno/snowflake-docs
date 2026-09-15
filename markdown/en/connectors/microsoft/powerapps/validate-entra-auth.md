# Snowflake Connector for Microsoft Power Platform: [Optional] Validate Entra authorization setup

Snowflake recommends the configuration be tested and
suggests using the cURL commands below to determine if Entra is correctly issuing a token.

## Delegated auth validation

The prior steps must be executed to get the required authorization code value.
To obtain the required code, follow the steps outlined in [request an authorization code](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow#request-an-authorization-code).

1. Get authorization code:

   In a browser enter the following URL, replacing the placeholders with your values:

   Copy code

   ```
   https://login.microsoftonline.com/<tenant_id>/oauth2/v2.0/authorize?client_id=<client_id>&response_type=code&redirect_uri=https%3A%2F%2Flocalhost&response_mode=query&scope=api://<app_resource_id>/session:role-any&state=12345
   ```
2. Get access token:

   Use the authorization code from the previous step to get an access token.
   Replace the placeholders with your values in the following cURL command:

   Copy code

   ```
   curl -X  POST \
     -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
     --data-urlencode "client_id=<your client id>" \
     --data-urlencode "client_secret=<your client secret>"  \
     --data-urlencode "grant_type=authorization_code" \
     --data-urlencode "code=<use auth code from 1>" \
     --data-urlencode "scope=api://7bd09dd9-a6ef-4461-b014-c3226df74ed0/.default"  \
     --data-urlencode "redirect_uri=http://localhost" \
     https://login.microsoftonline.com/9a2d78cb-73e9-40ee-a558-fc1ac5ef57a7/oauth2/v2.0/token
   ```

   Note

   You must add `localhost` as an additional redirect URI in the AAD client application.

## Service principal auth validation

Copy code

```
curl -X POST \
     -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
     --data-urlencode "client_id=<CLIENT_ID>" \
     --data-urlencode "client_secret=<CLIENT_SECRET>" \
     --data-urlencode "grant_type=client_credentials" \
     --data-urlencode "scope=api://<Appl_URI_ID from Oauth Server>/.default" \
     https://login.microsoftonline.com/<TENANT_ID>/oauth2/v2.0/token
```

Where:

> - `CLIENT_ID` = Client ID from [Oauth Client setup](/connectors/microsoft/powerapps/create-oauth-client).
> - `CLIENT_SECRET` = Client secret from Oauth Client setup.
> - `TENANT_ID` = Tenant ID from Oauth Client setup.

To validate the token in Snowflake, execute the SQL in the steps below with token from above :

1. Navigate to Snowsight.
2. Open a worksheet.
3. Execute the following code:

   Copy code

   ```
   system$verify_external_oauth_token({token});
   ```

## Next steps

After completing these procedures, follow the steps in [Snowflake Connector for Microsoft Power Platform: [Optional] Validate Snowflake access](/connectors/microsoft/powerapps/validate-sf-access).
