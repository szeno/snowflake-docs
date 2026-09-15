# Share a workspace in a Declarative Native App

[Preview Feature — Open](/release-notes/preview-features)

Workspace sharing in Declarative Native Apps is available to all accounts.

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

With workspace sharing, you can share a whole directory of files and folders as part of your
Declarative Native App. You point a workspace at a directory in your application package, and
consumers get a read-only [workspace](/user-guide/ui-snowsight/workspaces) when they install the
app.

This topic describes how to add a workspace to your app, which files you can share, and how
consumers use the result.

## About workspace sharing

A shared workspace is a directory of files that you declare in the
[manifest](/developer-guide/declarative-sharing/manifest-reference) file. The framework copies the
directory into the app and creates a workspace in the consumer account. Consumers browse the
folder structure and open the files, but they can’t change them.

Workspace sharing is how you share
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
the next-generation notebook experience. Include `.ipynb` files in the workspace directory, and
consumers can run and interact with those notebooks in their own account. For more information,
see [Share next-generation notebooks in a workspace](#label-dsna-workspace-notebooks).

Workspace sharing gives you the following:

- **One directory, many file types.** Share notebooks, documentation, images, and sample data
  together instead of declaring each object separately.
- **Folder structure that consumers see.** The folders you create in the app package are the
  folders consumers browse.
- **Read-only access.** Consumers can open and run the content, but they can’t modify it.
- **Role-based access.** Assign [app roles](/developer-guide/declarative-sharing/app-roles) to a
  workspace to control which teams in the consumer’s organization can see it.

## Supported file types

You can share any file type in a workspace except `.pdf`. Of the files you share, only notebook
(`.ipynb`) files are executable. Consumers can open every other file type, but they can’t run it.

The following table shows common examples:

| File type | Extension | What consumers can do |
| --- | --- | --- |
| Notebooks | `.ipynb` | Open, run, and interact with the notebook |
| Markdown | `.md` | Read the rendered file |
| Images | `.png`, `.jpg`, `.jpeg`, `.svg` | View the image |
| Python | `.py` | Read the file |
| SQL | `.sql` | Read the file |
| Data files | `.csv`, `.json`, `.yaml` | Read the file |

Expand

Show lessSee more

Note

Python (`.py`) and SQL (`.sql`) files in a shared workspace are read-only and can’t be run, even
though you can run them interactively in your own workspaces. To share runnable logic, put it in a
notebook cell, or use [stored procedures and user-defined functions](/developer-guide/declarative-sharing/udfs-sprocs)
in `shared_content`.

Important

You can’t share `.pdf` files in a workspace. The framework rejects them when you build, commit, or
release the application package, and again when a consumer installs the app.

## Add a workspace to your app

To share a workspace, add the files to your application package, declare the workspace in the
manifest file, and then release a new version.

### Step 1: Add the files to the live version

Upload your workspace files to a directory in the live version of the application package. The
directory structure you create here is the structure consumers see.

For example, to build a workspace with a notebook, a readme, and an image:

Copy code

```
snow sql -q "PUT file:///path/to/local/analysis.ipynb snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/workspace_content/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;"
snow sql -q "PUT file:///path/to/local/README.md snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/workspace_content/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;"
snow sql -q "PUT file:///path/to/local/chart.png snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/workspace_content/images/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;"
```

Verify the files with the following command:

Copy code

```
snow sql -q "LIST snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE"
```

You can also upload files using Snowsight. For more information, see
[Application Packages in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/package).

Note

Set `AUTO_COMPRESS = FALSE` when you upload workspace files. Compressed files aren’t readable in
the consumer’s workspace.

### Step 2: Declare the workspace in the manifest

Add a `workspaces` entry under `application_content` in your `manifest.yml` file. Each entry names
a workspace and points it at a directory using the `source` property:

Copy code

```
roles:
  - ANALYST:
      comment: "Can open the shared analysis workspace."

application_content:
  workspaces:
    - ANALYSIS_WORKSPACE:
        source: workspace_content/
        roles: [ANALYST]
        comment: "Notebooks and reference material for the shared population data."
```

The `source` property must meet the following requirements:

- It’s a directory path relative to the root of the package version, so it must not start with a
  slash (`/`).
- It must end with a slash (`/`).
- The directory must exist and contain at least one file.

Any role you list in `roles` must also be declared in the top-level `roles` field. Unlike objects
in `shared_content`, a workspace isn’t tied to a shared schema, so its roles don’t need to be a
subset of a parent schema’s roles.

If you omit `roles`, or set it to an empty list (`[]`), then only the app owner and roles with
[granted IMPORTED PRIVILEGES](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data) can access the workspace.

For the full field reference, see
[`application_content.workspaces`](/developer-guide/declarative-sharing/manifest-reference#label-dsna-manifest-fields-application-content-workspaces).

### Step 3: Build and release the app package

Build the application package to validate the manifest and the workspace content:

Copy code

```
ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> BUILD;
```

The build fails if the `source` directory is missing, is empty, or contains a `.pdf` file. Fix the
error and build again.

When you’re satisfied with the result, commit and release the package:

Copy code

```
ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> RELEASE LIVE VERSION;
```

For more information about the development lifecycle, see
[Application Packages in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/package).

## Share next-generation notebooks in a workspace

To share a
[Snowflake Notebook in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview),
include its `.ipynb` file in a workspace directory. Consumers can then run and interact with the
notebook in their own account. They can’t modify it.

Note

Workspace sharing replaces the older approach of declaring individual notebooks under
`application_content.notebooks`, which shares
[Legacy Notebooks](/user-guide/ui-snowsight/notebooks) and is deprecated. Share `.ipynb` files in a
workspace instead.

### How shared notebooks run in the consumer account

Shared notebooks run with
[restricted caller’s rights](/developer-guide/restricted-callers-rights) (RCR). Under RCR, a shared
notebook can only reach the objects your app shares. It can’t read the
consumer’s own data, query other apps, or inspect account metadata. For more information about
these boundaries, see [Declarative App Consumer-Side Execution Model](/developer-guide/declarative-sharing/consumer/consumer-execution).

Design your notebooks against the objects you declare in `shared_content`. A notebook that queries
a table or view you didn’t share fails when the consumer runs it.

### Install Python packages in a shared notebook

Shared notebooks install their Python dependencies at run time. Add a Python cell that calls `pip`
with the packages the notebook needs:

Copy code

```
!pip install <package_name>
```

Consumers run this cell like any other cell in the notebook. The packages install into the
notebook’s environment for that session.

Note

Because packages install at run time, you don’t need to add an `environment.yml` file to the
application package, and you don’t need to declare Anaconda packages for the notebook.

## Update or remove a shared workspace

To change the contents of a shared workspace, update the files in the live version of the
application package, and then release a new version. Consumers get the new content when the app
upgrades.

To rename a workspace, change its name in the manifest. To stop sharing a workspace, remove its
entry from `application_content.workspaces`. When you release a version that no longer declares a
workspace, the framework deletes that workspace from consumer accounts on upgrade.

## What consumers see

After a consumer installs your app, the shared workspace appears in their list of workspaces in
Snowsight, marked as read-only. Consumers browse the folders, open files, and run any
notebooks the workspace contains.

Consumers can also see the workspaces your app shares on the app’s page, under **Apps** in the
navigation menu.

To run a notebook you share, a consumer needs a
[Snowflake-managed notebook service](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup)
in their own account. Notebooks run on the consumer’s compute, not yours, and the service they
create is scoped to your app’s instance.

For the consumer’s view of this experience, see
[Access a shared workspace in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-shared-workspace).
