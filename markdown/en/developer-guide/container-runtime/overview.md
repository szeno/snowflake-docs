# Snowflake Container Runtime

The Snowflake Container Runtime is a preconfigured, versioned environment for analytics, data engineering, and machine
learning on Snowpark Container Services. It is the execution environment for Snowflake-native workloads, including interactive notebooks,
Python files, Code Bundles, and ML batch jobs.

Container Runtime includes Snowflake packages and popular open-source frameworks. Use it for exploration, scheduled
pipelines, distributed training, hyperparameter tuning, batch inference, and fine-tuning without assembling a separate
Python stack for each kind of work.

## First-party packages

Container Runtime includes the following Snowflake packages:

- **Snowpark** (`snowflake-snowpark-python`) for DataFrame pipelines and warehouse-pushdown compute.
- **Snowpark Connect** (`snowpark-connect`) for running Spark-style workloads against Snowflake without a
  lift-and-shift rewrite.
- **Snowflake ML** (`snowflake-ml-python`) for feature engineering, modeling, and the model registry, plus distributed
  data loading, training, and hyperparameter optimization across cores, GPUs, and multi-node compute pools.

## Use Container Runtime for machine learning

On Container Runtime, you can train and tune models next to your data instead of exporting it. Container Runtime
provides CPU or GPU compute pools on Snowpark Container Services, a versioned image with popular ML frameworks, and `pip` for installing
other packages. Snowflake ML APIs scale data loading, training, and hyperparameter search across cores and GPUs.

The `snowflake-ml-python` package includes:

- `DataConnector`, which loads Snowflake tables, DataFrames, and Datasets into pandas, PyTorch, or TensorFlow.
- Distributed XGBoost, LightGBM, and PyTorch APIs that follow the interfaces of the open-source libraries.

For more information, see [Snowflake Container Runtime for machine learning](/developer-guide/snowflake-ml/container-runtime-ml).

## Use Container Runtime for data engineering with Snowpark

For data engineering on Snowflake, both Snowpark Python and Snowpark Connect are included in Container Runtime. For
more information about Snowpark, see the [Snowpark API](/developer-guide/snowpark).

Snowpark Python (`snowflake-snowpark-python`) is the native DataFrame API. You write Python transformations that push
down to a warehouse, so pipelines stay next to the data and under Snowflake governance without a separate Spark
cluster.

Snowpark Connect (`snowpark-connect`) is intended for existing Spark workloads. PySpark DataFrame and Spark SQL code
runs on the Snowflake engine instead of a Spark cluster, with operations compiled to SQL and executed on a warehouse.

Use Snowpark when you build Snowflake-native pipelines. Use Snowpark Connect when you want Spark-style jobs to run on
Snowflake without a lift-and-shift rewrite.

## Supported instance families

Starting with Container Runtime 2.10, both x86 and ARM instance families are supported. To learn more about compute
pool instance families, see
[Snowpark Container Services: Understanding instance families](/developer-guide/snowpark-container-services/instance-families).

## Container Runtime lifecycle

Container Runtime versions follow a four-phase lifecycle: Latest, Stable, End of Support, and End of Life. You choose
a version when you create a notebook, Python file, Code Bundle, or ML Job. For changes in a specific version, see
[Snowflake Container Runtime release notes](/developer-guide/container-runtime/release-notes).

A major version starts as Latest. When the next major version is released, the last minor release of the previous
major version becomes Stable and is supported for one year. After that year, the version moves to End of Support and
then End of Life.

| Phase | Description | Updates |
| --- | --- | --- |
| Latest | The most recent release and the default in the Notebooks UI. You stay on the newest minor release in that major version. When the next major version is released, you remain on the last minor release of the previous major version, which becomes Stable. | New features, package upgrades, and major stability and security improvements. |
| Stable | A version that can be pinned (no automatic upgrades). Each Stable version is supported and patched for one year. | Major stability and security improvements. |
| End of Support | Still runnable on existing services, but no longer selectable for new services. | None. |
| End of Life | Removed. Existing services that use the runtime don’t start. | None. |

Expand

Show lessSee more

For example, while Container Runtime 3.x major is Latest, a notebook service automatically uses new minor releases in
the 3.x major version. When 4.0 is released, the last 3.x minor release becomes Stable for one year, and
4.0 becomes Latest. One year after 3.x becomes Stable, it moves to End of Support and then End of Life.

To learn about vulnerability detection and management, Snowflake response protocols, and shared security
responsibilities, see the
[Snowflake Security Addendum](https://www.snowflake.com/legal/security-addendum/2024-08-08/).

## Next steps

Learn how to select a runtime in the interactive Notebooks UI, in SQL for Code Bundles, and in APIs for ML Jobs. See
[Using a runtime](/developer-guide/container-runtime/using-runtime).
