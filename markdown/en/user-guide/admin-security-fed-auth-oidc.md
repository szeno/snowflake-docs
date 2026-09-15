# Configuring OpenID Connect (OIDC) federated authentication

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

OpenID Connect (OIDC) security integrations allow Snowflake to validate JSON Web Tokens (JWTs) issued by your identity provider (IdP) and map user identity claims to Snowflake users. OIDC, built on top of OAuth 2.0, enables IdPs to authenticate users and securely transmit identity information to Snowflake using signed JWTs.

Snowflake OIDC integrations support two types of OIDC providers:

- **Managed providers**: For example, `OIDC_PROVIDER = 'GOOGLE'` or `OIDC_PROVIDER = 'MICROSOFT'`. Snowflake handles the IdP app configuration, making it easy to enable social login experiences like “Sign in with Google” or “Sign in with Microsoft” with minimal setup.
- **Custom providers**: With `OIDC_PROVIDER = 'CUSTOM'`, use your own OpenID Connect-compliant IdP app (for example, Okta, PingFederate, Auth0, or Keycloak) and configure a matching OIDC security integration in Snowflake. You provide all configuration details, including client credentials and either an issuer URL (used for endpoint discovery) or explicit endpoints. For Microsoft Entra ID, use the managed `MICROSOFT` provider instead of a custom integration unless you need your own app registration.

Snowflake uses the **Authorization Code Flow with PKCE** (Proof Key for Code Exchange, per RFC 7636) for OIDC authentication.

## Supported sign-in surfaces

OIDC SSO is available for the following sign-in surfaces:

- Browser-based sign-in to Snowsight.
- Client connections that use the `authenticator=OAUTH_AUTHORIZATION_CODE` connection option. Enabled OIDC integrations appear as
  sign-in options during the browser-based authorization step.

OIDC **can’t** be used with the `authenticator=externalbrowser` connection option. The external-browser authenticator (used by Snowflake
drivers, connectors, and SnowSQL) supports **SAML 2.0 only**. We suggest you prioritize using OAuth over external browser.

## How OIDC SSO works

The following steps describe the SP-initiated OIDC authentication flow when a user logs in to Snowflake.

1. The user navigates to the Snowflake login page and selects the OIDC login option. For custom providers, the button label comes from
   `OIDC_LOGIN_PAGE_LABEL` (or the integration name if not set). For managed providers, Snowflake displays the official provider logo and a
   default label (for example, Sign in with Microsoft).
2. Snowflake generates cryptographic security parameters:

   - A `state` parameter (256-bit random value) to prevent CSRF attacks.
   - A `nonce` (256-bit random value) to prevent token replay attacks.
   - A PKCE `code_verifier` and S256 `code_challenge` to secure the authorization code exchange.
3. Snowflake redirects the user’s browser to the IdP authorization endpoint with a standard OpenID Connect authorization request
   (`response_type=code`).
4. The user authenticates at the IdP.
5. The IdP redirects the user back to the Snowflake callback URL with an authorization code and the `state` parameter. The callback URL
   differs depending on whether the integration uses a managed provider or a custom provider:

   - **Custom provider**: the IdP redirects to the per-account callback `https://<account_url>/oauth2/oidc/callback`.
   - **Managed provider** (Google or Microsoft): the IdP redirects to a global Snowflake-managed callback host (typically
     `identity.snowflake.com/oauth2/callback`), which then redirects to the account-specific endpoint `/oauth2/oidc/callback` to
     complete the flow.
6. Snowflake validates the `state` parameter against the stored value using a constant-time comparison.
7. Snowflake exchanges the authorization code for an ID token by sending a POST request to the IdP token endpoint, including the PKCE code
   verifier.
8. Snowflake validates the ID token:

   - Verifies the JWT signature using the IdP’s public keys (fetched from the JWKS endpoint).
   - Validates standard claims: `iss`, `aud`, `azp` (when `azp` is present in a token with multiple audiences), `exp`, `iat`,
     `nbf`, `nonce`, and `sub`.
9. Snowflake resolves the authenticated user by mapping a token claim to a Snowflake user attribute (login name or email address).
10. Snowflake evaluates any authentication policy applicable to the user (authentication method, integration allow-list, MFA requirement)
    and any network policy.
11. If all checks pass, Snowflake creates a session.

## Managed providers

With managed providers, Snowflake registers and manages the necessary application with the identity provider on your behalf. This streamlines the setup of OIDC federated authentication, eliminating the need for you to register and maintain an app directly with the provider. This approach supports seamless social login experiences, such as `Sign in with Google` or `Sign in with Microsoft`, with minimal configuration on your end.

The table below lists the managed providers currently supported by Snowflake for OIDC federated authentication and shows the configuration value for each provider:

| Provider | Configuration value (`OIDC_PROVIDER`) |
| --- | --- |
| Google | `GOOGLE` |
| Microsoft | `MICROSOFT` |

Expand

Show lessSee more

## Prerequisites

Before configuring OIDC federated authentication in Snowflake, ensure the following:

- You have the `ACCOUNTADMIN` role, or a role with the `CREATE INTEGRATION` privilege on the account.
- For custom providers:

  - You have registered an application with your IdP representing Snowflake.
  - You have obtained the client ID and client secret from the IdP.
  - The IdP redirect/callback URI is set to `https://<your_account_url>/oauth2/oidc/callback`.
  - You know the IdP issuer URL (for example, `https://your-org.okta.com` for Okta).
- Snowflake users exist with the appropriate `LOGIN_NAME` or `EMAIL_ADDRESS` attribute matching the IdP user claims you intend to map.

## Register Snowflake in your IdP (custom providers)

For custom providers, register an application in your IdP before you create the Snowflake security integration. Steps vary by IdP, but
you typically need to configure the following:

1. Create an OpenID Connect (OIDC) application in your IdP representing Snowflake.
2. Set the redirect (callback) URI to `https://<your_account_url>/oauth2/oidc/callback`. After you create the integration, you can run
   [DESC INTEGRATION](/sql-reference/sql/desc-integration) to view the auto-generated `OIDC_REDIRECT_URIS` for your account and confirm the
   exact value or values to register. If the command returns more than one URI, register each one your users might connect through.
3. Copy the client ID and client secret from the IdP application registration. You provide these values in
   `OIDC_CLIENT_ID` and `OIDC_CLIENT_SECRET` when you create the integration.
4. Note the IdP issuer URL (for example, `https://your-org.okta.com` for Okta). You provide this value in `OIDC_ISSUER`.
5. Ensure the IdP application uses the Authorization Code Flow and supports PKCE.

Note

If you create the integration with a placeholder `OIDC_CLIENT_ID` before your IdP assigns the real client ID, and the real value does not
match the placeholder, you must [drop the integration](/sql-reference/sql/drop-integration) and recreate it with the correct client ID.
`OIDC_CLIENT_ID` is immutable after creation.

Note

For managed providers (`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`), you do not register Snowflake as an OAuth client with the IdP. Snowflake manages
the OAuth client configuration.

## Configuring an OIDC security integration

OIDC authentication is configured through a security integration of type `OIDC`. Subject to account-level restrictions, multiple OIDC
integrations can exist on a single account.

Note

Only one SSO integration (SAML2 or OIDC) can be `ENABLED=TRUE` at a time on an account unless [identifier-first login](/user-guide/identifier-first-login)
is enabled. To run multiple OIDC integrations, or one OIDC integration alongside a SAML2 integration, identifier-first login must be
enabled.

For full syntax, parameters, and examples, see [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc).

### Creating a custom OIDC integration

To configure SSO with a custom OIDC identity provider, create a security integration using the
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oidc) command:

Copy code

```
CREATE SECURITY INTEGRATION <integration_name>
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'CUSTOM'
  OIDC_ISSUER = '<issuer_url>'
  OIDC_CLIENT_ID = '<client_id>'
  OIDC_CLIENT_SECRET = '<client_secret>'
  OIDC_TOKEN_USER_MAPPING_CLAIM = '<claim_name>'
  OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = '<LOGIN_NAME | EMAIL_ADDRESS>'
  OIDC_LOGIN_PAGE_LABEL = '<label_text>';
```

For a complete example, see [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc).

If you prefer to specify endpoints explicitly rather than relying on OpenID Connect discovery, add `OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, and `OIDC_JWKS_URI` to your CREATE statement.

Note

If you do not provide the endpoint parameters (`OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`), Snowflake
automatically discovers them from the issuer’s `.well-known/openid-configuration` metadata document. See
[OpenID Connect discovery](#label-oidc-discovery). If you provide some but not all of the three required endpoints, the CREATE is rejected.

### Creating a managed OIDC integration (Google)

For Google as a managed provider, Snowflake handles the OAuth client configuration and displays the official Google logo and default login label on the Snowflake login page. You must also specify `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS`, the Google Workspace hosted domains allowed to sign in through the integration:

Copy code

```
CREATE SECURITY INTEGRATION <integration_name>
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'GOOGLE'
  OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ('mycompany.com');
```

At sign-in, Snowflake compares the `hd` claim in the ID token against this list and rejects any Google account outside it. To allow personal or
unmanaged Google accounts, whose ID tokens carry no `hd` claim, include the literal `'personal'`.

If you signed up for your Snowflake account using Google, Snowflake creates this integration during account creation and sets the allow-list
from the `hd` claim in the ID token you signed up with, or to `'personal'` if you used a personal account. You can change the list later using
[ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).

For a complete Google example, see [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc).

### Creating a managed OIDC integration (Microsoft)

For Microsoft Entra ID as a managed provider, Snowflake handles the OAuth client configuration and displays the official Microsoft logo and default login label on the Snowflake login page. You must also specify `OIDC_ALLOWED_MSFT_TENANTS`, the Microsoft tenants allowed to sign in through the integration:

Copy code

```
CREATE SECURITY INTEGRATION <integration_name>
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'MICROSOFT'
  OIDC_ALLOWED_MSFT_TENANTS = ('a1b2c3d4-e5f6-4789-a012-3456789abcde');
```

At sign-in, Snowflake compares the `tid` claim in the ID token against this list and rejects any Microsoft tenant outside it. To allow personal
Microsoft accounts, which sign in through Microsoft’s static consumer tenant, include the literal `'personal'`.

If you signed up for your Snowflake account using Microsoft, Snowflake creates this integration during account creation and sets the allow-list
from the `tid` claim in the ID token you signed up with, or to `'personal'` if you used a personal account. You can change the list later using
[ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).

For a complete Microsoft example, see [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc).

Note

Snowflake uses a publisher-verified, multi-tenant Microsoft Entra application (“Snowflake Social Login”) for managed Microsoft OIDC sign-in. When a user signs in with an email from a home tenant other than Snowflake’s home tenant, Microsoft Entra shows a consent prompt on first sign-in. The user or a home tenant administrator must consent to the requested delegated permissions (scopes) before Snowflake can complete sign-in.

Managed Microsoft OIDC integrations map users using the `email` claim in the ID token. If the `email` claim is missing after consent, user resolution fails. A home tenant administrator may need to grant admin consent for the Snowflake application or configure optional claims on the enterprise application in their tenant so that ID tokens include `email`.

Managed integrations (Google and Microsoft) share the same parameter restrictions:

Important

For managed providers, you can’t set `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_SCOPES`, the endpoint parameters, the
user-mapping parameters (`OIDC_TOKEN_USER_MAPPING_CLAIM`, `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`), or `OIDC_LOGIN_PAGE_LABEL`. Snowflake manages these values, fixes
user mapping to the `email` claim → `EMAIL_ADDRESS`, and displays the official provider logo and default login label. Setting any of these options causes the CREATE or ALTER statement to fail.

The allow-list options are provider-specific: a `GOOGLE` integration accepts only `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS`, a `MICROSOFT`
integration only `OIDC_ALLOWED_MSFT_TENANTS`, and a `CUSTOM` integration neither. To restrict access on a custom integration, use
`ALLOWED_USER_DOMAINS` or `ALLOWED_EMAIL_PATTERNS`.

## Managing OIDC integrations

Use the following commands to manage OIDC security integrations:

- View configuration: [DESC INTEGRATION](/sql-reference/sql/desc-integration). The command returns all integration properties, including
  the auto-generated `OIDC_REDIRECT_URIS` that you must register with your IdP for custom providers. The `OIDC_CLIENT_SECRET` is omitted
  from the result because it is a secret.
- Modify properties: [ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).
- Remove an integration: [DROP INTEGRATION](/sql-reference/sql/drop-integration).

Warning

Dropping an active OIDC integration immediately prevents all users from authenticating via that IdP. If an authentication policy explicitly
references the integration in its `SECURITY_INTEGRATIONS` list, the drop is rejected until the policy is updated.

## Replication and failover

Snowflake supports replication and failover/failback of OIDC security integrations from a source account to a target account, using the
same failover group approach as SAML2 and OAuth security integrations. Integration properties replicate with the object, including
`OIDC_CLIENT_SECRET`.

For custom providers, after replication to a target account, register that account’s `OIDC_REDIRECT_URIS` with your IdP. Managed providers
(`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`) do not require a per-account redirect URI registration.

Note

Custom OIDC integrations are not Client Redirect-aware. The redirect URI registered with your IdP is bound to the account where the
integration was created. If you fail over to a secondary account via Client Redirect, register the secondary account’s redirect URI with
your IdP separately, or use a managed provider. SAML2 integrations advertise both primary and secondary ACS URLs through
`SAML2_SNOWFLAKE_OTHER_ACS_URLS`; OIDC does not currently have an equivalent.

For procedures and details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations#label-account-replication-security-integration-oidc).

## User mapping and resolution

When Snowflake receives a validated ID token from the IdP, it must map the authenticated identity to a Snowflake user. This is controlled by
two properties:

- `OIDC_TOKEN_USER_MAPPING_CLAIM`: specifies which ID token claim contains the user identifier. For multiple fallback claims, specify an
  ordered list (for example, `('email', 'sub')`).
- `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`: specifies which Snowflake user attribute to match against.

For managed providers (Google and Microsoft), user mapping is fixed to the `email` claim → `EMAIL_ADDRESS` and can’t be configured. For Microsoft managed integrations, see [Creating a managed OIDC integration (Microsoft)](#label-oidc-microsoft-managed-provider) for cross-tenant consent and email-claim requirements.

### Token claim mapping

The following table describes common ID token claims you can use in `OIDC_TOKEN_USER_MAPPING_CLAIM`.

| Claim | Typical value | When to use |
| --- | --- | --- |
| `email` | `user@company.com` | When Snowflake users are identified by email address. |
| `preferred_username` | `jsmith` | When Snowflake users are identified by a username that matches their IdP username. |
| `sub` | `10239485723` | When Snowflake users are mapped by the IdP’s unique subject identifier. |
| Any custom claim | (varies) | Any other named claim present in the ID token. |

Expand

Show lessSee more

You can specify multiple claims as an ordered list (for example, `('email', 'preferred_username', 'sub')`). Snowflake extracts all non-empty
values from the listed claims in order, then attempts user lookup with each value against `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`, using the
first successful match. If a claim is absent from the ID token, Snowflake skips it and tries the next. Only string-valued claims are
supported; a non-string claim (number, boolean, or object) is stringified and typically won’t match any Snowflake user attribute. Snowflake
does not call the UserInfo endpoint to retrieve missing claims. If no listed claim resolves a user, login fails:

Copy code

```
CREATE SECURITY INTEGRATION my_oidc
  TYPE = OIDC
  ...
  OIDC_TOKEN_USER_MAPPING_CLAIM = ('email', 'preferred_username', 'sub')
  OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'LOGIN_NAME';
```

Note

User matching is case-insensitive. For `LOGIN_NAME`, the claim value is normalized to uppercase before lookup (login names are unique within
an account). For `EMAIL_ADDRESS`, Snowflake performs a case-insensitive lookup, and the additional rules in
[Verified email requirement](#label-oidc-verified-email) apply.

### Verified email requirement

When mapping is configured against `EMAIL_ADDRESS`, the email address is a shared, user-supplied attribute rather than a unique identifier.
To prevent account takeover through an unverified or duplicated email, Snowflake applies the following rules to email-based resolution. These
rules don’t apply to `LOGIN_NAME` mapping.

For managed providers, users must also verify their email in their Google Workspace or Microsoft tenant before they can sign in.
Snowflake checks the `email_verified` claim in the ID token; if the email isn’t verified at the IdP, login fails. If you include
`'personal'` in `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS` or `OIDC_ALLOWED_MSFT_TENANTS`, both providers treat personal and unmanaged
accounts as verified by default.

- **The matched user’s email must be verified.** By default, a user whose email isn’t verified can’t sign in through email-based OIDC
  mapping; the login fails as an unresolved user (the same generic error as any other missed lookup). An email counts as verified in either
  of two ways: the user completed the email-verification flow on their user record, or the user’s email domain has been verified for the
  account through [domain verification](/user-guide/admin-domain-verification) (using
  [SYSTEM$VERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_verify_dns_domain), reversible with
  [SYSTEM$UNVERIFY\_DNS\_DOMAIN](/sql-reference/functions/system_unverify_dns_domain)). Domain verification matches exactly per domain:
  verifying `example.com` doesn’t cover `sub.example.com`. When you roll out email-based OIDC mapping to more than a handful of users,
  verifying the corporate email domain once is far easier than having every user complete the individual verification flow, and is the
  recommended path.
- **Verified email disambiguates duplicate addresses.** If more than one Snowflake user shares the email address in the token:

  - If exactly one of those users has a verified email, Snowflake resolves to that user.
  - If more than one has a verified email, the login fails because the identity is ambiguous.
  - If none has a verified email, the login fails.

To avoid ambiguity, ensure each email address maps to a single Snowflake user, or use `LOGIN_NAME` mapping, where identifiers are guaranteed
unique. Because these rules apply only to `EMAIL_ADDRESS` mapping, `LOGIN_NAME` mapping bypasses the verified-email requirement entirely,
even if the same Snowflake user has an unverified email on file.

### Restricting access by domain or email pattern

You can restrict which IdP users are allowed to authenticate by configuring domain or email pattern filters. The filter is enforced both at
the identifier-first login screen (when offering OIDC buttons) and after the IdP returns a token (against the resolved claim value used for
user lookup).

**Domain restriction (`ALLOWED_USER_DOMAINS`):**

Copy code

```
ALTER SECURITY INTEGRATION my_oidc
  SET ALLOWED_USER_DOMAINS = ('mycompany.com', 'subsidiary.com');
```

`ALLOWED_USER_DOMAINS` performs an exact, case-insensitive match on the email domain. The value `mycompany.com` matches `user@mycompany.com`
but not `user@evil-mycompany.com` or `user@mycompany.com.attacker.com`. This is the recommended way to restrict access by domain.

**Email pattern restriction (`ALLOWED_EMAIL_PATTERNS`):**

Copy code

```
ALTER SECURITY INTEGRATION my_oidc
  SET ALLOWED_EMAIL_PATTERNS = ('^[^@]+@mycompany\.com$', '^admin-.*@subsidiary\.com$');
```

Important

`ALLOWED_EMAIL_PATTERNS` accepts Java-style regular expressions that are matched as substrings (equivalent to a regex “find”), not as
full-string matches. An unanchored pattern therefore matches any value that *contains* it: for example, `mycompany.com` would also allow
`attacker@evil-mycompany.com`, and `.` matches any character. Always anchor patterns with `^` and `$` and escape literal dots (`\.`). When
you only need to restrict by domain, prefer `ALLOWED_USER_DOMAINS`.

Note

`ALLOWED_EMAIL_PATTERNS` requires the `ENABLE_IDENTIFIER_FIRST_LOGIN` account parameter to be enabled. Setting `ALLOWED_EMAIL_PATTERNS` when
identifier-first login is disabled fails with a feature-not-enabled error.

## OpenID Connect discovery

Snowflake supports automatic endpoint discovery using the OpenID Connect Discovery 1.0 specification. When you provide an `OIDC_ISSUER` URL
but omit endpoint parameters, Snowflake fetches the IdP’s metadata from:

Copy code

```
<OIDC_ISSUER>/.well-known/openid-configuration
```

Snowflake retrieves the following endpoints from the metadata document:

| Metadata field | Maps to | Required |
| --- | --- | --- |
| `authorization_endpoint` | `OIDC_AUTHORIZATION_ENDPOINT` | Yes |
| `token_endpoint` | `OIDC_TOKEN_ENDPOINT` | Yes |
| `jwks_uri` | `OIDC_JWKS_URI` | Yes |
| `userinfo_endpoint` | `OIDC_USERINFO_ENDPOINT` | No (stored only; not used at sign-in) |

Expand

Show lessSee more

If discovery populates `OIDC_USERINFO_ENDPOINT`, Snowflake records the value on the integration. Sign-in does not call this endpoint; user
resolution uses ID token claims only. See [User mapping and resolution](#label-oidc-user-mapping).

If discovery fails or the metadata document does not contain the required endpoints, the CREATE SECURITY INTEGRATION command fails with an
error.

Note

If you provide all three endpoint parameters (`OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`) explicitly, Snowflake
skips the discovery process. This is useful when the IdP does not publish a well-known metadata document, or when you need to override
discovered values. Providing only some of the three required endpoints is rejected. Snowflake either runs discovery (no endpoints supplied)
or accepts an explicit complete set.

## Authentication policy integration

OIDC integrates with Snowflake’s [authentication policy](/user-guide/authentication-policies) framework. Authentication policies allow
administrators to restrict which authentication methods, integrations, and clients are allowed for a given user or account.

### The OIDC authentication method

`AUTHENTICATION POLICY` accepts a list of allowed authentication methods. Adding `OIDC` to a policy’s `AUTHENTICATION_METHODS` declares that
OIDC-federated login is permitted under this policy. `ALL` already covers OIDC, so existing policies set to `ALL` automatically allow OIDC
without any policy change.

**Example: enable OIDC and password, disallow everything else**

Copy code

```
CREATE AUTHENTICATION POLICY oidc_or_password
  AUTHENTICATION_METHODS = ('OIDC', 'PASSWORD')
  COMMENT = 'Users may sign in via OIDC SSO or password';

ALTER USER alice SET AUTHENTICATION_POLICY = oidc_or_password;
```

### Restricting allowed integrations

You can scope a policy to specific OIDC integrations by name using the `SECURITY_INTEGRATIONS` policy property:

Copy code

```
CREATE AUTHENTICATION POLICY engineering_oidc
  AUTHENTICATION_METHODS = ('OIDC')
  SECURITY_INTEGRATIONS = ('GOOGLE_OIDC_INT');
```

When `SECURITY_INTEGRATIONS` is set, only the listed integrations are usable under this policy. Both SAML2 and OIDC integration types are
accepted in the list.

### Identifier-first login filtering

When identifier-first login is enabled on the account, the OIDC SSO options offered to a user on the login screen are
filtered by the user’s authentication policy:

- If `AUTHENTICATION_METHODS` does not include `OIDC` (and is not `ALL`), no OIDC buttons are shown.
- If `SECURITY_INTEGRATIONS` is set and lists only OIDC integrations, only those integrations are offered.
- If `SECURITY_INTEGRATIONS` includes only non-OIDC integrations, Snowflake falls back to the account-wide OIDC list, matching the existing
  SAML behavior.

### Login-name match check

After the IdP redirects back with an ID token, if the user typed a login name or email at the identifier-first prompt, Snowflake verifies
that the resolved Snowflake user matches that hint. If the resolved user does not match the typed identifier (and is not findable from it),
the login is rejected. This prevents a user from typing one identity at the Snowflake prompt and authenticating as a different identity at
the IdP.

### Multi-factor authentication after OIDC

To require Snowflake MFA after an OIDC SSO login, set `ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION = 'ALL'` in the authentication policy’s
`MFA_POLICY`. When `'ALL'` is specified, MFA is enforced after SSO login for users who are enrolled in MFA. This applies to OIDC and SAML
alike. For details, see [Hardening user or account authentication using MFA](/user-guide/authentication-policies#label-authentication-policy-hardening-authentication).

**Example: require OIDC SSO with MFA**

Copy code

```
CREATE AUTHENTICATION POLICY engineering_sso_policy
  AUTHENTICATION_METHODS = ('OIDC')
  SECURITY_INTEGRATIONS = ('GOOGLE_OIDC_INT')
  MFA_ENROLLMENT = 'REQUIRED'
  MFA_POLICY = (
    ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION = 'ALL'
  )
  COMMENT = 'Engineers must use Google SSO with MFA';

ALTER USER alice SET AUTHENTICATION_POLICY = engineering_sso_policy;
```

For troubleshooting OIDC login and integration issues, see [OIDC troubleshooting](/user-guide/errors-saml#label-oidc-troubleshooting).
