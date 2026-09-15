# DROP PASSWORD POLICY

Removes a password policy from the system.

See also:
:   [DDL commands](/user-guide/password-authentication#label-password-policy-mgmt)

## Syntax

Copy code

```
DROP PASSWORD POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the password policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

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

- Prior to dropping a password policy, execute the following statement to determine if any password policies are applied to the account or
  users in the account. For more information, see [POLICY\_REFERENCES](/sql-reference/functions/policy_references).

  Copy code

  ```
  SELECT * from table(information_schema.policy_references(policy_name=>'<string>'));
  ```
- A password policy cannot be dropped successfully if it is currently attached to an account or user. Before executing a DROP statement,
  UNSET the password policy from the account with an [ALTER ACCOUNT](/sql-reference/sql/alter-account) statement or unset the password policy from a
  user with an [ALTER USER](/sql-reference/sql/alter-user) statement.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

Drop a password policy:

> Copy code
>
> ```
> DROP PASSWORD POLICY password_policy_production_1;
> ```
