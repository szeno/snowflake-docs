# CREATE USER

Creates a new user or replaces an existing user in the system. For more details, see [User management](/user-guide/admin-user-management).

Note

Only user administrators (that is, users with the USERADMIN role or higher), or another role with the CREATE USER privilege on the account,
can create users.

See also:
:   [DROP USER](/sql-reference/sql/drop-user) , [ALTER USER](/sql-reference/sql/alter-user) , [DESCRIBE USER](/sql-reference/sql/desc-user) , [SHOW PARAMETERS](/sql-reference/sql/show-parameters)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] USER [ IF NOT EXISTS ] <name>
  [ objectProperties ]
  [ objectParams ]
  [ sessionParams ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

Where:

> Copy code
>
> ```
> objectProperties ::=
>   PASSWORD = '<string>'
>   LOGIN_NAME = <string>
>   DISPLAY_NAME = <string>
>   FIRST_NAME = <string>
>   MIDDLE_NAME = <string>
>   LAST_NAME = <string>
>   EMAIL = <string>
>   MUST_CHANGE_PASSWORD = { TRUE | FALSE }
>   DISABLED = { TRUE | FALSE }
>   ALLOWED_INTERFACES = ( <list_of_interfaces> )
>   DAYS_TO_EXPIRY = <integer>
>   MINS_TO_UNLOCK = <integer>
>   DEFAULT_WAREHOUSE = <string>
>   DEFAULT_NAMESPACE = <string>
>   DEFAULT_ROLE = <string>
>   DEFAULT_SECONDARY_ROLES = { ( 'ALL' ) | () }
>   MINS_TO_BYPASS_MFA = <integer>
>   RSA_PUBLIC_KEY = <string>
>   RSA_PUBLIC_KEY_FP = <string>
>   RSA_PUBLIC_KEY_2 = <string>
>   RSA_PUBLIC_KEY_2_FP = <string>
>   TYPE = { PERSON | SERVICE | SERVICE_AGENT | LEGACY_SERVICE }
>   WORKLOAD_IDENTITY = ( <list_of_properties> )
>   COMMENT = '<string_literal>'
> ```
>
> Copy code
>
> ```
> objectParams ::=
>   ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR = TRUE | FALSE
>   ENABLE_UNREDACTED_SECURE_OBJECT_ERROR = TRUE | FALSE
>   NETWORK_POLICY = <string>
> ```
>
> Copy code
>
> ```
> sessionParams ::=
>   ABORT_DETACHED_QUERY = TRUE | FALSE
>   AUTOCOMMIT = TRUE | FALSE
>   BINARY_INPUT_FORMAT = <string>
>   BINARY_OUTPUT_FORMAT = <string>
>   DATE_INPUT_FORMAT = <string>
>   DATE_OUTPUT_FORMAT = <string>
>   DEFAULT_NULL_ORDERING = <string>
>   ENABLE_GET_DDL_USE_DATA_TYPE_ALIAS = TRUE | FALSE
>   ERROR_ON_NONDETERMINISTIC_MERGE = TRUE | FALSE
>   ERROR_ON_NONDETERMINISTIC_UPDATE = TRUE | FALSE
>   JSON_INDENT = <num>
>   LOCK_TIMEOUT = <num>
>   OPT_OUT_ERROR_LOGGING = TRUE | FALSE
>   QUERY_TAG = <string>
>   ROWS_PER_RESULTSET = <num>
>   SIMULATED_DATA_SHARING_CONSUMER = <string>
>   STATEMENT_TIMEOUT_IN_SECONDS = <num>
>   STRICT_JSON_OUTPUT = TRUE | FALSE
>   TIMESTAMP_DAY_IS_ALWAYS_24H = TRUE | FALSE
>   TIMESTAMP_INPUT_FORMAT = <string>
>   TIMESTAMP_LTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_NTZ_OUTPUT_FORMAT = <string>
>   TIMESTAMP_OUTPUT_FORMAT = <string>
>   TIMESTAMP_TYPE_MAPPING = <string>
>   TIMESTAMP_TZ_OUTPUT_FORMAT = <string>
>   TIMEZONE = <string>
>   TIME_INPUT_FORMAT = <string>
>   TIME_OUTPUT_FORMAT = <string>
>   TRANSACTION_DEFAULT_ISOLATION_LEVEL = <string>
>   TWO_DIGIT_CENTURY_START = <num>
>   UNSUPPORTED_DDL_ACTION = <string>
>   USE_CACHED_RESULT = TRUE | FALSE
>   WEEK_OF_YEAR_POLICY = <num>
>   WEEK_START = <num>
> ```

Note

For readability, the complete list of session parameters that can be set for a user is not included here. For a complete list of all
session parameters, with their descriptions, as well as account and object parameters, see [Parameters](/sql-reference/parameters).

## Required parameters

`name`
:   Identifier for the user; must be unique for your account.

    The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

Note

The user does not use this value to log into Snowflake; instead, the user uses the value specified for the `LOGIN_NAME`
property to log in. However, if no login name is explicitly specified for the user, the user name/identifier serves as the default
login name.

## Optional object properties (`objectProperties`)

`PASSWORD = 'string'`
:   The password for the user must be enclosed in single or double quotes. If no password is specified, the user cannot log into Snowflake
    until a password has been explicitly specified for them.

    If the password uses the backslash (i.e. `\`) character, escape the character with a backslash or use double dollar sign (i.e. `$$`)
    delimiters when specifying the password in a SQL command. For details, refer to [String & binary data types](/sql-reference/data-types-text).

    For more information about passwords in Snowflake, refer to [Password policies](/user-guide/password-authentication#label-password-policies).

    Default: `NULL`

`LOGIN_NAME = string`
:   Name that the user enters to log into the system. Login names for users must be unique across your entire account.

    A login name can be any string, including spaces and non-alphanumeric characters, such as exclamation points (`!`), percent signs
    (`%`), and asterisks (`*`); however, if the string contains spaces or non-alphanumeric characters, it must be enclosed in single
    or double quotes. Login names are always case-insensitive.

    Snowflake allows specifying different user and login names to enable using common identifiers (e.g. email addresses) for login.

    Default: User’s name/identifier (i.e. if no value is specified, the value specified for `name` is used as the login name)

`DISPLAY_NAME = string`
:   Name displayed for the user in the Snowflake web interface.

    Default: User’s name/identifier (i.e. if no value is specified, the value specified for `name` is used as the display name)

`FIRST_NAME = string` , `MIDDLE_NAME = string` , `LAST_NAME = string`
:   First, middle, and last name of the user.

    Default: `NULL`

`EMAIL = string`
:   Email address for the user.

    An email address is not required to use Snowflake; however, to access the Snowflake Community to open support tickets or contribute to
    the community forums, a valid email address must be specified for the user.

    We recommend specifying a business email address rather than a personal email address. User email addresses are visible to all other
    users in your Snowflake account.

    Default: `NULL`

`MUST_CHANGE_PASSWORD = TRUE | FALSE`
:   Specifies whether the user is forced to change their password on next login (including their first/initial login) into the system.

    Default: `FALSE`

`DISABLED = TRUE | FALSE`
:   Specifies whether the user is disabled, which prevents the following actions:

    - For a new user, the user is locked out of Snowflake and cannot log in.
    - For an existing user, setting the property aborts all their currently-running queries and does not allow the user to issue any new
      queries; the user is also immediately locked out of Snowflake and cannot log back in.

    Default: `FALSE`

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

    Default: `('ALL')`

`DAYS_TO_EXPIRY = integer`
:   Specifies the number of days after which the user status is set to “Expired” and the user is no longer allowed to log in. This is useful
    for defining temporary users (that is, users who should only have access to Snowflake for a limited time period).

    Setting `DAYS_TO_EXPIRY` for [account administrators](/user-guide/security-access-control-considerations#label-accountadmin-users) (that is, users with the ACCOUNTADMIN role) is not
    allowed. If you set `DAYS_TO_EXPIRY` for [account administrators](/user-guide/security-access-control-considerations#label-accountadmin-users), Snowflake ignores the setting.

    Once set, the value counts down to `0`, but doesn’t stop. A negative value indicates the status for the user is “Expired”. To reset
    the value, use [ALTER USER](/sql-reference/sql/alter-user) to set the following values:

    - To re-enable the user as a temporary user, set the value to a value greater than `0`.
    - To specify the user as a permanent user, set the value to `NULL` or `0`.

    Default: `NULL`

`MINS_TO_UNLOCK = integer`
:   Specifies the number of minutes until the temporary lock on the user login is cleared. To protect against unauthorized user login,
    Snowflake places a temporary lock on a user after five consecutive unsuccessful login attempts:

    - A positive value indicates the status for the user is “Locked”.
    - Once the value counts down to `0` (or a negative value), the lock is cleared and the user is allowed to log in again.
    - When the user successfully logs into Snowflake, the value resets to `NULL`.

    When creating a user, this property can be set to prevent them from logging in until the specified amount of time passes.

    To remove a lock immediately for a user, use [ALTER USER](/sql-reference/sql/alter-user) and specify a value of `0` for this parameter.

    Default: `NULL`

`DEFAULT_WAREHOUSE = string`
:   Specifies the virtual warehouse that is active by default for the user’s session upon login.

    A user can specify or change their current default virtual warehouse using [ALTER USER](/sql-reference/sql/alter-user). In addition, after starting a session
    (i.e. logging in), a user can change the virtual warehouse for the session using [USE WAREHOUSE](/sql-reference/sql/use-warehouse).

    Note that the CREATE USER operation does not verify that the warehouse exists.

    Default: `NULL`

`DEFAULT_NAMESPACE = string`
:   Specifies the namespace (database only or database and schema) that is active by default for the user’s session upon login:

    - To specify a database only, enter the database name.
    - To specify a schema, enter the fully-qualified schema name in the form of `db_name.schema_name`.

    A user can specify or change their current default namespace using [ALTER USER](/sql-reference/sql/alter-user). In addition, after starting a session
    (i.e. logging in), a user can change the namespace for their session using [USE DATABASE](/sql-reference/sql/use-database) or [USE SCHEMA](/sql-reference/sql/use-schema).

    Note that the CREATE USER operation does not verify that the namespace exists.

    Default: `NULL`

`DEFAULT_ROLE = string`
:   Specifies the primary role that is active by default for the user’s session upon login. The primary role is a single role that
    authorizes the execution of [CREATE <object>](/sql-reference/sql/create) statements or any other SQL action. The permissions to perform these
    actions can be granted to the primary role or any lower role in the role hierarchy.

    Note that specifying a default role for a user does not grant the role to the user. The role must be granted explicitly to the
    user using the [GRANT ROLE](/sql-reference/sql/grant-role) command. In addition, the CREATE USER operation does not verify that the role exists.

    A user can specify or change their current default role using [ALTER USER](/sql-reference/sql/alter-user). In addition, after starting a session (i.e. logging in),
    a user can change the role for the session using [USE ROLE](/sql-reference/sql/use-role). In either case, they can only choose from roles that have been
    explicitly granted to them.

    Default: `NULL`

`DEFAULT_SECONDARY_ROLES = ( 'ALL' ) | ()`
:   Specifies the set of secondary roles that are active for the user’s session upon login. Secondary roles are a set of roles that authorize
    any SQL action other than the execution of CREATE *<object>* statements. The permissions to perform these actions can be granted
    to the primary role, secondary roles, or any lower roles in the role hierarchies.

    Note that specifying a default secondary role for a user does not grant the role to the user. The role must also be granted
    explicitly to the user using the GRANT ROLE command.

    The following values are supported:

    > `('ALL')`
    > :   All roles that have been granted to the user.
    >
    >     Note that the set of roles is reevaluated when each SQL statement executes. If additional roles are granted to the user, and that
    >     user executes a new SQL statement, the newly granted roles are active secondary roles for the new SQL statement. The same logic
    >     applies to roles that are revoked from a user.
    >
    > `()`
    > :   No roles.

    Default: `ALL`

`MINS_TO_BYPASS_MFA = integer`
:   Specifies the number of minutes to temporarily bypass MFA for the user.

    This property can be used to allow a MFA-enrolled user to temporarily bypass MFA during login in the event that their MFA device is
    not available.

`RSA_PUBLIC_KEY = string`
:   Specifies the user’s RSA public key; used for [key pair authentication](/user-guide/key-pair-auth).

`RSA_PUBLIC_KEY_FP = string`
:   Specifies the fingerprint of the user’s RSA public key; used for [key pair authentication](/user-guide/key-pair-auth).

`RSA_PUBLIC_KEY_2 = string`
:   Specifies the user’s second RSA public key; used to rotate the public and private keys for
    [key pair authentication](/user-guide/key-pair-auth) based on an expiration schedule set by your organization.

`RSA_PUBLIC_KEY_2_FP = string`
:   Specifies the fingerprint of the user’s second RSA public key; used to rotate the public and private keys for
    [key pair authentication](/user-guide/key-pair-auth) based on an expiration schedule set by your organization.

`TYPE = { PERSON | SERVICE | SERVICE_AGENT | LEGACY_SERVICE }`
:   Specifies the type of user. You can set this property to differentiate between human, service, service agent, and legacy service users. For
    information about the characteristics of these types of users, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

    `PERSON`
    :   User is a human user who can interact with Snowflake.

    `SERVICE`
    :   User is a service or application that interacts with Snowflake without human intervention.

    `SERVICE_AGENT`
    :   User is an automated AI agent that interacts with Snowflake using its own identity and privileges. Every session opened by
        a `SERVICE_AGENT` user is automatically agent-active.

    `LEGACY_SERVICE`
    :   A user with their `TYPE` property set to `LEGACY_SERVICE` represents a non-interactive integration. It is similar to
        `SERVICE`, but allows password and SAML authentication.

        Note

        The LEGACY\_SERVICE type is being deprecated. Use the SERVICE type for services and applications. For a timeline of the deprecation of
        LEGACY\_SERVICE, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

    Default: `PERSON`

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

`COMMENT = 'string_literal'`
:   Specifies a comment for the user.

    Default: `NULL`

## Optional object parameters (`objectParams`)

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
:   Specifies an existing [network policy](/user-guide/network-policies) is active for the user. The network policy restricts the
    list of user IP addresses when exchanging an authorization code for an access or refresh token and when using a refresh token to
    obtain a new access token.

    If this parameter is not set, the network policy for the account (if any) is used instead.

## Optional session parameters (`sessionParams`)

Specifies one (or more) session parameter defaults to set for the user (separated by blank spaces, commas, or new lines). These defaults
are set each time the user logs into Snowflake and initiates session. The user can always change these defaults themselves within the
session using [ALTER SESSION](/sql-reference/sql/alter-session).

For the complete list of session parameters, including their default values, that can be specified for a user, see
[Parameters](/sql-reference/parameters).

## Optional parameters

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE USER | Account | Only the USERADMIN role, or a higher role, has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The `TYPE` property of a new user object can’t be `NULL`. You can’t set the `TYPE` property of an existing user to `NULL`.
  Running a CREATE USER command without setting the `TYPE` property sets the `TYPE` property for that user to `PERSON`.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a user with all default properties, a default role, and a basic password that must be changed by the user after their first
login:

> Copy code
>
> ```
> CREATE USER user1 PASSWORD='abc123' DEFAULT_ROLE = myrole DEFAULT_SECONDARY_ROLES = ('ALL') MUST_CHANGE_PASSWORD = TRUE;
> ```
