# Develop and run code in Snowflake Notebooks

This topic describes how to write and run SQL, Python, and Markdown code in Snowflake Notebooks.

## Notebook cell basics

This section introduces some basic cell operations. When you [create a notebook](/user-guide/ui-snowsight/notebooks-create#label-notebooks-create), three example cells are
displayed. You can modify those cells or add new ones.

### Create a new cell

Snowflake Notebooks support three types of cells: SQL, Python, and Markdown. To create a new cell, you can either hover over an existing cell or
scroll to the bottom of the notebook, then select one of the buttons for the cell type you want to add.

> ![Add new cell buttons at the bottom of the notebook.](/static/images/snowsight/notebooks/snowsight-ui-add-cell-bottom.png)

Change the language of an existing cell by using one of the following methods:

- Select the language dropdown menu and then select a different language.

  ![Use the cell language drop down to change the cell language.](/static/images/snowsight/notebooks/snowsight-ui-change-cell.png)
- Use [keyboard shortcuts](#label-notebooks-keyboard-shortcuts).

### Edit a cell

To prevent editing conflicts, only one user can edit a cell at a time. If another user attempts to edit an active cell, a notification will be
displayed. The cell will become available for editing after 60 seconds of inactivity.

### Move cells

You can move a cell either by dragging and dropping the cell using your mouse or by using the actions menu:

1. (Option 1) Hover your mouse over the existing cell you want to move. Select the [![Notebooks drag and drop icon](/static/images/snowsight/notebooks/notebooks-drag-drop.png)](/static/images/snowsight/notebooks/notebooks-drag-drop.png) (drag and drop) icon on the left side of the cell
   and move the cell to its new location.
2. (Option 2) Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (actions) menu. Then select the appropriate action.

Note

To just move the focus between cells, use the `Up` and `Down` arrows.

### Delete a cell

To delete a cell, complete the following steps in a notebook:

1. Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) menu.
2. Select **Delete**.
3. Select **Delete** again to confirm.

You can also use a [keyboard shortcut](#label-notebooks-keyboard-shortcuts) to delete a cell.

For considerations when using Python and SQL cells, see [Considerations for running notebooks](#label-notebooks-considerations-cells).

## Run cells in Snowflake Notebooks

To run Python and SQL cells in Snowflake Notebooks, you can:

- **Run a single cell:** Choose this option when making frequent code updates.

  - Press `CMD` + `return` on a Mac keyboard, or `CTRL` + `Enter` on a Windows keyboard.
  - Select [![Run this cell only](/static/images/snowsight/icons/notebooks-run.png)](/static/images/snowsight/icons/notebooks-run.png), or **Run this cell only**.
- **Run all cells in a notebook in sequential order:** Choose this option before presenting or sharing a notebook to ensure that the recipients
  see the most current information. This option executes all SQL and Python code cells in the notebook from top to bottom. If an error occurs
  in any cell, execution will halt and subsequent cells will not run. This behavior also applies to scheduled notebooks. For example, if you
  run a notebook that has 10 cells, and in cell 2 there is a SQL syntax error, the notebook will stop running after cell 2.

  - Press `CMD` + `shift` + `return` on a Mac keyboard, or `CTRL` + `Shift` + `Enter` on a Windows keyboard.
  - Select **Run all**.
- **Run a cell and advance to the next cell:** Choose this option to run a cell and move on to the next cell more quickly.

  - Press `shift` + `return` on a Mac keyboard, or `Shift` + `Enter` on a Windows keyboard.
  - Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose **Run cell and advance**.
- **Run all above**: Choose this option when running a cell that references the results of earlier cells.

  - Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose **Run all above**.
- **Run all below**: Choose this option when running a cell that later cells depend on. This option runs the current cell and all following
  cells.

  - Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose **Run all below**.

When one cell is running, other run requests are queued and will be executed once the actively running cell finishes.

### Collapse and expand cells

You can control how much of the notebook is visible by selecting one of the cell display options at the top of the notebook:

1. Select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) menu.
2. Select **Show/hide all** and choose the appropriate option:
   - **Show all:** Displays both code and results for each cell.
   - **Show code only:** Hides the results and displays only the code cells.
   - **Show results only:** Hides the code and displays only the output.
   - **Hide all:** Collapses both code and results for all cells.

These options are helpful when:

- You want to focus on reading code or reviewing results.
- You are presenting or sharing your notebook.
- You need to navigate large notebooks more efficiently.

### Duplicate cells

Duplicating a cell can help with the following:

- Testing variations of a query or function.
- Debugging without overwriting the working version.
- Comparing different outputs side by side.
- Reusing code or modifying an existing cell without losing the original.

To duplicate a notebook cell:

1. From the cell to duplicate, select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) menu.
2. Select **Duplicate**.

   A copy of the cell appears immediately below the original.

### Cell minimap

The cell minimap appears in the right sidebar of the notebook and provides a compact, draggable list of all cells in the notebook. Each entry in the minimap corresponds to a code or text cell and reflects the order in which the cells appear.

- **Current cell:** The selected cell is highlighted in the minimap.
- **Reordering:** Drag and drop items in the minimap to quickly change the order of cells in the notebook.
- **Navigation:** Click a cell name in the minimap to jump directly to that cell.

This feature is useful for navigating large notebooks and reorganizing content more efficiently.

## Running notebooks with parameters

When you use the [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) command to run a notebook, you can pass arguments to the notebook.
In a Python cell in the notebook, you can access these arguments by using the `sys.argv` variable, which is a built-in Python list that holds command-line arguments.

Passing arguments to notebooks allows you to customize notebook behavior. You can:

- Personalize or customize notebook execution.
- Reuse the same notebook for multiple inputs.
- Support automation or task scheduling.

### Examples

In a Python cell in the notebook, you can access the arguments by using the `sys.argv` variable.

#### View all arguments passed to the notebook

Print the full list of arguments passed to the notebook.

Copy code

```
import sys
print(sys.argv)
```

If the notebook is executed with this command:

Copy code

```
EXECUTE NOTEBOOK MY_DATABASE.PUBLIC.MY_NOTEBOOK(
  'parameter_string a,b,c,d',
  'target_database=PROD_DB'
);
```

The output will be:

```
['parameter_string', 'a,b,c,d', 'target_database=PROD_DB']
```

#### Print each argument

Loop through and print each argument individually.

Copy code

```
for arg in sys.argv:
    print(arg)
```

The output will be:

```
parameter_string
a,b,c,d
target_database=PROD_DB
```

#### Access a specific argument

Access the second argument.

Copy code

```
second_param = sys.argv[1]
print(second_param)
```

The output will be:

```
a,b,c,d
```

#### Parse an argument containing comma-separated values

If an argument contains a comma-separated list of values, you can split it into individual values.

Copy code

```
value_list = sys.argv[1].split(",")
print(value_list)
```

The output will be:

```
['a', 'b', 'c', 'd']
```

You can also loop through the values:

Copy code

```
for value in value_list:
  print(value)
```

#### Extract an argument containing a key-value pair

If an argument includes a key-value pair (for example, `key=value`), extract the value.

Copy code

```
target_database = sys.argv[2].split("=")
print(target_database[1])
```

The output will be:

```
PROD_DB
```

#### Alternate syntax for a single string

You can set a [session variable](/sql-reference/session-variables) to the value of an argument and pass the session variable to the notebook.

Copy code

```
SET PARAMS = 'parameter_string a,b,c,d';
EXECUTE NOTEBOOK MY_DATABASE.PUBLIC.MY_NOTEBOOK($PARAMS);
```

### View results from a parameterized run

To view the result of a notebook run that was triggered using [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook):

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Notebooks**.
3. Select the **Calendar** icon.
4. Select **View run history**.
5. Find the notebook execution and open the result.

   A read-only notebook opens containing the result of that run.

### Notes

- `sys.argv` contains only the strings passed via [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook).
- Only strings are supported. If another data type (such as an integer) is passed, it will be interpreted as NULL. For more information,
  see [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook).

## Inspect cell status

The status of the cell run is indicated by the colors displayed by the cell. This status color is displayed in two places, the left wall of
the cell and in the right cell navigation map.

Cell status color:

- Blue dot: The cell was modified but hasn’t run yet.
- Red: The cell ran in the current session and an error occurred.
- Green: The cell ran in the current session without errors.
- Moving green: The cell is currently running.
- Gray: The cell has run in a previous session and the results shown are from the previous session. Cell results from the previous
  interactive session are kept for 7 days. Interactive session means the user runs the notebook in an interactive manner in Snowsight
  rather than those that were run by a schedule or the [EXECUTE NOTEBOOK](/sql-reference/sql/execute-notebook) SQL command.
- Blinking gray: The cell is waiting to be run after you select **Run All**.

Note

Markdown cells do not show any status.

After a cell finishes running, the time it took to run is displayed at the top of the cell. Select this text to view the run details,
including start and end times and total elapsed time.

SQL cells contain additional information, such as the warehouse used to run the query, rows returned, and a hyperlink to the query ID page.

> ![Cell run details window.](/static/images/snowsight/notebooks/snowsight-ui-cell-run-details.png)

### Stop a running cell

To stop the execution of any code cells that are currently running, select **Stop** on the top right of the cell. You can also select
**Stop** on the top right of the Notebooks page. While cells are running, **Run all** becomes **Stop**.

This stops the execution of the cell that is currently running and all subsequent cells that have been scheduled to run.

## Keyboard shortcuts

Snowflake Notebooks support various keyboard shortcuts to help accelerate your development process.

You can also see the list of keyboard shortcuts by selecting the keyboard icon at the bottom right corner, and then
selecting **Keyboard shortcuts**.

| Task | MacOS | Windows |
| --- | --- | --- |
| Run all cells | `CMD` + `Shift` + `Return` | `CTRL` + `Shift` + `Enter` |
| Run the selected cell | `CMD` + `Return` | `CTRL` + `Enter` |
| Run the selected cell and advance to the next cell | `Shift` + `Return` | `Shift` + `Enter` |
| Move between cells | `Up` and `Down` arrows | `Up` and `Down` arrows |
| Stop all cells | `ii` | `ii` |
| Find within the cell | `CMD` + `f` | `CTRL` + `f` |
| Move cell up | `CMD` + `SHIFT` + `Up` arrow | `CTRL` + `SHIFT` + `Up` arrow |
| Move cell down | `CMD` + `SHIFT` + `Down` arrow | `CTRL` + `SHIFT` + `Down` arrow |
| Add a cell above the currently selected cell | `a` | `a` |
| Add a cell below the currently selected cell | `b` | `b` |
| Delete the currently selected cell | `dd` or `DELETE` | `dd` or `DELETE` |
| Convert a SQL or Python cell into a Markdown cell | `m` | `m` |
| Convert a cell into a code cell:  - Change a Markdown cell to a Python cell - Change a Python cell to a SQL cell - Change a SQL cell to a Python cell | `y` | `y` |
| Show keyboard shortcuts | `Shift` + `?` | `Shift` + `?` |

Expand

Show lessSee more

In addition, you can use the same keyboard shortcuts that you use for worksheets. See [Perform tasks with keyboard shortcuts](/user-guide/ui-snowsight-worksheets#label-snowsight-keyboard-shortcuts).

## Format text with Markdown

To include Markdown in your notebook, add a Markdown cell:

1. Use a [keyboard shortcut](#label-notebooks-keyboard-shortcuts) and select **Markdown**, or select **+ Markdown**.
2. Select the **Edit markdown** pencil icon or double-click the cell, and start writing Markdown.

You can type valid Markdown to format a text cell. As you type, the formatted text appears below the Markdown syntax.

![Screenshot of a Markdown cell showing Markdown text with an H1 header indicated with a # and a header of An example Markdown cell
followed by body text of This is an example Markdown cell in a Snowflake Notebook. Below the raw Markdown content, the rendered
Markdown appears with a different font.](/static/images/screens/notebooks-markdown-editing.png)

To view only the formatted text, select the **Done editing** checkmark icon.

![Screenshot of a Markdown cell that is showing only the rendered Markdown: a header of An example Markdown
cell and body text of This is an example Markdown cell in a Snowflake Notebook.](/static/images/screens/notebooks-markdown-display.png)

Note

Markdown cells currently do not support rendering of HTML.

### Markdown basics

This section describes basic Markdown syntax to get you started.

**Headers**

| Heading level | Markdown syntax | Example |
| --- | --- | --- |
| Top level | Copy code  ``` # Top-level Header ``` | Header one in Markdown |
| 2nd-level | Copy code  ``` ## 2nd-level Header ``` | Header one in Markdown |
| 3rd-level | Copy code  ``` ### 3rd-level Header ``` | Header one in Markdown |

Expand

Show lessSee more

**Inline text formatting**

| Text format | Markdown syntax | Example |
| --- | --- | --- |
| Italics | Copy code  ``` *italicized text* ``` | Italicized text in Markdown |
| Bold | Copy code  ``` **bolded text** ``` | Bolded text in Markdown |
| Link | Copy code  ``` [Link text](url) ``` | Link in Markdown |

Expand

Show lessSee more

**Lists**

| List type | Markdown syntax | Example |
| --- | --- | --- |
| Ordered list | Copy code  ``` 1. first item 2. second item 3. Nested first 4. Nested second ``` | Ordered list in Markdown |
| Unordered list | Copy code  ``` - first item - second item   - Nested first   - Nested second ``` | Unordered list in Markdown |

Expand

Show lessSee more

**Code formatting**

| Language | Markdown syntax | Example |
| --- | --- | --- |
| Python | Copy code  ``` ```python import pandas as pd df = pd.DataFrame([1,2,3]) ``` ```  Copy code  ``` </td>       <td>  <Figure src="/static/images/snowsight/notebooks/notebooks-md-python.png" alt="Python code snippet in Markdown"> </Figure>  </td>     </tr>     <tr>       <td>SQL</td>       <td>  ```markdown ```sql SELECT * FROM MYTABLE ```  Copy code  ``` </td>       <td>  <Figure src="/static/images/snowsight/notebooks/notebooks-md-sql.png" alt="SQL code snippet in Markdown"> </Figure>  </td>     </tr>   </tbody> </Table>  </div>  **Embed images**  <div className="colwidths-given">  <Table>   <colgroup>     <col style={{width: "25.0%"}} />     <col style={{width: "25.0%"}} />     <col style={{width: "50.0%"}} />   </colgroup>   <thead>     <tr>       <th>File type</th>       <th>Markdown syntax</th>       <th>Example</th>     </tr>   </thead>   <tbody>     <tr>       <td>Image</td>       <td>  ```markdown ![<alt_text>](<path_to_image>) ``` | Embedded image in Markdown |

Expand

Show lessSee more

For a notebook that demonstrates these Markdown examples, see the [Markdown cells](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks.ipynb) section of the
visual data stories notebook.

## Understanding cell outputs

When you run a Python cell, the notebook displays the following types of output from the cell are displayed in the results:

- Any results written to the console, such as logs, errors, and warnings and output from print() statements.
- DataFrames are automatically printed with
  [Streamlit’s interactive table display](https://docs.streamlit.io/develop/api-reference/data/st.dataframe), `st.dataframe()`.

  - The supported DataFrame display types include pandas DataFrame, Snowpark DataFrames, and Snowpark Tables.
  - For Snowpark, printed DataFrames are evaluated eagerly without the need to run the `.show()` command. If you prefer not to evaluate the
    DataFrame eagerly, for example when running the notebook in non-interactive mode, Snowflake recommends removing the DataFrame
    print statements to speed up the overall runtime of your Snowpark code.
- Visualizations are rendered in outputs. To learn more about visualizing your data, see [Visualize data in Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-visualize-data).

Additionally, you can access the results of your SQL query in Python and vice versa. See [Reference cells and variables in Snowflake Notebooks](#label-notebooks-reference-cell-results).

### Cell output limits

Only 10,000 rows or 8 MB of DataFrame output is shown as cell results, whichever is lower. However, the entire DataFrame is still available in
the notebook session for use. For example, even though the entire DataFrame isn’t rendered, you can still perform data transformation tasks.

For each cell, only 20 MB of output is allowed. If the size of the cell output exceeds 20 MB, the output will be dropped. Consider splitting
the content into multiple cells if that happens.

## Reference cells and variables in Snowflake Notebooks

You can reference the previous cell results in a notebook cell. For example, to reference the result of a SQL cell or the value
of a Python variable, see the following tables:

Note

The cell name of the reference is case-sensitive and must exactly match the name of the referenced cell.

**Referencing SQL output in Python cells:**

| Reference cell type | Current cell type | Reference syntax | Example |
| --- | --- | --- | --- |
| SQL | Python | `cell1` | Convert a SQL results table to a Snowpark DataFrame.  If you have the following in a SQL cell called `cell1`:  Copy code  ``` SELECT 'FRIDAY' as SNOWDAY, 0.2 as CHANCE_OF_SNOW UNION ALL SELECT 'SATURDAY',0.5 UNION ALL SELECT 'SUNDAY', 0.9; ```  You can reference the cell to access the SQL result:  Copy code  ``` snowpark_df = cell1.to_df() ```  Convert the result to a pandas DataFrame:  Copy code  ``` my_df = cell1.to_pandas() ``` |

Expand

Show lessSee more

**Referencing variables in SQL code:**

Important

In SQL code, you can only reference Python variables of type `string`. You cannot reference a Snowpark DataFrame, pandas DataFrame or
other Python native DataFrame format.

| Reference cell type | Current cell type | Reference syntax | Example |
| --- | --- | --- | --- |
| SQL | SQL | `{{cell2}}` | For example, in a SQL cell named `cell1`, reference the cell results from `cell2`:  Copy code  ``` SELECT * FROM {{cell2}} where PRICE > 500 ``` |
| Python | SQL | `{{variable}}` | For example, in a Python cell named `cell1`:  **Using Python variable as a value**  Copy code  ``` c = "USA" ```  You can reference the value of the variable `c` in a SQL cell named `cell2` by enclosing it in single quotes to ensure that it is treated as a value:  Copy code  ``` SELECT * FROM my_table WHERE COUNTRY = '{{c}}' ```  **Using Python variable as an identifier**  If the Python variable represents a SQL identifier like a column or table name:  Copy code  ``` column_name = "COUNTRY" ```  If the Python variable represents a SQL identifier, such as a column or table name (`column_name = "COUNTRY"`), you can reference the variable directly without quotes:  Copy code  ``` SELECT * FROM my_table WHERE {{column_name}} = 'USA' ```  Make sure to differentiate between variables used as values (with quotes) and as identifiers (without quotes).  Note: Referencing Python DataFrames is not supported. |

Expand

Show lessSee more

## Considerations for running notebooks

- Notebooks run using caller’s rights. For additional considerations, see [Changing the session context for a notebook](/user-guide/ui-snowsight/notebooks-sessions#label-notebooks-callers-rights).
- You can import Python libraries to use in a notebook. For details, see [Import Python packages to use in notebooks](/user-guide/ui-snowsight/notebooks-import-packages).
- When referencing objects in SQL cells, you must use fully qualified object names, unless you are referencing object names in a specified
  database or schema. See [Changing the session context for a notebook](/user-guide/ui-snowsight/notebooks-sessions#label-notebooks-callers-rights).
- Notebook drafts are saved every three seconds.
- You can use [Git integration](/user-guide/ui-snowsight/notebooks-snowgit) to maintain notebook versions.
- You can configure an idle timeout setting to automatically shut down the notebook session once the setting is met. For information,
  see [Idle time and reconnection](/user-guide/ui-snowsight/notebooks-setup#label-notebooks-idle-time-property).
- Notebook cell results are only visible to the user who ran the notebook and are cached across sessions. Reopening a notebook displays
  past results from the last time the user ran the notebook using Snowsight.
- [BEGIN … END (Snowflake Scripting)](/sql-reference/snowflake-scripting/begin) is not supported in SQL cells. Instead, use the
  [Session.sql().collect()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Session.sql)
  method in a Python cell to run the scripting block. Chain the `sql` call with a call to `collect` to immediately execute
  the SQL query.

  The following code runs a Snowflake scripting block using the `session.sql().collect()` method:

  Copy code

  ```
  from snowflake.snowpark.context import get_active_session
  session = get_active_session()
  code_to_run = """
  BEGIN
   CALL TRANSACTION_ANOMALY_MODEL!DETECT_ANOMALIES(
       INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'ANOMALY_INFERENCE'),
       TIMESTAMP_COLNAME =>'DATE',
       TARGET_COLNAME => 'TRANSACTION_AMOUNT',
       CONFIG_OBJECT => {'prediction_interval': 0.95}
   );

   LET x := SQLID;
   CREATE TABLE ANOMALY_PREDICTIONS AS SELECT * FROM TABLE(RESULT_SCAN(:x));
  END;
  """
  data = session.sql(code_to_run).collect(block=True);
  ```
