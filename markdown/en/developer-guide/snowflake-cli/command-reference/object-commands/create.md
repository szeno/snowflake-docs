# snow object create

Create an object of a given type. Check documentation for the list of supported objects and parameters.

## Syntax

Copy code

```
snow object create
  <object_type>
  <object_attributes>
  --json <object_json>
  --if-not-exists
  --replace
  --connection <connection>
  --host <host>
  --port <port>
  --account <account>
  --user <user>
  --password <password>
  --authenticator <authenticator>
  --workload-identity-provider <workload_identity_provider>
  --private-key-file <private_key_file>
  --token <token>
  --token-file-path <token_file_path>
  --database <database>
  --schema <schema>
  --role <role>
  --warehouse <warehouse>
  --temporary-connection
  --mfa-passcode <mfa_passcode>
  --enable-diag
  --diag-log-path <diag_log_path>
  --diag-allowlist-path <diag_allowlist_path>
  --oauth-client-id <oauth_client_id>
  --oauth-client-secret <oauth_client_secret>
  --oauth-authorization-url <oauth_authorization_url>
  --oauth-token-request-url <oauth_token_request_url>
  --oauth-redirect-uri <oauth_redirect_uri>
  --oauth-scope <oauth_scope>
  --oauth-disable-pkce
  --oauth-enable-refresh-tokens
  --oauth-enable-single-use-refresh-tokens
  --client-store-temporary-credential
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`object_type`
:   Type of object. For example table, database, compute-pool.

`object_attributes...`
:   Object attributes provided as a list of key=value pairs, for example name=my\_db comment=’created with Snowflake CLI’. Check documentation for the full list of available parameters for every object. .

## Options

`--json TEXT`
:   Object definition in JSON format, for example ‘{“name”: “my\_db”, “comment”: “created with Snowflake CLI”}’. Check documentation for the full list of available parameters for every object.

`--if-not-exists`
:   Only apply this operation if the specified object does not already exist. Default: False.

`--replace`
:   Replace this object if it already exists. Default: False.

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your *config.toml* file. Default: *default*.

`--host TEXT`
:   Host address for the connection. Overrides the value specified for the connection.

`--port INTEGER`
:   Port for the connection. Overrides the value specified for the connection.

`--account, --accountname TEXT`
:   Name assigned to your Snowflake account. Overrides the value specified for the connection.

`--user, --username TEXT`
:   Username to connect to Snowflake. Overrides the value specified for the connection.

`--password TEXT`
:   Snowflake password. Overrides the value specified for the connection.

`--authenticator TEXT`
:   Snowflake authenticator. Overrides the value specified for the connection.

`--workload-identity-provider TEXT`
:   Workload identity provider (AWS, AZURE, GCP, OIDC). Overrides the value specified for the connection.

`--private-key-file, --private-key-path TEXT`
:   Snowflake private key file path. Overrides the value specified for the connection.

`--token TEXT`
:   OAuth token to use when connecting to Snowflake.

`--token-file-path TEXT`
:   Path to file with an OAuth token to use when connecting to Snowflake.

`--database, --dbname TEXT`
:   Database to use. Overrides the value specified for the connection.

`--schema, --schemaname TEXT`
:   Database schema to use. Overrides the value specified for the connection.

`--role, --rolename TEXT`
:   Role to use. Overrides the value specified for the connection.

`--warehouse TEXT`
:   Warehouse to use. Overrides the value specified for the connection.

`--temporary-connection, -x`
:   Uses a connection defined with command-line parameters, instead of one defined in config. Default: False.

`--mfa-passcode TEXT`
:   Token to use for multi-factor authentication (MFA).

`--enable-diag`
:   Whether to generate a connection diagnostic report. Default: False.

`--diag-log-path TEXT`
:   Path for the generated report. Defaults to system temporary directory. Default: <system\_temporary\_directory>.

`--diag-allowlist-path TEXT`
:   Path to a JSON file that contains allowlist parameters.

`--oauth-client-id TEXT`
:   Value of client id provided by the Identity Provider for Snowflake integration.

`--oauth-client-secret TEXT`
:   Value of the client secret provided by the Identity Provider for Snowflake integration.

`--oauth-authorization-url TEXT`
:   Identity Provider endpoint supplying the authorization code to the driver.

`--oauth-token-request-url TEXT`
:   Identity Provider endpoint supplying the access tokens to the driver.

`--oauth-redirect-uri TEXT`
:   URI to use for authorization code redirection.

`--oauth-scope TEXT`
:   Scope requested in the Identity Provider authorization request.

`--oauth-disable-pkce`
:   Disables Proof Key for Code Exchange (PKCE). Default: *False*.

`--oauth-enable-refresh-tokens`
:   Enables a silent re-authentication when the actual access token becomes outdated. Default: *False*.

`--oauth-enable-single-use-refresh-tokens`
:   Whether to opt-in to single-use refresh token semantics. Default: *False*.

`--client-store-temporary-credential`
:   Store the temporary credential.

`--format [TABLE%JSON%JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels *info* and higher. Default: False.

`--debug`
:   Displays log entries for log levels *debug* and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

The `snow object create` command creates one of the following types Snowflake objects, based on the provided object attributes or definitions:

- `account`
- `catalog-integration`
- `compute-pool`
- `database`
- `database-role`
- `dynamic-table`
- `event-table`
- `external-volume`
- `function`
- `image-repository`
- `managed-account`
- `network-policy`
- `notebook`
- `notification-integration`
- `pipe`
- `procedure`
- `role`
- `schema`
- `service`
- `stage`
- `stream`
- `table`
- `task`
- `user-defined-function`
- `view`
- `warehouse`

For each object, you must specify the appropriate object details using either the object attributes or the object definitions.

- Use the `object_attributes` parameter specifies the object details as a series of `<key>=<value>` pairs, such as:

  Copy code

  ```
  snow object create database name=my_db comment="Created with Snowflake CLI"
  ```
- Use the `--json object_definition` option to specify the object details as JSON, such as:

  Copy code

  ```
  snow object create table name=my_table columns='[{"name":"col1","datatype":"number", "nullable":false}]' constraints='[{"name":"prim_key", "column_names":["col1"], "constraint_type":"PRIMARY KEY"}]' --database my_db --schema public
  ```
- See [Examples](#label-cli-create-examples) for more examples.

Note

The following object types require a database to be identified in the connection configuration, such as `config.toml`, or passed to the command using the `--database` option.

- image-repository
- schema
- service
- table
- task

The following sections describe the attributes that Snowflake CLI supports for selected object types.

- [compute-pool](#label-cli-object-attrs-compute-pool)
- [database](#label-cli-object-attrs-database)
- [image-repository](#label-cli-object-attrs-image-repository)
- [schema](#label-cli-object-attrs-schema)
- [service](#label-cli-object-attrs-service)
- [table](#label-cli-object-attrs-table)
- [task](#label-cli-object-attrs-task)
- [warehouse](#label-cli-object-attrs-database)

You can find attributes for other types of objects by checking their corresponding SQL CREATE command references, such as [CREATE ACCOUNT](/sql-reference/sql/create-account).

### Compute pool object attributes

**Compute pool attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **min\_nodes**  *required*, *integer* | Minimum number of nodes for the compute pool. |
| **max\_nodes**  *required*, *integer* | Maximum number of nodes for the compute pool. |
| **instance\_family**  *required*, *string* | Name of the instance family. For more information about instance families, refer to the SQL CREATE COMPUTE POOL command. |
| **auto\_resume**  *optional*, *string* | Whether to resume the compute pool automatically when any statement that requires the compute pool is submitted. |
| **comment**  *optional*, *string* | Comment describing the compute pool. |
| **auto\_suspend\_secs**  *optional*, *string* | Number of seconds of inactivity after which you want Snowflake to automatically suspend the compute pool. |

Expand

Show lessSee more

### Database object attributes

**Database attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **comment**  *optional*, *string* | Comment describing the database. |
| **data\_retention\_time\_in\_days**  *optional*, *integer* | Number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the schema, as well as the default Time Travel retention time for all tables created in the schema. |
| **default\_ddl\_collation**  *optional*, *string* | Default collation specification for all schemas and tables added to the database. You can override this default at the schema and individual table level. |
| **max\_data\_extension\_time\_in\_days**  *optional*, *integer* | Maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. |
| **suspend\_task\_after\_num\_failures**  *optional*, *integer* | Number of consecutive failed task runs after which the current task is suspended automatically. |
| **user\_task\_managed\_initial\_warehouse\_size**  *optional*, *integer* | Size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. Possible values include: XSMALL, SMALL, MEDIUM, LARGE, and XLARGE. |
| **user\_task\_timeout\_ms**  *optional*, *integer* | Time limit, in milliseconds, for a single run of the task before it times out. For information, see [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms). |

Expand

Show lessSee more

### Image repository object attributes

**Image repository attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |

Expand

Show lessSee more

### Schema object attributes

**Schema attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **comment**  *optional*, *string* | Comment describing the schema. |
| **data\_retention\_time\_in\_days**  *optional*, *integer* | Number of days for which Time Travel actions (CLONE and UNDROP) can be performed on the schema, as well as the default Time Travel retention time for all tables created in the schema. |
| **default\_ddl\_collation**  *optional*, *string* | Default collation specification for all schemas and tables added to the database. You can override this default at the schema and individual table level. |
| **max\_data\_extension\_time\_in\_days**  *optional*, *integer* | Maximum number of days for which Snowflake can extend the data retention period for tables in the database to prevent streams on the tables from becoming stale. |
| **suspend\_task\_after\_num\_failures**  *optional*, *integer* | Number of consecutive failed task runs after which the current task is suspended automatically. |
| **user\_task\_managed\_initial\_warehouse\_size**  *optional*, *integer* | Size of the compute resources to provision for the first run of the task, before a task history is available for Snowflake to determine an ideal size. |
| **user\_task\_timeout\_ms**  *optional*, *integer* | Time limit, in milliseconds, for a single run of the task before it times out. For information, see [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms). |

Expand

Show lessSee more

### Service object attributes

**Service attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **compute\_pool**  *required*, *string* | Name of the compute pool in your account on which to run the service. |
| **spec**  *required*, *object* | Service specification. See [service specification table](/developer-guide/snowflake-cli/command-reference/object-commands/create#label-cli-object-attrs-service-spec) for details. |
| **external\_access\_integrations**  *optional*, *string list* | Names of the external access integrations that allow your service to access external sites. |
| **auto\_resume**  *optional*, *boolean* | Whether to automatically resume a service when a service function or ingress is called. |
| **min\_instances**  *optional*, *integer* | Minimum number of service instances to run. |
| **max\_instances**  *optional*, *integer* | Maximum number of service instances to run. |
| **query\_warehouse**  *optional*, *string* | Warehouse to use if a service container connects to Snowflake to execute a query but does not explicitly specify a warehouse to use. |
| **comment**  *optional*, *string* | Comment for the service. |

Expand

Show lessSee more

**Service specification attributes**

**Service specification attributes**

| Attribute | Description |
| --- | --- |
| **spec\_type**  *required*, *string* | Type of the service specification. Possible values include `from_file` or `from_inline`. |
| **spec\_text**  *required*, *string* | (Valid only for `spec_type="from_inline"`)  Service specification. You can use a pair of dollar signs ($$) to delimit the beginning and ending of the specification string. |
| **stage**  *required*, *string* | (Valid only for `spec_type="from_inline"`)  Snowflake internal stage where the specification file is stored, such as `@tutorial_stage`. |
| **name**  *required*, *string* | (Valid only for `spec_type="from_inline"`)  Path to the service specification file on the stage, such as `some-dir/echo_spec.yaml`. |

Expand

Show lessSee more

### Table object attributes

**Table attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. The name must be unique for the schema in which the table is created. |
| **kind**  *optional*, *string* | Table type. Possible values include: TABLE for permanent tables, TEMPORARY, and TRANSIENT. |
| **comment**  *optional*, *string* | Description of the table. |
| **cluster\_by[]**  *optional*, *string list* | List of one or more columns or column expressions in the table as the clustering key. |
| **enable\_schema\_evolution**  *optional*, *boolean* | Whether to enable or disable schema evolution for the table. |
| **change\_tracking**  *optional*, *boolean* | Whether to enable or disable change tracking for the table. |
| **data\_retention\_time\_in\_days**  *optional*, *integer* | Retention period, in days, for the table so that Time Travel actions SELECT, CLONE, UNDROP can be performed on historical data in the table. |
| **max\_data\_extension\_time\_in\_days**  *optional*, *integer* | Maximum number of days Snowflake can extend the data retention period to prevent streams on the table from becoming stale. |
| **default\_ddl\_collation**  *optional*, *string* | Default collation specification for the columns in the table, including columns added to the table in the future. |
| **columns**  *required*, *column list* | List of column definitions. See [Column definition attributes](/developer-guide/snowflake-cli/command-reference/object-commands/create#label-cli-object-attrs-table-columns). |
| **constraints**  *optional*, *constraint list* | List of constraint definitions. See [Constrain definition attributes](/developer-guide/snowflake-cli/command-reference/object-commands/create#label-cli-object-attrs-table-constraints). |

Expand

Show lessSee more

**Column definition attributes**

**Column definition attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Column name. |
| **datatype**  *required*, *string* | Type of data contained in the column. |
| **nullable**  *optional*, *boolean* | Whether the column allows NULL values. |
| **collate**  *optional*, *string* | Collation to use for column operations such as string comparison. |
| **default**  *optional*, *string* | Whether to automatically insert a default value in the column if a value is not explicitly specified with an INSERT or CREATE TABLE AS SELECT statement. |
| **autoincrement**  *optional*, *boolean* | Whether to automatically increment and include the number in successive columns. |
| **autoincrement\_start**  *optional*, *integer* | Staring value for the column. |
| **autoincrement\_increment**  *optional*, *integer* | Increment for determining the next auto-incremented number. |
| **comment**  *optional*, *string* | Column description. |

Expand

Show lessSee more

**Constraint definition attributes**

**Constraint definition attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Constraint name. |
| **column\_names**  *required*, *string list* | Names of columns to apply the constraint. |
| **constraint\_type**  *required*, *string* | Type of the constraint. Possible values include: UNIQUE, PRIMARY KEY and FOREIGN KEY. |
| **referenced\_table\_name**  *required*, *string* | (Valid only for `constraint_type="FOREIGN KEY"`)  Name of table referenced by foreign key |
| **referenced\_column\_names**  *optional*, *string* | (Valid only for `constraint_type="FOREIGN KEY"`)  Names of columns referenced by foreign key |

Expand

Show lessSee more

### Task attributes

**Task attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **definition**  *required*, *string* | SQL definition for the task. It can be a single SQL statement, a call to a stored procedure, or procedural logic using Snowflake scripting. |
| **warehouse**  *optional*, *string* | Virtual warehouse that provides compute resources for task runs. |
| **schedule**  *optional*, *string* | Schedule for periodically running the task. See [Task schedule attributes](/developer-guide/snowflake-cli/command-reference/object-commands/create#label-cli-object-attrs-task-scheduler) for details. |
| **comment**  *optional*, *string* | Comment description for the task. |
| **predecessors**  *optional*, *string list* | One or more predecessor tasks for the current task. |
| **user\_task\_managed\_initial\_warehouse\_size**  *optional*, *string* | Size of the compute resources to provision for the first run of the task. |
| **user\_task\_timeout\_ms**  *optional*, *string* | Time limit, in milliseconds, on a single run of the task before it times out. For information, see [USER\_TASK\_TIMEOUT\_MS](/sql-reference/parameters#label-user-task-timeout-ms). |
| **suspend\_task\_after\_num\_failures**  *optional*, *integer* | Number of consecutive failed task runs after which the current task is suspended automatically. |
| **condition**  *optional*, *string* | Boolean SQL expression condition; multiple conditions joined with AND/OR are supported. |
| **allow\_overlapping\_execution**  *optional*, *boolean* | Whether to allow multiple instances of the DAG to run concurrently. |

Expand

Show lessSee more

**Task schedule attributes**

**Task schedule attributes**

| Attribute | Description |
| --- | --- |
| **schedule\_type**  *optional*, *string* | Type of the schedule. Possible values include `CRON_TYPE` or `MINUTES_TYPE`. |
| **cron\_expr**  *optional*, *string* | (Valid only for `schedule_type="CRON_TYPE"`)  A cron expression for the task execution, such as `“* * * * ? *”`. |
| **timezone**  *optional*, *string* | (Valid only for `schedule_type="CRON_TYPE"`)  Time zone for the schedule, for example `"america/los_angeles"`. |
| **minutes**  *optional*, *string* | (Valid only for `schedule_type="MINUTES_TYPE"`)  Number of minutes between each task run. |

Expand

Show lessSee more

### Warehouse attributes

**Warehouse attributes**

| Attribute | Description |
| --- | --- |
| **name**  *required*, *string* | Snowflake object identifier. |
| **comment**  *optional*, *string* | Description of the warehouse. |
| **warehouse\_type**  *optional*, *string* | Type of warehouse. Possible values include: STANDARD and SNOWPARK-OPTIMIZED. |
| **warehouse\_size**  *optional*, *string* | Size of warehouse. Possible values include: XSMALL, SMALL, MEDIUM, LARGE, XLARGE, XXLARGE, XXXLARGE, X4LARGE, X5LARGE, and X6LARGE. |
| **auto\_suspend**  *optional*, *string* | Time, in seconds, before the warehouse automatically suspends itself. |
| **auto\_resume**  *optional*, *string* | Whether to automatically resume a warehouse when a SQL statement is submitted to it. Possible values include: “true” and “false”. |
| **max\_concurrency\_level**  *optional*, *integer* | Concurrency level for SQL statements executed by a warehouse cluster. |
| **statement\_queued\_timeout\_in\_seconds**  *optional*, *integer* | Time, in seconds, a SQL statement can be queued on a warehouse before it is canceled by the system. |
| **statement\_timeout\_in\_seconds**  *optional*, *integer* | Time, in seconds, after which a running SQL statement is canceled by the system. |
| **resource\_monitor**  *optional*, *string* | Name of a resource monitor that is explicitly assigned to the warehouse. When a resource monitor is explicitly assigned to a warehouse, the monitor controls the monthly credits used by the warehouse. |

Expand

Show lessSee more

## Examples

- Create a database object using the `option-attributes` parameter:

  Copy code

  ```
  snow object create database name=my_db comment='Created with Snowflake CLI'
  ```
- Create a table object using the `option-attributes` parameter:

  Copy code

  ```
  snow object create table name=my_table columns='[{"name":"col1","datatype":"number", "nullable":false}]' constraints='[{"name":"prim_key", "column_names":["col1"], "constraint_type":"PRIMARY KEY"}]' --database my_db --schema public
  ```
- Create a database using the `--json object-definition` option:

  Copy code

  ```
  snow object create database --json '{"name":"my_db", "comment":"Created with Snowflake CLI"}'
  ```
- Create a table using the `--json object-definition` option:

  Copy code

  ```
  snow object create table --json "$(cat table.json)" --database my_db
  ```

  where `table.json` contains the following:

  Copy code

  ```
  {
    "name": "my_table",
    "columns": [
   {
     "name": "col1",
     "datatype": "number",
     "nullable": false
   }
    ],
    "constraints": [
   {
     "name": "prim_key",
     "column_names": ["col1"],
     "constraint_type": "PRIMARY KEY"
   }
    ]
  }
  ```
