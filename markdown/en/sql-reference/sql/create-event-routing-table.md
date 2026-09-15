# CREATE EVENT ROUTING TABLE

Creates a new event routing table in the
current organization and region. The table is
used to route events and other telemetry data to a centralized location,
where they can be analyzed.

After you create an event routing table, you must activate it for the organization
using the [ALTER ORGANIZATION SET EVENT ROUTING TABLE](/sql-reference/sql/alter-organization-set-event-routing-table)
command.

For information about event routing tables,
see [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Syntax

Copy code

```
CREATE EVENT ROUTING TABLE <table_name>
   WITH RULES
    {rule name} = (REGION_GROUP={region group}, REGIONS=('{region1}', '{region2}', ...), DESTINATION_ACCOUNT = {organization}.{account_name})
    ...
```

## Required parameters

`table_name`
:   Specifies the identifier (the name) for the event routing table; must be unique for the organization in which the event routing table is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

Each rule has the following required parameters:

> `{rule name}`
> :   Specifies the name of the rule to create. The rule name must be unique for the event routing table.
>
> `region1, region2, ...`
> :   Specifies the regions to route the events to. You can specify individual
>     regions or use *ALL* to specify all regions.
>
>     For information about available regions, see [Region IDs](/user-guide/admin-account-identifier#label-snowflake-region-ids).
>
> `organization`
> :   Specifies the organization to route the events to.
>
> `DESTINATION_ACCOUNT`
> > Specifies the account to which the events are routed. You specify the routing account in the format *org.account\_name*.

## Optional parameters

> `{region group}`
> :   Specifies the region group to route the events to. The only supported value is *PUBLIC*.

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

The following example demonstrates how to create an event routing table:

Copy code

```
CREATE EVENT ROUTING TABLE org_table
   WITH RULES
     default = (REGION_GROUP='PUBLIC', REGIONS=('ALL'), DESTINATION_ACCOUNT = org.account1)
     aws_us = (REGION_GROUP='PUBLIC', REGIONS=('AWS_US_EAST_1', 'AWS_US_WEST_2'), DESTINATION_ACCOUNT = org.account1)
```
