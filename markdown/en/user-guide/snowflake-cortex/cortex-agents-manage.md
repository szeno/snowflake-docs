# Create and manage agents

You can build an agent with the following methods:

- In Snowsight
- Using the [Agents REST API](/user-guide/snowflake-cortex/cortex-agents-rest-api)
- With the [Cortex Agents SQL](/sql-reference/commands-cortex-agent) commands

You can then integrate the agent into your application to perform tasks or respond to queries. You must first create an agent object that contains information such as the metadata, tools, and orchestration instructions that the agent can use to perform a task or answer questions. You can then reference the agent object in your application to integrate the agent’s functionality. You can configure a thread to maintain the context in memory, so that the client does not have to send the context at every turn of the conversation.

Tip

If this is your first agent, [Get started with Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-get-started)
covers the whole path in one place: the grants you need, a semantic view over sample data, the agent,
and a first question. It also shows how to ask CoCo to build an agent over your own data.
This topic is the full reference for each of those methods.

Important

Before you create and call agents, set up the required roles, privileges, and authentication. For
details, see [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).

Cortex Agents determines permissions from the querying user’s **default role**, not the role active in
their session. The user must also have a **default warehouse**, with `USAGE` on that warehouse granted
to the default role. If either is missing, agent calls fail even when the user’s current role has every
required privilege. See
[User requirements](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-user-requirements).

When you call the Agents REST API, you can run a request under a role other than the user’s default
role by setting the `X-Snowflake-Role` header. For more information, see [Specify Snowflake context with Snowflake REST APIs](/developer-guide/snowflake-rest-api/setting-context).

## Create an agent

Create an agent object by specifying the database and schema where the agent should be located, along with a name and description for the agent. In addition, specify the display name, avatar, and the color. These attributes are used by the client application to display the agent. The display name is also used as the handle to reference the agent in conversations.

For best practices when creating an agent, see [Best Practices for Building Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents/).

The following examples show how to create an agent object from Snowsight or using the REST API:

> Method 1: Snowsight UIMethod 2: REST APIMethod 3: SQL
>
> 1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
> 2. In the navigation menu, select **AI & ML** » **Agents**.
> 3. Select **Create agent**.
> 4. For **Agent object name**, specify the identifier for the agent object in the database and schema. This is the name you use to reference the agent in SQL and in REST API requests.
> 5. For **Display name**, specify the name that client applications show to users. This is also the handle that users reference in conversations.
> 6. Select **Create agent**.
> 7. Prompt the agent with general knowledge requests.
>
> 1. Create an agent object by specifying the database and schema where the agent will be created, as well as the parameters needed for the agent. You can also specify tool fields when creating the agent object.
>
>    Copy code
>
>    ```
>    curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents" \
>    --header 'Content-Type: application/json' \
>    --header 'Accept: application/json' \
>    --header "Authorization: Bearer $PAT" \
>    --data '{
>     "name": "TransportationAgent",
>     "comment": "This agent handles queries related to transportation methods and costs.",
>     "models": {
>         "orchestration": "auto"
>     }
>    }'
>    ```
>
> Create an agent object in the database and schema where the agent will be created. You can specify the agent properties and specification using the `FROM SPECIFICATION` clause in the CREATE AGENT command. For more information, see [CREATE AGENT](/sql-reference/sql/create-agent).
>
> Copy code
>
> ```
> CREATE OR REPLACE AGENT myagent
>   COMMENT = 'agent level comment'
>   PROFILE = '{"display_name": "My Business Assistant", "avatar":  "business-icon.png", "color": "blue"}'
>   FROM SPECIFICATION
>   $$
>   orchestration:
>     tool_not_accessible: accept
>     budget:
>       seconds: 30
>       tokens: 16000
>
>   instructions:
>     response: "You will respond in a friendly but concise manner"
>     orchestration: "For any revenue question use Analyst; for policy use Search"
>     sample_questions:
>       - question: "What was our revenue last quarter?"
>
>   tools:
>     - tool_spec:
>         type: "cortex_analyst_text_to_sql"
>         name: "Analyst1"
>         description: "Converts natural language to SQL queries for financial analysis"
>     - tool_spec:
>         type: "cortex_search"
>         name: "Search1"
>         description: "Searches company policy and documentation"
>     - tool_spec:
>         type: "data_to_chart"
>         name: "data_to_chart"
>         description: "Generates visualizations from data"
>
>   tool_resources:
>     Analyst1:
>       semantic_view: "db.schema.semantic_view"
>     Search1:
>       search_service: "db.schema.service_name"
>       max_results: "5"
>       filter:
>         "@eq":
>           region: "North America"
>       title_column: "<title_name>"
>       id_column: "<column_name>"
>       stage_path: "@<db>.<schema>.<stage_name>"
>       relative_path_column: "<relative_path_column_name>"
>       columns_and_descriptions:
>         TEXT:
>           description: "The main text content of the document"
>           type: "string"
>           searchable: true
>           filterable: false
>         CATEGORY:
>           description: "Document category. Values include: policy, guide, reference."
>           type: "string"
>           searchable: false
>           filterable: true
>   $$;
> ```

### Create an agent in your Personal Database

You can create a Cortex Agent in your [Personal Database](/user-guide/personal-databases). This gives you a user-specific location for developing and testing an agent without first requesting access to a shared database.

Personal Database names use the `USER$<username>` format. Enclose the database name in double quotes when it contains special characters. The following example creates an agent in the `PUBLIC` schema of the Personal Database for the user `JSMITH`:

Copy code

```
CREATE OR REPLACE AGENT "USER$JSMITH".PUBLIC.MY_AGENT
  COMMENT = 'Personal Database agent'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  instructions:
    response: "You are a helpful assistant."
  $$;
```

To run the agent with SQL, pass its fully qualified name to [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex):

Copy code

```
SELECT TRY_PARSE_JSON(
  SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
    '"USER$JSMITH".PUBLIC.MY_AGENT',
    $${
      "messages": [
        {
          "role": "user",
          "content": [
            { "type": "text", "text": "What are some types of products?" }
          ]
        }
      ]
    }$$,
    TRUE
  )
) AS resp;
```

## Add tools

After you’ve created the agent, add the tools it can use and provide instructions on how to orchestrate across them. For a description of what each tool does, see [Tools](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-tools).

When you add a tool, you also specify the resources it uses:

> - **Cortex Analyst:** Provide one or more semantic views for the agent to retrieve structured data from, along with the warehouse and the query timeout. The agent can route across multiple semantic views to answer a request.
>
>   Note
>
>   When Cortex Analyst is invoked by an agent, it does not have access to open source LLM models. For a list of the models that Cortex Analyst can use when invoked by an agent, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
> - **Cortex Search:** Provide the Cortex Search services, along with the filters, the columns and column descriptions for filterable and searchable columns, and the maximum number of results to return. If the service indexes files on a Snowflake stage, you can also provide the source stage and relative path column so that users can open source documents from citations in Snowflake CoWork.
> - **Analytical search:** Enables the agent to run extensive analytics over large document collections, producing lists, counts, aggregates, and trends. Analytical search extends Cortex Search by orchestrating multi-index queries with configurable limits and using AISQL on the full result set. Analytical search is disabled by default. Enable it on the agent after you add a Cortex Search tool. For more information, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search).
> - **[Code execution](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool):** Enable the built-in tool so the agent can run Python in a secure, isolated sandbox. No additional resources are required.
> - **Data to Chart:** Enable the tool so the agent can generate visualizations from data returned by other tools. No additional resources are required.
> - **Custom tools:** Provide the stored procedure or user-defined function (UDF) that implements your logic, along with the warehouse used to run it.
> - **Agent skills:** Add a packaged agent skill to give the agent repeatable, task-specific capabilities.
> - **MCP connectors:** Provide the connection to a remote MCP server so the agent can use the tools that server hosts, such as those from Atlassian Jira or Salesforce.
> - **Agent toolsets:** Reference another agent so the calling agent inherits that agent’s tools at run time. See [Agent toolsets](/user-guide/snowflake-cortex/cortex-agents-toolsets).
> - **Web search:** Enable the web search tool on the agent. Web search must first be enabled at the account level. See [Enable web search](#label-cortex-agents-enable-web-search).

Note

Tool names must be between 1 and 64 characters. If you’re using a semantic view as a tool, the semantic view name is used as the tool name.

The tabs that follow cover the tools that most agents start with. Some tools are documented on their
own pages instead, and a few are configured only in the agent specification. Use this table to find
the right instructions for the tool you want to add:

| Tool | Where to configure it |
| --- | --- |
| Cortex Analyst | The tabs that follow, in all three methods. |
| Cortex Search | The tabs that follow, in all three methods. |
| Analytical search (Public Preview) | The tabs that follow, in all three methods. See [Set up analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search). |
| Custom tools | The Snowsight and REST API tabs that follow. |
| Web search | The Snowsight and REST API tabs that follow, after an account admin enables it. See [Enable web search](#label-cortex-agents-enable-web-search). |
| Data to Chart | The REST API and SQL tabs that follow. |
| [Code execution](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) | The agent specification. |
| Agent skills | The **Skills** tab in Snowsight, or the agent specification. See [Agent skills](/user-guide/snowflake-cortex/cortex-agents-skills). |
| MCP connectors | The **MCP Connectors** tab in Snowsight, after an account admin adds the connector. See [MCP Connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors). |
| Agent toolsets | The agent specification. See [Agent toolsets](/user-guide/snowflake-cortex/cortex-agents-toolsets). |

Expand

Show lessSee more

> Method 1: Snowsight UIMethod 2: REST APIMethod 3: SQL
>
> To modify the configuration for an existing agent, follow these steps:
>
> 1. In the navigation menu, select **AI & ML** » **Agents**.
> 2. From the list of agents, select the agent that you want to modify.
>    :   The configuration details for the agent are displayed.
> 3. Select **Edit**.
> 4. For **Description**, describe the agent and how users can interact with it.
> 5. To add sample questions that users can ask the agent, enter a sample question and select **Add a question**.
> 6. Select **Tools**. Add one or more of the following tools.
>
>    > - **To add a semantic view in Cortex Analyst to the agent**: This section assumes that you already have a semantic view created. For information about semantic views and how to create one, see [Overview of semantic views](/user-guide/views-semantic/overview).
>    >
>    >   1. Find **Cortex Analyst** and select the respective **+ Add** button.
>    >   2. For **Name**, enter a name for the semantic view.
>    >   3. Select **Semantic view**.
>    >   4. Select the semantic view that the agent uses.
>    >   5. For **Warehouse**, select the warehouse that the agent uses to run queries.
>    >   6. For **Query timeout (seconds)**, specify the maximum time in seconds that the agent waits for a query to complete before timing out.
>    >   7. For **Description**, describe the semantic view.
>    >   8. Select **Add**.
>    > - **To add a Cortex Search service to the agent**: This section assumes that you’ve already created a Cortex Search service. For information about creating a Cortex Search service, see [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview). You can also use a Cortex Knowledge Extension (CKE) that is shared with you. For a tutorial that uses a CKE, see [Tutorial 3: Add a CKE to Snowflake CoWork](/user-guide/snowflake-cortex/cortex-knowledge-extensions/tutorials/add-cke-to-snowflake-cowork-tutorial).
>    >
>    >   1. Find **Cortex Search Services** and select the respective **+ Add** button.
>    >   2. For **Name**, enter a name for the Cortex Search service.
>    >   3. For **Description**, describe the Cortex Search service.
>    >   4. For **Search service**, select the Cortex Search service that the agent uses.
>    >   5. For **ID column**, select the column used to generate hyperlinks to the source.
>    >   6. For **Title column**, select the column used in citations and source cards.
>    >   7. For **Source stage**, enter the Snowflake stage that stores the source documents, in `@DATABASE.SCHEMA.STAGE_NAME` format. This field is optional. Set it when you want users to open source files from citations in Snowflake CoWork.
>    >   8. For **Relative path column**, select the indexed column that stores each document’s file path relative to the source stage. Many services use a column named `RELATIVE_PATH`. This field is optional. Use it together with **Source stage**.
>    >   9. Under **Tool details**, add **Columns Description** to help the agent effectively use the search service. Column descriptions are not required for all columns, but providing them for filterable and searchable columns is recommended to improve the quality of results. Provide a description that explains the column’s content and sample values.
>    >   10. Select **Add**.
>    >
>    >   If you omit **Source stage** and **Relative path column**, citations still appear, but Snowflake CoWork can’t open the original file in the in-app document viewer. In-app preview supports PDF files. The role that queries the agent must have READ on the stage.
>    > - **To enable analytical search for a Cortex Search service**: After adding a Cortex Search service, toggle **Analytical Search** on to allow the agent to run extensive analytics on your search indexes. Analytical search is off by default. Additional costs apply when using AI functions. For more information, see [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search).
>    > - **To add a custom tool to the agent**: By adding custom tools, you can extend the functionality of your agents. With custom tools, the agent can call stored procedures and functions that you have defined to perform actions or do computations. This section assumes that you’ve already created a custom tool. For information about procedures and functions, see [Extending Snowflake with Functions and Procedures](/developer-guide/extensibility).
>    >
>    >   > 1. Find **Custom tools** and select the respective **+ Add** button.
>    >   > 2. For **Name**, enter a name for the custom tool.
>    >   > 3. For **Resource type**, select whether the custom tool is a function or a procedure. For information about whether to use a function or procedure, see [Choosing whether to write a stored procedure or a user-defined function](/developer-guide/stored-procedures-vs-udfs).
>    >   > 4. For **Custom tool identifier**, select the existing function or procedure that you want to add as a custom tool.
>    >   > 5. The related parameters for the function or procedure automatically appear. You can manually add parameters for the custom tool by adding a name, type, description, and selecting whether the parameter is required. You can also modify parameters that automatically populate.
>    >   >
>    >   >    Note
>    >   >
>    >   >    Snowflake Cortex does not support stored procedures and custom tools with a parameter of type `object`.
>    >   > 6. For **Warehouse**, select the warehouse that the agent uses to run the custom tool. You must manually select a warehouse.
>    >   > 7. For **Description**, describe the custom tool and how to use it.
>    >   > 8. Select **Add**.
>    >   > 9. After creating the custom tool, make sure users are granted USAGE privileges to the function or procedure that you added as a custom tool. When using stored procedures, agents maintain whether the procedure runs with owner’s or caller’s rights. For information about owner’s and caller’s rights, see [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
>    > - **To add the web search tool to the agent**: This section assumes that you’ve already enabled web search at the account level. For information about enabling web search at the account level, see [Web search](#label-cortex-agents-web-search).
>    >
>    >   1. Find **Web search** and select the respective toggle to enable the feature.
> 7. Select **Save**.
>
> To add tools to an agent using the REST API, add the following payloads as part of a request to [Update Cortex Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agents-rest-api-update). You can also specify these fields when creating the agent object.
>
> > - **Add Cortex Analyst tool and tool resources**: The following example shows how to add a Cortex Analyst tool and tool resources to an existing agent object.
> >
> >   1. Add a Cortex Analyst tool
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tools": [
> >        {
> >         "tool_spec": {
> >          "description": "Analyst to analyze price",
> >          "type": "cortex_analyst_text_to_sql",
> >          "name": "Analyst1"
> >         }
> >        }
> >       ]
> >      }'
> >      ```
> >   2. Add a Cortex Analyst tool resource
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tool_resources": {
> >        "Analyst1": {
> >         "semantic_model_file": "stage1",
> >         "semantic_view": "The name of the Snowflake native semantic model object",
> >         "execution_environment": {"type":"warehouse", "warehouse":"my_wh"}
> >        }
> >       }
> >      }'
> >      ```
> > - **Add Cortex Search tool and tool resources**: The following example shows how to add a Cortex Search tool and tool resources to an existing agent object.
> >
> >   1. Add a Cortex Search tool
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tool_spec": {
> >        "type": "cortex_search",
> >        "name": "Search1"
> >       }
> >      }'
> >      ```
> >   2. Add a Cortex Search tool resource:
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tool_resources": {
> >        "Search1": {
> >         "search_service": "db.schema.service_name",
> >         "filter": {"@eq": {"region": "North America"} },
> >         "max_results": 10,
> >         "title_column": "TITLE",
> >         "id_column": "<column_name>",
> >         "stage_path": "@<db>.<schema>.<stage_name>",
> >         "relative_path_column": "<relative_path_column_name>",
> >         "columns_and_descriptions": {
> >           "TEXT": {
> >       "description": "The main text content of the document",
> >       "type": "string",
> >       "searchable": true,
> >       "filterable": false
> >           },
> >           "CATEGORY": {
> >       "description": "Document category. Values include: policy, guide, reference.",
> >       "type": "string",
> >       "searchable": false,
> >       "filterable": true
> >           },
> >           "AUTHOR": {
> >       "description": "Author name in format: firstname.lastname",
> >       "type": "string",
> >       "searchable": false,
> >       "filterable": true
> >           }
> >         }
> >        }
> >       }
> >      }'
> >      ```
> >
> >      The `columns_and_descriptions` field is a map of column names to column properties. Descriptions are not required for all columns, but providing them for filterable and searchable columns improves the quality of results. Each column entry must include:
> >
> >      - `description` (string): A description of the column content and sample values. Include guidance on when and how to filter on this column.
> >      - `type` (string): The column data type. Use `"string"` or `"datetime"`.
> >      - `searchable` (boolean): Set to `true` for text index columns that can be searched. Vector index columns are not supported.
> >      - `filterable` (boolean): Set to `true` for attribute columns that can be used in filter conditions.
> > - **Enable analytical search**: After the agent has a Cortex Search tool, set `orchestration.capabilities.analytical_search` to `true`. Analytical search is disabled by default. If the agent already has budget or other orchestration settings, include those fields in the same `orchestration` object so they aren’t removed.
> >
> >   Copy code
> >
> >   ```
> >   curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >   --header 'Content-Type: application/json' \
> >   --header 'Accept: application/json' \
> >   --header "Authorization: Bearer $PAT" \
> >   --data '{
> >    "orchestration": {
> >     "capabilities": {
> >      "analytical_search": true
> >     }
> >    }
> >   }'
> >   ```
> > - **Add data\_to\_chart tool**: The following example shows how to add the data to chart tool to an existing agent object.
> >
> >   1. Add the data\_to\_chart tool
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tools": [
> >        {
> >         "tool_spec": {
> >           "type": "data_to_chart",
> >           "name": "data_to_chart",
> >           "description": "Generates visualizations from data"
> >         }
> >        }
> >       ]
> >      }'
> >      ```
> > - **Add custom tool and tool resources**: The following example shows how to add a custom tool and tool resources to an existing agent object.
> >
> >   1. Add a custom tool
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tools": [
> >        {
> >         "tool_spec": {
> >           "description": "Custom tool",
> >           "type": "generic",
> >           "name": "custom1"
> >         }
> >        }
> >       ]
> >      }'
> >      ```
> >   2. Add a custom tool resource
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tool_resources": {
> >        "custom1": {
> >         "user-defined-function-argument": "argument1"
> >        }
> >       }
> >      }'
> >      ```
> > - **Add web\_search tool**: The following example shows how to add the web\_search tool to an existing agent object. This section assumes that you’ve already enabled web search at the account level. For information about enabling web search at the account level, see [Web search](#label-cortex-agents-web-search).
> >
> >   1. Add the web\_search tool
> >
> >      Copy code
> >
> >      ```
> >      curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
> >      --header 'Content-Type: application/json' \
> >      --header 'Accept: application/json' \
> >      --header "Authorization: Bearer $PAT" \
> >      --data '{
> >       "tools": [
> >        {
> >         "tool_spec": {
> >           "type": "web_search",
> >           "name": "Web Search"
> >         }
> >        }
> >       ]
> >      }'
> >      ```
>
> You can update an agent object to add tools and tool resources using the ALTER AGENT command. For information about the ALTER AGENT command, see [ALTER AGENT](/sql-reference/sql/alter-agent).
>
> Note
>
> The new specification completely replaces the existing one. Fields that are not included in the new specification are removed.
>
> Copy code
>
> ```
> ALTER AGENT <agent_name> MODIFY LIVE VERSION SET SPECIFICATION =
> $$
> models:
>     orchestration: auto
>
>   orchestration:
>     capabilities:
>       analytical_search: true
>     tool_not_accessible: accept
>     budget:
>       seconds: 30
>       tokens: 16000
>
>   instructions:
>     response: "You will respond in a friendly but concise manner"
>     orchestration: "For any revenue question use Analyst; for policy use Search"
>     sample_questions:
>       - question: "What was our revenue last quarter?"
>
>   tools:
>     - tool_spec:
>         type: "cortex_analyst_text_to_sql"
>         name: "Analyst1"
>         description: "Converts natural language to SQL queries for financial analysis"
>     - tool_spec:
>         type: "cortex_search"
>         name: "Search1"
>         description: "Searches company policy and documentation"
>     - tool_spec:
>         type: "data_to_chart"
>         name: "data_to_chart"
>         description: "Generates visualizations from data"
>
>   tool_resources:
>     Analyst1:
>       semantic_view: "db.schema.semantic_view"
>     Search1:
>       search_service: "db.schema.service_name"
>       max_results: "5"
>       filter:
>         "@eq":
>           region: "North America"
>       title_column: "<title_name>"
>       id_column: "<column_name>"
>       stage_path: "@<db>.<schema>.<stage_name>"
>       relative_path_column: "<relative_path_column_name>"
> $$;
> ```

### Web search

Cortex Agents use the Brave Web Search API to retrieve real-time information during an interaction. The agent creates a query based on the user’s input and any relevant context, and the API returns results from Brave Search’s independent web index. The agent then incorporates relevant results into its response alongside data from other configured tools.

Note that the query and the results leave Snowflake and traverse the public internet. However, Snowflake has enabled zero data retention (ZDR) with Brave: Brave does not store the search query text, the results returned, or any metadata associated with the request, for any length of time.

Before agents can use the web search tool, an ACCOUNTADMIN must enable web search at the account level:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select **Settings**.
4. Select the **Web search** toggle to enable the feature, as shown below.

![Enable web search toggle](/static/images/cortex-code/enable-websearch.png)

After enabling web search at the account level, you can add the web search tool to your agents.

## Specify orchestration

Cortex Agents orchestrate the task by breaking it into a sequence of sub-tasks and identifying the right tool for each sub-task. You specify the LLM that the agent should use to conduct this orchestration. You can also influence the orchestration by providing instructions. For example, consider an agent built to respond to retail product questions. You can use the orchestration instruction `"Use the search tool for all requests related to refunds"` to ensure the agent only provides refund policy details (using Cortex Search) and does not actually calculate the refund amounts (using Cortex Analyst). You can also specify instructions to align the response to a brand or a tone, such as `"Always provide a concise response; maintain a friendly tone"`.

Use `orchestration.tool_not_accessible` to control whether a missing tool privilege aborts the run or lets the agent continue with the tools it can access. For details, see [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

Method 1: Snowsight UIMethod 2: REST APIMethod 3: SQL

1. Select **Orchestration**.
2. For the **Orchestration model**, select the model that the agent uses to handle orchestration.
3. For **Planning instructions**, provide instructions that influence tool selection by the agent based on user-provided input. These can include specific instructions about when to use each tool, or even to always use a tool at the beginning or end of a response.
4. For **Response instruction**, provide instructions that the model uses for response generation. For example, specify if you want the agent to prioritize chart creation, or to keep a certain tone with users.
5. For **Budget configuration**, you can specify time limit and token limit for the agent. The budget is the maximum amount of time or tokens that the agent can use to generate a response. After either one of the limits is reached, the agent will stop generating a response. Token limits are used only for orchestration and don’t include tokens used by Cortex Analyst, Cortex Search, and other tools invoked.
6. Select **Save**.

> To update an agent using the REST API, add the following payloads as part of a request to [Update Cortex Agent](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agents-rest-api-update). You can also specify these fields when creating the agent object. The following procedure shows how to update the agent with planning and response instructions, and specify the LLM model used for orchestration.

1. Update the LLM model

   Copy code

   ```
   curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
   --header 'Content-Type: application/json' \
   --header 'Accept: application/json' \
   --header "Authorization: Bearer $PAT" \
   --data '{
    "models": {
     "orchestration": "claude-sonnet-5"
    }
   }'
   ```
2. Specify the planning and response instructions

   Copy code

   ```
   curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
   --header 'Content-Type: application/json' \
   --header 'Accept: application/json' \
   --header "Authorization: Bearer $PAT" \
   --data '{
    "instructions": {
     "response": "Always provide a concise response and maintain a friendly tone.",
     "orchestration": "<orchestration instructions>"
    }
   }'
   ```
3. Specify what happens when a tool isn’t accessible. For values and default behavior, see [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

   Copy code

   ```
   curl -X PUT "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>" \
   --header 'Content-Type: application/json' \
   --header 'Accept: application/json' \
   --header "Authorization: Bearer $PAT" \
   --data '{
    "orchestration": {
     "tool_not_accessible": "accept"
    }
   }'
   ```

You can update an agent object to add orchestration information using the ALTER AGENT command. For information about the ALTER AGENT command, see [ALTER AGENT](/sql-reference/sql/alter-agent).

Copy code

```
ALTER AGENT <agent_name> MODIFY LIVE VERSION SET SPECIFICATION =
$$
models:
    orchestration: auto

  orchestration:
    capabilities:
      analytical_search: true
    tool_not_accessible: accept
    budget:
      seconds: 30
      tokens: 16000

  instructions:
    response: "You will respond in a friendly but concise manner"
    orchestration: "For any revenue question use Analyst; for policy use Search"
    sample_questions:
      - question: "What was our revenue last quarter?"

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "Analyst1"
        description: "Converts natural language to SQL queries for financial analysis"
    - tool_spec:
        type: "cortex_search"
        name: "Search1"
        description: "Searches company policy and documentation"
    - tool_spec:
        type: "data_to_chart"
        name: "data_to_chart"
        description: "Generates visualizations from data"

  tool_resources:
    Analyst1:
      semantic_view: "db.schema.semantic_view"
    Search1:
      search_service: "db.schema.service_name"
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

To enable analytical search, set `orchestration.capabilities.analytical_search` to `true` as shown in the example.
Analytical search is disabled by default. The new specification completely replaces the existing one, so include the
complete LIVE specification from `DESCRIBE AGENT`. For more information, see
[Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search#label-enable-analytical-search).

## Review the agent

After you have built the agent, you can review the agent to verify all parameters.

Method 1: Snowsight UIMethod 2: REST APIMethod 3: SQL

Note

When reviewing agents from Snowsight, you can only view agents in the Agent Admin UI. You cannot view agents in the Horizon Catalog Explorer.

1. In the navigation menu, select **AI & ML** » **Agents**.
2. From the list of agents, select the agent that you want to view the details for. This opens a new page that gives an overview of the agent details.
3. To review all agent details, select **Next**.

You can list and describe agents using the REST APIs.

1. List all agents.

   Copy code

   ```
   curl -X GET "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/{database}/schemas/{schema}/agents:" \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --header "Authorization: Bearer $PAT" \
   ```
2. Describe the desired agent.

   Copy code

   ```
   curl -X GET "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/{database}/schemas/{schema}/agents/{name}:" \
    --header 'Content-Type: application/json' \
    --header 'Accept: application/json' \
    --header "Authorization: Bearer $PAT" \
   ```

You can list and describe agents using SQL.

1. List all agents.

   Copy code

   ```
   SHOW AGENTS IN ACCOUNT;
   ```
2. Describe the desired agent.

   Copy code

   ```
   DESCRIBE AGENT myagent;
   ```

## Test the agent

After you’ve created the agent, you can test it to see how it responds to user queries. You can also test the agent using [Agent run request with agent object](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-data-agents-run-rest-api).

To test the agent, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select the agent from the list of agents.
4. On the agent details page, enter a query in the agent playground.
5. Verify that the agent responds to the query as expected. If the agent does not respond as expected, modify the agent’s configuration by following the steps in [Add tools](#label-snowflake-agents-modify-agents).

## Interact with the agent

After creating the agent object, you can integrate the agent directly into your application using the REST API. To maintain context during the interaction, use a thread. The agent object and thread combined simplify the client application code.

### Create a thread

Create a thread to maintain the context during a conversation. When the thread is created successfully, the system returns a `Thread ID`.

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/cortex/threads" \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
    "origin_application": <application_name>
}'
```

### Send a request to the agent

To interact with the agent, you must pass the agent object, thread ID, and a unique `parent_message_id` as part of your REST API request. The initial `parent_message_id` should be `0`.

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/{database}/schemas/{schema}/agents/{name}:run" \
 --header 'Content-Type: application/json' \
 --header 'Accept: application/json' \
 --header "Authorization: Bearer $PAT" \
 --data '{
     "thread_id": <thread id for context>,
     "parent_message_id": <parent message id>,
     "messages": [
      {
         "role": "user",
         "content": [
           {
            "type": "text",
              "text": "What are the projected transportation costs for the next three quarters?"
             }
         ]
       }
     ],
     "tool_choice": {
       "type": "required",
       "name": [
         "Analyst1",
         "Search1"
       ]
     }
 }'
```

## Collect feedback about the agent

You can collect feedback from users about the responses given by the agent. This feedback can help you refine the agent as you iterate on your use case. Users can provide an objective rating (positive/negative), as well as more subjective detail with a message. Also, users can classify the feedback across one of many categories.

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/<database-name>/schemas/<schema-name>/agents/<agent-name>:feedback:" \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "Authorization: Bearer $PAT" \
--data '{
    "request_id": "<request-id>",
    "positive": true,
    "feedback_message": "This answer was great",
    "categories":[
        "category1", "category2", "category3"
    ],
    "thread_id": "<thread-id>"
}'
```

## Interact without an agent object

In some cases, you may want to get started with Cortex Agents by using `agent:run` without an agent object. For example, this may be useful when you want to quickly try out a use case. For more information about the REST API, see [Agent run without an agent object](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-lite-agents-run-rest-api).

Note

When interacting with an agent without creating an agent object, you must manually maintain the context for the agent with every request.
