# Install and configure the Openflow Connector for Oracle

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes the steps to install and configure the Openflow Connector for Oracle connector.

As a data engineer, perform the following tasks to install and configure the connector:

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

## Runtime sizing

For sizing guidance, including node type tiers and how to resize after creation,
see [Runtime sizing and packing for CDC connectors](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing).

For migration instructions, see [Reinstall the connector](/user-guide/data-integration/openflow/connectors/oracle/maintenance#label-oracle-reinstall-connector).

## Configure the connector

To configure the connector, do the following as a data engineer:

1. Right-click on the added runtime and select **Parameters**.
2. Populate the required parameter values.

   For more information on the required parameter values, see the following sections:

   - [Snowflake Destination Parameters](#label-oracle-snowflake-destination-parameters): Used to establish connection with Snowflake.
   - [Oracle Ingestion Parameters](#label-oracle-ingestion-parameters): Used to specify the tables to replicate.
   - [Oracle Source Parameters](#label-oracle-source-parameters): Used to define the configuration of data downloaded from Oracle.

To run multiple CDC connector instances on one runtime, see .

### Snowflake Destination Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Destination Database | The database where data is persisted. It must already exist in Snowflake and the connector’s role must have `USAGE` and `CREATE SCHEMA` on it. The name is case-sensitive. For unquoted identifiers, provide the name in uppercase. | Yes |
| Destination Schema Pattern | A pattern for the names of destination schemas where data is persisted. The connector creates the schemas if they don’t exist.  You can customize the pattern per ingested table using these optional variables:   - `${source.database.name}`: a source table’s database. - `${source.schema.name}`: a source table’s schema. - `${source.table.name}`: a source table’s name.   For example, for a table with the qualified name `source_db.tenant_a.data`, the pattern `prefix_${source.database.name}_${source.schema.name}` evaluates to `prefix_source_db_tenant_a`.  To ingest all tables into a single schema, provide a schema name without any variables, like `destination_schema`.  Important  Don’t change this setting after the connector has begun ingesting data. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. | Yes |
| Snowflake Authentication Strategy | When using:   - **Snowflake Openflow Deployment** or **BYOC**: Use SNOWFLAKE\_MANAGED.   This token is managed automatically by Snowflake.   BYOC deployments must have previously configured   [execute-as roles](/user-guide/data-integration/openflow/setup-openflow-byoc#label-deployment-byoc-setup-runtime-role) to use SNOWFLAKE\_MANAGED. - **BYOC**: Alternatively, BYOC can use KEY\_PAIR as the value for the authentication strategy. | Yes |
| Snowflake Account Identifier | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Snowflake account name formatted as [organization-name]-[account-name]. | Yes |
| Snowflake Connection Strategy | When using KEY\_PAIR, specify the strategy for connecting to Snowflake:   - **STANDARD** (default): Connect using standard public routing to Snowflake services. - **PRIVATE\_CONNECTIVITY**: Connect using private addresses associated with the supporting cloud platform such as AWS PrivateLink. | Required for BYOC with KEY\_PAIR only, otherwise ignored. |
| Snowflake Private Key | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank.   **KEY\_PAIR**: Must be the RSA private key used for authentication.  The RSA key must be formatted according to PKCS8 standards and have standard PEM headers and footers. Note that either a Snowflake Private Key File or a Snowflake Private Key must be defined. | No |
| Snowflake Private Key File | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: The private key file must be blank. - **KEY\_PAIR**: Upload the file that contains the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`.   To upload the private key file, select the **Reference asset** checkbox. | No |
| Snowflake Private Key Password | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the password associated with the Snowflake Private Key File. | No |
| Snowflake Role | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it).   You can find your execute-as role in the Openflow UI by navigating to **View Details** for your runtime. - **KEY\_PAIR**: Use a valid role configured for your service user. | Yes |
| Snowflake Username | When using:   - **SNOWFLAKE\_MANAGED** Authentication Strategy: Must be blank. - **KEY\_PAIR**: Provide the username used to connect to the Snowflake instance. | Yes |
| Oversized Value Strategy | Determines how the connector handles values that exceed its internal size limits (16 MB) during replication. Possible values are:  - **Fail Table** (default): The table is marked as permanently failed, and replication stops for that table. - **Set Null**: The value is replaced with `NULL` in the destination table.   Use this to prevent table failures when it is acceptable to lose data in tables beyond the oversized value. | No |
| Error Handling Strategy | Determines how the connector handles invalid rows that Snowflake rejects during ingestion. Possible values are:  - **Fail Table** (default): The table is marked as failed on the first invalid row, and replication stops for that table. - **Log Errors and Continue** : The connector keeps replicating the valid rows and records each rejected row in the table’s error table. | No |
| Table Storage Format | Standard Snowflake tables or Iceberg tables. Defaults to **STANDARD**. Don’t change after the connector starts. | Yes |
| Iceberg Version | The Iceberg table version, 2 or 3 (default 3). Ignored unless Table Storage Format is **ICEBERG**. Don’t change this value after ingestion begins. | No |
| Snowflake Warehouse | Snowflake warehouse used to run merge queries. Start with `XSMALL`; for many tables, a multi-cluster warehouse scales better than a larger size. | Yes |

Expand

Show lessSee more

### Oracle Ingestion Parameters

| Parameter | Description |
| --- | --- |
| Included Table Names | Comma-separated list of fully-qualified table paths. Tables must be specified using fully-qualified database, schema, and table name format: DATABASE\_NAME.SCHEMA\_NAME.TABLE\_NAME.  For example: `MYPDB.SALES.CUSTOMERS, MYPDB.SALES.ORDERS` |
| Included Table Regex | A regular expression to match table paths for automatic inclusion of existing and new tables. The regex pattern must match the three-part naming convention: DATABASE\_NAME.SCHEMA\_NAME.TABLE\_NAME.  For example: `MYPDB\.SALES\..*` to match all tables in the SALES schema within the MYPDB database. |
| Column Filter JSON | Optional. A JSON array of filter objects specifying which columns to include or exclude per table. For syntax details and examples, see [Replicate a subset of columns in a table](#replicate-a-subset-of-columns-in-a-table). |
| Table Key Configuration Service | Optional. A `MultiDatabaseJsonTableKeyConfigService` controller service that supplies a user-declared logical key for one or more tables. The service exposes a **Table Key Configuration JSON** property where you define the key mappings. When configured, the logical key takes the highest priority and overrides any primary key, unique constraint, or unique index that the connector would otherwise auto-detect.  For more information on when to use this and how to configure it, see [Specify a logical key for a table](#label-oracle-logical-key). |
| Merge Task Schedule CRON | CRON expression defining periods when merge operations from Journal to Destination Table will be triggered. Set it to `* * * * * ?` if you want continuous merges, or configure a time schedule to limit warehouse run time. The connector evaluates the schedule in the UTC time zone.  For example:  - The string `* 0 * * * ?` indicates that you want to schedule merges at the full hour for one minute. - The string `* 20 14 ? * MON-FRI` indicates that you want to schedule merges at 2:20 PM every   Monday through Friday.  For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html). |
| Object Identifier Resolution | Specifies how source object identifiers such as schemas, tables, and column names are stored and queried in Snowflake. This setting determines if you must use double quotes in SQL queries.  Option 1: Default, case-insensitive (recommended).   - **Transformation**: All identifiers are converted to uppercase. For   example, `My_Table` becomes `MY_TABLE`. - **Queries**: SQL queries are case-insensitive and don’t require SQL   double quotes.   For example `SELECT * FROM my_table;` returns the same results as `SELECT * FROM MY_TABLE;`.  Note  Snowflake recommends using this option if database objects aren’t expected to have mixed case names.  Option 2: Case-sensitive.   - **Transformation**: Case is preserved.   For example, `My_Table` remains `My_Table`. - **Queries**: SQL queries must use double quotes to match the exact   case for database objects.   For example, `SELECT * FROM "My_Table";`.   Important  Do not change this setting after connector ingestion has begun. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. |
| Snapshot Fetching Strategy | Determines the snapshot load fetching strategy:   - **CONCURRENT\_BY\_ROWID** (default): Splits tables into chunks bound by ranges of physical row ids, and retrieves each chunk in parallel.   This strategy isn’t currently supported when the connector reads from a read-only database like Active Data Guard physical standby. - **SEQUENTIAL\_BY\_PRIMARY\_KEY**: Uses fixed-size batches retrieved sequentially by the table’s replication key (primary key, unique constraint,   unique index, or logical key). Despite the name, this strategy uses whatever key the connector resolved for the table, not specifically the primary key. |
| Concurrent Snapshot Queries | Maximum number of concurrent queries to the source database to run in the Snapshot flow. Increasing this can speed up snapshotting large numbers of tables, but will also increase the load on the source database. |

Expand

Show lessSee more

### Oracle Source Parameters

| Parameter | Description | Required |
| --- | --- | --- |
| Oracle Connection URL | JDBC URL of the database connection to the DB. The URL must specify the target container (PDB or CDB) that contains the data to be replicated. For example `jdbc:oracle:thin:@<host>:<port>/YOUR_DB_NAME` where YOUR\_DB\_NAME is the name of your PDB or CDB.  When SSL is enabled, use the TCPS protocol, for example `jdbc:oracle:thin:@tcps://<host>:<tcps_port>/YOUR_DB_NAME`.  Note  The connector works within a single database/container. Ensure the JDBC URL points directly to the container that holds the tables to be replicated. | Yes |
| Oracle Username | Username of the connect user that has access to the XStream Server. | Yes |
| Oracle Password | Password of the connect user that has access to the XStream Server. | Yes |
| Oracle SSL Mode | Controls SSL encryption for connections to the Oracle database.   - **DISABLED**, which is the default: Connect without SSL. - **VERIFY\_CA**: Connect with SSL. Verifies that a trusted Certificate Authority   issued the server certificate. - **VERIFY\_IDENTITY**: Connect with SSL. Verifies the CA certificate and that the   server hostname matches the certificate’s subject.   When set to VERIFY\_CA or VERIFY\_IDENTITY, you must also provide the Oracle Wallet Filename parameter. | Yes |
| Oracle Wallet Filename | Upload the file that contains the Oracle auto-login wallet file (`cwallet.sso`). The wallet must contain the trusted server certificate for SSL connections.  For information about creating the wallet, see [Configure SSL connections (optional)](/user-guide/data-integration/openflow/connectors/oracle/setup-oracledb#label-configure-ssl-connections). | Required when SSL Mode is not DISABLED |
| Oracle Database Processor Multiplier | Core Processor Licensing Factor as described in [Oracle Processor Core Factor Table](https://www.oracle.com/contracts/docs/processor-core-factor-table-070634.pdf). | Required for Embedded License only |
| Oracle Database Processor Cores | The number of processor cores in your Oracle database. | Required for Embedded License only |
| XStream Billing Acknowledgement | A confirmation of the licensing agreement. | Required for Embedded License only |
| XStream Out Server Name | The name of the XStream Server that must already exist in Oracle. | Yes |
| XStream Out Server URL | JDBC URL of the database connection for XStream, which must use the OCI driver. For example `jdbc:oracle:oci:@<host>:<port>/SID`.  When SSL is enabled, use the TCPS protocol, for example `jdbc:oracle:oci:@tcps://<host>:<tcps_port>/SID`.  Note  When SSL Mode is enabled, the connector automatically adds `SSL_SERVER_DN_MATCH` and `MY_WALLET_DIRECTORY` to the XStream URL. You don’t need to include these manually. | Yes |

Expand

Show lessSee more

## Restart table replication

A table in FAILED state — for example, due to a missing primary key or unsupported schema change — does not restart automatically. If a table enters a FAILED state or you need to restart replication from scratch, use the following procedure to remove and re-add the table to replication.

Note

If the failure was caused by an issue in the source table such as a missing primary key, resolve that issue in the source database before continuing.

1. Remove the table from replication, using one of the following methods:

   - Add the table to the **Re-snapshot Table Exclusions** parameter to temporarily exclude it from replication. This is convenient when the table is matched by an **Included Table Regex** that you don’t want to change.
   - In the Ingestion Parameters context, either remove the table from **Included Table Names** or modify the **Included Table Regex** so the table is no longer matched.
2. Verify the table has been removed:

   1. In the Openflow runtime canvas, right-click a processor group and choose **Controller Services**.
   2. In the table listing controller services, locate the **Table State Store** row, click the three vertical dots on the right side of the row, then choose **View State**.

   Important

   You must wait until the table’s state is fully removed from this list before proceeding. Do not continue until this configuration change has completed.
3. Clean up the destination: Once the table’s state shows as fully removed, manually [DROP](/sql-reference/sql/drop-table) the destination table in Snowflake. Note that the connector will not overwrite an existing destination table during the snapshot phase; if the table still exists, replication will fail again. Optionally, the journal table and stream can also be removed if they are no longer needed.
4. Re-add the table by reversing the change you made in the first step: either remove the table from **Re-snapshot Table Exclusions**, or add it back to **Included Table Names** or **Included Table Regex**. The connector then re-snapshots the table.
5. Verify the restart: Check the **Table State Store** using the instructions given previously. The state of the table should appear with the status NEW, then transition to SNAPSHOT\_REPLICATION, and finally INCREMENTAL\_REPLICATION.

## Replicate a subset of columns in a table

The connector can filter the data replicated per table to a subset of configured columns.
Primary key columns are always included regardless of exclusions.

To apply column filters, set the **Column Filter JSON** parameter in the Ingestion Parameters context
to a JSON array of filter objects, one per table you want to filter.

Columns can be included or excluded by name or by regular expression pattern. You can apply a single condition per table,
or combine multiple conditions, with exclusions always taking precedence over inclusions.

## Syntax

Each object in the array identifies a table and specifies which columns to include or exclude.
Because this connector uses three-part fully qualified names (database, schema, and table), each object
can include a `database` or `databasePattern` field in addition to the schema and table fields.

Copy code

```
[
    {
        "database": "<database>" | "databasePattern": "<regex>",
        "schema": "<schema>" | "schemaPattern": "<regex>",
        "table": "<table>" | "tablePattern": "<regex>",
        "included": ["<column>", "<column>"],
        "excluded": ["<column>", "<column>"],
        "includedPattern": "<regex>",
        "excludedPattern": "<regex>"
    }
]
```

The following rules apply:

- Use `database`, `schema`, and `table` for exact name matching, or `databasePattern`,
  `schemaPattern`, and `tablePattern` for regex matching. You can’t use both a field and its
  pattern variant in the same object (for example, `schema` and `schemaPattern` can’t both appear).
- At least one of `included`, `excluded`, `includedPattern`, or `excludedPattern` must be provided.
- When both included and excluded filters are specified, exclusions take precedence.
- When multiple filters match the same table, the last matching filter is used, with exact matches
  taking precedence over pattern-based filters.
- The value can be an array of objects to apply different filters to different tables.

## Examples

Include specific columns by name:

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "orders",
        "included": ["account_id", "status", "created_at"]
    }
]
```

Exclude specific columns by name:

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "orders",
        "excluded": ["internal_note", "debug_flag"]
    }
]
```

Combine an include pattern with a specific exclusion (for example, include all email columns except `admin_email`):

Copy code

```
[
    {
        "database": "my_db",
        "schema": "dbo",
        "table": "contacts",
        "includedPattern": ".*_email",
        "excluded": ["admin_email"]
    }
]
```

Mix a database pattern with an exact schema and table name to apply a filter across databases:

Copy code

```
[
    {
        "databasePattern": "prod_.*",
        "schema": "dbo",
        "table": "customers",
        "excluded": ["internal_note"]
    }
]
```

Pass multiple filter objects to apply different rules to different tables:

Copy code

```
[
    {"database": "my_db", "schema": "dbo", "table": "orders", "included": ["account_id", "status"]},
    {"database": "my_db", "schema": "dbo", "table": "customers", "excludedPattern": ".*_internal"}
]
```

### Including and excluding the same column

Removing a column from a table’s replicated set (by excluding it or by removing
it from the included list) has the same effect on the destination as dropping
the column at the source: the connector soft-deletes the column on the
destination by renaming it with a suffix (by default, `__SNOWFLAKE_DELETED`).
If you then add the column back to the replicated set and later remove it a
second time, replication for the affected table fails because the soft-deleted
column name is already taken. To recover, restart replication for the affected
table.

## Specify a logical key for a table

The connector requires a replication key for every table it replicates. By default, the
connector picks the replication key automatically, in this order: a primary key, then a
qualifying unique constraint, then a qualifying unique index. For the full selection
rules, see [How the connector chooses a replication key](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-replication-key-selection).

A *logical key* is a user-declared replacement for the auto-detected key. Configure a
logical key when:

- A table has no primary key and no qualifying unique constraint or unique index, but
  one or more columns are unique in the data.
- A specific column or set of columns should be used as the replication key, regardless
  of what the connector would auto-detect (for example, to override a synthetic primary
  key).

A logical key takes the highest priority. When the connector finds a logical key for a
table, it uses that key and ignores any primary key, unique constraint, or unique index
on the table.

### JSON syntax

The **Table Key Configuration JSON** value is a JSON array. Each entry maps one
table to its logical key columns:

Copy code

```
[
    {
        "database": "<database>",
        "schema": "<schema>",
        "table": "<table>",
        "logicalKey": ["<column>", "<column>"]
    }
]
```

The fields are:

| Field | Description |
| --- | --- |
| `database` | Required. The exact source database (PDB or CDB) name, matching the database in the table’s three-part fully qualified name. |
| `schema` | Required. The exact source schema name. |
| `table` | Required. The exact source table name. |
| `logicalKey` | Required. A non-empty array of source column names that uniquely identify rows in the table. |

Expand

Show lessSee more

The following rules apply:

- `database`, `schema`, and `table` matching is **case-sensitive**. Oracle stores
  identifiers in uppercase by default, so use uppercase names unless the identifiers
  were created with double-quoted mixed-case or lowercase names.
- `logicalKey` column matching is case-insensitive. The connector matches column
  names against the source table schema regardless of case.
- An entry whose `database`, `schema`, and `table` don’t match any replicated
  table is silently ignored.

### Logical key configuration examples

A single-column logical key on a table without a primary key:

Copy code

```
[
    {
        "database": "MYPDB",
        "schema": "SALES",
        "table": "AUDIT_LOG",
        "logicalKey": ["EVENT_ID"]
    }
]
```

A composite logical key:

Copy code

```
[
    {
        "database": "MYPDB",
        "schema": "SALES",
        "table": "ORDER_LINES",
        "logicalKey": ["ORDER_ID", "LINE_ITEM_ID"]
    }
]
```

Logical keys for several tables in one JSON value:

Copy code

```
[
    {
        "database": "MYPDB",
        "schema": "SALES",
        "table": "AUDIT_LOG",
        "logicalKey": ["EVENT_ID"]
    },
    {
        "database": "MYPDB",
        "schema": "SALES",
        "table": "ORDER_LINES",
        "logicalKey": ["ORDER_ID", "LINE_ITEM_ID"]
    }
]
```

### Restrictions

The connector rejects the configuration when any of the following is true:

- `logicalKey` is missing, empty, or not an array.
- `logicalKey` contains duplicate column names (compared case-insensitively).
- `logicalKey` contains the pseudo-column `ROWID`. `ROWID` isn’t a reliable
  replication key because it can change when a row is moved (for example, after a table
  rebuild or partition operation).
- `logicalKey` contains a column name that doesn’t exist in the source table.

When the configuration is rejected, the connector either fails to enable the
controller service (for structural issues detected at enablement time) or holds the
table in the `NEW` state (for issues detected when the table is initialized). After
you fix the configuration, replication for the table resumes without resetting state.

### Warnings logged for risky configurations

The connector accepts the following configurations but logs a warning at table
initialization. Verify the data carefully or arrange a periodic full reload to correct
drift.

When choosing logical-key columns, prefer columns with high cardinality and, where
possible, monotonically increasing values. Low-cardinality or non-monotonic keys can
degrade snapshot performance if you use the `SEQUENTIAL_BY_PRIMARY_KEY` strategy, which
orders rows by the replication key.

- A logical-key column is a large-object type (`BLOB`, `CLOB`, `NCLOB`, `LONG`,
  `LONG RAW`). Using large objects as keys severely degrades MERGE performance.
- A logical-key column is a floating-point type (`FLOAT`, `DOUBLE`, `REAL`,
  `BINARY_FLOAT`, `BINARY_DOUBLE`). Floating-point comparisons can produce
  inconsistent results because of precision differences.
- The composite logical key has more than five columns. Long composite keys often
  indicate a design issue and might degrade MERGE performance.
- The logical key replaces an existing primary key on the table.

### Limitation: Changes to a logical-key value

Important

When a source `UPDATE` changes the value of a logical-key column, the connector
does **not** soft-delete the row keyed by the old value before inserting the row
keyed by the new value. The destination table ends up with two active rows for
what’s a single row in the source: the original row, still active under its old
key value, and a new row under the new key value.

This differs from how the connector handles a primary-key value change on tables
that don’t use a logical key. For more information on that behavior, see
[Changes to a replication key value](/user-guide/data-integration/openflow/connectors/oracle/about#label-oracle-replication-key-value-change).

To avoid this limitation, choose logical-key columns whose values don’t change in
the source. If logical-key values do change, periodically run a full reload for
the affected tables to reconcile the destination with the source.

### Schema changes that affect a logical key

Logical keys reference column names. The connector doesn’t follow renames or drops of
those columns:

- If a logical-key column is dropped on the source, replication for the affected table
  fails. The table is marked `FAILED`. For recovery steps, see
  [A logical-key column was dropped or renamed on the source](/user-guide/data-integration/openflow/connectors/oracle/troubleshoot#label-oracle-logical-key-invalidated) in the troubleshooting topic.
- If a logical-key column is renamed on the source, the configuration still references
  the old name and replication fails. Update the JSON to use the new name and restart
  table replication.

## Configure scheduling of merge tasks

The connector uses a warehouse to merge change data capture (CDC) data into destination tables.
The processor named Merge Journal to Destination triggers this operation. When there are no new
changes, or when no new FlowFiles are waiting in the Merge Journal to Destination queue, no merge
is triggered and the warehouse is available for auto-suspension.

To limit warehouse cost and restrict merges to scheduled times, use the CRON expression in the
Merge Task Schedule CRON parameter. It throttles the FlowFiles that reach the Merge Journal to
Destination processor, so merges are triggered only during the specified period. The connector
evaluates the schedule in the UTC time zone.

For additional information and examples, see the cron triggers tutorial in the [Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.5.x/tutorials/crontrigger.html).

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## Next steps

- (Optional) [Set up incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/oracle/incremental-replication).
- [Monitor the flow](/user-guide/data-integration/openflow/monitor).
