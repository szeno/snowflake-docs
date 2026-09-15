# Dec 08, 2025: Snowpipe simplified pricing

Snowflake is extending a significant Snowpipe enhancement to Enterprise and Standard Edition Snowflake accounts. Starting December 8, 2025, you’ll benefit from a simpler, more predictable Snowpipe pricing model that may significantly lower your data ingestion costs for most types of workloads. This update is applied automatically to your account.

Instead of a per-second/per-core compute charge and a per-1,000-files fee, you are now charged a fixed credit amount per gigabyte (0.0037 credits per GB) of data ingested with Snowpipe. This pricing makes it easier for you to estimate your Snowpipe costs.

Data ingested is calculated in the following ways:

- Text files, such as CSV and JSON, are billed on their uncompressed size.
- Binary files, such as Parquet and Avro, are billed on their observed size.

For a complete breakdown of the updated billing documentation and cost verification guidance, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) and [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

Note

This simplified pricing model was previously rolled out to all Business Critical and VPS accounts on August 1, 2025. For more information, see [the previous release note](/release-notes/2025/9_21#label-simplified-snowpipe-pricing).
