# CREATE SECURITY INTEGRATION (SAML2)

Creates a new SAML2 security integration in the account or replaces an existing integration. A SAML2 security integration provides
single sign-on (SSO) workflows by creating an interface between Snowflake and a third-party Identity Provider (IdP).

For information about creating other types of security integrations (e.g. SCIM), see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration).

See also:
:   [ALTER SECURITY INTEGRATION (SAML2)](/sql-reference/sql/alter-security-integration-saml2) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = SAML2
    ENABLED = { TRUE | FALSE }
    { METADATA_URL = '<string_literal>' | <idp_parameters> }
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = '<string_literal>' ]
    [ SAML2_ENABLE_SP_INITIATED = TRUE | FALSE ]
    [ SAML2_SNOWFLAKE_X509_CERT = '<string_literal>' ]
    [ SAML2_SIGN_REQUEST = TRUE | FALSE ]
    [ SAML2_REQUESTED_NAMEID_FORMAT = '<string_literal>' ]
    [ SAML2_POST_LOGOUT_REDIRECT_URL = '<string_literal>' ]
    [ SAML2_FORCE_AUTHN = TRUE | FALSE ]
    [ SAML2_SNOWFLAKE_ISSUER_URL = '<string_literal>' ]
    [ SAML2_SNOWFLAKE_ACS_URL = '<string_literal>' ]
    [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = SAML2`
:   Specify the type of integration:

    - `SAML2`: Creates a security interface between Snowflake and the identity provider (IdP).

`ENABLED = { TRUE | FALSE }`
:   The Boolean that specifies whether to initiate operation of the integration or suspend it.

    - `TRUE` allows the integration to run based on the parameters specified in the pipe definition.
    - `FALSE` suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    The value is case-insensitive.

    The default is `TRUE`.

`{ METADATA_URL = 'string_literal' | idp_parameters }`
:   Specifies information about the IdP to establish the relationship between the IdP and Snowflake as the service provider.

    You must use the METADATA\_URL parameter or the other required IdP parameters, but can’t specify both. Snowflake uses a metadata
    URL to obtain all of the information specified by the other parameters. The metadata URL is preferred because it’s less error prone and
    allows Snowflake to dynamically update IdP configuration settings.

    `METADATA_URL = 'string_literal'`
    :   Specifies the metadata URL of the IdP. A metadata URL is an endpoint that allows Snowflake to dynamically
        retrieve and synchronize IdP configuration settings, including certificate updates.

        This parameter is only supported for Okta and Microsoft Entra ID. For help obtaining the metadata URL, see the section in
        [Configuring an identity provider (IdP) for Snowflake](/user-guide/admin-security-fed-auth-configure-idp) that corresponds to your IdP.

        After defining the metadata URL, you can keep Snowflake up-to-date with modified IdP configuration settings by running an ALTER
        SECURITY INTEGRATION REFRESH METADATA\_URL command.

    `idp_parameters`
    :   Parameters that specify information about the IdP, including its issuer identifier and certificate. The parameters can’t be set if you
        specified a `METADATA_URL`.

        `SAML2_ISSUER = 'string_literal'`
        :   The string containing the EntityID / Issuer of the IdP.

        `SAML2_SSO_URL = 'string_literal'`
        :   The string containing the IdP SSO URL, where the user should be redirected by Snowflake (the Service Provider) with a SAML
            `AuthnRequest` message.

        `SAML2_PROVIDER = 'string_literal'`
        :   The string describing the IdP.

            One of the following: OKTA, ADFS, `Custom`.

        `SAML2_X509_CERT = 'string_literal'`
        :   The Base64 encoded IdP signing certificate on a single line without the leading `-----BEGIN CERTIFICATE-----` and ending
            `-----END CERTIFICATE-----` markers.

## Optional parameters

`ALLOWED_USER_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   A list of email domains that can authenticate with a SAML2 security integration. For example,
    `ALLOWED_USER_DOMAINS = ("example.com", "example2.com", ...)`.

    This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

`ALLOWED_EMAIL_PATTERNS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   A list of regular expressions that email addresses are matched against to authenticate with a SAML2 security integration. For example,
    `ALLOWED_EMAIL_PATTERNS = ("^(.+dev)@example.com$", "^(.+dev)@example2.com$", ... )`.

    This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

`SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = 'string_literal'`
:   The string containing the label to display after the **Log In With** button on the login page.

`SAML2_ENABLE_SP_INITIATED = { TRUE | FALSE }`
:   The Boolean indicating if the **Log In With** button will be shown on the login page.

    - `TRUE` displays the **Log in With** button on the login page.
    - `FALSE` does not display the **Log in With** button on the login page.

`SAML2_SNOWFLAKE_X509_CERT = 'string_literal'`
:   The Base64 encoded self-signed certificate generated by Snowflake used for [encrypting SAML assertions](/user-guide/admin-security-fed-auth-security-integration#label-encrypt-saml-assertions) and [sending signed SAML requests](/user-guide/admin-security-fed-auth-security-integration#label-sign-saml-requests).

    You must have at least one of these features (encrypted SAML assertions or signed SAML responses) enabled in your Snowflake account to
    access the certificate value.

`SAML2_SIGN_REQUEST = { TRUE | FALSE }`
:   The Boolean indicating whether SAML requests are signed.

    - `TRUE` allows SAML requests to be signed.
    - `FALSE` does not allow SAML requests to be signed.

`SAML2_REQUESTED_NAMEID_FORMAT = 'string_literal'`
:   The SAML NameID format allows Snowflake to set an expectation of the identifying attribute of the user (i.e. SAML Subject) in the SAML
    assertion from the IdP to ensure a valid authentication to Snowflake. If a value is not specified, Snowflake sends the
    `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` value in the authentication request to the IdP.

    Optional.

    If you choose to specify the SAML `NameID` format, use one of the following values:

    - `urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified`
    - `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress`
    - `urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName`
    - `urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName`
    - `urn:oasis:names:tc:SAML:2.0:nameid-format:kerberos`
    - `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`
    - `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`

`SAML2_POST_LOGOUT_REDIRECT_URL = 'string_literal'`
:   The endpoint to which Snowflake redirects users after clicking the **Log Out** button in Snowsight.

    Snowflake terminates the Snowflake session upon redirecting to the specified endpoint.

`SAML2_FORCE_AUTHN = { TRUE | FALSE }`
:   The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake. When
    set to `TRUE`, Snowflake sets the `ForceAuthn` SAML parameter to `TRUE` in the outgoing request from Snowflake to the
    identity provider.

    - `TRUE` forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists.
    - `FALSE` does not force users to authenticate again to access Snowflake.

    Default: `FALSE`.

`SAML2_SNOWFLAKE_ISSUER_URL = 'string_literal'`
:   The string containing the `EntityID` / `Issuer` for the Snowflake service provider.

    If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use.

    The value of this property must match the Snowflake account URL specified in the IdP. It defaults to the
    [legacy URL](/user-guide/admin-account-identifier#label-account-locator), so if you define a different [URL format](/user-guide/organizations-connect#label-connecting-via-url) in the IdP, make
    sure to set this property appropriately when creating the security integration. For details, see [Create a SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration#label-saml-sso-create-integration).

`SAML2_SNOWFLAKE_ACS_URL = 'string_literal'`
:   The string containing the Snowflake Assertion Consumer Service URL to which the IdP will send its SAML authentication response back to
    Snowflake. This property will be set in the SAML authentication request generated by Snowflake when initiating a SAML SSO operation with
    the IdP.

    If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use.

    The value of this property must match the Snowflake account URL specified in the IdP. It defaults to the
    [legacy URL](/user-guide/admin-account-identifier#label-account-locator), so if you define a different [URL format](/user-guide/organizations-connect#label-connecting-via-url) in the IdP, make
    sure to set this property appropriately when creating the security integration. For details, see [Create a SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration#label-saml-sso-create-integration).

    Default: `https://<account_locator>.<region>.snowflakecomputing.com/fed/login`

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Example

The following example creates a Microsoft Active Directory Federation Services (AD FS) security integration with the two optional settings:

Copy code

```
CREATE SECURITY INTEGRATION my_idp
  TYPE = saml2
  ENABLED = true
  METADATA_URL = 'https://integrator-26580.okta.com/app/ex2kbcS30N697/sso/saml/metadata'
  SAML2_SNOWFLAKE_ISSUER_URL = 'https://myorg-acct1.privatelink.snowflakecomputing.com'
  SAML2_SNOWFLAKE_ACS_URL = 'https://myorg-acct1.privatelink.snowflakecomputing.com/fed/login';
```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

> Copy code
>
> ```
> DESC SECURITY INTEGRATION my_idp;
> ```
