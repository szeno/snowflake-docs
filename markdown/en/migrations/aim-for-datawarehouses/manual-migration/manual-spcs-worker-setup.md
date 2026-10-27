# Manual SPCS worker setup

This page is for operators who need to create Snowpark Container Services (SPCS) Worker objects by hand. For most projects, prefer the Snowflake AIM Agent for Data Warehouses or SnowConvert AI CLI (`scai data worker setup`), which create the secret, network rule, external access integration, and service for you. Manual creation is not recommended unless your environment requires it.

For deployment scenarios and when to use SPCS versus customer-hosted Workers, see [Deploying workers](../data-migration-validation/deploy-workers).

## Prerequisites

Prepare these objects before creating a Worker service:

1. **Compute pool**: hosts the SPCS services.

Copy code

```
CREATE COMPUTE POOL <compute_pool_name>
  MIN_NODES = 1
  MAX_NODES = <max_nodes>
  INSTANCE_FAMILY = <instance_family>
  AUTO_SUSPEND_SECS = 60;
```

Choose an instance family whose per-node vCPU and memory can fit the Worker instances you want. To list families available in your account:

Copy code

```
SHOW COMPUTE POOL INSTANCE FAMILIES;
```

See [Compute pool sizing](#compute-pool-sizing) for how to size the pool.

2. **Worker container image**: use the Snowflake-managed image at `/snowflake/images/snowflake_images/data-exchange-worker:<version>`. The `scai data worker setup` command reports the pinned version that corresponds to your SnowConvert AI CLI version. You don’t need to create an image repository or push the image.
3. **Warehouse**: a warehouse for the service specification’s `QUERY_WAREHOUSE`.

### Compute pool sizing

Size the pool based on how many Worker instances you want and how many parallel tasks each one runs.

Each Worker instance needs roughly **1–2 vCPU and 1–2 GB of memory per `MAX_PARALLEL_TASKS` thread**. Keep `MAX_PARALLEL_TASKS` at 5 or fewer per instance and prefer more instances over higher thread counts per instance. Set the service `resources.requests` and `resources.limits` to match.

Then choose an instance family and node count so the pool can fit all your Worker instances. The specific family doesn’t matter — what matters is that the per-node vCPU and memory are large enough for the instances you want to schedule on each node. Run `SHOW COMPUTE POOL INSTANCE FAMILIES` and pick one that fits. The pool scales the number of **nodes**; Worker count is set with `MIN_INSTANCES` and `MAX_INSTANCES` on the service.

The Orchestrator needs roughly 1 vCPU and 2 GB. `scai` requests only `cpu: 0.1` for it and sets no limit, so it can use spare capacity on its node. It can share a compute pool with the Workers, or run in its own single-node pool.

Snowflake places a service instance on a node by its `resources.requests`. Without `resources.limits`, a container can use up to the node’s capacity. Choose the node counts from those requests:

- **`MIN_NODES = 1`.** Every node counted in `MIN_NODES` bills whenever the pool runs, even while the services are idle. Don’t raise it for a heavy wave.
- **`MAX_NODES = 1`** when the services keep the requests that `scai` sets: `cpu: 0.1` and `memory: 2Gi` for the Orchestrator and for each Worker, with no limits. A node then holds as many services as fit in its memory at 2Gi each.
- **`MAX_NODES = 2` or `3`** when you raise the Worker requests to the sizing earlier in this section, enough nodes for the Orchestrator and two or three Worker instances. A pool wider than the source system can feed adds cost, not throughput. For a heavy wave, raise `MAX_NODES` and the Worker’s `MAX_INSTANCES` for that wave, and lower them again afterward.

`AUTO_SUSPEND_SECS = 60` suspends the pool about a minute after no service is running in it. It doesn’t stop the services: the Orchestrator and each Worker suspend their own services after `DM_IDLE_SHUTDOWN_MINUTES` without work (`60` by default), and only then does the pool’s `AUTO_SUSPEND_SECS` start counting. Resuming the pool costs roughly 30 to 60 seconds of warm-up, so raise the value if your migration waves run back to back. See [Idle shutdown](../data-migration-validation/deploy-workers#idle-shutdown).

To cap what the pool and the warehouse can spend, put both in a budget. See [Capping spend with a budget](../data-migration-validation/deploy-workers#capping-spend-with-a-budget).

## Network access objects

Workers in SPCS need outbound access from Snowflake to the source database and, for some platforms, to package hosts where drivers are downloaded at container startup. Create a [network rule](https://docs.snowflake.com/en/user-guide/network-rules) and an [external access integration](https://docs.snowflake.com/en/developer-guide/external-network-access/external-network-access-overview), then attach the integration to the Worker service.

Create the secret, network rule, and external access integration in a database and schema your role can manage. The examples below use placeholders; they are not tied to the AIM DMV metadata database.

### Setup flow

1. Create a **secret** with source database credentials (if the Worker reads them from Snowflake).
2. Create a **network rule** listing every host and port the Worker must reach (source database and any driver download hosts).
3. Create an **external access integration** that references the network rule.
4. Create or alter the Worker **service** with `EXTERNAL_ACCESS_INTEGRATIONS = (<integration_name>)`.

Copy code

```
CREATE OR REPLACE SECRET <database>.<schema>.<source_type>_SECRET
  TYPE = PASSWORD
  USERNAME = '<username>'
  PASSWORD = '<password>';

CREATE OR REPLACE NETWORK RULE <database>.<schema>.<source_type>_EGRESS_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    '<source_host>:<source_port>',
    -- driver download hosts (see per-platform lists below)
  );

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION <source_type>_EAI
  ALLOWED_NETWORK_RULES = (<database>.<schema>.<source_type>_EGRESS_RULE)
  ENABLED = TRUE;
```

When you use SnowConvert AI CLI (`scai data worker setup`) with a SQL Server, Azure Synapse, Amazon Redshift, PostgreSQL, Oracle, or Teradata source connection, the CLI creates these objects for you, including the driver download hosts for that platform. Use this page when you need to create them yourself, for example when you use `--skip-egress`.

Note

Account-level network policies, source-system firewalls, and corporate proxies are your responsibility. Verify egress from SPCS to every host in your network rule before starting a workflow.

## Allowing SPCS to reach your source system (inbound access)

An egress network rule only controls what the Worker is *allowed* to call out to. Your source system also needs to *accept* the connection: SPCS containers connect from Snowflake-managed IP addresses, not from an address you control, so the source system’s firewall, security group, or VPC ingress rules must explicitly allow those addresses.

1. Get the current Snowflake egress IP ranges for your account and region:

Copy code

```
SELECT SYSTEM$GET_SNOWFLAKE_EGRESS_IP_RANGES();
```

2. Add those ranges to the source system’s inbound allowlist (for example a security group rule for the source’s port, a firewall rule, or a VPC peering/PrivateLink configuration, depending on how the source is hosted).
3. Re-run the function periodically or before major changes: Snowflake can update egress IP ranges, and a stale allowlist causes connection failures on the Worker side even though the SPCS-side network rule and external access integration are configured correctly.

Warning

If Workers on SPCS can reach the source host over the network but the connection is refused or times out, check the source system’s inbound rules first. This is one of the most common causes of Worker connectivity failures on SPCS.

## Worked example: Redshift Worker service

The following sketch assembles a Worker service for a Redshift source using UNLOAD extraction. Replace every placeholder with your own values; this isn’t a copy-paste-ready script.

Copy code

```
-- Secret and network access
CREATE OR REPLACE SECRET <database>.<schema>.REDSHIFT_SECRET
  TYPE = PASSWORD
  USERNAME = '<username>'
  PASSWORD = '<password>';

CREATE OR REPLACE NETWORK RULE <database>.<schema>.REDSHIFT_EGRESS_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    '<redshift_endpoint>:5439'
    -- plus driver download hosts, see "Driver download hosts by platform" below
  );

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION REDSHIFT_EAI
  ALLOWED_NETWORK_RULES = (<database>.<schema>.REDSHIFT_EGRESS_RULE)
  ENABLED = TRUE;

-- Worker service
CREATE SERVICE <worker_service_name>
  IN COMPUTE POOL <compute_pool_name>
  FROM SPECIFICATION $$
    spec:
      containers:
        - name: agent
          image: /snowflake/images/snowflake_images/data-exchange-worker:<version>
          env:
            # Source system. DATA_SOURCE_TYPE is required: without it the
            # container installs the SQL Server driver.
            DATA_SOURCE_TYPE: redshift
            DATA_SOURCE_HOST: <redshift_endpoint>
            DATA_SOURCE_PORT: 5439
            DATA_SOURCE_DATABASE: <source_database>

            # Snowflake. SPCS doesn't set SNOWFLAKE_WAREHOUSE.
            SNOWFLAKE_WAREHOUSE: <warehouse_name>

            # Worker tuning
            MAX_PARALLEL_TASKS: 3
            AGENT_AFFINITY: <affinity_tag>

            # Required only when using the "unload" extraction strategy
            UNLOAD_S3_BUCKET: <bucket_name>
            UNLOAD_IAM_ROLE_ARN: <iam_role_arn>
          resources:
            requests:
              memory: 10G
              cpu: 6
            limits:
              memory: 10G
              cpu: 6
          secrets:
          - snowflakeSecret: <database>.<schema>.REDSHIFT_SECRET
            secretKeyRef: username
            envVarName: DATA_SOURCE_USERNAME
          - snowflakeSecret: <database>.<schema>.REDSHIFT_SECRET
            secretKeyRef: password
            envVarName: DATA_SOURCE_PASSWORD
  $$
  QUERY_WAREHOUSE = <warehouse_name>
  EXTERNAL_ACCESS_INTEGRATIONS = (REDSHIFT_EAI)
  MIN_INSTANCES = 1
  MAX_INSTANCES = 1;
```

`UNLOAD_S3_BUCKET` and `UNLOAD_IAM_ROLE_ARN` are only needed when a table’s `extraction.strategy` is `unload`; see [Migrating Data from Amazon Redshift](../data-migration-validation/migrate-redshift) and [Extraction strategies](./data-migration-configuration-reference#extraction-strategies). When you use affinity routing, set `AGENT_AFFINITY` to match the workflow’s `affinity` value (or a matching wildcard). See [Affinity](./data-migration-configuration-reference#affinity).

`scai data migrate generate-config` and `scai data validate generate-config` write the [project default affinity](./data-migration-configuration-reference#project-default-affinity) into a workflow unless you pass `--affinity`. A hand-written `AGENT_AFFINITY` doesn’t match those workflows, so generate them with the same `--affinity`. Leaving `AGENT_AFFINITY` out makes the Worker pick up every workflow’s tasks.

`DATA_SOURCE_TYPE` defaults to `sqlserver`, so set it on every Worker for another platform. For every variable the Worker container reads, with defaults and accepted values, see [Environment variables](./data-migration-configuration-reference#environment-variables).

### Instance count and resource sizing

The example above runs a single instance. Set `MIN_INSTANCES` and `MAX_INSTANCES` to the same value. Each instance runs `MAX_PARALLEL_TASKS` tasks concurrently, so total concurrency against your source is instance count × `MAX_PARALLEL_TASKS`. If you leave `MAX_PARALLEL_TASKS` out of the specification, the image runs `2` tasks per instance, not the Worker TOML default of `4`. See [Worker container: Core settings](./data-migration-configuration-reference#worker-container-core-settings).

Size each instance at roughly **1–2 vCPU and 1–2 GB per `MAX_PARALLEL_TASKS` thread**, keeping `MAX_PARALLEL_TASKS` at 5 or fewer. The example spec (`cpu: 6`, `memory: 10G`) suits a worker running 3–5 parallel tasks. Match your `resources.requests` and `resources.limits` to `MAX_PARALLEL_TASKS` and to the instance family you chose for the pool.

More Worker instances mean more throughput. Add Workers until you see diminishing returns or the source starts to struggle, then scale back. See [How many Worker instances](../data-migration-validation/deploy-workers#how-many-worker-instances).

`scai data worker setup` doesn’t apply this sizing. It creates one instance that requests `cpu: 0.1` and `memory: 2Gi`, sets no limits, and doesn’t set `MAX_PARALLEL_TASKS` or `DM_IDLE_SHUTDOWN_MINUTES`. To size a Worker that it created, change the service yourself:

- Change the instance count with `ALTER SERVICE <worker_service_name> SET MIN_INSTANCES = <n> MAX_INSTANCES = <n>`.
- Change `resources` or add variables with `ALTER SERVICE <worker_service_name> FROM SPECIFICATION`, starting from the specification that `DESCRIBE SERVICE` returns.

When `scai data worker update` moves the Worker to a new image, it drops the service and re-creates it from the deployed specification. It keeps your `resources` and variables, but the re-created service runs one instance, so set `MIN_INSTANCES` and `MAX_INSTANCES` again afterward. `scai data worker setup --yes` re-creates the service from its own specification and drops all of these changes. See [Environment variables](./data-migration-configuration-reference#environment-variables).

The Orchestrator’s idle shutdown suspends one Worker service: `DATA_EXCHANGE_WORKER_SERVICE` in the migration metadata schema (`SNOWCONVERT_AI.DATA_MIGRATION` by default), or the name passed to `scai data orchestrator setup --worker-service-name`. A Worker that you create under any other name or schema is never suspended by the Orchestrator. It suspends only itself, after its own idle period. Before each wave, resume every Worker that suspended. See [Idle shutdown with several Workers](../data-migration-validation/deploy-workers#idle-shutdown-with-several-workers).

Check that every instance came up before you start a workflow:

Copy code

```
SELECT SYSTEM$GET_SERVICE_STATUS('<worker_service_name>');
```

Every instance should report `READY`.

Also complete the **inbound access** step above: your Redshift cluster’s security group must allow connections from your account’s Snowflake egress IP ranges on port 5439.

## Passing other secrets to the Worker

The example binds the source user and password from a `PASSWORD` secret. Bind every other value marked **Secret** in [Environment variables](./data-migration-configuration-reference#environment-variables) the same way, so it doesn’t appear in `DESCRIBE SERVICE` output. For a single value, such as a Teradata JWT or a `write_nos` access key, use a `GENERIC_STRING` secret and its `secret_string` key:

Copy code

```
CREATE OR REPLACE SECRET <database>.<schema>.TERADATA_JWT_SECRET
  TYPE = GENERIC_STRING
  SECRET_STRING = '<jwt>';
```

Copy code

```
secrets:
- snowflakeSecret: <database>.<schema>.TERADATA_JWT_SECRET
  secretKeyRef: secret_string
  envVarName: TERADATA_JWT_TOKEN
```

The role that owns the service needs `USAGE` on each secret. See [Workers on Snowpark Container Services](../data-migration-validation/required-privileges#workers-on-snowpark-container-services).

## Driver download hosts by platform

Workers download some database drivers when the container starts. Include your **source host and port** in every network rule, plus the driver download hosts for your platform.

Note

Driver download hosts can change with driver or package versions. Verify the current hosts before locking down egress.

### SQL Server and Azure Synapse

On every start, the Worker container installs Microsoft ODBC Driver 18 from Microsoft’s package repository. For SQL Server it also installs the BCP tools, which `regular` extraction always uses in the container. The install runs whichever driver the connection uses, including the native `mssql-python` driver, so these hosts are always required on SPCS, in addition to your source host:

- `packages.microsoft.com:443`
- `pmc-geofence.trafficmanager.net:443`
- `deb.debian.org:80`
- `deb.debian.org:443`

If a host is missing, the driver install fails, the container exits, and SPCS restarts it repeatedly. `PREFER_NATIVE_DRIVER` (`prefer_native_driver` in Worker TOML) changes which driver the connection uses, not which hosts the container needs.

### Amazon Redshift

Recommended allowlist (plus your Redshift endpoint):

- `s3.amazonaws.com:443` (Redshift ODBC driver `.deb` download)
- `deb.debian.org:80`
- `deb.debian.org:443`

### PostgreSQL

Recommended allowlist (plus your PostgreSQL endpoint):

- `deb.debian.org:80`
- `deb.debian.org:443`

The Worker installs `odbc-postgresql` (the PostgreSQL ODBC driver) from Debian package mirrors at startup and connects through it. The image doesn’t include `psql`, so COPY extraction (`use_copy = true`) falls back to reading through the ODBC driver on SPCS. See [Migrating Data from PostgreSQL](../data-migration-validation/migrate-postgresql).

### Oracle

No driver download hosts. The Worker uses the pre-installed thin `oracledb` driver. Allow only your Oracle listener host and port.

### Teradata

The Worker installs the `teradatasql` driver from PyPI on every container start. Recommended allowlist (plus your Teradata host and port):

- `pypi.org:443`
- `files.pythonhosted.org:443`

The Worker installs the `teradatasql` Python driver from PyPI when the container starts. Without these hosts, the Worker can’t connect to Teradata.

The image doesn’t include `tbuild`, so Teradata TPT doesn’t run on SPCS. See [Teradata TPT selection](./data-migration-configuration-reference#teradata-tpt-selection).

### Google BigQuery

Recommended allowlist:

- `bigquery.googleapis.com:443` (BigQuery API: metadata, queries, and `EXPORT DATA` jobs)
- `oauth2.googleapis.com:443` (service-account token exchange)

No driver download hosts. The Worker uses the pre-installed `google-cloud-bigquery` client, with no ODBC driver. With `export_data`, BigQuery writes the Parquet files to GCS on its own side, and Snowflake reads them through the storage integration, so the Worker doesn’t need a GCS host.

Pass the service-account key to the Worker as a Snowflake secret. Base64-encode the key file and store it in a generic string secret:

Copy code

```
CREATE SECRET SNOWCONVERT_AI.DATA_MIGRATION.BIGQUERY_SA_SECRET
  TYPE = GENERIC_STRING
  SECRET_STRING = '<base64_encoded_service_account_key>';
```

Map that secret to `BIGQUERY_CREDENTIALS_JSON_BASE64` in the service spec, and set the project and dataset:

Copy code

```
          env:
            DATA_SOURCE_TYPE: bigquery
            DATA_SOURCE_PROJECT_ID: <gcp_project_id>
            DATA_SOURCE_DATABASE: <default_dataset>
            DATA_SOURCE_LOCATION: US
          secrets:
          - snowflakeSecret: BIGQUERY_SA_SECRET
            secretKeyRef: secret_string
            envVarName: BIGQUERY_CREDENTIALS_JSON_BASE64
```

Use the base64 secret rather than `BIGQUERY_CREDENTIALS_JSON`. A single-quoted `SECRET_STRING` turns the `\n` escapes inside the key’s `private_key` into real newlines, which makes the JSON invalid. Base64 has no characters that quoting can corrupt. `DATA_SOURCE_LOCATION` defaults to `US`. For `export_data`, also set `EXPORT_DATA_GCS_BUCKET` and, optionally, `EXPORT_DATA_GCS_PREFIX`.

### Azure Blob Storage for `cloud_direct`

When a table uses `cloud_direct` with an Azure Blob target, the Worker writes to the storage account itself. Allow both endpoints of the account, using your endpoint suffix if it isn’t `core.windows.net`:

- `<account>.blob.core.windows.net:443`
- `<account>.dfs.core.windows.net:443`

`scai data worker setup` adds these hosts when the Worker configuration names the account. S3 and Google Cloud Storage `cloud_direct` targets can’t be used from SPCS; see [Worker container: cloud\_direct](./data-migration-configuration-reference#worker-container-cloud-direct).

## Related content

- [Deploying workers](../data-migration-validation/deploy-workers)
- [Data migration (CLI)](./data-migration)
- [Data migration configuration reference](./data-migration-configuration-reference)
- [Environment variables](./data-migration-configuration-reference#environment-variables)
- [The SNOWCONVERT\_AI database](../data-migration-validation/snowconvert-ai-database)
