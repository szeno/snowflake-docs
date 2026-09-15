# Configuring private connectivity

This section explains inbound private connectivity (to endpoints exposed by Snowpark Container Services) and outbound private connectivity (egress traffic from your service).

## Inbound connectivity

Snowpark Container Services exposes three endpoints:

- **Image registry service:** It serves the OCIv2 API for you to upload your application images to a repository in your Snowflake account. For more information, see [Snowpark Container Services: Working with an image registry and repository](/developer-guide/snowpark-container-services/working-with-registry-repository).
- **Public endpoints exposed by a service:** You can allow users, in your account, access to your service from outside Snowflake (ingress) by declaring one or more endpoints as public. For more information, see [Using a service](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating).
- **Authentication endpoint:** When a user attempts to access a service’s public endpoint, Snowpark Container Services redirects the user through this endpoint for authentication.

This section explains how to enable private connectivity to these endpoints.

Note

- When configuring private connectivity, you control the DNS resolution; there are no DNS records controlled by Snowflake.

### Configure prerequisites

To enable private connectivity to Snowpark Container Services, first configure private connectivity to connect your Snowflake account to your cloud provider account’s network. For more information, see [Inbound private connectivity to Snowflake service](/user-guide/private-connectivity-inbound#label-private-connect-snowflake-service).

In addition, create CNAME records in your DNS for the `regionless-privatelink-account-url` value returned from calling [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config).

### Configure public endpoints access

To enable ingress requests from your network to your service’s public endpoint:

1. Call [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) in your Snowflake account to get a list of hostnames for your account. In the output:

   1. `app-service-privatelink-url` key provides a wildcard hostname for Snowpark Container Services public endpoints.
   2. `spcs-auth-privatelink-url` key provides the hostname required for routing Snowpark Container Services authentication.
2. To access Snowflake via private connectivity, you must create CNAME records in your DNS to resolve the endpoint values from the SYSTEM$GET\_PRIVATELINK\_CONFIG function to your private network.

   You can enable per-account hostname routing by setting the
   [ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_PRIVATELINK\_URL](/sql-reference/parameters#label-enable-per-account-app-service-privatelink-url)
   account parameter to `TRUE`.When enabled, the `app-service-privatelink-url` key returned by the function returns
   a per-account wildcard hostname in the format `*.orgname-account-name.region.cloud.privatelink.snowflake.app`.
   Before enablement, the function returns a `app-service-privatelink-url-next` key with this value. Use this value to create a
   single CNAME record scoped to your account for all Snowpark Container Services endpoints.

   Update your private DNS entries and firewall rules to use the new URL format before you enable this parameter.

### Configuring access to Snowpark Container Services Registry in Snowflake

1. Call SYSTEM$GET\_PRIVATELINK\_CONFIG in your Snowflake account to get a list of hostnames for your account. In the output, the `spcs-registry-privatelink-url` key provides the hostname required for routing Snowpark Container Services image registry requests.
2. To access Snowflake via private connectivity, it is necessary to create records in your DNS to resolve the endpoint values from the SYSTEM$GET\_PRIVATELINK\_CONFIG function to your private network.

### Security considerations

The following apply for public endpoints that services expose:

- Each endpoint can serve both HTTPS-encrypted traffic and WebSocket-encrypted traffic.
- Each endpoint has their own top-level domain, with no shared elements with Snowsight. This ensures that browsers isolate services from Snowsight and services from each other, mitigating risks of cross-origin attacks.

## Outbound connectivity

Instead of routing network egress via the public internet, you might opt to direct your service’s egress traffic through a private connectivity endpoint. For more information, see [Network egress using private connectivity](/developer-guide/snowpark-container-services/service-network-communications#label-working-with-services-jobs-egress-private).
