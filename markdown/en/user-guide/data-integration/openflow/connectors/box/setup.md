# Set up the Openflow Connector for Box

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Box.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Box](/user-guide/data-integration/openflow/connectors/box/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Box](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-box) connector.

## Get the credentials

As a **Box developer** or **Box administrator**, create a [Box Platform application](https://developer.box.com/guides/applications/app-types/platform-apps/) as follows:

1. Navigate to [Box Developer Console](https://app.box.com/developers/console).
2. Select **Create Platform App**.
3. Select **Custom App** as the application type.
4. Provide a name and description for the app, and select a purpose from the drop-down list.
5. Select **Server Authentication (with JWT)** as the authentication method.
6. Select **Create App**.
7. To configure the app, navigate to the **Configuration** tab.
8. In the **App Access Level** section, select **App + Enterprise Access**.
9. In the **Application Scopes** section, select the following options:

   - **Read all files and folders stored in Box**.
   - **Write all files and folders stored in Box**: To download files and folders. Note that the connector can’t upload any files.
     Snowflake recommends granting the service account only the Viewer role.
     To grant the application access to files in Box, select a folder that you want to synchronize. Share it with the app service account using the email of the service account saved from the **General Settings** tab.
     Openflow Connector for Box is able to discover and download files from the specified folder and all its subfolders, but it cannot modify the files.
   - **Manage users**: To read users in the enterprise.
   - **Manage groups**: To read groups and their members in the enterprise.
   - **Manage enterprise properties**: To read enterprise events.
10. In the **Add and Manage Public Keys** section, generate a public/private key pair. Box downloads a JSON configuration file with a private key.
11. Save the changes.
12. Navigate to the **Authorization** tab, and submit the app for authorization for access to the enterprise.
13. Request your enterprise administrator to approve the app.
14. After the approval is granted, go to the **General Settings** tab and save the app service account email address.

For more information, see [Setup with JWT](https://developer.box.com/guides/authentication/jwt/jwt-setup/).

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

## Use cases

You can configure the connector for the following use cases:

- [Ingest files only](#ingest-files-only)
- [Ingest files and perform processing with Cortex](#ingest-files-and-perform-processing-with-cortex)
- [Extract Box metadata using Box AI and ingest it into a Snowflake table](#extract-box-metadata-using-box-ai-and-ingest-it-into-a-snowflake-table)
- [Synchronize Box file metadata instances with a Snowflake table](#synchronize-box-file-metadata-instances-with-a-snowflake-table)

### Ingest files only

Use the connector definition to perform custom processing on ingested files.

#### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

##### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

##### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Enter the required parameter values as described in [Box ingestion parameters](#box-ingestion-parameters), [Box destination parameters](#box-destination-parameters) and [Box source parameters](#box-source-parameters).

###### Box source parameters

| Parameter | Description |
| --- | --- |
| Box App Config JSON | An application JSON configuration that was downloaded during the app creation. |
| Box App Config File | An application JSON file that was downloaded during the app creation. Either “Box App Config File” or “Box App Config JSON” has to be set. Select the **Reference asset** checkbox to upload the config file. |

Expand

Show lessSee more

###### Box destination parameters

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

###### Box ingestion parameters

| Parameter | Description |
| --- | --- |
| Box Folder ID | The ID of the folder to read the files from. Set this to `0` to synchronize all folders the Box app has access to. It can be retrieved from the URL, for example <https://app.box.com/folder/FOLDER_ID>. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Snowflake File Hash Table Name | Name of the table to store file hashes to determine if the content has changed. This parameter should generally not be changed. |

Expand

Show lessSee more

#### Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

After starting the connector, it retrieves all files from the specified folder, and then consumes `admin_logs_streaming` events within the last 14 days.
This is done to capture data that may otherwise have been missed during the initialization process.
During that time, `not found` errors may occur, which are caused by files that appear in the events but are no longer present.

### Ingest files and perform processing with Cortex

Use the connector definition to:

- Create AI assistants for public documents within your organization’s Box enterprise
- Enable your AI assistants to adhere to access controls specified in your organization’s Box enterprise

#### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

##### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

##### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Box Cortex Connect Ingestion Parameters](#box-cortex-connect-ingestion-parameters), [Box Cortex Connect Destination Parameters](#box-cortex-connect-destination-parameters) and [Box Cortex Connect Source Parameters](#box-cortex-connect-source-parameters).

###### Box Cortex Connect Source Parameters

| Parameter | Description |
| --- | --- |
| Box App Config JSON | An application JSON configuration that was downloaded during the app creation. |
| Box App Config File | An application JSON file that was downloaded during the app creation. Either “Box App Config File” or “Box App Config JSON” has to be set. Select the **Reference asset** checkbox to upload the config file. |

Expand

Show lessSee more

###### Box Cortex Connect Destination Parameters

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

###### Box Cortex connect ingestion parameters

| Parameter | Description |
| --- | --- |
| Box Folder ID | The ID of the folder to read the files from. Set this to `0` to synchronize all folders the Box app has access to. It can be retrieved from the URL, for example <https://app.box.com/folder/FOLDER_ID>. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Snowflake File Hash Table Name | Name of the table to store file hashes to determine if the content has changed. This parameter should generally not be changed. |
| OCR Mode | The OCR mode to use when parsing files with [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document) function. The value can be `OCR` or `LAYOUT`. |
| Snowflake Cortex Search Service User Role | An identifier of a role that is assigned usage permissions on the Cortex Search service. |

Expand

Show lessSee more

#### Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

After starting the connector, it retrieves all files from the specified folder, and then consumes `admin_logs_streaming` events within the last 14 days.
This is done to capture any data that may have been missed during the initialization process.
During that time, `not found` errors may occur, caused by the files that appear in the events but are no longer present.

#### Query the Cortex Search service

You can use the [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) service to build chat
and search applications to chat with or query your documents in Box.

After you install and configure the connector and it begins
ingesting content from Box, you can query the Cortex Search service.
For more information about using Cortex Search, see [Query a Cortex Search service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

**Filter responses**

To restrict responses from the Cortex Search service to documents that a specific user
has access to in Box, you can specify a filter containing the user ID or email address of the user
when you query Cortex Search. For example, `filter.@contains.user_ids` or `filter.@contains.user_emails`.
The name of the Cortex Search service created by the connector is `search_service` in the schema `Cortex`.

Run the following SQL code in a SQL worksheet to query
the Cortex Search service with files ingested from Box.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `user_emailID`: Email ID of the user who you want to filter the responses for.
- `your_question`: The question that you want to get responses for.
- `number_of_results`: Maximum number of results to return in the response. The maximum value is 1,000 and the default value is 10.

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

Here is a complete list of values that you can enter for `columns`:

| Column name | Type | Description |
| --- | --- | --- |
| `full_name` | String | A full path to the file from the Box folder root. Example: `folder_1/folder_2/file_name.pdf`. |
| `web_url` | String | A URL that displays an original Box file in a browser. |
| `last_modified_date_time` | String | Date and time when the item was most recently modified. |
| `chunk` | String | A piece of text from the document that matched the Cortex Search query. |
| `user_ids` | Array | An array of user IDs that have access to the document. |
| `user_emails` | Array | An array of user email IDs that have access to the document. |

Expand

Show lessSee more

**Example: Query an AI assistant for human resources (HR) information**

You can use Cortex Search to query an AI assistant for employees to chat with the latest versions of
HR information, such as onboarding, code of conduct, team processes, and organization policies.
Using response filters, you can also allow HR team members to query employee contracts while adhering to access controls configured in Box.

SQLPythonREST API

Run the following in a [SQL worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create-file) to query the Cortex Search service with files ingested from Box.
Select the database as your application instance name and schema as **Cortex**.

Replace the following:

- `application_instance_name`: Name of your database and connector application instance.
- `user_emailID`: Email ID of the user who you want to filter the responses for.

Copy code

```
SELECT PARSE_JSON(
     SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
          '<application_instance_name>.cortex.search_service',
          '{
             "query": "What is my vacation carryover policy?",
             "columns": ["chunk", "web_url"],
             "filter": {"@contains": {"user_emails": "<user_emailID>"} },
             "limit": 1
          }'
     )
 )['results'] AS results
```

Run the following code in a [Python worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create) to query the
Cortex Search service with files ingested from Box.
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
     query="What is my vacation carryover policy?",
     columns = ["chunk", "web_url"],
     filter = {"@contains": {"user_emails": "<user_emailID>"} },
     limit=1
   )
   return (resp.to_json())
```

Execute the following code in a command-line interface to query the Cortex Search
service with files ingested from your Box.
Access to the Snowflake REST APIs requires authentication via both key pair authentication and OAuth.
For more information,
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
         "query": "What is my vacation carryover policy?",
         "columns": ["chunk", "web_url"],
         "limit": 1
     }'
```

Sample response:

```
{
  "results" : [ {
  "web_url" : "https://<domain>.box.com/sites/<site_name>/<path_to_file>",
  "chunk" : "Answer to the question asked."
  } ]
}
```

### Extract Box metadata using Box AI and ingest it into a Snowflake table

Use the connector definition to:

- Extract metadata about your Box files and ingest it into a Snowflake table
- Perform operations on the metadata of your files stored in Box

#### Create a Snowflake table for storing the Box metadata

1. Ensure that Box AI is enabled for the extraction of metadata to occur. For more information, see [Configuring Box AI](https://support.box.com/hc/en-us/articles/22166647877011-Configuring-Box-AI).
2. Create a Snowflake table where the metadata will be sent.

   For the connector to know what kind of metadata to extract, you must create a Snowflake table in your database and schema with the column names of the fields you would like to extract.
   Add descriptions to each column to improve the performance of the model used to extract the metadata from the files.
3. In the table created in the previous step, ensure that there is a column to store the Box file ID and that it is of type VARCHAR.

   The name of this column is required to be entered as the Box File Identifier Column parameter in later steps.
   The list of supported column types for the metadata table is VARCHAR, STRING, TEXT, FLOAT, DOUBLE, and DATE.

Here is an example of the table that you can create for this connector:

Copy code

```
CREATE OR REPLACE TABLE OPENFLOW.BOX_METADATA_SCHEMA.LOAN_AGREEMENT_METADATA (
  BOX_FILE_ID               VARCHAR    COMMENT 'Box file identifier column',
  LOAN_ID                   STRING     COMMENT 'Unique loan agreement identifier (e.g. L-2025-0001)',
  BORROWER_NAME             STRING     COMMENT 'Name of the borrower entity or individual',
  LENDER_NAME               STRING     COMMENT 'Name of the lending institution',
  LOAN_AMOUNT               DOUBLE     COMMENT 'Principal amount of the loan (in USD)',
  INTEREST_RATE             FLOAT      COMMENT 'Annual interest rate (%)',
  EFFECTIVE_DATE            DATE       COMMENT 'Date on which the loan becomes effective',
  MATURITY_DATE             DATE       COMMENT 'Scheduled loan maturity date',
  LOAN_TERM_MONTHS          FLOAT      COMMENT 'Original term length in months',
  COLLATERAL_DESCRIPTION    TEXT       COMMENT 'Description of collateral securing the loan',
  CREDIT_SCORE              FLOAT      COMMENT 'Borrower credit score',
  JURISDICTION              STRING     COMMENT 'Governing law jurisdiction (e.g. NY, CA)'
);
```

#### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

##### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

##### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Box Ingest Metadata Source Parameters](#box-ingest-metadata-source-parameters), [Box Ingest Metadata Destination Parameters](#box-ingest-metadata-destination-parameters) and [Box Ingest Metadata Ingestion Parameters](#box-ingest-metadata-ingestion-parameters).

###### Box Ingest Metadata Source Parameters

| Parameter | Description |
| --- | --- |
| Box App Config JSON | An application JSON configuration that was downloaded during the app creation. |
| Box App Config File | An application JSON file that was downloaded during the app creation. Either “Box App Config File” or “Box App Config JSON” has to be set. Select the **Reference asset** checkbox to upload the config file. |

Expand

Show lessSee more

###### Box Ingest Metadata Destination Parameters

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

###### Box Ingest Metadata Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Box Folder ID | The ID of the folder to read the files from. Set this to `0` to synchronize all folders the Box app has access to. The ID can be retrieved from the URL, for example <https://app.box.com/folder/FOLDER_ID>. |
| Box File Identifier Column | The column of the metadata table that will store the Box file ID to associate the given metadata with a file. This column must be of type VARCHAR and be part of the table created in [Create a Snowflake table for storing the Box metadata](#create-a-snowflake-table-for-storing-the-box-metadata). |
| Destination Metadata Table | The Snowflake table you created in [Create a Snowflake table for storing the Box metadata](#create-a-snowflake-table-for-storing-the-box-metadata), which has the columns of the metadata you want to collect. |

Expand

Show lessSee more

#### Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

After starting the connector, it retrieves all files from the specified folder, and then consumes `admin_logs_streaming` events from the last 14 days.
This is done to capture any data that may have been missed during the initialization process.
During that time, `not found` errors may occur, caused by the files that appear in the events but are no longer present.

### Synchronize Box file metadata instances with a Snowflake table

Use the connector definition to perform a data transformation on metadata
from Box in a Snowflake table and add the changes back to a Box metadata instance.

#### Create a Snowflake stream for storing the Box metadata

1. Create a Snowflake stream for the metadata table you want to use. The stream is used to monitor any changes that occur to the table with which you want to synchronize your Box files.
   To learn how to create a table for storing Box metadata, see [Create a Snowflake table for storing the Box metadata](#create-a-snowflake-table-for-storing-the-box-metadata).
   If the connector is stopped beyond the data retention time and the stream becomes stale, then you must recreate a stream and replace the previous one. To learn more about managing streams, see [Manage streams](/user-guide/streams-manage).

   Here is an example of a stream that you can create for this connector:

   Copy code

   ```
   CREATE OR REPLACE STREAM OPENFLOW.BOX_METADATA_SCHEMA.LOAN_AGREEMENT_METADATA_STREAM
   ON TABLE OPENFLOW.BOX_METADATA_SCHEMA.LOAN_AGREEMENT_METADATA
   ```
2. In the metadata table, ensure that there is a column to store the Box file ID and that it is of type VARCHAR.

   The name of this column is required to be entered as the Box File Identifier Column parameter in later steps.
   The list of supported column types for the metadata table is VARCHAR, STRING, TEXT, FLOAT, DOUBLE, and DATE.

#### Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

##### Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

##### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Box Publish Metadata Source Parameters](#box-publish-metadata-source-parameters), [Box Publish Metadata Destination Parameters](#box-publish-metadata-destination-parameters) and [Box Publish Metadata Ingestion Parameters](#box-publish-metadata-ingestion-parameters).

###### Box Publish Metadata Source Parameters

| Parameter | Description |
| --- | --- |
| Source Database | Snowflake Database that contains the schema that contains the Snowflake Stream that ingests the changes. |
| Source Schema | Schema that contains the Snowflake Stream that ingests the changes. |
| Snowflake Account Identifier | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide your Snowflake account name formatted as [organization-name]-[account-name] where data will be persisted. |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. |
| Snowflake Private Key | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the RSA private key used for authentication. The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either Snowflake Private Key File or Snowflake Private Key must be defined. |
| Snowflake Private Key File | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, upload the file that contains the RSA Private Key used for authentication to Snowflake, formatted according to PKCS8 standards and having standard PEM headers and footers. The header line begins with `-----BEGIN PRIVATE`. Select the **Reference asset** checkbox to upload the private key file. |
| Snowflake Private Key Password | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the password associated with the Snowflake Private Key File. |
| Snowflake Role | When using SNOWFLAKE\_MANAGED Authentication Strategy, use the runtime’s execute-as role (or a child role granted to it). You can find your execute-as role in the Openflow UI by going to View Details for your runtime. When using Key Pair Authentication Strategy, use a valid role configured for your service user. |
| Snowflake Username | Leave this blank when using SNOWFLAKE\_MANAGED Authentication Strategy. When using KEY\_PAIR, provide the user name used to connect to the Snowflake instance. |
| Snowflake Warehouse | Snowflake warehouse used to run queries. |
| Snowflake Stream Name | Snowflake stream name used for ingestion of changes from the source Snowflake table. You must create it before starting the connector and link to the table. |

Expand

Show lessSee more

###### Box Publish Metadata Destination Parameters

| Parameter | Description |
| --- | --- |
| Box App Config JSON | An application JSON configuration that was downloaded during the app creation. |
| Box App Config File | An application JSON file that was downloaded during the app creation. Either “Box App Config File” or “Box App Config JSON” has to be set. Select the **Reference asset** checkbox to upload the config file. |

Expand

Show lessSee more

###### Box Publish Metadata Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Box File Identifier Column | The column of the metadata table that will store the Box file ID to associate the given metadata with a file. This column must be of type VARCHAR and be part of the table created in [Create a Snowflake table for storing the Box metadata](#create-a-snowflake-table-for-storing-the-box-metadata). |
| Box Metadata Template Name | Template name of the Box metadata template that will be added to the Box files. You don’t need to manually create a template before starting the connector. If you enter a value in this parameter, a template is automatically created with this template name. The name provided should not overlap with any template that you have already created in your Box environment. |
| Box Metadata Template Key | The Box template key of the Box metadata template that will be added to the Box files. This is the key that will be used to reference the template in the Box API. You don’t need to manually create a template before starting the connector. If you enter a value in this parameter, a template is automatically created with this template key. The key provided should not overlap with any template that you have already created in your Box environment. |

Expand

Show lessSee more

#### Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

After running the flow, you can query the Cortex Search service. For information on how to query the Cortex Search service, see [Query the Cortex Search service](#query-the-cortex-search-service).

### Finding files in stage

Files stored in the stage may have unreadable names. To find specific files, use the metadata
tables as your source of truth. These tables contain the mapping between file names and their
corresponding file IDs in the stage.

For Cortex-enabled setups, use the following query to find files:

Copy code

```
SELECT DISTINCT METADATA:id FROM DOCS_CHUNKS WHERE METADATA:fullName LIKE '%<file_name>';
```

For non-Cortex setups, use the following query:

Copy code

```
SELECT FILE_ID FROM DOC_METADATA WHERE FILE_NAME = '<file_name>';
```

Replace `<file_name>` with the name or partial name of the file you’re looking for.

The files in the stage start with the ID returned from these queries.
