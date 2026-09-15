# Add Anaconda packages to a notebook

Deprecated

Sharing individual notebooks with `application_content.notebooks` shares
[Legacy Notebooks](/user-guide/ui-snowsight/notebooks), and is deprecated. Starting
August 18, 2026, you can’t create new application packages that share notebooks this way. Starting
November 2026, Legacy Notebooks can no longer be run or edited. For the full timeline, see
[Disable Legacy Notebook creations](/release-notes/bcr-bundles/un-bundled/bcr-disable-legacy-notebooks).

Share [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
in a workspace instead. Consumers can run and interact with those notebooks the same way, and a
workspace can also share documentation, images, and sample data files. For more information, see
[Share a workspace in a Declarative Native App](/developer-guide/declarative-sharing/workspaces).

This topic applies only to Legacy Notebooks shared with `application_content.notebooks`. Notebooks
shared in a workspace install their Python packages at run time with `!pip install`, so they don’t
need an `environment.yml` file or an Anaconda package list. For more information, see
[Install Python packages in a shared notebook](/developer-guide/declarative-sharing/workspaces#label-dsna-workspace-notebook-packages).

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

The notebook environment includes a set of pre-installed Anaconda packages, such as Python and Streamlit.

If your notebook uses additional Anaconda packages, you must add those packages to your application package so that your notebook can access them.

You can add them while editing the notebook in development mode. You can also add the packages by providing an `environment.yml` file.

Note

If an `environment.yml` file is present in the same directory as a notebook, it overwrites the list of dependent packages, and any packages added through the Snowsight UI are ignored.

Using an `environment.yml` file is recommended for production applications as it allows you to manage dependencies in source control.

Using the UI is convenient for interactive development and testing.

## Adding Anaconda packages while editing the notebook in development mode

You can add Anaconda packages to your notebook while editing it in development mode. We recommend using this method rather than adding packages to the `environment.yml` file, because the process is considerably simpler.

To add packages while editing the notebook:

1. Install your application package locally from the live version.
2. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
3. In the navigation menu, select **Projects** » **Notebooks**.
4. Open your notebook file.
5. Make sure the notebook is in development mode. For information about development mode, see [Editing notebooks in a Declarative Native App](/developer-guide/declarative-sharing/live-editing).
6. Select the **Packages** button in the top center of the notebook editor.
7. Search for the package you want to add, and select it.

The notebook environment now automatically loads the selected dependencies when the notebook is run.

## Adding Anaconda packages to the `environment.yml` file

You can define your Python dependencies by creating an `environment.yml` file, and uploading it to the same stage directory as your notebook (.ipynb) file.

For information about creating an `environment.yml` file that includes your new packages, see
[Manage packages by using the environment.yml file](/developer-guide/streamlit/app-development/dependency-management#label-streamlit-install-packages-wh-environment-yaml).

Note

You can only install packages listed in the
[Snowflake Anaconda Channel](https://repo.anaconda.com/pkgs/snowflake/).
Notebooks in declarative sharing don’t support external Anaconda channels.

Use the PUT command to upload your `environment.yml` file from your local machine to the application package stage. The `environment.yml` file must be in the same directory on the stage as the notebook file it configures.

Replace the placeholders in the following command with your own values. If your notebook is at the root of the live version, do not include a directory path after `live/`.

Copy code

```
PUT <file:///path/to/your/environment.yml> snow://package/<PACKAGE_NAME>/versions/live/<path/to/your/notebook> OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
```
