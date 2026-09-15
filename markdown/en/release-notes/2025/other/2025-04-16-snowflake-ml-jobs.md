# Apr 16, 2025: Snowflake ML Jobs (*Preview*)

Snowflake announces the preview of Snowflake ML Jobs, a new capability that allows you to run machine learning (ML) workflows from your local environment.

Snowflake ML Jobs enable you to:

- Run ML workloads on Snowflake Compute Pools, leveraging GPU and high-memory CPU instances.
- Use your preferred development environment, such as VS Code or Jupyter notebooks, without requiring Snowflake worksheets or notebooks.
- Install and use custom Python packages within your runtime environment.
- Optimize data loading, training, and hyperparameter tuning with Snowflake’s distributed APIs.
- Integrate with orchestration tools, such as Apache Airflow.
- Monitor and manage jobs programmatically using Snowflake’s APIs.

Key benefits of Snowflake ML Jobs include:

- **Scalability**: Execute large-scale ML training on datasets requiring significant compute resources or GPU acceleration.
- **Flexibility**: Retain your existing development environment while leveraging Snowflake’s compute resources.
- **Efficiency**: Work directly with large Snowflake datasets to reduce data movement and avoid expensive data transfers.
- **Productionization**: Move ML code from development to production with minimal changes, enabling programmatic execution through pipelines.
- **Compatibility**: Lift and shift open-source ML workflows with minimal code modifications.

To get started with Snowflake ML Jobs, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

Important

Snowflake ML Jobs are available in Snowpark ML Python package (`snowflake-ml-python`) version 1.8.2 and later.
