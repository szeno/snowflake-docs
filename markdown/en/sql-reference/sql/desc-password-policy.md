# DESCRIBE PASSWORD POLICY

Describes the details about a password policy.

DESCRIBE can be abbreviated to DESC.

See also:
:   [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt)

## Syntax

Copy code

```
DESC[RIBE] PASSWORD POLICY <name>
```

## Parameters

`name`
:   Identifier for the password policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY PASSWORD POLICY | Account |  |
| OWNERSHIP | Password policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on password policy DDL and privileges, see [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt).

## Usage notes

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

## Example

Copy code

```
DESC PASSWORD POLICY password_policy_prod_1;
```

```
+-----------------------------------+----------------------------------------+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
|   property                        |   value                                |   default   |   description                                                                                                                                 |
+-----------------------------------+----------------------------------------+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
|   NAME                            |   PASSWORD_POLICY_PROD_1               |   null      |   Name of password policy.                                                                                                                    |
|   OWNER                           |   PROD_ADMIN                           |   null      |   Owner of password policy.                                                                                                                   |
|   COMMENT                         |   production account password policy   |   null      |   user comment associated to an object in the dictionary                                                                                      |
|   PASSWORD_MIN_LENGTH             |   12                                   |   8         |   Minimum length of new password.                                                                                                             |
|   PASSWORD_MAX_LENGTH             |   24                                   |   256       |   Maximum length of new password.                                                                                                             |
|   PASSWORD_MIN_UPPER_CASE_CHARS   |   2                                    |   1         |   Minimum number of uppercase characters in new password.                                                                                     |
|   PASSWORD_MIN_LOWER_CASE_CHARS   |   2                                    |   1         |   Minimum number of lowercase characters in new password.                                                                                     |
|   PASSWORD_MIN_NUMERIC_CHARS      |   2                                    |   1         |   Minimum number of numeric characters in new password.                                                                                       |
|   PASSWORD_MIN_SPECIAL_CHARS      |   2                                    |   0         |   Minimum number of special characters in new password.                                                                                       |
|   PASSWORD_MIN_AGE_DAYS           |   1                                    |   0         |   Period after a password is changed during which a password cannot be changed again, in days.                                                |
|   PASSWORD_MAX_AGE_DAYS           |   30                                   |   90        |   Period after which password must be changed, in days.                                                                                       |
|   PASSWORD_MAX_RETRIES            |   5                                    |   5         |   Number of attempts users have to enter the correct password before their account is locked.                                                 |
|   PASSWORD_LOCKOUT_TIME_MINS      |   30                                   |   15        |   Period of time for which users will be locked after entering their password incorrectly many times (specified by MAX_RETRIES), in minutes   |
|   PASSWORD_HISTORY                |   5                                    |   24        |   Number of most recent passwords that may not be repeated by the user                                                                        |
+-----------------------------------+----------------------------------------+-------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
```
