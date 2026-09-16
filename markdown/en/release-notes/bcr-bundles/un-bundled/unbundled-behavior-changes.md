# Unbundled behavior changes

Unbundled behavior changes are not associated or released with a behavior change bundle.

To help you manage your operations and minimize disruption to your Snowflake service, we document behavior changes that may impact your usage,
including:

- [Recently implemented changes](#label-unbundled-changes-recently-implemented-changes) that were previously pending/disabled, were not part of a behavior change bundle, and cannot be disabled.
- [Upcoming pending changes](#label-unbundled-changes-upcoming-pending-changes) that will not be part of a behavior change bundle and cannot be enabled in advance.
- [Canceled behavior changes](/release-notes/bcr-bundles/un-bundled/unbundled-cancelled-behavior-changes#label-unbundled-changes-canceled-changes) that have been removed from BCR bundles and will not be implemented.

If you have questions about any of these behavior changes, please feel free to contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Recently implemented changes

This table lists behavior changes that were implemented independently of a behavior change bundle.
This table includes certain types of changes to Snowflake clients (connectors, drivers, and so on), platforms, and libraries. Such changes can’t be disabled.

See also [Upcoming pending changes](#label-unbundled-changes-upcoming-pending-changes).

| Release Date | Functional Area | Implemented Behavior Change | Additional Notes |
| --- | --- | --- | --- |
| **September 4, 2026** | Behavior Changes | [New columns in table function output are no longer treated as behavior changes](/release-notes/bcr-bundles/un-bundled/bcr-no-bcrs-for-new-columns-table-functions) |  |
| **August 20, 2026** | Cortex Agents — Managed MCP Server | [MCP: Streaming responses for tool calls (August 2026)](/release-notes/bcr-bundles/un-bundled/bcr-2405) | Managed MCP `tools/call` responses changed from a single JSON body to an SSE stream. Spec-compliant clients are unaffected. |
| **August 12, 2026** | Cortex Model Updates for August | [Cortex model deprecations for August 2026](/release-notes/bcr-bundles/un-bundled/bcr-august-model-deprecations) | Listed models enter the legacy state. Accounts that already used a listed model can continue until each model’s end-of-life date; accounts that had not used it can’t start. |
| **July 24-27, 2026** | Billing Entity Deprecation - Account Management SQL and Account View Changes | [Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399) |  |
| **July 20-27, 2026** | Snowflake App Runtime | [Snowflake App Runtime: execution role and caller’s rights for apps in a personal database](/release-notes/bcr-bundles/un-bundled/bcr-snow-3708067) |  |
| **June 30, 2026** | Cortex Model Updates for June | [Cortex model deprecations for July 2026](/release-notes/bcr-bundles/un-bundled/bcr-june-model-deprecations) | Some models will remain available through cross-region inference only after this date. |
| **June 12-18, 2026** | Virtual Warehouses | [Warehouses: Enable QAS by default for newly created Gen2 and multi-cluster warehouses](/release-notes/bcr-bundles/un-bundled/bcr-2113) | This behavior change was originally in the 2025\_07 bundle. It was delivered through [Warehouses: Enable QAS by default for newly created Gen2 and multi-cluster warehouses](/release-notes/bcr-bundles/2026_03/bcr-2269) in the 2026\_03 behavior change bundle. |
| **May 18, 2026** | Snowpark Container Services | [BIND SERVICE ENDPOINT granted to PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-2321) |  |
| **May 8-14, 2026** | Behavior Changes | [New columns in views and SHOW command output are no longer treated as behavior changes](/release-notes/bcr-bundles/un-bundled/bcr-no-bcrs-for-new-columns) |  |
| **April 22, 2026** | Cortex Model Updates for April | [Cortex model deprecations for May 2026](/release-notes/bcr-bundles/un-bundled/bcr-may-model-deprecations) |  |
| **April 1, 2026** | Cortex Model Updates for April | [Cortex model deprecations for April 2026](/release-notes/bcr-bundles/un-bundled/bcr-april-model-deprecations) |  |
| **Week of March 16, 2026** | Document AI decommission | [Document AI decommission](/release-notes/bcr-bundles/un-bundled/bcr-2156) |  |
| **Weeks of December 2, 2025 (early adopters) and January 7, 2026 (late adopters)** | Snowsight Templates learning environment | [Snowsight Templates learning environment](/release-notes/bcr-bundles/un-bundled/bcr-1992) | This change is being rolled out gradually. |
| **Week of November 17, 2025** | Data quality monitoring | [Data quality: DATA\_METRIC\_USER database role granted to the PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-2155) |  |
| **Week of November 10, 2025** | Native Apps | [Snowflake Native Apps: Changes to restrictions on version name, setup file name](/release-notes/bcr-bundles/un-bundled/bcr-2169) |  |
| **Week of November 10, 2025** | Security | [Authentication for local applications: Built-in security integration for Snowflake OAuth](/release-notes/bcr-bundles/un-bundled/bcr-2056) | This change is being rolled out gradually to all accounts. |
| **Week of August 4, 2025** | Data quality monitoring | [Data quality: DATA\_QUALITY\_MONITORING\_LOOKUP application role granted to the PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-2068) |  |
| **Week of June 23, 2025** | Snowflake Native Apps | [Snowflake Native Apps: Changes to privileges commonly used by apps](/release-notes/bcr-bundles/un-bundled/bcr-1952) |  |
| **Week of March 17, 2025** | Data Lineage | [Data Lineage: VIEW LINEAGE privilege granted to the PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-1933) |  |
| **Week of March 3, 2025** | Document AI | [Document AI: CREATE MODEL privilege required to create, publish, and train model builds](/release-notes/bcr-bundles/un-bundled/bcr-1904) |  |
| **Week of February 24, 2025** | Virtual Private Cloud IDs | [Amazon Virtual Private Cloud ID for external stage, external function, and external volume](/release-notes/bcr-bundles/un-bundled/bcr-vpc-change-2025-02-03) |  |
| **Week of January 20, 2025** | Secure objects | [Secure objects: Redaction of information in error messages](/release-notes/bcr-bundles/un-bundled/bcr-1858) |  |
| **Week of June 17, 2024** | HTTP Error Codes | [Change in HTTP error code for URL not found error](/release-notes/bcr-bundles/un-bundled/bcr-1669) |  |
| **May 10, 2024** | Snowflake Cortex ML Functions Changes | [Cortex ML Functions - New column in single-series Forecasting and Anomaly Detection results](/release-notes/bcr-bundles/un-bundled/bcr-cortex-forecast-anomaly-detection-series-column) |  |
| **March 26, 2024** | SQL Changes — Organization Usage Views | [Organization Usage: Updated billing views](/release-notes/bcr-bundles/un-bundled/bcr-1584) |  |
| **March 04-05, 2024** | Data Pipelines: Dynamic Tables | [Dynamic tables: Changes to ACCOUNT\_USAGE.TABLES and INFORMATION\_SCHEMA.TABLES](/release-notes/bcr-bundles/un-bundled/bcr-account-usage-and-info-schema-changes) |  |

Expand

Show lessSee more

For additional released, but archived, unbundled BCRs see: [Archived implemented unbundled behavior changes](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes-implemented-archive).

## Upcoming pending changes

The following table lists unbundled behavior changes that are pending.
Pending unbundled behavior changes aren’t released yet.

Important

All information in this table, including planned versions and dates, is subject to change; the information is provided only as a guideline
for any updates you must make to accommodate the changes.

If a link isn’t provided to the individual pending behavior change, the release in which the bundle was introduced hasn’t started or is
still in progress.

| Planned Release | Functional Area | Pending Behavior Change | Additional Notes |
| --- | --- | --- | --- |
| **September 2, 2026** | Cortex Agents, Snowflake CoWork | [Cortex Agents and Snowflake CoWork: Runs proceed when some tools are inaccessible](/release-notes/bcr-bundles/un-bundled/bcr-2425) | Cortex Agents and Snowflake CoWork continue a run with the tools the caller’s role can access instead of failing with an HTTP 4XX error. Set `orchestration.tool_not_accessible` to `legacy` before the rollout to keep the current behavior. |
| **August 20, 2026** | Azure access: Snowflake Network Identifiers for rules that filter based on subnet IDs | [Use Snowflake Network Identifiers in Azure allowlists for Azure Storage and Azure Key Vault (August 2026) (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-2391) | Customers who allowlist Azure Storage or Azure Key Vault by subnet ID must also allowlist Snowflake Network Identifiers, preferably through Azure Network Security Perimeter (NSP). Key Vault requires NSP; Storage can use NSP or the storage firewall during migration. |
| **August 5, 2026** | Snowflake Cortex AI | [CORTEX\_MODELS\_ALLOWLIST deprecation and embedding model RBAC enforcement (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-2378) | `CORTEX_MODELS_ALLOWLIST` is deprecated and can only be set to `'None'`; accounts are migrated to model RBAC, and embedding model RBAC is enforced through the 2026\_07 bundle. Rollout completes November 18, 2026. |
| **September 1, 2026** | Snowsight — Notebooks | [Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks) | Creation of new Legacy Notebooks disabled September 1; execution and editing disabled November 2026. |
| **July 27-29, 2026** | Snowflake CoWork Automations | [Snowflake CoWork Automations: EXECUTE AGENT TASK privilege granted to PUBLIC by default](/release-notes/bcr-bundles/un-bundled/bcr-2349) | EXECUTE AGENT TASK privilege on the account is granted to PUBLIC by default. Administrators can revoke and re-grant to selected roles. |
| **June 26, 2026** | Snowpark Python | [Default package source changes for Snowpark Python](/release-notes/bcr-bundles/un-bundled/bcr-2325) | Affects Python 3.14+ workloads and newly created accounts. |
| Pending | Snowflake CoWork | [Snowflake CoWork: MANAGE ARTIFACT PUBLICATION ON ACCOUNT privilege granted to the PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-manage-artifact-publication) | This change will be rolled out gradually. |
| **April 24, 2026** | Cortex Agents, AI Observability | [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events) | The new **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE** account privilege is off by default for all roles and impacts visibility of raw content in Cortex and External Agent observability data. |
| **May 18, 2026** | Snowpark Python | [PYPI\_REPOSITORY\_USER database role granted to the PUBLIC role](/release-notes/bcr-bundles/un-bundled/bcr-2280) | This change will be rolled out gradually. |
| To be determined | Data pipelines | [Completed rollout of BYTES\_BILLED column in history views (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-2241) | None |
| Most of this change will occur gradually across all regions in June - July 2026. | Security | [Wider variety of Certificate Authorities and shorter certificate lifetimes](/release-notes/bcr-bundles/un-bundled/bcr-2255) |  |
| This change is planned for February 2026. | Network connectivity | [GCP PSC propagated connection limit set to 0](/release-notes/bcr-bundles/un-bundled/bcr-2193) |  |
| This change is planned for September 2026. | SQL Changes - General | [SQL general: New default column sizes for string and binary data types (Postponed)](/release-notes/bcr-bundles/un-bundled/bcr-2118) |  |
| This change is planned for October 2025. | Snowflake Native Apps: Decommissioning of Python versions 3.8 and 3.9 | [Snowflake Native Apps: Deprecation of Python versions 3.8 and 3.9 (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-2072) | Snowflake Native Apps will no longer support any decommissioned versions of Python when Python version 3.9 is deprecated in October 2025. For more information on Snowflake’s Python runtime support policy, see [Snowflake Python Runtime Support](/developer-guide/python-runtime-support-policy). |
| This change will occur gradually. | Worksheets to Workspaces upgrade | [Defaulting accounts from Worksheets to Workspaces](/release-notes/bcr-bundles/un-bundled/bcr-2117) | This change will roll out gradually beginning the week of September 22, 2025. |
| This change is planned for September 2025. | New VNET subnet IDs required for rules that filter based on subnet ID | [Azure access: New VNET subnet IDs required for rules that filter based on subnet ID (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-1955-2078) |  |
| This change will occur gradually across all AWS regions from January 5 to January 31, 2025. | Change of Certificate Authority & OCSP Allowlist for AWS Customers | [Change of Certificate Authority and OCSP Allowlist for AWS Customers](/release-notes/bcr-bundles/un-bundled/bcr-1657) |  |
| This change will occur gradually across all regions from October - November 2024 (Azure & GCP), February 2025 (AWS). | TLS Cipher Suite Requirements | [Changes in TLS Cipher Suite Requirements](/release-notes/bcr-bundles/un-bundled/bcr-1727) |  |
|  | Snowflake CLI, Connectors, Drivers, and SQL API Changes | [SnowSQL- Change to the value of the sql\_split property (Pending)](/release-notes/bcr-bundles/un-bundled/bcr-792) |  |
|  | Account Usage and Information Schema views: Changes to DATA\_TYPE output for string columns. | [Account Usage and Information Schema views: Changes to DATA\_TYPE output for string columns (Postponed)](/release-notes/bcr-bundles/un-bundled/bcr-1960) | This behavior change was originally in the 2025\_03 bundle and intended to become enabled by default in the 2025\_04 bundle. However, it has been postponed and a new release date has not been determined.  This change is not available for testing. |
|  | SHOW FUNCTIONS and SHOW PROCEDURES commands. | [SHOW FUNCTIONS and SHOW PROCEDURES commands: The complete data type for arguments is displayed in output (Postponed)](/release-notes/bcr-bundles/un-bundled/bcr-1944) | This behavior change was originally in the 2025\_03 bundle and intended to become enabled by default in the 2025\_04 bundle. However, it has been postponed and a new release date has not been determined.  This change is not available for testing. |
|  | Data Loading / Unloading Changes. | [Data loading, data unloading, and file staging DML commands: Single-character pattern matches (Postponed)](/release-notes/bcr-bundles/un-bundled/bcr-209969) | This change was originally planned for February 2021; however, it has been postponed and a new release date has not been determined.  This change is not available for testing. |
|  | Information Schema: TABLE\_PRIVILEGES view. | [TABLE\_PRIVILEGES View: Update GRANTOR column value in the consumer account (Postponed)](/release-notes/bcr-bundles/un-bundled/bcr-1321) | This behavior change was originally planned for **September 2023**; however, it has been postponed and a new release date has not been determined.  This change is not available for testing. |
|  | Cloning: Table history. | [Cloning: Table history not preserved on clone (Postponed)](/release-notes/bcr-bundles/2023_07/bcr-908) | This behavior change was originally in the 2023\_07 bundle and intended to become enabled by default in the 2023\_08 bundle. However, it has been postponed and a new release date has not been determined.  This change is not available for testing. |

Expand

Show lessSee more
