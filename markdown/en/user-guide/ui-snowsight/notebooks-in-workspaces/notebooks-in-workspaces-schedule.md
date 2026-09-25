# Run and schedule Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Notebook Project Objects are now Code Bundles

Notebook Project Objects have been renamed to **Code Bundles**. Your existing objects, schedules, and SQL continue to work without changes: `CREATE`/`EXECUTE NOTEBOOK PROJECT` statements are still supported. For details, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

## Scheduling notebooks in Workspaces

Note

If you plan to schedule notebooks in a **shared workspace**, see [Scheduling in Shared workspaces](#label-nb-in-ws-schedule-shared-workspace-execution) for how manual (non-interactive) runs and task-based schedules behave, and which privileges apply.

When deploying notebooks to production, Snowflake provides native functionality to manage deployment, orchestration, and monitoring. You develop
and iterate on notebooks interactively in Workspaces within Snowsight. Scheduling a notebook deploys its contents into a production
object called a Code Bundle (formerly a Notebook Project Object), which encapsulates the workspace contents (for example, `.ipynb` files, Python scripts,
and SQL files). Code Bundles support versioned deployments and are schema-level objects (for example, `db_name.schema_name.bundle_name`).

After deployment, you can orchestrate notebook execution using Snowflake Tasks (which run notebook code top-down using a consistent runtime
and dependency set) or with any third-party orchestration tool. Snowflake captures execution telemetry that you can monitor in Snowsight
or query programmatically through an event table. For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

### Code Bundles

A Code Bundle is a schema-level object that acts as a production-ready “unit” in your pipeline. A Code Bundle is linked to a workspace or a stage, and all
files from the workspace are copied over. Code Bundles are executed in a non-interactive way and can be embedded in a task for scheduling.

- **Placement:** Code Bundles exist within a specific schema inside a database (`database_name.schema_name.bundle_name`).
- **Encapsulation:** When you schedule a notebook, the Code Bundle captures the entire Workspace directory to ensure all dependencies are available during execution.
- **Execution:** You execute a Code Bundle by specifying the notebook file to run as the `ENTRYPOINT`. The main notebook can call additional notebooks using [%run](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-jupyter-magics).
- **Scheduling:** You can create multiple task objects that execute the same Code Bundle, allowing multiple schedules for the same object.

For the full Code Bundles developer guide, including running on warehouses and Spark jobs, see [Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

### Discovering Code Bundles

Code Bundles are standard database objects, so you can use metadata commands to audit or clean up scheduled tasks

| Scope | Command |
| --- | --- |
| Current context | SHOW CODE BUNDLES; |
| Database level | SHOW CODE BUNDLES IN DATABASE <database\_name>; |
| Schema level | SHOW CODE BUNDLES IN SCHEMA <database\_name>.<schema\_name>; |
| Account level | SHOW CODE BUNDLES IN ACCOUNT; |

Expand

Show lessSee more

## Permissions and sharing for Code Bundles

To execute or manage a Code Bundle, a role must have the following privileges:

- **Location:** USAGE or OWNERSHIP on the database and schema containing the Code Bundle.
- **Code Bundle access:** USAGE or OWNERSHIP on the specific Code Bundle.
- **Compute:** USAGE and MONITOR on the warehouse, and USAGE on the compute pool (for Container Runtime).
- **Scheduling:** The account-level global EXECUTE TASK privilege is required if the Code Bundle is triggered by a task.
- **External access integrations:** USAGE on any EAIs used by the notebook.
- **Tasks:** When the Code Bundle is scheduled via a task, the task owner role must be granted the USAGE privilege on all required objects (such as Code Bundles,
  warehouses, or databases). The task owner role must also have privileges to execute the USE DATABASE and USE SCHEMA commands if
  the notebook sets its execution context programmatically.

Note

Code Bundles use caller’s rights, where the caller is the user (not the role). When you run [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) directly in
Snowsight, the execution uses the calling user’s identity rather than the active role in the Snowsight session.
The notebook runs in its own dedicated session (separate from the Snowsight session), with the user’s default role as the primary
role and all secondary roles activated. This means the notebook can execute with all privileges granted to the user’s roles.

## Using a Code Bundle to schedule a notebook

Currently there are two supported scenarios for deploying and scheduling notebooks. In both scenarios, notebooks must be packaged in the Code Bundle.
[Scenario A](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-a) is scheduling notebooks from a private workspace. [Scenario B](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-b)
is integrating GitHub Actions (or another CI/CD system) to automate the creation of Code Bundles from an [internal or temporary stage](/sql-reference/sql/create-stage),
manage their lifecycle through versioned updates, and orchestrate their execution using Snowflake Tasks.

| Scenario | Workspace Type | Scheduling Method |
| --- | --- | --- |
| A: Individual Development | Private | Supported. Develop in your private workspace. Create [Code Bundles](#label-nb-in-ws-schedule-npo) and schedule tasks. |
| B: Production (CI/CD) | Git-integrated | Notebook files are deployed to an internal or temporary stage from GitHub using GitHub Actions (or other CI/CD tools) and a Code Bundle is created/updated from that stage. The Task is executed on the Code Bundle. |

Expand

Show lessSee more

For detailed workflows for each scenario, see [Scheduling workflows by scenario](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios).

## View scheduled notebook runs

You can view scheduled tasks in three places:

**From the notebook**

To view or interact with scheduled runs, you must use a role with access to the database and schema where the schedule and project object were created.

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Open a scheduled notebook.
3. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png). A popover displays the following information:

> - All scheduled runs for this notebook.
> - The next scheduled run time.
> - Status of past runs. Hover over a status indicator to see details such as Query ID, last run time, duration, and status.

**From the Actions menu**

- **Open Run History:** Opens the notebook’s Code Bundle showing all past runs, including status, duration, results, source file, logs, and metrics.
  Selecting a run’s result opens the executed notebook with its output. For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

**From the Horizon Catalog Explorer**

To view run history for any scheduled notebook (including those deployed via CI/CD):

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Select the database and schema that contain the Code Bundle.
3. Select the Code Bundle.
4. Select **Run history**.
5. Select a run to view the notebook output from that execution, along with logs and metrics (when available). For more information,
   see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Manage scheduled tasks

From the **Scheduled runs** popover, you can manage your scheduled tasks by selecting the ellipsis (more actions) [![sf options button](/static/images/snowsight/icons/horizontal-options.png)](/static/images/snowsight/icons/horizontal-options.png) next to a scheduled task:

- **Run now:** Triggers an immediate execution of the scheduled task.
- **Pause schedule:** Temporarily stops the schedule from running automatically. The task remains configured but won’t execute until resumed.
- **Delete:** Removes the scheduled task permanently. You can create a new schedule with different settings (such as a different role or database
  location) after deleting the existing schedule.

## Deploy updates to scheduled notebook tasks

After editing a notebook, you must deploy your changes before scheduled runs use the updated version. Deployment ensures reproducibility and prevents
scheduled tasks from running code that differs from what was last deployed. If this is the notebook’s first task and a notebook has changes that
require deployment, the Schedule (calendar) icon displays a clock indicator. If a schedule already exists, the icon is a calendar with a clock.

After modifying code or cells, the icon indicates that there are undeployed changes.

- Select **Deploy Changes**.

  Snowflake then updates the associated Code Bundle, and all scheduled tasks for that notebook will use the newly deployed version for the next run.

## Find a Code Bundle in the Horizon Catalog Explorer

Each scheduled notebook automatically creates a Code Bundle that stores its deployed code, execution history, and artifacts. You
can locate these objects in the Horizon Catalog Explorer in Snowsight.

To locate a Code Bundle in Snowsight, follow these steps:

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Navigate to **Database** » **Schema** » **Code Bundles** to view all Code Bundles in that schema.

Alternatively, you can:

1. Open the relevant notebook.
2. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png).
3. Select **Open run history** to open the associated Code Bundle.

## View the notebook’s run history

This section describes how to view execution details and troubleshoot notebook runs after a schedule has been created. If any step fails
during execution, Snowflake stops the run to prevent partial or inconsistent downstream results.

To view run history, follow these steps:

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Open the notebook whose run history you want to review.
3. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png).
4. Select **View run history** from the drop-down menu.

> **Run History** shows the following information for the notebook’s Code Bundle:
>
> - **Results:** View the notebook and output from past runs.
> - **Tasks:** See which tasks executed the Code Bundle.
> - **Source file:** View the notebook file that was executed.
> - **Logs and metrics:** View execution logs and performance metrics (ensure you have enabled logging and event tables). For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).
> - **Run details:** Start and end times, run status, and error details. When a run fails, the error details include a categorized reason that
>   distinguishes system errors from user errors. For more information, see
>   [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Run history and result visibility

The following table summarizes who can view run history and results for **non-interactive (manual)** Code Bundle runs, runs triggered by external orchestrators, and **task** runs.

| Run type | User role or privilege | View run history? | View run results? | Notes |
| --- | --- | --- | --- | --- |
| Non-interactive (manual) | Initiating user | Yes | Yes | Run history and results are visible to the user who triggered the execution. |
| Non-interactive (manual) | Different user | Yes if the role has Code Bundle `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the user; No otherwise. | Run history visibility is controlled by the role’s Code Bundle privileges, but run results are not visible unless the role can impersonate the user. |
| Non-interactive (Airflow or external orchestrator, run as service user with `TYPE = SERVICE`) | Different user | Yes if the role has Code Bundle `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the service user; No otherwise. | Run history visibility is controlled by the role’s Code Bundle privileges, but run results are not visible unless the role can impersonate the service user. |
| Task | Task owner role | Yes | Yes | Full lifecycle control; can see history and results for task-based runs. |
| Task | Role with task `MONITOR` or `OPERATE` provilege | Yes | No | Can see status and logs, but cannot access the results. |
| Task executing as user | Task’s executing user | Yes | Yes | Run history and results are visible to the user who triggered the execution. |
| Task executing as user | Different user | Yes if the role has Code Bundle `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the user; No otherwise. | Run history visibility is controlled by the role’s Code Bundle privileges, but run results are not visible unless the role can impersonate the user. |

Expand

Show lessSee more

## Scheduling in Shared workspaces

In a shared workspace, runs use the same building blocks as elsewhere in Workspaces: a [Code Bundle](#label-nb-in-ws-schedule-npo) for packaged code and Snowflake tasks for scheduled execution.

The Code Bundle and each task are separate objects. Grant explicit privileges so collaborators can work in the workspace, deploy to the Code Bundle, execute or monitor runs, and manage tasks.

### Non-interactive execution of a Code Bundle (manual)

**Non-interactive execution of a Code Bundle (manual)** runs the deployed project headlessly (outside the notebook editor) when you issue SQL such as [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle). Use this path for ad hoc validation and testing after you deploy to the Code Bundle.

- **Visibility:** Run history and result visibility depends on the viewing role’s Code Bundle privileges and `IMPERSONATE` privilege over the initiating user. For details, see [Run history and result visibility](#label-nb-in-ws-schedule-run-visibility).
- **Requirement:** You must have `USAGE` or `OWNERSHIP` on the Code Bundle to trigger a non-interactive run **(manual)**.
- **Where to view history:** In Snowsight, use **Database** » **Schema** » the Code Bundle.

### Scheduled execution (tasks)

To run on a cadence, execute the Code Bundle from a Snowflake task. Create or manage the schedule from **Workspaces** » **Notebooks** (calendar icon) or with SQL in a worksheet.

- **Visibility:** Run history and result visibility depends on the viewing role’s Code Bundle and task privileges. For details, see [Run history and result visibility](#label-nb-in-ws-schedule-run-visibility).
- **Requirement:** The executing role must have `USAGE` on the Code Bundle and `OWNERSHIP` on the task to initiate the schedule.

### General workspace permissions

- **Creating objects:** Requires `VIEW` permission on the workspace (or a higher privilege).
- **Deploying changes:** With write access to a shared workspace, you can publish changes to the workspace. For the schedule to run with updated files, the role must have `OWNERSHIP` on the Code Bundle.

## Schedule a notebook using Tasks

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Run the following command in a SQL file/worksheet:

> Copy code
>
> ```
> -- Execute a Code Bundle using a task
> CREATE OR REPLACE TASK <database_name>.<schema_name>.<name>
>   WAREHOUSE = <string>
>   SCHEDULE = 'USING CRON 10 13 * * * America/Los_Angeles'
>   -- CRON format: <minute> <hour> <day_of_month> <month> <day_of_week> <timezone>
> AS
>   -- Execute a notebook packaged in a Code Bundle.
>   EXECUTE CODE BUNDLE "<database_name>"."<schema_name>"."<bundle_name>"
>     ENTRYPOINT = 'notebook.ipynb'  -- Path to the notebook file to run
>     ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] );  -- Optional: one quoted string per argument
> ```
>
> The compute pool, runtime, query warehouse, dependencies, external access integrations, and secrets are defined in the Code Bundle’s `code_bundle.yml` specification. Alternatively, you can pass the configuration inline in the `EXECUTE CODE BUNDLE` statement with a `WITH SPECIFICATION` clause, which is closer to how the earlier `EXECUTE NOTEBOOK PROJECT` command passed everything inline:
>
> > Copy code
> >
> > ```
> > CREATE OR REPLACE TASK <database_name>.<schema_name>.<name>
> >   WAREHOUSE = <string>
> >   SCHEDULE = 'USING CRON 10 13 * * * America/Los_Angeles'
> > AS
> >   EXECUTE CODE BUNDLE "<database_name>"."<schema_name>"."<bundle_name>"
> >     ENTRYPOINT = 'notebook.ipynb'
> >     ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] )
> >     WITH SPECIFICATION
> >     $$
> >     bundle:
> >       type: custom
> >       compute_type: compute_pool
> >       language: python
> >       compute_options:
> >         compute_pool: <compute_pool_name>
> >         query_warehouse: <warehouse_name>
> >         runtime_version: 'V2.9-CPU-PY3.12'
> >     $$;
> > ```
>
> For the full command syntax, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle).

After creating this task, run the following command to activate the schedule:

> Copy code
>
> ```
> ALTER TASK <database_name>.<schema_name>.<task_name> RESUME;
> ```

If a task fails because your active role lacks the required privileges, Snowsight displays the relevant error messages so you can
address missing permissions.

For syntax, parameters, and examples, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle). For information about passing parameters to scheduled notebooks, see [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters).

Note

To learn more about credit usage, idle timeout behavior, and notebook service management, see [Setting up compute](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-compute-setup)
and [Idle timeout](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-idle-timeout).

## Run a scheduled notebook as a specific user

By default, a task runs as an internal system service that uses the privileges of the task owner role. Because Code Bundles
run with caller’s rights, you can add the [EXECUTE AS USER](/sql-reference/sql/create-task) clause to the task so that scheduled
runs are performed on behalf of a named user instead. This approach gives you:

- **Secondary roles:** the run activates the user’s default secondary roles, so the notebook can reach objects spread across
  multiple roles.
- **User-based policies:** masking policies and row access policies that evaluate the querying user resolve against the named
  user rather than a system user.
- **Audit attribution:** runs are attributed to the named user instead of the `SYSTEM` user, giving you a clear audit trail.

`EXECUTE AS USER` is supported for both compute paths: Container Runtime (compute pool) and warehouse execution.

Before you create the task, grant the task owner role the `IMPERSONATE` privilege on the user, and grant the user the task’s
owner role:

Copy code

```
GRANT IMPERSONATE ON USER notebook_service_user TO ROLE notebook_task_owner;
GRANT ROLE notebook_task_owner TO USER notebook_service_user;
```

Then specify the user when you create the task:

Copy code

```
CREATE OR REPLACE TASK my_db.my_schema.nightly_run
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
  EXECUTE AS USER notebook_service_user
AS
  EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
    ENTRYPOINT = 'notebook.ipynb';
```

For production schedules, we recommend a dedicated service user rather than a person’s user. A service user gets only the
privileges you intend, and the schedule keeps working if the person changes teams or leaves. For more information about
user-based task execution, see [Run tasks with user privileges](/user-guide/tasks-intro#label-user-based-security-for-tasks).

Note

Run history and results for these runs are visible to the executing user. Other users need Code Bundle `OWNERSHIP`, `USAGE`, or
`MONITOR` to see run history, and `IMPERSONATE` on the executing user to see run results. For details, see
[Run history and result visibility](#label-nb-in-ws-schedule-run-visibility).
