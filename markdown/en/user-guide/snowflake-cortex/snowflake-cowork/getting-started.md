# Getting started with Snowflake CoWork

This topic provides information about getting started with Snowflake CoWork with a simple example of creating an enterprise agent. This agent can be used with Snowflake CoWork to respond to questions by reasoning over both structured and unstructured data. For a more detailed guide, see [Getting Started with Snowflake CoWork](https://www.snowflake.com/en/developers/guides/getting-started-with-snowflake-intelligence/).

## Prerequisites

- [Git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- A Snowflake account
- Access to the ACCOUNTADMIN role

## Create a database, schema, and tables and load data from AWS S3

To create the building blocks for the enterprise agent, you must create a database, schema, tables, and load data from AWS S3.

1. Clone the [Getting Started with Snowflake CoWork GitHub repository](https://github.com/Snowflake-Labs/sfguide-getting-started-with-snowflake-intelligence/) to your local machine:

   Copy code

   ```
   git clone https://github.com/Snowflake-Labs/sfguide-getting-started-with-snowflake-intelligence.git
   ```
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. In the navigation menu, select **Projects** » **Workspaces**.
4. Select **+ Add new**.
5. Select **SQL File**.
6. Enter a name for the file.
7. Open the file.
8. Copy the contents of the [setup.sql](https://github.com/Snowflake-Labs/sfguide-getting-started-with-snowflake-intelligence/blob/main/setup.sql) file to the workspace.
9. Run all statements in order.
10. Run the following SQL statements in the workspace:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT;
GRANT USAGE ON SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT TO ROLE snowflake_intelligence_admin;
GRANT CREATE SEMANTIC VIEW ON SCHEMA DASH_DB_SI.RETAIL TO ROLE ACCOUNTADMIN;
```

11. Optionally, run the following SQL statement to enable cross-region inference:

Copy code

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

12. Switch the user role in Snowsight to SNOWFLAKE\_INTELLIGENCE\_ADMIN.

## Create tools for the agent to use

Create the tools that the agent will use.

**Create a semantic view for use with Cortex Analyst.**

1. In the navigation menu, select **AI & ML** » **Cortex Analyst**.
2. Select **Create new**, then select **Create new Semantic View**.
3. For the location to store the semantic view, select DASH\_DB\_SI.RETAIL.
4. For the name, enter `SALES_AND_MARKETING_DATA`.
5. For the description, enter `Semantic view for sales and marketing data analysis across campaigns, products, transactions, and social media engagement.`.
6. Select **Next**.
7. Select **Skip**.
8. Select the DASH\_DB\_SI.RETAIL schema.
9. For the tables, select the MARKETING\_CAMPAIGN\_METRICS, PRODUCTS, SALES, and SOCIAL\_MEDIA tables.
10. Select **Next**.
11. For the columns, select all available columns for the selected tables.
12. Select **Next**.
13. Review and accept all of the relationship and metric suggestions.
14. Select **Save**.
15. Wait for the semantic view to be created.

**Create a Cortex search tool by creating a search service.**

1. In the navigation menu, select **AI & ML** » **Cortex Search**.
2. Select **Create**.
3. For **Service database and schema**, select **DASH\_DB\_SI.RETAIL**.
4. For **Service name**, enter **Support\_Cases**, and then select **Next**.
5. In the list of data sources, select the SUPPORT\_CASES table, and then select **Next**.
6. In the list of search columns, select **TRANSCRIPT**, and then select **Next**.
7. For the attribute columns, select **TITLE** and **PRODUCT**, and then select **Next**.
8. For the columns to include, select **Select all**, and then select **Next**.
9. For the warehouse, select **DASH\_WH\_SI** (if that warehouse is not available, select **COMPUTE\_WH**), and then select **Create**.

## Create a Cortex Agent

To create the agent that will use the tools, follow these steps:

1. In the navigation menu, select **AI & ML** » **Agents**.
2. Select **Create agent**.
3. For the schema, use SNOWFLAKE\_INTELLIGENCE.AGENTS.
4. For the agent object name, use `Sales_AI`.
5. For the display name, use `Sales AI`.
6. Select **Create agent**.

## Add the tools to the agent

**Add the Cortex Analyst tool to the agent.**

1. From the agent page, select the **Tools** tab.
2. Navigate to the Cortex Analyst entry.
3. Select **+ Add**, then select **Semantic view**.
4. For the database and schema, select DASH\_DB\_SI.RETAIL.
5. For the semantic view, select `SALES_AND_MARKETING_DATA`.
6. For the name, use `SALES_AND_MARKETING_DATA`.
7. For the description, use the following:

   ```
   The Sales and Marketing Data semantic view in DASH_DB_SI.RETAIL schema provides a complete view of retail business performance by connecting marketing campaigns, product information, sales data, and social media engagement. The view enables tracking of marketing campaign effectiveness through clicks and impressions, while linking to actual sales performance across different regions. Social media engagement is monitored through influencer activities and mentions, with all data connected through product categories and IDs. The temporal alignment across tables allows for comprehensive analysis of marketing impact on sales performance and social media engagement over time.
   ```
8. For the warehouse, select **Custom**, then select DASH\_WH\_SI.
9. For the query timeout, use `60`.
10. Select **Add**.

**Add the Cortex Search tool to the agent.**

1. Navigate to the Cortex Search Services entry.
2. Select **+ Add**.
3. For the database and schema, select DASH\_DB\_SI.RETAIL.
4. For the search service, select `DASH_DB_SI.RETAIL.Support_Cases`.
5. For the ID column, use `ID`.
6. For the title column, use `TITLE`.
7. For the name, use `Support_Cases`.
8. Select **Add**.
9. Select the **Orchestration** tab.
10. Add the following orchestration instructions:

```
Whenever you can answer visually with a chart, always choose to generate a chart even if the user didn't specify to.
```

11. Select **Save**.

## Use Snowflake CoWork

Interact with the agent from Snowflake CoWork.

1. Navigate to Snowflake CoWork using one of the methods described in [Access the agent](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-intelligence-use-agent).
2. Select the newly created agent.
3. Enter the following prompts:
   - “What issues are reported with jackets recently in customer support tickets?”
   - “Show me the trend of sales by product category between June and August.”
   - “Why did sales of Fitness Wear grow so much in July?”
