# CREATE MAINTENANCE POLICY

Creates a new [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) in the current or specified schema.

See also:
:   [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy), [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy), [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] MAINTENANCE POLICY [ IF NOT EXISTS ] <name>
  SCHEDULE = 'USING CRON <cron_spec> <timezone>'
  [ COMMENT = '<comment>' ]
```

## Required parameters

`name`
:   Specifies the identifier of the maintenance policy. The identifier must be
    unique within the schema.

`SCHEDULE = 'USING CRON cron_spec timezone`
:   Specifies the schedule for the maintenance policy. This parameter uses the
    same syntax as the `SCHEDULE` parameter of the [CREATE TASK](/sql-reference/sql/create-task) command.

## Optional parameters

`COMMENT = 'comment'`
:   Specifies an optional comment for the maintenance policy.

## Usage notes

- Each app or account can have only one maintenance policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE MAINTENANCE POLICY | Schema |  |

Expand

Show lessSee more

## Examples

The following example creates a maintenance policy that schedules
upgrades for Saturdays at 2 AM UTC:

Copy code

```
CREATE MAINTENANCE POLICY my_maintenance_policy
  SCHEDULE = 'USING CRON 0 2 * * SAT UTC'
  COMMENT = 'Weekly Saturday maintenance window';
```
