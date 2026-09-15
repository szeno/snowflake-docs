# Snowflake AIM Agent for Data Warehouses - Assessment

This topic helps you use the Snowflake AIM Agent for Data Warehouses to assess the source code to be migrated to the target Snowflake database.

The Snowflake AIM Agent for Data Warehouses will analyze the source database code and generate an html report.
It invokes a structured, multi-dimensional analysis of the source database code and generates a detailed actionable report.
The generated report helps create a clear, dependency-aware migration plan by identifying potential road blocks and risks associated with the migration.

Note

Snowflake AIM Agent for Data Warehouses currently supports Assessment for SQL Server, Redshift, Teradata and Oracle database platforms. For SAS assessment, see [SAS Migration](/migrations/aim-for-datawarehouses/sas-migration).

## Core functionality of Assessment

Assessment is done by

- Categorizing the source database objects
- Evaluating the conversion complexity of the source database code
- Establishing a logical migration sequence

The agent then generates a unified comprehensive report in an `html` format for you to review.

## Running an Assessment

When you start a new migration project, the Snowflake AIM Agent for Data Warehouses will run an Assessment for you as part of initial setup.
When the html report is ready, the agent will open it in your browser for you to review

## Output of Assessment

On completion of the Assessment, you will see an interactive report that allows you to view objects and apply filters based on the object status. You can export the object lists into `csv` files.
The four sections of the unified report consist of:

- [Overview](#label-overview)
- [Exclusion Report](#label-exclusion-report)
- [Dynamic SQL Report](#label-dynamic-sql-report)
- [Waves Report](#label-waves-report)
- [SSIS Package Analysis](#label-ssis-package-analysis)

Each section of this report covers the following critical aspects of risk management during the migration process.

1. **Identifying migration scope**: The Exclusion report helps identify deprecated or unused objects that would have no impact if they were not migrated, preventing unnecessary migration efforts.
2. **Targeting code conversion pain points**: The Dynamic SQL report helps target SQL code containing dynamic SQL statements, which are often the most complex to convert and need to be evaluated for complexity.
3. **Establishing a migration sequence**: The Waves report helps organize the objects into logical execution groups called “waves”, ensuring that all prerequisites for **Wave Two** are fully converted and deployed during **Wave One**. This structured approach guarantees “bottom-up” deployment, eliminating the risk of “missing dependency” errors that can stall complex migration projects.
4. **Replicating the exact workflow of SSIS packages**: The SSIS package analysis report helps classify SSIS packages (for SQL Server Integration Services) into the categories of ingestion, transformation, and configuration. It also includes an assessment of the complexity of the package, and Directed Acyclic Graphs (DAGs) reflecting workflows inside the packages.

### Overview

This section contains a summarized view of the assessment results for the migration workload. It includes the total workload inventory, anticipated manual effort, and quick access tiles to the detailed exclusion report, dynamic SQL report, waves report and SSIS report. Select any tile to view the detailed reports. These reports can also be accessed from the left navigation bar.

### Exclusion report

This section contains a list of objects that can be potentially excluded from migration, based on additional review.
The Snowflake AIM Agent for Data Warehouses intelligently flags deprecated files, temporary staging objects, test objects, and duplicate objects found in source database code. These objects can be excluded after further review with the subject matter experts (SMEs) before the code conversion kickoff.

Under the **Detailed Objects Analysis** section, you will find a list of objects that are flagged as:

- Temporary/Staging
- Deprecated/Legacy
- Testing objects
- Duplicate objects

Excluding these objects from the migration may help in reducing the migration effort and time.

### Dynamic SQL report

This section contains a list of all source code files that were found to contain dynamic SQL. Select any file to view the dynamic SQL code. The detailed view shows the sections of the SQL file containing dynamic SQL and the corresponding line numbers. Select **Complexity** to view the assessed migration complexity of the dynamic SQL code in the file.

### Waves report

By default, each wave contains 40 objects. The Snowflake AIM Agent for Data Warehouses analyzes the relationships between the code objects and ensures that all prerequisites for **Wave Two** are fully converted and deployed during **Wave One**. This structured approach guarantees “bottom-up” deployment, eliminating the risk of “missing dependency” errors.

When the Snowflake AIM Agent for Data Warehouses is preparring to run an Assessment, it will ask you for your preferences. You can have it customize the waves report by specifying the number of objects per wave, or changing the order of migration to align with business needs.

### SSIS report

The SSIS Report helps determine the feasibility and effort required to migrate data workloads consisting of SQL Server Integration Services (SSIS) packages to Snowflake. The core components of this report are:

1. **AI summary**: This section contains an overview of the migration readiness of the SSIS packages analyzed by the Snowflake AIM Agent for Data Warehouses. It consists of migration workload overview, source and destination data flows, connection managers, and an overview of tasks that contribute to the complexity of migration. The AI summary section is further subdivided into three parts:

   - **Recommended Migration Approach** containing details on methods of migration and the number of packages it can be applied to.
   - **Key risks** containing details on connectivity gaps, process dependencies on external services like email-based data delivery, manual scripting effort required rewrite custom scripts that cannot be converted automatically, compliance requirements (such as HIPAA, FERPA) that may require data masking and role-based access control (RBAC) implementation.
   - **Consolidation opportunities** containing suggestions for applying the same migration approach to similar packages.
2. **Key metrics**: This section contains a quantified technical footprint of the source SSIS environment. The total component counts, number of transformation pipelines required for data flows, number of workflow and orchestration tasks for control flows and the number of databases with corresponding file connections are all summarized here.
3. **Package classification**: This section contains charts to show the classification of package categories and complexity. The interactive table contains a complete list of packages sorted by package name. Enter the package name to search on a specific package. Select options from the **classification** and **complexity** dropdowns to view a filtered list of packages. Select the package name in the list to view the complete AI analysis for the package. Select **Control Flow DAG** to open the Directed Acyclic Graph (DAG) depicting the workflow inside the package.
4. **Component conversion breakdown**: This section shows the number of SSIS package components that can be automatically converted to Snowflake and the number of components that require manual intervention.
