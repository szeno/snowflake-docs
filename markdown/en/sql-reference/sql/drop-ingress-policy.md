# DROP INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Removes an [ingress policy](/user-guide/ingress-policies) from the current or specified
schema.

See also:
:   [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy),
    [ALTER INGRESS POLICY](/sql-reference/sql/alter-ingress-policy),
    [DESCRIBE INGRESS POLICY](/sql-reference/sql/desc-ingress-policy),
    [SHOW INGRESS POLICIES](/sql-reference/sql/show-ingress-policies)

## Syntax

Copy code

```
DROP INGRESS POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Identifier for the ingress policy to drop. If the identifier contains spaces or special
    characters, enclose the entire string in double quotes. Identifiers enclosed in double quotes are
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot drop an ingress policy while it is attached to an account or a user. Detach it first
  with `ALTER ACCOUNT UNSET INGRESS POLICY` or `ALTER USER <user> UNSET INGRESS POLICY`.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

Detach the policy, then drop it:

Copy code

```
ALTER ACCOUNT UNSET INGRESS POLICY;
ALTER USER etl_runner UNSET INGRESS POLICY;
DROP INGRESS POLICY security_db.policies.corp_only;
```
