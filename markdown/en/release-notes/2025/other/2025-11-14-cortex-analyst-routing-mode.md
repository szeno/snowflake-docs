# Nov 14, 2025: Cortex Analyst Routing Mode (*Preview*)

Routing Mode is a query strategy that prioritizes semantic SQL and falls back to standard SQL only when needed. It acts as a simpler version of SQL, with guardrails provided by semantic views. Routing mode uses semantic views to drive higher accuracy and consistency. As a result, metrics, joins, and filters follow governed definitions from the semantic view.

Routing Mode offers the following benefits:

- **Consistent metrics:** Queries use definitions from semantic views, not SQL.
- **Safer defaults:** Dimensions, metrics, and joins come from governed metadata.
- **LLM-friendly:** Shorter SQL is easier for an LLM to produce correctly.

For more information, see [Routing Mode for Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-routing-mode).
