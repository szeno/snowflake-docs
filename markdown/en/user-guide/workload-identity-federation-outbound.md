# Workload identity federation for Snowflake workloads that access external services

Workload identity federation is an authentication method used by service-to-service applications and workloads that don’t interact with
human users. It is a strong authentication method because it uses short-lived credentials that don’t need to be rotated or managed by an
administrator.

In workload identity federation, which is based on the [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html) (OIDC)
identity layer of OAuth 2.0, the workload obtains an ID token from an OpenID provider, and then sends that token to an external service as
proof of the workload’s identity. The external service verifies that the token is valid, then allows the workload to access the service’s
resource.

Snowflake can act as the OIDC provider for Snowflake workloads that are accessing the resources of external services. As the OIDC provider,
Snowflake issues an ID token for the Snowflake workload to present to an external service for authentication.

## Workflow

Implementing workload identity federation for a Snowflake workload consists of the following steps:

1. [Create a secret object](#label-wif-snowflake-workload-create-secret) for the Snowflake workload that is authenticating with
   workload identity federation.
2. [Establish a trust relationship](#label-wif-snowflake-workload-trust-relationship) between the Snowflake workload and the external
   service.
3. [Obtain ID tokens](#label-wif-snowflake-workload-token) from Snowflake as the OIDC provider.

## Create a secret for workload identity federation

In Snowflake, a secret is a schema-level object that represents credentials required to authenticate. When you create a secret of type
`WORKLOAD_IDENTITY_FEDERATION`, two things happen:

- Snowflake becomes an OIDC provider with an issuer URL. This issuer URL is stored as a property of the secret.
- The Snowflake workload becomes an OIDC client that can obtain ID tokens from Snowflake as the OIDC provider. The secret identifier of the
  client, which becomes the subject claim of ID tokens, is stored as a property of the secret.

Create a secret that makes workload identity federation possible for a Snowflake workload by running the following command:

Copy code

```
CREATE SECRET my_db.auth.my_workload
    TYPE = WORKLOAD_IDENTITY_FEDERATION;
```

For more information about creating secrets, see [CREATE SECRET](/sql-reference/sql/create-secret).

Note

There is a 1:1 relationship between the Snowflake workload and Snowflake as the OIDC provider, but the workload can use the same secret to
authenticate to multiple services.

## Establish a trust relationship between the workload and the service

In workload identity federation, the Snowflake workload sends ID tokens it obtains from Snowflake to the external service. Before the
workload starts sending these tokens to authenticate, it must establish a relationship with the service to prove that the tokens are coming
from the workload and not another source.

To establish a trust relationship, a Snowflake user gives the administrator of the service the following information:

- Issuer URL of the Snowflake OIDC provider. This value is a property of the secret.
- Identifier of the workload as an OIDC client. This value is a property of the secret.

To obtain these identifiers that the service needs to establish the relationship of trust, run a [DESCRIBE SECRET](/sql-reference/sql/desc-secret)
command. For example, if you created the secret `my_workload` for your Snowflake workload, run the following command:

Copy code

```
DESC SECRET my_db.auth.my_workload;
```

Record the following values from the output to provide them to the service:

| Column | Description |
| --- | --- |
| `workload_identity_federation_issuer` | Issuer URL of Snowflake as the OIDC provider. Give this value to the service so it can compare it to the `iss` claim of the ID token. |
| `workload_identity_federation_subject` | Identifier of the workload as the OIDC client. Give this value to the service so it can compare it to the `sub` claim of the ID token. |

Expand

Show lessSee more

## Obtain ID tokens

With workload identity federation, every time the Snowflake workload wants to authenticate to the external service, it obtains an ID token
from Snowflake as the OIDC provider and sends it to the service.

To obtain an ID token, call the [SYSTEM$ISSUE\_WORKLOAD\_IDENTITY\_FEDERATION\_TOKEN](/sql-reference/functions/system_issue_workload_identity_federation_token) function. The function
accepts two arguments:

- The secret that was created so the workload can authenticate with workload identity federation.
- The identifier of the service where the workload is sending the ID token. A workload can use the same secret to authenticate to multiple
  services, so you must specify the service — that is, the audience — when obtaining the ID token. This identifier becomes the `aud`
  claim of the ID token.

For example, to obtain an ID token that is being sent to the service at `example-cloud-service.com`, run the following command:

Copy code

```
SELECT SYSTEM$ISSUE_WORKLOAD_IDENTITY_FEDERATION_TOKEN(
    'my_db.auth.my_workload',
    '{"aud": "example-cloud-service.com"}');
```

Take the encoded ID token returned by the system function and send it to the service to authenticate.

## Replication and failover

When you replicate a database that contains a `WORKLOAD_IDENTITY_FEDERATION` secret, keep the following in mind:

- The federated identity is preserved across failover. The secret’s issuer URL and subject identifier are replicated unchanged, so after a
  failover the external service continues to recognize the same `iss` and `sub` claims. You don’t need to re-establish the trust
  relationship with the external service.
- ID tokens can only be issued from the primary account. Calling
  [SYSTEM$ISSUE\_WORKLOAD\_IDENTITY\_FEDERATION\_TOKEN](/sql-reference/functions/system_issue_workload_identity_federation_token) in an account
  that is a read-only secondary fails. Issue tokens from the current primary account.
- Token verification continues to work after failover. The issuer URL that you provided to the external service automatically resolves to
  the current primary account, which publishes the public keys that the service uses to verify the ID token’s signature. You don’t need to
  update the external service’s configuration after a failover.
