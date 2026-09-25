# Set up Data Connectivity Proxy

Complete these steps to create a Data Connectivity Proxy (DCP) object, deploy an agent on your network, and route Openflow connector
traffic to a private data source.

The agent host needs at least 1 vCPU and 512 MB of memory. For the full prerequisite list, see
[Prerequisites](/user-guide/data-connectivity-proxy#label-dcp-prerequisites).

## Step 1: Create a DCP object in Snowflake

Create a Data Connectivity Proxy object using the ACCOUNTADMIN role (or a role with the `CREATE DATA CONNECTIVITY PROXY` privilege).

You can associate an external access integration when you create the DCP object. Create the network rule and EAI first
([Step 6](#label-dcp-setup-network-rule) and [Step 7](#label-dcp-setup-eai)), then:

Copy code

```
CREATE DATA CONNECTIVITY PROXY my_dcp_client
  EXTERNAL_ACCESS_INTEGRATIONS = (my_private_source_eai)
  ENABLED = TRUE;
```

You can also create the DCP object now and associate the EAI in [Step 7](#label-dcp-setup-eai):

Copy code

```
CREATE DATA CONNECTIVITY PROXY my_dcp_client;
```

Attaching a network policy is optional. Use this only if you want a DCP-specific network policy that restricts which source IPs can connect
to the DCP control plane:

Copy code

```
CREATE DATA CONNECTIVITY PROXY my_dcp_client
  NETWORK_POLICY = my_network_policy;
```

You can also attach or change the policy later with `ALTER DATA CONNECTIVITY PROXY ... SET NETWORK_POLICY`. For more information, see
[Controlling network traffic with network policies](/user-guide/network-policies).

Note

After you create the DCP object, issue account-level TLS certificates:

Copy code

```
SELECT SYSTEM$ISSUE_PER_ACCOUNT_CERTIFICATES();
```

A successful call returns `Certificates will be issued.` Issuance is asynchronous. Wait at least 30 minutes after the first call in the
account before you start the agent. Calling the function again has no additional effect.

For more information, see [SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES](/sql-reference/functions/system_issue_per_account_certificates).

## Step 2: Generate a bootstrap token

Generate a one-time bootstrap JWT that the agent uses to authenticate with Snowflake and receive its mTLS certificates. The second argument
is the token validity in days:

Copy code

```
SELECT SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN('my_dcp_client', 7);
```

Save the output token. You will write it to a credentials file on the agent host.

Important

The token format must be a Snowflake Access JWT. Tokens that begin with `PAT_` aren’t accepted and cause the agent to fail to start.

## Step 3: Write the credentials file

On the agent host, write the token to a file. The agent reads this file at startup and during certificate rotation:

Copy code

```
echo '<token from Step 2>' > /etc/dcp-agent/secrets/dcp-bootstrap-token
chmod 600 /etc/dcp-agent/secrets/dcp-bootstrap-token
```

The agent re-reads this file on every certificate rotation cycle. You can update the token without restarting the agent; see
[Rotate the bootstrap token without downtime](#label-dcp-rotate-bootstrap-token).

### Store the token in a secrets manager

Don’t leave the bootstrap JWT in a world-readable file or in your orchestration manifests. Store it in a secrets manager such as AWS
Secrets Manager, Microsoft Azure Key Vault, Google Cloud Secret Manager, or HashiCorp Vault, then write it to the credentials path the
agent mounts.

The agent only reads a local file (`--sf-bootstrap-credentials`, default `/etc/dcp-agent/secrets/dcp-bootstrap-token`). It doesn’t call a
secrets manager API itself. Fetch the secret at deploy time or from a sidecar, then place it at that path. Restrict file permissions
(`chmod 600`) and limit the IAM or RBAC identity that can read the secret.

The following examples write the secret to `/etc/dcp-agent/secrets/dcp-bootstrap-token`. Adapt the secret name and then start the agent as
in Step 4.

AWS Secrets Manager:

Copy code

```
aws secretsmanager get-secret-value \
  --secret-id dcp/my_dcp_client/bootstrap-token \
  --query SecretString \
  --output text > /etc/dcp-agent/secrets/dcp-bootstrap-token
chmod 600 /etc/dcp-agent/secrets/dcp-bootstrap-token
```

Microsoft Azure Key Vault:

Copy code

```
az keyvault secret show \
  --vault-name <your-key-vault> \
  --name dcp-my-dcp-client-bootstrap-token \
  --query value \
  --output tsv > /etc/dcp-agent/secrets/dcp-bootstrap-token
chmod 600 /etc/dcp-agent/secrets/dcp-bootstrap-token
```

Google Cloud Secret Manager:

Copy code

```
gcloud secrets versions access latest \
  --secret=dcp-my-dcp-client-bootstrap-token > /etc/dcp-agent/secrets/dcp-bootstrap-token
chmod 600 /etc/dcp-agent/secrets/dcp-bootstrap-token
```

When you rotate the bootstrap token, update the secret in the manager, rewrite the credentials file (see
[Rotate the bootstrap token without downtime](#label-dcp-rotate-bootstrap-token)), and leave the agent running. You can also mount the
secret with a CSI driver or an init container as long as the file appears at `--sf-bootstrap-credentials` (or the default mount path)
before the agent starts.

## Step 4: Deploy the agent

Pull and start the agent container, mounting the credentials file:

Copy code

```
docker run -d \
  --name dcp-agent \
  --restart unless-stopped \
  -v /etc/dcp-agent/secrets/dcp-bootstrap-token:/etc/dcp-agent/secrets/dcp-bootstrap-token:ro \
  -e DCP_METRICS_PORT=9092 \
  -p 9092:9092 \
  snowflakedb/dcp-client:latest
```

The control plane URL and account identity come from the bootstrap JWT.

Mounting the token at `/etc/dcp-agent/secrets/dcp-bootstrap-token` is the default path, so you don’t need to pass
`--sf-bootstrap-credentials`. Pass it only if you mount the token somewhere else.

Setting `DCP_METRICS_PORT` and publishing the port is recommended: by default the metrics and `/ready` endpoints bind to
loopback inside the container, unreachable from a monitoring stack on the host. See
[Prometheus metrics (agent-side)](/user-guide/data-connectivity-proxy-monitor#label-dcp-prometheus).

If the agent host pulls the image from Docker Hub, allow outbound HTTPS to `*.docker.io`. You can skip this if you copy the image into a
private registry and pull from there.

The agent starts, authenticates with the control plane using the bootstrap JWT, receives its mTLS certificate pair, and connects to the
relay. After this point the JWT isn’t used again until the next certificate rotation.

## Step 5: Verify the agent is connected

In Snowflake, describe the DCP client to confirm it shows a connected status:

Copy code

```
DESCRIBE DATA CONNECTIVITY PROXY my_dcp_client;
```

Confirm `AGENT_HEALTH` is `HEALTHY` and `AGENT_STATUS` is `DCP_AGENT_LIFECYCLE_CONNECTED`. For column details, see
[Monitor Data Connectivity Proxy](/user-guide/data-connectivity-proxy-monitor).

## Step 6: Create a network rule for the private destination

Create a network rule that names the host and port the agent should reach. Use a DNS hostname, not a raw IP address. Use
`MODE = DATA_CONNECTIVITY_PROXY_EGRESS` and `TYPE = HOST_PORT`. Ordinary `MODE = EGRESS` rules aren’t applied to DCP.

Copy code

```
CREATE NETWORK RULE my_private_network_rule
  MODE = DATA_CONNECTIVITY_PROXY_EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('my-private-db.internal:5432');
```

If the destination has no DNS name, add a hosts entry on the agent host (`/etc/hosts`, or `--add-host` for Docker) so the hostname in
`VALUE_LIST` resolves there.

For more information, see [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule).

## Step 7: Create an external access integration and associate it with the DCP object

Create an external access integration (EAI) that references the DCP network rule:

Copy code

```
CREATE EXTERNAL ACCESS INTEGRATION my_private_source_eai
  ALLOWED_NETWORK_RULES = (my_private_network_rule)
  ENABLED = TRUE;
```

Traffic to destinations in that rule is eligible for DCP because the rule uses `MODE = DATA_CONNECTIVITY_PROXY_EGRESS`.

Associate the EAI with the DCP object. Skip this `ALTER` if you already set `EXTERNAL_ACCESS_INTEGRATIONS` when you
created the object:

Copy code

```
ALTER DATA CONNECTIVITY PROXY my_dcp_client
  SET EXTERNAL_ACCESS_INTEGRATIONS = (my_private_source_eai);
```

For more information, see [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

## Step 8: Configure the connector

Attach the same EAI to your Openflow runtime in the Openflow UI so the connector is allowed to open connections to the
destination, then configure the connector to use the source FQDN and port as usual. You don’t need an explicit tunnel
reference on the connector. For the UI steps, see
[Attach the external access integration to the runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-dcp#label-openflow-spcs-dcp-attach-eai).

## Networking requirements

### Outbound ports

The agent requires only outbound access on port 443. You don’t need to open inbound ports.

Allow every hostname in the following table. The agent connects over either relay hostname automatically, based on what your
network allows. Both are fully supported — you don’t need to prefer one. If you allowlist only the fallback hostname, the agent
still works, and all relay traffic uses that hostname.

Important

The agent requires end-to-end TLS connectivity to these hostnames. Configure firewalls, proxies, and other network security
devices to pass this traffic without TLS inspection or decryption, certificate substitution, or TLS termination. An outbound
allow rule isn’t sufficient if a security device still intercepts or modifies the TLS connection.

If your network applies TLS inspection by default, create a narrowly scoped no-decrypt exception for traffic from the agent host
to these hostnames on port 443.

In these patterns, `<cloud>` is the cloud provider that hosts your Snowflake account: `aws`, `azure`, or `gcp`. The segment reflects the
hostname format only. It doesn’t mean the agent’s traffic transits that provider’s network.

| Destination | Port | Protocol | Purpose |
| --- | --- | --- | --- |
| `dcp.<org>-<account>.<region>.<cloud>.snowflake.com` | 443 | TLS | DCP control plane |
| `dcp-proxy.<org>-<account>.<region>.<cloud>.snowflake.com` | 443 | TLS | Relay (data path) |
| `dcp-proxy-fallback.<org>-<account>.<region>.<cloud>.snowflake.com` | 443 | TLS | Relay (data path), used when the agent doesn’t connect over the `dcp-proxy` hostname |

Expand

Show lessSee more

Required hostnames vary by cloud and region. To get the definitive list for your account, query
[SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist):

Copy code

```
SELECT f.VALUE:host::STRING AS host,
       f.VALUE:port::INT    AS port,
       f.VALUE:type::STRING AS type
FROM TABLE(FLATTEN(input => PARSE_JSON(SYSTEM$ALLOWLIST()))) f
WHERE f.VALUE:type::STRING LIKE 'DCP%';
```

For more information about forward proxy and TLS inspection restrictions, see
[Corporate proxy support](/user-guide/data-connectivity-proxy-security#label-dcp-corporate-proxy).

### DNS

The agent resolves Snowflake endpoint hostnames using standard public DNS. Don’t override those names to PrivateLink hostnames or
PrivateLink IP addresses. Connecting the DCP agent through a PrivateLink endpoint isn’t supported.

### Telemetry endpoints

Snowflake delivers the telemetry hostname to the agent at bootstrap. Allow outbound TLS on port 443 to:

`<org>-<account>.telemetry.<locator>.snowflakecomputing.com`

Connection history and some route-check stages stay empty until this endpoint is reachable.

## High availability

Run at least two agent instances in separate failure domains (for example, on different VMs or in different availability zones) to provide
failover coverage.

Each instance is live and handles its own set of connections simultaneously. The control plane maintains a routing table that maps each
workload-to-destination pair to a specific agent. If an agent becomes unavailable, the control plane updates the routing table to redirect
affected connections to a healthy instance.

Important

When an agent fails, the tunnels it was handling break and the workload’s TCP connections are torn down. The application must reconnect.
DCP doesn’t shield the application from the connection reset. Make sure your connector is configured with reconnect logic.

Active-active load-balancing across agents for the same destination is planned for a future release.

### Scaling for throughput

The agent is I/O-bound rather than CPU-bound. Data frames are encrypted with AES-256-GCM; on hardware with AES-NI, encryption isn’t a
throughput bottleneck. The relay uses zero-copy kernel I/O to minimize CPU cost per byte. The practical limit is available network bandwidth
on the agent host.

For more throughput, run additional agent instances (more containers or VMs) and split destinations across them with separate EAIs. DCP
doesn’t load-balance individual connections for the same destination across agents.

## Upgrade agents

### Snowflake-managed relay upgrades

When Snowflake upgrades the relay, you don’t need to take action. Active database connections stay up.

### Agent-process upgrades

Upgrading the agent binary (replacing the container image) does tear down active TCP connections to the data source. The agent supports
graceful drain: on receiving `SIGTERM`, it stops accepting new connections and waits for active tunnels to finish before exiting.

To upgrade with minimal disruption using graceful drain:

Copy code

```
# Start a new agent instance first (when running multiple agents for HA)
docker run -d --name dcp-agent-new ... snowflakedb/dcp-client:<new-version> ...

# Wait for routing table to shift traffic to the new instance, then drain the old one
docker stop --time 300 dcp-agent   # allows up to 300s for active connections to finish
```

## Rotate the bootstrap token without downtime

The agent re-reads the credentials file on every certificate rotation cycle. To replace the token without interrupting active connections,
write the new token to the file (from a secrets manager if that’s where you store it):

Copy code

```
# Write the new token to a temporary file
echo '<new-token>' > /etc/dcp-agent/secrets/dcp-bootstrap-token.new
chmod 600 /etc/dcp-agent/secrets/dcp-bootstrap-token.new

# Atomically replace the credentials file
mv /etc/dcp-agent/secrets/dcp-bootstrap-token.new /etc/dcp-agent/secrets/dcp-bootstrap-token
```

The agent picks up the new token on its next rotation cycle. No restart is required, and no connections are interrupted.

Note

Set an alert on the `dcp_agent_bootstrap_jwt_expires_at_seconds` Prometheus metric so you have advance warning before the token expires. If
the token expires before you replace it, the agent continues running on its current certificates but can’t obtain refreshed credentials at
the next rotation. Active connections aren’t immediately dropped, but rotation fails until a valid token is in place.
