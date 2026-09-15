# Snowpark Container Services: AWS Instance Families

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Instance families are grouped as current generation or previous generation. AWS instance families are available in three types:

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
| GEN\_X64\_G2\_2 | 1 | 6 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1 |
| GEN\_X64\_G2\_4 | 3 | 13 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1 |
| GEN\_X64\_G2\_8 | 6 | 28 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1 |
| GEN\_X64\_G2\_32 | 28 | 116 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1 |

Expand

Show lessSee more

#### ARM General Compute

Current generation ARM instances for general-purpose workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| GEN\_ARM\_G1\_2 | 1 | 6 | 100 | 12.5 | 150 | Not available in us-gov-west-1, us-gov-east-1, cn-northwest-1 |
| GEN\_ARM\_G1\_4 | 3 | 13 | 100 | 12.5 | 150 | Not available in us-gov-west-1, us-gov-east-1, cn-northwest-1 |
| GEN\_ARM\_G1\_8 | 6 | 28 | 100 | 15.0 | 150 | Not available in us-gov-west-1, us-gov-east-1, cn-northwest-1 |
| GEN\_ARM\_G1\_16 | 14 | 58 | 100 | 15.0 | 150 | Not available in us-gov-west-1, us-gov-east-1, cn-northwest-1 |
| GEN\_ARM\_G1\_32 | 28 | 116 | 100 | 15.0 | 150 | Not available in us-gov-west-1, us-gov-east-1, cn-northwest-1 |

Expand

Show lessSee more

Note

ARM instances require container images built for the `linux/arm64` platform.
x86 instances require `linux/amd64`. For multi-architecture deployments, use
multi-platform container images.

### High Memory Instance Families

Current generation x86 instances optimized for memory-intensive workloads.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| MEM\_X64\_G2\_8 | 6 | 58 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1, eu-central-2, me-central-1 |
| MEM\_X64\_G2\_32 | 28 | 240 | 100 | 12.5 | 150 | Not available in af-south-1, cn-northwest-1, eu-central-2, me-central-1 |
| MEM\_X64\_G2\_64 | 60 | 492 | 100 | 25.0 | 150 | Not available in af-south-1, cn-northwest-1, eu-central-2, me-central-1 |
| MEM\_X64\_G2\_192 | 188 | 1436 | 100 | 50.0 | 150 | Not available in af-south-1, cn-northwest-1, eu-central-2, me-central-1 |

Expand

Show lessSee more

### GPU Accelerated Instance Families

AWS GPU instance families feature four NVIDIA GPU architectures, each suited to different AI and ML workloads.

#### NVIDIA A10G

Mid-range Ampere GPU for ML model development and inference on small to medium models.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_NV\_S | 6 | 28 | 450 | 10.0 | 1 NVIDIA A10G | 24 | 150 | Not available in ap-southeast-1, eu-central-2, eu-west-3, ap-northeast-3 |
| GPU\_NV\_M | 44 | 178 | 3800 | 40.0 | 4 NVIDIA A10G | 96 | 10 | Not available in Gov Regions, ap-southeast-1, eu-central-2, eu-west-3, ap-northeast-3 |

Expand

Show lessSee more

#### NVIDIA A100

High-throughput Ampere GPU for large-scale model training and large dataset processing.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_NV\_L | 92 | 1112 | 100 | 400.0 | 8 NVIDIA A100 | 320 | On Request | Available only in AWS US West and US East non-gov regions; limited availability in other regions upon request |

Expand

Show lessSee more

#### NVIDIA L40S

Ada Lovelace GPU optimized for GenAI inference and fine-tuning.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_L40S\_G1\_8 | 6 | 58 | 450 | 25.0 | 1 NVIDIA L40S | 48 | 5 | Only available in us-east-1, us-east-2, us-west-2, eu-central-1, eu-north-1, ap-northeast-1, ap-northeast-2 |
| GPU\_L40S\_G1\_16 | 14 | 116 | 600 | 25.0 | 1 NVIDIA L40S | 48 | 5 | Only available in us-east-1, us-east-2, us-west-2, eu-central-1, eu-north-1, ap-northeast-1, ap-northeast-2 |
| GPU\_L40S\_G1\_48 | 44 | 368 | 3800 | 100.0 | 4 NVIDIA L40S | 192 | On Request | Only available in us-east-1, us-east-2, us-west-2, eu-central-1, eu-north-1, ap-northeast-1, ap-northeast-2 |
| GPU\_L40S\_G1\_192 | 188 | 1436 | 3800 | 400.0 | 8 NVIDIA L40S | 384 | On Request | Only available in us-east-1, us-east-2, us-west-2, eu-central-1, eu-north-1, ap-northeast-1, ap-northeast-2 |

Expand

Show lessSee more

#### NVIDIA RTX PRO 6000

Blackwell GPU with 96GB VRAM per GPU for large-scale inference and data-intensive workloads.

| Instance Family | vCPU | Memory (GiB) | NVMe Storage (GB) | Bandwidth limit (Gbps) | GPU | GPU Memory per Instance (GB) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPU\_R6K\_G1\_8 | 6 | 58 | 1900 | 50.0 | 1 NVIDIA RTX PRO 6000 | 96 | 5 | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |
| GPU\_R6K\_G1\_16 | 14 | 116 | 1900 | 50.0 | 1 NVIDIA RTX PRO 6000 | 96 | 5 | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |
| GPU\_R6K\_G1\_32 | 28 | 240 | 1900 | 100.0 | 1 NVIDIA RTX PRO 6000 | 96 | 5 | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |
| GPU\_R6K\_G1\_48 | 44 | 490 | 3800 | 400.0 | 2 NVIDIA RTX PRO 6000 | 192 | On Request | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |
| GPU\_R6K\_G1\_96 | 92 | 984 | 7600 | 800.0 | 4 NVIDIA RTX PRO 6000 | 384 | On Request | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |
| GPU\_R6K\_G1\_192 | 188 | 1843 | 11400 | 1600.0 | 8 NVIDIA RTX PRO 6000 | 768 | On Request | Only available in us-west-2, us-east-1, us-east-2, ap-northeast-1 |

Expand

Show lessSee more

## Previous Generation Instance Families

### General Compute Instance Families

Previous generation x86 instances. For new workloads, use GEN\_X64\_G2 instances instead.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| CPU\_X64\_XS | 1 | 6 | 100 | 12.5 | 500 | Available everywhere |
| CPU\_X64\_S | 3 | 13 | 100 | 12.5 | 500 | Available everywhere |
| CPU\_X64\_M | 6 | 28 | 100 | 12.5 | 500 | Available everywhere |
| CPU\_X64\_SL | 14 | 58 | 100 | 12.5 | 500 | Not available in China |
| CPU\_X64\_L | 28 | 116 | 100 | 12.5 | 500 | Available everywhere |

Expand

Show lessSee more

### High Memory Instance Families

Previous generation x86 instances optimized for memory. For new workloads, use MEM\_X64\_G2 instances instead.

| Instance Family | vCPU | Memory (GiB) | Storage (GB) | Bandwidth limit (Gbps) | Node limit | Region Availability |
| --- | --- | --- | --- | --- | --- | --- |
| HIGHMEM\_X64\_S | 6 | 58 | 100 | 12.5 | 500 | Available everywhere |
| HIGHMEM\_X64\_M | 28 | 240 | 100 | 12.5 | 500 | Available everywhere |
| HIGHMEM\_X64\_L | 124 | 984 | 100 | 50.0 | 500 | Available everywhere |

Expand

Show lessSee more
