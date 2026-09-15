# Jul 1, 2026: Workload identity federation for Snowflake workloads that access external services (*General availability*)

Snowflake can now act as the OpenID Connect (OIDC) provider when Snowflake workloads authenticate to external services. To use this capability, create a secret of type `WORKLOAD_IDENTITY_FEDERATION` and share its issuer URL and subject identifier with the external service to establish trust. When the workload needs to authenticate, call `SYSTEM$ISSUE_WORKLOAD_IDENTITY_FEDERATION_TOKEN` to obtain a short-lived ID token to send to the service.

For more information, see [Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound).
