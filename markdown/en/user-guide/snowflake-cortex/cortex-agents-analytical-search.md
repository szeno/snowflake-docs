# Analytical search

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Analytical search is an orchestration capability in Cortex Agents that enables analytical queries over large document collections.
Traditional retrieval-augmented generation (RAG) approaches retrieve only a small number of passages, which limits their ability to answer
questions requiring comprehensive analysis across hundreds or thousands of documents, including counts, aggregates, and trends. Analytical search
addresses this by combining semantic search, AI functions, and SQL into one loop to answer those questions with analytical rigor over unstructured data.
After you enable it on an agent, analytical search is available wherever that agent runs: the Cortex Agents SQL commands, the REST API, and
[Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork).

## How analytical search works

Analytical search enables precise analytical queries over large document sets, including filtered lists, aggregates,
and temporal analysis such as:

- “List all patients who were prescribed albuterol for asthma last year”
- “What percentage of sales calls mentioned product X in EMEA vs. the US last year?”
- “Identify the new themes that emerged in the notes in 2025, compared to 2024”

Analytical search operates in two layers:

### Layer 1: Search to prune

Cortex Search narrows the full corpus down to a relevant candidate set by finding documents about a specific topic, isolating records containing a particular clause, or filtering to a date range. This happens without scanning every document with a large model.

The agent runs these searches as SQL queries that call the
[SEARCH\_PREVIEW](/sql-reference/functions/search_preview-snowflake-cortex) function. The search results are materialized
in an intermediate table so that subsequent SQL and AI function calls can analyze the result set.

**Adaptive depth** controls how far to search. Rather than using a fixed top-k limit, the agent dynamically adjusts
the search depth based on the relevance of results: extending when the tail of results is still relevant to the question,
and stopping when quality drops. This avoids two common failure modes: stopping too early and missing key documents, or going too deep and wasting compute on irrelevant ones.

### Layer 2: AI functions and SQL to analyze

Once the corpus is pruned, the agent applies semantic operators directly on the result set:

- **AI\_FILTER**: Tests whether each document satisfies a specific semantic predicate (for example, “is this about a customer issue?”).
- **AI\_EXTRACT**: Pulls structured, deterministic fields out of unstructured text (for example, issue type, date, customer name).
- **AI\_AGG**: Summarizes and aggregates textual evidence at scale.
- **SQL**: Groups, counts, joins, ranks, trends, and calculates deltas over the extracted data.

Note

The agent generates and runs the SQL on a Snowflake virtual warehouse. In the Cortex Agents Run API response,
this implicit SQL execution is represented by
[`system_execute_sql`](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-agents-run-non-streaming-response)
tool-use and tool-result blocks. You don’t add this tool to the agent specification.

### Planning and auto-routing

Before executing any analysis, the agent generates a clear execution plan and presents it for review. This lets you verify the logical steps (the scope of the search, the filters applied, and the aggregation logic) and make adjustments before any data is processed.

**Auto-routing** classifies query intent at runtime: simple, single-passage questions stay on the standard RAG path;
corpus-wide analytical questions trigger the analytical search loop. Auto-routing runs only after you enable analytical
search on the agent.

## Analytical search vs. traditional RAG

The following example compares how traditional RAG and analytical search handle the query:
*“What were the most common customer issue types in the support cases in May 2025?”*

### Traditional RAG approach

With traditional RAG:

1. The agent issues one or two broad search queries (for example, `search("May 2025 customer issues")`) with a small limit
   (typically 10 results).
2. The agent receives approximately 10–20 search results and summarizes them directly.

Example output:

```
Based on the provided documents, latency and authentication are common issues,
with customers X and Y citing high query latency and customer Z mentioning
authentication errors. However, there may be more issues that were not analyzed.
```

This answer is imprecise and incomplete because it relies on a small subset of documents without strict date filters.

### Analytical search approach

With analytical search, Cortex Agents orchestrate a multi-step workflow:

1. Classify the query as analytical and generate an execution plan.
2. Run structured search queries through `SEARCH_PREVIEW` with adaptive depth to capture the full relevant set of results.
3. Materialize the search results in an intermediate table.
4. Apply AI\_FILTER to keep only rows related to customer issues.
5. Apply AI\_EXTRACT to pull issue type and customer name from each document.
6. Use AI\_AGG and SQL to aggregate results by issue type.
7. Return a precise, data-backed answer.

Example output:

```
In May 2025, quality issues (27 tickets) and latency issues (19 tickets)
were the most commonly cited customer problems. The breakdown of issue counts
by customer is as follows: ...
```

This result is precise because the agent works over the full relevant set of documents with date filters and SQL-style aggregation,
rather than summarizing a small sample.

## Set up analytical search

Analytical search is disabled by default (`analytical_search` is `false`). Agents that have a Cortex Search tool continue
to answer search questions using standard retrieval, but they don’t run the analytical search loop. Queries that need
corpus-wide counts, aggregates, or trends then return answers based on a small retrieved sample only.

You enable analytical search once on the agent object. The same setting applies when you run the agent with SQL or the
REST API and when users interact with the agent in Snowflake CoWork.

To use analytical search, complete these steps:

1. Create a Cortex Search service, or reuse an existing one.
2. Add that Cortex Search service as a tool on the agent, and enrich the tool resources with column descriptions so the
   agent can filter and extract effectively. For the YAML and REST `columns_and_descriptions` fields, see
   [Connect Cortex Search to an agent](/user-guide/snowflake-cortex/cortex-search/cortex-search-agents#label-cortex-search-connect-agent).
   For the Snowsight **Columns Description** fields, see
   [Configure and interact with Agents](/user-guide/snowflake-cortex/cortex-agents-manage).
   For what to include in each description, see [Add detailed column descriptions](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-analytical-search-column-descriptions).
3. Enable `analytical_search` on the agent in Snowsight, with SQL, or with the REST API.

Note

- If you already have a Cortex Search service, you can reuse it; you don’t need to create a new service specifically for analytical search.
- If your agent already has a Cortex Search tool configured, you don’t need to add another one.
- `analytical_search` is a field in the agent specification under `orchestration.capabilities`. It isn’t a standalone
  ALTER AGENT property.

### Create a Cortex Search service

Copy code

```
CREATE OR REPLACE CORTEX SEARCH SERVICE <database>.<schema>.<name>
  TEXT INDEXES CHUNK, DOC_ID [, <other_text_search_columns>]
  VECTOR INDEXES CHUNK (model = 'snowflake-arctic-embed-l-v2.0') [, <other_vector_search_columns>]
  ATTRIBUTES <filter_column> [, <other_filter_columns>]
  WAREHOUSE = <warehouse_name>
  TARGET_LAG = '1 day'
  AS
    SELECT <columns>
    FROM <chunks_table>;
```

Then create an agent and add the Cortex Search service as a tool. Include column descriptions in the tool resources.
For more information, see [Configure and interact with Agents](/user-guide/snowflake-cortex/cortex-agents-manage)
and [Connect Cortex Search to an agent](/user-guide/snowflake-cortex/cortex-search/cortex-search-agents#label-cortex-search-connect-agent).

For more information on the commands used, see [CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search) and [CREATE AGENT](/sql-reference/sql/create-agent).

### Enable analytical search on the agent

Set `analytical_search` to `true` on each agent where you want the analytical search loop. Set it to `false` to disable
analytical search. Use any of the following methods. They all update the same agent object, so the agent can use
analytical search from SQL, the REST API, and Snowflake CoWork.

Method 1: Snowsight UIMethod 2: REST APIMethod 3: SQL

1. In the navigation menu, select **AI & ML** » **Agents**.
2. Select the agent, then select **Edit**.
3. Select **Tools**.
4. After you add a Cortex Search service, toggle **Analytical Search** on.
5. Select **Save**.

Additional costs apply when the agent uses AI functions. For more information, see [Cost considerations](#label-analytical-search-cost).

To enable analytical search on an existing agent, call the
[Update Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agents-rest-api-update)
endpoint. If the agent already has budget or other orchestration settings, include those fields in the same
`orchestration` object so they aren’t removed.

Copy code

```
curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database>/schemas/<schema>/agents/<name>" \
  --header 'Content-Type: application/json' \
  --header 'Accept: application/json' \
  --header "Authorization: Bearer $PAT" \
  --data '{
    "orchestration": {
      "capabilities": {
        "analytical_search": true
      }
    }
  }'
```

For a new agent, include the same `orchestration.capabilities` object in the
[Create Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api)
request body, along with a Cortex Search tool:

Copy code

```
{
  "name": "my_agent",
  "orchestration": {
    "capabilities": {
      "analytical_search": true
    }
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "my_search_tool",
        "description": "Search documents"
      }
    }
  ],
  "tool_resources": {
    "my_search_tool": {
      "search_service": "my_db.my_schema.my_search_svc"
    }
  }
}
```

For an existing agent, retrieve the complete LIVE specification, add or update `orchestration.capabilities`, then apply
the complete updated specification. `ALTER AGENT ... SET SPECIFICATION` replaces the entire specification; fields that
you omit are removed.

1. Run [DESCRIBE AGENT](/sql-reference/sql/desc-agent) to retrieve the complete LIVE specification.
2. Add or update the following in the specification:

   Copy code

   ```
   "orchestration": {
     "capabilities": {
       "analytical_search": true
     }
   }
   ```
3. Apply the complete updated specification:

   Copy code

   ```
   ALTER AGENT <database>.<schema>.<agent>
     MODIFY LIVE VERSION SET SPECIFICATION = $$
     models:
       orchestration: auto

     orchestration:
       capabilities:
         analytical_search: true
       budget:
         seconds: 30
         tokens: 16000

     tools:
       - tool_spec:
           type: "cortex_search"
           name: "Search1"
           description: "Searches company documents"

     tool_resources:
       Search1:
         search_service: "db.schema.service_name"
         max_results: "1000"
     $$;
   ```

   Replace the tools, tool resources, instructions, and budget values with the full specification from `DESCRIBE AGENT`.

For a new agent, include the same `orchestration.capabilities` field in the specification passed to
[CREATE AGENT](/sql-reference/sql/create-agent):

Copy code

```
CREATE OR REPLACE AGENT my_agent
  FROM SPECIFICATION
  $$
  orchestration:
    capabilities:
      analytical_search: true

  tools:
    - tool_spec:
        type: "cortex_search"
        name: "Search1"
        description: "Searches company documents"

  tool_resources:
    Search1:
      search_service: "db.schema.service_name"
      max_results: "1000"
  $$;
```

After analytical search is enabled, ask the agent a question with analytical intent. The agent routes to the analytical
search loop when the query requires it.

## Recommendations

**Use a multi-index service and set a high result limit.** Snowflake recommends using a [multi-index Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-multi-index-search) for analytical search and setting `max_results` to 1,000. This gives the agent enough breadth to surface the full relevant set of documents. Adaptive depth will limit the actual compute to what the question requires.

**Add detailed column descriptions.** The most impactful thing you can do to improve analytical search quality is to add
rich descriptions to every column in the service definition. The agent uses these descriptions to decide which columns
to filter on, how to interpret values, and how to frame AI\_EXTRACT and AI\_FILTER calls. For each column, describe:

- What the column contains and its expected format or value range
- Sample values or enumerations (for example, `"Values include: policy, guide, reference"`)
- Whether the column is suitable for filtering, searching, or extraction
- Any relationships to other columns

Columns without descriptions are harder for the agent to use effectively, especially for filterable attributes that
determine how the search is scoped. For how to set these descriptions in the agent specification or in Snowsight, see
[Connect Cortex Search to an agent](/user-guide/snowflake-cortex/cortex-search/cortex-search-agents#label-cortex-search-connect-agent)
and [Configure and interact with Agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Use analytical search in Snowflake CoWork

Analytical search is supported in Snowflake CoWork on any agent where you have enabled it. Use the same Snowsight, SQL,
or REST API steps as for Cortex Agents. See [Enable analytical search](#label-enable-analytical-search).

When you use that agent in Snowflake CoWork, you also get these interactive capabilities:

- **Clarification questions**: When the query is ambiguous, the agent asks targeted clarifying questions before starting
  the analysis. For example, it may ask you to confirm the time range, the scope of the corpus, or the comparison group.
- **Plan mode**: The agent presents a step-by-step execution plan before running any analysis. You can review and adjust the plan, such as narrowing the date range or changing the peer set, before the agent processes any data.
- **Chart generation**: The agent can automatically generate charts from analytical results.
- **Save and share artifacts**: Results can be saved and shared as artifacts directly from the conversation.

Note

Analytical search does not produce PDF documents. Intermediate results used during analysis are not automatically
persisted. If you want to keep the results, save or export them before ending the session.

## Performance considerations

Analytical search involves both retrieval (Cortex Search queries) and compute (AI functions over result sets), so response
times are longer than standard RAG. Most analytical search workflows complete in **2–6 minutes**; complex analyses over
large corpora may take up to **15 minutes**.

## Cost considerations

These extra costs apply only when analytical search is enabled and the agent runs the analytical search loop.
Analytical search incurs costs associated with agent orchestration, warehouse compute for SQL execution, and the AI functions it uses
([AI\_EXTRACT](/sql-reference/functions/ai_extract), [AI\_FILTER](/sql-reference/functions/ai_filter),
and [AI\_AGG](/sql-reference/functions/ai_agg)). Adaptive depth limits unnecessary AI function calls by stopping the search
when results are no longer relevant. For more information on AI function costs, see [Snowflake Cortex AI functions incur compute cost based on the number of tokens…](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).
