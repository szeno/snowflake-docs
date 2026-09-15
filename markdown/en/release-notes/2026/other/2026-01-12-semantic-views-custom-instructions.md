# Jan 12, 2026: Specifying custom instructions in semantic views

When defining a [semantic view](/user-guide/views-semantic/overview), you can now provide
[instructions for Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst/custom-instructions) that explain how to:

- Generate the SQL statement
- Classify questions and prompt for additional information

In the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command, you can use the AI\_SQL\_GENERATION and AI\_QUESTION\_CATEGORIZATION
clauses to specify instructions for generating the SQL statement and classifying questions.

For more information, see [Providing custom instructions for Cortex Analyst](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions).
