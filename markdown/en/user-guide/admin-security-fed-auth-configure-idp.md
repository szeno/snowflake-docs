# Configuring an identity provider (IdP) for Snowflake

The tasks for configuring an IdP are different depending on whether you choose Okta, AD FS, or another (i.e. custom) SAML 2.0-compliant service/application to
provide federated authentication for your Snowflake users.

Note

This page covers SAML 2.0 IdP setup. For OpenID Connect (OIDC), including registering a custom OAuth application and obtaining client
credentials, see [Register Snowflake in your IdP (custom providers)](/user-guide/admin-security-fed-auth-oidc#label-oidc-register-idp).

Important

Prior to configuring your IdP, consider how to manage federated authentication after it is fully configured and how users will access Snowflake through
federated authentication.

For example, decide whether users will access Snowflake through a public URL or through a URL associated with
private connectivity to the Snowflake service. To learn more, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use).

## Okta setup

To use Okta as your IdP for federated authentication, you must perform the following tasks in Okta:

1. Create an Okta account for your company or organization.
2. Log into your Okta account as a user with administrator privileges and create a user for each person who will need access to Snowflake. When creating
   users, make sure to include an email address for each user. Email addresses are required to map the users in Okta with the corresponding users in Snowflake.

   Note

   Remember to ensure the email address you enter in Okta maps to the `login_name` value of the user object in Snowflake and
   the SAML `NameID` attribute.
3. Create a Snowflake application in Okta:

   - In the **Label** field for the application, you can specify any name.
   - In the **SubDomain** field for the application, enter the [account identifier](/user-guide/admin-account-identifier) of
     your Snowflake account. If you are using private connectivity, append `privatelink` to the account identifier. For example, if the
     URL used to access the Snowflake account is `https://myorg-myaccount.privatelink.snowflakecomputing.com`, then
     enter `myorg-myaccount.privatelink`.

     If the Snowflake account name contains an underscore and you are using the account name format of the identifier, you need to convert
     the underscore to a hyphen because Okta does not support underscores in URLs (e.g. `myorg-myaccount-name`).
4. Assign the Okta users you created to the Snowflake application in Okta.

### Obtain IdP information

Snowflake as the service provider needs information about the IdP to establish a relationship between the two. You’ll need this information
when you configure Snowflake, as described in [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).

The preferred method of providing information about the IdP is to obtain its metadata URL, which Snowflake can use to dynamically obtain
all of the information it needs. You can also manually define this information in multiple parameters in Snowflake, but that process is
error prone and the parameters must be manually updated if IdP configuration settings change, including when certificates are rotated.

#### Obtain the metadata URL (Preferred)

1. Navigate to the integration that you created for Snowflake and select the **Sign On** tab.
2. In the **SAML 2.0** tile of the **Sign on methods** section, copy the **Metadata URL**.

#### Obtain the SSO URL and certificate

1. Navigate to the integration that you created for Snowflake and select the **Sign On** tab.
2. Select **View Setup Instructions**.
3. Gather the required information from the setup instructions:
   - SSO URL (IdP URL endpoint to which Snowflake will send SAML requests)
   - Certificate (used to verify communication between the IdP and Snowflake)

## AD FS setup

To use AD FS as your IdP for federated authentication, you must perform the following tasks in AD FS.

### Prerequisites

- Verify that AD FS 3.0 is installed and working on Windows Server 2012 R2.
- Ensure that a user exists in AD FS for each person who will need access to Snowflake. When creating users, make sure to include an email address for each
  user. Email addresses are required to connect the users in AD FS with their corresponding users in Snowflake.

Note

Other versions of AD FS and Windows Server can be used; however, the configuration instructions may be different.

### Add a relying party trust for Snowflake

In the AD FS Management console, use the **Add Relying Party Trust Wizard** to add a new relying party trust to the AD FS configuration database:

1. When prompted, select the **Enter data about the relying party manually** radio button.
2. In the next screen, enter a display name (e.g. “Snowflake”) for the relying party.
3. In the next screen, select the **AD FS profile** radio button.
4. Skip the next screen (for specifying an optional token encryption certificate).
5. In the next screen:

   - Select the **Enable support for the SAML 2.0 WebSSO protocol** checkbox.
   - In the **Relying party SAML 2.0 SSO service URL** field, enter the SSO URL for your Snowflake account appended with `/fed/login`. For example, to use the Account Name URL with private connectivity, enter: `https://<orgname>-<account_name>.privatelink.snowflakecomputing.com/fed/login`. For a list of possible URL formats, see [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url). When you [create the security integration](/user-guide/admin-security-fed-auth-security-integration#label-saml-sso-create-integration) for federated authentication, make sure its URL parameters match the format used in this field.
6. In the next screen, in the **Relying party trust identifier** field, enter the URL for your Snowflake account as specified in the
   previous step.
7. In the next screen, select the
   **I do not want to configure multi-factor authentication settings for this relying party trust at this time** radio button.
8. In the next screen, select the **Permit all users to access this relying party** radio button.
9. In the next screen, review your configuration for the relying party trust. Also ensure that in the **Advanced** tab,
   **SHA-256** is selected as the secure hash algorithm.
10. In the next screen, select **Open the Edit Claim Rules dialog for this relying party trust when the wizard closes** and click
    **Close** to finish the wizard configuration.

### Define claim rules for the Snowflake relying party trust

The **Edit Claim Rules for** `snowflake_trust_name` window opens automatically after closing the wizard. You can also open this window from the
AD FS Management console by clicking on:

> **AD FS** » **Trust Relationships** » **Relying Party Trusts** » `snowflake_trust_name` » **Edit Claim Rules…**

In the window:

1. Create a rule for sending LDAP attributes as claims:

   1. Click **Add Rules** and select **Send LDAP Attributes as Claim**.
   2. In the **Edit Rule** dialog:

      - Enter a name (e.g. “Get Attributes”) for the rule.
        - Set **Attribute store** to: **Active Directory**.
        - Add two LDAP attributes for the rule:
          - **E-Mail-Addresses** with **E-Mail Address** as the Outgoing Claim Type.
          - **Display-Name** with **Name** as the Outgoing Claim Type.
   3. Click the **OK** button to create the rule.
2. Create a rule for transforming incoming claims:

   1. Click **Add Rules** and select **Transform an Incoming Claim**.
   2. In the **Add Transform Claim Rule Wizard** dialog:

      - Enter a name (e.g. “Name ID Transform”) for the claim rule.
      - Set **Incoming claim type** to: **E-Mail Address**.
      - Set **Outgoing claim type** to: **Name ID**.
      - Set **Outgoing name ID format** to: **Email**.
      - Select the **Pass through all claim values** radio button.
   3. Click the **Finish** button to create the rule.
3. Click the **OK** button to finish adding claim rules for the Snowflake relying party trust.

Important

Ensure that you enter the values for the rules exactly as described above.

Also, ensure that the rules you created are listed in the following order:

1. LDAP Attributes
2. Incoming Claim Transform

The rules will not work correctly if there are any typos in the rules or the rules are not listed in the correct order.

### Enable global logout — Optional

To enable global logout for Snowflake in AD FS, in the AD FS Management console, click on:

> **AD FS** » **Trust Relationships** » **Relying Party Trusts** » *<snowflake\_trust\_name>* » **Properties**

In the **Properties** dialog:

1. Go to the **Endpoints** tab and click the **Add SAML…** button.
2. In the **Edit Endpoint** dialog:
   - Set **Endpoint type** to: **SAML Logout**.
   - Set **Binding** to: **POST** or **REDIRECT**.
   - Set **Trusted URL** to the value specified in step 1.
   - Leave **Response URL** blank.
   - Click the **OK** button to save your changes.

### Obtain IdP information

Snowflake as the service provider needs information about the IdP to establish a relationship between the two. You’ll need this information
when you configure Snowflake, as described in [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).

The preferred method of providing information about the IdP is to obtain its metadata URL, which Snowflake can use to dynamically obtain
all of the information it needs. You can also manually define this information in multiple parameters in Snowflake, but that process is
error prone and the parameters must be manually updated if IdP configuration settings change, including when certificates are rotated.

#### Obtain the metadata URL (Preferred)

1. Navigate to the integration that you created for Snowflake and select the **Sign On** tab.
2. Select the **Endpoints** tab.
3. Find the **Federation metadata document** field and copy the URL. This is your metadata URL.

#### Obtain the SSO URL and certificate

To complete the AD FS setup, obtain the SSO URL and certificate from AD FS. You will use these two values in the next step:
[Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).

- SSO URL
  :   The AD FS URL endpoint to which Snowflake will send SAML requests. This is typically the Login URL for AD FS, which is usually the IP address or the
      fully-qualified domain name (i.e. FQDN) of your AD FS server with `/adfs/ls` appended to the end.
- Certificate
  :   Used to verify communication between AD FS and Snowflake. You download it from the AD FS Management console:

  1. In the console, click on:
     **AD FS** » **Service** » **Certificates**
  2. In the **Certificates** page, right-click the **Token-signing** entry and click **View Certificate…**.
  3. In the **Certificate** dialog, select the **Details** tab.
  4. Click **Copy to File…** to open the Certificate Export Wizard.
  5. For the export file format, select **Base-64 encoded X.509 (.CER)** and click **Next**.
  6. Save the file to a directory on your local environment.
  7. Open the file and copy the certificate, which consists of a single line located between the following lines:

     ```
     -----BEGIN CERTIFICATE-----
     <certificate>
     -----END CERTIFICATE-----
     ```

## Custom IdP setup

To use a SAML 2.0-compliant service or application as your IdP for federated authentication, you must perform the following tasks:

1. In the service/application interface, define a custom SHA-256 application for Snowflake. The instructions for defining a custom application are specific to
   the service/application that is serving as the IdP.
2. In the interface, create a user for each person who will need access to Snowflake. When creating users, make sure to include an email address for each
   user. Email addresses are required to connect the users in the IdP with their corresponding users in Snowflake.
3. Obtain the SSO URL and certificate from your Custom IdP. You will need the SSO URL value and Certificate in the next step,
   [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).
   - SSO URL (IdP URL endpoint to which Snowflake will send SAML requests)
   - Certificate (used to verify communication between the IdP and Snowflake)

Important

When configuring custom identity providers, field values are often case-sensitive. If error messages or error codes appear, double-check the casing for any
values you may have entered in the configuration process.

## Next steps

After you have completed the steps above, you must
[configure Snowflake to use federated authentication](/user-guide/admin-security-fed-auth-security-integration) to complete your custom IdP setup.
