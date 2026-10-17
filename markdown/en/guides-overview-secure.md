# Securing Snowflake

These topics are intended primarily for administrators, for example users with the `ACCOUNTADMIN` or `SECURITYADMIN` role.

## Why this matters

Snowflake secures your data in layers. Each layer answers a different question about who can reach data and what they can do with it:

- **Authentication** confirms who is signing in, whether that is a person or a service, and which sign-in methods and strength you require.
- **Network security** controls where clients can connect from, and whether that traffic uses the public internet or a private path.
- **Access and data protection** decide what an identity can see or change, and how sensitive data is kept from moving outside the boundaries you set.

Snowflake provides baseline protections by default, such as encryption and protections against known threats. You configure authentication, network, and access controls to match your governance standards.

### Built for AI

AI agents follow the same sign-in, network, and access rules as human users. Snowflake also provides controls so you can:

- Recognize when an agent is acting in a session, separately from the person who started it.
- Constrain the privileges that agent can use.
- Audit agent activity on its own.

## How it works

### What Snowflake provides by default

- **Encryption:** [Encryption of data at rest and in transit](/user-guide/security-encryption-end-to-end).
- **Threat protection:** [Malicious IP protection](/user-guide/malicious-ip-protection) and [leaked password protection](/user-guide/leaked-password-protection).
- **Security Essentials:** [Security Essentials](/user-guide/trust-center/overview#label-security-essentials-scanner-package) scanning in Trust Center, which checks for missing MFA and missing network policies.
- **AI guardrails:** Snowflake includes default guardrails that protect against known prompt injection techniques. These protections are separate from [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails), the prompt injection prevention control that you configure.

### What you configure

- **Authentication:** SSO, MFA, keys, OAuth, workload identity, and agent identity. See [Overview of Snowflake authentication](/user-guide/security-authentication-overview) and [Agent identity](/user-guide/agent-identity).
- **Network security:** [Network policies](/user-guide/network-policies), [network rules](/user-guide/network-rules), [malicious IP protection categories](/user-guide/malicious-ip-protection), and optional [private connectivity](/user-guide/private-connectivity-inbound).
- **Access control:** [Access Control](/user-guide/security-access-control-overview) for RBAC and privileges, and [Multi-party Approval](/user-guide/multi-party-approval).
- **Data protection:** [Data movement policies](/user-guide/data-movement-policies) and [Tri-Secret Secure](/user-guide/security-encryption-tss).
- **Security monitoring:** [Trust Center](/user-guide/trust-center/overview) for account findings and detections, and [AI Security in Trust Center](/user-guide/trust-center/using-the-trust-center#label-trust-center-ai-security-tab) for AI workloads.
- **AI security:** [Agent identity](/user-guide/agent-identity), [Restricted Session Scope for agents](/user-guide/restricted-session-scope), and [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails) for prompt injection and jailbreak attempts.

## Choosing where to go next

Use the following table to find the topic that matches your task:

| If you want to… | See |
| --- | --- |
| Establish who can sign in and with what strength | [Overview of Snowflake authentication](/user-guide/security-authentication-overview) and [Authentication policies](/user-guide/authentication-policies) |
| Require MFA for password sign-ins | [Multi-factor authentication (MFA)](/user-guide/security-mfa) |
| Provision or deprovision users and groups from your IdP | [SCIM](/user-guide/scim-intro) |
| Restrict where clients may connect from | [Network policies](/user-guide/network-policies) and [Network rules](/user-guide/network-rules) |
| Connect without public internet paths | [Private connectivity for inbound network traffic](/user-guide/private-connectivity-inbound) and [Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound) |
| Review account security findings | [Trust Center](/user-guide/trust-center/overview) |
| Monitor AI workload posture in Trust Center | [AI Security in Trust Center](/user-guide/trust-center/using-the-trust-center#label-trust-center-ai-security-tab) |
| Define what roles and policies can see or change | [Access Control](/user-guide/security-access-control-overview) |
| Govern AI agents as distinct principals | [Agent identity](/user-guide/agent-identity) and [Restricted Session Scope for agents](/user-guide/restricted-session-scope) |
| Defend Cortex AI against prompt injection | [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails) |
| Limit or alert on sensitive data leaving Snowflake | [Data movement policies](/user-guide/data-movement-policies) |
| Control your own encryption key | [Tri-Secret Secure](/user-guide/security-encryption-tss) |
| Require a second approver for high-risk operations | [Multi-party Approval](/user-guide/multi-party-approval) |

Expand

Show lessSee more

## Authentication

- **[Overview of Snowflake authentication](/user-guide/security-authentication-overview):** How Snowflake authenticates users and services, and how to plan sign-in methods.
- **[Authentication policies](/user-guide/authentication-policies):** Using authentication policies to restrict account and user authentication by client, authentication methods, and more.
- **[Multi-factor authentication (MFA)](/user-guide/security-mfa):** Using multi-factor authentication with Snowflake.
- **[Leaked password protection](/user-guide/leaked-password-protection):** Monitoring and disabling passwords that have been leaked.
- **[Federated Authentication and SSO](/user-guide/admin-security-fed-auth-overview):** Topics related to federated authentication to Snowflake.
- **[Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth):** Using key-pair authentication to Snowflake.
- **[Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens):** Generating and managing programmatic access tokens for authentication.
- **[OAuth](/user-guide/oauth-intro):** Topics related to using Snowflake OAuth and External OAuth to connect to Snowflake.
- **[Workload identity federation](/user-guide/workload-identity-federation):** Preferred authentication method for service-to-service workloads accessing Snowflake data.
- **[External API authentication and secrets](/user-guide/api-authentication):** Configuring Snowflake to authenticate to external services.

## Network security

- **[Malicious IP protection](/user-guide/malicious-ip-protection):** Protecting your account from IP addresses that are known to be malicious.
- **[Controlling network traffic with network policies](/user-guide/network-policies):** Using network policies to restrict access to Snowflake.
- **[Network rules](/user-guide/network-rules):** Using network rules with other Snowflake features to restrict access to and from Snowflake.
- **[Private connectivity for inbound network traffic](/user-guide/private-connectivity-inbound):** Using private connectivity to access the Snowflake service, Snowsight, Streamlit in Snowflake, internal stages, Snowflake managed storage volumes, and Snowpark Container Services.
- **[Private connectivity for outbound network traffic](/user-guide/private-connectivity-outbound):** Using private connectivity for external network locations, external functions, external stages, external tables, external volumes, and Snowpipe automation.

## Access control

- **[Access Control](/user-guide/security-access-control-overview):** Topics related to role-based access control (RBAC) in Snowflake.
- **[Sessions and session policies](/user-guide/session-policies):** Using session policies to manage your Snowflake session.
- **[SCIM](/user-guide/scim-intro):** Topics related to using SCIM to provision users and groups to Snowflake.
- **[Multi-party Approval](/user-guide/multi-party-approval):** Using Multi-party Approval for a second-person review of security-sensitive and operationally risky critical operations.

## Data protection

- **[End-to-End Encryption](/user-guide/security-encryption-end-to-end):** Using end-to-end encryption in Snowflake.
- **[Tri-Secret Secure](/user-guide/security-encryption-tss):** Using a customer-managed key with a Snowflake-managed key to protect your data.
- **[Data movement policies](/user-guide/data-movement-policies):** Using data movement policies to proactively prevent data exfiltration across various movement channels in Snowflake.

## Security monitoring

- **[Trust Center](/user-guide/trust-center/overview):** Using the Trust Center to evaluate and monitor your account for security risks.
- **[AI Security in Trust Center](/user-guide/trust-center/using-the-trust-center#label-trust-center-ai-security-tab):** Monitoring AI-related misconfigurations, guardrail status, and agent activity.

## AI security

- **[Agent identity](/user-guide/agent-identity):** Recognizing when an AI agent is active in a session so you can audit and govern agent access separately from human access.
- **[Restricted Session Scope for agents](/user-guide/restricted-session-scope):** Limiting the privileges an agent can use when it acts on behalf of a user.
- **[Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails):** Screening inputs to AI features for prompt injection and jailbreak attempts. Requires Enterprise Edition or higher.

To monitor AI security posture, see [Security monitoring](#label-guides-overview-secure-security-monitoring).
