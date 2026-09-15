# Integrate Apache Hive metastores with Snowflake

You can use the Hive metastore connector for Snowflake to integrate [Apache Hive](https://hive.apache.org/)
metastores with Snowflake by using external tables. The connector detects metastore events and transmits the events
to Snowflake to keep the external tables synchronized with the Hive metastore.
With this capability, users can manage their schema in Hive while querying the metastore from Snowflake.

The Apache Hive metastore must be integrated with cloud storage on one of the following cloud platforms:

- Amazon Web Services
- Google Cloud
- Microsoft Azure

## Install and configure the Hive metastore connector

This section describes how to install and configure the Hive metastore connector for Snowflake.

### Prerequisites

The Hive connector for Snowflake has the following prerequisites:

Snowflake database and schemas:
:   Store the external tables that map to the Hive tables in the metastore.

Designated Snowflake user:
:   The connector is configured to execute operations on the external tables as this user.

Storage integration:
:   With storage integrations, you can configure secure access to external cloud storage without passing explicit cloud provider credentials, such as secret keys or access tokens. Create a storage integration to access cloud storage locations referenced in Hive tables using [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).

    The STORAGE\_ALLOWED\_LOCATIONS parameter for the storage integration must list the same storage containers as the ones referenced in the `Location` parameter of the Hive tables in your metastore.

Role:
:   The role must be assigned to the designated Snowflake user and include the following object privileges on the other Snowflake objects identified in this section:

    | Object | Privileges |
    | --- | --- |
    | Database | USAGE |
    | Schema | USAGE , CREATE STAGE , CREATE EXTERNAL TABLE |
    | Storage integration | USAGE |

    Expand

    Show lessSee more

### Step 1: Install the connector

Complete the following steps to install the connector:

1. From the Maven Central Repository ([Sonatype](https://central.sonatype.com/search?q=g%3Anet.snowflake%20snowflake-hive-metastore-connector) or <https://repo1.maven.org/maven2/net/snowflake/snowflake-hive-metastore-connector/>), download the connector JAR file and configuration XML file.
2. Copy the JAR file to the following directory:

   Amazon S3 or Google Cloud Storage:
   :   `lib` directory in the Hive classpath. The location can vary depending on the Hive installation. To determine the classpath, check the HIVE\_AUX\_JARS\_PATH environment variable.

   Microsoft Azure HDInsight:
   :   `hive` directory in the user directory; for example, `/usr/hdp/<hdinsight_version>/atlas/hook/hive/`. The location can vary depending on the Azure HDInsight version and installation choices.

       Tip

       An example custom script is available in the `scripts` folder on the
       [GitHub project page for Hive](https://github.com/snowflakedb/snowflake-hive-metastore-connector/). The script adds the JAR file and
       configuration files to the correct directories.
3. Create a file named `snowflake-config.xml` in the following directory:

   Amazon S3 or Google Cloud Storage:
   :   `conf` directory in the Hive classpath.

   Microsoft Azure HDInsight:
   :   `conf/conf.server` directory in the Hive classpath.
4. In a text editor, open the `snowflake-config.xml` file, and then populate the file with the following `<name>` properties and corresponding `<values>`:

   > `snowflake.jdbc.username`
   > :   Specifies the sign-in name of the Snowflake user designated for refresh operations on the external tables.
   >
   > `snowflake.jdbc.password`
   > :   Specifies the password for the sign-in name.
   >
   >     Note
   >
   >     - You can set a placeholder for the password based on a system property or environment variable, depending on your Hadoop version.
   >       The configuration behaves like other Hadoop configurations. For more information, see the
   >       [Hadoop documentation](https://hadoop.apache.org/).
   >     - `snowflake.jdbc.privateKey`
   >
   >     Alternatively, authenticate by using key-pair authentication. For instructions about how to generate the key pair and assign the public key
   >     to a user, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
   >
   >     To pass the private key to Snowflake, add the `snowflake.jdbc.privateKey` property to the `snowflake-config.xml` file.
   >     Open the private key file (for example, `rsa_key.p8`) in a text editor. Copy the lines between `-----BEGIN RSA PRIVATE KEY-----` and
   >     `-----END RSA PRIVATE KEY-----` as the property or environment variable value.
   >
   > `snowflake.jdbc.account`
   > :   Specifies the name of your account (provided by Snowflake); for example, `xy12345`.
   >
   > `snowflake.jdbc.db`
   > :   Specifies an existing Snowflake database to use for the Hive metastore integration. For more information, see the [Prerequisites](#prerequisites) section earlier in this topic.
   >
   > `snowflake.jdbc.schema`
   > :   Specifies an existing Snowflake schema in the specified database. For more information, see the [Prerequisites](#prerequisites) section earlier in this topic.
   >
   >     To map multiple schemas in your Hive metastore to corresponding schemas in your Snowflake database, set the `snowflake.hive-metastore-listener.schemas` property in addition to the current property. Specify the default Snowflake schema in the `snowflake.jdbc.schema` property.
   >
   > `snowflake.jdbc.role`
   > :   Specifies the access-control role to use by the Hive connector. The role should be an existing role that was already assigned to the specified user.
   >
   >     If no role is specified here, then the Hive connector uses the default role for the specified user.
   >
   > `snowflake.jdbc.connection`
   > :   Specifies the connection string for your Snowflake account in the following format:
   >
   >     `jdbc:snowflake://<account_identifier>.snowflakecomputing.com`
   >
   >     Where:
   >
   >     `<account_identifier>`
   >     :   Unique identifier for your Snowflake account.
   >
   >         The following example shows the preferred format of the account identifier:
   >
   >         `organization_name-account_name`
   >         :   Names of your Snowflake organization and account. For information, see [Format 1 (preferred): Account name in your organization](/user-guide/admin-account-identifier#label-account-name).
   >
   >         Alternatively, specify your *account locator* and the geographical [region](/user-guide/intro-regions), and possibly the [cloud platform](/user-guide/intro-cloud-platforms), where the account is hosted. For more information, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).
   >
   > `snowflake.hive-metastore-connector.integration`
   > :   Specifies the name of the storage integration object to use for secure access to the external storage locations referenced in Hive tables in the metastore. For more information, see the [Prerequisites](#prerequisites) section earlier in this topic.
   >
   > `snowflake.hive-metastore-listener.schemas`
   > :   Specifies a comma-separated list of Snowflake schemas that exist in the Snowflake database specified in `snowflake.jdbc.db`.
   >
   >     When a table is created in the Hive metastore, the connector checks whether this property lists a Snowflake schema with the same name as the Hive schema or database that contains the new table:
   >
   >     - If a Snowflake schema with the same name is listed, the connector creates an external table in this schema.
   >     - If a Snowflake schema with the same name is not listed, the connector creates an external table in the default schema, which is defined in the `snowflake.jdbc.schema` property.
   >
   >     The external table has the same name as the new Hive table.
   >
   >     Note
   >
   >     This property requires version 0.5.0 (or higher) of the Hive Connector.

   (Optional) Add the following property:

   `snowflake.hive-metastore-listener.database-filter-regex`
   :   Specifies the names of any databases in the Hive metastore to skip with the integration. With this property, you can control which databases to integrate with Snowflake. This option is especially useful when multiple tables have the same name across Hive databases. Currently, in this situation, the Hive connector creates the first table with the name in the Snowflake target database but skips additional tables with the same name.

       For example, suppose databases `mydb1`, `mydb2`, and `mydb3` all contain a table named `table1`. You can omit all databases with the naming convention `mydb<number>` except for `mydb1` by adding the regular expression `mydb[^1]` as the property value.

       **Example property node**

       Copy code

       ```
       <configuration>
         ..
         <property>
        <name>snowflake.hive-metastore-listener.database-filter-regex</name>
        <value>mydb[^1]</value>
         </property>
       </configuration>
       ```

       **Example snowflake-config.xml file**

       Copy code

       ```
       <configuration>
         <property>
        <name>snowflake.jdbc.username</name>
        <value>jsmith</value>
         </property>
         <property>
        <name>snowflake.jdbc.password</name>
        <value>mySecurePassword</value>
         </property>
         <property>
        <name>snowflake.jdbc.role</name>
        <value>custom_role1</value>
         </property>
         <property>
        <name>snowflake.jdbc.account</name>
        <value>myaccount</value>
         </property>
         <property>
        <name>snowflake.jdbc.db</name>
        <value>mydb</value>
         </property>
         <property>
        <name>snowflake.jdbc.schema</name>
        <value>myschema</value>
         </property>
         <property>
        <name>snowflake.jdbc.connection</name>
        <value>jdbc:snowflake://myaccount.snowflakecomputing.com</value>
         </property>
         <property>
        <name>snowflake.hive-metastore-listener.integration</name>
        <value>s3_int</value>
         </property>
         <property>
        <name>snowflake.hive-metastore-listener.schemas</name>
        <value>myschema1,myschema2</value>
         </property>
       </configuration>
       ```
5. Save the changes to the file.
6. Edit the existing Hive configuration file (`hive-site.xml`):

   Amazon S3 or Google Cloud Storage:
   :   Open the `hive-site.xml` file in a text editor. Add the connector to the configuration file as follows:

       Copy code

       ```
       <configuration>
        ...
        <property>
         <name>hive.metastore.event.listeners</name>
         <value>net.snowflake.hivemetastoreconnector.SnowflakeHiveListener</value>
        </property>
       </configuration>
       ```

   Microsoft Azure HDInsight:
   :   Complete the steps in the
       [Azure HDInsight documentation](https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-hadoop-customize-cluster-bootstrap) to
       edit the `hive-site.xml` file. Add the following custom property to the cluster configuration:

       `hive.metastore.event.listeners=net.snowflake.hivemetastoreconnector.SnowflakeHiveListener`

       Alternatively, add the custom property in the HDInsight Cluster Management Portal:

       1. Click the **Hive** tab in the left-hand menu » **Configs** » **Advanced**.
       2. Scroll down to the **Custom Hive Site** tab.
       3. Add the custom property.

   Note

   If there are other connectors already configured in this file, add the Hive connector for Snowflake in a comma-separated list in the `<value>` node.
7. Save the changes to the file.
8. Restart the Hive metastore service.

### Step 2: Validate the installation

1. In Hive, create a new table.
2. In your Snowflake database and schema, query the list of external tables by using [SHOW EXTERNAL TABLES](/sql-reference/sql/show-external-tables):

   Copy code

   ```
   SHOW EXTERNAL TABLES IN <database>.<schema>;
   ```

   Where `database` and `schema` are the database and schema you specified in the `snowflake-config.xml` file in [Step 1: Install the Connector](#step-1-install-the-connector) earlier in this topic.

   The results should show an external table with the same name as the new Hive table.

Connector records are written to the Hive metastore logs. You can view queries run by the connector in the Snowflake QUERY\_HISTORY view/function output similar to other queries.

## Integrate existing Hive tables and partitions with Snowflake

To integrate existing Hive tables and partitions with Snowflake, run the following command in Hive for each table and partition:

Copy code

```
ALTER TABLE <table_name> TOUCH [PARTITION partition_spec];
```

For more information, see the [Hive documentation](https://cwiki.apache.org/confluence/display/Hive/Home).

Alternatively, Snowflake provides a script for synching existing Hive tables and partitions. For information, see the [GitHub project page](https://github.com/snowflakedb/snowflake-hive-metastore-connector/blob/master/scripts/sync_hive_to_snowflake.sh).

Important

If an external table with the same name as the Hive table already exists in the corresponding Snowflake schema in the database specified
in the `snowflake.jdbc.db` property, the ALTER TABLE … TOUCH command does not recreate the external table. If you need to
recreate the external table, drop the external table (by using [DROP EXTERNAL TABLE](/sql-reference/sql/drop-external-table)) before you run the ALTER
TABLE … TOUCH command in the Hive metastore.

## Supported and unsupported features

The following sections list supported and unsupported features of the Apache Hive metastores integration with the Hive metastore connector for Snowflake.

### Supported Hive operations and table types

#### Hive operations

The connector supports the following Hive operations:

- Create table
- Drop table
- Alter table add column
- Alter table drop column
- Alter (that is, *touch*) table
- Add partition
- Drop partition
- Alter (touch) partition

#### Hive table types

The connector supports the following types of Hive tables:

- External and managed tables
- Partitioned and unpartitioned tables

### Hive and Snowflake data types

The following table shows the mapping between Hive and Snowflake data types:

| Hive | Snowflake |
| --- | --- |
| BIGINT | BIGINT |
| BINARY | BINARY |
| BOOLEAN | BOOLEAN |
| CHAR | CHAR |
| DATE | DATE |
| DECIMAL | DECIMAL |
| DOUBLE | DOUBLE |
| DOUBLE PRECISION | DOUBLE |
| FLOAT | FLOAT |
| INT | INT |
| INTEGER | INT |
| NUMERIC | DECIMAL |
| SMALLINT | SMALLINT |
| STRING | STRING |
| TIMESTAMP | TIMESTAMP |
| TINYINT | SMALLINT |
| VARCHAR | VARCHAR |
| All other data types | VARIANT |

Expand

Show lessSee more

### Supported file formats and options

The following data file formats and Hive file format options are supported:

- CSV

  The following options are supported using the SerDe (Serializer/Deserializer) properties:

  - `field.delim` / `separatorChar`
  - `line.delim`
  - `escape.delim` / `escapeChar`
- JSON
- AVRO
- ORC
- PARQUET

  The following options are supported using the table properties:

  - `parquet.compression`.

### Unsupported Hive commands, features, and use cases

The connector does not support the following Hive commands, features, and use cases:

- Hive views
- ALTER statements other than TOUCH, ADD COLUMNS, and DROP COLUMNS
- Custom SerDe properties.
- Modifying an existing managed Hive table to become an external Hive table, or vice versa

## Refresh external table metadata to reflect Cloud Storage events

When any of the Hive operations listed in [Supported Hive Operations and Table Types](#supported-hive-operations-and-table-types) earlier in this topic are run on a table, the Hive connector listens to the Hive events and then refreshes the metadata for the corresponding external table in Snowflake.

However, the connector does not refresh the external table metadata based on events in cloud storage, such as adding or removing data files.

To refresh the metadata for an external table to reflect events in the cloud storage, run the respective ALTER TABLE … TOUCH command for your partitioned or unpartitioned Hive table. TOUCH reads the metadata and writes it back. For more information about the command, see the [Hive documentation](https://cwiki.apache.org/confluence/display/Hive/Home):

Partitioned Hive table:
:   Run the following command:

    Copy code

    ```
    ALTER TABLE <table_name> TOUCH PARTITION <partition_spec>;
    ```

Unpartitioned Hive table:
:   Run the following command:

    Copy code

    ```
    ALTER TABLE <table_name> TOUCH;
    ```

## Differences between Hive tables and Snowflake external tables

The following list describes the main differences between Hive tables and Snowflake external tables:

Partitions:
:   - Snowflake partitions are composed of subpaths of the storage location referenced by the table, while Hive partitions don’t have this constraint. If partitions are added in Hive tables that are not subpaths of the storage location, those partitions aren’t added to the corresponding external tables in Snowflake.

      For example, if the storage location associated with the Hive table (and corresponding Snowflake external table) is `s3://path/`, then all partition locations in the Hive table must also be prefixed by `s3://path/`.
    - Two Snowflake partitions in a single external table can’t point to the exact same storage location. For example, the following partitions conflict with each other:

      Copy code

      ```
      ALTER EXTERNAL TABLE exttable ADD PARTITION(partcol='1') LOCATION 's3:///files/2019/05/12';

      ALTER EXTERNAL TABLE exttable ADD PARTITION(partcol='2') LOCATION 's3:///files/2019/05/12';
      ```

Column names:
:   Hive column names are case-insensitive, but Snowflake virtual columns derived from VALUES are case-sensitive. If Hive tables contain columns with mixed-case names, the data in those columns might be NULL in the corresponding columns in the Snowflake external tables.
