# ALTER USER

Modifies the properties and object/session parameters for an existing user in the system:

- Administrators can use this command to alter properties and parameter defaults for any users for which the administrators have the
  appropriate privileges.
- Individual users can use this command to alter specific properties and any session parameter defaults for themselves. For more details, see
  [Usage Notes](#usage-notes) (in this topic).

Can also be used to abort all queries (and other SQL statements) submitted by the user.

See also:
:   [CREATE USER](/sql-reference/sql/create-user), [DROP USER](/sql-reference/sql/drop-user), [SHOW PARAMETERS](/sql-reference/sql/show-parameters), [SHOW USERS](/sql-reference/sql/show-users), [DESCRIBE USER](/sql-reference/sql/desc-user)

## Syntax

Copy code

```
ALTER USER [ IF EXISTS ] [ <name> ] RENAME TO <new_name>

ALTER USER [ IF EXISTS ] [ <name> ] RESET PASSWORD

ALTER USER [ IF EXISTS ] [ <name> ] ABORT ALL QUERIES

ALTER USER [ IF EXISTS ] [ <name> ] ADD DELEGATED AUTHORIZATION OF ROLE <role_name> TO SECURITY INTEGRATION <integration_name>

ALTER USER [ IF EXISTS ] [ <name> ] REMOVE DELEGATED { AUTHORIZATION OF ROLE <role_name> | AUTHORIZATIONS } FROM SECURITY INTEGRATION <integration_name>

ALTER USER [ IF EXISTS ] [ <name> ] REMOVE DELEGATED AUTHORIZATIONS OF ANY ROLE FROM SECURITY INTEGRATION <integration_name>

ALTER USER [ IF EXISTS ] [ <name> ] mfaActions

ALTER USER [ IF EXISTS ] [ <name> ] SET { AUTHENTICATION | PASSWORD | SESSION } POLICY <policy_name> [ FORCE ]

ALTER USER [ IF EXISTS ] [ <name> ] UNSET { AUTHENTICATION | PASSWORD | SESSION } POLICY

ALTER USER [ IF EXISTS ] [ <name> ] SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER USER [ IF EXISTS ] [ <name> ] UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER USER [ IF EXISTS ] [ <name> ] SET { [ objectProperties ] [ objectParams ] [ sessionParams ] }

ALTER USER [ IF EXISTS ] [ <name> ] UNSET { <object_property_name> | <object_param_name> | <session_param_name> } [ , ... ]
```

Where:

> Copy code
>
> ```
> mfaActions ::=
>   {
>     ENROLL MFA
>     SET DEFAULT_MFA_METHOD = { PASSKEY | TOTP | DUO }
>     REMOVE MFA METHOD <mfa_method>
>     MODIFY MFA METHOD <mfa_method> SET COMMENT = '<string>'
>     ADD MFA METHOD OTP [ COUNT = <number> ]
>   }
> ```
>
> Copy code
>
> ```
> objectProperties ::=
>     PASSWORD = '<string>'
>     LOGIN_NAME = <string>
>     DISPLAY_NAME = <string>
>     FIRST_NAME = <string>
>     MIDDLE_NAME = <string>
>     LAST_NAME = <string>
>     EMAIL = <string>
>     MUST_CHANGE_PASSWORD = TRUE | FALSE
>     DISABLED = TRUE | FALSE
>     ALLOWED_INTERFACES = ( <list_of_interfaces> )
>     DAYS_TO_EXPIRY = <integer>
>     MINS_TO_UNLOCK = <integer>
>     DEFAULT_WAREHOUSE = <string>
>     DEFAULT_NAMESPACE = <string>
>     DEFAULT_ROLE = <string>
>     DEFAULT_SECONDARY_ROLES = ( 'ALL' )
>     MINS_TO_BYPASS_MFA = <integer>
>     DISABLE_MFA = TRUE | FALSE
>     RSA_PUBLIC_KEY = <string>
>     RSA_PUBLIC_KEY_FP = <string>
>     RSA_PUBLIC_KEY_2 = <string>
>     RSA_PUBLIC_KEY_2_FP = <string>
>     TYPE = PERSON | SERVICE | SERVICE_AGENT | LEGACY_SERVICE
>     WORKLOAD_IDENTITY = ( <list_of_properties> )
>     COMMENT = '<string>'
> ```
>
> Copy code
>
> ```
> objectParams ::=
>     ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR = TRUE | FALSE
>     ENABLE_UNREDACTED_SECURE_OBJECT_ERROR = TRUE | FALSE
>     NETWORK_POLICY = <string>
>     PREVENT_UNLOAD_TO_INLINE_URL = TRUE | FALSE
>     PREVENT_UNLOAD_TO_INTERNAL_STAGES = TRUE | FALSE
> ```
>
> Copy code
>
> ```
> sessionParams ::=
>     ABORT_DETACHED_QUERY = TRUE | FALSE
>     AUTOCOMMIT = TRUE | FALSE
>     BINARY_INPUT_FORMAT = <string>
>     BINARY_OUTPUT_FORMAT = <string>
>     DATE_INPUT_FORMAT = <string>
>     DATE_OUTPUT_FORMAT = <string>
>     DEFAULT_NULL_ORDERING = <string>
>     ENABLE_GET_DDL_USE_DATA_TYPE_ALIAS = TRUE | FALSE
>     ENABLE_NOTEBOOK_CREATION_IN_PERSONAL_DB = TRUE | FALSE
>     ERROR_ON_NONDETERMINISTIC_MERGE = TRUE | FALSE
>     ERROR_ON_NONDETERMINISTIC_UPDATE = TRUE | FALSE
>     JSON_INDENT = <num>
>     LOCK_TIMEOUT = <num>
>     OPT_OUT_ERROR_LOGGING = TRUE | FALSE
>     QUERY_TAG = <string>
>     ROWS_PER_RESULTSET = <num>
>     S3_STAGE_VPCE_DNS_NAME = <string>
>     SEARCH_PATH = <string>
>     SIMULATED_DATA_SHARING_CONSUMER = <string>
>     STATEMENT_TIMEOUT_IN_SECONDS = <num>
>     STRICT_JSON_OUTPUT = TRUE | FALSE
>     TIMESTAMP_DAY_IS_ALWAYS_24H = TRUE | FALSE
>     TIMESTAMP_INPUT_FORMAT = <string>
>     TIMESTAMP_LTZ_OUTPUT_FORMAT = <string>
>     TIMESTAMP_NTZ_OUTPUT_FORMAT = <string>
>     TIMESTAMP_OUTPUT_FORMAT = <string>
>     TIMESTAMP_TYPE_MAPPING = <string>
>     TIMESTAMP_TZ_OUTPUT_FORMAT = <string>
>     TIMEZONE = <string>
>     TIME_INPUT_FORMAT = <string>
>     TIME_OUTPUT_FORMAT = <string>
>     TRANSACTION_DEFAULT_ISOLATION_LEVEL = <string>
>     TWO_DIGIT_CENTURY_START = <num>
>     UNSUPPORTED_DDL_ACTION = <string>
>     USE_CACHED_RESULT = TRUE | FALSE
>     WEEK_OF_YEAR_POLICY = <num>
>     WEEK_START = <num>
> ```

Note

For readability, the complete list of session parameters that can be set for a user is not included here. For a complete list of all session
parameters, with their descriptions, as well as account and object parameters, see [Parameters](/sql-reference/parameters).

## Parameters

`name`
:   Specifies the identifier for the user to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    If the identifier is omitted, the statement modifies the active (i.e. logged in) user. The restrictions described in [Usage Notes](#usage-notes) (in
    this topic) apply.

`RENAME TO new_name`
:   Specifies the new identifier for the user; must be unique for your account.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RESET PASSWORD`
:   Generates a URL, which you can share with the user, that opens a web page from which the user can enter a new password. The generated URL is
    valid for a single use and expires after 12 hours.

    Note that specifying this parameter does not invalidate the user’s current password. The user can continue to use their current password
    until they reset it through the URL.

    If you wish to invalidate their current password, use `SET PASSWORD = 'string'` instead, which changes their password to a new value.

`ABORT ALL QUERIES`
:   Aborts all the queries and other SQL statements currently running or scheduled by the user, regardless of the warehouse on which the queries
    are running/scheduled.

    Note that the user can still log into Snowflake and initiate new queries.

    If you want to abort all running/scheduled queries and prevent the user from logging into Snowflake or initiating new queries, specify
    `SET DISABLED = TRUE` instead.

`ADD DELEGATED AUTHORIZATION OF ROLE role_name TO SECURITY INTEGRATION integration_name;`
:   Adds user consent to initiate a session using a specified role for a particular integration.

    For more details, see [Adding Delegated Authorizations for OAuth User Consent](/user-guide/oauth-consent#label-add-delegated-authorization).

`REMOVE DELEGATED AUTHORIZATION OF ROLE role_name FROM SECURITY INTEGRATION integration_name` , `REMOVE DELEGATED AUTHORIZATIONS FROM SECURITY INTEGRATION integration_name`
:   Revokes consent for the user:

    - The first syntax revokes consent for a specified security integration for a specified role. This has the effect of revoking any OAuth
      access token associated with the integration and specific role.
    - The second syntax revokes all consent from a specified security integration. This has the effect of revoking any OAuth access token
      associated with the integration.

    For more details, see:

    - [Configure Snowflake OAuth for partner applications](/user-guide/oauth-partner)
    - [Configure Snowflake OAuth for custom clients](/user-guide/oauth-custom)

`REMOVE DELEGATED AUTHORIZATIONS OF ANY ROLE FROM SECURITY INTEGRATION integration_name`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Revokes the user’s consent to switch roles (the `session:role-any` scope) for the specified Snowflake OAuth security integration,
    without affecting the user’s consent for specific roles. This revokes any OAuth access token that relies on the any-role consent for
    that integration.

    Applies only to Snowflake OAuth custom-client integrations configured with `OAUTH_ANY_ROLE_MODE`. For more information, see
    [Allowing clients to switch roles](/user-guide/oauth-custom#label-oauth-custom-role-switching).

`{ AUTHENTICATION | PASSWORD | SESSION } POLICY policy_name [ FORCE ]`
:   Specifies one of the following policies for the user:

    - [Authentication policy](/user-guide/authentication-policies)
    - [Password policy](/user-guide/password-authentication#label-password-policies)
    - [Session policy](/user-guide/session-policies)

    If you already set a policy on the user, then you can specify FORCE to set the new policy without needing to
    unset the existing policy first.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Object properties (`objectProperties`)

`SET property_name = property_value [ ... ]` , `UNSET property_name [ , ... ]`
:   Specifies one (or more) object properties to set or unset for the user. Unsetting an object property resets it back to the default.

    `TYPE = { PERSON | SERVICE | SERVICE_AGENT | LEGACY_SERVICE | NULL }`
    :   Alters the type of user. You can set this property to differentiate between human, service, service agent, and legacy service users. For
        information about the characteristics of these types of users, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

        `PERSON`
        :   A user who is a human user that interacts with Snowflake.

        `SERVICE`
        :   A user that is a service or application that interacts with Snowflake without human intervention.

            If a user has their `TYPE` property set to `SERVICE` using the ALTER USER command, then incompatible properties remain
            stored, but are not returned by commands such as DESCRIBE USER. The incompatible properties cannot be set using
            the ALTER USER command.

            If a user, with their `TYPE` property set to `SERVICE`, is changed to a user with their `TYPE` property set to
            `PERSON`, the incompatible properties are restored and can be changed, including their `PASSWORD` property.

        `SERVICE_AGENT`
        :   An automated AI agent that interacts with Snowflake using its own identity and privileges. Every session
            opened by a `SERVICE_AGENT` user is automatically agent-active.

            If a user has their `TYPE` property set to `SERVICE_AGENT` using the ALTER USER command, then incompatible properties remain stored, but
            are not returned by commands such as DESCRIBE USER. The incompatible properties cannot be set using the ALTER USER command.

            If a user, with their `TYPE` property set to `SERVICE_AGENT`, is changed to a user with their `TYPE` property set to `PERSON`, the
            incompatible properties are restored and can be changed, including their `PASSWORD` property.

        `LEGACY_SERVICE`
        :   A user with their `TYPE` property set to `LEGACY_SERVICE` represents a non-interactive integration. It is similar to
            `SERVICE`, but allows password and SAML authentication.

            Note

            The LEGACY\_SERVICE type is being deprecated. Use the SERVICE type for services and applications. For a timeline of the deprecation of
            LEGACY\_SERVICE, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

        `NULL`
        :   Functions the same as `PERSON`. You can’t set the `TYPE` property as `NULL` for an existing user.

    `ALLOWED_INTERFACES = ( { 'ALL' | 'interface' [ , ... ] } )`
    :   Specifies which Snowflake interfaces the user can access.

        If you specify `('ALL')`, the user can access Snowsight and all other interfaces that can be
        specified for this property. If you specify one or more interfaces, the user can only access the interfaces
        specified and can’t interact with any Snowflake data outside of the interfaces specified.

        For `interface`, you can specify one or more of the following values in a comma-delimited list:

        > `SNOWFLAKE_INTELLIGENCE`
        > :   The user can access [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork).
        >
        > `STREAMLIT`
        > :   The user can access Streamlit apps through the app-viewer URLs.

    `DISABLE_MFA = { TRUE | FALSE }`
    :   The effect of this parameter depends on whether the user voluntarily enrolled in MFA or was required to enroll.

        - If the user is subject to an authentication policy that requires them to use MFA, setting this parameter to TRUE clears the MFA
          methods for the user. The next time the user signs in, they are prompted to add a new MFA method that they can use as a second factor
          of authentication.
        - If the user voluntarily enrolled in MFA, setting this parameter to TRUE allows the user to authenticate without a second
          factor of authentication.

    `WORKLOAD_IDENTITY = ( list_of_properties )`
    :   Configures the user to authenticate by using [workload identity federation](/user-guide/workload-identity-federation). You can set this
        property on users with their `TYPE` property set to `SERVICE` or `SERVICE_AGENT`.

        The following list shows the properties:

        `TYPE = { AWS | AZURE | GCP | OIDC }`
        :   Specifies the provider that issues the attestation that is sent by the application or workload to Snowflake.

        `ARN = 'string'`
        :   Required for `TYPE=AWS`. Not valid for other types.

            Specifies the Amazon Resource Identifier (ARN) that uniquely identifies the AWS user or role that is associated with the instance
            authenticating to Snowflake. Snowflake accepts the following forms of [IAM identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html):

            - `arn:aws:iam::account:user/user_name_with_path`
            - `arn:aws:iam::account:role/role_name_with_path`
            - `arn:aws:sts::account:assumed_role/role_name/role_session_name`

            For help obtaining the ARN, see [Configure Snowflake](/user-guide/workload-identity-federation#label-wif-aws-authentication-snowflake).

        `ISSUER = 'string'`
        :   Required for `TYPE=AZURE` and `TYPE=OIDC`. Not valid for other types.

            - For `TYPE=AZURE`, specifies the Entra ID tenant’s Authority URL in the following form:

              `https://login.microsoftonline.com/tenant/v2.0`

              For help obtaining this URL, see [Configure Microsoft Azure](/user-guide/workload-identity-federation#label-wif-azure-configure-azure).
            - For `TYPE=OIDC`, specifies the OpenID Connect (OIDC) issuer URL. An OIDC provider is identified by its issuer URL.

              For examples of how to obtain this issuer URL for different OIDC providers, [Use cases](/user-guide/workload-identity-federation#label-wif-getting-started).

        `SUBJECT = 'string'`
        :   Required for `TYPE=AZURE`, `TYPE=GCP`, and `TYPE=OIDC`. Not valid for other types.

            - For `TYPE=AZURE`, specifies the case-sensitive Object ID (Principal ID) of the managed identity assigned to the Azure workload.
            - For `TYPE=GCP`, specifies the `uniqueId` property of the service account associated with the workload that is connecting to
              Snowflake.

              For help obtaining this identifier, see [Configure Snowflake](/user-guide/workload-identity-federation#label-wif-gcp-authentication-snowflake).
            - For `TYPE=OIDC`, specifies the identifier of the workload that is connecting to Snowflake. The format of the value is specific to the
              OIDC provider that is issuing the attestation.

              For examples of how to construct the subject of an attestation issued by an OIDC provider, see [Use cases](/user-guide/workload-identity-federation#label-wif-getting-started).

        `OIDC_AUDIENCE_LIST = ( 'string' [ , 'string' ... ] )`
        :   Optional for `TYPE=OIDC`. Not valid for other types.

            Specifies which values must be present in the `aud` claim of the ID token issued by the OIDC provider. Snowflake
            accepts the attestation if the `aud` claim contains at least one of the specified audiences.

            If omitted or empty, the audience is assumed to be `snowflakecomputing.com`.

For information about the other object properties you can set (for example, PASSWORD, LOGIN\_NAME, DEFAULT\_ROLE), see [CREATE USER](/sql-reference/sql/create-user).

Refer to [Usage Notes](#usage-notes) (in this topic) for more general details about setting and unsetting properties.

## Object parameters (`objectParams`)

`SET ...`
:   Specifies one (or more) parameters to set for the user (separated by blank spaces, commas, or new
    lines):

    `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR = { TRUE | FALSE }`
    :   Controls how queries that fail due to syntax or parsing errors show up in a query history. If FALSE, the contents of a
        failed query is redacted from the views, pages, and functions that provide a query history.

        This parameter controls behavior for the user viewing the query history, not the user who executed the query.

        Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE\_UNREDACTED\_QUERY\_SYNTAX\_ERROR parameter.

    `ENABLE_UNREDACTED_SECURE_OBJECT_ERROR = { TRUE | FALSE }`
    :   Controls whether error messages related to secure objects are redacted in metadata. For more information about
        error message redaction for secure objects, see [Secure objects: Redaction of information in error messages](/release-notes/bcr-bundles/un-bundled/bcr-1858).

        Only users with a role that is granted or inherits the AUDIT privilege can set the ENABLE\_UNREDACTED\_SECURE\_OBJECT\_ERROR parameter.

        When using the ALTER USER command to set the parameter to `TRUE` for a particular user, modify the user that you want to see the
        redacted error messages in metadata, not the user who caused the error.

    `NETWORK_POLICY = string`
    :   Specifies the [network policy](/user-guide/network-policies) that is active for the user.

Also, see [Usage Notes](#usage-notes) (in this topic) for more general details about setting and unsetting parameters.

`UNSET ...`
:   Specifies the properties to unset for the user, which resets them to the defaults.

    - `NETWORK_POLICY`
    - `AUTHENTICATION POLICY`
    - `PASSWORD POLICY`
    - `SESSION POLICY`
    - `TAG tag_name [ , tag_name ... ]`

## Session parameters (`sessionParams`)

`SET session_param_name = param_value [ ... ]` , `UNSET session_param_name [ , ... ]`
:   Specifies one (or more) session parameters to set or unset for the user. Unsetting a session parameter resets it back to the default.

For more details about the session parameters you can set (ABORT\_DETACHED\_QUERY, AUTOCOMMIT, and others), see [Parameters](/sql-reference/parameters).

Also, see [Usage Notes](#usage-notes) (in this topic) for more general details about setting and unsetting parameters.

## Multi-factor authentication (MFA) actions (mfaActions)

`user ENROLL MFA`
:   Enrolls the specified user in multi-factor authentication (MFA) and prompts them to add a second factor of authentication.

    - If the user has a verified email, Snowflake sends an email prompting them to add an MFA authentication method.
    - If the user does not have a verified email, Snowflake returns the URL of a page that prompts the user to add an MFA authentication method.

`SET DEFAULT_MFA_METHOD = { PASSKEY | TOTP | DUO }`
:   If the current user has more than one MFA method, specifies which one will be used as the second factor of authentication.

`user REMOVE MFA METHOD mfa_method`
:   Removes an MFA method that the specified user previously set up. The user can no longer use the MFA method as a second factor of
    authentication.

    To obtain the identifier for `mfa_method`, execute the [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods) command and find the value in
    the `name` column.

`[ user ] MODIFY MFA METHOD mfa_method SET COMMENT = 'string'`
:   Sets a descriptive name for the specified MFA method.

    To obtain the identifier for `mfa_method`, execute the [SHOW MFA METHODS](/sql-reference/sql/show-mfa-methods) command and find the value in
    the `name` column.

    Users can omit `user` to set a descriptive name for their own MFA methods.

`ADD MFA METHOD OTP [ COUNT = number ]`
:   Generates one-time passcodes (OTPs) that highly privileged users can use to authenticate when other authentication methods are unavailable.

    `COUNT` controls how many OTPs are generated. If omitted, one OTP is generated. The maximum is 10 OTPs.

    For more information, see [Setting up administrators for break glass access](/user-guide/security-mfa#label-mfa-breakglass).

## Usage notes

- Only the role with the OWNERSHIP privilege on the user, or a higher role, can execute this command to modify most user properties.

  Tip

  When changing a user’s password using `SET PASSWORD = 'string'`, we recommend also specifying `MUST_CHANGE_PASSWORD = TRUE`
  to force the user to log into the web interface and change their password before they can log into Snowflake through any other interface
  (e.g. SnowSQL or another client application).

  Alternatively, use `RESET PASSWORD` to generate a URL to a web page that the user can access to change their password.
- Only users with the ACCOUNTADMIN role can set the following parameters:

  - `PREVENT_UNLOAD_TO_INLINE_URL`
  - `PREVENT_UNLOAD_TO_INTERNAL_STAGES`
- Individual users can execute the ALTER USER command on themselves (i.e. by specifying their user name/identifier in the command) and change
  the following:

  - `DEFAULT_WAREHOUSE`
  - `DEFAULT_NAMESPACE`
  - `DEFAULT_ROLE`
  - Any of their session parameter defaults

  Note that users can not use this command to change their password. For security reasons, Snowflake only allows users to change
  their passwords from within the web interface.

  However, an administrator with the appropriate privileges can use this command with `SET PASSWORD = 'string'` to change the password
  for a user.

  Tip

  When changing a user’s password, we recommend also specifying `MUST_CHANGE_PASSWORD = TRUE` to force the user to log into the web
  interface and change their password before they can log into Snowflake through any other interface (e.g. SnowSQL or another client application).

  Alternatively, use `RESET PASSWORD` to generate a URL to a web page that the user can access to change their password.
- An ALTER USER statement does not verify that default objects (`DEFAULT_WAREHOUSE`, `DEFAULT_NAMESPACE`,
  and `DEFAULT_ROLE`) exist. Note that `DEFAULT_SECONDARY_ROLES` does not accept an object name as the value, but an ALTER
  USER statement does verify that a supported value is specified.
- You can set and unset multiple object properties and object/session parameters with a single ALTER statement:

  - When setting multiple properties/parameters, separate them with blank spaces, commas, or new lines.
  - When unsetting multiple properties/parameters, they must be separated by a comma. Also, when unsetting a property/parameter,
    specify only the name; specifying a value for the property/parameter will return an error.
- If there is a conflict between a local user object and an [organization user](/user-guide/organization-users), a user that
  corresponds to the organization user is automatically created when you rename the local user.
- If you specify `SET DISABLED = TRUE` for a user:

  - All queries and other SQL statements currently running or scheduled by the user are aborted and the user cannot initiate additional queries.
  - The user is locked out of Snowflake and cannot log in again.

  If you only want to abort all running and scheduled queries/statements for a user, use `ABORT ALL QUERIES` instead.
- If the user’s `TYPE` property is `SERVICE` or `SERVICE_AGENT`, the following commands cannot be used:

  - ALTER USER RESET PASSWORD
  - ALTER USER SET DISABLE\_MFA = TRUE
- If you run an ALTER USER … UNSET TYPE command, the `TYPE` property is set to `PERSON`.
- If you run an ALTER USER … SET TYPE=NULL command, the `TYPE` property is set to `PERSON`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename `user1` to `user2`:

> Copy code
>
> ```
> ALTER USER user1 RENAME TO user2;
> ```

Set the password for a user named `user1` to `H8MZRqa8gEe/kvHzvJ+Giq94DuCYoQXmfbb$Xnt` and require the user to change their password
by logging into the Snowflake web interface:

> Copy code
>
> ```
> ALTER USER user1 SET PASSWORD = 'H8MZRqa8gEe/kvHzvJ+Giq94DuCYoQXmfbb$Xnt' MUST_CHANGE_PASSWORD = TRUE;
> ```

Change the [type of user](/user-guide/admin-user-management#label-user-management-types) to an application that interacts with Snowflake programmatically:

> Copy code
>
> ```
> ALTER USER user1 SET TYPE = SERVICE;
> ```

Remove an existing comment from a user:

> Copy code
>
> ```
> ALTER USER user1 UNSET COMMENT;
> ```

Activate no secondary roles by default:

> Copy code
>
> ```
> ALTER USER user1 SET DEFAULT_SECONDARY_ROLES = ();
> ```

Activate all secondary roles by default:

> Copy code
>
> ```
> ALTER USER user1 UNSET DEFAULT_SECONDARY_ROLES;
> ```

OR

> Copy code
>
> ```
> ALTER USER user1 SET DEFAULT_SECONDARY_ROLES = ('ALL');
> ```
