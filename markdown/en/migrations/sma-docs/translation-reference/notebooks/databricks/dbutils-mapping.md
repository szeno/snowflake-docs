# Mapping for dbutils and sfutils

This document provides a reference mapping between Databricks `dbutils` utilities and their Snowflake `sfutils` equivalents. When migrating notebooks from Databricks to Snowflake using the Snowpark Migration Accelerator (SMA), these utility functions are automatically translated to their corresponding Snowflake implementations.

The `dbutils` library in Databricks provides a set of utility functions for working with files, notebooks, and widgets. In Snowflake, the equivalent functionality is provided through the `sfutils` library, which offers compatible methods designed to work seamlessly within the Snowflake environment.

## File System Utilities

The file system utilities allow you to interact with cloud storage and manage files. These functions enable common file operations such as copying, moving, listing, and deleting files.

| Databricks | Snowflake |
| --- | --- |
| dbutils.fs | sfutils.fs |
| dbutils.fs.cp | sfutils.fs.cp |
| dbutils.fs.head | sfutils.fs.head |
| dbutils.fs.ls | sfutils.fs.ls |
| dbutils.fs.mkdirs | sfutils.fs.mkdirs |
| dbutils.fs.mv | sfutils.fs.mv |
| dbutils.fs.put | sfutils.fs.put |
| dbutils.fs.rm | sfutils.fs.rm |

Expand

Show lessSee more

## Notebook Utilities

The notebook utilities provide functionality to run notebooks programmatically and control notebook execution flow. These are essential for orchestrating multi-notebook workflows and building modular data pipelines.

| Databricks | Snowflake |
| --- | --- |
| dbutils.notebook | sfutils.notebook |
| dbutils.notebook.run | sfutils.notebook.run |
| dbutils.notebook.exit | sfutils.notebook.exit |

Expand

Show lessSee more

## Widget Utilities

Widget utilities enable you to create interactive input controls in notebooks. These are useful for parameterizing notebooks and allowing users to provide input values at runtime without modifying the code.

| Databricks | Snowflake |
| --- | --- |
| dbutils.widgets | sfutils.widgets |
| dbutils.widgets.combobox | sfutils.widgets.combobox |
| dbutils.widgets.dropdown | sfutils.widgets.dropdown |
| dbutils.widgets.get | sfutils.widgets.get |
| dbutils.widgets.getAll | sfutils.widgets.getAll |
| dbutils.widgets.getArgument | sfutils.widgets.getArgument |
| dbutils.widgets.multiselect | sfutils.widgets.multiselect |
| dbutils.widgets.remove | sfutils.widgets.remove |
| dbutils.widgets.removeAll | sfutils.widgets.removeAll |
| dbutils.widgets.text | sfutils.widgets.text |

Expand

Show lessSee more

## Usage Notes

- All `dbutils` calls in your Databricks notebooks are automatically translated to their `sfutils` equivalents during the migration process.
- The function signatures and parameters remain consistent between the two implementations to ensure a smooth transition.
- If you encounter any unsupported functionality, refer to the Snowflake documentation for alternative approaches.
