# Data Connectivity Proxy security

This page describes how Data Connectivity Proxy (DCP) authenticates agents, manages certificates, and encrypts data-path traffic, and how you
revoke access.

## Authentication and certificate management

DCP uses a two-phase authentication model:

Phase 1: Bootstrap
:   The agent reads the bootstrap JWT (minted with `SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN`) from the credentials file. It
    presents this JWT to the control plane and receives an mTLS certificate pair scoped to its DCP client identity.

Phase 2: Ongoing operation
:   The agent’s control sessions with the relay use mutual TLS (mTLS): the agent presents its client certificate and verifies the relay’s
    certificate. Data tunnels authenticate with a key established during the control session instead of exchanging certificates. Each
    data tunnel also performs its own key exchange.

    Control plane traffic (heartbeats, routing table and policy updates, and certificate rotation) goes to the `dcp.` hostname over TLS that
    authenticates the server only. The agent doesn’t present a client certificate on this connection. After bootstrap, the agent authenticates
    each control plane request with a short-lived JWT. The agent signs that JWT with the private key that matches the leaf certificate the
    control plane issued at bootstrap. The agent sends the bootstrap JWT again when it rotates that certificate, and if it bootstraps again
    after a control plane reconnect.

    By default, the outer TLS connection to the `dcp-proxy-fallback` relay hostname doesn’t use a client certificate. The relay control
    session still uses mTLS inside that connection, and data tunnels remain encrypted end to end (see
    [Data path security](#label-dcp-data-path-security)).

## Certificate hierarchy

The agent validates relay mTLS certificates against a Snowflake-managed CA bundle delivered during bootstrap, not the operating system
trust store. Connections to the control plane, the `dcp-proxy-fallback` hostname, and the telemetry endpoint use publicly trusted
certificates and are verified against the container’s trust store. The Snowflake-managed bundle implements a four-tier PKI hierarchy:

```
Deployment root CA
  └── Control-plane intermediate CA
        └── Per-account intermediate CA
              └── Leaf certificate (per agent)
```

The deployment root public key is pinned on first bootstrap. Any subsequent update that presents a different root is rejected. You don’t
need to install or trust any Snowflake certificates in the OS or JVM trust store.

Snowflake periodically directs the agent to rotate its leaf certificate. The agent re-reads the credentials file, re-authenticates with the
control plane, and receives a fresh certificate. Rotation is transparent to active connections.

## Revoking access

To immediately revoke an agent’s ability to connect:

Copy code

```
ALTER DATA CONNECTIVITY PROXY my_dcp_client SET ENABLED = FALSE;
```

Or drop the object entirely:

Copy code

```
DROP DATA CONNECTIVITY PROXY my_dcp_client;
```

After the DCP object is disabled or dropped, the control plane rejects the agent, and the relay no longer accepts the agent’s client
certificate for its control session, regardless of the certificate’s cryptographic validity.

If the bootstrap JWT is compromised before bootstrap completes, regenerate the token:

Copy code

```
SELECT SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN('my_dcp_client', 7);
```

Write the new token to the credentials file as described in
[Rotate the bootstrap token without downtime](/user-guide/data-connectivity-proxy-setup#label-dcp-rotate-bootstrap-token).

## Network policy enforcement

A network policy on the DCP object is optional. Use one only if you want a DCP-specific policy that restricts which source IPs can connect
to the DCP control plane:

Copy code

```
ALTER DATA CONNECTIVITY PROXY my_dcp_client
  SET NETWORK_POLICY = my_network_policy;
```

For more information about creating network policies, see [Controlling network traffic with network policies](/user-guide/network-policies).

## Data path security

All traffic between the agent and the Snowflake relay is encrypted using AES-256-GCM. Each data tunnel uses a separate P-256 ECDH
key exchange, authenticated with a key from its relay control session.

The agent is a TCP-level pass-through. It doesn’t inspect, parse, buffer, or store the data passing through its tunnels. Source credentials
remain in Snowflake and are never transmitted to the agent.

## Corporate proxy support

The agent can send its outbound traffic through an HTTP proxy server that supports the `CONNECT` method. For setup steps, see
[Route the agent through a corporate proxy](/user-guide/data-connectivity-proxy-setup#label-dcp-setup-corporate-proxy).

By default, the proxy only relays TCP. The agent establishes TLS end to end with Snowflake through the proxy, so the proxy can’t
read DCP traffic.

### TLS inspection

If your security policy requires it, the proxy can decrypt and inspect some DCP traffic. Whether a connection can be inspected
depends on the path the agent uses:

| Destination | Can be inspected | What an inspecting proxy can see |
| --- | --- | --- |
| `dcp.<org>-<account>.<region>.<cloud>.snowflake.com` (control plane) | Yes | Control plane messages. This includes the bootstrap token whenever the agent bootstraps, including certificate rotation, a short-lived token on later requests, and routing and policy updates. |
| `dcp-proxy-fallback.<org>-<account>.<region>.<cloud>.snowflake.com` (relay) | Yes | The `Host` and `x-snowflake-session` relay-routing headers of each `CONNECT` request. The private destination and tunnel contents stay encrypted (see [Data path security](#label-dcp-data-path-security)). |
| Relay public IP addresses (direct path) | No | The corporate proxy sees the relay public IP address in the `CONNECT` request, but can’t decrypt the relay control session or data tunnels. The control session uses mTLS, which a TLS-inspecting proxy can’t forward. Use `fallback-only` on networks that inspect this path. |
| `<org>-<account>.telemetry.<locator>.snowflakecomputing.com` (telemetry) | Yes | Agent metrics, logs, and traces, and the bearer token that authenticates them. |

Expand

Show lessSee more

The agent accepts the proxy’s certificate only if the proxy’s CA is in the container’s trust store. The agent never skips
certificate verification.

Because an inspecting proxy can read the bootstrap token, the short-lived control plane token, and the telemetry bearer token when
telemetry uses the proxy, restrict access to the proxy’s decrypted traffic and logs as you would any credential. If your policy allows
it, exempt the control plane hostname from inspection.
