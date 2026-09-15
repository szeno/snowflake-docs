# Access a shared workspace in a Declarative Native App

[Preview Feature — Open](/release-notes/preview-features)

Workspace sharing in Declarative Native Apps is available to all accounts.

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Some Declarative Native Apps share a workspace, which is a directory of files and folders
that the provider packages with the app. When you install the app, the shared workspace appears
alongside your own [workspaces](/user-guide/ui-snowsight/workspaces) as read-only content.

This topic describes how to open a shared workspace and run the notebooks it contains.

## About shared workspaces

A shared workspace is read-only. You can browse its folders, open its files, and run any notebooks
it contains, but you can’t change the content. Shared workspaces differ from your own workspaces in
the following ways:

| Capability | Your workspaces | Shared workspace from an app |
| --- | --- | --- |
| Browse folders and open files | Yes | Yes |
| Run notebooks | Yes | Yes |
| Edit, rename, or delete files | Yes | No |
| Add files to the workspace | Yes | No |
| Copy files to your own workspace | Yes | No |

Expand

Show lessSee more

The provider controls the contents of a shared workspace. When the provider releases a new version
of the app, the workspace content updates. If the provider stops sharing a workspace, it’s removed
from your account when the app upgrades.

## Open a shared workspace

You need access to the app, and to an app role that the provider assigned to the workspace. For
information about app roles, see [Install a Declarative Native App](/developer-guide/declarative-sharing/consumer/install).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **Workspaces** menu, and then select **Shared** to filter the list to workspaces
   shared with you.
4. Select the workspace that belongs to the app.

   The workspace opens in the file explorer, showing the folders and files the provider shared.
5. Select a file to open it.

   Notebooks (`.ipynb`) open in the notebook editor. Markdown files, images, and data files open in
   a read-only viewer.

You can also find the workspaces an app shares from the app itself:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Apps**.
3. Select the app, and then select the workspace you want to open.

## Run a shared notebook

Shared workspaces can include
[Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview).
You can run these notebooks and interact with their output.

Notebooks run on compute in your own account, not the provider’s. Before you can run a shared
notebook, you need a
[Snowflake-managed notebook service](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-compute-setup)
to host the notebook kernel and run the code.

1. Open the `.ipynb` file from the shared workspace.
2. Connect to a notebook service when prompted, or create one if you don’t have a service for this
   app yet.
3. Run individual cells, or run the whole notebook.
4. Interact with the results, including any charts and widgets the notebook produces.

You can’t edit the notebook’s cells or save changes to it. To keep a copy of a result, export it
from the notebook.

Note

A notebook service that you create for an app is scoped to that application instance. It can only
run the notebooks in that instance. Notebooks in workspaces that aren’t bound to an app, or
that belong to a different app instance, can’t use it. Each app instance needs its own notebook
service.

### What a shared notebook can access

Shared notebooks run with
[restricted caller’s rights](/developer-guide/restricted-callers-rights) (RCR). A shared notebook
can only access the objects that the app shares with you. It can’t read your other data, query
other apps, or inspect metadata about your account. For the full set of boundaries, see
[Declarative App Consumer-Side Execution Model](/developer-guide/declarative-sharing/consumer/consumer-execution).

### Install Python packages in a shared notebook

If a shared notebook needs a Python package, it installs the package when you run the cell that
calls `pip`:

Copy code

```
!pip install <package_name>
```

The provider includes these cells in the notebook. Run them like any other cell. The packages
install into the notebook’s environment for that session.

## Considerations

- You can’t share a workspace from an app with other members of your organization. Access follows
  the app roles that the app owner grants. For more information, see
  [Install a Declarative Native App](/developer-guide/declarative-sharing/consumer/install).
- You can’t move or copy files out of a shared workspace into your own workspace.
- Shared workspaces don’t contain `.pdf` files. Providers can’t share PDFs in a workspace.
- To query the tables and views the app shares, see
  [Access content in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-app-content).
