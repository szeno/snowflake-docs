# Step 5: Create a GCP security policy for the proxy service in the console

In the previous steps, you created a Google Cloud Function that can be called by anyone who has the correct Google Cloud API Gateway
endpoint. Unless you want the endpoint to be open to the public, you should secure it by creating a security policy on the Google Cloud
API Gateway.

This topic provides instructions for creating a security policy for the API Gateway by adding a customized `securityDefinitions`
section to the configuration file for the API definition.

Important

Snowflake strongly recommends creating a security policy for the API Gateway. After completing this step, only Snowflake is allowed to
call your Cloud Function through the API Gateway.

## Previous step

[Step 4: Create the external function for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-ext-function)

## Links to related Google documentation

For more detailed information about using the Google Cloud Console to perform the tasks described in this topic, see the following topics
in the [Google Cloud API Gateway documentation](https://cloud.google.com/api-gateway/docs/quickstart-console):

- [Securing Access by Using an API Key](https://cloud.google.com/api-gateway/docs/quickstart-console#securing_access_by_using_an_api_key)
- [Testing Your API Key](https://cloud.google.com/api-gateway/docs/quickstart-console#testing_your_api_key)

## Update the configuration file

Note

The name of the configuration file is recorded in the `Configuration File Name` field in your tracking worksheet.

1. Add or update the following `securityDefinitions` section in the configuration file. Add this immediately above the
   `schemes` section of the configuration file and at the same indentation level.

   Copy code

   ```
   securityDefinitions:
     <security-def-name>:
    authorizationUrl: ""
    flow: "implicit"
    type: "oauth2"
    x-google-issuer: "<gmail service account>"
    x-google-jwks_uri: "https://www.googleapis.com/robot/v1/metadata/x509/<gmail service account>"
   ```

   In the section:

   - Replace `<security-def-name>` with a unique security definition name (e.g. `snowflakeAccess01`). If you added the temporary security definition in step 2 of the tutorial ([Step 2: Create the proxy service (Google Cloud API Gateway) in the console](/sql-reference/external-functions-creating-gcp-ui-proxy-service)), this is already done.
   - In addition, record this name in the `Security Definition Name` field in your tracking worksheet.
   - Replace `<gmail service account>` with the value from the `API_GCP_SERVICE_ACCOUNT` field in your tracking worksheet.
     Add the value in two places in the configuration file:
     - `x-google-issuer` field
     - `x-google-jwks_uri` field (appended to the end of the field)
2. Update the `post:` section of the configuration file to reference the security definition that you created
   above.

   Below the `operationId` field, add:

   Copy code

   ```
   security:
     - <security-def-name>: []
   ```

   This should be indented at the same level as the `operationId` field.

   - Replace `<security-def-name>` with the value from the `Security Definition Name` field in your tracking worksheet if you have not already done so.
   - Make sure to include a hyphen and a blank prior to the security definition name, as shown above.
   - Make sure to include the empty square braces (`[]`) after the colon.

   For example:

   Copy code

   ```
   security:
     - snowflakeAccess01: []
   ```
3. Save the configuration file.

Your updated configuration file should look similar to the following:

Copy code

```
swagger: '2.0'
info:
  title: API Gateway config for Snowflake external function
  description: This configuration file connects the API Gateway resource to the remote service (Cloud Function).
  version: 1.0.0
securityDefinitions:
  snowflakeAccess01:
    authorizationUrl: ""
    flow: "implicit"
    type: "oauth2"
    x-google-issuer: "<API_GCP_SERVICE_ACCOUNT>"
    x-google-jwks_uri: "https://www.googleapis.com/robot/v1/metadata/x509/<API_GCP_SERVICE_ACCOUNT>"
schemes:
  - https
produces:
  - application/json
paths:
  /demo-func-resource:
    post:
      summary: Echo the input
      operationId: operationID
      security:
        - snowflakeAccess01: []
      x-google-backend:
        address: <Cloud Function Trigger URL>
        protocol: h2
      responses:
        '200':
          description: <DESCRIPTION>
          schema:
            type: string
```

## Reload the updated file

After updating the configuration file, you must reload the file in the Google Cloud Console:

1. On the **Gateways** page, click on the name of your gateway.
2. Click on **EDIT**.
3. Under **API Config**, click in the box titled **Select a Config**.
4. Select the option **Create new API config**.
5. In the box that contains **Upload an API Spec**, click on the **BROWSE** button.
6. Select the desired YAML file, which you created previously. Check that it has the extension `.yaml` or `.yml`.
7. Enter the **Display Name**. Use a new, unique name, not the name that you used previously.
8. If you are asked to **Select a Service Account**, then select **App Engine default service account**.

   If you are creating a function to use in production (rather than as a sample), you might choose a different service account.

   The selected service account must have appropriate privileges, including privileges to call the Google Cloud Function.
9. You should now be back on the page for your API gateway. If the **Config** field shows the old API config file’s display name:

   1. Click on **EDIT**.
   2. Under **API Config**, find the **Select a Config** box again, and click in the box.
   3. Select the new API config.
   4. Click the **UPDATE** button. This takes you back to the list of API gateways.

   You might need to wait a few minutes while the API Gateway is updated. An icon may appear to the left of the API gateway name,
   indicating that the gateway is being refreshed.

To check whether the refresh is still in progress, click on the **REFRESH** button above the gateway name. After the icon to the left
of the gateway name disappears, the gateway should be fully refreshed, and you can continue to the next step.

## Test your external function

To make sure that your external function works correctly with the new security configuration file, call your external function again.

For details, see [Calling an external function for GCP](/sql-reference/external-functions-creating-gcp-call).

## Next step

None. You’ve successfully created an external function for GCP.
