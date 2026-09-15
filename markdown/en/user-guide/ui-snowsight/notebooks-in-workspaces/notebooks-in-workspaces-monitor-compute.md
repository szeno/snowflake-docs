# Monitor compute for Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## Overview

While you develop a notebook interactively, you can see and control the compute that runs your code without leaving the notebook. Live utilization
indicators, a detailed utilization popup, and the Service Details pane let you understand how your notebook service is using CPU and memory, review
logs and queries, and take action when resources run low.

These tools apply to the interactive notebook service that hosts your kernel. For observability of scheduled, non-interactive runs, see
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

## Compute utilization at a glance

The notebook footer shows live CPU and memory utilization pills for the connected notebook service. The pills update as your code runs so you can spot
resource pressure early. They’re color-coded to show the current state:

- **Default:** utilization is within a comfortable range.
- **Yellow (caution):** utilization is elevated. Consider reducing memory use or moving to a larger compute pool.
- **Red (high):** utilization is high and code might fail or the kernel might be stopped to free memory.

![Notebook footer showing color-coded CPU and memory utilization pills.](/static/images/snowsight/workspaces/notebook-utilization-pills.png)

## View utilization details

Select the utilization pills to open the utilization popup, which breaks down memory use for the connected service:

- **Per-file memory breakdown:** memory consumed by each notebook and Python file connected to the service, with color swatches to distinguish files.
- **Required background processes:** an expandable list of processes that support the service, such as Ray, service infrastructure, and the terminal.

When the service is in the caution or high zone, the popup also shows in-context recommendations:

- **Inspect with CoCo:** open Cortex Code to investigate resource use.
- **Create a service on a larger compute pool:** move to more capable compute.
- **Restart the current kernel:** clear in-memory state for the active kernel.
- **Manage all running kernels:** review and stop kernels across connected files.
- **View service details:** open the Service Details pane for deeper monitoring.

![Utilization details popup showing per-file memory breakdown and recommendations.](/static/images/snowsight/workspaces/notebook-utilization-popup.png)

## Use the Service Details pane

The Service Details pane provides detailed, ongoing monitoring for the notebook service. You can open it as an inline pane at the bottom of the
workspace or expand it to full screen. The pane organizes information into the following tabs.

### Overview

The Overview tab summarizes the current state and configuration of the notebook service:

- Status
- Compute pool
- Runtime version
- Idle timeout
- Enabled external access integrations (EAIs)
- Python version
- Uptime
- Connected files

### Resource monitoring

The Resource Monitoring tab shows how the service uses compute over time:

- **CPU and memory timelines** with caution and warning thresholds so you can see trends and spikes.
- **Per-file breakdown** of resource use across connected notebooks and Python files.
- **Kill any kernel** to free resources held by a specific file.
- **Time-range filters** of 10 minutes, 1 hour, 6 hours, or 24 hours.
- **File filters** to focus on specific connected files.
- **Toggle background processes** to include or exclude supporting processes in the view.
- **Inspect with CoCo** to investigate resource use in Cortex Code.

![Resource Monitoring tab showing CPU and memory timelines with threshold markers.](/static/images/snowsight/workspaces/notebook-resource-monitoring.png)

### Logs

The Logs tab shows log entries emitted by the notebook service. You can filter by level, instance, and source. Each entry shows a timestamp,
severity, and source, and you can expand an entry to view the full message.

For log collection setup, event tables, and querying logs with Snowflake Trail, see
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging).

### Queries

The Queries tab shows the queries that have run in the notebook service, so you can correlate query activity with resource use.

Note

The Queries tab requires Snowflake Container Runtime 2.8 or later. For more information on runtime versions, see
[Managing packages and runtime](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-packages-runtime).
