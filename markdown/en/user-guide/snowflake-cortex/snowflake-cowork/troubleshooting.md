# Troubleshooting

This page provides information about common issues that you may run into when working with Snowflake CoWork, as well as solutions for those issues. It also provides information about best practices for optimizing the performance of your agents and how to get additional support.

## Common issues and solutions

**Inconsistent responses**
:   Inconsistent responses are most commonly caused by a lack of specificity in prompts. To get a specific style or format for your response, specify it clearly in the prompt.

    While LLMs inherently have some variance, inconsistent answers can also happen after changes in the agent configuration. To resolve this, check for recent changes to your agent configuration, semantic view configuration, chat history, or model selection.

    If you are using a semantic model, you should transition to a semantic view. Semantic views allow validation during creation to help avoid inconsistencies that are less obvious when using a semantic model.

**Streaming response issues**
:   If you see a streaming response on one machine but not another, it is likely due to your organization’s IT configurations, such as network DPI, scanning tools, endpoint security software, or browser extensions. Work with your internal IT team to resolve these issues.

**Error 370001**
:   This error indicates that Snowflake CoWork generated an unsafe SQL command. Snowflake CoWork does not execute these commands and instead returns this error.

**Execution\_environment not populated for analyst tool**
:   This occurs when the tool is configured to run SQL queries against the user’s warehouse and the user does not have a warehouse set. To resolve this, either set a warehouse for the user or configure the tool to execute against a specific custom warehouse. For more information about warehouses, see [Warehouse usage in sessions](/user-guide/warehouses-overview#label-warehouse-usage-in-sessions).

**“Table / search service / stage does not exist” errors**
:   If you encounter `table / search service / stage does not exist` errors, there might be privilege issues. Verify that the following privileges are set correctly:

    - For each semantic model:

      - The user’s role is granted USAGE on the database and schema of the semantic model stage or view, and table.
      - If using a semantic model, the user’s role is granted READ on the stage that stores the semantic model file.
      - If using a semantic view, the user’s role is granted REFERENCES on the semantic view.
      - The user’s role is granted SELECT for each table defined in the semantic model or view.
    - For each Cortex search service:

      - The user’s role is granted USAGE on the database and schema of the Cortex search service.
      - The user is granted USAGE on the Cortex search service.

**Context and memory limits**
:   Cortex Agents use a finite context window, so very long conversations will lose earlier context. For persistent context, use custom instructions in the agent configuration.

## Performance optimization

**Response time issues**
:   Response latency can vary because Snowflake CoWork performs a complicated series of reasoning, retrieval, and analysis tasks using LLMs and queries. Performance can be affected by the load on your Snowflake warehouse and by the LLM services themselves. Requests often take longer than a minute to complete. For better performance, ensure [Cross-region inference](/user-guide/snowflake-cortex/snowflake-cowork/build-agents#label-snowflake-intelligence-build-cross-region) is enabled, use the “auto” model in your [Model selection](/user-guide/snowflake-cortex/snowflake-cowork/build-agents#label-snowflake-intelligence-build-model), and consider adding more verified queries. For more information about verified queries, see [Cortex Analyst Verified Query Repository](/user-guide/views-semantic/verified-query-repository).

**Timeout issues**
:   First, check the [Snowflake Status page](https://status.snowflake.com/) for any reported incidents. Your requests might also time out if Snowflake CoWork is running in a cloud region with limited GPU compute resources. We recommend enabling [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference) to avoid limitations within a single region.

**Parallel requests**
:   You can request that the agent runs tool calls, such as Cortex Analyst and Cortex Search, in parallel. Add the following to the Agent orchestration instructions [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage):

    Copy code

    ```
    OVERALL: parallelize as many tool calls as possible for latency purposes.
    ```

    For information about orchestration instructions, see [Specify orchestration](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-orchestration).

**Model selection**
:   When creating an agent, you can directly specify the model that the agent should use. You can’t directly specify the model for the Cortex Search or Cortex Analyst tools. Instead, you can use role-based access control (RBAC) to limit which models these tools can use. For more information, see [Role-based access control (RBAC)](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-rbac).

**Multiple calls to the same tool**
:   When generated queries are large, they can sometimes trigger size limits, causing a retry. Cortex Analyst has a 2048 token generation limit for queries, which can trigger the size limit. A lot of custom agent response instructions can also trigger the size limit.

**Warehouse size**
:   Snowflake CoWork makes a series of LLM-based decisions to create the best answer and call tools as needed. You can’t impact the performance of those decisions with a larger warehouse allocation.

    However, when running a Cortex Analyst tool as part of a Snowflake CoWork request, the request is translated to SQL queries that are run using your warehouse. If your warehouse is too small or overloaded, that negatively impacts performance.

**Improve orchestration instructions and tool descriptions**
:   To resolve issues with tools and orchestration, prompt an LLM with the explanation of the issue and the desired outcome, as well as the existing description or instructions. The LLM can help automate the creation of the new prompt.

**Use verified queries**
:   To ensure predictable results for common or complex queries, add verified queries to your semantic view. This ensures that the agent uses an optimized and predictable query path for these requests.

**Identify latency bottlenecks**
:   To diagnose slow agent responses, you can use the agent monitoring tab in Snowsight to identify latency bottlenecks. These traces show the logical path the agent took and how long each step lasted. For more information about agent monitoring, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor).

## Getting support

To get support for Snowflake CoWork, you can use the [Support page in Snowsight](/user-guide/ui-support). You can also access the [Snowflake Forums](https://snowflake.discourse.group/c/ai-agents-snowflake-intelligence/103) for more help.
