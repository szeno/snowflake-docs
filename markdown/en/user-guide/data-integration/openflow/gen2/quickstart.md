# Quickstart: gen 2 Openflow

Gen 2 Openflow is available on AWS, Azure, and GCP. Gen 2 deployment and runtime SQL objects are
generally available; gen 2 connector configuration is in Public Preview (see [Create a gen 2 connector](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-connector)).

This topic walks through what’s needed to get your first gen 2 connector up and running. For
background on how gen 2 Openflow differs from gen 1, see [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).

**If you already have gen 1 deployments and runtimes** that you want to bring into gen 2, follow
the migration path instead of creating new resources here. Migration from gen 1 to gen 2 is
available in Private Preview; contact your Snowflake account representative to be included.
Return to this quickstart to set up privileges if you haven’t done that yet (the privilege
grants in [Set up privileges](#label-openflow-gen2-quickstart-privileges) apply regardless of
how you create your gen 2 resources).

## Before you begin

Complete the standard Openflow prerequisites described in
[About Openflow](/user-guide/data-integration/openflow/about)—role configuration, terms of service, and
deployment-type planning (BYOC or Openflow - Snowflake Deployment).

Gen 2 uses different account- and schema-level privileges than gen 1. If you previously set up
Openflow using the public guides, see [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) for how
the privilege model differs.

## Set up privileges

An account administrator grants privileges; an Openflow administrator role creates the database,
schema, and gen 2 objects.

### Grant privileges (account administrator)

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_admin;
GRANT ROLE openflow_admin TO ROLE ACCOUNTADMIN;

GRANT CREATE OPENFLOW DEPLOYMENT ON ACCOUNT TO ROLE openflow_admin;
GRANT CREATE DATABASE ON ACCOUNT TO ROLE openflow_admin;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE openflow_admin;

-- Snowflake deployments only
GRANT CREATE COMPUTE POOL ON ACCOUNT TO ROLE openflow_admin;
```

### Create database and schema (Openflow administrator)

Create a database and schema to **house gen 2 Openflow objects**—runtimes and connectors are
schema-level objects stored here. This is your Openflow **control schema**, not the database where
connectors load data. Grant the execute-as role access to destination databases separately (see
[Create an execute-as role](#label-openflow-gen2-quickstart-execute-as-role)).

Copy code

```
USE ROLE openflow_admin;

CREATE DATABASE IF NOT EXISTS openflow_db;
CREATE SCHEMA IF NOT EXISTS openflow_db.openflow_schema;

GRANT CREATE OPENFLOW RUNTIME ON SCHEMA openflow_db.openflow_schema TO ROLE openflow_admin;
GRANT CREATE OPENFLOW CONNECTOR ON SCHEMA openflow_db.openflow_schema TO ROLE openflow_admin;
```

Runtimes are schema-level objects. To run SQL against a runtime, users need `USAGE`, `OPERATE`, or
`MONITOR` on the runtime and `USAGE` on its database and schema. You can use a simple name when the
session database and schema are set—the same name resolution rules as other schema-level objects
apply, including in wait functions.

## Create a gen 2 deployment

Create a gen 2 deployment object with SQL or the Openflow UI. Gen 2 uses
`CREATE OPENFLOW DEPLOYMENT`—not the gen 1 `CREATE OPENFLOW DATA PLANE INTEGRATION`. For SQL
parameters (`DEPLOYMENT_TYPE`, `VPC_TYPE`, `USE_PRIVATE_LINK`, `EVENT_TABLE`, and so on), see
[CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment).

Note

**PrivateLink:** If your organization requires private connectivity to Snowflake or the Openflow
UI—not just to your data source—plan PrivateLink before you run `CREATE OPENFLOW DEPLOYMENT`.
Enable PrivateLink for your account first (see [AWS PrivateLink and Snowflake](/user-guide/admin-security-privatelink)). Set
`USE_PRIVATE_LINK = TRUE` in your `CREATE` statement (see
[CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment)). These flags are chosen at
deployment creation; you cannot change them later with `ALTER OPENFLOW DEPLOYMENT`.

- **BYOC:** Complete AWS PrivateLink setup (VPC endpoint, DNS, security groups) **before** you
  apply the CloudFormation template—if you deploy without it configured, you typically must create a
  new deployment rather than retrofit. Also set `USE_USER_AUTH_OVER_PRIVATELINK = TRUE` only if
  users access Snowsight or Openflow through a PrivateLink URL; leave it `FALSE` if they
  use public URLs (deployment traffic still uses PrivateLink when `USE_PRIVATE_LINK` is enabled).
  See [Configuring PrivateLink in AWS](/user-guide/data-integration/openflow/setup-openflow-byoc#label-setup-private-link).
- **Snowflake deployments:** Enable PrivateLink when creating the deployment and configure
  PrivateLink access to the Runtime UI. The user-auth-over-PrivateLink setting does not apply here.
  See [Set up PrivateLink UI access in Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs-configure-pr-ui).

Example (BYOC):

Copy code

```
USE ROLE openflow_admin;

CREATE OPENFLOW DEPLOYMENT my_deployment
  DEPLOYMENT_TYPE = BYOC
  VPC_TYPE = 'MANAGED'
  -- USE_PRIVATE_LINK = TRUE,
  -- USE_USER_AUTH_OVER_PRIVATELINK = FALSE,  -- BYOC only; see PrivateLink note above
  DISPLAY_NAME = 'My gen 2 Deployment';
```

Example (Snowflake deployment):

Copy code

```
CREATE OPENFLOW DEPLOYMENT my_snowflake_deployment
  DEPLOYMENT_TYPE = SNOWFLAKE
  -- USE_PRIVATE_LINK = TRUE,  -- see PrivateLink note above
  DISPLAY_NAME = 'My gen 2 Snowflake Deployment';
```

Caution

Each account supports up to three Snowflake Openflow deployments. Gen 1 and gen 2
deployments share this limit; `CREATE OPENFLOW DEPLOYMENT WITH DEPLOYMENT_TYPE = SNOWFLAKE`
fails when the account already has three Snowflake deployments, regardless of generation.

Next, complete cloud infrastructure setup—the networking and installation steps match the public
Openflow guides; only the Snowflake object you create first is different:

- **BYOC:** CloudFormation template, installation script, and VPC setup. See
  [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).
- **Snowflake deployments:** Core Snowflake and deployment prerequisites. See
  [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs).

## Create a gen 2 runtime

Create a runtime inside your gen 2 deployment. Use the database and schema you created in
[Set up privileges](#label-openflow-gen2-quickstart-privileges).

### Create an execute-as role

`EXECUTE_AS_ROLE` is the Snowflake role that connectors use when reading from and writing to
Snowflake during connector execution. Snowflake access follows that role’s grants—not your session
role and not privileges on the runtime’s home schema. Grant the control schema and other
connector-specific objects before you create the runtime (destination database grants are in
[Before you install a connector](#label-openflow-gen2-quickstart-connector-prereqs)).

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_execute_as_rl;
GRANT ROLE openflow_execute_as_rl TO ROLE openflow_admin;

-- Control schema: required if secrets, stages, or other connector-referenced objects live here
GRANT USAGE ON DATABASE openflow_db TO ROLE openflow_execute_as_rl;
GRANT USAGE ON SCHEMA openflow_db.openflow_schema TO ROLE openflow_execute_as_rl;
```

Grant **READ** on any [Snowflake secrets](/sql-reference/sql/create-secret) the connector references
(often in the control schema), plus **USAGE** on the secret’s database and schema. See
[Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) for secret grants. For background on the execute-as role, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) or
[What is an execute-as role?](/user-guide/data-integration/openflow/about-spcs#label-openflow-spcs-what-is-runtime-role).

### Configure external access (Snowflake deployments)

Openflow BYOC runtimes reach external sources through outbound connectivity you configure in your
cloud environment; EAIs are not used. See [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc).

For Openflow - Snowflake Deployments, the runtime must be associated with an
[external access integration](/developer-guide/external-network-access/external-network-access-overview)
(EAI) before connectors can reach external sources. The hostname and port in the network rule come from your
connector’s setup topic—update the rule before you start the connector (see
[Before you install a connector](#label-openflow-gen2-quickstart-connector-prereqs)).

1. Create a [network rule](/sql-reference/sql/create-network-rule) shell (placeholder
   `VALUE_LIST` is fine for now).
2. Create an [external access integration](/sql-reference/sql/create-external-access-integration)
   that references the network rule.
3. Grant `USAGE` on the integration to `openflow_execute_as_rl`.
4. Pass the integration in `EXTERNAL_ACCESS_INTEGRATIONS` when you create the runtime (next
   section), or run `ALTER OPENFLOW RUNTIME ... ADD EXTERNAL_ACCESS_INTEGRATIONS` afterward.

Network rules are schema-level objects. Set the session database and schema (or use a fully
qualified rule name) before you create them:

Copy code

```
USE ROLE ACCOUNTADMIN;
USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE NETWORK RULE IF NOT EXISTS openflow_my_runtime_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('<source-host>:<port>'); -- Placeholder; we'll update this VALUE_LIST at connector setup time

CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS openflow_my_runtime_eai
  ALLOWED_NETWORK_RULES = (openflow_db.openflow_schema.openflow_my_runtime_network_rule)
  ENABLED = TRUE;

GRANT USAGE ON INTEGRATION openflow_my_runtime_eai TO ROLE openflow_execute_as_rl;
```

If your source system is reachable only over **outbound PrivateLink** (not the public internet),
use `TYPE = PRIVATE_HOST_PORT` network rules and provision private connectivity endpoints before
you create the EAI. Outbound PrivateLink requires Business Critical Edition (or later). See
[External network locations using external access integrations](/user-guide/private-connectivity-outbound#label-private-connect-external-access) and
[Choosing the public internet or private connectivity](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-connectivity)
(AWS, Azure, and Google Cloud private-connectivity topics are linked from that page).

### Create the runtime

Set the session context, then create the runtime:

Copy code

```
USE ROLE openflow_admin;
USE DATABASE openflow_db;
USE SCHEMA openflow_schema;

CREATE OPENFLOW RUNTIME my_runtime
  IN DEPLOYMENT my_deployment
  NODE_TYPE = MEDIUM
  NODE_TYPE_TIER = 'M4'
  MIN_NODES = 1
  MAX_NODES = 1
  EXECUTE_AS_ROLE = openflow_execute_as_rl
  DISPLAY_NAME = 'My gen 2 Runtime';
```

For a Snowflake deployment, add `EXTERNAL_ACCESS_INTEGRATIONS` so the runtime can use the EAI you
created:

Copy code

```
CREATE OPENFLOW RUNTIME my_runtime
  IN DEPLOYMENT my_snowflake_deployment
  NODE_TYPE = MEDIUM
  NODE_TYPE_TIER = 'M4'
  MIN_NODES = 1
  MAX_NODES = 1
  EXECUTE_AS_ROLE = openflow_execute_as_rl
  EXTERNAL_ACCESS_INTEGRATIONS = (openflow_my_runtime_eai)
  DISPLAY_NAME = 'My gen 2 Runtime';
```

To add or change EAIs on an existing runtime, see `ADD EXTERNAL_ACCESS_INTEGRATIONS` in
[ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime).

## Create a gen 2 connector (Public Preview)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Tip

Gen 2 runtimes also run gen 1 connectors. If a gen 2 catalog entry isn’t available for your source
yet, or if you prefer the gen 1 connector, install it from the connector catalog — it runs on the
same runtime and follows that connector’s public setup documentation.

### Before you install a connector

Complete connector-specific setup before you run the wizard or start a connector:

- **Network rule (Snowflake deployments):** Update the rule you created for the runtime with the
  source hostname and port from your connector’s setup topic. For domain lists by connector, see
  [Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).

  Copy code

  ```
  ALTER NETWORK RULE openflow_my_runtime_network_rule SET
    VALUE_LIST = ('<source-host>:<port>');
  ```
- **Destination database (PostgreSQL CDC and MySQL CDC):** Create a destination database if you
  don’t already have one. Grant the runtime’s `EXECUTE_AS_ROLE` **USAGE** on the database and
  **CREATE SCHEMA** on the database—the connector creates destination schemas; you do not grant
  **USAGE** on a pre-existing destination schema. Also grant **USAGE, OPERATE** on the ingest
  warehouse. See [Set up the Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/setup) or
  [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup) for full destination setup.

  Copy code

  ```
  CREATE DATABASE IF NOT EXISTS my_dest_db;

  GRANT USAGE ON DATABASE my_dest_db TO ROLE openflow_execute_as_rl;
  GRANT CREATE SCHEMA ON DATABASE my_dest_db TO ROLE openflow_execute_as_rl;
  GRANT USAGE, OPERATE ON WAREHOUSE my_ingest_wh TO ROLE openflow_execute_as_rl;
  ```
- **Secrets:** Create [Snowflake secrets](/sql-reference/sql/create-secret) for credentials (for
  example, database passwords) and grant **READ** to the runtime’s `EXECUTE_AS_ROLE`. Check your
  connector’s setup topic for the required secret type. See
  [Create an execute-as role](#label-openflow-gen2-quickstart-execute-as-role). You can also source secret values
  from an
  [external secret provider](/user-guide/data-integration/openflow/security/external-secret-providers).
- **Source preparation:** Follow the public connector setup topic for your source (for example,
  PostgreSQL publication and replication for PostgreSQL CDC).

For your first connector, using the setup wizard is recommended:

- [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) — Install a **gen 2** catalog entry with
  step-by-step validation. The wizard manages configuration and versioning; you do not need
  [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) for day-to-day UI setup.

To create another connector from an already validated configuration—for example, when promoting
the same settings to another runtime—see [Create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create) in [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

### Create a connector with SQL (optional)

Use SQL when you need automation or repeat deployments. See [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql)
for the full workflow.

Example (PostgreSQL CDC connector):

Use the catalog **definition ID** in `FROM DEFINITION`. For PostgreSQL CDC, the ID is
`OPENFLOW_POSTGRES_CDC`. To list definition IDs available in your account, run
`SHOW OPENFLOW CONNECTOR DEFINITIONS` (see [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions)).

Copy code

```
CREATE OPENFLOW CONNECTOR my_postgres_connector
  IN RUNTIME my_runtime
  FROM DEFINITION OPENFLOW_POSTGRES_CDC
  DISPLAY_NAME = 'My PostgreSQL CDC Connector';
```

The connector will be in a **STOPPED** state and is a **Draft** until you commit a configuration
version. See [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) (and [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) if you use SQL or
automation).

## Start the connector (Public Preview)

After configuration is committed:

Copy code

```
ALTER OPENFLOW CONNECTOR my_postgres_connector START;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(
  600,
  'my_postgres_connector'
);
```

Manage the connector from the UI (**Installed Connectors** » **Start** / **Stop**) or with SQL.
See [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

## Next steps

- [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) — Full SQL workflow to configure and commit connector settings.
- [Second generation Openflow SQL command reference](/sql-reference/commands-openflow-gen2) — Full SQL command reference for gen 2 objects.
- [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) — Versioning model for SQL and Git (optional if you use the UI only).
- [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) — gen 1 vs gen 2 comparison, key differences, and documentation map.
