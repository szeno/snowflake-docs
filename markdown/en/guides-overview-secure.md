# Securing Snowflake

Snowflake provides industry-leading features that help ensure you can configure the highest levels of security for your account and users,
as well as all the data you store in Snowflake.

These topics are intended primarily for administrators (that is, users with the ACCOUNTADMIN, SYSADMIN, or SECURITYADMIN roles).

## Authentication

[Authentication policies](/user-guide/authentication-policies)
:   Using authentication policies to restrict account and user authentication by client, authentication methods, and more.

[Multi-factor authentication (MFA)](/user-guide/security-mfa)
:   Using multi-factor authentication with Snowflake.

[Federated Authentication and SSO](/user-guide/admin-security-fed-auth-overview)
:   Topics related to federated authentication to Snowflake.

[Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth)
:   Using key-pair authentication to Snowflake.

[Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens)
:   Generating and managing programmatic access tokens for authentication.

[OAuth](/user-guide/oauth-intro)
:   Topics related to using Snowflake OAuth and External OAuth to connect to Snowflake.

[Workload identity federation](/user-guide/workload-identity-federation)
:   Preferred authentication method for service-to-service workloads accessing Snowflake data.

[Workload identity federation for Snowflake workloads that access external services](/user-guide/workload-identity-federation-outbound)
:   Using workload identity federation so that Snowflake workloads can authenticate to external services, with Snowflake acting as the OIDC provider.

[External API authentication and secrets](/user-guide/api-authentication)
:   Configuring Snowflake to authenticate to external services.

## Network security

[Malicious IP Protection](/user-guide/malicious-ip-protection)
:   Protecting your account from IP addresses that are known to be malicious.

[Controlling network traffic with network policies](/user-guide/network-policies)
:   Using network policies to restrict access to Snowflake.

[Network rules](/user-guide/network-rules)
:   Using network rules with other Snowflake features to restrict access to and from Snowflake.

## Private connectivity

[Private connectivity for inbound network traffic](/user-guide/private-connectivity-inbound)
:   Using private connectivity to access the Snowflake service, Snowsight, Streamlit in Snowflake, internal stages, Snowflake managed
    storage volumes, and Snowpark Container Services.

[Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound)
:   Using private connectivity for external network locations, external functions, external stages, external tables, external
    volumes, and Snowpipe automation.

## Administration and authorization

[Trust Center](/user-guide/trust-center/overview)
:   Using the Trust Center to evaluate and monitor your account for security risks.

[Snowflake sessions and session policies](/user-guide/session-policies)
:   Using session policies to manage your Snowflake session.

[SCIM](/user-guide/scim-intro)
:   Topics related to using SCIM to provision users and groups to Snowflake.

[Access Control](/user-guide/security-access-control-overview)
:   Topics related to role-based access control (RBAC) in Snowflake.

## Defense in depth

[End-to-End Encryption](/user-guide/security-encryption-end-to-end)
:   Using end-to-end encryption in Snowflake.

[Data movement policies](/user-guide/data-movement-policies)
:   Using data movement policies to proactively prevent data exfiltration across various movement channels in Snowflake.

[Multi-party Approval](/user-guide/multi-party-approval)
:   Using Multi-party Approval for a second-person review of security-sensitive and operationally risky critical operations.
