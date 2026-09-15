# Packaging Java or Scala Handler Code with Maven

If you are using Maven to build and package your code, you can use the
[Maven Assembly Plugin](https://maven.apache.org/plugins/maven-assembly-plugin/index.html) to create a JAR file that contains
all of the dependencies.

Once you have a JAR file, you can upload the file to a Snowflake stage, then reference it in an IMPORTS statement when you create a
function or procedure. For more information on uploading JAR files, refer to [Making dependencies available to your code](/developer-guide/upload-dependencies). For more
information on choosing whether to have code inline or on a stage, refer to [Keeping handler code in-line or on a stage](/developer-guide/inline-or-staged).

To create an JAR file with your handler code, use the following steps.

1. In the directory for your project (for example, `hello-snowpark/`), create a subdirectory named `assembly/`.
2. In that directory, create an
   [assembly descriptor file](https://maven.apache.org/plugins/maven-assembly-plugin/assembly.html)
   that specifies that you want to include dependencies in your JAR file.

   For an example, see
   [jar-with-dependencies](https://maven.apache.org/plugins/maven-assembly-plugin/descriptor-refs.html#jar-with-dependencies).
3. If your project requires the Snowpark library, exclude its JAR file from the output archive because the library is already included on
   Snowflake.

   In the assembly descriptor, add a `<dependencySet>` element that excludes the Snowpark library from your JAR file.

   For example:

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
      <useProjectArtifact>false</useProjectArtifact>
      <unpack>true</unpack>
      <scope>provided</scope>
      <excludes>
        <exclude>com.snowflake:snowpark</exclude>
      </excludes>
    </dependencySet>
     </dependencySets>
   </assembly>
   ```

   For information about the elements in an assembly descriptor, see
   [Assembly Descriptor Format](https://maven.apache.org/plugins/maven-assembly-plugin/assembly.html).
4. In your `pom.xml` file, under the `<project>` » `<build>` » `<plugins>`, add a `<plugin>`
   element for the Maven Assembly Plugin.

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
