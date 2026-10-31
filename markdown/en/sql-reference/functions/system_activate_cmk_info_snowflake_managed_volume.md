Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$ACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Activates Tri-Secret Secure for Snowflake storage for Iceberg tables in your account by setting your registered customer-managed key (CMK) as the encryption
key on your account’s Snowflake-managed storage volume.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

Copy code

```
SYSTEM$ACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME()
```

## Arguments

None.

## Returns

Success or error messages.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- You must register a CMK with [SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_register_cmk_info_snowflake_managed_volume) before calling this
  function.
- Activation is immediate and applies only to data written after activation. Tri-Secret Secure for Snowflake storage for Iceberg tables doesn’t rekey data
  that was already written under a different key.
- If a different CMK is already active, activating the registered CMK rotates your Snowflake-managed storage volume to the new key.
- Activating a CMK that is already active succeeds and doesn’t change any state.

## Examples

Activate Tri-Secret Secure for Snowflake storage for Iceberg tables for your Snowflake account:

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME();
```
