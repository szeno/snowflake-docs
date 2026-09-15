# Setting Up IntelliJ IDEA CE for Snowpark Java

This topic explains how to set up IntelliJ IDEA CE for Snowpark.

## Creating a New Maven Project in IntelliJ IDEA

Create a new Maven project for Snowpark.

1. Choose **File** » **New** » **Project**.
2. From the **Project SDK** menu, select 11 (for Java version 11).

   Note that you don’t need to select an archetype. You can just leave the **Create from archetype** box unchecked.
3. Click **Next**.
4. Enter a name and location for your project (e.g. `hello-snowpark`).
5. Click **Finish** to create the new project.

## Configuring the IntelliJ IDEA Project for Snowpark

Next, configure the project for Snowpark.

1. Open the `pom.xml` file for the project.
2. In the `<project>` tag, add the tags to specify a dependency on the Snowpark library:

   ```
   <dependencies>
     ...
     <dependency>
       <groupId>com.snowflake</groupId>
       <artifactId>snowpark_2.12</artifactId>
       <version>1.18.0</version>
     </dependency>
     ...
   </dependencies>
   ```
3. Save the changes to the `pom.xml` file.
4. Update your Maven repositories.

   See [Update Maven repositories](https://www.jetbrains.com/help/idea/troubleshooting-common-maven-issues.html#5e1bf655).

## Verifying Your IntelliJ IDEA Project Configuration

To verify that you have configured your project to use Snowpark, run a simple example of Snowpark code.

1. In the **Project** tool window on the
   [left](https://www.jetbrains.com/help/idea/2020.3/guided-tour-around-the-user-interface.html),
   expand your project, expand the `src/main` folders, and select the `java` folder.
2. Right-click on the folder, and choose **New** » **Java class**.
3. In the **New Java Class** dialog box, enter the name “HelloSnowpark”, select **Class**, and press the Enter key.
4. In the `HelloSnowpark.java` file, replace the contents with the code below:

   Copy code

   ```
   import com.snowflake.snowpark_java.*;
   import java.util.HashMap;
   import java.util.Map;

   public class HelloSnowpark {
     public static void main(String[] args) {
       // Replace the <placeholders> below.
       Map<String, String> properties = new HashMap<>();
       properties.put("URL", "https://<account_identifier>.snowflakecomputing.com:443");
       properties.put("USER", "<user name>");
       properties.put("PASSWORD", "<password>");
       properties.put("ROLE", "<role name>");
       properties.put("WAREHOUSE", "<warehouse name>");
       properties.put("DB", "<database name>");
       properties.put("SCHEMA", "<schema name>");
       Session session = Session.builder().configs(properties).create();
       session.sql("show tables").show();
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
5. Click the green arrow next to the `Class` line, and choose **Run HelloSnowpark.main()** to run the example.
