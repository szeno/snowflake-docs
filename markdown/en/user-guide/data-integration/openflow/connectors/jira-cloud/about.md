# About Openflow Connector for Jira Cloud

Jira Cloud flow availability

- **Generally available:** The Atlassian Jira Cloud (Core) flow.
- **[Public Preview](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/):** The Atlassian Jira Cloud (Agile) flow.

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and Google Cloud Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts of Openflow Connector for Jira Cloud, its workflow, and limitations.

The Openflow Connector for Jira Cloud ingests data from multiple Atlassian Jira Cloud entities into Snowflake.
It consists of two separate flows:

- **Core flow** — uses the [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#about)
  to retrieve issues, projects, comments, changelogs, worklogs, users, deleted issues,
  votes, watchers, remote links, issue security schemes, and lookup tables for
  issue type, priority, resolution, and status.
- **Agile flow** — uses the [Jira Agile REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro/#about)
  to retrieve boards, sprints, board-sprint mappings, board-project mappings, and board-issue mappings.

Both flows store data in dedicated Snowflake tables with explicit column schemas. The two flows
can write to the same Snowflake destination schema, since they create tables with different names.

Use this connector if you’re looking to do the following:

- Centralize Jira data in Snowflake for cross-team visibility and deeper insights into engineering,
  support, and project workflows
- Ingest a broad set of Jira entities into separate, query-ready Snowflake tables, with a
  selectable subset of optional tables
- Extract Jira issues with per-project parallel ingestion for faster data loads
- Track deleted issues via Jira audit log polling
- Optionally ingest Jira Agile data using the separate agile flow

Note

If you previously deployed an earlier version of the Jira Cloud connector, see
[Migrate from the legacy Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/migrate-from-legacy) for a step-by-step migration guide.

## Destination tables

The connector creates the following tables in the configured Snowflake destination schema.
Most tables have a fixed column schema defined by the connector. The `ISSUE` table is the
exception: its columns are driven by the `Issue Fields` configuration and may include custom
fields from your Jira instance. See [Issue fields configuration](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core#label-jira-core-issue-fields) for details.

### Core flow tables

The `ISSUE`, `PROJECT`, `USER`, and `FIELD` tables are always created. The remaining
tables are created only when the corresponding table name is listed in the `Enabled Tables`
parameter (or, for `DELETED_ISSUE`, when delete tracking is enabled). See
[Jira Cloud (Core) Ingestion Parameters](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core#label-jira-core-ingestion-parameters) for details.

| Table | Enabled by | Contents |
| --- | --- | --- |
| ISSUE | Always | One row per Jira issue. The set of columns is driven by the `Issue Fields` configuration and may include custom fields. Fields such as issue type, priority, resolution, and status are stored as Jira IDs. Join to the following lookup tables to resolve names. |
| PROJECT | Always | One row per Jira project visible to the API token owner. |
| USER | Always | Jira users encountered during ingestion. |
| FIELD | Always | Metadata for Jira issue fields used to drive the dynamic `ISSUE` schema. |
| CHANGELOG | `CHANGELOG` | Issue field change history, one row per changelog entry. |
| COMMENT | `COMMENT` | Comments attached to issues, one row per comment. |
| ISSUE\_REMOTE\_LINK | `ISSUE_REMOTE_LINK` | Remote links attached to issues. |
| ISSUE\_SECURITY\_SCHEME | `ISSUE_SECURITY_SCHEME` | Issue-level security schemes and levels defined in the Jira instance. |
| ISSUE\_TYPE | `ISSUE_TYPE` | Issue type names and hierarchy. Join to `ISSUE` on `ISSUE.ISSUE_TYPE = ISSUE_TYPE.ID`. |
| ISSUE\_VOTE | `ISSUE_VOTE` | Per-issue vote records. |
| ISSUE\_WATCHER | `ISSUE_WATCHER` | Per-issue watcher records. |
| PERMISSION | `PERMISSION` | Global and project permission definitions. |
| PRIORITY | `PRIORITY` | Priority names. Join to `ISSUE` on `ISSUE.PRIORITY = PRIORITY.ID`. |
| PROJECT\_COMPONENT | `PROJECT_COMPONENT` | Components defined in each project. |
| PROJECT\_VERSION | `PROJECT_VERSION` | Release versions defined in each project. |
| RESOLUTION | `RESOLUTION` | Resolution names. Join to `ISSUE` on `ISSUE.RESOLUTION = RESOLUTION.ID`. |
| STATUS | `STATUS` | Status names and categories. Join to `ISSUE` on `ISSUE.STATUS = STATUS.ID`. |
| USER\_GROUP | `USER_GROUP` | Group memberships per user. |
| WORKLOG | `WORKLOG` | Time tracking entries on issues. |
| DELETED\_ISSUE | `Deletes Fetch Strategy = AUDIT` | Issues deleted from Jira, tracked via audit log. |

Expand

Show lessSee more

### Agile flow tables

The following tables are created by the agile flow. To populate these tables, install and run the agile
flow separately from the core flow. The `BOARD` table is always created. The remaining tables
are gated by the agile flow’s own `Enabled Tables` parameter.

| Table | Enabled by | Contents |
| --- | --- | --- |
| BOARD | Always | Agile boards visible to the API token owner. |
| SPRINT | `SPRINT` | Sprints across all ingested boards. |
| BOARD\_SPRINT | `SPRINT` | Board-to-sprint mappings. |
| BOARD\_PROJECT | `BOARD_PROJECT` | Board-to-project mappings. |
| BOARD\_ISSUE | `BOARD_ISSUE` | Board-to-issue mappings. |

Expand

Show lessSee more

### Connector-managed columns

In addition to the columns derived from the Jira API response, the connector adds the following
metadata columns. `_SNOWFLAKE_INSERTED_AT` and `_SNOWFLAKE_UPDATED_AT` are added to every
destination table. `_SNOWFLAKE_DELETED` is added only to tables that track soft deletes. To
see which tables have it, inspect the destination tables in Snowflake.

| Column | Type | Purpose |
| --- | --- | --- |
| `_SNOWFLAKE_INSERTED_AT` | `TIMESTAMP_NTZ` | When the row was first inserted by the connector. |
| `_SNOWFLAKE_UPDATED_AT` | `TIMESTAMP_NTZ` | When the row was last updated by the connector. |
| `_SNOWFLAKE_DELETED` | `BOOLEAN` | `TRUE` when the source record is no longer present in the corresponding Jira API response (for example, an issue deleted in Jira, or a comment removed from an issue). The row remains in the destination table. Filter on `_SNOWFLAKE_DELETED = FALSE` to exclude soft-deleted records. |

Expand

Show lessSee more

## Workflow

1. A **Jira Cloud administrator** performs the following tasks:

   1. Generates an API token within the Jira instance. This token is used by the connector for authentication.
      Both tokens with scopes and tokens without scopes are supported,
      although tokens with scopes are recommended for fine-grained access control.
      The required scopes depend on which features are enabled. See [Required API scopes](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core#label-jira-core-api-scopes) for details.
   2. Optionally, if delete tracking is required, ensures the API token owner has the **Administer Jira**
      global permission for access to the audit log endpoint.
2. A **Snowflake account administrator** performs the following tasks:

   1. Installs the core flow, the agile flow, or both, depending on which entities are needed.
   2. Configures each flow:

      1. Provides the Jira API token and email address.
      2. Specifies the Jira instance URL.
      3. For the core flow, optionally filters ingestion to specific projects using `Project Keys Filter`
         and configures the issue fields to ingest.
      4. Sets the database and schema names in the Snowflake account.
   3. Runs the flow in the Openflow canvas. Upon execution:

      - The **core flow** discovers projects and registers them in the ingestion state service,
        fetches issues in parallel across projects along with the per-issue tables listed in
        `Enabled Tables` (and optionally deleted issues), and fetches worklogs, users, user groups,
        permissions, project components, project versions, issue security schemes, and the `ISSUE_TYPE`,
        `PRIORITY`, `RESOLUTION`, and `STATUS` lookup tables on independent schedules.
      - The **agile flow** fetches boards, sprints, board-project mappings, board-sprint mappings,
        and board-issue mappings.
3. **Snowflake business users** can then query the destination tables directly with standard SQL,
   without needing to flatten JSON.

## Openflow requirements

- The minimum runtime size is `Small`. When you have many tables listed in
  `Enabled Tables`, more processors run concurrently and the default Small runtime thread budget
  may become a bottleneck. In that case, move to a `Medium` runtime (or larger).
- The connector supports multi-node Openflow runtimes. Each flow’s state service is cluster-aware,
  and the flow connections use load balancing where appropriate so that work is distributed across
  available nodes. If you want to run on multiple nodes, configure a static cluster size by setting
  **Min nodes** to the target node count rather than relying on autoscaling. The connector doesn’t
  generate enough sustained load on the runtime to trigger the runtime to scale up additional nodes
  on its own.
- For Jira instances with many projects, a multi-node runtime is recommended. Per-project work is
  distributed across nodes, so adding nodes increases the number of projects the connector processes
  in parallel. Use the project count as a rough guide when sizing **Min nodes**.
- The connector is primarily limited by Jira API rate limits rather than runtime compute capacity.
  Increasing the runtime size beyond `Medium`, or adding more nodes than the API rate budget can
  sustain, is unlikely to improve ingestion speed.
- The core flow and agile flow can run on the same or separate Openflow runtimes. If you run both
  flows on the same runtime, `Small` isn’t sufficient — use at least `Medium` (or larger,
  depending on the load).

## Limitations

- Basic authentication using an email and API token is the only supported authorization method.
  The connector can only ingest data accessible to the owner of the API token.
- Delete tracking via the `AUDIT` strategy requires the API token owner to have the **Administer Jira**
  global permission. The Jira audit log has limited retention (typically 6 months for Jira Premium,
  less for Free or Standard plans). If the connector is paused for longer than the retention period,
  delete events can be missed.
- Schema evolution for the `ISSUE` table is additive only. New columns can be added, but column type changes
  or removals aren’t supported. If a Jira custom field type changes, the connector may require redeployment.
- The `ISSUE` table schema is dynamic and depends on the `Issue Fields` configuration. Fields not included
  in the resolved field set aren’t loaded, and there is no raw JSON fallback. Issue type, priority,
  resolution, and status are stored as Jira IDs. Enable the `ISSUE_TYPE`, `PRIORITY`, `RESOLUTION`, and
  `STATUS` lookup tables (they’re in the default `Enabled Tables` value) and join them to resolve names.
- Narrowing `Project Keys Filter` to remove a project doesn’t delete that project’s rows from the
  destination tables. Rows that were previously ingested remain in place and are no longer updated.
  To remove orphaned rows after a filter change, manually delete them from the destination tables.
- Agile data (boards, sprints, board mappings) is fully re-fetched on every scheduled run of the agile flow.
  For Jira instances with many boards, this may result in increased API usage.
- Each connector instance can be associated with only one Jira Cloud site.

## Next steps

- [Set up the Atlassian Jira Cloud (Core) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core) to install the core flow.
- [Set up the Atlassian Jira Cloud (Agile) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile) to install the agile flow.
- [Migrate from the legacy Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/migrate-from-legacy) if you’re moving from a previous version of the Jira Cloud connector.
