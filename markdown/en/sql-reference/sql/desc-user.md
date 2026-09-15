# DESCRIBE USER

Describes a [user](/user-guide/admin-user-management), including the current and default values of the properties of the
user.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP USER](/sql-reference/sql/drop-user) , [ALTER USER](/sql-reference/sql/alter-user) , [CREATE USER](/sql-reference/sql/create-user) , [SHOW USERS](/sql-reference/sql/show-users)

## Syntax

Copy code

```
{ DESC | DESCRIBE } USER <name>
```

## Parameters

`name`
:   Specifies the identifier for the user to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `property` | The name of the property (see [Properties of users](/sql-reference/sql/desc-user#label-desc-user-properties)). |
| `property_type` | The data type of the property (for example, `Boolean` or `String`). |
| `property_value` | The value assigned to the property. |
| `property_default` | The default value of the property. |

Expand

Show lessSee more

The `property` column can include the following properties of the user:

**Properties of users**

| Property | Description |
| --- | --- |
| `NAME` | Name of the user. |
| `COMMENT` | Comment about the user. |
| `DISPLAY_NAME` | Name displayed for the user in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). |
| `TYPE` | Type of the user. For a list of possible values, see [Types of users](/user-guide/admin-user-management#label-user-management-types). |
| `LOGIN_NAME` | Name that the user enters to log into the system. |
| `FIRST_NAME` | First name of the user. |
| `MIDDLE_NAME` | Middle name of the user. |
| `LAST_NAME` | Last name of the user. |
| `EMAIL` | Email address for the user. |
| `PASSWORD` | Obfuscated password of the user. |
| `MUST_CHANGE_PASSWORD` | If TRUE, the user is forced to change their password on next login (including their first/initial login) into the system. |
| `DISABLED` | If TRUE, the user is [locked out of Snowflake and cannot log back in](/user-guide/admin-user-management#label-user-management-disable-enable-user). |
| `SNOWFLAKE_LOCK` | If TRUE, the user is locked by Snowflake. When a user is locked, they are unable to log in until the lock is removed. |
| `SNOWFLAKE_SUPPORT` | If TRUE, Snowflake Support is allowed to use the user or account. |
| `DAYS_TO_EXPIRY` | Number of days after which the user status is set to “Expired” and the user is no longer allowed to log in. |
| `MINS_TO_UNLOCK` | Number of minutes until [the temporary lock on the user login is cleared](/user-guide/admin-user-management#label-user-management-unlock). |
| `DEFAULT_WAREHOUSE` | Virtual warehouse that is active by default for the user’s session upon logging in. |
| `DEFAULT_NAMESPACE` | Namespace (database only or database and schema) that is active by default for the user’s session upon logging in. |
| `DEFAULT_ROLE` | Primary role that is active by default for the user’s session upon logging in. |
| `DEFAULT_SECONDARY_ROLES` | Set of secondary roles that are active for the user’s session upon logging in. |
| `EXT_AUTHN_DUO` | If TRUE, [Duo](/user-guide/security-mfa-duo) is enabled for the user, which requires the user to use [MFA (multi-factor authentication)](/user-guide/security-mfa) when logging in. |
| `EXT_AUTHN_UID` | Authorization ID used for Duo. |
| `DEFAULT_MFA_METHOD` | [Default MFA method](/user-guide/security-mfa-second-factor#label-mfa-secondary-methods-default) for the user. |
| `HAS_MFA` | If TRUE, the user is enrolled in [multi-factor authentication (MFA)](/user-guide/security-mfa). |
| `HAS_PAT` | If TRUE, the user has one or more [programmatic access tokens](/user-guide/programmatic-access-tokens). |
| `HAS_WORKLOAD_IDENTITY` | If TRUE, the user is configured to authenticate with [workload identity federation](/user-guide/workload-identity-federation). |
| `MINS_TO_BYPASS_MFA` | Number of minutes to [temporarily bypass MFA requirement for the user](/user-guide/security-mfa#label-mfa-temp-disable). |
| `MINS_TO_BYPASS_NETWORK_POLICY` | Number of minutes to [temporarily bypass the requirement of having a network policy for programmatic access tokens](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network). |
| `RSA_PUBLIC_KEY` | RSA public key of the user for [key-pair authentication](/user-guide/key-pair-auth). |
| `RSA_PUBLIC_KEY_FP` | Fingerprint of the user’s RSA public key. |
| `RSA_PUBLIC_KEY_LAST_SET_TIME` | Date and time when the RSA public key was last set for the user. |
| `RSA_PUBLIC_KEY_2` | Second RSA public key of the user for use during [key-pair rotation](/user-guide/key-pair-auth#label-key-pair-rotation). |
| `RSA_PUBLIC_KEY_2_FP` | Fingerprint of the user’s second RSA public key. |
| `RSA_PUBLIC_KEY_2_LAST_SET_TIME` | Date and time when the second RSA public key was last set for the user. |
| `PASSWORD_LAST_SET_TIME` | Date and time when the last non-NULL password was set for the user. If no password was set, the value of this property is NULL. |
| `CUSTOM_LANDING_PAGE_URL` | Reserved for future use. |
| `CUSTOM_LANDING_PAGE_URL_FLUSH_NEXT_UI_LOAD` | Reserved for future use. |
| `IS_FROM_ORGANIZATION_USER` | If TRUE, the user was imported from a global [organization user](/user-guide/organization-users). |

Expand

Show lessSee more

## Access control requirements

Individual users can see their own properties by executing this command and specifying their own `name`.

To view the properties of another user, you must use a role that has the following privilege:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | User |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The user object property `MINS_TO_BYPASS_NETWORK_POLICY` defines the number of minutes in which a user can access Snowflake
  without conforming to an existing [network policy](/user-guide/network-policies). The number of minutes can only be set by
  Snowflake (Default: `NULL`) and is intended as a temporary workaround to allow user access to Snowflake. To set a value for
  this property, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- This command does not show the session parameter defaults for a user. Instead, use [SHOW PARAMETERS IN USER](/sql-reference/sql/show-parameters).
- The user object property `PASSWORD_LAST_SET_TIME` defaults to `Null` if no password has been set yet. Values of
  `292278994-08-17 07:12:55.807` or `1969-12-31 23:59:59.999` indicate the password was set before the inclusion of this row.
  A value of `1969-12-31 23:59:59.999` can also indicate an expired password and the user needs to change their password.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

The following example describes the user named `my_user`:

Copy code

```
DESCRIBE USER my_user;
```

```
+--------------------------------------------+-------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
| property                                   | value                   | default | description                                                                                                                                |
|--------------------------------------------+-------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------|
| NAME                                       | JSMITH                  | null    | Name                                                                                                                                       |
| COMMENT                                    | null                    | null    | user comment associated to an object in the dictionary                                                                                     |
| DISPLAY_NAME                               | Jane Smith              | null    | Display name of the associated object                                                                                                      |
| TYPE                                       | PERSON                  | null    | Type of the account, application package, data exchange, data exchange listing, replication group, secret, network rule, or user.          |
| LOGIN_NAME                                 | JSMITH                  | null    | Login name of the user                                                                                                                     |
| FIRST_NAME                                 | Jane                    | null    | First name of the user                                                                                                                     |
| MIDDLE_NAME                                | null                    | null    | Middle name of the user                                                                                                                    |
| LAST_NAME                                  | Smith                   | null    | Last name of the user                                                                                                                      |
| EMAIL                                      | jane.smith@example.com  | null    | Email address of the user                                                                                                                  |
| PASSWORD                                   | ********                | null    | Password of the user                                                                                                                       |
| MUST_CHANGE_PASSWORD                       | false                   | false   | User must change the password                                                                                                              |
| DISABLED                                   | false                   | false   | Whether the entity is disabled                                                                                                             |
| SNOWFLAKE_LOCK                             | false                   | false   | Whether the user, account, or organization is locked by Snowflake                                                                          |
| SNOWFLAKE_SUPPORT                          | false                   | false   | Snowflake Support is allowed to use the user or account                                                                                    |
| DAYS_TO_EXPIRY                             | null                    | null    | User record will be treated as expired after specified number of days                                                                      |
| MINS_TO_UNLOCK                             | null                    | null    | Temporary lock on the user will be removed after specified number of minutes                                                               |
| DEFAULT_WAREHOUSE                          | MY_WAREHOUSE            | null    | Default warehouse for this user                                                                                                            |
| DEFAULT_NAMESPACE                          | MY_DB.MY_SCHEMA         | null    | Default database namespace prefix for this user                                                                                            |
| DEFAULT_ROLE                               | MY_ROLE                 | null    | Primary principal of user session will be set to this role                                                                                 |
| DEFAULT_SECONDARY_ROLES                    | []                      | [ALL]   | The secondary roles will be set to all roles provided here.                                                                                |
| EXT_AUTHN_DUO                              | false                   | false   | Whether Duo Security is enabled as second factor authentication                                                                            |
| EXT_AUTHN_UID                              | null                    | null    | External authentication ID of the user                                                                                                     |
| DEFAULT_MFA_METHOD                         | null                    | null    | Default MFA method for the user                                                                                                            |
| HAS_MFA                                    | true                    | false   | Whether the user is enrolled in multi-factor authentication                                                                                |
| HAS_PAT                                    | true                    | false   | Whether the user has a programmatic access token                                                                                           |
| HAS_FEDERATED_WORKLOAD_AUTHENTICATION      | false                   | false   | Reserved for future use                                                                                                                    |
| MINS_TO_BYPASS_MFA                         | null                    | null    | Temporary bypass MFA for the user for a specified number of minutes                                                                        |
| MINS_TO_BYPASS_NETWORK_POLICY              | null                    | null    | Temporary bypass network policy on the user for a specified number of minutes                                                              |
| RSA_PUBLIC_KEY                             | ...                     | null    | RSA public key of the user                                                                                                                 |
| RSA_PUBLIC_KEY_FP                          | SHA256:...=             | null    | Fingerprint of user's RSA public key.                                                                                                      |
| RSA_PUBLIC_KEY_LAST_SET_TIME               | null                    | null    | The timestamp at which the RSA public key was last set for the user. Defaults to null if no RSA public key has been set yet.               |
| RSA_PUBLIC_KEY_2                           | ...                     | null    | Second RSA public key of the user                                                                                                          |
| RSA_PUBLIC_KEY_2_FP                        | SHA256:...=             | null    | Fingerprint of user's second RSA public key.                                                                                               |
| RSA_PUBLIC_KEY_2_LAST_SET_TIME             | null                    | null    | The timestamp at which the second RSA public key was last set for the user. Defaults to null if no second RSA public key has been set yet. |
| PASSWORD_LAST_SET_TIME                     | 2020-10-08 01:33:13.43  | null    | The timestamp on which the last non-null password was set for the user. Default to null if no password has been set yet.                   |
| CUSTOM_LANDING_PAGE_URL                    | null                    | null    | Reserved for future use                                                                                                                    |
| CUSTOM_LANDING_PAGE_URL_FLUSH_NEXT_UI_LOAD | false                   | false   | Reserved for future use                                                                                                                    |
+--------------------------------------------+-------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------+
```
