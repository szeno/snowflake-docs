# Use Gateways to route ingress requests to multiple endpoints

If you want to expose multiple service endpoints behind a single host name, you can create a *gateway*
. A gateway has a hostname similar to a public service endpoint. For more information about public service endpoints, see [Configure service ingress](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-ingress).

Gateways route [ingress requests](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-ingress), including [inference requests](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api), from outside Snowflake to one or more service endpoints. With Gateways, you can do the following:

- **Traffic split among services:** You can allow multiple services to share the same hostname. Routing is done based on the percentage given for each service. This is useful in the following scenarios:

  - **A/B testing scenario:** You might choose to update a service and deploy it while keeping the original service running. For testing, you might choose to route a certain percentage of incoming ingress requests to the updated service for testing.
  - **High-availability scenario:** You have a highly available service that is deployed across, say, two compute pools, where each compute pool is created in a different [placement group](/developer-guide/snowpark-container-services/working-with-compute-pool#label-spcs-working-with-compute-pool-placement-group). You might choose to use the gateway to split incoming ingress requests.
- **Shadow traffic:** You can send all requests to a primary endpoint and mirror a percentage of requests to one or more shadow endpoints. The primary endpoint handles production responses. Responses from shadow endpoints aren’t returned to clients. Use shadow traffic to test a challenger service with production request patterns without directing production responses through that service.

  [Preview Feature](/release-notes/preview-features) — Open

  Shadow traffic gateways are available to all accounts.
- **Stable URL:** Each gateway has a hostname allocated at creation. The hostname doesn’t change for the lifetime of the gateway object. You can alter the gateway object to route to different endpoints or have different percentage configurations. Changes take effect within a minute.

The following list shows the differences between a service endpoint and a gateway:

- **Browser security:** Service endpoint supports CORS configuration (corsSettings) and cloud service provider (CSP) headers for browser-based access through external access integrations. A gateway currently doesn’t support CORS or CSP headers.
- **Caller’s rights:** Service endpoint supports caller’s rights. A gateway currently doesn’t support caller’s rights.
- **Role-based access control (RBAC):** When you use a service endpoint, access is managed by using [service roles](/developer-guide/snowpark-container-services/working-with-services#label-spcs-manage-service-related-privileges-service-roles).
  When you use a gateway, access is managed by granting the USAGE privilege on the gateway object. Users accessing a gateway don’t need service roles for the underlying service endpoints.

Gateway routing respects the relative percentage of the specified healthy endpoints. For more information about a
gateway’s failover behavior, see [Gateway failover behavior](#label-gateway-failover-behavior).

After you’ve reviewed the following sections, you can create and alter a gateway. For information about creating a gateway, see [CREATE GATEWAY](/sql-reference/sql/create-gateway). For information about altering a gateway, see [ALTER GATEWAY](/sql-reference/sql/alter-gateway).

## Access control requirements

The owner role of the gateway must have the following privileges:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE GATEWAY | Schema | Required to create a gateway. |
| BIND SERVICE ENDPOINT | Account | Required to bind service endpoints to the gateway. |
| USAGE | Database | Required to access the database containing the gateway. |
| USAGE | Schema | Required to access the schema containing the gateway. |
| USAGE | Target endpoints | Required to route traffic to the target endpoints. |
| MODIFY or OWNERSHIP | Gateway | Required to alter the gateway configuration. |
| USAGE, MODIFY, or OWNERSHIP | Gateway | Required to view the gateway specification. |

Expand

Show lessSee more

Note

When listing gateways, Snowflake only shows gateways that the role has USAGE, MODIFY, or OWNERSHIP privileges on. The role used must also have USAGE privileges on the database and schema containing the gateway.

For gateway CREATE, ALTER, and DROP operations, see [CREATE GATEWAY](/sql-reference/sql/create-gateway),
[ALTER GATEWAY](/sql-reference/sql/alter-gateway), and [DROP GATEWAY](/sql-reference/sql/drop-gateway).

## Configurations

By default, you get a maximum of 5 endpoints per gateway. For additional endpoints, contact support to split traffic into more endpoints. To configure a traffic split or shadow traffic gateway, see [CREATE GATEWAY](/sql-reference/sql/create-gateway).

## Gateway failover behavior

Gateway failover is the process where a gateway automatically redirects traffic from one endpoint (Endpoint A) to
other endpoints when Endpoint A becomes unavailable or non-operational.

Note

Snowflake does not fail over onto an endpoint with 0% traffic split or a shadow endpoint with a `weight` of 0. The endpoint must have at least 1% traffic.

The relative percentage of the available endpoints is respected.

Failover from one endpoint (Endpoint A) to other endpoints with at least 1% traffic split happens if any of the
following conditions is true:

- The service of Endpoint A is suspended and `auto_resume` is set to false.
- The compute pool of Endpoint A is suspended.
- The service of Endpoint A fails the readiness probe. This is updated once every 40 seconds (cache refresh rate) at
  the longest. At the time of the update, traffic is immediately adjusted with no ramp up period.
- The service of Endpoint A is dropped.
- The gateway owner role loses privilege (USAGE or OWNERSHIP) on Endpoint A.
