# Setting Up IntelliJ IDEA CE for Snowpark Scala

This topic explains how to set up IntelliJ IDEA CE for Snowpark.

## Setting Up IntelliJ IDEA CE for Scala Development

To use Scala in IntelliJ IDEA CE, you need to install the Scala plugin. See the
[Installation section](https://docs.scala-lang.org/getting-started/intellij-track/getting-started-with-scala-in-intellij.html#installation)
of the tutorial
[Getting Started with Scala in IntelliJ IDEA](https://docs.scala-lang.org/getting-started/intellij-track/getting-started-with-scala-in-intellij.html).

## Creating a New Scala Project in IntelliJ IDEA

Next, create a new Scala project for Snowpark.

1. Choose **File** » **New** » **Project**.

   1. In the list on the left, select Scala.
   2. In the list on the right, select sbt.

      ![Window for selecting the type of project to create](/static/images/screens/intellij-create-new-project-1.png)
   3. Click **Next**.
2. Fill in the details for your new project.

   For the JDK and Scala SDK, select the [JDK and Scala versions supported for use with Snowpark](/developer-guide/snowpark/scala/prerequisites).
3. Click **Finish** to create the new project.

## Configuring the IntelliJ IDEA Project for Snowpark

Next, configure the project for Snowpark.

1. In the **Project** tool window on the
   [left](https://www.jetbrains.com/help/idea/2020.3/guided-tour-around-the-user-interface.html), double-click on the
   `build.sbt` file for your project.

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
2. Save the changes to the `build.sbt` file.
3. Update your Maven repositories.

   See [Update Maven repositories](https://www.jetbrains.com/help/idea/troubleshooting-common-maven-issues.html#5e1bf655).
4. Reload the SBT project:

   1. Choose **View** » **Tool Windows** » **sbt** to display the **sbt Tool** window.
   2. Right-click on the project name, and choose **Reload sbt Project**.

   This causes IntelliJ IDEA CE to download the Snowpark library and makes the API available for use in your code.

## Verifying Your IntelliJ IDEA Project Configuration

To verify that you have configured your project to use Snowpark, run a simple example of Snowpark code.

1. In the **Project** tool window on the
   [left](https://www.jetbrains.com/help/idea/2020.3/guided-tour-around-the-user-interface.html),
   expand your project, expand the `src/main` folders, and select the `scala` folder.
2. Right-click on the folder, and choose **New** » **Scala class**.
3. In the **Create New Scala Class** dialog box, enter the name “Main”, select **Object**, and press the Enter key.
4. In the `Main.scala` file, replace the contents with the code below:

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
5. Click the green arrow next to the `Object` line, and choose **Run Main** to run the example.

   ![Arrow icon for running the sample program](/static/images/screens/intellij-run-program-arrow.png)
