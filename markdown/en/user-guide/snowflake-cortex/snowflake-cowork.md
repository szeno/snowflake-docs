# Overview of Snowflake CoWork

Snowflake CoWork is a ready-to-use agentic application with an intuitive, conversational interface
that helps business users discover and act on deep insights. It lets users interact with their
structured and unstructured enterprise data using natural language. Snowflake CoWork uses
AI-powered “data agents” to:

- Understand questions
- Perform analysis
- Generate trusted insights
- Take action

It bridges the gap between valuable enterprise data and the people who need it, empowering users
to move beyond stale dashboards and rigid reports. Users are empowered to find answers independently,
reducing their reliance on data teams. Insights are trustworthy with full traceability, while
respecting Snowflake’s robust security and governance policies.

## Key capabilities

Business users are often stuck navigating stale dashboards that can’t keep up with their questions
and waiting on data teams for answers. Snowflake CoWork solves this with the following capabilities:

- **Natural language interaction**: An intuitive, conversational interface allows users to ask
  questions using natural language and receive deep insights.
- **Unified data access**: Analyzes both structured and unstructured data from enterprise sources.
- **Deep, trustworthy insights**: Breaks down questions and chooses the best tools to deliver
  accurate, actionable insights. Provides traceability to source data
  and queries, while “Verified Answers” allow data teams to add trusted responses.
- **Built-in visualization**: Instantly generates and customizes charts to help visualize trends
  and patterns, with clear explanations about how each chart was created. The agent determines
  whether data is best shown as a chart or table based on the query type. Trends and comparisons
  render as visualizations, while detailed lookups return tables. Snowflake CoWork supports
  most [Vega-Lite](https://vega.github.io/vega-lite/examples/) chart types, including
  area charts, heatmaps, box plots, dual-axis and layered charts, faceted small-multiple charts,
  error bars, and text annotations, in addition to bar, line, pie, and scatter charts. Geographic
  map charts are not supported. Users can customize chart preferences through agent instructions,
  including default chart types, colors, and formatting rules. For more information, see
  [Customize charts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/chart-customization).
- **Artifacts**: A persistent chart or table object that Snowflake CoWork generates in response to a question. Save, share, and revisit tables and charts without regenerating them. For more information, see [Artifacts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/artifacts).
- **Automations**: Turn a one-time report into a recurring one that re-runs your question with fresh data and emails you the results. Set up and manage automations conversationally or from the **Automations** tab. For more information, see [Automations in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/automations).
- **User skills**: Codify a repeatable workflow once, then reuse it explicitly with `/` or from the Skills menus, or implicitly when your conversation matches the skill. Create skills conversationally, from the **+** menu (**Create new**), or by uploading a skill folder. For more information, see [User skills in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/user-skills).
- **Document generation**: Turn analysis into shareable files such as PDF documents and PowerPoint presentations. Upload a PowerPoint template to match your organization’s style, or customize behavior with a user or agent skill. Requires the [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) on the associated agent. For more information, see [Document generation in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation).
- **Seamless governance**: Automatically inherits and respects all existing Snowflake data governance
  controls, including row-access policies and column-level security.
- **Full administrative control**: Administrators can use existing identity providers to give teams
  access only to Snowflake CoWork, making sure users only interact with the data experiences built
  for them.

### Snowflake CoWork Mobile App (iOS)

The Snowflake CoWork mobile app for iOS is available on the [App Store](https://apps.apple.com/us/app/snowflake-intelligence/id6755540372). The app supports the same features as the web app, so you can ask questions about your data, continue conversations, and review results from anywhere. It supports chat, agents, file and image attachments, voice input, citations, and role and warehouse selection, extending the core experience to mobile in a secure, touch-first format.

### Additional UI options

Snowflake CoWork offers the following additional options for users from the UI:

#### Deep Research

Deep Research is an investigation mode for complex, open-ended questions that require multi-step
reasoning across your data. Instead of returning a single result, Snowflake CoWork decomposes the
question into multiple sub-investigations, runs them in parallel across your structured and
unstructured data, and synthesizes the findings into a structured report. Every claim in the
report is traced back to its source data and queries, so you can verify the reasoning and share
results with confidence.

Reach for Deep Research when you need to understand why something happened, when the answer likely
spans multiple tables or domains, or when you want a citable report you can hand to stakeholders.
Examples include questions like “Why has forecast accuracy been declining, and what’s driving the
variance?” or “Which customer segments show early churn signals, and what do they share?” For
specific lookups, quick metrics, or interactive follow-ups, the standard chat experience is faster
and better suited.

To start an investigation, select the **+** button in the message bar and choose **Deep Research**.
Investigations can take up to 10 minutes to complete. When the report is ready, it stays in context
for the rest of the thread, so follow-up questions such as “break that down by region” run as
standard chat turns without restarting the research.

Deep Research compared to extended thinking

Deep Research and extended thinking solve different problems and can be used together. Extended
thinking is internal reasoning: the agent thinks harder on a single answer, validating SQL logic,
joins, and access controls before execution against the same tools and data. Deep Research is
agentic exploration: the agent runs an autonomous loop that cross-references structured tables,
unstructured data in stages, and external context to explain the *why* behind the numbers. You can
enable extended thinking during a Deep Research investigation to combine deeper reasoning with
wider exploration.

#### Extended thinking

By default, Snowflake CoWork agents balance speed and quality when answering questions.

If users have a complex question or want the agent to explore more options, they can enable
extended thinking in the chat window. With extended thinking, the agent will be more thorough, but
the process might take more time and use more tokens. This setting remains selected.

#### Zero-setup file upload

Snowflake CoWork supports uploading files directly in the chat interface to provide more
context for the agent. The agent can use the content of the files to answer questions and provide
insights.

When you upload a file, it is automatically saved in your user stage. The file is accessible within the same thread. Documents are automatically cleaned up when threads are deleted, either by the thread delete API or after the thread TTL (time to live) expires.

Snowflake CoWork supports the following file types for zero-setup file upload:

- Documents: `.pdf`, `.txt`, `.md`, `.docx`, `.doc`
- Spreadsheets: `.xlsx`, `.xls`, `.csv`
- Presentations: `.pptx`
- Code and data: `.json`
- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.bmp`, `.tiff`, `.tif`, `.webp`, `.heic`, `.heif`

Each file must be less than 50 MB, and users can upload up to 5 files.

If the document requires complex processing, the user’s default warehouse might be used to run
Snowpark code for the agent to better analyze and process the data.

Important

Uploaded documents are stored on a personal stage and treated as customer data, following the same data governance and access controls as other Snowflake data. Account administrators have standard access based on existing permissions.

## How it works

Snowflake CoWork combines multiple tools with the following architecture:

[![Describes the architecture of %sf-intelligence%, including the Cortex Agent API, the orchestrator, and the tools.](/static/images/snowflake-intelligence-architecture.png)](/static/images/snowflake-intelligence-architecture.png)

When a user asks a question in Snowflake CoWork, Cortex Agents turn
natural language into governed actions and answers. An interaction with Snowflake CoWork
follows this workflow:

1. **User input**: A user submits a natural language question. For example, “How are Q4 sales trending?”
2. **Cortex Agent API**: The question is routed to the [Cortex Agent API](/user-guide/snowflake-cortex/cortex-agents-rest-api), which powers Snowflake CoWork.
   Agents are AI models that can be connected to one or more semantic views, semantic models, Cortex
   search services, and tools. Agents reason through tasks, choose the right tools, deliver results
   in natural language, and take actions on your behalf. You can create, update, and deploy these
   high-quality agents directly inside your Snowflake environment. Agents integrate
   directly with Snowflake CoWork. For more information, see [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).
3. **Orchestration**: An LLM (the orchestrator) interprets intent, selects the right tools, and
   plans the sequence of actions. It may use one tool, chain several together, or decide that
   the question is out of scope.
4. **Tool execution**: Runs the tools selected by the orchestrator and returns results. You can
   integrate tools to give Snowflake CoWork access to structured and unstructured data, as well
   as existing functions and procedures. Cortex Agents support the following tool types:

   - **Cortex Analyst**: Create SQL queries from natural language, then run these queries on your
     semantic views for structured data with [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst). Semantic views address the mismatch between how business
     users describe data and how it’s stored in database schemas. With semantic views, you can
     define business metrics and model business entities and their relationships. Cortex Agents
     use these semantic views to enhance data-driven decisions and provide consistent business
     definitions across enterprise applications. For more information, see
     [Overview of semantic views](/user-guide/views-semantic/overview).
   - **Cortex Search**: Search through your unstructured data to return relevant document text with [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).
   - **Custom Tools**: Execute user-defined functions or stored procedures to perform actions.
5. **Reflection & response**: The orchestrator reviews and refines results, then generates
   the final answer, including summaries, tables, or charts, in the Snowflake CoWork UI.

## Cost considerations

To monitor spend for a Snowflake CoWork object and act when that spend crosses a threshold, use [resource budgets](/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets). To enforce per-user credit limits for individual users, and optionally block users who reach their AI quota, use [per-user quotas](/user-guide/budgets/per-user-quotas).

## Legal notices

Where your configuration of Snowflake CoWork uses a model provided on the
[Model and Service Flow-down Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs is as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
