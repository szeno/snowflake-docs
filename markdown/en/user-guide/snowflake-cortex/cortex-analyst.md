# Cortex Analyst

Transition to Cortex Agents

Snowflake recommends transitioning to [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents), which supports every Cortex Analyst capability with higher answer quality.

## Overview

Cortex Analyst is a fully managed, LLM-powered [Snowflake Cortex](https://www.snowflake.com/en/data-cloud/cortex/)
feature that helps you create applications capable of reliably answering business questions based on your structured
data in Snowflake. With Cortex Analyst, business users can ask questions in natural language and receive direct
answers without writing SQL. Available as a convenient REST API, Cortex Analyst can be seamlessly integrated into any
application.

Building a production-grade conversational self-service analytics solution requires a service that generates accurate
text-to-SQL responses. For most teams, developing such a service that successfully balances accuracy, latency, and costs
is a daunting task. Cortex Analyst simplifies this process by providing a fully managed, sophisticated
agentic AI system that handles all of these complexities, generating highly accurate text-to-SQL responses. It helps you
accelerate the delivery of high-precision, self-serve conversational analytics to business teams, while avoiding time
sinks such as complex RAG solution patterns, model experimentation, and GPU capacity planning. The generated SQL queries
are executed against the scalable Snowflake engine, ensuring industry-leading price performance and lower total cost of
ownership (TCO).

Tip

Want to get started with Cortex Analyst quickly? Try the [Tutorial: Answer questions about time-series revenue data with Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst/tutorials/tutorial-1) tutorial.

### Key features

- *Self-serve analytics via natural language queries.* Delight your business teams and non-technical users with instant
  answers and insights from their structured data in Snowflake. Using Cortex Analyst, you can build downstream chat
  applications that allow your users to ask questions using natural language and receive accurate answers on the fly.
- *Convenient REST API for integration into existing business workflows.* Cortex Analyst takes an API-first approach,
  giving you full control over the end user experience. Easily integrate Cortex Analyst into existing business tools
  and platforms, bringing the power of data insights to where business users already operate, such as Streamlit apps,
  Slack, Teams, custom chat interfaces, and more.
- *Powered by state-of-the-art large language models:* By default, Cortex Analyst is powered by industry-leading models
  which run securely inside [Snowflake Cortex](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability), Snowflake’s
  intelligent, fully managed AI service. At runtime, Cortex Analyst selects the best combination of models to ensure the
  highest accuracy and performance for each query. As LLMs evolve, Snowflake may add more models to the mix
  to further improve performance and accuracy.
- *Semantic models for high precision and accuracy:* Generic AI solutions often struggle with text-to-SQL conversions
  when given only a database schema, as schemas lack critical knowledge like business process definitions and metrics
  handling. Cortex Analyst overcomes this limitation by using a [semantic model](/user-guide/views-semantic/sql) to
  bridge the gap between business users and databases. Captured in a lightweight YAML file, the overall structure and
  concepts of the semantic model are similar to those of database schemas, but allow for a richer description of the
  semantic information around the data.

  If you set up Cortex Analyst to answer questions from a large number of data sources, Cortex Analyst can
  automatically figure out which one to use. You don’t have to worry about specifying the right one with each query.
- *Security and governance.* Snowflake’s privacy-first foundation and enterprise-grade security ensure that you can
  explore AI-driven use cases with confidence, knowing your data is protected by the highest standards of privacy and
  governance.

  - Cortex Analyst does not train on Customer Data. We do not use your Customer Data to train or fine-tune any Model to
    be made available for use across our customer base. Additionally, for inference, Cortex Analyst uses the metadata
    provided in the semantic model YAML file (for example, table names, column names, value type, descriptions, and so on) only for
    SQL-query generation. This SQL query is then executed in your Snowflake virtual warehouse to generate the final
    output.
  - Data stays within Snowflake’s governance boundary. By default, Cortex Analyst is powered by Snowflake-hosted LLMs
    from Mistral and Meta, ensuring that no data, including metadata or prompts, leaves Snowflake’s governance boundary.
  - Seamless integration with Snowflake’s Privacy and Governance features. Cortex Analyst fully integrates with
    Snowflake’s role-based access control (RBAC) policies, ensuring that SQL queries generated and executed adhere to
    all established access controls. This guarantees robust security and governance for your data.

## Understanding Semantic Views

Cortex Analyst uses [Semantic Views](/user-guide/views-semantic/overview) to understand your data and generate
accurate SQL queries. Semantic Views are schema-level objects that define business concepts, metrics, and relationships
in a way that bridges the gap between how business users think about data and how it’s stored in database tables.

### What are Semantic Views?

Semantic Views provide a business-friendly layer over your data by defining:

- **Logical tables** that represent business entities (such as customers, orders, or products)
- **Dimensions** that provide categorical context (such as customer name, product category, or order date)
- **Facts** that capture row-level quantitative data (such as sale amounts or quantities)
- **Metrics** that aggregate data into business KPIs (such as total revenue or average order value)
- **Relationships** that define how tables join together

### Why use Semantic Views with Cortex Analyst?

Semantic Views significantly improve the accuracy and reliability of Cortex Analyst by:

- **Providing rich metadata**: Descriptions, synonyms, and data types help the LLM understand your data
- **Defining business logic**: Metrics capture the correct aggregation formulas and calculation rules
- **Establishing relationships**: Join paths are predefined, ensuring correct multi-table queries
- **Offering verified examples**: Sample questions and their SQL answers guide query generation

### Benefits of Semantic Views

Semantic Views are the recommended approach for working with Cortex Analyst because they offer:

- **Native Snowflake integration**: Full RBAC, privilege management, and governance features
- **Sharing capabilities**: Easily share semantic views through Snowflake’s sharing mechanisms
- **Advanced features**: Support for derived metrics that combine data from multiple tables
- **Access modifiers**: Mark facts and metrics as public or private to control visibility
- **Custom instructions**: Provide guidance to Cortex Analyst for SQL generation and question categorization

### Legacy semantic model support

Note

Legacy semantic model YAML files (stored on stages) are still supported for backward compatibility, but Semantic Views
are the recommended approach for new implementations.

For more information about Semantic Views and their YAML specification, see:

- [Overview of semantic views](/user-guide/views-semantic/overview)
- [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec)
- [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql)

## Access control requirements

To make requests to Cortex Analyst, use a role with either the SNOWFLAKE.CORTEX\_USER or SNOWFLAKE.CORTEX\_ANALYST\_USER database role.
CORTEX\_USER provides access to all Covered AI features, while CORTEX\_ANALYST\_USER provides access only to Cortex Analyst.
For information about Covered AI features, see [Legal notices](#label-analyst-legal-notices).

To use Cortex Analyst with a semantic model, you also need the following privileges:

| Privilege | Object |
| --- | --- |
| READ or WRITE | Stage that contains the semantic model YAML file, if the semantic model is uploaded to a stage. |
| USAGE | The Cortex Search services mentioned in the semantic model. |
| SELECT | The tables mentioned in the semantic model. |

Expand

Show lessSee more

Requests to the Cortex Analyst API must include an authorization token. For details on how to authenticate to the API,
see [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

Note that the example in this topic uses a session token to authenticate to a Snowflake account.

### Limiting access to specific roles

By default, the CORTEX\_USER role is granted to the PUBLIC role. The PUBLIC role is automatically granted to all users and roles.
If you don’t want all users to have this privilege, you can revoke access to the PUBLIC role and grant access to specific roles.
For more information, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

To control access to specific semantic models, you can store the YAML file in a stage and control access to that stage.

### Limiting access using the Cortex Analyst user role

To provide selective access to Cortex Analyst for specific users, use the SNOWFLAKE.CORTEX\_ANALYST\_USER database role.
This role includes the privileges needed to call the Cortex Analyst API. For more information about Covered AI features, see [Legal notices](#label-analyst-legal-notices).

Important

If your user roles have the CORTEX\_USER role, you must revoke access to the CORTEX\_USER role.
To revoke the CORTEX\_USER database role from your user roles, run the following command using the
ACCOUNTADMIN role:

Copy code

```
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER FROM ROLE analyst;
```

To provide access to Cortex Analyst, use the ACCOUNTADMIN role to do the following:

1. Grant the SNOWFLAKE.CORTEX\_ANALYST\_USER database role to a custom role.
2. Assign this custom role to users.

Note

You can’t grant database roles directly to users. For more information, see [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

The following example:

1. Creates the custom role, `cortex_analyst_user_role`.
2. Grants it the CORTEX\_ANALYST\_USER database role.
3. Assigns this role to `example_user`.

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE cortex_analyst_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_ANALYST_USER TO ROLE cortex_analyst_user_role;

GRANT ROLE cortex_analyst_user_role TO USER example_user;
```

You can also grant access to Cortex Analyst through existing roles. For example, if you have an `analyst` role
used by analysts in your organization, you can grant access with a single GRANT statement:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_ANALYST_USER TO ROLE analyst;
```

## Region availability

Cortex Analyst is natively available in the following regions.

- AWS ap-northeast-1 (Tokyo)
- AWS ap-southeast-2 (Sydney)
- AWS us-east-1 (Virginia)
- AWS US East (Commercial Gov - N. Virginia)
- AWS us-west-2 (Oregon)
- AWS eu-central-1 (Frankfurt)
- AWS eu-west-1 (Ireland)
- Azure East US 2 (Virginia)
- Azure West Europe (Netherlands)

If your Snowflake account is in a different cloud region, you can still use Cortex Analyst by leveraging
[Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference). Once cross-region inference is enabled, Cortex Analyst
processes requests in other regions for models that are not available in your default region. For optimal performance,
configure cross-region with AWS US regions.

## Multi-turn conversation in Cortex Analyst

Cortex Analyst supports multi-turn conversations for data-related questions. This feature enables asking follow-up
questions that build on previous queries, creating a more dynamic and interactive data exploration experience.
For example, the user asks, “What is the month-over-month revenue growth for 2021 in Asia?”, then follows up with,
“What about North America?”

Cortex Analyst recognizes the follow-up, retrieves the context from the initial query, and rephrases the second question as:
“What is the month-over-month revenue growth for 2021 in North America?” Cortex Analyst then generates a SQL
query to answer this question.

To use this feature, pass the conversation history in the `messages` field:

Copy code

```
{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is the month over month revenue growth for 2021 in Asia?"
                }
            ]
        },
        {
            "role": "analyst",
            "content": [
                {
                    "type": "text",
                    "text": "We interpreted your question as ..."
                },
                {
                    "type": "sql",
                    "statement": "SELECT * FROM table"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What about North America?"
                }
            ]
        },
    ],
    "semantic_model_file": "@my_stage/my_semantic_model.yaml"
}
```

The conversation history is an array of messages in chronological order, where each message has a role and content. The
role can be `"user"` (for previous questions) or `"analyst"` (for previous responses). Analyst responses have both text and
SQL responses, as shown in the example above, while user messages have only text.

Important

Large language models like the ones used by Cortex Analyst do not store state between requests. The full history is
processed for each new query in a conversation, with corresponding compute cost that increases with each round.

### Known limitations in multi-turn conversations

Some of the following limitations might be addressed in future versions of Cortex Analyst.

Access to the results of previous SQL queries
:   Cortex Analyst doesn’t have access to results from previous SQL queries. For example, if you first ask,
    “What are my products?” and then ask, “What is the revenue of the second product?”, Cortex Analyst cannot refer to
    the list of products from the first query to get the second product.

General business insights
:   Cortex Analyst is limited to answering questions that can be resolved with SQL. It does not generate insights
    for broader business-related queries, such as “What trends do you observe?”

Long conversations
:   If a conversation includes too many turns or the user shifts intent frequently, Cortex Analyst might struggle to interpret
    the follow-up questions. In such cases, reset the conversation and start again.

## Evaluate and improve your semantic view

You can evaluate the quality of your semantic view by running your verified queries against Cortex Analyst and
measuring how accurately it generates SQL. Use evaluation results to identify areas for improvement, track regressions
over time, and iteratively refine your semantic view. For more information, see
[Cortex Analyst evaluations](/user-guide/snowflake-cortex/cortex-analyst-evaluations).

## Getting started

Developers can use the following resources to get started with Cortex Analyst:

1. Basic code example: The [Cortex Analyst example](#label-analyst-access-example) in the following section provides a simple, easy-to-read script that helps
   you create an interactive app using Cortex Analyst.

   Choose this option if you want a basic fundamental example to start with, and are comfortable with using Streamlit and making your own
   modifications. You can run this example either in Streamlit in Snowflake (SiS) or locally.
2. Snowflake Samples repository: If you’re instead looking for a more comprehensive implementation, the Cortex Analyst advanced SiS demo
   in the Snowflake Samples repository has all the features and options already set up. This repository is configured with various pre-built
   features that make deploying Cortex Analyst seamless and robust.

   Choose this option if you are trying to test out the feature for the first time, or have fewer custom modifications to make.

   Note

   This is shown only as an example. Snowflake does not provide support for the below content,
   nor does Snowflake warrant that the below content is accurate.

   To learn more, see the [Cortex Analyst advanced SiS demo](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/cortex-analyst/Advanced%20SiS%20Demo) in the Snowflake Samples GitHub
   repository.

## Cortex Analyst example

Follow these steps to create an interactive Streamlit in Snowflake (SiS) or standalone Streamlit app that uses Cortex Analyst.

1. [Create a semantic model](#label-copilot-create-semantic-model)
2. [Upload the semantic model to stage](#label-copilot-upload-semantic-model)
3. Create and run a [Streamlit in Snowflake app](#label-copilot-create-streamlit-app)
4. [Interact with the Streamlit in Snowflake app](#label-copilot-interact-with-copilot)

### Create a semantic model

A [semantic model](/user-guide/views-semantic/sql) is a lightweight mechanism that addresses issues related to the language difference between
business users and database definitions by allowing for the specification of additional semantic details
about a dataset. These additional semantic details, like more descriptive names or synonyms, enable Cortex Analyst to answer data questions
much more reliably.

1. Start with a list of questions you would like Cortex Analyst to answer. Based on that, decide on the dataset for your semantic model.
2. Create your semantic view using the [Semantic View Autopilot](/user-guide/views-semantic/autopilot) or review the [YAML specification](/user-guide/views-semantic/sql#label-semantic-views-create-from-yaml) to create one manually.

### Upload semantic model

You can upload a semantic model YAML file to a [stage](/sql-reference/sql/create-stage) or pass the semantic model YAML
as a string in the request body. If you upload a semantic model YAML to a stage, access to that semantic model is controlled by
access to the stage it’s uploaded to. This means that any role with access to the stage can access the semantic models on that
stage even if the role doesn’t have access to the tables that the models are based on. Ensure that roles granted access to a stage
have SELECT access on all tables referenced in all semantic models on that stage.

Below is an example of how to set up the stages containing the semantic models. One stage (`public`) is accessible to all members of the
organization, whereas another stage (`sales`) is only accessible to the `sales_analyst` role.

Create the database and schema for the stage. The following example creates a database named `semantic_model` with a schema named
`definition` but you can use any valid identifier string for these names.

Copy code

```
CREATE DATABASE semantic_model;
CREATE SCHEMA semantic_model.definitions;
GRANT USAGE ON DATABASE semantic_model TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA semantic_model.definitions TO ROLE PUBLIC;

USE SCHEMA semantic_model.definitions;
```

Then create the stages for storing your semantic models:

Copy code

```
CREATE STAGE public DIRECTORY = (ENABLE = TRUE);
GRANT READ ON STAGE public TO ROLE PUBLIC;

CREATE STAGE sales DIRECTORY = (ENABLE = TRUE);
GRANT READ ON STAGE sales TO ROLE sales_analyst;
```

In Snowsight, you can refresh the page and find the newly created stages in the
[Horizon Catalog Explorer](/user-guide/ui-snowsight-data).
You can open the stage page in a new tab and upload your YAML files in Snowsight.

Alternatively, you can use the [Snowflake CLI client](/developer-guide/snowflake-cli/command-reference/stage-commands/copy)
to upload from your local file system.

Copy code

```
snow stage copy file:///path/to/local/file.yaml @sales
```

### Creating a Streamlit in Snowflake App

This example shows you how to create a Streamlit in Snowflake app that takes a natural language question as input and calls
Cortex Analyst to generate an answer based on the semantic model you provide.

Note

This is shown only as an example. Snowflake does not provide support for the below content,
nor does Snowflake warrant that the below content is accurate.

For more information on creating and running Streamlit apps in Snowflake, see [About Streamlit in Snowflake](/developer-guide/streamlit/about-streamlit).

1. Follow the directions in [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app#label-streamlit-create-app) to create a new
   Streamlit app in Snowsight.
2. Copy the [Streamlit code](https://github.com/Snowflake-Labs/sfguide-getting-started-with-cortex-analyst/blob/main/cortex_analyst_sis_demo_app.py) from our GitHub repo into the code editor.
3. Replace the placeholder values with your account details.
4. To preview the app, select **Run** to update the content in the Streamlit preview pane.

### Interact with the Streamlit App

1. Navigate to the Streamlit app in your browser or the Streamlit in Snowflake preview pane.
2. Start asking questions about your data in natural language (for example, “What questions can I ask?”).

### Create a standalone Streamlit app

You can also use the example code to build a standalone app.

Note

This is shown only as an example. Snowflake does not provide support for the below content,
nor does Snowflake warrant that the below content is accurate.

1. Install [Streamlit](https://pypi.org/project/streamlit/).
2. Create a Python file locally called `analyst_api.py`.
3. Copy the [Streamlit code](https://github.com/Snowflake-Labs/sfguide-getting-started-with-cortex-analyst/blob/main/cortex_analyst_streaming_demo.py) from our GitHub repo into the file.
4. Replace the placeholder values with your account details.
5. Run the Streamlit app using `streamlit run analyst_api.py`.

The database and schema specified in the code is the stage location for the semantic model YAML file. The role used
in the Snowflake connector should have access to underlying data defined in the semantic model.

For a more comprehensive implementation, see the [Cortex Analyst advanced SiS demo](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/cortex-analyst/Advanced%20SiS%20Demo) in the Snowflake Samples GitHub
repository. This repository is configured with various pre-built features that make deploying Cortex Analyst seamless and robust.

## Disable Cortex Analyst functionality

If you do not want Cortex Analyst to be available in your account, disable the feature by changing the
ENABLE\_CORTEX\_ANALYST parameter using the ACCOUNTADMIN role:

Copy code

```
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET ENABLE_CORTEX_ANALYST = FALSE;
```

| Parameter Type | Session |
| --- | --- |
| Data Type | BOOLEAN |
| Description | Controls whether Cortex Analyst functionality is enabled in your account. |
| Values | - FALSE: Cortex Analyst functionality is not available. - TRUE: Cortex Analyst functionality is available. |
| Default | TRUE |

Expand

Show lessSee more

## Control models used by Cortex Analyst

You can use model-level RBAC (role-based access control) to control access to the models used by Cortex Analyst. Each
model is protected by a designated application role, and administrators can grant or revoke access to specific LLMs via
these model-specific roles. For more information, see [Role-based access control (RBAC)](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-rbac).

Important

Model-level RBAC is an advanced feature intended for customers with specific regulatory or compliance requirements
that dictate which models can be used and where they can be hosted. If you do not have such requirements, Snowflake
recommends that you do not use this feature.

You cannot choose a model directly. Instead, Cortex Analyst assigns each request to a model, or to a combination of
models, taking into account the following factors:

- The models [available in your Snowflake region](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).
- The account’s [cross-region inference configuration](/user-guide/snowflake-cortex/cross-region-inference).
- Any model-level [RBAC restrictions](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-rbac) you have established.

Tip

Different models produce different results. For consistent results, use the same Snowflake region, cross-region
inference configuration, and model-level RBAC restrictions for all requests.

Cortex Analyst selects models in the following order of preference, using the highest-ranked model to which your role
has access. If your role has access to none of these models, the request fails.

1. Anthropic Claude Sonnet 4.6
2. Anthropic Claude Sonnet 4.5
3. OpenAI GPT 4.1
4. Arctic Text2SQL R1.5 (with thinking enabled)
5. Combination of Mistral Large 2 and Llama 3.1 70b

Cortex Analyst’s model selection behavior may change from time to time to take advantage of advances in model functionality.

### Risks and limitations

Cortex Analyst relies upon the availability of at least one supported model configuration. Disabling specific models
reduces fallback options and increases the risk of query failures.

Model-level restrictions apply to all Cortex features that can use the model; it is not possible to restrict access to a
model only in Cortex Analyst or in any other single Cortex feature.

## Cost considerations

The credit rate usage for Cortex Analyst is based on the number of messages processed as outlined in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf). Only successful responses (HTTP 200) are counted. The number of tokens in each message only affects cost when Cortex Analyst is invoked using Cortex Agents. Otherwise, the number of tokens in each message does not affect cost.

Note

The above charges cover AI costs for text-to-SQL. Additional warehouse costs apply when you execute the SQL generated by Cortex Analyst.

### Monitoring the cost of Cortex Analyst

To view credit consumption for Cortex Analyst, use the [CORTEX\_ANALYST\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_analyst_usage_history). For example:

Copy code

```
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_ANALYST_USAGE_HISTORY;
```

Usage of Cortex Analyst also appears in the [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) in the ACCOUNT\_USAGE schema with a service type of AI\_SERVICES.

## Legal notices

Where your configuration of Cortex Analyst uses a model provided on the
[Model and Service Flow-down Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Output (SQL query suggestion): Usage Data  Query result (using SQL query suggestion): Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
