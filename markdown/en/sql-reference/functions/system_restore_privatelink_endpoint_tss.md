Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT\_TSS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Restores a private connectivity endpoint in the Snowflake VPC or VNet to enable Snowflake to connect to an external key management service (KMS) resource
by using private connectivity. The endpoint can be a service endpoint or a resource endpoint, depending on the cloud platform that hosts your
Snowflake account.

You can restore a private endpoint within 7 days of deprovisioning it. After 7 days, the endpoint cannot be restored and you need to
recreate the endpoint with the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_provision_privatelink_endpoint_tss) system function.

## Syntax

**AWS:**

Copy code

```
SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  '<provider_service_name>'
  )
```

**Azure:**

Copy code

```
SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  '<provider_resource_id>'
  )
```

**Google Cloud:**

Copy code

```
SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  '<target_service_id>'
  )
```

## Arguments

**AWS:**

`provider_service_name`
:   Specifies the external KMS resource endpoint to restore.

**Azure:**

`provider_resource_id`
:   Specifies the fully-qualified identifier for the resource in your VPC or VNet.

**Google Cloud:**

`target_service_id`
:   Specifies the service attachment ID (to a custom service), or regional Google API endpoint to connect to.

## Returns

Returns a status message stating that the endpoint, with its identifier, is restored successfully.

If unsuccessful, returns an error — for example, if the provided argument is not a valid existing endpoint. If you do not know the endpoint
name, you can use the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function to list all endpoints in your
Snowflake account.

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can call this function.

## Usage notes

An error message occurs if a private connectivity endpoint is not associated with the specified arguments.

## Examples

**AWS:**

Restore a private endpoint with external access to an AWS key store.

Copy code

```
SELECT SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  'com.amazonaws.us-west-2.s3'
);
```

**Azure:**

Restore a private endpoint to allow Snowflake on Microsoft Azure to connect to the Azure key vault in your Azure VNet:

Copy code

```
SELECT SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  '/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/providers/Microsoft.KeyVault/vaults/TriSecretVault'
);
```

```
"Resource Endpoint with id "/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/privatelink-test/providers/Microsoft.KeyVault/vaults/TriSecretVault/privateEndpoints/" restored successfully.
```

**Google Cloud:**

Copy code

```
SELECT SYSTEM$RESTORE_PRIVATELINK_ENDPOINT_TSS(
  'cloudkms.us-west2.rep.googleapis.com'
);
```

```
Private endpoint with id 'abcd0000000000001234' restored successfully.
```
