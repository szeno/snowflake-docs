# Configure centralized event sharing for an app

This topic describes how providers can configure a Snowflake Native App to share log
messages and trace events from different regions with a central location.

## About centralized event sharing

The Snowflake Native App Framework supports centralized event sharing, which allows an app to share
telemetry messages from different regions to a central location. These telemetry
messages can include log messages, trace events, and other data. This feature
is useful for monitoring and troubleshooting applications that are deployed
across multiple regions. Without centralized event sharing, providers would need to
manually route the events from each region to a central location using a custom
solution.

Note

When using centralized event sharing, you must ensure that your
app is compliant with all relevant regulations and standards, such as GDPR,
HIPAA, and PCI DSS.

### Overview: Implement centralized event sharing

1. Create an event routing table for the organization.
2. Activate the event routing table for the organization.
3. After the application starts to produce events, query the event routing table to retrieve the telemetry data.

### Routing rules

When you create an event routing table, you define rules that control which
account the telemetry events are routed to. These rules contain the following information:

- The region or regions from which the events are routed.
- The account to which the events are routed.

Typically, each table uses routing rules to route telemetry data to one or more
accounts where the telemetry
data will be analyzed.

You can define rules that are applied to specific regions, and
a default rule that is applied to regions without specific rules. For example,
you can define a rule to route events from all European regions to a specific
account, and a default rule to route events from all other regions to a
different account.

## Create an event routing table

When you create an event routing table, you define rules that control to which account the
events are routed. You use the [CREATE EVENT ROUTING TABLE](/sql-reference/sql/create-event-routing-table)
command to create an event routing table.

The following command creates an event routing table:

Copy code

```
CREATE EVENT ROUTING TABLE org_table
  WITH RULES
    default = (REGION_GROUP='PUBLIC', REGIONS=('ALL'), DESTINATION_ACCOUNT = org.account1)
    {rule_name} = (REGION_GROUP='PUBLIC', REGIONS=('AWS_US_EAST_1', 'AWS_US_EAST_2'),
      DESTINATION_ACCOUNT = org.account1);
```

Where:

`rule_name`
:   The name of the rule. The rule name must be named “default” if ALL is used for the REGIONS.

`REGION_GROUP`
:   Optional. Specifies the group of regions that the rule applies to.
    The only supported value is `PUBLIC`.

`REGIONS`
:   The list of regions that the rule applies to. You can specify individual
    regions or use `ALL` to specify all regions. Rules with specific regions
    take precedence over rules for `ALL`. You can’t use `ALL` and specific
    regions in the same rule. For a list of available regions, see the **Snowflake Region ID**
    column in the Region IDs table here: [Region IDs](/user-guide/admin-account-identifier#label-snowflake-region-ids).

`DESTINATION_ACCOUNT`
:   The account to which the events are routed. You specify the routing account
    in the format `org.account_name`, or `account_name` for accounts in the
    current account’s organization.

Each organization can have only one event routing table activated for it. Each
event routing table can have a maximum of 200 rules.

## Update rules for an event routing table

To update the rules for an event routing table with a new set of rules, use the [ALTER EVENT ROUTING TABLE](/sql-reference/sql/alter-event-routing-table) command.

The following command updates the rules for an event routing table:

Copy code

```
ALTER EVENT ROUTING TABLE org_table [FORCE]
  SET RULES
    default_rule = (REGIONS=('ALL'), DESTINATION_ACCOUNT = org.account1)
    aws_eu_west = (REGIONS=('AWS_EU_WEST_1', 'AWS_EU_WEST_2'), DESTINATION_ACCOUNT = org.account1)
```

The preceding command replaces the existing rules with the new set of rules. The
FORCE keyword is optional. If the event routing table is currently activated for an organization, and you do not use the FORCE option,
the command fails.

## Activate or deactivate an event routing table for an organization

To activate an existing event routing table for the organization, use the
[ALTER ORGANIZATION SET EVENT ROUTING TABLE](/sql-reference/sql/alter-organization-set-event-routing-table) command.
The following command activates the event routing table for the organization:

Copy code

```
ALTER ORGANIZATION SET EVENT ROUTING TABLE 'org_table' FOR ALL APPLICATION LISTINGS;
```

When you activate an event routing table for the organization, the events are routed
to the accounts specified in the `DESTINATION_ACCOUNT` parameter of the table’s rules.

The following command deactivates the event routing table for the organization:

Copy code

```
ALTER ORGANIZATION UNSET EVENT ROUTING TABLE FOR ALL APPLICATION LISTINGS;
```

## Drop an event routing table

To drop an event routing table, use the [DROP EVENT ROUTING TABLE](/sql-reference/sql/drop-event-routing-table) command.
The following command drops the event routing table:

Copy code

```
DROP EVENT ROUTING TABLE org_table;
```

If the event routing table is currently activated for an organization, the
command fails with an error.

## Show available event routing tables

To show the available event routing tables, providers can use the [SHOW EVENT ROUTING TABLES](/sql-reference/sql/show-event-routing-tables) command.

The following command shows the available event routing tables:

Copy code

```
SHOW EVENT ROUTING TABLES;
```

```
+----------+-------------+-------------+
| name     | created_on  | modified_on |
|----------+-------------+-------------+
| TABLE_1  | 2025...     | 2025...     |
+----------+-------------+-------------+
```

## Show rules in an event routing table

To show the rules in an event routing table, providers can use the [SHOW RULES IN EVENT ROUTING TABLE](/sql-reference/sql/show-rules-in-event-routing-table) command.

The following command shows the rules in an event routing table:

Copy code

```
SHOW RULES IN EVENT ROUTING TABLE 'table_1';
```

```
+----------+--------------+-----------------------------------+---------------------+
| name     | region_group | regions                           | destination_account |
|----------+--------------+-----------------------------------+---------------------+
| RULE_1   | PUBLIC       | [ALL]                             | org.account1        |
| RULE_2   | PUBLIC       | [AWS_EU_WEST_1, AWS_EU_CENTRAL_1] | org.account2        |
+----------+--------------+-----------------------------------+---------------------+
```

## Show the active event routing table for an organization

- To show the active event routing table for an organization, use the [SHOW EVENT ROUTING TABLE ON ORGANIZATION](/sql-reference/sql/show-event-routing-table-on-organization) command, as shown in the following example:

Copy code

```
SHOW EVENT ROUTING TABLE ON ORGANIZATION FOR ALL APPLICATION LISTINGS;
```

```
+----------+-------------+-------------+
| name     | created_on  | modified_on |
|----------+-------------+-------------+
| TABLE_1  | 2025...     | 2025...     |
+----------+-------------+-------------+
```

If there is no event routing table activated for the organization, the command
returns no rows.

## Required privileges

This section describes the privileges required to modify centralized event sharing
settings or retrieve events from the central location.

### Privileges required to modify centralized event routing

To configure centralized event routing at the organization level, you must have
the following privileges:

- Accounts using org accounts must have the `ORGADMIN` role.

### Privileges for viewing event routing configuration

To view the event routing configuration for an account, your account must have
one of the following roles or privileges:

- `ORGADMIN` role.
- `CREATE ORGANIZATION LISTING` privilege.
- `CREATE DATA EXCHANGE LISTING` privilege.

## Compatibility with existing event sharing

Centralized event sharing supports compatibility with your existing event sharing
configuration. With this feature, you can continue to use your existing event routing configuration while migrating to the new centralized event sharing feature. You can also continue to use event sharing for regions that are not supported by centralized event sharing, such as sovereign or government regions.

Events are routed using the existing event sharing configuration if either of the following conditions are met:

- There is no event routing table assigned to the organization.
- The event routing table has no default rule and no rule for the current region.

For information about the existing event sharing feature, see [About event sharing](/developer-guide/native-apps/event-about#label-nativeapps-provider-logging-about-events).

## Troubleshooting

To troubleshoot issues with centralized event sharing, use the following commands
to view the event routing configuration for an account:

- [SHOW EVENT ROUTING TABLE ON ORGANIZATION](/sql-reference/sql/show-event-routing-table-on-organization)
- [SHOW RULES IN EVENT ROUTING TABLE](/sql-reference/sql/show-rules-in-event-routing-table)

If you need to troubleshoot issues with legacy event routing configuration, use the following command:

- [SYSTEM$SHOW\_EVENT\_SHARING\_ACCOUNTS](/sql-reference/functions/system_show_event_sharing_accounts)

## Cross-region data transfer cost

Routing telemetry from one region to a destination account in a different region
incurs cross-region data transfer (egress) charges. Providers are responsible for these
costs. For background on how data transfer is billed, see
[Understanding data transfer cost](/user-guide/cost-understanding-data-transfer).

To monitor cross-region egress associated with centralized event sharing, query the
`DATA_TRANSFER_HISTORY` view in the `ACCOUNT_USAGE` schema in the destination event account.
This view reports the number of bytes transferred along with the source cloud and region,
target cloud and region, and the transfer type.

Copy code

```
SELECT
  start_time,
  end_time,
  source_cloud,
  source_region,
  target_cloud,
  target_region,
  bytes_transferred,
  transfer_type
FROM SNOWFLAKE.ACCOUNT_USAGE.DATA_TRANSFER_HISTORY
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
  AND source_region != target_region
ORDER BY start_time DESC;
```

To view the egress cost in currency rather than bytes, query the
`USAGE_IN_CURRENCY_DAILY` view in the `ORGANIZATION_USAGE` schema:

Copy code

```
SELECT
  usage_date,
  usage_type,
  usage,
  currency,
  usage_in_currency
FROM SNOWFLAKE.ORGANIZATION_USAGE.USAGE_IN_CURRENCY_DAILY
WHERE usage_type = 'data transfer'
  AND usage_date >= DATEADD('day', -30, CURRENT_DATE())
ORDER BY usage_date DESC;
```

For more information about exploring data transfer cost, see
[Exploring data transfer cost](/user-guide/cost-exploring-data-transfer).

## Limitations

The following limitations apply to centralized event sharing:

Special regions
:   Special regions such as FedRAMP regions and sovereign regions such as
    AWS China regions are not supported.

Private Links
:   Sharing events over Private Links is not supported.
