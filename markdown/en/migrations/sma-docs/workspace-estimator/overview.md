description:
:   Overview of the Workspace Estimator for the Snowpark Migration Accelerator

# Workspace Estimator

The Workspace Estimator connects to your Databricks workspace, collects usage data, and generates a cost comparison for running the same workloads on Snowflake. It analyzes the following areas:

1. **Infrastructure inventory** — node types, cluster configurations
2. **Usage patterns** — cluster events, lifecycle data
3. **Workload analysis** — job definitions, execution history
4. **Performance metrics** — run statistics, resource consumption
5. **SQL analytics** — warehouse configurations, query history
6. **Data pipelines** — DLT pipeline configurations and performance

You can run the Workspace Estimator in two ways:

## SMA CLI

The SMA CLI includes the Workspace Estimator as a built-in command. This is the recommended way to run it. Use the `sma we dbx run` command to connect to your Databricks workspace, extract metadata, and upload the results to Snowflake in a single step.

For full usage instructions, command options, and examples, see [the SMA CLI walkthrough](/migrations/sma-docs/use-cases/sma-cli-walkthrough).

## Jupyter notebook

The Workspace Estimator is also available as a Jupyter notebook hosted on the [Snowflake Labs GitHub repository](https://github.com/Snowflake-Labs/Workspace-Estimator). This version is in maintenance mode and receives bug fixes only. The SMA CLI is the recommended path for new users.
