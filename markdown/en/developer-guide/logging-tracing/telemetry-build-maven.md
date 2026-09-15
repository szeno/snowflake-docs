# Setting up your Java and Scala environment to use the Telemetry class

You can build and package handler code that uses the `com.snowflake.telemetry.Telemetry` class, then reference the handler on a stage.
The Telemetry library is available through Maven and through an archive file that you can download from the
[Drivers and Libraries page](https://developers.snowflake.com/drivers-and-libraries/) in the Snowflake Developer site.

If you are using Maven to develop function or procedure handlers in Java or Scala, you can build a JAR file containing your code:

1. In the pom.xml file for your project, add a dependency on the `com.snowflake:telemetry` package:

   Copy code

   ```
   <dependency>
     <groupId>com.snowflake</groupId>
     <artifactId>telemetry</artifactId>
     <version>0.01</version>
   </dependency>
   ```
2. Exclude the `telemetry` package from the JAR file that you build because it is already included in Snowflake.

   1. In the directory for your project, create a subdirectory named `assembly/`.
   2. In that directory, create an assembly descriptor file that specifies that you want to include dependencies in your JAR file.

      For an example, see [jar-with-dependencies](https://maven.apache.org/plugins/maven-assembly-plugin/descriptor-refs.html#jar-with-dependencies).
   3. In the assembly descriptor, add a `<dependencySet>` element that excludes the Snowpark library from your JAR file. For example:

      Copy code

      ```
      <assembly xmlns="http://maven.apache.org/ASSEMBLY/2.1.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/ASSEMBLY/2.1.0 http://maven.apache.org/xsd/assembly-2.1.0.xsd">
        <id>jar-with-dependencies</id>
        <formats>
      <format>jar</format>
        </formats>
        <includeBaseDirectory>false</includeBaseDirectory>
        <dependencySets>
          <dependencySet>
      <outputDirectory>/</outputDirectory>
      <useProjectArtifact>true</useProjectArtifact>
      <unpack>true</unpack>
      <scope>runtime</scope>
      <excludes>
        <exclude>com.snowflake:telemetry</exclude>
      </excludes>
          </dependencySet>
        </dependencySets>
      </assembly>
      ```

      For information about the elements in an assembly descriptor, see
      [Assembly Descriptor Format](https://maven.apache.org/plugins/maven-assembly-plugin/assembly.html).
3. In your pom.xml file, under the `<project>` » `<build>` » `<plugins>`, add a `<plugin>` element for the
   Maven Assembly Plugin.

   In addition, under `<configuration>` » `<descriptors>`, add a `<descriptor>` that points to the assembly
   descriptor file that you created in the previous steps.

   For example:

   Copy code

   ```
   <project>
     [...]
     <build>
    [...]
    <plugins>
      <plugin>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.3.0</version>
        <configuration>
          <descriptors>
            <descriptor>src/assembly/jar-with-dependencies.xml</descriptor>
          </descriptors>
        </configuration>
        [...]
      </plugin>
      [...]
    </plugins>
    [...]
     </build>
     [...]
   </project>
   ```
