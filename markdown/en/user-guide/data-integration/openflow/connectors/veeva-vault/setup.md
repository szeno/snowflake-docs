# Setting up the Openflow Connector for Veeva Vault

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Veeva Vault.

## Prerequisites

1. Review [About the Openflow Connector for Veeva Vault](/user-guide/data-integration/openflow/connectors/veeva-vault/about).
2. Set up your runtime deployment.

   - [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
3. If you are using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the [Veeva Vault](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-veeva-vault) connector.
   If you are using Openflow - BYOC Deployments, configure your cloud network egress to allow TLS 443 access to
   your Vault hostname (for example, `myvault.veevavault.com:443`).
4. You have access to the Openflow admin role or a similar role you use to manage Openflow.
5. If you’re deploying in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication strategy, you have created key pair authentication. For more information, see [key pair authentication](/user-guide/key-pair-auth).

## Set up Veeva Vault

The connector uses Direct Data API to retrieve data. Before you can use the
connector, your Vault administrator must complete the following tasks.

### Enable Direct Data

Direct Data must be enabled on your Vault. This is a Vault-level feature that
allows external systems to retrieve data exports via the Direct Data API.

To verify that Direct Data is enabled, your Vault administrator can check
**Admin** » **Settings** » **General Settings** » **Direct Data**
in the Veeva Vault UI.

For more information, see the [Direct Data API documentation](https://general.veevavault.dev/direct-data-api).

### Create a service account

Create a dedicated Veeva Vault user account for the connector. Refer to the
[Direct Data API permissions documentation](https://general.veevavault.dev/direct-data-api/references/direct-data-permissions) for configuring
this account.

Record the username and password for this service account. You need these values when configuring the connector.

Note

Snowflake recommends using a dedicated service account rather than a personal user account.
This ensures that the connector continues to function if a personal account is disabled or
its password is changed.

## Set up your Snowflake account

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

### Grant the privilege to create a pipe

The connector uses Snowpipe Streaming with high-performance architecture, which requires a `PIPE`
object. Grant the additional privilege needed to create it:

Copy code

```
GRANT CREATE PIPE ON SCHEMA <destination_database>.<destination_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
```

## Install the connector

To install the connector, do the following as a data engineer:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find the connector and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down list and click **Install**.

   Note

   Before you install the connector, ensure that you have created a database and schema in Snowflake for the connector to store ingested data.
4. Authenticate to the deployment with your Snowflake account credentials and select **Allow** when prompted to allow the runtime application to access your Snowflake account. The connector installation process takes a few minutes to complete.
5. Authenticate to the runtime with your Snowflake account credentials.

The Openflow canvas appears with the connector process group added to it.

## Configure the connector

To configure the connector, perform the following steps:

1. Right-click on the added connector process group and select **Parameters**.
2. Populate the required parameter values as described in the sections below.

### Veeva Vault parameters

| Parameter | Description |
| --- | --- |
| Veeva Vault Base URL | Base URL for the Veeva Vault environment. Must be a valid URL including the protocol.  **Example:** `https://myvault.veevavault.com` |
| Veeva Vault Username | Service account username for Veeva Vault authentication. |
| Veeva Vault Password | Service account password for Veeva Vault authentication. Stored securely as a sensitive parameter. |
| Veeva Vault Ingestion Mode | Determines how Direct Data files are consumed. Allowed values:   - `SNAPSHOT_AND_INCREMENTAL` (default): Load the latest full archive first, then continue with incremental archives. - `SNAPSHOT`: Poll for the latest full archive only. - `INCREMENTAL`: Poll for incremental archives only. |
| Veeva Vault Incremental Start Time | Optional starting timestamp for incremental polling. Only applicable when the ingestion mode is `INCREMENTAL`. If not set, incremental polling starts from the current time. Expected format: `yyyy-MM-dd'T'HH:mmZ`.  **Example:** `2025-01-15T08:30Z` |
| Veeva Vault Include Audit Logs | Whether to also ingest Direct Data audit log files.  **Default:** `true` |

Expand

Show lessSee more

### Snowflake destination parameters

| Parameter | Description |
| --- | --- |
| Snowflake Authentication Strategy | Authentication strategy for the connector to connect to Snowflake.   - `SNOWFLAKE_MANAGED` (default): Uses the Snowflake-managed token associated with the runtime’s execute-as role. This is the recommended strategy for both Openflow - Snowflake Deployments and Openflow - BYOC Deployments. - `KEY_PAIR`: Uses a user-provided RSA key pair. Available only on Openflow - BYOC Deployments, for cross-account scenarios where the connector writes to a Snowflake account different from the one hosting the Openflow runtime. |
| Snowflake Account | Snowflake account identifier, formatted as `<organization>-<account>`. Required when the authentication strategy is `KEY_PAIR`.  **Example:** `MYORG-MYACCOUNT` |
| Snowflake Username | The Snowflake user for authentication. Required when the authentication strategy is `KEY_PAIR`. |
| Snowflake Private Key | PEM-encoded private key content for Snowflake key pair authentication. Required when the authentication strategy is `KEY_PAIR`. This value is stored securely as a sensitive parameter.  You can also upload the private key file by selecting the **Reference asset** checkbox, uploading the file as an asset, and selecting the asset as the value for the parameter. |
| Snowflake Private Key Password | Password to decrypt the Snowflake private key, if the key is encrypted. Only applicable when the authentication strategy is `KEY_PAIR`. |
| Snowflake Role | The execute-as role used for table creation, data ingestion, and access verification. When using `SNOWFLAKE_MANAGED`, this is the execute-as role for Openflow runtimes. When using `KEY_PAIR`, this is the role assigned to the specified Snowflake user. |
| Snowflake Database | Name of the destination database in Snowflake. The database must already exist before starting the connector. |
| Snowflake Schema | Name of the destination schema in Snowflake. The schema must already exist before starting the connector. |
| Snowflake Warehouse | The Snowflake warehouse used for table management operations such as `CREATE TABLE` and `MERGE`. |
| Snowflake Table Prefix | Optional prefix applied to all destination table names in Snowflake. Use this to namespace tables when multiple connectors write to the same schema. |
| Snowflake Delete Strategy | How to apply Veeva delete extracts in Snowflake.   - `Hard Delete` (default): Permanently remove rows from the table. - `Soft Delete`: Set `__SNOWFLAKE_DELETED` to `TRUE` and `__SNOWFLAKE_DELETED_AT` to the current timestamp. The columns are added automatically if they don’t exist. |

Expand

Show lessSee more

### Schema evolution parameters

| Parameter | Description |
| --- | --- |
| Column Removal Strategy | Defines the strategy when a column should be removed from the destination table based on the latest received schema.   - `Drop Column` (default): Drop the column from the Snowflake table. - `Rename Column`: Rename the column in the Snowflake table by appending the suffix defined in the **Removed Column Name Suffix** parameter. - `Ignore Column`: Leave the column as-is in the Snowflake table. |
| Removed Column Name Suffix | Suffix appended to the column name when the **Column Removal Strategy** is set to `Rename Column`.  **Default:** `__deleted` |

Expand

Show lessSee more

## Run the flow

1. Right-click on an empty area of the canvas and select **Enable all Controller Services**.
2. Right-click on the connector process group and select **Start**.

The connector starts polling Veeva Vault for Direct Data files and loading data into
Snowflake.

## Next steps

- For information on tasks you can perform after installing the connector, see
  [Use the connector](/user-guide/data-integration/openflow/connectors/veeva-vault/use).
- For information on monitoring the flow, see
  [Monitor the flow](/user-guide/data-integration/openflow/monitor).
