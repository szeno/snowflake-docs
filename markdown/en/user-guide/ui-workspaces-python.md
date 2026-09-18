# Python files in Workspaces

## Overview

You can run Python files (`.py`) interactively in Workspaces using the same notebook services infrastructure as
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview). Open a `.py` file in your
workspace, connect to a notebook service, and use **Run** to execute the file. Output appears in the **Output** tab in the Tools panel.

Use Python files when you want a script-style workflow in the same governed Workspaces environment as notebooks—for example, utilities, training
scripts, or ETL jobs you also deploy to production.

## Open and run a Python file

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Open an existing `.py` file, or create one:
   - Select **+** next to a folder » **File**, then name the file with a `.py` extension.
   - Or upload a `.py` file with **Upload Files**.
4. Connect to a notebook service when prompted. See [Connect to compute](#label-py-in-ws-connect-compute).
5. Select **Run** to execute the file. The **Output** tab opens automatically and shows results, including the interactive datagrid when applicable.

**Run** executes the entire file in one pass, the same way as in other Python development environments (for example, your IDE or running a script from
the terminal)—not individual sections or cells. There is no per-cell **Run all** control.

## Connect to compute

Python files use the same Snowflake-managed notebook services as notebooks in Workspaces. When you first run a Python file or notebook in a
workspace, you create or select a service and configure Python version, Snowflake Container Runtime version, compute pool, idle timeout, and
external access integrations.

- A single running notebook service can be shared by notebooks (`.ipynb`) and Python files in the same workspace.
- If a service is already running for a notebook, you can reuse it to run Python files without starting a separate service.

For full details on creating, suspending, and governing notebook services, see
[Compute setup for Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup).

## Tools panel

Select <icon>:ui:*Tools* in the editor toolbar to open the Tools panel.

| Tab | Python files |
| --- | --- |
| **Output** | Primary surface for run results. Opens automatically when you select **Run**. Use **Clear output** to clear this pane. |
| **Terminal** | Same behavior as for notebooks. See [Using the Terminal](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-terminal). |
| **Variables** | Same behavior as for notebooks. See [Developer tools](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-terminal). |
| **Dependency graph** | Not available. |
| **Scratchpad** | Not available. |

Expand

Show lessSee more

You must be connected to a notebook service to use the Tools panel.

## Python libraries and Snowflake data

You can use the same Python ecosystem and Snowflake connectivity patterns as in notebooks, including third-party packages, Snowpark, and
utilities imported from other files in your workspace.

- **Packages:** Install and manage dependencies the same way as for notebooks. See
  [Managing packages and runtime](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-packages-runtime).
- **Snowpark:** Create a session in your script the same way as in a notebook Python cell:

  Copy code

  ```
  from snowflake.snowpark.context import get_active_session
  session = get_active_session()
  ```

  For more information, see [Create a Snowpark session](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-create-snowpark-session).
- **Secrets:** Use workspace secrets the same way as for notebooks. See
  [Using secrets in notebooks](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets).
- **Files in the workspace:** Reference data and modules by relative path. See
  [Working with the file system](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-file-system).

## Deploy and schedule

**Deploy** and **Schedule** in the Python file editor work similarly to notebooks in Workspaces. You can deploy your workspace to a
Code Bundle (formerly a Notebook Project Object) and run or schedule production executions with Snowflake Tasks.

When you create a schedule for a Python file, you can choose **Warehouse** as the runtime, in addition to a compute pool. The warehouse
runtime option is labeled **Preview** and is available for Python files (`.py`) only. Notebooks (`.ipynb`) run on compute pools
(Snowpark Container Services). Running Code Bundles on compute pools is generally available; running on warehouses is in Public Preview.

For permissions, deployment steps, scheduling, and monitoring, see
[Run and schedule Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule).

## Shared with notebooks

The following capabilities use the same notebook services infrastructure and documentation as notebooks in Workspaces:

- Compute pools, idle timeout, and credit usage
- External access integrations
- Python and Snowflake Container Runtime versions
- Observability and logging for scheduled runs

## Differences from notebooks

| Capability | Notebooks (`.ipynb`) | Python files (`.py`) |
| --- | --- | --- |
| Execution unit | Cells | Entire file |
| Run controls | **Run all**, per-cell run, and related options | **Run** only |
| Output | Per-cell output; **Export as HTML** | **Output** tab only; no export or share of output |
| Role and warehouse picker | Available in the notebook editor | Not shown in the Python file editor |
| SQL cells and cell referencing | Supported | Not supported |
| Dependency graph | Available | Not available |
| Scratchpad | Available | Not available |
| Show/hide all and clear all results | Available | Not available; use **Clear output** on the **Output** tab |
| Start and stop tracing | Available | Not available |

Expand

Show lessSee more

## Limitations

In addition to the [limitations for notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-limitations), the following apply to Python files:

- Interactive output is shown only in the **Output** tab. Output is not saved to the `.py` file, and **Export as HTML** is not supported.
- The **Dependency graph** and **Scratchpad** tools are not available.
- Cell-level features (SQL cells, cell referencing, minimap cell status, and Jupyter magics tied to cells) apply only to notebooks, not to `.py` files.
