Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$REVOKE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS

Revokes the authorization for Snowflake to access the private endpoint for
[Azure private endpoints for Snowflake-managed storage volumes](/user-guide/private-managed-volumes-azure) for the current account.

See also:
:   [SYSTEM$AUTHORIZE\_SNOWFLAKE\_MANAGED\_STORAGE\_VOLUME\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_snowflake_managed_storage_volume_privatelink_access),
    [Revoking private endpoints to access Snowflake-managed storage volumes](/user-guide/private-managed-volumes-azure#label-private-managed-volumes-azure-disable-endpoints)

## Syntax

Copy code

```
SYSTEM$REVOKE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK_ACCESS( '<private_endpoint_resource_id>' )
```

## Arguments

`'private_endpoint_resource_id'`
:   The unique identifier for the Azure Private Endpoint.

    For instructions on how to obtain this value, see
    [Configuring private endpoints to access Snowflake-managed storage volumes](/user-guide/private-managed-volumes-azure#label-private-managed-volumes-azure-configure-endpoints).

## Usage notes

- Only account administrators (that is, users with the ACCOUNTADMIN role) can call this function.
- This function is supported for Snowflake accounts on Microsoft Azure only.

## Examples

Revoke access to an Azure private endpoint for a Snowflake-managed storage volume:

> Copy code
>
> ```
> USE ROLE ACCOUNTADMIN;
>
> SELECT SYSTEM$REVOKE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK_ACCESS(
>   '/subscriptions/subId/resourceGroups/rg1/providers/Microsoft.Network/privateEndpoints/pe1');
> ```
