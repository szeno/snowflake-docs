# Set up Openflow - Snowflake Deployment: Create the execute-as role and external access integrations

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow - Snowflake Deployment runtimes need a few supporting resources before they can access your data:

- An execute-as role that flows use to access Snowflake objects
- Network rules and external access integrations (EAI) that let the runtime reach external data sources

This topic describes the creation of these resources.

1. Create an execute-as role and grant it the privileges needed to write data to Snowflake.
2. Associate the execute-as role with the runtime.
3. Create external access integrations and associate them with the runtime.
   See [Creating network rules and external access integrations](#label-create-network-rules-and-external-access-integrations).
4. Configure outbound PrivateLink if required to connect to a private system using SPCS egress.

## Create the execute-as role

When creating an Openflow runtime, you associate a role with it. Flows that run within the runtime
execute as this role, so it’s called the execute-as role. You can reuse the same execute-as role
across multiple runtimes. For more information, see
[What is an execute-as role?](/user-guide/data-integration/openflow/about-spcs#label-openflow-spcs-what-is-runtime-role).

Creating the role is a prerequisite for creating a runtime:

1. Create the role.

   Note

   `<RUNTIME_NAME>` denotes the name of the associated runtime.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE ROLE IF NOT EXISTS OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;

   GRANT ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL TO ROLE OPENFLOW_ADMIN;
   ```
2. Allow the execute-as role to use an existing warehouse that you plan to use for data ingestion.
   Use this warehouse later when configuring your connectors for runtimes where you use this execute-as role.

   Copy code

   ```
   GRANT USAGE, OPERATE ON WAREHOUSE <OPENFLOW_INGEST_WAREHOUSE> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```
3. Allow the execute-as role to use, create, or otherwise access Snowflake objects.

   Note

   Depending on the Openflow connector being created, the required underlying objects vary.
   The example below is for illustration purposes only.

   Copy code

   ```
   GRANT USAGE ON DATABASE <openflow_db> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   GRANT USAGE ON SCHEMA <openflow_schema> TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

## Creating network rules and external access integrations

The following steps apply to both gen 1 and gen 2 Snowflake deployments. Both generations
require network rules and EAIs so the runtime can reach external data sources.

Snowflake’s security model provides secure access to specific endpoints and systems
external to Snowflake using [network policies](/user-guide/network-policies).

Two key aspects of network policies are [Network rules](/user-guide/network-rules) and
[External Access Integrations (EAI)](/developer-guide/external-network-access/external-network-access-overview).
Each of which is used to provide secure access to external resources required by the runtime.

There are three steps that are required to create network rules and external access integrations:

1. Create the network rule, grouping the network identifiers into logical areas.
2. Create the external access integration (EAI), specifying the list of network rules and ensuring the execute-as role has USAGE on the EAI.
3. Associate the EAI with the Runtime in the Openflow UI when creating Runtimes.

To create the required network rule and EAI, perform the following steps:

Note

These examples use RUNTIME\_NAME as a placeholder for the name of the Runtime being created.

Do not use CREATE OR REPLACE on network rules or EAIs

Replacing a network rule or external access integration silently detaches it from every runtime
that references it. Use `CREATE ... IF NOT EXISTS` for new objects, and `ALTER` to modify existing
ones.

1. Create an appropriate network rule. See [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule) for more information.

   Note

   Snowflake recommends creating network rules in the same infrastructure schema
   (`openflow_db.openflow_schema`) you’ve been using for Openflow objects, so that
   everything is in one place. An EAI is an account-level object, so it has no
   database or schema; a network rule is a schema-level object. Where you keep the
   network rule is your choice as long as the execute-as role has access to the
   EAI, but using the infrastructure schema keeps things simple and consistent.

   Copy code

   ```
   USE DATABASE <openflow_db>;
   USE SCHEMA <openflow_schema>;

   CREATE NETWORK RULE IF NOT EXISTS OPENFLOW_<RUNTIME_NAME>_NETWORK_RULE
    MODE = EGRESS
    TYPE = HOST_PORT
    VALUE_LIST = ('comma separated list of host:port pairs');
   ```
2. Create an external access integration, or add the network rule to an existing one.
   See [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration) for more information.

   To create a new EAI:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   CREATE EXTERNAL ACCESS INTEGRATION IF NOT EXISTS OPENFLOW_<RUNTIME_NAME>_EAI
   ALLOWED_NETWORK_RULES = (OPENFLOW_<RUNTIME_NAME>_NETWORK_RULE)
   ENABLED = TRUE;
   ```

   To add the network rule to an existing EAI, first check which rules are already
   associated with it, then update the EAI to include both the existing and new rules:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   -- Check the current rules on the EAI
   DESCRIBE EXTERNAL ACCESS INTEGRATION OPENFLOW_<RUNTIME_NAME>_EAI;
   ```

   In the output, find the `ALLOWED_NETWORK_RULES` property and note the existing rules.
   Then update the EAI, listing all existing rules along with the new one:

   Copy code

   ```
   ALTER EXTERNAL ACCESS INTEGRATION OPENFLOW_<RUNTIME_NAME>_EAI
   SET ALLOWED_NETWORK_RULES = (
      <EXISTING_RULE_1>,
      <EXISTING_RULE_2>,
      OPENFLOW_<RUNTIME_NAME>_NETWORK_RULE
   );
   ```
3. Grant access to the EAI to the previously created execute-as role.

   Copy code

   ```
   GRANT USAGE ON INTEGRATION OPENFLOW_<RUNTIME_NAME>_EAI TO ROLE OPENFLOW_<RUNTIME_NAME>_EXECUTE_AS_RL;
   ```

Do not use CREATE OR REPLACE on network rules or EAIs

Replacing a network rule or external access integration silently detaches it from every runtime
that references it. Use `CREATE ... IF NOT EXISTS` for new objects, and `ALTER` to modify existing
ones.

## Next steps

[Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime)
