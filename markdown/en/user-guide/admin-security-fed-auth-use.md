# Managing/Using federated authentication

This topic describes how to manage and use federated authentication once it has been
[configured](/user-guide/admin-security-fed-auth-security-integration) for SAML or [configured for OIDC](/user-guide/admin-security-fed-auth-oidc).

Note

This topic focuses on SAML 2.0 federated authentication. For OpenID Connect (OIDC) configuration, user mapping, and troubleshooting, see
[Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc). Post-configuration user management patterns in this topic (for example, maintaining Snowflake
passwords alongside SSO) apply to both SAML and OIDC unless noted otherwise.

## Managing users with federated authentication enabled

### Managing Snowflake user passwords

With federated authentication enabled for your account, Snowflake still allows maintaining and using Snowflake user credentials (login name and password).
In other words:

- Account and security administrators can still create users with passwords maintained in Snowflake.
- Users can still log into Snowflake using their Snowflake credentials.

However, if federated authentication is enabled for your account, Snowflake does not recommend maintaining user passwords in Snowflake. Instead, user
passwords should be maintained solely in your IdP.

If you create a user with no password (or alter an existing user and remove their password), this effectively disables Snowflake authentication for the user.
Without a password in Snowflake, a user cannot log in using Snowflake authentication and must use federated authentication instead. Note that you cannot use
the Snowflake web interface to create users with no passwords or remove passwords from existing users. You must use [CREATE USER](/sql-reference/sql/create-user) or
[ALTER USER](/sql-reference/sql/alter-user).

Specifically, we recommend that you disable Snowflake authentication for all non-administrator users.

Important

The MUST\_CHANGE\_PASSWORD user property does not apply for federated authentication and should not be used. In particular, if you choose to not maintain
passwords in Snowflake for users, ensure this property is set to FALSE for these users.

Also, you must maintain at least one Snowflake account administrator with a Snowflake password. This ensures that an account administrator can
access Snowflake at all times to manage federated authentication and troubleshoot any issues that occur.

### Disabling and dropping users

As an account or security administrator in Snowflake, you may find it necessary to drop or, more likely, disable a user. Users who are dropped or disabled
in Snowflake are still able to log into their Okta accounts, but they will receive an error message when they attempt to connect to Snowflake. You must
recreate or enable the user before they can log in.

You can drop/create and disable/enable users using either the Snowflake web interface or the equivalent SQL commands.

## Using SSO with client applications that connect to Snowflake

With an [IdP configured for your account](/user-guide/admin-security-fed-auth-configure-idp), Snowflake supports using SSO to connect
and authenticate with the following Snowflake-provided clients:

Snowflake CLI:
:   v3.0.0 or higher

SnowSQL:
:   v1.1.43 or higher

Python Connector:
:   v1.4.8 or higher

JDBC Driver:
:   v3.2.7 or higher

ODBC Driver:
:   v2.13.11 or higher

.NET Driver:
:   v1.0.13 or higher

Node.js Driver:
:   v1.6.0 or higher (for browser-based SSO); v1.6.1 or higher (for native SSO authentication through Okta)

Go Driver:
:   v1.1.5 or higher

Snowflake supports two methods of authenticating:

- Browser-based SSO
- Programmatic SSO (only for Okta)

Important

When using SSO with client applications that connect to Snowflake, users must enter their login credentials when prompted; however, for security reasons,
these credentials are never processed through the client. Instead, the credentials are sent to the IdP for authentication and the IdP sends back a valid
SAML response which enables the client to initiate a Snowflake session.

### Browser-based SSO

If users have [the required version (or higher) of the Snowflake-provided clients](#label-sso-with-command-line-clients) installed,
they can use browser-based SSO to log into Snowflake.

#### How browser-based SSO works

When a client application is configured to use browser-based SSO, the application uses the following workflow for user authentication:

1. The application launches the default web browser in the user’s operating system or opens a new browser tab/window, displaying the authentication page for
   the IdP.
2. The user enters their IdP credentials (username and password).
3. If the user is enrolled in MFA (multi-factor authentication) in Snowflake, they are prompted to type the MFA passcode (sent from another device) or
   confirm the authentication (on the other device).
4. After the IdP has authenticated the user’s credentials, the browser displays a success message. The user can then close the browser tab/window (it does not
   need to be open after authentication), return to the application, and use the Snowflake session that has been initiated.

#### Requirements for using browser-based SSO

With browser-based SSO, the Snowflake-provided client (for example, the Snowflake JDBC driver) needs to be able to open the user’s web browser. For this
reason, the Snowflake-provided client and the client application that uses it need to be installed on the user’s machine. Browser-based SSO does not work if
the Snowflake-provided client is used by code that runs on a server.

#### Setting up browser-based SSO

To set up browser-based SSO for authentication, set the `authenticator` login parameter/option to
`externalbrowser` for the client.

| Client | Instructions |
| --- | --- |
| Snowflake CLI | Set the `authenticator` parameter for the connection in the `config.toml` file, or specify the command line flag `--authenticator externalbrowser` when starting the client. |
| SnowSQL | Specify the command line flag `--authenticator externalbrowser` when starting the client. |
| Python | Pass `authenticator='externalbrowser'` to the `snowflake.connector.connect()` function. |
| JDBC | Set `authenticator=externalbrowser` in the connection string for the driver. |
| ODBC (Linux/macOS) | Set `authenticator=externalbrowser` in the `odbc.ini` file. |
| ODBC (Windows) | In the ODBC Data Source Administrator tool, edit the DSN for Snowflake and set **Authenticator** to `externalbrowser`. |
| .NET | Set `authenticator=externalbrowser` in the connection string for the driver. |
| Node.js | Set the `authenticator=EXTERNALBROWSER` option when calling the `snowflake.createConnection` function. |
| Go | Set `authenticator=externalbrowser` in the connection string for the driver. |

Expand

Show lessSee more

#### Using connection caching to minimize the number of prompts for authentication — *Optional*

Whenever a client application establishes a new connection to Snowflake, the user is prompted for authentication. This can
result in multiple prompts for authentication if the client application establishes a connection multiple times.

To minimize the number of times that a user is prompted for authentication, the account administrator can enable connection
caching.

When connection caching is enabled, the client application stores a connection token for use in subsequent connections. For
security, the connection token is stored in the keystore for the operating system. Before you enable connection caching,
consult with your security team to determine if this complies with your security policies.

Tip

Connection caching can be combined with MFA token caching.

For more information on how to combine these two features, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

Snowflake supports connection caching with the following drivers and connectors:

- .NET driver version 4.4.0 (or later)
- Go driver version 1.6.15 (or later)
- JDBC driver version 3.12.8 (or later)
- Node.js driver version 1.12.0 (or later)
- ODBC driver version 2.21.2 (or later)
- Snowflake Connector for Python 2.2.8 (or later)

To enable connection caching:

1. Set the account-level parameter [ALLOW\_ID\_TOKEN](/sql-reference/parameters#label-allow-id-token) to `true`:

   Copy code

   ```
   alter account set allow_id_token = true;
   ```

   Note

   You must be an account administrator (i.e. a user with the ACCOUNTADMIN role) to enable connection caching.
2. Add the package or libraries needed by the driver or connector:

   - If you are using the Snowflake Connector for Python, install the optional keyring package by running:

     > Copy code
     >
     > ```
     > pip install "snowflake-connector-python[secure-local-storage]"
     > ```
     >
     > You must enter the square brackets (`[` and `]`) as shown in the command. The square brackets specify the [extra part of the package](https://www.python.org/dev/peps/pep-0508/#extras) that should be installed.
     >
     > Use quotes around the name of the package as shown to prevent the square brackets from being interpreted as a wildcard.
     >
     > If you need to install other extras (for example, `pandas` for [using the Python Connector APIs for Pandas](/developer-guide/python-connector/python-connector-pandas#label-python-connector-pandas-install)), use a comma between the extras:
     >
     > Copy code
     >
     > ```
     > pip install "snowflake-connector-python[secure-local-storage,pandas]"
     > ```
   - For the Snowflake JDBC Driver, see [Add the JNA classes to your classpath](/developer-guide/jdbc/jdbc-download#label-jdbc-driver-add-jna-classes-to-classpath).

### Native SSO — *Okta only*

If Okta is your IdP, Snowflake also supports authenticating natively through Okta. This authentication method is useful when you are using SSO with a client
that doesn’t have access to a web browser (e.g. connecting programmatically through the Python connector or either the JDBC or ODBC driver).

Note

Please disable Okta MFA for the user who uses Native SSO authentication with client drivers.
Please consult your Okta administrator for more information.

To enable native SSO through Okta, set the `authenticator` login parameter/option for the client to the Okta URL endpoint for your Okta account
(provided by Okta), typically in the form of `https://<okta_account_name>.okta.com`:

| Client | Instructions |
| --- | --- |
| Snowflake CLI | Set the `authenticator` parameter for the connection in the `config.toml` file, or specify the command line flag `--authenticator https://<okta_account_name>.okta.com` when starting the client. |
| SnowSQL | Specify the command line flag `--authenticator https://<okta_account_name>.okta.com` when starting the client. |
| Python | Pass `authenticator='https://<okta_account_name>.okta.com'` to the `snowflake.connector.connect()` function. |
| JDBC | Set `authenticator=https://<okta_account_name>.okta.com` in the connection string for the driver. |
| ODBC (Linux/macOS) | Set `authenticator=https://<okta_account_name>.okta.com` in the `odbc.ini` file. |
| ODBC (Windows) | In the ODBC Data Source Administrator tool, edit the DSN for Snowflake and set **Authenticator** to `https://<okta_account_name>.okta.com`. |
| .NET | Set `authenticator=https://<okta_account_name>.okta.com` in the connection string for the driver. |
| Node.js | Set the `authenticator` option to `https://<okta_account_name>.okta.com` when calling `snowflake.createConnection`. |

Expand

Show lessSee more

#### Upgrading to Okta Identity Engine

If you are upgrading from Okta Classic to Okta Identity Engine for native SSO, you need to update your Snowflake client drivers before the
upgrade.

If you encounter HTTP 429 errors after your upgrade, you have most likely hit the rate limit enforced by the authentication endpoint used
by the latest client drivers. For details, refer to [HTTP 429 errors](#label-fed-auth-429-errors) (in this topic).

#### HTTP 429 errors

The Okta Identity Engine requires communication through its authentication endpoint (`/api/v1/authn`), which currently has
a rate limit of 20 requests per user per 5 seconds. To support the Okta Identity Engine, the latest Snowflake client drivers use this
Authentication endpoint, and are therefore subject to the rate limit. If this limit is prohibitive, contact Okta Support to increase the
rate limit of the authentication endpoint.

Snowflake client drivers switched to the authentication endpoint in the following versions:

> - Go: 1.6.20
> - JDBC: 3.13.22
> - .NET: 2.0.20
> - Node.js: 1.6.21
> - ODBC: 2.25.5
> - Python: 2.7.12
> - Snowflake CLI: 3.0.0
> - SnowSQL: 1.2.24
> - SQLAlchemy: 1.4.6

## Using SSO with MFA

Snowflake supports using MFA in conjunction with SSO to provide additional levels of security:

- Individual users in Snowflake can enroll in MFA. If a Snowflake user is enrolled in MFA and uses SSO to connect, the MFA login workflow is initiated within
  the SSO workflow and is required to successfully complete the authentication. For more information about MFA in Snowflake, see
  [Multi-factor authentication (MFA)](/user-guide/security-mfa).

  Note

  To connect through Okta SSO with MFA, Snowflake requires using browser-based SSO. If you are using native SSO for Okta, MFA is not supported.
- In addition, your IdP may also support MFA, but this is separate from MFA in Snowflake and must be configured separately through your IdP. If MFA is enabled
  for your IdP, the IdP determines the workflow. To determine whether your IdP supports MFA and how it is implemented, see the documentation for your IdP.
- With certain Snowflake-provided clients, you can cache MFA tokens for up to four hours. For more information, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

## Using SSO with multiple audience values

Snowflake supports multiple audience values (i.e. Audience or Audience Restriction Fields) in the SAML 2.0 assertion from the identity provider to Snowflake.

This functionality supports the URLs to access Snowflake as audience values. The URLs for multiple Snowflake accounts are supported because
each account has a URL with a unique [account identifier](/user-guide/admin-account-identifier) to access Snowflake. Additionally,
Snowflake accepts the account domain names and the URLs to access Snowflake using private connectivity to the Snowflake service as audience
values.

For more details on SSO and avoiding the public Internet, see [SSO with private connectivity](/user-guide/admin-security-fed-auth-overview#label-sso-private-connectivity).

Currently, Snowflake supports and accepts up to four different audience values. No configuration is necessary in Snowflake. If it is
necessary to include more than four audience values, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

For help in configuring SAML 2.0 audience values, please contact your organization’s identity provider administrator.

## Using SSO with private connectivity

Snowflake supports SSO with private connectivity to the Snowflake service for Snowflake accounts on Amazon Web Services (AWS),
Microsoft Azure, and Google Cloud Platform (GCP).

For details, see [SSO with private connectivity](/user-guide/admin-security-fed-auth-overview#label-sso-private-connectivity).
