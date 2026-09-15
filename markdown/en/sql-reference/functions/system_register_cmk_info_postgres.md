Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REGISTER\_CMK\_INFO\_POSTGRES

Registers your customer-managed key (CMK) for use with Snowflake Postgres Tri-Secret Secure.

## Syntax

**AWS:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO_POSTGRES( '<cmk_arn>' )
```

**Azure:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO_POSTGRES( '<vault_uri>' , '<key_name>' )
```

## Arguments

`cmk_arn`
:   Specifies the Amazon Web Services resource number (ARN) that specifies the customer-managed key (CMK) for use with Tri-Secret Secure.

`vault_uri`
:   Specifies the Microsoft Azure unique endpoint identifier for your Azure Key Vault.

`key_name`
:   Specifies the name for your CMK in Microsoft Azure.

`project_id`
:   Specifies the unique identifier for your project in Google Cloud Platform.

`location`
:   Specifies the Google Cloud Platform region that hosts your Snowflake account.

`key_ring`
:   Specifies the key ring for your CMK in Google Cloud Platform.

`key_name`
:   Specifies the name of your CMK.

## Returns

Returns a status message stating that the registration is complete.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

Register your CMK for your Snowflake account on Amazon Web Services:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO_POSTGRES('arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59');
```

Register your CMK for your Snowflake account on Microsoft Azure:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO_POSTGRES('https://trisecretsite.vault.azure.net/', 'trisecretazkey');
```
