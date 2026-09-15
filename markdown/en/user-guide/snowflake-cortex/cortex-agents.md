# Cortex Agents

Get started with Cortex Agents

[Try it in Snowsight](https://app.snowflake.com/_deeplink/#/agents?utm_source=docs&utm_medium=growth&utm_campaign=-us-en-all&utm_content=-app-user-guide-snowflake-cortex-cortex-agents)

## Overview

Cortex Agents is a fully managed agentic platform for building and running AI agents within Snowflake’s governed environment. An agent reasons over a request, plans the work, calls tools, executes code, and generates a response, without requiring you to build or operate your own orchestration loop, runtime, or sandbox infrastructure. Data access is governed by Snowflake privileges and the execution context of each configured tool.

Agents bring your structured and unstructured data together in a single governed workflow. They generate SQL over structured data using Cortex Analyst semantic views and use Cortex Search to retrieve insights from unstructured sources, then reason over the combined results. You can extend what an agent can do with several types of tools:

- A built-in [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) that, when enabled, runs Python in a secure, isolated sandbox to process data and perform calculations.
- A Data to Chart tool that generates visualizations from data.
- Custom tools built from stored procedures and user-defined functions (UDFs) to call backend systems or implement your own business logic.
- Packaged agent skills, modular bundles of instructions and scripts that give an agent repeatable, task-specific capabilities.
- MCP connectors to remote Model Context Protocol (MCP) servers, letting agents discover and invoke tools hosted by providers such as Atlassian Jira, Salesforce, or your own applications.
- Web search for real-time information from the public internet.

Threads maintain conversation context across turns, so your client application doesn’t have to manage state. After deployment, you can monitor agents, collect end-user feedback, and run evaluations to continuously refine their behavior.

To answer a request, an agent follows a reasoning loop with three steps:

1. **Plan**: The agent parses the request and decides how to answer it. It can disambiguate a vague question (for example, “Tell me about Acme Supplies” might refer to products, location, or sales personnel), split a complex request into subtasks (for example, “What are the differences between contract terms for Acme Supplies and Acme Stationery?”), and choose which tool to use for each part.
2. **Use tools**: The agent calls the tools it selected, such as Cortex Analyst for structured data, Cortex Search for unstructured data, or the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) to process results.
3. **Reflect and respond**: The agent evaluates the results from each tool to decide what to do next, whether that’s asking a clarifying question, calling another tool, or generating a final response. This loop lets the agent handle complex, multi-step questions.

The agent repeats this loop as needed within a single request.

You define an agent as a reusable object that bundles its model, tools, and orchestration instructions. Create one in Snowsight, with the Cortex Agents SQL commands, or through the REST API, then integrate it into your application using the REST API. You guide its behavior with natural-language instructions, and you can choose the language model that powers it or let Snowflake select one automatically. In addition to calling agents from your own applications through the REST API, users can interact with them in [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) and [Cortex Code](/user-guide/cortex-code/cortex-code).

An agent’s tools give it access to your data. An agent with no tools configured can still
hold a conversation, but it answers only from the language model’s general knowledge and can’t query
anything in your account. If the caller’s role can’t use every configured tool, the run can still
continue with the tools it can access. See [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

To build your first agent end to end, see [Get started with Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-get-started).
For more scenarios, see
[Tutorials](/user-guide/snowflake-cortex/cortex-agents-get-started#label-cortex-agents-get-started-tutorials).

Note

While Snowflake strives to provide high-quality responses, the accuracy of the LLM responses or
the citations provided is not guaranteed. You should review all answers from the Agents API before serving them to your users.

## Key concepts

Cortex Agents is built around the following concepts:

| Concept | Description |
| --- | --- |
| **Agent** | A schema-level object that bundles the agent’s model, tools, orchestration settings, and instructions. Create it once and reuse it across interactions and applications. |
| **Tools** | How the agent acts on your data and systems: Cortex Analyst, Cortex Search, [code execution](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool), custom tools, and more. See [Tools](#label-cortex-agents-tools). |
| **Orchestration** | The LLM-driven plan, use tools, reflect loop the agent runs to answer a request. You shape it with natural-language planning and response instructions. |
| **Thread** | Persisted conversation context across turns, so your client application doesn’t manage state. Create a thread object and reference its ID in agent interactions. |
| **Run** | A single request to an agent through the `agent:run` API. The agent emits events throughout the run that surface its reasoning, tool calls, and reflections. |

Expand

Show lessSee more

### Models

When creating an agent, we recommend selecting **auto** for the model. With this option, Cortex automatically selects the highest quality model for your account, and quality improves as new models become available.

Cortex Agents supports the following models. These models run through [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference), so availability is shown by cross-region routing scope (the value of the `CORTEX_ENABLED_CROSS_REGION` account parameter), not by individual region. A model is available to your account when your routing scope is marked for that model. Columns match the scopes listed in [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability) and [Model availability](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-complete-llm-model-availability).

| Provider | Model | Status | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region) | Azure EU (Cross-Region) | Google Cloud US (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anthropic | `claude-opus-5` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-opus-4-8` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-opus-4-7` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-opus-4-6` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-opus-4-5` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ |  |  |  |  |  |  |  |
| Anthropic | `claude-sonnet-5` | GA | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-sonnet-4-6` | GA | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| Anthropic | `claude-sonnet-4-5` | GA | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  | ✔ |  |  |
| Anthropic | `claude-4-sonnet` (legacy) | GA | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ |  |  |  |  |  |  |
| Anthropic | `claude-haiku-4-5` | GA | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  |  |  |  |  |
| OpenAI | `openai-gpt-5.4` | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| OpenAI | `openai-gpt-5.2` | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| OpenAI | `openai-gpt-5.1` | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| OpenAI | `openai-gpt-5` | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |  |
| OpenAI | `openai-gpt-5-mini` | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| OpenAI | `openai-gpt-4.1` (legacy) | GA | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |  |
| Google | `gemini-3.1-pro` | Public preview | ✔ |  |  |  |  |  |  |  |  |  |  |  |  | ✔ |
| Google | `gemini-3.5-flash` | GA | ✔ |  |  |  |  |  |  |  |  |  |  |  |  | ✔ |

Expand

Show lessSee more

Public preview models aren’t intended for production workloads. After a model’s legacy date, only
accounts that already used the model can continue to call it until end-of-life; accounts that had
not used it can’t start. Run [SHOW CORTEX BASE MODELS](/sql-reference/sql/show-cortex-base-models)
to see legacy and end-of-life dates, and switch to a newer model before then.

## How it works

Building with Cortex Agents follows a five-step lifecycle:

1. **Create an agent**: Define the agent object in Snowsight, with SQL, or through the REST API, including its name, model, and instructions. See [Create an agent](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-create).
2. **Add tools**: Configure the tools the agent can use and the resources each tool needs, such as semantic views, search services, and warehouses. See [Add tools](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-modify-agents).
3. **Test the agent**: Prompt the agent in the Snowsight playground and refine its tools and instructions until it responds as expected. See [Test the agent](/user-guide/snowflake-cortex/cortex-agents-manage#label-snowflake-agents-use-agent).
4. **Integrate it into your application**: Call the agent through the `agent:run` REST API, using threads to maintain conversation context. Users can also interact with agents directly in [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) and [Cortex Code](/user-guide/cortex-code/cortex-code). See [Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run).
5. **Monitor, evaluate, and iterate**: Review threads, logs, and traces, collect end-user feedback as ratings and free-text comments, and run evaluations to refine the agent over its lifecycle. See [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor) and [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations).

If you want to experiment before creating an agent object, you can call `agent:run` directly and pass the agent configuration with every request. See [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## When to use Cortex Agents

Cortex Agents is best for workloads that need:

- **Reasoning across structured and unstructured data**: Questions whose answers combine SQL results over semantic views with retrieval from documents and other unstructured sources.
- **Multi-step task execution**: Requests that the agent must break into subtasks, route to different tools, and reflect on intermediate results.
- **Minimal infrastructure**: No orchestration loop, runtime, or sandbox to build or operate; Snowflake manages all of it.
- **Governance**: Data access controlled by your existing Snowflake roles and privileges, and by the execution context of each configured tool.
- **Stateful conversations**: Threads that persist context across turns without client-side state management.

Most tools run entirely inside Snowflake. Tools that reach external services, such as [web search](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-web-search) and [MCP connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors), send requests over the public internet.

## Tools

Cortex Agents supports the following tools:

| Tool | Description |
| --- | --- |
| Cortex Analyst | Generates SQL queries over your structured data from natural language, using a semantic view. |
| Cortex Search | Retrieves information from your unstructured data. Agents can dynamically adjust filters, retrieved columns, result counts, per-index queries, and time-decay settings based on the user’s query. |
| Analytical search (Public Preview) | Answers analytical questions, such as counts, aggregates, and trends, over large document collections by combining Cortex Search with AI functions and SQL. See [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search). |
| [Code execution](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) | Runs Python in a secure, isolated sandbox to process data and perform calculations. |
| Data to Chart | Generates visualizations from data returned by other tools. |
| Custom tools | Stored procedures and user-defined functions (UDFs) that implement your own business logic or call backend systems. |
| Agent skills | Packaged, modular bundles of instructions and scripts that give an agent repeatable, task-specific capabilities. |
| MCP connectors | Tools hosted on remote Model Context Protocol (MCP) servers, such as those from Atlassian Jira, Salesforce, or your own applications. |
| Agent toolsets | References to other agents whose tools are inherited at run time, enabling modular and composable agent architectures. See [Agent toolsets](/user-guide/snowflake-cortex/cortex-agents-toolsets). |
| Web search | Real-time information from the public internet. Must be enabled at the account level. See [Web search](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-web-search). |

Expand

Show lessSee more

For how to add and configure each tool, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Access control and authentication

Calling an agent requires the SNOWFLAKE.CORTEX\_USER or SNOWFLAKE.CORTEX\_AGENT\_USER database role, privileges on the agent object, and privileges on the objects used by the agent’s tools. If the user’s role is missing privileges on a tool, the request is rejected with a 4XX error. Cortex Agents determines session permissions from the querying user’s default role. Requests to the Cortex Agents API must include an authorization token.

For the full requirements, including role setup, privilege tables, and authentication methods, see [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).

## Limitations

Cortex Agents APIs are not supported from within a Streamlit in Snowflake (SiS) application using a warehouse runtime. To call Cortex Agents APIs from a SiS app, use a container runtime instead. For more information, see [Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

## Cost considerations

Cortex Agents incurs charges for orchestration and for the tools the agent uses:

- Orchestration is charged based on the tokens used.
- Cortex Analyst is charged per token.
- Cortex Search charges depend on the size of the index and the time it has persisted.
- Custom tools incur [warehouse costs](/user-guide/cost-understanding-compute), which depend on the size of the warehouse and how long it runs.
- [Analytical search](/user-guide/snowflake-cortex/cortex-agents-analytical-search) adds warehouse compute for SQL execution, plus the [AI functions](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations) it calls. These extra costs apply only when analytical search is enabled on the agent and the agent runs the analytical search loop.

This list isn’t exhaustive. Tools that run their own compute or call other services, including
[web search](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-web-search), the
[code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool),
[MCP connectors](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors), and
[agent skills](/user-guide/snowflake-cortex/cortex-agents-skills), can add cost beyond orchestration.
For the rates that apply to each feature, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

To limit what a single run consumes, set an orchestration budget on the agent. To monitor spend for an agent object and act when that spend crosses a threshold, use [resource budgets](/user-guide/snowflake-cortex/cortex-agents-resource-budgets). To enforce monthly or daily credit limits for individual users, and optionally block users who reach their AI quota, use [per-user quotas](/user-guide/budgets/per-user-quotas).

## Legal notices

Where your configuration of Cortex Agents uses a model provided on the
[Model and Service Flow-down Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
