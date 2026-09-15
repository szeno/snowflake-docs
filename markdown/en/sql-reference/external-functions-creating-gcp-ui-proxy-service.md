# Step 2: Create the proxy service (Google Cloud API Gateway) in the console

Snowflake does not send data (HTTP POST requests) directly to a remote service. Instead, Snowflake sends the data to a proxy service that
relays the data from Snowflake to the remote service (i.e. GCP Cloud Function) and back again.

This topic provides instructions for creating and configuring a Google Cloud API Gateway for use as the proxy service for your
external function.

## Previous step

[Step 1: Create the remote service (Google Cloud Function) in the console](/sql-reference/external-functions-creating-gcp-ui-remote-service)

## Links to related Google documentation

For more detailed information about using the Google Cloud Console to perform the tasks described in this topic, see the following sections
in the [Quickstart for Deploying an API/API Gateway using the Google Cloud Console](https://cloud.google.com/api-gateway/docs/quickstart-console):

- [Creating an API definition](https://cloud.google.com/api-gateway/docs/quickstart-console#creating_an_api_definition)
- [Creating a gateway](https://cloud.google.com/api-gateway/docs/quickstart-console#creating_a_gateway)

If you prefer to use the command line instead of the Google Cloud Console, see the following sections in the
[Quickstart for Deploying an API/API Gateway using gcloud](https://cloud.google.com/api-gateway/docs/quickstart):

- [Creating an API](https://cloud.google.com/api-gateway/docs/creating-api#creating-an-api)
- [Creating an API config](https://cloud.google.com/api-gateway/docs/creating-api-config)
- [Deploy an API to a gateway](https://cloud.google.com/api-gateway/docs/deploying-api)

If you use the Google documentation, remember to copy the required information (e.g. Gateway URL) to your tracking worksheet.

## Create an API definition

On your local file system, create and customize a YAML-formatted configuration file that specifies the API you are creating. The file
should have the `.yaml` or `.yml` extension.

Configuration file template:

Copy code

```
swagger: '2.0'
info:
  title: API Gateway config for Snowflake external function.
  description: This configuration file connects the API Gateway resource to the remote service (Cloud Function).
  version: 1.0.0
schemes:
  - https
produces:
  - application/json
paths:
  /<PATH>:
    post:
      summary: Echo the input.
      operationId: echo
      x-google-backend:
        address: <HTTP ENDPOINT TO ROUTE REQUEST TO>
        protocol: h2
      responses:
        '200':
          description: <DESCRIPTION>
          schema:
            type: string
```

Fill in or update the following fields:

1. Replace `<PATH>` with a unique name. This will be incorporated into URLs, so use only characters that are valid in URLs. For
   example, enter `demo-func-resource`.

   Note that, unlike the other fields in this configuration file, enter the `<PATH>` value before the colon, rather than
   after the colon. For example, the following is correct:

   Copy code

   ```
   paths:
     /demo-func-resource:
   ```

   The path name should not contain any
   [path parameters](https://swagger.io/docs/specification/2-0/describing-parameters/#path-parameters).
   Google supports path parameters when
   [setting the path to a URL](https://cloud.google.com/api-gateway/docs/passing-data#setting_the_backend_service_address_and_path_in_the_openapi_spec).
   However, Snowflake does not support path parameters in the corresponding URL specified in the CREATE EXTERNAL FUNCTION statement.
2. Copy the path (e.g. `demo-func-resource`) from the immediately preceding step to the `Path Suffix` field
   in your tracking worksheet.
3. Find the `address` field under the `x-google-backend` field, and replace `<HTTP ENDPOINT TO ROUTE REQUEST TO>` with the
   value from the `Cloud Function Trigger URL` field in your tracking worksheet. The result should look similar to:

   Copy code

   ```
   x-google-backend:
     address: https:// ...
   ```

   The URL should not be enclosed in quotation marks.

   The URL does not need to be an endpoint hosted by Google; it can be the path to any HTTP endpoint.

   If you selected **Require HTTPS** in [Step 1: Create the remote service (Google Cloud Function) in the console](/sql-reference/external-functions-creating-gcp-ui-remote-service), then ensure
   that the URL you enter into the `address` field starts with `https`.
4. Optionally, you can update any of the following values:

   - `title` in the `info` section.
   - `description` in the `info` section.
   - `operationId` in the `post` subsection of the `paths` section.
   - `summary` in the `post` subsection of the `paths` section.
5. Review your sample configuration file. It should look similar to the following:

   Copy code

   ```
   swagger: '2.0'
   info:
     title: "API Gateway config for Snowflake external function"
     description: "This configuration file connects the API Gateway resource to the remote service (Cloud Function)."
     version: 1.0.0
   schemes:
     - https
   produces:
     - application/json
   paths:
     /demo-func-resource:
    post:
      summary: "echo the input"
      operationId: echo
      x-google-backend:
        address: https://my_dev.cloudfunctions.net/demo-cloud-function-01
        protocol: h2
      responses:
        '200':
          description: echo result
          schema:
            type: string
   ```

   Note

   This configuration will leave your gateway open to the public until you secure it in [Step 5: Create a GCP security policy for the proxy service in the console](/sql-reference/external-functions-creating-gcp-ui-security-policy) of this tutorial.
6. Optionally, to make sure that no one can use your gateway in the meantime, add a security definition to the configuration file that uses a temporary,
   invalid service account name (`google_service_account`) as described in this optional step. Adding this security definition in this step means that you cannot test your
   external function until you finish configuring security in [Step 5: Create a GCP security policy for the proxy service in the console](/sql-reference/external-functions-creating-gcp-ui-security-policy). Specifically, the instruction
   to test your external function in [Step 4: Create the external function for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-ext-function) will not work yet.

   1. Add the following `securityDefinitions` section immediately above the `schemes` section of the configuration file and at the same indentation level.

      Copy code

      ```
      securityDefinitions:
        <security-def-name>:
          authorizationUrl: ""
          flow: "implicit"
          type: "oauth2"
          x-google-issuer: "google_service_account"
          x-google-jwks_uri: "https://www.googleapis.com/robot/v1/metadata/x509/google_service_account"
      ```

      - Replace `<security-def-name>` with a unique security definition name (e.g. `snowflakeAccess01`).
      - Record this name in the `Security Definition Name` field in your tracking worksheet.
   2. Update the `post:` section of the configuration file to reference the security definition that you created above. Below the `operationId` field, add:

      Copy code

      ```
      security:
        - <security-def-name>: []
      ```

      - Make sure it is indented at the same level as the `operationId` field.
      - Replace `<security-def-name>` with the value from the `Security Definition Name` field in your tracking worksheet.
      - Make sure to include a hyphen and a blank prior to the security definition name, as shown above.
      - Make sure to include the empty square braces (`[]`) after the colon.

      For example:

      Copy code

      ```
      paths:
        /demo-func-resource:
          post:
      summary: "echo the input"
      operationId: echo
      security:
        - snowflakeAccess01: []
      x-google-backend:
        address: https://my_dev.cloudfunctions.net/demo-cloud-function-01
        protocol: h2
      ```
7. Save the configuration file.
8. Record the file path and name in the `Configuration File Name` field in your tracking worksheet.

To learn more about the API configuration file, see the following GCP documentation:

- [OpenAPI overview](https://cloud.google.com/api-gateway/docs/openapi-overview) .
- [Create an API definition](https://cloud.google.com/api-gateway/docs/quickstart-console#creating_an_api_definition) .

## Create an API Gateway

To create an API Gateway:

1. Create a GCP API.
2. Create an API Config.
3. Create a Gateway with the API Config.

### Create a GCP API

This step creates a *GCP API*, which is a container that can contain one or more API Gateways and one or more configuration files:

1. If you have not already done so, go to the **Google Cloud API Gateway** screen by clicking on the GCP menu and selecting
   **API Gateway**.
2. Click on **CREATE GATEWAY**.
3. Enter the **Display Name** and the **API ID** (e.g. `demo-api-display-name-for-external-function1` and
   `demo-api-id-for-external-function1`).

   You do not need to record these values in your tracking worksheet because you do not need to enter these later to create your
   external function. However, you might want to record the API ID so that you can delete it when you are done with it.

### Create an API config

Upload your configuration file to the console, which creates an *API Config*.

1. Scroll to the **API Config** section of the screen.
2. Search for the field that contains **Upload an API Spec**.

   Click on **BROWSE** and select your configuration file. The name of your configuration file was recorded in
   the `Configuration File Name` field in your tracking worksheet.
3. Enter a display name into the field that contains **Display Name**.
4. Select a service account.

   If you created the sample function, then in the field that contains **Select a Service Account**, select
   **App Engine default service account**.

   If you are creating a function to use in production (rather than as a sample), you might choose a different service account.

   The selected service account must have appropriate privileges, including privileges to call the Cloud Function.

### Create a gateway with the API config

1. Scroll to the **Gateway details** section of the screen.
2. Enter the **Display Name** of the new API Gateway.
3. Click in the **Location** field and select the appropriate region (e.g. `us-central1`).
4. Click on **CREATE GATEWAY**.

   This takes you to the **APIs** screen and shows you a list of your APIs.

   If your new API is not visible immediately, wait a few minutes, then click the **Refresh** button.
5. Copy the value of the API’s **Managed Service** to the `Managed Service Identifier` field in your tracking worksheet.
6. At this point, you should still see a list of your APIs. Click on the name of the API.

   You should see 4 tabs: **OVERVIEW**, **DETAILS**, **CONFIGS**, and **GATEWAYS**.
7. Click on the **GATEWAYS** tab.
8. Copy the **Gateway URL** to the `Gateway Base URL` field in your tracking worksheet.

## Next step

[Step 3: Create the API integration for GCP in Snowflake](/sql-reference/external-functions-creating-gcp-common-api-integration)
