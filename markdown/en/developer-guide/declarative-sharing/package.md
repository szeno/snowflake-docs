# Application Packages in Declarative Sharing in the Native Application Framework

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

As a provider, you create an application package to bundle your data content and notebooks into a Declarative Native App.
This topic explains what an app package is and describes the high-level steps to create one, from creating the initial package to adding your manifest and notebook files.

## The application package and the live version

The app package is a container for all the files that make up the app, including the [manifest](/developer-guide/declarative-sharing/manifest-reference) file and any [Snowflake Notebooks](/user-guide/ui-snowsight/notebooks). When you create an app package, a live (staged) version of the app package is also created. The live version is a development workspace where you can add or update files, such as the manifest file and notebook files, and preview and test the experience before publishing.

Once you’re satisfied with the live version of the app, you can commit the live version to create a new immutable version of the app package, that you can then publish.

Using the live version for development simplifies version management by maintaining a single immutable version of the app package that is ready to be published, and a single live version for development. The Snowflake Native App Framework automatically manages the versioning of the app package, so you don’t need to manually track version numbers.

The Snowflake Native App Framework maintains a live version for any app package automatically. Even if you remove the live version, a new live version is created automatically from the last committed version of the app package.

## Create an application package

Providers develop and test an **application (app) package**. An app package includes files necessary to share the data in the app, and defines how data can be accessed by consumers.

The process involves the following steps:

1. **Create an app package project** (first time only): creates an app package project that will later be published. This also creates the live version of the app package.
2. **Add content to the app package**:

   1. **Create or update a manifest file**: This file describes the app package and its contents.
   2. **Download notebook files**. If notebooks are to be included, download a copy to be included in the app package.
   3. **Add the files to the live version of the app package**.
3. **Build the app package**: allows you to verify that the manifest file is valid and that all links in the manifest file are correct.
4. **Test the app**. Install the app and try it out. Make changes, and rebuild.
5. **Commit the app package**: creates a new immutable version of the app that can be published.
6. **Release the app package**. With a released package, you can create a new listing, either privately or publicly on the Snowflake Marketplace.

This process is described in the [Tutorial: Getting started with Declarative Native Apps](/developer-guide/declarative-sharing/tutorials/getting-started). This section includes additional details of options available at the different stages of development.

![Diagram showing the steps of creating an application package: Add live package, build, commit, and release. The diagram also shows the optional steps to skip ahead to build, commit, and release a live version all at once.](/static/images/ds-native-apps/dsna-lifecycle.png)

### Create a new application package

First, create a new Declarative Native App package to hold the app’s files, either via Snowsight or SQL commands from [Snowflake CLI](/developer-guide/snowflake-cli/index), using the *snow://package/<DECL\_SHARE\_APP\_PKG>/versions/LIVE/* URL scheme.

SnowsightSnowflake CLI

To use Snowsight to create a new app package:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App Packages**.
3. In the **Share Data + Code** card, select **Create**.
4. Enter a name for your app package, and then select **Create**.

To use SQL in [Snowflake CLI](/developer-guide/snowflake-cli/index) to create a new app package:

- Create a Declarative Native App package using the [CREATE APPLICATION PACKAGE … TYPE=DATA](/developer-guide/declarative-sharing/command-reference#label-dsna-create-application-package) command, replacing *<DECL\_SHARE\_APP\_PKG>* with the name you want to give the app package:

Copy code

```
snow sql -q "CREATE APPLICATION PACKAGE <DECL_SHARE_APP_PKG> TYPE = DATA;"
```

The new empty app package is created. This also creates a live version of the app package that you can edit.

### Assemble content for the application package

An app package includes the following components:

- A [manifest](/developer-guide/declarative-sharing/manifest-reference) file (required): A text-based file that defines the app’s structure.
- [Workspace](/developer-guide/declarative-sharing/workspaces) directories (optional): One or more directories of files and folders that consumers get as read-only workspaces. A workspace can contain notebook (`.ipynb`) files, documentation, images, and sample data files.
- [Snowflake Notebook](/user-guide/ui-snowsight/notebooks) files (optional): One or more text-based files that can act as a front end to the consumer experience, referencing the shared views and tables. They can also include code, reference visualizations, and include logic to help present the data.

![App package components diagram](/static/images/ds-native-apps/dsna-components.png)

### Create or update a manifest file

You can create or update a [manifest](/developer-guide/declarative-sharing/manifest-reference) file, which describes the app package and its shared content: for example, notebooks, tables, and views. It defines other metadata, such as [app roles](/developer-guide/declarative-sharing/app-roles) included with the app.

The manifest file must be named `manifest.yml`, and must be added to the root level of the app package.

For more information, see [Declarative Native App manifest reference](/developer-guide/declarative-sharing/manifest-reference). The associated [Tutorial: Getting started with Declarative Native Apps](/developer-guide/declarative-sharing/tutorials/getting-started) includes an example manifest file.

#### Create or update a manifest file from a Snowflake data share

Note

The following content is not supported by Snowflake. All code is provided “AS IS” and without warranty.

If you have an existing data share in Snowflake, you can automatically create a manifest file using the open-source Manifest from Share tool. This Snowflake-provided tool generates a manifest file based on the objects in a specified share. The tool also includes options to customize the generated manifest file. You can use this tool in the following ways:

- Generate a manifest file using the command-line interface (CLI).
- Integrate the tool into an existing Python automation workflow as a library.

For more information about how to download and use the tool, see the [Snowflake Manifest from Share](https://github.com/snowflakedb/native-apps-examples/tree/main/snowflake-manifest-from-share-library) repository on GitHub.

Note

The Manifest from Share tool only creates the manifest file using the data share’s databases, schemas, tables and views. The tool doesn’t include any other objects in the generated manifest file.

### Get notebook files

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

If [Snowflake Notebooks](/user-guide/ui-snowsight/notebooks) are to be included in the app, download a copy of each notebook file so you can include it in the app package.

From Snowsight:

1. In the navigation menu, select **Projects** » **Notebooks**, and then select the notebook you want to download.
2. In the left pane, next to your notebook, select **…** » **Download**.

The file is downloaded to your local machine, as a file named `<notebook_name>.ipynb`.

Note

The notebook environment has a set of pre-installed Anaconda packages, including Python and Streamlit. If your notebook uses additional Anaconda packages, you must add those as packages to your notebook so they can be used in the consumer’s environment. For information about how to add Anaconda packages to your notebook, see the [Add Anaconda packages to a notebook](/developer-guide/declarative-sharing/add-packages).

### Add files to the live version

Add the manifest and notebook files to the live version of the app package:

SnowsightSnowflake CLI

To use Snowsight to populate the app package:

1. If you’re not already viewing the app package’s listing, from the navigation menu, select **Projects** » **App Packages**, and then select the app package you want to add files to.
2. Select **Upload files**. (If you are replacing or adding additional files, select **Manage files**, and then select **Upload files**.)
3. Drag the notebook files and the manifest from your hard disk to the **Upload files** dialog where indicated, or select **Browse** to locate and select the files.
4. Select **Upload** to upload the files to the live stage and trigger a build.

1. To use SQL in Snowflake CLI to populate the app package, use the following commands, replacing the file paths with your own and *<DECL\_SHARE\_APP\_PKG>* with the name of the app package:

   1. Manifest file:

      Copy code

      ```
      snow sql -q "PUT file:////Users/test_user/Documents/manifest.yml  snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/ OVERWRITE=TRUE AUTO_COMPRESS=false;"
      ```
   2. Notebook file:

      Copy code

      ```
      snow sql -q "PUT file:////Users/test_user/Documents/NOTEBOOK.ipynb  snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE OVERWRITE=TRUE AUTO_COMPRESS=false;"
      ```
2. Verify the files are in the application package with the following command:

   Copy code

   ```
   snow sql -q "LIST snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE"
   ```

   The output shows the files in the live version of the app package, similar to the following:

   ```
   +--------------------------------------------------------------------------------+
   | name                          | size | md5     | last_modified                 |
   |-----------------------------------------+------+---------+---------------------|
   | /versions/live/manifest.yml   | 304  | 843a... | Wed, 23 Jul 2025 08:27:26 GMT |
   | /versions/live/NOTEBOOK.ipynb | 832  | b014... | Wed, 23 Jul 2025 04:32:22 GMT |
   +--------------------------------------------------------------------------------+
   ```

### Download a file from the application package

You can download a file from the app package using the [GET](/sql-reference/sql/get) SQL command in Snowflake CLI:

> Copy code
>
> ```
> snow sql -q "GET snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/manifest.yml file://manifest.yml"
> ```

### Remove content from the application package

You can remove files from the application package.

SnowsightSnowflake CLI

Using Snowsight:

1. If you’re not already viewing the app package’s listing, from the navigation menu, select **Projects** » **App Packages**, and then select the app package you want to remove files from.
2. Select **Manage files** » **Remove files**.
3. Select the file(s) you want to remove, and then select **Delete**.
4. In the **Remove files** dialog, choose the files to remove, and then select **Remove & build**.

Using the REMOVE (or RM) SQL command in Snowflake CLI:

Copy code

```
snow sql -q "RM snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/manifest.yml"
```

### Build the application package

Next, build a testable version of the app.

SnowsightSQL

In Snowsight:

- When you upload a complete set of files to the app package, a build kicks off automatically.
- To perform a build at any other time, select the Build button on the app package’s page.

If there are any errors in the manifest file, the build fails and gives information on how to fix the error. Correct the errors and rebuild the app package.

The [ALTER APPLICATION PACKAGE … BUILD](/developer-guide/declarative-sharing/command-reference#label-dsna-alter-application-package) command builds a testable version of the app package and verifies that the manifest file is valid and that all links work.

Copy code

```
ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> BUILD;
```

If there are any errors in the manifest file, the build fails and gives information on how to fix the error. Correct those errors and rebuild the app package.

The built app remains in the live state, and you can continue to make changes to the application package.

#### Skip ahead!

For updates that don’t require further testing, you can skip ahead by building, committing, and releasing an app package all at once using the [ALTER APPLICATION PACKAGE … RELEASE LIVE VERSION](/developer-guide/declarative-sharing/command-reference#label-dsna-alter-application-package) command.

Copy code

```
ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> RELEASE LIVE VERSION;
```

### Test the application

After building the app package, you can perform basic tests on it from the live environment.

Install the app from an app package using the command: [CREATE APPLICATION … FROM APPLICATION PACKAGE](/sql-reference/sql/create-application), replacing *<DECL\_SHARE\_APP>* with the name of the app. For example:

Copy code

```
CREATE APPLICATION <DECL_SHARE_APP> FROM APPLICATION PACKAGE <DECL_SHARE_APP_PKG>
```

Update the files in the app package as needed, and then see if it worked by using the command: [ALTER APPLICATION … UPGRADE USING VERSION LIVE](/sql-reference/sql/alter-application).

Copy code

```
ALTER APPLICATION <DECL_SHARE_APP> UPGRADE USING VERSION LIVE;
```

To test some features, such as app roles, you must first release a new version of the app package, and then test using a separate consumer account. For more information, see [Install a Declarative Native App](/developer-guide/declarative-sharing/consumer/install) and [Access content in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-app-content).

#### Optional: Reset edits on a live version

If the edits made to the live version of the app package are no longer needed, you can reset the app package to the state before the edits were made with the [ALTER APPLICATION PACKAGE … ABORT LIVE VERSION](/developer-guide/declarative-sharing/command-reference#label-dsna-alter-application-package) command.

Copy code

```
ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> ABORT LIVE VERSION;
```

When you use the preceding command to remove the current live version, a new live version is created with the same contents as the last committed version of the app package. The live version is reset to the last committed version, and all changes made to the live version are discarded.

### Commit and release the application package

Committing the app package builds a new immutable version of the app that can’t be edited and is ready to be published. Releasing the app package does the following:

- Makes a committed app ready to be shared with consumers.
- If the provider has already shared the app with consumers, the new version is automatically available to those consumers.
- If there’s already a live version of the app on the Snowflake Marketplace, the new version is automatically available to consumers who have installed the app.

SnowsightSQL

To use Snowsight to commit and release the app package:

1. If you’re not already viewing the app package’s listing, from the navigation menu, select **Projects** » **App Packages**, and then select the app package you want to release.
2. Select **Commit & release**.
3. In the confirmation dialog, select **Acknowledge & continue**.

The committed app package is released, and the live version of the app package is removed. A new live version of the app package is created from the new committed version for further development.

Once you’ve committed and released the app package, the **Latest release** tab shows the contents of the release, which is the same as the contents of the last build.

1. In SQL, use the [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application) commands as shown:

   Copy code

   ```
   ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> COMMIT;
   ```

   The live version of the app package is removed. A new live version of the app package is created from the new committed version for further development.
2. Next, release the committed app package:

   Copy code

   ```
   ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> RELEASE;
   ```

   You can also build, commit, and release a live version of the app package, all at once:

   Copy code

   ```
   ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> RELEASE LIVE VERSION;
   ```

After you release the app package, you can create a new listing for the app, either privately or publicly on the Snowflake Marketplace. For more information, see [Creating a Listing using Declarative Sharing](/developer-guide/declarative-sharing/listing).
