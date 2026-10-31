Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Deactivates Tri-Secret Secure for Snowflake storage for Iceberg tables in your account by reverting your account’s Snowflake-managed storage volume to
Snowflake-managed encryption.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$DEACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

Success or error messages.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- Data written while the CMK was active stays encrypted under that key after deactivation. Keep the key available in AWS KMS for as
  long as you need to read that data.
- On AWS, deactivation reverts the default encryption on your Snowflake-managed storage volume to Snowflake-managed encryption and removes the
  bucket policy statements that enforced the CMK.
- Calling this function when no CMK is active succeeds and doesn’t change any state.
- On Microsoft Azure, deactivation switches the storage accounts that back your Snowflake-managed storage volumes to Microsoft-managed encryption. Keep your key available in Azure Key Vault until this function completes successfully.

## Examples

Deactivate Tri-Secret Secure for Snowflake storage for Iceberg tables for your Snowflake account:

Copy code

```
SELECT SYSTEM$DEACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```
