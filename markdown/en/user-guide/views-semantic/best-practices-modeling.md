# Best practices for modeling semantic views

High-quality semantic views are the foundation for accurate, intuitive, and trustworthy answers in
[Cortex Agents](/user-guide/snowflake-cortex/cortex-agents). This section describes best practices for *designing and
modeling* semantic views: how to scope them, describe them, and iterate on them so that Cortex Agents generates correct SQL.

These recommendations apply whether you author a semantic view manually or generate one with
[Semantic View Autopilot](/user-guide/views-semantic/autopilot), which is the fastest way to produce a high-quality
starting point. If you prefer to build semantic views programmatically, for example in a CI/CD pipeline, see
[Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql) and [Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev). This section covers the following
topics:

- [Design principles](#label-semantic-views-modeling-design-principles)
- [Scope and organization](#label-semantic-views-modeling-scope)
- [Write high-quality descriptions](#label-semantic-views-modeling-descriptions)
- [Synonyms](#label-semantic-views-modeling-synonyms)
- [Define relationships](#label-semantic-views-modeling-relationships)
- [Define metrics and filters](#label-semantic-views-modeling-metrics-filters)
- [Increase accuracy after initial setup](#label-semantic-views-modeling-increase-accuracy)
- [Test and iterate](#label-semantic-views-modeling-test-iterate)
- [Common pitfalls to avoid](#label-semantic-views-modeling-pitfalls)
- [Production-ready checklist](#label-semantic-views-modeling-checklist)

Note

This section addresses best practices for *modeling* semantic views. For guidance on managing semantic views as part of a
data engineering pipeline or data product, ownership and access, deployment, dbt, and BI integrations, see
[Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev).

## Design principles

Design from the perspective of your end users, not the database. When you model a semantic view, ask: “If I were explaining
this data to a business stakeholder, how would I describe it?” Use business terminology rather than technical table and
column names.

**Organize by business domain.** Structure semantic views around a business topic or domain — for example, Sales, Marketing,
or Customer Support — and split by use case rather than by data structure. Keep each model focused instead of trying to cover
everything in a single semantic view.

- Good: a *Sales Performance* semantic view, a *Customer Support Metrics* semantic view, a *Marketing Campaign Analysis* semantic view.
- Avoid: a single “All CRM Tables” semantic view.

## Scope and organization

**Start small.** Even though Cortex Agents no longer imposes hard limits on semantic view size, begin with 5–10 tables
for an initial proof of concept to keep debugging manageable. A simple star schema (a central fact table joined to
dimension tables) is a good starting point. Expand as the use case grows.

**Keep the semantic view under about 100,000 tokens.** There’s no hard limit on semantic view size, but larger semantic
views carry more risk. As a semantic view grows past roughly 100,000 tokens, the combined size of the semantic view, the
agent’s instructions, and the conversation history is more likely to approach the LLM’s context window. At that point,
Cortex Agents may need to *prune* the semantic view to make it fit, which adds latency and can reduce answer quality.
Staying under about 100,000 tokens minimizes the chance of pruning. Treat this as a guideline rather than a fixed
threshold: the effective limit depends on your conversation history length, agent instructions, and the LLM’s context
window.

**Include only business-relevant columns.** Add columns that will actually be used in SQL generation. Apply the litmus
test: *“Will my end users ask about this?”* Excluding irrelevant columns keeps the model concise and improves accuracy.

**Choose between one large semantic view and multiple semantic views.** As a semantic view grows, consider whether to split it:

- Prefer a single, larger semantic view when you have densely connected tables that are frequently joined, a single
  business domain with many related tables, or you’re using large context window models where pruning enables larger semantic views.
- Prefer multiple semantic views when you have distinct business domains that don’t need to be joined, or different user
  groups that need different views of the data.

When you use multiple semantic views, Cortex Agents selects the most relevant semantic view for each question. Keep the
following in mind:

- Write clear, distinct descriptions for each semantic view. Multiple very similar descriptions reduce selection accuracy.
- Split by use case (for example, Sales vs. Legal vs. Marketing), not by similarity.
- Each semantic view is queried independently; Cortex Agents does not join across separate semantic views.
- Selecting among semantic views adds slight latency (a few seconds for reranking).

Customers have run Cortex Agents successfully with 50 or more semantic views in production, but fewer semantic views
generally perform better.

## Write high-quality descriptions

Descriptions are the single most important element for accuracy. Large language models can’t reliably infer proprietary
terms, abbreviations, or business logic, so explicit, authoritative descriptions directly determine answer quality.

Write a clear business description for every table and every column. Explain proprietary terms and legacy names.

Table description:

Copy code

```
# Good
description: "Daily sales data by product line, aligned with 'Cost of Goods Sold' (COGS) and forecasted revenue. Use this table to analyze sales trends and profit by product."

# Poor — too vague
description: "Sales table"
```

Column description:

Copy code

```
# Good
- name: csat_score
  description: "Customer Satisfaction Score (CSAT): measures customer satisfaction on a scale of 1-5, where 5 is most satisfied. Also referred to as KPI_1 in legacy systems."

# Poor — assumes knowledge
- name: csat_score
  description: "Score"
```

## Synonyms

Current guidance is to avoid synonyms unless you have unique or industry-specific terms that the model is unlikely to know.
Recent evaluations with frontier models show that synonyms generally add little accuracy and typically consume tokens
without meaningful benefit. Reserve them for internal terminology, abbreviations, or legacy names, and add them manually
rather than auto-generating them: auto-generated synonyms often reduce semantic view quality.

For instructions on adding synonyms in Semantic Studio, see [Semantic Studio](/user-guide/views-semantic/semantic-studio). Synonyms remain
available in the [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec) for these edge cases.

## Define relationships

Cortex Agents does not join tables unless the relationships are explicitly defined in the semantic view. Make sure to
define all relationships your questions require. For relationship syntax, see the
[YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec) or
[Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).

**Many-to-many relationships** are not directly supported. As a workaround, introduce a shared dimension (bridge) table so
that two many-to-one relationships simulate the many-to-many behavior.

## Define metrics and filters

Metrics and filters are often underused, but they are critical for accuracy and consistency. Define them wherever possible.
Where your workflow offers **Get more suggestions** (often driven by high-quality verified queries), use it to discover
additional metrics and filters.

Metrics are pre-defined calculations:

Copy code

```
metrics:
  - name: total_revenue
    description: "Sum of all order revenue, calculated as unit price × quantity"
    expr: SUM(unit_price * quantity)
  - name: average_order_value
    description: "Average revenue per order"
    expr: SUM(revenue) / COUNT(DISTINCT order_id)
```

Filters describe reusable WHERE-clause logic:

Copy code

```
filters:
  - name: active_customers
    description: "Customers with purchases in the last year"
    expr: last_purchase_date >= DATEADD(year, -1, CURRENT_DATE())
```

For more information about defining and using filters, see [Defining filters for logical tables in a semantic view](/user-guide/views-semantic/filters). For the full metric and
filter syntax, see the [YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec).

## Increase accuracy after initial setup

Once your basic structure is in place, the following features separate a working proof of concept from a trusted production
model. Each has a dedicated topic; use the summaries below to decide what to apply, then follow the links for detailed
instructions.

### Verified queries

Verified queries are examples of questions paired with validated “gold” SQL. They improve accuracy on similar questions,
can reduce latency, and let Cortex Agents generalize from them to suggest filters, metrics, and descriptions.

Add verified queries after your tables, columns, and descriptions are solid — use them to optimize latency and cover
special cases, not to compensate for an incomplete model. Start with your most common questions and add more based on real
usage over time. For details, see [the verified query repository](/user-guide/views-semantic/verified-query-repository)
and [Optimize an existing semantic view or model with verified queries](/user-guide/snowflake-cortex/cortex-analyst/analyst-optimization).

### Custom instructions

Custom instructions let you control SQL generation and question handling in natural language. There are two categories, and
the most common mistake is mixing them up:

- **SQL generation** instructions apply during SQL generation for all queries — for example, business-specific logic,
  default filters, fiscal-year definitions, or data quirks.
- **Question categorization** instructions apply only to question understanding — for example, when to reject a question or
  ask a clarifying question.

Be specific (“If no date filter is provided, apply a filter for the last year” rather than “Filter queries for the last
year”), and always test after adding an instruction: the playground is a quick way to check changes. For details and
examples, see [custom instructions](/user-guide/views-semantic/custom-instructions).

### Cortex Search services

A Cortex Search service enables fuzzy matching for text columns where user input won’t exactly match your data, for
example, product names (“iPhone 13” vs. “Apple iPhone 13 - 128GB Blue”), customer names, or company names. As a general
rule, configure a Cortex Search service for high-cardinality text columns (more than about 10 distinct values), and provide
representative sample values for low-cardinality dimensions.

Avoid using search services with numeric or date columns, or with paragraph-style text fields such as notes, descriptions,
or comments. For setup instructions and the cardinality guidance in full, see
[the literal search guide](/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-search-integration).

## Test and iterate

Treat modeling as an iterative loop rather than a one-time setup.

1. **Create an evaluation set.** Start with about 10 representative benchmark questions sourced from business users, existing
   dashboards, or actual usage. Cover different complexity levels and use cases.
2. **Measure accuracy.** Run [native evaluations](/user-guide/snowflake-cortex/cortex-analyst-evaluations) in Snowflake to
   score SQL correctness against your verified queries.
3. **Close the loop.** Use suggestion panels and feedback data to add verified queries from real usage, then refine metrics,
   filters, custom instructions, and descriptions to match how users actually ask questions. See
   [Suggestions for semantic models and views](/user-guide/views-semantic/verified-query-suggestions) and
   [Optimize an existing semantic view or model with verified queries](/user-guide/snowflake-cortex/cortex-analyst/analyst-optimization).

## Common pitfalls to avoid

Undefined scope.
:   Stakeholders keep adding “just one more thing” to the proof of concept. Define crisp success criteria upfront with clear
    boundaries.

Starting too big.
:   Trying to model an entire enterprise data warehouse from day one. Start with 5–10 tables, one business domain, and a
    specific use case.

Over-relying on verified queries.
:   Adding many verified queries to patch a weak model. Get your tables, columns, and descriptions right first, then add
    verified queries to optimize latency and cover special cases.

Wrong initial use case.
:   Starting with a domain such as Finance or Legal where near-100% accuracy is required. Begin with lower-stakes domains like
    Sales or Marketing.

## Production-ready checklist

Foundation:

- Every table has a clear business description.
- Every column has a clear description.
- Proprietary terms and abbreviations are explained.

Critical features:

- Verified queries cover common questions and known edge cases.
- Custom instructions capture business-specific logic.
- Cortex Search services are configured for high-cardinality text columns.
- Metrics are defined for reusable calculations.
- Filters are defined for common conditions.

Testing (recommended before deployment):

- An evaluation set has been created.
- SQL accuracy has been measured with an evaluation tool.

Ongoing optimization:

- Suggestions and feedback data are reviewed on a regular cadence (for example, weekly).
- A process for adding new verified queries and related suggestions is in place.
