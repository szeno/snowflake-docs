# Sep 17, 2026: Snowpark Container Services backup instance types (*General availability*)

Backup instance types for Snowpark Container Services compute pools are now generally available and are no longer in [Preview](/release-notes/preview-features).

Backup instance types let you specify an ordered list of fallback instance families on a compute pool. When the primary instance type is capacity-constrained, Snowflake automatically retries provisioning with the backup families in the order you specify instead of returning an insufficient capacity error (ICE).

You configure the fallback list with the `BACKUP_INSTANCE_FAMILIES` parameter. For example, the following command enables backup instance types for an existing compute pool:

Copy code

```
ALTER COMPUTE POOL my_compute_pool
  SET BACKUP_INSTANCE_FAMILIES = ('GEN_X64_G2_8');
```

Key capabilities include:

- **Automatic fallback**: Snowflake works through your ordered backup list when the primary instance type is capacity-constrained, and prefers the primary again for new nodes once its capacity recovers.
- **Customer-controlled configuration**: Define the ordered fallback list using the `BACKUP_INSTANCE_FAMILIES` parameter on [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) and [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool).
- **Node observability**: Use the [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool) command to see the actual instance family in use on each provisioned node.
- **Transparent billing**: Nodes are billed at the rate of their actual instance type. Primary nodes are billed at the primary family’s rate; backup nodes are billed at the backup family’s rate.

For more information, see [Backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types).
