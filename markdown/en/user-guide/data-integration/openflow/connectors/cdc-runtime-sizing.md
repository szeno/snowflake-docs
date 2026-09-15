# Runtime sizing and packing for CDC connectors

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes how to size an Openflow runtime for change data capture (CDC) connectors,
how many connectors you can run on one runtime, and what to do when you need a different size
after a connector is already installed.

The guidance applies to all Openflow CDC connectors, because the sizing thresholds are expressed
in replication throughput rather than in terms of any particular source database.

## Size a runtime

Each runtime has a **node type** (Small, Medium, or Large) and a **node type tier** that
determines the CPU and heap memory available to each node. Choose both when you create the
runtime. You can change the tier within the same node type after creation using the UI or
[ALTER OPENFLOW RUNTIME](/sql-reference/sql/alter-openflow-runtime); you can’t change the node type itself.

| Tier | Node type | CPUs per node | Heap per node |
| --- | --- | --- | --- |
| S1 | Small | 1 | 4 GB |
| S2 | Small | 2 | 8 GB |
| S3 | Small | 3 | 12 GB |
| M4 | Medium | 4 | 16 GB |
| M6 | Medium | 6 | 24 GB |
| L8 | Large | 8 | 33 GB |

Expand

Show lessSee more

Size the runtime based on the sustained workload it needs to handle across all connectors running
on it. Sustained means typical steady-state throughput, not peak. Peak load can temporarily
increase connector queues and end-to-end replication latency; the workload catches up when the
load drops back to the steady-state level.

The following ranges are starting points based on internal benchmarks and production customer
data. They aren’t service guarantees. Your fit depends on row size, event distribution, schema
width, and source burstiness. Start at the lower bound, measure runtime CPU, memory, queue depth,
and end-to-end replication latency in production, then increase from there.

- Light workload (aggregate sustained throughput below approximately 1,000 events per second,
  fewer than approximately 100 actively changing tables): a Small runtime can host a
  single low-volume connector on S1, approximately two on S2, and approximately three to
  four on S3. Pack additional connectors on Small only when each source is genuinely light.
- Moderate workload (approximately 1,000 to 5,000 events per second, hundreds of actively
  changing tables): a Medium runtime can typically host approximately 5 to 8 connectors on
  M4, and approximately 7 to 10 on M6.
- Heavy workload (approximately 5,000 to 15,000 events per second, hundreds to low thousands of
  actively changing tables): a Large runtime (L8) can typically host 15 or more connectors.
  If you want better resource isolation, split the load across multiple smaller runtimes
  instead. That prevents one problematic connector from affecting the others.

For the steps to create a runtime at the size you choose, see
[Set up Openflow - Snowflake Deployment: Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime).

## Run multiple connectors on one runtime

You can run multiple CDC connector instances on a single runtime. This is useful for replicating
many small databases, for example a multi-tenant SaaS with one database per tenant, or a fleet of
operational databases per business unit or region.

Important

Run a connector on a dedicated runtime, not packed with others, when any of the following applies:

- A single source sustains more than approximately 15,000 events per second.
- You need sub-1-minute end-to-end replication latency under load.
- You can’t tolerate noisy-neighbor effects from other sources sharing the runtime.

Each replicated table can consume two Snowpipe Streaming pipes: one for snapshot replication and
one for incremental replication. As you pack more tables onto a runtime, check your account’s
[Snowpipe Streaming pipe limit](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-limitations#pipe-limits)
and raise it before you approach the cap.

How you configure multiple connector instances on one runtime depends on the generation:

- **Gen 2**: each connector instance carries its own configuration, so running multiple
  instances on one runtime is just installing each connector on the same runtime. There is
  no shared configuration to inherit or override.
- **Gen 1**: each connector instance uses Source, Destination, and Ingestion parameter
  contexts. The Ingestion context inherits from the Source and Destination contexts, so any
  value you don’t override in Ingestion resolves from the parent context. The rest of this
  section describes the recommended gen 1 setup.

### Use shared Source and Destination contexts with per-connector overrides in Ingestion

Snowflake recommends this setup for running multiple CDC connector instances manually. It’s the
same pattern the openflow skill applies automatically at scale.

Tip

You don’t have to configure multiple CDC connector instances by hand. The **openflow skill in
Snowflake CoCo** is the recommended path when you need to run many CDC connectors on one runtime.
The skill applies this pattern consistently across the connector fleet. To get started, install
and connect the [Snowflake CoCo CLI](/user-guide/cortex-code/cortex-code-cli), then ask the
bundled [openflow skill](/user-guide/cortex-code/bundled-skills#label-bundled-skill-openflow) to
configure the layout.

When you import more than one CDC connector instance of the same type into one runtime, keep the
Source and Destination contexts at their default names and let every connector instance inherit
from them. In that connector’s Ingestion parameter context, override only the values that differ
from the shared defaults: the connection URL, replication slot or server ID, destination
database, and table list. Leave shared values, such as the Snowflake role, warehouse, and JDBC
driver, in the Source and Destination contexts so every connector instance inherits them.

Use the following process for each additional connector instance:

1. Import the connector instance.
2. Confirm that its Ingestion context inherits from the existing Source and Destination contexts,
   instead of creating a new set of Source and Destination contexts.
3. In the Ingestion context, override every value that must differ from the shared defaults: at
   minimum, the source connection identity (for example, the JDBC URL and replication slot or
   server ID) and the destination database.
4. Confirm that the connector replicates from the correct source into the correct destination
   before moving on to the next connector instance.

### Don’t rename the Source and Destination contexts

Don’t rename the Source or Destination parameter contexts to make them unique per connector
instance. Renaming these contexts might seem like a simpler way to keep each connector instance
visually distinct, but it silently breaks future connector version upgrades.

When Snowflake ships a connector version that adds a new parameter to the Source or Destination
context, the upgrade process looks for a context with the connector’s default name to apply that
new parameter to. If you renamed the context, the upgrade process can’t find it, and the new
parameter isn’t added to the context your connector instances actually use. Your connector
instances then silently fall out of sync with the new version, and the Snowflake registry can’t
repair this automatically. This risk applies whether you rename the contexts to a single shared
alternate name or to a distinct name per connector instance.

The Ingestion context is safe to rename, because the registry creates a fresh Ingestion context
for every new connector instance. Renaming it doesn’t affect any other connector instance or any
future upgrade. If you want every connector instance to be individually identifiable in the
parameter context list, rename only its Ingestion context, for example to the source database
name, tenant name, or region.

### Avoid unintended inheritance from an earlier connector instance

The most common mistake when importing an additional CDC connector instance is unintentionally
reusing the previous instance’s Ingestion context, instead of creating a dedicated context. If
this happens, the new connector instance uses the earlier instance’s source database, destination
database, table list, replication slot, server ID, or XStream configuration, and replicates the
wrong data without any error.

After importing each additional connector instance, always confirm that its Ingestion context is
new and dedicated to that instance, and not shared with any earlier connector instance. If the
import wizard offers an option to inherit existing parameter contexts, confirm that it creates a
new Ingestion context rather than reusing an existing one.

## Resize a runtime

Openflow supports two types of resize depending on what you need to change.

### Resize within the same node type

To change the tier within the same node type (for example, S1 to S2, or M4 to M6), use
the Openflow UI or SQL. No connector migration is needed.

The most common reason to resize within a node type is that connectors are failing or running
slowly due to insufficient CPU or heap memory at the current tier. To measure CPU usage on
your runtime, use the high CPU query in the
[monitoring guide](/user-guide/data-integration/openflow/monitor).

**Using the Openflow UI:**

1. In the runtime list, open the menu for the runtime you want to resize.
2. Select **Edit runtime**.
3. Change the **Node type tier** to the tier you want.
4. Select **Save**.

**Using SQL:**

Copy code

```
ALTER OPENFLOW RUNTIME my_runtime SET NODE_TYPE_TIER = 'S2';
```

### Change the node type

A runtime’s node type is fixed at creation. To switch from one node type to another (for
example, Small to Medium), you need a new runtime of the target node type. You have two options
depending on whether you want to preserve the current replication progress.

If you don’t need to keep the progress of the current connector, the simplest path is to create a
new runtime of the node type you need and install a new connector instance on it. The new connector
starts from scratch: it snapshots all configured tables and then captures ongoing changes from
that point. The replication progress of the existing connector is discarded.

To keep the progress of the current connector, for example to avoid re-snapshotting tables that
took a long time to snapshot initially, migrate the connector to the new runtime. This reuses the
existing destination tables and resumes incremental replication from where it left off. For the
migration steps, which differ by source, see the reinstall or migration instructions for the
connector you are running.
