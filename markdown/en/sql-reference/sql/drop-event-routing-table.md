# DROP EVENT ROUTING TABLE

Drops an event routing table. Routing tables are
used to route events to a centralized location.

For information about event routing tables,
see [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Syntax

Copy code

```
DROP EVENT ROUTING TABLE <table_name>
```

## Required parameters

`table_name`
:   Specifies the identifier (the name) for the event routing table to be dropped.

## Access control requirements

| Role | Notes |
| --- | --- |
| ORGADMIN | Required to run this command. If the organization account has the GLOBALORGADMIN role enabled, only GLOBALORGADMIN can run this command. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

Drop the event routing table `org_table`:

Copy code

```
DROP EVENT ROUTING TABLE org_table
```
