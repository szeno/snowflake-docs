# Jul 31, 2026: Compute monitoring and run observability for Notebooks in Workspaces

With this release, Snowflake Notebooks in Workspaces gives you more visibility and control over the compute that runs your notebooks, both while
you develop interactively and when you troubleshoot scheduled runs.

While you develop a notebook, you can now see and control your compute without leaving the notebook:

- **Live utilization pills** in the notebook footer show CPU and memory use, color-coded to highlight caution and high-usage states.
- A **utilization details popup** breaks down memory use per file, lists required background processes, and offers in-context recommendations when
  resources run low.
- The **Service Details pane** provides ongoing monitoring across four tabs: Overview, Resource Monitoring, Logs, and Queries.

For more information, see [Monitor compute for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-monitor-compute).

This release also improves observability for scheduled, non-interactive runs. When a run fails, Snowflake now reports a categorized reason that
distinguishes system errors from user errors, so failures are easier to diagnose. For more information, see
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).
