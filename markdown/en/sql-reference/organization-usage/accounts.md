Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# ACCOUNTS view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The ACCOUNTS view in the ORGANIZATION\_USAGE schema can be used to obtain details about the accounts in an organization.

Note

This view is getting updated to transition from use of “billing entities” to “contract number”. The
`CONTRACT_NUMBER` column has been added, and the `CONSUMPTION_BILLING_ENTITY_NAME`,
`MARKETPLACE_CONSUMER_BILLING_ENTITY_NAME`, and `MARKETPLACE_PROVIDER_BILLING_ENTITY_NAME` columns are
deprecated and will be removed after October 26, 2026. Update any queries that reference the billing entity
columns to use `CONTRACT_NUMBER` instead. For more information, see
[Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399).

## Columns

| Column, Data Type, Description |  |  |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_NAME | VARCHAR | User-defined name that identifies an account within the organization. |
| CREATED\_ON | TIMESTAMP | Date and time when the account was created. |
| REGION | VARCHAR | Snowflake Region where the account is located. A Snowflake Region is a distinct location within a cloud platform region that is isolated from other Snowflake Regions. A Snowflake Region can be either multi-tenant or single-tenant (for a Virtual Private Snowflake account). |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account is located. |
| EDITION | VARCHAR | [Snowflake Edition](/user-guide/intro-editions) of the account. |
| IS\_ORG\_ADMIN | BOOLEAN | Indicates whether the [ORGADMIN role](/user-guide/organization-administrators) is enabled in an account. |
| IS\_LOCKED | BOOLEAN | Indicates whether the account is locked. To determine if it was locked because it was dropped, look for a date and time in the SCHEDULED\_DELETION\_TIME column. If an account is unexpectedly locked, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support). |
| ACCOUNT\_URL | VARCHAR | Preferred Snowflake [account URL](/user-guide/organizations-connect#label-connecting-via-url) that includes the values of organization\_name and account\_name. |
| ACCOUNT\_OLD\_URL | VARCHAR | If the original [account URL](/user-guide/organizations-connect#label-connecting-via-url) was saved when the account was renamed, provides the original URL. If the original account URL was dropped, the value is NULL even if the account was renamed. |
| ACCOUNT\_OLD\_URL\_LAST\_USED | VARCHAR | If the original account URL was saved when the account was renamed, indicates the last time the account was accessed using the original URL. |
| ORGANIZATION\_OLD\_URL | VARCHAR | If the account’s organization was changed in a way that created a new [account URL](/user-guide/organizations-connect#label-connecting-via-url) and the original account URL was saved, provides the original account URL. If the original account URL was dropped, the value is NULL even if the organization changed. |
| ORGANIZATION\_OLD\_URL\_LAST\_USED | VARCHAR | If the account’s organization was changed in a way that created a new account URL and the original account URL was saved, indicates the last time the account was accessed using the original account URL. |
| ACCOUNT\_LOCATOR | VARCHAR | [System-assigned identifier](/user-guide/admin-account-identifier#label-account-locator) of the account. |
| MANAGED\_ACCOUNTS | VARCHAR | Indicates how many [reader accounts](/user-guide/data-sharing-reader-create) have been created by the account. |
| IS\_MANAGED | BOOLEAN | Indicates whether the account is a reader account. If `true`, the account is a reader account. |
| PARENT\_ACCOUNT | VARCHAR | For reader accounts, provides the name of the parent account that is providing the reader account to consumers. |
| CONTRACT\_NUMBER | NUMBER(38, 0) | Number of the active contract that the account is mapped to. For multi-contract organizations, use this column to determine which contract an account bills against. To list all active contracts in the organization, use [SHOW ORGANIZATION CONTRACTS](/sql-reference/sql/show-organization-contracts). |
| CONSUMPTION\_BILLING\_ENTITY\_NAME | VARCHAR | **Deprecated.** Name of the consumption billing entity associated with an account. Replaced by CONTRACT\_NUMBER; this column will be removed after October 26, 2026. See [Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399). |
| MARKETPLACE\_CONSUMER\_BILLING\_ENTITY\_NAME | VARCHAR | **Deprecated.** Name of the marketplace consumer billing entity associated with an account. Replaced by CONTRACT\_NUMBER; this column will be removed after October 26, 2026. See [Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399). |
| MARKETPLACE\_PROVIDER\_BILLING\_ENTITY\_NAME | VARCHAR | **Deprecated.** Name of the marketplace provider billing entity associated with an account. Replaced by CONTRACT\_NUMBER; this column will be removed after October 26, 2026. See [Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399). |
| ALTERED\_ON | TIMESTAMP | Date and time of the most recent change to the account. |
| SCHEDULED\_DELETION\_TIME | TIMESTAMP | Date and time when a [dropped account](/user-guide/organizations-manage-accounts-delete) will be permanently deleted. |
| DELETED\_ON | TIMESTAMP | Date and time when the account was permanently deleted. |
| MOVED\_ON | TIMESTAMP | Date and time when the account was moved from the current organization to a different one. |
| COMMENT | VARCHAR | Comment associated with the account. |
| IS\_EVENTS\_ACCOUNT | BOOLEAN | Indicates whether an account is an events account. For more information, see [Use logging and event tracing for an app](/developer-guide/native-apps/event-about). |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- Deleted accounts are removed from the view after one year.
- Use the CONTRACT\_NUMBER column to identify which contract an account bills
  against. The billing entity columns are deprecated and will be removed after October 26, 2026. For more
  information, see [Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399).
