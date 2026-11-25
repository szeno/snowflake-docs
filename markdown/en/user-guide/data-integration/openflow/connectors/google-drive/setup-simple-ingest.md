# Set up the Openflow Connector for Google Drive without domain-wide delegation (*Preview*)

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

This topic describes how to set up these catalog variants:

- **Google Drive (Simple Ingest, No Domain-wide authority, no ACLs)** ingests files into a Snowflake stage.
- **Google Drive (Cortex Connect, No Domain-wide authority, no ACLs)** indexes files in Snowflake Cortex Search.

Both variants ingest files from a Google Workspace Shared Drive. They don’t
ingest permissions (ACLs), and they don’t require domain-wide delegation. You
don’t configure OAuth scopes in the Google Admin Console. The service account
authenticates with its own credentials and reaches the Shared Drive through
direct membership.

If you installed **Google Drive (Simple Ingest)** or **Google Drive (Cortex Connect)**,
which require domain-wide delegation, use
[Set up the Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/setup)
instead.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Google Drive](/user-guide/data-integration/openflow/connectors/google-drive/about).
2. Ensure that you have [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs) or [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Google Drive](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-google-drive) connector.

## Get the credentials

You need a Google Cloud service account, the Google Drive API enabled in that
project, and the service account added as a member of the Shared Drive you want
to ingest.

You don’t need Super Admin access, domain-wide delegation, or OAuth scopes in
the Google Admin Console.

### Enable service account key creation

By default Google disables service account key creation. For Openflow to
use the service account JSON, this key creation policy must be turned
off.

1. Log in to the [Google Cloud Console](https://console.cloud.google.com/) with
   an account that can manage organization policies, if key creation is
   disabled for your organization.
2. In the resource selector, make sure you’re in the organization, not a
   project in the organization.
3. Select **Organization Policies**.
4. Select the **Disable service account key creation** policy.
5. Select **Manage Policy** and turn off enforcement.
6. Select **Set Policy**.

### Create a service account and key

1. Open the [Google Cloud Console](https://console.cloud.google.com/)
   and authenticate using a user that has been granted access to create
   service accounts.
2. Make sure you’re in a project in your organization.
3. In the left navigation, under **IAM & Admin**, select the
   **Service Accounts** tab.
4. Select **Create Service Account**.
5. Enter the service account name and select **Create and Continue**.
6. Select **Done**. Copy the service account email. You use it when you add
   the account as a member of the Shared Drive.
7. On the newly created service account, select the menu under the table
   with the service accounts listed for that service account and select
   **Manage keys**.
8. Select **Add key** and then **Create new key**.
9. Leave the default selection of JSON and select **Create**.

The key is downloaded into your browser Downloads directory as a `.json`
file.

### Enable the Google Drive API

In the [Google Cloud Console](https://console.cloud.google.com/), enable the
[Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)
for the project that contains the service account.

### Add the service account to the Shared Drive

1. Open Google Drive and go to the Shared Drive that you want to ingest.
2. Add the service account email as a member of that Shared Drive.

The service account authenticates with its own credentials. Access to the drive
comes from this membership, not from domain-wide delegation.

## Set up Snowflake account

These steps apply to both variants. If you installed **Google Drive (Cortex Connect, No Domain-wide authority, no ACLs)**,
also grant the Cortex Search privileges in the procedure below. That section
applies when you ingest files and perform processing with Cortex.

As an Openflow administrator, perform the following tasks to set up your Snowflake account. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant it the following privileges.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

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

## Install and configure the connector

As a data engineer, perform the following tasks to install and configure the connector:

### Install the connector

In the connector library, install one of these variants:

- **Google Drive (Simple Ingest, No Domain-wide authority, no ACLs)**
- **Google Drive (Cortex Connect, No Domain-wide authority, no ACLs)**

Don’t install **Google Drive (Simple Ingest)** or **Google Drive (Cortex Connect)**.
Those variants require domain-wide delegation.

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

### Configure the connector

1. Right-click the imported process group and select **Parameters**.
2. Enter the required parameter values as described in [Source parameters](#label-gdrive-simple-ingest-source-parameters), [Destination parameters](#label-gdrive-simple-ingest-destination-parameters), and [Ingestion parameters](#label-gdrive-simple-ingest-ingestion-parameters).
   If you installed **Google Drive (Cortex Connect, No Domain-wide authority, no ACLs)**,
   also set [Additional parameters for Cortex Connect](#label-gdrive-no-delegation-cortex-parameters).

#### Source parameters

| Parameter | Description |
| --- | --- |
| GCP Service Account JSON | The service account JSON downloaded from Google Cloud Console to allow access to Google APIs in the connector |

Expand

Show lessSee more

If the process group shows **Google Delegation User**, leave it unset. These
variants authenticate as the service account and don’t impersonate a Google
Workspace user.

#### Destination parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data will be persisted. It must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema | The schema where data will be persisted, which must already exist in Snowflake. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase.  See the following examples:  - `CREATE SCHEMA SCHEMA_NAME` or `CREATE SCHEMA schema_name`: use `SCHEMA_NAME` - `CREATE SCHEMA "schema_name"` or `CREATE SCHEMA "SCHEMA_NAME"`: use `schema_name` or `SCHEMA_NAME`, respectively | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/privileges#label-openflow-execute-as-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Must be the RSA private key used for authentication, formatted according to PKCS8   standards and including standard PEM headers and footers. Note that either a Snowflake Private   Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake private key file. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Snowflake Warehouse | Snowflake warehouse used to run queries. | Yes |

Expand

Show lessSee more

#### Ingestion parameters

| Parameter | Description |
| --- | --- |
| Google Drive ID | The Google Shared Drive to watch for content and updates |
| Google Folder Name | Optionally, the Google Drive folder identifier (human-readable folder name) can be set to filter incoming files by. If all files are desired, then select “Set Empty String”. When set, the connector retrieves only files that are in the provided folder or subfolder. When blank or unset, no folder filtering is applied and all files under the drive are retrieved. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The extension check is performed on the original file extension. |
| Snowflake File Hash Table Name | Internal table used to store file content hashes to prevent updates to content when it has not changed. |

Expand

Show lessSee more

If the process group shows **Google Domain**, leave it unset. These variants
don’t resolve Google Groups or ingest ACLs.

#### Additional parameters for Cortex Connect

If you installed **Google Drive (Cortex Connect, No Domain-wide authority, no ACLs)**,
also set these parameters. The connector tries to convert files to PDF before
it checks **File Extensions To Ingest**. If a listed extension isn’t supported
by Cortex Parse Document, the connector skips that file, logs a warning, and
continues.

| Parameter | Description |
| --- | --- |
| OCR Mode | The OCR mode to use when parsing files with the [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document) function. The value can be `OCR` or `LAYOUT`. |
| Snowflake Cortex Search Service User Role | An identifier of a role that is assigned usage permissions on the Cortex Search service. |

Expand

Show lessSee more

### Run the flow

1. Right-click the canvas and select **Enable all Controller Services**.
2. Right-click the imported process group and select **Start**. The connector starts the data ingestion.

## Finding files in stage

Files stored in the stage might have unreadable names. To find specific files, use the metadata
tables as your source of truth. These tables contain the mapping between file names and their
corresponding file IDs in the stage.

Copy code

```
SELECT FILE_ID FROM DOC_METADATA WHERE FILE_NAME = '<file_name>';
```

Replace `<file_name>` with the name or partial name of the file you’re looking for.

The files in the stage start with the ID returned from this query.
