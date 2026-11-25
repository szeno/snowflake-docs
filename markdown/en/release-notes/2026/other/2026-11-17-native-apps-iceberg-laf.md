# Nov 17, 2026: Cross-Cloud Auto-Fulfillment for Native Apps that share Iceberg tables

Providers can enable Cross-Cloud Auto-Fulfillment for a Snowflake Native App listing that shares
Apache Iceberg™ tables when every Iceberg table the app exposes can be auto-fulfilled, including
tables reached through the `REFERENCE_USAGE` privilege. External tables in a Native App remain
unsupported for Cross-Cloud Auto-Fulfillment. This capability is included in Snowflake version
10.42.

For more information, see
[Cross-Cloud Auto-Fulfillment for external and Iceberg tables](/developer-guide/native-apps/preparing-data-content#label-native-apps-ext-table-laf)
and
[Limitations](/collaboration/use-auto-fulfillment-with-open-table-formats#label-auto-fulfillment-open-formats-limitations).
