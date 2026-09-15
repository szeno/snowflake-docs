# Snowflake Connector for Kafka: Configure Snowflake

This topic describes the steps to configure Snowflake for Snowflake Connector for Kafka.

Snowflake recommends that you create a separate user, using [CREATE USER](/sql-reference/sql/create-user) and role using [CREATE ROLE](/sql-reference/sql/create-role) for each Kafka instance so that the access privileges can be individually revoked as required.

## Creating a role to use the Kafka connector

The following creates a custom role for use by the Kafka connector, for example KAFKA\_CONNECTOR\_ROLE.
The script references a specific existing database and schema (`kafka_db.kafka_schema`)
and user (`kafka_connector_user_1`):

Copy code

```
-- Use a role that can create and manage roles and privileges.
USE ROLE securityadmin;

-- Create a Snowflake role with the privileges to work with the connector.
CREATE ROLE kafka_connector_role;

-- Grant privileges on the database.
GRANT USAGE ON DATABASE kafka_db TO ROLE kafka_connector_role;

-- Grant privileges on the schema.
GRANT USAGE ON SCHEMA kafka_schema TO ROLE kafka_connector_role;

-- Grant OPERATE on pipes only if you manually created them (user-defined pipe mode).
-- GRANT OPERATE ON PIPE existing_pipe1 TO ROLE kafka_connector_role;

-- Grant INSERT on the table to insert data into.
GRANT INSERT ON TABLE kafka_schema.existing_table TO ROLE kafka_connector_role;

-- Grant the custom role to the user configured in the Kafka connector configuration properties.
GRANT ROLE kafka_connector_role TO USER kafka_connector_user;
```

Note that any privileges must be granted directly to the role used by the connector. Grants cannot be inherited from role hierarchy.

For more information on creating custom roles and role hierarchies, see [Configuring access control](/user-guide/security-access-control-configure).

## Required privileges

The connector requires the following privileges to create and manage Snowflake objects:

| Object | Privilege | When Required |
| --- | --- | --- |
| Database | USAGE | Always required |
| Schema | USAGE | Always required |
| Schema | CREATE TABLE | If the connector auto-creates tables |
| Schema | CREATE PIPE | If the connector auto-creates pipes (default pipe mode) |
| Schema | CREATE VIEW | Recommended for future Error Table features |
| Pipe | OPERATE | If using user-defined pipes |
| Destination table | INSERT | Always required |

Expand

Show lessSee more

## Next steps

[Set up Kafka](/user-guide/kafka-connector/setup-kafka).
