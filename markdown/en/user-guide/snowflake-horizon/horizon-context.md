# Horizon Context

Horizon Context is the governed context layer built into [Horizon Catalog](/user-guide/snowflake-horizon). It collects metadata from
across your data estate, enriches it with business meaning, and activates it so that people, BI tools, and AI agents all work from the
same trusted definitions.

Context doesn’t live in one place. It’s spread across your BI tools, your query history, your pipeline definitions, and the knowledge
your teams have built up over years. Horizon Context connects to those sources and keeps the results in one governed system. When an
AI agent queries data, Snowflake enforces the role’s [access control](/user-guide/security-access-control-overview), masking, and
row-access policies at the query engine. Access to metadata is managed separately from access to the underlying data.

## Why use Horizon Context?

A table name and a column list tell you what a dataset is called, not what it means or whether you should trust it. That gap is what
makes data hard to find, reports inconsistent, and AI answers unreliable.

Horizon Context addresses that gap in three ways:

- **One catalog for the whole estate.** Snowflake objects, external databases, BI dashboards, and pipeline models are described in one
  place, so you don’t have to know which system a dataset lives in before you can find it.
- **One set of definitions.** Business metrics, dimensions, and relationships are defined once in
  [semantic views](/user-guide/views-semantic/overview) and reused by every consumer, instead of being redefined in each dashboard and
  each prompt.
- **One governance model for data queries.** Snowflake applies the same role-based access control, masking, and row-access policies to
  queries from people, BI tools, and AI agents. Metadata visibility can require separate grants.

## Layers of context

Horizon Context gathers four kinds of context. Each layer answers a different question about a data asset, and an agent or analyst
usually needs all four to pick the right dataset and interpret it correctly:

| Layer | Question it answers | Examples |
| --- | --- | --- |
| Structural | What exists, and how is it connected? | Tables, columns, dashboards, joins, [lineage](/user-guide/ui-snowsight-lineage) |
| Operational | What’s happening to it? | Query history, freshness, [data quality](/user-guide/data-quality-intro) metrics |
| Semantic | What does it mean? | Business definitions, metrics, relationships in [semantic views](/user-guide/views-semantic/overview) |
| Behavioral | How is it used, and by whom? | Popularity, query patterns, downstream consumers |

Expand

Show lessSee more

## How Horizon Context works

Horizon Context works in three stages: it collects raw context, enriches it with business meaning, and activates it for the tools and
agents that consume your data.

### Collect

Snowflake continuously gathers metadata from objects in your account. To cover the rest of your estate, Horizon Context adds two more
sources:

Metadata connectors
:   Depending on the connector and its configuration, out-of-the-box connectors collect schemas, query logs, dashboard definitions, and
    popularity data from external databases, BI tools, and data pipeline systems, including PostgreSQL, SQL Server, Tableau, Power BI, and
    dbt. Metadata connectors are in private preview. Contact your account team for availability and setup details.

[External lineage](/user-guide/external-lineage)
:   Any OpenLineage producer, such as Apache Airflow, can post lineage events to a Snowflake REST endpoint. Snowflake folds those events
    into the same lineage graph it builds from its own query history.

### Enrich

Collected metadata becomes useful only after it carries business meaning. Horizon Context enriches it with the following:

[Semantic views](/user-guide/views-semantic/overview)
:   Governed, business-aligned definitions of your metrics, dimensions, and relationships. You can build them in
    [Semantic Studio](/user-guide/views-semantic/semantic-studio), generate them with
    [Autopilot](/user-guide/views-semantic/autopilot), or ingest them from
    [Tableau](/user-guide/views-semantic/tableau-ingestion) and [Power BI](/user-guide/views-semantic/power-bi-ingestion) files.

[Auto-generated descriptions](/user-guide/ui-snowsight-cortex-descriptions)
:   Snowflake Cortex writes table and column documentation from metadata and sample data, so undocumented objects don’t stay that way.

[Object tagging](/user-guide/object-tagging/introduction)
:   Tags record project, sensitivity, environment, and certification status. Snowflake-provided tags give you a consistent vocabulary
    across every account. For more information, see [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags).

[End-to-end lineage](/user-guide/ui-snowsight-lineage)
:   Snowflake stitches lineage mined from Snowflake query history, external query logs, BI systems, and OpenLineage feeds into a single
    column-level graph.

### Activate

Enriched context is only valuable when something consumes it. The same context layer serves the following:

- People browsing the catalog in Snowsight or searching with
  [Universal Search](/user-guide/ui-snowsight-universal-search).
- [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) and [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst),
  which answer natural language questions against semantic views.
- [Snowflake CoCo](/user-guide/cortex-code/cortex-code), which uses catalog context when it writes SQL, traces lineage, or reviews
  governance posture.
- BI tools and applications that read semantic definitions instead of reimplementing them.

## Example use cases

### 1. See metadata and cross-platform lineage for data outside Snowflake

A retail analytics team runs reporting on Snowflake, but raw orders land in PostgreSQL first, dbt builds the transformation layer, and
executives read the results in Tableau. Nobody can answer a simple question, such as which dashboard a given PostgreSQL column ends up
in, without opening three tools.

With metadata connectors configured for PostgreSQL, dbt, and Tableau, Horizon Context collects the schemas, query logs, model
definitions, and dashboard definitions from each system and indexes them alongside Snowflake objects. Lineage from all of those sources
is stitched into one column-level graph, so the team can start at a PostgreSQL column and follow it through dbt models and Snowflake
tables to the Tableau dashboards that display it.

Metadata connectors are in private preview. Contact your account team to find out which connectors are available to you. If your
pipelines emit OpenLineage events, you can send them to Snowflake today. For more information, see [External lineage](/user-guide/external-lineage).

### 2. Certify trusted assets so that search and AI point to them

A finance organization has seven tables with `revenue` in the name. Three are sandbox copies, two are staging, and only one is the
table that the close process uses. New analysts pick the wrong one, and so do AI agents.

A data steward applies the `SNOWFLAKE.TAGS.CERTIFICATION_STATUS` tag to mark the authoritative table `'CERTIFIED'` and the sandbox
copies `'DEPRECATED'`. Because the tag’s allowed values are fixed and can’t be modified, every account interprets them the same way,
and governance and AI workflows can act on them without custom mapping.

Certification then pays off in two places:

- **Search and discovery.** [Universal Search](/user-guide/ui-snowsight-universal-search) searches object and column tags along with
  names and comments, so searches can match certification status as part of an asset’s metadata.
- **AI understanding.** Agents that retrieve context from the catalog get an explicit, machine-readable trust signal that separates the
  production table from the sandbox copies, instead of guessing from the table name.

Pair certification with [auto-generated descriptions](/user-guide/ui-snowsight-cortex-descriptions) and a
[semantic view](/user-guide/views-semantic/overview) over the certified table. The description explains what the asset holds, the
semantic view defines how to aggregate it, and the certification tag says it’s the one to use. For more information about the tag and
its allowed values, see [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags).

### 3. Run cross-platform impact analysis with Snowflake CoCo

A data engineer needs to drop a column from a staging table. The Snowflake dependencies are easy enough to find, but the risk is in
what sits beyond Snowflake: a dbt model that selects the column and an executive dashboard built on the result.

Because Horizon Context already stitches lineage from Snowflake, external databases, BI tools, and OpenLineage feeds into one graph,
the engineer doesn’t have to assemble that picture by hand. They can ask [Snowflake CoCo](/user-guide/cortex-code/cortex-code) a
question in natural language, such as “What will break if I change `raw_db.sales.orders`?” CoCo reads the same lineage that the catalog
exposes and reports the downstream objects, ranked by risk, along with how often each is queried and how many users it affects.

The same lineage supports the reverse question. When a dashboard shows a number that looks wrong, CoCo can trace the value upstream
through the transformation layers and flag recent schema or data changes along the path.

For the lineage skill and its example prompts, see [Lineage](/user-guide/governance-skills#label-dg-skills-lineage). For the full set of
skills available to CoCo, see [CoCo CLI bundled skills](/user-guide/cortex-code/bundled-skills).

## Getting started

1. Review what the catalog already knows about your Snowflake objects. Browse them in Snowsight and check the
   [lineage graph](/user-guide/ui-snowsight-lineage) for a table your team depends on.
2. Fill in the gaps outside Snowflake. Configure [external lineage](/user-guide/external-lineage) for pipelines that emit OpenLineage
   events, and ask your account team about metadata connectors for your external databases and BI tools.
3. Enrich what you collected. Generate [descriptions](/user-guide/ui-snowsight-cortex-descriptions) for undocumented objects, and
   apply [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags) to record project, sensitivity, and
   certification status.
4. Define your business logic once. Create [semantic views](/user-guide/views-semantic/overview) for the metrics your organization
   reports on, starting with the ones that are defined inconsistently today.
5. Put the context to work. Add semantic views as tools on [an agent](/user-guide/snowflake-cortex/cortex-agents), and use
   [Snowflake CoCo](/user-guide/cortex-code/cortex-code) for lineage, impact analysis, and
   [governance](/user-guide/governance-skills) tasks.

## Additional information

- [Snowflake Horizon Catalog](/user-guide/snowflake-horizon)
- [Overview of semantic views](/user-guide/views-semantic/overview)
- [Data Lineage](/user-guide/ui-snowsight-lineage)
- [External lineage](/user-guide/external-lineage)
- [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags)
- [Generate descriptions with Snowflake Cortex](/user-guide/ui-snowsight-cortex-descriptions)
- [Search Snowflake objects and resources](/user-guide/ui-snowsight-universal-search)
- [Data governance skills for Cortex Code](/user-guide/governance-skills)
