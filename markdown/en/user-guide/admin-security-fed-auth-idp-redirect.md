# Automatically redirecting users to your identity provider

This topic describes how to configure Snowflake to automatically redirect
users to your identity provider (IdP) for authentication when they access
a Snowflake interface, instead of presenting the Snowflake sign-in page
first.

You configure the redirect through the
[LOGIN\_IDP\_REDIRECT](/sql-reference/sql/alter-account#label-alter-account-login-idp-redirect) account
property. Each interface (such as Snowsight, Streamlit in Snowflake, or
Snowpark Container Services ingress) can be mapped to a different SAML2
security integration, or you can set a single default mapping that
applies to every interface.

## Overview

When federated authentication is configured for your account, the default
sign-in flow asks the user to first reach the Snowflake sign-in page and
then choose to sign in through your IdP. With `LOGIN_IDP_REDIRECT`
configured, Snowflake skips the Snowflake sign-in page entirely: the
user is sent directly to the IdP to authenticate, and is then returned
to the requested Snowflake interface.

This streamlines the sign-in flow for users whose only authentication
path is the IdP configured for that interface. It’s especially useful
for embedded user experiences, such as Streamlit in Snowflake
app-viewer URLs and Snowpark Container Services ingress endpoints,
where the Snowflake sign-in page adds an extra step before the user
reaches the only IdP they can authenticate against.

## Prerequisites

Before you configure `LOGIN_IDP_REDIRECT`, make sure the following
requirements are met:

- You have at least one SAML2 security integration configured and
  enabled. The redirect property only accepts SAML2 security
  integrations. For instructions, see
  [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).
- You have the ACCOUNTADMIN role, or a role with the privileges required
  to run [ALTER ACCOUNT](/sql-reference/sql/alter-account).
- At least one account administrator can sign in with a backup
  authentication method (such as a Snowflake password with MFA) so that
  your organization can recover access if the IdP becomes unavailable.
  See [Managing users with federated authentication enabled](/user-guide/admin-security-fed-auth-use#label-users-fed-auth).

## Supported interfaces

You can configure a redirect for any of the following Snowflake
interfaces. Each interface can be mapped to a different SAML2 security
integration.

`DEFAULT`
:   Applies to two situations:

    - Login flows that start at `app.snowflake.com` (the Snowsight
      sign-in page). When `DEFAULT` is set, those flows redirect to
      the IdP instead of presenting the Snowflake sign-in screen.
    - Any other interface key listed below that you don’t explicitly
      configure. For example, if you set `DEFAULT` but not
      `STREAMLIT`, Streamlit in Snowflake app-viewer URLs use the
      `DEFAULT` mapping.

    To opt a specific interface out of the `DEFAULT` fallback, set
    that interface to `NULL`. See [Remove or opt out a redirect](#label-login-idp-redirect-opt-out).

`SNOWFLAKE_INTELLIGENCE`
:   Applies to [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) URLs. Overrides
    the `DEFAULT` mapping for Snowflake CoWork URLs. Set this
    key to `NULL` to opt Snowflake CoWork URLs out of the
    `DEFAULT` fallback. For interface-specific guidance, including the
    DNS configuration required when Snowflake CoWork is accessed
    with private connectivity, see
    [Redirect users to your identity provider](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-intelligence-configure-redirect).

`STREAMLIT`
:   Applies to Streamlit in Snowflake app-viewer URLs. Overrides the `DEFAULT` mapping
    for app-viewer URLs. Set this key to `NULL` to opt Streamlit
    app-viewer URLs out of the `DEFAULT` fallback. For
    interface-specific guidance, see [Redirect app viewers to your identity provider](/developer-guide/streamlit/object-management/security#label-streamlit-redirect-idp).

`SPCS`
:   Applies to Snowpark Container Services ingress endpoints. Overrides
    the `DEFAULT` mapping for SPCS ingress URLs. Set this key to
    `NULL` to opt SPCS ingress URLs out of the `DEFAULT` fallback.
    For interface-specific guidance, see
    [Ingress and your Identity Provider (IdP) considerations](/developer-guide/snowpark-container-services/service-network-communications#label-spcs-redirect-ingress-login).

Snowflake resolves the redirect for an interface in this order:

1. If the interface key is set explicitly, that mapping is used. A
   value of `NULL` means “no redirect for this interface”.
2. Otherwise, if `DEFAULT` is set, the `DEFAULT` mapping is used.
3. Otherwise, the standard Snowflake sign-in page is displayed.

## Configure the redirect

Use [ALTER ACCOUNT](/sql-reference/sql/alter-account) to set `LOGIN_IDP_REDIRECT`.
You can map multiple interfaces in a single statement. Replace
`your_security_integration` with the name of an existing,
enabled SAML2 security integration.

To redirect every interface in the account through the same IdP:

Copy code

```
ALTER ACCOUNT SET LOGIN_IDP_REDIRECT = (
  DEFAULT = my_saml_integration
);
```

To configure a different SAML2 security integration for individual
interfaces, list them in the same statement. Per-interface mappings
override the `DEFAULT` mapping for that interface.

Copy code

```
ALTER ACCOUNT SET LOGIN_IDP_REDIRECT = (
  DEFAULT = my_saml_integration,
  SNOWFLAKE_INTELLIGENCE = my_intelligence_saml_integration,
  STREAMLIT = my_streamlit_saml_integration,
  SPCS = my_spcs_saml_integration
);
```

Setting `LOGIN_IDP_REDIRECT` again replaces the entire mapping with the
new values. List every interface you want to keep configured each time
you change the property.

## View the current configuration

To see which interfaces are currently mapped, query the view-only
`LOGIN_IDP_REDIRECT` account parameter. The parameter returns a JSON
object that summarizes the mapping set on the account.

Copy code

```
SHOW PARAMETERS LIKE 'LOGIN_IDP_REDIRECT' IN ACCOUNT;
```

For more information, see
[LOGIN\_IDP\_REDIRECT (view-only)](/sql-reference/parameters#label-login-idp-redirect) in the
parameters reference.

## Remove or opt out a redirect

To stop redirecting a single interface to your IdP while leaving other
mappings in place, set that interface to `NULL` in a new
`ALTER ACCOUNT SET LOGIN_IDP_REDIRECT` statement. Users of that
interface then see the standard Snowflake sign-in page. Setting an
interface to `NULL` also opts that interface out of the `DEFAULT`
fallback.

For example, to keep the `DEFAULT` mapping but stop redirecting
Streamlit app-viewer URLs:

Copy code

```
ALTER ACCOUNT SET LOGIN_IDP_REDIRECT = (
  DEFAULT = my_saml_integration,
  STREAMLIT = NULL
);
```

To remove all mappings and restore the standard sign-in flow for every
interface, unset the property:

Copy code

```
ALTER ACCOUNT UNSET LOGIN_IDP_REDIRECT;
```

## Bypass the redirect to reach the Snowflake sign-in page

Snowflake supports a recovery procedure that lets you reach the standard
sign-in page even when a redirect is configured. Use this procedure when
you can’t sign in through your IdP, or when you need to sign in with a
backup authentication method, such as a Snowflake password with MFA.

The procedure relies on the standard OIDC `prompt=login` parameter,
which Snowflake honors to suppress the IdP redirect for a single
sign-in attempt.

To use it:

1. In your browser, open the developer tools and select the Network
   tab.
2. Start loading the Snowflake URL that is being redirected.
3. Find the request to the `/oauth/authorize` endpoint on
   `snowflakecomputing.com` and copy its full URL.
4. Append `&prompt=login` to the end of the URL and load the edited
   URL in your browser.

Snowflake displays the standard sign-in page, where you can choose any
authentication method that is enabled for your user.

Important

Make sure at least one account administrator has a working backup
authentication method (such as a Snowflake password) so that your
organization can recover access if the IdP becomes unavailable. See
[Managing users with federated authentication enabled](/user-guide/admin-security-fed-auth-use#label-users-fed-auth) for guidance on managing administrator
credentials in a federated environment.

## Considerations

Keep the following in mind when you configure `LOGIN_IDP_REDIRECT`:

- Only SAML2 security integrations are supported. Other types of
  security integrations cannot be referenced by the property.
- The referenced security integration must exist and be enabled. If you
  drop or disable the security integration, users of the affected
  interface receive an error when they try to sign in. Update or remove
  the mapping before you disable or drop the integration.
- `ALTER ACCOUNT SET LOGIN_IDP_REDIRECT` replaces the entire mapping.
  Always include every interface you want to keep configured.
- `ALTER ACCOUNT UNSET LOGIN_IDP_REDIRECT` removes every mapping at
  once.
- The redirect bypasses the Snowflake sign-in page for configured
  interfaces, including the option to choose a different authentication
  method. Users who need to sign in with a backup authentication method
  must follow the recovery procedure described in
  [Bypass the redirect to reach the Snowflake sign-in page](#label-login-idp-redirect-bypass).
