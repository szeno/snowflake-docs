# Jan 16, 2026: External lineage (*Preview*)

External lineage extends Snowflake’s lineage capabilities by including external data sources and destinations, providing visibility into
data flows across your entire data ecosystem.

External lineage leverages the [OpenLineage](https://openlineage.io) framework, accepting OpenLineage-compatible
events through a REST endpoint. External tools like dbt and Apache Airflow can send lineage metadata to Snowflake,
which then incorporates this information into the native lineage graph displayed in Snowsight.

For more information, see [External lineage](/user-guide/external-lineage).
