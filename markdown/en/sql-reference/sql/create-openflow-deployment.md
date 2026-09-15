# CREATE OPENFLOW DEPLOYMENT

See also:
:   [ALTER OPENFLOW DEPLOYMENT](/sql-reference/sql/alter-openflow-deployment), [DROP OPENFLOW DEPLOYMENT](/sql-reference/sql/drop-openflow-deployment), [SHOW OPENFLOW DEPLOYMENTS](/sql-reference/sql/show-openflow-deployments), [DESCRIBE OPENFLOW DEPLOYMENT](/sql-reference/sql/desc-openflow-deployment)

Creates a gen 2 Openflow deployment in the account.

## Syntax

Copy code

```
CREATE OPENFLOW DEPLOYMENT [ IF NOT EXISTS ] <name>
  [ DEPLOYMENT_TYPE = { SNOWFLAKE | BYOC } ]
  [ VPC_TYPE = { 'MANAGED' | 'PROVIDED' } ]
  [ USE_PRIVATE_LINK = { TRUE | FALSE } ]
  [ USE_USER_AUTH_OVER_PRIVATE_LINK = { TRUE | FALSE } ]
  [ CUSTOM_INGRESS_HOSTNAME = <string> ]
  [ DISPLAY_NAME = <string> ]
  [ COMMENT = <string> ]
  [ EVENT_TABLE = { '<database>.<schema>.<tablename>' | NONE } ]
```

## Required parameters

`name`
:   Specifies the identifier for the deployment. Any valid object identifier is supported. For more
    information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`IF NOT EXISTS`
:   Creates the deployment only if it does not already exist. If the deployment already exists, the
    statement does nothing and returns a success message.

`DEPLOYMENT_TYPE = { SNOWFLAKE | BYOC }`
:   `SNOWFLAKE` creates an Openflow - Snowflake Deployment deployment. `BYOC` creates a deployment in your cloud account.

    Default: `SNOWFLAKE`

`VPC_TYPE = { 'MANAGED' | 'PROVIDED' }`
:   BYOC only. `MANAGED` uses a Snowflake-managed VPC. `PROVIDED` uses your existing VPC.

    Default: No value

`USE_PRIVATE_LINK = { TRUE | FALSE }`
:   Default: `FALSE`

`USE_USER_AUTH_OVER_PRIVATE_LINK = { TRUE | FALSE }`
:   BYOC only. Requires `USE_PRIVATE_LINK = TRUE`.

    Default: `FALSE`

`CUSTOM_INGRESS_HOSTNAME = string`
:   BYOC only. Custom hostname for ingress traffic.

    Default: No value

`DISPLAY_NAME = string`
:   UI display name. If unset, the SQL `name` is shown in the Openflow UI.

    Default: No value

`COMMENT = string`
:   Default: No value

`EVENT_TABLE = { 'database.schema.tablename' | NONE }`
:   [Event table](/developer-guide/logging-tracing/event-table-setting-up) that receives Openflow logs and
    metrics for this deployment. Specify a fully qualified name to use a deployment-specific table.

    Default: No value (inherits the account-level event table)

    To view the current value, run `SHOW PARAMETERS LIKE 'EVENT_TABLE' IN OPENFLOW DEPLOYMENT <name>`.
    `EVENT_TABLE` is not shown in `SHOW OPENFLOW DEPLOYMENTS` or `DESCRIBE OPENFLOW DEPLOYMENT` output.

## Access control

Requires `CREATE OPENFLOW DEPLOYMENT` on the account. For `DEPLOYMENT_TYPE = SNOWFLAKE` (the
default), also requires `CREATE COMPUTE POOL` on the account.

## Usage notes

- This command returns immediately. Deployment provisioning runs asynchronously and typically takes
  5–10 minutes for Snowflake deployments. Use
  [SYSTEM$WAIT\_FOR\_OPENFLOW\_DEPLOYMENT\_STATUS](/sql-reference/functions/system_wait_for_openflow_deployment_status)
  or
  [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments)
  to wait for the deployment to become `ACTIVE`.
- Each account supports up to three Snowflake Openflow deployments. Gen 1 and gen 2
  deployments share this limit; `CREATE OPENFLOW DEPLOYMENT WITH DEPLOYMENT_TYPE = SNOWFLAKE`
  fails when the account already has three Snowflake deployments, regardless of generation.
- After creating a BYOC deployment, complete cloud installation using the CloudFormation template from
  the Openflow UI. See [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).

## Example

Copy code

```
CREATE OPENFLOW DEPLOYMENT my_deployment
  DEPLOYMENT_TYPE = BYOC
  VPC_TYPE = 'MANAGED'
  DISPLAY_NAME = 'My BYOC Deployment';
```

Copy code

```
CREATE OPENFLOW DEPLOYMENT my_snowflake_deployment
  DEPLOYMENT_TYPE = SNOWFLAKE
  EVENT_TABLE = 'openflow.telemetry.events';
```
