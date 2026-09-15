# ALTER EVENT ROUTING TABLE

Alters an event routing table used to route events to a centralized location.
You can make the following changes to an event routing table:

- Specify a new set of rules using `SET RULES`
- Create a new rule or replace a single rule using `SET RULE`
- Delete a rule using `UNSET RULE`
- Rename a rule using `MODIFY RULE ... RENAME`
- Rename the event routing table

For information about event routing tables, see
[Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

## Syntax

Copy code

```
ALTER EVENT ROUTING TABLE <table_name> [ FORCE ]
  SET RULES
  <rule_name> = (REGION_GROUP=<region_group>, REGIONS=('<region1>', '<region2>', ...), DESTINATION_ACCOUNT = <organization>.<account_name>),
  ...

ALTER EVENT ROUTING TABLE <table_name> [ FORCE ]
  SET RULE
  <rule_name> REGION_GROUP=<region_group> REGIONS=('<region1>', '<region2>', ...) DESTINATION_ACCOUNT = <organization>.<account_name>

ALTER EVENT ROUTING TABLE <table_name> [ FORCE ]
  UNSET RULE <rule_name>

ALTER EVENT ROUTING TABLE <table_name>
  MODIFY RULE <rule_name> RENAME TO <new_rule_name>

ALTER EVENT ROUTING TABLE <table_name>
  RENAME TO <new_table_name>
```

## Parameters

`table_name`
:   Specifies the identifier (name) for the event routing table to alter. If the
    identifier contains spaces or special characters, enclose the entire string in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`FORCE`
:   Specifies that the operation should be performed even if the event routing
    table is currently activated for an organization. If you omit FORCE and the
    table is currently activated, the command fails. FORCE is not required for
    renaming commands.

`SET RULES`
:   Replaces all existing rules with a new set of rules. Each rule has the
    following parameters:

    `rule_name` (required)
    :   Specifies the name of the rule. The rule name must be unique within the
        event routing table. If `REGIONS` is set to `ALL`, the name must be
        `default`. Default rules can’t be enclosed in double quotes. Other rule
        names can be enclosed in double quotes to preserve letter case.

    `REGIONS = ('region1', 'region2', ...)` (required)
    :   Specifies the regions from which events are routed. You can specify
        individual regions or use `ALL` to specify all regions. For information
        about available regions, see [Region IDs](/user-guide/admin-account-identifier#label-snowflake-region-ids).

    `DESTINATION_ACCOUNT = organization.account_name` (required)
    :   Specifies the destination account to route events to. Organization is not
        required. The account must be in the organization.

    `REGION_GROUP = region_group` (optional)
    :   Specifies the region group. The only supported value is `PUBLIC`.

`SET RULE`
:   Creates or replaces a single rule. Accepts the same parameters as
    `SET RULES`.

`UNSET RULE <rule_name>`
:   Deletes a rule from the event routing table.

    `rule_name` (required)
    :   Specifies the name of the rule to delete. If only one rule remains in the
        event routing table, it can’t be unset.

`MODIFY RULE rule_name RENAME TO new_rule_name`
:   Renames a rule.

    `rule_name` (required)
    :   Specifies the name of the rule to rename.

    `new_rule_name` (required)
    :   Specifies the new name for the rule.

`RENAME TO new_table_name`
:   Renames the event routing table.

    `new_table_name` (required)
    :   Specifies the new name for the event routing table.

## Access control requirements

| Role | Notes |
| --- | --- |
| ORGADMIN | Required to run this command. If the organization account has the GLOBALORGADMIN role enabled, only GLOBALORGADMIN can run this command. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Use `FORCE` to modify an event routing table that is currently activated for an
  organization. Tables are activated by the command `ALTER ORGANIZATION SET EVENT ROUTING TABLE FOR ALL APPLICATION LISTINGS`. If you omit FORCE and the table is
  activated, the command fails. FORCE is not required for renaming commands.
- `SET RULES` replaces all existing rules. To add or update a single rule
  without affecting others, use `SET RULE` instead.
- If only one rule remains in the event routing table, you can’t use
  `UNSET RULE` to remove it.

## Examples

Replace all rules in `org_table` with a new set of rules:

Copy code

```
ALTER EVENT ROUTING TABLE org_table FORCE
  SET RULES
    default = (REGION_GROUP=PUBLIC, REGIONS=('ALL'), DESTINATION_ACCOUNT = org.account1)
    aws_us_east_rule = (REGION_GROUP=PUBLIC, REGIONS=('AWS_US_EAST_1', 'AWS_US_EAST_2'), DESTINATION_ACCOUNT = org.account1)
```

Create or replace a rule called `AWS_EU_WEST_RULE` on `org_table` that routes
events from `AWS_EU_WEST_1` to `account2` in the organization:

Copy code

```
ALTER EVENT ROUTING TABLE org_table FORCE
  SET RULE "AWS_EU_WEST_RULE"
    REGION_GROUP=PUBLIC REGIONS=('AWS_EU_WEST_1') DESTINATION_ACCOUNT = org.account2
```

Delete the rule `AWS_EU_WEST_RULE` from `org_table`:

Copy code

```
ALTER EVENT ROUTING TABLE org_table FORCE
  UNSET RULE aws_eu_west_rule
```

Rename the rule `AWS_US_EAST_RULE` to `RULE_1` on `org_table`:

Copy code

```
ALTER EVENT ROUTING TABLE org_table
  MODIFY RULE aws_us_east_rule RENAME TO rule_1
```

Rename the event routing table `org_table` to `org_table_2`:

Copy code

```
ALTER EVENT ROUTING TABLE org_table
  RENAME TO org_table_2
```
