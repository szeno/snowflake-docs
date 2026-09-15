# ALTER AUTHENTICATION POLICY

Modifies the properties of an [authentication policy](/user-guide/authentication-policies).

See also:
:   [CREATE AUTHENTICATION POLICY](/sql-reference/sql/create-authentication-policy), [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy), [DROP AUTHENTICATION POLICY](/sql-reference/sql/drop-authentication-policy), [SHOW AUTHENTICATION POLICIES](/sql-reference/sql/show-authentication-policies)

## Syntax

Copy code

```
ALTER AUTHENTICATION POLICY <name> RENAME TO <new_name>

ALTER AUTHENTICATION POLICY [ IF EXISTS ] <name> SET
  [ AUTHENTICATION_METHODS = ( '<string_literal>' [ , '<string_literal>' , ...  ] ) ]
  [ CLIENT_TYPES = ( '<string_literal>' [ , '<string_literal>' , ...  ] ) ]
  [ CLIENT_POLICY = ( <client_type> = ( MINIMUM_VERSION = '<version>' ) [ , ... ] ) ]
  [ SECURITY_INTEGRATIONS = ( '<string_literal>' [ , '<string_literal>' , ...  ] ) ]
  [ MFA_ENROLLMENT = { 'REQUIRED' | 'REQUIRED_PASSWORD_ONLY' | 'OPTIONAL' } ]
  [ MFA_POLICY = ( <list_of_properties> ) ]
  [ PAT_POLICY = ( <list_of_properties> ) ]
  [ WORKLOAD_IDENTITY_POLICY = ( <list_of_properties> ) ]
  [ COMMENT = '<string_literal>' ]

ALTER AUTHENTICATION POLICY [ IF EXISTS ] <name> UNSET
  [ AUTHENTICATION_METHODS ]
  [ CLIENT_TYPES ]
  [ CLIENT_POLICY ]
  [ SECURITY_INTEGRATIONS ]
  [ MFA_ENROLLMENT ]
  [ MFA_POLICY ]
  [ PAT_POLICY ]
  [ WORKLOAD_IDENTITY_POLICY ]
  [ COMMENT ]
  [ DCM PROJECT ]
```

## Parameters

`name`
:   Specifies the identifier for the authentication policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO ...`
:   Specifies a new name for an existing authentication policy.

`SET ...`
:   Specifies one or more properties to set for the authentication policy, separated by blank spaces, commas, or new lines.

    `AUTHENTICATION_METHODS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Changes the authentication methods that are allowed during login. This parameter accepts one or more of the following values:

        Caution

        Restricting by authentication method can have unintended consequences, such as blocking driver connections or third-party
        integrations.

        `ALL`
        :   Allow all authentication methods.

        `SAML`
        :   Allows [SAML2 security integrations](/user-guide/admin-security-fed-auth-security-integration). If `SAML` is
            present, an SSO login option appears. If `SAML` is not present, an SSO login option does not appear.

        `OIDC`
        :   Allows [OIDC security integrations](/user-guide/admin-security-fed-auth-oidc). If `OIDC` is present, an OIDC SSO login option appears. If
            `OIDC` is not present, an OIDC SSO login option does not appear.

        `PASSWORD`
        :   Allows users to authenticate using username and password.

        `OAUTH`
        :   Allows [External OAuth](/user-guide/oauth-ext-overview).

        `KEYPAIR`
        :   Allows [Key pair authentication](/user-guide/key-pair-auth).

        `PROGRAMMATIC_ACCESS_TOKEN`
        :   Allows users to authenticate with a [programmatic access token](/user-guide/programmatic-access-tokens).

        `WORKLOAD_IDENTITY`
        :   Allows users to authenticate through [workload identity federation](/user-guide/workload-identity-federation).

        Default: `ALL`.

    `CLIENT_TYPES = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Changes which clients can authenticate with Snowflake.

        If a client tries to connect, and the client is not one of the valid `CLIENT_TYPES` values listed below, then the login attempt fails.

        If you set `MFA_ENROLLMENT` to `REQUIRED`, then you must include `SNOWFLAKE_UI` in the `CLIENT_TYPES` list to allow
        users to enroll in MFA.

        If you want to exclude `SNOWFLAKE_UI` from the `CLIENT_TYPES` list, then you must set `MFA_ENROLLMENT` to
        `OPTIONAL`.

        The `CLIENT_TYPES` property of an authentication policy is a best-effort method to block user logins based on specific clients. It should not be used as the sole control to establish a security boundary. Notably, it does not restrict access to the Snowflake REST APIs.

        This property accepts one or more of the following values:

        `ALL`
        :   Allow all clients to authenticate.

        `SNOWFLAKE_UI`
        :   [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), the Snowflake web interface.

            Caution

            If `SNOWFLAKE_UI` is not included in the `CLIENT_TYPES` list while `MFA_ENROLLMENT` is set to `REQUIRED`, or `MFA_ENROLLMENT` is unspecified, MFA enrollment doesn’t work.

        `DRIVERS`
        :   Drivers allow access to Snowflake from applications written in
            [supported languages](/developer-guide/drivers). For example, the [Go](/developer-guide/golang/go-driver),
            [JDBC](/developer-guide/jdbc/jdbc), [.NET](/developer-guide/dotnet/dotnet-driver) drivers, and
            [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview).

            Caution

            If `DRIVERS` is not included in the `CLIENT_TYPES` list, automated ingestion may stop working.

        `SNOWFLAKE_CLI`
        :   A [command-line client](/developer-guide/snowflake-cli/index) for connecting to Snowflake and for managing developer-centric workloads and SQL operations.

        `SNOWSQL`
        :   A [command-line client](/user-guide/snowsql) for connecting to Snowflake.

        If a client tries to connect, and the client is not one of the valid `CLIENT_TYPES`, then the login attempt fails. If
        `CLIENT_TYPES` is unset, any client can connect.

        Default: `ALL`.

    `CLIENT_POLICY = client_type = ( MINIMUM_VERSION = 'version' )`
    :   Specifies a policy within the authentication policy that sets the minimum version allowed for each specified client type.

        If CLIENT\_TYPES is empty, contains `ALL`, or contains `DRIVERS`, the CLIENT\_POLICY parameter accepts one or more of the following driver clients (and a specific version string). For any driver client that is not specified, the policy implicitly allows any
        version of that client.

        If CLIENT\_TYPES contains another value, such as `SNOWFLAKE_CLI`, and does not also contain `DRIVERS`, specifying any of the following client types results in an error. You can’t create (or alter) an authentication policy such that the CLIENT\_TYPES and CLIENT\_POLICY parameters aren’t compatible.

        `client_type`
        :   One or more valid client type values. This is a different set of values from those that the CLIENT\_TYPES parameter accepts. Do not use single quotes for these values.

            - `JDBC_DRIVER` (Snowflake JDBC Driver)
            - `ODBC_DRIVER` (Snowflake ODBC Driver)
            - `PYTHON_DRIVER` (Snowflake Python Driver)
            - `JAVASCRIPT_DRIVER` (Snowflake Javascript Driver)
            - `C_DRIVER` (Libsnowflakeclient C Driver)
            - `GO_DRIVER` (Snowflake Go Driver)
            - `PHP_DRIVER` (Snowflake PHP PDO Driver)
            - `DOTNET_DRIVER` (Snowflake .NET Driver)
            - `SQL_API` (SQL API)
            - `SNOWPIPE_STREAMING_CLIENT_SDK` (Snowpipe Streaming Client SDK)
            - `PY_CORE` (Snowflake Python Core Driver)
            - `SPROC_PYTHON` (Snowflake Python Stored Procedure)
            - `PYTHON_SNOWPARK` (Snowflake Python Snowpark Driver)
            - `SQL_ALCHEMY` (Snowflake SQLAlchemy)
            - `SNOWPARK` (Snowpark)
            - `SNOWFLAKE_CLIENT` (Snowflake Client SDK)

        `'version'`
        :   The minimum accepted version for each specified client type: a sequence of three digits delimited by periods and enclosed by single quotation marks.
            For example: `'1.0.0'` or `'3.14.1'`. Authentication attempts with lower client versions are blocked when this policy is in effect for an account or a user.

        The CLIENT\_POLICY property of an authentication policy is a best-effort method to block user logins based on specific client versions. It should not be used as the sole control to establish a security boundary.

    `SECURITY_INTEGRATIONS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Changes the security integrations that the authentication policy is associated with. This parameter has no effect when `SAML`, `OIDC`,
        or `OAUTH` are not in the `AUTHENTICATION_METHODS` list.

        All values in the `SECURITY_INTEGRATIONS` list must be compatible with the values in the `AUTHENTICATION_METHODS` list. For
        example, if `SECURITY_INTEGRATIONS` contains a SAML security integration, and `AUTHENTICATION_METHODS` contains
        `OAUTH`, then you cannot create the authentication policy. Similarly, if `SECURITY_INTEGRATIONS` contains an OIDC security integration,
        and `AUTHENTICATION_METHODS` contains `SAML` only, then you cannot create the authentication policy.

        `ALL`
        :   Allow all security integrations.

        Default: `ALL`.

    `MFA_ENROLLMENT = { 'REQUIRED' | 'REQUIRED_PASSWORD_ONLY' | 'OPTIONAL' }`
    :   Determines whether a user must enroll in multi-factor authentication. If this value is used, then
        the `CLIENT_TYPES` parameter must include `SNOWFLAKE_UI`, because Snowsight is the only place users can
        [enroll in multi-factor authentication (MFA)](/user-guide/ui-snowsight-profile#label-snowsight-set-up-mfa).

        `REQUIRED`
        :   Human users who are using password or single sign-on (SSO) authentication must enroll in MFA.

        `REQUIRED_PASSWORD_ONLY`
        :   All human users who are using password authentication must enroll in MFA, regardless of the client they are using. Users using SSO
            authentication are not required to enroll.

        `OPTIONAL`
        :   Retained for backward compatibility only.

    `MFA_POLICY= ( list_of_properties )`
    :   Specifies the policies that affect how multi-factor authentication (MFA) is enforced. Set this to a space-delimited list of one or more
        of the following properties and values:

        `ALLOWED_METHODS = ( { 'ALL' | 'PASSKEY' | 'TOTP' | 'OTP' | 'DUO' } [ , { 'PASSKEY' | 'TOTP' | 'OTP' | 'DUO' } ... ] )`
        :   Specifies the multi-factor authentication (MFA) methods that users can use as a second factor of authentication. You can specify more than one method as a comma-delimited list.

            `ALL`
            :   Users can use a passkey, an authenticator app, or Duo as their second factor of authentication.

            `PASSKEY`
            :   Users can use a passkey as their second factor of authentication.

            `TOTP`
            :   Users can use an authenticator app as their second factor of authentication.

            `OTP`
            :   User can use a one-time passcode as their second factor of authentication. For more information, see [Setting up administrators for break glass access](/user-guide/security-mfa#label-mfa-breakglass).

            `DUO`
            :   Users can use Duo as their second factor of authentication.

            Default: `ALL`.

        `ENFORCE_MFA_ON_EXTERNAL_AUTHENTICATION = { 'ALL' | 'NONE' }`
        :   Specifies whether multi-factor authentication (MFA) is required when users authenticate with single sign-on (SSO). To require MFA, specify
            `ALL`.

            Default: `NONE`

    `PAT_POLICY = ( list_of_properties )`
    :   Specifies the policies for [programmatic access tokens](/user-guide/programmatic-access-tokens). Set this to a
        space-delimited list of one or more of the following properties and values:

        `DEFAULT_EXPIRY_IN_DAYS = number_of_days`
        :   Specifies the default expiration time (in days) for a programmatic access token. You can specify a value from 1 to the
            maximum expiration time (which you can specify by setting MAX\_EXPIRY\_IN\_DAYS).

            The default expiration time is 15 days.

            For more information, see [Setting the default expiration time](/user-guide/programmatic-access-tokens#label-pat-default-expiration-time).

        `MAX_EXPIRY_IN_DAYS = number_of_days`
        :   Specifies the maximum number of days that can be set for the expiration time for a programmatic access token. You can specify
            a value from the default expiration time (which you can specify by setting DEFAULT\_EXPIRY\_IN\_DAYS) to 365.

            The default maximum expiration time is 365 days.

            Note

            If there are existing programmatic access tokens with expiration times that exceed the new maximum expiration time, attempts to
            authenticate with those tokens will fail.

            For example, suppose that you generate a programmatic access token named `my_token` with the expiration time of 7 days. If you
            later change the maximum expiration time for all tokens to 2 days, authenticating with `my_token` will fail because the
            expiration time of the token exceeds the new maximum expiration time.

            For more information, see [Setting the maximum expiration time](/user-guide/programmatic-access-tokens#label-pat-maximum-expiration-time).

        `NETWORK_POLICY_EVALUATION = { ENFORCED_REQUIRED | ENFORCED_NOT_REQUIRED | NOT_ENFORCED }`
        :   Specifies how network policy requirements are handled for programmatic access tokens.

            By default, a user must be subject to a [network policy](/user-guide/network-policies) with one or more
            [network rules](/user-guide/network-rules) to generate or use programmatic access tokens:

            - Service users (with TYPE=SERVICE) must be subject to a network policy to generate and use programmatic access tokens.
            - Human users (with TYPE=PERSON) must be subject to a network policy to use programmatic access tokens.

            To override this behavior, set this property to one of the following values:

            `ENFORCED_REQUIRED` (default behavior)
            :   The user must be subject to a network policy to generate and use programmatic access tokens.

                If the user is subject to a network policy, the network policy is enforced during authentication.

            `ENFORCED_NOT_REQUIRED`
            :   The user does not need to be subject to a network policy to generate and use programmatic access tokens.

                If the user is subject to a network policy, the network policy is enforced during authentication.

            `NOT_ENFORCED`
            :   The user does not need to be subject to a network policy to generate and use programmatic access tokens.

                If the user is subject to a network policy, the network policy is not enforced during authentication.

        `REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS = { TRUE | FALSE }`
        :   If TRUE, when you generate a programmatic access token for a service user, you must restrict the use of that token to a
            specific role.

            If you set this parameter to FALSE, you can generate a programmatic access token for a service user without restricting that
            token to a specific role.

            Changing REQUIRE\_ROLE\_RESTRICTION\_FOR\_SERVICE\_USERS from FALSE back to TRUE invalidates any programmatic access tokens for
            service users that were generated without the role restriction.

            Default value: TRUE

        The following example of the PAT\_POLICY clause specifies the following policy:

        - By default, programmatic access tokens expire in 30 days.
        - Programmatic access tokens have a maximum expiration time of 365 days.
        - You can generate a programmatic access token for a user if the user is not subject to a network policy requirement. Any
          network policy that the user is subject to is still enforced.
        - When you generate a programmatic access token for a service user, you do not need to restrict to token to use a specific role.

        Copy code

        ```
        PAT_POLICY=(
          DEFAULT_EXPIRY_IN_DAYS=30
          MAX_EXPIRY_IN_DAYS=365
          NETWORK_POLICY_EVALUATION = ENFORCED_NOT_REQUIRED
          REQUIRE_ROLE_RESTRICTION_FOR_SERVICE_USERS = FALSE
        );
        ```

    `WORKLOAD_IDENTITY_POLICY = ( list_of_properties )`
    :   Specifies the policies for [workload identity federation](/user-guide/workload-identity-federation). Set this to a
        space-delimited list that contains one or more of the following properties and values:

        `ALLOWED_PROVIDERS = ( { ALL | AWS | AZURE | GCP | OIDC } [ , { AWS | AZURE | GCP | OIDC } ... ] )`
        :   Specifies the workload identity providers allowed by the authentication policy during workload identity authentication.
            If this parameter is omitted, all workload identity providers are allowed.

            `ALL`
            :   Users can authenticate with any supported and configured workload identity provider.

            `AWS`
            :   Users can authenticate with an AWS IAM role or user.

            `AZURE`
            :   Users can authenticate with an Azure Entra ID access token.

            `GCP`
            :   Users can authenticate with a Google-signed ID token.

            `OIDC`
            :   Users can authenticate with an ID token from a configured OIDC provider.

        `ALLOWED_AWS_ACCOUNTS = ( 'string_literal' [ , 'string_literal' , ... ] )`
        :   Specifies the list of AWS account IDs allowed by the authentication policy during workload identity authentication of type `AWS`.

            By default, when a Snowflake service user has a `WORKLOAD_IDENTITY` of type `AWS`, then the ARN can reference any AWS account.
            If this parameter is set, then only ARNs from the specified AWS account IDs are allowed to authenticate.

            Each element must be a 12-digit string representing the AWS account ID.

            For more information, see [View AWS account identifiers](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-identifiers.html).

        `ALLOWED_AZURE_ISSUERS = ( 'string_literal' [ , 'string_literal' , ... ] )`
        :   Specifies the list of Azure Entra ID issuers allowed by the authentication policy during workload identity authentication of type `AZURE`.

            By default, when a Snowflake service user has a `WORKLOAD_IDENTITY` of type `AZURE`, then the issuer can be any Entra ID tenant.
            If this parameter is set, then only Azure tokens from the specified issuers are allowed to authenticate.

            Each element must be a valid Authority URL with following format:

            - `https://login.microsoftonline.com/<tenantId>/v2.0`

        `ALLOWED_OIDC_ISSUERS = ( 'string_literal' [ , 'string_literal' , ... ] )`
        :   Specifies the list of OIDC issuers allowed by the authentication policy during workload identity authentication of type `OIDC`.

            By default, when a Snowflake service user has a `WORKLOAD_IDENTITY` of type `OIDC`, then the issuer can be any valid OIDC issuer.
            If this parameter is set, then only tokens from the specified OIDC issuers are allowed to authenticate.

            Each element must be a valid HTTPS URL that contains scheme, host, and optionally, port number and path components but no query or fragment
            components. The URL must not contain spaces, and it must not exceed 2048 characters in length.

        For example:

        Copy code

        ```
        WORKLOAD_IDENTITY_POLICY=(
          ALLOWED_PROVIDERS = (AWS, AZURE, GCP, OIDC)
          ALLOWED_AWS_ACCOUNTS = ('123456789012', '210987654321')
          ALLOWED_AZURE_ISSUERS = ('https://login.microsoftonline.com/8c7832f5-de56-4d9f-ba94-3b2c361abe6b/v2.0',
            'https://login.microsoftonline.com/9ebd1ec9-9a78-4429-8f53-5cf870a812d1/v2.0')
          ALLOWED_OIDC_ISSUERS = ('https://my.custom.oidc.issuer/', 'https://another.custom/oidc/issuer')
        );
        ```

    `COMMENT = 'string_literal'`
    :   Changes the comment for the authentication policy.

`UNSET ...`
:   Specifies the properties to unset for the authentication policy, which resets them to their defaults.

`UNSET DCM PROJECT`

> Detaches the authentication policy from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the authentication policy and the DCM project without dropping the authentication policy. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Authentication policy | Only the SECURITYADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If you want to update an existing authentication policy and need to see the definition of the policy, run the
  [DESCRIBE AUTHENTICATION POLICY](/sql-reference/sql/desc-authentication-policy) command or [GET\_DDL](/sql-reference/functions/get_ddl) function.

## Examples

Alter the list of allowed clients on an authentication policy:

Copy code

```
ALTER AUTHENTICATION POLICY restrict_client_types_policy
  SET CLIENT_TYPES = ('SNOWFLAKE_UI', 'SNOWSQL');
```
