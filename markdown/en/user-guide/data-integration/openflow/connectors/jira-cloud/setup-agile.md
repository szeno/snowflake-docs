# Set up the Atlassian Jira Cloud (Agile) flow

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to install and configure the Atlassian Jira Cloud (Agile) flow, the agile
flow of the Openflow Connector for Jira Cloud. The core flow is documented separately in [Set up the Atlassian Jira Cloud (Core) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core).

The agile flow is independent of the core flow. It uses its own API token, parameter contexts,
state service, and Snowflake destination configuration. Both flows can write to the same Snowflake
database and schema, since they create tables with different names.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Jira Cloud](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-jira-cloud) connector.

## Get the credentials

As a Jira Cloud administrator, perform the following tasks in your Atlassian account. You can reuse
the API token from the core flow or create a separate token. The core flow and agile flow can use
the same token, but they always share the underlying Jira API rate budget regardless.

1. Navigate to the [API tokens page](https://id.atlassian.com/manage-profile/security/api-tokens).
2. Select **Create API token with scopes**.
3. In the **Create an API token** dialog box, provide a descriptive name for the API token and
   select an expiration date for the API token. This can range from 1 to 365 days.
4. Select the API token app **Jira**.
5. Select the agile scopes listed in [Required API scopes](#label-jira-agile-api-scopes).
6. Select **Create token**.
7. In the **Copy your API token** dialog box, select **Copy** to copy your generated API
   token and then paste the token to the connector parameters, or save it securely.
8. Select **Close** to close the dialog box.

### Required API scopes

Atlassian API tokens with scopes list both **classic** (broader, recommended) and **granular**
(narrower) scopes. The agile flow uses Jira Software scopes. Classic scopes are the recommended
starting set when Atlassian documents one. Use granular scopes when your organization requires a
narrower token; a granular token needs every scope Atlassian lists for an endpoint, not just one.

The `BOARD` table is always created, so every token needs the scopes in the `BOARD` row of the
following table.

The connector also calls
[`GET /rest/api/3/myself`](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-myself/#api-rest-api-3-myself-get)
for connection verification. The `BOARD_ISSUE` ingestion path also calls this endpoint at startup
to look up the Jira timezone. For this endpoint, use the classic scope `read:jira-user` or the
granular scopes `read:application-role:jira`, `read:group:jira`, `read:user:jira`, and
`read:avatar:jira`.

To ingest a board, the API token owner must be able to view the board and its saved filter. A saved
filter is visible when the token owner owns it or when it is shared with the token owner through a
group, a project that the token owner can browse, or public access.

For the `Enabled Tables` parameter that turns optional tables on, see [Jira Cloud (Agile) Ingestion Parameters](#label-jira-agile-ingestion-parameters).

The following table lists each destination table, the recommended classic scope when Atlassian
documents one, the full set of granular scopes Atlassian documents for the endpoints, and links to
the endpoints the connector calls:

| Table | Classic scope (recommended when available) | Granular scopes | Jira API reference | Notes |
| --- | --- | --- | --- | --- |
| `BOARD` (always) | `read:jira-work` (Get filter only) | **Get all boards:** `read:board-scope:jira-software`, `read:project:jira`  **Get configuration:** `read:board-scope.admin:jira-software`, `read:project:jira`  **Get filter:** `read:filter:jira`, `read:group:jira`, `read:project:jira`, `read:project-role:jira`, `read:user:jira`, `read:jql:jira`, `read:application-role:jira`, `read:avatar:jira`, `read:issue-type-hierarchy:jira` | [Get all boards](https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/#api-rest-agile-1-0-board-get), [Get configuration](https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/#api-rest-agile-1-0-board-boardid-configuration-get), and [Get filter](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filters/#api-rest-api-3-filter-id-get) | Get all boards and Get configuration are Jira Software endpoints and don’t have classic scopes. Get filter is a Jira Platform endpoint. |
| `SPRINT` (populates `SPRINT` and `BOARD_SPRINT`) | None. | `read:sprint:jira-software` | [Get all sprints](https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/#api-rest-agile-1-0-board-boardid-sprint-get) | Atlassian documents only a granular Jira Software scope for this endpoint. The endpoint returns only sprints that the API token owner has permission to view. |
| `BOARD_PROJECT` | None. | `read:board-scope.admin:jira-software`, `read:project:jira` | [Get projects associated with the board](https://developer.atlassian.com/cloud/jira/software/rest/api-group-board/#api-rest-agile-1-0-board-boardid-project-get) | Covered by the `BOARD` baseline. Atlassian documents only granular Jira Software scopes for this endpoint. |
| `BOARD_ISSUE` | `read:jira-work` | `read:issue-details:jira`, `read:field.default-value:jira`, `read:field.option:jira`, `read:field:jira`, `read:group:jira` | [Search for issues using JQL](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-jql-post) | **Browse projects** on the relevant projects. Issues that fail per-issue permission checks (for example, issue-level security) are skipped silently. |

Expand

Show lessSee more

If you reuse a single API token across both flows, combine these scopes with the core flow scopes
documented in [Required API scopes](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core#label-jira-core-api-scopes).

Tokens without scopes are also supported and grant access based solely on the API token owner’s
permissions. However, tokens with scopes are recommended for fine-grained access control.

## Set up Snowflake account

If you’ve already completed the Snowflake account setup for the core flow, you can reuse the same
role, service user, key pair, database, schema, and warehouse for the agile flow. The agile flow
parameters point at this same Snowflake configuration.

Otherwise, perform the following tasks:

As a Snowflake account administrator, perform the following tasks:

1. Create a new role or use an existing role.
2. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
3. Grant the Snowflake service user the role you created in the previous steps.
4. Configure with [key-pair auth](/user-guide/key-pair-auth) for the Snowflake SERVICE user from step 2.
5. Configure a secrets manager supported by Openflow (recommended), for example, AWS, Azure, and HashiCorp, and store the public and private keys in the secret store.

   Note

   If for any reason, you don’t want to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.

   1. After the secrets manager is configured, determine how you will authenticate to it. On AWS, use the
      EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the main menu (⋮) in the upper-right corner.
      Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
   3. At this point, all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
6. If any other Snowflake users require access to the tables ingested by the connector (for example, for custom processing in Snowflake),
   then grant those users the role created in step 1.
7. Create a database and schema in Snowflake for the connector to store ingested data. Grant the following [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the role created in the first step.

   Copy code

   ```
   CREATE DATABASE jira_destination_db;
   CREATE SCHEMA jira_destination_db.jira_destination_schema;
   GRANT USAGE ON DATABASE jira_destination_db TO ROLE <jira_connector_role>;
   GRANT USAGE ON SCHEMA jira_destination_db.jira_destination_schema TO ROLE <jira_connector_role>;
   GRANT CREATE TABLE ON SCHEMA jira_destination_db.jira_destination_schema TO ROLE <jira_connector_role>;
   ```
8. Create a warehouse that the connector will use or use an existing one. Start with the smallest warehouse size, then experiment with size depending on the
   amount of data transferred. Large data volumes typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than larger warehouse sizes.
9. Ensure that the user with the role used by the connector has the required privileges to use the warehouse. If that’s not the case then grant the required privileges to the role.

   Copy code

   ```
   CREATE WAREHOUSE jira_connector_warehouse WITH WAREHOUSE_SIZE = 'X-Small';
   GRANT USAGE ON WAREHOUSE jira_connector_warehouse TO ROLE <jira_connector_role>;
   ```

## Set up the connector

The agile flow is shipped as the Atlassian Jira Cloud (Agile) process group. As a data engineer, perform the
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

After import, the agile flow appears on the canvas as the Atlassian Jira Cloud (Agile) process group.

### Configure the connector

1. Right-click on the imported Atlassian Jira Cloud (Agile) process group and select **Parameters**.
2. Populate the required parameter values as described in
   [Flow parameters](#label-jira-agile-flow-parameters).

### Flow parameters

The agile flow uses its own separate parameter contexts. The Jira credentials and Snowflake destination
must be configured independently from the core flow. Both flows can point to the same Snowflake
destination database and schema.

- [Jira Cloud (Agile) Source Parameters](#label-jira-agile-source-parameters): Used to establish connection with the Jira API.
- [Jira Cloud (Agile) Destination Parameters](#label-jira-agile-destination-parameters): Used to establish connection with Snowflake.
- [Jira Cloud (Agile) Ingestion Parameters](#label-jira-agile-ingestion-parameters): Used to define the configuration of data ingested from Jira.

#### Jira Cloud (Agile) Source Parameters

| Parameter | Description |
| --- | --- |
| Jira Email | Email address for the Atlassian account used for authentication. |
| Jira API Token | API access token for your Atlassian Jira account. See [Required API scopes](#label-jira-agile-api-scopes) for the scopes to configure. |
| Environment URL | URL to the Atlassian Jira environment. For example, `https://your-domain.atlassian.net`. |

Expand

Show lessSee more

#### Jira Cloud (Agile) Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  - `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME` - `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank.   **KEY\_PAIR**: Must be the RSA private key used for authentication.  The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either a Snowflake Private Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake private key file. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### Jira Cloud (Agile) Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Enabled Tables | Comma-separated list of optional tables to populate. Ingestion of `BOARD` is always enabled and can’t be disabled. For the API scopes each table needs, see [Required API scopes](#label-jira-agile-api-scopes). Available values:   - `BOARD_ISSUE` (issues associated with the board) - `BOARD_PROJECT` (projects associated with the boards) - `SPRINT` (sprints and board-sprint associations, populates both `SPRINT` and   `BOARD_SPRINT`)   Default value: `BOARD_ISSUE, BOARD_PROJECT, SPRINT`. |
| Merge Interval | Time interval between journal-to-destination merge operations. When a merge runs, the Snowflake warehouse resumes. The merge is skipped if no new data has been loaded since the previous merge. Default value: `1 min`. |

Expand

Show lessSee more

## Run the flow

1. Right-click on the canvas and select **Enable all Controller Services**.
2. Right-click on the Atlassian Jira Cloud (Agile) process group and select **Start**. The flow starts the data ingestion.

On first run, the flow creates the required Snowflake tables in the destination schema. See
[Destination tables](/user-guide/data-integration/openflow/connectors/jira-cloud/about#label-jira-entities) for the full list of tables created by the agile flow and the parameters
that control which optional tables are populated.

## Resetting the connector state

If you want to restart the ingestion from scratch, clear the agile flow’s ingestion state. The
agile flow uses its own centralized state service rather than per-processor state.

To reset the state, perform the following steps:

1. Right-click the Atlassian Jira Cloud (Agile) process group and select **Stop**.
2. Navigate to the **Controller Settings** for the process group.
3. Find the **StandardJiraIngestionStateService** controller service and select **View State**.
4. Select **Clear State**. This clears the agile flow’s ingestion tracking.
5. Optionally, update the connector parameters if needed.
6. Right-click the Atlassian Jira Cloud (Agile) process group and select **Start**.

Note

The agile flow’s destination tables (`BOARD`, `SPRINT`, `BOARD_SPRINT`, `BOARD_PROJECT`,
`BOARD_ISSUE`) are fully refreshed on every scheduled run, regardless of whether you clear the
state.

## Next steps

- [Set up the Atlassian Jira Cloud (Core) flow](/user-guide/data-integration/openflow/connectors/jira-cloud/setup-core) if you haven’t yet installed the core flow.
- [Migrate from the legacy Openflow Connector for Jira Cloud](/user-guide/data-integration/openflow/connectors/jira-cloud/migrate-from-legacy) if you’re moving from a previous version of the Jira Cloud connector.
