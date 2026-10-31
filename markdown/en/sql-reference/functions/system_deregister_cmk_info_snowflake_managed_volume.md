Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEREGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Cancels registration of your currently-registered customer-managed key (CMK) for use with Tri-Secret Secure for Snowflake storage for Iceberg tables.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$DEREGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

Returns a status message stating that registration of your current CMK is cancelled.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- You can register only one CMK at a time. If
  [SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) fails because a different CMK is already registered,
  call this function to remove it, then register the new key.
- Deregistering removes the CMK from the registered slot only. It doesn’t deactivate a key that’s already active, and it has no effect
  on the encryption configuration or bucket policy of your Snowflake-managed storage volume.
- Calling this function when no CMK is registered succeeds and doesn’t change any state.

## Examples

Deregister the CMK registered on your Snowflake account:

Copy code

```
SELECT SYSTEM$DEREGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```
