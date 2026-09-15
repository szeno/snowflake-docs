# Snowflake Postgres Instance Sizes

Snowflake Postgres offers three tiers of instances — Burstable, Standard, and Memory — to cover a variety of use cases.

For credit costs for each instance size, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

In general:

- **Burstable** instances have a baseline CPU level but can temporarily burst above this baseline.
- **Standard** instances have a good balance of CPU and memory.
- **Memory-optimized** instances have a higher ratio of memory to CPU, which may improve performance for workloads with greater
  memory needs.

## Burstable

*Important notes*

- Burstable instances can be provisioned with a maximum of 100GB storage.
- Burstable instances have burstable vCPUs. Utilization in excess of the CPU baseline shown below will deplete available vCPU
  credits, leading to CPU rate limiting. This may appear as a sudden downgrade in performance with no other cause.
- Burstable instances do not support High Availability standbys.

| Name | Cores | Memory | IOPS | HA supported | AWS | Azure |
| --- | --- | --- | --- | --- | --- | --- |
| BURST\_S | 2 | 2GB | 11,800 | No | Yes | No |
| BURST\_M | 2 | 4GB | 11,800 | No | Yes | Yes |

Expand

Show lessSee more

## General purpose

| Name | Cores | Memory | IOPS | HA supported | AWS | Azure |
| --- | --- | --- | --- | --- | --- | --- |
| STANDARD\_M | 1 | 4GB | 20,000 | Yes | Yes | No |
| STANDARD\_L | 2 | 8GB | 40,000 | Yes | Yes | Yes |
| STANDARD\_XL | 4 | 16GB | 40,000 | Yes | Yes | Yes |
| STANDARD\_2XL | 8 | 32GB | 40,000 | Yes | Yes | Yes |
| STANDARD\_4XL | 16 | 64GB | 40,000 | Yes | Yes | Yes |
| STANDARD\_8XL | 32 | 128GB | 40,000 | Yes | Yes | Yes |
| STANDARD\_12XL | 48 | 192GB | 60,000 | Yes | Yes | Yes |
| STANDARD\_24XL | 96 | 384GB | 78,000 | Yes | Yes | Yes |

Expand

Show lessSee more

## Memory optimized

| Name | Cores | Memory | IOPS | HA supported | AWS | Azure |
| --- | --- | --- | --- | --- | --- | --- |
| HIGHMEM\_L | 2 | 16GB | 40,000 | Yes | Yes | Yes |
| HIGHMEM\_XL | 4 | 32GB | 40,000 | Yes | Yes | Yes |
| HIGHMEM\_2XL | 8 | 64GB | 40,000 | Yes | Yes | Yes |
| HIGHMEM\_4XL | 16 | 128GB | 40,000 | Yes | Yes | Yes |
| HIGHMEM\_8XL | 32 | 256GB | 40,000 | Yes | Yes | Yes |
| HIGHMEM\_12XL | 48 | 384GB | 78,000 | Yes | Yes | Yes |
| HIGHMEM\_16XL | 64 | 512GB | 78,000 | Yes | Yes | Yes |
| HIGHMEM\_24XL | 96 | 768GB | 78,000 | Yes | Yes | Yes |
| HIGHMEM\_32XL | 128 | 1TB | 78,000 | Yes | Yes | Yes |
| HIGHMEM\_48XL | 192 | 1.5TB | 78,000 | Yes | Yes | Yes |

Expand

Show lessSee more
