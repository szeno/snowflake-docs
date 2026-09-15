# Snowflake Postgres High Availability

High Availability (HA) preserves the uptime of your instance by provisioning a secondary virtual machine in a separate
availability zone that receives the same writes as your primary. When HA is enabled, in the event your primary becomes
unavailable, we will automatically fail over to the secondary host by promoting the standby to replace the impacted host. You
don’t need to update your connection details. Once the promotion occurs, the original primary is destroyed and a new standby
host is created.

For instances that are sensitive to protracted downtime, we recommend using our HA feature. Without HA, if your instance becomes
unavailable, Snowflake attempts to provision a new host for your instance, and the control plane automatically restores your
instance using the most recent automated backup and all WAL (write-ahead-log) statements that have been generated since the
latest backup. For small, inactive clusters this could be a matter of minutes, but for larger or active clusters this could take
many hours.

To turn high availability on or off for your Snowflake Postgres instance, run the [ALTER POSTGRES INSTANCE](/sql-reference/sql/alter-postgres-instance) command with the
SET HIGH\_AVAILABILITY option. The following example shows how to turn high availability on or off:

Copy code

```
ALTER POSTGRES INSTANCE production_instance SET HIGH_AVAILABILITY = TRUE;
ALTER POSTGRES INSTANCE dev_test_instance SET HIGH_AVAILABILITY = FALSE;
```
