# July 20, 2026: OIDC federated authentication (*Public Preview*)

OpenID Connect (OIDC) security integrations for federated single sign-on (SSO) are available in Public Preview. Multiple OIDC integrations, or
OIDC alongside an existing SAML2 integration, require [identifier-first login](/user-guide/identifier-first-login). Without
identifier-first login, only one SSO integration (SAML2 or OIDC) can be `ENABLED=TRUE` at a time.

Use a custom OIDC-compliant identity provider (IdP) or Google or Microsoft as a managed provider. Create an OIDC security integration with
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oidc). For Google or Microsoft, Snowflake manages the OAuth client
configuration:

Copy code

```
CREATE SECURITY INTEGRATION my_google_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'GOOGLE';
```

For Microsoft, set `OIDC_PROVIDER = 'MICROSOFT'` instead:

Copy code

```
CREATE SECURITY INTEGRATION my_microsoft_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'MICROSOFT';
```

Users managed by Entra ID must grant consent to Snowflake, or an admin must grant consent on their behalf. Your Registered App in Entra ID must also be configured to issue the optional `email` claim in ID tokens. See [OIDC federated authentication and SSO](/user-guide/admin-security-fed-auth-oidc#label-oidc-microsoft-managed-provider).

You can restrict login methods with authentication policies by setting `AUTHENTICATION_METHODS` to include `OIDC`. To require MFA after external
authentication (including OIDC SSO), set `MFA_POLICY=(ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION='ALL')`.

For more information, see [OIDC federated authentication and SSO](/user-guide/admin-security-fed-auth-oidc),
[CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc), and
[ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).
