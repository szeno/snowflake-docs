# Migrate from the legacy Openflow Connector for Jira Cloud

Jira Cloud flow availability

- **Generally available:** The Atlassian Jira Cloud (Core) flow.
- **[Public Preview](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/):** The Atlassian Jira Cloud (Agile) flow.

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and Google Cloud Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to migrate from the legacy Openflow Connector for Jira Cloud to the new Openflow Connector for Jira Cloud.

## Overview

The new connector is a complete rewrite that changes how data is stored in Snowflake.
It consists of two separate flows: a **core flow** (issues, projects, comments, changelogs,
worklogs, users, votes, watchers, remote links, issue security schemes, deleted issues, and lookup
tables for issue type, priority, resolution, and status) and an **agile flow** (boards, sprints,
board mappings).

The core flow and agile flow can write to the same Snowflake destination schema, since they
create tables with different names. The legacy connector and the new connector can run side by
side during migration — including on the same Openflow runtime — as long as they write to
**separate** destination schemas, so you can validate the new output before decommissioning
the legacy connector.

## Feature comparison

| Aspect | Legacy connector | New connector |
| --- | --- | --- |
| Entities | Issues only (with optional worklog enrichment). | Core flow: issues, projects, users, comments, changelogs, worklogs, votes, watchers, remote links, security schemes, permissions, project components, project versions, user groups, deleted issues, and lookup tables for issue type, priority, resolution, and status. Agile flow: boards, sprints, board-sprint, board-project, board-issue mappings. |
| Concurrency | Single-threaded. | Parallel per-project issue fetching, with optional multi-node distribution. |
| Schema strategy | Raw JSON in an `OBJECT` column with a dynamically generated flattened view. | Explicit column schemas per entity, evolved additively from the API responses. |
| Deletion tracking | Not supported. | Tracks deleted issues via Jira audit log polling (optional). |
| Agile data | Not supported. | Available through a separate agile flow. |

Expand

Show lessSee more

## Key differences

### Schema changes

The most significant difference is how data is stored in Snowflake:

| Aspect | Legacy connector | New connector |
| --- | --- | --- |
| Issues table | Single table with an `ISSUE` column containing the full raw JSON as an `OBJECT` type. A flattened `_VIEW` is auto-generated. | Explicit columns per field. Column names are derived from Jira field display names. No raw JSON fallback. |
| Other entities | Not available. Comments and worklogs are embedded in the issue JSON. | Separate tables: `BOARD`, `BOARD_ISSUE`, `BOARD_PROJECT`, `BOARD_SPRINT`, `CHANGELOG`, `COMMENT`, `DELETED_ISSUE`, `FIELD`, `ISSUE_REMOTE_LINK`, `ISSUE_SECURITY_SCHEME`, `ISSUE_TYPE`, `ISSUE_VOTE`, `ISSUE_WATCHER`, `PERMISSION`, `PRIORITY`, `PROJECT`, `PROJECT_COMPONENT`, `PROJECT_VERSION`, `RESOLUTION`, `SPRINT`, `STATUS`, `USER`, `USER_GROUP`, `WORKLOG`. See [Destination tables](/user-guide/data-integration/openflow/connectors/jira-cloud/about#label-jira-entities) for the full inventory. |
| Views | Auto-generated `<table>_VIEW` with all issue fields flattened. | No views created. Data is directly queryable from the destination tables. |

Expand

Show lessSee more

Any queries that reference the legacy `ISSUE` column (for example, `SELECT issue:fields:summary`) or the
auto-generated `_VIEW` must be rewritten to use the new column names directly (for example, `SELECT SUMMARY`).

### Parameter changes

The following parameters from the legacy connector are not available in the new connector:

| Legacy parameter | Current equivalent |
| --- | --- |
| Search Type | Removed. The new connector always fetches all issues from discovered projects. Use `Project Keys Filter` to limit ingestion to specific projects. |
| JQL Query | Removed. The new connector doesn’t support arbitrary JQL for issue filtering. Use `Project Keys Filter` instead. |
| Project Names | Replaced by `Project Keys Filter`, which accepts project keys (not names or IDs). |
| Status Category | Removed. The new connector fetches all issues regardless of status. |
| Updated After | Removed. The new connector manages incremental state automatically. |
| Created After | Removed. The new connector manages incremental state automatically. |
| Destination Table | Removed. The new connector creates fixed table names per entity (`ISSUE`, `PROJECT`, `COMMENT`, and others) in the configured destination schema. |
| Fetch All Worklogs | Removed. The new connector fetches all worklogs into a separate `WORKLOG` table by default when `WORKLOG` is listed in `Enabled Tables`. |
| Connection Method | Not exposed as a parameter. The new connector uses the `DIRECT` connection method. |

Expand

Show lessSee more

The following parameters are introduced in the new connector:

| Parameter | Description |
| --- | --- |
| Deletes Fetch Strategy | Enables tracking of deleted issues via the Jira audit log. Not available in the legacy connector. |
| Merge Interval | Time interval between journal-to-destination merge operations. Available in both the core flow and the agile flow. |

Expand

Show lessSee more

Additionally, agile data (boards, sprints, and board mappings) is now available through a separate
agile flow rather than a parameter toggle. See [Set up the Atlassian Jira Cloud (Agile) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile) for details on installing and configuring
the agile flow.

### API token scopes

If you’re using API tokens with scopes, the new connector may require additional scopes
depending on the features you enable. See [Required API scopes](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core#label-jira-core-api-scopes) for the core flow scopes and [Required API scopes](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile#label-jira-agile-api-scopes) for the agile flow scopes.

### Snowflake privileges

The new connector requires only `CREATE TABLE` on the destination schema. The legacy
connector additionally required `CREATE VIEW` to create flattened issue views. The new
connector doesn’t create views, so the `CREATE VIEW` privilege is no longer needed. If you’re
reusing an existing role, you can revoke `CREATE VIEW` after the legacy connector is
decommissioned.

## Migration steps

1. **Set up the new connector.** Install the core flow on the same
   or a different Openflow runtime. If you need agile data, also install the agile flow.
   Configure both flows to write to a **different destination schema** than the one used by the legacy
   connector. This allows the legacy and new connectors to run simultaneously.
2. **Map your legacy configuration to the new parameters.**

   - Copy the `Jira Email`, `Jira API Token`, and `Environment URL` values from the legacy connector
     to the new core flow. If using the agile flow, configure these values separately for that flow as well.
   - If the legacy connector uses `Project Names`, convert them to project keys for the
     `Project Keys Filter` parameter.
   - If the legacy connector uses a `JQL Query`, evaluate whether `Project Keys Filter` covers your
     use case. If your JQL filters by criteria other than project (for example, status or custom fields),
     those filters aren’t available in the new connector. All matching issues from the configured
     projects are ingested.
   - Set `Issue Fields` to match your previous configuration. The default changed from `*all` (legacy)
     to `*standard`.
   - Configure the Snowflake destination parameters (database, schema, warehouse, credentials) for each flow.
3. **Start the new connector.** Run the core flow and allow the initial load to complete.
   If using the agile flow, start it as well.
4. **Validate the data.** Compare the data in the new destination tables against the legacy destination
   table to check for completeness. Expect some differences: the legacy connector didn’t track deletes,
   so issues that were deleted in Jira still appear in the legacy table but not in the new `ISSUE`
   table (or they appear with `_SNOWFLAKE_DELETED = TRUE` if delete tracking is enabled). Row counts
   will not match exactly when any issues have been deleted.

   Copy code

   ```
   -- Compare issue counts (expect differences if issues were deleted in Jira)
   SELECT COUNT(*) AS legacy_count FROM legacy_schema.JIRA_ISSUES;
   SELECT COUNT(*) AS new_count FROM new_schema.ISSUE;

   -- Spot-check specific issues. ISSUE_TYPE, PRIORITY, RESOLUTION, and STATUS
   -- are Jira IDs; join the lookup tables to resolve names.
   SELECT i.KEY, i.SUMMARY, s.NAME AS status_name
   FROM new_schema.ISSUE i
   LEFT JOIN new_schema.STATUS s ON i.STATUS = s.ID
   WHERE i.KEY = 'PROJ-123';
   ```
5. **Update downstream queries.** Rewrite any queries, views, dashboards, or pipelines that reference
   the legacy table structure. Key changes:

   - Replace references to the legacy `ISSUE` `OBJECT` column or `_VIEW` with direct column references.
   - Replace `FLATTEN`-based queries with standard `SELECT` statements.
   - Add `JOIN` statements to combine data across the new entity tables (for example, join `ISSUE`
     with `COMMENT` on `ISSUE_ID`, or join `ISSUE` to `STATUS` on `ISSUE.STATUS = STATUS.ID` to
     resolve status names).
   - If you want queries to ignore deleted issues, filter on the new `_SNOWFLAKE_DELETED` column
     (`WHERE _SNOWFLAKE_DELETED = FALSE`). The legacy connector didn’t track deletes at all, so
     legacy queries against `JIRA_ISSUES` returned issues that had since been removed in Jira.
6. **Stop the legacy connector.** Once you’ve confirmed that the new data is complete and downstream
   consumers have been updated, stop the legacy connector process group. Both new flows (core and agile)
   can continue running independently.
7. **Clean up.** Optionally, drop the legacy destination table and view after confirming they’re no
   longer needed.

Note

When the legacy connector and the new connector use the same Jira API token, they share the
same Jira API rate limits. Running both simultaneously roughly doubles the API call volume, which
may cause rate limiting on Jira instances with heavy API usage. Consider reducing the legacy
ingestion frequency during the migration period, or run the new connector with a separate
API token whose rate budget you can manage independently.
