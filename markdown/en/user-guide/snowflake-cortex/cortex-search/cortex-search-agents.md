# Use Cortex Search with Cortex Agents

Cortex Search gives Cortex Agents a retrieval layer over your unstructured data. By connecting a Cortex Search service as a tool, an agent can search across documents, policies, transcripts, contracts, or any text-based corpus, and use those results to answer questions, surface information, or perform analysis.

The same Cortex Search REST API is also accessible directly from external agents and MCP-compatible tools. For information about querying Cortex Search programmatically, see [Query a Cortex Search Service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

## Use cases

Cortex Search supports three levels of agent capability over unstructured data, from direct lookup to deep analysis:

### Direct retrieval and enterprise search

The agent uses Cortex Search to surface the most relevant documents or passages in response to a query. The results are returned directly, with source citations, without additional LLM synthesis. This is the right pattern when users need to find specific information, navigate a knowledge base, or verify a source.

Common use cases:

- **Enterprise search**: Employees search for policies, procedures, contracts, or technical documentation through a conversational interface.
- **Source lookup**: The agent finds and cites the specific document or section that answers a question.
- **Navigation and discovery**: Users explore a large corpus by topic, date, author, or other attributes.

### Retrieval-augmented generation (RAG)

The agent retrieves context from Cortex Search and passes it to the LLM to generate a grounded, natural-language response. This is the right pattern when the answer requires synthesis across a few relevant passages rather than a direct lookup.

Common use cases:

- **Knowledge base Q&A**: Customers or employees ask open-ended questions and receive answers grounded in proprietary documents.
- **Conversational search**: A chatbot answers follow-up questions while maintaining context, drawing on a continuously updated document corpus.
- **Compliance and policy assistance**: The agent answers questions about internal policies, citing the relevant sections.

### Analytical search

Analytical search is for questions that require analysis across many documents: counts, aggregates, comparisons, and trends. Rather than returning a handful of relevant passages, the agent searches broadly, applies AI functions over the result set, and produces data-backed answers.

Common use cases:

- **Cross-document analysis**: “What were the most common issues in support cases from Q1?”
- **Trend detection**: “How has risk language in our contracts changed over the past two years?”
- **Corpus-wide aggregation**: “What percentage of sales calls mentioned product X in EMEA versus the US?”

For details, including how to enable analytical search, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search).

## Connect Cortex Search to an agent

Specify the Cortex Search service as a tool in the agent specification. The `columns_and_descriptions` field is the most important configuration. It tells the agent what each column contains and how to use it for filtering and search, directly affecting retrieval quality.

If the service indexes files on a Snowflake stage, set `stage_path` and `relative_path_column` so that Snowflake CoWork can open the source document when a user selects a citation. For the Snowsight fields and file-type support, see [Configure and interact with agents](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).

Copy code

```
tools:
  - tool_spec:
      type: "cortex_search"
      name: "<your-search-tool-name>"
      description: "<describe what this index contains and when to use it>"

tool_resources:
  <your-search-tool-name>:
    search_service: "<db>.<schema>.<search_service_name>"
    max_results: "5"
    title_column: "<title_column_name>"
    id_column: "<id_column_name>"
    stage_path: "@<db>.<schema>.<stage_name>"
    relative_path_column: "<relative_path_column_name>"
    columns_and_descriptions:
      <text_column>:
        description: "<what this column contains, with sample values>"
        type: "string"
        searchable: true
        filterable: false
      <filter_column>:
        description: "<what this column contains; valid values: X, Y, Z>"
        type: "string"
        searchable: false
        filterable: true
```

For full configuration options including filters, multi-index services, and UI setup, see [Configure and interact with agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Analytical search

Analytical search extends standard retrieval by combining Cortex Search, AI functions, and SQL into one orchestrated loop. It is the right tool when the question requires analysis across many documents rather than a direct lookup.

Analytical search operates in two layers:

**Layer 1: Search to prune.** Cortex Search narrows the full corpus to a relevant candidate set. **Adaptive depth** dynamically adjusts how far to search. It extends when results are still relevant and stops when quality drops, so the agent finds the answer without wasting compute on irrelevant documents.

**Layer 2: AI functions and SQL to analyze.** Semantic operators run directly on the pruned result set:

- **AI\_FILTER** — Tests whether each document satisfies a specific semantic predicate.
- **AI\_EXTRACT** — Pulls structured, deterministic fields out of unstructured text.
- **AI\_AGG** — Summarizes and aggregates textual evidence at scale.
- **SQL** — Groups, counts, joins, ranks, trends, and calculates deltas.

Before executing, the agent presents an execution plan for review. After you enable analytical search, **auto-routing** classifies query intent at runtime. Simple questions stay on the standard retrieval path; corpus-wide analytical questions trigger the full analytical search loop.

Analytical search is disabled by default. For setup instructions, including how to enable it in Snowsight, SQL, or the REST API, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search).
