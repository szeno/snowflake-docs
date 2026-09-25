# Data Connectivity Proxy security

This page describes how Data Connectivity Proxy (DCP) authenticates agents, manages certificates, and encrypts data-path traffic, and how you
revoke access.

## Authentication and certificate management

DCP uses a two-phase authentication model:

Phase 1: Bootstrap
:   The agent reads the bootstrap JWT (minted with `SYSTEM$GENERATE_DATA_CONNECTIVITY_PROXY_BOOTSTRAP_TOKEN`) from the credentials file. It
    presents this JWT to the control plane and receives an mTLS certificate pair scoped to its DCP client identity.

Phase 2: Ongoing operation
:   All subsequent communication (data tunnels, control plane heartbeats, routing table updates) uses mutual TLS (mTLS). Both the agent and
    the relay authenticate each other’s certificates on every connection. The bootstrap JWT isn’t used again until the next certificate
    rotation cycle.

## Certificate hierarchy

The agent validates all peer certificates against a Snowflake-managed CA bundle delivered during bootstrap, not the operating system trust
store. The bundle implements a four-tier PKI hierarchy:

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

The control plane validates mTLS certificates against registered key pairs on every connection attempt. After the DCP object is disabled or
dropped, the agent’s certificate is unusable regardless of its cryptographic validity.

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

All traffic between the agent and the Snowflake relay is encrypted using AES-256-GCM. Each TCP connection uses an independent P-256 ECDH
key exchange. There is no shared key material across connections; a compromise of one connection’s key material doesn’t affect others.

The agent is a TCP-level pass-through. It doesn’t inspect, parse, buffer, or store the data passing through its tunnels. Source credentials
remain in Snowflake and are never transmitted to the agent.

## Corporate proxy support

Routing the agent’s own outbound traffic through an enterprise-managed forward proxy (HTTPS\_PROXY / CONNECT-based forwarding) isn’t
supported. The agent host must have direct outbound access to the required Snowflake hostnames on port 443.

Every connection path requires end-to-end TLS without interception.

The TLS connection between the agent and Snowflake must remain end-to-end and unmodified. Don’t use TLS inspection or decryption,
certificate substitution, or TLS termination for DCP traffic. These controls can prevent the agent from authenticating with its
client certificate and from establishing stable relay connections, even when a firewall allows outbound traffic on port 443.

Configure firewalls, proxies, and other network security devices to bypass TLS inspection for traffic from the agent host to every
DCP hostname listed under [DCP networking requirements](/user-guide/data-connectivity-proxy-setup#label-dcp-networking).
