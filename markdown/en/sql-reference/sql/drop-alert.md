# DROP ALERT

Drops an existing [alert](/user-guide/alerts).

See also:
:   [CREATE ALERT](/sql-reference/sql/create-alert) , [ALTER ALERT](/sql-reference/sql/alter-alert), [DESCRIBE ALERT](/sql-reference/sql/desc-alert) , [SHOW ALERTS](/sql-reference/sql/show-alerts) , [EXECUTE ALERT](/sql-reference/sql/execute-alert)

## Syntax

Copy code

```
DROP ALERT [ IF EXISTS ] <name>
```

## Required parameters

`name`
:   Identifier for the alert to drop. If the identifier contains spaces or special characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Alert | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- When an alert is dropped, any current evaluation of the condition of the alert (i.e. a run with an EXECUTING state in the
  [ALERT\_HISTORY](/sql-reference/functions/alert_history) output) is completed.
- An alert can be dropped by the alert owner (i.e. the role that has the OWNERSHIP privilege on the alert) or a higher role
  without first suspending the alert.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

See [Dropping an alert](/user-guide/alerts#label-alerts-drop).
