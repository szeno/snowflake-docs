# Snowpark Container Services: Azure instance families

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Instance families are grouped as current generation or previous generation.
Azure instance families are available in three types:

- **General Compute (GEN)**: Recommended for general-purpose containerized workloads.
- **High Memory (MEM)**: High memory-to-vCPU ratio for applications that require large amounts of RAM, such as CPU-based model serving, large-scale in-memory data processing, and vector index serving.
- **GPU Accelerated (GPU)**: For machine learning training, inference, and AI workloads requiring GPU acceleration.

For pricing information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Note

Instance family availability varies by region and can change over time. To list the instance families
available in the region of your current account, run
[SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families).
If an instance family you need isn’t listed, contact your Snowflake account team.

The **Node limit** column shows the default maximum number of nodes of each instance family that an account can use.
An account can also have at most 750 active or idle nodes in total, across all instance families. For more
information, see
[Guidelines and limitations](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-guidelines-limitations).

## Current generation instance families

### General compute instance families

Current generation instances recommended for general-purpose workloads.

#### x86 general compute

Current generation x86 instances for general-purpose workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit |
| --- | --- | --- | --- | --- | --- |
| GEN\_X64\_G2\_2 | 1 | 6 | 100 | 12.5 | 500 |
| GEN\_X64\_G2\_4 | 3 | 13 | 100 | 12.5 | 500 |
| GEN\_X64\_G2\_8 | 6 | 28 | 100 | 12.5 | 500 |
| GEN\_X64\_G2\_16 | 14 | 58 | 100 | 12.5 | 500 |
| GEN\_X64\_G2\_32 | 28 | 116 | 100 | 16.0 | 500 |

Expand

Show lessSee more

### High memory instance families

Current generation x86 instances optimized for memory-intensive workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit |
| --- | --- | --- | --- | --- | --- |
| MEM\_X64\_G2\_8 | 6 | 58 | 100 | 12.5 | 500 |
| MEM\_X64\_G2\_32 | 28 | 240 | 100 | 12.5 | 500 |
| MEM\_X64\_G2\_64 | 60 | 492 | 100 | 16.0 | 500 |
| MEM\_X64\_G2\_96 | 92 | 652 | 100 | 16.0 | 500 |

Expand

Show lessSee more

### GPU accelerated instance families

Azure GPU instance families feature three NVIDIA GPU architectures, each suited to different AI and ML workloads.

#### NVIDIA T4

Turing GPU for cost-effective inference and light ML workloads.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_NV\_XS | 3 | 26 | 100 | 8.0 | 1 NVIDIA T4 | 16 | 10 |

Expand

Show lessSee more

#### NVIDIA A10

Mid-range Ampere GPU for ML model development and inference on small to medium models.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_NV\_SM | 32 | 424 | 100 | 40.0 | 1 NVIDIA A10 | 24 | 10 |
| GPU\_NV\_2M | 68 | 858 | 100 | 80.0 | 2 NVIDIA A10 | 48 | 5 |

Expand

Show lessSee more

#### NVIDIA A100

High-throughput Ampere GPU for large-scale model training and large dataset processing.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_NV\_3M | 44 | 424 | 100 | 40.0 | 2 NVIDIA A100 | 160 | On Request |
| GPU\_NV\_SL | 92 | 858 | 100 | 80.0 | 4 NVIDIA A100 | 320 | On Request |

Expand

Show lessSee more

## Previous generation instance families

### General compute instance families

Previous generation x86 instances. For new workloads, use GEN\_X64\_G2 instances instead.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit |
| --- | --- | --- | --- | --- | --- |
| CPU\_X64\_XS | 1 | 6 | 100 | 12.5 | 500 |
| CPU\_X64\_S | 3 | 13 | 100 | 12.5 | 500 |
| CPU\_X64\_M | 6 | 28 | 100 | 12.5 | 500 |
| CPU\_X64\_SL | 14 | 58 | 100 | 12.5 | 500 |
| CPU\_X64\_L | 28 | 116 | 100 | 16.0 | 500 |

Expand

Show lessSee more

### High memory instance families

Previous generation x86 instances optimized for memory. For new workloads, use MEM\_X64\_G2 instances instead.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit |
| --- | --- | --- | --- | --- | --- |
| HIGHMEM\_X64\_S | 6 | 58 | 100 | 8.0 | 500 |
| HIGHMEM\_X64\_M | 28 | 240 | 100 | 16.0 | 500 |
| HIGHMEM\_X64\_SL | 60 | 492 | 100 | 32.0 | 500 |

Expand

Show lessSee more
