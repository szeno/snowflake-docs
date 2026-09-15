# Tutorial: Getting started with Declarative Native Apps

[Preview Feature — Open](/release-notes/preview-features)

Workspace sharing in Declarative Native Apps is available to all accounts.

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

## Introduction

This tutorial takes Snowflake data providers through the process of creating, publishing, and accessing a Snowflake Declarative Native App.
The tutorial uses [Snowflake CLI](/developer-guide/snowflake-cli/index) as well
as a provided workspace directory and a partially complete manifest file to create a Declarative Native App.

This tutorial includes two personas:

- **Provider**: The provider creates a Declarative Native App, creates a listing for it, and shares it with a consumer
- **Consumer**: The consumer installs the Declarative Native App and uses its features and functionality.

### What you’ll learn

As a provider, you will learn how to:

- Create a manifest that declares the data and logic of a Declarative Native App.
- Package and test the app locally.
- Create and share a listing for the app that a consumer can see.

and as a consumer:

- Install a Declarative Native App listing into a test consumer account and explore its features.

### Prerequisites

Before getting started, make sure that you meet the following requirements:

- You are familiar with YAML. YAML is the language used to define the manifest of a Declarative Native App.

  If you are not familiar with YAML, see <https://yaml.org/spec/>.
- You have installed Snowflake CLI.

  Snowflake CLI allows you to manage Snowflake objects and perform various tasks.

  For more information on Snowflake CLI installation, see the [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
- You’ll require access to two Snowflake accounts:

  - **Provider account**, used to create and publish the Declarative Native App.
    This account should have the necessary privileges to create and manage Snowflake objects
    such as databases, schemas, tables, and virtual warehouses.
  - **Consumer account**, a separate test account representing a consumer,
    used to test the Declarative Native App consumer experience.
    This account should have the necessary privileges to install apps and access shared data.

Each section in the tutorial specifies whether the steps should be completed using the provider or consumer account.

In addition, you need to do the following before you start the tutorial:

- Download sample files provided for this exercise.
- Create a database, and tables for this tutorial.

  These are the basic Snowflake objects needed for most Snowflake activities.

## Preparing the tutorial environment

The tutorial provides sample data files and instructions for setting up your local environment.

### Downloading the sample data files

For this tutorial, download the sample data files provided by Snowflake.

To download and unzip the sample data files:

1. Click the name of the
   archive file, [tutorial-getting-started.zip](/static/samples/sa/tutorial-getting-started.zip)
   and save the link/file to your local file system.
2. Unzip the sample files. The tutorial assumes you unpacked files into the following directories:

> - Linux/macOS: `/tmp/tutorial`
> - Windows: `C:\temp\tutorial`

For example, to unzip the file on Linux/macOS, assuming it was downloaded to the
`/tmp` folder, execute the following command:

Copy code

```
unzip /tmp/tutorial-getting-started.zip -d /tmp/tutorial
```

These files include:

- SQL files for creating all required artifacts. These files can be used to speed the process of setting up and tearing down your tutorial environment.
- A workspace directory (*app/workspace*) that contains the content shared by the Declarative Native App: a notebook (`.ipynb`) file and a readme.
- A manifest file that contains the metadata for the Declarative Native App, which you will need to make minor modifications to during the tutorial.
- A sample configuration file for Snowflake CLI, which you can use to configure your Snowflake connection.

### Snowflake CLI configuration

The [Snowflake CLI](/developer-guide/snowflake-cli/index) tool is
required to build, deploy, and install the application in this tutorial.
If you do not have Snowflake CLI on your machine, install it as per instructions
available in [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).

After Snowflake CLI is installed, you need to configure a connection to Snowflake in your
[configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations). This tutorial uses `connections.toml`.
`connections.toml` can be found in:

- macOS: `~/.snowflake/connections.toml`
- Windows: `%USERPROFILE%\.snowflake\connections.toml`.

For more information on configuring Snowflake CLI connections, see [Define connections](/developer-guide/snowflake-cli/connecting/configure-connections#label-snowcli-define-connections).

To add and test a connection:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the lower-left corner, select your name » **Account**, and then select **View account details**.
3. In the **Account Details** dialog, in the **Account** tab, copy the **Account Identifier** value.
4. Using a text editor, open the `connections.toml` file.
5. Add a new connection named `tutorial_connection` to the `connections.toml` file.
   The connection should look similar to:

   Copy code

   ```
   [tutorial_connection]
   account = "your_account_identifier"
   user = "your_username"
   password = "your_password"
   authenticator = "snowflake"
   ```
6. Save the `connections.toml` file.
7. Open a command prompt or terminal window and execute the following command to test the connection:

   Copy code

   ```
   snow connection test
   ```

   If the connection is successful, you should see output similar to:

   ```
   +-------------------------------------------------------------------+
   | key             | value                                           |
   |-----------------+-------------------------------------------------|
   | Connection name | tutorial_connection                             |
   | Status          | OK                                              |
   | Host            | . . .                                           |
   | Account         | . . .                                           |
   | . . .                                                             |
   +-------------------------------------------------------------------+
   ```
8. Optionally, you can use the following to set the default connection for Snowflake CLI.
   Setting the default connection allows you to use the connection name without specifying it in every command.

   Copy code

   ```
   snow connection set-default tutorial_connection
   ```

If you already have a connection configured and would like to use it with this tutorial, use its
name instead of `tutorial_connection` whenever this connection is used in this tutorial.

Note

The `tutorial_connection` connection is used throughout this tutorial to refer to the provider account.
The remainder of this tutorial assumes you have set this as the default connection for Snowflake CLI.

When connecting to the consumer account, you will use Snowsight.
For instructions on how to access Snowsight,
see [Snowflake in 20 minutes: Prerequisites](/user-guide/tutorials/snowflake-in-20minutes#label-tutorial-snowflake-in-20-mins-prerequisites),
and then return to this tutorial.

## Create Snowflake objects

During this step, you, as a provider, will use Snowflake CLI and create the required Snowflake objects.

- A database (`DB_TO_SHARE`)
- A schema (`SCHEMA_TO_SHARE`)
- A table (`TABLE_TO_SHARE`).
- Sample data for the table.

At the completion of this tutorial, you’ll remove these objects.

Note

Commands are shown at the command line using Snowflake CLI as well as in combination using files.

For example, the following command creates a database named `DB_TO_SHARE` using Snowflake CLI and the required connection.

> > Copy code
> >
> > ```
> > snow sql -q "CREATE OR REPLACE DATABASE DB_TO_SHARE"
> > ```
>
> Assuming the same SQL command exists in a text file named `create_db.sql`, you can also run the command using Snowflake CLI as follows:
>
> > Copy code
> >
> > ```
> > snow sql -f create_db.sql
> > ```

Assuming you set a default connection, you can also run the command without specifying the connection:

> Copy code
>
> ```
> snow sql -f create_db.sql
> ```

Review each of the following steps to create the required objects.
Again, as a reminder, a script is provided which can be used to create all the objects in one command.

1. Create the `DB_TO_SHARE` database using the [CREATE DATABASE](/sql-reference/sql/create-database) command:

   Copy code

   ```
   snow sql -q "CREATE OR REPLACE DATABASE DB_TO_SHARE;"
   ```
2. Create the `SCHEMA_TO_SHARE` schema using the [CREATE SCHEMA](/sql-reference/sql/create-schema) command:

   Copy code

   ```
   snow sql -q "CREATE OR REPLACE SCHEMA DB_TO_SHARE.SCHEMA_TO_SHARE;"
   ```

   Note

   The database and schema you just created are now in use for your current session. You can also use the context functions to get this information.
3. Create the table named `TABLE_TO_SHARE` in `SCHEMA_TO_SHARE` using the [CREATE TABLE](/sql-reference/sql/create-table) command:

   Copy code

   ```
   snow sql -q "CREATE OR REPLACE TABLE DB_TO_SHARE.SCHEMA_TO_SHARE.TABLE_TO_SHARE (random_number INTEGER); \
    "
   ```
4. Add data to the table.

   To add a row containing a random value use the [INSERT](/sql-reference/sql/insert) command:

   Copy code

   ```
   snow sql -q "INSERT INTO DB_TO_SHARE.SCHEMA_TO_SHARE.TABLE_TO_SHARE (random_number) \
    SELECT UNIFORM(1, 100, RANDOM()) AS RANDOMNUMBER;"
   ```

   Validate that data was inserted.

   Copy code

   ```
   snow sql -q "SELECT * FROM DB_TO_SHARE.SCHEMA_TO_SHARE.TABLE_TO_SHARE;"
   ```

At this point the backing database, schema, and populated table exist and are ready for use.

To create all the objects in one step, you can use the provided `1.create-database-artifacts.sql`.

For example:

Copy code

```
snow sql  -f /tmp/tutorial/sql/1.create-database-artifacts.sql
```

## Create and package a Declarative Native App

As a provider, create and package the Declarative Native App. Note that this step uses:

- A provided workspace directory, *app/workspace*, that contains the content shared by the Declarative Native App.
  The directory holds a notebook that queries the table created in the previous step, and a readme that describes
  what the app shares.

Creating a Declarative Native App involves:

1. Defining a YAML manifest representing the data and logic in the Declarative Native App.
   A starting point for the manifest is provided in the `manifest.yml` file.
2. Creating the Declarative Native App package.
3. Packaging the app with its manifest and the associated workspace directory.
4. Validating the Declarative Native App package.

See the [Declarative Native App manifest reference](/developer-guide/declarative-sharing/manifest-reference) for a complete list of all required and optional fields.

### Create the application package

To create an app package, you first create an app package project.

SnowsightSnowflake CLI

To use Snowsight to create a new app package:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **App Packages**.
3. In the **Share Data + Code** card, select **Create**.
4. Enter a name for your app package, and then select **Create**.

To use SQL to create a new app package, complete the following procedure in Snowflake CLI, where *<DECL\_SHARE\_APP\_PKG>* is the name of the app package to create:

1. Create a new app package using [CREATE APPLICATION PACKAGE](/developer-guide/declarative-sharing/command-reference#label-dsna-create-application-package). Creating the app package also creates a live version of the app package that you can modify.

   Copy code

   ```
   snow sql -q "CREATE APPLICATION PACKAGE <DECL_SHARE_APP_PKG> TYPE=DATA;"
   ```
2. To verify that your app was created, use [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages):

   Copy code

   ```
   snow sql -q "SHOW APPLICATION PACKAGES LIKE '%DECL_SHARE_%';"
   ```

   This returns a result similar to:

   ```
   +-------------------------------+----------------------+-. . .-+
   | Created_on                    | name                 |       |
   +-------------------------------+----------------------+-. . .-+
   + 2025-06-12 09:40:08.845 -0700 | <DECL_SHARE_APP_PKG> | . . . |
   +-------------------------------+----------------------+-. . .-+
   ```

Once the app package is created, you populate it with the required files.

### Populate the application package

Next, populate the app package with the manifest file and the workspace files.

The `manifest.yml` file provided with this tutorial declares a workspace whose `source` is the
*workspace/* directory:

Copy code

```
application_content:
  workspaces:
    - DS_WORKSPACE:
        source: workspace/
        comment: My first DS app workspace.
```

Because `source` is `workspace/`, the workspace files must be uploaded into a *workspace/* directory
of the package version. Uploading them to the root of the version makes the build fail, because the
declared source directory would be empty.

SnowsightSnowflake CLI

To use Snowsight to populate the app package:

1. In Snowsight, navigate to the listing for the app package you created in the previous step.
2. Select **Manage files**, and then select **Upload files**.
3. Drag the manifest from the */tmp/tutorial/app* folder to the **Upload files** dialog where indicated, or select **Browse** to locate and select the file.
4. Drag the *workspace* folder from */tmp/tutorial/app* to the dialog. The folder structure is preserved, so the files land in a *workspace/* directory.
5. Select **Upload** to upload the files to the live stage and trigger a build.

If the build is successful, the **Live version** tab on the app package’s listing displays the following:

- The last build time
- The contents of the last build, including:

  - A list of the app package’s workspaces
  - A list of shared objects
- A file list of the package’s contents

To use SQL in Snowflake CLI to populate the app package:

1. First, add the workspace files using the commands below. For more information see [PUT](/sql-reference/sql/put).

   The notebook provided with this tutorial queries the table you created previously. The readme
   describes what the app shares.

   Note

   These commands assume the workspace files are in the `/tmp/tutorial/app/workspace` folder. You may need to modify the paths based on where you unzipped the tutorial files.

   Note the `workspace/` suffix on the target URL. It must match the `source` value in the manifest file.

   Copy code

   ```
   snow sql -q "PUT file:////tmp/tutorial/app/workspace/NOTEBOOK.ipynb \
            snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/workspace/ \
            OVERWRITE=TRUE AUTO_COMPRESS=false;"
   ```

   This command will return a result similar to:

   ```
   +----------------------------------------------------------------------------------------------------------------------------+
   | source         | target         | source_size | target_size | source_compression | target_compression | status   | message |
   |----------------+----------------+-------------+-------------+--------------------+--------------------+----------+---------|
   | NOTEBOOK.ipynb | NOTEBOOK.ipynb | 1777        | 1792        | NONE               | NONE               | UPLOADED |         |
   +----------------------------------------------------------------------------------------------------------------------------+
   ```

   Then add the readme:

   Copy code

   ```
   snow sql -q "PUT file:////tmp/tutorial/app/workspace/README.md \
            snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/workspace/ \
            OVERWRITE=TRUE AUTO_COMPRESS=false;"
   ```
2. Add a manifest. Note that this command assumes the manifest is located in the `/tmp/tutorial/app` folder.

   Copy code

   ```
   snow sql -q "PUT file:////tmp/tutorial/app/manifest.yml \
            snow://package/<DECL_SHARE_APP_PKG>/versions/LIVE/ \
            OVERWRITE=TRUE AUTO_COMPRESS=false;"
   ```

   This command will return a result similar to:

   ```
   +------------------------------------------------------------------------------------------------------------------------+
   | source       | target       | source_size | target_size | source_compression | target_compression | status   | message |
   |--------------+--------------+-------------+-------------+--------------------+--------------------+----------+---------|
   | manifest.yml | manifest.yml | 359         | 368         | NONE               | NONE               | UPLOADED |         |
   +------------------------------------------------------------------------------------------------------------------------+
   ```
3. Build the application package.

   Copy code

   ```
   snow sql -q "ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> BUILD;"
   ```

   This returns a result similar to:

   ```
   +----------------------------------------------------------------------------------+
   | status                                                                           |
   |----------------------------------------------------------------------------------|
   | Built the live version of APPLICATION PACKAGE <DECL_SHARE_APP_PKG> successfully. |
   +----------------------------------------------------------------------------------+
   ```

To create, package, and test the app in one step, use the provided `2.create-package-build-app.sql` file
containing all SQL commands to create, package, test a Declarative Native App.

Copy code

```
snow sql  -f /tmp/tutorial/sql/2.create-package-build-app.sql
```

Once the app package has been populated, you can commit and release it.

### Version and release the app

Once an app package has been created and populated with a workspace and manifest, all that remains is to commit (version) and release it.

SnowsightSnowflake CLI

To release a new version of the app package using Snowsight:

1. Within the app package’s listing, select the **Commit & release** button.
2. In the confirmation dialog, select **Acknowledge & continue**.

Once you’ve committed and released the app package, the **Latest release** tab shows the contents of the release, which is the same as the contents of the last build.

To release a new version of the app package using SQL in Snowflake CLI:

- Use the following command:

  Copy code

  ```
  snow sql -q "ALTER APPLICATION PACKAGE <DECL_SHARE_APP_PKG> RELEASE LIVE VERSION;"
  ```

  This returns a result similar to:

  ```
  +---------------------------------------------------------------------------------------------+
  | status                                                                                      |
  |---------------------------------------------------------------------------------------------|
  | Released LIVE version (VERSION$2) of APPLICATION PACKAGE <DECL_SHARE_APP_PKG> successfully. |
  +---------------------------------------------------------------------------------------------+
  ```

  You can also use the provided `3.release-app.sql` file containing SQL commands to release a Declarative Native App.

  Copy code

  ```
  snow sql  -f /tmp/tutorial/sql/3.release-app.sql
  ```

## Test a Declarative Native App

Once a Declarative Native App is packaged and released, the database and logic it contains can be tested locally.

This section describes how to complete the following tasks:

- Create an app from an application package.
- Create a database from an application package.
- Examine the contents of a database created from an application package.

Note

These steps are used by providers to test their app before it is published.

### Create an app from an application package

1. Using the [CREATE APPLICATION](/sql-reference/sql/create-application) command, create an app from an application package using a command similar to:

> Copy code
>
> ```
> snow sql -q "CREATE APPLICATION DECL_SHARE FROM APPLICATION PACKAGE <DECL_SHARE_APP_PKG>;"
> ```

### Examine app contents

You can test your Declarative Native App by examining the contents using either SQL commands or the Snowsight.

Snowflake CLISnowsight

Copy code

```
snow sql -q "USE DATABASE DECL_SHARE;
             DESCRIBE APPLICATION DECL_SHARE; \
             SHOW SCHEMAS IN APPLICATION DECL_SHARE; \
             SHOW TABLES IN APPLICATION DECL_SHARE; \
             SHOW WORKSPACES IN APPLICATION DECL_SHARE; "
```

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. At the top of the navigation menu, select [![Add a dashboard tile](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png)](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png) (**Create**) » **SQL Worksheet**.
3. In the worksheet, enter the following command:

   Copy code

   ```
   USE DATABASE DECL_SHARE;
   DESCRIBE APPLICATION DECL_SHARE;
   SHOW SCHEMAS IN APPLICATION DECL_SHARE;
   SHOW TABLES IN APPLICATION DECL_SHARE;
   SHOW WORKSPACES IN APPLICATION DECL_SHARE;
   ```

Declarative Native Apps include a special schema, `APP$UI`, which holds the app’s bundled content, including its workspaces.

To open the workspace shared by the app:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Workspaces**.
3. Select the **Workspaces** menu, and then select **Shared**.
4. Select the workspace that belongs to the app, and then open `NOTEBOOK.ipynb`.
5. Run the notebook cells. The notebook queries the table that the app shares.

The workspace is read-only, so you can run the notebook but you can’t change it. For more information, see
[Access a shared workspace in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-shared-workspace).

Use the provided `4.test-locally-app.sql` file which contains commands to examine the content of a Declarative Native App.
In addition, the file, `4.test-only-app.sql`, contains commands to test the app but does not attempt to create a database
from the application package.

Copy code

```
snow sql  -f /tmp/tutorial/sql/4.test-locally-app.sql
```

## Share your Declarative Native App using a listing

After successfully creating and testing a Declarative Native App, we can create a listing and add the app as a data product for that listing.
Making the app available as a listing allows other Snowflake users to discover and install the app.

This allows you to share your app with other Snowflake users and allows them to install and use the app in their account.

### Create a listing for your app

Note

The following steps are performed by a provider to create a listing for the Declarative Native App.
The listing is then used by consumers to install the Declarative Native App.

To create a listing for your app:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Provider Studio**.
3. In the **+ Create Listing** menu, select **Specified consumers for selected accounts**.
4. Under **What’s the title of the listing?**, enter `Declarative Sharing Tutorial`.
5. Select **Only Specified Consumers**. Select **Next**.
6. Under **What’s in the listing**, click **+ Select**.
7. Select `DECL_SHARE_APP_PKG`.
8. Optional: Enter a description for your listing.
9. Under **Consumer Data Sharing Account ID**, provide a valid account identifier to share the listing to.

   Note

   The account identifier is a unique identifier for your Snowflake account.
   It is used to identify your account when sharing data and apps with other Snowflake accounts.
   To find your account identifier see [Account identifiers](/user-guide/admin-account-identifier).
10. Select **Publish**.

### Install the app in a consumer account

Important

The consumer account installing an app must specify a default warehouse.

To create a warehouse:

1. in the navigation menu, select **Compute** » **Warehouses**.
2. Click **+ Warehouse**.
3. Configure the warehouse as needed.

To set a default warehouse:

1. in the lower-left corner, select your name » **Settings**, and then select **Preferences**.
2. Select warehouse from the **Default Warehouse** drop-down list.

To install your app from the listing:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Apps**.
3. Select the tile for the listing under Recently shared with you.
4. Select **Get**.
5. Select **Options** and enter a name for the app. For this tutorial, use `DeclarativeAppConsumer`.
6. Select the warehouse where you want to install the app.
7. Select **Get**.
8. Select **Open** to view your listing or **Done** to finish.
9. Explore the listing as you would any other listing.

   For more information see [Access content in a Declarative Native App](/developer-guide/declarative-sharing/consumer/access-app-content).

## Summary, clean up, and additional resources

Congratulations! You’ve successfully completed this tutorial.

Take a few minutes to review a short summary and the key points covered in the tutorial.

You might also want to consider cleaning up by dropping any objects you created in the tutorial. Learn more by reviewing other topics in the Snowflake Documentation.

### Summary and key points

In summary, Declarative Native Apps:

- Can be easily used to expose databases, tables, views, and schemas.
- Have a well-defined lifecycle.
- Can be accessed by consumers using [listings](/collaboration/collaboration-listings-about) or an app.

### Clean up (optional)

On the consumer account used to install the Declarative Native App, to uninstall the listing, follow these steps:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Apps**.
3. In the row for `DeclarativeAppConsumer` on the **…** menu, select **Uninstall**.

If the objects you created in this tutorial are no longer needed, you can remove them from the system using the following commands:

As the provider who originally created the objects, run the following commands using Snowflake CLI:

> Copy code
>
> ```
> snow sql -q "DROP LISTING IF EXISTS DECLARATIVE_APP_TUTORIAL; \
>              DROP APPLICATION IF EXISTS DECL_SHARE; \
>              DROP APPLICATION PACKAGE IF EXISTS DECL_SHARE_APP_PKG; \
>              DROP TABLE IF EXISTS DB_TO_SHARE.SCHEMA_TO_SHARE.TABLE_TO_SHARE; \
>              DROP SCHEMA IF EXISTS DB_TO_SHARE.SCHEMA_TO_SHARE; \
>              DROP DATABASE IF EXISTS DB_TO_SHARE; "
> ```

For simplicity, you can use the provided `teardown-tutorial.sql` file containing all SQL commands to remove the objects created in this tutorial.

> Copy code
>
> ```
> snow sql  -f /tmp/tutorial/sql/teardown-tutorial.sql
> ```

## Learn more

To learn more about Declarative Native Apps, see the following topics:

- [About Declarative Sharing in the Native Application Framework](/developer-guide/declarative-sharing/about)
