# ALTER ORGANIZATION UNSET EVENT ROUTING TABLE

Deactivates the event routing table for all application listings in the
specified organization.

For information about event routing tables,
see [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Syntax

Copy code

```
ALTER ORGANIZATION UNSET EVENT ROUTING TABLE FOR ALL APPLICATION LISTINGS
```

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

The following example demonstrates how to unset the event routing table for
all application listings in the organization:

Copy code

```
ALTER ORGANIZATION UNSET EVENT ROUTING TABLE FOR ALL APPLICATION LISTINGS
```
