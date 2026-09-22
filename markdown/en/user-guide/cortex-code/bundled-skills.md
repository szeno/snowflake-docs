# CoCo CLI bundled skills

CoCo CLI includes a set of built-in skills that cover common Snowflake workflows. You don’t need to install or configure anything to use them; they’re available in every session.

To invoke a skill, describe what you want to do and CoCo automatically loads the appropriate skill. You can also invoke a skill by name using the `/skill` command.

## Getting started

### `cortex-code-guide`

Complete reference guide for CoCo CLI: all commands, sessions, MCP integration, keyboard shortcuts, and configuration options.

Ways to use it:

- Learn all available slash commands, keyboard shortcuts, and operational modes
- Configure MCP servers, manage Snowflake connections, and set up integrations
- Understand how to resume sessions, manage context, and use file references with @

## Development and applications

### `developing-with-streamlit`

Create, edit, debug, and style Streamlit in Snowflake apps: including custom CSS theming, custom components, and packaged component development.

Ways to use it:

- Build a data exploration app with interactive filters, Snowpark queries, and Altair charts
- Apply Snowflake brand CSS theming and custom colors to beautify an existing app
- Create a packaged custom component with HTML/JS for reuse across multiple Streamlit apps

### `snowflake-notebooks`

Create and edit Workspace notebooks (.ipynb files) in Snowflake: Snowpark Python cells, SQL cells, data analysis, and debugging.

Ways to use it:

- Create a new notebook for exploratory data analysis combining SQL and Snowpark Python cells
- Upload and deploy an existing Jupyter notebook to the Snowflake Workspace
- Debug a failing notebook cell and fix Snowpark session initialization issues

### `snowflake-apps`

Scaffold, build, test, and deploy [Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime) apps: Next.js projects with Snowflake data access, local testing, and `snow app deploy`. This skill is bundled with [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) and CoCo Desktop.

Ways to use it:

- **CoCo CLI:** invoke with `$snowflake-apps` followed by a description of the app you want to build
- **CoCo Desktop:** type `/` in chat and select **snowflake-apps** (see [Skills in CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/skills#label-cortex-code-desktop-skills) for other ways to invoke skills)
- Build a warehouse monitor or internal operations dashboard backed by live Snowflake tables
- Iterate locally, then deploy to a running Application Service with a Snowflake-authenticated URL

## Compute or warehouse

### `warehouse`

Information, recommendations, and analysis for Gen1, Gen2, or [Adaptive warehouses](/user-guide/warehouses-adaptive): compare compute options, get sizing and conversion guidance, review warehouse properties, and check availability and eligibility for your region and account.

Ways to use it:

- Compare Gen1, Gen2, and Adaptive warehouses to understand the right compute option for your workload
- Modify warehouse properties such as size, type, and scaling settings
- Get recommendations for optimal Adaptive warehouse settings based on your workload

### `snowflake-interactive`

Create and manage [Interactive Warehouses](/user-guide/interactive) for low-latency, high-concurrency workloads: sub-second dashboards, API backends, and agentic queries.
Interactive warehouses work on any table type: standard, Iceberg, dynamic, hybrid, and interactive tables.

Ways to use it:

- Get started with interactive analytics and choose the right path: zero-copy queries on existing tables or purpose-built interactive tables
- Create static or dynamic interactive tables with optimal clustering keys and TARGET\_LAG settings
- Create and configure interactive warehouses, associate tables, and set up a fallback warehouse for mixed workloads
- Diagnose interactive query timeouts, cache warming issues, and fallback warehouse behavior

### `workload-performance-analysis`

Analyze SQL query performance via ACCOUNT\_USAGE: spilling, partition pruning, cache hit rates, clustering key recommendations, SOS and QAS eligibility.

Ways to use it:

- Identify queries with excessive disk spilling and get concrete fix recommendations
- Analyze partition pruning ratios and suggest better clustering keys for large tables
- Find queries eligible for Search Optimization Service or Query Acceleration Service

For Snowsight entry points, example prompts, and prerequisites, see
[Analyze Workload Performance with CoCo](/user-guide/analyze-workload-performance-coco).

### `deploy-to-spcs`

Deploy containerized applications to Snowpark Container Services (SPCS): push images to Snowflake registry, create services, configure networking and access.

Ways to use it:

- Package and deploy a Python ML inference service as an SPCS service endpoint
- Push a Docker image to the Snowflake container registry and launch a running service
- Grant role-based access to an SPCS service endpoint for secure consumer access

## Data engineering and pipelines

### `openflow`

Openflow (NiFi-based) data integration: deploy and configure connectors, diagnose flow failures, and build custom ingestion pipelines into Snowflake.

Ways to use it:

- Deploy a Google Drive to Snowflake CDC connector using Openflow connector templates
- Diagnose a failing NiFi flow by inspecting processor state, logs, and back-pressure
- Build a custom REST API-to-Snowflake ingestion flow with configurable parameters

### `openflow-observability`

Diagnose and troubleshoot Snowflake Openflow connector, runtime, and deployment issues by analyzing the event table to find the root cause, then get guided remediation you can apply in your Openflow UI, runtime, or Snowflake account.

Ways to use it:

- Diagnose an unhealthy connector or a stuck runtime by scanning event-table logs and error patterns for the root cause
- Investigate CDC replication failures such as FAILED tables or WAL/binlog lag and get step-by-step recovery guidance
- Troubleshoot network and external access integration errors, or runtime out-of-memory and crash issues, that surface as connector failures

### `dynamic-tables`

Work with Snowflake Dynamic Tables: create incremental pipelines, optimize target lag, monitor refresh health, and troubleshoot failures.

Ways to use it:

- Convert a scheduled Task pipeline to a Dynamic Table DAG for simpler, declarative maintenance
- Debug a Dynamic Table stuck in UPSTREAM\_FAILED state and restore it to healthy
- Set optimal target lag and clustering keys for a high-frequency downstream reporting table

### `dbt-projects-on-snowflake`

Manage dbt projects deployed as native Snowflake objects via the `snow dbt` CLI: not standard dbt workflows. Covers deploy, execute, schedule, and document.

Ways to use it:

- Deploy a dbt project as a Snowflake object and schedule it with a Snowflake Task
- Execute a deployed dbt project and inspect run status via EXECUTE DBT PROJECT
- Generate documentation and lineage for a deployed dbt project from within Snowflake

### `dcm`

Database Change Management: create, audit, and debug DCM projects for infrastructure-as-code database schema and role management.

Ways to use it:

- Initialize a new DCM project with DEFINE TABLE, DEFINE SCHEMA, and three-tier role patterns
- Deploy schema changes across dev, staging, and production environments via manifest
- Audit an existing DCM project for drift, misconfigurations, or missing role grants

### `iceberg`

Manage Apache Iceberg tables in Snowflake: catalog integrations (Glue, Unity Catalog, Polaris), external volumes, auto-refresh, and write support.

Ways to use it:

- Create a catalog integration with AWS Glue IRC and query external Iceberg tables from Snowflake
- Set up an S3 external volume and create Iceberg tables with ALLOW\_WRITES enabled
- Diagnose and fix auto-refresh failures or stale data on Iceberg tables

### `delta-sharing`

Consume Delta Shares in Horizon Catalog: create Delta Sharing catalog integrations (bearer token, OIDC, or OAuth), bring shared Delta tables into a read-only catalog-linked database, and verify and troubleshoot the connection.

Ways to use it:

- Create a Delta Sharing catalog integration from a recipient credential file and connect to a remote Delta Sharing server
- Bring shared Delta tables into a read-only catalog-linked database and query them as Iceberg tables in Snowflake
- Verify a catalog integration and diagnose connection, authentication, or vended-credential errors

### `snowflake-postgres`

Manage Snowflake Postgres instances: create, suspend, resume, reset credentials, configure network policies, and perform health checks.

Ways to use it:

- Create a new Snowflake Postgres instance and retrieve connection credentials
- Diagnose connectivity issues with an existing instance using health check diagnostics
- Reset credentials and update the network policy allowlist for a Postgres instance

### `snowflake-tasks`

Snowflake Tasks: create scheduled and triggered tasks, build task graphs (DAGs), manage task lifecycle (suspend, resume, modify), monitor execution history, and troubleshoot failures including auto-suspended tasks and owner-role privilege issues.

Ways to use it:

- Create a CRON or interval task that aggregates data on a schedule, or a triggered task that runs only when new data arrives
- Build a multi-step pipeline as a task graph with parent-child dependencies, fan-out and fan-in patterns, and finalizer tasks
- Diagnose issues with tasks: for example, diagnose an auto-suspended task, or a task that runs interactively but fails when run by the scheduler, by inspecting `TASK_HISTORY` and owner-role privileges

### `integrations`

Create and manage all Snowflake integration types: API, catalog, external access, notification, security, and storage integrations.

Ways to use it:

- Create an external access integration to allow UDFs to call external REST APIs
- Set up a notification integration to send pipeline alerts via email or Slack
- Configure a storage integration with S3, Azure Blob, or GCS for external stage access

### `manage-zerocopy-sapbdc`

Manage the zero-copy connector for bidirectional, no-copy data sharing between SAP® Business Data Cloud (BDC) and Snowflake: SAP data products become queryable in Snowflake as catalog-linked databases, and Snowflake databases can be published back to SAP BDC as data products. The skill provides five workflows from a single menu: create a connector, consume, publish, analyze, and troubleshoot.

Ways to use it:

- Create a new zero-copy connector and enroll it with SAP BDC
- Consume SAP BDC data products by mounting them as catalog-linked databases
- Publish a Snowflake database back to SAP BDC as a data product
- Explore, query, and join data from mounted SAP data products
- Troubleshoot and fix connector, catalog-linked database (CLD), and publishing issues

For more information, see [About Snowflake and SAP® Zero-Copy Integration](/user-guide/data-integration/zero-copy/about-sap-snowflake).

## Analytics and dashboards

### `dashboard`

Create and modify interactive Snowflake dashboards with charts, KPI widgets, tables, and markdown: including adding, editing, and fixing widgets.

Ways to use it:

- Build a sales performance dashboard combining multiple charts and KPI summary cards
- Create an executive summary view merging data from multiple Snowflake tables
- Add a new chart widget to an existing dashboard without disturbing other tiles

### `search-optimization`

Create and configure Cortex Search Services: build search pipelines from documents on a stage, process them into searchable tables, and deploy Cortex Search.

Ways to use it:

- Build a document Q&A search service over PDFs and text files stored on a Snowflake stage
- Ingest Google Docs, DOCX, audio, or video files into a searchable Cortex Search Service
- Update an existing Cortex Search Service with new documents without rebuilding from scratch

### `ai-readiness-score`

Score your Snowflake account’s AI readiness: consumption-ready (CR) table coverage, semantic view coverage and quality, demand coverage, and composite AI readiness: with a self-contained HTML report and gap-specific improvement recommendations.

Ways to use it:

- Measure how much of your query traffic lands on well-modeled, consumption-ready tables and get a ranked list of schemas to prioritize
- Check semantic view coverage across your CR tables and identify the highest-read tables that are missing semantic views
- Score existing semantic views on a 9-point quality scale and get actionable recommendations for missing signals (primary keys, metrics, verified queries, and so on)
- Invoke with `/ai-readiness-score` in CoCo CLI or in the CoCo UI in Snowsight; in Snowsight, you must have a Workspace open

## Snowpark development

### `snowpark-python`

Deploy Snowpark Python workloads to Snowflake: UDFs, UDAFs, UDTFs, and stored procedures using the `snow snowpark` CLI.

Ways to use it:

- Deploy a Python UDF for custom text processing callable directly from Snowflake SQL
- Create and register a Python stored procedure for complex multi-step ETL logic
- Build and deploy a UDTF (table function) for row-by-row data transformation at scale

### `snowpark-connect`

Migrate and validate PySpark workloads to run natively on Snowflake using Snowpark Connect: compatibility analysis and output validation.

Ways to use it:

- Assess a PySpark codebase for Snowpark Connect compatibility and migration effort
- Migrate a PySpark ETL pipeline to run natively on Snowflake compute
- Validate that migrated Spark workloads produce identical outputs to the original PySpark jobs

## AI and machine learning

### `agent-studio`

Create, manage, edit, debug, delete, and chat with Cortex Agents (including multi-tool agents combining Cortex Search and Analyst); create and manage semantic views for Cortex Analyst with VQR suggestions, verified queries, metrics, dimensions, and filters; test, evaluate, and publish agents; generate datasets; and audit quality.

Ways to use it:

- Create a natural language Q&A agent grounded in your Snowflake data warehouse using semantic views
- Build semantic views for Cortex Analyst with verified query representations, metrics, and dimensions
- Test agents by sending questions and debugging tool configuration issues
- Generate evaluation datasets from production queries and measure agent accuracy
- Import Tableau workbooks to automatically create semantic views
- Audit agent configurations and semantic view quality scores
- Deploy multi-tool agents combining Cortex Search, Analyst, and custom tools
- Connect agents to Snowflake Intelligence (CoWork) for end-user access

### `document-intelligence`

Use Snowflake Cortex AI functions for text and document processing: classification, entity extraction, sentiment analysis, translation, embedding, OCR, and document parsing.

Ways to use it:

- Extract structured fields from unstructured invoice PDFs stored on a Snowflake stage
- Classify and sentiment-score customer support tickets at scale using AI\_CLASSIFY and AI\_SENTIMENT
- Translate multilingual product reviews and summarize them at scale

### `ai-functions-pipeline-builder`

Turn a plain-language request into a Snowflake-native pipeline across structured and unstructured data: documents and files on a stage plus your warehouse tables. It builds an incremental pipeline on dynamic tables with Cortex AI functions, keeping outputs fresh as new files land.

Ways to use it:

- **Enterprise Search**: turn a mixed document library into AI-ready, governed knowledge for grounded search and RAG
- **Structured Extraction**: automate business documents into a clean, queryable dataset, with human review where confidence is low, then trends and recommended actions
- **Research & Analytics**: turn an unfamiliar document collection into corpus-level themes, trends, outliers, and cited cross-document answers
- **Customer 360**: unify warehouse tables and customer documents into one record per account, with risk scoring, triage lanes, and executive rollups
- **Custom pipeline**: when no template fits, compose block lanes from a shared palette or define new blocks, so the builder generalizes beyond the templates

### `cortex-ai-function-studio`

Build, evaluate, and optimize custom AI functions powered by Snowflake Cortex AI Complete, and recommend the right built-in AI function for your task, with SQL drafted from live docs and validated before you run it.

Ways to use it:

- Create a custom AI function that classifies support tickets, extracts structured fields, or applies domain-specific scoring logic using AI\_COMPLETE
- Evaluate a custom AI function against labeled test data and compare models side-by-side to find the best cost-quality tradeoff
- Optimize a custom AI function automatically: tuning the prompt, SQL pre/post-processing, and model selection to improve accuracy and reduce cost
- Get guided to the right built-in AI function for your task (AI\_CLASSIFY, AI\_EXTRACT, AI\_SENTIMENT, AI\_TRANSLATE, and more), with SQL drafted from live docs and validated before you run it

### `machine-learning`

End-to-end ML workflows: model training, Model Registry, feature engineering, time-series forecasting, anomaly detection, and GPU-accelerated jobs.

Ways to use it:

- Train a churn prediction model with Snowpark ML and register it in the Snowflake Model Registry
- Run a GPU-enabled deep learning training job on Snowflake compute via ML Jobs
- Deploy a registered model for batch inference directly within Snowflake SQL

## Data quality and observability

### `data-quality`

Monitor data quality using Data Metric Functions (DMFs): table comparisons, dataset popularity tracking, SLA alerting, and quality dashboards.

Ways to use it:

- Set up freshness and row count monitors on critical pipeline tables with SLA alerts
- Compare source and target tables after a migration to validate data integrity
- Detect sudden drops in row counts or spikes in null rates before they reach reports

### `lineage`

Analyze data lineage in Snowflake: downstream impact analysis, upstream source tracing, column-level lineage, and root cause debugging.

Ways to use it:

- Trace which downstream tables and dashboards break if a source table schema changes
- Find the upstream origin of a specific column in a complex reporting table
- Investigate unexpected metric values by tracing the full lineage back to the source

### `error-tables-ops`

Assess, enable, monitor, and manage Error Tables (DML error logging) across your account: which tables have errors, storage usage, and cleanup.

Ways to use it:

- Identify which tables should have error logging enabled and set it up in bulk
- Analyze DML errors such as NOT NULL violations, string truncation, and constraint failures
- Monitor error table storage and retention, and clean up old error records

### `alert`

Manage Snowflake alerts end to end: create, alter, suspend, resume, and troubleshoot alerts when conditions misfire, actions fail, or notifications are not delivered.

Ways to use it:

- Create a new alert to monitor pipeline health and trigger an action when thresholds are breached
- Set up all recommended alert templates for a product (for example, Openflow) to manage alerts in bulk
- Modify, suspend, or resume an existing alert as operational requirements change
- Diagnose why an alert is firing unexpectedly, failing with `ACTION_FAILED`, or not sending notifications

For more information, see [Alerts](/user-guide/alerts).

### `notification`

Work with Snowflake notifications across integration setup, content formatting, and delivery for email and webhook endpoints such as Slack, Teams, and PagerDuty.

Ways to use it:

- Create or manage notification integrations for email and webhook destinations
- Format alert output or query results into message payloads suitable for each destination
- Send notifications through `SYSTEM$SEND_SNOWFLAKE_NOTIFICATION` and validate delivery behavior

For more information, see [About notifications](/user-guide/notifications/about-notifications).

### `event-table`

Manage event tables and telemetry configuration: view current setup, modify log or trace levels, and query telemetry records to investigate product behavior and failures.

Ways to use it:

- Check which event table and telemetry levels are currently configured in your account
- Configure or update event table associations and logging, tracing, or metrics levels
- Query event table data to investigate telemetry for dynamic tables, tasks, Snowpark, or Openflow workloads

For more information, see [Logging, tracing, and metrics overview](/developer-guide/logging-tracing/logging-tracing-overview).

## Trusted data assets

These skills form a certification loop around the built-in system tag `SNOWFLAKE.CORE.CERTIFICATION_STATUS = 'CERTIFIED'`: find candidates, apply certification, and consume certified data.

### `recommend-object`

Scores and ranks candidate Snowflake objects on trust signals to identify the most authoritative source for a given question.

Ways to use it:

- Rank candidate tables for a business question (for example, which ARR table to trust) and surface the top certification-ready object
- Score objects against freshness, service-role ownership, semantic view backing, and downstream dashboard usage
- Hand off the top candidate to `certify-object` after reviewing scores

### `certify-object`

Applies `SNOWFLAKE.CORE.CERTIFICATION_STATUS = 'CERTIFIED'` to a confirmed table or view, with permission checks and immediate verification.

Ways to use it:

- Certify a specific table or view as the authoritative source after confirming the fully qualified name
- Verify the tag was applied with `SYSTEM$GET_TAG` immediately after certification
- Surface the exact grant SQL when `APPLY TAG` on `SNOWFLAKE.CORE.CERTIFICATION_STATUS` is missing

### `certified-data-product-discovery`

Answers a data question using only certified (or best available) Snowflake objects: searches via Snowscope, classifies results, and executes SQL.

Ways to use it:

- Answer a business question from certified data only and run SQL against accessible certified objects
- List certified tables for a topic before writing SQL, and warn when a selected object is uncertified
- Route Discover-Not-Access (DNA) objects through the request-access workflow instead of ad-hoc grants

## Data governance and security

### `access-troubleshooter`

Debug Snowflake access control errors: analyze the privileges a statement requires, find roles that are authorized to run it, create least-privilege roles, and grant missing privileges to resolve authorization failures.

Ways to use it:

- Troubleshoot an “Insufficient privileges” or “access denied” error and get a breakdown of exactly which privileges are missing
- Analyze the privileges a DDL or DML statement requires, and check whether a specific role is authorized to run it
- Get least-privilege role recommendations that unblock a user or team while preserving access boundaries

### `data-governance`

Implement data governance: dynamic masking, row access policies, automated PII classification, GDPR/CCPA compliance tagging, and access auditing.

Ways to use it:

- Auto-classify PII columns across an entire schema using SYSTEM$CLASSIFY
- Apply dynamic masking policies so non-privileged roles see only redacted values
- Audit who accessed sensitive tables in the last 30 days using ACCESS\_HISTORY

### `network-security`

Recommend, evaluate, and migrate Snowflake network policies: including SaaS-managed rules, hybrid policies, and access history-based recommendations.

Ways to use it:

- Generate network policy recommendations based on 90 days of account access history
- Evaluate a candidate policy before deployment to avoid accidentally locking out users
- Migrate existing custom network policies to use Snowflake-managed SaaS IP rules

### `trust-center`

Use Snowflake Trust Center: review security findings, manage scanners, check CIS benchmarks, enable Threat Intelligence, and track remediations.

Ways to use it:

- Run a full security scan and review critical findings against CIS benchmark controls
- Enable Threat Intelligence scanner to detect compromised credentials or anomalous logins
- Remediate a high-severity finding, document the resolution, and track it to closure

### `key-and-secret-management`

Manage Tri-Secret Secure, customer-managed keys (CMK/BYOK), key rotation schedules, and periodic data rekeying for compliance.

Ways to use it:

- Activate a customer-managed encryption key (CMK) to enable Tri-Secret Secure
- Rotate an existing CMK and audit the full key change history for compliance records
- Enable periodic data rekeying to meet regulatory encryption refresh requirements

### `manage-authentication-policy`

Manage Snowflake authentication policies: the account-level and user-level controls that govern how users authenticate and which clients and methods they’re allowed to use.

Ways to use it:

- Create, alter, view, attach, detach, or drop an authentication policy
- Restrict authentication methods or client types: for example, enforce MFA, configure PAT expiry, require a minimum driver version, or limit workload identity federation
- Get a recommended starting-point set of policies, tailored to your account’s recent login history

## Data sharing and marketplace

### `sharing`

Router for Snowflake sharing and collaboration: compare Secure Data Sharing, Declarative Sharing, Native Apps, and Data Clean Rooms, then hand off to the matching skill, or generate RBAC grants for same-account access.

Ways to use it:

- Decide between Secure Data Sharing, Declarative Sharing, Native Apps, and Data Clean Rooms when the right construct isn’t obvious from the request
- Compare the four sharing constructs side by side: zero-copy live access, packaged data products, consumer-side apps, and multi-party clean rooms
- Generate RBAC grants for same-account access between roles without a share or listing

### `data-sharing`

Snowflake Secure Data Sharing and listings: create data products and listings from Snowflake tables and views or from external storage in S3, Azure, or GCS (including open table formats), target the right consumer, and mitigate any issues.

Ways to use it:

- Create a listing or data product from one or more Snowflake tables or views and target an external customer or another account in your organization
- Create a listing from external storage in S3, Azure, or GCS (including open table formats) by choosing an ingestion path before publishing
- Troubleshoot failed grants and listing access for shares and listings, including permission denied and missing-object errors

### `listing-observability`

Providers monitor, troubleshoot, analyze, audit, and attribute costs for listings they publish. Consumers check refresh history and assess data staleness for listings they consume.

Ways to use it:

- **Provider (monitor and troubleshoot):** Monitor replication and refresh health across target clouds; troubleshoot auto-fulfillment failures
- **Provider (analyze consumption):** Analyze which consumers query which objects, with column-level access statistics
- **Provider (audit listing status):** Audit listing state, target accounts, resharing, and refresh schedule
- **Consumer (check and assess freshness):** Check when a consumed listing last refreshed and assess whether shared data is stale

### `ai-data-share`

Make a listing or data share AI-ready by automatically creating a semantic view from shared tables and deploying a Cortex Agent connected to it.

Ways to use it:

- Create a semantic view and Cortex Agent for a Marketplace listing so consumers can query shared data conversationally
- Turn an existing data share into an AI-ready product with auto-generated semantic models and agent orchestration
- Resolve a listing or share, inspect its objects, and build a complete data agent end-to-end without manual SQL

### `attach-ai-products-to-share`

Attach AI products (semantic views, Cortex Agents, Cortex Search Services) to Snowflake shares with correct grant ordering and dependency resolution.

Ways to use it:

- Grant a semantic view and its underlying tables to a share in the correct order so consumers can use Cortex Analyst
- Attach a Cortex Agent and all of its tool dependencies (semantic views, search services) to an outbound share
- Add a Cortex Search Service (Cortex Knowledge Extension) to a share for consumer RAG workflows

### `data-cleanrooms`

Work with Snowflake Data Clean Rooms: set up collaborations, run audience overlap analysis, and activate matched segments without exposing raw PII.

Ways to use it:

- Set up a clean room with a partner to analyze overlapping customer segments securely
- Run audience overlap analysis to find shared customers without sharing raw data
- Activate and export a matched audience segment for a targeted marketing campaign

### `declarative-sharing`

Declaratively share data products across Snowflake accounts using application packages with versioning: for Internal Marketplace and cross-account distribution.

Ways to use it:

- Share a curated dataset with another Snowflake account via the Internal Marketplace
- Publish a versioned data product with controlled access tiers for different consumers
- Create an application package for cross-region data distribution with release channels

### `native-app-consumer`

Install and configure Snowflake Native Apps as a consumer: grant privileges, approve specifications, configure references, and manage installed apps.

Ways to use it:

- Install a partner Native App from the Snowflake Marketplace into your account
- Grant required database privileges and configure references for a newly installed app
- Approve an app specification and set up data access bindings for the application

### `native-app-provider`

Build Snowflake Native Apps: create packages, write manifest files, setup scripts, manage versioning, release channels, and publish to the Marketplace.

Ways to use it:

- Create an app package with a manifest.yml and setup.sql script from scratch
- Add a new app version, register a patch, and push it through a release channel
- Publish a Native App to the Snowflake Marketplace with a consumer-facing listing

### `marketplace-provider`

End-to-end guidance for Snowflake Marketplace providers: listing type guidance, create and manage listings, configure pricing plans and offers for paid listings, make listings Cortex AI Ready, troubleshooting, provider success, and more.

Ways to use it:

- Get started as a provider with privilege checks, profile creation, and a step-by-step guide to getting listed on the Marketplace
- Create and manage listings, configure pricing plans and offers, and submit for Snowflake review
- Troubleshoot provider issues, evaluate how to make your listing AI Ready, and query data sharing usage views with natural language

### `marketplace-search`

Search the Snowflake Marketplace or your Internal Marketplace for data products, apps, and other listings that match a data or product need, then surface the matching listings so you can inspect or install them.

Ways to use it:

- Discover products that may be helpful for the work you are currently doing
- Find products for a topic such as weather, demographics, or credit card transactions across the Snowflake Marketplace and your Internal Marketplace
- Discover a listing for working with a third-party data source such as Salesforce, HubSpot, or Stripe before building a custom integration

### `get-marketplace-listing-details`

Present detailed information about a single Snowflake Marketplace listing and explain why it’s useful given your existing Snowflake data.

Ways to use it:

- Get an overview of one listing by title or global name, including provider, coverage, refresh rate, certifications, and pricing
- Understand why a product may be helpful for the work you are currently doing
- Generate runnable SQL examples for a data listing, joined against tables you already have where possible

## Platform and cost management

### `cost-intelligence`

Analyze Snowflake costs end-to-end: credits, budgets, warehouse costs, serverless services, anomaly detection, and cost breakdowns by team or department.

Ways to use it:

- Identify the top 5 most expensive warehouses and right-size them for cost savings
- Set up budget alerts and detect unexpected cost spikes before they escalate
- Generate a chargeback report breaking down Cortex AI, storage, and compute costs by team

### `organization-management`

Manage a Snowflake organization: accounts, org users, org-wide spending analysis, security posture, MFA readiness, and ORGANIZATION\_USAGE views.

To invoke this skill, type `/organization-management` in Cortex Code, then describe what you want to analyze.

Ways to use it:

- Get a 30-day executive summary of all org accounts including costs, usage, and reliability
- Review the org-wide security posture: MFA adoption, login failures, and auth settings
- Analyze cross-account credit and storage spending trends for a quarterly business review

## Migration and assessment

### `snowconvert-assessment`

Analyze SQL Server (or other warehouse) to Snowflake migration projects using SnowConvert assessment reports: waves, exclusions, dynamic SQL.

Ways to use it:

- Parse a SnowConvert assessment report to identify high-risk objects and conversion blockers
- Plan deployment waves based on object complexity scores and inter-object dependencies
- Analyze dynamic SQL patterns that require manual conversion effort and estimate scope

## Skill development

### `skill-development`

Create, document, and audit skills for CoCo: define triggers, structure multi-step workflows, write sub-skills, and test behavior.

Ways to use it:

- Build a new custom skill from scratch with a SKILL.md, frontmatter, and sub-skill structure
- Audit an existing skill for missing trigger keywords, incomplete workflows, or gaps
- Capture a successful CoCo session workflow and convert it into a reusable team skill

## Airflow plugin skills

The Airflow plugin is a separate install that extends CoCo with skills for building, testing, and managing Apache Airflow pipelines on Astro. These skills are available only when the plugin is active. The plugin covers four domains:

### Environment setup

#### `setting-up-astro-project`

Initialize and configure Astro/Airflow projects: set up folder structure, install providers, configure connections, variables, and secrets.

Ways to use it:

- Create a new Astro project with the correct folder structure and required provider packages
- Configure Snowflake, S3, and dbt connections in a freshly initialized Airflow project
- Set up Airflow variables and secrets management for a production-ready pipeline project

#### `managing-astro-local-env`

Manage your local Airflow environment with Astro CLI: start, stop, restart services, view component logs, and troubleshoot broken containers.

Ways to use it:

- Start the local Airflow environment and verify all services (scheduler, webserver) are healthy
- View scheduler and triggerer logs to diagnose a broken local environment
- Reset a corrupted local Airflow environment by cleaning containers and volumes

#### `init`

Initialize schema discovery for your Airflow/Astro project: generates `.astro/warehouse.md` with full table metadata for accurate SQL authoring.

Ways to use it:

- Run schema discovery on a new project to enable table-aware, accurate SQL generation
- Refresh the warehouse metadata file after schema changes or new tables are added
- Set up initial project metadata so agents can write SQL without guessing column names

### DAG authoring and testing

#### `airflow`

Manage Apache Airflow deployments: list, test, run, and debug DAGs, view task-level logs, inspect connections and variables, and check system health.

Ways to use it:

- List all DAGs in your Airflow deployment and check their current status and last run
- Trigger a specific DAG run and monitor task-level execution logs in real time
- Diagnose a broken Airflow connection and validate environment variables are set correctly

#### `authoring-dags`

Write Airflow DAGs following best practices: design patterns, naming conventions, task structure, retry logic, and dependency management.

Ways to use it:

- Create a new daily ETL DAG with proper retry policies, SLA settings, and alerting hooks
- Refactor a monolithic DAG into smaller, testable task groups
- Implement sensor-based upstream dependencies between decoupled pipelines

#### `testing-dags`

Complex DAG testing workflows with iterative debugging and fixing cycles: for multi-step test-debug-fix loops.

Ways to use it:

- Test a DAG end-to-end and automatically fix any failures that occur
- Run a full pipeline test suite and diagnose root causes of failing tasks
- Validate a new DAG against production data before deploying it

#### `debugging-dags`

Comprehensive DAG failure diagnosis and root cause analysis: structured investigation and prevention recommendations.

Ways to use it:

- Diagnose and fix a complex pipeline failure with full root cause analysis
- Investigate why a DAG is intermittently failing and recommend prevention strategies
- Analyze task retry patterns and identify flaky operators

#### `migrating-airflow-2-to-3`

Guide for migrating Apache Airflow 2.x projects to Airflow 3.x: breaking changes, compatibility fixes, and modernization.

Ways to use it:

- Assess an Airflow 2.x project for breaking changes before upgrading to Airflow 3
- Fix deprecated API usages and update DAG code for Airflow 3 compatibility
- Modernize scheduling, triggers, and dataset dependencies for Airflow 3

### Data operations

#### `cosmos-dbt-core`

Turn a dbt Core project into an Airflow DAG or TaskGroup using Astronomer Cosmos.

Ways to use it:

- Convert a dbt Core project into an Airflow DAG using Cosmos with ExecutionMode.LOCAL
- Configure Cosmos to run dbt models as individual Airflow tasks with dependency mapping
- Set up a Cosmos-based pipeline that runs dbt tests after each model transformation

#### `cosmos-dbt-fusion`

Run a dbt Fusion project with Astronomer Cosmos: Cosmos 1.11+ for Fusion on Snowflake/Databricks with ExecutionMode.LOCAL.

Ways to use it:

- Configure Cosmos to use the dbt Fusion engine on a Snowflake warehouse
- Set up a dbt Fusion pipeline as an Airflow TaskGroup with Cosmos 1.11+
- Migrate from dbt Core to dbt Fusion within an existing Cosmos-based DAG

#### `checking-freshness`

Quick data freshness checks: verify when tables were last updated and whether data is stale before use.

Ways to use it:

- Check if a set of source tables are fresh before kicking off a downstream pipeline
- Verify data currency for a reporting table before an executive dashboard runs
- Detect stale data conditions in a pipeline and trigger a refresh alert

#### `analyzing-data`

Query data warehouses and answer business questions: SQL generation, metrics, trends, and data lookups.

Ways to use it:

- Answer “how many customers used feature X last month?” with generated SQL
- Produce a trend analysis of pipeline run times over the past 30 days
- Look up counts, metrics, or segment breakdowns from warehouse tables

#### `profiling-tables`

Deep-dive data profiling for a specific table: statistics, data quality indicators, and structural content analysis.

Ways to use it:

- Profile a new source table to understand its cardinality, nullability, and value distributions
- Check for data quality issues in a table before building transformations on top of it
- Generate a statistical summary of a fact table for documentation or stakeholder review

### Lineage and observability

#### `annotating-task-lineage`

Annotate Airflow tasks with data lineage using inlets and outlets for OpenLineage tracking.

Ways to use it:

- Add lineage metadata to a custom operator that reads from S3 and writes to Snowflake
- Specify input/output datasets for tasks to enable lineage visibility in Marquez or Atlan
- Instrument a DAG with inlets/outlets to enable column-level lineage extraction

#### `creating-openlineage-extractors`

Create custom OpenLineage extractors for Airflow operators that lack built-in extraction support.

Ways to use it:

- Write a custom extractor for a third-party operator to capture its input/output datasets
- Implement column-level lineage extraction for a complex SQL transformation operator
- Build an extractor for a custom internal operator to enable full lineage tracing

#### `tracing-upstream-lineage`

Trace upstream data lineage: find where data comes from, what sources feed a table, and understand data origins.

Ways to use it:

- Find all upstream sources that feed into a reporting table
- Trace which raw tables and transformations a specific column passed through
- Identify which external data sources flow into a high-priority metric

#### `tracing-downstream-lineage`

Trace downstream data lineage and impact analysis: find what depends on a table and assess the risk of changes.

Ways to use it:

- Find all downstream tables, dashboards, and pipelines that depend on a source table
- Assess the blast radius before renaming or dropping a column in a core table
- Generate a change impact report for a planned schema migration
