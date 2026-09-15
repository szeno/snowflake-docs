# Setting Up the Openflow Connector for Google BigQuery

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Google BigQuery.

## Prerequisites

1. Review [About the Openflow Connector for Google BigQuery](/user-guide/data-integration/openflow/connectors/google-big-query/about).
2. Set up your runtime deployment.

   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
   - [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
3. If you are using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the [domains](#label-of-bq-req-domains) required by the connector.
4. You have access to the Openflow admin role or similar role you use to manage Openflow.
5. If you are creating a Snowflake service user to manage the connector, you have created a key pair authentication. For more information, see [key-pair authentication](/user-guide/key-pair-auth).

## Required endpoints

The following endpoints are required for the connector to function:

- `bigquery.googleapis.com:443`
- `bigquerystorage.googleapis.com:443`
- `oauth2.googleapis.com:443`

If you are using Openflow - BYOC, you need to configure your cloud network egress to allow TLS 443 access to the endpoints listed above.
If you are using Openflow - Snowflake Deployments, you need to create a network rule and an external access integration (EAI). Then, grant the execute-as role usage privileges on the EAI.

## Set up BigQuery

1. Create a Google Cloud Service account and grant it the necessary permissions to read BigQuery data. The connector uses this account for authentication.

   This account must have the following permissions:

   - [BigQuery User](https://docs.cloud.google.com/bigquery/docs/access-control#bigquery.user)
   - [BigQuery Data Editor](https://docs.cloud.google.com/bigquery/docs/access-control#bigquery.dataEditor)

> Important
>
> `BigQuery Data Editor` must be granted at the **project level**, not at individual datasets.
> The connector queries `{project}.{region}.INFORMATION_SCHEMA.TABLES` to discover tables
> across all configured regions - a region-scoped view that requires project-level access. The
> connector also queries `{project}.{dataset}.INFORMATION_SCHEMA.KEY_COLUMN_USAGE` to
> determine primary keys for each replicated table. Without project-level access, the query
> fails with a `Access Denied` error and the connector does not run correctly.

1. Generate and download the corresponding JSON key file for the service account. You will need the full contents of this file for the connector’s configuration.
2. Enable change history on each source table to allow the connector to perform incremental replication. This feature allows BigQuery to track row-level changes (inserts, updates, and deletes), which the connector uses to sync data efficiently.

   Run the following query in the BigQuery console for each table:

   Copy code

   ```
   ALTER TABLE `project.dataset.table`
   SET OPTIONS (enable_change_history = TRUE);
   ```

## Set up your Snowflake account

As an Openflow administrator, perform the following tasks to set up your Snowflake account:

1. Create a Snowflake service user:

   Copy code

   ```
   USE ROLE USERADMIN;
   CREATE USER <openflow_service_user>
     TYPE=SERVICE
     COMMENT='Service user for Openflow automation';
   ```
2. Store the private key for that user in a file to supply to the connector’s configuration. For more information, see [key-pair authentication](/user-guide/key-pair-auth).

   Copy code

   ```
   ALTER USER <openflow_service_user> SET RSA_PUBLIC_KEY = '<pubkey>';
   ```
3. Create a database that stores the replicated data, and set up permissions for the
   Snowflake user to create objects in that database by granting USAGE and CREATE SCHEMA privileges.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CREATE DATABASE IF NOT EXISTS <destination_database>;
   GRANT USAGE ON DATABASE <destination_database> TO USER <openflow_service_user>;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO USER <openflow_service_user>;
   ```
4. Create a new warehouse or use an existing warehouse for the connector.

   To create a new warehouse:

   Copy code

   ```
   CREATE WAREHOUSE <openflow_warehouse>
   WITH
   WAREHOUSE_SIZE = 'MEDIUM'
   AUTO_SUSPEND = 300
   AUTO_RESUME = TRUE;
   GRANT USAGE, OPERATE ON WAREHOUSE <openflow_warehouse> TO USER <openflow_service_user>;
   ```

   Start with the MEDIUM warehouse size, then experiment with size depending on the amount of tables being replicated, and the amount of data transferred.

   To determine if you should increase, monitor the connector and database while data replication is in progress. If you observe significant delays during incremental replication, experiment with a larger warehouse size. However large table numbers typically scale better using [multi-cluster warehouses](/user-guide/warehouses-multicluster) instead of increasing the warehouse size.
5. Create an external access integration to enable network access outside of Snowflake.

   Caution

   If your runtime executes in Openflow - BYOC, you do not need to create an External Access Integration (EAI). Instead, configure your cloud network egress to allow TLS 443 access to the endpoints listed below.

   Required host:port endpoints are listed in [Required endpoints](#label-of-bq-req-domains).

   To allow the connector to call the required Google APIs from a Snowflake-hosted runtime, you must create a network rule and an external access integration (EAI). Then, grant the execute-as role usage privileges on the EAI.

   To create the external access integration and network rule and grant access, perform the following steps:

   1. Create a network rule to allow the connector to access the required Google APIs:

      Copy code

      ```
      USE ROLE ACCOUNTADMIN;
      USE DATABASE <openflow_network_db>;

      CREATE OR REPLACE NETWORK RULE openflow_<runtime_name>_network_rule
        TYPE = HOST_PORT
        MODE = EGRESS
        VALUE_LIST = (
          'bigquery.googleapis.com:443',
          'bigquerystorage.googleapis.com:443',
          'oauth2.googleapis.com:443'
        );
      ```
   2. Create an External Access Integration that references the network rule:

      Copy code

      ```
      CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION openflow_<runtime_name>_eai
        ALLOWED_NETWORK_RULES = (openflow_<runtime_name>_network_rule)
        ENABLED = TRUE;
      ```
   3. Grant your execute-as role USAGE on the integration:

      Copy code

      ```
      GRANT USAGE ON INTEGRATION openflow_<runtime_name>_eai
        TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
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

1. Right-click on the added runtime and select **Parameters**.
2. Populate the required parameter values as described in [Specify flow parameters](#label-specify-bq-connector-flow-parameters).

### Specify flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [BigQuery Source Parameters](#bigquery-source-parameters): Used to define the configuration for reading data from BigQuery.
- [BigQuery Destination Parameters](#bigquery-destination-parameters): Used to establish connection with Snowflake.
- [BigQuery Ingestion Parameters](#bigquery-ingestion-parameters): Used to specify the tables and views to replicate.

#### BigQuery Source Parameters

| Parameter | Description |
| --- | --- |
| BigQuery Project Name | The unique identifier of the Google Cloud Project that contains BigQuery datasets and tables.  Where to find: open BigQuery Studio (Google Cloud Console > BigQuery) and in the left Explorer pane hover over your project to see the Project ID.  **Example:** `example-team-gcp` |
| GCP Service Account JSON | The entire content of the JSON key file for the Google Cloud Platform Service Account used for authentication. Ensure the service account has the necessary IAM permissions to perform BigQuery operations, such as the BigQuery Job User and BigQuery Data Viewer roles.  Where to get it: Google Cloud Console > IAM & Admin > Service Accounts > select the service account > Keys tab > Add key > Create new key > JSON. This downloads a .json file—open it and paste the entire file content (including braces) into this field. |

Expand

Show lessSee more

#### BigQuery Destination Parameters

| Parameter | Description |
| --- | --- |
| Snowflake Authentication Strategy | When using SPCS, use `SNOWFLAKE_MANAGED` as the value for Authentication Strategy. When using BYOC, use `KEY_PAIR` as the value for Authentication Strategy.  **Example:** `KEY_PAIR` |
| Snowflake Account Identifier | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Snowflake account name where data will be persisted. |
| Destination Database | The name of the destination database to replicate into. Mixed case is supported. |
| Snowflake Private Key File | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: The private key file must be blank. - `KEY_PAIR`: Upload the file that contains the RSA private key used for authentication to Snowflake, formatted according to PKCS8 standards and including standard PEM headers and footers. The header line begins with `-----BEGIN PRIVATE`. To upload the private key file, select the Reference asset checkbox. |
| Snowflake Private Key Password | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Provide the password associated with the Snowflake Private Key File. |
| Snowflake Role | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it). You can find your execute-as role in the Openflow UI by navigating to View Details for your runtime. - `KEY_PAIR` Authentication Strategy: Use a valid role configured for your service user. |
| Snowflake Username | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Provide the user name used to connect to the Snowflake instance. |
| Snowflake Warehouse | The name of the warehouse to use by the connector. |

Expand

Show lessSee more

#### BigQuery Ingestion Parameters

| Parameter | Description |
| --- | --- |
| BigQuery Regions | Specifies a comma-separated list of the locations to query for BigQuery datasets. You can combine both regional and multi-regional locations in the same list.  **Example:** `us,eu,us-west1` |
| Included Dataset Names | Comma-separated list of datasets to replicate (queried across all selected regions).  **Example:** `sales_data,marketing_leads` |
| Included Dataset Names Regex | Regular expression for specifying dataset names to replicate (queried across all selected regions). Combined with the Included Dataset Names to include any matching dataset. Note: REGEXP expression should match Google’s RE2 syntax.  **Example:** `^sales_.*` |
| Included Table Names | Comma-separated list of tables to replicate across datasets.  **Example:** `transactions,customers` |
| Included Table Names Regex | Regular expression for specifying table names to replicate across datasets. Combined with the Included Table Names to include any matching table. Note: REGEXP expression should match Google’s RE2 syntax.  **Example:** `^revenue_.*` |
| Included View Names | Comma-separated list of views to replicate across datasets.  **Example:** `customer_summary,revenue_report` |
| Included View Names Regex | Regular expression for specifying view names to replicate across datasets. Combined with the Included View Names to include any matching view. Note: REGEXP expression should match Google’s RE2 syntax.  **Example:** `^report_.*` |
| Incremental Sync Frequency | How often the connector runs incremental synchronization for each table. Runs do not overlap if a cycle takes longer than the configured interval, the next run waits for the prior one to finish. Because BigQuery limits max size of window to 24h, schedule must be more frequent than this value.  **Example:** `10m` |
| View Sync Frequency | How often the connector runs synchronization for each view. Runs do not overlap, if a cycle takes longer than the configured interval, the next run waits for the prior one to finish. View ingestion does not support CDC, only truncate and load.  **Example:** `1h` |
| Temporary Table Dataset | Dataset in which necessary temporary tables are created, such as CDC journal tables or temporary tables for view ingestion. Snowflake recommends having a separate dataset for temporary tables and not using the ingested dataset for this purpose.  **Example:** `openflow_temp` |

Expand

Show lessSee more

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## Next steps

- For information on tasks you can perform after installing the connector, see
  [Use the connector](/user-guide/data-integration/openflow/connectors/google-big-query/use)
- For information on monitoring the flow, see
  [Monitor the flow](/user-guide/data-integration/openflow/monitor)
