# Nov 17, 2026: Data governance policy inheritance for Cortex Search (*Public Preview*)

Data governance policy inheritance for Cortex Search is now available in Public Preview. When you set
`INHERIT_DATA_GOVERNANCE_POLICIES = TRUE` on a Cortex Search service, the service honors the row access
policies and masking policies on its base table, so query results reflect each caller’s own access
instead of the service owner’s.

Inherited policies are enforced for queries that use the `CORTEX_SEARCH_BATCH` and `CORTEX_SEARCH_RETRIEVE`
SQL functions.

For more information, see [Data governance policy inheritance for Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-data-governance-inheritance).
