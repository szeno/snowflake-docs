Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$GET\_CMK\_AKV\_CONSENT\_URL

Returns a consent URL to the Azure Key Vault account related to customer-managed keys.

You can use the consent URL for your customer-managed keys with [Tri-Secret Secure](/user-guide/security-encryption-tss) for Snowflake accounts on Microsoft Azure.

See also:
:   [Customer-managed keys](/user-guide/security-encryption-manage#label-customer-managed-keys)

## Syntax

> Copy code
>
> ```
> SYSTEM$GET_CMK_AKV_CONSENT_URL( '<account_identifier>' , '<tenant_id>' )
> ```

## Arguments

`'account_identifier'`
:   Specifies the [account identifier](/user-guide/admin-account-identifier) for your Snowflake account on Azure.

    Required.

`'tenant_id'`
:   Specifies the unique identifier for the [tenant](https://docs.microsoft.com/en-us/azure/key-vault/general/basic-concepts) in your Azure
    subscription. This value is in the GUID/UUID format, such as `b3ddabe4-e5ed-4e71-8827-0cefb99af240`.

    Required.

    To locate this value, follow the instructions in [How to find your Azure Active Directory tenant ID](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant).

## Usage notes

- This function is for use in Snowflake accounts on Microsoft Azure only.
- Only account administrators (i.e. users with the ACCOUNTADMIN role) or a role that is granted the global MONITOR SECURITY privilege can
  call this function.

## Examples

Return the consent URL to the Azure Key Vault account related to customer-managed keys, where `my-account`
is the Snowflake account identifier in the [account name format](/user-guide/admin-account-identifier#label-account-name) for your Snowflake account on Azure and
`b3ddabe4-e5ed-4e71-8827-0cefb99af240` is the tenant identifier for your Azure subscription:

> Copy code
>
> ```
> SELECT SYSTEM$GET_CMK_AKV_CONSENT_URL('my-account' , 'b3ddabe4-e5ed-4e71-8827-0cefb99af240');
> ```
>
> Returns:
>
> ```
> https://login.microsoftonline.com/tenantId/oauth2/authorize?client_id=myClientId&response_type=code
> ```
