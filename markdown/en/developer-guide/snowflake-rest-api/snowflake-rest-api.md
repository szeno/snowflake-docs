# Snowflake REST APIs

Feature — Generally Available

The Snowflake REST APIs are supported in government regions, but some resources are currently not available in government regions.

Snowflake REST APIs for resource management provide a set of endpoints that lets users programmatically interact with and control various resources within the Snowflake Data Cloud.

The Snowflake REST APIs suite of APIs enables developers to build end-to-end automation and integration with Snowflake resources. These REST APIs are compliant with the [OpenAPI specification](https://spec.openapis.org/oas/v3.1.0). Snowflake REST APIs enable developers and partners to use the language of their choice to build integrations with Snowflake using the openAPI specifications.

The Snowflake REST APIs supports the following resources through the corresponding APIs. The APIs support CREATE OR ALTER operations for applicable resources.

- Working with accounts

  - [Accounts](/developer-guide/snowflake-rest-api/account/account-introduction)
  - [Managed accounts](/developer-guide/snowflake-rest-api/managed-account/managed-account-introduction)
- Working with users, roles, and privileges

  - [Users](/developer-guide/snowflake-rest-api/users/users-introduction)
  - [Roles](/developer-guide/snowflake-rest-api/roles/roles-introduction)
  - [Database roles](/developer-guide/snowflake-rest-api/database-role/database-role-introduction)
  - [Grants](/developer-guide/snowflake-rest-api/grants/grants-introduction)
- Managing virtual warehouses

  - [Warehouses](/developer-guide/snowflake-rest-api/warehouses/warehouses-introduction)
- Working with databases and schemas

  - [Databases](/developer-guide/snowflake-rest-api/databases/db-introduction)
  - [Schemas](/developer-guide/snowflake-rest-api/schemas/schemas-introduction)
- Managing tables and views

  - [Tables](/developer-guide/snowflake-rest-api/tables/tables-introduction)
  - [Dynamic tables](/developer-guide/snowflake-rest-api/dynamic-tables/dynamic-tables-introduction)
  - [Event tables](/developer-guide/snowflake-rest-api/event-table/event-table-introduction)
  - [Iceberg tables](/developer-guide/snowflake-rest-api/iceberg-table/iceberg-table-introduction)
  - [Sequences](/developer-guide/snowflake-rest-api/sequence/sequence-introduction)
  - [Views](/developer-guide/snowflake-rest-api/view/view-introduction)
- Loading and unloading data

  - [Stages](/developer-guide/snowflake-rest-api/stages/stages-introduction)
  - [External volumes](/developer-guide/snowflake-rest-api/external-volume/external-volume-introduction)
  - [Pipes](/developer-guide/snowflake-rest-api/pipe/pipe-introduction)
- Managing notebooks and Streamlit apps

  - [Notebooks](/developer-guide/snowflake-rest-api/notebook/notebook-introduction)
  - [Streamlit](/developer-guide/snowflake-rest-api/streamlit/streamlit-introduction)
- Working with Snowpark Container Services

  - [Compute Pools](/developer-guide/snowflake-rest-api/compute-pools/cp-introduction)
  - [Image Repositories](/developer-guide/snowflake-rest-api/image-repositories/images-introduction)
  - [Services](/developer-guide/snowflake-rest-api/services/services-introduction)
- Using functions and procedures

  - [Artifact repositories](/developer-guide/snowflake-rest-api/artifact-repository/artifact-repository-introduction)
  - [Functions](/developer-guide/snowflake-rest-api/functions/functions-introduction)
  - [User-defined functions](/developer-guide/snowflake-rest-api/user-defined-function/user-defined-function-introduction)
  - [Procedures](/developer-guide/snowflake-rest-api/procedure/procedure-introduction)
- Managing security

  - [Network policies](/developer-guide/snowflake-rest-api/network-policy/network-policy-introduction)
  - [Network rules](/developer-guide/snowflake-rest-api/network-rule/network-rule-introduction)
  - [Password policies](/developer-guide/snowflake-rest-api/password-policy/password-policy-introduction)
  - [Secrets](/developer-guide/snowflake-rest-api/secret/secret-introduction)
- Managing alerts

  - [Alerts](/developer-guide/snowflake-rest-api/alert/alert-introduction)
- Leveraging AI/ML

  - [Cortex Embed](/developer-guide/snowflake-rest-api/cortex-embed/cortex-embed-introduction)
  - [Cortex Inference](/developer-guide/snowflake-rest-api/cortex-inference/cortex-inference-introduction)
  - [Cortex Search Service](/developer-guide/snowflake-rest-api/cortex-search/cortex-search-introduction)
- Managing streams and tasks

  - [Streams](/developer-guide/snowflake-rest-api/stream/stream-introduction)
  - [Tasks](/developer-guide/snowflake-rest-api/tasks/tasks-introduction)
- Managing integrations

  - [API integration](/developer-guide/snowflake-rest-api/api-integration/api-integration-introduction)
  - [Use catalog integrations](/developer-guide/snowflake-rest-api/catalog-integration/catalog-integration-introduction)
  - [Use notification integrations](/developer-guide/snowflake-rest-api/notification-integration/notification-integration-introduction)
- Managing tags

  - [Tags](/developer-guide/snowflake-rest-api/tag/tag-introduction)

For reference information about the APIs and their endpoints, see [Snowflake REST APIs reference](/developer-guide/snowflake-rest-api/reference).

You can access the Snowflake REST APIs OpenAPI specifications in the [snowflake-rest-api-specs](https://github.com/snowflakedb/snowflake-rest-api-specs) Git repository.

Note

The [Snowflake REST APIs reference documentation](/developer-guide/snowflake-rest-api/snowflake-rest-api) reflects the
latest version of the Snowflake REST APIs. Note that not all resources in the API currently provide 100% coverage of their
equivalent [SQL commands](/sql-reference-commands), but the Snowflake REST APIs are under active development and are continuously expanding.

## Requirements

The Snowflake REST APIs has the following requirements:

- You must have a way to submit REST requests, such as the [Postman app](https://www.postman.com/downloads/), [curl](https://curl.se/), or an HTTP client in the programming language of your choice, installed on your machine.

## Suggested tools

- [Postman app](https://www.postman.com/downloads/)
- [curl](https://curl.se/)
- [Snowflake CLI](/developer-guide/snowflake-cli/index)
- [SnowSQL](/user-guide/snowsql)
