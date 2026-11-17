# Using a runtime

Choose the Latest runtime while you explore and develop. Pin a Stable runtime when you move a workload to production.

## Choose Latest or Stable

| Workload | Recommendation |
| --- | --- |
| Interactive, open-ended analysis | Use Latest to get new notebook behavior, package updates, and performance improvements as they are released. |
| A pipeline that you plan to schedule | If you want your scheduled notebook to automatically receive minor runtime version updates, use the “Latest” option. When a new major version is released, the last minor release of the previous major version becomes Stable and your work remains on that version. |
| Fully locked production | Pair a Stable runtime with `requirements.txt` and Artifact Repository, or use a [custom runtime image](/developer-guide/snowflake-ml/custom-runtime-images). |

Expand

Show lessSee more

## Specify a runtime in the Notebooks UI

In Snowsight, when you create a notebook service in a Workspace, select a runtime from the version list. The UI shows
the support phase and the major and minor version. For example, the list might include **Latest (3.0)** and
**Stable (2.10)**. Latest is the default.

To change the runtime for an existing service:

1. Open the connection dropdown.
2. Select the pencil icon for the current service.
3. In the **Edit service** dialog, select a different **Runtime version**.
4. Select **Save and restart**.

Changing the runtime restarts the service.

End of Support versions aren’t shown for new notebooks. Existing notebooks already on an End of Support version
continue to run until the version reaches End of Life.

## Specify a runtime in SQL

Code Bundles use version labels of the form `V<major>-<CPU|GPU>-PY<python-version>`. For example, use `V3-CPU-PY3.12`
or `V3-GPU-PY3.12` to pin a workload to the 3.x major version and Python 3.12.

Confirm the exact labels in [Snowflake Container Runtime release notes](/developer-guide/container-runtime/release-notes)
for the version that you want to pin.

### Code Bundles

Note

Notebook Project Objects have been renamed to Code Bundles. Read more in
[Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

Specify a runtime with `compute_options.runtime_version` in the Code Bundle specification. The following example runs
`main.py` on the CPU runtime for major version 3 and Python 3.12:

Copy code

```
EXECUTE CODE BUNDLE my_bundle ENTRYPOINT = 'main.py'
WITH SPECIFICATION
$$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  compute_options:
    compute_pool: system_compute_pool_cpu
    query_warehouse: my_database.my_schema.my_warehouse
    runtime_version: 'V3-CPU-PY3.12'
  properties:
    requirements-file: requirements.txt
$$;
```

A compute pool is required for Container Runtime. The warehouse runs SQL and Snowpark pushdown compute. Python runs
on the compute pool.

Existing SQL that uses `EXECUTE NOTEBOOK PROJECT` still works. Set `RUNTIME` to the same version labels:

Copy code

```
EXECUTE NOTEBOOK PROJECT my_db.my_schema.my_project
  MAIN_FILE = 'notebook.ipynb'
  COMPUTE_POOL = 'system_compute_pool_cpu'
  QUERY_WAREHOUSE = 'my_wh'
  RUNTIME = 'V3-CPU-PY3.12';
```

### Map UI labels to SQL labels

| UI label | `RUNTIME` or `compute_options.runtime_version` |
| --- | --- |
| Latest (3.0), CPU | `V3-CPU-PY3.12` |
| Latest (3.0), GPU | `V3-GPU-PY3.12` |
| Stable (2.10), CPU | `V2-CPU-PY3.12` |

Expand

Show lessSee more

When a new major version is released, new notebooks that use the Latest alias move to the new major version. A
versioned label such as `V3-CPU-PY3.12` stays on that major version after the next major version is released.

## Specify a runtime for an ML Job

Specify a runtime with the `runtime_environment` argument on the job or `@remote` decorator. If you omit this argument,
the job uses Latest.

Copy code

```
from snowflake.ml import jobs

@jobs.remote(
    "MY_COMPUTE_POOL",
    stage_name="payload_stage",
    runtime_environment="3.0",
)
def train():
    ...
```

ML Jobs use the full Container Runtime release number, not the SQL version label. Confirm the exact release number in
[Snowflake Container Runtime release notes](/developer-guide/container-runtime/release-notes).

## Change the runtime for a scheduled notebook

A scheduled notebook runs as a Snowflake task against a Code Bundle. That run uses the runtime stored on
the schedule (the task definition or the Code Bundle specification), not the runtime of the interactive
notebook service.

Changing the runtime on **Edit service** updates only the interactive service. To move a scheduled notebook
to Latest or Stable, update the schedule.

### From Workspaces

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Open the notebook that has the schedule.
3. At the top of the notebook editor, select **Scheduled runs**.
4. Next to the schedule, select the ellipsis [![sf options button](/static/images/snowsight/icons/horizontal-options.png)](/static/images/snowsight/icons/horizontal-options.png), then **Delete**.
5. Select **Scheduled runs** again, then **Create Schedule**.
6. Keep the existing **Task name**, **Owner role**, **Location**, and **Frequency** unless you intend to
   change them.
7. Under **Advanced settings**, for **Runtime version**, select the runtime to use (for example,
   **Latest (3.0)** or **Stable (2.10)**). Match **Runtime variant** (CPU or GPU) and **Python version**
   to the new image.
8. Review the other advanced settings (compute pool, query warehouse, external access integrations), then
   select **Create**.

The new schedule uses the selected runtime on the next run. For the fields on this dialog, see
[Scheduling workflows by scenario](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios).

### From the Tasks UI

Use this path to change `runtime_version` without deleting the schedule.

Find the task:

1. In the navigation menu, select **Catalog** » **Explorer**.
2. Open the database and schema where the schedule was created (the **Location** on the original
   schedule).
3. Select **Tasks**, then select the task. Scheduled notebooks often use a name like
   `{notebook-name}_task_#`.

You can also open the notebook in Workspaces, select **Scheduled runs**, then **Open run history**, and
use the **Tasks** list for that Code Bundle.

Edit the runtime:

1. On the task, select the **…** actions button, then **Edit**.
2. In the **Task Definition**, find `compute_options.runtime_version` in the `EXECUTE CODE BUNDLE`
   `WITH SPECIFICATION` clause.
3. Set the label for the runtime you want. For example, use `V3-CPU-PY3.12` for Latest on CPU with
   Python 3.12, or `V2-CPU-PY3.12` for Stable 2.10. See
   [Map UI labels to SQL labels](#label-container-runtime-map-ui-sql).
4. Save the task.

Snowsight suspends the task while you edit it and resumes it when you finish. The next scheduled run uses
the updated runtime. You need the `OWNERSHIP` privilege on the task. For the Edit control, see
[View tasks and task graphs in Snowsight](/user-guide/ui-snowsight-tasks).

To change the same definition in SQL, replace the task and keep the existing `SCHEDULE`. For the
specification shape, see [Specify a runtime in SQL](#label-container-runtime-specify-sql).

Copy code

```
CREATE OR REPLACE TASK my_db.my_schema.my_notebook_task
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
AS
  EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
    ENTRYPOINT = 'notebook.ipynb'
    WITH SPECIFICATION
    $$
    bundle:
      type: custom
      compute_type: compute_pool
      language: python
      compute_options:
        compute_pool: system_compute_pool_cpu
        query_warehouse: my_wh
        runtime_version: 'V3-CPU-PY3.12'
    $$;
```

If the schedule uses `EXECUTE NOTEBOOK PROJECT`, set `RUNTIME` to the same label:

Copy code

```
CREATE OR REPLACE TASK my_db.my_schema.my_notebook_task
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
AS
  EXECUTE NOTEBOOK PROJECT my_db.my_schema.my_project
    MAIN_FILE = 'notebook.ipynb'
    COMPUTE_POOL = 'system_compute_pool_cpu'
    QUERY_WAREHOUSE = 'my_wh'
    RUNTIME = 'V3-CPU-PY3.12';
```

## After End of Support and End of Life

When a version reaches End of Support, existing notebooks and jobs on that runtime continue to start, but you can’t
select the version for new notebooks or jobs. Plan to move to Latest or a remaining Stable version.

When a version reaches End of Life, its image is removed and services that use it don’t start. Before the End of Life
date, update `RUNTIME` for a Notebook Project, `compute_options.runtime_version` for a Code Bundle, the runtime in
Notebook settings, or the runtime stored on a scheduled notebook task. For scheduled notebooks, see
[Change the runtime for a scheduled notebook](#label-container-runtime-upgrade-scheduled). For End of Support and End of Life dates, see
[Snowflake Container Runtime release notes](/developer-guide/container-runtime/release-notes).
