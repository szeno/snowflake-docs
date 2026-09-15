# DROP MULTI PARTY APPROVAL POLICY

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes a Multi-party Approval policy from the system.

## Syntax

Copy code

```
DROP MULTI PARTY APPROVAL POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the Multi-party Approval policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Multi-party Approval policy |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A Multi-party Approval policy can’t be dropped while it is attached to an account.
  Before dropping the policy, detach it from the account using an
  [ALTER ACCOUNT](/sql-reference/sql/alter-account) statement.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Example

Copy code

```
DROP MULTI PARTY APPROVAL POLICY security_db.policies.mpa_policy;
```
