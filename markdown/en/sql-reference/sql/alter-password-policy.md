# ALTER PASSWORD POLICY

Modifies the properties for an existing password policy.

Any changes made to the password policy properties go into effect when the next SQL query that uses the password policy runs.

See also:
:   [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt)

## Syntax

Copy code

```
ALTER PASSWORD POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER PASSWORD POLICY [ IF EXISTS ] <name> SET [ PASSWORD_MIN_LENGTH = <integer> ]
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

ALTER PASSWORD POLICY [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER PASSWORD POLICY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER PASSWORD POLICY [ IF EXISTS ] <name> UNSET [ PASSWORD_MIN_LENGTH ]
                                                 [ PASSWORD_MAX_LENGTH ]
                                                 [ PASSWORD_MIN_UPPER_CASE_CHARS ]
                                                 [ PASSWORD_MIN_LOWER_CASE_CHARS ]
                                                 [ PASSWORD_MIN_NUMERIC_CHARS ]
                                                 [ PASSWORD_MIN_SPECIAL_CHARS ]
                                                 [ PASSWORD_MIN_AGE_DAYS ]
                                                 [ PASSWORD_MAX_AGE_DAYS ]
                                                 [ PASSWORD_MAX_RETRIES ]
                                                 [ PASSWORD_LOCKOUT_TIME_MINS ]
                                                 [ PASSWORD_HISTORY ]
                                                 [ COMMENT ]
```

## Parameters

`name`
:   Identifier for the password policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the session policy; must be unique for your account.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`SET ...`
:   Specifies one or more parameters to set for the password policy separated by blank spaces, commas, or new lines.

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
        you change the history value to 3, Snowflake stores the most recent 3 password values and deletes the 5 older password values from the
        history.

        Default: 5

        Max: 24

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the password policy.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more parameters to unset for the password policy, which resets them to the system defaults.

    You can reset multiple properties with a single ALTER statement. Each property must be separated by a comma. When
    resetting a property, specify only the name. Specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Password policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on password policy DDL and privileges, see [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt).

## Usage notes

- Before executing this command, run the [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy) command to determine the attribute values of the policy.

  If you want to update an existing password policy and need to see the current definition of the policy, call the
  [GET\_DDL](/sql-reference/functions/get_ddl) function or run the [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy) command.
- Moving a password policy to a managed access schema is prohibited unless the password policy owner (i.e. the role that has the
  OWNERSHIP privilege on the password policy) also owns the target schema. For more information, see
  [Overview of Access Control Privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges).

## Examples

The following example describes the current password policy, and then updates the password policy to specify the number of allowed password
retries:

> Copy code
>
> ```
> DESC PASSWORD POLICY password_policy_prod_1;
>
> ALTER PASSWORD POLICY password_policy_prod_1 SET PASSWORD_MAX_RETRIES = 3;
> ```
