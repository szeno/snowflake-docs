# Set up the Openflow Connector for Slack

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Slack.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Slack](/user-guide/data-integration/openflow/connectors/slack/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Slack](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-slack) connector.

## Set up a Slack App

Set up a Slack App in your Slack workspace. A Slack Admin is needed to
set up access to the Slack Workspace. This is done by creating or
supplying credentials to a Slack App and installing the App to the
Slack workspace and channels. You can create a Slack App by using the
JSON configuration:

1. Update the JSON manifest. Copy the JSON manifest text below. Change
   the name and display name properties from
   `EXAMPLE_NAME_CHANGE_THIS` to the desired name of your Slack App.
   It is recommended to use the same name and display name for your App.

   Copy code

   ```
   {
    "display_information": {
        "name": "EXAMPLE_NAME_CHANGE_THIS"
    },
    "features": {
        "bot_user": {
            "display_name": "EXAMPLE_NAME_CHANGE_THIS",
            "always_online": false
        }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "channels:history",
                "channels:read",
                "groups:history",
                "groups:read",
                "im:history",
                "im:read",
                "mpim:history",
                "mpim:read",
                "users.profile:read",
                "users:read",
                "users:read.email",
                "files:read",
                "app_mentions:read",
                "reactions:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "bot_events": [
                "message.channels",
                "message.groups",
                "message.im",
                "message.mpim",
                "reaction_added",
                "reaction_removed",
                "file_created",
                "file_deleted",
                "file_change"
            ]
        },
        "interactivity": {
            "is_enabled": true
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
   }
   ```
2. Create a Slack app through the [Apps page](https://api.slack.com/apps).

   1. On the **Your Apps** page, select **Create New App**.
   2. Select **From a manifest**.
   3. Select the **Workspace** where you’ll be developing your app. You’ll be able to [distribute your app](https://api.slack.com/distribution) to other workspaces later if you choose.
   4. Copy the updated manifest JSON from step 1.
3. Generate an app-level token. You need to create an app-level token even after using the JSON manifest. Under **Basic Information**, scroll to the **App-level tokens** section and click the button to generate an [app-level token](https://api.slack.com/concepts/token-types#app). Include the *connections:write* scope to the token.
4. Install and authorize the app.

   1. Return to the **Basic Information** section of the app management page.
   2. Install your app by selecting the **Install to Workspace** button.
   3. You’ll now be sent through the Slack OAuth flow. Select **Allow** on the following screen.

   If you want to add your app to a different workspace besides your own, these steps would need to be performed by a user from that workspace.
   After installation, navigate back to the **OAuth & Permissions** page. You’ll see an **access token** under **OAuth Tokens**.
   Access tokens represent the permissions delegated to your app by the installing user. Keep it safe and secure. Avoid checking them into public version control. Instead, access them through an environment variable.
5. Adding the App to channels. Your app isn’t a member of any channels yet, so pick a channel to add some test messages in and `/invite` your app. For example, `/invite @Grocery Reminders`.

Note

Restart the processors to load the new channels. After the App is added to a new channel, the `Consume Slack Conversation` processor in the OpenFlow Runtime needs to be stopped and restarted.

## Setup necessary ingress rules

A Snowflake Admin should follow the [egress guide](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress)
to apply egress rules to the endpoint `https://slack.com/api` and
enable WebSocket egress on `wss://wss.slack.com`. This is easiest
done by adding a rule to enable egress on the “slack.com” domain.

## Set up Snowflake account

As a Snowflake account administrator, perform the following tasks. With the default `SNOWFLAKE_MANAGED`
authentication strategy, the runtime’s execute-as role is the identity the connector uses to access
Snowflake, so you grant it the privileges below.

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant the privileges needed for the connector’s tables and internal stage to the execute-as role.

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS <destination_database>;
   CREATE SCHEMA IF NOT EXISTS <destination_database>.<destination_schema>;
   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE TABLE, CREATE STAGE, CREATE SEQUENCE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

   If you’re using [Use case 2: Ingest Slack content and enable Cortex](#label-slack-use-case-2-ingest-slack-content-and-enable-cortex), also grant the privilege to create the optional Cortex Search service:

   Copy code

   ```
   GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
2. If any other Snowflake users require access to the raw documents and tables ingested by the connector (for example, for custom processing in Snowflake),
   then grant those users the execute-as role.
3. Designate a warehouse for the connector to use. Start with the smallest warehouse size, then experiment with size depending on the number of tables being replicated,
   and the amount of data transferred. Large table numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than larger warehouse sizes.

   Copy code

   ```
   CREATE WAREHOUSE IF NOT EXISTS <openflow_warehouse>
     WITH
     WAREHOUSE_SIZE = 'XSMALL'
     AUTO_SUSPEND = 300
     AUTO_RESUME = TRUE;
   GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Use case 1: Ingest Slack content only

Use the connector definition to:

> - Perform custom analysis on ingested Slack data (no Cortex Search processing).
> - Ingest Slack messages, reactions, file attachments, and member lists into Snowflake, and keep them up to date.

### Set up the connector

As a data engineer, perform the following tasks to configure the connector:

#### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the execute-as role, as described in [Set up Snowflake account](#label-slack-set-up-snowflake-account).

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

#### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Enter the required parameter values as described in **Flow parameters: Ingest content only** below.
3. Right-click on the canvas and select **Enable all controller services**.
4. Right-click on the imported process group and select **Start**. The flow creates the required tables and begins ingesting Slack data.

##### Flow parameters: Ingest content only

| Parameter | Description |
| --- | --- |
| App Token | Slack *App-level token* generated in the Slack App. |
| Bot Token | Slack *Bot token* generated in the Slack App. |
| Destination Database | Database to contain all connector objects. It must already exist. |
| Destination Schema | Schema inside the database. It must already exist. |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. |
| Snowflake Account | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Snowflake account identifier. |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED**: Use the runtime’s execute-as role (or a child role granted to it). - **KEY\_PAIR**: Use a valid role configured for your service user. |
| Snowflake User | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Username the flow uses to connect. |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: RSA private key used for authentication (PKCS8 PEM format). Note that either Snowflake   Private Key or Snowflake Private Key File must be defined. |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Password for the encrypted private key (leave blank if unencrypted). |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: File containing the RSA Private Key (PKCS8 PEM format). The header line starts with   `-----BEGIN PRIVATE`. |
| Snowflake Warehouse | Warehouse used for SQL executed by the flow. |
| Upload Interval | Time to gather data before pushing to Snowflake. A longer interval reduces load on Snowflake but may increase latency and memory usage. |
| Refresh Slack Members | Minutes between Slack membership (ACL) refreshes. |

Expand

Show lessSee more

## Use case 2: Ingest Slack content and enable Cortex

Use the connector definition to:

> - Make Slack data ready for conversational search with Snowflake Cortex.
> - Ensure Slack channel access controls are respected in search results.

### Set up the connector

As a data engineer, perform the following tasks to configure the connector:

#### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the execute-as role, as described in [Set up Snowflake account](#label-slack-set-up-snowflake-account).

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

#### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Enter the required parameter values as described in **Flow parameters: Ingest content and enable Cortex** below.
3. Right-click on the canvas and select **Enable all controller services**.
4. Right-click on the imported process group and select **Start**.
5. Once the flow is running, proceed to [Query the Cortex Search service](#query-the-cortex-search-service) for testing.

##### Flow parameters: Ingest content and enable Cortex

| Parameter | Description |
| --- | --- |
| App Token | Slack *App-level token* generated in the Slack App. |
| Bot Token | Slack *Bot token* generated in the Slack App. |
| Destination Database | Database to contain all connector objects. It must already exist. |
| Destination Schema | Schema inside the database. It must already exist. |
| Upload Interval | Time to gather data before pushing to Snowflake. A larger value reduces load but increases data latency. |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. |
| Snowflake Account | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Snowflake account identifier. |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED**: Use the runtime’s execute-as role (or a child role granted to it). - **KEY\_PAIR**: Use a valid role configured for your service user. |
| Snowflake User | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Username the flow uses to connect. |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: PEM-formatted private key for key-pair authentication. |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED**: Must be blank. - **KEY\_PAIR**: Password for the encrypted private key (blank if unencrypted). |
| Snowflake Warehouse | Warehouse used for all SQL executed by the flow **and** by Cortex. |
| Refresh Slack Members | Minutes between Slack membership (ACL) refreshes. |

Expand

Show lessSee more

## Enabling private-channel ACLs

No extra steps are required beyond **inviting the Slack App** to each private channel. The connector automatically refreshes the member list and stores it in the membership table at each **Refresh Slack Members** interval.

## Query the Cortex Search service

After Use case 2 is running and the Cortex Search service has been created, you can query it as follows:

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    '<openflow_db>.<openflow_schema>.<<SLACK_CORTEX_SEARCH>',
    '{
      "query": "What is my vacation carry over policy?",
      "columns": ["text","channel","ts","username"],
      "filter": {"@contains": {"memberemails": "alice@example.com"}},
      "limit": 10
    }'
  )
)['results'] AS results;
```

**Common searchable columns**

`text`, `type`, `subtype`, `channel`, `user`, `username`, `connectorId`, `workspaceId`, `ts`, `threadTs`

**Example: Query an AI assistant for human resources (HR) information**

You can use Cortex Search to query an AI assistant for employees to chat about the latest Slack posts. The messages
that are searched can come from informative Slack channels such as general or it-help.

PythonREST API

Run the following code in a [Python worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create) to query the
Cortex Search service over messages ingested from Slack
Ensure that you add the `snowflake.core` package to your database.

Replace the following:

- `cortex_db`: Name of the database containing the cortex search service, specified by the *Destination Database* parameter.
- `cortex_schema`: Name of the schema containing the cortex search service, specified by the *Destination Schema* parameter.
- `cortex_search_service_name`: Name of the cortex search service, specified by the *Cortex Search Name* parameter.
- `user_emailID`: Email ID of the user who you want to filter the responses for.

Copy code

```
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.core import Root

def main(session: snowpark.Session):

   root = Root(session)

   # fetch service
   my_service = (root
     .databases["<cortex_db>"]
     .schemas["<cortex_schema>"]
     .cortex_search_services["<cortex_search_service_name>"]
   )

   # query service
   resp = my_service.search(
     query="What is my vacation carry over policy?",
     columns = ["text", "channel", "ts","username"],
     filter = {"@contains": {"memberemails": "<user_emailID>"} },
     limit=1
     )
   return (resp.to_json())
```

Execute the following code in a command-line interface to query the Cortex Search
service over messages ingested from Slack.
You will need to authentication through key pair authentication and OAuth to access the
Snowflake REST APIs. For more information,
see [REST API](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service#label-cortex-search-query-syntax-rest)
and [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

Replace the following:

- `cortex_db`: Name of the database containing the cortex search service, specified by the *Destination Database* parameter.
- `cortex_schema`: Name of the schema containing the cortex search service, specified by the *Destination Schema* parameter.
- `cortex_search_service_name`: Name of the cortex search service, specified by the *Cortex Search Name* parameter.
- `account_url`: Your Snowflake account URL. For instructions on finding your account URL, see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

Copy code

```
curl --location "https://<account_url>/api/v2/databases/<cortex_db>/schemas/<cortex_schema>/cortex-search-services/<cortex_search_service_name>" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer <CORTEX_SEARCH_JWT>" \
     --data '{
         "query": "What is my vacation carry over policy?",
         "columns": ["text", "channel"],
         "limit": 1
     }'
```

Sample response:

```
{
  "results" : [ {
  "channel" : "dev notes",
  "text" : "Answer to the question asked."
  } ]
}
```
