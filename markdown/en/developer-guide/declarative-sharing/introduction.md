# Introduction to Declarative Sharing in the Native Application Framework

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Declarative Sharing in the Snowflake Native App Framework enables providers to share not just data,
but code objects: workspaces containing notebooks, stored procedures, and user-defined
functions, alongside
tables and views as a single data product. Providers define all shared objects in a YAML
manifest file, and the framework handles privilege management, object resolution, and
versioning automatically, with no setup script required. This topic provides a high-level
overview of the steps required to get started as a provider.

## Become a Snowflake listing provider

Becoming a provider allows you to create and manage listings to share your app with consumers.

For more information, see [Become a provider](https://other-docs.snowflake.com/collaboration/provider-becoming).

## Create your data content

Providers create data and objects to share with consumers. This can include the following:

> - [Tables](/user-guide/tables-micro-partitions), including:
>
>   - [Dynamic tables](/user-guide/dynamic-tables/overview)
>   - [Apache Iceberg tables](/user-guide/tables-iceberg)
> - [Views](/user-guide/views-introduction), including:
>
>   - [Semantic views](/user-guide/views-semantic/overview)
> - [Workspaces](/developer-guide/declarative-sharing/workspaces), which can include
>   [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
> - [Notebooks](/user-guide/ui-snowsight/notebooks-working) (deprecated)
> - [Stored procedures](/developer-guide/stored-procedure/stored-procedures-overview)
> - [User-defined functions](/developer-guide/udf/udf-overview)

### Access control requirements

The provider account should have the necessary privileges to create and manage Snowflake objects such as databases, schemas, tables, and virtual warehouses.

This includes:

- Databases and schemas: Requires USAGE privileges
- Tables and views: Requires SELECT privileges
