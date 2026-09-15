# Managing Snowpark Container Services in Snowflake CLI

Note

You can use Snowpark Container Services from Snowflake CLI only if you have the necessary permissions to use Snowpark Container Services.

Snowpark Container Services is a fully managed container offering that helps you easily deploy,
manage, and scale containerized applications without having to move data out of Snowflake.
As a fully managed service, it comes with Snowflake security, configuration, and operational best practices built in.

Snowpark Container Services is fully integrated with Snowflake. For example, your application can easily:

- Connect to Snowflake and run SQL in a Snowflake virtual warehouse.
- Access data files in a Snowflake stage.

Snowpark Container Services is also integrated with third-party tools. It allows you to use third-party clients
(such as Docker) to easily upload your application images to Snowflake. Seamless integration makes it easier for
teams to focus on building the data applications, not the environment.

This section describes the following topics:

- [Working with image registries and repositories](/developer-guide/snowflake-cli/services/manage-images)
- [Managing compute pools](/developer-guide/snowflake-cli/services/manage-compute-pools)
- [Managing services](/developer-guide/snowflake-cli/services/manage-services)
