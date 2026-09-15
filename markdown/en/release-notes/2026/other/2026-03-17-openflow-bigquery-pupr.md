# Mar 17, 2026: Openflow Connector for Google BigQuery (*Preview*)

The Openflow Connector for Google BigQuery is now available in preview. The connector replicates
datasets, tables, and views from Google BigQuery into Snowflake. Tables
are synchronized using incremental change capture with BigQuery’s
native CHANGES function. Views are replicated using a truncate and load
strategy. The connector leverages the BigQuery Storage Read API for
high-throughput data transfer.

For more information, see
[About the Openflow Connector for Google BigQuery](/user-guide/data-integration/openflow/connectors/google-big-query/about).
