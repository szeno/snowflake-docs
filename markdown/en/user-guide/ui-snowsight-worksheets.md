# Work with worksheets in Snowsight

Worksheets provide a powerful and versatile method for running SQL queries or Python code within the Snowflake platform, as well as
performing other Snowflake data loading, definition, and manipulation tasks.

Important

Legacy Worksheets will be removed from Snowsight on **June 22, 2026**.
[Workspaces](/user-guide/ui-snowsight/workspaces) is the replacement
SQL editing experience. For the full deprecation timeline and migration guidance, see
[Deprecation of Legacy Worksheets and Dashboards](/release-notes/bcr-bundles/un-bundled/bcr-2260).

After you open a worksheet in Snowsight, you can do any of the following:

- [Write SQL statements](/user-guide/ui-snowsight-query) and [visualize the results](/user-guide/ui-snowsight-visualizations).
- [Write Python code](/developer-guide/snowpark/python/python-worksheets).
- [Browse and open other worksheets](#label-snowsight-worksheets-browse).
- [Change the context for the worksheet](#label-snowsight-worksheet-session-context).
- [Update and organize worksheets into folders](#label-worksheets-manage).
- [Share worksheets](#label-sharing-worksheets-and-folders).
- [Manage the history and versioning of worksheets](#label-snowsight-worksheet-history).
- [Perform tasks with keyboard shortcuts](#label-snowsight-keyboard-shortcuts).
- [Recover worksheets owned by a dropped user](#label-snowsight-worksheets-recover).

Note

Executing SQL or Python code in worksheets consumes warehouse credits. To learn how to run code more cost-efficiently, see [Optimizing cost](/user-guide/cost-optimize).

## Browse and open worksheets

When you open a worksheet, you can view and manage other worksheets in the **Worksheets explorer**. The **Worksheets explorer** also
allows you to search for specific worksheets.

Note

The search functionality is designed to index worksheet metadata, such as titles and object names. It does not index user-written values
within queries (such as numbers, string literals, or personally identifiable information/PII) as this is by design to protect sensitive data.

### Preview worksheet contents

To preview the contents of a worksheet, you can hover over the name of the worksheet in the **Worksheets explorer**. The preview also
shows the role used to run the worksheet.

From the preview, you can also copy the contents of the worksheet. Hover over the worksheet contents preview and
select the **Copy** button that appears.

## Perform tasks with keyboard shortcuts

Snowsight provides keyboard shortcuts to help you quickly navigate and edit queries in worksheets. For example, you can move your
cursor within a worksheet, perform find and replace, copy lines, format queries, and more using hotkeys.

| Task | MacOS shortcut | Windows shortcut |
| --- | --- | --- |
| Show keyboard shortcuts | `⌘` + `Shift` + `/` | `Ctrl` + `Shift` + `/` |
| New query | `Ctrl` + `⌘` + `n` | `Ctrl` + `Alt` + `n` |
| Search schema or results | `⌘` + `Shift` + `f` | `Ctrl` + `Shift` + `f` |
| Clear selection | `Escape` | `Escape` |
| Make bottom pane larger | `Ctrl` + `` + `↑`</td> <td>`Ctrl` + `` + `↑` |
| Make bottom pane smaller | `Ctrl` + `` + `↓`</td> <td>`Ctrl` + `` + `↓` |
| Go right one pane tab | `Ctrl` + `` + `→`</td> <td>`Ctrl` + `` + `→` |
| Go left one pane tab | `Ctrl` + `` + `←`</td> <td>`Ctrl` + `` + `←` |
| Run selected | `⌘` + `Return` | `Ctrl` + `Enter` |
| Run all | `⌘` + `Shift` + `Return` | `Ctrl` + `Alt` + `Enter` |
| Format query | `⌘` + `Shift` + `o` | `Ctrl` + `Shift` + `o` |
| Indent line | `⌘` + `]` | `Ctrl` + `]` |
| Outdent line | `⌘` + `[` | `Ctrl` + `[` |
| Toggle comment | `⌘` + `/` | `Ctrl` + `/` |
| Search | `⌘` + `f` | `Ctrl` + `f` |
| Replace | `⌘` + `Shift` + `h` | `Ctrl` + `h` |
| Find next | `⌘` + `g` | `F3` |
| Find previous | `⌘` + `Shift` + `g` | `Shift` + `F3` |
| Move line up | ``` + `↑` | `Alt` + `↑` |
| Move line down | ``` + `↓` | `Alt` + `↓` |
| Copy line up | ``` + `Shift` + `↑` | `Alt` + `Shift` + `↑` |
| Copy line down | ``` + `Shift` + `↓` | `Alt` + `Shift` + `↓` |
| Delete line | `Ctrl` + `Shift` + `k` | `Ctrl` + `Shift` + `k` |
| Split pane horizontally | `Ctrl` + `\` | `Ctrl` + `\` |
| Split pane vertically | `Ctrl` + `Shift` + `\` | `Ctrl` + `Shift` + `\` |

Expand

Show lessSee more

To see all available keyboard shortcuts in Snowsight, open a worksheet and press `CMD` + `SHIFT` + `/` on a Mac keyboard or
`CTRL` + `SHIFT` + `/` on a Windows keyboard.

## Change the context for a worksheet

When you create a worksheet, you specify the role and warehouse used to execute the worksheet’s contents. This information is referred to
as **worksheet context**, is preserved for future sessions, and is shared with all users of the same worksheet.

Note

The role selector lets you choose your primary role. To enable secondary roles in a SQL worksheet, run
[USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles). To determine whether secondary roles are active in your current session, call the CURRENT\_SECONDARY\_ROLES function [CURRENT\_SECONDARY\_ROLES](/sql-reference/functions/current_secondary_roles).

The role context for a worksheet determines which operations can be performed on Snowflake objects based on the access control
privileges granted to the role.

To set the context for a worksheet, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Open the context selector.
5. Select a role to run the worksheet as.
6. Select a warehouse that the role has privileges to use.
7. Select anywhere outside the drop-down to close the context selector.

Note

Each worksheet has a unique session and can use roles different from the role you select in the user menu (your *active role*).
Changing your active role does not change the role assigned to the worksheet with the context selector.

### Resume or resize a warehouse

Before or after you run your worksheet, you might need to resume or resize your warehouse.

Note

You must have MODIFY or OWNERSHIP privileges on the warehouse to alter warehouse details.

To view or adjust warehouse details using the context selector, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. Open the context selector.
5. Select the **Show warehouse details** icon.
6. For the **Status** option, select the status and choose **Resume** if the warehouse is suspended.
7. For the **Size** option, select the size and choose a different size.
8. Select anywhere outside the drop-down to close the context selector.

## Manage worksheets

You can manage worksheets in Snowsight from the worksheet tab or the **Worksheets explorer**. To access the worksheet tab menu,
open a worksheet, hover over the tab, and select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png). To access the **Worksheets explorer**, hover over a
worksheet name and select the [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png).

The actions available in each menu are based on your current role. Depending on your permissions, you can do the following:

- Rename, delete, or move a worksheet (requires Edit or Ownership permissions).
- Organize worksheets by moving them into folders or a dashboard.
- Import SQL from an external file.
- Format your queries.
- Search for other worksheets.
- Duplicate a worksheet (any role).

Tip

You can hover over a worksheet to preview its contents.

You can identify which worksheets are open in tabs by referencing the worksheet icon. A solid icon indicates that the worksheet is
currently open. To access menu options, hover over a worksheet name and select the ellipsis visible.

## Share worksheets and folders

Sharing a worksheet or worksheet folder allows you to collaborate with colleagues. Recipients of a shared worksheet can edit or view its
contents, run queries, view results, or duplicate the shared worksheet.

You can share worksheets and folders of worksheets with other Snowflake users in your account. You can only share worksheets directly
with users who have previously signed in to Snowsight. To share with someone who has not yet signed in to
Snowsight, share a link instead (ensure that link sharing is enabled).

### Permissions for shared worksheets

When you share a worksheet with someone, you can manage access to the worksheet and its contents by choosing which permissions to grant to
the other user. These permissions are also used for [sharing dashboards](/user-guide/ui-snowsight-dashboards#label-snowsight-dashboards-sharing).
Worksheet owners have the same permissions as worksheet editors.

Each worksheet in Snowsight uses a unique session with a specific role and warehouse assigned in the context of the worksheet.
The *worksheet role* is the *primary role* last used to run the worksheet and is required to run the worksheet.

Note

Users with Run permissions can also change the worksheet’s role using [USE ROLE](/sql-reference/sql/use-role).

To view the results of an earlier worksheet version, you need to have the primary role that was used to run the SQL statement that
generated the results. See [Viewing results for past runs of a worksheet](#label-snowsight-worksheets-viewing-results).

| Permissions Granted | Recipient Can: |
| --- | --- |
| Edit | - Edit the worksheet contents. - Run the worksheet, including using a different role. - View and manage past versions of the worksheet. - View and manage results from past worksheet versions, provided they have the role used to generate the results. - Share the worksheet with others. - Add the worksheet to a different folder. |
| View + Run | - Inherits all privileges from View Results (see below). - Run the worksheet, provided they have the worksheet role. - View the results of the most recent worksheet version. - Duplicate and run the worksheet using their own role. |
| View Results | - Inherits all privileges from Link with View Results (see below). - View the results of the most recent worksheet version, provided they have the worksheet role. - Duplicate and run the worksheet using their own role. |
| Link with View + Run | - Inherits all privileges from Link with View Results (see below). - Run the worksheet, provided they have the worksheet role. - View the results of the most recent worksheet version. - View the worksheet contents (but cannot duplicate or run the worksheet). |
| Link with View Results | - View the results of the most recent worksheet version, provided they have the worksheet role. - View the worksheet contents (but cannot duplicate or run the worksheet). |

Expand

Show lessSee more

The worksheet owner is the user who created the worksheet and has the same permissions as a worksheet editor. The worksheet owner changes
if the worksheet is added to a folder owned by another user.

Important

If a worksheet owner is dropped from Snowflake, the dropped user will remain the owner of the worksheet; however, users with any share
permissions can continue to access and use the worksheet. Any user with the worksheet link will still be able to access it if link
sharing is enabled. To maintain worksheet access, Snowflake recommends having the user share their worksheets with Edit permissions
(rather than View or View + Run) *before dropping the user* so others can continue to modify or delete the worksheet. To recover the
worksheets owned by a dropped user including those that aren’t shared, see [Recover worksheets owned by a dropped user](#label-snowsight-worksheets-recover).

#### Viewing results for past runs of a worksheet

When you run one or all queries in a worksheet, your query results are displayed as a table. You can navigate the query results with the
[arrow keys](#label-snowsight-keyboard-shortcuts), as you would with a spreadsheet. You can select columns, cells, rows, or ranges in
the results table. You can copy and paste any selection.

To view the results for past runs of a worksheet, the following must be true:

- The user must have the role used to run the SQL statement that generated the results.
- The results must still be stored in Snowflake. See [Stored results for past worksheet versions](#label-snowsight-worksheets-results-cache).

Snowsight allows you to review generated statistics for up to 1 million rows of results. These statistics provide contextual
information for any selection,
as well as overall statistics. See [Automatic contextual statistics](/user-guide/ui-snowsight-query#label-snowsight-contextual-stats) for more details.

You can also:

- View your results as a chart by selecting **Chart**. For more details about charts, see [Visualizing worksheet data](/user-guide/ui-snowsight-visualizations).
- Review results of a past worksheet run by viewing the **Query History** for a worksheet. See [View query history](/user-guide/ui-snowsight-query#label-snowsight-worksheet-query-history).

### Share a worksheet

To share a worksheet, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a worksheet.
4. In the upper-right corner of the worksheet, select **Share**.
5. Enter the names or usernames of the Snowflake users to invite to use your worksheet. The list only shows users who have
   previously signed in to Snowsight. To share with someone who has not yet signed in to
   Snowsight, select **Get Link** to generate a link to share instead.
6. Choose the [permissions to grant to the users](#label-sharing-worksheets-permissions) with whom you share the worksheet.
7. Optionally, set permissions for what people with the link to the worksheet can access.
8. Select **Done**.

Note

The worksheet that is shared is the most recently run version. If the worksheet has never been run, the contents will appear empty. Any edits
that you make to your version of the worksheet, whether you’re an editor or an owner of the worksheet, do not appear for collaborators
until you run part or all of the worksheet code.

Any worksheet that you share (either directly or through a link) with a collaborator can appear in their search results or worksheets
list. Worksheets shared directly appear immediately, while those shared through a link appear once they have been accessed. These
worksheets will continue to appear in the collaborator’s search results or lists unless they are deleted by a user with edit access, or
if the collaborator’s access permissions to the worksheets are removed.

### Share a folder of worksheets

To share a folder, including all worksheets in the folder, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open a folder.
4. Select **Share**.
5. Enter the names or usernames of the Snowflake users to invite them to your folder. The list only shows users who have previously
   signed in to Snowsight. If you want to share with someone who has not yet signed in to Snowsight, share a link instead.
6. Choose the [permissions to grant to the users](#label-sharing-worksheets-permissions) with whom you share the folder.
7. Optionally, set permissions for what people with the link to the folder can access.
8. Optionally, select **Get Link** to get a link to your folder that you can share with others.
9. Select **Done**.

If you add a worksheet to a shared folder, the worksheet inherits the sharing settings of the folder. If the folder is owned by someone
other than the worksheet owner, the folder owner becomes the worksheet owner, and the original worksheet owner inherits
the sharing permissions from the folder.

For example, if a worksheet owner adds a worksheet to a folder on which they have edit permissions, the worksheet updates
to be owned by the folder owner, and the original worksheet owner then has edit permissions on the worksheet.

Any folder shared (either directly or through a link) with a collaborator can appear in their search results or folders
list. Folders shared directly appear immediately, while those shared through a link appear once they have been accessed. These folders will
continue to appear in the collaborator’s search results or lists unless they are deleted by a user with edit access, or if the
collaborator’s access permissions to the worksheets are removed.

### Share worksheets across accounts

Worksheets cannot be replicated or shared across accounts. To share the contents of a worksheet
with users in another Snowflake account, copy the contents and share it with users in the account outside of Snowflake.

## Manage worksheet history and versions

Any local edits you make to a worksheet are automatically saved every three seconds but remain visible only to you. When you run a SQL
query or execute code in a worksheet, the latest version is updated and shared with all collaborators. You can also view past versions of a
worksheet and optionally copy details from any version. For more information, see [Switch worksheet versions](#label-snowsight-worksheet-versions).

When making changes to worksheets and managing worksheet versions, consider the following:

- When you share a worksheet with other users, users with edit permissions can view past versions of the worksheet.
  All users that you share a worksheet with can view up to 10,000 rows of the results for the most recent version of the worksheet.
- Whenever someone with permissions runs a worksheet, a new version of the worksheet is saved.
- If you make changes to the worksheet and they seem to disappear, use the version history to open the saved draft with your changes.
- The most recently run version of the worksheet is the version visible to collaborators.
- If you make changes to the worksheet that you want to be visible to the users with whom you shared the worksheet, you must run the worksheet.
- If multiple users edit and run a shared worksheet at the same time, each run of the worksheet creates a new version. The most recently
  run version of the worksheet is the one visible when you open or refresh the worksheet.

### Switch worksheet versions

To view past versions of a worksheet, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open the worksheet.
4. Select **Code Versions** for the worksheet.
5. From the list of worksheet versions, select the timestamp of the version that you want to view.
6. Review and optionally copy the worksheet details for that version.
7. Select **Close** to return to the current version of the worksheet.

To view the results of a past worksheet run, view the **Query History** for the worksheet.
See [View query history](/user-guide/ui-snowsight-query#label-snowsight-worksheet-query-history).

### Stored results for past worksheet versions

Note

Available to most accounts. Accounts in U.S. government regions, accounts using Virtual Private Snowflake (VPS), and accounts
that use Private Connectivity to access Snowflake continue to see query results limited to 10,000 rows.

All results for queries executed in worksheets are available for up to 24 hours. After 24 hours, you must run your query again to view
results.

To support contextual statistics and sharing worksheet results, the 25 latest query results are cached for up to 90 days. This cache is
included in the data storage usage for your account.

## Recover worksheets owned by a dropped user

If you drop a user, you can recover up to 500 of the worksheets owned by that user. To recover the worksheets, do the following:

1. [Download recovered worksheets](#label-snowsight-worksheets-recover-dropped) owned by a dropped user.
2. [Create worksheets from a SQL file](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create-file) to add the recovered worksheets back to Snowflake.

If you want to change ownership or retain access to worksheets before dropping a user, ask that user to share the worksheets.
See [Share worksheets and folders](#label-sharing-worksheets-and-folders).

### Download recovered worksheets owned by a dropped user

To recover worksheets owned by a dropped user, download a `.tar.gz` archive file of up to 500 worksheets owned by that user.

Note

You must be granted the ACCOUNTADMIN role to recover worksheets of dropped users.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Settings**.
3. Select **General**.
4. Next to **Recover worksheets from dropped users**, select **Recover worksheets**.
5. In the dialog box, enter the username of a dropped user in your account.

   Important

   The case and spelling of the username must exactly match the username as it was stored in Snowflake.
6. Select **Recover**.

   Your web browser downloads a `.tar` file containing up to 500 worksheets. If the dropped user has more than 500 worksheets,
   only the 500 most recently modified worksheets are downloaded.

After downloading worksheets owned by a dropped user, add the recovered worksheets to Snowsight by creating worksheets from
the SQL files.

You must expand the downloaded `.tar` file into a folder of `.sql` files before you can add recovered worksheets to
Snowsight. You can only add one worksheet at a time to Snowsight, and the user who adds the recovered worksheets to
Snowsight becomes the new owner of the worksheets.

See [Create worksheets from a SQL file](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create-file) for details.

### Considerations for recovering worksheets owned by dropped users

- Only the title and contents of the most recently executed version of a worksheet are recovered. Worksheet version history,
  sharing recipients and permissions, query results, and worksheet metadata are not recovered.
- A maximum of 500 worksheets are recovered. For dropped users with more than 500 worksheets, only the 500 most recently modified worksheets
  are recovered.
- Only worksheets in Snowsight are recovered. Worksheets in Classic Console owned by dropped users cannot be recovered with
  this method.
- If multiple dropped users have the same username, worksheets owned by all dropped users with that username are recovered.

If the worksheet recovery fails for unexpected reasons, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Internal Snowflake objects for worksheets

Snowflake creates the following internal objects to support using worksheets in Snowsight:

| Object Type | Name |
| --- | --- |
| Security integration | WORKSHEETS |
| Blobs | WORKSHEETS\_APP |
| Database | WORKSHEETS\_APP |
| User | WORKSHEETS\_APP\_USER |
| Roles | APPADMIN, WORKSHEETS\_APP\_RL |

Expand

Show lessSee more

These internal objects are used to cache query results in an internal stage in your account. This cached data is encrypted and protected by
the key hierarchy for the account.

The limited privileges granted to the internal role only allow Snowsight to access the internal stage to store those results. The
role cannot list objects in your account or access data in your tables.

The Snowsight user and role are returned when you query the [USERS](/sql-reference/account-usage/users) and
[ROLES](/sql-reference/account-usage/roles) views, respectively, in the [ACCOUNT\_USAGE](/sql-reference/account-usage) schema
in the SNOWFLAKE shared database. [SHOW <objects>](/sql-reference/sql/show) statements do not return these internal objects.
