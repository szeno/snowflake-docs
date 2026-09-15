# About Declarative Sharing in the Native Application Framework

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

## About Declarative Sharing

Declarative Sharing in the Snowflake Native App Framework enables providers to share not just data,
but code objects ([workspaces](/developer-guide/declarative-sharing/workspaces) containing
[notebooks](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
[stored procedures](/developer-guide/stored-procedure/stored-procedures-overview),
and [user-defined functions](/developer-guide/udf/udf-overview)) alongside
tables and views as a single data product. Providers define all shared objects in a YAML
manifest file, and the framework handles privilege management, object resolution, and
versioning automatically, with no setup script required.

The Declarative Native Apps development experience provides the following features:

- **A declarative sharing model** that allows you to define shared objects using a simple text-based YAML file.
- **Streamlined testing**, so developers can work directly with the content in a live environment.
- **Automatic versioning and updates** of the app.
- **Capabilities to prepare multiple views of data**, including filtered data views, that are optimized for different consumer types.
- **Capabilities to protect sensitive data** by categorizing data into application roles. Consumers can delegate these app roles to teams, so that team members only see data that’s relevant to their work.
- **Runs in the consumer account**, allowing the customer to manage their resource usage and costs.

## What is a Declarative Sharing app?

A Declarative Native App is a data product that uses the declarative sharing model to share data and logic with Snowflake consumers.

Declarative Native Apps are built using a combination of Snowflake objects, including the following:

[Databases](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-databases)
:   Databases that the provider shares with consumers.

[Schemas](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-schemas)
:   Schemas in the shared databases.

[Tables](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-tables)
:   Database tables in the shared schemas.

[Views](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-views)
:   Shared views in the shared databases. Views can reference other databases that are not shared, if the dependent databases are included in the manifest file.

[Required databases](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-required-databases)
:   Databases that are not shared, but are referenced by views in the shared databases. These databases must be included in the manifest file. Consumers can only access data in these databases using the views shared in the app.

[Workspaces](/developer-guide/declarative-sharing/workspaces)
:   A directory of files and folders that consumers get as a read-only workspace. Use a workspace to
    share [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
    documentation, images, and sample data files together.

[Notebooks](/user-guide/ui-snowsight/notebooks), [stored procedures](/developer-guide/stored-procedure/stored-procedures-overview), and [user-defined functions](/developer-guide/udf/udf-overview)
:   Code objects that help consumers visualize and explore the data. Sharing notebooks directly is
    deprecated. Share notebooks in a workspace instead.

[Manifest file](/developer-guide/declarative-sharing/manifest-reference)
:   A manifest file defines the app structure and shared objects.

[App roles](/developer-guide/declarative-sharing/app-roles)
:   App roles categorize data and control access to shared objects.

For information about how to declare these objects in the manifest file, see [Declarative Native App manifest reference](/developer-guide/declarative-sharing/manifest-reference).

# Security

Declarative Native Apps have a similar security model to secure data sharing:

- Apps only have access to the data included in the app.
- Apps can’t access the consumer’s private data.
- Apps aren’t allowed to make external calls or to access data outside of the Snowflake account.

## Data product types

Choosing the right data product for your organization is determined by your business needs.
Do you want to get started quickly? Do you need an app with advanced features?
The following table lists the available Snowflake data products and provides their typical use cases.
An overview of Snowflake data products.

**Data product best uses**

| Data product | Description | Best for |
| --- | --- | --- |
| Secure Data Sharing | Traditional read-only sharing of tables and views. | Organizations beginning data monetization or with simple sharing needs. |
| Declarative Native Apps | Enhanced sharing with workspaces and other logic, role-based access control (RBAC), and declarative configuration. | Data providers ready to add value through guided experiences and documentation. |
| Full Native Apps | Apps running fully inside of a consumer account with complex business logic and interfaces. | Organizations building complex data products with advanced capabilities. |

Expand

Show lessSee more

## Choosing a data product

Before choosing a data product, consider the following:

**Data product types**

| Data product | Description | Provider builds | Security and functionality balance | Best provider use cases |
| --- | --- | --- | --- | --- |
| Secure Data Sharing | Traditional read-only sharing of tables and views   - **Technical Expertise**: Basic Snowflake - **Development Skills**: SQL knowledge - **Maintenance Effort**: Low: SQL updates only | SQL grants for tables, views | - Data stays within Snowflake | - Providers focusing on datasets only - Initial marketplace entry |
| Declarative Native App | Enhanced sharing   - **Technical Expertise**: Intermediate Snowflake - **Development Skills**: SQL, YAML, notebooks - **Maintenance Effort**: Low: declarative updates, workspace/SQL changes | Application package | - Data stays within Snowflake - Limited functionality, that is, workspaces, notebooks, Streamlit, stored procedures, and user-defined functions | - Complex data requiring explanation - Demonstrating data value through examples - Reducing support burden through better documentation |
| Full Native Apps | Apps running fully inside the Snowflake customer’s account with complex business logic and interfaces   - **Technical Expertise**: Advanced Snowflake - **Development Skills**: SQL, containers, programming languages - **Maintenance Effort**: High: containers, security reviews | Application package, services (in Containers) | - Data by default within Snowflake, can leave Snowflake with consumer consent - Snowflake primitives and container runtime | - Data requiring complex logic and workflows - Complex visualization needs - Re-use of SaaS application components |

Expand

Show lessSee more

## Declarative Native Apps resources

In the following topics, you’ll find information you need to get started with Declarative Native Apps.

- [Introduction to Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/introduction)
- [Application Packages in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/package)
- [Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces)
- [Editing notebooks in a Declarative Native App](/developer-guide/declarative-sharing/live-editing)
- [User-Defined Functions and Stored Procedures in Declarative Shared Native Applications](/developer-guide/declarative-sharing/udfs-sprocs)
- [Creating a Listing using Declarative Sharing](/developer-guide/declarative-sharing/listing)
- [Monitoring Usage with Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/monitoring)
- [Package Versions in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/versioning)
- [Tutorial: Getting started with Declarative Native Apps](/developer-guide/declarative-sharing/tutorials/getting-started)
- [Tutorial: Create a Declarative Share with Cortex Code](/developer-guide/declarative-sharing/tutorials/create-share-coco)
- [Declarative Native App command reference](/developer-guide/declarative-sharing/command-reference)
- [Application roles: Allow consumers to share different views of the same data](/developer-guide/declarative-sharing/app-roles)
- [Declarative Native App manifest reference](/developer-guide/declarative-sharing/manifest-reference)
- [Install a Declarative Native App](/developer-guide/declarative-sharing/consumer/install)
- [Access content in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-app-content)
- [Access a shared workspace in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-shared-workspace)
- [Declarative App Consumer-Side Execution Model](/developer-guide/declarative-sharing/consumer/consumer-execution)
- [Declarative Sharing in Native Apps: Limitations](/developer-guide/declarative-sharing/limitations)
