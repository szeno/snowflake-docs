Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# TRI\_SECRET\_SECURE\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view provides information about [Tri-Secret Secure](/user-guide/security-encryption-tss)
customer-managed keys (CMKs) for accounts in your organization within the last year (365 days).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | System-generated ID that uniquely identifies a CMK used in the account. |
| REGISTERED\_BY\_USER\_ID | NUMBER | Identifies the user who registered the CMK. Also appears in the ACCOUNT\_USAGE view if a customer self-registered the CMK. |
| CMK\_ACTIVATION\_STATUS | VARCHAR | Activation status of the CMK. Valid values are:   - PENDING\_ACTIVATION - ACTIVATED - PENDING\_DEACTIVATION - DISABLED |
| CMK\_IDENTIFIER | VARCHAR | Displays a value that you can use to locate your customer managed key. For example:   - AWS: key ARN - Azure: `https://mykeyvault.vault.azure.com/keys/my-rsa-key` - Google Cloud: `projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME` |
| IS\_REGISTERED | BOOLEAN | Whether the key represented by the CMK identifier is registered or not. |
| REGISTERED\_ON | TIMESTAMP\_LTZ | Identifies the last time when a user registered the CMK. |
| ACTIVATED\_ON | TIMESTAMP\_LTZ | Identifies the last time when a user activated the CMK. |
| DISABLED\_ON | TIMESTAMP\_LTZ | Identifies the last time when a user disabled the CMK. |
| UPDATED\_ON | TIMESTAMP\_LTZ | Identifies the time of the last update to this view. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
- This view only returns rows for accounts with the Business Critical or Virtual Private Snowflake (VPS) service level.

## Examples

Retrieve all Tri-Secret Secure history records for accounts in your organization:

> Copy code
>
> ```
> SELECT * FROM SNOWFLAKE.ORGANIZATION_USAGE.TRI_SECRET_SECURE_HISTORY;
> ```
