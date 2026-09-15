# External API authentication and secrets

This topic provides concepts about external API authentication and secrets.

## Overview

External API authentication provides a pathway to authenticate to a service that is hosted outside of Snowflake. The API request to access
the service requires the API request to be authenticated. Snowflake supports the following methods of authentication while using External
API Authentication:

- Basic authentication.
- OAuth with code grant flow.
- OAuth with client credentials flow.

Snowflake supports basic authentication (i.e. username and password) in the API request header as specified in
[RFC 7617](https://datatracker.ietf.org/doc/html/rfc7617), where the authentication credentials are encoded using Base64. Similarly,
Snowflake supports OAuth 2.0 as specified in [RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749). In Snowflake,
the authentication credentials are stored and accessed securely from an object called a secret. The secret is used with a connector to
access the service outside of Snowflake, such as the [Snowflake Connector for ServiceNow](https://other-docs.snowflake.com/connectors/servicenow/about.html). A security integration for
[external API authentication](/sql-reference/sql/create-security-integration-api-auth) enables Snowflake to connect to the service
hosted outside of Snowflake when using the OAuth flows.

A secret is a schema-level object that stores sensitive information, limits access to the sensitive information using
[RBAC](/user-guide/security-access-control-overview), and is encrypted using the Snowflake
[key encryption hierarchy](/user-guide/security-encryption-manage#label-encryption-key-mgmt). Information present in the secret object is encrypted using a key in the key
hierarchy. After you create a secret, only dedicated Snowflake components such as integrations and external functions can read the
sensitive information.

For example, an external function needs to access and read the secret to pass the authentication credentials into an API authorization
header to make an API request to the service outside of Snowflake. The binding of the secret to the external function occurs during the
connector installation process. However, if a user runs a [DESCRIBE SECRET](/sql-reference/sql/desc-secret) operation on the secret, the password value
stored in the secret is never exposed.

Snowflake provides centralized management and access control of credentials used for API authentication in the secret. You can implement
separation of duties (i.e. SoD) for the management of the secret and the roles associated with managing the connector. The connector only
needs to use the secret name, and the users granted the connector roles do not need to view the sensitive information stored in the secret.

## Managing secrets

Snowflake provides the following commands to manage the secret object:

- [CREATE SECRET](/sql-reference/sql/create-secret)
- [ALTER SECRET](/sql-reference/sql/alter-secret)
- [DESCRIBE SECRET](/sql-reference/sql/desc-secret)
- [DROP SECRET](/sql-reference/sql/drop-secret)
- [SHOW SECRETS](/sql-reference/sql/show-secrets)

Snowflake supports the following privileges to determine whether users can create, use and own secrets.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Usage |
| --- | --- |
| CREATE | Enables creating a new secret in a schema. |
| USAGE | Enables using a secret. |
| OWNERSHIP | Transfers ownership of the secret, which grants full control over the secret. Required to alter most properties of a secret. |

Expand

Show lessSee more

The following table summarizes the relationship between the secret command operations and their necessary privileges.

| Operation | Privilege |
| --- | --- |
| CREATE SECRET | A role with the USAGE privilege on the parent database and schema with the CREATE SECRET privilege in the same schema. |
| ALTER SECRET | A role with the OWNERSHIP privilege on the secret. |
| DROP SECRET | A role with the OWNERSHIP privilege on the secret. |
| DESCRIBE SECRET | A role with the USAGE privilege on the secret. |
| SHOW SECRETS | A role with the USAGE privilege on the secret. |
| USE SECRET | A role with the USAGE privilege on the secret.  This privilege is required for the role creating the external function and calling the external function at query runtime, if the secret is to be used with an external function. |

Expand

Show lessSee more

## Using external API authentication and secrets

For representative examples, see:

- [Snowflake Connectors](https://other-docs.snowflake.com/connectors.html)
- [Creating and using an external access integration](/developer-guide/external-network-access/creating-using-external-network-access)

Additionally, you can replicate secrets using [account replication](/user-guide/account-replication-intro). For details, see
the Replication and secrets section in [Replication considerations](/user-guide/account-replication-considerations).
