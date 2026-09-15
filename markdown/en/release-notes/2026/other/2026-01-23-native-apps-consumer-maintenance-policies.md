# Jan 23, 2026: Consumer-controlled maintenance policies for Snowflake Native Apps (*Preview*)

Consumer-controlled maintenance policies are now in public preview for Snowflake Native Apps.

With Snowflake Native Apps, consumers can set a maintenance policy for an upgrade so that apps don’t
update during specific time periods. When an upgrade is ready and a new release
directive is set, the upgrade begins. However, if the consumer has set a
maintenance policy, the upgrade is delayed until the start date and time
specified in the maintenance policy.

For more information, see [Consumer-controlled maintenance policies](/developer-guide/native-apps/consumer-maintenance-policies).

To create and set a maintenance policy, the consumer uses the following SQL commands:

- [CREATE MAINTENANCE POLICY](/sql-reference/sql/create-maintenance-policy): Creates a new maintenance policy. The customer sets a schedule for the maintenance policy to allow upgrades to begin at a specific time.
- [ALTER MAINTENANCE POLICY](/sql-reference/sql/alter-maintenance-policy): Applies or removes a maintenance policy.
