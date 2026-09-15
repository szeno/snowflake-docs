# Environment setup for Snowpark Connect for Spark

Before you can develop Spark workloads with Snowpark Connect for Spark, you need to set up your development environment and
configure a connection to Snowflake.

You can develop Snowpark Connect for Spark workloads in the following environments:

- **Local IDE**: Use your preferred local tools such as VS Code, Jupyter Notebooks, IntelliJ, or a terminal. The
  `snowpark-connect` Python package is required for all languages. For Java and Scala projects, also add the
  `snowpark-connect-java-client` Maven dependency. These handle server lifecycle and session management automatically.
- **Snowflake Workspaces**: Use Snowflake Notebooks running on warehouses or in workspaces. The `snowpark-connect`
  package is available as a notebook dependency.

For setup instructions, see the following topics:

- [Install Snowpark Connect using the Snowpark package](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-local-ide-install)
- [Run Java or Scala workloads](/developer-guide/snowpark-connect/snowpark-connect-local-ide#label-snowpark-connect-execute-jar-cli)
- [Develop in Snowflake Workspaces](/developer-guide/snowpark-connect/snowpark-connect-snowflake-workspaces)
