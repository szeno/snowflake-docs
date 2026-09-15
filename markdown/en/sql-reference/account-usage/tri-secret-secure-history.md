Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TRI\_SECRET\_SECURE\_HISTORY view

This Account Usage view provides information about [Tri-Secret Secure](/user-guide/security-encryption-tss)
customer-managed keys (CMKs) within the last year (365 days).

## Columns

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

- This view requires the SECURITY\_VIEWER role.
- Latency for the view may be up to 120 minutes (2 hours).

## Examples

Retrieve all Tri-Secret Secure history records:

> Copy code
>
> ```
> SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TRI_SECRET_SECURE_HISTORY;
> ```
