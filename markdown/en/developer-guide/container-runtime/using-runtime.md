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

## After End of Support and End of Life

When a version reaches End of Support, existing notebooks and jobs on that runtime continue to start, but you can’t
select the version for new notebooks or jobs. Plan to move to Latest or a remaining Stable version.

When a version reaches End of Life, its image is removed and services that use it don’t start. Before the End of Life
date, update `RUNTIME` for a Notebook Project, `compute_options.runtime_version` for a Code Bundle, or the runtime in
Notebook settings. For End of Support and End of Life dates, see
[Snowflake Container Runtime release notes](/developer-guide/container-runtime/release-notes).
