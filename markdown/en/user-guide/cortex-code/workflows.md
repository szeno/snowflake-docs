# CoCo CLI workflow examples

This topic provides workflow examples for common tasks to help you get the most out of CoCo CLI. It covers
data discovery, synthetic data generation, building dashboards, and creating Cortex Agents.

## Use cases: Data discovery and querying

This section walks through creating a synthetic dataset and performing basic analysis to generate a dashboard.

### Connect to a Snowflake account

Copy code

```
cortex -c <your-demo-account>
```

Or connect interactively:

```
> connect to <my demo account>
```

### Discover and explore data

Search your data catalog, understand lineage, and find relevant tables:

```
> Find all tables related to customers that I have write access to
```

### Ensure you have the right role with the correct permissions

```
> What privileges does my role have on this database?
```

Diagnose access issues and understand role privileges:

```
> Why am I getting a permissions error?
```

### Generate synthetic data

Here are some examples of generating synthetic data for different use cases.

**Fraud analysis for a fintech company:**

```
> Generate realistic looking synthetic data into <database name>. Create a table of 10000
  financial transactions where ~0.5% of them are fraudulent. Include Amount, Location,
  Merchant, and Time. Make the fraudulent ones look suspicious based on location or amount.
```

**Pharma trial data:**

```
> Make a dummy dataset for a clinical trial of a new blood pressure medication. List 100
  patients, their age, their dosage group (Placebo vs. 10mg), and their blood pressure
  readings over 4 weeks.
```

**Customer churn data:**

```
> Create a customer churn dataset for a telecom company showing customer usage for 100000
  customers. Include basic demographic data such as fake names, phone numbers, US city and
  state. Also include data usage (GB), call minutes, contract length, and whether they
  cancelled their service (churn). Ensure there's a customer_id column that's unique.
  Create the data locally and then upload it to Snowflake.
```

### Perform basic queries against this data

```
> Calculate the Churn Rate grouped by state and contract length. Order the results by the
  highest churn rate first so I can see the most risky regions and contract types.
```

```
> I want to identify the heaviest data users who are also churning.
```

### Build interactive dashboards

Create and deploy Streamlit apps with charts, filters, and interactivity.

Tip

Open an example dashboard you like (or find one online) and copy it to your clipboard.
You can paste images directly into CoCo (Ctrl+V) as design references.

```
> Build an interactive Streamlit dashboard on this data with state filters and use the
  conversation so far for examples of the kinds of charts to show. Use the attached image
  as a template for visuals and branding.
```

Once you’ve verified that the dashboard is working and looks good, upload it to Snowflake:

```
> Ensure that the Streamlit app will work with Snowflake and upload it to Snowflake.
  Give me a link to access the dashboard when it's done.
```

Congratulations! You should now have a working Streamlit dashboard that displays the dataset you created.

## Use cases: Building Cortex Agents

This section walks through creating a Cortex Agent to answer questions about your data in Snowflake CoWork.
We’ll augment the existing synthetic data with customer call transcripts.

### Create a Semantic View for Cortex Analyst

Create a semantic view so you can use Cortex Analyst with your data. Use the defaults for all the questions it asks:

```
> Write a Semantic View named DEMO_TELECOM_CHURN_ANALYTICS for Cortex Analyst based on
  this data. Use the semantic-view optimization skill.
```

### Create a Cortex Search service

First, generate synthetic data containing customer service calls:

```
> Generate a new table called customer_call_logs. Generate 50 realistic customer service
  transcripts (2-3 sentences each) as PDF files. Some should be angry complaints about
  coverage, others should be questions about billing. Then use the AI_PARSE_DOCUMENT
  function to extract the text and layout information from the PDFs into the TRANSCRIPT_TEXT
  column. Split text into chunks for better search quality.
```

Then create a Cortex Search service that indexes the transcripts:

```
> Create a Cortex Search Service named CALL_LOGS_SEARCH that indexes these transcripts.
  It should index the TRANSCRIPT_TEXT column and filter by CUSTOMER_ID.
```

### Create a Cortex Agent

Build a Cortex Agent that uses both the Analyst and Search services:

```
> Build a Cortex Agent that has access to two tools:
  - cortex_analyst: For querying the TELECOM_CUSTOMERS SQL table.
  - cortex_search: For searching the CALL_LOGS_SEARCH service.

  Write a system prompt for this agent:
  - Persona: You are a Senior Retention Specialist.
  - Routing Logic: If the user asks for 'metrics', 'counts', or 'averages', use the
    Analyst tool. If the user asks for 'sentiment', 'reasons', or 'summaries of calls',
    use the Search tool.
  - Output Format: Always verify the customer ID before answering. If the risk score is
    high, end the response with a recommended retention offer (e.g., 'Offer 10% discount').
  - Constraint: Never reveal the raw CHURN_RISK_SCORE to the user; interpret it as 'Low',
    'Medium', or 'High'.
```

### Deploy to Snowflake CoWork

Deploy the agent to Snowflake CoWork:

```
> Let's deploy this agent to Snowflake CoWork.
```

Congratulations! You have successfully created and deployed a Snowflake CoWork agent.

You should now be able to access this agent in Snowflake CoWork and ask it questions like:

- “What are customers complaining about in their calls?”
- “Show me high-risk customers with monthly charges over $100”

## See also

[CoCo CLI](/user-guide/cortex-code/cortex-code-cli)
:   Get started with installation and first prompts

[Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills)
:   Specialized skills for semantic models, agents, and documents

[Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst)
:   Cortex Analyst documentation
