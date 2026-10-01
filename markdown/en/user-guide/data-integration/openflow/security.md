# Openflow security

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

This section describes how Openflow authenticates to Snowflake and to external
systems, and how you manage secrets used by connectors and runtimes.

For a high-level summary of authentication, authorization, encryption, secrets,
private connectivity, and Tri-Secret Secure support, see
[Security](/user-guide/data-integration/openflow/about#label-openflow-security) in About Openflow.
For Snowflake Managed Token details (the default runtime-to-Snowflake
authentication method), see
[Snowflake Managed Token authentication](/user-guide/data-integration/openflow/about#label-openflow-snowflake-managed-token).

## Topics

- [Use Workload Identity Federation with Openflow](/user-guide/data-integration/openflow/security/workload-identity-federation):
  Authenticate from Openflow runtimes to AWS, Azure, and Google Cloud without
  long-lived cloud credentials.
- [Use external secret providers with Openflow](/user-guide/data-integration/openflow/security/external-secret-providers):
  Expose secrets from AWS Secrets Manager, Azure Key Vault, or Google Cloud
  Secret Manager as Openflow parameters.
- [Data Connectivity Proxy](/user-guide/data-connectivity-proxy):
  Route connector traffic through a Data Connectivity Proxy for private or
  controlled network paths.
