# Configuring a second factor of authentication

When a password user is enrolled in [Multi-factor authentication (MFA)](/user-guide/security-mfa), they must use a second factor of
authentication when signing in to Snowflake. These users enter their password, then use the second factor.

Snowflake provides the following possible second factors:

- Authenticating with a passkey that can be stored and accessed in a variety of ways.
- Authenticating with your preferred authenticator app.
- Authenticating with Duo.

Your administrator controls which factors are available to you. For more information, see [Restricting which MFA methods are available](/user-guide/security-mfa#label-mfa-restrict-methods).

## Get started

When an administrator requires a user to enroll in MFA, the user is prompted to add a second factor of authentication the next time they
sign in to Snowsight.

If you are already signed in to Snowsight and want to set up a second factor of authentication, do the following:

1. In the left-hand navigation, select your name. The user menu opens.
2. Select **Settings**.
3. Select **Authentication**.
4. In the **Multi-factor authentication** section, select **Add new authentication method**.
5. Follow the prompts to configure your second factor of authentication.

## Using passkey authentication

A passkey is a form of authentication based on the [WebAuthn standard](https://www.w3.org/TR/webauthn-3/), which uses public/private key
cryptography. When you successfully configure Snowflake to authenticate with a passkey, the private key is securely stored in a personal
location, whether it’s on your machine, a hardware security key (for example, a Yubikey), or a password manager.

To set up a passkey as your second factor of authentication, complete the following tasks:

1. When [prompted](#label-mfa-secondary-methods-get-started), select **Passkey**.
2. Complete the steps to store your passkey as you would with any other website or application. For example, you can use a hardware security
   key or configure your machine so you must use a fingerprint to access the passkey when authenticating.
3. Specify a name for the authentication method so that you can identify it when signing in to Snowflake.

After you enter your password, you’ll be prompted to provide your passkey, using the method you configured.

## Using an authenticator app

Snowflake allows you to use your preferred authenticator app to use a time-based one-time passcode (TOTP) as your second factor of
authentication. Common authenticator apps include Google Authenticator, Microsoft Authenticator, and Authy.

To set up an authenticator app as your second factor, complete the following tasks:

1. When [prompted](#label-mfa-secondary-methods-get-started), select **Authenticator**.
2. Complete the steps with your authenticator app as you would with any other website or application.
3. Specify a name for the authentication method so that you can identify it when signing in to Snowflake.

After you enter your password, you’ll be prompted to enter the TOTP from your authenticator app.

## Using Duo

To set up Duo as your second factor, complete the following tasks:

1. When [prompted](#label-mfa-secondary-methods-get-started), select **DUO**.
2. Complete the steps with Duo as you would with any other website or application.

Note

Your administrator must configure your organization’s firewall before you can use Duo as a second factor of authentication. For more
information, see [Prerequisite](/user-guide/security-mfa-duo#label-mfa-duo).

## View your authentication methods

You can use Snowsight or SQL to view your second factors of authentication.

SnowsightSQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the left-hand navigation, select your name. The user menu opens.
3. Select **Settings**.
4. Select **Authentication**.
5. Use the **Multi-factor authentication** section to view your MFA methods.

Execute the [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods) command.

Copy code

```
SHOW MFA METHODS;
```

Note

If you’re an administrator who wants to view the authentication method of another user, see [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods).

For information about the passkeys and TOTPs for all users in the account, query the
[CREDENTIALS view](/sql-reference/account-usage/credentials). Note that this view does not include information about
[Duo authenticators](/user-guide/security-mfa-duo) (Duo push and passcodes).

## Set a default authentication method

If you configured more than one MFA method as a second factor of authentication, you can choose which one you’ll use to authenticate after
you enter your password. To set the default second factor, do the following:

1. In the left-hand navigation, select your name. The user menu opens.
2. Select **Settings**.
3. Select **Authentication**.
4. In the **Multi-factor authentication** section, select an MFA method from the **Default sign-in method** drop-down.

## Identifying the login sessions in which a second-factor credential was used

To determine when a second-factor credential was used for authentication (for example, a specific passkey or time-based one-time
passcode), you can join the [LOGIN\_HISTORY](/sql-reference/account-usage/login_history) and
[CREDENTIALS](/sql-reference/account-usage/credentials) views in the ACCOUNT\_USAGE schema on the column containing the
credential ID:

- The LOGIN\_HISTORY view contains the credential ID in the `second_authentication_factor_id` column, if the
  `second_authentication_factor` column contains `PASSKEY` or `TOTP`.
- The CREDENTIALS view contains the credential ID in the `credential_id` column.

For example:

Copy code

```
SELECT
    login.event_timestamp,
    login.user_name,
    cred.name
  FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY login
    JOIN SNOWFLAKE.ACCOUNT_USAGE.CREDENTIALS cred
    ON login.second_authentication_factor_id = cred.credential_id
  WHERE login.second_authentication_factor IN ('PASSKEY', 'TOTP');
```

```
+-------------------------------+-----------+--------------+
| EVENT_TIMESTAMP               | USER_NAME | NAME         |
|-------------------------------+-----------+--------------|
| 2025-08-05 17:10:00.941 -0700 | USER_A    | PASSKEY_RALU |
| 2025-07-28 13:04:27.201 -0700 | USER_B    | TOTP_D406    |
| 2025-07-21 09:09:47.701 -0700 | USER_C    | PASSKEY_GN1N |
+-------------------------------+-----------+--------------+
```

To get information about the queries that were run during this login session, you can join the LOGIN\_HISTORY view with the
[SESSIONS](/sql-reference/account-usage/sessions) view on the `login_event_id` column to get the session ID, and then
use that to join the [QUERY\_HISTORY](/sql-reference/account-usage/query_history) view.
