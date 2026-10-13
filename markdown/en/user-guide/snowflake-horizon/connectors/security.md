# Security and data protection

Horizon Catalog connects to external data sources and BI tools to collect metadata, lineage,
and popularity data. Securing these connections is a shared responsibility between Snowflake
and the customer. Snowflake provides TLS-capable clients, encrypted credential storage, and
scoped IAM role validation. You are responsible for enabling TLS on your database instances,
managing network access, and following the principle of least privilege when granting
permissions.

## Encryption in transit

Horizon Catalog uses encrypted connections whenever the remote system supports them. The
level of enforcement depends on the connector type:

| Connector type | TLS behavior | Your responsibility |
| --- | --- | --- |
| **SaaS connectors** (Databricks, Power BI, Tableau) | HTTPS enforced (TLS 1.2+). Cannot be disabled. | None. Encryption is always active. |
| **SQL Server** | Encryption enabled by default (`Encrypt=yes`). Self-signed certificates accepted. | Use a CA-signed TLS certificate for full protection against man-in-the-middle attacks. Do not disable the `Encrypt` setting. |
| **PostgreSQL** (RDS, Aurora, on-prem) | TLS-capable client. Connects over TLS if available; falls back to unencrypted if the server does not support TLS. | Enable and enforce TLS on your PostgreSQL instance. For AWS RDS/Aurora, set `rds.force_ssl = 1`. For on-prem, set `ssl = on` in `postgresql.conf`. In all cases, set `ssl_min_protocol_version = 'TLSv1.2'`. |

Expand

Show lessSee more

Note

This approach is consistent with how Snowflake treats other customer-managed integrations
such as external stages, external functions, and Openflow BYOC deployments: Snowflake provides
TLS-capable infrastructure, and the customer is responsible for configuring their environment
to enforce encryption.

## Network security

### Your responsibility

Horizon Catalog connects to your data sources over the network. You control network access to
your instances:

- **Firewalls and security groups**: Open inbound access on the data source port. Because
  Horizon Catalog doesn’t guarantee stable egress IP addresses (see
  [Horizon Catalog egress](#horizon-catalog-egress)), protect the data source with
  authentication and TLS rather than relying on an IP allowlist.
- **Public accessibility**: The data source must be reachable from the internet, either
  directly (e.g. RDS with *Publicly accessible = Yes*) or through an internet-facing proxy or
  load balancer you control.

### Horizon Catalog egress

Horizon Catalog doesn’t provide static or dedicated egress IP addresses, and Snowflake doesn’t
guarantee that the egress IP addresses Horizon Catalog connects from stay the same. These
addresses can change at any time without notice, which breaks any connection that depends on an
IP allowlist.

If your security policy requires an IP allowlist rather than `0.0.0.0/0` on the data source
port, contact Snowflake support for the egress IP addresses currently in use for your Snowflake
account. Treat that list as a point-in-time snapshot rather than a guarantee, and expect to
update your allowlist when the addresses change.

## IAM role security (AWS connectors)

AWS database connectors (PostgreSQL on RDS/Aurora, SQL Server with DAS logs) use a
cross-account IAM role for CloudWatch log access and instance discovery. Horizon Catalog
enforces the following security controls:

- **Role naming convention**: The IAM role name must start with `SnowflakeHorizon-` (console)
  or use the path `/SnowflakeHorizon/` (CLI/Terraform). Roles with other naming patterns
  are rejected.
- **External ID enforcement**: Every connector generates a unique External ID prefixed with
  `sf_horizon_`. The IAM trust policy must include this External ID in a `sts:ExternalId`
  condition. This prevents [confused deputy](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html) attacks.
- **Least-privilege policies**: The access policies shown in each connector’s setup guide grant
  only the minimum permissions needed: `rds:Describe*` for instance discovery and
  `logs:FilterLogEvents` / `logs:GetQueryResults` for CloudWatch reads. Do not grant broader
  permissions than what the setup guide specifies.

## Credentials management

### How credentials are stored

When you configure a connector, Horizon Catalog stores the credentials you provide
(database user/password, API tokens, OAuth client secrets) in a Snowflake-managed encrypted
storage layer.

### Rotation recommendations

- **Database passwords**: Rotate periodically according to your organization’s policy.
  Update the password in the Horizon Catalog connector settings after rotating.
- **API tokens and OAuth secrets**: Follow the rotation guidance from the SaaS provider
  (Databricks, Power BI, Tableau). Update the connector settings after rotating.
- **IAM roles**: IAM role credentials are temporary (STS) and rotate automatically.
  No manual rotation is needed for the cross-account role itself, but review and rotate
  the trust policy’s External ID if you suspect it has been compromised.
