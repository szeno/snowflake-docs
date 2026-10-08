# Oct 7, 2026: Snowflake Decision with AI\_COMPLETE (*Private Preview*)

With this release, we introduce the private preview of Snowflake Decision, a model available through
[AI\_COMPLETE](/sql-reference/functions/ai_complete) that evaluates text and structured data against user-defined
questions. The `snowflake-decision` model supports classification, rubric-based scoring, and true-or-false assessment,
returning structured answers with probabilities for downstream application logic.

Snowflake Decision supports the following question types:

- **Choice:** Selects an option from a fixed set and returns the selected key, a probability for each option, and
  confidence.
- **Score:** Evaluates content against an ordered rubric and returns a probability-weighted score, a probability for
  each level, and confidence.
- **True-or-false assessment:** Returns the probability that a specified statement is true.

You can combine multiple assessments of the same content in one request and evaluate rows across a table or query
result in a single SQL statement. Applications can use the returned probabilities and confidence values to route
results to automated actions, human review, or a fallback.

For example, a support-ticket workflow can select the responsible department, score customer frustration, and assess
urgency in one call.

For more information, see
[Snowflake Decision with AI\_COMPLETE](/LIMITEDACCESS/snowflake-cortex/ai-complete-snowflake-decision).
