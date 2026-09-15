# Overview of Snowflake authentication

The following sections describe the authentication methods that users and applications can use to access Snowflake. They also provide key
considerations to help you select the best authentication method for your use case.

## Choosing authentication for Snowsight

Snowsight is the user interface for Snowflake. This section provides an overview of the authentication methods that users can use
to sign in to Snowsight, followed by a comparison of the methods.

Note

When you create a Snowflake user object for a person authenticating to Snowsight, specify `TYPE = PERSON`. For more information
about user types, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

Single sign-on (SSO)
:   With SSO for Snowsight, users authenticate with a third-party identity provider (IdP) rather than authenticating
    with Snowflake directly. When a user accesses Snowsight, the sign-in page includes an option to authenticate with the IdP instead
    of a Snowflake-managed password. The IdP confirms the user’s identity and sends proof to Snowflake. Depending on how federated authentication is configured, this proof is
    either a Security Assertion Markup Language (SAML) assertion or an OpenID Connect (OIDC) ID token. Because Snowflake and the IdP have a
    previously established relationship of trust, Snowflake accepts this proof as verification of the user’s identity, and allows the user to access
    Snowsight.

    For configuration details, see [Overview of federated authentication and SSO](/user-guide/admin-security-fed-auth-overview) and [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc).

    Some organizations use the same IdP to provide an SSO experience for all of the organization’s applications. These organizations can
    simply add Snowflake as a new service provider (SP) to allow its employees to use the IdP to access Snowsight.

Username and password with multi-factor authentication (MFA)
:   Password authentication lets users access Snowsight by entering a string of characters that conform to the requirements enforced
    by a password policy. To strengthen the security of this authentication method, Snowflake requires MFA for all
    password users. With MFA, the user enters a password, and then uses a second factor of authentication to confirm their identity. For
    example, a user might use a passkey stored on their computer as the second factor of authentication.

The following table compares authentication methods that users can use to sign in to Snowsight:

| Method | Advantages | Challenges |
| --- | --- | --- |
| Single sign-on   Preferred option | Lets an organization centrally manage authentication. A user authenticates with the same IdP for all of the organization’s applications, not just Snowflake.  Ideal for organizations that already use an IdP to provide SSO for applications. | Requires configuration of a third-party IdP. |
| Password with MFA | Simple implementation. | If passwords are managed by Snowflake, an organization must repeat authentication setup for all of its applications. |

Expand

Show lessSee more

## Overview of authentication methods for applications

In this topic, *application* refers to anything that accesses Snowflake data programmatically rather than
through the Snowsight user interface. This definition includes custom web applications, third-party multi-tenant applications,
desktop applications, local scripts, and workloads in the cloud.

When discussing available authentication methods, this topic distinguishes between two types of applications:

> - An *interactive application* that interacts with a person and authenticates to Snowflake on behalf of that person; for example, a
>   business intelligence (BI) tool that interacts with analysts.
> - A *service-to-service application* that doesn’t interact with a person and has a dedicated authentication method for the service; for
>   example, a CI/CD pipeline.

Workload identity federation (WIF)
:   Workload identity federation is a form of secretless authentication, and is highly secure because it leverages short-lived credentials
    that are already available to cloud workloads. It eliminates the need to manage and rotate secrets.

    When a workload is running on a cloud provider like AWS EC2, Microsoft Azure VMs, or Google Cloud VMs, workload identity federation lets
    the workload authenticate to Snowflake by using the cloud provider’s native identity mechanism. For example, a workload running on AWS
    EC2 can obtain an attestation — that is, proof of its identity — from an AWS Identity and Access Management (IAM) role that is
    associated with the workload. The workload’s driver obtains the attestation from the native identity mechanism and then sends it to
    Snowflake to authenticate the workload.

    Workload identity federation also allows third-party workloads like GitHub Actions and workloads running in Kubernetes to authenticate
    with an OpenID Connect-compliant identity provider (IdP), in a process known as *OIDC federation*. Snowflake accepts ID tokens generated
    by the IdP as proof of the workload’s identity.

    **Suitable for**:

    - Service-to-service applications

OAuth using Snowflake as the authorization server (Snowflake OAuth)
:   Snowflake OAuth provides the security of the [OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749). With
    Snowflake OAuth, Snowflake is both the authorization server that authenticates a Snowflake user and the resource server that accepts an
    access token from the client to access that user’s data. Snowflake OAuth lets the client use the authorization code grant type.

    Because Snowflake is the authorization server, the user who is interacting with the application uses the Snowflake user interface to
    authenticate. You can configure Snowflake to authenticate the user with single sign-on (SSO) or a password. For information about the
    advantages and challenges of SSO and password authentication, see [Choosing authentication for Snowsight](#label-auth-overview-choose-snowsight).

    **Suitable for**:

    - Interactive applications

OAuth using a third-party authorization server (External OAuth)
:   External OAuth also provides the security of OAuth 2.0, but a third-party IdP, not Snowflake, acts as the authorization
    server. An application obtains an access token from the third-party IdP, then uses the token to access Snowflake as the resource.

    A service-to-service application could use the client credentials grant type to access its own Snowflake data. An interactive application
    could use the authorization code grant type to access the Snowflake data of a person who is using the application.

    **Suitable for**:

    - Interactive applications
    - Service-to-service applications

Key-pair authentication
:   Key-pair authentication relies on a *cryptographic key pair*: a private key and a public key. The private key is a secret kept by the
    application, while the public key is associated with a Snowflake user object. During authentication, the application sends proof that it
    has the private key, and Snowflake responds by verifying that the private key corresponds to the public key associated with the Snowflake
    user. This authentication method eliminates the need to transmit or store passwords, reducing the risk of credential theft.

    **Suitable for**:

    - Interactive applications
    - Service-to-service applications

Programmatic access tokens (PATs)
:   A PAT is a time-limited credential that allows applications to authenticate without a password. A PAT can be
    used as a drop-in replacement for a single-factor password in scenarios where MFA or more secure methods of
    authentication won’t work. A PAT is stronger than a password because it is a short-lived credential, requires that you implement additional
    security measures, and can be scoped to a specific access control role.

    **Suitable for**:

    - Interactive applications
    - Service-to-service applications

## Choosing authentication for interactive applications

An interactive application is one that interacts with a person and authenticates to Snowflake on behalf of that person. The following table
provides the advantages and challenges associated with authentication methods that you can use for interactive applications. For an
overview of these authentication methods, see [Overview of authentication methods for applications](#label-auth-overview-applications).

Note

When you create Snowflake user objects for the people who are using an interactive app, specify `TYPE = PERSON`. For more information
about user types, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

| Method | Advantages | Challenges |
| --- | --- | --- |
| Snowflake OAuth   Strong option | - Can be simpler to implement than External OAuth. - Local applications, such as a script running in VS Code, can use a built-in implementation of Snowflake OAuth, which provides the   security of OAuth without administrative setup. [Learn more](/user-guide/oauth-local-applications) - Avoids driver limitations. - User can authorize access with single sign-on (SSO), which allows them to use the secure authentication methods of a third-party   IdP. | None. |
| External OAuth   Strong option | - If the IdP supports it, the person using the application can use a secretless form of authentication. - Ideal for organizations that already use a third-party IdP as an authorization server for their applications. | Requires expertise in configuring a third-party IdP as an authorization server. |
| Programmatic access token (PAT) | - Easy replacement for single-factor passwords. - Snowflake-generated credential, so it can’t be reused outside of Snowflake. - Can be scoped to a specific access control role to limit damage if it is compromised. - Snowflake *requires* that you implement additional security measures to mitigate the risks of using long-lived secrets. - [GitHub secret scanner program](https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partnership-program/secret-scanning-partner-program)   automatically detects leaked Snowflake PATs in public repositories, disables them, and notifies Snowflake administrators. | - Unlike key-pair, must be secured on both client and server. - Unlike key-pair, the secret must be sent in the request to Snowflake, increasing exposure. - If compromised, anyone with possession can impersonate the application. - Security risks associated with long-lived credentials must be mitigated with other security measures like a robust storage and   rotation strategy. - Because network policies are required, if you have a multi-tenant cloud application, you must provide your customers with your   IP addresses so they can create a network policy that allows those address ranges. - Input field that accepts PATs must be at least 256 characters. |
| Key-pair | - Flexible authentication method. - Passwordless credential that isn’t exposed in a request. | - Not usually used for interactive applications. - Security risks associated with long-lived credentials must be mitigated with other security measures like network policies and a   robust storage and rotation strategy. Unlike programmatic access tokens, key-pair doesn’t *require* additional measures, which can   result in less secure authentication. |

Expand

Show lessSee more

## Choosing authentication for service-to-service applications

A service-to-service application doesn’t interact with a person and has a dedicated authentication method for the service. The following
table provides the advantages and challenges associated with authentication methods that you can use for service-to-service applications.
For an overview of these authentication methods, see [Overview of authentication methods for applications](#label-auth-overview-applications).

Note

When you create a Snowflake user object for a service-to-service application, specify `TYPE = SERVICE`. For more information about user
types, see [Types of users](/user-guide/admin-user-management#label-user-management-types).

| Method | Advantages | Challenges |
| --- | --- | --- |
| Workload identity federation   Preferred option | - Secretless authentication. - Administrators don’t have to continuously secure and rotate client IDs and secrets. | None. |
| External OAuth   Strong option | - If the IdP supports it, the application can use a secretless form of authentication. - Ideal for organizations that already use a third-party IdP as an authorization server for their applications. | Requires expertise in configuring a third-party IdP as an authorization server. |
| Key-pair | - Flexible authentication method. - Passwordless credential that isn’t exposed in a request. | Security risks associated with long-lived credentials must be mitigated with other security measures like network policies and a robust storage and rotation strategy. Unlike programmatic access tokens, key-pair doesn’t *require* additional measures, which can result in less secure authentication. |
| Programmatic access token (PAT) | - Easy replacement for single-factor passwords. - Snowflake-generated credential, so it can’t be reused outside of Snowflake. - Can be scoped to a specific access control role to limit damage if it is compromised. - Snowflake *requires* that you implement additional security measures to mitigate the risks of using long-lived secrets. - [GitHub secret scanner program](https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partnership-program/secret-scanning-partner-program)   automatically detects leaked Snowflake PATs in public repositories, disables them, and notifies Snowflake administrators. | - Unlike key-pair, must be secured on both client and server. - Unlike key-pair, the secret must be sent in the request to Snowflake, increasing exposure. - If compromised, anyone with possession can impersonate the application. - Security risks associated with long-lived credentials must be mitigated with other security measures like a robust storage and   rotation strategy. |

Expand

Show lessSee more
