# Scheduling workflows by scenario

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Notebook Project Objects are now Code Bundles

Notebook Project Objects have been renamed to **Code Bundles**. Your existing objects, schedules, and SQL continue to work without changes: `CREATE`/`EXECUTE NOTEBOOK PROJECT` statements are still supported. For details, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

This topic provides detailed workflows for scheduling notebooks in two common scenarios:

- **Scenario A:** Development in a private workspace - Schedule notebooks directly from Snowsight
- **Scenario B:** Production (CI/CD) - Deploy notebooks from a Git repository using CI/CD pipelines

## Scenario A: Development in a private workspace

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Select **+ Add new** » **Notebook** to create a new notebook, or open an existing notebook to be scheduled.

   Note

   Ensure that you have specified the execution context (database and schema) in the notebook you are scheduling. For more information,
   see [Set the execution context](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-execution-context).
3. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png).

   - If this is the notebook’s first task, the [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png) icon is a calendar.
   - If a schedule already exists, the [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png) icon is a calendar with a clock.
4. Select **Create Schedule**.
5. In the **Schedule a Notebook Task** dialog, provide the following information:

   **Basic settings**

   - **Task name:** The unique name for the scheduled task. The default name is `{notebook-name}_task_#` but can be updated if necessary.
   - **Owner role:** The Snowflake role under which the task executes. Select a role with the required permissions to execute all operations performed by
     the scheduled notebook. This role must have permissions to:

     - Read/write the database objects the notebook uses.
     - Access warehouses, compute pools, and integrations.
     - Create/update the task and Code Bundle objects.
   - **Location:** The database and schema where the task object and associated Code Bundle is created. Choose a schema where your role
     has CREATE TASK and USAGE privileges. If your role has only USAGE privileges on the schema, ensure it also has the CREATE CODE BUNDLE privilege.
   - **Frequency:** How often the notebook should run. Choose from: Hourly, Daily, Weekly, Monthly, or Custom (Cron scheduling). All execution times use
     your local time zone.

   **Advanced settings (all fields are required unless otherwise specified)**

   - **Code Bundle name (formerly Notebook project name):** A unique name for the notebook’s Code Bundle that Snowflake creates for task execution. If not edited, Snowflake provides a
     default name.
   - **Parameters (optional):** Key-value parameters are passed to the notebook at runtime and appear as command-line arguments (in `sys.argv`). Parameters
     are useful for passing dates, environment flags, thresholds, or model versions. Parameters can be passed in Snowsight as whitespace-separated values
     or in the [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) command as `ARGUMENTS = ('env', 'prod')`. For more information, see
     [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters).
   - **Runtime variant:** The runtime environment used for notebook execution. Choose from:

     - **CPU:** Uses a CPU Container Runtime environment and runs on a CPU compute pool (for example, the automatically provisioned `SYSTEM_COMPUTE_POOL_CPU`).
     - **GPU:** Uses a GPU Container Runtime environment that includes GPU-accelerated libraries and runs on a GPU compute pool (such as `SYSTEM_COMPUTE_POOL_GPU`).
     - **Python version:** The Python version used during task execution.
     - **Runtime version:** The base Container Runtime image. Choosing the correct runtime version ensures that your notebook runs consistently between
       development and scheduled execution.
   - **Compute pool:** The compute pool that executes the notebook task. Ensure that the compute pool has capacity (free nodes) at the time of
     the scheduled execution. To prevent scheduled runs from failing, we recommend that you use a dedicated compute pool to ensure no other SPCS services
     take up full capacity.
   - **Query warehouse:** The Snowflake warehouse used for all SQL queries inside the notebook.
   - **External access integrations (optional):** Defines which external access integrations (EAIs) the notebook may use. EAIs are required if
     your notebook requires external APIs, third-party services, or cloud storage outside of Snowflake’s internal stages. If no EAIs are listed, your
     selected role does not own or have privileges on any integrations.
   - **Secrets (optional):** Selects authentication secrets the scheduled run can read (for example, API keys or OAuth tokens) when used together with EAIs.
     For prerequisites, mount paths, and Python examples, see [Using secrets in Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets).
   - **Requirements file (optional):** Pre-install Python dependencies for repeatable runs using the `REQUIREMENTS_FILE` parameter. For more
     information, see [Managing packages and runtime](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-packages-runtime).
6. Review the schedule preview, and select **Create**.

## Scenario B: Production (CI/CD)

For production environments, we recommend managing notebook code in a Git-based workspace (for details, see [Integrate workspaces with a Git repository](/user-guide/ui-snowsight/workspaces-git))
or developing locally in your preferred IDE. You can use a CI/CD pipeline (such as GitHub Actions) to deploy files to a Snowflake internal or temporary stage.

For a hands-on walkthrough of this pattern, see the [Getting Started with Data Engineering using Snowflake Notebooks](https://www.snowflake.com/en/developers/guides/data-engineering-with-notebooks/)
quickstart and the accompanying [code repository](https://github.com/Snowflake-Labs/sfguide-data-engineering-with-notebooks) on GitHub.

After the files are on the stage, you can:

- Create a Code Bundle sourced from that stage location.
- Schedule the Code Bundle using a Snowflake Task for automated execution.

1. **Create a stage**

   Use [CREATE STAGE](/sql-reference/sql/create-stage) to create an internal or temporary stage:

   Copy code

   ```
   -- Ensure the landing zone exists
   CREATE STAGE IF NOT EXISTS <database_name>.<schema_name>.<stage_name>;
   ```
2. **Load/deploy notebook file(s) to the internal or temporary stage**

   Your CI/CD pipeline should upload the `.ipynb` file(s) to a Snowflake stage. Use the [PUT](/sql-reference/sql/put) command to ensure that the notebook
   files are loaded into a stage readable by the Code Bundle.

   Copy code

   ```
   PUT file://<absolute_path_to_file>/ @<database_name>.<schema_name>.<stage_name> AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```

   Example:

   Copy code

   ```
   PUT file://notebooks/ml_model/train.ipynb @<database_name>.<schema_name>.<stage_name> AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
   ```
3. **Create or update the Code Bundle**

   Create (or update) the Code Bundle to reference the internal or temporary stage that contains your deployed notebook files:

   Copy code

   ```
   CREATE CODE BUNDLE IF NOT EXISTS <database_name>.<schema_name>.<bundle_name>
     FROM '@<database_name>.<schema_name>.<stage_name>';
   ```
4. **Alter the Code Bundle details**

   For subsequent code changes, your pipeline executes an ALTER command. This adds a new version of the code without
   having to drop and recreate the object:

   Copy code

   ```
   -- Add a new version with the latest code from the stage
   ALTER CODE BUNDLE <database_name>.<schema_name>.<bundle_name>
     ADD VERSION FROM '@<database_name>.<schema_name>.<stage_name>';
   ```
5. **Execute the Code Bundle (orchestrate with a task)**

   Create a task to schedule and execute the Code Bundle. Use a Snowflake task to define the schedule for the Code Bundle.

   Note

   Ensure that you specify your notebook execution context (use the database and schema of the notebook you want to schedule). For more
   information, see [Set the execution context](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-execution-context).

   Copy code

   ```
   -- Create or replace the task to orchestrate the notebook
   CREATE OR REPLACE TASK <database_name>.<schema_name>.<task_name>
     WAREHOUSE = '<warehouse_name>'
     SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
   AS
     EXECUTE CODE BUNDLE <database_name>.<schema_name>.<bundle_name>
    ENTRYPOINT = 'path/to/notebook.ipynb'
    ARGUMENTS = ('<db_name>', '<schema_name>', '<warehouse_name>');
   ```

   The compute pool, runtime, and query warehouse are defined in the Code Bundle’s `code_bundle.yml` specification. Alternatively, pass the
   configuration inline with a `WITH SPECIFICATION` clause (closer to the earlier `EXECUTE NOTEBOOK PROJECT` inline style):

   Copy code

   ```
   CREATE OR REPLACE TASK <database_name>.<schema_name>.<task_name>
     WAREHOUSE = '<warehouse_name>'
     SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
   AS
     EXECUTE CODE BUNDLE <database_name>.<schema_name>.<bundle_name>
       ENTRYPOINT = 'path/to/notebook.ipynb'
       ARGUMENTS = ('<db_name>', '<schema_name>', '<warehouse_name>')
       WITH SPECIFICATION
       $$
       bundle:
         type: custom
         compute_type: compute_pool
         language: python
         compute_options:
           compute_pool: SYSTEM_COMPUTE_POOL_CPU
           query_warehouse: <warehouse_name>
           runtime_version: 'V2.9-CPU-PY3.12'
       $$;
   ```

   For information about passing parameters to scheduled notebooks, see [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters).

   When the notebook needs authenticated outbound access, define the external access integrations and secrets in the Code Bundle’s `code_bundle.yml`
   specification. For syntax and examples, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) and [Using secrets in Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets).
6. **View your notebook run or execution history**

   After the task runs, you can monitor its success or failure in Snowsight to ensure the CI/CD deployment is performing as expected.
   For detailed instructions on viewing run history, see [View scheduled notebook runs](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-view-runs).

Snowsight supports non-interactive (headless) execution of notebooks. This allows you to trigger a programmatic run of a notebook without
opening Snowsight and without requiring a recurring schedule.

Headless execution is intended for tasks, scheduled tasks, or workflows orchestrated by tools such as Airflow, Prefect, Dagster, CI/CD pipelines, or
external systems that need to execute a notebook programmatically. For more information, see [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle).

Note

To run the SQL commands in this workflow (such as `CREATE CODE BUNDLE` and `CREATE TASK`), you must execute them from a SQL
file or SQL worksheet in Workspaces, not from within a notebook cell.
