# Snowpark Container Services troubleshooting

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

This topic discusses common issues and how you might resolve them.

## Image registry

- “invalid consent request” error received when accessing a public service endpoint.

  In the current implementation, Snowflake authenticates the current user using their default role. This error is probably
  because the user is using one of the privileged roles, such as ACCOUNTADMIN or SECURITYADMIN, as their default role
  (see [Blocking specific roles from using the integration](/user-guide/oauth-custom#label-oauth-custom-blocking-specific-roles-from-using-the-integration)). Use the
  [ALTER USER](/sql-reference/sql/alter-user) command to change the default role for the user, and try again.
- `docker login` authentication failure.

  Do not use an uppercase hostname in the `docker login` command and then use a lowercase hostname in the
  `docker push`, `docker pull` command. Docker CLI stores credentials with cased keys. Related Docker CLI
  [issue](https://github.com/docker/cli/issues/2753).
- `docker push` error: no Host in request URL.

  When interacting with Docker CLI, always replace the underscores in your account name in a URL with hyphens. Docker CLI will
  return an error if hostnames have underscores in them (even though cURL works). For example, the following Docker push
  specifies “my\_acct” as the account name:

  Copy code

  ```
  docker push myorg-my_acct.registry.snowflakecomputing.com/tutorial_db/data_schema/tutorial_repository/service_to_service
  ```

  Docker returns this error:

  ```
  Get "https:/v2/": http: no Host in request URL.
  ```

  You can also use the [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories) command to get a valid repository URL.

## Compute pool

- Suspended compute pool stuck in STOPPING state.

  Running services will prevent the compute pool from stopping. Suspend all remaining active services in the compute pool using
  the [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) command:

  Copy code

  ```
  ALTER COMPUTE POOL <pool_name> STOP ALL
  ```

## Service

- A running service is no longer responding to requests (from a service function or a public endpoint). The service status
  changed from running to pending.

  This could be an indication of resource starvation on compute pool nodes. If your containers are resource-intensive
  (CPU/memory), you should explicitly specify resource requests in the service specification to prevent too many
  services (including job services) being placed on a single node.

  In the current implementation, you can only specify memory requests.

  For example, if a node in the compute pool has 64 GB of RAM, requesting more than 32 GB for your service (or job service) would guarantee
  that only one service or job service can be running on a node at a time. For more information about the capability of each instance
  type, see [CREATE COMPUTE POOL](/sql-reference/sql/create-compute-pool).
- If you are submitting a request to the public endpoint for the service, do not use double quotes in the HTTP authentication
  header.

## Service functions

- Service function timeout and duplicate execution issues.

  If a single service function invocation takes longer than 30 seconds, Snowflake retries the function, and after a few retries,
  the function fails with a timeout error. You might get unexpected results if the function implementation in the container is
  not idempotent. Consider using asynchronous execution by returning a different HTTP code (202), which allows a longer timeout.
  For more information, see [Asynchronous remote service](/sql-reference/external-functions-implementation#label-external-functions-implementation-asynchronous-remote-service).

## Ingress

- If authentication fails, it might be because of the network policy associated with the user or account.
- When accessing the public endpoint from the internet, you might find that username/password authentication works, but SSO results in a blank page or the error: “OAuth client integration with the given client ID is not found.”. For information about addressing this issue, see [Ingress and SSO considerations](/developer-guide/snowpark-container-services/service-network-communications#label-additional-considerations-ingress-sso).
- When a client receives a 5XX error from an ingress endpoint (500/503/504), the client should retry, with some backoff. We recommend bounded [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff).
- A CORS pre-flight request returns status 404-Endpoint does not exist:

  Check if the endpoint exists by running the [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints) command.
- A CORS pre-flight request returns status 302.

  The CORS request did not have any form of authentication. Due to the inability to distinguish between CORS requests and redirects/anchor tags, we have to assume it’s a redirect/anchor tag case and return a 302.
- Response status 403 “Rejecting a CORS request since cookie was present, and request does not have an auth header”.

  This occurs when a cross-origin non-GET non-HEAD request is attempting to use cookie as the authentication method. The Authentication header is required for these cross-origin requests. This error occurs when the request has cookies present and the Authentication header is not present.
- Error message “Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at …”.

  Browser returns this error when the service indicated it does not support the requested cross-origin access. This typically happens because the `Origin` provided by the browser does not match one of the origins specified in `Access-Control-Allow-Origin` in the service specification for the endpoint. For these to match, both the scheme (HTTP/HTTPS) and hostname must match.
