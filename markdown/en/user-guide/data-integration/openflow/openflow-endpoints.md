# Openflow Endpoints

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow endpoints let external systems push data into an Openflow runtime using a stable HTTPS URL. After you create a custom flow with a compatible Listen processor, you attach an endpoint to that processor and send requests to the endpoint URL from an external HTTP client.

![Openflow endpoints are created in a deployment and attached to a ListenHTTP or ListenOTLP processor in a runtime. External clients authenticate with a PAT and send requests to the endpoint URL, which Openflow routes to the attached processor.](/static/images/openflow-endpoints-architecture.svg)

## Before you begin

Before you start, confirm the following:

- You have an Openflow deployment and at least one runtime. The deployment must be on one of the following Openflow deployment versions:
  - Snowflake Deployments (SPCS): 1.53 or later
  - BYOC deployments: 1.70.0 or later
- You have a custom flow that uses a compatible HTTP Listen processor, such as [ListenHTTP](/user-guide/data-integration/openflow/processors/listenhttp) or [ListenOTLP](/user-guide/data-integration/openflow/processors/listenotlp).

## Grant endpoint management privileges

Endpoint management uses existing Openflow privileges. A role with `USAGE` or `OWNERSHIP` on a deployment or runtime can manage endpoints in that scope.

Grant access at one of these levels:

| Grant on | The role can |
| --- | --- |
| Deployment | Create endpoints and manage every endpoint in the deployment. |
| Runtime | Create endpoints that target processors in the runtime, manage endpoints that route to the runtime, and manage endpoints in the same deployment that have no target processor. |

Expand

Show lessSee more

The grant syntax depends on the [generation](/user-guide/data-integration/openflow/gen2/openflow-generations) of the deployment:

- **Gen 2**, including objects migrated from gen 1: Grant on the `OPENFLOW DEPLOYMENT` or `OPENFLOW RUNTIME` object.
- **Gen 1:** Grant on the deployment’s or runtime’s `INTEGRATION` object.

Sending data to an endpoint requires [separate privileges](#label-openflow-endpoints-create-service-user).

### Grant access to specific runtimes

Use this option to limit a data engineer to endpoints that route to selected runtimes. The role can also manage endpoints in the same deployment that have no target processor.

#### Gen 2 runtimes

Grant `USAGE` on the runtime and its database and schema:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_runtime_de_rl;

GRANT USAGE ON DATABASE <runtime_db> TO ROLE openflow_runtime_de_rl;
GRANT USAGE ON SCHEMA <runtime_db>.<runtime_schema> TO ROLE openflow_runtime_de_rl;
GRANT USAGE ON OPENFLOW RUNTIME <runtime_db>.<runtime_schema>.<runtime_name>
  TO ROLE openflow_runtime_de_rl;
GRANT ROLE openflow_runtime_de_rl TO USER <openflow_data_engineer_user>;
```

Repeat the runtime grant for each runtime the role should manage, and grant access to each containing database and schema as needed.

#### Gen 1 runtimes

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_runtime_de_rl;

SHOW INTEGRATIONS LIKE 'OPENFLOW_RUNTIME_%';
-- Find the integration that matches your runtime ID from the Openflow UI.
-- Hyphens in the runtime ID are replaced with underscores in the integration name.

GRANT USAGE ON INTEGRATION openflow_runtime_<runtime_id> TO ROLE openflow_runtime_de_rl;
GRANT ROLE openflow_runtime_de_rl TO USER <openflow_data_engineer_user>;
```

Repeat the integration grant for each gen 1 runtime the role should manage.

### Grant access to an entire deployment

Use this option when a data engineer should manage endpoints for all runtimes in a deployment, including runtimes created later.

#### Gen 2 deployments

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_deployment_de_rl;

GRANT USAGE ON OPENFLOW DEPLOYMENT <deployment_name> TO ROLE openflow_deployment_de_rl;
GRANT ROLE openflow_deployment_de_rl TO USER <openflow_data_engineer_user>;
```

This grant authorizes endpoint management across the deployment. For runtime access, see [Authorization differences](/user-guide/data-integration/openflow/gen2/openflow-generations#label-openflow-generations-authorization).

#### Gen 1 deployments

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_deployment_de_rl;

SHOW INTEGRATIONS LIKE 'OPENFLOW_DATAPLANE_%';
-- Find the integration that matches your deployment ID from the Openflow UI.
-- Hyphens in the deployment ID are replaced with underscores in the integration name.

GRANT USAGE ON INTEGRATION openflow_dataplane_<deployment_id> TO ROLE openflow_deployment_de_rl;
GRANT ROLE openflow_deployment_de_rl TO USER <openflow_data_engineer_user>;
```

## Create a service user for data ingress

External clients authenticate to an Openflow endpoint with a programmatic access token (PAT) that belongs to a service user. To configure authentication, create a service user, generate a PAT for it, and configure your HTTP client to send the PAT in an `Authorization: Bearer` header with each request.

An account administrator or authorized Openflow admin creates the service user, grants its role access to the endpoint’s **target runtime**, and generates the PAT. To send authenticated requests, the PAT’s restricted role must have `USAGE`, `OPERATE`, or `OWNERSHIP` on the endpoint’s target runtime. For a gen 1 runtime, grant the corresponding privilege on its Openflow runtime `INTEGRATION` object.

### Grant the sender role access to the target runtime

Create the role:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS openflow_endpoint_data_sender
  COMMENT = 'Role for sending data to Openflow endpoints';
```

For a **gen 2 runtime**, grant access to the runtime and its database and schema:

Copy code

```
GRANT USAGE ON DATABASE <runtime_db> TO ROLE openflow_endpoint_data_sender;
GRANT USAGE ON SCHEMA <runtime_db>.<runtime_schema> TO ROLE openflow_endpoint_data_sender;
GRANT USAGE ON OPENFLOW RUNTIME <runtime_db>.<runtime_schema>.<runtime_name>
  TO ROLE openflow_endpoint_data_sender;
```

For a **gen 1 runtime**, grant the corresponding privilege on its Openflow runtime `INTEGRATION` object:

Copy code

```
SHOW INTEGRATIONS LIKE 'OPENFLOW_RUNTIME_%';
-- Find the integration that matches the runtime attached to your endpoint.

GRANT USAGE ON INTEGRATION openflow_runtime_<runtime_id> TO ROLE openflow_endpoint_data_sender;
```

### Create the service user

Use the sender role as the service user’s default role, and grant that role to the service user. The role must already have the target-runtime grants.

Copy code

```
CREATE USER IF NOT EXISTS data_source_service_user
  TYPE = SERVICE
  DEFAULT_ROLE = openflow_endpoint_data_sender
  COMMENT = 'Service user for sending data to Openflow endpoints';

GRANT ROLE openflow_endpoint_data_sender TO USER data_source_service_user;
```

### Restrict network access

By default, a service user must be subject to a network policy to generate or use a PAT. An authentication policy can change this requirement. For details, see [Network policy requirements](/user-guide/programmatic-access-tokens#label-pat-prerequisites-network).

Limit the policy to the source addresses that send requests to the endpoint. Network rules can identify IPv4 addresses, IPv6 addresses, or private-connectivity endpoints. Use the rule type that matches the path your client uses. For the rule types and for how to activate a policy, see [Network rules](/user-guide/network-rules) and [Controlling network traffic with network policies](/user-guide/network-policies).

Replace `<client_ip_address>` with the public source address of the client that sends requests to the endpoint.

Copy code

```
CREATE OR REPLACE NETWORK RULE openflow_db.openflow_schema.openflow_data_source_allowed_ips
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('<client_ip_address>/32');

CREATE OR REPLACE NETWORK POLICY openflow_data_source_network_policy
  ALLOWED_NETWORK_RULE_LIST = ('openflow_db.openflow_schema.openflow_data_source_allowed_ips');

ALTER USER data_source_service_user
  SET NETWORK_POLICY = openflow_data_source_network_policy;
```

### Generate a role-restricted PAT

Set the PAT’s `ROLE_RESTRICTION` to the sender role.

Copy code

```
ALTER USER IF EXISTS data_source_service_user
  ADD PROGRAMMATIC ACCESS TOKEN data_source_service_user_openflow_pat
  ROLE_RESTRICTION = openflow_endpoint_data_sender
  DAYS_TO_EXPIRY = 365
  COMMENT = 'PAT for sending data to Openflow endpoints';
```

Copy the PAT secret from the command output and store it securely. You can’t retrieve it later. If your authentication policy requires a shorter token lifetime, reduce `DAYS_TO_EXPIRY` accordingly.

For more information about PAT prerequisites, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

## Design a custom flow with ListenHTTP

Before you create an endpoint, build and start a custom flow that contains a compatible Listen processor.

Snowflake recommends starting with the [ListenHTTP](/user-guide/data-integration/openflow/processors/listenhttp) processor.

1. In the runtime UI, create a process group for your custom flow.
2. Add a **ListenHTTP** processor to the process group.
3. Configure the processor:
   - **Settings > Name**: Give the processor a descriptive name, such as `ListenHTTP for Foo data`.
   - **Properties > Base Path**: Select **Set empty string** so the processor accepts requests sent to the endpoint URL.
   - **Properties > Listening Port**: Choose an integer between `1024` and `65535` that is not already used by another Listen processor on the same runtime and is not one of the Openflow-reserved ports: `3448`, `8443`, `8444`, `8445`, or `52020`.
   - **Properties > SSL Context Service**: Create an `OpenflowRuntimeSSLContextProvider` service, enable it, and select it for the processor.
4. Connect the Listen processor to the rest of your flow logic.
5. Start the process group.

The listening port is used only inside Openflow to route traffic from the endpoint to the correct processor. External clients always send requests to the endpoint URL on HTTPS port `443`.

## Create and attach an endpoint

After the custom flow is running, create an endpoint in the Openflow control plane UI.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Ingestion** » **Openflow**.
3. Select **Launch Openflow**.
4. On the **Deployments** tab, open the action menu for your deployment and select **Manage endpoints**.
5. Select **Create**.
6. Enter a name and description, then select the Listen processor you configured in your custom flow.
7. Wait for the endpoint to reach the **Attached** state.

Copy the full endpoint URL from the **URL PATH** column on the **Manage endpoints** page. Configure your HTTP client to send requests to this URL.

## Test the endpoint with curl

After the endpoint is attached, test data ingress with the service user PAT and the endpoint URL.

Copy code

```
curl -X POST \
  -H "Authorization: Bearer YOUR_SERVICE_USER_PAT" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, Snowflake."}' \
  YOUR_ENDPOINT_URL
```

A successful response, such as HTTP `200`, confirms the following:

- The PAT was authenticated by the Openflow ingress controller.
- The service user was authorized to use the endpoint.
- The request was routed to the correct runtime and Listen processor.
- The payload was accepted by the flow.

You should also see the request reflected in the runtime flow metrics in the Openflow UI.

## Troubleshoot endpoint requests

Use the following checks when endpoint requests fail.

### Endpoint management is unavailable or permission checks fail

- Confirm the deployment is on Openflow deployment version 1.53 or later for Snowflake Deployments, or 1.70.0 or later for BYOC deployments.
- Confirm the active Openflow role has `USAGE` or `OWNERSHIP` on the deployment or the relevant runtime object. For gen 1, check the corresponding integration.
- For gen 2 runtime-based access, also check `USAGE` on the runtime’s database and schema.
- If the UI reports that a permission check failed, retry the check.

### Listen processor is not available as an endpoint target

- Confirm the runtime is upgraded to a version that supports Openflow endpoints.
- Confirm the processor uses an HTTP-based Listen processor, such as [ListenHTTP](/user-guide/data-integration/openflow/processors/listenhttp) or [ListenOTLP](/user-guide/data-integration/openflow/processors/listenotlp).
- Confirm the processor has a configured listening port.
- Confirm your role has endpoint management access to the deployment or the runtime that contains the processor.
- Wait about 30 seconds and try again. Openflow might still be discovering the processor.

### HTTP requests fail with status code 401

- Confirm the request includes the service user PAT in the `Authorization: Bearer` header.
- Confirm the PAT has not expired.

### HTTP requests fail with status code 403

- Confirm the role in the PAT’s `ROLE_RESTRICTION` has `USAGE`, `OPERATE`, or `OWNERSHIP` on the endpoint’s target runtime. For gen 1, check the Openflow runtime `INTEGRATION` object instead.
- For gen 2, also check `USAGE` on the runtime’s database and schema.

### HTTP requests fail with status code 404

- Confirm the endpoint is in the **Attached** state.
- Confirm you are using the correct endpoint URL.

### HTTP requests fail with status code 405

- Confirm the ListenHTTP processor **Base Path** property is set to **Set empty string**.

### HTTP requests fail with a connection timeout or status code 500

- Confirm the Listen processor and its `OpenflowRuntimeSSLContextProvider` service are enabled and running.
- Confirm the runtime is active and reachable in the Openflow UI.
- Confirm the endpoint is attached and you are using the correct URL.
