# Snowflake Horizon Catalog

Horizon Catalog is the agentic catalog for all your data, whether it is inside or outside of Snowflake. It is open,
interoperable, and compatible with any engine, any data, and any cloud. You can find the right data fast, understand it through
rich semantic context, and trust every answer with enterprise-grade governance:
[sensitive data protection](/user-guide/classify-intro), [data quality](/user-guide/data-quality-intro),
[end-to-end lineage](/user-guide/ui-snowsight-lineage), [AI guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails), and
[AI governance](/user-guide/snowflake-cortex/governance-and-availability).

## Problems that Horizon Catalog solves

Organizations with data and AI agents spread across teams and systems face common challenges around discoverability,
context, and trust:

- **Disconnected data slows discovery.** When data is spread across disconnected silos and incompatible formats,
  neither AI agents nor human users can find the authoritative information they need.
- **AI requires governed, contextualized data.** Without business context, AI agents cannot distinguish authoritative
  assets from noise. This results in technically accurate but operationally irrelevant answers.
- **Fragmented security leaves gaps.** When access controls and lineage are siloed across systems, sensitive data
  becomes difficult to track and protect as it moves across formats and platforms.

## Connect your entire data estate

Horizon Catalog provides full interoperability across data inside and outside of Snowflake, with any engine, any data,
and any cloud.

[Apache Iceberg tables](/user-guide/tables-iceberg)
:   Read and write Iceberg tables from any engine. Supports both Snowflake-managed and external Iceberg tables.

[Iceberg REST Catalog API](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
:   Query Iceberg tables natively from Spark, Flink, and Trino through the Iceberg REST Catalog API. Governance is enforced automatically.

[External tables](/user-guide/tables-external-intro) and [catalog-linked databases](/user-guide/tables-iceberg-catalog-linked-database)
:   Connect to your Iceberg ecosystem, including AWS Glue and Azure OneLake, through catalog-linked databases.

[Internal Marketplace](/user-guide/collaboration/listings/organizational/org-listing-about)
:   Discover and share governed data products across teams without copying data.

## Build your AI context layer

Collect, enrich, and activate context across BI tools and data so that both humans and AI agents operate on the same
trusted semantics.

[Semantic views](/user-guide/views-semantic/overview)
:   Create governed, business-aligned definitions that AI agents use to understand your data. You can create them from scratch by using Autopilot, or ingest them from Tableau and Power BI.

[End-to-end data lineage](/user-guide/ui-snowsight-lineage)
:   Column-level lineage across Snowflake, external databases, BI tools, and OpenLineage feeds. You can trace any AI answer back to its exact data origin.

[Auto-generated descriptions](/user-guide/ui-snowsight-cortex-descriptions)
:   Snowflake Cortex generates table and column documentation from metadata and sample data, consistent across every engine.

[Object tagging](/user-guide/object-tagging/introduction)
:   Consistent metadata ensures that table definitions, query logs, joins, and lineage are presented the same way to every engine.

## Deploy governed, trustworthy AI

Governance policies execute at the query engine layer, not the application layer. They apply automatically to every
caller: human analyst, BI tool, or AI agent. There is no separate governance configuration for AI workloads.

[Data quality monitoring](/user-guide/data-quality-intro)
:   Continuous monitoring with root cause analysis ensures that every query, whether from a human or an AI agent, returns fresh and accurate data.

[Sensitive data classification](/user-guide/classify-intro)
:   Automatically discover and classify columns. Snowflake applies tags and policies without manual intervention as schemas evolve.

[Data protection policies](/user-guide/security-column-intro)
:   Masking and [row-access policies](/user-guide/security-row-intro) are enforced across any Iceberg REST Catalog-compatible engine.

[AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails)
:   Detect, redact, and block personally identifiable information (PII) and protected health information (PHI) from agent outputs. Agents operate under the same role-based access control (RBAC) policies as human users.

[Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
:   Version, tag, and govern ML models under the same RBAC model as tables, with training data lineage tracked end-to-end.

[Access control](/user-guide/security-access-control-overview)
:   Role-based access controls, [Time Travel](/user-guide/data-time-travel), and [access history](/user-guide/access-history) let you review past activity and data states. [Trust Center](/user-guide/trust-center/overview) continuously monitors for misconfigured roles and unprotected columns.

[Governance with Snowflake CoCo](/user-guide/governance-skills)
:   Configure governance policies in natural language, assess your governance and observability maturity with scoring skills, and get prioritized recommendations. No SQL expertise is required.

[Cross-engine policy enforcement](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies)
:   Governance policies follow your data to Iceberg tables and [Snowflake Marketplace](/collaboration/collaboration-marketplace-about). Shared data products carry their tags and permissions.

## Business continuity

You can [manage](/user-guide/account-replication-failover-failback) primary and secondary environments, keeping them
consistent through database and account replication across regions and accounts.
