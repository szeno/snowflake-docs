# Optimize an existing semantic view or model with verified queries

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Snowflake allows you to optimize existing semantic views and models using only verified queries, by analyzing your verified queries to find useful information to add to the rest of the semantic layer. This optimization helps Cortex Analyst answer a broader range of questions correctly, not just those that match existing verified queries.

Consider this verified query: “How many active users did we have last month?” Cortex Analyst uses the verified SQL to determine how you’re defining *active*. From there, it can suggest the addition of an “is\_active” filter on the customer table, using that exact definition of *active users*. This filter then gives Cortex Analyst more accurate results for queries about “active users”.

This optimization feature is part of an iteration feedback loop that helps Cortex Analyst improve its accuracy and coverage over time:

1. Cortex Analyst suggests common and useful user questions for addition based on usage data and query history.
2. Users verify the suggested queries and add them to the list of verified queries.
3. Cortex Analyst uses these verified queries to generate more generalizable semantic model concepts and improve suggested queries.

## Prerequisites

- Ensure that you have the CORTEX\_USER role, which is granted by default, directly or indirectly. Secondary roles are not valid for this purpose.
- Have access to at least one large language model (LLM). We recommend using Claude Sonnet 4, but you can use any other LLM.
- Ensure that you have read access to the underlying tables and columns that you will interact with using Cortex Analyst.
- Have an existing semantic view or model with at least one [verified query](/user-guide/views-semantic/verified-query-repository).

  Note

  Cortex Analyst can learn more from unique verified queries using optimization. Simple queries may not have as much useful information.

  - You can use the suggestions panel to get ideas for useful verified queries to add.
  - Adding more than 20 verified queries can cause the optimization feature to take longer.

## Use optimization

To use optimization, select a warehouse that can run your verified queries without too much delay. Cortex Analyst might execute verified queries up to four times per verified query. The process can take from a few minutes for a small number of verified queries to hours for dozens of slow-running verified queries.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Cortex Analyst**.
3. From the list, select the semantic view or model to optimize.
4. In the right pane under **Suggestions**, select **Get more suggestions**.
5. Select the role that will run optimization.
6. Select the warehouse that will run verified queries.
