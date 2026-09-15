# Azure private endpoints for internal stages

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides concepts as well as detailed instructions for connecting to Snowflake internal stages through Microsoft Azure Private
Endpoints.

## Overview

[Azure private endpoints](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview) and
[Azure Private Link](https://docs.microsoft.com/en-us/azure/private-link/private-link-overview) can be combined to provide secure
connectivity to Snowflake internal stages. This setup ensures that data loading and data unloading operations to Snowflake internal stages
use the Azure internal network and do not take place over the public internet.

Before Microsoft supported private endpoints for internal stage access, it was necessary to create a proxy farm within the Azure VNet to
facilitate secure access to Snowflake internal stages. With the added support of private endpoints for Snowflake internal stages, users
and client applications can now access Snowflake internal stages over the private Azure network. The following diagram summarizes this new support:

![Connect to internal stage using Azure Private Link](/static/images/internal-stage-private-connect-azure.png)

Note the following regarding the numbers in the BEFORE diagram:

- Users have two options to connect to a Snowflake internal stage:

  - Option A allows an on-premises connection directly to the internal stage as shown by the number 1.
  - Option B allows a connection to the internal stage through a proxy farm as shown by the numbers 2 and 3.
- If using the proxy farm, users can also connect to Snowflake directly as denoted by the number 4.

Note the following regarding the numbers in the AFTER diagram:

- For clarity, the diagram shows a single private endpoint from one Azure VNet pointing to a single Snowflake internal stage (6 and 7).

  Note that it is possible to configure multiple private endpoints, each within a different VNet, that point to the same Snowflake internal
  stage.
- The updates in this feature remove the need to connect to Snowflake or a Snowflake internal stage through a proxy farm.
- An on-premises user can connect to Snowflake directly as shown in number 5.
- To connect to a Snowflake internal stage, on-premises user connects to a private endpoint, number 6, and then uses Azure Private Link
  to connect to the Snowflake internal stage as shown in number 7.

In Azure, each Snowflake account has a dedicated storage account to use as an internal stage. The storage account URIs are different
depending on whether the connection to the storage account uses private connectivity (that is, Azure Private Link). The private connectivity
URL includes a `privatelink` segment in the URL.

Public storage account URI:
:   `<storage_account_name>.blob.core.windows.net`

Private connectivity storage account URI:
:   `<storage_account_name>.privatelink.blob.core.windows.net`

After you [configure a private endpoint connection](#label-private-internal-stages-azure-configure-endpoints) for your account’s internal
stage, Microsoft Azure automatically creates a CNAME record in the public DNS service that points the storage account host to its Azure
Private Link counterpart. This counterpart is `.privatelink.blob.core.windows.net`.

## Benefits

Implementing private endpoints to access Snowflake internal stages provides the following advantages:

- Internal stage data does not traverse the public internet.
- Client and SaaS applications, such as Microsoft PowerBI, that run outside of the Azure VNet can connect to Snowflake securely.
- Administrators are not required to modify firewall settings to access internal stage data.
- Administrators can implement consistent security and monitoring regarding how users connect to storage accounts.

## Limitations

Microsoft Azure defines how a private endpoint can interact with Snowflake:

- A single private endpoint can communicate to a single Snowflake Service Endpoint. You can have multiple one-to-one configurations that
  connect to the same Snowflake internal stage.
- The maximum number of private endpoints in your storage account that can connect to a Snowflake internal stage is fixed. For details, see
  [Standard storage account limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#standard-storage-account-limits).

## Configuring private endpoints to access Snowflake internal stages

To configure private endpoints to access Snowflake internal stages, you must have support from the following three roles in your
organization:

1. The Snowflake account administrator (that is, a user with the Snowflake ACCOUNTADMIN system role).
2. The Microsoft Azure administrator.
3. The network administrator.

Depending on the organization, it may be necessary to coordinate the configuration efforts with more than one person or team to implement
the following configuration steps.

Complete the following steps to configure and implement secure access to Snowflake internal stages through Azure private endpoints:

1. Verify that your Azure subscription is registered with the Azure Storage resource manager. This step allows you to connect to the
   internal stage from a private endpoint.
2. As a Snowflake account administrator, run the following commands in your Snowflake account and record the `ResourceID` of the
   internal stage storage account defined by the `privatelink_internal_stage` key. For more information, see
   [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) and [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config).

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   ALTER ACCOUNT SET ENABLE_INTERNAL_STAGES_PRIVATELINK = true;
   SELECT KEY, VALUE FROM TABLE(flatten(input=>parse_json(system$get_privatelink_config())));
   ```
3. As the Azure administrator, create a private endpoint through the Azure portal.

   View the private endpoint properties and record the resource ID value. You will provide this value as the `privateEndpointResourceID`
   function argument in the next step.

   Verify that the **Target sub-resource** value is set to `blob`.

   For more information, see the Microsoft Azure Private Link [documentation](https://docs.microsoft.com/en-us/azure/private-link/).

   Important

   Before you proceed with the next step to authorize the private endpoint, you should be aware of the Microsoft Azure DNS behavior when a private
   endpoint is authorized on a storage location *for the very first time*.

   When the first private endpoint is connected and authorized, Azure automatically creates a CNAME record in its public DNS for
   `storage-account-name.privatelink.blob.core.windows.net`.

   Under normal circumstances, this DNS update should not affect existing public connectivity to the storage account. However, if your
   environment already has private DNS zones configured for `.privatelink.blob.core.windows.net`, this DNS update can lead to unintended
   behavior. Specifically, existing storage clients attempting to access the public endpoint `storage-account-name.blob.core.windows.net`
   may fail DNS resolution or be unable to reach the storage account using public IP.

   To avoid this issue, Microsoft recommends enabling the **Fallback to Internet** option in the private DNS zone configuration before
   authorizing the first private endpoint. This guidance also appears as a cautionary note in the Microsoft Azure [DNS zone configuration documentation](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns#azure-services-dns-zone-configuration).
4. As the Snowflake administrator, call the [SYSTEM$AUTHORIZE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_authorize_stage_privatelink_access) function using the
   `privateEndpointResourceID` value as the function argument. This step authorizes access to the Snowflake internal stage through the
   private endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$AUTHORIZE_STAGE_PRIVATELINK_ACCESS('<privateEndpointResourceID>');
   ```

   To verify which private endpoints are authorized for the internal stage of
   your account and to check the approval status of each endpoint connection,
   call the
   [SYSTEM$GET\_STAGE\_PRIVATELINK\_AUTHORIZED\_ENDPOINTS](/sql-reference/functions/system_get_stage_privatelink_authorized_endpoints)
   function.

   If necessary, complete these steps to [revoke](#label-private-internal-stages-azure-disable-endpoints) access to the internal
   stage.
5. Involve your network administrator to update the DNS settings in a private DNS zone. The settings must resolve the privatelink blob URL
   `<storage_account_name>.privatelink.blob.core.windows.net` to the private IP address(es) of the Azure private endpoint that connects
   to your storage account internal stage.

   For more information, see
   [Azure Private Endpoint DNS configuration](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-dns).

   Tip

   - Use a separate Snowflake account for testing, and configure a private DNS zone in a test VNet to test the feature so that the testing
     is isolated and does not impact your other workloads.
   - If using a separate Snowflake account is not possible, use a test user to access Snowflake from a test VPC where the DNS changes are
     made.
   - To test from on-premises applications, use DNS forwarding to forward requests to the Azure private DNS in the VNet where the DNS
     settings are made. Run the following command from the client machine to verify that the IP address returned is the private IP
     address for the storage account:

     Copy code

     ```
     dig <storage_account_name>.blob.core.windows.net
     ```

## Blocking public access — *Recommended*

After you configure private endpoints to access the internal stage using Azure Private Link, you can optionally block requests from
public IP addresses to the internal stage. After blocking public access, all traffic must be through the private endpoint.

Controlling public access to an Azure internal stage differs from controlling public access to the Snowflake service. You use the
[SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_block_internal_stages_public_access) function, not a network policy, to block requests to the internal
stage. Unlike network policies, this function can’t block some public IP addresses while allowing others. Calling the SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS function blocks all public IP addresses.

Important

Confirm that traffic using private connectivity is successfully reaching the internal stage before blocking public access. Blocking
public access without configuring private connectivity can cause unintended disruptions, including interference with managed services like
Azure Data Factory.

The SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS function enforces its restrictions by altering the **Networking** settings of the Azure
storage account where the internal stage is located. These Azure settings are commonly referred to as the “storage account firewall
settings”. Calling this Snowflake system function does the following actions in Azure:

- Sets the **Public network access** field to **Enabled from selected virtual networks and IP addresses**.
- Adds Snowflake VNet subnet ids to the **Virtual Networks** section.
- Clears all IP addresses from the **Firewall** section.

To block all traffic from public IP addresses to the internal stage, call the following function:

Copy code

```
SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS();
```

The function can take a few minutes to complete.

### Blocking public access with IP allowlist exceptions

The [SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_internal_stages_public_access_with_exception) function extends the set of functions for
blocking public access to internal stages. While the SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS function blocks all public IP addresses,
SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION lets you block public access while maintaining an allowlist of IP addresses or CIDR blocks that are permitted to reach an internal stage location on Microsoft Azure.

Note

This feature is not supported on Amazon Web Services or Google Cloud.

To block public access to internal stages on Microsoft Azure while allowing specific IP addresses or CIDR blocks, take the following steps:

1. [Define IP allowlist exceptions](#label-block-public-define-allowlist)
2. [Verify function status](#label-block-public-verify-status)
3. [Test stage access with a pre-signed URL](#label-block-public-test-access)

#### Define IP allowlist exceptions

To create or modify an allowlist that defines which IP addresses can access an internal stage location on Microsoft Azure, call the
[SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS\_WITH\_EXCEPTION](/sql-reference/functions/system_block_internal_stages_public_access_with_exception) function and provide a comma-separated
list of IP addresses or CIDR ranges as function arguments. For example:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS_WITH_EXCEPTION('1.2.3.4/24, 100.0.0.1, 101.0.0.0/31');
```

Note

You can also call this function to replace an existing allowlist with a different one.

#### Verify function status

Check that the feature is active and view the IP allowlist by calling the
[SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_internal_stages_public_access_status) function:

Copy code

```
SELECT SYSTEM$INTERNAL_STAGES_PUBLIC_ACCESS_STATUS();
```

#### Test stage access with a pre-signed URL

To confirm the allowlist is working correctly:

1. Ensure the [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) parameter is set to TRUE.
2. Create an internal stage and upload a sample file for testing.
3. Generate a pre-signed URL for that file and test access from different IP addresses. Only requests originating from allowlisted IPs
   should be allowed.

   Copy code

   ```
   SELECT GET_PRESIGNED_URL(@my_stage, 'data/sample.csv');
   ```

#### Examples

Block public access while allowing specific IP addresses and CIDR ranges:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS_WITH_EXCEPTION('100.0.0.1', '1.2.3.0/24', '101.0.0.0/31');
```

```
Public Access to internal stages is blocked. Private link is required to connect to internal stages of this account. Exceptions: 100.0.0.1, 1.2.3.0/24, 101.0.0.0/31
```

Replace the existing allowlist with a new set of exceptions:

Copy code

```
SELECT SYSTEM$BLOCK_INTERNAL_STAGES_PUBLIC_ACCESS_WITH_EXCEPTION('200.0.0.1', '10.0.0.0/16');
```

```
Public Access to internal stages is blocked. Private link is required to connect to internal stages of this account. Exceptions: 200.0.0.1, 10.0.0.0/16
```

### Ensuring public access is blocked

To determine whether public IP addresses are able to access an internal stage, call the [SYSTEM$INTERNAL\_STAGES\_PUBLIC\_ACCESS\_STATUS](/sql-reference/functions/system_internal_stages_public_access_status) function.

If the Azure settings are currently blocking all public traffic, the function returns `Public Access to internal stages is blocked`.
This verifies that the settings have not been changed since the SYSTEM$BLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS function was called.

If at least some public IP addresses can access the internal stage, the function returns
`Public Access to internal stages is unblocked`.

### Unblocking public access

To allow public access to an internal stage that was previously blocked, call the [SYSTEM$UNBLOCK\_INTERNAL\_STAGES\_PUBLIC\_ACCESS](/sql-reference/functions/system_unblock_internal_stages_public_access) function.

Calling this function alters the **Networking** settings of the Azure storage account where the internal stage is located. It sets the
Azure **Public network access** field to **Enabled from all networks**.

## Revoking private endpoints to access Snowflake internal stages

To revoke access to Snowflake internal stages through Microsoft Azure private endpoints, complete the following steps:

1. As a Snowflake administrator, confirm that the [ENABLE\_INTERNAL\_STAGES\_PRIVATELINK](/sql-reference/parameters#label-enable-internal-stages-privatelink) parameter is set to `TRUE`. For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SHOW PARAMETERS LIKE 'enable_internal_stages_privatelink' IN ACCOUNT;
   ```
2. As a Snowflake administrator, call the [SYSTEM$REVOKE\_STAGE\_PRIVATELINK\_ACCESS](/sql-reference/functions/system_revoke_stage_privatelink_access) function to revoke access
   to the private endpoint, and use the same `privateEndpointResourceID` value that was used to originally authorize access to the private
   endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SELECT SYSTEM$REVOKE_STAGE_PRIVATELINK_ACCESS('<privateEndpointResourceID>');
   ```
3. As an Azure administrator, delete the private endpoint through the Azure portal.
4. As a network administrator, remove the DNS and alias records that were used to resolve the storage account URLs.

At this point, the access to the private endpoint is revoked. The query result from calling the
[SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) function shouldn’t return the `privatelink_internal_stage` key and its
value.

## Troubleshooting

Azure applications that access Snowflake stages over the public internet and also use a private DNS service to resolve service host names
cannot access Snowflake stages if a private endpoint connection is established to the stage as described in this topic.

If any application has configured a private DNS region for the same domain, then Microsoft Azure tries to resolve the storage account host
by querying the private DNS service. If the entry for the storage account is not found in the private DNS service, a connection error occurs.

To address this issue, use one of the following two options:

1. Remove or dissociate the private DNS region from the application.
2. Create a CNAME record for the storage account private hostname — that is, `<storage_account_name>.privatelink.blob.core.windows.net`
   — in the private DNS service and point it to the hostname specified by the output of this command:

   Copy code

   ```
   dig CNAME <storage_account_name>.privatelink.blob.core.windows.net
   ```
