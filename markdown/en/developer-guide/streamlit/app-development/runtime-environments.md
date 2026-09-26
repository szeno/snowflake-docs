# Runtime environments for Streamlit apps

Streamlit in Snowflake offers two types of runtime environments for Streamlit apps:

- **Container runtime**: Serves an app as a long-running service and creates a dedicated
  instance of the app that is shared among all viewers.
- **Warehouse runtime**: Runs on-demand and creates a personal instance of the app for each
  viewer.

Note

If you use the CREATE STREAMLIT command with the ROOT\_LOCATION parameter, your app can only
use a warehouse runtime and is subject to additional limitations. This page covers apps
created with the FROM parameter. For more information, see [Understanding the different types of Streamlit objects](/developer-guide/streamlit/migrations-and-upgrades/overview).

The following table compares the features supported by warehouse runtimes and container runtimes for Streamlit in Snowflake apps.

| Supported features | Warehouse runtime | Container runtime |
| --- | --- | --- |
| Compute | Virtual warehouse for app code and internal queries. | [Compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) node for app code. Virtual warehouse for internal queries. |
| Execution length | Configurable with a [sleep timer](/developer-guide/streamlit/features/sleep-timer). | Suspension after three days of viewer inactivity. |
| Maintenance window | Not applicable. | Subject to the Snowpark Container Services [maintenance window](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-maintenance-window). |
| Base image | Linux in a Python stored procedure. | Linux in a Snowpark container. |
| Python versions | 3.9, 3.10, 3.11 | 3.11 |
| Streamlit versions | 1.22+ (limited selection). | 1.50+ (any version, including `streamlit-nightly` versions). |
| Dependencies | Packages from the Snowflake Conda channel via `environment.yml`. | Packages from an external package index like PyPI via `pyproject.toml` or `requirements.txt`. |
|  | Pin versions with the `=` operator. | Pin versions with the `==` operator. |
|  | Use version ranges with the `*` wildcard. | Use version ranges with `<`, `<=`, `>=`, `>`, and comma-separated lists. |
| Entrypoint location | Root of your source directory. | Root or subdirectory within your source directory. |
| Streamlit server | Temporary, individual instance of the Streamlit server for each viewer session. | Persistent, shared server instance for all viewer sessions. |
|  | Doesn’t share disk, compute, and memory resources between viewer sessions. | Shares disk, compute, and memory resources between viewer sessions. |
|  | Doesn’t support caching between sessions. | Fully supports Streamlit’s caching features. |
| Startup times | Slower per viewer session due to on-demand app creation. | Faster per viewer session but slower deployment due to container startup. |
| Access | Requires ownership to edit. | Same as warehouse runtime. |
|  | Uses owner’s rights for queries, limited similarly to owner’s rights stored procedures. | Uses owner’s rights for queries by default. Supports [restricted caller’s rights (Preview)](/developer-guide/streamlit/features/restricted-callers-rights) on some or all queries. |
| Logging | Event table logging and tracing via the [telemetry framework](/developer-guide/logging-tracing/logging-tracing-overview). | Live console logs and historical event table logs. |

Expand

Show lessSee more

## Container runtimes

Feature — Generally Available

Not supported in government regions.

A container runtime provides a dedicated instance of your Streamlit app that is shared
among all viewers. Each viewer connects to the same instance of the app, which means
viewers connect quickly to an already-live app. Containers cost significantly less
than warehouses per minute and are generally a more cost effective hosting solution,
especially for apps with frequent usage.

Container runtimes share disk, compute, and memory resources between viewer sessions.
This means you can fully take advantage of Streamlit’s caching features to improve
performance. Efficient app design is important with container runtimes to ensure that
all viewers have a good experience.

With an external access integration, you can install Python packages from PyPI or other
package indexes that support the [simple repository API](https://peps.python.org/pep-0503/).
This makes container runtimes more flexible. You’ll always have access to the latest
version of Streamlit, including `streamlit-nightly` versions. Container runtimes also
support [restricted caller’s rights (Preview)](/developer-guide/streamlit/features/restricted-callers-rights).

Note

You can also run a Streamlit app on a container runtime inside a Snowflake Native App, where the app
creates and owns the compute pool in the consumer account. That path has additional requirements,
including manifest privileges and an app specification for external access. For more information,
see [Container runtime](/developer-guide/native-apps/adding-streamlit#label-streamlit-container-runtime-na).

## Warehouse runtimes

Warehouse runtimes provide an on-demand, personal instance of the Streamlit app for
each viewer. When a viewer opens the app, a new instance of the app is created for
that viewer. Each viewer has their own isolated environment, which increases user
load times. While both runtimes execute SQL queries using the owner’s privileges,
apps using warehouse runtimes are subject to similar restrictions as owner’s rights
stored procedures. For more information, see [Owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights#label-stored-procedure-session-state-owners).

## Guidelines for selecting resources in Streamlit in Snowflake

When you run a Streamlit app in Streamlit in Snowflake, multiple factors may affect performance, including
the complexity of the Streamlit app, availability of warehouses, and latency. The following
sections provide general guidelines for using virtual warehouses and compute pools in Streamlit in Snowflake.

### Selecting a compute pool

When you use a container runtime, you must select a compute pool to run the Streamlit app.

When you select `SYSTEM_COMPUTE_POOL_CPU` as the compute pool for your
Streamlit app, Snowflake runs three apps per compute pool node.
Otherwise, each Streamlit app runs on a single compute pool node; a Streamlit
app takes an entire node.

The size of the compute pool node affects the performance of the app. Larger node sizes can
be used if your app requires more memory. However, because Streamlit runs as a single process,
your app is unlikely to benefit from multiple CPUs. For more information, see
[Creating a compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-creating-compute-pool).

Tip

- To reduce friction when you add more apps in the future, set MAX\_NODES to
  account for future Streamlit apps.
- To ensure that app creation is fast, create your compute pool with MIN\_NODES
  equal to the number of apps you intend to run simultaneously, including testing
  and experiments.
- To reduce costs, use smaller node sizes.
- Both node quantity and node size impact costs. For more information, see
  [Compute pool cost](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-compute-pool-cost).

For example, the following command creates a compute pool to run two to five
Streamlit apps simultaneously:

Copy code

```
CREATE COMPUTE POOL streamlit_compute_pool
 MIN_NODES = 2
 MAX_NODES = 5
 INSTANCE_FAMILY = CPU_X64_XS;
```

### Selecting a virtual warehouse

To optimize costs, performance, and monitoring, use separate compute resources for
running your app and executing queries within your app. If you use a container runtime,
your compute resources are automatically separated because your app code runs on a
compute pool node and its queries run on a virtual warehouse. If you use a warehouse
runtime, your app will use the same warehouse to run your app code and execute queries
unless you activate a different query warehouse within your app code.

For example, with a warehouse runtime, you might use an X-Small warehouse to run your
Python code and activate a Large query warehouse in your app to run complex queries.

Note

In the CREATE STREAMLIT and ALTER STREAMLIT commands, the QUERY\_WAREHOUSE parameter
should be used differently depending on the runtime type:

- For container runtimes, QUERY\_WAREHOUSE sets the query warehouse for executing queries
  within the app.
- For warehouse runtimes, QUERY\_WAREHOUSE sets the code warehouse for running the app code.
  If you don’t activate a different warehouse within your app code, the same warehouse will
  be used for executing queries.

#### Best practices for query warehouses

In a Streamlit app, to select a query warehouse, follow the same general guidelines
as you would for any other Snowflake workload. Consider the complexity of the queries,
the size of the data being queried, and the expected concurrency when selecting a warehouse size.

If your app uses a container runtime, use the QUERY\_WAREHOUSE parameter to set the query warehouse
when you create or alter the Streamlit app. However, if your app uses a warehouse runtime, use the
QUERY\_WAREHOUSE parameter to set your code warehouse. You should generally use a smaller, dedicated
warehouse for running the app code and manually switch to different query warehouse within your app code.

**Example: Container runtime**

When you use a container runtime, set a sufficiently large query warehouse to run your app’s internal queries:

Copy code

```
CREATE STREAMLIT my_app
FROM '@my_stage/app_folder'
MAIN_FILE = 'streamlit_app.py'
RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
COMPUTE_POOL = streamlit_compute_pool
QUERY_WAREHOUSE = my_large_warehouse
;
```

**Example: Warehouse runtime**

When you use a warehouse runtime, set a small, dedicated code warehouse for running Streamlit apps:

Copy code

```
CREATE STREAMLIT my_app
FROM '@my_stage/app_folder'
MAIN_FILE = 'streamlit_app.py'
QUERY_WAREHOUSE = my_small_warehouse;
```

Within your app code, switch to a different warehouse for queries:

Copy code

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()
session.use_warehouse("my_large_warehouse")
```

#### Best practices for code warehouses

When use a warehouse runtime in Streamlit in Snowflake, select the smallest warehouse possible to run your app code.

Warehouses cache Python packages used by Streamlit apps, improving performance for subsequent app loads.
The cache is removed when the warehouse suspends, which may slow initial app loading after the warehouse resumes.
If the resumed warehouse runs more apps, the package cache rebuilds and improves loading performance.

Per-second billing and auto-suspend provide flexibility to start with smaller warehouses and adjust sizes
as needed. You can increase warehouse size at any time. For more information, see [Change the query warehouse](/developer-guide/streamlit/app-development/managing-your-app#label-streamlit-change-warehouse).

Snowflake recommends using a dedicated warehouse for Streamlit apps to isolate costs and potentially
improve load times by avoiding other workloads. Within your app code, activate a different warehouse for
queries as needed.

For more information, see [Warehouse considerations](/user-guide/warehouses-considerations).

Tip

- Set auto-suspend to at least 30 seconds to avoid warehouse suspension during initialization.
- Configure sleep times and WebSocket timeouts for your Streamlit apps to reduce costs. For more information, see [Custom sleep timer for a Streamlit app](/developer-guide/streamlit/features/sleep-timer).
