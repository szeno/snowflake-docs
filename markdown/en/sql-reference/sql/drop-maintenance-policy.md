# DROP MAINTENANCE POLICY

Removes a [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) from the current or specified schema. The command
fails if the maintenance policy is applied to an app or account.

See also:
:   [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy), [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy), [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies)

## Syntax

Copy code

```
DROP MAINTENANCE POLICY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier of the maintenance policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| DROP MAINTENANCE POLICY | Maintenance policy |  |
| OWNERSHIP | Maintenance policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

## Examples

The following example drops a maintenance policy named `my_maintenance_policy`:

Copy code

```
DROP MAINTENANCE POLICY my_maintenance_policy;
```
