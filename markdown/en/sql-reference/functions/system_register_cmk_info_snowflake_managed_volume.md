Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME

Registers your customer-managed key (CMK) for use with Tri-Secret Secure for Snowflake storage for Iceberg tables.

See also:
:   [Tri-Secret Secure for Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-snowflake-storage-tss)

## Syntax

**AWS:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME( '<cmk_arn>' )
```

**Azure:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME( '<vault_uri>', '<key_name>' )
```

## Arguments

**AWS:**

`cmk_arn`
:   The Amazon Resource Name (ARN) of the AWS KMS key to register. Accepts both `key/<uuid>` and `alias/<name>` ARN formats.

**Azure:**

`vault_uri`
:   Specifies the Microsoft Azure unique endpoint identifier for your Azure Key Vault.

`key_name`
:   Specifies the name for your CMK in Microsoft Azure. Don’t include a key version.

## Returns

Returns a status message stating that the registration is complete.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

- You can register only one CMK at a time. If a different CMK is already registered, this function fails and directs you to call
  [SYSTEM$DEREGISTER\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_deregister_cmk_info_snowflake_managed_volume) before registering a new one.
- Registering a CMK doesn’t affect active Iceberg table reads or writes. The key isn’t applied to storage until you call
  [SYSTEM$ACTIVATE\_CMK\_INFO\_SNOWFLAKE\_MANAGED\_VOLUME](/sql-reference/functions/system_activate_cmk_info_snowflake_managed_volume).
- Calling this function with the CMK that is already registered succeeds and doesn’t change any state.
- The CMK must be unique to Tri-Secret Secure for Snowflake storage for Iceberg tables. This function fails if the key is already used by Tri-Secret Secure on your Snowflake account or by Snowflake Postgres Tri-Secret Secure.

## Examples

Register your CMK for your Snowflake account:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME('arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59');
```

Register your CMK for your Snowflake account on Microsoft Azure:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO_SNOWFLAKE_MANAGED_VOLUME('https://trisecretsite.vault.azure.net/', 'trisecretazkey');
```
