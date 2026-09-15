# Data Connectivity Proxy

Data Connectivity Proxy (DCP) lets Snowflake securely reach data sources on your private network (on-premises, in a VPC, or in a hybrid
environment) without requiring you to open inbound firewall ports or expose your network to the public internet.

DCP works by running a lightweight agent process on your network. The agent makes a single outbound connection on port 443 to Snowflake and
establishes an encrypted tunnel. Snowflake routes requests through that tunnel to reach the private data source. Your firewall sees only
outbound traffic: there is no inbound listener, no public IP, and no VPN required.

DCP is available on AWS, Azure, and Google Cloud across Standard, Enterprise, and Business Critical editions.

## When to use DCP

Use DCP when Snowflake needs to reach a data source that isn’t accessible from the public internet:

- Databases inside a VPC or VNet (PostgreSQL, MySQL, Oracle, SQL Server, MongoDB, and similar sources)
- On-premises databases behind a corporate firewall
- Any source that’s accessible within your network but not reachable over the internet
- Environments where opening inbound firewall rules is prohibited by policy (zero-trust, deny-all-inbound architectures)

DCP is currently available for use with Snowflake Openflow. Support for additional Snowflake services is planned for a future release.

## How DCP compares to other private connectivity options

Snowflake provides several options for private network access. The right choice depends on your edition, direction of traffic, and network
topology:

| Capability | DCP | PrivateLink / PSC / PE | Stable egress with IP allowlisting |
| --- | --- | --- | --- |
| Direction | Your network to Snowflake | Snowflake to your network | Snowflake to your network |
| Editions | Standard, Enterprise, Business Critical | Business Critical and higher only | Standard, Enterprise, Business Critical |
| Inbound ports required | None | None | Required on your side |
| Works across clouds and on-premises | Yes | CSP-native only | Yes |
| Zero-trust compatible | Yes | Yes | Only if your policy permits IP-based rules |
| Setup complexity | Low (deploy agent, run bootstrap) | High (VPC/VNet configuration, DNS, peering) | Low (add IPs to firewall allowlist) |

Expand

Show lessSee more

Use DCP when you need Snowflake to pull data from a source on a private network and opening inbound ports isn’t possible or desirable.
Use outbound PrivateLink / PSC / PE when you need Snowflake to reach a private data source and require fully private network connectivity without traversing the public internet (CSP-native configuration required). Use stable egress IPs when
your firewall policy allows IP-based inbound rules.

DCP and PrivateLink aren’t mutually exclusive. If your Snowflake account uses PrivateLink for inbound access, you can still use DCP for
outbound connectivity to private data sources. The DCP agent itself must connect to the public DCP hostnames on port 443. Connecting the
agent through a PrivateLink endpoint isn’t supported.

## Architecture

DCP has three main components:

DCP agent
:   A lightweight process you deploy on your network, close to your data source. It makes a single outbound TLS connection to Snowflake’s
    relay infrastructure and holds it open. It has no knowledge of the connector type or data content; it operates at the TCP level only.

Snowflake relay
:   Snowflake-operated infrastructure that maintains the other end of the tunnel. When a connector needs to open a database connection, the
    relay routes the TCP stream through the tunnel to the appropriate agent. The relay handles reconnection transparently when a proxy is
    upgraded or restarted.

DCP control plane
:   Snowflake-operated service that manages agent identity, certificate issuance and rotation, routing table distribution, and health
    monitoring. The agent communicates with the DCP control plane over outbound port 443.

### Data path

```
Connector (on Snowflake)
    ↓  TCP connection request
Snowflake relay (routes by destination FQDN:port)
    ↓  Encrypted tunnel (mTLS)
DCP agent (on your network)
    ↓  Direct TCP connection
Data source (database, private endpoint)
```

The agent is a TCP-level pass-through. It doesn’t inspect, parse, buffer, or store data. Source credentials and connector logic remain
entirely within Snowflake.

### Routing

Routing is destination-driven. Connectors specify a source host and port; the relay looks up which DCP client’s associated external
access integration (EAI) covers that host:port and routes the connection there. Associate the EAI with the DCP object by using
`EXTERNAL_ACCESS_INTEGRATIONS` on `CREATE DATA CONNECTIVITY PROXY` or `ALTER DATA CONNECTIVITY PROXY`. There is no per-connector tunnel
reference; the destination determines the path.

Each TCP connection produces an independent end-to-end encrypted tunnel. There is no stream multiplexing across connections.

## Prerequisites

Before you set up DCP:

- You have the ACCOUNTADMIN role, or a role with the `CREATE DATA CONNECTIVITY PROXY` privilege.
- You have a host on your network (VM, bare-metal, or container host) with:
  - Linux OS, kernel 5.x or later
  - Docker or any OCI-compatible container runtime
  - At least 1 vCPU and 512 MB of memory
  - Outbound internet access on port 443
  - Network access to the data source you want to connect to
- Kubernetes isn’t required.

For the setup procedure, see [Set up Data Connectivity Proxy](/user-guide/data-connectivity-proxy-setup).
