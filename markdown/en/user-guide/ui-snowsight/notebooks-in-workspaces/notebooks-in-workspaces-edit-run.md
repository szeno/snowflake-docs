# Editing and running Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Note

This topic describes editing and running `.ipynb` notebooks. To run `.py` files interactively in Workspaces, see
[Python files in Workspaces](/user-guide/ui-workspaces-python).

## Set the execution context

Notebooks in Workspaces do not automatically set a database or schema. To query data, you must define the execution context in a cell using the
following SQL commands:

Copy code

```
USE DATABASE <database>;
USE SCHEMA <schema>;
```

To ensure notebooks run consistently across environments and clients, use fully qualified names for tables and other objects. For example:

Copy code

```
-- Query data objects using a fully qualified name
SELECT * FROM TABLE <database_name.schema_name.table_name>;

-- Create a table using a fully qualified name
WITH filtered_events AS (
    SELECT
        user_id,
        event_type,
        event_timestamp
    FROM raw_events
    WHERE event_timestamp >= '2025-01-01'
)
CREATE OR REPLACE TABLE <database_name.schema_name.table_name> AS
SELECT *
FROM filtered_events;
```

## Use the role and warehouse picker

You can set the active role and warehouse for your notebook.

SnowsightSQL

Use the picker at the top left of the Notebooks editor:

![Role and warehouse picker](/static/images/workspaces/nb-warehouse-picker.png)

Run the following SQL commands:

Copy code

```
USE ROLE <role>;
USE WAREHOUSE <warehouse>;
```

The query warehouse is used to run SQL queries and Snowpark pushdown compute invoked by the notebook. It is also used to render the interactive
datagrid, but there is no credit charge for this operation.

To learn more about credit usage, see [Setting up compute](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-compute-setup).

## Create a Snowpark session

Snowpark is a Snowflake developer framework that lets you build data pipelines, transformations, and machine learning logic directly inside
Snowflake without moving data out of the platform. It provides APIs that operate on Snowflake data as DataFrames, pushing computation down to
Snowflake’s engine for scalability, performance, and security.

To use [Snowpark Python APIs](/developer-guide/snowpark/python/index) in Notebooks, first create a Snowpark session in a Python cell:

Copy code

```
from snowflake.snowpark.context import get_active_session
session = get_active_session()
```

## Run cells

There are five supported execution options:

- Run all cells
- Run one single cell
- Run current cell and all descendant cells
- Run current cell and all above cells (via the cell’s ellipsis menu)
- Run current cell and all below cells (via the cell’s ellipsis menu)

Run current cell and all descendant cells is especially helpful when you have complex variable referencing throughout
your notebook. After updating a variable in a cell, use this option to automatically rerun all cells that reuse the
variable.

### Cancel cell execution

Use **Stop** at the top of the notebook or **Cancel execution** in a cell.

Both actions stop the currently executing cell and any queued cells triggered by **Run all**.

Note

The **Run all** button may temporarily change to **Stop** when the notebook is connecting or reconnecting to the service.

### Delete a cell

Deleting a cell takes effect immediately without a confirmation dialog. To undo a deletion, press **Ctrl+Z** (Windows/Linux)
or **Cmd+Z** (macOS). The undo history retains up to 50 actions per session.

## Cell names

You can assign names to cells to make navigation easier and provide contextual labels.

If an imported `.ipynb` file already contains name or title metadata, those values are used automatically.

## Cell referencing

Bidirectional SQL to Python cell referencing allows you to reuse results and variables across cells in either language, enabling seamless transitions
between SQL and Python workflows.

You can hover over the result tooltip to see the DataFrame name you can use to reference the result in Python and SQL.

![Cell referencing](/static/images/snowsight/workspaces/nb-in-ws-dataframe-name.png)

### Referencing SQL cell results

Each SQL cell exposes its result as a DataFrame pointer named `dataframe_x`. You can edit the name by double-clicking
on it.

In Runtime 2.6 and above, this is a Snowpark DataFrame to improve memory usage and time to interactivity. In
Runtime 2.5 and below, this is a pandas DataFrame.

- In SQL, reference it using double curly braces: `{{dataframe_x}}`.
- In Python, reference it directly as a DataFrame: `dataframe_x`.
- To convert a pandas DataFrame `pdf` to a Snowpark DataFrame, run:

  Copy code

  ```
  snow_df = session.create_dataframe(pdf)
  ```
- To convert a Snowpark DataFrame `snow_df` to a pandas DataFrame, run:

  Copy code

  ```
  pdf = snow_df.to_pandas()
  ```

### Referencing Python variables

To reference Python variables in SQL queries, wrap them in double curly braces. For example:

Copy code

```
SELECT * FROM {{uploaded_df}} WHERE "price" > 326;
```

DataFrame variables are also supported when referencing Python variables in SQL.

### Example workflow

**Python cell**

Copy code

```
import pandas as pd

uploaded_df = pd.read_csv("../data/diamonds.csv")
uploaded_df
```

**SQL cell referencing Python variable**

Copy code

```
SELECT * FROM {{uploaded_df}} WHERE "price" > 326;
```

**SQL cell referencing SQL cell results**

The result of a SQL cell provides a DataFrame pointer called `dataframe_1`. You can reference it in another SQL query:

Copy code

```
SELECT * FROM {{dataframe_1}} WHERE "carat" < 1.0
UNION ALL
SELECT * FROM {{dataframe_2}} WHERE "carat" >= 1.0;
```

## Interactive datagrid

The datagrid supports:

- Scrolling
- Search
- Filtering
- Sorting
- Chart creation without code

### Built-in chart builder

Provides a consistent user experience for data manipulation and visualization across editing surfaces in Workspaces.

## Minimap and cell status

The minimap generates a table of contents from Markdown headers and displays a comprehensive in-session status for each cell (running, succeeded,
failed, and modified).

## Global search and replace

You can search for keywords across all cells in the current notebook. If you’re editing a particular cell, press `esc` to exit the edit mode for that cell first.

To search keywords across all cells in the current notebook, do the following:

- To search for keywords, select **Search** in the minimap, or use the keyboard shortcut `CTRL` + `F`.

  Matching keywords in all cells are shown. Optionally, you can replace the search term with the desired value using **Replace next** or **Replace all**.

## Keyboard shortcuts

Notebooks in Workspaces support various keyboard shortcuts to help accelerate your development process.

You can also see the list of keyboard shortcuts by selecting the keyboard icon at the bottom right corner, and then
selecting **Keyboard shortcuts**.

| Task | macOS | Windows |
| --- | --- | --- |
| Run this cell only | `CMD` + `Return` | `CTRL` + `Enter` |
| Run cell and advance to next (unless Shift+Enter is your AI suggestion accept key) | `Shift` + `Return` | `Shift` + `Enter` |
| Run all cells | `CMD` + `Shift` + `Return` | `CTRL` + `Shift` + `Enter` |
| Run all cells with Container Runtime | `CMD` + `Option` + `Return` | `CTRL` + `Alt` + `Enter` |
| Stop all cells | `ii` | `ii` |
| Enter selected cell | `Return` | `Enter` |
| Exit selected cell | `Escape` | `Escape` |
| Go to next cell | `↓` or `J` | `↓` or `J` |
| Go to previous cell | `↑` or `K` | `↑` or `K` |
| Add a cell above the currently selected cell | `a` | `a` |
| Add a cell below the currently selected cell | `b` | `b` |
| Move cell up | `CTRL` + `Shift` + `↑` | `CTRL` + `Shift` + `↑` |
| Move cell down | `CTRL` + `Shift` + `↓` | `CTRL` + `Shift` + `↓` |
| Duplicate cell | `CTRL` + `D` | `CTRL` + `D` |
| Delete selected cell | `dd` or `Backspace` | `dd` or `Backspace` |
| Delete selected cell (no prompt) | `Shift+D`, `Shift+D` or `Shift` + `Backspace` | `Shift+D`, `Shift+D` or `Shift` + `Backspace` |
| Convert cell to Markdown | `m` | `m` |
| Convert cell to Python or SQL | `y` | `y` |
| Format query | `CMD` + `Shift` + `O` | `CTRL` + `Shift` + `O` |
| Comment out code | `CMD` + `/` | `CTRL` + `/` |
| Undo | `CMD` + `Z` | `CTRL` + `Z` |
| Redo | `CMD` + `Shift` + `Z` | `CTRL` + `Shift` + `Z` |

Expand

Show lessSee more

In addition, you can use the same keyboard shortcuts that you use for worksheets. See [Keyboard shortcuts](/user-guide/ui-snowsight/workspaces-working#label-workspaces-keyboard-shortcuts).

## Notebook kernel

The notebook kernel remains active as long as the notebook service is in the `RUNNING` state, allowing uninterrupted execution of critical,
long-running processes such as ML training and data engineering jobs.

Actions that do not affect kernel execution:

- Navigating to other pages
- Working elsewhere in Snowsight
- Closing your browser
- Shutting down your computer

You can shut down or restart the kernel using the **Connected** dropdown.

Note

Using **Shut down kernel** or **Restart kernel** will clear variables in memory but retain any user-installed packages. If you want a completely clean
environment with only the pre-installed packages, you must restart the service or create a new service and connect to it.

If the notebook service is suspended, the notebook kernel is also shut down. For more information, see [Setting up compute](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup#label-nb-in-ws-compute-setup).

## Cell output

- Cell outputs in a notebook in Workspaces (both private and shared workspaces) are accessible to the user who executed the notebook.
- Cell outputs are not saved to the `.ipynb` file. To export and share outputs, choose **Export as HTML**. For interactive sessions in
  Workspaces, **Export as HTML** can be accessed from the ellipsis menu in the top right of each notebook file. For scheduled notebooks, it can
  be accessed in each past execution’s result page.
- The exported HTML file has the following behaviors:
  - The collapsed state of each cell’s code and output is saved.
  - Tables and DataFrames are capped at 1,000 rows and default to the **Table** view. You can toggle to **Chart** and configure it in the HTML file.

## Jupyter magics

Notebooks in Workspaces run the IPython (Interactive Python) kernel and provide standard Jupyter cell and line magics. Run `%lsmagic` to view available magics.

For example, you can use the `%run` magic command to invoke another notebook:

- In a Python cell of `notebook_a`, call `%run path/to/notebook_b.ipynb`. This executes `notebook_b` in the same Python process as `notebook_a`.
- For variables and pandas DataFrames in `notebook_b` to render in `notebook_a` cell results, make sure to explicitly print them. For example:
  `print(var)` or `display(df)`.

## Developer tools

For information about the Variables Explorer, Terminal, Scratchpad, and Dependency graph, see
[Developer tools](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-developer-tools).
