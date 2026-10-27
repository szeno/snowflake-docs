# Deploying workers

AIM DMV Workers connect to your source system and to Snowflake to move and compare data. This page covers the deployment scenarios Workers support and what you need for the most common option, Snowpark Container Services (SPCS).

For shared architecture and deployment options at a glance, see [Data Migration & Validation overview](./overview).

## Prefer automated setup

Creating Worker-related Snowflake objects by hand (secrets, network rules, external access integrations, and the service itself) is **not recommended** for routine projects. Normally the Snowflake AIM Agent for Data Warehouses or SnowConvert AI CLI (`scai data worker setup`) creates those objects for you after you provide connection details and a compute pool.

Use [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup) only when your environment requires hand-written SQL, or when you need the per-platform driver download host lists and a full service specification example.

## Deployment scenarios

Workers (and the Orchestrator) can run in several places. Mix and match per component: for example, run the Orchestrator on SPCS while Workers run in your data center, or the reverse.

| Scenario | When to use it | How setup usually works |
| --- | --- | --- |
| **Snowpark Container Services (SPCS)** | You want Worker compute inside Snowflake, without provisioning or patching your own hosts. Snowflake manages the compute pool’s lifecycle; you manage the service. | Prefer the Snowflake AIM Agent for Data Warehouses or `scai data worker setup`. See [SPCS walkthrough](#snowpark-container-services) below. |
| **Customer-hosted virtual machines or bare metal** | You want Workers close to the source system (same data center or VPC), or your organization requires source access to originate from infrastructure it directly controls. | Install the Worker binary or container runtime, provide it a TOML configuration file, and ensure it has network access to both the source system and Snowflake. Use the Snowflake AIM Agent for Data Warehouses or SnowConvert AI CLI (`scai data worker start --local <config.toml>`) to generate the configuration and start the process. |
| **Kubernetes (outside Snowflake)** | You already operate a Kubernetes cluster and want Workers managed alongside other workloads, with your own scaling, scheduling, and secrets management. | Deploy the Worker container image with your usual Kubernetes tooling (Deployment or Job, depending on whether you want it long-running or run-to-completion). Supply the same TOML configuration as a mounted config file or generated from a ConfigMap/Secret, and ensure the cluster’s egress allows the pod to reach both the source system and Snowflake. If you run multiple deployment types together, use [affinity](../manual-migration/data-migration-configuration-reference#affinity) to route each workflow to the right Worker pool. |
| **Mixed** | Different tables or source systems have different constraints, for example one source is only reachable from an on-premises network while another can be reached from SPCS. | Run multiple Worker deployments concurrently and use [affinity](../manual-migration/data-migration-configuration-reference#affinity) to route each workflow to the right Workers. |

Expand

Show lessSee more

Whichever option you choose, every Worker needs the same three things: a path to the source system, a path to Snowflake, and a Worker configuration file (TOML) describing both. See [Data migration configuration reference: Worker configuration](../manual-migration/data-migration-configuration-reference#worker-configuration) for the file format.

### Keeping source credentials out of Worker TOML

Worker configuration examples show source credentials inline for readability. How you avoid that in practice depends on where the Worker runs:

- **On SPCS**, source credentials come from Snowflake `SECRET` objects bound into the service specification. The agent or CLI creates them for you. See [Network access objects](../manual-migration/manual-spcs-worker-setup#network-access-objects).
- **On your own hosts or in Kubernetes**, the Worker can resolve credentials at startup from an external secret store, referencing them in the connection fields instead of storing a password. See [Resolving credentials from an external secret manager](../manual-migration/data-migration-configuration-reference#external-secret-manager).

## Snowpark Container Services

### When to use SPCS

Deploy on SPCS when you want Orchestrator and Worker compute inside Snowflake rather than on customer-hosted machines. You can run both components on SPCS, both outside Snowflake, or mix the two (for example Orchestrator on SPCS and Workers in your data center).

For Workers on SPCS, **Snowflake must be able to reach your source system**. That is a hard requirement: the Worker originates outbound connections from Snowflake to the source database (and often to driver download hosts). Before you choose SPCS, confirm that:

- Your account can open outbound access to the source host and port through a [network rule](/user-guide/network-rules) and an [external access integration](/developer-guide/external-network-access/external-network-access-overview).
- The source system can accept those connections (inbound allowlisting of Snowflake egress IPs). See [Allowing SPCS to reach your source system](#allowing-spcs-to-reach-your-source-system-inbound-access).

If the source is only reachable from a private network that Snowflake can’t egress to, deploy Workers on customer-hosted VMs or Kubernetes next to the source instead, and keep the Orchestrator on SPCS if you want.

### What you typically prepare

You usually create a **compute pool** and warehouse before the agent or CLI deploys services. For `INSTANCE_FAMILY` sizing and `SHOW COMPUTE POOL INSTANCE FAMILIES`, see [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup#prerequisites).

The agent or CLI then typically creates the Worker **secret**, **network rule**, **external access integration**, and **service**. Avoid recreating those by hand unless you have a reason to. Full SQL templates live on the [manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup) page.

### How many Worker instances

More Worker instances mean more concurrent extraction and load, which increases throughput. The source system is usually the constraint — keep adding Workers until you see diminishing returns or the source starts to struggle, then scale back.

Each instance runs up to `MAX_PARALLEL_TASKS` tasks concurrently (default `2` on the SPCS Worker image, and `4` for `max_parallel_tasks` in Worker TOML). Total concurrency against your source is roughly the instance count multiplied by that value, so tune both to what the source can absorb. When the source is struggling, prefer [rate limiting](../manual-migration/data-migration-configuration-reference#rate-limiting) to keep Workers up while holding back specific extraction tasks.

Prefer more Workers with a lower `MAX_PARALLEL_TASKS` (5 or fewer) over fewer Workers with many threads each. Size each instance at roughly **1–2 vCPU and 1–2 GB per `MAX_PARALLEL_TASKS` thread**. `scai data worker setup` doesn’t apply this sizing: it creates one instance that requests `cpu: 0.1` and `memory: 2Gi`, and it doesn’t set `MAX_PARALLEL_TASKS`, so the Worker runs two tasks at a time. See [Instance count and resource sizing](../manual-migration/manual-spcs-worker-setup#instance-count-and-resource-sizing).

### Orchestrator versus Worker services

| Service | Connects to source? | External Access Integration |
| --- | --- | --- |
| Orchestrator | No (Snowflake only) | Not required |
| Worker | Yes | Required when Workers reach a source database or download drivers at runtime |

Expand

Show lessSee more

Run both as **Services** (not Jobs). Both suspend themselves after a period without work. See [Controlling cost on SPCS](#controlling-cost-on-spcs).

The Orchestrator creates the AIM DMV metadata database and schema objects on startup if they do not already exist. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database) for what that database contains after setup.

### Network access for Workers

Workers in SPCS run inside Snowflake’s network. Outbound connectivity from Snowflake to the source is required: without it, the Worker can’t extract or validate data. The usual path is:

1. Allow outbound access with a network rule and external access integration (created for you by the agent or CLI in normal setups).
2. Attach that integration to the Worker service.
3. Allow inbound connections on the source system from Snowflake egress IPs (your responsibility; see the next section).

Driver download hosts and hand-written SQL for secrets, rules, and services are documented under [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup).

### Allowing SPCS to reach your source system (inbound access)

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

## Controlling cost on SPCS

On SPCS, the compute pool bills for every node while it runs, and the warehouse bills while the Orchestrator and Workers run queries on it. Three controls keep that spend bounded:

- A **budget** that suspends the warehouse and the compute pool when spend reaches a limit. You decide whether to create one.
- A **compute pool** sized to what the migration needs. You choose its node counts.
- **Idle shutdown**, which suspends the services when there’s no work. It’s always on.

### Capping spend with a budget

A [custom budget](/user-guide/budgets/custom-budget) can track the migration warehouse and the compute pool together and call a stored procedure when spend reaches a threshold. Use that procedure as a stop action: it turns off auto-resume on both objects and then suspends them, so nothing restarts them until you do. [Resource monitors](/user-guide/resource-monitors) don’t cover compute pools, so they can’t replace the budget on SPCS.

When you deploy on SPCS with the Snowflake AIM Agent for Data Warehouses, the agent offers this budget before it starts the services for the first time. It runs nothing until you agree, and it continues without a cap if you decline.

**Prompt:**

Copy code

```
Cap the migration's spend at 200 credits a month.
```

The agent asks for the monthly limit in credits, the threshold (default 100% of the limit), and whether to trigger on actual or projected spend. It checks whether the warehouse or the pool is already in another budget and asks before it moves either object to the new budget. It lists any missing privileges as `GRANT` statements for an administrator, shows the SQL before it runs it, and reads the budget back afterward.

To create the same guardrail yourself, first check that neither object is in another budget. Each call returns `[]` when no budget tracks the object:

Copy code

```
SELECT SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('WAREHOUSE', '<warehouse>');
SELECT SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('COMPUTE_POOL', '<compute_pool>');
```

Then run the following as the role that you want to own the budget. Use the warehouse that the Orchestrator and the Workers run on, not the warehouse of your current session. If they use different warehouses, add each one. `<POOL_ID>` is the pool name in uppercase, with every character other than letters, digits, and `_` replaced by `_`. These are the names that the agent uses:

Copy code

```
CREATE SCHEMA IF NOT EXISTS SNOWCONVERT_AI.BUDGETS;

-- The budget and its monthly limit in credits
CREATE SNOWFLAKE.CORE.BUDGET IF NOT EXISTS SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET();
CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!SET_SPENDING_LIMIT(<limit>);

-- The two objects it tracks
CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!ADD_RESOURCE(
  SELECT SYSTEM$REFERENCE('WAREHOUSE', '<warehouse>', 'SESSION', 'APPLYBUDGET'));
CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!ADD_RESOURCE(
  SELECT SYSTEM$REFERENCE('COMPUTE_POOL', '<compute_pool>', 'SESSION', 'APPLYBUDGET'));

-- The stop action. Auto-resume goes off first so that nothing restarts either object.
-- It attempts all four changes, skips a suspend only for an object that is already
-- suspended, and fails if any change failed, so that Snowflake retries the action.
CREATE OR REPLACE PROCEDURE SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_STOP()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
  failed BOOLEAN DEFAULT FALSE;
  obj_state STRING;
  stop_failed EXCEPTION (-20001, 'DMV budget stop failed: <warehouse> or <compute_pool> might still be running.');
BEGIN
  BEGIN
    ALTER WAREHOUSE <warehouse> SET AUTO_RESUME = FALSE;
  EXCEPTION
    WHEN OTHER THEN failed := TRUE;
  END;
  BEGIN
    ALTER COMPUTE POOL <compute_pool> SET AUTO_RESUME = FALSE;
  EXCEPTION
    WHEN OTHER THEN failed := TRUE;
  END;
  BEGIN
    obj_state := NULL;
    SHOW WAREHOUSES LIKE '<warehouse>';
    SELECT "state" INTO :obj_state FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
      WHERE UPPER("name") = UPPER('<warehouse>');
    IF (obj_state IS DISTINCT FROM 'SUSPENDED') THEN
      ALTER WAREHOUSE <warehouse> SUSPEND;
    END IF;
  EXCEPTION
    WHEN OTHER THEN failed := TRUE;
  END;
  BEGIN
    obj_state := NULL;
    SHOW COMPUTE POOLS LIKE '<compute_pool>';
    SELECT "state" INTO :obj_state FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
      WHERE UPPER("name") = UPPER('<compute_pool>');
    IF (obj_state IS DISTINCT FROM 'SUSPENDED') THEN
      ALTER COMPUTE POOL <compute_pool> SUSPEND;
    END IF;
  EXCEPTION
    WHEN OTHER THEN failed := TRUE;
  END;
  IF (failed) THEN
    RAISE stop_failed;
  END IF;
  RETURN 'DMV warehouse and compute pool suspended by budget';
END;
$$;

-- The SNOWFLAKE application calls the procedure. Grant again whenever you replace it.
GRANT USAGE ON DATABASE SNOWCONVERT_AI TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA SNOWCONVERT_AI.BUDGETS TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_STOP() TO APPLICATION SNOWFLAKE;

-- Call the stop when actual spend reaches 100% of the limit.
CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE('PROCEDURE', 'SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_STOP()', 'SESSION', 'USAGE'),
  ARRAY_CONSTRUCT(),
  'ACTUAL',
  100);
```

The role needs these privileges:

| Needed for | Privileges |
| --- | --- |
| Creating the budget and the procedure | The `SNOWFLAKE.BUDGET_CREATOR` and `SNOWFLAKE.USAGE_VIEWER` database roles, `USAGE` on the database, and `CREATE SNOWFLAKE.CORE.BUDGET` and `CREATE PROCEDURE` on the schema |
| Adding the two objects | `APPLYBUDGET` on the warehouse and on the compute pool |
| The stop, which runs with the owner’s rights | `OPERATE` and `MODIFY` on the warehouse and on the compute pool |

Expand

Show lessSee more

To confirm that the budget can call the stop, run `CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!CONFIRM_CUSTOM_ACTIONS_ACCESS();` and check that `IS_VALID` is `TRUE`. Keep the budget in its own schema, as here, so that cleaning up the migration schemas never drops it. For the budget methods, see [Custom budgets](/user-guide/budgets/custom-budget) and [Custom actions for budgets](/user-guide/budgets/custom-actions). The budget itself incurs a small serverless compute cost; see [Understanding budget costs](/user-guide/budgets/cost).

Before you rely on the budget, know how it behaves:

- **It’s a backstop, not a meter.** A budget refreshes up to every 6.5 hours, so spend can pass the threshold before the stop runs. See [Adjusting the budget refresh interval](/user-guide/budgets#label-budgets-refresh-interval).
- **Actions run at most once per period.** An `ACTUAL` action runs at most once a month, and a `PROJECTED` one at most once a day. After a stop and a recovery in the same month, an `ACTUAL` stop doesn’t run again until the next month. Snowflake retries a failed action once, so check the state of both objects after a budget notification.
- **It stops everything on those objects.** Suspending the warehouse affects every other workload that uses it, and suspending the pool suspends every service in it. Use a dedicated warehouse if the cap must stop only the migration.
- **Running queries aren’t canceled.** Suspending a warehouse lets its running queries finish.

After a stop, raise the limit if the migration needs more, turn auto-resume back on, and then resume the services as described in [Resuming services before the next wave](#resuming-services-before-the-next-wave):

Copy code

```
CALL SNOWCONVERT_AI.BUDGETS.DMV_<POOL_ID>_BUDGET!SET_SPENDING_LIMIT(<new_limit>);
ALTER WAREHOUSE <warehouse> SET AUTO_RESUME = TRUE;
ALTER COMPUTE POOL <compute_pool> SET AUTO_RESUME = TRUE;
```

### Sizing the compute pool for cost

Every node counted in `MIN_NODES` bills whenever the pool runs, even while the services are idle. Create the pool with `MIN_NODES = 1`, and use `MAX_NODES` as the cost ceiling:

- **Services that `scai` creates:** keep `MAX_NODES = 1` unless they don’t fit. `scai data orchestrator setup` and `scai data worker setup` request `cpu: 0.1` and `memory: 2Gi` for each service and set no limits, so a node holds as many of them as fit in its memory at 2Gi each.
- **Workers whose resource requests you raised:** set `MAX_NODES` to `2` or `3`, enough nodes for the Orchestrator and two or three Worker instances. A pool wider than the source system can feed adds cost, not throughput.

Don’t set a large `MIN_NODES` for a heavy wave. Raise `MAX_NODES` and the Worker’s `MAX_INSTANCES` for that wave, and lower them again afterward. For instance families and per-instance sizing, see [Compute pool sizing](../manual-migration/manual-spcs-worker-setup#compute-pool-sizing).

### Idle shutdown

The Orchestrator and every Worker shut themselves down after a period without work. The period is `DM_IDLE_SHUTDOWN_MINUTES`, `60` minutes by default, and each process reads its own value. You can’t turn idle shutdown off. For the settings, see [Idle shutdown settings](../manual-migration/data-migration-configuration-reference#idle-shutdown-settings).

- **The Orchestrator** shuts down when it has had no active, pending, or upcoming work for the whole period. On SPCS, it first suspends the one Worker service named in `DM_SPCS_SUSPEND_AGENT_SERVICE`, and then suspends its own service. `scai data orchestrator setup` sets that variable to `DATA_EXCHANGE_WORKER_SERVICE`, or to the name that you pass with `--worker-service-name`.
- **Each Worker** shuts down when it has pulled no tasks and held none for the whole period. On SPCS, it suspends its own service. On your own hosts or in Kubernetes, the Worker process exits, and your process manager decides whether to restart it.

A Worker takes its period from `DM_IDLE_SHUTDOWN_MINUTES`, or from `[idle_shutdown]` `minutes` in its TOML when the variable is unset. `scai` sets neither, so every service it creates uses 60 minutes. To change the period of an SPCS service, add the variable to its service specification.

The compute pool’s `AUTO_SUSPEND_SECS` is a separate, later step. The pool suspends only when no service is running in it, so `AUTO_SUSPEND_SECS` starts counting after idle shutdown has suspended every service in the pool. Idle shutdown stops the services; `AUTO_SUSPEND_SECS` then stops the pool’s nodes from billing. See [Compute pool sizing](../manual-migration/manual-spcs-worker-setup#compute-pool-sizing).

### Idle shutdown with several Workers

`DM_SPCS_SUSPEND_AGENT_SERVICE` holds one service name. When you run several Worker services, the Orchestrator suspends only the one whose name you passed to `--worker-service-name`. Every other Worker service is suspended only by its own idle shutdown.

With several Workers, keep these points in mind:

- **The other Workers depend on their own period.** A Worker whose `DM_IDLE_SHUTDOWN_MINUTES` is longer keeps running after the Orchestrator has suspended, and keeps the pool from suspending.
- **A failed self-suspend has no fallback for most Workers.** If a Worker can’t suspend its own service, it stays up and retries after 1, 2, 4, 8, and 16 minutes, then waits for another full idle period. The Orchestrator still suspends the Worker named in `--worker-service-name`, but no other.
- **A Worker that you create by hand follows the same rule.** The Orchestrator suspends it only when it’s `DATA_EXCHANGE_WORKER_SERVICE` in the migration metadata schema (`SNOWCONVERT_AI.DATA_MIGRATION` by default), or the service whose name you passed to `--worker-service-name`.

After a wave, run `scai data worker list` and check that every Worker is `SUSPENDED`. Suspend any that isn’t with `scai data worker stop --service-name <name>`.

### Resuming services before the next wave

A suspended service stays suspended until you resume it. Submitting a workflow with `scai data migrate create-workflow` or `scai data validate create-workflow` doesn’t resume it. Before the next wave, resume the Orchestrator and every Worker service, including the ones that suspended themselves:

Copy code

```
scai data orchestrator start
scai data worker start --service-name <worker_service_name>
```

- Without `--service-name`, `scai data worker start` resumes `DATA_EXCHANGE_WORKER_SERVICE`.
- If the compute pool has suspended too, for example after `AUTO_SUSPEND_SECS` or a budget stop, add `--resume-compute-pool`. Without it, the command fails while the pool is suspended.
- A workflow that you submit while its Workers are suspended stays `pending` until you resume them.

## Related content

- [Data Migration & Validation overview](./overview)
- [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup)
- [Data migration](./data-migration)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [Data validation](./data-validation)
- [Data migration configuration reference](../manual-migration/data-migration-configuration-reference)
- [Data migration (CLI)](../manual-migration/data-migration)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
