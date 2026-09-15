# Set up the Openflow Connector for MongoDB

[Preview Feature](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/)

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the steps to set up the Openflow Connector for MongoDB.

## Configure the connector

To configure the connector, perform the following steps:

1. Right-click on the added runtime, and select **Parameters**.
2. Populate the required parameter values as described in [Specify flow parameters](#label-specify-mongo-connector-flow-parameters).

### Specify flow parameters

These sections describe the flow parameters that you can configure in the following parameter contexts:

- [MongoDB source parameters](#label-mongodb-source-parameters): Used to define the configuration for reading data from MongoDB.
- [MongoDB destination parameters](#label-mongodb-destination-parameters): Used to establish a connection with Snowflake.
- [MongoDB ingestion parameters](#label-mongodb-ingestion-parameters): Used to specify the collections to replicate.

### MongoDB source parameters

| Parameter | Description |
| --- | --- |
| MongoDB Connection URI | MongoURI, typically of the form: `mongodb://host1[:port1][,host2[:port2],...]/?[options]`  Snowflake recommends that you include the `readPreference=secondaryPreferred` option in the URI. This directs read operations to the secondary nodes, reducing the overhead on the primary node of the replica set.  Database username and password must not be provided in the URI as this is considered a security issue.  Example: `mongodb://10.11.98.246:27017,10.11.104.58:27017/?replicaSet=myReplicaSet&readPreference=secondaryPreferred` |
| MongoDB Username | The username for interacting with MongoDB.  Example: `openflowUser` |
| MongoDB Password | The password for interacting with MongoDB.  Example: `myPassword123` |
| MongoDB Authentication Source | The database containing user credentials.  Example: `admin` |
| MongoDB Authentication Mechanism | Authentication mechanism that MongoDB uses to authenticate the connection. Possible values are:   - `None`: Connect without authentication. - `SCRAM-SHA-256`: Authentication mechanism that uses the SHA-256 hashing function. |

Expand

Show lessSee more

### MongoDB destination parameters

| Parameter | Description |
| --- | --- |
| Destination Database | The name of the destination database to replicate into. Mixed case is supported.  Example: `MY_DESTINATION_DB` |
| Snowflake Account Identifier | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Snowflake account name where data will be persisted. |
| Snowflake Authentication Strategy | When using:   - SPCS, use `SNOWFLAKE_MANAGED` as the value for Authentication Strategy. - BYOC, use `KEY_PAIR` as the value for Authentication Strategy.   Example: `KEY_PAIR` |
| Snowflake Connection Strategy | When using:   - `KEY_PAIR`: Specify the strategy for connecting to Snowflake. Possible values: `STANDARD`, `PRIVATE_CONNECTIVITY`. |
| Snowflake Private Key | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: The private key must be blank. - `KEY_PAIR`: Copy the content of the RSA private key used for authentication to Snowflake,   formatted according to PKCS8 standards and including standard PEM headers and footers.   The header line begins with `-----BEGIN PRIVATE`. |
| Snowflake Private Key File | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: The private key file must be blank. - `KEY_PAIR`: Upload the file that contains the RSA private key used for authentication to   Snowflake, formatted according to PKCS8 standards and including standard PEM headers and   footers. The header line begins with `-----BEGIN PRIVATE`. To upload the private key   file, select the Reference asset checkbox. |
| Snowflake Private Key Password | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Provide the password associated with the Snowflake Private Key File. |
| Snowflake Role | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Use the runtime’s execute-as role (or a child role granted to it). You can find your   execute-as role in the Openflow UI by navigating to View Details for your runtime. - `KEY_PAIR` Authentication Strategy: Use a valid role configured for your service user.   Example: `OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL` |
| Snowflake Username | When using:   - `SNOWFLAKE_MANAGED` Authentication Strategy: Must be blank. - `KEY_PAIR`: Provide the username used to connect to the Snowflake instance.   Example: `OPENFLOW_USER` |
| Snowflake Warehouse | The name of the warehouse used by the connector.  Example: `OPENFLOW_WH` |

Expand

Show lessSee more

### MongoDB ingestion parameters

| Parameter | Description |
| --- | --- |
| Included Collection Names | Comma-separated list of the collections to replicate.  Example: `my_db.collection1,my_db.collection2` |
| Included Collection Regex | Regular expression for specifying collection names to replicate.  Example: `my_db.*` |
| Object Identifier Resolution | The default for the Openflow Connector for MongoDB is `CASE_INSENSITIVE`. This differs from other Openflow database connectors (such as Postgres and MySQL), which default to `CASE_SENSITIVE` for backwards compatibility.  Specifies how source object identifiers such as the names of schemas, tables, and columns are stored and queried in Snowflake. This setting specifies that you must use double quotes in SQL queries.  Option 1: Default, case-sensitive. For backwards compatibility.   - **Transformation**: Case is preserved.   For example, `My_Table` remains `My_Table`. - **Queries**: SQL queries must use double quotes to match the exact case for database objects.   For example, `SELECT * FROM "My_Table";`.   Note  Snowflake recommends using this option if you must preserve source casing for legacy or compatibility reasons. For example, if the source database includes table names that differ in case only–such as `MY_TABLE` and `my_table`–that would result in a name collision when using when using case-insensitive comparisons. Option 2: Recommended, case-insensitive  - **Transformation**: All identifiers are converted to uppercase. For example, `My_Table` becomes `MY_TABLE`. - **Queries**: SQL queries are case-insensitive and don’t require SQL double quotes.   For example, `SELECT * FROM my_table;` returns the same results as `SELECT * FROM MY_TABLE;`.   Note  Snowflake recommends using this option if database objects are not expected to have mixed case names.  Important  Do not change this setting after the connector has begun ingesting data. Changing this setting after ingestion has begun breaks the existing ingestion. If you must change this setting, create a new connector instance. |
| Merge Task Schedule CRON | CRON expression defining periods when merge operations from journal to destination table are triggered.  Use `* * * * * ?` for continuous merge, or a time schedule to limit warehouse run time.  For example:   - The string `* 0 * * * ?` schedules merges at the full hour for   one minute. - The string `* 20 14 ? * MON-FRI` schedules merges at 2:20 PM   every Monday through Friday.   For additional information and examples, see the [cron triggers tutorial in the Quartz Documentation](https://www.quartz-scheduler.org/documentation/quartz-2.2.2/tutorials/tutorial-lesson-06.html).  Example: `* * * * * ?` |

Expand

Show lessSee more

## Run the flow

1. Right-click on the plane and select **Enable all Controller Services**.
2. Right-click on the imported process group and select **Start**. The connector starts the data ingestion.

## Next steps

For information about using the connector after installation, see [Use the Openflow Connector for MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/use).
