Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REGISTER\_CMK\_INFO

Registers your customer-managed key (CMK) for use with Tri-Secret Secure.

See also:
:   [Understanding CMK self-registration with support activation of Tri-Secret Secure](/user-guide/security-encryption-tss#label-encryption-tss-self-register)

## Syntax

**AWS:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO( '<cmk_arn>' [ , '<privatelink_enabled>' ] )
```

**Azure:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO( '<vault_uri>' , '<key_name>' [ , '<privatelink_enabled>' ] )
```

**Google Cloud:**

Copy code

```
SYSTEM$REGISTER_CMK_INFO( '<project_id>' , '<location>', '<key_ring>' , '<key_name>' [ , '<privatelink_enabled>' ] )
```

## Arguments

**Required:**

**AWS**

`cmk_arn`
:   Specifies the Amazon Web Services resource number (ARN) that specifies the customer-managed key (CMK) for use with Tri-Secret Secure.

**Azure**

`vault_uri`
:   Specifies the Microsoft Azure unique endpoint identifier for your Azure Key Vault.

`key_name`
:   Specifies the name for your CMK in Microsoft Azure.

**Google Cloud**

`project_id`
:   Specifies the unique identifier for your project in Google Cloud.

`location`
:   Specifies the Google Cloud region that hosts your Snowflake account.

`key_ring`
:   Specifies the key ring for your CMK in Google Cloud.

`key_name`
:   Specifies the name for your CMK in Google Cloud.

**Optional:**

`privatelink_enabled`

> Specify whether or not to use your private connectivity endpoint for Tri-Secret Secure by passing in one of the following values:
>
> Important
>
> If you omit this argument or pass in an empty string, Snowflake doesn’t use a private connectivity endpoint for Tri-Secret Secure.
>
> `'TRUE'`
> :   Specifies that Snowflake uses the provisioned private connectivity endpoint for Tri-Secret Secure.
>
> `'FALSE'` (default)
> :   Specifies that Snowflake doesn’t use a private connectivity endpoint for Tri-Secret Secure.
>
> `''`
> :   Empty string. Same behavior as `'FALSE'`.

## Returns

Returns a status message stating that the registration is complete.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Examples

Register your CMK for your Snowflake account on Amazon Web Services:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59');
```

Register your CMK for your Snowflake account on Microsoft Azure:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('https://trisecretsite.vault.azure.net/', 'trisecretazkey');
```

Register your CMK for your Snowflake account on Google Cloud:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('my-env', 'us-west1', 'trisecrettest', 'trisecretgcpkey');
```

Register your CMK with a privatelink endpoint for your Snowflake account on Amazon Web Services:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('arn:aws:kms:us-west-2:736112632310:key/ceab36e4-f0e5-4b46-9a78-86e8f17a0f59', 'true');
```

Register your CMK with a privatelink endpoint for your Snowflake account on Microsoft Azure:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('https://trisecretsite.vault.azure.net/', 'trisecretazkey', 'true');
```

Register your CMK with a privatelink endpoint for your Snowflake account on Google Cloud:

Copy code

```
SELECT SYSTEM$REGISTER_CMK_INFO('my-env', 'us-west1', 'trisecrettest', 'trisecretgcpkey', 'true');
```
