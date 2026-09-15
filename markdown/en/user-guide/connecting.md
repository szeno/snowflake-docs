# Sign in to Snowflake

You can sign in to Snowflake in several ways. If you’re getting started with Snowflake, start by using
[Snowsight](/user-guide/ui-snowsight), Snowflake’s browser-based web interface. After you get
comfortable with using Snowsight, you can explore other ways to connect.

To sign in to Snowflake, you need the following information:

- Your account identifier.

  All access to Snowflake is through your account identifier. If you don’t know your account identifier, ask
  your Snowflake account administrator. For more information, see [Account identifiers](/user-guide/admin-account-identifier).
- Your authentication method.

  The way you sign in to Snowflake depends on the authentication method used by your organization. Two
  common authentication methods for users are federated authentication with single sign-on (SSO) and password with
  multi-factor authentication (MFA):

  - **SSO:** Users authenticate with a third-party identity provider (IdP) instead of authenticating with Snowflake directly.
    Examples of IdPs are Okta and Microsoft Entra ID.
  - **Password with MFA:** When users sign in with a username and password, they must use a second factor of authentication.
    These users enter their username and password, and then use the second factor to complete the authentication. Currently,
    Snowflake allows the following MFA methods: passkeys, authenticator apps, and Duo.

  If you don’t know which authentication method your organization uses, check with your Snowflake account
  administrator.

  If your organization uses password with MFA authentication, you can configure MFA when you
  [sign in to Snowsight](#label-sign-in-using-snowsight).

  Other authentication methods are supported for both users and applications. For more information about authentication
  methods, see [Overview of Snowflake authentication](/user-guide/security-authentication-overview).

## Sign in by using Snowsight

You can access [Snowsight](/user-guide/ui-snowsight) over the public internet or through private connectivity
to the Snowflake service.

Note

- Check with your Snowflake account administrator about instructions for signing in.
- If your organization uses private connectivity to access Snowsight, see
  [Using private connectivity](/user-guide/ui-snowsight-gs#label-ui-snowsight-gs-private-connectivity).

To access Snowsight over the public internet, complete the following steps:

1. In a supported web browser, navigate to <https://app.snowflake.com>.
2. Provide your [account identifier](/user-guide/admin-account-identifier) or account URL.
   If you previously signed in to Snowsight, you might see an account name that you can select.
3. Choose your authentication method, and then sign in.

If you are signing in to Snowsight for the first time, you might be prompted to configure
MFA. For instructions, see [Snowsight and MFA](/user-guide/ui-snowsight-gs#label-ui-snowsight-gs-mfa-notifications).

For information about the tasks that you can perform in Snowsight, see
[Snowsight quick tour](/user-guide/ui-snowsight-quick-tour).

## Connect by using other methods

In addition to Snowsight, you can use the following methods to connect to Snowflake:

- Using [Snowflake CLI](/developer-guide/snowflake-cli/index).
- Using third-party client services and applications that support JDBC or ODBC.
- Developing applications that connect through the Snowflake connectors and drivers for Python, Node.js, Spark,
  and so on.

These methods require additional installation, configuration, and development tasks. For more information, see
[Applications and tools for connecting to Snowflake](/guides-overview-connecting).
