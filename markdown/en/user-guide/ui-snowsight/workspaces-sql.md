# Workspace operations using SQL

This topic provides a step-by-step walkthrough of workspace lifecycle operations using SQL. You can run
these SQL statements from any Snowflake client, including Snowsight, SnowSQL, or the
[Snowflake CLI](/developer-guide/snowflake-cli/sql/execute-sql).

Workspaces can be **shared** or **private**. In a shared workspace, changes made with `PUT` must be
committed (published) before other users can see them. In a private workspace, no commit is needed because
only the owner can access the workspace.

## Prerequisites

Required privileges vary by operation and are noted in each section below.

## Reference workspace files in SQL

Use the same `snow://workspace/` path format for reading and modifying files in a workspace:

```
snow://workspace/<database>.<schema>.<workspace>/versions/head/<path>
```

The database, schema, and workspace identify the workspace object. The optional path after `/versions/head/` identifies a file or folder
within the workspace. Omit that path to reference the workspace root.

Your default **My Workspace** uses the object name `USER$.PUBLIC.DEFAULT$`, not `My Workspace`.
`USER$` refers to your personal database. For example, list files in **My Workspace**:

Copy code

```
LIST 'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/head/';
```

For another private workspace, replace `DEFAULT$` with the workspace’s object name. Enclose case-sensitive names or names
containing spaces in double quotes, and enclose the full path in single quotes. For example, for a workspace named `my_workspace`:

Copy code

```
LIST 'snow://workspace/USER$.PUBLIC."my_workspace"/versions/head/';
```

For a shared workspace, use the database and schema that contain it. For example, list files in a shared workspace:

Copy code

```
LIST 'snow://workspace/MY_DB.WORK.MY_WORKSPACE/versions/head/';
```

For full `LIST` syntax and options, see [LIST](/sql-reference/sql/list). The following sections show how to use workspace paths
to upload, download, and remove files.

## Create a workspace

Copy code

```
CREATE OR REPLACE WORKSPACE MY_DB.WORK.MY_WORKSPACE;
```

Note

Requires CREATE WORKSPACE on the target schema.

## Grant privileges to another role

Copy code

```
GRANT { READ | WRITE } ON WORKSPACE MY_DB.WORK.MY_WORKSPACE TO ROLE <role_name>;
```

Granting WRITE also grants READ. For more information, see [Access control privileges](/user-guide/security-access-control-privileges) and
[Shared workspaces](/user-guide/ui-snowsight/workspaces-shared).

Note

Requires OWNERSHIP on the workspace.

## Add a live version

A mutable live version must exist before you can upload or remove files.
If an operation fails because no live version exists, run the following command and retry the operation with the same `/versions/head/` path:

Copy code

```
ALTER WORKSPACE MY_DB.WORK.MY_WORKSPACE ADD LIVE VERSION FROM LAST;
```

Note

If a live version already exists, you must commit or abort it before adding a new one.

Requires WRITE privilege on the workspace.

## Upload a file

Copy code

```
PUT file:///path/to/report.sql
    snow://workspace/MY_DB.WORK.MY_WORKSPACE/versions/head/
    AUTO_COMPRESS=false OVERWRITE=true;
```

The destination folder comes after `/versions/head/`:

- `/versions/head/` places the file at the workspace root.
- `/versions/head/reports/monthly/` places the file in a subdirectory.

For full `PUT` syntax and options, see [PUT](/sql-reference/sql/put).

Note

In a shared workspace, the file is only visible to you until it is published. See
[Commit (publish all changes)](#label-workspaces-sql-commands-commit).

A live version must exist before running `PUT`. If it does not, [add a live version](#label-workspaces-sql-add-live-version) first.

Requires WRITE privilege on the workspace.

## Download a file

Copy code

```
GET snow://workspace/MY_DB.WORK.MY_WORKSPACE/versions/head/report.sql
    file:///path/to/download/;
```

For full `GET` syntax and options, see [GET](/sql-reference/sql/get).

Note

Requires READ privilege on the workspace.

## Remove a file

Copy code

```
REMOVE snow://workspace/MY_DB.WORK.MY_WORKSPACE/versions/head/report.sql;
```

Warning

Unlike `PUT`, which requires `COMMIT` to publish changes, `REMOVE` auto-publishes: The file is
immediately removed from the published workspace for all users unless they have their own uncommitted version
of that same file. This auto-publish behavior is relevant for shared workspaces, where other users see
the removal right away. This behavior may change to require an explicit commit in a future release.

For full `REMOVE` syntax and options, see [REMOVE](/sql-reference/sql/remove).

Note

A live version must exist before running `REMOVE`. If it does not, [add a live version](#label-workspaces-sql-add-live-version) first.

Requires WRITE privilege on the workspace.

## List files

Copy code

```
LIST 'snow://workspace/MY_DB.WORK.MY_WORKSPACE/versions/head/';
```

For full `LIST` syntax and options, see [LIST](/sql-reference/sql/list).

Note

Requires READ privilege on the workspace.

## Commit (publish all changes)

Committing publishes all file changes, making them available to other users. Users with their own live version might still see their unpublished changes.

Copy code

```
ALTER WORKSPACE MY_DB.WORK.MY_WORKSPACE COMMIT;
```

Important

- After committing, the live version no longer exists. You must [add a live version](#label-workspaces-sql-add-live-version) again before
  the next `PUT` or `REMOVE`.
- Unlike [publishing from the UI](/user-guide/ui-snowsight/workspaces-shared#label-shared-workspaces-resolve-conflicts), `COMMIT` offers
  no conflict protection — the commit might override files that other users have changed recently.

Note

Requires WRITE privilege on the workspace.

## Abort live version

Discards all unpublished changes, removing the entire live version.

Copy code

```
ALTER WORKSPACE MY_DB.WORK.MY_WORKSPACE ABORT;
```

Important

All uncommitted changes in the live version are permanently lost — files added via `PUT` are
discarded, and modified files revert to their last committed state.

Note

After abort, the live version no longer exists. You must [add a live version](#label-workspaces-sql-add-live-version) again before the
next `PUT` or `REMOVE`.

Requires WRITE privilege on the workspace.

## Rename a workspace

Copy code

```
ALTER WORKSPACE MY_DB.WORK.MY_WORKSPACE
    RENAME TO MY_DB.WORK.MY_WORKSPACE_V2;
```

Note

Requires OWNERSHIP on the workspace.

## Drop a workspace

Copy code

```
DROP WORKSPACE MY_DB.WORK.MY_WORKSPACE;
```

Note

Requires OWNERSHIP on the workspace.

## Restore a dropped workspace

Use UNDROP to restore a workspace that was dropped, as long as it is still within the retention period.

Copy code

```
UNDROP WORKSPACE MY_DB.WORK.MY_WORKSPACE;
```

Note

Requires OWNERSHIP on the workspace (the same privilege required to drop it). Restoring fails if a workspace with the
same name already exists in the schema; rename or drop the conflicting workspace first.
