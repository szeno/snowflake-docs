# SHOW USERS

Lists all [users](/user-guide/admin-user-management) in the system.

See also:
:   [CREATE USER](/sql-reference/sql/create-user) , [ALTER USER](/sql-reference/sql/alter-user) , [DROP USER](/sql-reference/sql/drop-user) , [DESCRIBE USER](/sql-reference/sql/desc-user)

## Syntax

Copy code

```
SHOW [ TERSE ] USERS
  [ LIKE '<pattern>' ]
  [ STARTS WITH '<name_string>' ]
  [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`TERSE`
:   Returns only the following output columns:

    - `name`
    - `created_on`
    - `display_name`
    - `first_name`
    - `last_name`
    - `email`
    - `org_identity`
    - `comment`
    - `has_password`
    - `has_rsa_public_key`
    - `type`
    - `has_mfa`
    - `has_pat`
    - `has_federated_workload_authentication`
    - `is_from_organization_user`

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the user. |
| `created_on` | Date and time when the user was created. |
| `login_name` | Name that the user enters to log into the system. |
| `display_name` | Name displayed for the user in [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). |
| `first_name` | First name of the user. |
| `last_name` | Last name of the user. |
| `email` | Email addresss for the user. |
| `mins_to_unlock` | Number of minutes until [the temporary lock on the user login is cleared](/user-guide/admin-user-management#label-user-management-unlock). |
| `days_to_expiry` | Number of days after which the user status is set to “Expired” and the user is no longer allowed to log in. |
| `comment` | Comment about the user. |
| `disabled` | If TRUE, the user is [locked out of Snowflake and cannot log back in](/user-guide/admin-user-management#label-user-management-disable-enable-user). |
| `must_change_password` | If TRUE, the user is forced to change their password on next login (including their first/initial login) into the system. |
| `snowflake_lock` | If TRUE, the user is locked by Snowflake. When a user is locked, they are unable to log in until the lock is removed. |
| `default_warehouse` | Virtual warehouse that is active by default for the user’s session upon logging in. |
| `default_namespace` | Namespace (database only or database and schema) that is active by default for the user’s session upon logging in. |
| `default_role` | Primary role that is active by default for the user’s session upon logging in. |
| `default_secondary_roles` | Set of secondary roles that are active for the user’s session upon logging in. |
| `ext_authn_duo` | If TRUE, [Duo](/user-guide/security-mfa-duo) is enabled for the user, which requires the user to use [MFA (multi-factor authentication)](/user-guide/security-mfa) when logging in. |
| `ext_authn_uid` | Authorization ID used for Duo. |
| `mins_to_bypass_mfa` | Number of minutes to [temporarily bypass MFA requirement for the user](/user-guide/security-mfa#label-mfa-temp-disable). |
| `owner` | Role that owns the user. |
| `last_success_login` | Date and time when the user last logged in to the Snowflake. |
| `expires_at_time` | Date and time when the user’s status is set to `EXPIRED` and the user can no longer log in. |
| `locked_until_time` | Number of minutes until the temporary lock on the user login is cleared. |
| `has_password` | If TRUE, the user has a password. |
| `has_rsa_public_key` | If TRUE, the user has a public key for [key-pair authentication](/user-guide/key-pair-auth). |
| `type` | Type of the user. For a list of possible values, see [Types of users](/user-guide/admin-user-management#label-user-management-types). |
| `has_mfa` | If TRUE, the user is enrolled in [multi-factor authentication (MFA)](/user-guide/security-mfa). |
| `has_pat` | If TRUE, the user has one or more [programmatic access tokens](/user-guide/programmatic-access-tokens). |
| `has_workload_identity` | If TRUE, the user is configured to authenticate with [workload identity federation](/user-guide/workload-identity-federation). |
| `is_from_organization_user` | If TRUE, the user was imported from a global [organization user](/user-guide/organization-users). |

Expand

Show lessSee more

## Access control requirements

Any user can execute the SHOW USERS command. The output always includes the username in the `name` column.

For the other columns, Snowflake filters the output based upon the privileges granted to the user’s
[active role](/user-guide/security-access-control-overview#label-access-control-overview-active-roles). The values in the other columns are returned if the active role
has either of the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | User |  |
| MANAGE GRANTS | Account |  |

Expand

Show lessSee more

Otherwise, the other columns contain NULL.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- If the account has more than 10,000 users, you can use the [LIMIT … FROM …](#label-show-users-parameters-limit-from)
  parameter to return smaller sets of users.

  For example, you can run `SHOW USERS LIMIT 10000 FROM my_user` to return the next 10000 users starting from the user named
  `my_user`.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

The following example lists the users in the account:

Copy code

```
SHOW USERS;
```

```
+--------------+-------------------------------+---------------+--------------+------------+-----------+------------------------+----------------+----------------+---------+----------+----------------------+----------------+-------------------+-------------------+--------------+-------------------------+---------------+---------------+--------------------+--------------+-------------------------------+-----------------+-------------------+--------------+--------------------+--------+---------+---------+---------------------------------------+
| name         | created_on                    | login_name    | display_name | first_name | last_name | email                  | mins_to_unlock | days_to_expiry | comment | disabled | must_change_password | snowflake_lock | default_warehouse | default_namespace | default_role | default_secondary_roles | ext_authn_duo | ext_authn_uid | mins_to_bypass_mfa | owner        | last_success_login            | expires_at_time | locked_until_time | has_password | has_rsa_public_key | type   | has_mfa | has_pat | has_federated_workload_authentication |
|--------------+-------------------------------+---------------+------------- +------------+-----------+------------------------+----------------+----------------+---------+----------+----------------------+----------------+-------------------+-------------------+--------------+-------------------------+---------------+---------------+--------------------+--------------+-------------------------------+-----------------+-------------------+--------------+--------------------+--------+---------+---------+---------------------------------------|
| MY_USER_NAME | 2020-04-28 12:24:38.722 -0700 | MY_LOGIN_NAME | Jane Smith   | Jane       | Smith     | jane.smith@example.com | NULL           | NULL           | NULL    | false    | false                | false          | MY_WAREHOUSE      | MY_DB.MY_SCHEMA   | MY_ROLE      | []                      | false         | NULL          | NULL               | ACCOUNTADMIN | 2025-06-12 15:02:22.783 -0700 | NULL            | NULL              | true         | true               | PERSON | true    | true    | false                                 |
+--------------+-------------------------------+---------------+--------------+------------+-----------+------------------------+----------------+----------------+---------+----------+----------------------+----------------+-------------------+-------------------+--------------+-------------------------+---------------+---------------+--------------------+--------------+-------------------------------+-----------------+-------------------+--------------+--------------------+--------+---------+---------+---------------------------------------+
```
