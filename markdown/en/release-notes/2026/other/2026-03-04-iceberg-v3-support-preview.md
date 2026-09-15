# Mar 04, 2026: Support for Apache Iceberg™ version 3 (*Preview*)

Support for version 3 (v3) of the Apache Iceberg™ table specification is now in public preview.

The following data types are supported:

- `geography`
- `geometry`
- `nanosecond`
- `variant`

The following additional features are supported:

- **Default values**: Define default values for columns in Iceberg tables. For more information, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).
- **Deletion vectors**: Use deletion vectors to improve write performance. For more information, see [Deletion vectors](/user-guide/tables-iceberg-manage#tables-iceberg-deletion-vectors).
- **Row lineage**: Track row-level lineage information for data governance and auditing. For more information, see [Use row lineage with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-lineage).

You can read and write to v3 Iceberg tables by using these features with either Snowflake-managed or externally managed Iceberg tables.
Iceberg v3 support is integrated across the Snowflake platform, including streaming and batch ingestion, transformation, analytics, machine
learning, AI, business continuity and disaster recovery, external engine and catalog integrations, and more.

For more information, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).
