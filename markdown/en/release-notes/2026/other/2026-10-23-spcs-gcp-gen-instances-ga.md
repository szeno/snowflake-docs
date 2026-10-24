# October 23, 2026: Snowpark Container Services GEN\_ARM\_G1 and GEN\_X64\_G1 instances on Google Cloud (*General availability*)

With this release, the GEN\_ARM\_G1 and GEN\_X64\_G1 instance families are generally available for Snowpark Container Services on Google Cloud.
Each family provides general-purpose compute in five sizes, from 1 vCPU to 28 vCPU.

- **GEN\_ARM\_G1** is a current generation ARM instance family for workloads with `linux/arm64` container images.
- **GEN\_X64\_G1** is a previous generation x86 instance family. For new x86 workloads, use CPU\_X64 instances.

To use these instances, specify a size-specific instance family, such as `GEN_ARM_G1_2` or `GEN_X64_G1_2`, when [creating a compute pool](/sql-reference/sql/create-compute-pool).

For pricing information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

For specifications of all Google Cloud instance families, see
[Snowpark Container Services: Google Cloud Instance Families](/developer-guide/snowpark-container-services/instance-families-gcp).
