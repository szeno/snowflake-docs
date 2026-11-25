# Openflow privileges

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow privileges control who can create deployments and runtimes, operate them, install
connectors from the connector library, and edit flows on the canvas. Grant them with SQL; you
can’t grant the account-level `CREATE` privileges from the Openflow UI.

Use a dedicated Openflow administrator role for day-to-day work. Set `DEFAULT_ROLE` to that
role for users who open a runtime. For the sign-in restrictions, see
[Considerations](#considerations).

## Overview

Snowflake authorizes Openflow actions from **any** of the signed-in user’s roles, not only the
default role. Snowflake recommends setting `DEFAULT_SECONDARY_ROLES = ('ALL')` on each Openflow
user so those grants apply in the UI. Without it, users select a role in the role picker, and
that role must hold the required grants.

Gen 1 and gen 2 use the same four object privileges (`OWNERSHIP`, `USAGE`, `OPERATE`, `MONITOR`)
but different object types and `CREATE` privileges:

| Task | Gen 2 | Gen 1 (existing deployments only) |
| --- | --- | --- |
| Create a deployment | `CREATE OPENFLOW DEPLOYMENT` on the account | New gen 1 deployments can’t be created |
| Create a runtime | `CREATE OPENFLOW RUNTIME` on the schema, plus `OWNERSHIP` or `USAGE` on the parent deployment | `CREATE OPENFLOW RUNTIME INTEGRATION` on the account, plus `OWNERSHIP` or `USAGE` on the parent deployment |
| Create a connector | `CREATE OPENFLOW CONNECTOR` on the schema, plus `USAGE` on the runtime | Install from the connector library with `USAGE` on the runtime |
| Grant object privileges | `GRANT ... ON OPENFLOW DEPLOYMENT` / `OPENFLOW RUNTIME` | `GRANT ... ON INTEGRATION` |

Expand

Show lessSee more

New deployments are gen 2. For object-level differences, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).

## How Openflow privileges work

Snowflake evaluates two layers:

1. **Create privileges** on the account or schema, which let a role create objects.
2. **Object privileges** on a deployment or runtime, which let a role view, operate, or change
   that object.

`OWNERSHIP` includes the capabilities of `USAGE`, `OPERATE`, and `MONITOR`. After you create an
object, you own it until you transfer ownership.

`USAGE` is **not** read-only. On a runtime it includes editing the canvas and installing
connectors from the connector library. `MONITOR` is the read-only privilege.

Connectors that use `SNOWFLAKE_MANAGED` authentication run as the runtime’s **execute-as role**,
not as the user who clicked in the UI. Grant warehouse, database, and schema access to that
role separately. See [Execute-as role](#label-openflow-execute-as-role).

## Recommended administrator privileges

An account administrator creates an Openflow administrator role and grants the privileges it
needs. `OPENFLOW_ADMIN` is a conventional name. The setup topics have the SQL. Grant each
privilege for this reason:

- `CREATE ROLE` lets the Openflow administrator create execute-as roles and other Openflow roles.
- `CREATE OPENFLOW DEPLOYMENT` creates gen 2 deployments.
- `CREATE DATABASE` creates the infrastructure database for schema-level runtimes, connectors,
  and secrets. Keep that database separate from destination databases.
- `CREATE INTEGRATION` creates external access integrations. A Snowflake deployment uses an
  external access integration so a runtime can reach hosts outside Snowflake.
  `CREATE OPENFLOW RUNTIME INTEGRATION` is a different privilege: it adds a runtime on an
  existing gen 1 deployment.
- `CREATE COMPUTE POOL` is required for Snowflake deployments. A Snowflake deployment is backed
  by a compute pool, and `CREATE OPENFLOW DEPLOYMENT` with `DEPLOYMENT_TYPE = SNOWFLAKE`
  requires this privilege.
- `CREATE OPENFLOW RUNTIME` and `CREATE OPENFLOW CONNECTOR` on the infrastructure schema create
  gen 2 runtimes and connectors after the database and schema exist.
- `CREATE OPENFLOW RUNTIME INTEGRATION` applies to existing gen 1 deployments only. It adds a
  runtime. New gen 1 deployments can’t be created.

Grant the role to each Openflow user and set `DEFAULT_ROLE` to that role. Snowflake also
recommends setting `DEFAULT_SECONDARY_ROLES = ('ALL')`.

For the SQL, see:

- [Set up and access Openflow](/user-guide/data-integration/openflow/setup-openflow-roles-login) for the role and the user
- [Set up Openflow - Snowflake Deployment: Core Snowflake](/user-guide/data-integration/openflow/setup-openflow-spcs-sf) for Snowflake deployments
- [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) for BYOC
- [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart) for a gen 2 walkthrough

## Deployment privileges

A deployment is the set of resources that hosts one or more runtimes. In BYOC it represents a
managed Kubernetes cluster. In gen 2 the SQL object is an `OPENFLOW DEPLOYMENT`. In gen 1 it is
an `OPENFLOW DATA PLANE INTEGRATION`.

Users with `CREATE OPENFLOW DEPLOYMENT` on the account can create gen 2 deployments. You can
then grant privileges on a specific deployment to other roles.

The following table maps deployment operations to object privileges. `Yes` means the privilege
is sufficient for that operation (along with any required `CREATE` privilege noted in the
operation). `OWNERSHIP` also covers every operation listed:

| Operation | OWNERSHIP | USAGE | OPERATE | MONITOR |
| --- | --- | --- | --- | --- |
| View details | Yes | Yes | Yes | Yes |
| List child runtimes | Yes | Yes | Yes | Yes |
| Create a runtime | Yes | Yes | No | No |
| Manage endpoints | Yes | Yes | No | No |
| Upgrade the deployment | Yes | No | Yes | No |
| Rename or edit | Yes | No | No | No |
| Delete | Yes | No | No | No |
| Manage grants | Yes | No | No | No |
| Get the bootstrap template | Yes | No | No | No |

Expand

Show lessSee more

Creating a runtime also requires the gen 2 `CREATE OPENFLOW RUNTIME` privilege on the schema,
or the gen 1 `CREATE OPENFLOW RUNTIME INTEGRATION` privilege on the account.

**Gen 2 example** (monitoring role):

Copy code

```
USE ROLE OPENFLOW_ADMIN;

CREATE ROLE IF NOT EXISTS OPENFLOW_MONITOR;
GRANT MONITOR ON OPENFLOW DEPLOYMENT <deployment_name> TO ROLE OPENFLOW_MONITOR;
GRANT ROLE OPENFLOW_MONITOR TO USER <snowflake_user>;
```

**Gen 1 example:**

Copy code

```
CREATE ROLE IF NOT EXISTS OPENFLOW_MONITOR;
GRANT MONITOR ON INTEGRATION <openflow_dataplane_integration_name> TO ROLE OPENFLOW_MONITOR;
```

## Runtime privileges

A runtime is the cluster that runs flow definitions. In gen 2 it is a schema-level
`OPENFLOW RUNTIME`. In gen 1 it is an account-level `OPENFLOW RUNTIME INTEGRATION`.

Creating a runtime requires `OWNERSHIP` or `USAGE` on the parent deployment plus the matching
`CREATE` privilege.

The following table maps runtime operations to object privileges:

| Operation | OWNERSHIP | USAGE | OPERATE | MONITOR |
| --- | --- | --- | --- | --- |
| View details | Yes | Yes | Yes | Yes |
| View canvas | Yes | Yes | Yes | Yes |
| List or download a diagnostic bundle | Yes | Yes | Yes | Yes |
| Edit the canvas | Yes | Yes | No | No |
| Install a connector from the connector library | Yes | Yes | No | No |
| Restart | Yes | No | Yes | No |
| Upgrade | Yes | No | Yes | No |
| Suspend and activate | Yes | No | Yes | No |
| Rename or edit | Yes | No | No | No |
| Delete | Yes | No | No | No |
| Manage grants | Yes | No | No | No |
| Generate or delete a diagnostic bundle | Yes | No | No | No |
| Update the execute-as role | Yes | No | No | No |
| Alter external access integrations | Yes | No | No | No |

Expand

Show lessSee more

Grant `MONITOR` to roles that should observe a runtime without changing flows. Grant `USAGE` to
roles that should install connectors from the connector library or edit the canvas. Grant
`OPERATE` to roles that should restart, upgrade, or suspend a runtime without owning it.

**Gen 2 example:**

Copy code

```
GRANT USAGE ON OPENFLOW RUNTIME openflow_db.openflow_schema.<runtime_name> TO ROLE RUNTIME_EDITOR;
GRANT MONITOR ON OPENFLOW RUNTIME openflow_db.openflow_schema.<runtime_name> TO ROLE RUNTIME_VIEWER;
GRANT OPERATE ON OPENFLOW RUNTIME openflow_db.openflow_schema.<runtime_name> TO ROLE RUNTIME_OPERATOR;
```

## Connector privileges

To create a gen 2 connector, the role needs `CREATE OPENFLOW CONNECTOR` on the schema and
`USAGE` on the runtime. Connector-specific access to Snowflake objects (warehouse, destination
database, secrets) is granted to the execute-as role, not to the Openflow administrator.

For connector library install steps, see [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard).
For SQL, see [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql).

## Execute-as role

An execute-as role is a Snowflake role bound to a runtime. Connectors that use
`SNOWFLAKE_MANAGED` authentication run with this role’s privileges (or a child role granted to
it). Use it to grant access to warehouses, destination databases, and connector-specific
objects.

Because execute-as roles are linked to Openflow managed tokens, you don’t need a separate
service user and key pair for Snowflake authentication. For `KEY_PAIR` authentication instead,
see [Set up key-pair authentication for Openflow - BYOC Deployments](/user-guide/data-integration/openflow/setup-openflow-byoc-key-pair-auth).

`<RUNTIME_NAME>` is the name of the associated runtime. Run the example as `OPENFLOW_ADMIN`,
which has `CREATE ROLE`. The role you use must also be able to grant privileges on the warehouse,
database, and schema.

Copy code

```
USE ROLE OPENFLOW_ADMIN;

CREATE ROLE IF NOT EXISTS OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;

GRANT USAGE, OPERATE ON WAREHOUSE <openflow_ingest_warehouse>
  TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;

GRANT USAGE ON DATABASE <destination_database>
  TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;

GRANT USAGE ON SCHEMA <destination_database>.<destination_schema>
  TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;

GRANT ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL TO USER <username>;
```

Required objects vary by connector. Connector setup topics list the grants for that connector.

## Example: separate admin, editor, and viewer roles

This example uses one gen 2 deployment. `OPENFLOW_ADMIN` owns the deployment.
`DEPLOYMENT1_RUNTIME_MANAGER` can create and edit runtimes only in deployment 1.
`DEPLOYMENT1_RUNTIME_VIEWER` can view a runtime canvas without changing it. The example assumes
that the `openflow_db` database and `openflow_schema` schema already exist.

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS OPENFLOW_ADMIN;
CREATE ROLE IF NOT EXISTS DEPLOYMENT1_RUNTIME_MANAGER;
CREATE ROLE IF NOT EXISTS DEPLOYMENT1_RUNTIME_VIEWER;

GRANT CREATE OPENFLOW DEPLOYMENT ON ACCOUNT TO ROLE OPENFLOW_ADMIN;

-- The runtime manager needs USAGE on the database and schema to create runtimes in them.
GRANT USAGE ON DATABASE openflow_db TO ROLE DEPLOYMENT1_RUNTIME_MANAGER;
GRANT USAGE ON SCHEMA openflow_db.openflow_schema TO ROLE DEPLOYMENT1_RUNTIME_MANAGER;
GRANT CREATE OPENFLOW RUNTIME ON SCHEMA openflow_db.openflow_schema
  TO ROLE DEPLOYMENT1_RUNTIME_MANAGER;

GRANT ROLE OPENFLOW_ADMIN TO USER <admin_user>;
GRANT ROLE DEPLOYMENT1_RUNTIME_MANAGER TO USER <editor_user>;
GRANT ROLE DEPLOYMENT1_RUNTIME_VIEWER TO USER <viewer_user>;
```

1. Sign in to Openflow as `OPENFLOW_ADMIN` and create deployment 1.
2. Grant `USAGE` on that deployment to `DEPLOYMENT1_RUNTIME_MANAGER` so the manager can create
   runtimes there:

   Copy code

   ```
   USE ROLE OPENFLOW_ADMIN;

   GRANT USAGE ON OPENFLOW DEPLOYMENT <deployment_name>
     TO ROLE DEPLOYMENT1_RUNTIME_MANAGER;
   ```
3. Sign in as `DEPLOYMENT1_RUNTIME_MANAGER` and create a runtime. That role owns the runtime it
   created.
4. Grant `MONITOR` on that runtime to `DEPLOYMENT1_RUNTIME_VIEWER`. Grant `USAGE` only to roles
   that should edit the canvas or install connectors from the connector library.

## Considerations

- You can’t grant `CREATE OPENFLOW DEPLOYMENT` or the gen 1 `CREATE OPENFLOW RUNTIME INTEGRATION`
  privilege from the Openflow UI. Use SQL.
- Runtime sign-in fails when the user’s default role is `ACCOUNTADMIN`, `ORGADMIN`,
  `GLOBALORGADMIN`, or `SECURITYADMIN`. Set `DEFAULT_ROLE` to an Openflow role for users who
  open a runtime. Snowflake recommends also setting `DEFAULT_SECONDARY_ROLES = ('ALL')`.
- If the runtime UI shows a blank screen, `Invalid consent request`, or `Unable to log in`,
  check the user’s default role and secondary roles.
- Schema owners can create gen 2 runtimes in a schema without an explicit
  `CREATE OPENFLOW RUNTIME` grant. They still need `USAGE` on the parent deployment.
- Each account supports up to three Snowflake Openflow deployments. Gen 1 and gen 2 Snowflake
  deployments share that limit.
