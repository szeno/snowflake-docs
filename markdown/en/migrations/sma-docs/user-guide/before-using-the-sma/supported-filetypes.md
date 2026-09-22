description:
:   What will the SMA accept as an input?

# Snowpark Migration Accelerator: Supported Filetypes

The Snowpark Migration Accelerator (SMA) scans files in your selected source directory during project creation. While some files are [excluded](/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes) based on their type, SMA generates a summary report showing the count of files by extension.

The SMA tool searches for specific file extensions when analyzing references to the Spark API, SQL Statements, and other elements that contribute to the [Readiness Scores](/migrations/sma-docs/user-guide/assessment/readiness-scores). The tool can analyze both code files and notebooks located in any directory or subdirectory of your project.

## Code Files

The Snowpark Migration Accelerator scans the following file types to identify references to Spark API and other third-party APIs:

- Files with the extension .scala
- Files with the extension .py
- Files with the extension .python

SQL statements written in Spark SQL or HiveQL can be detected in the following file types:

- SQL files with the extension .sql
- Hive Query Language files with the extension .hql

## Notebooks

Both the Spark Scala and PySpark parsers in the Snowpark Migration Accelerator (SMA) automatically scan and process Jupyter Notebook files and exported Databricks files when they are present in the source code directory.

- Jupyter Notebook files (`*.ipynb`)
- Databricks Notebook files (`*.dbc`)

The SMA will analyze notebook files to identify:

- References to the Spark API
- References to other third-party APIs
- SQL statements

The analysis is performed based on the cell type within each notebook. Notebooks can contain a mix of SQL, Python, and Scala cells. The SMA will create an [inventory of all cell types](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories) in its output report.

### Excluded Files and Folders

By default, certain files and folders are excluded from scanning. These exclusions primarily consist of project configuration files and their associated directories.

#### Folders type excluded from the scanning:

- Python package installer (pip) - A tool for installing Python packages
- Distribution packages (dist) - A directory containing Python packages ready for distribution
- Virtual environment (venv) - An isolated Python environment for managing project dependencies
- Site-packages - A directory where Python packages are installed for use across the system

#### Files type excluded from the scanning:

- input.wsp - Workspace input file
- .DS\_Store - macOS system file that stores custom folder attributes
- build.gradle - Gradle build configuration file
- build.sbt - Scala Build Tool configuration file
- pom.xml - Maven Project Object Model configuration file
- storage.lck - Storage lock file
