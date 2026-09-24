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

   - [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs)
   - [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc)
3. If you are using Openflow - Snowflake Deployments, ensure that you have reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list) and have granted access to the required domains for the [BigQuery](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-bigquery) connector.
4. You have access to the Openflow admin role or similar role you use to manage Openflow.
5. If you’re deploying in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication strategy, you have created key pair authentication. For more information, see [key-pair authentication](/user-guide/key-pair-auth).

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

As an Openflow administrator, perform the following tasks for this connector. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant these privileges to that role.

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

1. Create a database to store the replicated data, and grant the execute-as role
   [USAGE and CREATE SCHEMA](/user-guide/security-access-control-privileges#label-database-privileges) on it. The connector creates
   destination schemas automatically. Snowflake recommends a dedicated destination database per
   connector, to avoid collisions with other data sources including other connectors.

   Keep this destination database separate from the database that holds your Openflow
   infrastructure objects, such as the runtime, the connector, and any secrets. A connector
   creates destination objects based on the source schema and table names, so those names aren’t
   under your control and can change as the source changes.

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS <destination_database>;

   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
2. Designate a warehouse for the connector to use, and grant the execute-as role **USAGE** and
   **OPERATE** on it. Start with the `XSMALL` warehouse size, then experiment with size depending
   on the number of tables being replicated, and the amount of data transferred. Large table
   numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than the warehouse size.

   Copy code

   ```
   CREATE WAREHOUSE <ingest_warehouse>
     WITH
       WAREHOUSE_SIZE = 'XSMALL'
       AUTO_SUSPEND = 300
       AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <ingest_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
3. **Snowflake deployments only:** Make sure this connector’s source host and port are permitted
   by a network rule that your runtime’s external access integration (EAI) allows.

   The EAI itself belongs to the runtime, not to this connector. You create it once, attach it to
   the runtime, and grant the execute-as role `USAGE` on it. For those steps, see
   [Creating network rules and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-network-rules-and-external-access-integrations).
   What is specific to this connector is getting its source host into a rule that EAI references.

   The rule takes the source’s host and port as a single value, such as `db.example.com:<port>`.
   That’s the host and port from the connector’s connection URL, without the `jdbc:` scheme, the
   driver name, or the database path.

   BYOC deployments handle outbound connectivity in the cloud environment and don’t use EAIs or
   network rules.

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
| Snowflake Authentication Strategy | Use `SNOWFLAKE_MANAGED` as the value for Authentication Strategy for both Openflow - Snowflake Deployments and Openflow - BYOC Deployments. Alternatively, if you’re deploying in Openflow - BYOC Deployments, you can use `KEY_PAIR`.  **Example:** `SNOWFLAKE_MANAGED` |
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
