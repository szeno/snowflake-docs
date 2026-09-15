# Use the Trust Center to set up sensitive data classification

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Trust Center lets you set up [sensitive data classification](/user-guide/classify-intro) in the Snowsight user interface, so you
don’t have to write any SQL code. After it is set up, sensitive data classification automatically identifies which data in a database is sensitive and needs to be protected.

## Sensitive data classification recommendations in Snowsight

Note

This recommendation is rolling out in phases to all customers.

Snowflake is introducing recommendations on Snowsight (**Database details** and **Trust Center** pages) for databases that are likely to contain
sensitive data. Snowflake uses table metadata to assess databases and, when appropriate, shows a banner prompting you to enable classification.

Select the button on the banner to enable classification for that database in one step. Snowflake creates or updates a
[classification profile](/user-guide/classify-intro#label-classify-classification-profiles) for the database. After classification is enabled, open
**Governance & security** » **Trust Center** » **Data Security** to view the profile configuration and
[review classification results](#label-classify-trust-center-review-results).

## Get started

Note

The following steps apply only to the first user who accesses the **Data Security** tab in the Trust Center. If you aren’t the first
user and want to set up classification, see [Set up classification with advanced settings](#label-classify-trust-center-advanced).

To use a web interface to set up sensitive data classification, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select **Get started**.
5. In the **Set up auto-classification** dialog, do the following:

   1. Select the databases that you want to classify.
   2. Specify whether you want to auto-apply tags instead of just recommending them. For more information about tags and categories, see [Core concepts of sensitive data classification](/user-guide/classify-intro#label-classify-core-concepts).
6. Select **Enable**.
7. Select **Close**.

Based on this default setup, sensitive data classification has the following behavior:

- Reclassifies previously classified objects every 30 days.
- Scans data for all [native semantic categories](/user-guide/classify-native).
- Excludes views from classification.
- Bases classification on a sample of up to 10,000 randomly selected rows per table.

When the classification process is complete, you are ready to [view the results](/user-guide/classify-results).

## Set up classification with advanced settings

To set up sensitive data classification with advanced settings, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select **Settings**.
5. Do one of the following:

   - If you’re fine-tuning existing classification settings, find the classification profile that contains the settings and
     select [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **Edit**. If the first person to set up classification chose the default settings during
     setup, the profile is `Default Snowflake profile`.
   - If you are creating a new [classification profile](/user-guide/classify-intro#label-classify-classification-profiles) so different databases can be
     classified with different settings, select **Create New**.
6. Select the databases that you want to scan for sensitive data.

   If a database is greyed out, it’s associated with an existing
   classification profile and is already being classified. You’ll need to edit the existing classification profile to remove the database
   before you can classify it with the settings of a new profile.
7. Select **Next**.
8. If your account classifies sensitive data into [custom categories](/user-guide/classify-custom), select the ones that you want to use.
9. Select **Next**.
10. If you don’t want tags automatically applied to columns containing sensitive data, deselect **Auto-apply tags**.
11. If you want to apply a user-defined tag in addition to a system tag on matching columns, do the following:

    1. In the **Tag to apply** column, select the user-defined tag/value pair that you want applied to sensitive data.
    2. In the **Detected semantic categories** column, select values of the `SNOWFLAKE.CORE.SEMANTIC_CATEGORY` tag. These can be
       native and custom semantic categories.

    For example, if you select `PII = CONFIDENTIAL` as the user-defined tag/value pair in **Tag to apply**, and
    then select the `NAME` semantic category in **Detected semantic categories**, when Snowflake assigns the
    `SNOWFLAKE.CORE.SEMANTIC_CATEGORY = NAME` system tag to a column, it also applies the `PII = CONFIDENTIAL` tag.
12. Select **Next**.
13. Specify the database, schema, and name of the [classification profile](/user-guide/classify-intro#label-classify-classification-profiles) where all of your
    settings will be saved.
14. In the **AI Mode** section, optionally select **AI Mode** to improve the accuracy of classification using a large language model.

    Note

    Currently, AI mode only supports the OpenAI GPT-5 Mini model.
15. Select the cadence at which previously classified objects are re-classified.
16. Specify if you want to exclude certain objects from the classification process. For information about excluding specific objects, see [Excluding data from sensitive data classification](/user-guide/classify-auto-exclude).
17. Select **Enable**.

## Review classification results

Only tables that need a manual decision appear in the review workflow. If **Auto-apply tags** is enabled on the [classification profile](/user-guide/classify-intro#label-classify-classification-profiles), Snowflake applies system tags and any user-defined tags you configured, and those objects are marked as reviewed. If **Auto-apply tags** is not enabled, objects with recommended classifications and tags appear as needing review.

On the Trust Center **Data Security** tab, select the **Dashboard** tab. The **Objects that need review** tile shows how many tables still need you to accept or change recommendations. Open the review experience from that tile (or the equivalent control on the dashboard) to open the **Review classification** dialog. In the dialog you can:

- Use **Search tables** and the **Database** filter to find tables. Switch between the **Pending review** and **Selected** tabs to work through tables that need action or tables you have marked for batch updates.
- Select a table to inspect each column’s recommended **CLASSIFICATION CATEGORY**, **TAGS** (system and user-defined), and **SAMPLE VALUES** so you can confirm detections.
- Change recommended categories, add or adjust user-defined tags, and remove recommendations you do not want to apply.
- Select one or more tables, then select **Save and apply tags to selected tables** to apply your choices.

For high-level dashboard metrics, the full **Sensitive objects** list, and related tasks, see [Use the Trust Center to view classification results](/user-guide/classify-results#label-classify-trust-center-review).

## Classify additional databases

You can classify additional databases with the same classification settings by editing an existing classification profile. To edit a classification profile:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select **Settings**.
5. Find the classification profile in the list and select [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) » **Edit**. If the first person to set up classification used the default settings, the classification profile is `Default Snowflake profile`.
6. On the first page that appears, select the additional databases.
7. Complete the setup.

## Classification errors

When the classification process encounters errors for some objects, the Trust Center **Dashboard** tab shows a **Classification errors** tile with a count and warning indicator.

Select the **Classification errors** tile to open the **Classification errors** dialog. Use **Search objects** and the **Database** filter to narrow the list. The table lists each object, its database and schema, and the classification error message that explains why classification failed (for example, data format issues, restrictions on secure objects, or SQL compilation errors for views). Select **Close** when you are finished.

For SQL examples that query the event table and other troubleshooting guidance, see [Troubleshooting sensitive data classification](/user-guide/classify-troubleshooting).

## Sensitive Data Entitlement report

[Preview Feature](/release-notes/preview-features) — Open

Available to Enterprise Edition or higher.

The Sensitive Data Entitlement report lets you view who can access sensitive data in your account. The report generates a
view that includes a list of users who have an access control role that gives them privileges to tables that contain
sensitive data. It lists the table, the user, the role, and the privilege on the table.

### Enable the Sensitive Data Entitlement report

To enable the Sensitive Data Entitlement report, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select **Settings**.
5. In the **Reporting** section, locate **Sensitive Data Entitlement report** and select **Enable**.
6. In the **Enable sensitive data entitlement report** dialog, select a **Report Cadence** from the dropdown menu.
   Options include **Daily**, **Weekly**, **Monthly**, and **Quarterly**.
7. Select **Enable report**.

Note

Insights may take a couple of moments to populate after enabling the report.

After enabling the report, you can view the status, frequency, and last run time in the **Reporting** section of the
**Settings** tab. You can also select **Run now** to generate a report immediately, or select **Settings** to change
the report cadence.

### Entitlement report view

When an entitlement report runs, it stores its results in the `ENTITLEMENT_REPORT` view, which is located in the
`SNOWFLAKE.DATA_SECURITY` schema. The view displays one row for each privilege on a table containing sensitive data that
has been granted to a user or role.

The view contains the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| RUN\_ID | VARCHAR | UUID generated for each run of the entitlement report. |
| CREATED\_TIME | TIMESTAMP\_LTZ | Timestamp when the entitlement report was generated. |
| TABLE\_ID | NUMBER | System-generated ID of the table. |
| TABLE\_CATALOG | VARCHAR | Database that contains the table with sensitive data. |
| TABLE\_SCHEMA | VARCHAR | Fully qualified name of the schema containing the table. |
| TABLE\_NAME | VARCHAR | Fully qualified name of the table containing sensitive data. |
| USER\_ID | NUMBER | System-generated ID of the user. |
| USER\_NAME | VARCHAR | User who has privileges on the table. |
| ROLE\_ID | NUMBER | System-generated ID of the role. |
| ROLE\_NAME | VARCHAR | Name of the role that has privileges on the table. |
| PRIVILEGE | VARCHAR | Name of the access control privilege. |

Expand

Show lessSee more

### Access the Entitlement report

You can run queries against the `ENTITLEMENT_REPORT` view to learn who has access to tables with sensitive data and what
privileges are providing that access.

For example, to return a list of users who have access to sensitive data along with the privileges they have on each table,
run the following query:

Copy code

```
SELECT DISTINCT
   user_name,
   table_catalog,
   table_schema,
   table_name,
   privilege
FROM SNOWFLAKE.DATA_SECURITY.ENTITLEMENT_REPORT
ORDER BY user_name, table_catalog, table_schema, table_name, privilege;
```

If you want to get a list of the entitlement reports that have been generated, run the following query:

Copy code

```
SELECT DISTINCT run_id, created_time
FROM SNOWFLAKE.DATA_SECURITY.ENTITLEMENT_REPORT;
```

### Delete reports for a time range

To delete entitlement reports generated within a specific time range, call the `DELETE_REPORT_DATA` stored procedure. This
procedure allows you to remove report data that was generated after a specified start timestamp and before a specified end
timestamp.

You can use Snowflake functions like `TO_TIMESTAMP_LTZ` to specify the beginning and ending timestamps.

The following example deletes entitlement report data that was generated between January 1, 2025 and February 1, 2025:

Copy code

```
CALL SNOWFLAKE.DATA_SECURITY.DELETE_REPORT_DATA(
  'entitlement_report',
  TO_TIMESTAMP_LTZ('2025-01-01'),
  TO_TIMESTAMP_LTZ('2025-02-01')
);
```

## Sensitive Data Access report

[Preview Feature](/release-notes/preview-features) — Open

Available to Enterprise Edition or higher.

The Sensitive Data Access report shows which users accessed sensitive data in your account during a specified lookback period. The report
generates a view that lists each user-table-role combination identified in query and access history for tables that contain sensitive data. It
includes when access occurred, how often, and which row access and masking policies were in effect during the most recent query.

### What is sensitive data?

For this report, sensitive data is data in objects that meet all of the following criteria:

- The object was classified using [automatic sensitive data classification](/user-guide/classify-auto).
- Classification was performed by the Snowflake classifier or a custom classifier.
- At least one column is classified with a `PRIVACY_CATEGORY` tag value.

Only [classification-supported objects](/user-guide/classify-intro#supported-objects) are included in the report.

### Enable the Sensitive Data Access report

To enable the Sensitive Data Access report, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required privileges](#label-classify-trust-center-access-control).
2. In the navigation menu, select **Governance & security** » **Trust Center**.
3. Select the **Data Security** tab.
4. Select **Settings**.
5. In the **Reporting** section, locate **Sensitive Data Access report** and select **Enable**.
6. In the **Enable sensitive data access report** dialog, do the following:
   1. Select a **Report Cadence** from the dropdown menu. Options include **Daily**, **Weekly**, **Monthly**, and **Quarterly**.
   2. Select a **Lookback period** to specify how far back in query history each report run analyzes. Options include **1 day**, **7 days**, **30 days**, and **90 days**.
7. Select **Enable report**.

Note

Insights may take a couple of moments to populate after enabling the report. Longer lookback periods provide more comprehensive results but
require additional processing time.

After enabling the report, you can view the status, frequency, lookback period, and last run time in the **Reporting** section of the
**Settings** tab. You can also select **Run now** to generate a report immediately, or select **Settings** to change the report cadence or
lookback period.

### Access report view

When an access report runs, it stores its results in the `ACCESS_REPORT` view, which is located in the `SNOWFLAKE.DATA_SECURITY` schema.
The view displays one row for each user-table-role combination identified during the lookback window. This differs from the
[entitlement report](#label-classify-trust-center-entitlement-report), which provides one row for each privilege granted on a sensitive
table.

The view contains the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| RUN\_ID | VARCHAR | UUID generated for each run of the access report. |
| CREATED\_ON | TIMESTAMP\_LTZ | Timestamp when the access report was generated. |
| TABLE\_ID | NUMBER | System-generated ID of the table. |
| TABLE\_NAME | VARCHAR | Name of the table containing sensitive data. |
| TABLE\_DATABASE | VARCHAR | Database that contains the table with sensitive data. |
| TABLE\_SCHEMA | VARCHAR | Schema that contains the table with sensitive data. |
| USER\_NAME | VARCHAR | User who accessed the table. |
| ROLE\_NAME | VARCHAR | Primary role used when the table was accessed. |
| DIRECT\_ACCESS | BOOLEAN | Whether the table was accessed directly (`TRUE`) or indirectly (`FALSE`). |
| LAST\_ACCESS\_TIME | TIMESTAMP\_LTZ | Timestamp of the most recent query that accessed the table during the lookback window. |
| LAST\_QUERY\_ID | VARCHAR | ID of the most recent query that accessed the table during the lookback window. |
| LAST\_POLICIES\_REFERENCED | VARIANT | Row access and masking policies applied during the most recent query that accessed the table. |
| ACCESS\_COUNT | NUMBER | Number of distinct queries that accessed the table during the lookback window. |
| LAST\_QUERY\_TYPE | VARCHAR | Type of the most recent query that accessed the table (for example, `SELECT` or `INSERT`). |
| SECONDARY\_ROLE\_NAMES | VARIANT | Secondary roles active when the table was accessed. |

Expand

Show lessSee more

### Lookback period

Each report run analyzes query history within the lookback period configured for the report. You can set the lookback period when you
enable the report or change it later in report settings.

| Lookback period | Value (seconds) |
| --- | --- |
| 1 day | 86400 |
| 7 days | 604800 |
| 30 days | 2592000 |
| 90 days | 7776000 |

Expand

Show lessSee more

### Access the Sensitive Data Access report

You can run queries against the `ACCESS_REPORT` view to learn which users accessed tables with sensitive data during a report run.

For example, to return a list of users who accessed sensitive data along with how many times they accessed each table, run the following
query:

Copy code

```
SELECT DISTINCT
   user_name,
   table_database,
   table_schema,
   table_name,
   access_count
FROM SNOWFLAKE.DATA_SECURITY.ACCESS_REPORT
ORDER BY user_name, table_database, table_schema, table_name;
```

To preview recent report results, run the following query:

Copy code

```
SELECT
   table_database,
   table_schema,
   table_name,
   table_id,
   user_name,
   role_name,
   secondary_role_names,
   direct_access,
   last_access_time,
   last_query_id,
   last_query_type,
   access_count
FROM SNOWFLAKE.DATA_SECURITY.ACCESS_REPORT
LIMIT 100;
```

If you want to get a list of the access reports that have been generated, run the following query:

Copy code

```
SELECT DISTINCT run_id, created_on
FROM SNOWFLAKE.DATA_SECURITY.ACCESS_REPORT;
```

Note

`ACCESS_COUNT` reflects the number of distinct queries, not row-level access events.

### Delete reports for a time range

To delete access reports generated within a specific time range, call the `DELETE_REPORT_DATA` stored procedure. This procedure allows you
to remove report data that was generated after a specified start timestamp and before a specified end timestamp.

You can use Snowflake functions like `TO_TIMESTAMP_LTZ` to specify the beginning and ending timestamps.

The following example deletes access report data that was generated between January 1, 2025 and February 1, 2025:

Copy code

```
CALL SNOWFLAKE.DATA_SECURITY.DELETE_REPORT_DATA(
  'access_report',
  TO_TIMESTAMP_LTZ('2025-01-01'),
  TO_TIMESTAMP_LTZ('2025-02-01')
);
```

## Next steps

After sensitive data classification is set up and running, use the Trust Center **Data Security** tab to monitor outcomes:

- [Review classification results and apply tags](#label-classify-trust-center-review-results) using the **Dashboard** tab and **Objects that need review**.
- [Inspect classification errors](#label-classify-trust-center-classification-errors) using the **Classification errors** tile.
- For additional dashboards, the **Sensitive objects** list, and column detail, see [Use the Trust Center to view classification results](/user-guide/classify-results#label-classify-trust-center-review).
- [Generate a sensitive data entitlement report](#label-classify-trust-center-entitlement-report) to see who can access sensitive tables.
- [Generate a Sensitive Data Access report](#label-classify-trust-center-access-report) to see who has accessed sensitive tables.

## Access control requirements

Note

The `DATA_SECURITY_*` application roles alone are not sufficient to access the Trust Center **Data Security** tab. You must have the
SNOWFLAKE.TRUST\_CENTER\_VIEWER or SNOWFLAKE.TRUST\_CENTER\_ADMIN application role to use the Trust Center UI for classification. If your
account previously relied on `DATA_SECURITY_*` roles, update your role grants accordingly.

| Task | Required privileges/roles | Notes |
| --- | --- | --- |
| Set up classification for a database | One of the following:   - SNOWFLAKE.TRUST\_CENTER\_VIEWER application role - SNOWFLAKE.TRUST\_CENTER\_ADMIN application role |  |
|  | EXECUTE AUTO CLASSIFICATION privilege on ACCOUNT |  |
|  | APPLY TAG privilege on ACCOUNT |  |
|  | USAGE on the database | More powerful privileges on the database meet this requirement. |
| Review classification insights and classified objects | One of the following:   - SNOWFLAKE.TRUST\_CENTER\_VIEWER application role - SNOWFLAKE.TRUST\_CENTER\_ADMIN application role |  |
| Set up and generate an entitlement or access report | One of the following:   - SNOWFLAKE.DATA\_SECURITY\_ADMIN application role - ACCOUNTADMIN role | The DATA\_SECURITY\_ADMIN role provides the ability to enable sensitive data reporting, configure and generate reports, and access generated entitlement and access reports. |
| View an entitlement or access report | One of the following:   - SNOWFLAKE.DATA\_SECURITY\_VIEWER application role - SNOWFLAKE.DATA\_SECURITY\_ADMIN application role - ACCOUNTADMIN role | The DATA\_SECURITY\_VIEWER role provides read-only access to generated entitlement and access reports. |

Expand

Show lessSee more

**Example: Allow a user to set up classification**

To allow user `mary` to set up sensitive data classification and review classification findings, run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE trust_center_admin_role;

GRANT APPLICATION ROLE SNOWFLAKE.TRUST_CENTER_ADMIN TO ROLE trust_center_admin_role;
GRANT EXECUTE AUTO CLASSIFICATION ON ACCOUNT TO ROLE trust_center_admin_role;
GRANT APPLY TAG ON ACCOUNT TO ROLE trust_center_admin_role;
GRANT USAGE ON DATABASE mydb TO ROLE trust_center_admin_role;

GRANT ROLE trust_center_admin_role TO USER mary;
```

**Example: Allow user to review classification findings**

If you want user `joe` to be able to review classification findings, but not be able to set up classification, run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE trust_center_viewer_role;

GRANT APPLICATION ROLE SNOWFLAKE.TRUST_CENTER_VIEWER TO ROLE trust_center_viewer_role;

GRANT ROLE trust_center_viewer_role TO USER joe;
```

**Example: Allow user to view an entitlement or access report**

If you want user `alex` to be able to view an entitlement or access report, run the following commands:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE report_viewer;
GRANT APPLICATION ROLE SNOWFLAKE.DATA_SECURITY_VIEWER TO ROLE report_viewer;
GRANT ROLE report_viewer TO USER alex;
```
