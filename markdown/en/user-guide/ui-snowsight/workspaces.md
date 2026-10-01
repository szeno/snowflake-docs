# Workspaces

Get started with Workspaces

[Try it in Snowsight](https://app.snowflake.com/_deeplink/#/workspaces?utm_source=docs&utm_medium=growth&utm_campaign=-us-en-all&utm_content=-app-user-guide-ui-snowsight-workspaces)

Important

Workspaces has replaced Legacy Worksheets in Snowsight, including in reader accounts.
You can’t disable Workspaces or switch back to Legacy Worksheets. For the deprecation timeline and migration details, see
[Deprecation of Legacy Worksheets and Dashboards](/release-notes/bcr-bundles/un-bundled/bcr-2260).

## Run your first SQL query

To write and run SQL, create a SQL file in your default workspace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. In **My Workspace**, select **+ Add New** or the **+** next to a folder, then select **SQL File**.
4. In the SQL file’s editor, select a role and a warehouse that you have access to. If your query references tables,
   select their database and schema, or use fully qualified table names.
5. Enter a query. For example:

   Copy code

   ```
   SELECT 1 AS result;
   ```
6. Select the statement and press `command` + `return` on macOS or `CTRL` + `Enter` on Windows to run it.
7. Review the output in the **Results** pane.

For more ways to work with results, see [Exploring query results](/user-guide/ui-snowsight/workspaces-working#label-workspaces-explore-query-results).
To run a Python file instead, see [Python files in Workspaces](/user-guide/ui-workspaces-python).

## Overview

Workspaces provides a unified editor for creating, organizing, and managing code across multiple file types that you can use to analyze data,
develop models, and build pipelines.

A *workspace* contains files and folders for your code.
In Workspaces, you write SQL in `.sql` files and organize related files in the same workspace.

Your default workspace, **My Workspace**, is private to you. For collaboration, use
[shared workspaces](/user-guide/ui-snowsight/workspaces-shared). To work with code in a Git repository, see
[Integrate workspaces with a Git repository](/user-guide/ui-snowsight/workspaces-git).

When a user accesses Workspaces for the first time, Snowflake automatically creates an internal, user-specific personal database. This database
is used to store workspaces and cannot contain standard objects such as tables or views. It does not grant the user any additional
capabilities or privileges beyond enabling Workspace functionality. For details on personal databases, see [Personal Databases](/user-guide/personal-databases).

Administrators may notice that users appear to have OWNERSHIP, USAGE, and CREATE SCHEMA privileges on this database. These privileges are
required for interacting with Workspaces and do not affect access to other resources.

## Roles in Workspaces

The Workspaces experience uses your current role from the Snowsight user menu. This role determines which workspaces
appear in the **Workspaces** menu and which resources you can access. To change it, in the lower-left corner, select your name » **Switch role**.

For example, when you create a Git workspace, this role determines which API integrations and secrets you can access.
Private workspaces belong to you, rather than to the role used to create them. When you create a
[shared workspace](/user-guide/ui-snowsight/workspaces-shared), your current role is selected as the owner by default.
You can select another role from the owner role menu in the creation dialog.

The role selector inside an open SQL file controls only the SQL statements run in that file. Changing it doesn’t change
your current role for the rest of the Workspaces experience.

## The Workspaces environment

Workspaces is a new editor composed of six sections, or *panes*:

![Overview of the Workspaces environment.](/static/images/snowsight/ui-snowsight-workspaces.png)

1. **Workspaces:** One area for all your files and folders. Drag files to move them between folders. Use nested folders to group related
   worksheets under logical categories so that you can quickly find specific worksheets without searching through a flat list. Each user has a
   default workspace named “My Workspace” that is automatically provisioned by Snowflake. You can also create a new workspace by selecting
   **+ Add New** in the **Workspaces** menu. The default workspace cannot be deleted or renamed.
2. **Worksheets:** Open and edit worksheets you own or have any permissions on. Note that edits will not be saved if you only have read
   permissions on the worksheet. To convert a worksheet into a file in a workspace, drag it to a folder inside the workspace. You can only move
   worksheets individually; moving multiple worksheets at once is not supported. Workspace queries are run similarly to worksheets with a few
   small differences, including improved UI performance and the ability to run two queries simultaneously from the same SQL file.
3. **Database Explorer:** A hierarchical view of all databases in your account, the schemas for each database, and other objects, organized
   by type. Use the filter to search for objects. You can also filter out unusable objects to simplify your view by selecting **Show databases I can query**.
   The options available in the vertical ellipsis [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) (more actions) button vary by object type, but include features such as
   placing names in the editor, copying names, and viewing definitions. To open or close the **Database Explorer** or **File Explorer**, select the
   **File Explorer** icon [![File explorer](/static/images/snowsight/file-explorer-open-close.png)](/static/images/snowsight/file-explorer-open-close.png) in the bottom toolbar of the Workspaces window.
4. **Editor:** Edit queries and split them side by side to view multiple files simultaneously. Use inline Copilot to get suggestions and
   completions directly within the editor workspace.
5. **Results:** Split results side-by-side or pin them for easy comparison.
6. **Query History:** View the history of all queries you have run. **Current File** shows historical queries from the file currently open
   and selected in the editor. Filter to the current file or across all files. **All Files** displays all historical queries you have run
   across all files. To open or close this view, select the **Query History** icon [![Query history](/static/images/snowsight/query-history-open-close.png)](/static/images/snowsight/query-history-open-close.png) in the bottom toolbar of the Workspaces window.

## Limitations

- [Query filters](/user-guide/ui-snowsight-filters) are not supported. Any queries containing filters will fail.
