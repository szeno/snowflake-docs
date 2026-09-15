# Openflow Connector for Salesforce Bulk API: Set up Salesforce

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up Salesforce for the Openflow Connector for Salesforce Bulk API.

The connector authenticates with Salesforce using the OAuth 2.0 JWT Bearer Flow. This requires creating a certificate key pair, configuring an external client app in Salesforce, and authorizing a user to use the app.

Important

Salesforce has deprecated Connected Apps in favor of External Client Apps. If you have an existing Connected App, Snowflake recommends creating a new External Client App instead.

## Create certificates

You need a private key and public certificate to configure the external client app in Salesforce. The private key is used by the connector to sign JWT tokens, and the public certificate is uploaded to the external client app in Salesforce so that Salesforce can verify the signature.

1. Generate the private key. You are asked for a password to secure the private key.

   Copy code

   ```
   openssl genpkey -algorithm RSA -out private.key -aes256
   ```

   Record the password. You need it when configuring the connector parameters in Snowflake.
2. Create a self-signed certificate from the private key.

   Copy code

   ```
   openssl req -new -x509 -key private.key -out public.crt -days 365
   ```

   You can also generate a Certificate Signing Request (CSR) to have a certificate signed by your company CA.

Note

You are responsible for safeguarding and rotating the public key and private key files used for key-pair authentication according to the security policies of your organization.

## Create an external client app in Salesforce

Create an external client app in Salesforce with JWT Bearer Flow. The connector requires this specific OAuth flow to authenticate. Using a different OAuth flow (such as Authorization Code Flow) causes `invalid_grant` errors.

1. Log in to Salesforce as an administrator.
2. Go to **Setup** » **Apps** » **App Manager**, and then select **New External Client App**.
3. Fill in the required fields:

   - **External Client App Name**: For example, `Openflow connector for Salesforce Bulk API`.
   - **Contact Email**: For example, `salesforceadmin@mycompany.com`.
4. In the **API (Enable OAuth Settings)** section, select the **Enable OAuth** checkbox.
5. Provide a valid **Callback URL** (for example, `https://www.google.com/`).

   Note

   The callback URL is required by Salesforce, but it is not used by the JWT Bearer Flow. You can provide any valid URL.
6. Provide the desired **OAuth Scopes** for the application. The following scopes are required for the connector to operate properly:

   - Manage user data via APIs (`api`)
   - Perform requests at any time (`refresh_token`, `offline_access`)
7. In **Flow Enablement**, select the **Enable JWT Bearer Flow** checkbox and upload the `public.crt` file created in the previous step.

   Important

   You must select **Enable JWT Bearer Flow** specifically. Do not enable other flows unless you have a specific reason to do so. The certificate you upload here must correspond to the private key (`private.key`) that you configure in the connector parameters.
8. Click **Create** to complete the application creation process.
9. Go to the **Settings** tab, expand the **OAuth Settings** section, and click **Consumer Key and Secret** to retrieve the credentials of your application.
10. Record the values for the **Consumer Key** and the **Consumer Secret** for use when configuring the connector in Snowflake. The **Consumer Key** is used as the **OAuth2 Client ID** parameter in the connector configuration.

## Approve the client app for a user

The connector interacts with Salesforce APIs on behalf of a specific user (the OAuth2 Subject configured in the connector parameters). You must authorize this user to use the external client app by assigning the appropriate profiles or permission sets.

If this step is not completed, the connector receives a permission error when attempting to authenticate, even if the JWT Bearer Flow is configured correctly.

1. Go to the **Policies** tab of the client application.
2. Click **Edit**.
3. Expand the **OAuth Policies** section and change **Permitted Users** to **Admin approved users are pre-authorized**.
4. Expand the **App Policies** section and select the profiles or permission sets that are assigned to the Salesforce user you want the connector to use. For example, if the user has the `System Administrator` profile, select that profile.

   Note

   The user specified as the **OAuth2 Subject** in the connector configuration must belong to at least one of the profiles or permission sets selected here. If the user is not authorized, you receive a permission error when verifying or running the connector.
5. Click **Save**.

## Verify credentials match

Before proceeding to the Snowflake setup, confirm that the following credentials all belong to the same external client app and key pair:

- The **Consumer Key** (Client ID) was retrieved from the external client app you just created.
- The **private key** (`private.key`) corresponds to the **certificate** (`public.crt`) uploaded to the same external client app.
- The **OAuth2 Subject** (user) is authorized for this external client app through the profile or permission set assignment.

If you have created multiple external client apps or experimented with different configurations, mixing credentials from different apps or key pairs is a common source of `invalid_grant` errors. When in doubt, create a new external client app with a fresh certificate and key pair.

## Next steps

Perform the Snowflake setup tasks:

[Openflow Connector for Salesforce Bulk API: Set up Snowflake](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-snowflake)
