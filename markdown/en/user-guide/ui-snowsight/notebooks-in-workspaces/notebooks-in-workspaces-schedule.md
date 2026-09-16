# Run and schedule Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## Scheduling notebooks in Workspaces

Note

If you plan to schedule notebooks in a **shared workspace**, see [Scheduling in Shared workspaces](#label-nb-in-ws-schedule-shared-workspace-execution) for how manual (non-interactive) runs and task-based schedules behave, and which privileges apply.

When deploying notebooks to production, Snowflake provides native functionality to manage deployment, orchestration, and monitoring. You develop
and iterate on notebooks interactively in Workspaces within Snowsight. Scheduling a notebook deploys its contents into a production
object called a Notebook Project Object (NPO), which encapsulates the workspace contents (for example, `.ipynb` files, Python scripts,
and SQL files). NPOs support versioned deployments and are schema-level objects (for example, `db_name.schema_name.npo_name`).

After deployment, you can orchestrate notebook execution using Snowflake Tasks (which run notebook code top-down using a consistent runtime
and dependency set) or with any third-party orchestration tool. Snowflake captures execution telemetry that you can monitor in Snowsight
or query programmatically through an event table. For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

### Notebook Project Objects (NPOs)

An NPO is a schema-level object that acts as a production-ready “unit” in your pipeline. A Notebook project is linked to a workspace or a stage, and all
files from the workspace are copied over. NPOs are executed in a non-interactive way and can be embedded in a task for scheduling.

- **Placement:** NPOs exist within a specific schema inside a database (`database_name.schema_name.npo_name`).
- **Encapsulation:** When you schedule a notebook, the NPO captures the entire Workspace directory to ensure all dependencies are available during execution.
- **Execution:** You execute an NPO by specifying a main `.ipynb` file (for example, using the `MAIN_FILE` parameter). The main notebook can call additional notebooks using [%run](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-jupyter-magics).
- **Scheduling:** You can create multiple task objects that execute the same NPO, allowing multiple schedules for the same notebook project object.

### Discovering NPOs

NPOs are standard database objects, so you can use metadata commands to audit or clean up scheduled tasks

| Scope | Command |
| --- | --- |
| Current context | SHOW NOTEBOOK PROJECTS; |
| Database level | SHOW NOTEBOOK PROJECTS IN DATABASE <database\_name>; |
| Schema level | SHOW NOTEBOOK PROJECTS IN SCHEMA <database\_name>.<schema\_name>; |
| Account level | SHOW NOTEBOOK PROJECTS IN ACCOUNT; |

Expand

Show lessSee more

## Permissions and sharing for NPOs

To execute or manage an NPO, a role must have the following privileges:

- **Location:** USAGE or OWNERSHIP on the database and schema containing the NPO.
- **NPO access:** USAGE or OWNERSHIP on the specific NPO.
- **Compute:** USAGE and MONITOR on the warehouse, and USAGE on the compute pool (for Container Runtime).
- **Scheduling:** The account-level global EXECUTE TASK privilege is required if the NPO is triggered by a task.
- **External access integrations:** USAGE on any EAIs used by the notebook.
- **Tasks:** When the NPO is scheduled via a task, the task owner role must be granted the USAGE privilege on all required objects (such as NPOs,
  warehouses, or databases). The task owner role must also have privileges to execute the USE DATABASE and USE SCHEMA commands if
  the notebook sets its execution context programmatically.

Note

NPOs use caller’s rights, where the caller is the user (not the role). When you run [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) directly in
Snowsight, the execution uses the calling user’s identity rather than the active role in the Snowsight session.
The notebook runs in its own dedicated session (separate from the Snowsight session), with the user’s default role as the primary
role and all secondary roles activated. This means the notebook can execute with all privileges granted to the user’s roles.

## Using an NPO to schedule a notebook

Currently there are two supported scenarios for deploying and scheduling notebooks. In both scenarios, notebooks must be packaged in the NPO.
[Scenario A](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-a) is scheduling notebooks from a private workspace. [Scenario B](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-b)
is integrating GitHub Actions (or another CI/CD system) to automate the creation of NPOs from an [internal or temporary stage](/sql-reference/sql/create-stage),
manage their lifecycle through versioned updates, and orchestrate their execution using Snowflake Tasks.

| Scenario | Workspace Type | Scheduling Method |
| --- | --- | --- |
| A: Individual Development | Private | Supported. Develop in your private workspace. Create [Notebook Project Objects](#label-nb-in-ws-schedule-npo) (NPO) and schedule tasks. |
| B: Production (CI/CD) | Git-integrated | Notebook files are deployed to an internal or temporary stage from GitHub using GitHub Actions (or other CI/CD tools) and an NPO is created/updated from that stage. The Task is executed on the NPO. |

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

- **Open Run History:** Opens the notebook’s project object showing all past runs, including status, duration, results, source file, logs, and metrics.
  Selecting a run’s result opens the executed notebook with its output. For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

**From the Horizon Catalog Explorer**

To view run history for any scheduled notebook (including those deployed via CI/CD):

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Select the database and schema that contain the Notebook Project Object (NPO).
3. Select the NPO.
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

  Snowflake then updates the associated notebook project object, and all scheduled tasks for that notebook will use the newly deployed version for the next run.

## Find a notebook project object (NPO) in the Horizon Catalog Explorer

Each scheduled notebook automatically creates an NPO that stores its deployed code, execution history, and artifacts. You
can locate these objects in the Horizon Catalog Explorer in Snowsight.

To locate an NPO in Snowsight, follow these steps:

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Navigate to **Database** » **Schema** » **Notebook Project Objects** to view all NPOs in that schema.

Alternatively, you can:

1. Open the relevant notebook.
2. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png).
3. Select **Open run history** to open the associated NPO.

## View the notebook’s run history

This section describes how to view execution details and troubleshoot notebook runs after a schedule has been created. If any step fails
during execution, Snowflake stops the run to prevent partial or inconsistent downstream results.

To view run history, follow these steps:

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Open the notebook whose run history you want to review.
3. At the top of the notebook editor, select **Scheduled runs** [![Scheduled runs icon](/static/images/workspaces/nb-scheduled-runs.png)](/static/images/workspaces/nb-scheduled-runs.png).
4. Select **View run history** from the drop-down menu.

> **Run History** shows the following information for the notebook’s project object:
>
> - **Results:** View the notebook and output from past runs.
> - **Tasks:** See which tasks executed the NPO.
> - **Source file:** View the notebook file that was executed.
> - **Logs and metrics:** View execution logs and performance metrics (ensure you have enabled logging and event tables). For more information, see [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).
> - **Run details:** Start and end times, run status, and error details. When a run fails, the error details include a categorized reason that
>   distinguishes system errors from user errors. For more information, see
>   [Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Run history and result visibility

The following table summarizes who can view run history and results for **non-interactive (manual)** NPO runs, runs triggered by external orchestrators, and **task** runs.

| Run type | User role or privilege | View run history? | View run results? | Notes |
| --- | --- | --- | --- | --- |
| Non-interactive (manual) | Initiating user | Yes | Yes | Run history and results are visible to the user who triggered the execution. |
| Non-interactive (manual) | Different user | Yes if the role has NPO `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the user; No otherwise. | Run history visibility is controlled by the role’s NPO privileges, but run results are not visible unless the role can impersonate the user. |
| Non-interactive (Airflow or external orchestrator, run as service user with `TYPE = SERVICE`) | Different user | Yes if the role has NPO `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the service user; No otherwise. | Run history visibility is controlled by the role’s NPO privileges, but run results are not visible unless the role can impersonate the service user. |
| Task | Task owner role | Yes | Yes | Full lifecycle control; can see history and results for task-based runs. |
| Task | Role with task `MONITOR` or `OPERATE` provilege | Yes | No | Can see status and logs, but cannot access the results. |
| Task executing as user | Task’s executing user | Yes | Yes | Run history and results are visible to the user who triggered the execution. |
| Task executing as user | Different user | Yes if the role has NPO `OWNERSHIP`, `USAGE`, or `MONITOR`; No otherwise. | Yes if the role has `IMPERSONATE` privilege over the user; No otherwise. | Run history visibility is controlled by the role’s NPO privileges, but run results are not visible unless the role can impersonate the user. |

Expand

Show lessSee more

## Scheduling in Shared workspaces

In a shared workspace, runs use the same building blocks as elsewhere in Workspaces: a [Notebook Project Object](#label-nb-in-ws-schedule-npo) (NPO) for packaged code and Snowflake tasks for scheduled execution.

The NPO and each task are separate objects. Grant explicit privileges so collaborators can work in the workspace, deploy to the NPO, execute or monitor runs, and manage tasks.

### Non-interactive execution of an NPO (manual)

**Non-interactive execution of an NPO (manual)** runs the deployed project headlessly (outside the notebook editor) when you issue SQL such as [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project). Use this path for ad hoc validation and testing after you deploy to the NPO.

- **Visibility:** Run history and result visibility depends on the viewing role’s NPO privileges and `IMPERSONATE` privilege over the initiating user. For details, see [Run history and result visibility](#label-nb-in-ws-schedule-run-visibility).
- **Requirement:** You must have `USAGE` or `OWNERSHIP` on the NPO to trigger a non-interactive run **(manual)**.
- **Where to view history:** In Snowsight, use **Database** » **Schema** » the NPO.

### Scheduled execution (tasks)

To run on a cadence, execute the NPO from a Snowflake task. Create or manage the schedule from **Workspaces** » **Notebooks** (calendar icon) or with SQL in a worksheet.

- **Visibility:** Run history and result visibility depends on the viewing role’s NPO and task privileges. For details, see [Run history and result visibility](#label-nb-in-ws-schedule-run-visibility).
- **Requirement:** The executing role must have `USAGE` on the NPO and `OWNERSHIP` on the task to initiate the schedule.

### General workspace permissions

- **Creating objects:** Requires `VIEW` permission on the workspace (or a higher privilege).
- **Deploying changes:** With write access to a shared workspace, you can publish changes to the workspace. For the schedule to run with updated files, the role must have `OWNERSHIP` on the NPO.

## Schedule a notebook using Tasks

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Run the following command in a SQL file/worksheet:

> Copy code
>
> ```
> -- Execute a notebook project using a task
> CREATE OR REPLACE TASK <database_name>.<schema_name>.<name>
>   WAREHOUSE = <string>
>   SCHEDULE = 'USING CRON 10 13 * * * America/Los_Angeles'
>   -- CRON format: <minute> <hour> <day_of_month> <month> <day_of_week> <timezone>
> AS
>   -- Execute a notebook stored within a notebook project.
>   EXECUTE NOTEBOOK PROJECT "<database_name>"."<schema_name>"."<project_name>"
>     MAIN_FILE = 'notebook.ipynb'  -- Path to the notebook file
>     COMPUTE_POOL = '<compute_pool_name>'
>     RUNTIME = '<runtime_version>'  -- e.g. V2.2-CPU-PY3.11
>     QUERY_WAREHOUSE = '<wh_name>'
>     ARGUMENTS = '<string>'  -- Can pass a single string parsed in the notebook code
>     REQUIREMENTS_FILE = '<path/to/requirements.txt>'  -- Pre-installs dependencies before the notebook runs
>     EXTERNAL_ACCESS_INTEGRATIONS = ('integration_name');  -- e.g. ('http_eai', 's3_eai')
> ```

After creating this task, run the following command to activate the schedule:

> Copy code
>
> ```
> ALTER TASK <database_name>.<schema_name>.<task_name> RESUME;
> ```

If a task fails because your active role lacks the required privileges, Snowsight displays the relevant error messages so you can
address missing permissions.

For syntax, parameters, and examples, see [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project). For information about passing parameters to scheduled notebooks, see [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters).

Note

To learn more about credit usage, idle timeout behavior, and notebook service management, see [Setting up compute](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-compute-setup)
and [Idle timeout](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-idle-timeout).
