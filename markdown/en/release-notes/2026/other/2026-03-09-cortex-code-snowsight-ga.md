# Mar 9, 2026: Cortex Code in Snowsight - *General availability*

Cortex Code is now generally available in Snowsight, bringing an agentic assistant directly into Snowflake
for SQL and Python development, end-to-end machine learning, data exploration, and account administration.

Because it is integrated into Snowsight and Workspaces, it provides context-aware assistance within
the active workspace and helps users complete development, exploration, and admin tasks without leaving Snowsight.

That changes the day-to-day experience for both technical and business users. Instead of treating AI as
a separate tool, teams can use natural language inside the same platform where they already build and operate.
And because Cortex Code works using Snowflake’s existing policies and role-based access controls, organizations
can accelerate work without stepping outside their secure and governed environment.

## Why this matters

- **Faster coding, without giving up control.**
  In Workspaces, Cortex Code can generate, modify, optimize, and explain SQL and Python code, preview proposed
  edits in a diff view before changes are applied, and let users add tables, schemas, or views as inline context
  with `@` mentions. It can also suggest fixes when a SQL statement fails.
- **A shorter path from idea to production.**
  Cortex Code provides verified solutions in the form of fully functional ML pipelines that can be directly
  executed from a Snowflake Notebook in Workspaces. For dbt Projects on Snowflake, it can help explore source
  data, scaffold models, add tests, run dbt commands, and generate documentation.
- **Better discovery across data and documentation.**
  Cortex Code uses Horizon Catalog context and Snowflake documentation to help users find tables and columns
  with plain-language questions, answer product and SQL questions from official documentation, and surface
  metadata such as tags, masking policies, and lineage when available. It also supports semantic-model-oriented
  workflows for Cortex Analyst.
- **Smarter governance and cost conversations.**
  Teams can ask about user and role access, data ownership, and tables containing PII, while also querying
  account usage, credit consumption, and the warehouses or queries driving spend.

Because Cortex Code is embedded in Snowsight, users can get assistance without switching tools or
leaving the environment where they write and run queries.

For details, see [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight).

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
