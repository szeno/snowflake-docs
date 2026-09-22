# Set up the Atlassian Jira Cloud (Core) flow

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to install and configure the Atlassian Jira Cloud (Core) flow, the core flow
of the Openflow Connector for Jira Cloud. The agile flow is documented separately in [Set up the Atlassian Jira Cloud (Agile) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile).

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Jira Cloud](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-jira-cloud) connector.

## Get the credentials

As a Jira Cloud administrator, perform the following tasks in your Atlassian account:

1. Navigate to the [API tokens page](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Select **Create API token with scopes**.
3. In the **Create an API token** dialog box, provide a descriptive name for the API token and
   select an expiration date for the API token. This can range from 1 to 365 days.
4. Select the API token app **Jira**.
5. Select the required scopes based on the features you plan to use. See
   [Required API scopes](#label-jira-core-api-scopes) for details.
6. Select **Create token**.
7. In the **Copy your API token** dialog box, select **Copy** to copy your generated API
   token and then paste the token to the connector parameters, or save it securely.
8. Select **Close** to close the dialog box.

### Required API scopes

Atlassian API tokens with scopes list both **classic** (broader, recommended) and **granular**
(narrower) scopes. Classic scopes are the recommended starting set. Use granular scopes when your
organization requires a narrower token; a granular token needs every scope Atlassian lists for an
endpoint, not just one.

The core flow always requires these classic baseline scopes (or the equivalent granular set for
each table you enable):

- `read:jira-work`
- `read:jira-user` (covers users and user groups, and the connection verification and timezone
  lookup that run at startup against [`GET /rest/api/3/myself`](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-myself/#api-rest-api-3-myself-get))

The API token owner additionally needs the **Browse projects** Jira permission on every project
that you want to ingest.

For the `Enabled Tables` parameter that turns optional tables on, see [Enabled tables configuration](#label-jira-core-enabled-tables).

The following table lists each destination table, the recommended classic scope, the full set of
granular scopes Atlassian documents for the endpoints, and links to the endpoints the connector
calls:

| Table | Classic scope (recommended) | Granular scopes | Jira API reference | Additional Jira permission |
| --- | --- | --- | --- | --- |
| `ISSUE` (always) | `read:jira-work` | `read:issue-details:jira`, `read:field.default-value:jira`, `read:field.option:jira`, `read:field:jira`, `read:group:jira`, `read:jql:jira`, `validate:jql:jira` | [Parse JQL query](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-jql/#api-rest-api-3-jql-parse-post) and [Search for issues using JQL](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-post) | **Browse projects** on the relevant projects. |
| `PROJECT` (always) | `read:jira-work` | `read:issue-type:jira`, `read:project:jira`, `read:project.property:jira`, `read:user:jira`, `read:application-role:jira`, `read:avatar:jira`, `read:group:jira`, `read:issue-type-hierarchy:jira`, `read:project-category:jira`, `read:project-version:jira`, `read:project.component:jira` | [Get projects paginated](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-search-get) | **Browse projects** on the relevant projects. |
| `USER` (always) | `read:jira-user` | `read:user:jira`, `read:application-role:jira`, `read:avatar:jira`, `read:group:jira` | [Get all users (default)](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-users-get) | **Browse users and groups** (global). |
| `FIELD` (always) | `read:jira-work` | `read:field:jira`, `read:avatar:jira`, `read:project-category:jira`, `read:project:jira`, `read:field-configuration:jira` | [Get fields](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/#api-rest-api-3-field-get) | None. |
| `CHANGELOG` | `read:jira-work` | `read:issue-meta:jira`, `read:avatar:jira`, `read:issue.changelog:jira` | [Bulk fetch changelogs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-changelog-bulkfetch-post) | **Browse projects** on the relevant projects. |
| `COMMENT` | `read:jira-work` | `read:comment:jira`, `read:comment.property:jira`, `read:group:jira`, `read:project:jira`, `read:project-role:jira`, `read:user:jira`, `read:avatar:jira` | [Get comments](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-comments/#api-rest-api-3-issue-issueidorkey-comment-get) | **Browse projects** on the relevant projects. |
| `ISSUE_REMOTE_LINK` | `read:jira-work` | `read:issue.remote-link:jira`, `read:status:jira` | [Get remote issue links](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-remote-links/#api-rest-api-3-issue-issueidorkey-remotelink-get) | **Browse projects** on the relevant projects. |
| `ISSUE_SECURITY_SCHEME` | `manage:jira-project` | `read:issue-security-level:jira`, `read:issue-security-scheme:jira` | [Get issue security schemes](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-security-schemes/#api-rest-api-3-issuesecurityschemes-get) | **Administer Jira** (global). |
| `ISSUE_TYPE` | `read:jira-work` | `read:issue-type:jira`, `read:avatar:jira`, `read:project-category:jira`, `read:project:jira` | [Get all issue types for user](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-get) | None. |
| `ISSUE_VOTE` | `read:jira-work` | `read:issue.vote:jira`, `read:user:jira`, `read:application-role:jira`, `read:avatar:jira`, `read:group:jira` | [Get votes](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-votes/#api-rest-api-3-issue-issueidorkey-votes-get) | **Browse projects** on the relevant projects. **View voters and watchers** is also required to return voter details. |
| `ISSUE_WATCHER` | `read:jira-work` | `read:issue.watcher:jira`, `read:user:jira`, `read:avatar:jira` | [Get issue watchers](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-watchers/#api-rest-api-3-issue-issueidorkey-watchers-get) | **Browse projects** on the relevant projects. **View voters and watchers** is also required to return details for watchers other than the API token owner. |
| `PERMISSION` | `manage:jira-configuration` | `read:permission:jira` | [Get all permissions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/#api-rest-api-3-permissions-get) | None. |
| `PRIORITY` | `manage:jira-configuration` | None. | [Search priorities](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-priorities/#api-rest-api-3-priority-search-get) | None. |
| `PROJECT_COMPONENT` | `read:jira-work` | `read:project:jira`, `read:project.component:jira`, `read:user:jira`, `read:application-role:jira`, `read:avatar:jira`, `read:group:jira` | [Get project components paginated](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-components/#api-rest-api-3-project-projectidorkey-component-get) | **Browse projects** on the relevant projects. |
| `PROJECT_VERSION` | `read:jira-work` | `read:project-version:jira` | [Get project versions paginated](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/#api-rest-api-3-project-projectidorkey-version-get) | **Browse projects** on the relevant projects. |
| `RESOLUTION` | `read:jira-work` | `read:resolution:jira` | [Search resolutions](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-resolutions/#api-rest-api-3-resolution-search-get) | None. |
| `STATUS` | `manage:jira-configuration` | `read:workflow:jira` | [Search statuses paginated](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-status/#api-rest-api-3-statuses-search-get) | **Administer projects** on the relevant projects or **Administer Jira** (global). |
| `USER_GROUP` | `read:jira-user` | `read:group:jira` | [Get user groups](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-groups-get) | **Browse users and groups** (global). |
| `WORKLOG` | `read:jira-work` | `read:comment:jira`, `read:group:jira`, `read:issue-worklog:jira`, `read:issue-worklog.property:jira`, `read:project-role:jira`, `read:user:jira`, `read:avatar:jira` | [Get IDs of updated worklogs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-worklog-updated-get) and [Get worklogs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-worklog-list-post) | None. Restricted worklogs are returned only when the API token owner belongs to the permitted project role or group. |
| `DELETED_ISSUE` (`Deletes Fetch Strategy = AUDIT`) | `manage:jira-configuration` | `read:audit-log:jira`, `read:user:jira` | [Get audit records](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-audit-records/#api-rest-api-3-auditing-record-get) | **Administer Jira** (global). Audit logs are available only when at least one Jira product is on a paid plan. |

Expand

Show lessSee more

For the `ISSUE`, `CHANGELOG`, `COMMENT`, `ISSUE_REMOTE_LINK`, `ISSUE_VOTE`, and `ISSUE_WATCHER`
tables, the API token owner must also have permission to view an issue when issue-level security is
configured for the issue.

Comments restricted to specific roles or groups are visible only when the API token owner is a member
of these roles or groups, regardless of the token scope or permission configuration.

The `ISSUE_REMOTE_LINK` table requires issue linking to be active in Jira. The `ISSUE_VOTE` and
`ISSUE_WATCHER` tables require the Jira settings that allow users to vote on and watch issues,
respectively.

Tokens without scopes are also supported and grant access based solely on the API token owner’s
permissions. However, tokens with scopes are recommended for fine-grained access control.

## Set up Snowflake account

As an Openflow administrator, perform the following tasks to set up your Snowflake account. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant it the following privileges.

### Create database, schema, and warehouse

1. Create the destination database:

   Copy code

   ```
   USE ROLE OPENFLOW_ADMIN;
   CREATE DATABASE IF NOT EXISTS <destination_database>;
   ```
2. Create the destination schema:

   Copy code

   ```
   CREATE SCHEMA IF NOT EXISTS <destination_database>.<destination_schema>;
   ```
3. Grant the required privileges to the runtime’s execute-as role:

   Copy code

   ```
   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE TABLE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
4. Create a warehouse (or use an existing one) and grant usage privileges:

   Copy code

   ```
   CREATE WAREHOUSE IF NOT EXISTS <openflow_warehouse>
     WITH
     WAREHOUSE_SIZE = 'XSMALL'
     AUTO_SUSPEND = 300
     AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
5. If any other Snowflake users require access to the tables ingested by the
   connector (for example, for custom processing in Snowflake), grant those users the execute-as
   role.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Set up the connector

The core flow is shipped as the Atlassian Jira Cloud (Core) process group. As a data engineer, perform the
following tasks to install and configure it.

### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

After import, the core flow appears on the canvas as the Atlassian Jira Cloud (Core) process group.

### Configure the connector

1. Right-click on the imported Atlassian Jira Cloud (Core) process group and select **Parameters**.
2. Populate the required parameter values as described in
   [Flow parameters](#label-jira-core-flow-parameters).

### Flow parameters

The core flow uses the following parameter contexts:

- [Jira Cloud (Core) Source Parameters](#label-jira-core-source-parameters): Used to establish connection with the Jira API.
- [Jira Cloud (Core) Destination Parameters](#label-jira-core-destination-parameters): Used to establish connection with Snowflake.
- [Jira Cloud (Core) Ingestion Parameters](#label-jira-core-ingestion-parameters): Used to define the configuration of data ingested from Jira.

#### Jira Cloud (Core) Source Parameters

| Parameter | Description |
| --- | --- |
| Jira Email | Email address for the Atlassian account used for authentication. |
| Jira API Token | API access token for your Atlassian Jira account. See [Required API scopes](#label-jira-core-api-scopes) for the scopes to configure. |
| Environment URL | URL to the Atlassian Jira environment. For example, `https://your-domain.atlassian.net`. |

Expand

Show lessSee more

#### Jira Cloud (Core) Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  - `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME` - `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Must be the RSA private key used for authentication, formatted according to PKCS8   standards and including standard PEM headers and footers. Note that either a Snowflake Private   Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake private key file. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### Jira Cloud (Core) Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Enabled Tables | Comma-separated list of optional tables to populate. See [Enabled tables configuration](#label-jira-core-enabled-tables) for the full list of values and guidance on which tables to enable. Default value: `CHANGELOG, COMMENT, ISSUE_TYPE, PRIORITY, RESOLUTION, STATUS, WORKLOG`. |
| Issue Fields | A list of fields to return for each issue, used to retrieve a subset of fields. See [Issue fields configuration](#label-jira-core-issue-fields) for available values and custom field handling. Default value: `*standard`. |
| Project Keys Filter | Optional comma-separated list of Jira project keys to limit ingestion to specific projects. If empty, all projects accessible by the API token owner are fetched. For example, `PROJ1, PROJ2`. |
| Deletes Fetch Strategy | Strategy for fetching deleted issues. Set to `NONE` to skip delete tracking, or `AUDIT` to fetch deleted issues from the Jira audit log endpoint. The `AUDIT` strategy requires the API token owner to have the **Administer Jira** global permission and the `manage:jira-configuration` scope. Default value: `NONE`. |
| Merge Interval | Time interval between journal-to-destination merge operations. When a merge runs, the Snowflake warehouse resumes. The merge is skipped if no new data has been loaded since the previous merge. Default value: `1 min`. |

Expand

Show lessSee more

## Run the flow

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the Atlassian Jira Cloud (Core) process group and select **Start**. The flow starts the data ingestion.

On first run, the flow creates the required Snowflake tables in the destination schema. See
[Destination tables](/user-guide/data-integration/openflow/connectors/jira-cloud/about#label-jira-entities) for the full list of tables created by the core flow and the parameters
that control which optional tables are populated.

## Resetting the connector state

If you need to change the project filter or want to restart the ingestion from scratch, you must
clear the ingestion state. The core flow uses a centralized state service rather than per-processor state.

To reset the state, perform the following steps:

1. Right-click the Atlassian Jira Cloud (Core) process group and select **Stop**.
2. Navigate to the **Controller Settings** for the process group.
3. Find the **StandardJiraIngestionStateService** controller service and select **View State**.
4. Select **Clear State**. This clears all project tracking, pagination, and timestamp state.
5. Optionally, update the connector parameters if needed.
6. Right-click the Atlassian Jira Cloud (Core) process group and select **Start**.

Note

Clearing the ingestion state causes the connector to re-fetch all data from the beginning. The
destination tables are not truncated. Existing rows are updated in place, and rows that no
longer exist in Jira are flagged with `_SNOWFLAKE_DELETED = TRUE`.

## Accessing the data

Data fetched from Jira is available in the destination tables with explicit column schemas. There is
no need to use JSON flattening or views to query the data.

Each entity is stored in its own table. For example, to query issues and their comments:

Copy code

```
SELECT i.KEY, i.SUMMARY, c.BODY AS comment_body, c.CREATED AS comment_created
FROM ISSUE i
JOIN COMMENT c ON i.ID = c.ISSUE_ID
ORDER BY c.CREATED DESC;
```

The `ISSUE` table stores Jira IDs for issue type, priority, resolution, and status, not the
display names. Enable the matching lookup tables (they’re in the default `Enabled Tables`
value) and join them to resolve names:

Copy code

```
SELECT
  i.KEY,
  i.SUMMARY,
  it.NAME AS issue_type_name,
  p.NAME AS priority_name,
  r.NAME AS resolution_name,
  s.NAME AS status_name
FROM ISSUE i
LEFT JOIN ISSUE_TYPE it ON i.ISSUE_TYPE = it.ID
LEFT JOIN PRIORITY p ON i.PRIORITY = p.ID
LEFT JOIN RESOLUTION r ON i.RESOLUTION = r.ID
LEFT JOIN STATUS s ON i.STATUS = s.ID
WHERE i._SNOWFLAKE_DELETED = FALSE;
```

To exclude deleted issues from query results, filter on the connector-managed
`_SNOWFLAKE_DELETED` column. The connector sets this flag to `TRUE` on the matching `ISSUE`
row when an issue is deleted in Jira, so no anti-join against `DELETED_ISSUE` is needed:

Copy code

```
SELECT i.*
FROM ISSUE i
WHERE i._SNOWFLAKE_DELETED = FALSE;
```

The `DELETED_ISSUE` table is still useful when you need the deletion timestamp or the user who
performed the deletion. See [Connector-managed columns](/user-guide/data-integration/openflow/connectors/jira-cloud/about#label-jira-metadata-columns) for the full set of connector-managed
metadata columns.

## Enabled tables configuration

The `Enabled Tables` parameter controls which optional tables are populated. Ingestion of the
`ISSUE`, `PROJECT`, `USER`, and `FIELD` tables is always enabled and can’t be disabled.
`ISSUE_TYPE`, `PRIORITY`, `RESOLUTION`, and `STATUS` are lookup tables that resolve the Jira
IDs stored on `ISSUE` to their descriptive names. Enabling all tables may cause performance issues
and require a larger runtime.

Available values for `Enabled Tables`:

- `CHANGELOG` (field change history for issues)
- `COMMENT` (comments on issues)
- `ISSUE_REMOTE_LINK` (remote links attached to issues)
- `ISSUE_SECURITY_SCHEME` (issue-level security configurations)
- `ISSUE_TYPE` (issue type names referenced by issues)
- `ISSUE_VOTE` (users who voted on issues)
- `ISSUE_WATCHER` (users watching issues)
- `PERMISSION` (global and project permission definitions)
- `PRIORITY` (priority names referenced by issues)
- `PROJECT_COMPONENT` (components defined in a project)
- `PROJECT_VERSION` (release versions of a project)
- `RESOLUTION` (resolution names referenced by issues)
- `STATUS` (status names and categories referenced by issues)
- `USER_GROUP` (group memberships per user)
- `WORKLOG` (time tracking entries on issues)

The per-issue tables (`CHANGELOG`, `COMMENT`, `ISSUE_REMOTE_LINK`,
`ISSUE_VOTE`, `ISSUE_WATCHER`, `WORKLOG`) and per-project tables
(`PROJECT_COMPONENT`, `PROJECT_VERSION`) only ingest data for issues and projects
that are also covered by `Project Keys Filter`.

Some tables are populated by calling the Jira API once per parent entity (for example, once per
user or once per issue). On large Jira instances, enabling these tables can significantly increase
the number of API calls and the load on the ingestion runtime, and can slow down population of the
parent table due to back-pressure on the upstream processor. Enable these tables only when the
corresponding data is required.

## Issue fields configuration

The `ISSUE` table schema depends on the `Issue Fields` parameter. The parameter accepts a
comma-separated list of field IDs or one of the special values below. Prefix a field with a minus
(`-`) to exclude it. For example, `*all,-description` returns all fields except `description`.

- `*standard` (default): Fetches all non-custom Jira fields. For information about resolving Jira IDs
  to display names, see [Accessing the data](#label-jira-core-accessing-data).
- `*navigable`: Fetches all navigable fields.
- `*all`: Fetches all fields, including custom fields.
- Individual field IDs can be specified (for example, `summary,status,customfield_10001`).

The default value `*standard` **doesn’t include custom fields**. To ingest custom fields,
set this parameter to `*all` or list the custom fields explicitly by ID, for example,
`*standard,customfield_10001`. To find custom field IDs, follow
[this guide](https://confluence.atlassian.com/jirakb/get-custom-field-ids-for-jira-and-jira-service-management-744522503.html).

Column names in the `ISSUE` table are derived from Jira field display names by:

1. Uppercasing the display name.
2. Replacing spaces with underscores.
3. Removing every character that isn’t a letter, digit, or underscore.

For example, the display name `OF Test (Multi-User)` becomes the column `OF_TEST_MULTIUSER`.

If two fields produce the same column name after this transformation, the second field’s column
is suffixed with `__<flattened_field_id>` to keep names unique. For example, two fields with
display name `Custom Field` and IDs `customfield_1` and `customfield_2` produce columns
`CUSTOM_FIELD` and `CUSTOM_FIELD__CUSTOMFIELD_2`.

Jira field types are mapped to Snowflake column types as follows:

| Jira field type | Snowflake column type |
| --- | --- |
| `number` | NUMBER |
| `array` | ARRAY |
| `progress`, `votes`, `watches`, `timetracking` | VARIANT |
| All other types | VARCHAR |

Expand

Show lessSee more

## Next steps

- [Set up the Atlassian Jira Cloud (Agile) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-agile) to install the agile flow.
- [Migrate from the legacy Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/migrate-from-legacy) if you’re moving from a previous version of the Jira Cloud connector.
