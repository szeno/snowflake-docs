# May 5, 2026: Four new Snowpark Container Services instance families (*General availability*)

With this release, four new instance families are generally available for Snowpark Container Services:

- **GEN\_X64\_G2** (AWS, Azure): Second-generation general-purpose compute, replacing CPU\_X64 as the
  recommended instance family for all new workloads.
- **MEM\_X64\_G2** (AWS, Azure): Second-generation high-memory compute, replacing HIGHMEM\_X64 as the recommended instance family for memory-intensive workloads.
- **GPU\_L40S** (AWS): NVIDIA L40S GPU (Ada Lovelace) with 48 GB VRAM per GPU, scaling up to
  8 GPUs (384 GB total).
- **GPU\_R6K** (AWS): NVIDIA RTX PRO 6000 GPU (Blackwell) with 96 GB VRAM per GPU, scaling up to
  8 GPUs (768 GB total).

Customers on CPU\_X64 or HIGHMEM\_X64 instances can upgrade by changing the instance family parameter in their
compute pool definition.

For pricing information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

For a complete list of available instance families and specifications, see
[Snowpark Container Services: Understanding Instance families](/developer-guide/snowpark-container-services/instance-families).
