# SHOW RULES IN EVENT ROUTING TABLE

Returns the list of rules for the specified event routing table.
Event routing table rules are used to specify where to route events.

For information about event routing tables, see
[Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Syntax

Copy code

```
SHOW RULES IN EVENT ROUTING TABLE (<event_routing_table_name>)
```

## Required parameters

`event_routing_table_name`
:   Specifies the name of the event routing table to show the rules for.

## Access control requirements

| Role | Notes |
| --- | --- |
| ORGADMIN | Required to run this command. |
| Role with CREATE ORGANIZATION LISTING privilege |  |
| Role with CREATE DATA EXCHANGE LISTING privilege |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).
