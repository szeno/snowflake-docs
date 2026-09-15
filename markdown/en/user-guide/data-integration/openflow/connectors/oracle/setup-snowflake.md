# Openflow Connector for Oracle: Set up Snowflake

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Note

The Openflow Connector for Oracle is also subject to additional terms of service beyond the standard
connector terms of service. For more information, see the
[Openflow Connector for Oracle Addendum](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/openflow-oracle-terms/).

This topic describes how to set up your Snowflake environment for the
Openflow Connector for Oracle.

## Snowflake account setup

As an Openflow administrator, perform the following tasks for this connector. With the
default `SNOWFLAKE_MANAGED` authentication strategy, the runtime’s execute-as role is the identity
the connector uses to access Snowflake, so you grant these privileges to that role rather than
creating a separate service user.

1. Create a database to store the replicated data, and grant the execute-as role
   [USAGE and CREATE SCHEMA](/user-guide/security-access-control-privileges#label-database-privileges) on it. The connector creates
   destination schemas automatically. Snowflake recommends a dedicated destination database per
   connector, to avoid collisions with other data sources including other connectors.

   Keep this destination database separate from the database that holds your Openflow
   infrastructure objects, such as the runtime, the connector, and any secrets. A connector
   creates destination objects based on the source schema and table names, so those names aren’t
   under your control and can change as the source changes.

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS <destination_database>;

   GRANT USAGE ON DATABASE <destination_database> TO ROLE <execute_as_role>;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO ROLE <execute_as_role>;
   ```
2. Designate a warehouse for the connector to use, and grant the execute-as role **USAGE** and
   **OPERATE** on it. Start with the `XSMALL` warehouse size, then experiment with size depending
   on the number of tables being replicated, and the amount of data transferred. Large table
   numbers typically scale better with
   [multi-cluster warehouses](/user-guide/warehouses-multicluster), rather than the warehouse size.

   Copy code

   ```
   CREATE WAREHOUSE <ingest_warehouse>
     WITH
       WAREHOUSE_SIZE = 'XSMALL'
       AUTO_SUSPEND = 300
       AUTO_RESUME = TRUE;

   GRANT USAGE, OPERATE ON WAREHOUSE <ingest_warehouse> TO ROLE <execute_as_role>;
   ```
3. **Snowflake deployments only:** Make sure this connector’s source host and port are permitted
   by a network rule that your runtime’s external access integration (EAI) allows.

   The EAI itself belongs to the runtime, not to this connector. You create it once, attach it to
   the runtime, and grant the execute-as role `USAGE` on it. For those steps, see
   [Creating network rules and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-network-rules-and-external-access-integrations).
   What is specific to this connector is getting its source host into a rule that EAI references.

   The rule takes the source’s host and port as a single value, such as `db.example.com:<port>`.
   That’s the host and port from the connector’s connection URL, without the `jdbc:` scheme, the
   driver name, or the database path.

   BYOC deployments handle outbound connectivity in the cloud environment and don’t use EAIs or
   network rules.

### Additional setup for key-pair authentication (BYOC only)

Key-pair authentication is available only for BYOC deployments, and is not required for the
default `SNOWFLAKE_MANAGED` authentication strategy. Skip this section unless you set the
connector’s **Snowflake Authentication Strategy** parameter to `KEY_PAIR`.

1. Create a Snowflake user with the type as [SERVICE](/sql-reference/sql/create-user#label-user-type-property), create a role for
   it, and grant that role the same destination database and warehouse privileges you granted the
   execute-as role:

   Copy code

   ```
   CREATE USER <username> TYPE=SERVICE COMMENT='Service user for automated access of Openflow';
   CREATE ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL TO USER <username>;

   GRANT USAGE ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT CREATE SCHEMA ON DATABASE <destination_database> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE, OPERATE ON WAREHOUSE <ingest_warehouse> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
2. Create a pair of secure keys (public and private). Store the private key for the user in a file
   to supply to the connector’s configuration. Assign the public key to the Snowflake service user:

   Copy code

   ```
   ALTER USER <username> SET RSA_PUBLIC_KEY = 'thekey';
   ```

   For more information, see [pair of keys](/user-guide/key-pair-auth).

When using `KEY_PAIR`, you must also set the connector’s **Snowflake Account Identifier** and
**Snowflake Connection Strategy** parameters. Both are left blank or ignored under
`SNOWFLAKE_MANAGED`.

## Next steps

[Configure the connector](/user-guide/data-integration/openflow/connectors/oracle/setup-connector).
