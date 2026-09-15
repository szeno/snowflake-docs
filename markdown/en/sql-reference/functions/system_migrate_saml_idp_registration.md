Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$MIGRATE\_SAML\_IDP\_REGISTRATION

Migrates an existing SAML identity provider (i.e. IdP) configuration as defined by the account parameter [SAML\_IDENTITY\_PROVIDER](/sql-reference/parameters#label-saml-identity-provider) to a security integration.

If the account parameter SAML\_IDENTITY\_PROVIDER is present, SYSTEM$MIGRATE\_SAML\_IDP\_REGISTRATION creates a new security integration using the data in the SAML\_IDENTITY\_PROVIDER parameter.

If the SAML\_IDENTITY\_PROVIDER account parameter is not present, the function fails. If this occurs, create a security integration where `TYPE = SAML2` as shown in [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-saml2).

## Syntax

Copy code

```
SYSTEM$MIGRATE_SAML_IDP_REGISTRATION( '<integration_name>', '<issuer>' )
```

## Arguments

`integration_name`
:   Name of the new SAML2 security integration that will be created by the function.

    Note that the entire name must be enclosed in single quotes.

    Required.

`issuer`
:   The EntityID / Issuer of the IdP.

    The entire name must be enclosed in single quotes.

    Required if not specified in the SAML\_IDENTITY\_PROVIDER parameter as the `Issuer` attribute.

    Important

    If the SAML\_IDENTITY\_PROVIDER parameter does not contain a value for `Issuer`, use your IdP’s metadata to locate the exact
    value. Depending on the IdP, you might be able to locate the `issuer` value through the user interface administrator settings,
    a URL your IdP provides, or by downloading the SAML federation metadata XML to a local file.

    As a representative example, the following references detail how to locate the `issuer` value for Okta and Microsoft Entra ID:

    - [Okta SAML Settings](https://developer.okta.com/docs/guides/build-sso-integration/saml2/specify-your-settings/)
    - [Microsoft Entra ID integration with Snowflake](https://docs.microsoft.com/en-us/azure/active-directory/saas-apps/snowflake-tutorial)

## Examples

The commands below provide an example of how you can migrate an existing IdP configuration:

Copy code

```
SELECT SYSTEM$MIGRATE_SAML_IDP_REGISTRATION('my_fed_integration', 'http://my_idp.com');
```

Output:

```
+---------------------------------------------------------------------------------+
| SYSTEM$MIGRATE_SAML_IDP_REGISTRATION('MY_FED_INTEGRATION', 'HTTP://MY_IDP.COM') |
+---------------------------------------------------------------------------------+
| SUCCESS : [MY_FED_INTEGRATION] Fed SAML integration created                     |
+---------------------------------------------------------------------------------+
```

To view details about your migrated IdP, you can use the `DESCRIBE` command:

Copy code

```
DESC INTEGRATION my_fed_integration;
```
