# CREATE PASSWORD POLICY

Creates a new password policy or replaces an existing password policy.

After creating a password policy, apply the password policy to an account using an [ALTER ACCOUNT](/sql-reference/sql/alter-account) statement or
a user using an [ALTER USER](/sql-reference/sql/alter-user) statement.

See also:
:   [Using password policies](/user-guide/password-authentication#label-using-password-policies) , [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] PASSWORD POLICY [ IF NOT EXISTS ] <name>
  [ PASSWORD_MIN_LENGTH = <integer> ]
  [ PASSWORD_MAX_LENGTH = <integer> ]
  [ PASSWORD_MIN_UPPER_CASE_CHARS = <integer> ]
  [ PASSWORD_MIN_LOWER_CASE_CHARS = <integer> ]
  [ PASSWORD_MIN_NUMERIC_CHARS = <integer> ]
  [ PASSWORD_MIN_SPECIAL_CHARS = <integer> ]
  [ PASSWORD_MIN_AGE_DAYS = <integer> ]
  [ PASSWORD_MAX_AGE_DAYS = <integer> ]
  [ PASSWORD_MAX_RETRIES = <integer> ]
  [ PASSWORD_LOCKOUT_TIME_MINS = <integer> ]
  [ PASSWORD_HISTORY = <integer> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Identifier for the password policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`PASSWORD_MIN_LENGTH = integer`
:   Specifies the minimum number of characters the password must contain.

    Supported range: 8 to 256, inclusive.

    Default: 14

`PASSWORD_MAX_LENGTH = integer`
:   Specifies the maximum number of characters the password must contain. This number must be greater than or equal to the sum of
    `PASSWORD_MIN_LENGTH`, `PASSWORD_MIN_UPPER_CASE_CHARS`, and `PASSWORD_MIN_LOWER_CASE_CHARS`.

    Supported range: 8 to 256, inclusive.

    Default: 256

`PASSWORD_MIN_UPPER_CASE_CHARS = integer`
:   Specifies the minimum number of uppercase characters the password must contain.

    Supported range: 0 to 256, inclusive.

    Default: 1

`PASSWORD_MIN_LOWER_CASE_CHARS = integer`
:   Specifies the minimum number of lowercase characters the password must contain.

    Supported range: 0 to 256, inclusive.

    Default: 1

`PASSWORD_MIN_NUMERIC_CHARS = integer`
:   Specifies the minimum number of numeric characters the password must contain.

    Supported range: 0 to 256, inclusive.

    Default: 1

`PASSWORD_MIN_SPECIAL_CHARS = integer`
:   Specifies the minimum number of special characters the password must contain.

    Supported range: 0 to 256, inclusive.

    Default: 0

`PASSWORD_MIN_AGE_DAYS = integer`
:   Specifies the number of days the user must wait before a recently changed password can be changed again.

    Supported range: 0 to 999, inclusive.

    Default: 0

`PASSWORD_MAX_AGE_DAYS = integer`
:   Specifies the maximum number of days before the password must be changed.

    Supported range: 0 to 999, inclusive.

    A value of zero (i.e. `0`) indicates that the password does not need to be changed. Snowflake does not recommend choosing this
    value for a default account-level password policy or for any user-level policy. Instead, choose a value that meets your internal
    security guidelines.

    Default: 90, which means the password must be changed every 90 days.

    Important

    This parameter is stateful. For details, see the note in [Custom password policy for the account and users](/user-guide/password-authentication#label-custom-password-policies).

`PASSWORD_MAX_RETRIES = integer`
:   Specifies the maximum number of attempts to enter a password before being locked out.

    Supported range: 1 to 10, inclusive.

    Default: 5

    Important

    This parameter is stateful. For details, see the note in [Custom password policy for the account and users](/user-guide/password-authentication#label-custom-password-policies).

`PASSWORD_LOCKOUT_TIME_MINS = integer`
:   Specifies the number of minutes the user account will be locked after exhausting the designated number of password retries
    (i.e. `PASSWORD_MAX_RETRIES`).

    Supported range: 1 to 999, inclusive.

    Default: 15

    Important

    This parameter is stateful. For details, see the note in [Custom password policy for the account and users](/user-guide/password-authentication#label-custom-password-policies).

`PASSWORD_HISTORY = integer`
:   Specifies the number of the most recent passwords that Snowflake stores. These stored passwords cannot be repeated when a user updates
    their password value.

    The current password value does not count towards the history.

    When you increase the history value, Snowflake saves the previous values.

    When you decrease the value, Snowflake saves the stored values up to that value that is set. For example, if the history value is 8 and
    you change the history value to 3, Snowflake stores the most recent 3 passwords and deletes the 5 older password values from the history.

    Default: 5

    Max: 24

`COMMENT = 'string_literal'`
:   Adds a comment or overwrites an existing comment for the password policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE PASSWORD POLICY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on password policy DDL and privileges, see [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt).

## Usage notes

- If you want to replace an existing password policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy) command.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create a password policy named `password_policy_prod_1` for your current account:

> Copy code
>
> ```
> CREATE PASSWORD POLICY PASSWORD_POLICY_PROD_1
>     PASSWORD_MIN_LENGTH = 14
>     PASSWORD_MAX_LENGTH = 24
>     PASSWORD_MIN_UPPER_CASE_CHARS = 2
>     PASSWORD_MIN_LOWER_CASE_CHARS = 2
>     PASSWORD_MIN_NUMERIC_CHARS = 2
>     PASSWORD_MIN_SPECIAL_CHARS = 2
>     PASSWORD_MAX_AGE_DAYS = 30
>     PASSWORD_MAX_RETRIES = 3
>     PASSWORD_LOCKOUT_TIME_MINS = 30
>     PASSWORD_HISTORY = 5
>     COMMENT = 'production account password policy';
> ```
