# Mar 02, 2026: Support for new dbt Core versions for dbt Projects on Snowflake

Snowflake now supports explicit version pinning for dbt projects with the new DBT\_VERSION parameter. You can pin a
dbt Core version when creating, altering, or executing a dbt project object. You can also query supported versions and engine types
using the [SYSTEM$SUPPORTED\_DBT\_VERSIONS](/sql-reference/functions/system_supported_dbt_versions) system function to plan
upgrades and maintain environment stability.

The following example creates a dbt project pinned to a specific dbt Core version:

Copy code

```
CREATE DBT PROJECT my_dbt_project
  FROM '@my_stage/dbt_files'
  DBT_VERSION = '1.10.15';
```

The following example overrides the project’s pinned version at execution time:

Copy code

```
EXECUTE DBT PROJECT my_dbt_project
  DBT_VERSION = '1.10.15';
```

This release also introduces the following changes:

- The [DEFAULT\_DBT\_VERSION](/sql-reference/parameters#label-default-dbt-version) account parameter enables organization administrators to set a default dbt version for all
  future dbt project objects created in the account without requiring users to manually update CREATE DBT PROJECT DDL statements for
  every individual project.
- The [DESCRIBE DBT PROJECT](/sql-reference/sql/desc-dbt-project) and [SHOW DBT PROJECTS](/sql-reference/sql/show-dbt-projects) commands now return
  `dbt_version` and `dbt_snowflake_version` columns.
- The [DBT\_PROJECT\_EXECUTION\_HISTORY](/sql-reference/functions/dbt_project_execution_history) table function now returns `DBT_VERSION` and
  `DBT_SNOWFLAKE_VERSION` columns for auditing which engine version was used for each run.

For more information about the dbt Core versions that Snowflake supports, see
[Supported dbt versions for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions).
