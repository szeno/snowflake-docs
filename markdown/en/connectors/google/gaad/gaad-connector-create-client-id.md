# Configure OAuth authentication for Google Cloud

## About customer-provided OAuth client authentication

An application that authenticates to Google using OAuth 2.0 must provide two objects in Google Cloud:

- An *OAuth consent screen* that tells users who is requesting access to their data and what kind of data users are allowing your application to access.
- An *OAuth Client ID* that is used to authenticate an application to Google. This is necessary when you want to access resources owned by your end user.

You must provide your own OAuth consent screen and client ID to authenticate.

## Prerequisites

To provide the OAuth consent screen and OAuth client ID, you must first create a Google Cloud project. For information about creating Google Cloud projects, see the Google Cloud documentation.

Note

If possible, create an OAuth consent screen in a Google Cloud project that belongs to an organization. Ensure that the connector users are members of the same organization.

If your project does not belong to an organization, you must renew authentication every seven days.

## Configure the OAuth consent screen

1. To open the OAuth consent screen creator, in your Google Cloud project, select **APIs & Services** » **OAuth consent screen**.
2. Select one of the following user types:

   - **Internal**: Select this user type only if the Google Cloud project belongs to an organization and the connector users are members of the same organization.
   - **External**: If you select this user type, you must renew authentication weekly.
3. Select **Create**.
4. Provide the following information:

   - **App name**:
   - **User support email**: your email address
   - **Developer contact information**: your email address
5. Select **Save and continue**.
6. Select **Add or remove scopes** » **Manually add scopes**.
7. Copy the following address:

   Copy code

   ```
   https://www.googleapis.com/auth/analytics.readonly
   ```
8. Paste the address in the dialog, and then select **Add to table**.
9. Select **Update**.
10. If you selected the **External** user type, follow these steps:
11. Select **Test users** » **Add users**.
12. Enter the email addresses of users who are allowed to use the connector.
13. Select **Add**.
14. To finish the configuration, select **Save and continue** » **Back to dashboard**.

## Configure the OAuth client ID

In this procedure, you acquire a redirect URL from Snowsight and paste it into your Google Cloud project.

1. In Snowsight, start the configuration wizard.
2. In the third step of the connector configuration, **Authenticate Google Cloud Platform**, copy the value from the **Redirect URL** section.
3. In your Google Cloud project, to open the OAuth consent screen creator, select **APIs & Services** » **Credentials**.
4. Select **Create credentials** » **OAuth client ID**.
5. In the **Application type** dropdown list, select **Web application**.
6. In the **Name** box, enter the following name: ID
7. Select **Authorized redirect URIs** » **Add URI**.
8. Select **Create**.
9. Copy the **Your Client ID** and **Your Client Secret** values.
10. Return to the interface, and paste the values into the corresponding boxes.
11. Select **Sign in**.

## Prevent session expiration for the OAuth consent screen

1. In the Google Admin Console menu, select **Security** » **Access and data control** » **Google Cloud session control**.
2. In the **Reauthentication policy** section, select the **Exempt Trusted apps** checkbox.
3. In the Google Admin Console menu, select **Security** » **API Controls** » **App Access Control**.
4. In the **Configured apps** section, select **Add app** » **OAuth App Name Or Client ID**.
5. Copy the client ID created in [Configure the OAuth client ID](#configure-the-oauth-client-id), and paste it in the box.
6. Select **Search**.
7. Select the application name.
8. Select the created **OAuth Client ID** checkbox, and then click **Select**.
9. In the **Scope** section, select **All users**.
10. Select **Continue**.
11. In the **Access to Google Data** section, select **Trusted**.
12. Select **Continue**.
13. On the **Review** screen, select **Finish**.
