# May 19, 2025: Snowflake ML Data Connector release notes

## Snowflake ML Data Connector for Container Runtime (*General availability*)

The Snowflake ML Data Connector is now generally available for use with container runtime instances, such as notebook sessions and ML jobs. This connector enables you to efficiently ingest data from Snowflake data sources
into your containerized Python environments. It leverages distributed processing to accelerate data loading.

Key capabilities include:

- Data loading from any Snowflake data source (tables or stages) directly into a pandas dataframe for use in open source ML workflows.
- Create PyTorch and TensorFlow datasets from Snowflake data for seamless integration with popular ML frameworks.
- Use the same code both inside and outside of Snowflake’s container runtime.
- Support for both Snowpark DataFrames (ideal for development) and Snowflake Datasets (versioned, schema-level objects for production).
- Integration with Snowflake’s distributed APIs for large-scale model training and tuning.
