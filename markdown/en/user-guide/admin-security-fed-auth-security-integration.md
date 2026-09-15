# Configuring SAML 2.0 federated authentication

This topic describes how to configure Snowflake for federated authentication using a SAML2 security integration. For OpenID Connect (OIDC), see [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc). This topic assumes you have
already [configured your IdP to work with Snowflake](/user-guide/admin-security-fed-auth-configure-idp).

Note

A SAML2 security integration replaces the deprecated [SAML\_IDENTITY\_PROVIDER](/sql-reference/parameters#label-saml-identity-provider) account parameter.

If you have an existing SSO implementation that uses this deprecated account parameter, you should [migrate to a SAML security integration](/user-guide/admin-security-fed-auth-configure-snowflake) before continuing to configure Snowflake for federated
authentication.

Snowflake will continue to support the deprecated account parameter as long as there are implementations that use it.

## Create a SAML2 security integration

Snowflake uses a SAML2 security integration to integrate with the IdP you are using to implement federated authentication. Use the
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-saml2) command to start configuring Snowflake for SSO.

Before you begin

- When you [configured an IdP](/user-guide/admin-security-fed-auth-configure-idp) for SSO, you provided a URL for the Snowflake
  account. The [format](/user-guide/organizations-connect#label-connecting-via-url) of this URL must match the URLs in the `SAML2_SNOWFLAKE_ISSUER_URL` and
  `SAML2_SNOWFLAKE_ACS_URL` properties of the security integration.

  If you do not define these properties when creating the security integration, then they default to the
  [legacy URL](/user-guide/admin-account-identifier#label-account-locator) of the account.
- Note that `/fed/login` is appended to the URL for the `SAML2_SNOWFLAKE_ACS_URL` property.
- The preferred method of providing information about the IdP to Snowflake is to use the integration’s `METADATA_URL` parameter to
  specify the IdP’s metadata URL. Snowflake uses the metadata URL to dynamically obtain the IdP’s configuration settings, including its
  certificate.

  If you define the IdP’s metadata URL, then you can run an ALTER SECURITY INTEGRATION REFRESH METADATA\_URL command to refresh the IdP’s
  configuration settings without having to change any of the integration’s parameters. This simplifies the rotation of certificates.

For example, to create a security integration that uses an account name URL with private connectivity, run the following SQL command:

Copy code

```
CREATE SECURITY INTEGRATION my_idp
  TYPE = saml2
  ENABLED = true
  METADATA_URL = 'https://integrator-26580.okta.com/app/ex2kbcS30N697/sso/saml/metadata'
  SAML2_SNOWFLAKE_ISSUER_URL = 'https://<orgname>-<account_name>.privatelink.snowflakecomputing.com'
  SAML2_SNOWFLAKE_ACS_URL = 'https://<orgname>-<account_name>.privatelink.snowflakecomputing.com/fed/login';
```

After configuring a SAML2 security integration, you can use the security integration to do the following tasks:

- Encrypt SAML Assertions
- Send Signed SAML Requests
- Specify the SAML NameID Format
- Export the SAML2 Security Integration Metadata
- Force Re-authentication to Snowflake Procedure

Note

You can [use a SAML2 security integration with Client Redirect](/user-guide/account-replication-security-integrations#label-account-replication-security-integration-saml2) if your
account is a [Business Critical Edition or higher](/user-guide/replication-intro).

For more information, see [Redirecting client connections](/user-guide/client-redirect).

## Configure SSO login for users

After you have created a SAML2 security integration, you can configure whether the user starts their SSO login from the IdP or from
Snowflake.

An IdP-initiated SSO does not require configuration in Snowflake. You only need to inform your users about how to access Snowflake (e.g.
using an internal portal).

The `SAML2_ENABLE_SP_INITIATED` property enables Snowflake-initiated SSO. The `SAML2_SP_INITIATED_LOGIN_PAGE_LABEL` property
defines a string that identifies the IdP. This string appears on the Snowflake login page so users can access the IdP.

Use the `ALTER SECURITY INTEGRATION` command to set these properties:

Copy code

```
ALTER SECURITY INTEGRATION my_idp SET SAML2_ENABLE_SP_INITIATED = true;
ALTER SECURITY INTEGRATION my_idp SET SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = 'My IdP';
```

For information about how clients connect to Snowflake after you have configured SSO login for users, see
[Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients)

## Encrypt SAML assertions

The `SAML2_SNOWFLAKE_X509_CERT` property ensures that SAML2 assertions are encrypted using Snowflake’s public certificate, securing
traffic when users access Snowflake through federated authentication.

After receiving the encrypted assertions from the customer IdP, Snowflake decrypts the encrypted assertions with its private key. Snowflake
never exports or makes its private key available.

To encrypt SAML assertions, see the sections below.

### Export the public certificate from Snowflake

After you have [created a SAML2 security integration](#label-saml-sso-create-integration), follow the steps below:

1. Execute the following SQL statement on the SAML2 integration.

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```
2. Find the `SAML2_SNOWFLAKE_X509_CERT` value in row 7, which is the public certificate in PEM format.
3. Save the value, ensuring you include the `BEGIN CERTIFICATE` and `END CERTIFICATE` delimiters. For example, the codeblock
   below contains a truncated certificate in PEM format:

   ```
   -----BEGIN CERTIFICATE-----
   MIICr...
   -----END CERTIFICATE-----
   ```

### Create a certificate signing request (CSR) — *Optional*

By default, a SAML2 security integration in Snowflake uses a self-signed certificate for the SAML IdP to encrypt SAML assertions. If your
organization requires using a certificate issued from a Certificate Authority (CA), then complete the steps below:

1. Generate a certificate signing request (CSR) from Snowflake using the system function
   [SYSTEM$GENERATE\_SAML\_CSR](/sql-reference/functions/system_generate_saml_csr).
2. Provide the CSR to the CA of your choice so that the certificate can be issued.
3. Upload the Base64-encoded certificate into the SAML integration using the following ALTER statement, without the
   `BEGIN CERTIFICATE` and `END CERTIFICATE` delimiters.

   Copy code

   ```
   ALTER SECURITY INTEGRATION my_idp SET SAML2_SNOWFLAKE_X509_CERT = 'AX2bv...';
   ```
4. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to view the updated security integration:

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```

You can then upload the certificate for your private key using the CSR generated by the function into Snowflake.

### Configure Your SAML IdP

1. Upload the saved certificate in PEM format to your organization’s IdP as the SAML Encryption certificate.
2. Configure your IdP to encrypt SAML Assertions for the Snowflake service provider (SP).

## Send signed SAML requests

You can send a signed SAML request from Snowflake to the IdP to verify Snowflake as an authentic service provider. To verify Snowflake, you
can configure your IdP to use the certificate stored in the SAML2 security integration to ensure the SAML request originates from Snowflake,
not a third-party that is impersonating Snowflake.

### Set the SAML2\_SIGN\_REQUEST property

If you are [creating a SAML2 security integration](#label-saml-sso-create-integration) for the first time, ensure you set the
[SAML2\_SIGN\_REQUEST](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property.

If you created a SAML2 security integration without setting the `SAML2_SIGN_REQUEST` property, follow the steps below:

1. Execute the [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2) command as a user with an
   ACCOUNTADMIN role to update the security integration:

   Copy code

   ```
   ALTER SECURITY INTEGRATION my_idp SET SAML2_SIGN_REQUEST = true;
   ```
2. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to view the updated security integration:

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```

### Configure your IdP to accept signed requests

Configure your IdP to accept signed requests from Snowflake. During the configuration, your IdP needs to have the certificate stored in the
[SAML2\_SNOWFLAKE\_X509\_CERT](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property. Your IdP uses this certificate to verify
that the SAML request originates from Snowflake.

Note

Snowflake is not responsible for configuring your IdP. For help with configuring your IdP, please consult your internal security
administrator.

1. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command:

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```
2. Save the value of the [SAML2\_SNOWFLAKE\_X509\_CERT](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property in row 7 to use in
   your IdP settings.

## Specify the SAML `NameID` format

Snowflake supports allowing the administrator (i.e. user with the ACCOUNTADMIN role) to specify the SAML `NameID` format that will be
requested in the outgoing SAML authentication request sent from Snowflake to the IdP.

Specifying the SAML `NameID` format allows Snowflake to set an expectation of the identifying attribute of the user (i.e. SAML
Subject) in the SAML assertion from the IdP to ensure a valid authentication to Snowflake.

The SAML `NameID` format can be integrated into the SAML2 security integration. You can specify the SAML `NameID` in the
security integration using one of the following values:

- `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified`
- `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`
- `urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName`
- `urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName`
- `urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos`
- `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`
- `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`

If the SAML `NameID` format is not specified, Snowflake uses the following value:

`urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`

### Set the SAML2\_REQUESTED\_NAMEID\_FORMAT property

If you are [creating a SAML2 security integration](#label-saml-sso-create-integration) for the first time, ensure you set the
[SAML2\_REQUESTED\_NAMEID\_FORMAT](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property.

If you created a SAML2 security integration without setting the `SAML2_REQUESTED_NAMEID_FORMAT` property, follow the steps below:

1. Execute the [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2) command as a user with an
   ACCOUNTADMIN role to specify the SAML `NameId` format:

   Copy code

   ```
   ALTER SECURITY INTEGRATION my_idp SET SAML2_REQUESTED_NAMEID_FORMAT = '<string_literal>';
   ```
2. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to view the updated security integration:

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```

### Configure your IdP to specify the `NameID`

Configure your IdP to specify the SAML `NameID` format in SAML assertions.

Note

Snowflake is not responsible for configuring your IdP. For help with configuring your IdP, please consult your internal security
administrator.

## Export the SAML2 security integration metadata

Snowflake provides SAML 2.0 metadata for the SAML2 security integration to facilitate configuring the Snowflake service provider in your
IdP.

The SAML 2.0 metadata is contained in the `SAML2_SNOWFLAKE_METADATA` property and can be obtained by executing a
[DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command on the SAML2 security integration. For example:

Copy code

```
DESC SECURITY INTEGRATION my_idp;
```

```
------------------------------------+---------------+-----------------------------------------------------------------------------+------------------+
              property              | property_type |                               property_value                                | property_default |
------------------------------------+---------------+-----------------------------------------------------------------------------+------------------+
SAML2_X509_CERT                     | String        | MIICr...                                                                    |                  |
SAML2_PROVIDER                      | String        | OKTA                                                                        |                  |
SAML2_ENABLE_SP_INITIATED           | Boolean       | false                                                                       | false            |
SAML2_SP_INITIATED_LOGIN_PAGE_LABEL | String        | my_idp                                                                      |                  |
SAML2_SSO_URL                       | String        | https://okta.com/sso                                                        |                  |
SAML2_ISSUER                        | String        | https://okta.com                                                            |                  |
SAML2_SNOWFLAKE_X509_CERT           | String        | MIICr...                                                                    |                  |
SAML2_REQUESTED_NAMEID_FORMAT       | String        | urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress                      |                  |
SAML2_SNOWFLAKE_ACS_URL             | String        | https://example.snowflakecomputing.com/fed/login                            |                  |
SAML2_SNOWFLAKE_ISSUER_URL          | String        | https://example.snowflakecomputing.com                                      |                  |
SAML2_SNOWFLAKE_METADATA            | String        | <md:EntityDescriptor entityID="https://example.snowflakecomputing.com"> ... |                  |
SAML2_DIGEST_METHODS_USED           | String        | http://www.w3.org/2001/04/xmlenc#sha256                                     |                  |
SAML2_SIGNATURE_METHODS_USED        | String        | http://www.w3.org/2001/04/xmldsig-more#rsa-sha256                           |                  |
------------------------------------+---------------+-----------------------------------------------------------------------------+------------------+
```

As a representative example, the formatted SAML 2.0 XML metadata from the `SAML2_SNOWFLAKE_METADATA` property is shown below. Note
that the `X509certificate` values for `signing` and `encryption` are truncated.

Copy code

```
<md:EntityDescriptor xmlns:dsig="http://www.w3.org/2000/09/xmldsig#" xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:xenc="http://www.w3.org/2001/04/xmlenc#" xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion" entityID="https://example.snowflakecomputing.com">
 <md:SPSSODescriptor AuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
  <md:KeyDescriptor use="signing">
    <dsig:KeyInfo>
      <dsig:X509Data>
        <dsig:X509Certificate>MIICr...</dsig:X509Certificate>
      </dsig:X509Data>
    </dsig:KeyInfo>
  </md:KeyDescriptor>
  <md:KeyDescriptor use="encryption">
    <dsig:KeyInfo>
      <dsig:X509Data>
        <dsig:X509Certificate>MIICr...</dsig:X509Certificate>
      </dsig:X509Data>
    </dsig:KeyInfo>
  </md:KeyDescriptor>
  <md:AssertionConsumerService index="0" isDefault="true" Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://example.snowflakecomputing.com/fed/login" />
 </md:SPSSODescriptor>
</md:EntityDescriptor>
```

For reference, the following table maps the XML metadata tags to the Snowflake SAML2 security integration properties.

| XML Output | SAML2 Security Integration Property |
| --- | --- |
| entityID | SAML2\_SNOWFLAKE\_ISSUER\_URL |
| AuthnRequestsSigned | SAML2\_SIGN\_REQUEST |
| Signing Certificate | SAML2\_SNOWFLAKE\_X509\_CERT |
| Encryption Certificate | SAML2\_SNOWFLAKE\_X509\_CERT |
| Assertion Consumer Service URL | SAML2\_SNOWFLAKE\_ACS\_URL |

Expand

Show lessSee more

## Force re-authentication to Snowflake

Snowflake supports configuring your SAML2 security integration to require the authenticating user to re-authenticate to access Snowflake
during the initial authentication SSO flow or when a current Snowflake session expires.

When enabling this feature in the Snowflake SAML2 security integration, Snowflake sets the SAML specification `ForceAuthn` property
to `True` in the outgoing SAML request from Snowflake to the IdP. Once the IdP receives the request with `ForceAuthn` property
set to `True`, the IdP sends a request to Snowflake which results in users being prompted to re-enter their authentication credentials
(e.g. username, password) to access Snowflake.

This feature provides enhanced security through re-authentication. In addition, the re-authentication prompt allows users to input a
different set of credentials than those used to initiate SSO to access Snowflake.

Important

Before implementing this feature, verify that your IdP supports switching identities during an SSO authentication flow.

If this feature is implemented in Snowflake and your IdP does not support switching identities during the initial SSO authentication flow,
users might not be able to access Snowflake using the different set of credentials provided in the re-authentication prompt.

If you are [creating a SAML2 security integration](#label-saml-sso-create-integration) for the first time, ensure you set the
[SAML2\_FORCE\_AUTHN](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property.

To update an existing SAML2 security integration to support forced re-authentication to access Snowflake, follow the steps below:

1. Execute the [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2) command to update the security
   integration:

   Copy code

   ```
   ALTER SECURITY INTEGRATION my_idp SET SAML2_FORCE_AUTHN = true;
   ```
2. Execute the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to view the updated security integration:

   Copy code

   ```
   DESC SECURITY INTEGRATION my_idp;
   ```

Where:

> `SAML2_FORCE_AUTHN = TRUE | FALSE`
> :   The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake. When
>     set to `TRUE`, Snowflake sets the `ForceAuthn` SAML property to `TRUE` in the outgoing request from Snowflake to the
>     identity provider.
>
>     - `TRUE` forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists.
>     - `FALSE` does not force users to authenticate again to access Snowflake.
>
>     Default: `FALSE`.

## Custom logout endpoint

Snowflake supports defining a custom endpoint URL to redirect users to after logging out of Snowflake. The endpoint is set through the
`SAML2_POST_LOGOUT_REDIRECT_URL` property in the SAML2 security integration.

Once enabled for users who access Snowflake through SAML SSO, clicking the **Log Out** button in Snowsight results in
Snowflake terminating the Snowflake session and redirecting users to the specified endpoint.

Important

This behavior does not apply to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).

Defining a logout endpoint provides administrators the option to control where users are redirected after logging out of Snowflake. For
example, a custom endpoint could trigger a script to simultaneously terminate the IdP session. The advantage of this implementation is that
both the Snowflake and IdP sessions are terminated, which forces users to re-authenticate against the IdP to access Snowflake.

If you are [creating a SAML2 security integration](#label-saml-sso-create-integration) for the first time, ensure you set the
[SAML2\_POST\_LOGOUT\_REDIRECT\_URL](/sql-reference/sql/create-security-integration-saml2#label-parameter-sql-reference-optional-parameters) property.

If you created a SAML2 security integration without setting the `SAML2_POST_LOGOUT_REDIRECT_URL` property, execute the
[ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2) command to configure the custom logout endpoint:

Copy code

```
ALTER SECURITY INTEGRATION my_idp SET SAML2_POST_LOGOUT_REDIRECT_URL = 'https://logout.example.com';
```

## Manage Your SAML2 security integration

You can use an [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2) command to manage the SAML2 security
integration. For example:

- Update the X.509 certificate as a string into an existing SAML2 security integration.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp SET SAML2_X509_CERT = 'AX2bv...';
  ```
- If you are a customer who configures your IdP to verify SAML request signatures or encrypt SAML responses, then you can overwrite your
  existing private key and self-signed certificate, and generate a new private key and self-signed certificate:

  1. Generate a new private key:

     Caution

     After running the command below, SAML authentication stops working because your IdP still uses your old
     `SAML2_SNOWFLAKE_X509_CERT` certificate. To minimize disruptions, you should run the command below when users are not as
     active.

     Copy code

     ```
     ALTER SECURITY INTEGRATION my_idp REFRESH SAML2_SNOWFLAKE_PRIVATE_KEY;
     ```
  2. Retrieve the value of the `SAML2_SNOWFLAKE_X509_CERT` property in your security integration:

     Copy code

     ```
     DESCRIBE SECURITY INTEGRATION my_idp;
     SELECT "property_value" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
       WHERE "property" = 'SAML2_SNOWFLAKE_X509_CERT';
     ```
  3. Upload the retrieved value to your IdP to replace your old certificate with your new certificate in your IdP.
- Enable signed requests.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp SET SAML2_SIGN_REQUEST = true;
  ```
- Specify the `NameID` format.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp SET SAML2_REQUESTED_NAMEID_FORMAT = 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified';
  ```
- Update an existing security integration to enable forced re-authentication.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp SET SAML2_FORCE_AUTHN = true;
  ```
- Update an existing security integration to disable forced re-authentication.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp UNSET SAML2_FORCE_AUTHN;
  ```
- Update the custom logout endpoint.

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_idp SET SAML2_POST_LOGOUT_REDIRECT_URL = 'https://logout.example.com';
  ```

For more information, see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-saml2).

# Replicate the SSO Configuration

Snowflake supports replication and failover/failback of the
[SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration) and
[OIDC security integration](/user-guide/admin-security-fed-auth-oidc) from a source account to a target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).
