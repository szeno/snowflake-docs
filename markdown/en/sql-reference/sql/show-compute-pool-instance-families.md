# SHOW COMPUTE POOL INSTANCE FAMILIES

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the available [compute pool instance families](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pools-instance-family-table)
that you can use to create a compute pool.

See also:
:   [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool) , [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool)

## Syntax

Copy code

```
SHOW COMPUTE POOL INSTANCE FAMILIES
```

## Output

The command output provides compute pool instance family properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Instance family name. |
| `description` | Instance family description. |
| `vcpu` | Number of vCPUs that are accessible to the user. |
| `memory_gib` | Memory in GiB that is accessible to the user. |
| `storage_gib` | Storage in GiB that is accessible to the user. |
| `gpu` | Name of the GPU if applicable, else an empty string. |
| `gpu_count` | Count of GPUs if applicable, else 0. |
| `gpu_memory_gib` | GPU Memory available per GPU if applicable, else 0. |
| `current_node_usage` | Number of nodes of this type currently in use by your Snowflake account. |
| `message` | Additional information about the instance family. |

Expand

Show lessSee more

## Examples

The following command lists the compute pool instance families:

Copy code

```
SHOW COMPUTE POOL INSTANCE FAMILIES;
```
