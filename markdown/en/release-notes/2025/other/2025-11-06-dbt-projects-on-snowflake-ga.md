# Nov 06, 2025: dbt Projects on Snowflake (*General availability*)

dbt Projects on Snowflake are now generally available.

dbt Projects on Snowflake let you use familiar Snowflake features to create, edit, test, run, and manage dbt Core projects. You can use Workspaces in
Snowsight to work with dbt project files and directories and deploy a dbt project as a schema-level DBT PROJECT object. You can also
use SQL to work with dbt project objects and use Snowflake CLI commands to integrate deployment and execution into your CI/CD workflows.

## What’s new since preview

- **Performance improvements and optimizations when running dbt commands on Snowflake:** During preview, result upload usually took approximately
  6 to 6.5 minutes. Now, upload completes approximately 8 to 10x faster in ~40 to 45 seconds.
- **Secondary roles requirement:** Using dbt in Workspaces no longer requires secondary roles.
- **Increased coverage for dbt commands:** dbt Projects on Snowflake now support the `dbt docs generate` and `dbt retry` commands and additional
  flags in `dbt compile`.
- **Support in Snowsight:** View the project DAG alongside model and test source code from the **Project details** page.
- **Expanded execution and scheduling UI support:** Enable customers to run and schedule dbt projects from the **Project details** page in
  Snowsight.
- **Easy access to dbt execution artifacts:** Easily access the dbt project execution artifacts containing execution results and log files. This
  is helpful for debugging dbt project executions and integration with central observability tools.
- **Replication support of dbt project objects:** Replicate dbt project objects to failover accounts.

For more information, see [dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake).
