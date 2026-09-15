Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT\_TSS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprovisions a private connectivity endpoint in the Snowflake VPC or VNet to prevent Snowflake from connecting to an external key management service (KMS) resource
using private connectivity. The endpoint can be a service endpoint or a resource endpoint depending on the cloud platform that hosts your
Snowflake account.

If you call this function and mistakenly remove an endpoint, call the [SYSTEM$RESTORE\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_restore_privatelink_endpoint_tss)
system function to restore the endpoint within seven days. After seven days, the endpoint is deleted and can’t be recovered;
you will need to recreate the endpoint with the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_provision_privatelink_endpoint_tss).

## Syntax

**AWS:**

Copy code

```
SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<provider_service_name>'
  )
```

**Azure:**

Copy code

```
SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<provider_resource_id>'
  )
```

**Google Cloud:**

Copy code

```
SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<target_service_id>'
  )
```

## Arguments

**AWS:**

`provider_service_name`
:   Specifies the external KMS resource endpoint.

**Azure:**

`provider_resource_id`
:   Specifies the fully-qualified identifier for the resource in your VPC or VNet.

**Google Cloud:**

`target_service_id`
:   Specifies the service attachment ID or regional Google API endpoint.

## Returns

Returns a status message stating that the endpoint, with its identifier, is deprovisioned successfully.

## Access control requirements

Only users granted the MODIFY privilege on the account can call this function.
The MODIFY privilege is typically granted only to the ACCOUNTADMIN role.

## Usage notes

An error message occurs if a private connectivity endpoint is not associated with the specified arguments.

## Examples

**AWS:**

Deprovision a private endpoint with external access to the AWS KMS:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS('com.amazonaws.us-west-2.s3');
```

**Azure:**

Deprovision a private endpoint to prevent Snowflake from connecting to an external key vault on Microsoft Azure for Tri-Secret Secure:

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS(
  '/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/providers/Microsoft.KeyVault/vaults/TriSecretVault', 'trisecretvault.vault.azure.net'
);
```

```
"Resource Endpoint with id "/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/privatelink-test/providers/Microsoft.KeyVault/vaults/TriSecretVault/privateEndpoints/" deprovisioned successfully"
```

**Google Cloud:**

Copy code

```
SELECT SYSTEM$DEPROVISION_PRIVATELINK_ENDPOINT_TSS(
  'cloudkms.us-west2.rep.googleapis.com'
);
```

```
Private endpoint with id 'abcd0000000000001234' successfully marked for deletion. It may be restored within 7 days of deprovisioning.
```
