Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VERIFY\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Verifies that Snowflake can use your customer-managed key (CMK) for Tri-Secret Secure for Snowflake storage for Iceberg tables, and returns a message about
the result.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$VERIFY_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

Verifies your pre-registered CMK, falling back to your active CMK if none is registered, and returns a descriptive string rather than
raising an error when verification fails. Always read the output before continuing.

Successful output begins:

```
CMK verification successful for Snowflake-managed storage.
```

Unsuccessful output begins:

```
CMK verification failed for Snowflake-managed storage:
```

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

On AWS, if verification fails, review the key-policy statement returned by
[SYSTEM$GET\_CMK\_CONFIG\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_get_cmk_config_snowflake_managed_volume), confirm you added it to your KMS key policy, and call this
function again.

On Microsoft Azure, if verification fails, confirm that the Snowflake service principal has the `Microsoft.KeyVault/vaults/keys/read`,
`Microsoft.KeyVault/vaults/keys/wrap/action`, and `Microsoft.KeyVault/vaults/keys/unwrap/action` permissions on your key, and call this
function again.

## Examples

Verify the CMK registered or active on your Snowflake account:

Copy code

```
SELECT SYSTEM$VERIFY_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```
