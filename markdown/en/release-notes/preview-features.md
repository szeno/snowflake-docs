# Preview features

Preview features have been implemented and tested in Snowflake; however, full usability and corner-case handling may not be complete yet.
We do not guarantee the use of these features against defects that may produce unexpected or undesired results. Additionally, we may change
the behavior of features while they are in preview. If we change the behavior of a preview feature, we do our best to notify users before
making the change, but we do not guarantee to always pre-announce changes.

In addition, preview features can be disabled, enabled, or viewed for an entire account.
See [Managing access to all preview features](#label-preview-feature-management), on this page, for details.

Attention

Preview features are provided primarily for evaluation and testing purposes. They should not be used in production systems or with
production data.

For more details about the usage of preview features, see the Snowflake
[Preview Terms of Service](https://www.snowflake.com/legal/preview-terms-of-service/).

## Preview availability

Availability is determined on a per-feature basis:

Open:
:   Most preview features are *Open*, meaning they are enabled by default for all accounts and, therefore, openly available for use.

On Request:
:   Some preview features are provided *On Request*, particularly in the early stages of the preview period. To request access to these
    features for your account, you must contact Snowflake.

Some preview features are available only in certain [Snowflake editions](/user-guide/intro-editions) or in specific
[cloud platforms](/user-guide/intro-cloud-platforms) or [regions](/user-guide/intro-regions).

## Features currently in preview

The following features are currently available for preview, listed roughly in the order in which they were introduced:

| Feature | Availability | Introduced | Additional reading | Notes |
| --- | --- | --- | --- | --- |
| [Cortex Agents Compact API](/user-guide/snowflake-cortex/cortex-agents-compact) | Open | September 2026 | [Cortex Agents Compact API](/user-guide/snowflake-cortex/cortex-agents-compact) | Summarize conversation history and use the compact representation in subsequent Cortex Agent requests to reduce token consumption and stay within the model context window. |
| Horizon Catalog Explorer UI | Open | September 2026 | [Explore and manage database objects in Snowsight](/user-guide/ui-snowsight-data) | Browse Snowflake objects in the Horizon Catalog Explorer, which replaces Database Explorer and adds a persistent navigation tree, breadcrumbs, and unified object detail pages. |
| Cortex AI Gateway | Open | September 2026 | [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway) | A governed entry point for AI traffic in your account. Send inference through one endpoint from coding agents, third-party clients, and SDKs, trace every request, and attribute spend to teams and users with budgets and per-user quotas. |
| Iceberg Scan Plan API in Snowflake Horizon Catalog | Open | September 2026 | [Enforce data protection policies on Apache Iceberg™ tables from external query engines](/user-guide/tables-iceberg-query-using-external-query-engine-snowflake-horizon-enforce-access-policies) | Enforce data protection policies on Apache Iceberg tables queried from external engines through Snowflake Horizon Catalog. |
| [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags) | Open | August 2026 | [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags) | Use predefined tags in the `SNOWFLAKE.TAGS` schema for cost center, certification status, sensitivity, environment, project, and pausing tag propagation. `SKIP_TAG_PROPAGATION` requires Enterprise Edition or higher. |
| [SAS Migration](/migrations/aim-for-datawarehouses/sas-migration) | Open | September 2026 | [Snowflake AIM Agent for Data Warehouses - SAS Migration](/migrations/aim-for-datawarehouses/sas-migration) | AI-assisted assessment and code conversion for migrating SAS workloads to Snowflake, available through the Snowflake AIM Agent for Data Warehouses. |
| [Second generation Openflow](/user-guide/data-integration/openflow/gen2/index) | Open | August 2026 | [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index) | Gen 2 Openflow connector configuration (the setup wizard, SQL/stage-based configuration, and standard RBAC on connector objects) is in Public Preview. Gen 2 deployment and runtime SQL objects are generally available on AWS, Azure, and GCP. Supported connectors at Public Preview: PostgreSQL CDC, MySQL/MariaDB CDC. Migration from gen 1 to gen 2 is separately available in Private Preview. |
| Stable egress IP addresses on Azure | Open | August 2026 | [Securing ingress of Snowflake requests with egress IP addresses](/user-guide/egress-ip/network-egress), [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) | Generate Snowflake egress IP address ranges to allowlist on external servers. This preview covers Azure deployments. The feature is generally available on AWS Commercial deployments. |
| Remote Development with the Snowflake Extension for Visual Studio Code | Open | August 2026 | [Remote Development with the Snowflake Extension for Visual Studio Code](/user-guide/vscode-ext-remote-development) | Connect to a Snowflake-backed remote development environment from Visual Studio Code or Cursor to run notebooks, SQL, scripts, terminals, Git, and Cortex Code on Snowflake-managed compute. |
| Request Access in Workspaces | Open | August 2026 | [Request Access in Workspaces](/user-guide/access-requests-workspaces) | Resolve access-related SQL errors in Workspaces by submitting access requests from Snowsight. ACCOUNTADMIN and SECURITYADMIN roles review requests on the Requests & Approvals page. Enable per account by setting `FEATURE_ENABLE_REQUEST_ACCESS_FOR_WORKSPACES = 'ENABLED'`. |
| [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) | Open | August 2026 | [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool) | Let an agent generate and run Python in a secure, isolated sandbox to process data, perform calculations, and produce visualizations. The sandbox doesn’t run SQL, is scoped to a single conversation thread, and isn’t available to agents invoked with owner’s rights. |
| Preset tables in clean room templates | Open | August 2026 | [Preset tables](/user-guide/cleanrooms/custom-templates#label-dcr-template-preset-tables) | Preset a specific dataset in a Collaboration Data Clean Rooms template with a `preset_tables` block, so the template always reads that dataset and the analysis runner doesn’t supply it at run time. |
| Remote app operations for Snowflake Native Apps | Open | August 2026 | [Use remote app operations](/developer-guide/native-apps/remote-app-operation) | Providers can perform on-demand operations on a consumer Snowflake Native App, such as running SQL statements, disabling the app, enabling the app, or retrying an upgrade. |
| Anomaly monitors for cost anomalies | Open | August 2026 | [Anomaly monitors](/user-guide/cost-anomalies#label-cost-anomaly-monitors) | Define a custom cost anomaly detection scope using object tags and account-level service types, so you can monitor a business unit, cost center, or project instead of a whole account. Manage monitors in Snowsight or with new ANOMALY\_INSIGHTS class methods. |
| DCM Projects extensions | Open | August 2026 | [Supported object types in DCM Projects](/user-guide/dcm-projects/dcm-projects-supported-entities), [Deploy and manage DCM Projects](/user-guide/dcm-projects/dcm-projects-use), [DCM Projects for data pipelines](/user-guide/dcm-projects/dcm-projects-pipelines) | - [`DEFINE PIPE`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-pipe): Declaratively manage pipes in DCM Projects definition files. - [`DEFINE SHARE`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-share): Declaratively manage share objects and their grants in DCM Projects definition files, controlling which objects are exposed to the share. - [`DEFINE STREAM`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-stream): Declaratively manage streams in DCM Projects definition files. - [`DEFINE MASKING POLICY`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-masking-policy): Declaratively manage masking policies in DCM Projects definition files. Attaching to tables or views isn’t yet supported. - [`DEFINE ROW ACCESS POLICY`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-row-access-policy): Declaratively manage row access policies in DCM Projects definition files. Attaching to tables or views isn’t yet supported. - [`DEFINE SEMANTIC VIEW`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-object-type-semantic-view): Declaratively manage semantic views in DCM Projects definition files. - [`ATTACH TAG`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-attach-tag): Declaratively assign Snowflake object tags to DCM Projects-managed entities; DCM Projects reconciles declared tag assignments on every deployment. - [Inherited grants](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-inherited-grants): Declaratively define a single `GRANT INHERITED` statement on a container (`ACCOUNT`, `DATABASE`, or `SCHEMA`) that automatically applies to every current and future object of a specified type within it. - [Container-level `MANAGE GRANTS`](/user-guide/dcm-projects/dcm-projects-supported-entities#label-dcm-projects-container-manage-grants): Delegate grant administration for a database or schema to a role that manages all grant types on objects inside that container. - [DCM Projects `TEST` and `PREVIEW` commands](/user-guide/dcm-projects/dcm-projects-pipelines): Test data quality expectations attached to managed objects, and return sample rows from tables, views, or dynamic tables defined in a DCM project before or after deployment. - [DCM Projects GitHub Actions](/user-guide/dcm-projects/dcm-projects-use#label-dcm-github-actions): Reusable composite GitHub Actions (`dcm-parse-manifest`, `dcm-connection-test`, `dcm-plan`, and `dcm-deploy`) that automate DCM Projects CI/CD pipelines. |
| Snowflake ODBC Driver 4.x, built on the Universal Core | Open | August 2026 | [Snowflake ODBC Driver built on the Universal Core](/developer-guide/odbc/odbc-universal-core) | A new major version of the ODBC driver, built on the Universal Core shared Rust library. Installing it replaces the 3.x driver on the same machine, so validate it on a dedicated host, VM, or container. Certificate revocation checking uses certificate revocation lists (CRLs) rather than the Online Certificate Status Protocol (OCSP), and is off by default. |
| Snowflake Connector for Python 5.x, built on the Universal Core | Open | August 2026 | [Snowflake Connector for Python built on the Universal Core](/developer-guide/python-connector/python-connector-universal-core) | A new major version of the Python connector, built on the Universal Core shared Rust library and published as a release candidate under the existing `snowflake-connector-python` package name. Because pre-release versions are not installed by default, `pip install --pre` is required. Certificate revocation checking uses CRLs rather than OCSP, and is off by default. |
| Access externally managed Apache Iceberg™ tables through Snowflake Horizon Catalog | Open | August 2026 | [Access externally managed Apache Iceberg™ tables in a catalog-linked database with an external engine through Snowflake Horizon Catalog](/user-guide/externally-managed-iceberg-tables-access-horizon-irc) | Use the Horizon Iceberg REST Catalog API to read and perform DML and DDL operations on externally managed Iceberg tables in a catalog-linked database from external engines such as Apache Spark™, Trino, DuckDB, or PyIceberg. |
| Open Data Sharing | Open | August 2026 | [Open Data Sharing](/user-guide/open-data-sharing) | Share live, read-only Iceberg table data with consumers outside of Snowflake using standard Iceberg REST Catalog APIs, without data movement or ETL pipelines. |
| Workday Live Data Query for Snowflake | On Request | August 2026 | [About Workday Live Data Query for Snowflake](/user-guide/data-integration/zero-copy/about-workday-ldq) | Query Workday business data in real time from a Snowflake Notebook through a Python connector, with no ETL or data replication. In preview for Snowflake and Early Adopter for Workday; contact your Workday account representative to request access. |
| Intent-Driven Governance | Open | August 2026 | [Intent-Driven Governance](/user-guide/intent-driven-governance) | Use Snowflake CoCo to assess governance controls, classify sensitive data, review proposed tags and protections, and approve generated SQL before changes are applied. |
| CoCo automations in CLI and Snowsight | Open | August 2026 | [CoCo automations in CLI and Snowsight (Preview)](/user-guide/cortex-code/cortex-code-automations) | Schedule recurring, unattended CoCo runs that execute in a Snowflake-managed sandbox and can be created, monitored, and managed from the CoCo CLI or CoCo in Snowsight. |
| User skills in Snowflake CoWork | Open | August 2026 | [User skills in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/user-skills) | Create reusable workflows conversationally, from the UI (+ menu > Skills > Create new), or by uploading a skill folder, then run them explicitly with / or from Skills menus, or implicitly when a conversation matches the skill. Chat creation and scripted skills require the Cortex Agent [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool). |
| Document generation in Snowflake CoWork | Open | August 2026 | [Document generation in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/document-generation) | Generate shareable files such as PDF documents and PowerPoint presentations from your analysis. Upload a PowerPoint template to match your organization’s style, or customize behavior with a user or agent skill. Requires the Cortex Agent [code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool). |
| Inline Stored Procedures for hybrid tables | Open | August 2026 | [Inline Stored Procedures for hybrid tables](/user-guide/hybrid-tables-inline-stored-procedures) | A new type of stored procedure for operational workloads on hybrid tables. The procedure body runs as a single atomic unit pushed to the query processing layer, reducing per-statement overhead for OLTP-style workloads. Set `ENABLE_USE_STABLE_PATH = TRUE` on the warehouse for the best performance. |
| AI Agents in the Trust Center AI Security tab | Open | August 2026 | [Using the Trust Center](/user-guide/trust-center/using-the-trust-center) | View a list of all Cortex Agents directly in the Trust Center AI Security tab, with filtering by category and per-agent details. Use it to inventory and investigate agents that fall outside your governance policy. |
| Organization Command Center Organization Features | Open | August 2026 | [Organization Command Center](/user-guide/organization-hub-command-center), [Organization Features](/user-guide/organization-hub-command-center-features) | From the organization account, see which organization-level capabilities are enabled in Command Center, starting with premium views. You can enable or disable premium views through Snowflake Support. |
| Organization Command Center 3rd party access configuration | Open | August 2026 | [Organization Command Center](/user-guide/organization-hub-command-center), [Command Center 3rd party access configuration](/user-guide/organization-hub-command-center-third-party) | From the organization account, classify member accounts as internal or external, set the default tenant type for new accounts, and maintain allowed email domains. Logins from domains that aren’t on the allowlist can raise Trust Center security violations. |
| FOCUS\_COST\_USAGE\_V1\_3 view | Open | July 2026 | [FOCUS\_COST\_USAGE\_V1\_3 view](/sql-reference/billing/focus_cost_usage_v1_3) | Query FOCUS v1.3-compliant cost and usage data from the `SNOWFLAKE.BILLING` schema for invoice reconciliation, cost allocation, and FinOps reporting. |
| Skill and plugin sharing in CoCo | Open | July 2026 | [Share skills and plugins](/user-guide/cortex-code/cortex-code-skill-plugin-sharing) | Share, discover, and govern CoCo skills and plugins across your Snowflake account. Publish them as Cortex Extension objects that teammates can find and install, with administrator certification, access control, and usage telemetry. |
| AI\_EXTRACT and AI\_PARSE\_DOCUMENT support for client-side encrypted stages and network-restricted accounts | Open | July 2026 | [AI\_EXTRACT](/sql-reference/functions/ai_extract), [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document) | Use AI\_EXTRACT and AI\_PARSE\_DOCUMENT with client-side encrypted stages and in accounts that use PrivateLink or other network policies that restrict public network access to stages. |
| SAML2 JIT user provisioning | Closed | July 2026 | [SAML2 JIT user provisioning](/LIMITEDACCESS/security/saml2-jit-user-provisioning) | Automatically create Snowflake user accounts when a user authenticates through a SAML2 security integration for the first time. |
| AI Gateway in budgets and per-user quotas | Open | August 2026 | [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources), [Per-user quotas](/user-guide/budgets/per-user-quotas) | Add an AI Gateway or the AI Gateway domain as a shared resource on a custom budget or per-user quota so you can track and control credit consumption by tagged users. |
| AI mode for sensitive data classification | Open | August 2026 | [AI mode](/user-guide/classify-intro#label-classify-ai-mode) | Use LLMs to identify additional semantic categories beyond standard classification when you enable AI mode on a classification profile in the Trust Center or with SQL. |
| Custom configurations for Trust Center scanners | Open | July 2026 | [Configure custom settings for a scanner](/user-guide/trust-center/using-the-trust-center#label-trust-center-configure-scanner-custom-config) | Tune scanner behavior by setting custom configurations that adjust thresholds, lookback windows, or other scanner logic (such as allowlists), reducing false positives while keeping scanners enabled. |
| Cortex Agent tool evaluation metrics (TSA and TEA) | Open | June 2026 | [Tool selection and execution metrics ground truth](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-cortex-agent-evaluation-tool-metrics) | Evaluate how your agent uses tools with the tool selection accuracy and tool execution accuracy metrics for Cortex Agent evaluations. |
| Open Semantic Interchange (OSI) YAML format for semantic views | Open | June 2026 | [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSI\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_osi_yaml) | Create and export semantic views using the open-standard OSI YAML format for interoperability with external AI and BI tools. |
| Operational query improvements for hybrid tables | Open | June 2026 | [Performance improvements for operational queries on hybrid tables](/user-guide/hybrid-tables-operational-query-performance) | Automatic performance improvements for operational queries on hybrid tables that do point operations or select or modify a small number of rows. Enable it by setting `ENABLE_USE_STABLE_PATH = TRUE` on a warehouse. |
| OIDC federated authentication | Open | July 2026 | [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc), [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc) | Configure OpenID Connect (OIDC) security integrations for federated SSO with Google or Microsoft as a managed provider, or any custom OIDC-compliant identity provider. |
| Optimized refresh for account replication | Open | June 2026 | [Optimized refresh for failover groups](/user-guide/account-replication-config#label-optimized-refresh) | A new refresh mode for failover groups that applies only metadata changes since the previous refresh, so refresh duration scales with the rate of change rather than the total number of objects in the failover group. Opt in per failover group with `OPTIMIZED_REFRESH = TRUE`. |
| Openflow Connector for MongoDB | Open | June 2026 | [About the Openflow Connector for MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/about) | The Openflow Connector for MongoDB enables CDC replication of MongoDB collections into Snowflake using change streams; supports initial snapshot load and incremental sync. |
| Openflow Connector for Shopify | Open | June 2026 | [About the Openflow Connector for Shopify](/user-guide/data-integration/openflow/connectors/shopify/about) | Replicates Shopify store data using the Admin GraphQL API; supports bulk load, incremental sync, and delete detection. |
| CREATE OR ALTER <OBJECT> | Open | June 2026 | - [CREATE OR ALTER PIPE](/sql-reference/sql/create-pipe#label-create-or-alter-pipe-syntax) - [CREATE OR ALTER STREAM](/sql-reference/sql/create-stream#label-create-or-alter-stream-syntax) | Additional commands that create an object if it doesn’t exist, or alter it according to the object definition. |
| Openflow Connector for Jira Cloud: Agile flow | Open | May 2026 | [Set up the Atlassian Jira Cloud (Agile) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile) | The Atlassian Jira Cloud (Agile) flow ingests boards, sprints, and board mappings from Jira Cloud. |
| Sensitive Data Access report | Open | May 2026 | [Sensitive Data Access report](/user-guide/classify-ui-trust-center#label-classify-trust-center-access-report) | Generate a report that lists users who accessed tables containing sensitive data classified by the Trust Center during a configurable lookback period. |
| Data protection policies in Snowsight | Open | May 2026 | [Manage data protection policies in Snowsight](/user-guide/data-protection-policies-snowsight) | Requires Enterprise Edition (or higher). Create and manage masking, row access, projection, aggregation, and join policies in Snowsight, with a Dashboard for policy posture, a Policies tab, and an Objects with policies tab. |
| DCR Agent | Open | May 2026 | [Snowflake Data Clean Rooms Agent](/user-guide/cleanrooms/dcr-agent) | Conversational interface in Snowflake CoWork for running approved Collaboration Data Clean Rooms analyses. |
| Online Feature Store | Open | May 2026 | [Serving online features](/developer-guide/snowflake-ml/feature-store/online-feature-store) | Serve features with low-latency online retrieval backed by Snowflake Postgres, with support for batch, stream, and real-time feature views. |
| Sensitive Data Entitlement report | Open | May 2026 | [Sensitive Data Entitlement report](/user-guide/classify-ui-trust-center#label-classify-trust-center-entitlement-report) | Generate a report that lists the users, roles, and privileges that grant access to tables containing sensitive data classified by the Trust Center. |
| Cortex Search auto-suspend | Open | May 2026 |  | Automatically suspend and resume serving compute for a Cortex Search Service after a period of query inactivity to reduce costs on idle services. |
| CUSTOM\_INCREMENTAL refresh mode for dynamic tables | Open | May 2026 | [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization) | Define custom MERGE or INSERT refresh logic for dynamic tables when standard refresh modes don’t support your transformation pattern. |
| Create tags in Snowsight (Tags & policies) | Open | April 2026 | [Work with object tags](/user-guide/object-tagging/work) | Create tags in Snowsight and use an expanded **Tags & policies** dashboard for tagging coverage across more object types. |
| Centralized event sharing for apps | Open | April 2026 | [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central) |  |
| Visualization policies for chart customization in Snowflake CoWork | Open | April 2026 | [Visualization policies for chart customization in Snowflake CoWork](/user-guide/snowflake-cortex/cortex-agents-viz-policies) |  |
| Apache Iceberg™ tables: Support for the Azure Data Lake Storage Gen2 with external volumes | Open | March 2026 | [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure) |  |
| Chart customization in Snowflake CoWork | Open | March 2026 | [Customize charts in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/chart-customization) |  |
| Semantic view materializations | Open | June 2026 | [Materializing dimensions and metrics in semantic views](/user-guide/views-semantic/materializations) |  |
| Semantic Studio | Open | August 2026 | [Semantic Studio](/user-guide/views-semantic/semantic-studio) |  |
| Supported Java and Scala APIs for Snowpark Connect | Open | March 2026 | [DataFrame support for Snowpark Connect for Spark](/developer-guide/snowpark-connect/snowpark-connect-dataframe-support) |  |
| Exporting a semantic view to a Tableau Data Source (TDS) file | Open | March 2026 | [Exporting a semantic view to a Tableau Data Source (TDS) file](/user-guide/views-semantic/sql#label-semantic-views-export-tableau) |  |
| pg\_lake extension for Snowflake Postgres | Open | March 2026 | [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake) |  |
| Custom runtime images | Open | May 2026 | [Custom Runtime Images](/developer-guide/snowflake-ml/custom-runtime-images) |  |
| Share Cortex Agents | Open | April 2026 | [Share Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-sharing) |  |
| Using the Snowpark Python JDBC | Open | January 2026 | [Using the Snowpark Python JDBC](/developer-guide/snowpark/python/snowpark-jdbc#label-snowpark-jdbc) |  |
| Optimize an existing semantic view or model with verified queries | Open | December 2025 | [Optimize an existing semantic view or model with verified queries](/user-guide/snowflake-cortex/cortex-analyst/analyst-optimization) |  |
| Import machine learning models from external services | Open | November 2025 | [Import and deploy models from an external service](/developer-guide/snowflake-ml/model-registry/snowsight-ui#label-model-import-external) |  |
| Cortex Analyst Routing Mode | Open | November 2025 | [Routing Mode for Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst/cortex-analyst-routing-mode) |  |
| Data quality anomaly detection | Open | November 2025 | [Detecting anomalies in data quality](/user-guide/data-quality-anomaly) |  |
| Executing Scala code using Snowpark Connect for Spark | Open | November 2025 | [Run Scala code from your client](/developer-guide/snowpark-connect/snowpark-connect-workloads-jupyter#label-snowpark-connect-run-scala-code) |  |
| Listings in government regions can be shared on the internal marketplace | Open | October 2025 | [About organizational listings](/user-guide/collaboration/listings/organizational/org-listing-about) |  |
| Use organization user groups with organizational listings | Open | October 2025 | [Use organization user groups with organizational listings](/user-guide/collaboration/listings/organizational/org-listings-org-user-groups) |  |
| Make database objects discoverable in Universal Search | Open | October 2025 | [Make database objects discoverable in Universal Search](/user-guide/ui-snowsight/object-visibility-universal-search) |  |
| Declarative Sharing for Native Apps | Open | September 2025 | [About Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/about) |  |
| Workspace sharing in Declarative Native Apps | Open | August 2026 | [Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces) | Share a directory of files and folders, including Snowflake Notebooks in Workspaces, as a read-only workspace in a Declarative Native App. |
| SnowConvert AI - ETL Migration | Open | October 2025 | [ETL Migration](/migrations/snowconvert-docs/general/user-guide/etl-migration-replatform) | Public preview feature for migrating SSIS packages to dbt projects on Snowflake. |
| Data quality monitoring dashboard | Open | July 2026 | [Using the data quality monitoring dashboard](/user-guide/data-quality-centralized-dashboard) | Account-wide data quality monitoring dashboard in Snowsight showing health KPIs, incidents, and monitored schemas across all tables in an Enterprise Edition account. |
| Data quality in Snowsight | Open | September 2025 | - [Monitoring data quality checks in Snowsight](/user-guide/data-quality-ui-monitor) - [Use data profiling to understand your data](/user-guide/data-quality-profile) |  |
| Gap-filling time-series data | Open | September 2025 | [RESAMPLE](/sql-reference/constructs/resample) |  |
| Manage integrations using Snowsight | Open | June 2025 | [Managing integrations in Snowsight](/user-guide/ui-snowsight-integrations) |  |
| Preconfigured Notebook runtimes | Open | June 2025 | [Create a notebook](/user-guide/ui-snowsight/notebooks-create) |  |
| Automated refresh and auto-ingest pipes for internal named stages | Open | April 2025 | - [CREATE STAGE](/sql-reference/sql/create-stage) - [CREATE PIPE](/sql-reference/sql/create-pipe) - [Automated directory table refreshes for internal stages](/user-guide/data-load-dirtables-auto#label-refreshing-directory-tables-automatically-internal-stages) | Currently available for Snowflake accounts hosted on AWS. |
| Cloning databases that contain hybrid tables | Open | March 2025 | [Clone databases that contain hybrid tables](/user-guide/tables-hybrid-clone) |  |
| Join policies | Open | January 2025 | [Join policies](/user-guide/join-policies) |  |
| CREATE OR ALTER <OBJECT> | Open | December 2024 | - [CREATE OR ALTER EXTERNAL FUNCTION](/sql-reference/sql/create-external-function#label-create-or-alter-external-function-syntax) - [CREATE OR ALTER FUNCTION (Snowpark Container Services)](/sql-reference/sql/create-function-spcs#label-create-or-alter-function-spcs-syntax) | Additional commands that create an object if it doesn’t exist, or alter it according to the object definition. |
| Snowflake Connector for SharePoint | Open | November 2024 | [About the Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/about) |  |
| Resource constraints for Snowpark-optimized warehouses | Open | September 2024 | [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized) |  |
| Snowflake Connector for PostgreSQL | Open | July 2024 | [About the Snowflake Connector for PostgreSQL](/connectors/postgres6/about) |  |
| Snowflake Connector for MySQL | Open | July 2024 | [About the Snowflake Connector for MySQL](/connectors/mysql6/about) |  |
| VS Code extension | Open | July 2024 | [Edit the Snowflake `connections.toml` file](/user-guide/vscode-ext#label-edit-toml) |  |
| Snowflake Native SDK for Connectors | Open | June 2024 | [Snowflake Native SDK for Connectors](/developer-guide/native-apps/connector-sdk/about-connector-sdk) |  |
| EXECUTE IMMEDIATE FROM template file | Open | May 2024 | [EXECUTE IMMEDIATE FROM](/sql-reference/sql/execute-immediate-from) | Execute a template file using the Jinja2 templating language. |
| Snowflake Connector for Google Analytics Raw Data | Open | January 2024 | [Snowflake Connector for Google Analytics Raw Data](/connectors/google/gard/gard-connector-about) |  |
| Snowflake Connector for Google Analytics Aggregate Data | Open | January 2024 | [Snowflake Connector for Google Analytics Aggregate Data](https://other-docs.snowflake.com/connectors/google/gaad/gaad-connector-about.html) |  |
| CREATE OR ALTER VERSIONED SCHEMA | Open | April 2023 | [CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) | Creates a versioned schema for an application instance if it doesn’t exist, or alters it according to the definition. Only supported in the Native Apps Framework. |
| Snowflake ML - FileSystem and FileSet | Open | N/A | [Load and write data](/developer-guide/snowflake-ml/load-data) | This feature is currently supported, but will not be made generally available. |
| External table support for Delta Lake | Open | February 2022 | [Introduction to external tables](/user-guide/tables-external-intro) |  |

Expand

Show lessSee more

## Managing access to all preview features

Snowflake provides the ability for account administrators to manage access to
preview features at the account level.

- Account administrators can enable or disable access to preview features for their entire Snowflake account.
  Additionally, account administrators can check whether all preview features are enabled or disabled.
- This setting affects all users and all preview features (including private preview features) within the account.
- By default, access to all preview features is enabled for most accounts.

Caution

Before disabling or enabling preview features for your account, please review
the associated documentation for a complete list of limitations and other information.

The following limitations apply to enabling and disabling preview feature access:

- Applies to both private and open preview features.
- This is an all-or-nothing setting that affects all users and all previews within an account.
- Any user in the account who is using a preview feature will lose access to that feature immediately after SYSTEM$DISABLE\_PREVIEW\_ACCESS is executed.
- Snowflake Marketplace products, which are managed separately through [IMPORTED PRIVILEGES](/user-guide/data-exchange-marketplace-privileges), are not covered as part of this capability.
- Client-side libraries (such as Snowpark API) are not covered as part of this capability.

### Checking the status of preview features in your account

To check whether preview features are enabled in your account, call the [SYSTEM$GET\_PREVIEW\_ACCESS\_STATUS](/sql-reference/functions/system_get_preview_access_status) function.

For example:

Copy code

```
SELECT SYSTEM$GET_PREVIEW_ACCESS_STATUS();
```

Which returns:

```
+-------------------------------------------------------+
| SYSTEM$GET_PREVIEW_ACCESS_STATUS()                    |
+-------------------------------------------------------+
| Preview access is [ENABLED|DISABLED] for this account |
+-------------------------------------------------------+
```

Indicating the current state of preview features for the account.

### Enabling preview features in your account

To enable preview features for your account, call the [SYSTEM$ENABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_enable_preview_access) function.

For example:

Copy code

```
SELECT SYSTEM$ENABLE_PREVIEW_ACCESS();
```

Which returns:

```
+---------------------------------------------------------------+
| SELECT SYSTEM$ENABLE_PREVIEW_ACCESS();                        |
+---------------------------------------------------------------+
| Preview access has been successfully enabled for this account |
+---------------------------------------------------------------+
```

### Disabling preview features in your account

To disable preview features for your account, call the [SYSTEM$DISABLE\_PREVIEW\_ACCESS](/sql-reference/functions/system_disable_preview_access) function.

Caution

Caution should be exercised when disabling preview features.
All preview features, including both public and private, are disabled when you call SYSTEM$DISABLE\_PREVIEW\_ACCESS.
Private preview features cannot be enabled by calling SYSTEM$ENABLE\_PREVIEW\_ACCESS.

Copy code

```
SELECT SYSTEM$DISABLE_PREVIEW_ACCESS();
```

Which returns:

```
+----------------------------------------------------------------+
| SYSTEM$DISABLE_PREVIEW_ACCESS()                                |
+----------------------------------------------------------------+
| Preview access has been successfully disabled for this account |
+----------------------------------------------------------------+
```
