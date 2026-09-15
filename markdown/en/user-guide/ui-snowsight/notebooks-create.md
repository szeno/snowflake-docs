# Create a notebook

This topic describes how to create a Snowflake notebook on Warehouse Runtime. You can also create a notebook on Container Runtime. For details,
see [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).

Snowflake Notebooks provide an interactive, cell-based development environment within Snowsight. They enable you to work with Snowflake data
using SQL and Python in a single interface, making it easier to build and iterate on workflows for data exploration, transformation, and machine
learning.

You can access notebooks through [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), where you can [Create a new notebook](#label-notebooks-create) or [Open an existing notebook](#label-notebooks-existing-nb). You
can also create a notebook using SQL. For more information, see [CREATE NOTEBOOK](/sql-reference/sql/create-notebook).

## Prerequisites

- You have [set up and enabled notebooks](/user-guide/ui-snowsight/notebooks-setup#label-notebooks-setup).
- You are using a role with the [required privileges](/user-guide/ui-snowsight/notebooks-setup#label-notebooks-create-resources-grant-privileges).

## Runtimes

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When creating a notebook using the Warehouse Runtime, you specify a name, location, and warehouse. In this preview, you can also select
a specific pre-configured runtime environment for your notebook. Using a Snowflake default runtime environment ensures that your notebook runs
in a consistent setting, which supports reproducible results. This setup does not require initial configuration and is ready to use immediately.

The Snowflake Warehouse Runtime environment consists of the following components:

| Snowflake Warehouse Runtime version | Python runtime | Streamlit version |
| --- | --- | --- |
| 1.0 | 3.9 | 1.39.1 |
| 2.0 | 3.10 | 1.39.1 |

Expand

Show lessSee more

All new notebooks are defaulted to the Python 3.9 runtime (Warehouse Runtime 1.0).

Note

If you install packages on top of the Snowflake runtime, Snowflake can no longer guarantee compatibility across your environment.

## Create a new notebook

You can create a new notebook by selecting **+ Notebook**, or you can import a file with the `*.ipynb` extension. This could be
a notebook file created from an application outside of Snowflake.

**To create a new notebook,** follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. Select **+ Notebook**.
4. Enter a name for your notebook. Snowflake preserves the exact casing of the notebook name as entered, including names that contain spaces.
   Notebook names are case-sensitive.
5. Select a **Notebook location**. This is the database and schema in which to store your notebook. These cannot be changed after you
   create the notebook.

   Note

   The **Notebook location** list might not show databases that were created after you opened the **Create Notebook** dialog. If you can’t
   find your recently created database, schema, or warehouse, reload your browser window.

   Querying data in the notebook is not restricted to this location. In the notebook, you can query data in any location you have access to.
   To specify the location, run [USE WAREHOUSE](/sql-reference/sql/use-warehouse) and [USE SCHEMA](/sql-reference/sql/use-schema).
6. Select **Run on warehouse** as your Python environment. For details on what is included in each runtime, see [Legacy Notebook runtimes](/user-guide/ui-snowsight/notebooks#label-notebook-runtime-descriptions).

   For details on Container Runtime, see [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).
7. Optional: Select a **Query warehouse** to run any SQL and Snowpark queries issued by the notebook.
8. Select a **Notebook warehouse** to run notebook-specific tasks. Snowflake recommends that you use [SYSTEM$STREAMLIT\_NOTEBOOK\_WH](/user-guide/warehouses-overview#label-default-warehouse),
   a Snowflake-managed warehouse that is provisioned in each account for running notebooks.

   Note

   By default, notebooks are suspended after a period of inactivity. The default idle timeout depends on the runtime:

   - **Warehouse Runtime notebooks:** 30 minutes (1,800 seconds) of inactivity
   - **Container Runtime notebooks:** 60 minutes (3,600 seconds) of inactivity

   You can set the idle timeout to a maximum of 72 hours (259,200 seconds). To update the idle timeout setting, use either the CREATE NOTEBOOK
   or ALTER NOTEBOOK commands to set the value of the IDLE\_AUTO\_SHUTDOWN\_TIME\_SECONDS property.

   You can change the idle timeout setting after creation from the notebook settings. For more information, see [Idle time and reconnection](/user-guide/ui-snowsight/notebooks-setup#label-notebooks-idle-time-property).
9. Select **Create** to create and open your notebook.

**To create a new notebook from an existing file,** follow these steps:

1. Select the down arrow next to **+ Notebook** and then select **Import .ipynb file**.
2. Open the file to import, such as a notebook file that was created from an application outside of Snowflake.

   Note

   If your notebook imports Python packages, you must add the packages to the notebook before you can run the imported notebook. See
   [Import Python packages to use in notebooks](/user-guide/ui-snowsight/notebooks-import-packages). If the package you use in your imported notebook is not available, your code might not run. For
   information about adding cells, see [Develop and run code in Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-develop-run).

## Create a notebook using SQL

You can create a notebook using the [CREATE NOTEBOOK](/sql-reference/sql/create-notebook) command. This command lets you define the notebook’s location, main
file, and version source programmatically. However, when you create a notebook using SQL, the notebook does not automatically include a live
version. A live version is required in order to run the notebook using the [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) command.

If you attempt to run a notebook that does not have a live version, or if the notebook was dropped and recreated, you may see the following
error:

```
Live version is not found.
```

To resolve this, add a live version to the notebook before executing it, as shown in the following example:

Copy code

```
ALTER NOTEBOOK DB_NAME.SCHEMA_NAME.NOTEBOOK_NAME ADD LIVE VERSION FROM LAST;
```

- `DB_NAME` is the name of the database that contains the notebook
- `SCHEMA_NAME` is the name of the schema that contains the notebook
- `NOTEBOOK_NAME` is the name of the notebook

## Create a notebook from a Git repository

You can sync your notebook development with a Git repository. Then you can create Snowflake Notebooks from notebooks in that Git repository.

To create a notebook from a file in Git, see [Create a notebook from a file in a Git repository](/user-guide/ui-snowsight/notebooks-snowgit#label-snowsight-notebooks-git-create).

## Duplicate an existing notebook

You can duplicate existing Snowflake Notebooks. Duplicating notebooks may be useful if you want to, for example, test out some code changes
without altering the original notebook version.

When you duplicate a notebook, the copied notebook is created with the same role and warehouse as the original notebook, and is contained
in the same database and schema as the original notebook. Because of this, you cannot duplicate a notebook to move it to a different
database and schema, or to change ownership.

To duplicate a notebook, complete the following steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. Open the notebook that you want to duplicate.
4. Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) menu, then select **Duplicate**.
5. (Optional) Enter a name for the duplicate notebook, then select **Duplicate**.
6. In the confirmation dialog, select **Close** to return to the original notebook, or **Open notebook** to open the duplicate
   notebook.

## Open an existing notebook

To open an existing notebook, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.

   Note

   Recently used notebooks also appear in Snowsight. Under **Recently viewed**, select **Notebooks**.
3. Review the list of notebooks.

   You can see all notebooks owned by your active role or owned by a role inherited by your active role. Each notebook displays the following information:

   - **Title**: The title of the notebook
   - **Viewed**: The last time the notebook was viewed
   - **Updated**: The last time the notebook was executed
   - **Environment**: The runtime environment for the notebook (Container Runtime or Warehouse Runtime)
   - **Location**: The database and schema locations for the notebook
   - **Owner**: The owner of the notebook
4. Select a notebook to open it for editing.

   For details about editing notebooks, see [Develop and run code in Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-develop-run).

When you open a notebook, you can see cached results from the last time you ran any cells in the notebook. The notebook is in the
**Not connected** state by default, but if you select that state or run any cell, your notebook connects to your virtual warehouse.
