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

You usually create a **compute pool** (and often an image repository and warehouse) before the agent or CLI deploys services. For `INSTANCE_FAMILY` sizing and `SHOW COMPUTE POOL INSTANCE FAMILIES`, see [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup#prerequisites).

The agent or CLI then typically creates the Worker **secret**, **network rule**, **external access integration**, and **service**. Avoid recreating those by hand unless you have a reason to. Full SQL templates live on the [manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup) page.

### How many Worker instances

More Worker instances mean more concurrent extraction and load, which increases throughput. The source system is usually the constraint — keep adding Workers until you see diminishing returns or the source starts to struggle, then scale back.

Each instance runs up to `MAX_PARALLEL_TASKS` tasks concurrently (default `4`). Total concurrency against your source is roughly the instance count multiplied by that value, so tune both to what the source can absorb. When the source is struggling, prefer [rate limiting](../manual-migration/data-migration-configuration-reference#rate-limiting) to keep Workers up while holding back specific extraction tasks.

Prefer more Workers with a lower `MAX_PARALLEL_TASKS` (5 or fewer) over fewer Workers with many threads each. Size each instance at roughly **1–2 vCPU and 1–2 GB per `MAX_PARALLEL_TASKS` thread**. See [Instance count and resource sizing](../manual-migration/manual-spcs-worker-setup#instance-count-and-resource-sizing).

### Orchestrator versus Worker services

| Service | Connects to source? | External Access Integration |
| --- | --- | --- |
| Orchestrator | No (Snowflake only) | Not required |
| Worker | Yes | Required when Workers reach a source database or download drivers at runtime |

Expand

Show lessSee more

Run both as **Services** (not Jobs), monitor usage, and suspend when idle.

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

## Related content

- [Data Migration & Validation overview](./overview)
- [Manual SPCS worker setup](../manual-migration/manual-spcs-worker-setup)
- [Data migration](./data-migration)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [Data validation](./data-validation)
- [Data migration configuration reference](../manual-migration/data-migration-configuration-reference)
- [Data migration (CLI)](../manual-migration/data-migration)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
