# Set up the Openflow Connector for Microsoft Dataverse

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for Microsoft Dataverse.

## Prerequisites

1. Ensure that you have reviewed [About Openflow Connector for Microsoft Dataverse](/user-guide/data-integration/openflow/connectors/dataverse/about).
2. Ensure that you have [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) or [Set up Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs).
3. If using Openflow - Snowflake Deployments, ensure that you’ve reviewed [configuring required domains](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list)
   and have granted access to the required domains for the [Microsoft Dataverse](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-dataverse) connector.

## Get the credentials

As a Microsoft Dataverse administrator, perform the following steps:

1. Ensure you have a Dataverse Environment to work with, and you have
   access to that environment through
   <https://admin.powerplatform.microsoft.com/>.
2. Ensure that you have an application registered in Microsoft Entra ID in portal.azure.com. This application must have
   access to the tenant we have our Dataverse Environment available. To register the application follow
   [this guide](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/walkthrough-register-app-azure-active-directory).
3. Generate and store ClientID and Client Secret within that application.
4. Go to Power Apps Admin Center and configure your Dataverse Environment to be accessed via applications registered before.
   To do that, go to **Manage** » **Environments** and select the environment to configure. Then go to
   **Settings** » **Users & permissions** » **Application users**. Previously created applications
   must be added and granted with privileges necessary to read data from Microsoft Dataverse.
5. Copy and save the Environment URL of the selected Dataverse
   Environment from <https://admin.powerplatform.microsoft.com/>.

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

Note

If you’re deploying the connector in Openflow - BYOC Deployments and using the `KEY_PAIR` authentication
strategy instead of the recommended `SNOWFLAKE_MANAGED`, you’ll also grant this same execute-as
role to a service user rather than relying on the runtime’s managed token. See
[Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth)
to create the service user.

## Set up the connector

As a data engineer, perform the following tasks to install and configure the connector:

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

### Configure the connector

1. Right-click on the imported process group and select **Parameters**.
2. Populate the required parameter values as described in [Flow parameters](#flow-parameters).

### Flow parameters

This section describes the flow parameters that you can configure based on the following parameter contexts:

- [Dataverse Source Parameters](#dataverse-source-parameters): Used to establish connection with Dataverse.
- [Dataverse Destination Parameters](#dataverse-destination-parameters): Used to establish connection with Snowflake.
- [Dataverse Ingestion Parameters](#dataverse-ingestion-parameters): Used to define the configuration of data downloaded from Dataverse.

#### Dataverse Source Parameters

| Parameter | Description |
| --- | --- |
| Source Dataverse Environment URL | The main identifier of a source system to fetch data. The URL indicates a namespace where Dataverse tables exist. It also lets you create a scope parameter for OAuth. |
| Source Tenant ID | Microsoft Azure Tenant ID. It’s used to create OAuth URLs. Microsoft Dataverse Environment must belong to this tenant. |
| Source OAuth Client ID | Microsoft Azure Client ID used to access Microsoft Dataverse API. [Microsoft Dataverse Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) uses OAuth authentication to secure access, and the connector uses the client credentials flow. To learn about client ID and how to find it in Microsoft Entra, see [Application ID (client ID)](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#application-id-client-id). |
| Source OAuth Client Secret | Microsoft Azure Client Secret used to access Microsoft Dataverse API. [Microsoft Dataverse Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) uses OAuth authentication to secure access, and the connector uses the client credentials flow. To learn about client secret and how to find it in Microsoft Entra, see [Certificates & secrets](https://learn.microsoft.com/en-us/azure/healthcare-apis/register-application#certificates--secrets). |

Expand

Show lessSee more

#### Dataverse Destination Parameters

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

#### Dataverse Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Ingestion Schedule Interval | Interval used as the triggering interval for the processor that fetches the list of tables and initializes ingestion. The default is `300 s`. |
| Source Tables Filter Strategy | Strategy for filtering tables to be ingested. Can be one of REGEXP and LIST. |
| Source Tables Filter Value | Value of the tables filter. When Source Tables Filter Strategy is set to REGEXP - this is the regular expression to be matching selected tables. When LIST is provided, then it is a comma separated list of table names. |
| Column Filter JSON | Optional. A JSON array specifying per-table column filters. Columns can be included or excluded by name (`included`, `excluded`) or by regular expression pattern (`includedPattern`, `excludedPattern`). The `table` value must be the **singular logical entity name** (e.g., `annotation`), not the plural entity set name used in `Source Tables Filter Value` (e.g., `annotations`). For example: `[ {"table": "mytable", "excluded": ["binarycolumn", "binarycolumn_binary"]} ]` excludes large binary columns from `mytable`. See [Replicate a subset of columns in a table](#replicate-a-subset-of-columns-in-a-table) for full details. |
| Max Page Size | Number of records fetched from a Dataverse table in a single request. It can’t be larger than 5000. A higher value can increase ingestion speed, but it can also cause timeouts. The default is `1000`. |
| Merge Task Schedule CRON | CRON expression that defines when data is merged from the journal table into the destination table. The default is `* * * * * ?`, which merges continuously. Use a narrower schedule to reduce how long the warehouse runs. For example, `* 0 * * * ?` merges for one minute at the top of every hour. |
| Include Formatted Values | Optional. Whether the connector also fetches Dataverse formatted values and writes them to the `_DATAVERSE_FORMATTED_VALUES` column of the destination table. The default is `false`. See [Include formatted values](#label-include-formatted-values). |

Expand

Show lessSee more

Note

When configuring `Source Tables Filter Value`, use the **entity set name** (plural form,
e.g., `annotations`) rather than the table name displayed in the Microsoft Dataverse
interface. To find the entity set name for a table, go to
[Power Apps](https://make.powerapps.com), select **Tables**, find your table,
then select **Advanced** » **Tools** » **Copy set name**.

The `Column Filter JSON` parameter uses a different naming convention — it requires the
**singular logical entity name** (e.g., `annotation`). See
[Replicate a subset of columns in a table](#replicate-a-subset-of-columns-in-a-table) for details.

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

### Replicate a subset of columns in a table

The connector can filter the data replicated per table to a subset of configured columns.

To apply filters to columns, set the `Column Filter JSON` parameter in the Dataverse ingestion parameters to a JSON filter.
Add an array of configurations, one entry for every table to which you want to apply a filter.

Important

The `table` field must use the **singular logical entity name** (e.g., `annotation`),
not the plural entity set name used in `Source Tables Filter Value` (e.g., `annotations`).
To find the logical entity name in Power Apps, go to [Power Apps](https://make.powerapps.com),
select **Tables**, find your table, then select **Advanced** » **Tools**
» **Copy logical name**.

Some columns have a binary representation stored under a `_binary`-suffixed column name
(for example, a column `mycolumn` may also appear as `mycolumn_binary`). To fully
exclude such a column, list both names in the `excluded` array.

The following example excludes large binary columns from a table:

Copy code

```
[
    {
        "table": "mytable",
        "excluded": ["mycolumn", "mycolumn_binary"]
    }
]
```

Columns can be included or excluded by name or pattern. You can apply a single condition per table,
or combine multiple conditions, with exclusions taking precedence over inclusions.

The following example shows all available fields. The `table` field is mandatory. One or
more of `included`, `excluded`, `includedPattern`, `excludedPattern` is required.

Copy code

```
[
    {
        "table" : "<singular logical entity name>",
        "included": ["<column name>", "<column name>"],
        "excluded": ["<column name>", "<column name>"],
        "includedPattern": "<regular expression>",
        "excludedPattern": "<regular expression>",
    }
]
```

### Include formatted values

Microsoft Dataverse stores many columns as raw values, such as an option set integer, a
lookup GUID, or an unformatted amount. For those columns, Dataverse can also return a
display value, called a formatted value: the localized label of a choice, yes/no, status,
or status reason column, the primary name of a lookup or owner column, and locale-formatted
numbers, currencies, and dates. For details about which columns have formatted values, see
[Select columns using OData](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query/select-columns)
in the Microsoft documentation.

By default, the connector replicates raw values only. To also replicate formatted values,
set the `Include Formatted Values` parameter in the Dataverse ingestion parameters to
`true`, then restart the connector process group so that the change takes effect.

Raw columns are unchanged when you enable this parameter. Instead, the connector adds a
single `_DATAVERSE_FORMATTED_VALUES` column of type `OBJECT` to each replicated table. The
keys of the object are source column names and the values are always strings:

Copy code

```
{
  "statuscode": "Active",
  "annualincome": "$80,000.00",
  "_transactioncurrencyid_value": "US Dollar"
}
```

Keep the following in mind when you query the column:

- Lookup and owner columns keep the `_<column>_value` form that Dataverse uses, as shown by
  `_transactioncurrencyid_value` in the preceding example.
- Columns that don’t have a formatted value are absent from the object. If a row has no
  formatted values at all, `_DATAVERSE_FORMATTED_VALUES` is `NULL` for that row.
- Rows that were deleted at the source don’t carry formatted values. For more information about
  how deletes are replicated, see
  [Connector-managed columns](/user-guide/data-integration/openflow/connectors/dataverse/about#label-dataverse-connector-managed-columns).
- If you enable the parameter for a connector that already replicated data, the column is
  populated from the next ingestion onwards. Rows that were replicated earlier keep `NULL`
  until they change at the source again.
- If a source table already has a column named `_DATAVERSE_FORMATTED_VALUES`, ingestion of
  that table fails.

To read a single formatted value, extract it by key and cast it:

Copy code

```
SELECT
    "statuscode",
    _DATAVERSE_FORMATTED_VALUES:statuscode::STRING AS statuscode_label
  FROM <destination_database>.<destination_schema>.ACCOUNTS;
```

Dataverse column names are lowercase, so quote them in queries. The connector-managed columns
are uppercase and don’t need quoting.

Note

Formatted values are display strings that depend on the locale and configuration of your
Dataverse environment, so they can change without the underlying data changing. Use the raw
columns for joins, filters, and calculations, and use formatted values for presentation.

### Manage table state

The connector maintains per-table ingestion state in the `Dataverse Table State Service`
controller service. Each entry records the current ingestion status and the delta token
used for change tracking.

#### View connector state

To view the current state of all tables:

1. Right-click on the canvas and select **Controller services**.
2. Locate the controller service named **Dataverse Table State Service**.
3. In the **Dataverse Table State Service** menu, click **View state**.

The state is a set of key/value pairs where the key is the table entity set name
(for example, `accounts`). The value has the format
`<STATUS>;<deltaToken>;<skipToken>;<staleFlag>`, for example:

```
accounts -> DONE;!AAAAAjE...;;
```

The `STATUS` can be one of the following:

- `FETCHING` — the connector is actively fetching records for this table.
- `PROCESSING` — the table is queued for ingestion but not currently being fetched.
- `DONE` — all available data was fetched successfully. The connector will check for new data on the next scheduled run according to the **Ingestion Schedule Interval** parameter.
- `FAILED` — an unrecoverable error occurred. Review the connector logs for details. If the logs indicate a configuration issue or a [known limitation](/user-guide/data-integration/openflow/connectors/dataverse/about#limitations), resolve it and restart ingestion for the affected table. If no known cause is found, this may indicate a bug or an unsupported scenario; contact Snowflake Support.

#### Restart ingestion for a single table

Removing a table from the filter and re-adding it causes the connector to perform a full
re-ingestion of that table. All currently available records are fetched again and merged
into the destination table by primary key, so existing rows are updated in place rather
than duplicated. However, the connector doesn’t recover delete operations that occurred
during downtime.

To restart ingestion for a specific table:

1. Make sure the connector is running and open the connector process group.
2. Right-click on the canvas, select **Parameters** and remove the target table’s entity
   set name from the **Source Tables Filter Value** parameter.
3. Stop the **List Dataverse Tables** processor and start it again to trigger removal of the table state.
4. Wait until the table’s state has been removed:

   1. Right-click on the canvas and select **Controller services**.
   2. Locate the controller service named **Dataverse Table State Service** and select **View state** from its ellipsis menu.
   3. Wait until the table’s entity set name no longer appears in the list.
5. Stop the **List Dataverse Tables** processor and wait until all queues are empty.
6. (Optional) DROP the destination objects in Snowflake and let the connector recreate them.

   Since a full re-ingestion only upserts records that currently exist at the source, rows deleted
   at the source during downtime are not removed from the destination table automatically.
   After you delete the destination table and re-ingest it, the table includes only records that are
   still present in the source.

   DROP the following objects, where `<TABLE>` is the table’s entity set name in uppercase:

   - Destination table: `<destination_database>.<destination_schema>.<TABLE>`
   - Journal table: `<destination_database>.<destination_schema>.<TABLE>__JOURNAL`
   - Journal stream: `<destination_database>.<destination_schema>.<TABLE>__JOURNAL_STREAM`

   Copy code

   ```
   DROP STREAM IF EXISTS <destination_database>.<destination_schema>.<TABLE>__JOURNAL_STREAM;
   DROP TABLE IF EXISTS <destination_database>.<destination_schema>.<TABLE>__JOURNAL;
   DROP TABLE IF EXISTS <destination_database>.<destination_schema>.<TABLE>;
   ```
7. Re-add the table’s entity set name to **Source Tables Filter Value** and start the
   **List Dataverse Tables** processor again.
8. Verify that an entry for the table is present in **Dataverse Table State Service** state again.

Note

To restart ingestion for all replicated tables, repeat this procedure for each table, or remove all
entity set names from the **Source Tables Filter Value** parameter and then re-add them.

Do not delete FlowFiles manually while the connector is running. Doing so can leave a table in the
`FETCHING` status indefinitely. If this occurs, restart ingestion for that table as described above.
