Important

- Advance notice: The classic Kafka connector (v3 and earlier) is fully supported today,
  but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe
  and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026.
  After the announcement, an 18-month migration window begins before end-of-life.
- Recommendation: Use the
  [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
  for all new implementations.

For migration guidance, see [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

# Loading protobuf data using the Snowflake Connector for Kafka

This topic provides instructions for installing and configuring protocol buffers (protobuf) support in the Snowflake Connector for Kafka (“Kafka connector”). Support for protobuf requires Kafka connector 1.5.0 (or higher).

The Kafka connector supports the following versions of the protobuf converter:

Confluent version:
:   This version is supported by the Confluent package version of Kafka only.

Community version:
:   This version is supported by the open source software (OSS) Apache Kafka package. This version is also supported by the Confluent package version of Kafka; however, for ease of use, we suggest using the Confluent version instead.

Install only one of these protobuf converters.

## Prerequisite: Installing the Snowflake Connector for Kafka

Install the Kafka connector using the instructions in [Installing and configuring the Kafka connector](/user-guide/kafka-connector/classic/install).

## Configuring the Confluent version of the protobuf converter

Note

The Confluent version of the Protobuf converter is available with Confluent version 5.5.0 (or higher).

1. Open your Kafka configuration file (e.g. `<kafka_dir>/config/connect-distributed.properties`) in a text editor.
2. Configure the converter properties in the file. For information about the Kafka connector properties in general, see [Kafka configuration properties](/user-guide/kafka-connector-install#label-kafka-properties).

   Copy code

   ```
   {
    "name":"XYZCompanySensorData",
   "config":{
     ..
     "key.converter":"io.confluent.connect.protobuf.ProtobufConverter",
     "key.converter.schema.registry.url":"CONFLUENT_SCHEMA_REGISTRY",
     "value.converter":"io.confluent.connect.protobuf.ProtobufConverter",
     "value.converter.schema.registry.url":"http://localhost:8081"
   }
    }
   ```

   For example:

   Copy code

   ```
   {
     "name":"XYZCompanySensorData",
     "config":{
    "connector.class":"com.snowflake.kafka.connector.SnowflakeSinkConnector",
    "tasks.max":"8",
    "topics":"topic1,topic2",
    "snowflake.topic2table.map": "topic1:table1,topic2:table2",
    "buffer.count.records":"10000",
    "buffer.flush.time":"60",
    "buffer.size.bytes":"5000000",
    "snowflake.url.name":"myorganization-myaccount.snowflakecomputing.com:443",
    "snowflake.user.name":"jane.smith",
    "snowflake.private.key":"xyz123",
    "snowflake.private.key.passphrase":"jkladu098jfd089adsq4r",
    "snowflake.database.name":"mydb",
    "snowflake.schema.name":"myschema",
    "key.converter":"io.confluent.connect.protobuf.ProtobufConverter",
    "key.converter.schema.registry.url":"CONFLUENT_SCHEMA_REGISTRY",
    "value.converter":"io.confluent.connect.protobuf.ProtobufConverter",
    "value.converter.schema.registry.url":"http://localhost:8081"
     }
   }
   ```
3. Save the file.

Produce protobuf data from Kafka using the Confluent console protobuf producer, the source protobuf producer, or the Python producer.

Example Python code located in [GitHub](https://github.com/snowflakedb/snowflake-kafka-connector/blob/3bb3e0491d932cdbc58fba3efc0f5c71fa341429/test/test_suit/test_confluent_protobuf_protobuf.py) demonstrates how to produce protobuf data from Kafka.

## Configuring the community version of the protobuf converter

This section provides instructions for installing and configuring the community version of the protobuf converter.

### Step 1: Installing the community protobuf converter

1. In a terminal window, change to the directory where you want to store a clone of the GitHub repository for the protobuf converter.
2. Execute the following command to clone the [GitHub repository](https://github.com/blueapron/kafka-connect-protobuf-converter):

   Copy code

   ```
   git clone https://github.com/blueapron/kafka-connect-protobuf-converter
   ```
3. Execute the following commands to build the 3.1.0 version of the converter using [Apache Maven](https://maven.apache.org/). Note that versions 2.3.0, 3.0.0, and 3.1.0 of the converter are supported by the Kafka connector:

   Note

   Maven must already be installed on your local machine.

   Copy code

   ```
   cd kafka-connect-protobuf-converter

   git checkout tags/v3.1.0

   mvn clean package
   ```

   Maven builds a file named `kafka-connect-protobuf-converter-<version>-jar-with-dependencies.jar` in the current folder. This is the converter JAR file.
4. Copy the compiled `kafka-connect-protobuf-converter-<version>-jar-with-dependencies.jar` file to the directory for your Kafka package version:

   Confluent:
   :   `<confluent_dir>/share/java/kafka-serde-tools`

   Apache Kafka:
   :   `<apache_kafka_dir>/libs`

### Step 2: Compiling your .proto file

Compile the protobuf `.proto` file that defines your messages into a `java` file.

For example, suppose your messages are defined in a file named `sensor.proto`. In a terminal window, execute the following command to compile the protocol buffers file. Specify the source directory for the application source code, the destination directory (for the `.java` file), and the path to your `.proto` file:

Copy code

```
protoc -I=$SRC_DIR --java_out=$DST_DIR $SRC_DIR/sensor.proto
```

A sample `.proto` file is available here: <https://github.com/snowflakedb/snowflake-kafka-connector/blob/master/test/test_data/sensor.proto>.

The command generates a file named `SensorReadingImpl.java` in the specified destination directory.

For more information, see the [Google developer documentation](https://developers.google.com/protocol-buffers/docs/javatutorial)

### Step 3: Compiling the SensorReadingImpl.Java file

Compile the generated `SensorReadingImpl.java` file from [Step 2: Compiling Your .proto File](#step-2-compiling-your-proto-file) along with the Project Object Model of the protobuf project structure.

1. Open your `.pom` file from [Step 2: Compiling Your .proto File](#step-2-compiling-your-proto-file) in a text editor.
2. Create an otherwise empty directory with a structure:

   Copy code

   ```
   protobuf_folder
   ├── pom.xml
   └── src
    └── main
        └── java
            └── com
                └── ..
   ```

   Where the directory structure under `src` / `main` / `java` mirrors the package name in your `.proto` file (line 3).
3. Copy the generated `SensorReadingImpl.java` file from [Step 2: Compiling Your .proto File](#step-2-compiling-your-proto-file) to the bottom folder in the directory structure.
4. Create a file named `pom.xml` in the root of the `protobuf_folder` directory.
5. Open the empty `pom.xml` file in a text editor. Copy the following example project model into the file and modify it:

   Copy code

   ```
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>

   <groupId><group_id></groupId>
   <artifactId><artifact_id></artifactId>
   <version><version></version>

   <properties>
       <java.version><java_version></java.version>
       <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
   </properties>

   <dependencies>
       <dependency>
           <groupId>com.google.protobuf</groupId>
           <artifactId>protobuf-java</artifactId>
           <version>3.11.1</version>
       </dependency>
   </dependencies>

   <build>
       <plugins>
           <plugin>
               <groupId>org.apache.maven.plugins</groupId>
               <artifactId>maven-compiler-plugin</artifactId>
               <version>3.3</version>
               <configuration>
                   <source>${java.version}</source>
                   <target>${java.version}</target>
               </configuration>
           </plugin>
           <plugin>
               <artifactId>maven-assembly-plugin</artifactId>
               <version>3.1.0</version>
               <configuration>
                   <descriptorRefs>
                       <descriptorRef>jar-with-dependencies</descriptorRef>
                   </descriptorRefs>
               </configuration>
               <executions>
                   <execution>
                       <id>make-assembly</id>
                       <phase>package</phase>
                       <goals>
                           <goal>single</goal>
                       </goals>
                   </execution>
               </executions>
           </plugin>
       </plugins>
   </build>
   </project>
   ```

   Where:

   `<group_id>`
   :   Group ID segments of the package name specified in your `.proto` file. For example, if the package name is `com.foo.bar.buz`, then the group ID is `com.foo`.

   `<artifact_id>`
   :   Artifact ID for the package that you choose. The artifact ID can be randomly picked.

   `<version>`
   :   Version of the package that you choose. The version can be randomly picked.

   `<java_version>`
   :   Version of the Java Runtime Environment (JRE) installed on your local machine.

   For example:

   Copy code

   ```
   <?xml version="1.0" encoding="UTF-8"?>
   <project xmlns="http://maven.apache.org/POM/4.0.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
   <modelVersion>4.0.0</modelVersion>

   <groupId>com.snowflake</groupId>
   <artifactId>kafka-test-protobuf</artifactId>
   <version>1.0.0</version>

   <properties>
       <java.version>1.8</java.version>
       <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
   </properties>

   <dependencies>
       <dependency>
           <groupId>com.google.protobuf</groupId>
           <artifactId>protobuf-java</artifactId>
           <version>3.11.1</version>
       </dependency>
   </dependencies>

   <build>
       <plugins>
           <plugin>
               <groupId>org.apache.maven.plugins</groupId>
               <artifactId>maven-compiler-plugin</artifactId>
               <version>3.3</version>
               <configuration>
                   <source>${java.version}</source>
                   <target>${java.version}</target>
               </configuration>
           </plugin>
           <plugin>
               <artifactId>maven-assembly-plugin</artifactId>
               <version>3.1.0</version>
               <configuration>
                   <descriptorRefs>
                       <descriptorRef>jar-with-dependencies</descriptorRef>
                   </descriptorRefs>
               </configuration>
               <executions>
                   <execution>
                       <id>make-assembly</id>
                       <phase>package</phase>
                       <goals>
                           <goal>single</goal>
                       </goals>
                   </execution>
               </executions>
           </plugin>
       </plugins>
   </build>
   </project>
   ```
6. In a terminal window, change to the root of the `protobuf_folder` directory. Execute the following command to compile the protobuf data JAR file from the files in the directory:

   Copy code

   ```
   mvn clean package
   ```

   Maven generates a file named `<artifact_id>-<version>-jar-with-dependencies.jar` in the `protobuf_folder/target` folder (e.g. `kafka-test-protobuf-1.0.0-jar-with-dependencies.jar`).
7. Copy the compiled `kafka-test-protobuf-1.0.0-jar-with-dependencies.jar` file to the directory for your Kafka package version:

   Confluent:
   :   `<confluent_dir>/share/java/kafka-serde-tools`

   Apache Kafka:
   :   Copy the file to the directory in your `$CLASSPATH` environment variable.

### Step 4: Configuring the Kafka connector

1. Open your Kafka configuration file (e.g. `<kafka_dir>/config/connect-distributed.properties`) in a text editor.
2. Add the `value.converter.protoClassName` property to the file. This property specifies the protocol buffer class to use to deserialize messages (e.g. `com.google.protobuf.Int32Value`).

   Note

   Nested classes must be specified using the `$` notation (e.g. `com.blueapron.connect.protobuf.NestedTestProtoOuterClass$NestedTestProto`).

   For example:

   Copy code

   ```
   {
    "name":"XYZCompanySensorData",
   "config":{
     ..
     "value.converter.protoClassName":"com.snowflake.kafka.test.protobuf.SensorReadingImpl$SensorReading"
   }
    }
   ```

   For information about the Kafka connector properties in general, see [Kafka configuration properties](/user-guide/kafka-connector-install#label-kafka-properties).

   For more information about protocol buffer classes, see the Google developer documentation referenced earlier in this topic.
3. Save the file.
