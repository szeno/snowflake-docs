# Configure an identity provider (IdP) for Snowflake Open Catalog

Feature — Generally Available

Not available in government regions.

This topic shows you how to [configure Okta](#configure-okta) or [configure Auth0](#configure-auth0) as the IdP for your Snowflake Open Catalog account.

## Before you begin

To set up an IdP for Open Catalog SSO, you use your full Open Catalog account identifier, which includes your Snowflake
organization name and your Open Catalog account name; for example: `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

## Configure Okta

Note

To create an Okta account for your company or
organization, see <https://www.okta.com/>.

To set up Okta as the IdP for your Open Catalog account, follow these steps:

### Create an application in Okta for your Snowflake Open Catalog account

1. Sign in to the Okta Admin Portal.
2. In the left pane, select **Applications** > **Applications**, and then select **Browse App Catalog**.
3. In the search bar, search for and select the **Snowflake** application.
4. Select **Add Integration**.
5. In the **General settings** tab, enter the following values:

   - For **Application label**, enter Snowflake Open Catalog.
   - For **Subdomain**, enter your Snowflake organization name and Snowflake Open Catalog account name, using the format `<orgname>-<my-snowflake-open-catalog-account-name>`.

     For example: `ABCDEFG-MYACCOUNT1`.
     To find these names, see [Before you begin](#before-you-begin).
6. Under **Sign-On Options - Required**, select **SAML 2.0**.
7. Under **Credentials Details**, for **Application username format**, select **Okta username**.

   This is the NameID value passed to Snowflake from Okta, which must
   match the LOGIN\_NAME value of each user in Snowflake Open Catalog.
8. Select **Done**.
9. Select **View Setup Instructions**.

   This opens a new browser tab that contains information for configuring your Snowflake Open Catalog account to use SSO.
10. From the setup instructions, copy the following values, and paste them into a text editor for later use:

    - Entity ID (sometimes referred to as Issuer URL)
    - IDP SSO URL (sometimes referred to as Login URL)
    - Authentication Certificate

### Create a user (person)

Okta uses the term *person* to mean *user*. These are the users who will have access to your Open Catalog account.

To create users in Okta, follow these steps:

1. In the Okta Admin Portal, in the left pane, select **Directory** > **People**.
2. Select **Add Person**.
3. Enter the user’s details:

   | Field | Value |
   | --- | --- |
   | **User type** | Select **User**. |
   | **First name** | The user’s first name. |
   | **Last name** | The user’s last name. |
   | **Username** | The user’s email address.   Note: The **Username** that you enter here must match the LOGIN\_NAME used to [create the user in Open Catalog](./sso-configure-open-catalog#create-a-user-in-the-open-catalog-account). |
   | **Primary email** | This field is automatically populated with the **Username** that you enter. |
   | **Activation** | Select **Activate now**. |
   | **I will set password** | Select this option, and then enter a password for the user. |

   Expand

   Show lessSee more
4. Select **Save**.

### Assign the Snowflake Open Catalog application to users

Assigning the Open Catalog application to a user allows you to grant them access to your Open Catalog account. When you
[create the user in Open Catalog](sso-configure-open-catalog#create-a-user-in-the-open-catalog-account), you grant them access to the
account.

To assign the Snowflake Open Catalog application to users in Okta, follow these steps:

1. In the Okta Admin Portal, navigate to the Snowflake Open Catalog application that you previously created.
2. Select the **Assignments** tab.
3. Assign the application to users through individual user assignment (**Assign to People**) or group assignment (**Assign to Groups**).

## Configure Auth0

Note

To create an Auth0 account for your company or organization, see <https://auth0.com/>.

To set up Auth0 as the IdP for your Open Catalog account, follow these steps:

### Create a Snowflake Open Catalog application

1. Sign in to the Auth0 console.
2. Select **Applications** > **Applications** > **+ Create Application**.
3. Create an application for Snowflake Open Catalog:

   1. Select **Native**.
   2. Enter a name for the application: **Snowflake Open Catalog**
   3. Select **Create**.
4. On the **Settings** tab, under **Application URIs**, provide the following details:

   | Field | Value |
   | --- | --- |
   | **Application Login URI** | `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com`    For example: `https://ABCDEFG-MYACCOUNT1.snowflakecomputing.com`    To find these names, see [Before you begin](#before-you-begin). |
   | **Allowed Callback URLs** | `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com`   `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login`    For example: `https://ABCDEFG-MYACCOUNT1.snowflakecomputing.com <br /><br /> https://ABCDEFG-MYACCOUNT1.snowflakecomputing.com/fed/login`    To find these names, see [Before you begin](#before-you-begin). |
   | **Allowed Logout URLs** | `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/logout`    For example: `https://ABCDEFG-MYACCOUNT1.snowflakecomputing.com/fed/logout`    To find these names, see [Before you begin](#before-you-begin). |

   Expand

   Show lessSee more
5. Under **Advanced settings**, select the **Grant Types** tab.
6. Select the **Password** checkbox. Accept the default values for the other settings.
7. At the top of the page, select the **Addons** tab.
8. Select the **SAML2 WEB APP**.
9. In the window that opens, select the **Settings** tab.
10. For **Application Callback URL**, enter:
    `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login`
      
      
     For example: `https://ABCDEFG-MYACCOUNT1.snowflakecomputing.com/fed/login`   
      
     To find these names, see [Before you begin](#before-you-begin).|
11. For **Settings**, replace the contents with the following code:

    Copy code

    ```
    {
           "audience": "https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com",
           "recipient": "https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login",
           "signatureAlgorithm": "rsa-sha256",
           "digestAlgorithm": "sha256",
           "destination": "https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login",
           "nameIdentifierProbes": [
                "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress""
            ],
           "logout": {
              "callback": "https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/logout"
            },
           "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
      }
    ```

    Where:

    `<orgname>` is the name of your Snowflake organization, and`<my-snowflake-open-catalog-account-name>` is the name of your Snowflake Open Catalog account. To find these names, see [Before you begin](#before-you-begin).
12. Scroll down and select **Enable**.

    This button changes to **Save**.
13. to save your settings, select **Save**.

### Create users

These are the users who will have access to your Open Catalog account.

To create users in Auth0, follow these steps:

1. In the Auth0 console, in the left pane, select **User Management** > **Users**.
2. Select **+ Create User**.
3. In the **Create user** dialog, enter these values:

   - For **Connection**, select **Username-Password-Authentication**.
   - For **Email**, enter an email address for the user.

Note

The email address that you enter here must match the LOGIN\_NAME used to [create the user in Open Catalog](./sso-configure-open-catalog#create-a-user-in-the-open-catalog-account).

1. For **Password** and **Repeat Password**, enter the same password for the user twice.
2. Select **Create**.
