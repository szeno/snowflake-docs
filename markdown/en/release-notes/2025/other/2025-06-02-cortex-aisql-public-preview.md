# Jun 02, 2025: Snowflake Cortex AI Functions (*Preview*)

## AI capability meets SQL operators across multimodal data

Snowflake announces the preview of Cortex AI Functions, bringing powerful AI capabilities directly into Snowflake’s SQL engine.
AI Functions help you build scalable AI pipelines across multimodal enterprise data with familiar SQL
commands. You can now process text and images faster and more cost effectively while gaining deeper insights from
structured and unstructured data.

The available Cortex AI Functions include:

- [AI\_FILTER](/sql-reference/functions/ai_filter): Evaluates a plain-language yes-or-no question against text or
  image input, allowing you to filter results in SELECT, WHERE, and JOIN clauses using AI capabilities.
- [AI\_CLASSIFY](/sql-reference/functions/ai_classify): Classifies a text or image input into a single or multiple
  user-defined categories based on plain-language category definitions.
- [AI\_AGG](/sql-reference/functions/ai_agg): Aggregates a text column and returns insights across multiple rows
  based on a user-defined prompt. This function is not subject to context window limitations.
- [AI\_SUMMARIZE\_AGG](/sql-reference/functions/ai_summarize_agg): Aggregates a text column and returns a summary
  across multiple rows. This function is not subject to context window limitations.
- [AI\_SIMILARITY](/sql-reference/functions/ai_similarity): Calculates the embedding similarity between two inputs
  without needing to explicitly create the embedding vectors.
- [AI\_COMPLETE](/sql-reference/functions/ai_complete): Generates a completion for a given text string or image
  using one of several available LLMs. Use this function for generative AI tasks that aren’t covered by other functions.

Key benefits of Cortex AI Functions include:

- **Expressive and Composable AI Operators**: A new suite of AI-powered operators integrates seamlessly with familiar
  SQL primitives like FILTER and AGGREGATE, enabling more intuitive and powerful data manipulation.
- **Simplified AI Pipelines**: Build advanced, multi-step AI pipelines with greater ease and efficiency using standard
  SQL.
- **Unified Analytics for All Data**: Run analytics across structured and unstructured data within the same SQL query,
  breaking down data silos.
- **Native Multimodal Data Support**: Cortex AI Functions are designed to work fluidly across diverse modalities,
  eliminating the need for separate processing systems for text and image data.
- **Performance Enhancements**: Improved query engine performance and scalability within Snowflake.

To get started, see [Cortex AI Functions](/user-guide/snowflake-cortex/aisql).
