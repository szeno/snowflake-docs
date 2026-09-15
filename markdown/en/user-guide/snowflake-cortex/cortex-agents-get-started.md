# Get started with Cortex Agents

This topic gives you two ways to build a working Cortex Agent. You can ask CoCo to build an agent over
your own data, or follow a runnable walkthrough that uses the TPC-H sample data available in most
Snowflake accounts. You don’t need to download or load data.

## Let CoCo walk you through it

If you want to use your own tables, ask CoCo to build the agent. CoCo prompts you for what it needs
and generates the objects:

```
Help me build and deploy a Cortex Agent
```

CoCo asks which data you want the agent to answer questions about, proposes a semantic view over
those tables, creates the agent, and helps you test and refine it. Review each object it proposes
before you let it run the SQL.

Use whichever surface you already work in:

- In Snowsight, select the CoCo icon [![Cortex Code icon](/static/images/cortex-code/cortex-code-icon.png)](/static/images/cortex-code/cortex-code-icon.png) in the lower-right corner. See
  [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight).
- In the CoCo CLI, the [`agent-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio)
  bundled skill handles this workflow. CoCo loads it automatically, or you can name it in your prompt.

Before you use CoCo, complete [Step 1](#label-cortex-agents-get-started-grants), then grant your
default role access to CoCo and read access to the data you want the agent to use:

Copy code

```
USE ROLE ACCOUNTADMIN;

-- Access to CoCo.
GRANT DATABASE ROLE SNOWFLAKE.COPILOT_USER TO ROLE <default_role>;

-- Read access to the tables you point CoCo at.
GRANT USAGE ON DATABASE <source_database> TO ROLE <default_role>;
GRANT USAGE ON SCHEMA <source_database>.<source_schema> TO ROLE <default_role>;
GRANT SELECT ON TABLE <source_database>.<source_schema>.<table> TO ROLE <default_role>;
```

In Snowsight, CoCo starts with your default role regardless of the role selected in the
interface. For the CoCo CLI, use a connection whose role has the same privileges. If your default
role is missing something, you can ask CoCo to switch roles for the session, as in “switch to the
SYSADMIN role”. If you don’t have `ACCOUNTADMIN`, send the preceding block to an administrator along
with the one in step 1: the `SNOWFLAKE.COPILOT_USER` grant is account-level, and the read grants
require a role that can grant privileges on the tables.

When CoCo finishes, you have a working agent. To call it from your own application, see
[Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run).

The rest of this topic uses sample data to cover the same path by hand. Working through it once shows
you what each object does and gives you SQL you can script and repeat. The walkthrough uses SQL to
create and update the agent, and Snowsight to test it. You can perform the same agent
operations with the [Cortex Agents REST API](/user-guide/snowflake-cortex/cortex-agents-rest-api).
The semantic view itself is a Snowflake schema object that you create with SQL.

## What the manual walkthrough builds

An agent that answers natural-language questions about customers and orders, such as “What’s the
average order value by market segment?”

The agent has two names, and they serve different purposes:

- The object name, `sales_agent`, is the identifier you use in SQL and in REST API requests.
- The display name, `Sales Insights Agent`, is what Snowsight and other client applications
  show to users.

You create the agent first, with no tools. It can already answer questions from the language model’s
general knowledge, but it has no access to data in your account. You then create a semantic view and
attach Cortex Analyst, which generates SQL from your question and runs it against that view.

## Before you begin

You need the following:

- A Snowflake account where Cortex Agents is available. See [Governance and availability](/user-guide/snowflake-cortex/governance-and-availability).
- The `ACCOUNTADMIN` role, or an administrator who can run the grants in step 1 for you. Step 1 puts
  all of them in one block you can hand off. After that, you work as your default role until
  [Clean up](#label-cortex-agents-get-started-cleanup), which also needs an administrator if you
  don’t have `ACCOUNTADMIN`.
- A default role and a default warehouse. Step 1 grants the privileges to that role, so you don’t have
  to change your account defaults.
- Cross-region inference enabled, unless every model your agent uses is available in your own region.
  Agents route model calls through cross-region inference, and `CORTEX_ENABLED_CROSS_REGION` defaults
  to `DISABLED` in every account except new organizations created in commercial regions after
  March 9, 2026. Only an account administrator can change it. See
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).
- Access to the `SNOWFLAKE_SAMPLE_DATA` database, which Snowflake provides in most accounts, for the
  manual walkthrough. See [Use the sample database](/user-guide/sample-data-using).
- Optionally, access to CoCo if you want it to build an agent over your own data. CoCo is built into
  Snowsight, but the role you use it with needs the database roles listed in
  [Access control requirements](/user-guide/cortex-code/cortex-code-snowsight#label-cortex-code-snowsight-access-control).

Important

Cortex Agents determines permissions from your **default role**, not the role active in your session.
You must also have a **default warehouse**. If either is missing, agent calls fail even when your
current role has every required privilege.

In this topic, you grant the required privileges to your existing default role so that you don’t have
to change your account defaults. For details, see
[User requirements](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-user-requirements).

## Step 1: Grant the required privileges

First, confirm which role and warehouse are your defaults. Run the following command and note the
`DEFAULT_ROLE` and `DEFAULT_WAREHOUSE` values:

Copy code

```
DESC USER <your_user>;
```

Next, create the database and schema that hold the agent and grant your default role the privileges it
needs. Replace `<default_role>` and `<default_warehouse>` with the values you just noted.

These statements deliberately omit `IF NOT EXISTS` so that they fail rather than reuse a database that
already exists. If `agent_quickstart` is already taken in your account, pick a different name and use
it consistently through the rest of this topic:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE DATABASE agent_quickstart;
CREATE SCHEMA agent_quickstart.demo;

-- Access to Cortex Agents.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE <default_role>;

-- Privileges to create and run the semantic view and the agent.
GRANT USAGE ON DATABASE agent_quickstart TO ROLE <default_role>;
GRANT USAGE ON SCHEMA agent_quickstart.demo TO ROLE <default_role>;
GRANT CREATE SEMANTIC VIEW ON SCHEMA agent_quickstart.demo TO ROLE <default_role>;
GRANT CREATE AGENT ON SCHEMA agent_quickstart.demo TO ROLE <default_role>;
GRANT USAGE ON WAREHOUSE <default_warehouse> TO ROLE <default_role>;

-- Read access to the sample data the semantic view is built on.
GRANT IMPORTED PRIVILEGES ON DATABASE snowflake_sample_data TO ROLE <default_role>;
```

If you don’t have `ACCOUNTADMIN`, you don’t have to stop here. Send the preceding block to an
administrator and ask them to run it, filling in your default role and warehouse. Mention the
following:

- If cross-region inference is disabled in your account, they also need to run
  `ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';`. See
  [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).
- If you plan to build the agent with CoCo, they also need to grant
  `SNOWFLAKE.COPILOT_USER` and read access to the tables CoCo uses. See
  [Let CoCo walk you through it](#label-cortex-agents-get-started-coco).
- Every step after this one except [Clean up](#label-cortex-agents-get-started-cleanup) runs as your
  default role. If you don’t have `ACCOUNTADMIN`, the same administrator needs to drop the database
  when you’re done.

Note

The `SNOWFLAKE.CORTEX_USER` database role is granted to `PUBLIC` by default, so your role might
already have access to Cortex Agents. To check, run `SHOW GRANTS TO ROLE <default_role>;` and look for
`CORTEX_USER` or `CORTEX_AGENT_USER`. Granting `SNOWFLAKE.CORTEX_AGENT_USER` explicitly makes this
walkthrough work even in accounts where that default grant was revoked. For the difference between
the two roles, see [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).

## Step 2: Create the agent

Create the agent object with no tools. Replace `<default_role>` and `<default_warehouse>` with the
values you noted in step 1:

Copy code

```
USE ROLE <default_role>;
USE WAREHOUSE <default_warehouse>;
USE SCHEMA agent_quickstart.demo;

CREATE OR REPLACE AGENT agent_quickstart.demo.sales_agent
  COMMENT = 'Quickstart agent for questions about sample sales data'
  PROFILE = '{"display_name": "Sales Insights Agent"}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: auto

  instructions:
    response: "Answer concisely."
  $$;
```

A few things worth noting:

- `orchestration: auto` lets Snowflake pick the model, so your agent keeps working as models change.
  See [Models](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-models).
- `COMMENT` describes the object, while `display_name` in `PROFILE` is what client applications show
  to users.

Verify that the agent exists:

Copy code

```
DESCRIBE AGENT agent_quickstart.demo.sales_agent;
```

## Step 3: Ask the agent a question

The agent is already usable. Test it in Snowsight before you give it any data:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select **Sales Insights Agent** from the list.
4. In the agent playground, enter a general-knowledge question, such as “What is a semantic view?”
5. Review the answer.

The agent replies from the language model’s general knowledge. It does not run SQL, and it can’t see
the tables in your account. After you attach Cortex Analyst, you can ask questions about your data.

If the agent doesn’t appear in the list, your role is missing `USAGE` on the agent, database, or
schema.

## Step 4: Create a semantic view

Cortex Analyst needs a [semantic view](/user-guide/views-semantic/overview) to know what your data
means: which tables to join, which columns to treat as dimensions, and how to calculate metrics.

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW sales_insights

  TABLES (
    customers AS SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER
      PRIMARY KEY (c_custkey)
      COMMENT = 'One row per customer',
    orders AS SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS
      PRIMARY KEY (o_orderkey)
      COMMENT = 'One row per sales order'
  )

  RELATIONSHIPS (
    orders_to_customers AS
      orders (o_custkey) REFERENCES customers
  )

  DIMENSIONS (
    customers.customer_name AS c_name
      WITH SYNONYMS = ('customer', 'account name')
      COMMENT = 'Name of the customer',
    customers.market_segment AS c_mktsegment
      WITH SYNONYMS = ('segment', 'industry')
      COMMENT = 'Market segment the customer belongs to',
    orders.order_date AS o_orderdate
      COMMENT = 'Date the order was placed',
    orders.order_year AS YEAR(o_orderdate)
      COMMENT = 'Year the order was placed'
  )

  METRICS (
    orders.order_count AS COUNT(o_orderkey)
      COMMENT = 'Number of orders',
    orders.total_order_value AS SUM(o_totalprice)
      COMMENT = 'Total value of orders',
    orders.average_order_value AS AVG(o_totalprice)
      COMMENT = 'Average value of an order'
  )

  COMMENT = 'Customers and orders from the TPC-H sample data';
```

Confirm the view returns data before you attach it to an agent:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
    sales_insights
    DIMENSIONS customers.market_segment
    METRICS orders.average_order_value
  )
  ORDER BY market_segment;
```

You should get one row per market segment. If this query fails, fix the semantic view first: the
agent can’t answer data questions until the query succeeds.

The comments and synonyms aren’t decoration. Cortex Analyst uses them to map your wording onto
columns, so better descriptions produce better answers. For guidance, see
[Best practices for semantic views](/user-guide/views-semantic/best-practices).

## Step 5: Attach Cortex Analyst to the agent

Add a Cortex Analyst tool that points at your semantic view. The new specification replaces the
existing one, so include everything you want the agent to keep:

Copy code

```
ALTER AGENT agent_quickstart.demo.sales_agent
  MODIFY LIVE VERSION SET SPECIFICATION =
  $$
  models:
    orchestration: auto

  instructions:
    response: "Answer concisely. Format currency values with a dollar sign."
    orchestration: "Use the Sales_Analyst tool for any question about customers, orders, or revenue."
    sample_questions:
      - question: "What is the average order value by market segment?"

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "Sales_Analyst"
        description: "Generates SQL over customers and orders using the sales_insights semantic view."

  tool_resources:
    Sales_Analyst:
      semantic_view: "agent_quickstart.demo.sales_insights"
      execution_environment:
        type: "warehouse"
        warehouse: "<default_warehouse>"
  $$;
```

The key under `tool_resources` must match the tool’s `name` exactly. Here both are `Sales_Analyst`.
For other ways to add tools, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Step 6: Ask a question about your data

Return to the agent playground and ask a question about your data: “What is the average order value by
market segment?” The agent should call Cortex Analyst, generate SQL, and return one row per market
segment. Review the SQL it ran.

Try a follow-up question, such as “Which segment placed the most orders in 1995?”, to see the agent
plan a new query rather than reuse the previous answer.

If the agent replies that it can’t find the data, or answers from general knowledge instead of
querying your data, look for one of these causes:

| Symptom | Likely cause |
| --- | --- |
| Agent answers without running SQL | The Cortex Analyst tool isn’t attached, or `tool_resources` doesn’t match the tool name |
| Tool call fails with a privilege error | Your **default role** is missing privileges, or the user has no default warehouse |
| Query timeouts | The warehouse in `execution_environment` is suspended or too small |

Expand

Show lessSee more

## Clean up

Remove the objects you created. This statement needs `ACCOUNTADMIN` because that role created the
database in step 1. If you don’t have `ACCOUNTADMIN`, send the following statement to the same
administrator who ran the grants.

Warning

Dropping a database drops everything in it. Only run the following statement if you created
`agent_quickstart` in step 1, and change the name if you used a different one.

Copy code

```
USE ROLE ACCOUNTADMIN;
DROP DATABASE agent_quickstart;
```

Dropping the database removes the agent and the semantic view. The sample data is shared with your
account and isn’t affected.

## What’s next

Now that you have a working agent, extend it:

- Call the agent from your own application with the `agent:run` endpoint. See
  [Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run).
- Add more tools, including Cortex Search for unstructured data, custom tools, and web search. See
  [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).
- Keep conversation context across turns. See [Use threads with the Cortex Agent REST API](/user-guide/snowflake-cortex/cortex-agents-threads).
- Set up roles and authentication for real users. See [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).
- Watch how the agent behaves in production and collect feedback. See
  [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor) and
  [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations).

## Tutorials

For longer, application-oriented builds and best practices, use the following tutorials:

- [Getting Started with Cortex Agents](https://www.snowflake.com/en/developers/guides/getting-started-with-cortex-agents/)
- [Getting Started with Snowflake Cortex Agents API and React](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake_agents_api_and_react/index.html?index=../..index#0)
- [Getting Started with Cortex Agents and Slack](https://quickstarts.snowflake.com/guide/integrate_snowflake_cortex_agents_with_slack/index.html#0)
- [Getting Started with Cortex Agents for Microsoft Teams and Microsoft 365 Copilot](https://quickstarts.snowflake.com/guide/getting_started_with_the_microsoft_teams_and_365_copilot_cortex_app)
- [Best Practices to Building Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-to-building-cortex-agents/)
- [Best Practices for Evaluating Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-for-evaluating-cortex-agents/)
