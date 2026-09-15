# DROP PACKAGES POLICY

Removes a packages policy from the system.

## Syntax

Copy code

```
DROP PACKAGES POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the packages policy to drop. If the identifier contains spaces or special characters, the entire string must be
    enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Packages policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A packages policy cannot be dropped successfully if it is currently attached to an account. Before executing a DROP statement,
  to UNSET the packages policy from the account,
  run [ALTER ACCOUNT UNSET PACKAGES POLICY](/sql-reference/sql/alter-account).

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.
