# Snowsight templates

## Overview

[Snowsight templates](http://app.snowflake.com/templates) provide users with interactive walkthroughs for exploring Snowflake features and use cases. Templates are available
as executable worksheets, notebooks, or Streamlit apps, and come pre-configured with sample data and the required permissions.

Templates run in a dedicated `SNOWFLAKE_LEARNING` environment, which includes a pre-provisioned role (`SNOWFLAKE_LEARNING_ROLE`), an X-Small
compute warehouse (`SNOWFLAKE_LEARNING_WH`), and a database (`SNOWFLAKE_LEARNING_DB`). Costs associated with
the `SNOWFLAKE_LEARNING_WH` and `SNOWFLAKE_LEARNING_DB` are managed in the same way as any other object owned
by `ACCOUNTADMIN`. See [Monitor credit usage with budgets](/user-guide/budgets) for details on monitoring and optimizing warehouse compute costs.

Note

`SNOWFLAKE_LEARNING_WH` is owned by the `ACCOUNTADMIN` role. Standard usage costs apply.

Templates offer the following advantages:

- Safely try new features and use cases without impacting production data.
- Sample data is included to get up and running quickly.
- Concise, self-contained experiences that are typically completed in under five minutes.

Snowflake automatically provisions the `SNOWFLAKE_LEARNING` environment for both new and existing accounts as part of
[BCR-1992](/release-notes/bcr-bundles/un-bundled/bcr-1992). No action is required to enable it.

If your organization prefers **not** to include this environment, an `ACCOUNTADMIN` can opt out by running:

Copy code

```
SELECT SYSTEM$DISABLE_SNOWFLAKE_LEARNING_ENVIRONMENT();
```

If [BCR-1992](/release-notes/bcr-bundles/un-bundled/bcr-1992) is not enabled for your account, you can provision the
`SNOWFLAKE_LEARNING` environment manually using the following SQL:

Copy code

```
CREATE DATABASE SNOWFLAKE_LEARNING_DB;
CREATE ROLE SNOWFLAKE_LEARNING_ROLE;
GRANT ROLE SNOWFLAKE_LEARNING_ROLE TO ROLE PUBLIC;
CREATE WAREHOUSE SNOWFLAKE_LEARNING_WH
  COMMENT = 'Warehouse used for executing template and demo content'
  WAREHOUSE_SIZE = 'X-Small'
  AUTO_RESUME = true
  AUTO_SUSPEND = 300;
GRANT USAGE, MONITOR, OPERATE ON WAREHOUSE SNOWFLAKE_LEARNING_WH TO ROLE SNOWFLAKE_LEARNING_ROLE;
GRANT USAGE ON DATABASE SNOWFLAKE_LEARNING_DB TO ROLE SNOWFLAKE_LEARNING_ROLE;
GRANT CREATE SCHEMA ON DATABASE SNOWFLAKE_LEARNING_DB TO ROLE SNOWFLAKE_LEARNING_ROLE;
```

If the `SNOWFLAKE_LEARNING` environment has already been provisioned in your account, but you want to disable it and drop the objects,
a user with the `ACCOUNTADMIN` role can run the following script to disable and drop the learning environment:

Copy code

```
USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$DISABLE_SNOWFLAKE_LEARNING_ENVIRONMENT();

-- DATABASE
SHOW DATABASES LIKE 'SNOWFLAKE_LEARNING_DB';
DROP DATABASE SNOWFLAKE_LEARNING_DB;

-- WAREHOUSE
SHOW WAREHOUSES LIKE 'SNOWFLAKE_LEARNING_WH';
DROP WAREHOUSE SNOWFLAKE_LEARNING_WH;

-- ROLE
SHOW ROLES LIKE 'SNOWFLAKE_LEARNING_ROLE';
DROP ROLE SNOWFLAKE_LEARNING_ROLE;
```

Get started with templates at <http://app.snowflake.com/templates>.
