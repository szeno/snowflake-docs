# Setting Up Other Development Environments for Snowpark Scala

If you are using a development environment not covered earlier (see [Setting Up Your Development Environment for Snowpark Scala](/developer-guide/snowpark/scala/setup)), see the instructions in this topic for
configuring your environment to use Snowpark.

## Using the Snowpark Library in an sbt Build File

To integrate the Snowpark library into a project that uses an sbt build file, add the library as a dependency.

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

## Using the Snowpark Library in a Maven Project

To integrate the Snowpark library into a Maven project, add the library as a dependency to your `pom.xml` file. For example:

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

Set the `<version>` tag to the version of the library that you want to use. Note that version 1.18.0 is
used in this example for illustration purposes only. The latest available version of the driver may be higher.

## Downloading the Snowpark Library and its Dependencies

If you are not using sbt or Maven to manage the dependencies for your application and you need a copy of the Snowpark library and
its dependencies, you can download a TAR archive file or a zip file that contains the JAR files for the library and all of
its dependencies. The TAR/ZIP archive includes the API reference documentation in scaladoc format.

To download the Snowpark library:

1. Go to the [Snowpark Client Download](https://developers.snowflake.com/snowpark/) page, and find the version that you want to use.
2. Browse to the directory for the version that you want to use.

   The rest of the steps use 1.18.0 as an example.
3. Download the snowpark\_2.12-1.18.0-bundle.tar.gz (or .zip) file.

   Note

   As of Snowpark 0.9.0, rather than downloading an archive file that contains the Snowpark library and its dependencies in
   separate JAR files, you can choose to download a single JAR file that contains the Snowpark library and its dependencies.
   This JAR file is named snowpark\_2.12-1.18.0-with-dependencies.jar.

   If you download this JAR file, skip the rest of the steps. (The steps apply to the archive file.)
4. If you want to verify the signature of the file:

   1. Download the snowpark\_2.12-1.18.0-bundle.tar.gz.asc file.
   2. From the public keyserver, download and import the Snowflake GPG public key for the version of the library that you are
      using:

      - For version 1.17.0 and higher:

        ```
        $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 2A3149C82551A34A
        ```
      - For version 1.15.0:

        ```
        $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 5A125630709DD64B
        ```
      - For version 1.6.1 through 1.14.0:

        ```
        $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 630D9F3CAB551AF3
        ```
      - For version 0.6.0 through 1.6.0:

        ```
        $ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys 37C7086698CB005C
        ```

        Note

        If this command fails with the following error:

        > Copy code
        >
        > ```
        > gpg: keyserver receive failed: Server indicated a failure
        > ```

        then specify that you want to use port 80 for the keyserver:

        > Copy code
        >
        > ```
        > gpg --keyserver hkp://keyserver.ubuntu.com:80  ...
        > ```
   3. Run the `gpg --verify` command to verify the signature. For example:

      ```
      gpg --verify snowpark_2.12-1.18.0-bundle.tar.gz.asc snowpark_2.12-1.18.0-bundle.tar.gz
      ```

      The output of the command should indicate that the archive file was signed with this key.

      Note

      Verifying the signature produces a warning similar to the following:

      > Copy code
      >
      > ```
      > gpg: Signature made Mon 24 Sep 2018 03:03:45 AM UTC using RSA key ID <gpg_key_id>
      > gpg: Good signature from "Snowflake Computing <snowflake_gpg@snowflake.net>" unknown
      > gpg: WARNING: This key is not certified with a trusted signature!
      > gpg: There is no indication that the signature belongs to the owner.
      > ```

      To avoid the warning, you can grant the Snowflake GPG public key implicit trust.
5. Extract the contents of the archive file.

   The README.txt file in the archive file describes the contents of each directory.
6. Add the following extracted file and directory to the classpath for building and running your application:

   - The snowpark\_2.12-1.18.0.jar file
   - The lib directory
