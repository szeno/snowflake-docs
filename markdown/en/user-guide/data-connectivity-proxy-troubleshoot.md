# Troubleshoot Data Connectivity Proxy

Use these symptoms and resolutions when a Data Connectivity Proxy (DCP) agent or connector path isn’t working as expected.

## Agent fails to start: token rejected

**Symptom:** The agent exits immediately with an authentication error.

**Cause:** The credentials file contains an opaque token (starting with `PAT_`) instead of a Snowflake Access JWT.

**Resolution:** Regenerate the token using `SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN` and write the output (not a PAT) to
the credentials file.

## TLS handshake fails: certificate doesn’t match the DCP hostname

**Symptom:** DNS for `dcp.<org>-<account>.<region>.<cloud>.snowflake.com` resolves and TCP to port 443 succeeds, but the TLS handshake
fails. The server presents a certificate whose common name doesn’t match the DCP hostname, often `*.privatelink.snowflakecomputing.com`.

**Cause:** The account doesn’t yet have TLS certificates for nested `snowflake.com` hostnames, or the agent is reaching a PrivateLink
endpoint instead of the public DCP control plane.

**Resolution:**

1. Confirm the agent uses the public DCP hostname from [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist), not a PrivateLink
   hostname or a PrivateLink DNS override. Connecting the DCP agent through a PrivateLink endpoint isn’t supported.
2. Issue account-level certificates, then wait at least 30 minutes before retrying the agent:

   Copy code

   ```
   SELECT SYSTEM$ISSUE_PER_ACCOUNT_CERTIFICATES();
   ```

   For more information, see [SYSTEM$ISSUE\_PER\_ACCOUNT\_CERTIFICATES](/sql-reference/functions/system_issue_per_account_certificates) and the
   [note in the setup topic](/user-guide/data-connectivity-proxy-setup#label-dcp-setup-issue-certificates).

## Agent shows disconnected or down health

**Symptom:** `DESCRIBE DATA CONNECTIVITY PROXY` returns `AGENT_HEALTH = DOWN`, or `AGENT_STATUS` isn’t `DCP_AGENT_LIFECYCLE_CONNECTED`.

**Steps:**

1. Check that the agent container is running: `docker ps | grep dcp-agent`
2. Check agent logs: `docker logs dcp-agent --tail 50`
3. Verify outbound port 443 is open from the agent host to `<account>.snowflakecomputing.com`
4. Run the agent health check (see [Health check](/user-guide/data-connectivity-proxy-monitor#label-dcp-health-check)) to isolate which
   step is failing
5. Check `DCP_CLIENT_EVENT_HISTORY` for `EVENT_TYPE = 'BOOTSTRAP'` or `'CONTROL_PLANE'` rows with `STATUS = 'FAILURE'`. Check DESCRIBE
   for `LAST_AUTH_FAILURE_REASON` if authentication is failing.

## Connector can’t reach a private source

**Symptom:** Connector connection attempts fail even though the agent is connected.

**Steps:**

1. Verify `DESCRIBE DATA CONNECTIVITY PROXY` lists the EAI in `EXTERNAL_ACCESS_INTEGRATIONS`. If it’s empty, associate the EAI with
   `ALTER DATA CONNECTIVITY PROXY ... SET EXTERNAL_ACCESS_INTEGRATIONS`.
2. Verify the destination FQDN and port are covered by a `HOST_PORT` network rule with
   `MODE = DATA_CONNECTIVITY_PROXY_EGRESS` in that EAI
3. Confirm the same EAI is attached to the Openflow runtime
4. Run `DCP_CLIENT_ROUTE_CHECK` for the destination as `host:port`
5. Verify the agent host can reach the destination: `docker exec dcp-agent nc -z <host> <port>`
6. Check firewall rules between the agent host and the data source

## Bootstrap token expired before rotation

**Symptom:** `DCP_CLIENT_EVENT_HISTORY` shows `EVENT_TYPE = 'CERT_ROTATION'` with `STATUS = 'FAILURE'`. The agent is still running but
can’t renew its certificates. DESCRIBE also shows `CERT_ROTATION_STATUS` as failed.

**Resolution:** The agent continues operating on its current certificates but can’t rotate them until a valid token is in place. Generate a
new token and write it to the credentials file (see
[Rotate the bootstrap token without downtime](/user-guide/data-connectivity-proxy-setup#label-dcp-rotate-bootstrap-token)). The agent
picks it up on the next rotation attempt; no restart is required.

## Multiple agents: some connections land on the wrong agent

**Cause:** DCP doesn’t load-balance individual connections across agents. Each workload-to-destination mapping is owned by exactly one
agent at a time. Connections route deterministically through the control plane routing table.

**Resolution:** This is expected behavior, not a misconfiguration. For throughput scaling, size individual agent hosts appropriately. If a
specific agent is saturated, review the EAI scoping so destinations are partitioned correctly across agents.
