[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Note

The Snowflake Connector for PostgreSQL and Snowflake Connector for MySQL are subject to the [Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms).

# Tutorial: Get started with the MySQL and PostgreSQL connectors for Snowflake

## Introduction

Welcome to our tutorial on using the Snowflake Database Connectors. This guide will help you seamlessly transfer data from relational databases into Snowflake.

In this tutorial, you’ll gain the skills to:

- Set up MySQL and PostgreSQL in Docker, complete with sample data for ingestion.
- Install and configure two native applications, one for each database.
- Set up and fine-tune two agents, again one for each database.
- Initiate and manage data ingestion processes.
- Monitor the data ingestion workflow.

Let’s get started!

### Prerequisites

Before beginning this tutorial, ensure you meet the following requirements:

- Docker is installed and operational on your local machine.
- You have a tool available for connecting to the database. This can be a database-specific tool or a general-purpose tool such as IntelliJ or Visual Studio Code.

## Creating MySQL and PostgreSQL Source Databases

In this section, we will guide you through the following steps:

- [Starting the Database Instances](#starting-the-database-instances) - Learn how to launch your MySQL and PostgreSQL instances using Docker.
- [Connecting to the Database](#connecting-to-the-database) - Instructions on how to establish a connection to your databases.
- [Loading Sample Data](#loading-sample-data) - A walkthrough on how to populate your databases with sample data.

### Starting the database instances

To begin the MySQL and PostgreSQL database configuration process using Docker, create the file `docker-compose.yaml`.
The content of the file should resemble:

Copy code

```
services:
  mysql:
    container_name: mysql8
    restart: always
    image: mysql:8.0.28-oracle
    command: --log-bin=/var/lib/mysql/mysql-bin
      --max-binlog-size=4096
      --binlog-format=ROW
      --binlog-row-image=FULL
      --binlog-row-metadata=FULL
      --sql_mode="ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,PAD_CHAR_TO_FULL_LENGTH"
    environment:
      MYSQL_ROOT_PASSWORD: 'mysql'
    volumes:
      - ./mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"
  postgres:
    image: "postgres:11"
    container_name: "postgres11"
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
    ports:
      - "5432:5432"
    command:
      - "postgres"
      - "-c"
      - "wal_level=logical"
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
```

Once your `docker-compose.yaml` is ready, follow these steps:

1. Open a terminal.
2. Navigate to the directory containing the `docker-compose.yaml` file.
3. Execute the following command to start source databases in containers:

   Copy code

   ```
   docker compose up -d
   ```

After running this command, you should see two containers actively running the source databases.

### Connecting to the Database

To connect to the pre-configured databases using IntelliJ’s or Visual Studio Code database connections,
perform the following steps with the provided credentials:

MySQLPostgreSQL

1. Open your tool of choice for connecting to the MySQL.
2. Click the ‘+’ sign or similar to add data source.
3. Fill in the connection details:

   - **User**: `root`
   - **Password**: `mysql`
   - **URL**: `jdbc:mysql://localhost:3306`
4. Test the connection and save.

1. Open your tool of choice for connecting to the PostgreSQL.
2. Click the ‘+’ sign or similar to add data source.
3. Fill in the connection details:

   - **User**: `postgres`
   - **Password**: `postgres`
   - **Database**: `postgres`
   - **URL**: `jdbc:postgresql://localhost:5432`
4. Test the connection and save.

### Loading Sample Data

To initialize and load sample please execute those scripts in those connections.

MySQLPostgreSQL

Execute the script to generate sample data

Copy code

```
CREATE DATABASE mysql_ingest_database;
USE mysql_ingest_database;

CREATE TABLE mysql_rows(
    id INT AUTO_INCREMENT PRIMARY KEY,
    random_string VARCHAR(255),
    random_number INT);

INSERT INTO mysql_rows (random_string, random_number) VALUES
    ('fukjxyiteb', 100),
    ('ndhbbipodi', 37),
    ('laebpztxzh', 83);

SELECT * FROM mysql_ingest_database.mysql_rows;
```

Execute the script to generate sample data

Copy code

```
CREATE SCHEMA psql_rows_schema;
SET search_path TO psql_rows_schema;

CREATE TABLE psql_rows_schema.postgres_rows (
  id SERIAL PRIMARY KEY,
  a_text TEXT,
  a_boolean BOOLEAN,
  a_number INTEGER,
  a_decimal DOUBLE PRECISION);

INSERT INTO psql_rows_schema.postgres_rows (a_text, a_boolean, a_number, a_decimal) VALUES
  ('QfJhyWwFuC', True, 37, 15.46),
  ('GwmIFgwvFy', True, 14, 13.21),
  ('jYvqOSEtam', True, 25, 20.85);

-- The publication is required to start the replication progress as the Connector is based on PostgreSQL Logical Replication
CREATE PUBLICATION agent_postgres_publication FOR ALL TABLES;

SELECT * FROM psql_rows_schema.postgres_rows;
```

You should see three rows in each populated database.

## Install and configure the Native App

During this step you will:

- [Install the Native Applications](#install-the-native-applications)
- [Configuring the Native Applications](#configuring-the-native-applications)

### Install the Native Applications

Follow these steps to install the Application from the Snowflake Native Apps Marketplace:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Marketplace** » **Snowflake Marketplace**.
3. Install the **Snowflake Connector for MySQL** and **Snowflake Connector for PostgreSQL** applications.
4. Install both applications.

After installation, you will see the new applications listed in **Catalog** » **Apps**.

### Configuring the Native Applications

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Open each application and do the following:

MySQLPostgreSQL

1. Select **Download Driver** and save the file. The file name will resemble `mariadb-java-client-3.4.1.jar` or with newer version when available. Save this file for use during agent configuration.
2. Select **Mark all as done** as we will create and populate source databases from scratch.

   Note

   No addition additional network configuration is required at this point as we’ll configure the agent later in the tutorial.
3. Click **Start configuration**.
4. On the **Configure Connector** screen, select **Configure**. The **Verify Agent Connection** page will display.
5. Select **Generate file** to generate an agent configuration file. The file name should resemble `snowflake.json`. Save this file for later use in the Agent Configuration section.

1. Select **Mark all as done** as we will create and populate source databases from scratch.

   Note

   No addition additional network configuration is required at this point as we’ll configure the agent later in the tutorial.
2. Click **Start configuration**
3. On the **Configure Connector** screen, select **Configure**.
4. In the **Verify Agent Connection** page select **Generate file** to generate the agent configuration file. The file name should resemble `snowflake.json`. Save this file for use during the Agent Configuration section.

## Configure the agents

In this section, we’ll configure the agent that will operate with your source databases.

The first step is to create directories `agent-mysql` and `agent-postgresql`.

Within each directory, create subdirectories `agent-keys` and `configuration`. Your directory structure should resemble:

```
.
├── agent-mysql
│   ├── agent-keys
│   └── configuration
└── agent-postgresql
    ├── agent-keys
    └── configuration
```

### Creating configuration files

In this section, we’ll add content to the configuration files for each agent to operate correctly. The configuration files include:

- `snowflake.json` file to connect to the Snowflake.
- `datasources.json` file to connect to the source databases.
- `postgresql.conf/mysql.conf` files with additional agent environment variables.
- JDBC Driver file for MySQL agent.

MySQLPostgreSQL

1. In a terminal, navigate to the `agent-mysql` directory.
2. Create the Docker Compose file `docker-compose.yaml` with the following content:

   Copy code

   ```
   services:
     mysql-agent:
    container_name: mysql-agent
    image: snowflakedb/database-connector-agent:latest
    volumes:
      - ./agent-keys:/home/agent/.ssh
      - ./configuration/snowflake.json:/home/agent/snowflake.json
      - ./configuration/datasources.json:/home/agent/datasources.json
      - ./configuration/mariadb-java-client-3.4.1.jar:/home/agent/libs/mariadb-java-client-3.4.1.jar
    env_file:
      - configuration/mysql.conf
    mem_limit: 6g
   ```
3. Move the previously downloaded `snowflake.json` file into the `configuration` directory.
4. Move the previously downloaded `mariadb-java-client-3.4.1.jar` file into the `configuration` directory.
5. In the `configuration` directory create `datasources.json` with content:

   Copy code

   ```
   {
     "MYSQLDS1": {
    "url": "jdbc:mariadb://host.docker.internal:3306/?allowPublicKeyRetrieval=true&useSSL=false",
    "username": "root",
    "password": "mysql",
    "ssl": false
     }
   }
   ```
6. In the `configuration` directory create `mysql.conf` with content:

   Copy code

   ```
   JAVA_OPTS=-Xmx5g
   MYSQL_DATASOURCE_DRIVERPATH=/home/agent/libs/mariadb-java-client-3.4.1.jar
   ```
7. Start the agent using the following command. There shouldn’t be any error message and the agent should generate a public and private key pair for authentication to Snowflake.

   Copy code

   ```
   docker compose stop  # stops the previous container in case you've launched it before
   docker compose rm -f # removes the agent container to recreate it with the latest image in case you had one before
   docker compose pull  # refresh remote latest tag in case you have cached previous version
   docker compose up -d # run the agent
   ```
8. Please note that the **driver jar file** name should be **identical** to the one downloaded and used in the `docker-compose.yaml` and `mysql.conf` files.

1. On the command line, navigate to the `agent-postgresql` directory.
2. Create the Docker Compose file `docker-compose.yaml` with the following content:

   Copy code

   ```
   services:
     postgresql-agent:
    container_name: postgresql-agent
    image: snowflakedb/database-connector-agent:latest
    volumes:
      - ./agent-keys:/home/agent/.ssh
      - ./configuration/snowflake.json:/home/agent/snowflake.json
      - ./configuration/datasources.json:/home/agent/datasources.json
    env_file:
      - configuration/postgresql.conf
    mem_limit: 6g
   ```
3. Move the previously downloaded `snowflake.json` file into the `configuration` directory.
4. In the `configuration` directory create `datasources.json` with content:

   Copy code

   ```
   {
     "PSQLDS1": {
    "url": "jdbc:postgresql://host.docker.internal:5432/postgres",
    "username": "postgres",
    "password": "postgres",
    "publication": "agent_postgres_publication",
    "ssl": false
     }
   }
   ```
5. In the `configuration` directory, create `postgresql.conf` with the following content:

   Copy code

   ```
   JAVA_OPTS=-Xmx5g
   ```
6. Start the agent using the following command. There shouldn’t be any error message and the agent should generate a public and private key pair for authentication to Snowflake.

   Copy code

   ```
   docker compose up -d
   ```

When complete, your directory structure should resemble the following. Please note the inclusion of the automatically generated private and public keys within the agent-keys directories.

```
.
├── agent-mysql
│   ├── agent-keys
│   │   ├── database-connector-agent-app-private-key.p8
│   │   └── database-connector-agent-app-public-key.pub
│   ├── configuration
│   │   ├── datasources.json
│   │   ├── mariadb-java-client-3.4.1.jar
│   │   ├── mysql.conf
│   │   └── snowflake.json
│   └── docker-compose.yaml
└── agent-postgresql
    ├── agent-keys
    │   ├── database-connector-agent-app-private-key.p8
    │   └── database-connector-agent-app-public-key.pub
    ├── configuration
    │   ├── datasources.json
    │   ├── postgresql.conf
    │   └── snowflake.json
    └── docker-compose.yaml
```

### Verifying connection with Snowflake

Go back to your previously created native apps. Click on the **Refresh** button in the Agent Connection section.

When successfully Configured you should see:

```
Agent is fully set up and connected. To select data to ingest Open Worksheet.
```

## Configure and monitor the data ingestion process

In this step, we will instruct the Connector to begin replicating the selected tables. First, let’s create a shared sink database in Snowflake.

Copy code

```
CREATE DATABASE CONNECTORS_DEST_DB;
GRANT CREATE SCHEMA ON DATABASE CONNECTORS_DEST_DB TO APPLICATION SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL;
GRANT CREATE SCHEMA ON DATABASE CONNECTORS_DEST_DB TO APPLICATION SNOWFLAKE_CONNECTOR_FOR_MYSQL;
```

Once the database is ready, we can move on to the configuration process.

MySQLPostgreSQL

1. To begin table replication, you must first add a datasource from which to replicate and then specify the table to be replicated.

   Copy code

   ```
   CALL SNOWFLAKE_CONNECTOR_FOR_MYSQL.PUBLIC.ADD_DATA_SOURCE('MYSQLDS1', 'CONNECTORS_DEST_DB');
   CALL SNOWFLAKE_CONNECTOR_FOR_MYSQL.PUBLIC.ADD_TABLES('MYSQLDS1', 'mysql_ingest_database', ARRAY_CONSTRUCT('mysql_rows'));
   ```
2. To monitor the replication, execute the following queries:

   Copy code

   ```
   SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_MYSQL.PUBLIC.REPLICATION_STATE;
   SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_MYSQL.PUBLIC.CONNECTOR_STATS;
   ```

1. To begin table replication, you must first add a data source from which to replicate and then specify the table to be replicated.

   Copy code

   ```
   CALL SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL.PUBLIC.ADD_DATA_SOURCE('PSQLDS1', 'CONNECTORS_DEST_DB');
   CALL SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL.PUBLIC.ADD_TABLES('PSQLDS1', 'psql_rows_schema', ARRAY_CONSTRUCT('postgres_rows'));
   ```
2. To monitor the replication you can execute the following queries

   Copy code

   ```
   SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL.PUBLIC.REPLICATION_STATE;
   SELECT * FROM SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL.PUBLIC.CONNECTOR_STATS;
   ```

### Understanding connector status

The `REPLICATION_STATE` view is crucial for monitoring the status of table replication. This process encompasses three distinct phases:

1. `SCHEMA_INTROSPECTION`: Ensures that the schema of the source table is accurately replicated.
2. `INITIAL_LOAD`: Transfers the existing data from the source table to the destination.
3. `INCREMENTAL_LOAD`: Continuously replicates ongoing changes from the source.

Upon successful replication, the status display will resemble the following:

> | REPLICATION\_PHASE | SCHEMA\_INTROSPECTION\_STATUS | SNAPSHOT\_REPLICATION\_STATUS | INCREMENTAL\_REPLICATION\_STATUS |
> | --- | --- | --- | --- |
> | INCREMENTAL\_LOAD | DONE | DONE | IN PROGRESS |
>
> Expand
>
> Show lessSee more

You can read more about it in the [official Connector Documentation](/connectors/postgres6/monitor#label-postgres-connector-monitoring-replication-state-6).

## View data

Execute the following commands to view data, which should include roughly 3 rows per database.

Copy code

```
SELECT * FROM CONNECTORS_DEST_DB."psql_rows_schema"."postgres_rows";
SELECT * FROM CONNECTORS_DEST_DB."mysql_ingest_database"."mysql_rows";
```

## Clean up and additional resources

Congratulations! You have successfully completed this tutorial.

To clean up your environment, execute the commands listed below. Failing to do so will leave the connector running and generating costs.

### Remove the native app

Copy code

```
DROP APPLICATION SNOWFLAKE_CONNECTOR_FOR_POSTGRESQL CASCADE;
DROP APPLICATION SNOWFLAKE_CONNECTOR_FOR_MYSQL CASCADE;
```

### Remove warehouses, roles and users

During the installation multiple warehouses, roles and users were created. Execute the following queries to drop those objects.

MySQLPostgreSQL

Copy code

```
DROP ROLE MYSQL_ADMINISTRATIVE_AGENT_ROLE;
DROP ROLE MYSQL_AGENT_ROLE;

DROP USER MYSQL_AGENT_USER;

DROP WAREHOUSE MYSQL_COMPUTE_WH;
DROP WAREHOUSE MYSQL_OPS_WH;
```

Copy code

```
DROP ROLE POSTGRESQL_ADMINISTRATIVE_AGENT_ROLE;
DROP ROLE POSTGRESQL_AGENT_ROLE;

DROP USER POSTGRESQL_AGENT_USER;

DROP WAREHOUSE POSTGRESQL_COMPUTE_WH;
DROP WAREHOUSE POSTGRESQL_OPS_WH;
```

### Stop database containers

To stop the running containers with MySQL and PostgreSQL, navigate to the directory containing the `docker-compose.yaml` files, then execute the `docker compose down -v`.

### Additional resources

Continue learning about connectors using the following resources:

- [About the Snowflake Connector for MySQL](/connectors/mysql6/about)
- [About the Snowflake Connector for PostgreSQL](/connectors/postgres6/about)
