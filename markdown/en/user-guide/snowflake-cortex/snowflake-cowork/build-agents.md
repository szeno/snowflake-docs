# Build agents

You can build agents for Snowflake CoWork using the following methods:

- In Snowsight
- Using the [Agent object REST API](/user-guide/snowflake-cortex/cortex-agents-rest-api)
- With the [Cortex Agents SQL](/sql-reference/commands-cortex-agent) commands

The following sections provide information about how to build agents for Snowflake CoWork using SQL commands. Each section provides information about a different part of the agent configuration. The final section shows an example of an agent configuration that includes all of the components described in this topic.

For more information about the other methods to create an agent and the options available, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Agent structure

An agent consists of the following parts:

- The base model that provides the foundation for the agent’s behavior
- A model (the orchestrator) that interprets intent, selects the right tools, and plans the sequence of actions
- Instructions for the agent’s behavior
- Tools for the agent to use
- Resources for the tools

The following sections provide information about model selection and tool configuration. This example uses a semantic view, a Cortex Search service, and a custom tool to provide answers. Although you can create a basic agent that doesn’t use any of these tools, that basic agent can only use the base model to provide answers. As a result, the agent lacks access to data within your Snowflake account and has limited context for answers.

For information about the other components of the agent, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).

## Prerequisites

To create a Cortex Agent, you must use a role with the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE AGENT | Schema | Required to create the Cortex Agent. |
| USAGE | Database, schema | Required to create the Cortex Agent in the specified database and schema. |

Expand

Show lessSee more

The following code grants the necessary privileges to create a Cortex Agent:

> Copy code
>
> ```
> GRANT USAGE ON DATABASE <database_name> TO ROLE <role_name>;
> GRANT USAGE ON SCHEMA <database_name>.<schema_name> TO ROLE <role_name>;
> GRANT CREATE AGENT ON SCHEMA <database_name>.<schema_name> TO ROLE <role_name>;
> ```

In addition to the privileges required to create a Cortex Agent, the following prerequisites are necessary to connect the agent to specific tools:

- A semantic view to connect to the agent
  :   For information about creating a semantic view, see [Overview of semantic views](/user-guide/views-semantic/overview).
- A Cortex Analyst tool to connect to the agent
  :   For information about creating a Cortex Analyst tool, see [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst).
- Unstructured data in a database to connect to the agent
- A Cortex Search tool to connect to the agent
  :   For information about creating a Cortex Search tool, see [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).
- A custom tool to connect to the agent
  :   For information about creating user-defined functions (UDFs) and stored procedures to use as custom tools, see [Extending Snowflake with Functions and Procedures](/developer-guide/extensibility).

To attach tools to an agent, the role that is used to create the agent must have the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Cortex Search service | Required to add the Cortex Search service to the Cortex Agent. |
| SELECT | Table/View | Required to access the objects referenced in the agent’s semantic view/model. |
| USAGE | Tools | Required to access all of the custom tools to attach to the agent. For example, if the custom tool is a stored procedure, then you must have USAGE on the procedure. |
| USAGE | Semantic view/model | Required to access the semantic view/model to attach to the agent. |

Expand

Show lessSee more

## Agent configuration basics

When you create an agent, you must specify information about the agent, such as the name, description, and model. You can also specify the tools that the agent can use and the resources that the agent can access. These resources are passed as a YAML specification in the `FROM SPECIFICATION` clause of the `CREATE AGENT` command.

The following recommendations provide best practices for this configuration:

**Scope agents narrowly:** Before adding tools or writing instructions, define why the agent exists, who it serves, and what specific questions it should answer. This step shapes everything that follows, from tool selection to performance and trust. Snowflake recommends that you narrow the agent’s scope to a specific, high-value use case.

After an agent proves reliable in one area, you can replicate the pattern for others. For example, you could have one agent to analyze your store’s recent sales and marketing data, and another that recommends the best SKUs to pitch to the retailer.

**Select the number of tools carefully:** Every agent should have access to only the tools it needs. To determine that, consider the documents or data that the agent needs to fulfill its purpose. If the agent needs to access unstructured data, use [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). If the agent needs to access structured data, use [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst). If the agent needs other tools, you can use custom tools.

**Write a useful tool description:** These descriptions are used to help the agent understand what the tool does and how to use it. Unclear tool descriptions can create cascading failures and lead to “hallucinations.”

> To create a useful tool description, follow these guidelines:
>
> > - Add a clear and specific tool name that clarifies the tool’s domain (“Customer”, “Sales”) and function (“Analytics”, “Search”).
> > - Write a purpose-driven tool description that tells the agent:
> >
> >   - What the tool does
> >   - Which data it accesses
> >   - When to use it
> >   - When NOT to use it
> > - Be explicit about the tool’s expected inputs. Ambiguous inputs to your tools lead to incorrect tool calls and errors.
> >
> >   - Be specific.
> >   - Specify the data format.
> >   - Provide clear data instructions.
> >   - Provide default guidance.
> >   - Use consistent terminology.

For more agent configuration recommendations, see [Best Practices for Building Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents/).

For guidance on evaluating reliability and behavior, see [Best Practices for Evaluating Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-for-evaluating-cortex-agents/).

## Model selection

When you create an agent, we recommend that you select **auto** for the model. With this option, Cortex automatically selects the highest quality model for your account, and the quality automatically improves as new models become available. For more information about the available models, see [Supported models and regions](/user-guide/snowflake-cortex/snowflake-cowork/reference#label-snowflake-intelligence-models).

The following example shows how to specify the model for the agent:

Copy code

```
models:
  orchestration: auto
```

### Cross-region inference

Important

Cross-region inference is disabled by default. We recommend using cross-region inference to access the full set of LLMs and avoid limitations within a single region.

When using a model that is not available in the local region, you must use Cortex cross-region inference. This setting enables inference requests to be processed in a different region from the default region. The parameter for cross-region inference can only be set at the account level by the ACCOUNTADMIN role, not at the user or session levels.

To set the parameter, use the following command:

Copy code

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

For more information about configuring Cortex cross-region inference, see [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

## Connect semantic views using Cortex Analyst (structured data)

Snowflake CoWork supports semantic views, which are a type of structured data with instructions that tell the agent how to query or interpret the data. Cortex Agents use Cortex Analyst to retrieve structured data from semantic views by converting natural language requests into SQL queries. Agents can route across multiple semantic views to provide the response.

Each semantic view should cover a similar set of tables. You can set data-specific defaults, such as always adding a date filter for the past three months if not specified or always excluding internal accounts.

You can connect a semantic view to an agent by specifying the semantic view as part of the tool resources. The following example shows how to connect a semantic view to an agent and how to specify the Cortex Analyst tool to retrieve structured data from the semantic view:

Copy code

```
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "<your cortex analyst tool name>"
      description: "<clear and specific tool description>"

tool_resources:
  <your cortex analyst tool name>:
    semantic_view: "<db>.<schema>.<semantic_view>"
```

### Best practices for semantic views

Semantic views power how Snowflake CoWork understands and queries your data. For guidance on designing an accurate,
efficient semantic view — scoping and organization, high-quality descriptions, relationships, metrics and filters, verified
queries, custom instructions, and Cortex Search — see [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling).

## Connect Cortex Search (unstructured data)

To process unstructured data, you can connect a Cortex Search tool to an agent by specifying the Cortex Search tool in the YAML specification as part of the tool resources. Cortex Search services retrieve documents and records from unstructured data sources using semantic search. The two primary use cases for Cortex Search are retrieval augmented generation (RAG) and enterprise search. For information about creating a Cortex Search service, see [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). You can also use a Cortex Knowledge Extension (CKE) that is shared with you.

You can also use **analytical search** to go beyond standard RAG retrieval. Analytical search lets the agent run extensive analytics over large document collections, returning lists, counts, aggregates, and trends rather than just a few relevant passages. Analytical search is supported in Snowflake CoWork and for Cortex Agents you call with SQL or the REST API. Enable it once on the agent; the same setting applies in both places. It is disabled by default. For steps, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search). For information about powering agents with Cortex Search more broadly, see [Use Cortex Search with Cortex Agents](/user-guide/snowflake-cortex/cortex-search/cortex-search-agents).

When you connect a Cortex Search tool to an agent, it is especially important to include the following information about the parameters and their expected values:

- Type and format (include examples)
- Whether required or optional (with default values)
- Valid values or constraints (enums, ranges, formats)
- Relationship to other parameters (dependencies, conflicts)
- How to obtain the value (especially for IDs)

If the search service indexes files stored on a Snowflake stage, you can also configure the tool so that users can open the source document in Snowflake CoWork when they select a citation. Set both of the following optional fields:

- **Source stage** (`stage_path`): The stage that stores the source documents, in `@DATABASE.SCHEMA.STAGE_NAME` format.
- **Relative path column** (`relative_path_column`): The indexed column that stores each document’s file path relative to that stage. Many services use a column named `RELATIVE_PATH`.

Both fields are optional. If you omit them, citations still appear, but Snowflake CoWork can’t open the original file in the in-app document viewer. In-app preview supports PDF files. The role that queries the agent must have READ on the stage.

If the ID column already stores a full stage path that starts with `@` (for example, `@MY_DB.MY_SCHEMA.DOCS_STAGE/policies/refund.pdf`), you can omit `stage_path` and `relative_path_column`. Snowflake CoWork uses that ID value as the file location.

To set these fields in Snowsight, see [Configure and interact with agents](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).

The following example shows how to connect a Cortex Search tool to an agent and how to specify the Cortex Search tool in the YAML specification:

Copy code

```
tools:
  - tool_spec:
      type: "cortex_search"
      name: "<your cortex search tool name>"
      description: "<clear and specific tool description>"

tool_resources:
  <your cortex search tool name>:
    search_service: "<db>.<schema>.<search_service_name>"
    max_results: "5"
    filter:
      "@eq":
        region: "North America"
    title_column: "<title_name>"
    id_column: "<column_name>"
    stage_path: "@<db>.<schema>.<stage_name>"
    relative_path_column: "<relative_path_column_name>"
```

## Add custom tools

Snowflake CoWork supports custom tools, which are user-defined functions or stored procedures that can be used to implement custom business logic. You can connect a custom tool to an agent by specifying the custom tool in the YAML specification as part of the tool resources.

The following example shows how to connect a custom tool to an agent and how to specify the custom tool in the YAML specification:

Copy code

```
tools:
  - tool_spec:
      type: "generic"
      name: "<your custom tool name>"
      description: "<clear and specific tool description>"

tool_resources:
  <your custom tool name>:
    user-defined-function-argument: "argument1"
```

## Create an agent

To create an agent using SQL:

Copy code

```
CREATE OR REPLACE AGENT <agent_name>
 COMMENT = 'agent level comment'
 PROFILE = '{"display_name": "My Business Assistant", "avatar": "business-icon.png", "color": "blue"}'
 FROM SPECIFICATION
 $$
 models:
 orchestration: claude-sonnet-4-6

 orchestration:
 budget:
     seconds: 30
     tokens: 16000

 instructions:
 response: "You will respond in a friendly but concise manner"
 orchestration: "For any revenue question, use Analyst; for policy questions, use Search"
 sample_questions:
     - question: "What was our revenue last quarter?"

 tools:
 - tool_spec:
     type: "cortex_analyst_text_to_sql"
     name: "<your cortex analyst tool name>"
     description: "<clear and specific tool description>"
 - tool_spec:
     type: "cortex_search"
     name: "<your cortex search tool name>"
     description: "<clear and specific tool description>"
 - tool_spec:
     type: "data_to_chart"
     name: "data_to_chart"
     description: "Generates visualizations from data"

 tool_resources:
 <your cortex analyst tool name>:
     semantic_view: "<db>.<schema>.<semantic_view>"
 <your cortex search tool name>:
     search_service: "<db>.<schema>.<search_service_name>"
     max_results: "5"
     filter:
     "@eq":
         region: "North America"
     title_column: "<title_name>"
     id_column: "<column_name>"
     stage_path: "@<db>.<schema>.<stage_name>"
     relative_path_column: "<relative_path_column_name>"
 $$;
```

## Modify an existing agent

For instructions on modifying the configuration for an existing agent, including adding tools and updating other details, see [Add tools](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).
