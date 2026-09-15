# Orchestrating Snowpark Connect for Spark workloads

You can run Snowpark Connect for Spark workloads in a non-interactive, asynchronous way directly on Snowflake’s infrastructure. With Snowpark Submit, you
can submit production-ready Spark applications, such as ETL pipelines and scheduled data transformations, by using a simple CLI
interface. This lets you maintain your existing Spark development workflows without a dedicated Spark cluster.

For example, you can package your PySpark ETL script, then use the Snowpark Submit CLI to run the script as a batch job on a Snowpark Container Services
container. This lets you automate nightly data pipelines with Apache Airflow or CI/CD tools. Your Spark code runs in cluster mode
on Snowpark Container Services, scaling seamlessly with built-in dependency and resource management.

Snowpark Submit offers the following benefits:

- Ability to run in cluster mode on Snowflake-managed infrastructure with no external Spark setup.
- Workflow integration, supporting automation through CI/CD pipelines, Apache Airflow, or cron-based scheduling.
- Support for Python, enabling reuse of existing Spark applications across languages.
- Dependency management, with support for packaging external Python modules or JARs.

Note

`snowpark-submit` supports much of the same functionality as `spark-submit`. However, some functionality has been
omitted because it is not needed when running Spark workloads on Snowflake.

## Get started with Snowpark Submit

To get started using Snowpark Submit, follow these steps:

1. Install Snowpark Submit by following the steps in [Using Snowpark Submit](/developer-guide/snowpark-connect/snowpark-connect-using-submit).
2. Study the [Snowpark Submit examples](/developer-guide/snowpark-connect/snowpark-connect-submit-cookbook).
3. Get to know how to use Snowpark Submit with [Snowpark Submit reference](/developer-guide/snowpark-connect/snowpark-connect-submit-reference).

## Programmatic access with the Python API

Instead of the CLI, you can submit and manage Spark workloads from Python scripts using the
[Snowpark Submit Python API](/developer-guide/snowpark-connect/snowpark-connect-submit-python-api). The API uses your
existing Snowpark session and supports the full job lifecycle: submission, status polling, log retrieval, and
cancellation. It also supports Python, Java, and Scala workloads.
