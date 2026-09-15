# Manual SPCS worker setup

This page is for operators who need to create Snowpark Container Services (SPCS) Worker objects by hand. For most projects, prefer the Snowflake AIM Agent for Data Warehouses or SnowConvert AI CLI (`scai data worker setup`), which create the secret, network rule, external access integration, and service for you. Manual creation is not recommended unless your environment requires it.

For deployment scenarios and when to use SPCS versus customer-hosted Workers, see [Deploying workers](../data-migration-validation/deploy-workers).

## Prerequisites

Prepare these objects before creating a Worker service (the agent or CLI can help with images; you usually create the compute pool yourself):

1. **Compute pool**: hosts the SPCS services.

Copy code

```
CREATE COMPUTE POOL <compute_pool_name>
  MIN_NODES = 1
  MAX_NODES = <max_nodes>
  INSTANCE_FAMILY = <instance_family>;
```

Choose an instance family whose per-node vCPU and memory can fit the Worker instances you want. To list families available in your account:

Copy code

```
SHOW COMPUTE POOL INSTANCE FAMILIES;
```

See [Compute pool sizing](#compute-pool-sizing) for how to size the pool.

2. **Image repository**: stores Orchestrator and Worker container images. Your role needs WRITE on the repository.
3. **Container images**: push Orchestrator and Worker images to the repository. The Snowflake AIM Agent for Data Warehouses or SnowConvert AI CLI can help with image preparation and upload.
4. **Warehouse**: a warehouse for the service specification’s `QUERY_WAREHOUSE`.

### Compute pool sizing

Size the pool based on how many Worker instances you want and how many parallel tasks each one runs.

Each Worker instance needs roughly **1–2 vCPU and 1–2 GB of memory per `MAX_PARALLEL_TASKS` thread**. Keep `MAX_PARALLEL_TASKS` at 5 or fewer per instance and prefer more instances over higher thread counts per instance. Set the service `resources.requests` and `resources.limits` to match.

Then choose an instance family and node count so the pool can fit all your Worker instances. The specific family doesn’t matter — what matters is that the per-node vCPU and memory are large enough for the instances you want to schedule on each node. Run `SHOW COMPUTE POOL INSTANCE FAMILIES` and pick one that fits. The pool scales the number of **nodes**; Worker count is set with `MIN_INSTANCES` and `MAX_INSTANCES` on the service.

The Orchestrator needs roughly 1 vCPU and 2 GB. It can share a compute pool with the Workers, or run in its own single-node pool.

Consider `AUTO_SUSPEND_SECS = 60` on the pool so it goes cold about a minute after the services suspend. Resuming costs roughly 30 to 60 seconds of warm-up, so raise the value if your migration waves run back to back.

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

When you use SnowConvert AI CLI (`scai data worker setup`) with a SQL Server source connection, the CLI can create these objects automatically. Use this page when you need to create them yourself (for example for other platforms, or when you use `--skip-egress`).

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
          image: <your_image_repository>/data-exchange-agent:redshift
          env:
            # Source system
            DATA_SOURCE_HOST: <redshift_endpoint>
            DATA_SOURCE_PORT: 5439
            DATA_SOURCE_DATABASE: <source_database>

            # Snowflake
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
          - snowflakeSecret: REDSHIFT_SECRET
            secretKeyRef: USERNAME
            envVarName: DATA_SOURCE_USERNAME
          - snowflakeSecret: REDSHIFT_SECRET
            secretKeyRef: PASSWORD
            envVarName: DATA_SOURCE_PASSWORD
  $$
  EXTERNAL_ACCESS_INTEGRATIONS = (REDSHIFT_EAI)
  MIN_INSTANCES = 1
  MAX_INSTANCES = 1;
```

`UNLOAD_S3_BUCKET` and `UNLOAD_IAM_ROLE_ARN` are only needed when a table’s `extraction.strategy` is `unload`; see [Migrating Data from Amazon Redshift](../data-migration-validation/migrate-redshift) and [Extraction strategies](./data-migration-configuration-reference#extraction-strategies). When you use affinity routing, set `AGENT_AFFINITY` to match the workflow’s `affinity` value (or a matching wildcard). See [Affinity](./data-migration-configuration-reference#affinity).

### Instance count and resource sizing

The example above runs a single instance. Set `MIN_INSTANCES` and `MAX_INSTANCES` to the same value. Each instance runs `MAX_PARALLEL_TASKS` tasks concurrently, so total concurrency against your source is instance count × `MAX_PARALLEL_TASKS`.

Size each instance at roughly **1–2 vCPU and 1–2 GB per `MAX_PARALLEL_TASKS` thread**, keeping `MAX_PARALLEL_TASKS` at 5 or fewer. The example spec (`cpu: 6`, `memory: 10G`) suits a worker running 3–5 parallel tasks. Match your `resources.requests` and `resources.limits` to `MAX_PARALLEL_TASKS` and to the instance family you chose for the pool.

More Worker instances mean more throughput. Add Workers until you see diminishing returns or the source starts to struggle, then scale back. See [How many Worker instances](../data-migration-validation/deploy-workers#how-many-worker-instances).

Check that every instance came up before you start a workflow:

Copy code

```
SELECT SYSTEM$GET_SERVICE_STATUS('SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_SERVICE');
```

Every instance should report `READY`.

Also complete the **inbound access** step above: your Redshift cluster’s security group must allow connections from your account’s Snowflake egress IP ranges on port 5439.

## Driver download hosts by platform

Workers download some database drivers when the container starts. Include your **source host and port** in every network rule, plus the driver download hosts for your platform.

Note

Driver download hosts can change with driver or package versions. Verify the current hosts before locking down egress.

### SQL Server and Azure Synapse

SQL Server connections prefer the bundled `mssql-python` driver when the Worker includes the `sqlserver` extra. This path doesn’t require unixODBC or `msodbcsql`. SQL Server BCP extraction and the ODBC fallback still use Microsoft packages downloaded at container startup.

If you use BCP or the ODBC fallback, add the following authoritative allowlist entries in addition to your source host:

- `packages.microsoft.com:443`
- `pmc-geofence.trafficmanager.net:443`
- `deb.debian.org:80`
- `deb.debian.org:443`

Set `prefer_native_driver = false` in the SQL Server source connection only when you need to force the ODBC fallback.

### Amazon Redshift

Recommended allowlist (plus your Redshift endpoint):

- `s3.amazonaws.com:443` (Redshift ODBC driver `.deb` download)
- `deb.debian.org:80`
- `deb.debian.org:443`

### PostgreSQL

Recommended allowlist (plus your PostgreSQL endpoint):

- `deb.debian.org:80`
- `deb.debian.org:443`

The Worker installs `odbc-postgresql` from Debian package mirrors at startup.

### Oracle

No driver download hosts. The Worker uses the pre-installed thin `oracledb` driver. Allow only your Oracle listener host and port.

### Teradata

No driver download hosts. The Worker uses the pre-installed `teradatasql` driver. Allow only your Teradata host and port.

## Related content

- [Deploying workers](../data-migration-validation/deploy-workers)
- [Data migration (CLI)](./data-migration)
- [Data migration configuration reference](./data-migration-configuration-reference)
- [The SNOWCONVERT\_AI database](../data-migration-validation/snowconvert-ai-database)
