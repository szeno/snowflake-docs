# SCIM security integrations

Snowflake supports SCIM integration with the following identity providers to provision, manage, and synchronize users and groups in Snowflake:

- [Okta](/user-guide/scim-okta)
- [Microsoft Azure Active Directory](/user-guide/scim-azure)
- [Custom integrations](/user-guide/scim-custom)

Note

You can use custom SCIM integrations with identity providers that do not have a dedicated integration to provision, manage, and
synchronize users and groups in Snowflake.

You should use custom SCIM integrations for identity providers that are neither Okta nor Microsoft Azure AD.

## Replicating security integrations

Snowflake supports replication and failover/failback with the SCIM security integration from the source account to the target account.

For details, see [Replication of security integrations & network policies across multiple accounts](/user-guide/account-replication-security-integrations).
