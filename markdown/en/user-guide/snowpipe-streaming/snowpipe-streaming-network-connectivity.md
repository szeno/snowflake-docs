# Network connectivity prerequisites for Snowpipe Streaming

Complete these prerequisites from the VM, container, pod, or Kafka Connect worker that sends streaming requests. This procedure applies to the high-performance architecture with Named or Elastic Channels, including the Java, Python, and Node.js SDKs, direct REST clients, and Kafka Connector v4. It doesn’t describe the classic architecture.

## Required destinations

Successful access to your Snowflake account doesn’t establish access to the separate streaming ingest endpoint or SDK upload destinations.

| Destination | Required for | How to identify it | Port |
| --- | --- | --- | --- |
| Snowflake account endpoint | All streaming clients: authentication and ingest-host discovery | Your [account URL](/user-guide/admin-account-identifier); for private connectivity, `privatelink-account-url` from `SYSTEM$GET_PRIVATELINK_CONFIG` | HTTPS 443 |
| Streaming ingest endpoint | All streaming clients: streaming management and data operations | Authenticated `GET /v2/streaming/hostname` through the account endpoint | HTTPS 443 |
| Cloud-storage upload endpoints | SDK clients and Kafka Connector v4 | Storage destinations returned by Snowflake for SDK uploads; use the account’s hostname inventory as a starting point | HTTPS 443 |
| Authentication and other client endpoints | Depends on authentication and runtime | Your configured External OAuth token endpoint, and applicable auxiliary entries in the account’s hostname inventory | Ports specified by that configuration or inventory |

Expand

Show lessSee more

Direct REST row-append clients send rows to the ingest endpoint; this procedure doesn’t require them to upload files directly to cloud storage. SDK and Kafka deployments also need connectivity to the cloud-storage destinations used for their uploads.

## Configure and verify connectivity

### 1. Identify the account endpoint

Use your Snowflake account URL for the SDK `url` or Kafka `snowflake.url.name` property. The SDK discovers the ingest hostname automatically during initialization. Don’t replace the account URL with an ingest hostname, a VPC endpoint DNS target, or a raw IP address.

For private connectivity, first complete the platform setup for [AWS PrivateLink](/user-guide/admin-security-privatelink), [Azure Private Link](/user-guide/privatelink-azure), or [Google Cloud Private Service Connect](/user-guide/private-service-connect-google). Ask an account administrator with the `ACCOUNTADMIN` role to run:

Copy code

```
SELECT SYSTEM$GET_PRIVATELINK_CONFIG();
```

Use the `privatelink-account-url` value as the account hostname. See [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) for administrative requirements and returned values.

### 2. Discover the ingest hostname

Network administrators can discover the hostname before starting an SDK application or Kafka worker. Set `CONTROL_HOST` to the public or private account hostname for the intended connection mode, without `https://` or a trailing slash. The following example uses an existing key-pair JWT; see [REST authentication and setup](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-tutorial#prerequisites) to generate it. Keep the token out of logs and source control.

Copy code

```
CONTROL_HOST="<account-hostname>"
INGEST_HOST=$(curl --fail --silent --show-error \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "X-Snowflake-Authorization-Token-Type: KEYPAIR_JWT" \
  "https://${CONTROL_HOST}/v2/streaming/hostname")
INGEST_HOST=$(printf '%s' "$INGEST_HOST" | tr '_' '-')
printf 'Ingest hostname: %s\n' "$INGEST_HOST"
```

The successful response body is the hostname as plain text, not a JSON object. Replace underscores with dashes, as the SDK does, and use that normalized hostname for DNS configuration and subsequent streaming requests. Don’t construct the ingest hostname from an account locator or region. Direct REST clients must also complete the scoped-token exchange in their tutorial.

### 3. Configure private DNS and routing

For private connectivity, the discovered ingest hostname must resolve through the existing Snowflake private endpoint. It is separate from the account hostname and might not appear in `SYSTEM$GET_PRIVATELINK_CONFIG` or `SYSTEM$ALLOWLIST_PRIVATELINK`.

Create a private DNS record for the exact normalized `INGEST_HOST`:

- On AWS, create a private hosted-zone `CNAME` or appropriate alias targeting the existing Snowflake VPC endpoint regional DNS name.
- On Azure, resolve the ingest hostname to the existing Snowflake private endpoint IP address.
- On Google Cloud, resolve the ingest hostname to the existing Private Service Connect endpoint.

Link or forward the private DNS configuration to the application or worker network, and ensure that network can route to the endpoint. Follow the platform setup guides linked in Step 1. You don’t need a second Snowflake service private endpoint for the ingest hostname.

This service-endpoint configuration doesn’t establish private connectivity to SDK cloud-storage upload destinations. Validate storage routing separately for your cloud and deployment. If private-only storage egress is required, confirm the supported configuration with Snowflake Support before deployment rather than assuming storage traffic uses the Snowflake service endpoint.

### 4. Configure firewall and proxy access

Obtain your account’s hostname and port inventory using the appropriate function:

Copy code

```
-- Public connectivity:
SELECT SYSTEM$ALLOWLIST();

-- Private connectivity:
SELECT SYSTEM$ALLOWLIST_PRIVATELINK();
```

See [Allowing hostnames](/user-guide/hostname-allowlist). Include the discovered ingest hostname explicitly if it is absent. Allow HTTPS on port 443 to both the account and ingest endpoints. Retain the required storage and auxiliary entries, with their specified ports, for your runtime and authentication method.

For SDK and Kafka uploads, verify the actual storage destinations returned by Snowflake rather than testing only a generic cloud hostname. Don’t assume the inventory covers every streaming upload destination. If uploads identify a destination missing from the inventory, confirm the required hostname and supported routing with Snowflake Support. Don’t substitute a blanket wildcard for an account-specific inventory.

For Kafka proxy configuration, follow [Configure proxy access](/user-guide/kafka-connector/setup-kafka#label-kafkahp-proxy-configuration). The native SDK and JVM use separate settings. Set worker process environment variables before starting the worker; restarting only a connector or task doesn’t reload the worker environment.

DNS, routing, and firewall egress are customer-side connectivity requirements. [Snowflake network policies](/user-guide/network-policies) control access to Snowflake; changing them doesn’t fix an unresolved hostname.

### 5. Test from the application or worker runtime

Run these checks for both `CONTROL_HOST` and `INGEST_HOST` from the actual producer or worker network:

Copy code

```
nslookup "$CONTROL_HOST"
nslookup "$INGEST_HOST"
nc -vz "$CONTROL_HOST" 443
nc -vz "$INGEST_HOST" 443
curl --silent --show-error --output /dev/null \
  --write-out 'HTTP status: %{http_code}\n' "https://${INGEST_HOST}/"
```

DNS must resolve each hostname to the intended public or private destination. A successful TCP check establishes port reachability, not TLS or authentication. The `curl` check preserves the hostname for TLS Server Name Indication (SNI), certificate verification, and HTTP routing. An HTTP error response can establish transport reachability, but it doesn’t prove valid credentials or successful ingestion. Don’t use raw-IP HTTPS or disable certificate verification.

If a proxy is required, direct TCP checks might be blocked by design; verify the configured proxy path as well. Shell checks alone don’t validate the native SDK or JVM proxy configuration.

Repeat authenticated hostname discovery, then run your SDK, REST, or [Kafka connector test](/user-guide/kafka-connector/test-connector) with a small batch and verify the rows in the target table. For SDK uploads, also verify storage access during that test. [SnowCD](/user-guide/snowcd) checks its supplied inventory; success doesn’t cover an ingest hostname or upload destination omitted from that inventory.

## Troubleshoot connectivity

| Symptom | Check |
| --- | --- |
| Account hostname doesn’t resolve | Account URL, private DNS zone linkage or forwarding, and resolution from the worker runtime. |
| Account connection or table creation succeeds, but `get_pipe_info` fails with a DNS lookup error | Resolution of the distinct ingest hostname. For private connectivity, configure its DNS record to use the existing Snowflake private endpoint. |
| Hostname resolves, but HTTPS times out | Routing, TCP 443 firewall rules, endpoint access, and the configured proxy path. |
| TLS hostname mismatch | Keep the discovered hostname in the URL; don’t replace it with the endpoint IP or override SNI or the HTTP `Host` header. |
| Discovery succeeds, but SDK uploads fail | The actual cloud-storage upload destination and its DNS, routing, firewall, and proxy configuration. |
| Checks pass on a laptop but fail in Kafka Connect | Repeat them inside the worker runtime. Restart the worker after process-environment changes, or if it caches a failed DNS lookup. |
| HTTP 401 or 403 | Check authentication and authorization separately from transport connectivity; follow your client’s authentication troubleshooting. |

Expand

Show lessSee more
