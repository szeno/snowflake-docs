# Overview of federated authentication and SSO

This topic describes the components that make up a federated environment for authenticating users, and the SSO (single sign-on) workflows supported by
Snowflake.

## What is a federated environment?

In a federated environment, user authentication is separated from user access through the use of one or more external entities that provide independent
authentication of user credentials. The authentication is then passed to one or more services, enabling users to access the services through SSO. A federated
environment consists of the following components:

- **Service provider (SP):** In a Snowflake federated environment, Snowflake serves as the SP.
- **Identity provider (IdP):** The external, independent entity responsible for providing the following services to the SP:

  - Creating and maintaining user credentials and other profile information.
  - Authenticating users for SSO access to the SP.

Snowflake supports federated authentication through SAML 2.0 and [OpenID Connect (OIDC)](/user-guide/admin-security-fed-auth-oidc) security integrations. For SAML, Snowflake supports most SAML 2.0-compliant vendors as an IdP; however, certain vendors include native support for Snowflake (see below for details).

## Supported identity providers

### SAML 2.0 identity providers

The following vendors provide native Snowflake support for federated authentication and SSO:

- Okta
- Microsoft Entra ID

In addition to the native Snowflake support provided by Okta and Entra ID, Snowflake supports using most SAML 2.0-compliant vendors as an IdP, including:

- [Google G Suite](https://gsuite.google.com/)
- [Microsoft Entra ID](https://www.microsoft.com/en-us/security/business/identity-access/microsoft-entra-id)
- [OneLogin](https://www.onelogin.com/product/sso)
- [Ping Identity PingOne](https://www.pingidentity.com/en/products/pingone.html)

Note

To use an IdP other than Okta or Entra ID, you must define a custom application for Snowflake in the IdP.

For details about configuring Okta, Entra ID, or another SAML 2.0-compliant vendor as the IdP for Snowflake, see [Configuring an identity provider (IdP) for Snowflake](/user-guide/admin-security-fed-auth-configure-idp).

### OIDC identity providers

Snowflake supports OIDC federated authentication with managed providers (Google and Microsoft Entra ID) or any custom OpenID Connect-compliant identity provider (for example, Okta, PingFederate, Auth0, or Keycloak). For managed providers, Snowflake manages the OAuth client configuration. For custom providers, you register an application in your IdP and provide client credentials to Snowflake.

For details about configuring OIDC federated authentication, see [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc).

## OIDC vs. SAML comparison

If you are evaluating whether to use OIDC or SAML for federated authentication, the following table summarizes the key differences.

| Aspect | OIDC | SAML 2.0 |
| --- | --- | --- |
| Protocol | OAuth 2.0 + OpenID Connect 1.0 | SAML 2.0 |
| Token format | JWT (JSON Web Token) | XML assertion |
| Authentication flow | Authorization Code Flow with PKCE | POST or Redirect binding |
| User identity mapping | JSON claims (email, sub, etc.) | XML attributes |
| Integration type | `TYPE = OIDC` | `TYPE = SAML2` |
| Endpoint discovery | Automatic via `.well-known/openid-configuration` | Manual or via SAML metadata document |
| Managed providers | Google, Microsoft | None |
| Credential type | Client ID + Client Secret | X.509 certificate |
| Primary configuration | Client credentials; issuer URL or explicit OAuth/OIDC endpoints; JWT claim mapping | X.509 certificate; SAML metadata or manual ACS/entity ID exchange; XML attribute mapping |
| Authentication-policy support | `AUTHENTICATION_METHODS = ('OIDC')` | `AUTHENTICATION_METHODS = ('SAML')` |
| MFA enforcement after SSO | `MFA_POLICY=(ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION='ALL')` | `MFA_POLICY=(ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION='ALL')` |
| Web interface (browser) SSO | Supported | Supported |
| Driver SSO with `authenticator=externalbrowser` | Not supported (use `authenticator=OAUTH_AUTHORIZATION_CODE` for driver OIDC SSO) | Supported |
| Replication and failover | Supported via failover groups (same as SAML2) | Supported via failover groups |
| Client Redirect (custom providers) | Not supported; register each account’s `OIDC_REDIRECT_URIS` with your IdP, or use a managed provider | Supported via `SAML2_SNOWFLAKE_OTHER_ACS_URLS` |

Expand

Show lessSee more

## Using multiple identity providers

You can configure Snowflake so different users authenticate using different identity providers.

For SAML IdPs, [configure each identity provider](/user-guide/admin-security-fed-auth-configure-idp), then follow the guidance in
[Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple). For OIDC IdPs, register each IdP application and create an OIDC security integration as described in [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc), then follow the same multiple-IdP guidance.

Note

Currently, only a subset of Snowflake drivers support the use of multiple identity providers. These drivers include JDBC, ODBC, and Python.

## Supported SSO workflows

Federated authentication enables the following SSO workflows:

- Logging into Snowflake.
- Logging out of Snowflake.
- System timeout due to inactivity.

The behavior for each workflow is determined by whether the action is initiated within Snowflake or your IdP.

### Login workflow

When a user logs in, the behavior of the system is determined by whether the login is initiated through Snowflake or the IdP:

- **Snowflake-initiated login:**

  To log in through Snowflake:

  1. User goes to the Snowflake web interface.

  Note

  You can configure Snowflake so that a user accessing Snowflake with a URL is redirected to the IdP to authenticate without seeing
  the Snowflake sign-in page. For more information, see
  [Automatically redirecting users to your identity provider](/user-guide/admin-security-fed-auth-idp-redirect).

  2. User chooses to log in using the IdP configured for your account (Okta, Entra ID, or a custom IdP).
  3. User authenticates with the IdP using their IdP credentials (for example, email address and password).
  4. If authentication is successful, the IdP sends a SAML response to Snowflake to initiate a session and displays the Snowflake web
     interface.
- **IdP-initiated login:**

To log in through the IdP for your account:

1. User goes to the IdP site/application and authenticates using their IdP credentials (for example, email address and password).
2. In the IdP, user selects the Snowflake application (if using Okta or Entra ID) or the custom application that has been defined in the IdP (if using
   another IdP).
3. The IdP sends a SAML response to Snowflake to initiate a session and then displays the Snowflake web interface.

### Logout workflow

When a user logs out, the available options are dictated by whether the IdP supports *global* logout or only *standard* logout:

> Standard:
> :   Requires users to explicitly log out of both the IdP and Snowflake to completely disconnect. All IdPs support standard logout.
>
> Global:
> :   Enables a user to log out of the IdP and subsequently all their Snowflake sessions. Support for global logout is IdP-dependent.

In addition, the behavior of the system is determined by whether the logout is initiated through Snowflake or the IdP:

- **Snowflake-initiated logout:** Global logout is not supported from within Snowflake, regardless of whether the IdP supports it. When a user logs out of a Snowflake session, they are
  logged out of that session only. All their other current Snowflake sessions stay open, as does their IdP session. As a result, they can continue working
  in their other sessions or they can initiate additional sessions without having to re-authenticate through the IdP.

  To completely disconnect, users must explicitly log out of both Snowflake and the IdP.
- **IdP-initiated logout:**

  When a user logs out through an IdP, the behavior depends on whether the IdP supports standard logout only or also global logout:

  - Entra ID supports both standard and global logout. If global logout is enabled, the Entra ID IdP login page
    provides an option for signing out from all sites
    that the user has accessed. Selecting this option logs the user out of Entra ID and all
    their Snowflake sessions. To access Snowflake again, they must re-authenticate using Entra ID.
  - Okta supports standard logout only. When a user logs out of Okta, they are not automatically logged out of any of their active
    Snowflake sessions and they can continue working. However, to initiate any new Snowflake sessions, they must authenticate again through
    Okta.
  - All custom providers support standard logout; support for global logout varies by provider.

  Note

  For a web-based IdP (for example, Okta), closing the browser tab/window does not necessarily end the IdP session. If a user’s IdP session is
  still active, they can still access Snowflake until the IdP session times out.

### Timeout workflow

When a user’s session times out, the behavior is determined by whether it is their Snowflake session or IdP session that timed out:

- **Snowflake timeout:** If a user logs into Snowflake using SSO and their Snowflake session expires due to inactivity, the Snowflake web interface is disabled and the prompt for
  IdP authentication is displayed:

  - To continue using their expired Snowflake session, the user must authenticate again through the IdP.
  - The user can exit the session by selecting the **Cancel** button.
  - The user can also go to the IdP site/application directly and relaunch Snowflake, but this initiates a new Snowflake session.
- **IdP timeout:** After a specified period of time (defined by the IdP), a user’s session in the IdP automatically times out, but this does not affect their Snowflake
  sessions. Any Snowflake sessions that are active at the time remain open and do not require re-authentication. However, to initiate any new Snowflake
  sessions, the user must log into the IdP again.

## SSO with private connectivity

Snowflake supports SSO with private connectivity to the Snowflake service for Snowflake accounts on Amazon Web Services (AWS),
Microsoft Azure, and Google Cloud Platform (GCP).

Currently, for any given Snowflake account, SSO works with only one account URL at a time: either the public account URL or the URL
associated with the private connectivity service on AWS, Microsoft Azure, or Google Cloud Platform.

Snowflake supports using SSO with [organizations](/user-guide/organizations), and you can use the corresponding URL in the SAML2
security integration. For more information, see [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).

To use SSO with private connectivity to Snowflake, configure private connectivity before configuring SSO:

- If your Snowflake account is on AWS or Azure, follow the self-service instructions as listed in
  [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink) and [Azure Private Link and Snowflake](/user-guide/privatelink-azure).
- If your Snowflake account is on GCP, you must contact
  [Snowflake Support](/user-guide/contacting-support) and provide the
  Snowflake account URL to use with [Google Cloud Private Service Connect and Snowflake](/user-guide/private-service-connect-google).

  To determine the correct URL to use, call the [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function in your Snowflake
  account on GCP.

# Replicate the SSO Configuration

Snowflake supports replication and failover/failback of the
[SAML2 security integration](/user-guide/admin-security-fed-auth-security-integration) and
[OIDC security integration](/user-guide/admin-security-fed-auth-oidc) from a source account to a target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).
