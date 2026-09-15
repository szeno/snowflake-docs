# Data governance skills for Cortex Code

Cortex Code includes built-in data governance skills designed to help you understand, protect, and monitor the data in your
Snowflake account. These skills work directly in your Snowflake environment — describe what you need in plain English, and
Cortex Code generates and executes the necessary queries, classifications, and analyses for you. You don’t need to know which skill to run;
Cortex Code automatically selects the skill that it needs to answer your question.

## Getting started

1. [Install Cortex Code CLI and connect to your account](/user-guide/cortex-code/cortex-code-cli).
2. Ensure that you [meet the access control requirements](#label-dg-skills-access-control-requirements).
3. Start asking questions from the command line. You can use any of the example prompts below directly in Cortex Code. Cortex Code selects
   the appropriate skill automatically based on your question — no special commands are needed.

## General data governance

Data governance skills can answer questions about access control, audit trails, permissions, role hierarchies, and compliance monitoring
across your Snowflake account. Cortex Code uses skills to run SQL queries against Snowflake’s ACCOUNT\_USAGE views using an embedded semantic
model with effective query patterns.

Cortex Code can help you do the following tasks:

- **Audit who accessed what data and when** — Understand user access patterns, track query history, and identify after-hours or unusual
  activity.
- **Analyze permissions and role hierarchies** — Review grants, role assignments, and privilege structures to ensure least-privilege access
  for users.
- **Monitor compliance posture** — Analyze masking policies, row access policies, aggregation policies, and tag usage across your account.
- **Investigate object dependencies** — Understand how databases, schemas, tables, and views relate to one another.
- **Track DDL changes** — See who created, altered, or dropped objects and when.

**Example prompts**

Copy code

```
"Who has accessed the SALES.NA.CUSTOMERS table in the last 30 days?"
"Show me all users with the ACCOUNTADMIN role"
"What tables were accessed outside of business hours last week?"
"List all grants to the ANALYST_ROLE"
"Which users have run DDL operations on the FINANCE database in the last 7 days?"
"Show me the role hierarchy for my account"
"What masking policies are applied across my account?"
"Which tables have no row access policies attached?"
"Show me all tag references in the ANALYTICS database"
```

## Sensitive data classification

The data governance skill for sensitive data classification can detect and classify personally identifiable information (PII) and other
sensitive data in your Snowflake tables. It uses Snowflake’s native [SYSTEM$CLASSIFY](/sql-reference/stored-procedures/system_classify)
function to scan tables and identify columns containing data like emails, phone numbers, social security numbers, and addresses. It can
also set up automated classification profiles for continuous monitoring.

Cortex Code can help you do the following tasks:

- **Discover PII in your tables** — Scan individual tables or entire schemas to find columns containing sensitive data such as emails, names,
  phone numbers, credit card numbers, and social security numbers.
- **Analyze existing classification results** — Query the [DATA\_CLASSIFICATION\_LATEST](/sql-reference/account-usage/data_classification_latest)
  view to see what PII has already been detected, which tables have the most sensitive columns, and what categories of sensitive data exist.
- **Set up automated classification** — Create classification profiles that continuously monitor databases for new sensitive data and, if
  desired, auto-tag columns.
- **Create custom classifiers** — Define regex-based classifiers for domain-specific sensitive data (employee IDs, internal codes, custom
  formats) that Snowflake’s built-in categories don’t cover.
- **Test and validate classification accuracy** — Run classifiers against representative tables to verify detection accuracy before deploying
  them to production.

**Example prompts**

Copy code

```
"Scan SALES.NA.ORDERS for PII"
"Does the CUSTOMERS table contain any sensitive data?"
"What PII exists across my ANALYTICS database?"
"Show me all columns classified as EMAIL or PHONE in my account"
"Which tables have the most sensitive columns?"
"Create a classification profile for the PROD_DB database"
"Set up auto-classification with auto-tagging enabled"
"Create a custom classifier for employee IDs that match the pattern EMP-XXXXX"
"Show me classification results for the NA.FINANCE schema"
"Which tables need re-classification (older than 90 days)?"
```

## Data protection policies

The data governance skill for data protection policies helps you create, audit, and manage Snowflake masking policies, row access policies,
and projection policies. It provides best practices, proven patterns (like Attribute-Based Access Control), and guided workflows for both
building new policies and auditing existing ones. It also includes compliance reference material for PCI-DSS, HIPAA, GDPR, CCPA, SOX, and
FERPA.

Cortex Code can help you do the following tasks:

- **Create masking policies** — Build column-level masking policies that dynamically redact sensitive data based on the querying user’s role,
  using best practices like `IS_ROLE_IN_SESSION()` and memoizable functions.
- **Create row access policies** — Restrict which rows a user can see based on role membership, attributes, or lookup tables.
- **Create projection policies** — Control whether a column can appear in query results at all.
- **Audit existing policies** — Inventory all policies in your account, evaluate them against a checklist of security best practices, and
  identify anti-patterns (for example, using the CURRENT\_ROLE function instead of IS\_ROLE\_IN\_SESSION).
- **Consolidate scattered policies** — Migrate from table-specific policies to generic, reusable policies centralized in a governance
  database.
- **Meet regulatory requirements** — Get policy templates and guidance tailored to specific compliance frameworks (HIPAA for healthcare,
  PCI-DSS for payment data, GDPR for EU personal data).

**Example prompts**

Copy code

```
"Create a masking policy for the EMAIL column in the SALES.NA.CUSTOMERS table"
"Help me set up row access policies for the FINANCE schema"
"Audit all masking policies in my account"
"Are there any anti-patterns in my existing data policies?"
"Create a HIPAA-compliant masking policy for PHI columns"
"Show me the best practice for role-based masking"
"I need a projection policy to prevent the SSN column from appearing in query results"
"Help me consolidate my scattered masking policies into reusable ones"
"What's the recommended pattern for Attribute-Based Access Control (ABAC)?"
"Generate a policy health report for my account"
```

## Data quality

The data governance skill for data quality monitors and analyzes data quality across your Snowflake schemas using Data Metric Functions
(DMFs). It provides health scoring, root cause analysis for failing metrics, regression detection, trend analysis, SLA alerting, table
comparison for migration validation, and dataset popularity analysis.

Cortex Code can help you do the following tasks:

- **Check schema health** — Get an overall data quality score for a schema, showing how many metrics are passing versus failing, and which tables
  are monitored.
- **Investigate quality failures** — Drill into failing metrics to understand which tables and columns have issues, what the issues are, and
  get fix recommendations.
- **Detect quality regressions** — Compare current quality against previous measurements to see if quality improved or degraded, and identify
  new failures.
- **Track quality trends** — View time-series quality scores to understand whether quality is improving, stable, or declining over time.
- **Set up SLA alerts** — Create automated Snowflake ALERT objects that notify you when data quality drops below a threshold.
- **Compare tables** — Validate data migrations, reconcile dev versus prod data, or find row-level differences between two table versions
  (added, removed, modified rows, schema diffs).
- **Analyze dataset popularity** — Identify the most and least used tables, find unused or stale data, and understand who is consuming which
  datasets.

**Example prompts**

Copy code

```
"What is the data quality score for ANALYTICS.REPORTING?"
"Why is the SALES.CUSTOMERS.ORDERS table failing quality checks?"
"Has data quality improved or gotten worse in the DB.FINANCE schema this month?"
"Show me quality trends for PROD_DB.SALES over the last 30 days"
"Set up an alert if data quality in ANALYTICS.CORE drops below 90%"
"Compare STAGING.ORDERS_V1 with STAGING.ORDERS_V2"
"Find the differences between dev and prod versions of the SALES.ORDERS.CUSTOMERS table"
"Which tables in my account are the most popular?"
"Are there any unused tables in the SANDBOX database?"
"Show me the root cause of quality failures in SALES.ORDERS"
```

## Lineage

The data governance skill for lineage traces data dependencies across your Snowflake account — both upstream (where data comes from) and
downstream (what depends on it). It supports table-level and column-level lineage, impact analysis with risk scoring, root cause analysis
with change detection, and data discovery with trust scoring.

Cortex Code can help you do the following tasks:

- **Assess the impact of changes** — Before modifying a table, see all downstream objects that depend on it, ranked by risk (CRITICAL,
  MODERATE, LOW), with usage frequency and affected user counts.
- **Debug data issues by tracing upstream** — When a report shows wrong numbers, trace the data back through its transformation layers to
  identify where the issue originated, including recent schema and data changes.
- **Discover and verify trusted datasets** — Find the best table to use for a given analysis, with trust scores based on schema tier
  (production, staging, raw, sandbox), usage patterns, and data freshness.
- **Trace column-level dependencies** — Understand which downstream columns consume a specific column, or trace a column back to its original
  source through transformation layers.
- **Detect recent changes in the lineage** — Identify schema changes, data modifications, and DDL operations across the lineage path to
  correlate with data quality issues.

**Example prompts**

Copy code

```
"What will break if I change RAW_DB.SALES.ORDERS?"
"What depends on the SALES.SCH1.CUSTOMERS table?"
"Where does ANALYTICS_DB.REPORTING.REVENUE come from?"
"Why is the REVENUE_SUMMARY table showing wrong numbers?"
"Which table should I use for customer revenue analysis?"
"Is STAGING_DB.TRANSFORM.ORDERS_ENRICHED trustworthy?"
"What uses the AMOUNT column in SALES.ORDERS?"
"Where does the TOTAL_SALES column in the REVENUE report come from?"
"Show me the full lineage for SUMMIT.DEMO.SHIPMENTS"
"Has the DISCOUNT_PCT column in ORDERS changed recently?"
```

## Access control requirements

To successfully invoke the data governance skills from Cortex Code, you must have the following:

- [Privileges and roles required by Cortex Code](/user-guide/cortex-code/cortex-code-cli#label-cortex-code-cli-prerequisites).
- Access to the schemas, tables, and views that you’re interested in.

  - For sensitive data classification questions, you need the OWNERSHIP or USAGE privilege on the table or view.
  - For data protection policies, you need the CREATE MASKING POLICY or CREATE ROW ACCESS POLICY privilege on the schema that contains the
    table.
- Access to views in the ACCOUNT\_USAGE schema. By default, only the ACCOUNTADMIN system role has privileges to access the views in the ACCOUNT\_USAGE schema. To
  grant the ability to access these views to other people, you can do either of the following:

  - Grant the IMPORTED PRIVILEGES privilege on the SNOWFLAKE database to the user’s role. This is a broad grant of privileges that allows a
    user to view all ACCOUNT\_USAGE views, but also grants access to views in the ORGANIZATION\_USAGE schema.
  - Grant database roles needed to access views. To use Cortex Code for all governance-related topics, a user needs all of these database roles:
    OBJECT\_VIEWER, USAGE\_VIEWER, GOVERNANCE\_VIEWER, and SECURITY\_VIEWER. To restrict a user from learning about certain aspects of data
    governance, grant a subset of these roles. For a list of the views that each role can access, see [ACCOUNT\_USAGE schema](/sql-reference/snowflake-db-roles#label-db-roles-account-usage).

## Tips for best results

- **Be specific with object names** — Use fully qualified names like `DATABASE.SCHEMA.TABLE` for the most accurate results.
- **Start broad, then drill in** — Begin with a health check or overview, then ask follow-up questions to investigate specific issues.
