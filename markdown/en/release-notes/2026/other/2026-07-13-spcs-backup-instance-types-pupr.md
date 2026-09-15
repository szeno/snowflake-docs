# Jul 13, 2026: Snowpark Container Services backup instance types (*Public preview*)

Cloud capacity isn’t always guaranteed. When a compute pool’s instance type is unavailable, provisioning fails with an insufficient capacity error (ICE), leaving the pool unable to scale. Previously, resolving an ICE required manually switching the pool to a different instance type. Backup instance types remove that manual step: you specify an ordered list of fallback instance families, and Snowflake automatically retries provisioning using the backup families in the order you specify.

Each time the pool scales up, Snowflake checks the primary instance type first. If capacity is available, new nodes use the primary; otherwise, Snowflake works through the backup list in order. Nodes already running on a backup family are not disrupted; they are replaced with primary-family nodes only when cycled, for example during a maintenance window.

You configure the fallback list with the new `BACKUP_INSTANCE_FAMILIES` parameter. For example, the following command enables backup instance types for an existing compute pool:

Copy code

```
ALTER COMPUTE POOL my_compute_pool
  SET BACKUP_INSTANCE_FAMILIES = ('GEN_X64_G2_8');
```

Key capabilities include:

- **Automatic fallback**: Snowflake works through your ordered backup list when the primary instance type is capacity-constrained, and prefers the primary again for new nodes once its capacity recovers.
- **Customer-controlled configuration**: Define the ordered fallback list using the new `BACKUP_INSTANCE_FAMILIES` parameter on [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) and [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool).
- **Node observability**: Use the new [SHOW NODES IN COMPUTE POOL](/sql-reference/sql/show-nodes-compute-pool) command to see the actual instance family in use on each provisioned node.
- **Transparent billing**: Nodes are billed at the rate of their actual instance type. Primary nodes are billed at the primary family’s rate; backup nodes are billed at the backup family’s rate.

For more information, see [Backup instance types](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-backup-instance-types).
