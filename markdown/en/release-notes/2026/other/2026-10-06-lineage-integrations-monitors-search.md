# Oct 6, 2026: Data lineage for storage integrations, external tables, model monitors, and Cortex Search services

[Data lineage](/user-guide/ui-snowsight-lineage) now includes the following relationships:

- A [storage integration](/sql-reference/sql/create-storage-integration) is upstream of each stage that uses it.
- A stage is upstream of each [external table](/user-guide/tables-external-intro) created on it.
- A model version is upstream of each [model monitor](/developer-guide/snowflake-ml/model-registry/model-observability)
  that observes it.
- A stage is upstream of the tables or dynamic tables that hold processed content for a
  [Cortex Search service created from that stage](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-overview-example-ui)
  in Snowsight, and those tables or dynamic tables are upstream of the service. Creating a Cortex Search service
  from a stage is in preview.

These relationships are recorded when the object is created, so they don’t appear for objects created before this
release. For a stage or external table, the relationship isn’t shown until you recreate the object. For a model monitor
created before this release, the relationship to its model version isn’t shown until you recreate the monitor. For a
Cortex Search service created from a stage before this release, the relationships to the stage aren’t shown until you
create the service from the stage again in Snowsight. Creating a service with `CREATE CORTEX SEARCH SERVICE`
doesn’t record these relationships.

For more information, see [Data Lineage](/user-guide/ui-snowsight-lineage).
