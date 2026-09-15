# Setting Up the SBT REPL for Snowpark Scala

This topic explains how to set up the SBT REPL for Snowpark.

## Creating a New Scala Project in sbt

Next, create a new Scala project for Snowpark.

1. Create a new directory for your project, and change to that directory.

   Copy code

   ```
   mkdir snowpark_project
   cd snowpark_project
   ```
2. Run the `sbt new` command, and specify the [template](https://www.scala-sbt.org/1.x/docs/sbt-new-and-Templates.html)
   that you want to use to create the new project. For example:

   Copy code

   ```
   sbt new scala/hello-world.g8
   ```

   Enter a name for your project. This creates a project directory with that name.

## Configuring the sbt Project for Snowpark

Next, configure the project for Snowpark.

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

1. Add the following lines to configure the REPL:

   Copy code

   ```
   Compile/console/scalacOptions += "-Yrepl-class-based"
   Compile/console/scalacOptions += "-Yrepl-outdir"
   Compile/console/scalacOptions += "repl_classes"
   ```

## Verifying Your sbt Project Configuration

To verify that you have configured your project to use Snowpark, run a simple example of Snowpark code.

1. In the `src/main/scala/Main.scala` file, replace the contents with the code below:

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
2. Change to your project directory, and run the following command to run the sample code:

   Copy code

   ```
   sbt "runMain Main"
   ```
