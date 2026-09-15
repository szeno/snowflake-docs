# Best practices for semantic views

Best practices for [semantic views](/user-guide/views-semantic/overview) are organized into two guides, plus a set of
accuracy-tuning topics for Cortex Agents. Use this page to find the right one.

## Modeling

Design semantic views that produce accurate, trustworthy answers in Cortex Agents: scoping and organization,
high-quality descriptions, relationships, metrics and filters, and how to increase accuracy and iterate. See
[Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling).

## Developing and deploying

Manage semantic views as part of a data engineering pipeline or data product: ownership and data access (RBAC, masking,
and row access policies), creation and update options, automated (CI/CD) deployment, dbt, and BI integrations. See
[Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev).

## Increasing accuracy

Detailed guidance for the features that most improve Cortex Agents’ answer quality:

- Add verified (“gold”) queries — see [the verified query repository](/user-guide/views-semantic/verified-query-repository).
- Optimize a model from its verified queries — see [Optimize an existing semantic view or model with verified queries](/user-guide/snowflake-cortex/cortex-analyst/analyst-optimization).
- Steer SQL generation and question handling — see [custom instructions](/user-guide/views-semantic/custom-instructions).
- Improve literal matching with Cortex Search — see [the literal search guide](/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-search-integration).
