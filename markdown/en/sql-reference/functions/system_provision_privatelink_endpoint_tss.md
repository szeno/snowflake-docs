Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT\_TSS

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Provisions a private connectivity endpoint in the Snowflake VPC or VNet to enable Snowflake to connect to a key management service (KMS) by using
private connectivity. The endpoint can be a service endpoint or resource endpoint, depending on the cloud platform that hosts your Snowflake account.

Note

If the Snowflake account is in an Azure government region, the provider resource ID must be the ID of a resource in a government
subscription. For more information about government regions for Snowflake customers, see [U.S. SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions).

## Syntax

**AWS:**

Copy code

```
SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<provider_service_name>',
  '<host_name>'
  )
```

**Azure:**

Copy code

```
SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<provider_resource_id>',
  '<host_name>'
  )
```

**Google Cloud:**

Copy code

```
SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  '<target_service_id>',
  '<host_name>'
  )
```

## Arguments

**AWS:**

`provider_service_name`
:   Specifies the KMS service in AWS to connect to.

    For information about retrieving this value from AWS, see [Provision private connectivity endpoints](/user-guide/private-manage-endpoints-aws#label-private-link-external-access-aws-create-endpoints).

**Azure:**

`provider_resource_id`
:   Specifies the fully qualified identifier for the Azure Key Vault in your VPC or VNet.

**Google Cloud:**

`target_service_id`
:   Specifies the KMS service in Google Cloud to connect to.

`host_name`
:   Specifies the fully-qualified hostname to access the KMS resource in your VPC, VNet, or PSC network.

    This value does not contain any port numbers and must match what you specified in the Snowflake object that enables you to connect to the
    KMS.

## Returns

Returns a status message that the endpoint was provisioned successfully or details and instructions about why the endpoint was not
provisioned successfully.

## Access control requirements

Only users granted the MODIFY privilege on the account can call this function.
The MODIFY privilege is typically granted only to the ACCOUNTADMIN role.

## Usage notes

- You cannot modify an existing private connectivity endpoint; you must deprovision the endpoint, then provision a new one. To deprovision
  the endpoint, call the [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT\_TSS](/sql-reference/functions/system_deprovision_privatelink_endpoint_tss) system function.
- This function can take approximately 5 minutes to execute because it depends on the process to provision the private connectivity
  endpoint in the cloud platform (outside of Snowflake).
- For details about private endpoint limits, see [Scaling considerations](/user-guide/private-connectivity-outbound#label-private-connect-external-service-limits).

## Examples

**AWS:**

Set up outbound private connectivity to an external KMS resource:

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  'com.amazonaws.us-west-2.kms',
  'kms.us-west-2.amazonaws.com'
);
```

```
Private endpoint with ID "vpce-0123456789abcdef0" to resource "com.amazonaws.us-west-2.kms" has been provisioned successfully.
Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
```

**Azure:**

Provision a private endpoint on Microsoft Azure for TSS

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  '/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/providers/Microsoft.KeyVault/vaults/TriSecretVault',
  'trisecretvault.vault.azure.net'
);
```

```
Private endpoint with ID "/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/prod-snowplex-rg/providers/Microsoft.Network/privateEndpoints/12345678-90ab-cdef-1234-567890abcdef"
to resource "/subscriptions/12345678-90ab-cdef-1234-567890abcdef/resourceGroups/myvault/providers/Microsoft.KeyVault/vaults/TriSecretVault"
has been provisioned successfully.

 Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
```

**Google Cloud:**

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT_TSS(
  'cloudkms.us-west2.rep.googleapis.com',
  'cloudkms.us-west2.rep.googleapis.com'
);
```

```
Private endpoint with ID "abcd0000000000001234" to resource "cloudkms.us-west2.rep.googleapis.com" has been provisioned successfully.
Please note the Private Endpoint ID and approve the corresponding connection request in the cloud provider console.
```
