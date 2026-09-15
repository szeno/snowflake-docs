# JDBC data sources for Snowpark Connect for Spark

This section provides a guide and sample code for reading data from and writing
data to external databases (such as MySQL and PostgreSQL) using the Snowpark Connect for Spark
JDBC data source feature. It covers both client-side and Snowflake Notebook setup.

## Supported data sources

- SQL Server
- MySQL
- PostgreSQL
- Neo4j
- Derby

## Client-side setup (MySQL)

This setup is required when running Snowpark Connect from a local client
application, such as a Python script or IDE.

### Prerequisites

1. **Java Runtime Environment (JRE) / Java Development Kit (JDK):**

   - Install a JRE or JDK. The architecture (for example, 64-bit) of your Java
     installation **must** match the architecture of your Python
     installation.
   - *Example source for installation:* [Adoptium Temurin Releases](https://adoptium.net/temurin/releases/?version=11) (if
     using Java 11).
2. **Set JAVA\_HOME Environment Variable:**

   - Configure the `JAVA_HOME` environment variable to point to the
     root directory of your Java installation.
   - *Example (macOS/Linux):*

   Copy code

   ```
   export JAVA_HOME=/path/to/your/jdk/home
   ```
3. **Set CLASSPATH Environment Variable:**

   - Add the path to your specific database’s JDBC driver `.jar` file
     to the `CLASSPATH` environment variable. This allows the Java
     environment to find the necessary driver.
   - *Example (for MySQL driver):*

   Copy code

   ```
   export CLASSPATH=$CLASSPATH:/path/to/your/driver/mysql-connector-j-9.2.0.jar
   ```

### Sample client code (read from MySQL)

This example demonstrates how to read a table from a MySQL database
using `spark_session.read.jdbc()`.

Copy code

```
from pyspark.sql import Row

# Adjust the URL for your server host, port, and database name
MYSQL_JDBC_URL = "jdbc:mysql://localhost/test_db"

# Ensure this driver name matches your version of the JDBC driver
MYSQL_JDBC_DRIVER = "com.mysql.cj.jdbc.Driver"

def test_jdbc_read_from_mysql(self, spark_session):
    # This code snippet uses the Snowpark Connect Spark session
    jdbc_df = spark_session.read.jdbc(
        MYSQL_JDBC_URL,
        "my_schema.my_table",  # Specify your table name in MySQL
        properties={
            "user": "root",           # Your MySQL user name
            "password": "****",       # Your password for MySQL
            "driver": MYSQL_JDBC_DRIVER,
        },
    ).collect()

    # After reading via JDBC, the data is loaded into a temporary table in Snowflake.
    # You can now perform any standard DataFrame operations supported by Snowpark Connect.
```

### Sample client code (write to MySQL)

This example demonstrates how to write data into a MySQL database using
`spark_session.write.jdbc()`.

Copy code

```
from pyspark.sql import Row

# Adjust the URL for your server host, port, and database name
MYSQL_JDBC_URL = "jdbc:mysql://localhost/test_db"

# Ensure this driver name matches your version of the JDBC driver
MYSQL_JDBC_DRIVER = "com.mysql.cj.jdbc.Driver"

def test_jdbc_write_overwrite_to_mysql(self, spark_session):
    # This code snippet uses the Snowpark Connect Spark session
    jdbc_df = spark_session.createDataFrame(
        [
            Row(a=1, b=2.0, c="test1"),
            Row(a=2, b=3.0, c="test2"),
            Row(a=4, b=5.0, c="test3"),
        ]
    )

    jdbc_df.write.jdbc(
        MYSQL_JDBC_URL,
        "my_schema.my_table2",  # Specify your table name in MySQL
        mode="overwrite",
        properties={
            "user": "root",        # Your MySQL user name
            "password": "****",    # Your password for MySQL
            "driver": MYSQL_JDBC_DRIVER,
        },
    )
```

## Snowflake Workspace Notebook setup (PostgreSQL)

This setup is used when running Snowpark Connect directly within a
Snowflake Workspace Notebook environment.

### Setup steps

- The `snowpark-connect` package is included in Workspace Notebook by default.
- **Download and Upload JDBC Driver:**
  - Download the appropriate JDBC driver `.jar` file for your external
    database (for example, [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/download/postgresql-42.7.8.jar)).
  - Upload the downloaded `.jar` file directly into your notebook
    environment.

![Uploading JDBC driver in Snowflake Workspace Notebook](/static/images/snowpark-connect/jdbc-datasource-image4.png)

- **Create External Integration:**

Copy code

```
-- 1. Create a Network Rule for the external database host and port
CREATE OR REPLACE NETWORK RULE JDBC_READ_NETWORK_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('hh-pgsql-public.ebi.ac.uk:5432'); -- REPLACE with your host:port

-- 2. Create the External Access Integration using the new Network Rule
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION JDBC_READ_ACCESS_INTEGRATION
  ALLOWED_NETWORK_RULES = (JDBC_READ_NETWORK_RULE)
  ENABLED = true;

-- NOTE: This integration must be referenced/activated within your notebook's settings.
```

- **Activate External Integrations (Network Rule & Integration):**

  - Snowflake requires an **External Access Integration** to allow the
    notebook to communicate with external network locations. You must
    define a **Network Rule** for the host and port of your external
    database.![Activating external access integration in Workspace Notebook settings](/static/images/snowpark-connect/jdbc-datasource-image5.png)

### Sample Workspace Notebook code (read from PostgreSQL)

This example shows the necessary Python code to initialize the session,
load the driver, and read data from PostgreSQL.

Copy code

```
from snowflake import snowpark_connect
import jpype
import os

# Initialize the Spark session for Snowpark Connect
spark = snowpark_connect.server.init_spark_session()
df = spark.sql("show schemas").limit(2)
df.show()

# Add the uploaded JDBC driver JAR to the Java Classpath using jpype
# Adjust the path to match the name of the JAR file you uploaded
# Copy the driver to /tmp directory
os.system("cp ./postgresql-42.7.8.jar /tmp/postgresql-42.7.8.jar")
jpype.addClassPath('/tmp/postgresql-42.7.8.jar')

# Using public PostgreSQL DB as an example: https://rnacentral.org/help/public-database
jdbc_df = spark.read.jdbc(
    # Adjust this URL as per your server host, port, and database
    "jdbc:postgresql://hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs",
    "",  # Empty string for table name when providing a custom query
    properties={
        "user": "reader",                # Your PostgreSQL user name
        "password": "***",               # Your password for PostgreSQL
        "driver": "org.postgresql.Driver",
        # Use the "query" property for a custom SQL statement
        "query": """SELECT
  upi,     -- RNAcentral URS identifier
  taxid,   -- NCBI taxid
  ac       -- external accession
FROM xref
WHERE ac IN ('OTTHUMT00000106564.1', 'OTTHUMT00000416802.1')"""
    },
)

jdbc_df.show()
```

### Sample Workspace Notebook code (write to PostgreSQL)

This example shows the necessary Python code to initialize the session,
load the driver, and write data into PostgreSQL.

Copy code

```
from snowflake import snowpark_connect
from pyspark.sql import Row
import jpype
import os

# Initialize the Spark session for Snowpark Connect
spark = snowpark_connect.server.init_spark_session()
df = spark.sql("show schemas").limit(2)
df.show()

# Add the uploaded JDBC driver JAR to the Java Classpath using jpype
# Adjust the path to match the name of the JAR file you uploaded
# Copy the driver to /tmp directory
os.system("cp ./postgresql-42.7.8.jar /tmp/postgresql-42.7.8.jar")
jpype.addClassPath('/tmp/postgresql-42.7.8.jar')

# Create dataframe
jdbc_df = spark.createDataFrame(
    [
        Row(a=1, b=2.0, c="test1"),
        Row(a=2, b=3.0, c="test2"),
        Row(a=4, b=5.0, c="test3"),
    ]
)

# Using public PostgreSQL DB as an example: https://rnacentral.org/help/public-database
jdbc_df.write.jdbc(
    # Adjust this URL as per your server host, port, and database
    "jdbc:postgresql://hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs",
    "public.my_table2",  # Specify your table name in PostgreSQL
    mode="overwrite",
    properties={
        "user": "writer",                # Your PostgreSQL user name
        "password": "***",               # Your password for PostgreSQL
        "driver": "org.postgresql.Driver",
    },
)
```

## Snowflake Warehouse Notebook setup (PostgreSQL)

This setup is used when running Snowpark Connect directly within a
Snowflake Notebook environment.

### Setup steps

- **Add the snowpark-connect package:**
  - Ensure the `snowflake-snowpark-connect` package is added to your
    notebook environment.

![Adding the snowflake-snowpark-connect package in Snowflake Notebook](/static/images/snowpark-connect/jdbc-datasource-image1.png)

- **Download and Upload JDBC Driver:**

  - Download the appropriate JDBC driver `.jar` file for your external
    database (for example, [PostgreSQL JDBC Driver](https://jdbc.postgresql.org/download/postgresql-42.7.8.jar)).
  - Upload the downloaded `.jar` file directly into your notebook
    environment.
- **Activate External Integrations (Network Rule & Integration):**

  - Snowflake requires an **External Access Integration** to allow the
    notebook to communicate with external network locations. You must
    define a **Network Rule** for the host and port of your external
    database.

![Configuring network rule settings in Snowflake Notebook](/static/images/snowpark-connect/jdbc-datasource-image2.png)
![Uploading the JDBC driver JAR file in Snowflake Notebook](/static/images/snowpark-connect/jdbc-datasource-image3.png)

Copy code

```
-- 1. Create a Network Rule for the external database host and port
CREATE OR REPLACE NETWORK RULE JDBC_READ_NETWORK_RULE
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('hh-pgsql-public.ebi.ac.uk:5432'); -- REPLACE with your host:port

-- 2. Create the External Access Integration using the new Network Rule
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION JDBC_READ_ACCESS_INTEGRATION
  ALLOWED_NETWORK_RULES = (JDBC_READ_NETWORK_RULE)
  ENABLED = true;

-- NOTE: This integration must be referenced/activated within your notebook's settings.
```

### Sample Warehouse Notebook code (read from PostgreSQL)

This example shows the necessary Python code to initialize the session,
load the driver, and read data from PostgreSQL.

Copy code

```
from snowflake import snowpark_connect
import jpype

# Initialize the Spark session for Snowpark Connect
spark = snowpark_connect.server.init_spark_session()
df = spark.sql("show schemas").limit(2)
df.show()

# Add the uploaded JDBC driver JAR to the Java Classpath using jpype
# Adjust the path to match the name of the JAR file you uploaded
jpype.addClassPath('/tmp/appRoot/postgresql-42.7.8.jar')

# Using public PostgreSQL DB as an example: https://rnacentral.org/help/public-database
jdbc_df = spark.read.jdbc(
    # Adjust this URL as per your server host, port, and database
    "jdbc:postgresql://hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs",
    "",  # Empty string for table name when providing a custom query
    properties={
        "user": "reader",                # Your PostgreSQL user name
        "password": "***",               # Your password for PostgreSQL
        "driver": "org.postgresql.Driver",
        # Use the "query" property for a custom SQL statement
        "query": """SELECT
  upi,     -- RNAcentral URS identifier
  taxid,   -- NCBI taxid
  ac       -- external accession
FROM xref
WHERE ac IN ('OTTHUMT00000106564.1', 'OTTHUMT00000416802.1')"""
    },
)

jdbc_df.show()
```

### Sample Warehouse Notebook code (write to PostgreSQL)

This example shows the necessary Python code to initialize the session,
load the driver, and write data into PostgreSQL.

Copy code

```
from snowflake import snowpark_connect
from pyspark.sql import Row
import jpype

# Initialize the Spark session for Snowpark Connect
spark = snowpark_connect.server.init_spark_session()
df = spark.sql("show schemas").limit(2)
df.show()

# Add the uploaded JDBC driver JAR to the Java Classpath using jpype
# Adjust the path to match the name of the JAR file you uploaded
jpype.addClassPath('/tmp/appRoot/postgresql-42.7.8.jar')

# Create dataframe
jdbc_df = spark.createDataFrame(
    [
        Row(a=1, b=2.0, c="test1"),
        Row(a=2, b=3.0, c="test2"),
        Row(a=4, b=5.0, c="test3"),
    ]
)

# Using public PostgreSQL DB as an example: https://rnacentral.org/help/public-database
jdbc_df.write.jdbc(
    # Adjust this URL as per your server host, port, and database
    "jdbc:postgresql://hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs",
    "public.my_table2",  # Specify your table name in PostgreSQL
    mode="overwrite",
    properties={
        "user": "writer",                # Your PostgreSQL user name
        "password": "***",               # Your password for PostgreSQL
        "driver": "org.postgresql.Driver",
    },
)
```

## Client-side setup (Neo4j)

Snowpark Connect for Spark supports reading and writing data from Neo4j graph databases using the `org.neo4j.spark.DataSource`
format. This section covers client-side setup.

### Prerequisites

1. **Running Neo4j instance:**

   You need a running Neo4j instance accessible over the Bolt protocol (port 7687).
2. **Neo4j JDBC driver:**

   Download the `full-bundle` JAR from [Maven Central](https://search.maven.org/artifact/org.neo4j/neo4j-jdbc-full-bundle)
   (for example, `neo4j-jdbc-full-bundle-6.10.2.jar`).
3. **Configure spark.jars:**

   Point to the local path of the downloaded JAR when creating the Spark session:

   Copy code

   ```
   spark = SparkSession.builder \
    .remote("sc://<your-host>:15002") \
    .config("spark.jars", "/path/to/neo4j-jdbc-full-bundle-6.10.2.jar") \
    .getOrCreate()
   ```

### Sample client code (read from Neo4j)

Copy code

```
# Read nodes by label
df = spark.read.format("org.neo4j.spark.DataSource") \
    .option("url", "bolt://<neo4j-host>:7687") \
    .option("authentication.basic.username", "neo4j") \
    .option("authentication.basic.password", "password") \
    .option("labels", "Person") \
    .load()

df.show()

# Read with a custom Cypher query
df = spark.read.format("org.neo4j.spark.DataSource") \
    .option("url", "bolt://<neo4j-host>:7687") \
    .option("authentication.basic.username", "neo4j") \
    .option("authentication.basic.password", "password") \
    .option("query", "MATCH (n:Person) RETURN n.name AS name, n.age AS age LIMIT 10") \
    .load()

df.show()
```

### Sample client code (write to Neo4j)

Copy code

```
data = [("Alice", 30, "New York"), ("Bob", 25, "Los Angeles")]
df = spark.createDataFrame(data, ["name", "age", "city"])

df.write.format("org.neo4j.spark.DataSource") \
    .option("url", "bolt://<neo4j-host>:7687") \
    .option("authentication.basic.username", "neo4j") \
    .option("authentication.basic.password", "password") \
    .option("labels", "Person") \
    .mode("append") \
    .save()
```

### Snowflake Notebook setup

To connect to Neo4j from a Snowflake Notebook (Warehouse or Workspace), follow the same Network Rule and
External Access Integration steps described in the PostgreSQL sections above. Use the Neo4j Bolt port
(typically 7687) in your Network Rule, upload the Neo4j JDBC `full-bundle` JAR, and load it with
`spark.jars` configuration. The read and write code is identical to the client-side examples.

### Supported configurations

The following options are available when using the `org.neo4j.spark.DataSource` format:

| Option | Description | Required |
| --- | --- | --- |
| `url` | Neo4j connection URL (for example, `bolt://<neo4j-host>:7687`). | Yes |
| `authentication.basic.username` | Neo4j username. | Yes |
| `authentication.basic.password` | Neo4j password. | Yes |
| `labels` | Node label to read or write (for example, `Person`). | Required for writes. One of `labels`, `query`, or `relationship` for reads. |
| `query` | Custom Cypher query to execute on read. | One of `labels`, `query`, or `relationship` for reads. |
| `relationship` | Relationship type to read (for example, `KNOWS`). | One of `labels`, `query`, or `relationship` for reads. |

Expand

Show lessSee more

Supported URL formats:

| Format | Description |
| --- | --- |
| `bolt://host:7687` | Standard Bolt protocol (standalone instances). |
| `bolt+s://host:7687` | Bolt with TLS encryption. |
| `neo4j://host:7687` | Neo4j protocol with routing (clusters). |
| `neo4j+s://host:7687` | Neo4j protocol with TLS and routing. |

Expand

Show lessSee more

Note

For standalone Neo4j instances, use `bolt://`. The `neo4j://` protocol requires a Neo4j cluster
with routing capabilities.
