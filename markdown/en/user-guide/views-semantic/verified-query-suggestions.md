# Suggestions for semantic models and views

Suggestions help you enrich and improve your semantic models and views by identifying elements that appear useful based on real user behavior. These suggestions require human review before being added.

Cortex Analyst surfaces suggestions in contexts where it has enough information to propose new verified queries, filters, metrics, and other model elements.

Suggestions are not automatically applied. Instead, Cortex Analyst uses suggestions as a queue of potential improvements that you can accept, edit, or dismiss.

## Review suggestions

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Cortex Analyst**.
3. Select the semantic model or view you want to review suggestions for.
4. Review the suggestions on the right panel.
5. Select a suggestion to **Accept**, **Edit**, or **Dismiss**. Cortex Analyst only allows renaming, rewriting SQL, or updating descriptions depending on the type of suggestion.
6. Refresh the page to generate new suggestions. Some suggestions that are fetched from query history may take a few minutes to appear.

## Dismissing a suggestion

When you dismiss a suggestion, the dismissal is valid only for the current session. Refreshing the page may result in the return of previously dismissed suggestions.

## Types of suggestions

The following sections list all suggestion types, organized by their source.

### Suggestions from query history

Snowflake analyzes recent SQL query history available to the current role to discover frequently used or missing elements.

Note

All suggestions based on query history only appear after the model or view has accumulated sufficient query activity. If a query was either run far in the past or run recently in a database that gets a lot of new query traffic, it may be omitted.

### Verified query suggestions

These suggestions come from Cortex Analyst when it identifies queries that could be added to your Verified Query repository (VQR). Snowflake suggests up to 10 verified queries at a time. If you accept all suggestions, refresh the page to get more.

The criteria for these queries to be suggested are:

- **High frequency:** Queries similar to the candidate appear frequently.
- **Contains interesting semantic information:** Extremely simple queries are removed since they are unlikely to add value.
- **Novelty:** No existing verified query looks similar.

### Filter and metric suggestions

These suggestions analyze SQL query history to find frequently used SQL expressions that are not yet represented in the Semantic Model or view. Snowflake suggests up to 10 filters and 10 metrics at a time. If you accept all suggestions, refresh the page to get more.

The criteria for these queries to be suggested are:

- **High frequency:** Queries similar to the candidate appear frequently.
- **Novelty:** No existing verified query looks similar.

### Suggestions from usage data

Cortex Analyst aggregates recent user queries to make suggestions. If there are commonly asked questions by users of Cortex Analyst, Cortex Agents, or Snowflake CoWork that don’t match any existing verified queries, these questions get aggregated, grouped, and suggested in up to 10 verified query suggestions.

The criteria for these questions to be suggested are:

- Appears in Cortex Analyst monitoring tables. This includes questions from Cortex Agents and Snowflake CoWork by default.
- Frequently asked by users.

### Suggestions from optimization

Snowflake can optimize a semantic model or view from existing verified queries. This process produces different types of suggestions, including:

- Metrics
- Filters
- Custom Instructions
- Descriptions
- Synonyms
