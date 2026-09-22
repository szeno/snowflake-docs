# Set up the Openflow Connector for Google Drive

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Google Drive.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Google Drive](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-google-drive) connector.

## Get the credentials

Setting up the connector requires specific permissions and account
settings for Snowflake Openflow processors to read data from Google.
This access is provided in part through setting up a service account and
a key for Openflow to authenticate as that service account.
For more information, see:

- [Configure access to the Google Cloud Search API](https://developers.google.com/cloud-search/docs/guides/project-setup#create_service_account_credentials)
- [Delegating domain-wide authority to the service
  account](https://developers.google.com/identity/protocols/oauth2/service-account#delegatingauthority)

As a Google Drive administrator, perform the following steps:

### Prerequisites

Ensure that you meet the following requirements:

- You have a Google user with Super Admin permissions
- You have a Google Cloud Project with the following roles:
  - Organization Policy Administrator
  - Organization Administrator

### Enable service account key creation

By default Google disables service account key creation. For Openflow to
use the service account JSON, this key creation policy must be turned
off.

1. Log in to the [Google Cloud Console](https://console.cloud.google.com/) with a super admin
   account that has the Organizational Policy Admin Role.
2. Ensure you are in the project associated with your organization, not
   the project in your organization.
3. Click **Organization Policies**.
4. Select the **Disable service account key creation** policy.
5. Click **Manage Policy** and turn off enforcement.
6. Click **Set Policy**.

### Create service account and key

1. Open the [Google Cloud Console](https://console.cloud.google.com/)
   and authenticate using a user that has been granted access to create
   service accounts.
2. Ensure you are in a project of your organization.
3. In the left navigation, under **IAM & Admin**, select the
   **Service Accounts** tab.
4. Click **Create Service Account**.
5. Enter the service account name and click **Create and Continue**.
6. Click **Done**. In the table with the service accounts listed, find
   the **OAuth 2 Client ID** column. Copy the Client ID as this will be
   required later to set up domain-wide delegation in the next section.
7. On the newly created service account, click the menu under the table
   with the service accounts listed for that service account and select
   **Manage keys**.
8. Select **Add key** and then **Create new key**.
9. Leave the default selection of JSON and click **Create**.

The key is downloaded into your browser Downloads directory as a .json
file.

### Grant service account domain-wide delegation for listed scopes

1. Log in to your Google Admin account.
2. Select **Admin** from **Google Apps selector**.
3. In the left navigation, expand **Security** and then **Access** and select **Data
   control**, then click on **API Controls**.
4. On the **API Controls** screen, select **Manage domain-wide
   delegation**.
5. Click **Add new**.
6. Enter the OAuth 2 Client ID taken from the Create service account and key section and the following scopes:

   - <https://www.googleapis.com/auth/drive>
   - <https://www.googleapis.com/auth/drive.metadata.readonly>
   - <https://www.googleapis.com/auth/admin.directory.group.member.readonly>
   - <https://www.googleapis.com/auth/admin.directory.group.readonly>
   - <https://www.googleapis.com/auth/drive.file>
   - <https://www.googleapis.com/auth/drive.metadata>
7. Click **Authorize**.

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
   GRANT CREATE TABLE, CREATE DYNAMIC TABLE, CREATE STAGE, CREATE SEQUENCE ON SCHEMA <destination_database>.<destination_schema>
     TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
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
5. If any other Snowflake users require access to the raw documents and tables ingested by the
   connector (for example, for custom processing in Snowflake), grant those users the execute-as
   role.

### Grant Cortex Search privileges

If you’re using the connector for the use case **Ingest files and perform processing with Cortex**,
also perform the following tasks:

1. Create a role for read access to the Cortex Search service created by this connector, and grant
   it to any role that will use the service:

   Copy code

   ```
   USE ROLE SECURITYADMIN;
   CREATE ROLE IF NOT EXISTS <cortex_search_service_read_only_role>;
   GRANT ROLE <cortex_search_service_read_only_role> TO ROLE <whatever_roles_will_access_search_service>;
   ```
2. Grant the privilege to create the Cortex Search service, and grant the read-only role access to
   the database and schema:

   Copy code

   ```
   GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON DATABASE <destination_database> TO ROLE <cortex_search_service_read_only_role>;
   GRANT USAGE ON SCHEMA <destination_database>.<destination_schema> TO ROLE <cortex_search_service_read_only_role>;
   ```

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Use case 1: Use the connector definition to ingest files only

Use the connector definition to:

- Perform custom processing on ingested files
- Ingest Google Drive files and permissions and keep them up to date

### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

#### Install the connector

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
2. Enter the required parameter values as described in [Google Drive Source Parameters](#google-drive-source-parameters), [Google Drive Destination Parameters](#google-drive-destination-parameters) and [Google Drive Ingestion Parameters](#google-drive-ingestion-parameters).

##### Google Drive Source Parameters

| Parameter | Description |
| --- | --- |
| Google Delegation User | The user that is used by the service account |
| GCP Service Account JSON | The service account JSON downloaded from Google Cloud Console to allow access to Google APIs in the connector |

Expand

Show lessSee more

##### Google Drive Destination Parameters

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

##### Google Drive Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Google Drive ID | The Google Shared Drive to watch for content and updates |
| Google Folder Name | Optionally, the Google Drive folder identifier (human-readable folder name) can be set to filter incoming files by. If all files are desired, then select “Set Empty String”. When set, only files that are in the provided folder or subfolder will be retrieved. When blank or unset, no folder filtering is applied and all files under the drive are retrieved. |
| Google Domain | The Google Workspace Domain that the Google Groups and Drive reside in. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Snowflake File Hash Table Name | Internal table used to store file content hashes to prevent updates to content when it has not changed. |

Expand

Show lessSee more

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## Use case 2: Use the connector definition to ingest files and perform processing with Cortex

Use the predefined flow definition to:

- Create AI assistants for public documents within your organization’s
  Google Drive.
- Enable your AI assistants to adhere to access controls specified in
  your organization’s Google Drive.

### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

#### Install the connector

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
2. Enter the required parameter values as described in [Google Drive Cortex Connect Source Parameters](#google-drive-cortex-connect-source-parameters), [Google Drive Cortex Connect Destination Parameters](#google-drive-cortex-connect-destination-parameters) and [Google Drive Cortex Connect Ingestion Parameters](#google-drive-cortex-connect-ingestion-parameters).

##### Google Drive Cortex Connect Source Parameters

| Parameter | Description |
| --- | --- |
| Google Delegation User | The user that is used by the service account |
| GCP Service Account JSON | The service account JSON downloaded from Google Cloud Console to allow access to Google APIs in the connector |

Expand

Show lessSee more

##### Google Drive Cortex Connect Destination Parameters

| Parameter | Description |
| --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake |
| Destination Schema | The schema where data will be persisted. It must already exist in Snowflake |
| Snowflake Account Identifier | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide your Snowflake account name formatted as [organization-name]-[account-name] where data will be persisted. |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. |
| Snowflake Private Key | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the RSA private key used for authentication. The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either Snowflake Private Key File or Snowflake Private Key must be defined. |
| Snowflake Private Key File | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, upload the file that contains the RSA Private Key used for authentication to Snowflake, formatted according to PKCS8 standards and having standard PEM headers and footers. The header line begins with `-----BEGIN PRIVATE`. Select the **Reference asset** checkbox to upload the private key file. |
| Snowflake Private Key Password | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the password associated with the Snowflake Private Key File. |
| Snowflake Role | When using SNOWFLAKE\_MANAGED Authentication Strategy, use the runtime’s execute-as role (or a child role granted to it). You can find your execute-as role in the Openflow UI by going to View Details for your runtime. When using Key Pair Authentication Strategy, use a valid role configured for your service user. |
| Snowflake Username | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the user name used to connect to Snowflake instance. |
| Snowflake Warehouse | Snowflake warehouse used to run queries |

Expand

Show lessSee more

##### Google Drive Cortex Connect Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Google Drive ID | The Google Shared Drive to watch for content and updates |
| Google Folder Name | Optionally, the Google Drive folder identifier (human-readable folder name) can be set to filter incoming files by. If all files are desired, then select “Set Empty String”.  When set, only files that are in the provided folder or subfolder will be retrieved. When blank or unset, no folder filtering is applied and all files under the drive are retrieved. |
| Google Domain | The Google Workspace Domain that the Google Groups and Drive reside in. |
| OCR Mode | The OCR mode to use when parsing files with [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document) function. The value can be `OCR` or `LAYOUT`. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Snowflake File Hash Table Name | Internal table used to store file content hashes to prevent updates to content when it has not changed. |
| Snowflake Cortex Search Service User Role | An identifier of a role that is assigned usage permissions on the Cortex Search service. |

Expand

Show lessSee more

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.
3. [Query the Cortex Search service](#label-openflow-gdrive-cortex).

## Use case 3: Customize the connector definition

Customize the connector definition to perform custom processing on ingested files.

### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

#### Install the connector

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

1. Customize the connector definition.

   1. Remove the following process groups:

      - Check If Duplicate Content
      - Snowflake Stage and Parse PDF
      - Update Snowflake Cortex
   2. Attach any custom processing to the output of the *Process Google
      Drive Metadata* process group. Each flow file represents a single
      Google Drive file change. Flow file attributes can be seen in the
      `Fetch Google Drive Metadata` documentation.
2. Populate the process group parameters. Follow the same process as for
   [Use case 1: Use the connector definition to ingest files only](#use-case-1-use-the-connector-definition-to-ingest-files-only). Note that after modifying the connector definition,
   not all parameters might be required.

### Run the flow

1. Run the flow.

   1. Start the process group. The flow will create all required objects
      inside Snowflake.
   2. Right-click on the imported process group and select **Start**.
2. [Query the Cortex Search service](#label-openflow-gdrive-cortex).

#### Query the Cortex Search service

You can use the [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) service to build chat
and search applications to chat with or query your documents in Google Drive.

After you install and configure the connector and it begins
ingesting content from Google Drive, you can query the Cortex Search service.
For more information about using Cortex Search, see [Query a Cortex Search service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

**Filter responses**

To restrict responses from the Cortex Search service to documents that a specific user
has access to in Google Drive, you can specify a filter containing the user ID or email address of the user
when you query Cortex Search. For example, `filter.@contains.user_ids` or `filter.@contains.user_emails`.
The name of the Cortex Search service created by the connector is `search_service` in the schema `Cortex`.

Run the following SQL code in a SQL worksheet to query
the Cortex Search service with files ingested from your Google Drive.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `user_emailID`: Email ID of the user who you want to filter the responses for.
- `your_question`: The question that you want to get responses for.
- `number_of_results`: Maximum number of results to return in the response. The maximum value is 1000 and the default value is 10.

Copy code

```
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    '<application_instance_name>.cortex.search_service',
      '{
        "query": "<your_question>",
         "columns": ["chunk", "web_url"],
         "filter": {"@contains": {"user_emails": "<user_emailID>"} },
         "limit": <number_of_results>
       }'
   )
)['results'] AS results
```

Here’s a complete list of values that you can enter for `columns`:

| Column name | Type | Description |
| --- | --- | --- |
| `full_name` | String | A full path to the file from the Google Drive documents root. Example: `folder_1/folder_2/file_name.pdf`. |
| `web_url` | String | A URL that displays an original Google Drive file in a browser. |
| `last_modified_date_time` | String | Date and time when the item was most recently modified. |
| `chunk` | String | A piece of text from the document that matched the Cortex Search query. |
| `user_ids` | Array | An array of Google Drive user IDs that have access to the document. It also includes user IDs from all the Google Groups that are assigned to the document. |
| `user_emails` | Array | An array of Google Drive user email IDs that have access to the document. It also includes user email IDs from all the Google Groups that are assigned to the document. |

Expand

Show lessSee more

**Example: Query an AI assistant for human resources (HR) information**

You can use Cortex Search to query an AI assistant for employees to chat with the latest versions of
HR information, such as onboarding, code of conduct, team processes, and organization policies.
Using response filters, you can also allow HR team members to query employee contracts while adhering to access controls configured in Google Drive.

PythonREST API

Run the following code in a [Python worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create) to query the
Cortex Search service with files ingested from Google Drive.
Ensure that you add the `snowflake.core` package to your database.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
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
     .databases["<application_instance_name>"]
     .schemas["cortex"]
     .cortex_search_services["search_service"]
   )

   # query service
   resp = my_service.search(
     query="What is my vacation carry over policy?",
     columns = ["chunk", "web_url"],
     filter = {"@contains": {"user_emails": "<user_emailID>"} },
     limit=1
   )
   return (resp.to_json())
```

Execute the following code in a command-line interface to query the Cortex Search
service with files ingested from your Google Drive.
You’ll need to authenticate through key pair authentication and OAuth to access the
Snowflake REST APIs. For more information,
see [REST API](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service#label-cortex-search-query-syntax-rest)
and [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `account_url`: Your Snowflake account URL. For instructions on finding your account URL, see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

Copy code

```
curl --location "https://<account_url>/api/v2/databases/<application_instance_name>/schemas/cortex/cortex-search-services/search_service" \
     --header 'Content-Type: application/json' \
     --header 'Accept: application/json' \
     --header "Authorization: Bearer <CORTEX_SEARCH_JWT>" \
     --data '{
         "query": "What is my vacation carry over policy?",
         "columns": ["chunk", "web_url"],
         "limit": 1
     }'
```

## Finding files in stage

Files stored in the stage may have unreadable names. To find specific files, use the metadata
tables as your source of truth. These tables contain the mapping between file names and their
corresponding file IDs in the stage.

For Cortex-enabled setups, use the following query to find files:

Copy code

```
SELECT DISTINCT METADATA:id FROM DOCS_CHUNKS WHERE METADATA:fullName LIKE '%<file_name>%';
```

For non-Cortex setups, use the following query:

Copy code

```
SELECT FILE_ID FROM DOC_METADATA WHERE FILE_NAME = '<file_name>';
```

Replace `<file_name>` with the name or partial name of the file you’re looking for.

The files in the stage start with the ID returned from these queries.
