# Consumer-controlled maintenance policies

With Snowflake Native Apps, consumers can set a maintenance policy for an upgrade so that apps don’t
update during specific time periods. When an upgrade is ready and a new release
directive is set, the upgrade begins. However, if the consumer has set a
maintenance policy, the upgrade is delayed until the start date and time
specified in the maintenance policy.

To create and set a maintenance policy, the consumer uses the following SQL commands:

- [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy): Creates a new maintenance policy. The customer sets a schedule for the maintenance policy to allow upgrades to begin at a specific time.

To view and manage maintenance policies, the consumer uses the following SQL commands:

- [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy): Modifies an existing maintenance policy.
- [ALTER ACCOUNT](/sql-reference/sql/alter-account): Applies or removes a maintenance policy for all apps in the account.
- [ALTER APPLICATION](/sql-reference/sql/alter-application): Applies or removes a maintenance policy for a specific app.
- [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies): Lists the maintenance policies for the specified account or app.
- [DESCRIBE MAINTENANCE POLICY](/sql-reference/sql/desc-maintenance-policy): Shows the details of a maintenance policy.
- [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy): Removes a maintenance policy from the current or specified schema.

Note the following details about consumer-controlled maintenance policies:

- If a consumer does not set a maintenance policy, the upgrade begins when the default upgrade time is reached. For more information, see
  [Maintenance window](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-maintenance-window).
- Only the start time for a maintenance policy can be specified; not the end time or the duration of the maintenance policy.
- Each app or account can only have one maintenance policy set.
- The provider can set a maintenance deadline for an upgrade, so that the consumer can’t postpone the upgrade indefinitely. As a consumer,
  you should schedule your upgrades as soon as possible during a time when you can be available to test the upgrade and make any necessary adjustments, so that you can avoid having your app become unexpectedly unavailable during an upgrade.

For information about how providers enable maintenance window upgrades, see
[Consumer-controlled maintenance policies: Provider guide](/developer-guide/native-apps/consumer-maintenance-policies-provider).

## Creating a maintenance policy

To create a maintenance policy, a consumer uses the [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy) command.

Copy code

```
CREATE MAINTENANCE POLICY my_maintenance_policy
  SCHEDULE = 'USING CRON 0 2 * * SAT UTC'
  COMMENT = 'Weekly Saturday maintenance policy';
```

Once the maintenance policy is created, it can be applied to an account or app using the [ALTER ACCOUNT](/sql-reference/sql/alter-account) or [ALTER APPLICATION](/sql-reference/sql/alter-application) commands.

Copy code

```
ALTER ACCOUNT SET MAINTENANCE POLICY my_maintenance_policy FOR ALL APPLICATIONS;

ALTER APPLICATION my_app SET MAINTENANCE POLICY my_maintenance_policy;
```

## Privileges

Use the following privileges to manage consumer-controlled maintenance policies.

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE MAINTENANCE POLICY | Schema | Required to create a new maintenance policy. |
| APPLY MAINTENANCE POLICY | Account | Required to apply a maintenance policy to an account or app. |
| APPLY or OWNERSHIP | Maintenance policy | Allows users access to apply or view a maintenance policy. |

Expand

Show lessSee more

## SQL reference

The following SQL commands are used to manage consumer-controlled maintenance policies:

- [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy)
- [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy)
- [DROP MAINTENANCE POLICY](/sql-reference/sql/drop-maintenance-policy)
- [SHOW MAINTENANCE POLICIES](/sql-reference/sql/show-maintenance-policies)
- [DESCRIBE MAINTENANCE POLICY](/sql-reference/sql/desc-maintenance-policy)
