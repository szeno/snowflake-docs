description:
:   How do you get the code?

# Snowpark Migration Accelerator: Code Extraction

The Snowpark Migration Accelerator (SMA) processes all files within a specified directory. While it creates an inventory of every file, it specifically analyzes files with certain extensions to identify Spark API references.

There are several ways to add files to this directory.

Place all your relevant code files into a single directory before proceeding with the migration.

To extract notebooks from your existing environment (such as Databricks), you can use an extraction script to help with the migration process.

## Extraction Scripts

Snowflake provides publicly available extraction scripts that you can find on the [Snowflake Labs GitHub page](https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main). For Spark migrations, these scripts support various platforms.

### Databricks

For Jupyter (.ipynb) or Databricks (.dbc) notebooks that run in Databricks, you can directly place them in a directory for SMA analysis without any extraction. To learn how to export your Databricks notebook files, visit the Databricks documentation here: <https://docs.databricks.com/en/notebooks/notebook-export-import.html#export-notebooks>.

For an alternative approach, you can follow the instructions and use the scripts available in the Databricks folder of the SC.DDLExportScripts repository:
<https://github.com/Snowflake-Labs/SC.DDLExportScripts/tree/main/Databricks>

Additional information about data extraction will be provided soon.
