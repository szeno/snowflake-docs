# ALTER MAINTENANCE POLICY

Modifies an existing [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies).

See also:
:   [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy), [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy), [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies)

## Syntax

Copy code

```
 ALTER MAINTENANCE POLICY [ IF EXISTS ] <name> SET
   [ SCHEDULE = '<schedule>' ]
   [ COMMENT = '<comment>' ]

ALTER MAINTENANCE POLICY [ IF EXISTS ] <name> UNSET
   [ COMMENT ]

ALTER MAINTENANCE POLICY [ IF EXISTS ] <name> RENAME TO <new_name>
```

## Parameters

`name`
:   Specifies the identifier of the maintenance policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET`
:   Sets one or more specified properties for the maintenance policy.

    `SCHEDULE = 'schedule'`
    :   Specifies the schedule for the maintenance policy. This parameter uses the
        same syntax as the `SCHEDULE` parameter of the [CREATE TASK](/sql-reference/sql/create-task) command.

    `COMMENT = 'comment'`
    :   Specifies a comment for the maintenance policy.

`UNSET`
:   Unsets one or more properties for the maintenance policy.

    `COMMENT`
    :   Unsets the maintenance policy.

`RENAME TO new_name`
:   Renames the maintenance policy to a new identifier.
    The new identifier must be unique for the schema.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY or OWNERSHIP | Maintenance policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example changes the maintenance policy schedule to Sundays at 3 AM UTC:

Copy code

```
ALTER MAINTENANCE POLICY my_maintenance_policy SET
  SCHEDULE = 'USING CRON 0 3 * * SUN UTC';
```
