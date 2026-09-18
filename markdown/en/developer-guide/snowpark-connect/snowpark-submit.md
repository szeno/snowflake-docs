# Orchestrating Snowpark Connect for Spark workloads

You can run Snowpark Connect for Spark workloads in a non-interactive, asynchronous way directly on Snowflake’s infrastructure, without
maintaining a dedicated Spark cluster. This lets you run production-ready Spark applications, such as ETL pipelines and
scheduled data transformations, and orchestrate them with tools such as Apache Airflow or CI/CD systems.

## Submit Spark jobs as Code Bundles

Submit a packaged Spark application as a batch job that runs directly on warehouse compute; there’s no compute pool to
provision or manage. You submit a job in one of two ways:

- **SQL.** A synchronous `EXECUTE CODE BUNDLE` statement that submits the job and waits for it to finish. Because it’s
  SQL, it integrates natively with [Snowflake tasks](/developer-guide/code-bundles/code-bundles#scheduling-with-tasks),
  so you can build scheduled Spark pipelines on Snowflake.
- **REST API.** A call to the Code Bundle executions endpoint that external orchestrators such as Apache Airflow, CI/CD
  systems, and other control planes can use to submit jobs and poll for status.

For details on packaging your application, submitting it with SQL or the REST API, and monitoring runs, see
[Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle).
