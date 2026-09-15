# Openflow Connector for Salesforce Bulk API: Configure the connector

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to configure the Openflow Connector for Salesforce Bulk API.

## Install the connector

Follow these steps to install the Openflow Connector for Salesforce Bulk API in an Openflow runtime:

1. Navigate to the **Connector library** tab in Openflow.
2. On the Openflow connectors page, find **Openflow connector for Salesforce Bulk API** and select **Install**.
3. In the **Select runtime** dialog, select your runtime from the **Available runtimes** drop-down.

The Openflow canvas appears with the connector process group added to it.

## Configure the connector

To configure the connector, perform the following steps:

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in the table below.

| Parameter | Description |
| --- | --- |
| Column Removal Strategy | Defines the strategy to adopt when a column should be removed in the destination table based on the latest received schema. Three possible values: `Drop Column`, `Rename Column`, `Ignore Column`.   - `Drop Column`: Drop the column from the Snowflake table. - `Rename Column`: Rename the column in the Snowflake table. - `Ignore Column`: Ignore the column, leaving it as is in the Snowflake table. |
| Connected App Key | The private key used for JWT Bearer Flow authentication with Salesforce. Copy-paste the content of the `private.key` file generated during the [Salesforce setup](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-salesforce). This private key must correspond to the public certificate (`public.crt`) uploaded to the external client app in Salesforce. You can also use the next parameter to upload the private key file instead. |
| Connected App Key File | Upload the `private.key` file by selecting the **Reference asset** checkbox, then upload the file as an asset and select the asset as the value for the parameter. This is an alternative to pasting the key content in the **Connected App Key** parameter. |
| Connected App Key Password | Password set on the private key file during the [Salesforce setup](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/setup-salesforce) steps. |
| Destination Database | Name of the database in Snowflake where the Salesforce data will be replicated. The database must exist before starting the connector. |
| Destination Schema | Name of the schema, in the database above, into which the connector will create tables for the Salesforce data to be added. The schema must exist before starting the connector. |
| Enable Capture Blob Fields | If set to `true`, fields of type `base64` (binary fields such as `Attachment.Body` and `ContentVersion.VersionData`) are fetched by the connector. The objects that contain blob fields must be listed in the **Special Objects Filter** parameter (Non-Bulk API path). Default: `false`. See [Configure blob field ingestion](#blob-fields) for details. |
| Enable Journal Tables | If set to `true`, a `JOURNAL_<Object Name>` table is created for each synced object that has a `SystemModstamp` or `LastModifiedDate` field. All changes are appended to the journal table, providing a full history of modifications. This is in addition to the main table that contains the merged data for the object. If a full reload occurs for a given object type, its journal table is also recreated. Default: `false`. |
| Enable Merge Metrics | If set to `true`, the connector runs an additional query to count records that are added, updated, deleted, or restored during replication. The additional query uses the **Snowflake Warehouse** and applies only to objects that include the `IsDeleted` field. The connector writes the counts to logs in the event table. Default: `false`. See [Monitor the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/monitor). |
| Enable Views Creation | If set to `true`, a view named `<Object Type>_FORMULA_VW` is created for each synced object that contains formula fields. The view translates supported Salesforce formula expressions into Snowflake SQL, allowing you to query formula results directly without replicating formula field values from Salesforce. See  for details. Default: `false`. |
| Filter | Comma-separated list of objects to replicate from Salesforce, or regular expression to apply against all existing objects. The filter is case-insensitive, meaning that a filter set to `account` would match the object type `Account`. Example: `Account, Opportunity, Contact`.  Note  If left empty, all objects will be replicated. This is not recommended as there are usually thousands of objects in a Salesforce instance. |
| Incremental Offload | Whether the processor should perform incremental offload. If `true`, the processor will only fetch the records that have been modified since the last query job submission by using a `WHERE` clause on the appropriate timestamp field. If `false`, all records will be fetched at every execution of the connector. |
| Initial Load Chunking | If set to a value other than `NONE`, the initial data load will be split into multiple jobs based on this interval. On the first run for an object, the connector will query Salesforce to find the oldest record and use that as the starting point. Each subsequent job will query the next time chunk until caught up to the current time. Set to one of: `NONE`, `MONTHLY`, `QUARTERLY`, `YEARLY`.  This is useful for large datasets where loading all historical data in a single query may time out, exceed API limits, or exceed the storage size of the content repository of the runtime. After catching up, the processor continues with normal incremental offload behavior. |
| Iceberg Version | Only applicable when **Table Storage Format** is set to `ICEBERG` (preview). Specifies the Iceberg version for the destination Iceberg table. Supported values are `2` and `3`. Default: `3`. Don’t change this value after ingestion begins. For setup instructions, see [Openflow Connector for Salesforce Bulk API: Iceberg table destinations](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/iceberg). |
| OAuth2 Audience | Audience to set in the JWT token. Set to `https://login.salesforce.com` for production environments or `https://test.salesforce.com` for sandboxes and test environments. |
| OAuth2 Client ID | Should be set to the **Consumer Key** value retrieved during the Salesforce Setup steps. |
| OAuth2 Subject | Should be set to the username of an admin-approved user on whose behalf the application interacts with Salesforce APIs. |
| OAuth2 Token Endpoint URL | Endpoint to negotiate tokens via the JWT Bearer Flow. Example: `https://myCompany.my.salesforce.com/services/oauth2/token`. |
| Object Fields Filter JSON | A JSON specifying which fields and field patterns should be included or excluded, per Salesforce object. Takes the form of an array with one item per object.  Example 1: This will include all fields that end with ‘name’ in the ‘Account’ Salesforce object:  `[ {"objectType":"Account", "includedPattern":".*name"} ]`  Example 2: This will include the fields Id, Name, and Revenue in the ‘Account’ Salesforce object:  `[ {"objectType":"Account", "included": ["Id", "Name", "Revenue"]} ]`  `excluded` and `excludedPattern` are also available for configuring the filters. |
| Object Identifier Resolution | Determines whether schema/table/column names are treated as case-sensitive or case-insensitive. One of: `CASE_INSENSITIVE` / `CASE_SENSITIVE`.  Note  Changing this parameter value will require clearing the state and doing a full reload of all objects. |
| Removed Column Name Suffix | Suffix added to the column name when the parameter **Column Removal Strategy** is set to `Rename Column`. Default: `__deleted`. |
| Run Schedule | Frequency at which the connector will check for updates in Salesforce for configured objects via the **Filter** parameter. Default: `15 minutes`. |
| Salesforce Instance | Hostname of the Salesforce instance including the domain name. Do not include the protocol prefix (`https://`). For example, use `myCompany.my.salesforce.com`. |
| Snowflake Account Identifier | Snowflake account name formatted as `[organization-name]-[account-name]` where data will be persisted. Example: `PM-CONNECTORS`. |
| Snowflake Username | The name of the service user that the connector uses to connect to Snowflake. The service user is required only when using the `KEY_PAIR` authentication strategy (Openflow BYOC only). |
| Snowflake Private Key | The RSA Private Key that the connector uses for authentication to Snowflake, formatted according to PKCS8 standards and including standard PEM headers and footers. The header line starts with `-----BEGIN PRIVATE`. This is required only when using the `KEY_PAIR` authentication strategy (Openflow BYOC only).  You may also use the next parameter to upload the private key to the Openflow runtime instead. |
| Snowflake Private Key File | The file containing the RSA Private Key that the connector uses for authentication to Snowflake, formatted according to PKCS8 standards and including standard PEM headers and footers. The header line starts with `-----BEGIN PRIVATE`. Required only when using the `KEY_PAIR` authentication strategy (Openflow BYOC only).  Select the **Reference asset** checkbox to upload the private key file and store it securely in the Openflow runtime. |
| Snowflake Private Key Password | The password associated with the Snowflake Private Key File (if encrypted). This is required only when using the `KEY_PAIR` authentication strategy (Openflow BYOC only). |
| Snowflake Role | Name of the execute-as role used during query execution. When using `SNOWFLAKE_MANAGED`, this is the execute-as role for Openflow runtimes. When using `KEY_PAIR` (Openflow BYOC only), this is the role assigned to the specified Snowflake username. |
| Snowflake Authentication Strategy | Authentication strategy for the connector to connect to Snowflake.  Using `SNOWFLAKE_MANAGED` (default) uses the Snowflake managed token associated with the runtime’s execute-as role. If using Openflow BYOC, you can also use `KEY_PAIR` to specify a specific user and role via a custom Key Pair. |
| Snowflake Warehouse | The Snowflake warehouse used to run queries. |
| Special Objects Filter | Comma-separated list of objects to offload from Salesforce (using direct API access), or regular expression to apply against all existing objects. The filter is case-insensitive, meaning that a filter set to `account` would match the object type `Account`.  This filter should only be used for objects that are **not** supported by the Salesforce Bulk API, such as knowledge data. This parameter should not overlap with the parameter **Filter**.  Example: `Knowledge.*` |
| Table Storage Format | The storage format of the destination Snowflake table. Use `STANDARD` for standard Snowflake tables. The `ICEBERG` option, which writes to Apache Iceberg tables, is a preview feature. Default: `STANDARD`. Don’t change this value after ingestion begins. For setup instructions, see [Openflow Connector for Salesforce Bulk API: Iceberg table destinations](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/iceberg). |

Expand

Show lessSee more

## Verify the Salesforce connection

Before enabling and starting the connector, Snowflake recommends verifying that the Salesforce authentication is properly configured. The **Verification** feature on controller services lets you test the connection without starting the full connector flow.

The **JWT Bearer OAuth2 Access Token Provider** controller service depends on two other controller services that must be enabled first: the **Salesforce Private Key Service** and the **Web Client Service Provider**.

1. Double-click the connector process group to open it.
2. Right-click on an empty area of the canvas and select **Controller Services**.
3. Enable the **Salesforce Private Key Service** and the **Web Client Service Provider** services.
4. Locate the **JWT Bearer OAuth2 Access Token Provider** service in the list.
5. Click the **Verification** button for the service. A dialog opens where you can provide property overrides. You can ignore this and click **Verify** directly.
6. If everything is configured properly, the **Acquire token** step shows a green checkmark indicating success. This confirms the connector can authenticate with Salesforce and obtain an access token. You can proceed to the next step to run the connector.
7. If verification fails, review the error message and check the following:

   - The **OAuth2 Client ID** parameter matches the **Consumer Key** from the external client app in Salesforce.
   - The private key corresponds to the certificate uploaded to the external client app.
   - The **OAuth2 Subject** user is authorized for the external client app (see ).
   - The **OAuth2 Token Endpoint URL** uses the correct Salesforce instance hostname.
   - The **OAuth2 Audience** is set to the correct value: `https://login.salesforce.com` for production or `https://test.salesforce.com` for sandboxes.

   For detailed troubleshooting, see [Troubleshooting the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/troubleshoot).

## Run the connector

Follow these steps to start the connector and begin replicating data from Salesforce to Snowflake:

1. Right-click on an empty area in the canvas and select **Enable all Controller Services**.
2. Right-click on the connector process group and select **Start**.

## Manage object replication

After the connector has been started and objects have been replicated, you can add new objects or remove existing objects from replication.

### Add new objects to replication

To add a new object to replication, update the **Filter** parameter (or **Special Objects Filter** parameter, if applicable) with the new object names. You do not need to stop the connector. The new object is replicated at the next scheduled execution.

For example, if the current **Filter** value is `Account, Opportunity` and you want to add the `Contact` object, change the value to `Account, Opportunity, Contact`.

### Remove objects from replication

Removing an object from replication requires stopping the connector and cleaning up both the connector state and the destination table in Snowflake:

1. Stop all processors in the flow by right-clicking on the connector process group and selecting **Stop**.
2. Ensure that no in-flight FlowFiles are being processed.
3. Right-click on the canvas and select **Parameters**, then remove the object name from the **Filter** parameter (or the **Special Objects Filter** parameter, if applicable).
4. Right-click on the canvas and select **Disable all controller services**.
5. Go to **Controller services** and open the state of the controller service named **Salesforce Bulk Jobs State**.
6. Select the trash icon next to the object type you removed to delete its state entry.
7. Right-click on the canvas and select **Enable all controller services**, then start all processors to resume the connector.
8. If applicable, drop the corresponding table from the Snowflake destination database to clean up the previously replicated data. For example:

   Copy code

   ```
   DROP TABLE <database_name>.<schema_name>.<object_name>;
   ```

## Configure blob field ingestion

The Salesforce Bulk API 2.0 does not support binary (base64-encoded) fields. The
connector handles these fields through a dedicated Non-Bulk API path that uses the
Salesforce REST Query API. Objects with blob fields must be listed in the **Special
Objects Filter** parameter so they are routed to this path.

To enable blob field ingestion, set **Enable Capture Blob Fields** to `true` in the
connector parameters.

## Next steps

- To monitor replication activity and merge metrics, see [Monitor the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/monitor).
- To diagnose connector issues, see [Troubleshooting the Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/troubleshoot).
