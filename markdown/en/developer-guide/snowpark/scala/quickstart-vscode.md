# Setting Up Visual Studio Code for Snowpark Scala

This topic explains how to set up Visual Studio Code for Snowpark.

## Setting Up Visual Studio Code for Scala Development

For convenience when writing Scala code in Visual Studio Code, install the
[Metals extension](https://scalameta.org/metals/docs/editors/vscode.html). The Metals extension provides code completion,
parameter hints, and information about types and methods.

To install the Metals extension:

1. In the **Activity Bar** on the [left side of the window](https://code.visualstudio.com/docs/getstarted/userinterface), click the **Extensions** icon.

   ![Extensions icon in the Activity Bar in Visual Studio Code](/static/images/screens/vscode-extensions-button.png)

   (If the **Activity Bar** isn’t displayed, make sure that **View** » **Appearance** »
   **Show Activity Bar** is checked.)

   This displays the **Extensions** view, which allows you to browse and install extensions from the Extensions Marketplace.
2. In the search box for **Search Extensions in Marketplace**, search for the term:

   Copy code

   ```
   metals
   ```
3. In the search results, find the Scala (Metals) extension, and click **Install**.

For more information about the Scala (Metals) extension, see
[Visual Studio Code](https://scalameta.org/metals/docs/editors/vscode.html) in the
[Metals documentation](https://scalameta.org/metals/docs/editors/overview.html).

## Creating a New Scala Project in Visual Studio Code

Next, create a new Scala project for Snowpark.

1. Create a workspace directory for your projects. For example:

   Copy code

   ```
   mkdir snowpark_projects
   ```

   This directory will contain subdirectories for the projects that you create.
2. In Visual Studio Code, choose **File** » **Open**, select the directory that you created, and click **Open**.
3. In the **Activity Bar** on the left, click the **Metals** icon.

   ![Metals extension icon in the Activity Bar in Visual Studio Code](/static/images/screens/vscode-metals-extension-button.png)
4. Under **Packages** in the **Side Bar** ([to the right](https://code.visualstudio.com/docs/getstarted/userinterface) of the **Activity Bar**), click the
   **New Scala Project** button.

   ![Button to create a new Scala project Visual Studio Code](/static/images/screens/vscode-new-scala-project-button.png)
5. Select a template to use for the new project (e.g. `scala/hello-world.g8`).
6. Select the workspace directory that you created earlier (`snowpark_projects`), and click **Ok**.
7. Enter a name for the new project (e.g. `hello_snowpark`).
8. When prompted by the dialog box in the lower right corner of the window, click **Yes** to open the new project in a new
   window.

   ![Dialog box prompting you to open the new project in a new window](/static/images/screens/vscode-open-new-project.png)
9. When prompted by the dialog box in the lower right corner of the window, click **Import build** to
   [import the build](https://scalameta.org/metals/docs/editors/vscode.html#importing-a-build).

   ![Dialog box prompting you to import the build for the new project](/static/images/screens/vscode-import-build-new-project.png)

## Configuring the Visual Studio Code Project for Snowpark

Next, configure the project for Snowpark.

1. In the **Activity Bar** on the [left side of the window](https://code.visualstudio.com/docs/getstarted/userinterface), make sure that the **Explorer** icon (the first icon at
   the top) is selected.

   ![Explorer icon selected in the Activity Bar in Visual Studio Code](/static/images/screens/vscode-explorer-icon-selected.png)
2. Under **Explorer** in the **Side Bar** ([to the right](https://code.visualstudio.com/docs/getstarted/userinterface) of the **Activity Bar**), under your project, select
   the `build.sbt` file for editing.

   ![Selecting the build.sbt file for editing](/static/images/screens/vscode-select-build-sbt-file.png)

   In the `build.sbt` file for your project, make the following changes:

   1. If the `scalaVersion` setting does not match the version that you plan to use, update the setting. For example:

      Copy code

      ```
      scalaVersion := "2.12.20"
      ```

      Note that you must use a
      [Scala version that is supported for use with the Snowpark library](/developer-guide/snowpark/scala/prerequisites#label-snowpark-supported-languages).
   2. Add the Snowpark library to the list of dependencies. For example:

      ```
      libraryDependencies += "com.snowflake" % "snowpark_2.12" % "1.18.0"
      ```
3. After making those changes, choose **File** » **Save** to save your changes.
4. When prompted by the dialog box in the lower right corner of the window, click **Import changes** to
   [re-import the file](https://scalameta.org/metals/docs/editors/vscode.html#importing-changes).

   ![Dialog box prompting you to re-import the build.sbt file](/static/images/screens/vscode-reimport-build-sbt-file.png)

## Verifying Your Visual Studio Code Project Configuration

To verify that you have configured your project to use Snowpark, run a simple example of Snowpark code.

1. In the **Activity Bar** on the [left side of the window](https://code.visualstudio.com/docs/getstarted/userinterface), make sure that the **Explorer** icon (the first icon at
   the top) is selected.

   ![Explorer icon selected in the Activity Bar in Visual Studio Code](/static/images/screens/vscode-explorer-icon-selected.png)
2. Under **Explorer** in the **Side Bar**, under your project, expand the `src/main/scala` folder, and select and open
   the `Main.scala` file.
3. In the `Main.scala` file, replace the contents with the code below:

   Copy code

   ```
   import com.snowflake.snowpark._
   import com.snowflake.snowpark.functions._

   object Main {
     def main(args: Array[String]): Unit = {
       // Replace the <placeholders> below.
       val configs = Map (
         "URL" -> "https://<account_identifier>.snowflakecomputing.com:443",
         "USER" -> "<user name>",
         "PASSWORD" -> "<password>",
         "ROLE" -> "<role name>",
         "WAREHOUSE" -> "<warehouse name>",
         "DB" -> "<database name>",
         "SCHEMA" -> "<schema name>"
       )
       val session = Session.builder.configs(configs).create
       session.sql("show tables").show()
     }
   }
   ```

   Note the following:

   - Replace the `placeholders` with values that you use to connect to Snowflake.
   - For `account_identifier`, specify your [account identifier](/user-guide/admin-account-identifier).
   - If you prefer to use [key pair authentication](/user-guide/key-pair-auth):

     - Replace `PASSWORD` with `PRIVATE_KEY_FILE`, and set it to the path to your private key file.
     - If the private key is encrypted, you must set `PRIVATE_KEY_FILE_PWD` to the passphrase for decrypting the private key.

     As an alternative to setting `PRIVATE_KEY_FILE` and `PRIVATE_KEY_FILE_PWD`, you can set the `PRIVATEKEY`
     property to the string value of the unencrypted private key from the private key file.

     - For example, if your private key file is unencrypted, set this to the value of the key in the file (without the
       `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` header and footer and without the line endings).
     - Note that if the private key is encrypted, you must decrypt the key before setting it as the value of the `PRIVATEKEY`
       property.

   - If you plan to create UDFs:
     - Don’t set up your `object` to extend the `App` trait. For details, see
       [Caveat About Creating UDFs in an Object With the App Trait](/developer-guide/snowpark/scala/creating-udfs#label-snowpark-udf-inline-scala-app-trait).
     - Don’t set up your `object` to extend a class or trait that is not serializable.
4. Click **run** above the `Object` line to run the example.

If the following error message appears:

Copy code

```
Run session not started
```

check the **Problems** tab in the bottom of the window. If this tab does not appear in the bottom of the window, select the
**View > Problems** item from the menu.
