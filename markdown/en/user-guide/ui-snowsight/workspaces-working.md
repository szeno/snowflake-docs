# Working with workspaces

Important

Workspaces has replaced Legacy Worksheets. To start running SQL, see
[Run your first SQL query](/user-guide/ui-snowsight/workspaces#label-workspaces-run-first-query).

## Create and work with files and folders

In a workspace you can use a familiar IDE and source control conventions to author, organize, and run code.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **+** next to the appropriate folder. If you’re using Workspaces for the first time, select **+ Add New**.
4. Select from the following options to create a new file or folder or to upload an existing file or folder:
   - **SQL File**: Creates a new, blank SQL file in the editor as a tab in the editor. By default, `.sql` is appended to unnamed files. The editor
     recognizes it as a SQL file and enables syntax highlighting and autocomplete.
   - **File**: Creates a new file. Name the file and its extension. If the extension is recognized by the editor (for example, Java, JavaScript, or
     Scala), code highlighting and autocomplete are enabled.
   - **Folder**: Creates a new, empty folder inside the workspace.
   - **Upload Files**: Upload one or more files to any location in your workspace. The editor uses the file extension and applies the appropriate icon,
     behavior, and syntax highlighting to the file when it’s opened. For example, `.sql` files show SQL-specific features.
   - **Upload Folder**: Select one or more files or folders to add to the selected workspace.

To create and run a Python script, name the file with a `.py` extension and follow
[Open and run a Python file](/user-guide/ui-workspaces-python#label-py-in-ws-open-and-run).

### Manage files

You can rename, delete, move, and organize your workspaces, files, and folders.

To rename or delete a workspace, file, or folder, follow these steps:

1. Hover over the target and select the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions).
2. Select **Rename** or **Delete**. If you choose to delete, you are prompted to confirm.

- To create a folder in a workspace, select the **+** next to the workspace or an existing folder.
- To organize files and folders, drag any file or folder into a different location in the same workspace. You can also drag a worksheet into a workspace.

### Format SQL code

Workspaces include a built-in functionality to format and standardize SQL code for improved readability and maintenance.

1. In the **Workspaces editor**, select the horizontal ellipsis.

   ![Format SQL query](/static/images/workspaces/ui-snowsight-workspaces-format-query.png)
2. Select **Format SQL** or use the [keyboard shortcut](#label-workspaces-keyboard-shortcuts) `command` + `shift` + `O`
   (Windows: `CTRL` + `Alt` + `O`).

### Organize sections of code

Use code folding to collapse and expand large blocks of code, allowing you to focus on specific sections and improve overall code navigation.

1. In the **Workspaces editor**, locate the code section to collapse.
2. Hover the mouse to the right of the line numbers. A code folding icon ([![Code folding icon to collapse and expand a code selection.](/static/images/workspaces/workspaces-code-fold-chevron-down.png)](/static/images/workspaces/workspaces-code-fold-chevron-down.png)) appears at the fold line.
3. Toggle the icon to fold or unfold the section of code.

### Split the editor pane

Split the editor pane to work in multiple files at once. For example, reference one query while you write another. Each
editor pane shows its own files and query results.

To split the editor pane, do one of the following:

- Hover over a file tab, select **More options** (**…**), and then select **Split right** or **Split down**.
- In the top-right corner of the editor, select the settings icon, and then select **Split editor pane**.
- Use the [keyboard shortcuts](#label-workspaces-keyboard-shortcuts) `control` + `\` (split horizontally) or
  `control` + `shift` + `\` (split vertically).

To close the other tabs in a pane, hover over a tab, select **More options** (**…**), and then select **Close other tabs**.

Splitting the editor pane changes the layout of the whole editor. To compare query results without splitting the editor, see
[Pin and compare query results](#label-workspaces-pin-compare-results).

## Exploring query results

When you run a query in Workspaces, you can use interactive features to filter, analyze, and explore your results without writing
additional SQL. These features help you quickly understand your data and identify patterns.

Note

These interactive result features are available in Workspaces in different locations than in the legacy Worksheets interface.

### Use interactive column statistics

Each column in your query results includes interactive visual statistics (mini graphs or histograms) that help you understand data
distribution and quality. You can click these statistics to open a detailed panel and create filters.

**To view column statistics:**

1. Run a query in a Workspaces SQL file.
2. In the results table, show the column statistics by doing one of the following:

   - Click **Show column stats** in the top-left corner of the table (next to the column headers).
   - Click the ellipsis button in any column header and select **Show column stats**.

   Mini graphs (histograms or distribution charts) appear in each column header showing the data distribution.
3. Click a histogram to view sum and average values for that entire column in the bottom-right of the table.

   Alternatively, you can select a range of cells in the results table to view statistics in the bottom-right of the table. For numeric columns,
   sum and average values are displayed. For non-numeric columns, the count is displayed.

**To filter using column statistics:**

1. Click **Show column stats** in the top-left corner of the results table, or click the ellipsis button in any column header and select **Show column stats**.
2. Click the histogram for the column you want to filter by. A popover displays detailed statistics for that column, including:

   - **Sum and average values** for numeric columns
   - **Distribution charts** showing value frequency
   - **Data quality metrics** such as null and filled percentages
3. In the popover, select the values or ranges you want to filter by.
4. Select **Apply** to apply the filter to your results.

This interactive filtering helps you explore your data visually without writing WHERE clauses or other SQL filter logic.

### Inspect cell values

The cell inspector provides detailed information about individual cells or selections in your query results.

To inspect a single cell:

1. In the results table, double-click any cell to open the **Inspector Panel**.
2. Review the detailed value, including formatting and data type information.

To view aggregate statistics for multiple cells:

- In the results table, select multiple cells by clicking and dragging across rows and columns.

  A statistics bar appears at the bottom showing:

  - **Sum** of numeric values
  - **Average** of numeric values
  - **Count** of selected cells
  - **Min and max** values in the selection

This feature is useful for quick calculations and data exploration without creating new queries.

### Pin and compare query results

By default, each query you run replaces the result that you are viewing. Pin a result to keep it open while you run other queries.

**To pin a result:**

- In the results area, hover over the result’s tab and select the pin icon (**Pin tab**).

  The tab stays open when you run more queries, and new results open in a separate tab. A pinned tab always shows a filled pin icon.

You can also pin a result from the **Query History** pane: hover over a query and select **Pin result**, or hold `option` (macOS) or
`Alt` (Windows) and click the query.

**To unpin a result:**

- Select the filled pin icon (**Unpin tab**) on the pinned tab.

**To close a pinned result:**

Pinned tabs don’t show a close button, which protects them from being closed by accident.

1. Select the filled pin icon to unpin the tab.
2. Hover over the tab and select the close button (**X**).

**To view results side by side:**

1. Pin the result that you want to compare.
2. Run another query, or open another result.
3. Hover over the pinned result’s tab, select **More options** (**…**), and then select **Split right** or **Split down**.

## Keyboard shortcuts

Workspaces provides keyboard shortcuts to help you quickly navigate, customize your view, and edit queries. The following table identifies
commonly used keyboard shortcuts:

| Task | macOS shortcut | Windows shortcut |
| --- | --- | --- |
| Run selected | `command` + `return` | `CTRL` + `Enter` |
| Run all | `command` + `shift` + `return` | `CTRL` + `Shift` + `Enter` |
| Format SQL file | `command` + `shift` + `O` | `CTRL` + `Alt` + `O` |
| Split editor pane horizontally | `control` + `\` | `CTRL` + `\` |
| Split editor pane vertically | `control` + `shift` + `\` | `CTRL` + `Shift` + `\` |
| Close focused tab | `control` + `W` | `CTRL` + `Q` |
| Copy selected file | `command` + `C` | `CTRL` + `C` |
| Cut selected file | `command` + `X` | `CTRL` + `X` |
| Paste file in selected location | `command` + `V` | `CTRL` + `V` |
| Open query results pane | `control` + `option` + `↑` | `CTRL` + `Alt` + `↑` |
| Close query results pane | `control` + `option` + `↓` | `CTRL` + `Alt` + `↓` |
| Open query history pane | `control` + `shift` + `H` | `CTRL` + `Shift` + `H` |
| Open inline Copilot | `command` + `I` | `CTRL` + `I` |
| Comment out code | `command` + `/` | `CTRL` + `/` |
| Go to top of file | `command` + `home` or `command` + `↑` | `CTRL` + `home` or `CTRL` + `↑` |
| Go to bottom of file | `command` + `end` or `command` + `↓` | `CTRL` + `end` or `CTRL` + `↓` |

Expand

Show lessSee more

### Recover a workspace from a dropped user

When a user is dropped, their personal database (PDB) and all files within their workspaces are retained. The PDB is
renamed to `DROPPED_USER$<dropped_user_name>_<timestamp>` and is owned by the primary role that was active when the
`DROP USER` statement ran (referred to here as `<owning_role>`).

Recovery usually involves two people:

- an **administrator** — someone with the privileges to drop users, with access to `<owning_role>`
- the **recovering user** — the person inheriting the work from the dropped user, who wants the files in their own
  private workspace.

In order for the recovering user to recover deleted workspace into their own private workspaces they must run the final
`CREATE WORKSPACE` step themselves targetting their own `USER$` PDB.

To locate the dropped user’s PDB the administrator lists them and identifies the one to recover, those that start with the
reserved prefix `DROPPED_USER$`, then they locate the specific workspaces inside to recover:

Copy code

```
SHOW DATABASES STARTS WITH 'DROPPED_USER$';
-- surfaces database "DROPPED_USER$user_123"
SHOW WORKSPACES IN DATABASE "DROPPED_USER$user_123";
-- surfaces workspace "DROPPED_USER$user_123".PUBLIC."deleted_ws"
```

**Option 1: Use the owning role.** Use this when the recovering user already has access to `<owning_role>`, or when
`<owning_role>` can be granted to them.

Copy code

```
-- Administrator (skip if the recovering user already has the role):
GRANT ROLE <owning_role> TO USER <recovering_user>;

-- Recovering user:
USE ROLE <owning_role>;
```

The administrator can revoke the role after recovery with `REVOKE ROLE <owning_role> FROM USER <recovering_user>`.

**Option 2: Create a temporary recovery role.** Use this when you don’t want to grant `<owning_role>`. An administrator
creates a role scoped to just the dropped PDB and grants it to the recovering user.

Copy code

```
-- Administrator:
CREATE ROLE recovery_temp;
GRANT ROLE recovery_temp TO USER <recovering_user>;
GRANT USAGE ON DATABASE "DROPPED_USER$user_123" TO ROLE recovery_temp;
GRANT USAGE ON SCHEMA "DROPPED_USER$user_123".PUBLIC TO ROLE recovery_temp;
GRANT READ ON WORKSPACE "DROPPED_USER$user_123".PUBLIC."deleted_ws" TO ROLE recovery_temp;

-- Recovering user:
USE ROLE recovery_temp;
```

The administrator can drop the role after recovery with `DROP ROLE recovery_temp`; the recovered workspace is
unaffected.

**Recover the workspace.** With a role that has access active, the recovering user runs the following steps.

1. List the origin workspace files to confirm access:

   Copy code

   ```
   LS 'snow://workspace/"DROPPED_USER$user_123".PUBLIC."deleted_ws"/versions/head/';
   ```
2. Create a copy of the workspace into your own PDB, then add a live version so it’s ready to edit:

   Copy code

   ```
   CREATE WORKSPACE USER$.PUBLIC."recovered_ws"
     FROM 'snow://workspace/"DROPPED_USER$user_123".PUBLIC."deleted_ws"/versions/head';
   ALTER WORKSPACE USER$.PUBLIC."recovered_ws" ADD LIVE VERSION FROM LAST;
   ```

## Limitations

- Column statistics may take longer to generate as the number of columns increases.
- Snowflake Copilot (legacy) is not available in Workspaces. For AI-assisted coding in Workspaces, use
  [Cortex Code](/user-guide/cortex-code/cortex-code-snowsight).
- [Query filters](/user-guide/ui-snowsight-filters) are not supported. Any queries containing filters will fail.
- Opening and editing the same worksheet in the new Workspaces UI and old Worksheets UI simultaneously can result in lost changes.
- For worksheets, execution context settings (role, warehouse, and namespace) are not synchronized across the new Workspaces UI and the old Worksheets UI.
