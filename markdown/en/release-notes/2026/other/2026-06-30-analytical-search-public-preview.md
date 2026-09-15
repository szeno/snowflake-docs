# Jun 30, 2026: Analytical search (*Public Preview*)

Analytical search, an orchestration capability in Cortex Agents that enables analytical queries over large document collections, is now in Public Preview.

Traditional retrieval-augmented generation (RAG) approaches retrieve a small number of passages, which limits their ability to answer questions requiring comprehensive analysis, such as counts, aggregates, or trends across thousands of documents. Analytical search addresses this by orchestrating multi-index Cortex Search queries with configurable result limits, metadata-based filtering, and AISQL (AI\_FILTER, AI\_AGG) to analyze the full result set precisely.

Example queries analytical search enables:

- “List all patients who were prescribed albuterol for asthma last year.”
- “What percentage of sales calls mentioned product X in EMEA versus the US?”
- “What new themes emerged in 2025 compared to 2024?”

For more information, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search).
