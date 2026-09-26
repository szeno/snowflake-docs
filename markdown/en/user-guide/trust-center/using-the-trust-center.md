# Using the Trust Center

This topic describes how to monitor Trust Center costs, and manage scanners, findings, and security risks by using the Trust Center
Snowsight interface.

## Monitoring cost

The Trust Center incurs [serverless compute cost](/user-guide/cost-understanding-compute#label-serverless-credit-usage) when it scans your Snowflake environment for
security vulnerabilities.

You can use cost-related views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas to track the costs associated with the Trust Center. When
querying these views, filter on the `service_type` column to find `TRUST_CENTER` values.

| View | Schema | `service_type` | Roles with required privileges |
| --- | --- | --- | --- |
| [METERING\_HISTORY](/sql-reference/account-usage/metering_history) | ACCOUNT\_USAGE | TRUST\_CENTER | - ACCOUNTADMIN role - USAGE\_VIEWER database role |
| [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history) | ACCOUNT\_USAGE | TRUST\_CENTER | - ACCOUNTADMIN role - USAGE\_VIEWER database role |
| [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history) | ORGANIZATION\_USAGE | TRUST\_CENTER | - ORGADMIN role - ORGANIZATION\_USAGE\_VIEWER database role |
| [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) | ORGANIZATION\_USAGE | TRUST\_CENTER | - ORGADMIN role - ORGANIZATION\_BILLING\_VIEWER database role |

Expand

Show lessSee more

**Example:** View the total cost that the Trust Center incurred between December 1, 2024 and December 31, 2024.

Copy code

```
SELECT
   SUM(credits_used) AS total_credits
FROM snowflake.account_usage.metering_history
WHERE
   service_type = 'TRUST_CENTER' AND
   start_time >= '2024-12-01' AND
   end_time <= '2024-12-31';
```

**Example:** View the daily cost that the Trust Center incurred after December 1, 2024.

Copy code

```
SELECT
   usage_date AS date,
   credits_used AS credits
FROM snowflake.account_usage.metering_daily_history
WHERE
   service_type = 'TRUST_CENTER' AND
   date > '2024-12-01';
```

For information about how many credits are charged per Compute-Hour for the operation of the Trust Center, see Table 5 in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Use the Trust Center Snowsight interface

The Trust Center Snowsight interface has the following tabs:

- **Overview** - Displays a high-level summary of Trust Center findings for your account, including the [Account posture](#label-trust-center-account-posture)
  section. Select the **View** option in each section of **Overview** to see more detailed information about a specific aspect of your
  account’s security posture.
- **Violations** - Shows violations, suggests remediation actions for them, and provides detailed information about them. For information
  about using this tab, see [Manage the violation findings lifecycle](#label-managing-findings) and [Manage security risks](#label-trust-center-managing-security-risks).
- **Detections** - Shows the detections found by the scanners and provides information about them. For information about using this tab,
  see [View Trust Center detection findings](#label-trust-center-alerts-managing).
- **Manage scanners** - Contains the **Scanner packages**, **Extensions**, and **Settings** sub-tabs:
  - **Scanner packages** - View and manage scanner packages and individual scanners. For more information, see
    [Manage scanner packages](#label-trust-center-managing-scanners) and [Manage scanners](#label-trust-center-managing-individual-scanners).
  - **Extensions** - Create Trust Center extensions by using the Snowflake Native App Framework. For more information, see
    [Using Trust Center extensions](/user-guide/trust-center/trust-center-extensions).
  - **Settings** - Manage account-level Trust Center settings, such as [Secure by default](#label-trust-center-secure-by-default)
    (available only for accounts on [Business Critical Edition](/user-guide/intro-editions) or
    [Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract).
- **Data Security** - Set up [sensitive data classification](/user-guide/classify-intro) and monitor classification
  results from a dedicated dashboard. For more information, see [Use the Trust Center to set up sensitive data classification](/user-guide/classify-ui-trust-center).
- **AI Security** - Monitor the security posture of AI workloads in your account, including
  Cortex Agents, the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package), and [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails)
  runtime protections. For more information, see [View the AI Security tab](#label-trust-center-ai-security-tab).

## Review account posture

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The **Account posture** section on the **Overview** tab aggregates Trust Center monitoring activity for your account over a time period
that you select, and generates a PDF report of that activity.

The rest of the Trust Center tells you what’s at risk in your account right now: open [violations](#label-trust-center-view-violations)
and [detections](#label-trust-center-detections-view), authentication readiness, [sensitive data](/user-guide/classify-ui-trust-center),
and [AI workload risks](#label-trust-center-ai-security-tab). Account posture adds the other half of that picture. It shows which findings
were remediated, which violations you triaged and muted, and which scanners ran and reported no at-risk entities. Reporting on that
activity previously meant writing your own queries against account usage data, or building your own tooling to share the results.

Use account posture and the posture report to:

- **Show the controls that pass, not just the risks that are open.** Scanners that ran clean during the period are reported alongside open
  findings, so a reviewer can see which checks your account satisfies.
- **Show progress over a period.** Violation findings are grouped as newly opened, remediated, increased, decreased, unchanged, and muted,
  so you can demonstrate how your posture changed instead of reporting a single count.
- **Share evidence with people who don’t use your account.** The PDF is a self-contained, point-in-time record of the period you select,
  which makes it useful for compliance evidence and for management or auditor reporting.

To open the section, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has the `SNOWFLAKE.TRUST_CENTER_VIEWER` or `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it. For
   more information, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Overview** tab.

### Account posture widgets

The **Account posture** section includes the following widgets:

- **Scanning status** - A chart that shows how many of your account’s total scanners ran during the selected period, and what share of
  findings report zero at-risk entities.
- **Findings** - The number of open findings and how that count changed compared with the start of the selected period.
- **At-risk entities** - The total number of entities discovered and the change over the period, broken out by entity type such as **User**,
  **Table**, and **Procedure**.

### Generate a posture report

To generate a PDF posture report:

1. On the **Overview** tab, in the **Account posture** section, select a time period from the drop-down menu. The default is **Last 28
   days**.
2. Select **Generate report**.

The Trust Center generates a PDF report. The report header records the account name, reporting period, and generation time. All timestamps in the
report are shown in UTC.

### Contents of the posture report

The PDF posture report includes the following sections:

- **Scanner enablement** - How many first-party scanners are enabled, with coverage for each scanner package.
- **Scanner activity in period** - Which scanners ran during the period, how many found no at-risk entities, and active scanner posture by
  package.
- **Configuration changes** - The most recent enable or disable per scanner package, and violation triage activity (mute, unmute, comments)
  within the reporting period. This section doesn’t include earlier package state history, individual scanner enable or disable, schedule
  updates, or notification-setting changes. To see who made other configuration changes, review your account’s query history.
- **Violation findings activity in period** - Violations grouped as newly opened, remediated, increased, decreased, unchanged, no active
  findings, and muted. Each entry includes the scanner, scanner package, at-risk entity count, and percent change where applicable.
- **Detection findings activity in period** - Detections reported during the period and scanners that ran but reported no detections.
- **Scanner status** - For each scanner package, each scanner’s description, status, last run in the period, and schedule.

## View the AI Security tab

The **AI Security** tab provides centralized security observability for the AI workloads in your
account. It surfaces the list of Cortex AI agents, AI Security scanner coverage, enablement status of Cortex AI guardrails, and any
violations and detections that are reported by the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package).

Snowflake recommends that you use this tab as the starting point for monitoring AI security if you are using
[Cortex Agents](/user-guide/snowflake-cortex/cortex-agents),
[Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork), or
[Cortex Code](/user-guide/cortex-code/cortex-code).

To open the tab, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has the `SNOWFLAKE.TRUST_CENTER_VIEWER` or `SNOWFLAKE.TRUST_CENTER_ADMIN` application
   role granted to it. For more information, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **AI Security** tab.

The tab is organized into the following sections:

### AI Security status

The top of the tab shows the current state of AI agents, scanner coverage, and guardrails through the following
status cards:

- **AI Agents** - Shows the number of [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) that have been
  created in your account, so that you can quickly understand the scope of agentic AI usage that you must secure.
  Select the card to open a list of all AI agents in the account. For more information, see
  [AI agents inventory](#label-trust-center-ai-security-ai-agents).
- **AI Security Scanners** - Shows how many scanners in the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package) are currently
  enabled (for example, `4 of 4 scanners enabled`). Select the card to open the AI Security scanner package
  settings, where you can [enable or disable individual scanners](#label-trust-center-enable-disable-scanner)
  and [change their schedule](#label-trust-center-change-scanner-schedule). If fewer than all scanners are
  enabled, enable the remaining scanners to maximize coverage of AI-related security findings.
- **Cortex AI Guardrails** - Shows whether [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails)
  are configured for the account. If guardrails are not configured, select the card to open the account-level
  AI settings where you can turn on the runtime `advanced_prompt_injection` guardrail for Cortex Code.
  Configuring guardrails provides a runtime layer of protection.

### Violations and detections

The lower section of the tab shows the AI-related findings reported by the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package)
over the last 7 days:

- **Violations** - A time-series chart of AI-related violations, broken down by severity. Select the chart to
  open the Violations tab filtered to AI Security findings. For more information, see
  [View violations](#label-trust-center-view-violations).
- **Detections** - A time-series chart of AI-related detections, for example, sensitive data accessed by an agent.
  Select the chart to open the Detections tab filtered to AI Security findings. For more
  information, see [View detections](#label-trust-center-detections-view).

Note

The **AI Security** tab depends on findings from the [AI Security scanner package](/user-guide/trust-center/overview#label-ai-security-scanner-package). Enable
the package on the Manage scanners tab to populate the violations and detections charts. For
more information, see [Enable the AI Security scanner package](/user-guide/trust-center/getting-started#label-trust-center-enable-ai-security-scanner-package).

### AI agents inventory

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The **AI Agents Inventory** section provides a consolidated inventory of the [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
in your account, filtered by one or more categories. It helps identify which agents should be assessed or investigated further for better governance and security posture.

The section includes:

- **Observability categories**: Summary cards showing how many agents match a given category. Select a card to
  filter the agent list to that category. The categories are: **No budget**, **Web search**, **Code execution**,
  **Internal MCP**, **No instructions**, and **External MCP**.
- **Agent list**: A searchable, sortable table of Cortex Agents with the following columns: **Name**, **Owner**,
  **Database**, **Schema**, **Categories** (the categories that apply to the agent), and **Created**. Select an
  agent to open its details.

## Manage scanner packages

You can complete the following tasks to manage scanner packages in the Trust Center:

- [Manage secure by default](#label-trust-center-secure-by-default) (available only for accounts on
  [Business Critical Edition](/user-guide/intro-editions) or
  [Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract).
- [View the list of scanners in a package](#label-trust-center-view-scanner-list).
- [Enable scanner packages](#label-trust-center-enable-scanner-packages).
- [View available scanner packages](#label-trust-center-view-scanner-packages).
- [Change the schedule for a scanner package](#label-trust-center-change-scanner-package-schedule).
- [Run a scanner package on demand](#label-trust-center-start-scanner-package-on-demand).

### Secure by default

Note

Secure by default is available only for accounts on
[Business Critical Edition](/user-guide/intro-editions) or
[Virtual Private Snowflake (VPS)](/user-guide/intro-editions) with a capacity contract.

For those accounts, Snowflake automatically enables the Trust Center
[AI Security scanner package](/user-guide/trust-center/getting-started#label-trust-center-enable-ai-security-scanner-package)
when AI feature usage is detected, so you get coverage without enabling that package
manually. This *secure by default* approach applies to new and existing accounts.

Snowflake automatically enables the AI Security scanner package only if it has never been
explicitly disabled.

The automatically enabled AI Security scanner package incurs
[serverless compute cost](#label-trust-center-monitoring-cost) the same way as a manually enabled
package. You can disable the package at any time, and Snowflake won’t re-enable it.

#### Enable or disable secure by default

To change the secure by default setting, your role must have the `SNOWFLAKE.TRUST_CENTER_ADMIN`
application role. To view the current setting, your role must have either the
`SNOWFLAKE.TRUST_CENTER_ADMIN` or `SNOWFLAKE.TRUST_CENTER_VIEWER` application role. For more
information, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).

Disabling secure by default doesn’t disable scanner packages that are already enabled.

To change the setting in Snowsight, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select the account **Settings** sub-tab. Don’t open the **Settings** tab of an individual
   scanner package.
6. Enable or disable secure by default.

   If you’re disabling secure by default, enter a comment that describes why you’re changing the
   setting.

Alternatively, use stored procedures:

- To enable or disable secure by default, call
  [UPDATE\_AUTO\_ENABLEMENT\_STATUS](/sql-reference/stored-procedures/update_auto_enablement_status).
- To view the current setting, call
  [GET\_AUTO\_ENABLEMENT\_STATUS](/sql-reference/stored-procedures/get_auto_enablement_status). The `IS_OPTED_IN` column is
  `TRUE` when secure by default is enabled for the account.

### View the list of scanners in a package

To view the list of scanners provided in a scanner package, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. From the list, select a scanner package.

### Enable scanner packages

To enable a scanner package, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select **Enable Package**.

After you enable a scanner package, you can
[enable or disable individual scanners in the scanner package](#label-trust-center-enable-disable-scanner).

### View available scanner packages

To view available scanner packages, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Optionally, select **Provider**, **Status**, or **Search** to filter the list of scanner packages available.

### Change the schedule for a scanner package

You can change the schedule for all scanner packages, except the [Security Essentials scanner package](/user-guide/trust-center/overview#label-security-essentials-scanner-package).

Tip

After a scanner package is enabled, you can
[change the schedule for individual scanners in the scanner package](#label-trust-center-change-scanner-schedule).

To change the schedule for a scanner package, follow these steps:

1. Ensure you’ve enabled the [CIS Benchmarks scanner package](/user-guide/trust-center/overview#label-cis-benchmarks-scanner-package).
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
4. In the navigation menu, select **Governance & security** » **Trust Center**.
5. Select the **Manage scanners** tab.
6. Select a scanner package from the list.
7. Select the **Settings** tab.
8. Under **Scanner Package Schedule**, select [![trust center edit image](/static/images/ui-trust-center-edit.png)](/static/images/ui-trust-center-edit.png) **Edit**.
9. Set your desired **Frequency**.
10. Select **Continue**.

### Run a scanner package on demand

To run a scanner package on demand, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Next to **Search**, select [![trust center start image](/static/images/ui-trust-center-start.png)](/static/images/ui-trust-center-start.png) **Run Package**.

## Manage scanners

You can complete the following tasks to manage scanners in the Trust Center:

- [View details for a scanner](#label-trust-center-view-scanner-detail-descriptions).
- [Enable or disable a scanner in a scanner package](#label-trust-center-enable-disable-scanner).
- [Change the schedule for a scanner](#label-trust-center-change-scanner-schedule).
- [Reset the schedule for a scanner to the scanner package schedule](#label-trust-center-reset-scanner-schedule).
- [Run a scanner on demand](#label-trust-center-start-scanner-on-demand).
- [Configure custom settings for a scanner](#label-trust-center-configure-scanner-custom-config).

### View details for a scanner

To view details that describe what each scanner does, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. Select a scanner from the list of scanner names.

### Enable or disable a scanner in a scanner package

Attention

Scanners provide valuable information about possible security risks at a minimal cost.
Before disabling a scanner, we recommend evaluating the value of the information provided
by the scanner in relation to the cost associated with running it. For more information about
evaluating the cost associated with a scanner, see [Monitoring cost](#label-trust-center-monitoring-cost).

If a scanner package is disabled, all of the scanners in the package are disabled, including
scanners that were enabled individually.

To enable or disable a scanner in a scanner package, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Manage scanners** tab.
5. Select a scanner package from the list.
6. In the scanner **STATE**, enable or disable the scanner.
7. In the confirmation box, select **Confirm**.

### Change the schedule for a scanner

You can change the schedule for schedule-based scanners. You can’t change the schedule for event-based scanners. You can only
[enable or disable](#label-trust-center-enable-disable-scanner) an event-driven scanner.

Note

When a custom schedule is set for an individual scanner, that setting is used instead of its scanner package schedule,
even if the scanner package schedule is changed.

To change the schedule for a scanner, follow these steps:

1. Ensure that you [enabled the scanner](#label-trust-center-enable-disable-scanner).
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
4. In the navigation menu, select **Governance & security** » **Trust Center**.
5. Select the **Manage scanners** tab.
6. Select a scanner package from the list.
7. Select [![trust center vertical more image](/static/images/ui-trust-center-vertical-more.png)](/static/images/ui-trust-center-vertical-more.png) **More** for the scanner, and then select **Edit schedule**.
8. Set your desired **Frequency**.
9. Select **Save**.

### Reset the schedule for a scanner to the scanner package schedule

To change the schedule for a scanner to match its scanner package schedule, follow these steps:

1. Ensure that you [enabled the scanner](#label-trust-center-enable-disable-scanner).
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
4. In the navigation menu, select **Governance & security** » **Trust Center**.
5. Select the **Manage scanners** tab.
6. Select a scanner package from the list.
7. Select [![trust center vertical more image](/static/images/ui-trust-center-vertical-more.png)](/static/images/ui-trust-center-vertical-more.png) **More** for the scanner, and then select **Edit schedule**.
8. Select **Reset**, and then select **Reset to scanner package schedule**.
9. Select **Save**.

### Run a scanner on demand

To run a scanner on demand, follow these steps:

1. Ensure that you [enabled the scanner](#label-trust-center-enable-disable-scanner).
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
4. In the navigation menu, select **Governance & security** » **Trust Center**.
5. Select the **Manage scanners** tab.
6. Select a scanner package from the list.
7. Select [![trust center vertical more image](/static/images/ui-trust-center-vertical-more.png)](/static/images/ui-trust-center-vertical-more.png) **More** for the scanner, and then select **Run scanner**.

### Configure custom settings for a scanner

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Some scanners expose configurable parameters, called custom configurations, that let you tune scanner behavior for your environment. Custom configurations are defined by the scanner itself and typically adjust thresholds or lookback windows. Tuning these values can reduce false positives and let you keep a scanner enabled while still getting meaningful findings.

#### Identify which scanners support custom configurations

Not all scanners have custom configurations. To check whether a scanner supports them, query the `SNOWFLAKE.TRUST_CENTER.SCANNERS` view and look for scanners where `HAS_CUSTOM_CONFIGURATION` is `TRUE`:

Copy code

```
SELECT SCANNER_PACKAGE_ID, SCANNER_ID, SCANNER_NAME, HAS_CUSTOM_CONFIGURATION
FROM SNOWFLAKE.TRUST_CENTER.SCANNERS
WHERE HAS_CUSTOM_CONFIGURATION = TRUE;
```

The following first-party scanners currently support custom configurations:

**CIS Benchmarks** (`CIS_BENCHMARKS`)

| Scanner | SCANNER\_ID | Configuration |
| --- | --- | --- |
| Password length policy | `CIS_BENCHMARKS_CIS1_5` | `MIN_PASSWORD_LENGTH` |
| RSA key rotation | `CIS_BENCHMARKS_CIS1_7` | `KEY_ROTATION_DAYS` |
| User inactivity | `CIS_BENCHMARKS_CIS1_8` | `INACTIVITY_DAYS` |
| Admin session timeout | `CIS_BENCHMARKS_CIS1_9` | `MAX_IDLE_TIMEOUT_MINS` |
| Data retention floor | `CIS_BENCHMARKS_CIS4_4` | `MIN_DATA_RETENTION_FLOOR` |

Expand

Show lessSee more

**Threat Intelligence** (`THREAT_INTELLIGENCE`)

| Scanner | SCANNER\_ID | Configuration |
| --- | --- | --- |
| Long-running queries | `THREAT_INTELLIGENCE_ENTITIES_WITH_LONG_RUNNING_QUERIES` | `NUM_STANDARD_DEVIATIONS` |
| Long-running queries | `THREAT_INTELLIGENCE_ENTITIES_WITH_LONG_RUNNING_QUERIES` | `EXCLUDED_APP_NAMES` |

Expand

Show lessSee more

Use the `SCANNER_PACKAGE_ID` and `SCANNER_ID` values when calling the stored procedures below. Don’t use display names; only the IDs are accepted.

To see the available configurations for a specific scanner, including their descriptions, allowed values, and current defaults, query `SNOWFLAKE.TRUST_CENTER.CONFIGURATION_VIEW` filtered by `SCANNER_PACKAGE_ID` and `SCANNER_ID`:

Copy code

```
SELECT
  SCANNER_PACKAGE_ID,
  SCANNER_ID,
  CONFIGURATION_NAME,
  SET_CONFIGURATION_VALUE,
  COALESCE(DEFAULT_SCANNER_VALUE, DEFAULT_SCANNER_PACKAGE_VALUE) AS DEFAULT_CONFIGURATION_VALUE,
  DESCRIPTION,
  ALLOWED_VALUES,
  ALLOWED_PATTERN,
  EXPECTED_TYPE
FROM SNOWFLAKE.TRUST_CENTER.CONFIGURATION_VIEW
WHERE SCANNER_ID = '<SCANNER_ID>'
  AND SCANNER_PACKAGE_ID = '<SCANNER_PACKAGE_ID>';
```

The `CONFIGURATION_NAME` column is the value to pass as the first argument to `set_configuration` and `unset_configuration`. The `SET_CONFIGURATION_VALUE` column shows the value currently applied to your account, or `NULL` if no override is set and the default is in effect.

#### Set a custom configuration

To set a custom configuration value for a scanner, call `snowflake.trust_center.set_configuration`:

Copy code

```
CALL snowflake.trust_center.set_configuration(
  '<CONFIG_NAME>',
  '<VALUE>',
  '<SCANNER_PACKAGE_ID>',
  '<SCANNER_ID>'
);
```

Example:

Copy code

```
-- CIS 1.5: require password policies to have a minimum password length of 16 characters
CALL snowflake.trust_center.set_configuration(
  'MIN_PASSWORD_LENGTH', '16',
  'CIS_BENCHMARKS', 'CIS_BENCHMARKS_CIS1_5'
);
```

#### Unset a custom configuration

To remove a custom configuration and revert the scanner to its default value, call `snowflake.trust_center.unset_configuration`:

Copy code

```
CALL snowflake.trust_center.unset_configuration(
  '<CONFIG_NAME>',
  '<SCANNER_PACKAGE_ID>',
  '<SCANNER_ID>'
);
```

#### How configured values appear in findings

When a scanner has a custom configuration applied, violation descriptions and risk summaries reflect the configured values rather than the scanner defaults. For example, if `MIN_PASSWORD_LENGTH` is set to `14`, a violation will state that passwords must be at least 14 characters, not the scanner’s built-in default.

#### Prerequisites

- The `SNOWFLAKE.TRUST_CENTER_ADMIN` application role.

## Manage the violation findings lifecycle

Specific application roles allow you to view and manage violation findings by using the **Violations** tab. For more
information, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).

### View violations

To view and filter your violations data to see your current progress, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_VIEWER` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. To view the list of open, muted, or all violations, select an option from the **Status** drop-down menu.
6. To see a detailed pane with the violation’s summary, recommendations, and activity, select any violation.
7. In the violation bar, select **Activity** to see the comments history and the responsible users.
8. To see the scanner’s last run and when the violation was generated, select **Scanned**.
9. To see when the violation status was last changed, select **Updated**.

### Change the status of a violation finding

Attention

Marking a violation as `Muted` is a way to triage the open violation so you can focus on the ones most important for your environment.
Muting a violation also ceases the periodic email notifications for that violation. Scanners still run as scheduled irrespective of the
violation status: `Open` or `Muted`. The scanner continues to run and detect violations if the configuration remains unchanged.

All new security violations are raised with an `Open` status. You can mute a violation for multiple reasons, such as not being applicable
to your account, being deferred for a future date, being in progress already, or another reason.

You can change the status of a violation for any reason, such as not being applicable to your account, deferred for a future date, being in
progress already, or another reason. To change the status of a violation, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. Select a violation to open its detailed pane. By default, only violations with the **Open** status are shown.
6. Select the **Mute notification** button.
7. (Optional) To justify the resolution, add a comment.
8. Select **Submit**.

You can reopen a muted violation by selecting the **Unmute** button.

Note

Manually muting a violation finding isn’t mandatory for customers. The Trust Center automatically removes violation findings from the
**Violations** tab when a scanner run determines that any misconfiguration was corrected or remediation steps were
followed correctly.

## Remediate violation findings with one-click remediation

For supported violation findings, the Trust Center generates the SQL statements that resolve the violation finding, shows you the
plan, and runs it after you approve it. You review the exact statements before anything runs.

The statements run in your session under your current role. They are subject to the same access control as any other SQL you run, and
they appear in your query history. The Trust Center doesn’t change anything in your account on its own.

### Violation findings that support one-click remediation

One-click remediation is available for violation findings reported by the following CIS Benchmarks scanners:

| Scanner | SCANNER\_ID | What the remediation does |
| --- | --- | --- |
| Password length policy | `CIS_BENCHMARKS_CIS1_5` | Creates a password policy that requires at least 14 characters, then applies it to the account. |
| User inactivity | `CIS_BENCHMARKS_CIS1_8` | Disables each user that hasn’t signed in for 90 days. |
| Admin session timeout | `CIS_BENCHMARKS_CIS1_9` | Creates a session policy with a 15-minute idle timeout, then applies it to each affected administrator. |
| Privileged default role | `CIS_BENCHMARKS_CIS1_12` | Sets the default role to `PUBLIC` for each user whose default role is `ACCOUNTADMIN` or `SECURITYADMIN`. |
| Yearly rekeying | `CIS_BENCHMARKS_CIS4_1` | Sets `PERIODIC_DATA_REKEYING` to `TRUE` for the account. |
| Client encryption key size | `CIS_BENCHMARKS_CIS4_2` | Sets `CLIENT_ENCRYPTION_KEY_SIZE` to `256` for the account. |
| Data retention floor | `CIS_BENCHMARKS_CIS4_4` | Sets `MIN_DATA_RETENTION_TIME_IN_DAYS` to `7` for the account. |
| Storage integration for stage creation | `CIS_BENCHMARKS_CIS4_5` | Sets `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION` to `TRUE` for the account. |
| Storage integration for stage operations | `CIS_BENCHMARKS_CIS4_6` | Sets `REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION` to `TRUE` for the account. |
| Unload to inline URL | `CIS_BENCHMARKS_CIS4_8` | Sets `PREVENT_UNLOAD_TO_INLINE_URL` to `TRUE` for the account. |

Expand

Show lessSee more

Violation findings from other scanner packages, and from the remaining CIS Benchmarks scanners, don’t support one-click
remediation. For those violation findings, use CoCo or follow the instructions on the **Remediation** tab. For more information, see
[Remediate violation findings with CoCo](#label-trust-center-remediate-with-cortex-code).

Note

The remediations for `CIS_BENCHMARKS_CIS1_5` and `CIS_BENCHMARKS_CIS1_9` create a `TC_POLICIES` database with a `PUBLIC` schema inside
it to hold the policy they apply. If those objects already exist, the Trust Center uses them and leaves them unchanged.

### Remediate a violation finding with one-click remediation

To remediate a violation finding, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. Select a violation finding to open the findings detail panel, and select **Remediate Now**, or select the remediation icon in the
   list of violation findings.

   The Trust Center generates the remediation plan and opens the **Remediate violation** dialog.
6. Review the plan. The dialog shows the following information:

   - **Potential impact**: what the remediation changes in your account. If CoCo is available for your account,
     select **Explain** to open a CoCo chat that describes in more detail what the remediation does and how it
     affects your account, and answers follow-up questions about it.
   - **Violation**: the violation finding that the plan resolves.
   - **Affected entities**: the users that the remediation acts on. This appears only for remediations that act on individual users.
   - The SQL statements that the Trust Center runs on your behalf, in the order that they run.
7. Select **Execute plan**.

   The dialog reports **Violation remediated**, **Violation partially remediated**, or **Remediation failed**. If a statement fails,
   the dialog identifies the failing statement and its SQL error.
8. Wait for the next scheduled scanner run, or [run the scanner on demand](#label-trust-center-start-scanner-on-demand), to confirm
   that the root cause of the violation finding has been remediated.

   The Trust Center automatically removes the violation finding from the **Violations** tab after the scanner
   confirms the remediation. A remediated finding might appear as an open finding in Snowsight for up to 3 hours after the violation
   finding is remediated and the scanner is re-run.

### Considerations for one-click remediation

- Always review the SQL statements in the plan before you select **Execute plan**.
- If a statement fails, the Trust Center stops that step and doesn’t run the remaining steps in the plan. Statements that already ran
  successfully stay applied, and the result is reported as **Violation partially remediated**.
- If a violation finding was already remediated, generating a plan for it fails. The dialog reports that the violation finding is
  already remediated and offers only **Close**. A new plan becomes available only if a later scanner run reports the violation
  finding again.
- A remediation plan is generated for a specific scanner result. If the plan is no longer current, or if the violation finding
  changed after the plan was generated, select **Refresh plan** to generate a new plan.

## Remediate violation findings with CoCo

You can use CoCo to get AI-guided remediation for Trust Center violation findings directly in Snowsight. When you select
**Remediate with Coco** for a finding, CoCo opens a chat that explains the violation finding in the context of your account,
recommends remediation steps, and can execute remediation actions with your approval.

CoCo provides interactive, conversational remediation that is personalized to your account’s specific configuration. Unlike
the static remediation instructions on the **Remediation** tab, CoCo can tailor its guidance based on the entities and
configurations involved in the violation finding, answer follow-up questions, and generate SQL statements that you can review and run.

CoCo handles violation findings that don’t support one-click remediation. If a violation finding does support one-click remediation,
the remediation option opens the **Remediate violation** dialog instead. For more information, see
[Remediate violation findings with one-click remediation](#label-trust-center-remediate-violations-programmatically).

### Prerequisites

To use CoCo to remediate violation findings, the following conditions must be met:

- CoCo in Snowsight must be available for your account.
- Your role must have the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it. For more information about granting
  this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
- Your role must have the `SNOWFLAKE.CORTEX_USER` database role granted to it.

### Remediate a violation finding with CoCo

To remediate a violation finding, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting this role, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. Select a violation finding to open the findings detail panel, and select **Remediate with Coco**, or select the Cortex icon in the
   list of violation findings.

   CoCo opens in a chat panel on the right side of the screen. The chat is pre-populated with the context of the selected
   violation finding, including the violation type, severity, affected entities, and scanner details.
6. Review the explanation and remediation steps that CoCo provides. You can:

   - Ask follow-up questions to understand the violation finding in more detail.
   - Request alternative remediation approaches.
   - Ask CoCo to generate SQL statements for the remediation.
   - Review and run SQL statements directly from the chat.
7. After you complete the remediation, wait for the next scheduled scanner run or
   [run the scanner on demand](#label-trust-center-start-scanner-on-demand) to verify that the root cause of the violation finding
   has been remediated. The Trust Center automatically removes the violation finding from the **Violations** tab
   after the scanner confirms the remediation. A remediated finding might appear as an open finding in Snowsight for up to 3 hours
   after the violation finding is remediated and the scanner is re-run.

Note

AI-guided remediation is available for violation findings only. Detections represent unique events that occurred in the past and don’t
have direct remediation steps. However, you can use CoCo to investigate and plan a course of action for detection findings
as well.

### Considerations for CoCo

- CoCo generates remediation suggestions based on your account’s configuration and the details of the specific violation finding.
  Always review the suggested SQL statements before running them.
- Some violation findings require actions outside of Snowflake, such as coordinating an organization-wide MFA policy change or investigating
  whether a login from an unrecognized IP address is legitimate. In these cases, CoCo explains the required steps but cannot
  execute them on your behalf.
- After completing a remediation, you can verify the fix by running the scanner on demand rather than waiting for the next scheduled
  run. For more information, see [Run a scanner package on demand](#label-trust-center-start-scanner-package-on-demand).

## View Trust Center detection findings

The **Detections** tab displays information about the detection findings reported by the Trust Center and lets
you examine them:

Note

Currently, you can’t manage the lifecycle — that is, mute or reopen — a detection finding. Detection findings aren’t currently aggregated
into the Organization account.

### View detections

To view detections, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has either the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role or the `SNOWFLAKE.TRUST_CENTER_VIEWER`
   application role granted to it.

   For more information about granting these roles, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Detections** tab.

   A chart displays information about detections in the specified time period. You can adjust filters
   to modify the detections displayed on the tab. See the next step for information about modifying filters.

   The detections bar displays information about each detection, such as the detection type, entity type,
   entity name, and additional information.
5. To analyze the detections displayed on the tab, adjust the filters:

   - **Detection Type** - Clear the filter to show detections of any type, or select a type to show only detections of that type; for
     example, **Abnormal Account Activities**, **Insecure Login**, or **Privilege Escalation**.
   - **Severity** - Clear the filter to show detections of any severity, or select a severity to show only detections of that severity;
     for example, **Critical**, **High**, **Medium**, or **Low**.
   - **Entity Type** - Clear the filter to show detections for any entity type, or select an entity type to show only detections for that
     entity type; for example, **QUERY**, **ROLE**, or **USER**.
   - **Reported By** - Clear the filter to show detections reported by all scanners in the **Security Essentials** and **Threat Intelligence**
     scanner packages, or select a scanner package to only show detections reported by scanners in that scanner package.
   - **Time Range** - Clear the filter to show all detections that were reported at any time or select a time range to view detections
     reported in the selected time range.
6. To see a detailed pane with the detection’s summary, remediation recommendations, and activity, select any detection.

   To open a worksheet with queries that you can run to get more information on the scanner output,
   on the **Remediation** tab, select **Open a Worksheet**.

## Manage security risks

You can complete the following tasks to manage security risks in the Trust Center:

- [View security risks](#label-trust-center-view-security-risks).
- [Remediate security risks](#label-trust-center-mute-violations).

### View security risks

To view security risks, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role with the `SNOWFLAKE.TRUST_CENTER_VIEWER` or `SNOWFLAKE.TRUST_CENTER_ADMIN`
   application role granted to it.

   For more information about granting these roles, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. Select a recommendation from the list of violations to view details about the violation associated with the recommendation.
6. Optionally, select **Severity**, **Violations**, or **Search** to filter the list of recommendations shown.

### Remediate security risks

When [viewing individual security risks](#label-trust-center-view-security-risks), you can learn how to remediate the risks associated
with the recommendations that display, allowing you to harden the security of your account.

To remediate security risks, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. Switch to a role that has the `SNOWFLAKE.TRUST_CENTER_ADMIN` application role granted to it.

   For more information about granting these roles, see [Required roles](/user-guide/trust-center/overview#label-trust-center-requirements).
3. In the navigation menu, select **Governance & security** » **Trust Center**.
4. Select the **Violations** tab.
5. From the list of violations, select a recommendation.
6. In the **Remediation** tab, follow the steps that are shown.
