# Snowpark Container Services: Google Cloud Instance Families

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Instance families are grouped by type: general compute, high memory, and GPU accelerated.
GCP instance families are available in three types:

- **General Compute (GEN)**: Recommended for general-purpose containerized workloads.
- **High Memory (MEM)**: High memory-to-vCPU ratio for applications that require large amounts of RAM, such as CPU-based model serving, large-scale in-memory data processing, and vector index serving.
- **GPU Accelerated (GPU)**: For machine learning training, inference, and AI workloads requiring GPU acceleration.

For pricing information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

Note

Region availability is subject to change. To retrieve current availability and
instance family specifications programmatically, use
[SHOW COMPUTE POOL INSTANCE FAMILIES](/sql-reference/sql/show-compute-pool-instance-families).

## Current Generation Instance Families

### General Compute Instance Families

Current generation instances recommended for general-purpose workloads.

#### x86 General Compute

Current generation x86 instances for general-purpose workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| CPU\_X64\_XS | 1 | 6 | 100 | 10.0 | 500 | Available everywhere |
| CPU\_X64\_S | 3 | 13 | 100 | 10.0 | 500 | Available everywhere |
| CPU\_X64\_M | 6 | 28 | 100 | 16.0 | 500 | Available everywhere |
| CPU\_X64\_SL | 14 | 58 | 100 | 32.0 | 500 | Available everywhere |
| CPU\_X64\_L | 28 | 116 | 100 | 32.0 | 500 | Available everywhere |

Expand

Show lessSee more

### High Memory Instance Families

Current generation x86 instances optimized for memory-intensive workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| HIGHMEM\_X64\_S | 6 | 58 | 100 | 16.0 | 500 | Available everywhere |
| HIGHMEM\_X64\_M | 28 | 240 | 100 | 32.0 | 500 | Available everywhere |
| HIGHMEM\_X64\_SL | 92 | 654 | 100 | 67.0 | 500 | Not available in me-central2 |

Expand

Show lessSee more

### GPU Accelerated Instance Families

GCP GPU instance families feature two NVIDIA GPU architectures, each suited to different AI and ML workloads.

#### NVIDIA L4

Ada Lovelace GPU for efficient AI inference and media workloads.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_GCP\_NV\_L4\_1\_24G | 6 | 28 | 100 | 16.0 | 1 NVIDIA L4 | 24 | 10 | Available everywhere |
| GPU\_GCP\_NV\_L4\_4\_24G | 44 | 178 | 100 | 50.0 | 4 NVIDIA L4 | 24 | 10 | Available everywhere |

Expand

Show lessSee more

#### NVIDIA A100

High-throughput Ampere GPU for large-scale model training and large dataset processing.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_A100\_G1\_12 | 10 | 77 | 100 | 10.0 | 1 NVIDIA A100 | 40 | On Request | Only available in us-central1 and europe-west4 |
| GPU\_A100\_G1\_48 | 44 | 324 | 100 | 50.0 | 4 NVIDIA A100 | 160 | On Request | Only available in us-central1 and europe-west4 |
| GPU\_GCP\_NV\_A100\_8\_40G | 92 | 654 | 100 | 100.0 | 8 NVIDIA A100 | 320 | On Request | Only available in us-central1 and europe-west4 |

Expand

Show lessSee more

## Previous Generation Instance Families

There are no previous generation instance families on Google Cloud. All listed instance families are current generation.
