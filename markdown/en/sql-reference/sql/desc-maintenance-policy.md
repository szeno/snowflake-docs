# DESCRIBE MAINTENANCE POLICY

Shows the details of a [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies).

See also:
:   [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy), [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy), [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy), [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies)

## Syntax

Copy code

```
DESCRIBE MAINTENANCE POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier of the maintenance policy to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY MAINTENANCE POLICY | Account |  |
| OWNERSHIP | Maintenance policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

## Examples

The following example describes a maintenance policy named `my_maintenance_policy`:

Copy code

```
DESCRIBE MAINTENANCE POLICY my_maintenance_policy;
```
