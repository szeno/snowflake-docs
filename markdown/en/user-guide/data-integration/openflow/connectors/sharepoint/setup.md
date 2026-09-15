# Set up the Openflow Connector for SharePoint

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for SharePoint.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [SharePoint](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-sharepoint) connector.

## Set up access to your SharePoint site

As an Azure or Office 365 account administrator, perform the following actions:

1. Ensure that you have a [Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview) application registered and that it is configured with the
   following [application permissions](https://learn.microsoft.com/en-us/graph/permissions-overview?tabs=http#application-permissions) based on your requirements:

> **For Microsoft SharePoint (Cortex Search, document ACLs) and Microsoft SharePoint (Simple Ingest, document ACLs):**
>
> - `Sites.Selected`: Limits access to only specified sites.
>   :   For more information, see [Sites.Selected](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesselected).
> - `GroupMember.Read.All`: Used for resolving SharePoint group permissions.
>   :   For more information, see [GroupMember.Read.All](https://learn.microsoft.com/en-us/graph/permissions-reference#groupmemberreadall).
> - `User.ReadBasic.All`: Used for resolving Microsoft 365 user emails.
>   :   For more information, see [User.ReadBasic.All](https://learn.microsoft.com/en-us/graph/permissions-reference#userreadbasicall).
>
> **For Microsoft SharePoint (Cortex Search, no document ACLs) and Microsoft SharePoint (Simple Ingest, no document ACLs):**
>
> - `Sites.Selected`: Limits access to only specified sites.
>   :   For more information, see [Sites.Selected](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesselected).

1. Grant the `fullcontrol` role to the application in the selected sites.

   This role handles folder access changes during CDC ingestion. Grant it using the [Grant-PnPAzureADAppSitePermission](https://github.com/pnp/powershell/blob/dev/documentation/Grant-PnPAzureADAppSitePermission.md) cmdlet, or by calling the [GraphAPI permission endpoint](https://learn.microsoft.com/en-us/graph/api/site-post-permissions), e.g. using `curl`.

   For more information, see [Roles](https://learn.microsoft.com/en-us/graph/permissions-selected-overview?tabs=http#roles).

   Note

   If you cannot grant the `fullcontrol` role, grant the narrower `read` role to the application instead. However, if access to a folder in the ingested site changes, the connector may enter an irreparable state and will require a full re-ingestion of data. Snowflake recommends granting the `fullcontrol` role to fully mitigate this issue.
2. Configure application credentials based on your use case:

   **For Microsoft SharePoint (Cortex Search, document ACLs) and Microsoft SharePoint (Simple Ingest, document ACLs):**

   - Add a new certificate or ensure that you have access to the existing certificate file and its private key.
     For more information, see [Option 1: Add a certificate](https://learn.microsoft.com/en-us/graph/auth-register-app-v2#option-1-add-a-certificate).
   - Create a new client secret and record the secret’s value.
     :   For more information, see [Option 2: Add a client secret](https://learn.microsoft.com/en-us/graph/auth-register-app-v2#option-2-add-a-client-secret).

   **For Microsoft SharePoint (Cortex Search, no document ACLs) and Microsoft SharePoint (Simple Ingest, no document ACLs):**

   - Create a new client secret and record the secret’s value.
     :   For more information, see [Option 2: Add a client secret](https://learn.microsoft.com/en-us/graph/auth-register-app-v2#option-2-add-a-client-secret).
3. Record the following information from your Microsoft Graph application:

   - The client ID of your application.
     :   For more information, see [Application ID (client ID)](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id).
   - The tenant ID of your application.
     :   For more information, see [Find your Microsoft 365 tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id).
   - The site URL of the Microsoft 365 SharePoint site with the files or folders that you want to ingest into Snowflake; for example, `https://yourtenant.sharepoint.com/sites/YourSite`.

## Set up your Snowflake account

As a Snowflake account administrator, perform the following tasks manually
or by using the script included below:

1. Create a new role or use an existing role and grant the [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges).
2. Create a new Snowflake service user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property).
3. Grant the Snowflake service user the role you created in the previous steps.
4. Configure with [key-pair auth](/user-guide/key-pair-auth) for the Snowflake SERVICE user from step 2.
5. Snowflake strongly recommends this step. Configure a secrets manager supported by Openflow, for example, AWS, Azure, and Hashicorp, and store the public and private keys in the secret store.

   Note

   If for any reason, you do not wish to use a secrets manager, then you are responsible for safeguarding the
   public key and private key files used for key-pair authentication according to the security policies of your organization.

   1. Once the secrets manager is configured, determine how you will authenticate to it. On AWS, it’s recommended that you the
      EC2 instance role associated with Openflow as this way no other secrets have to be persisted.
   2. In Openflow, configure a Parameter Provider associated with this Secrets Manager, from the hamburger menu in the upper right.
      Navigate to **Controller Settings** » **Parameter Provider** and then fetch your parameter values.
   3. At this point all credentials can be referenced with the associated parameter paths and no sensitive values need to be persisted within Openflow.
6. If any other Snowflake users require access to the raw ingested documents and tables ingested by the connector (for example, for custom processing in Snowflake),
   then grant those users the role created in step 1.
7. Designate a warehouse for the connector to use. Start with the smallest warehouse size, then experiment with size depending on the number of tables being replicated,
   and the amount of data transferred. Large table numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than larger warehouse sizes.

### Example setup

> Copy code
>
> ```
> --The following script assumes you'll need to create all required roles, users, and objects.
> --However, you may want to reuse some that are already in existence.
>
> --Create a Snowflake service user to manage the connector
> USE ROLE USERADMIN;
> CREATE USER <openflow_service_user> TYPE=SERVICE COMMENT='Service user for Openflow automation';
>
> --Create a pair of secure keys (public and private). For more information, see
> --key-pair authentication. Store the private key for the user in a file to supply
> --to the connector’s configuration. Assign the public key to the Snowflake service user:
> ALTER USER <openflow_service_user> SET RSA_PUBLIC_KEY = '<pubkey>';
>
>
> --Create a role to manage the connector and the associated data and
> --grant it to that user
> USE ROLE SECURITYADMIN;
> CREATE ROLE <openflow_connector_admin_role>;
> GRANT ROLE <openflow_connector_admin_role> TO USER <openflow_service_user>;
>
>
> --The following block is for USE CASE 2 (Cortex connect) ONLY
> --Create a role for read access to the cortex search service created by this connector.
> --This role should be granted to any role that will use the service
> CREATE ROLE <cortex_search_service_read_only_role>;
> GRANT ROLE <cortex_search_service_read_only_role> TO ROLE <whatever_roles_will_access_search_service>;
>
> --Create the database the data will be stored in and grant usage to the roles created
> USE ROLE ACCOUNTADMIN; --use whatever role you want to own your DB
> CREATE DATABASE IF NOT EXISTS <destination_database>;
> GRANT USAGE ON DATABASE <destination_database> TO ROLE <openflow_connector_admin_role>;
>
> --Create the schema the data will be stored in and grant the necessary privileges
> --on that schema to the connector admin role:
> USE DATABASE <destination_database>;
> CREATE SCHEMA IF NOT EXISTS <destination_schema>;
> GRANT USAGE ON SCHEMA <destination_schema> TO ROLE <openflow_connector_admin_role>;
> GRANT CREATE TABLE, CREATE DYNAMIC TABLE, CREATE STAGE, CREATE SEQUENCE, CREATE CORTEX
> SEARCH SERVICE ON SCHEMA <destination_schema> TO ROLE <openflow_connector_admin_role>;
>
> --The following block is for CASE 2 (Cortex connect) ONLY
> --Grant the Cortex read-only role access to the database and schema
> GRANT USAGE ON DATABASE <destination_database> TO ROLE <cortex_search_service_read_only_role>;
> GRANT USAGE ON SCHEMA <destination_schema> TO ROLE <cortex_search_service_read_only_role>;
>
> --Create the warehouse this connector will use if it doesn't already exist. Grant the
> --appropriate privileges to the connector admin role. Adjust the size according to your needs.
> CREATE WAREHOUSE <openflow_warehouse>
> WITH
>    WAREHOUSE_SIZE = 'MEDIUM'
>    AUTO_SUSPEND = 300
>    AUTO_RESUME = TRUE;
> GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO ROLE <openflow_connector_admin_role>;
> ```

## Use case 1: Ingest files only

Use a connector to:

- Ingest and continuously update Sharepoint files for custom processing within Snowflake
- Optionally ingest file permissions (ACL connectors) to persist access controls downstream

### Set up the connector

As a data engineer, perform the following tasks to configure the connector:

#### Install the connector

Note

There are multiple variants of the SharePoint connector. Choose the variant that best fits your use case as described in [Variants of the Openflow Connector for SharePoint](/user-guide/data-integration/openflow/connectors/sharepoint/about#label-sharepoint-overview-use-cases).

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

1. Populate the process group parameters
   1. Right-click on the imported process group and select **Parameters**.
   2. Enter the required parameter values as described in [Sharepoint Ingestion Parameters](#sharepoint-ingestion-parameters), [Sharepoint Destination Parameters](#sharepoint-destination-parameters) and [Sharepoint Source Parameters](#sharepoint-source-parameters).

##### Sharepoint Source Parameters

**For all connectors:**

| Parameter | Description |
| --- | --- |
| SharePoint Site URL | URL or SharePoint site from which the connector will ingest content |
| SharePoint Client ID | Microsoft Entra client ID. To learn about client ID and how to find it in Microsoft Entra, see [Application ID (client ID)](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id). |
| SharePoint Client Secret | Microsoft Entra Client Secret. To learn about a client secret and how to find it in Microsoft Entra, see [Certificates & secrets](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). |
| SharePoint Tenant ID | Microsoft Entra Tenant ID. To learn about tenant ID and how to find it in Microsoft Entra, see [Find your Microsoft 365 tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id). |

Expand

Show lessSee more

**For ACL connectors only:**

| Parameter | Description |
| --- | --- |
| Sharepoint Application Private Key | A generated application private key in PEM format. The key must be unencrypted. |
| Sharepoint Site Domain | A domain name of the synchronized Sharepoint site. |
| Sharepoint Application Certificate | A generated application certificate in PEM format. |

Expand

Show lessSee more

##### Sharepoint Destination Parameters

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

##### Sharepoint Ingestion Parameters

**For all connectors:**

| Parameter | Description |
| --- | --- |
| SharePoint Source Folder | Supported files from this folder and all its subfolders is ingested into Snowflake. The folder path is relative to a Shared Documents library. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. To learn about the formats that can be converted, see [Format options](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content-format?view=graph-rest-1.0&tabs=http#format-options) If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Sharepoint Document Library Name | A library in the SharePoint Site to ingest files from. |
| Snowflake File Hash Table Name | Name of the table to store file hashes to determine if the content has changed. This parameter should generally not be changed. |

Expand

Show lessSee more

**For ACL connectors only:**

| Parameter | Description |
| --- | --- |
| Sharepoint Site Groups Enabled | Specifies whether the Site Groups functionality is enabled. |

Expand

Show lessSee more

1. Run the flow.
   1. Start the process group. The flow will create all required objects
      inside of Snowflake.
   2. Right click on the imported process group and select **Start**.

## Use case 2: Ingest files and perform processing with Cortex

Use the predefined flow definition to:

- Create AI assistants for documents within your organization’s SharePoint site
- Enable your AI assistants to adhere to access controls specified in your organization’s SharePoint site

### Set up the connector

As a data engineer, perform the following tasks to configure the connector:

#### Install the connector

1. Create a database and schema in Snowflake for the connector to store ingested data. Grant required [Database privileges](/user-guide/security-access-control-privileges#label-database-privileges) to the role created in the first step. Substitute the role placeholder with the actual value and use the following SQL commands:

   Copy code

   ```
   CREATE DATABASE DESTINATION_DB;
   CREATE SCHEMA DESTINATION_DB.DESTINATION_SCHEMA;
   GRANT USAGE ON DATABASE DESTINATION_DB TO ROLE <CONNECTOR_ROLE>;
   GRANT USAGE ON SCHEMA DESTINATION_DB.DESTINATION_SCHEMA TO ROLE <CONNECTOR_ROLE>;
   GRANT CREATE TABLE ON SCHEMA DESTINATION_DB.DESTINATION_SCHEMA TO ROLE <CONNECTOR_ROLE>;
   ```

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

1. Populate the process group parameters
   1. Right click on the imported process group and select **Parameters**.
   2. Enter the required parameter values as described in [Sharepoint Cortex Connect Source Parameters](#sharepoint-cortex-connect-source-parameters), [Sharepoint Cortex Connect Destination Parameters](#sharepoint-cortex-connect-destination-parameters) and [Sharepoint Cortex Connect Ingestion Parameters](#sharepoint-cortex-connect-ingestion-parameters).

##### Sharepoint Cortex Connect Source Parameters

**For all connectors:**

| Parameter | Description |
| --- | --- |
| SharePoint Site URL | URL or SharePoint site from which the connector will ingest content |
| SharePoint Client ID | Microsoft Entra client ID. To learn about client ID and how to find it in Microsoft Entra, see [Application ID (client ID)](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id). |
| SharePoint Client Secret | Microsoft Entra Client Secret. To learn about a client secret and how to find it in Microsoft Entra, see [Certificates & secrets](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). |
| SharePoint Tenant ID | Microsoft Entra Tenant ID. To learn about tenant ID and how to find it in Microsoft Entra, see [Find your Microsoft 365 tenant ID](https://learn.microsoft.com/en-us/sharepoint/find-your-office-365-tenant-id). |

Expand

Show lessSee more

**For ACL connectors only:**

| Parameter | Description |
| --- | --- |
| Sharepoint Application Private Key | A generated application private key in PEM format. The key must be unencrypted. |
| Sharepoint Site Domain | A domain name of the synchronized Sharepoint site. |
| Sharepoint Application Certificate | A generated application certificate in PEM format. |

Expand

Show lessSee more

##### Sharepoint Cortex Connect Destination Parameters

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

##### Sharepoint Cortex Connect Ingestion Parameters

**For all connectors:**

| Parameter | Description |
| --- | --- |
| SharePoint Source Folder | Supported files from this folder and all its subfolders is ingested into Snowflake. The folder path is relative to a Shared Documents library. |
| File Extensions To Ingest | A comma-separated list that specifies file extensions to ingest. The connector tries to convert the files to PDF format first, if possible. Nonetheless, the extension check is performed on the original file extension. To learn about the formats that can be converted, see [Format options](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content-format?view=graph-rest-1.0&tabs=http#format-options) If some of the specified file extensions are not supported by Cortex Parse Document, then the connector ignores those files, logs a warning message in an event log, and continues processing other files. |
| Sharepoint Document Library Name | A library in the SharePoint Site to ingest files from. |
| Snowflake File Hash Table Name | Name of the table to store file hashes to determine if the content has changed. This parameter should generally not be changed. |
| OCR Mode | The OCR mode to use when parsing files with [Parsing documents with AI\_PARSE\_DOCUMENT](/user-guide/snowflake-cortex/parse-document) function. The value can be `OCR` or `LAYOUT`. In `OCR` mode, only raw text content is extracted, ignoring formatting and table structures. In `LAYOUT` mode, the output preserves table structures as Markdown. |
| Snowflake Cortex Search Service User Role | An identifier of a role that is assigned usage permissions on the Cortex Search service. |

Expand

Show lessSee more

**For ACL connectors only:**

| Parameter | Description |
| --- | --- |
| Sharepoint Site Groups Enabled | Specifies whether the Site Groups functionality is enabled. |

Expand

Show lessSee more

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.
3. [Query the Cortex Search service](#query-the-cortex-search-service).

## Use case 3: Customise the connector definition

Customize the connector definition to perform custom processing on ingested files.

### Set up the connector

As a data engineer, perform the following tasks to configure the connector:

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
      - (Optional) Process Microsoft365 Groups
   2. Attach any custom processing to the output of the
      `Process SharePoint Metadata` process group. Each flow file
      represents a single SharePoint file change.
2. Populate the process group parameters. Follow the same process as for
   the use case 1. Note that after modifying the connector definition,
   not all parameters might be required.
3. Run the flow.

   1. Start the process group. The flow will create all required objects
      inside of Snowflake.
   2. Right click on the imported process group and select **Start**.
4. [Query the Cortex Search service](#query-the-cortex-search-service).

## Enabling Sharepoint site groups

### Microsoft Graph application for site groups

In addition to the steps specified in [Set up access to your SharePoint site](#label-openflow-sharepoint-setup-access), do the following:

1. Add [Sites.Selected](https://learn.microsoft.com/en-us/graph/permissions-reference#sitesselected) SharePoint permission.

   Note

   You should see *Sites.Selected* in both Microsoft Graph and SharePoint permissions.
2. [Generate a key pair](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-self-signed-certificate).
   Alternatively, you can create a self-signed certificate with *openssl* by running the following command:

   Copy code

   ```
   openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365
   ```

   Note

   The command above doesn’t encrypt the generated private key. Remove the *-nodes* argument if you want to generate an encrypted key.
3. [Attach the certificate](https://learn.microsoft.com/en-us/graph/applications-how-to-add-certificate?tabs=http) to the Microsoft Graph application.

## Query the Cortex Search service

You can use the [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) service to build chat
and search applications to chat with or query your documents in SharePoint.

After you install and configure the connector and it begins
ingesting content from Sharepoint, you can query the Cortex Search service.
For more information about using Cortex Search, see [Query a Cortex Search service](/user-guide/snowflake-cortex/cortex-search/query-cortex-search-service).

**Filter responses**

To restrict responses from the Cortex Search service to documents that a specific user
has access to in SharePoint, you can specify a filter containing the user ID or email address of the user
when you query Cortex Search. For example, `filter.@contains.user_ids` or `filter.@contains.user_emails`.
The name of the Cortex Search service created by the connector is `search_service` in the schema `Cortex`.

Run the following SQL code in a SQL worksheet to query
the Cortex Search service with files ingested from your SharePoint site.

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

**For all connectors:**

| Column name | Type | Description |
| --- | --- | --- |
| `full_name` | String | A full path to the file from the Sharepoint site documents root. Example: `folder_1/folder_2/file_name.pdf`. |
| `web_url` | String | A URL that displays an original Sharepoint file in a browser. |
| `last_modified_date_time` | String | Date and time when the item was most recently modified. |
| `chunk` | String | A piece of text from the document that matched the Cortex Search query. |

Expand

Show lessSee more

**For ACL connectors only:**

| Column name | Type | Description |
| --- | --- | --- |
| `user_ids` | Array | An array of Microsoft 365 user IDs that have access to the document. It also includes user IDs from all the Microsoft 365 groups that are assigned to the document. To find a specific user ID, see [Get a user](https://learn.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http). |
| `user_emails` | Array | An array of Microsoft 365 user email IDs that have access to the document. It also includes user email IDs from all the Microsoft 365 groups that are assigned to the document. |

Expand

Show lessSee more

**Example: Query an AI assistant for human resources (HR) information**

You can use Cortex Search to query an AI assistant for employees to chat with the latest versions of
HR information, such as onboarding, code of conduct, team processes, and organization policies.
Using response filters, you can also allow HR team members to query employee contracts while adhering to access controls configured in SharePoint.

PythonREST API

Run the following code in a [Python worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create) to query the
Cortex Search service with files ingested from SharePoint.
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
service with files ingested from your SharePoint.
You will need to authentication through key pair authentication and OAuth to access the
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

Sample response:

```
{
  "results" : [ {
  "web_url" : "https://<domain>.sharepoint.com/sites/<site_name>/<path_to_file>",
  "chunk" : "Answer to the question asked."
  } ]
}
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
