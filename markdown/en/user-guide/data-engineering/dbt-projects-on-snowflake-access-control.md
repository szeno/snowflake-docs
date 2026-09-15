# Access control for dbt projects on Snowflake

The following commands demonstrate commonly granted privileges for dbt project objects.

- **To grant privileges to create a dbt project object, including deploying from within a workspace:**

  Copy code

  ```
  GRANT CREATE DBT PROJECT ON SCHEMA my_database.my_schema TO ROLE my_role;
  ```
- **To grant privileges to alter or drop (delete) a dbt project object, including connecting a workspace to a dbt project object:**

  Copy code

  ```
  GRANT OWNERSHIP ON DBT PROJECT my_dbt_project_object TO ROLE my_role;
  ```
- **To grant privileges to execute a dbt project object and to list or get files:**

  Copy code

  ```
  GRANT USAGE ON DBT PROJECT my_dbt_project_object TO ROLE my_role;
  ```
- **To view a dbt project object in Snowsight or retrieve dbt artifacts from recent executions:**
  Use a role that has the `MONITOR` privilege on the dbt project object. This privilege is required to call
  `SYSTEM$DBT_GET_LAST_SUCCESSFUL_RUN_TARGET`, `SYSTEM$DBT_GET_LAST_FAILED_RUN_TARGET`, or `SYSTEM$DBT_GET_LAST_RUN_TARGET`. Without it, you
  can’t access the project details, run history, monitoring information, or artifacts returned by these functions.

  Copy code

  ```
  GRANT MONITOR ON DBT PROJECT my_dbt_project_object TO ROLE my_role;
  ```

For more information, see [dbt project object privileges](/user-guide/security-access-control-privileges#label-access-control-privs-dbt).

## Roles and privileges for dbt project deployment

Deployment happens in two phases: an initial phase that creates or updates the dbt project object, and a compilation phase where dbt resolves Jinja, validates SQL, and optionally installs dependencies. Each phase can use a different role: the initial phase uses whichever role is active in your SQL worksheet, selected in the Snowsight deploy dialog, or configured in your Snowflake CLI’s `connection.toml`, while the compilation phase uses the role from the target in [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`.

| Deploy method | Initial phase role (creates or updates the object) |
| --- | --- |
| **Snowsight** | The role you select in **Connect** » **Deploy dbt project** |
| **SQL** | The role active in the worksheet when you run `CREATE DBT PROJECT` or `ALTER DBT PROJECT` |
| **CLI** | The role in your `connection.toml` (or overridden by `--role`) when you run `snow dbt deploy` |

Expand

Show lessSee more

For the compilation phase, Snowflake uses the target named by `DEFAULT_TARGET`. If `DEFAULT_TARGET` isn’t set, Snowflake uses the default
target defined in the profile file. When both profile files are present,
[`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) takes
precedence over `profiles.yml`.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

### Optionally separate deployment from execution

For stronger separation of duties, use a deploy-only role in your CI/CD pipeline. To create a dbt project object, grant this role
`CREATE DBT PROJECT` on the target schema. The role owns the object after creating it. To replace the live version of an existing object,
grant the role `OWNERSHIP` on that object.

With automatic compilation enabled, Snowflake runs `dbt compile` during deployment using the role defined by the selected target. If an
external access integration is configured, Snowflake first runs `dbt deps`, then `dbt compile`. Deploy with
`snow dbt deploy --no-auto-compile` to skip both commands and leave dbt command execution to a separate role.

For the simplest setup, use one execution role as both the calling role and the profile role. For external orchestration, configure it as the
active Snowflake role. For Snowflake tasks, use it as the task owner role.

Grant the execution role `USAGE` on the dbt project object and the warehouse and data privileges required to compile, run, or test the
project. The calling role and profile role can differ; the following sections describe the permissions for each execution method.

If the execution role uses any recent-run artifact retrieval function to import artifacts from a production dbt project object, also grant
it `MONITOR` on that object.

## Roles and privileges for dbt project execution

When you execute a dbt project object, the roles that perform execution and that materialize output when you specify the dbt `run` or `build` commands depend on the method of execution.

### Execution from SQL or CLI

The dbt command specified in EXECUTE DBT PROJECT runs with the privileges of the `role` specified in the `outputs` block of the project’s [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file. Operations are further restricted to only those privileges granted to the Snowflake user calling EXECUTE DBT PROJECT. Both the user and the role specified must have the required privileges to use the `warehouse`, perform operations on the `database` and `schema` specified in the profile file, and perform operations on any other Snowflake objects that the dbt model specifies. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

### Execution from within Workspaces

Choosing the dbt **Run** or **Build** command for a project from within a workspace materializes target output using the `role` defined in the project’s [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` file. Both the user and the role specified must have the required privileges to use the `warehouse`, perform operations on the `database` and `schema` that are specified in the profile file, and perform operations on any other Snowflake objects that the dbt model specifies. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

### Scheduled execution from within Workspaces

Scheduling dbt project object execution from within Workspaces creates user-managed tasks. To create a task from within Workspaces, a user must have a role with privileges described under [Access control requirements](/sql-reference/sql/create-task#label-create-task-sql-access-control) in the CREATE TASK reference. Snowflake runs tasks with the privileges of the task owner, but task runs are not associated with the user. For more information, see [Tasks run by a system service](/user-guide/tasks-intro#label-system-service).
