# Editing notebooks in a Declarative Native App

[Preview Feature — Open](/release-notes/preview-features)

Workspace sharing in Declarative Native Apps is available to all accounts.

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

Declarative Native Apps share [Snowflake Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-overview)
in a [workspace](/developer-guide/declarative-sharing/workspaces). As a provider, you can edit those
notebooks in place while you develop the app, instead of editing them elsewhere and rebuilding the
application package for every change.

To do this, you create a test application from the live version of your application package. Notebooks
in a workspace in that test application are editable, so you can change a notebook, run it to check
the result, and publish the change when you’re satisfied. Publishing writes the change back to the
application package, so the next version you release includes it.

Consumers who install your app always get a read-only workspace. Editing applies only to a test
application you create from your own package.

## How it works

The live version of your application package acts as a development sandbox. You edit notebooks in a
test application, publish the changes you want to keep, and then release the live version when the
app is ready.

### Step 1: Create a test application from the live version

Build the package, and then create an application from its live version:

Copy code

```
ALTER APPLICATION PACKAGE <pkg_name> BUILD;

CREATE APPLICATION <test_app_name>
  FROM APPLICATION PACKAGE <pkg_name>
  USING VERSION LIVE;
```

Notebooks in the workspaces of this application are editable. For more information about building and
releasing a package, see [Application Packages in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/package).

### Step 2: Edit a notebook in the workspace

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Apps**.
3. Select your test application. The workspaces that the application contains are listed.
4. Select the workspace, and then open an `.ipynb` file.
5. Edit the notebook cells and run them to test your changes.

Your edits are a draft: only you can see them until you publish. For more information about the draft
and publishing model in workspaces, see
[Collaborate in a shared workspace](/user-guide/ui-snowsight/workspaces-shared#label-shared-workspaces-collaborate-in-a-shared-workspace).

### Step 3: Review and publish your changes

The **Publish changes** drop-down, at the top right of the editor, lets you review a draft before you
commit to it:

- To compare your draft against the last published version side by side, select **Show changes**.
  Select **Hide changes** to return to the editor.
- To throw the draft away and go back to the last published version, select **Discard changes**. You’re
  prompted to confirm.

When you’re happy with the notebook, select **Publish**. The change is saved to the test application
and written back to the file system of the parent application package.

Publishing is a per-file action. Repeat steps 2 and 3 for every notebook you want to change, in every
workspace the app shares.

### Step 4: Release the version

After you publish the changes to all of the notebooks, release the live version whenever you’re ready:

Copy code

```
ALTER APPLICATION PACKAGE <pkg_name> RELEASE LIVE VERSION;
```

This command creates a new immutable version of the application package that includes your published
notebook changes. For more information about versions, see
[Package Versions in Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/versioning).
