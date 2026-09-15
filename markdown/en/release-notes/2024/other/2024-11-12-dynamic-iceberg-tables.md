# November 12, 2024 — Dynamic tables: Support for reading from Snowflake-managed Iceberg tables and creating dynamic Apache Iceberg™ tables –— *General Availability*

We are pleased to announce the general availability of the following new capabilities related to dynamic tables and Snowflake-managed Apache Iceberg™ tables:

- Creating a dynamic table that reads from a Snowflake-managed Iceberg table as the source, just like regular tables.
- Creating a dynamic Iceberg table, a new dynamic table type that stores query results in the Iceberg table format.

You can use dynamic Iceberg tables for the following scenarios:

- **Data lake integration:** You can store large datasets cost-effectively while performing transformations and analytics within
  Snowflake, leveraging the Iceberg format for efficient querying and management.
- **Defining continuous data transformation pipelines:** By using dynamic tables, you can ensure data is always up to date without
  manual intervention and handle high-velocity data streams efficiently with incremental processing.

For more information, see [Create a dynamic Apache Iceberg™ table](/user-guide/dynamic-tables/create-iceberg) and [Introduction to streams](/user-guide/streams-intro).
