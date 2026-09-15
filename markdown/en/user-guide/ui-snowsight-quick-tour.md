# Snowsight quick tour

In Snowsight, you can perform data analysis and engineering tasks, monitor query and data loading and transformation activity,
explore your Snowflake database objects, and administer your Snowflake database, including managing the cost and adding users and roles.

You can use Snowsight to perform the following tasks:

**Work with data**

- Build and develop in Workspaces and Notebooks with SQL, Python, and multi-file projects.
- Ingest and transform data using Snowpipe, connectors, tasks, and streams.
- Analyze with AI using Snowflake Cortex functions, agents, and ML models.
- Monitor activity including query history, task graphs, and data loading.
- Discover and share on the Snowflake Marketplace.

**Explore the Horizon Catalog**

- Discover data across your data estate with Universal Search and the catalog.
- Share data products securely with other Snowflake accounts through listings.
- Govern and protect data with masking policies, row access policies, and tags.

**Manage your account**

- Optimize compute resources including warehouses and compute pools.
- Administer users, roles, and access control.
- Monitor and control costs with budgets and cost management views.
- Manage Postgres instances within Snowflake.

For more information about these and other tasks that you can perform, see [Snowsight: The Snowflake web interface](/user-guide/ui-snowsight).

## Work with data

### Workspaces

Workspaces is the unified editor for creating, organizing, and managing code across multiple file types. Workspaces provides a file-based
development environment where you can write SQL and Python, organize projects with folders, and integrate with Git for version control.

For more information, see:

- [Workspaces](/user-guide/ui-snowsight/workspaces)
- [Integrate workspaces with a Git repository](/user-guide/ui-snowsight/workspaces-git)
- [Work with worksheets in Snowsight](/user-guide/ui-snowsight-worksheets)

### Notebooks in Workspaces

Notebooks in Workspaces provide an interactive, cell-based environment for Python, SQL, and Markdown. Use notebooks for exploratory data analysis,
machine learning model development, and data science workflows with embedded visualizations and Git integration.

For more information, see:

- [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)

### Streamlit

Build and deploy interactive data applications with Streamlit in Snowflake. Create custom dashboards, reports, and data apps
using Python without managing infrastructure.

For more information, see:

- [About Streamlit in Snowflake](/developer-guide/streamlit/about-streamlit)
- [Create your Streamlit app](/developer-guide/streamlit/app-development/creating-your-app)

### dbt projects

Develop and manage dbt projects with a web-based IDE that connects to Git repositories. Build, test, and run SQL-based data
transformation pipelines directly in Snowflake with version control integration.

For more information, see:

- [Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces)

### Ingestion

Load data into Snowflake using Snowpipe for continuous ingestion, connectors for various data sources, and file uploads through the UI.

For more information, see:

- [Load data using Snowsight](/user-guide/data-load-web-ui)
- [Snowpipe](/user-guide/data-load-snowpipe-intro)
- [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui)

### Transformation

Transform your data with dbt projects for analytics engineering, dynamic tables for continuously refreshed materialized views,
and tasks for scheduling transformation workflows.

For more information, see:

- [Dynamic tables](/user-guide/dynamic-tables/overview)
- [Introduction to tasks](/user-guide/tasks-intro)
- [View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks)

### AI & ML

Build AI-powered applications with AI Studio, interact with data conversationally using Snowflake CoWork, and leverage
Cortex AI functions for text analysis and LLM capabilities. Use Cortex Agents for natural language interactions, Cortex Analyst
for data analysis, Cortex Search for vector similarity search, and Cortex Code for AI-powered coding assistance. Manage machine
learning models, features, and experiments for production ML workflows.

For more information, see:

- [Overview of Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork)
- [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql)
- [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code)

### Monitoring

Monitor and track query performance, container services and jobs, task execution, data loading activity, and system health.
Review query history with Performance Explorer to analyze and optimize queries, view traces and logs for observability,
and debug failed operations.

For more information, see:

- [Monitor query activity with Query History](/user-guide/ui-snowsight-activity)
- [View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks)
- [Monitor data loading activity by using Copy History](/user-guide/data-load-monitor)

### Marketplace

Discover and share data products on the Snowflake Marketplace. As a provider, publish data products and application packages
on the Snowflake Marketplace to share with the broader Snowflake community. As a consumer, access datasets and application packages
from providers to derive real-time data insights without needing to set up a data pipeline or write any code.

For more information, see:

- [About Snowflake Marketplace](/collaboration/collaboration-marketplace-about)
- [Create and configure shares](/user-guide/data-sharing-provider)
- [About the Snowflake Native App Framework](/developer-guide/native-apps/native-apps-about)

## Explore the Horizon Catalog

### Catalog

Discover database objects across your entire data estate with Universal Search and the Horizon Catalog. Explore databases, tables,
functions, views, and more using the Database Explorer. Browse the Internal Marketplace to find data products shared within
your organization, and manage apps and native application packages.

To learn more, see:

- [Snowflake Horizon Catalog](/user-guide/snowflake-horizon)
- [Explore and manage database objects in Snowsight](/user-guide/ui-snowsight-data)
- [About organizational listings](/user-guide/collaboration/listings/organizational/org-listing-about)

### Data sharing

Collaborate with users in other Snowflake accounts by sharing data and application packages securely through Internal sharing
(within your organization) or External sharing (to other organizations). As a provider, create data product listings, manage
sharing agreements, and use auto-fulfillment to provide data across regions. As a consumer, access datasets and application
packages shared with your account.

For more information, see:

- [Create and configure shares](/user-guide/data-sharing-provider)
- [About organizational listings](/user-guide/collaboration/listings/organizational/org-listing-about)
- [Access Provider Studio](/collaboration/provider-studio-accessing)

### Governance & security

Apply data governance policies to protect sensitive information, manage user access control, and monitor security posture.
Use masking policies for column-level security, row access policies for row-level filtering, tags for data classification,
create and manage users and roles, and evaluate account security in the Trust Center.

For more information, see:

- [Data Governance in Snowflake](/guides-overview-govern)
- [Configuring access control](/user-guide/security-access-control-configure)
- [Trust Center](/user-guide/trust-center/overview)

## Manage your account

### Compute

Manage virtual warehouses for query execution and compute pools for container-based workloads. Optimize resource allocation,
monitor utilization, and configure auto-suspend and auto-resume settings.

For more information, see:

- [Working with warehouses](/user-guide/warehouses-tasks)
- [Overview of warehouses](/user-guide/warehouses-overview)

### Postgres

Create and manage Postgres instances within Snowflake. Deploy Postgres databases for compatibility with existing applications
while leveraging Snowflake’s infrastructure and management capabilities.

For more information, see:

- [Snowflake Postgres](/user-guide/snowflake-postgres/about)

### Admin

Manage cost and billing, configure account settings, set up integrations with external systems and services,
and connect with partner tools through the Snowflake Marketplace.

For more information, see:

- [Exploring overall cost](/user-guide/cost-exploring-overall)
- [Managing integrations in Snowsight](/user-guide/ui-snowsight-integrations)
- [Trial SaaS applications from listings](/collaboration/consumer-saas-trials)

## User menu

Access account information, switch roles and accounts, manage your user profile and settings, file support cases, and sign out from the user menu in the lower-left corner.

For more information, see:

- [Manage your user settings in Snowsight](/user-guide/ui-snowsight-profile)
- [Getting started with Snowsight](/user-guide/ui-snowsight-gs)
- [Overview of Access Control](/user-guide/security-access-control-overview)
