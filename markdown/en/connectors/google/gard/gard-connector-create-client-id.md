# Configuring OAuth authentication for Google Cloud Platform (GCP)

## About customer-provided OAuth client authentication

An application that authenticates to Google using OAuth 2.0 must provide two objects in GCP:

- OAuth consent screen that tells users who is requesting access to their data and what kind of data users are allowing your application to access.
- OAuth Client ID used to authenticate an application to Google. It is necessary when you want to access resources owned by your end user.

You must provide your own OAuth consent screen and client ID to authenticate. In a future release, the consent screen will be provided.

## Prerequisites

To provide the OAuth consent screen and OAuth client ID, you must create a Google Cloud Platform (GCP) project first. Refer to the GCP documentation to learn how to create a GCP project.

Note

If possible, create an OAuth consent screen in a GCP project that belongs to an organization. Make sure that the connector users are members of the same organization.

If your project does not belong to an organization, you must renew authentication every seven days.

## Configuring the OAuth consent screen

1. To open the OAuth consent screen creator, select **APIs & Services** » **OAuth consent screen** in your GCP project.
2. Select the user type.
   You can select the **Internal** user type only if the GCP project belongs to an organization and the connector users are members of the same organization.

   The **External** user type causes the authentication to expire in seven days. If you choose this type, you need to renew authentication weekly.
3. Select **Create**.
4. Provide the following information:

   - App name: Snowflake Connector for Google Analytics Raw Data
   - User support email: your email address
   - Developer contact information: your email address
5. Select **Save and continue**.
6. Select **Add or remove scopes** » **Manually add scopes**. Copy the following addresses:

   Copy code

   ```
   https://www.googleapis.com/auth/bigquery.readonly
   https://www.googleapis.com/auth/cloudplatformprojects.readonly
   ```
7. To add the scopes, paste each address in a dialog and select **Add to table**.
8. Select **Update**.

For **External** user type:

> 1. Select **Test users** » **Add users**.
> 2. Enter the email addresses of users that are allowed to use the connector.
> 3. Select **Add**.

To finish configuration, select **Save and continue** » **Back to dashboard**.

## Configuring the OAuth client ID

The following procedure describes how to configure the OAuth Client ID:

1. To open the OAuth consent screen creator, select **APIs & Services** » **Credentials** in your GCP project.
2. Select **Create credentials** » **OAuth client ID**.
3. In the **Application type** dropdown list, select **Web application**.
4. In the **Name** box, enter the following name: Snowflake Connector for Google Analytics Raw Data ID.
5. Select **Authorized redirect URIs** » **Add URI**.
6. In the Snowflake Connector for Google Analytics Raw Data interface, go to the third step of the connector configuration: **Authentication**. Choose **OAuth2** and copy the value from the **Redirect URL** box.
7. Go back to the GCP interface, and paste the value to the URI box.
8. Select **Create**.
9. Copy the **Your Client ID** and **Your Client Secret** values.
10. Paste the values into the corresponding boxes in the Snowflake Connector for Google Analytics Raw Data interface.
11. Select **Sign in**.

## Preventing session expiration for OAuth consent screen

The following procedure describes how to prevent session expiration for OAuth Consent Screen:

1. In the Google Admin Console menu, select **Security** » **Access and data control** » **Google Cloud session control**.
2. In the **Reauthentication policy** section, select the **Exempt Trusted apps** checkbox.
3. In the Google Admin Console menu, select **Security** » **API Controls** » **App Access Control**.
4. In the **Configured apps** section, select **Add app** » **OAuth App Name Or Client ID**.
5. Copy the client ID created in [Configuring the OAuth Client ID](#configuring-the-oauth-client-id), and paste it into the box.
6. Select **Search**.
7. Select **Snowflake Connector for Google Analytics Raw Data** application name.
8. Select the created **OAuth Client ID** checkbox, and click **Select**.
9. In the **Scope** section, select **All users**.
10. Select **Continue**.
11. In the **Access to Google Data** section, select **Trusted**.
12. Select **Continue**.
13. On the **Review** screen, select **Finish**.
