# Notebooks in Workspaces limitations

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## Notebook services and runtime

- The number of notebook services allowed in an account is subject to the Snowpark Container Services [account limits](/developer-guide/snowpark-container-services/working-with-compute-pool#guidelines-and-limitations).
- Notebook services can only run on x86-based compute pools. ARM-based compute pools are not yet supported.
- Users may create multiple services and assign notebooks to different services as needed. Services can be shared across Workspaces but are scoped to per user.
- Notebook services may be restarted over the weekend for container service maintenance. After a restart, you must rerun notebooks and reinstall any
  packages to restore variables and packages. For more information, see [Service maintenance](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-service-maintenance).
- Package installation and listing behavior differs between `uv` and standard `pip`. Snowflake supports installing packages using
  `uv pip install`, and `uv pip freeze` lists only packages installed using `uv pip install`. `pip freeze` lists all packages available in the environment, including packages in the base image, packages installed with standard pip install, and packages installed with `uv pip install`.
- Installing packages from external stages is not supported.

## Using notebooks in Workspaces

- Queries in SQL cells do not appear in the **Query History** pane until you shut down the kernel:

  1. Select **Connected**.
  2. Select **Shut down kernel**.
  3. Suspend the notebook service.
- Renaming notebook files, folders, or the workspace can cause unexpected behavior, including service disconnection, clearing the notebook’s output
  cache, or delays in updating referenced files.
- If you are disconnected, try reconnecting the notebook. If you renamed the workspace, create and use a new service.
- If account session policies block the use of secondary roles, notebooks cannot run in shared workspaces.
- Cell-by-cell rendering is not currently supported when viewing differences in Git-integrated workspaces or when viewing publish history in
  shared workspaces. The entire notebook file is displayed as a unified diff.

## Editing and running notebooks

- Updates to Python files (`.py`) imported by a notebook are not automatically detected by the active notebook service. To apply changes,
  restart the notebook kernel or use the `%autoreload` magic command before your initial import so that file updates are detected automatically.
- Each Python cell has an output limit of 20 MB.
- Output of previous notebook executions is cached in an internal storage system, which is not yet
  [Tri-Secret Secure](/user-guide/security-encryption-tss). Access to this cache is encrypted at rest and results in the cache are guarded
  by governance rules.
- Embedding remote images via URLs is not yet supported. To embed an image, upload it to your workspace and display it in a Markdown or
  Python cell. Example:

  Copy code

  ```
  ![My Image](path/to/example_image.png)
  ```

  Copy code

  ```
  from IPython.display import Image, display
  display(Image(filename="path/to/example_image.png"))
  ```
- SQL cells cannot run [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) (non-interactive execution). To chain notebooks,
  use Jupyter magic commands, such as `%run`, which executes another notebook in the same Python process. For more information, see
  [Jupyter magics](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-jupyter-magics).
- If the execution context (database and schema) or the query warehouse is not set when you run notebooks in Workspaces, the interactive datagrid for
  displaying table results in code cells and cell referencing may not function properly. For information about setting the execution context, see
  [Set the execution context](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run#label-nb-in-ws-edit-run-execution-context).
- The following values are not supported as column names:

  - CURRENT\_DATE
  - CURRENT\_TIME
  - CURRENT\_TIMESTAMP
  - LOCALTIME
  - LOCALTIMESTAMP
  - CURRENT\_USER
  - SESSION\_USER
  - SYSTEM\_USER

## Python files in Workspaces

For feature-specific limitations for Python files, see
[Limitations](/user-guide/ui-workspaces-python#label-py-in-ws-limitations) in
[Python files in Workspaces](/user-guide/ui-workspaces-python).

## Migrating from legacy notebooks

For information about migrating legacy notebooks to Workspaces, see [Migrating legacy notebooks to Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-migrate).
