# Snowflake Python APIs: Managing Snowflake objects with Python

Feature — Generally Available

The Snowflake Python APIs library is supported in government regions, but some resource types are currently not available in government regions.

The Snowflake Python APIs package is a unified library that seamlessly connects Python with Snowflake workloads. It is intended to provide
comprehensive APIs for interacting with Snowflake resources across data engineering, Snowpark, Snowpark ML, and application workloads using
a first-class Python API.

You can use the Snowflake Python APIs to manage Snowflake resources by creating, dropping, or altering them, and more. You can use
Python to perform tasks you might otherwise perform with Snowflake [SQL commands](/sql-reference-commands).

To learn more about the API, including its general concepts and design patterns, see [Snowflake Python APIs: General concepts](/developer-guide/snowflake-python-api/snowflake-python-general-concepts).

## Supported Snowflake resource objects

Note

The [API reference documentation](https://docs.snowflake.com/developer-guide/snowflake-python-api/reference/latest/index) reflects the
latest version of the Snowflake Python APIs. Note that not all resources in the API currently provide 100% coverage of their
equivalent [SQL commands](/sql-reference-commands), but the Python APIs are under active development and are continuously expanding.

With the Snowflake Python APIs, you can currently manage the following Snowflake resource objects:

- [Accounts](/developer-guide/snowflake-python-api/snowflake-python-managing-accounts)

  - [Account](/developer-guide/snowflake-python-api/snowflake-python-managing-accounts#label-snowflake-python-accounts)
  - [Managed account](/developer-guide/snowflake-python-api/snowflake-python-managing-accounts#label-snowflake-python-managed-accounts)
- [Users, roles, and privileges](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles)

  - [User](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles#label-snowflake-python-users)
  - [Role](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles#label-snowflake-python-roles)
  - [Database role](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles#label-snowflake-python-db-roles)
  - [Access privileges](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles#label-snowflake-python-privileges)
- [Integrations](/developer-guide/snowflake-python-api/snowflake-python-managing-integrations)

  - [API integration](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.api_integration)
  - [Catalog integration](/developer-guide/snowflake-python-api/snowflake-python-managing-integrations#label-snowflake-python-catalog-integrations)
  - [Notification integration](/developer-guide/snowflake-python-api/snowflake-python-managing-integrations#label-snowflake-python-notification-integrations)
- [Virtual warehouse](/developer-guide/snowflake-python-api/snowflake-python-managing-warehouses)
- [Databases, schemas, tables, and views](/developer-guide/snowflake-python-api/snowflake-python-managing-databases)

  - [Database](/developer-guide/snowflake-python-api/snowflake-python-managing-databases#label-snowflake-python-databases)
  - [Schema](/developer-guide/snowflake-python-api/snowflake-python-managing-databases#label-snowflake-python-schemas)
  - [Standard table](/developer-guide/snowflake-python-api/snowflake-python-managing-databases#label-snowflake-python-tables)
  - [Dynamic table](/developer-guide/snowflake-python-api/snowflake-python-managing-dynamic-tables)
  - [Event table](/developer-guide/snowflake-python-api/snowflake-python-managing-databases#label-snowflake-python-event-tables)
  - [Iceberg table](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.iceberg_table)
  - [View](/developer-guide/snowflake-python-api/snowflake-python-managing-databases#label-snowflake-python-views)
  - [Sequence](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.sequence)
- [Functions and procedures](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures)

  - [Stored procedure](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-procedures)
  - [User-defined function (UDF)](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures#label-snowflake-python-udfs)
  - [Artifact repository](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.artifact_repository)
- Data pipeline

  - [Stream](/developer-guide/snowflake-python-api/snowflake-python-managing-streams)
  - [Task](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks)
- AI and ML (not available in government regions)

  - [Cortex Chat service](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.cortex.chat_service)
  - [Cortex Embed service](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.cortex.embed_service)
  - [Cortex Inference service](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.cortex.inference_service)
  - [Cortex Lite Agent service](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.cortex.lite_agent_service)
  - [Cortex Search service](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.cortex.search_service)
- Security

  - [Network policy](/developer-guide/snowflake-python-api/snowflake-python-managing-network-policies)
  - [Network rule](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.network_rule)
  - [Password policy](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.password_policy)
  - [Secret](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.secret)
- Data governance

  - [Tag](/developer-guide/snowflake-python-api/snowflake-python-managing-tags)
- [Data loading and unloading](/developer-guide/snowflake-python-api/snowflake-python-managing-data-loading)

  - [External volume](/developer-guide/snowflake-python-api/snowflake-python-managing-data-loading#label-snowflake-python-external-volumes)
  - [Pipe](/developer-guide/snowflake-python-api/snowflake-python-managing-data-loading#label-snowflake-python-pipes)
  - [Stage](/developer-guide/snowflake-python-api/snowflake-python-managing-data-loading#label-snowflake-python-stages)
- [Alert](/developer-guide/snowflake-python-api/snowflake-python-managing-alerts)
- [Notebook](/developer-guide/snowflake-python-api/snowflake-python-managing-notebooks)
- [Snowpark Container Services components](/developer-guide/snowflake-python-api/snowflake-python-managing-containers)
  (not available in government regions)

  - [Compute pool](/developer-guide/snowflake-python-api/snowflake-python-managing-containers#label-snowflake-python-compute-pools)
  - [Image repository](/developer-guide/snowflake-python-api/snowflake-python-managing-containers#label-snowflake-python-image-repositories)
  - [Service and service function](/developer-guide/snowflake-python-api/snowflake-python-managing-containers#label-snowflake-python-services)
- Streamlit

  - [Streamlit object](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.streamlit)

## Python ecosystem in Snowflake

The Snowflake Python APIs, the [Snowpark API for Python](/developer-guide/snowpark/python/index), and the
[Snowflake Connector for Python](/developer-guide/python-connector/python-connector) are interfaces that each have distinct purposes
in Snowflake. This section explains their differences and describes the typical use cases for each.

Snowflake Python APIs
:   You can use this set of first-class Python APIs to define and manage core resources (such as tables, warehouses, and tasks) across
    Snowflake workloads. Unlike the Python Connector, these APIs interact with Snowflake using native Python without the need to use SQL.

    The Snowflake Python APIs package unifies all Snowflake Python libraries (including `connector`, `core`, `snowpark`, and
    `ml`) so that you can simply start with the command `pip install snowflake`.

    Following the declarative programming approach, this API can be used as a DevOps tool to manage changes to your resources and automate
    code and infrastructure deployment in Snowflake.

Snowpark
:   This set of libraries and code execution environments can run Python and other programming languages next to your data in Snowflake.

    - Libraries: With the [Snowpark API](/developer-guide/snowpark/index), you can use Snowpark DataFrames in your code to query and transform data
      entirely within Snowflake. Snowpark applications process your data at scale directly on the Snowflake engine without moving the data to
      the system where your application code runs.

      The Snowpark API is available in Python, Java, and Scala.
    - Code execution environments: Snowpark runtime environments support container images and Python, Java, and Scala code.

      - You can execute custom Python code through Python user-defined functions (UDFs) or stored procedures for building data pipelines,
        apps, and more. Python runtime environments have access to a package repository and package manager from Anaconda.

        Runtime environments are also available in Scala and Java.
      - You can run containerized applications directly within Snowflake using
        [Snowpark Container Services](/developer-guide/snowpark-container-services/overview).

Snowflake Connector for Python
:   Use this SQL driver to connect to Snowflake, execute SQL statements, and then get the results using a Python client.

    With the Python Connector, you write all of your interactions with Snowflake using SQL statement strings.

## Get started with the Snowflake Python APIs

To get started with the Snowflake Python APIs, see the instructions in the following topics:

1. [Install the library](/developer-guide/snowflake-python-api/snowflake-python-installing).
2. [Connect to Snowflake](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

For tutorials on getting started with the Snowflake Python APIs, see [Tutorials: Getting started with the Snowflake Python APIs](/developer-guide/snowflake-python-api/overview-tutorials).

## Supported Python versions

The supported versions of Python are:

Generally available versions:

- 3.9 (deprecated)
- 3.10
- 3.11
- 3.12
- 3.13
- 3.14

## Developer guides

| Guide | Description |
| --- | --- |
| [Install the Snowflake Python APIs library](/developer-guide/snowflake-python-api/snowflake-python-installing) | Install the Snowflake Python APIs package. |
| [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake) | Connect to Snowflake from Python code. |
| [Managing Snowflake accounts and managed accounts with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-accounts) | Use the API to create and manage accounts and managed accounts. |
| [Managing Snowflake alerts with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-alerts) | Use the API to create and manage alerts. |
| [Managing data loading and unloading resources with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-data-loading) | Use the API to create and manage data loading and unloading resources, including external volumes, pipes, and stages. |
| [Managing Snowflake databases, schemas, tables, and views with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-databases) | Use the API to create and manage databases, schemas, and tables. |
| [Managing Snowflake dynamic tables with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-dynamic-tables) | Use the API to create and manage dynamic tables. |
| [Managing Snowflake functions and stored procedures with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-functions-procedures) | Use the API to create and manage user-defined functions (UDFs) and stored procedures. |
| [Managing Snowflake integrations with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-integrations) | Use the API to create and manage catalog integrations and notification integrations. |
| [Managing Snowflake network policies with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-network-policies) | Use the API to create and manage network policies. |
| [Managing Snowflake Notebooks with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-notebooks) | Use the API to create and manage Snowflake Notebooks. |
| [Managing Snowpark Container Services (including service functions) with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-containers) | Use the API to manage components of Snowpark Container Services, including compute pools, image repositories, services, and service functions. |
| [Managing Snowflake streams with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-streams) | Use the API to create and manage streams. |
| [Managing Snowflake tasks and task graphs with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-tasks) | Use the API to create, execute, and manage tasks and task graphs. |
| [Managing Snowflake users, roles, and grants with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-user-roles) | Use the API to create and manage users, roles, and grants. |
| [Managing Snowflake virtual warehouses with Python](/developer-guide/snowflake-python-api/snowflake-python-managing-warehouses) | Use the API to create and manage virtual warehouses. |

Expand

Show lessSee more

## References

[Snowflake Python APIs Reference](https://docs.snowflake.com/developer-guide/snowflake-python-api/reference/latest/index)

## Costs of Snowflake access

To reduce costs—–for both usage credit and network activity—–the Snowflake Python APIs are designed to communicate with Snowflake
only when you call methods designed to synchronize with Snowflake.

Objects in the API are either local references (or *handles*) or snapshots of state stored on Snowflake. In general, when you process
information that was retrieved from Snowflake, you do so through a local, in-memory reference object.

These references do not synchronize with Snowflake until you call a method. When you call a method, you are usually incurring costs in
both usage credit and network activity. In contrast, when you work with in-memory references, such as when accessing attributes, your work
is performed locally and incurs no such costs.
