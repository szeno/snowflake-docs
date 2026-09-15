# Feb 05, 2026: Notebooks in Workspaces (*General Availability*)

Snowflake Notebooks in Workspaces is now generally available. This new notebook experience provides
a fully-managed, end-to-end environment for data science and machine learning development on Snowflake data, combining the familiar Jupyter
notebook interface with enterprise-grade compute, governance, and collaboration capabilities.

Notebooks in Workspaces runs on a Container Runtime powered by Snowpark Container Services, offering preconfigured containers optimized for AI/ML workloads with
access to CPUs and GPUs, parallel data loading, and distributed training APIs for popular ML packages.

## Key features

**Integration with Workspaces**

- Notebooks are files in Workspaces, enabling easy file management and organization.
- Git integration provides version control and collaboration across development environments.

**Updates to compute and cost management**

- CPU or GPU compute pools match your workload requirements.
- Shared container service connections reduce start-up time and improve resource utilization.
- Background kernel persistence ensures uninterrupted execution of long-running processes.
- Simplified idle time configuration prevents unused compute resources from running indefinitely.
- Service-level External Access Integration (EAI) management applies to all notebooks in the workspace.

**Jupyter compatibility**

- Standard Jupyter magic commands for familiar development experience.
- Pre-installed data science and machine learning packages.
- Install additional packages via `pip`, PyPI, or file upload.

**Enhanced editing experience**

- Bidirectional SQL and Python cell referencing for seamless language switching.
- Interactive datagrid and automated chart builder for data visualization.
- Enhanced minimap with cell status tracking and table of contents.

For details, see [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview).
