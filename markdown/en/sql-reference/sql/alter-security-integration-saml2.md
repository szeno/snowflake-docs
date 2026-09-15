# ALTER SECURITY INTEGRATION (SAML2)

Modifies the properties of an existing SAML2 security integration. For information about modifying other types of
security integrations (e.g. SCIM), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

See also:
:   [CREATE SECURITY INTEGRATION (SAML2)](/sql-reference/sql/create-security-integration-saml2) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET
    [ TYPE = SAML2 ]
    [ ENABLED = { TRUE | FALSE } ]
    [ METADATA_URL = '<string_literal>' ]
    [ SAML2_ISSUER = '<string_literal>' ]
    [ SAML2_SSO_URL = '<string_literal>' ]
    [ SAML2_PROVIDER = '<string_literal>' ]
    [ SAML2_X509_CERT = '<string_literal>' ]
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

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> UNSET {
    ENABLED |
    [ , ... ]
    }

ALTER [ SECURITY ] INTEGRATION <name> REFRESH
  [ SAML2_SNOWFLAKE_PRIVATE_KEY ]
  [ METADATA_URL ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Identifier for the integration to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ALLOWED_USER_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Specifies a list of email domains that can authenticate with a SAML2 security integration. For example,
        `ALLOWED_USER_DOMAINS = ("example.com", "example2.com", ...)`.

        This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

    `ALLOWED_EMAIL_PATTERNS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Specifies a list of regular expressions that email addresses are matched against to authenticate with a SAML2 security integration. For
        example,
        `ALLOWED_EMAIL_PATTERNS = ("^(.+dev)@example.com$", "^(.+dev)@example2.com$", ... )`.

        This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

    `TYPE = SAML2`
    :   Specify the type of integration:

    - `SAML2`: Creates a security interface between Snowflake and the identity provider.

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to initiate operation of the integration or suspend it.

        - `TRUE` allows the integration to run based on the parameters specified in the integration definition.
        - `FALSE` suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    `METADATA_URL = 'string_literal'`
    :   Specifies the metadata URL of the IdP. A metadata URL is an endpoint that allows Snowflake to dynamically
        retrieve and synchronize IdP configuration settings, including certificate updates.

        This parameter is only supported for Okta and Microsoft Entra ID. For help obtaining the metadata URL, see the section in [Configuring an identity provider (IdP) for Snowflake](/user-guide/admin-security-fed-auth-configure-idp) that corresponds to your IdP.

        If you specify a metadata URL, you can’t use the `SAML2_ISSUER`, `SAML2_SSO_URL`, `SAML2_PROVIDER`, and
        `SAML2_X509_CERT` parameters. The information specified with these parameters is obtained from the metadata URL.

    `SAML2_ISSUER = 'string_literal'`
    :   The string containing the EntityID / Issuer of the IdP.

    `SAML2_SSO_URL = 'string_literal'`
    :   The string containing the IdP SSO URL, where the user should be redirected by Snowflake (the Service Provider) with a SAML
        `AuthnRequest` message.

    `SAML2_PROVIDER = 'string_literal'`
    :   The string describing the IdP.

        One of the following: OKTA, ADFS, Custom.

    `SAML2_X509_CERT = 'string_literal'`
    :   The Base64 encoded IdP signing certificate on a single line without the leading `-----BEGIN CERTIFICATE-----` and ending
        `-----END CERTIFICATE-----` markers.

    `SAML2_SP_INITIATED_LOGIN_PAGE_LABEL = 'string_literal'`
    :   The string containing the label to display after the **Log In With** button on the login page.

    `SAML2_ENABLE_SP_INITIATED = TRUE | FALSE`
    :   The Boolean indicating if the **Log In With** button will be shown on the login page.

        - `TRUE` displays the **Log in With** button on the login page.
        - `FALSE` does not display the **Log in With** button on the login page.

    `SAML2_SNOWFLAKE_X509_CERT = 'string_literal'`
    :   The Base64 encoded self-signed certificate generated by Snowflake for use with [Encrypt SAML assertions](/user-guide/admin-security-fed-auth-security-integration#label-encrypt-saml-assertions) and
        [Send signed SAML requests](/user-guide/admin-security-fed-auth-security-integration#label-sign-saml-requests).

        You must have at least one of these features (encrypted SAML assertions or signed SAML responses) enabled in your Snowflake account to
        access the certificate value.

    `SAML2_SIGN_REQUEST = TRUE | FALSE`
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

    `SAML2_POST_LOGOUT_REDIRECT_URL = '<string_literal>'`
    :   The endpoint to which Snowflake redirects users after clicking the **Log Out** button in Snowsight.

        Snowflake terminates the Snowflake session upon redirecting to the specified endpoint.

    `SAML2_FORCE_AUTHN = TRUE | FALSE`
    :   The Boolean indicating whether users, during the initial authentication flow, are forced to authenticate again to access Snowflake.
        When set to `TRUE`, Snowflake sets the `ForceAuthn` SAML parameter to `TRUE` in the outgoing request from Snowflake
        to the identity provider.

        - `TRUE` forces users to authenticate again to access Snowflake, even if a valid session with the identity provider exists.
        - `FALSE` does not force users to authenticate again to access Snowflake.

        Default: `FALSE`.

    `SAML2_SNOWFLAKE_ISSUER_URL = '<string_literal>'`
    :   The string containing the `EntityID` / `Issuer` for the Snowflake service provider.

        If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use.

        The value of this property must match the Snowflake account URL specified in the IdP. It defaults to the
        [legacy URL](/user-guide/admin-account-identifier#label-account-locator), so if you define a different [URL format](/user-guide/organizations-connect#label-connecting-via-url) in the IdP, make
        sure to set this property appropriately.

    `SAML2_SNOWFLAKE_ACS_URL = '<string_literal>'`
    :   The string containing the Snowflake Assertion Consumer Service URL to which the IdP will send its SAML authentication response back to
        Snowflake. This property will be set in the SAML authentication request generated by Snowflake when initiating a SAML SSO operation with the IdP.

        If an incorrect value is specified, Snowflake returns an error message indicating the acceptable values to use.

        The value of this property must match the Snowflake account URL specified in the IdP. It defaults to the
        [legacy URL](/user-guide/admin-account-identifier#label-account-locator), so if you define a different [URL format](/user-guide/organizations-connect#label-connecting-via-url) in the IdP,
        make sure to set this property appropriately.

        Default: `https://<account_locator>.<region>.snowflakecomputing.com/fed/login`

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the integration.

        Default: No value

`REFRESH ...`
:   Updates integration values.

    `SAML2_SNOWFLAKE_PRIVATE_KEY`
    :   Generates a new private key and self-signed certificate for a SAML2 security integration. The old private key and self-signed
        certificate are overwritten by the new ones. For more information about best practices for rotating keys, see
        [Manage Your SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration#label-modify-saml2-security-integration).

    `METADATA_URL`
    :   Updates the security integration with the current IdP configuration settings. Snowflake uses the metadata URL, which is specified with
        the integration’s `METADATA_URL` parameter, to update the settings. Use `REFRESH METADATA_URL` to keep Snowflake
        synchronized with modified IdP configuration settings, including certificate updates, without manually updating parameters.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the security integration, which resets them back to their defaults:

    - `ENABLED`
    - `TAG tag_name [ , tag_name ... ]`

## Usage notes

- Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- After rotating your `SAML2_SNOWFLAKE_PRIVATE_KEY` using the `REFRESH` command, you need to upload your new
  `SAML2_SNOWFLAKE_X509_CERT` value to your IdP, otherwise SAML authentication stops working. For more information about best
  practices around rotating keys, see [Manage Your SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration#label-modify-saml2-security-integration).

## Examples

- The following example initiates operation of a suspended integration:

  Copy code

  ```
  ALTER SECURITY INTEGRATION myint SET ENABLED = TRUE;
  ```
- The following example rotates the private key and generates a new self-signed certificate for a SAML2 security integration named
  `my_idp`:

  Caution

  After running the command below, SAML authentication stops working because your IdP still uses your old
  `SAML2_SNOWFLAKE_X509_CERT` certificate. To minimize disruptions, you should run this command when users are not as active. For
  more information, see [Manage Your SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration#label-modify-saml2-security-integration).

  Copy code

  ```
  alter security integration my_idp refresh SAML2_SNOWFLAKE_PRIVATE_KEY;
  ```
