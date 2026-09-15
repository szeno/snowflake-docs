# Multi-factor authentication (MFA)

Multi-factor authentication (MFA) reduces the security risks associated with password authentication. When a password user is enrolled in
MFA, they must use a second factor of authentication when signing in to Snowflake. These users enter their password, and then use the second
factor. For information about how a user adds an MFA method that they can use as a second factor of authentication, see
[Configuring a second factor of authentication](/user-guide/security-mfa-second-factor).

MFA is intended for *human users* who authenticate with a password. *Service users* must use another form of authentication. For more
information about these user types, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

Important

To improve the security posture of all of its customers, Snowflake is rolling out changes to require MFA for all password sign-ins. For
information about this rollout, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

## Requiring users to enroll in MFA

Currently, strategies for implementing MFA for your organization vary depending on whether or not an account existed when the
[2024\_08 behavior change bundle](/release-notes/bcr-bundles/2024_08_bundle) was enabled:

- If an account existed before the 2024\_08 bundle was enabled, then you must configure your account if you want to require all human users to
  use MFA. For information about implementing MFA to require all human users to enroll in MFA, see
  [Hardening user or account authentication using MFA](/user-guide/authentication-policies#label-authentication-policy-hardening-authentication).
- If the account was created after the 2024\_08 bundle was enabled, then all human users who authenticate with a password must enroll in MFA
  by default. This MFA requirement does not apply to service users.

  If you want to disable the requirement that all human users enroll in MFA, create a custom authentication policy with
  `MFA_ENROLLMENT=OPTIONAL`, and then set the authentication policy on the account. Password users who use Snowsight must still
  use MFA, but MFA isn’t required for other interfaces. For more information about creating and setting authentication policies, see
  [Authentication policies](/user-guide/authentication-policies).

  Be aware that the ability to opt out of mandatory MFA for human users is temporary; see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

## Requiring MFA for single sign-on authentication

By default, Snowflake doesn’t require MFA for users who authenticate with single sign-on (SSO). Snowflake relies on the identity provider
(IdP) to enforce MFA or some other strong authentication method. If you want to harden authentication for SSO users, you use an
[authentication policy](/user-guide/authentication-policies) to require SSO users to use Snowflake MFA after authenticating with the
IdP.

The following authentication policy requires SSO users to enroll and use Snowflake MFA:

Copy code

```
CREATE AUTHENTICATION POLICY ACCOUNTADMIN_DOUBLE_MFA
  AUTHENTICATION_METHODS = ('PASSWORD', 'SAML', 'OIDC')
  SECURITY_INTEGRATIONS = ('<SAML OR OIDC SECURITY INTEGRATIONS>')
  MFA_ENROLLMENT = 'REQUIRED'
  MFA_POLICY=(ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION='ALL');
```

## Restricting which MFA methods are available

When a user is enrolled in MFA, they are required to use an MFA method as a second factor of authentication. Snowflake allows the following
MFA methods:

- Authenticating with a passkey that can be stored and accessed in a variety of ways.
- Authenticating with an authenticator app that generates a time-based one-time passcode (TOTP).
- Authenticating with Duo.

Tip

As you decide which MFA methods to allow, keep in mind the following:

- Passkeys are recommended due to their security and usability.
- Duo is not replicated like the other MFA methods.

As an administrator, you can use an [authentication policy](/user-guide/authentication-policies) to control which MFA methods can be
used as a second factor of authentication. For example, the following authentication policy allows users to use a passkey or authenticator
app as their second factor of authentication, but not Duo:

Copy code

```
CREATE AUTHENTICATION POLICY mfa_policy
  MFA_ENROLLMENT = REQUIRED
  MFA_POLICY = (ALLOWED_METHODS = ('PASSKEY', 'TOTP'));
```

If a user previously configured an MFA method that is now prohibited, the next time they sign in they’ll be prompted to authenticate
using the pre-existing method, then prompted to configure a new, allowed method.

For more information about the MFA\_POLICY parameter, see [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy).

## Removing a user’s MFA methods

You can remove an MFA method that a user previously added so that they can no longer use it as their second factor of authentication.

1. Execute the [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods) command and find the value in the `name` column. For example, if you are
   removing an MFA method for a user `joe`, execute the following and copy the `name` of the MFA method from the output:

   Copy code

   ```
   SHOW MFA METHODS FOR USER joe;
   ```

   ```
   +---------------+-----------------+------------------------+-------------------------------+---------------------------------+---------------------+
   |   name        |      type       |    comment             |     last_used                 |        created_on               |  additional_info    |
   +---------------+-----------------+------------------------+-------------------------------+---------------------------------+---------------------+
   | TOTP-48A7     |    TOTP         | Authenticator App 48A7 | 2025-02-26 11:14:38.000 -0800 |  2025-02-26 11:13:19.000 -0800  | null                |
   +---------------+-----------------+------------------------+-------------------------------+---------------------------------+---------------------+
   ```
2. Execute an [ALTER USER … REMOVE MFA METHOD](/sql-reference/sql/alter-user) statement to remove the MFA method:

   Copy code

   ```
   ALTER USER joe REMOVE MFA METHOD TOTP-48A7;
   ```

## Recovering a user who is locked out

If a password user is locked out of Snowflake because they don’t have access to a second factor of authentication, an administrator can help
them recover the ability to sign in by [temporarily disabling MFA](#label-mfa-temp-disable) or by helping the user
[set up a new MFA method](#label-mfa-recovery-new-method).

### Prompt user to add a new MFA method

If a user loses access to the MFA method that they use as their second factor of authentication (for example, by losing the YubiKey that
stores their passkey), an administrator can help the user set up a new MFA method so that they can sign in to Snowflake.

When a user does not have access to their MFA method and needs to set up a new one, the administrator executes an
[ALTER USER … ENROLL MFA](/sql-reference/sql/alter-user) statement. For example, if user `joe` needs to establish a new MFA
method, the administrator can execute the following:

Copy code

```
ALTER USER joe ENROLL MFA;
```

- If the user has a [verified email](/user-guide/ui-snowsight-profile#label-snowsight-verify-email-address), Snowflake sends an email prompting them to add an MFA
  authentication method.
- If the user doesn’t have a verified email, Snowflake returns the URL of a page that prompts the user to add an MFA authentication method.
  Administrators can send this URL to the locked-out user.

### Temporarily disable MFA

If an administrator needs to temporarily disable MFA for a user, they can execute an
[ALTER USER … SET MINS\_TO\_BYPASS\_MFA](/sql-reference/sql/alter-user) statement. For example, to temporarily disable MFA so that user
`joe` can authenticate with a single-factor password for 30 minutes, execute the following:

Copy code

```
ALTER USER joe SET MINS_TO_BYPASS_MFA = 30;
```

## Setting up administrators for break glass access

Break glass refers to the ability to log in using alternative authentication methods not typically available in the account. Administrators
need break glass access to Snowflake if regular authentication methods become unavailable; for example, if an organization’s identity
provider has an outage.

Organizations can provide break glass access by creating a dedicated Snowflake user, and then storing the user’s password credential in a
key vault. An administrator can generate one or more one-time passcodes (OTPs) that can be stored in the vault with the user’s password. To
access Snowflake, an administrator can retrieve the password and OTP from the vault, and then sign in. Using OTPs creates an additional
layer of protection and satisfies Snowflake multi-factor authentication requirements.

Important

After an OTP is used to authenticate, it is invalidated and can’t be used to authenticate again.

If there aren’t additional OTPs available and the user doesn’t have another MFA method available, the user might be locked out when their
session expires. Always ensure a backup MFA method is available for the user to prevent accidental lockouts. For information about
recovering a user who is locked out, see [Recovering a user who is locked out](#label-mfa-recovery).

### Generating one-time passcodes

To generate one or more OTPs for a user, run an [ALTER USER … ADD MFA METHOD OTP](/sql-reference/sql/alter-user) command. The
optional COUNT keyword determines how many OTPs are generated. For example, to generate 5 OTPs for the user `breakglass_user`, run the
following command:

Copy code

```
ALTER USER breakglass_user ADD MFA METHOD OTP COUNT = 5;
```

After the codes are generated, you can use them as your second factor of authentication when authenticating to Snowflake.

### Invalidating one-time passcodes

You have the following options if you want to invalidate a one-time passcode (OTP) so it can’t be used to authenticate.

**Invalidate all existing OTPs for a user**

- Use the ALTER USER … ADD MFA METHOD OTP command to generate new OTPs. Previously generated OTPs are invalidated.

**Invalidate a specific OTP for the current user**

- Use Snowsight to invalidate an OTP by taking the following steps:
  1. In the left-hand navigation, select your name.
  2. In the user menu, select **Settings**.
  3. Select **Authentication**.
  4. In the **Multi-factor authentication** section, find the OTP, and then select the **More** icon.
  5. Select **Unenroll**, and then confirm that you want to delete the OTP.

**Invalidate a specific OTP for a different user**

- Use the ALTER USER … REMOVE MFA METHOD command to invalidate a specific OTP for a different user. If you want to invalidate an OTP for
  yourself, use Snowsight. For example, to invalidate the `OTP_2` passcode for user `joe`, run the following command:

  Copy code

  ```
  ALTER USER joe REMOVE MFA METHOD OTP_2;
  ```

### Replicating authentication for break glass users

You can’t replicate OTPs from a source account to a target account when you replicate the break glass user. This is to prevent a scenario where an OTP could be used twice, once in the source account and again in the target account. You have two options to implement authentication for the break glass user in the target account:

- Sign in to the target account and generate OTPs for the user in that account.
- Replace the use of OTPs with a time-based one-time passcode (TOTP) or passkey, which can be replicated.

## Connecting to Snowflake with MFA

MFA login is designed primarily for connecting to Snowflake through the web interface, but is also fully-supported by Snowflake CLI, SnowSQL, and the
Snowflake JDBC, Node.js, and ODBC drivers.

Note

MFA configurations using landline or phone callbacks do not support connecting with drivers, such as ODBC and JDBC.

### Using MFA token caching to minimize the number of prompts during authentication — *optional*

MFA token caching can help to reduce the number of prompts that must be acknowledged while connecting and authenticating to Snowflake,
especially when multiple connection attempts are made within a relatively short time interval.

A cached MFA token is valid for up to four hours.

The cached MFA token is invalid if any of the following conditions are met:

1. The [ALLOW\_CLIENT\_MFA\_CACHING](/sql-reference/parameters#label-allow-client-mfa-caching) parameter is set to FALSE for the account.
2. The method of authentication changes.
3. The authentication credentials change (i.e. username and/or password).
4. The authentication credentials are not valid.
5. The cached token expires or is not cryptographically valid.
6. The account name associated with the cached token changes.

The overall process Snowflake uses to cache MFA tokens is similar to that used to cache connection tokens for browser-based federated
[single sign-on](/user-guide/admin-security-fed-auth-use#label-browser-based-sso-connection-caching). The client application stores the MFA token in the keystore of the
client-side operating system. Users can delete the cached MFA token from the keystore at any time.

Snowflake supports MFA token caching with the following drivers, connectors, and tools:

- .NET driver version 4.3.0 (or later)
- ODBC driver version 2.23.0 (or later).
- JDBC driver version 3.12.16 (or later).
- Python Connector for Snowflake version 2.3.7 (or later).
- Snowflake CLI version 3.0 (or later)

Snowflake recommends consulting with internal security and compliance officers prior to enabling MFA token caching.

Tip

MFA token caching can be combined with connection caching in federated [single sign-on](/user-guide/admin-security-fed-auth-use#label-browser-based-sso-connection-caching).

To combine these two features, ensure that the [ALLOW\_ID\_TOKEN](/sql-reference/parameters#label-allow-id-token) parameter is set to `true` in tandem with the ALLOW\_CLIENT\_MFA\_CACHING parameter.

To enable MFA token caching, complete the following steps:

1. As an account administrator (i.e. a user with the ACCOUNTADMIN system role), set the ALLOW\_CLIENT\_MFA\_CACHING parameter to `true`
   for an account using the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command.

   Copy code

   ```
   ALTER ACCOUNT SET ALLOW_CLIENT_MFA_CACHING = TRUE;
   ```
2. In the client connection string, update the authenticator value to `authenticator = username_password_mfa`.
3. Add the package or libraries needed by the driver or connector:

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

To disable MFA token caching, unset the ALLOW\_CLIENT\_MFA\_CACHING parameter:

Copy code

```
ALTER ACCOUNT UNSET ALLOW_CLIENT_MFA_CACHING;
```

To find all users who use MFA token caching as the second-factor authentication to log in, you can execute the following SQL statement as an
account administrator (a user with the ACCOUNTADMIN role):

Copy code

```
SELECT EVENT_TIMESTAMP,
       USER_NAME,
       IS_SUCCESS
  FROM SNOWFLAKE.ACCOUNT_USAGE.LOGIN_HISTORY
  WHERE SECOND_AUTHENTICATION_FACTOR = 'MFA_TOKEN';
```

### Using MFA with Snowflake CLI

MFA can be used for connecting to Snowflake through Snowflake CLI. By default, the Duo Push authentication mechanism is used when a user is
enrolled in MFA.

To use a Duo-generated passcode instead of the push mechanism, the login parameters must include one of the following connection options:

- Use the `--mfa-passcode <string>` option.
- Set `passcode_in_password=true` in the `config.toml` configuration file.

For more details, see [Use multi-factor authentication (MFA)](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-mfa).

### Using MFA with SnowSQL

MFA can be used for connecting to Snowflake through SnowSQL. By default, the Duo Push authentication mechanism is used when a user is
enrolled in MFA.

To use a Duo-generated passcode instead of the push mechanism, the login parameters must include one of the following connection options:

> `--mfa-passcode <string>` OR `--mfa-passcode-in-password`

For more details, see [SnowSQL (CLI client)](/user-guide/snowsql).

### Using MFA with JDBC

MFA can be used for connecting to Snowflake via the Snowflake JDBC driver. By default, the Duo Push authentication mechanism is used when a
user is enrolled in MFA; no changes to the JDBC connection string are required.

To use a Duo-generated passcode instead of the push mechanism, one of the following parameters must be included in the JDBC connection
string:

> `passcode=<passcode_string>` OR `passcodeInPassword=on`

Where:

- `passcode_string` is a Duo-generated passcode for the user who is connecting. This can be a passcode generated by the Duo Mobile
  application or an SMS passcode.
- If `passcodeInPassword=on`, then the password and passcode are concatenated, in the form of
  `<password_string><passcode_string>`.

For more details, see [JDBC Driver](/developer-guide/jdbc/jdbc).

#### Examples of JDBC connection strings using Duo

JDBC connection string for user `demo` connecting to the `xy12345` account (in the US West region) using a Duo passcode:

> Copy code
>
> ```
> jdbc:snowflake://xy12345.snowflakecomputing.com/?user=demo&passcode=123456
> ```

JDBC connection string for user `demo` connecting to the `xy12345` account (in the US West region) using a Duo passcode that is
embedded in the password:

> Copy code
>
> ```
> jdbc:snowflake://xy12345.snowflakecomputing.com/?user=demo&passcodeInPassword=on
> ```

### Using MFA with Node.js

MFA can be used for connecting to Snowflake through the Snowflake Node.js driver. By default, the Duo Push authentication mechanism is used when a user is enrolled in MFA.

To use a Duo-generated passcode instead of the push mechanism, the login parameters must include one of the following connection options. Both examples use a password of `abc123` and MFA passcode of `987654` to demonstrate the configuration.

- Set the `passcodeInPassword` option to `true` and include the passcode as part of the password string, similar to the following:

  Copy code

  ```
  authenticator: 'USERNAME_PASSWORD_MFA',
  password: "abc123987654", // passcode 987654 is part of the password
  passcodeInPassword: true  // because passcodeInPassword is true
  ```
- Set the `passcode` option to the value of the passcode to specify the password and the passcode separately, similar to the following:

  Copy code

  ```
  authenticator: 'USERNAME_PASSWORD_MFA',
  password: "abc123", // password and MFA passcode are input separately
  passcode: "987654"
  ```

  To use this approach, ensure that the `passcodeInPassword` option is `false` (the default value). If both `passcodeInPassword` is set to `true` and `passcode` is also configured, the `passcodeInPassword` setting takes precedence and the driver assumes the `password` field contains both the password and the MFA passcode when authenticating.

For more details, see [Use an MFA passcode](/developer-guide/node-js/nodejs-driver-authenticate#label-nodejs-mfa).

### Using MFA with ODBC

MFA can be used for connecting to Snowflake via the Snowflake ODBC driver. By default, the Duo Push authentication mechanism is used when a
user is enrolled in MFA; no changes to the ODBC settings are required.

To use a Duo-generated passcode instead of the push mechanism, one of the following parameters must be specified for the driver:

> `passcode=<passcode_string>` OR `passcodeInPassword=on`

Where:

- `passcode_string` is a Duo-generated passcode for the user who is connecting. This can be a passcode generated by the Duo Mobile
  application or an SMS passcode.
- If `passcodeInPassword=on`, then the password and passcode are concatenated, in the form of
  `<password_string><passcode_string>`.

For more details, see [ODBC Driver](/developer-guide/odbc/odbc).

### Using MFA with Python

MFA can be used for connecting to Snowflake via the Snowflake Python Connector. By default, the Duo Push authentication mechanism is used
when a user is enrolled in MFA; no changes to the Python API calls are required.

To use a Duo-generated passcode instead of the push mechanism, one of the following parameters must be specified for the driver in the
connect() method:

> `passcode=<passcode_string>` OR `passcode_in_password=True`

Where:

- `passcode_string` is a Duo-generated passcode for the user who is connecting. This can be a passcode generated by the Duo Mobile
  application or an SMS passcode.
- If `passcode_in_password=True`, then the password and passcode are concatenated, in the form of
  `<password_string><passcode_string>`.

For more details, see the description of the connect() method in the [Functions](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods) section of the Python
Connector API documentation.
