# Configure Snowflake Open Catalog to use SSO

Feature — Generally Available

Not available in government regions.

This topic shows you how to configure Snowflake Open Catalog to use SAML-based SSO.

Before you configure Snowflake Open Catalog to use SSO, you must configure your IdP for Open Catalog. For instructions, see the following
topics:

- [Configure Okta as the IdP for Open Catalog](./sso-configure-idp#configure-okta)
- [Configure Auth0 as the Idp for Open Catalog](./sso-configure-idp#configure-auth0)

## Before you begin

To set up Snowflake Open Catalog for SSO, you need your full Open Catalog account identifier, which includes your Snowflake
organization name and your Open Catalog account name; for example: `<orgname>.<my-snowflake-open-catalog-account-name>`.

- To find your *Snowflake* organization name (`<orgname>`), see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
- To find your *Snowflake Open Catalog* account name (`<my-snowflake-open-catalog-account-name>`), see
  [Find the account name for a Snowflake Open Catalog account](/user-guide/opencatalog/find-account-name).

## Create a Snowflake CLI connection for Open Catalog

To configure Snowflake Open Catalog to use SSO, you need a Snowflake CLI connection for Open Catalog. Follow these steps to create this
connection. If you don’t already have Snowflake CLI installed, see [Installing Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation).

Important

To create this connection, you must be an Open Catalog user with service
admin privileges. For information about service admin privileges, see [Service admin role](../opencatalog/access-control#service-admin-role).

### Add a Snowflake CLI connection for Snowflake Open Catalog

Add a connection for the Snowflake Open Catalog account where you want to enable SSO.

- [Add a connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-snow-connection-command-add)
  with the following values. For all other parameters, press `Enter` to skip specifying a value for the parameter.

  | Connection configuration parameters | Value |
  | --- | --- |
  | **Name for this connection** | Specify a name for the connection; for example, `myopencatalogconnection`. |
  | **Account name** | Specify your Snowflake organization name, followed by your Open Catalog account name, in this format:  `<orgname>-<my-snowflake-open-catalog-account-name>`.  For example, `ABCDEFG-MYACCOUNT1`.  To find these names, see [Before you begin](#before-you-begin). |
  | **Username** | Specify your username for Open Catalog; for example, `jsmith`. |
  | **Password [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  Enter your password for Open Catalog; for example, `MyPassword123456789`. |
  | **Role for the connection [optional]** | This parameter is *not* optional when you create a connection for Open Catalog.  You must enter `POLARIS_ACCOUNT_ADMIN` |

  Expand

  Show lessSee more

### Test the Snowflake CLI connection

- To test your CLI connection, follow this example, which tests the connection for `myopencatalogconnection`:

  Copy code

  ```
  snow connection test -c myopencatalogconnection
  ```

  The response should look like this:

  Copy code

  ```
  +------------------------------------------------------------------------------+
  | key              | value                                                     |
  |----------------------------+-------------------------------------------------|
  | Connection name  | myopencatalogconnection                                   |
  | Status           | OK                                                        |
  | Host             | ABCDEFG-MYACCOUNT1.snowflakecomputing.com                 |
  | Account          | ABCDEFG-MYACCOUNT1                                        |
  | User             | jsmith                                                    |
  | Role             | POLARIS_ACCOUNT_ADMIN                                     |
  | Database         | not set                                                   |
  | Warehouse        | not set                                                   |
  +------------------------------------------------------------------------------+
  ```

### Set your Snowflake CLI connection for Snowflake Open Catalog as the default

To ensure that the connection you’re using always has the required POLARIS\_ACCOUNT\_ADMIN role granted to it, you can set the Snowflake CLI
connection you created for Open Catalog as the default connection. For more information about the default connection, see
[label-cli\_set\_default\_connection](/developer-guide/snowflake-cli/connecting/configure-connections#label-cli-set-default-connection).

1. Follow this example, which sets the `myopencatalogconnection` connection as the default:

   Copy code

   ```
   snow connection set-default myopencatalogconnection
   ```
2. To confirm that you’re using the correct user and role, run the following:

   Copy code

   ```
   snow sql -q "Select current_user(); select current_role();"
   ```

   The response should return your Open Catalog username and the CURRENT
   ROLE should be POLARIS\_ACCOUNT\_ADMIN.

   Copy code

   ```
   +----------------+
   | CURRENT_USER() |
   |----------------|
   | JSMITH        |
   +----------------+
   select current_role();
   +-----------------------+
   | CURRENT_ROLE()        |
   |-----------------------|
   | POLARIS_ACCOUNT_ADMIN |
   +-----------------------+
   ```

## Create a security integration

To create a security integration, run the CREATE SECURITY INTEGRATION command by using a Snowflake CLI connection. You can create an
[Auth0 security integration](#auth0-security-integration) or an [Okta security integration](#okta-security-integration).

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

### Auth0 security integration

- To create a SAML security integration for Auth0, run the following command in Snowflake CLI:

  Copy code

  ```
  snow sql -q “create security integration <Name>
      type = saml2
      enabled = true
      saml2_issuer = 'urn:<Auth0 Domain>'
      saml2_sso_url = '<SAML Protocol URL>'
      saml2_provider = 'Custom'
      saml2_x509_cert='<Certificate from Auth0>'
      saml2_sp_initiated_login_page_label = 'Auth0'
      saml2_enable_sp_initiated = true
      saml2_snowflake_acs_url = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login'
      saml2_snowflake_issuer_url = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com'
      saml2_requested_nameid_format = 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress';”
  ```

  Where:

  - `<Name>` specifies the identifier for the security integration; must be unique for your account.
  - `<Auth0 Domain>` is copied in the Auth0 console. To find this value, in Auth0, navigate to Applications &gt; Applications &gt; Snowflake Open Catalog application &gt; Settings &gt;
    Basic Information: **Domain** field.
  - `<SAML Protocol URL>` is copied in the Auth0 console. To find this value, in Auth0, navigate to Applications &gt; Applications &gt; Snowflake Open Catalog application
    > Settings > Advanced settings > Endpoints tab: **SAML Protocol URL** field.
  - `<Certificate from Auth0>` is copied in the Auth0 console. To find this value, in Auth0, navigate to: Applications &gt; Applications &gt; Snowflake Open Catalog application
    &gt; Settings &gt; Advanced Settings &gt; Certificate tab: **Signing Certificates** field. Copy the value between &lt;BEGIN CERTIFICATE&gt; and &lt;END CERTIFICATE&gt;.
  - `<orgname>` is the name of your Snowflake organization. To find this name, see [Before you begin](#before-you-begin).
  - `<my-snowflake-open-catalog-account-name>` is the name of your Snowflake Open Catalog account. To find this name, see
    [Before you begin](#before-you-begin).

### Okta security integration

- To create a SAML security integration for Okta, run the following
  command in Snowflake CLI:

  Copy code

  ```
  snow sql -q “CREATE SECURITY INTEGRATION <Name>
      TYPE = SAML2
      ENABLED = TRUE
      SAML2_ISSUER = '<ENTITY ID>'
      SAML2_SSO_URL = '<IDP SSO URL>'
      SAML2_PROVIDER = 'OKTA'
      SAML2_X509_CERT='<Authentication Certificate>'
      SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = 'OKTA SSO'
      SAML2_ENABLE_SP_INITIATED = TRUE
      SAML2_SNOWFLAKE_ACS_URL = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/fed/login'
      SAML2_SNOWFLAKE_ISSUER_URL = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com';”
  ```

  Where:

  - `<Name>` specifies the identifier for the security integration; must be unique for your account.
  - `<ENTITY ID>` is the Entity ID value you copied when you [created an application in Okta](./sso-configure-idp#create-an-application-in-okta-for-your-snowflake-open-catalog-account).
  - `<IDP SSO URL>` is the IDP SSO URL value you copied when you created an application in Okta.
  - `<Authentication Certificate>` is the IDP Authentication Certificate value you copied when you created an application in Okta.
  - `<orgname>` is the name of your Snowflake organization. To find this name, see [Before you begin](#before-you-begin).
  - `<my-snowflake-open-catalog-account-name>` is the name of your Snowflake Open Catalog account. To find this name, see
    [Before you begin](#before-you-begin).

## Verify the security integration

You can only use one security integration at a time, and the integration you want to use must be enabled.

Note

If the default Snowflake CLI connection that you set doesn’t have the POLARIS\_ACCOUNT\_ADMIN role granted to it, you must include the
following statement with your command: `USE ROLE POLARIS_ACCOUNT_ADMIN`.

1. To verify that the security integration you want to use is enabled, run the following command:

   Copy code

   ```
   snow sql -q "desc security integration <saml2-security-integration-name>;"
   ```

   If the response contains SAML2\_ENABLE\_SP\_INITIATED=true, the SAML2 security integration is enabled.
2. Optional: If the response contains SAML2\_ENABLE\_SP\_INITIATED=false, to enable it, run the following command:

   Copy code

   ```
   snow sql -q “ALTER SECURITY INTEGRATION <saml-security-integration-name> SET ENABLED = TRUE;”
   ```

## Create a user in the Open Catalog account

For SSO to work for a user, you must create an Open Catalog user that corresponds to the user you created in your IdP.

Important

To create a user, you must use Snowflake CLI.

If you create a user by using the Open Catalog UI, you must specify a password,
which would allow the user to sign in through SSO or by using Open Catalog credentials.

- To create a user, run the following command:

  Copy code

  ```
  snow sql -q "CREATE USER \"<login-name>\" EMAIL='<email>';"
  ```

  Where:

  - `<login-name>` must match one of the following:

    - The **Email** that you specified for the user in Auth0.
    - The **Username** that you specified for the user in Okta.
  - `<email>` is the user’s email address. If you’re using Auth0, this value will match &lt;login-name&gt;.

  For example:

  Copy code

  ```
  snow sql -q "CREATE USER \"testuser123@example.com\" EMAIL='testuser123@example.com';"
  ```
- To confirm that you set up the users correctly, run the following command:

  Copy code

  ```
  snow sql -q "show users;"
  ```

  In the response, the value in the LOGIN\_NAME column must match the **Email** in Auth0 or **Username** in Okta.
