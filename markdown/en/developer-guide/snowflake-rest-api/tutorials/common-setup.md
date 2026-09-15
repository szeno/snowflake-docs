# Common setup for Snowflake REST APIs tutorials

## Introduction

This topic provides instructions for the common setup required for all Snowflake REST APIs tutorials available in this documentation.

Feature — Generally Available

The Snowflake REST APIs are supported in government regions, but some resources are currently not available in government regions.

### Overview of the Snowflake REST APIs

Before starting your setup, take a look at the Snowflake REST APIs.

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
  - [Views](/developer-guide/snowflake-rest-api/view/view-introduction)
- Loading and unloading data

  - [Stages](/developer-guide/snowflake-rest-api/stages/stages-introduction)
  - [External volumes](/developer-guide/snowflake-rest-api/external-volume/external-volume-introduction)
  - [Pipes](/developer-guide/snowflake-rest-api/pipe/pipe-introduction)
- Managing notebooks

  - [Notebooks](/developer-guide/snowflake-rest-api/notebook/notebook-introduction)
- Working with Snowpark Container Services

  - [Compute Pools](/developer-guide/snowflake-rest-api/compute-pools/cp-introduction)
  - [Image Repositories](/developer-guide/snowflake-rest-api/image-repositories/images-introduction)
  - [Services](/developer-guide/snowflake-rest-api/services/services-introduction)
- Using functions and procedures

  - [Functions](/developer-guide/snowflake-rest-api/functions/functions-introduction)
  - [User-defined functions](/developer-guide/snowflake-rest-api/user-defined-function/user-defined-function-introduction)
  - [Procedures](/developer-guide/snowflake-rest-api/procedure/procedure-introduction)
- Managing security

  - [Network policies](/developer-guide/snowflake-rest-api/network-policy/network-policy-introduction)
- Managing alerts

  - [Alerts](/developer-guide/snowflake-rest-api/alert/alert-introduction)
- Leveraging AI/ML

  - [Cortex Inference](/developer-guide/snowflake-rest-api/cortex-inference/cortex-inference-introduction)
  - [Cortex Search Service](/developer-guide/snowflake-rest-api/cortex-search/cortex-search-introduction)
- Managing streams and tasks

  - [Streams](/developer-guide/snowflake-rest-api/stream/stream-introduction)
  - [Tasks](/developer-guide/snowflake-rest-api/tasks/tasks-introduction)
- Managing integrations

  - [Catalog Integration](/developer-guide/snowflake-rest-api/catalog-integration/catalog-integration-introduction)
  - [Notification](/developer-guide/snowflake-rest-api/notification-integration/notification-integration-introduction)

For reference information about the APIs and their endpoints, see [Snowflake REST APIs reference](/developer-guide/snowflake-rest-api/reference).

Tip

If you prefer writing Python applications, you can use the Snowflake Python APIs to manage Snowflake objects. For more information, see [Snowflake Python APIs: Managing Snowflake objects with Python](/developer-guide/snowflake-python-api/snowflake-python-overview).

## Import the Snowflake REST APIs collections

This tutorial walks you through the process of importing the Snowflake REST APIs collections from Postman.

1. Download the API collections from the [Git repository](https://github.com/snowflakedb/snowflake-rest-api-specs/tree/main/collections) into a folder.

   ![](/static/images/screens/rest-api/api-collections-git.png)
2. Open the Postman application, and create an account, if necessary.
3. In Postman, open the desired workspace.

   ![](/static/images/screens/rest-api/postman-workspace.png)
4. Select **Import**.

   ![](/static/images/screens/rest-api/postman-import-workspace.png)
5. Select **folders**.

   ![](/static/images/screens/rest-api/postman-download-collections.png)
6. In the dialog, select the folder where you extracted the collection, and select **Open**.

   ![](/static/images/screens/rest-api/postman-import-elements.png)
7. Verify that all of the items are selected, and select **Import**.

   You should see the collections listed in the left panel, as shown:

   ![](/static/images/screens/rest-api/postman-verify-import.png)

## Specify the bearer token in Postman

REST requests require a JWT token in the request header to authenticate the request. If you don’t have a JWT token, see [Generate a JWT token](/developer-guide/snowflake-rest-api/authentication#label-sfrest-api-jwt-token).

In Postman, you can copy the JWT token into the `bearerToken` header property, as shown.

![](/static/images/screens/rest-api/postman-bearer-token.png)

Note

As mentioned in the tutorial [prerequisites](/developer-guide/snowflake-rest-api/tutorials-overview), you must define an AUTHENTICATION POLICY. If you receive an error message similar to `{ "code": "390202", "message": "Authentication attempt rejected by the current authentication policy." }`, you can run the following SQL command to define a policy:

Copy code

```
SHOW AUTHENTICATION POLICIES; alter AUTHENTICATION POLICY <your authentication policy> set AUTHENTICATION_METHODS = ('KEYPAIR', 'PASSWORD', 'OAUTH');
```

## Set environment variables in the Postman environment

You can set environment variables in your Postman environment. You can then use these variables in Postman, in the form `{{variable_name}}`.

All endpoint URLs begin with a `baseURL`, which identifies your Snowflake account. The baseURL has the form: `<account_locator>.snowflakecomputing.com`, where `<account_locator>` is your Snowflake account name.

To set the `baseURL` variable, as well as any other variables, in Postman, enable each parameter and set its value, as shown:

![](/static/images/screens/rest-api/tutorials/postman-env-vars.png)

For each value you set, you must select **Save** to save the new value.

## What’s next?

Congratulations! In this tutorial, you learned the fundamentals for managing Snowflake database, schema, and table resources using the Snowflake REST APIs.

### Summary

Along the way, you completed the following steps:

- Import Snowflake REST APIs collections.
- Specify a bearer token in Postman.
- Set environment variables in the Postman environment.

### Next tutorial

You can now proceed to [Tutorial 1: Create and manage databases, schemas, and tables](/developer-guide/snowflake-rest-api/tutorials/tutorial-1), which shows you how to create and manage Snowflake databases, schemas, and tables.
