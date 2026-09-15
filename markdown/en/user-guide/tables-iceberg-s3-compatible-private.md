# Private connectivity to external volumes for S3-compatible storage

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up outbound private connectivity to an external volume for S3-compatible storage. The
primary difference between outbound public connectivity and outbound private connectivity is how you set the `USE_PRIVATELINK_ENDPOINT`
property for the external volume.

When the external volume is configured to use private connectivity, your connection to the S3-compatible storage service goes through your
cloud provider’s internal network. By configuring your external volume to use outbound private connectivity, you add additional security
to your operations by blocking public access to the storage location.

S3-compatible external volumes are supported on Snowflake accounts deployed on Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP). The steps to provision a private endpoint depend on which cloud provider hosts your Snowflake account.

For more information about using external volumes to connect to your external cloud storage for Iceberg tables, see
[Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations

You can configure outbound public connectivity and outbound private connectivity for the same S3-compatible storage service. If you want
to do this, create a dedicated external volume for outbound public connectivity and specify `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Set up outbound private connectivity to an external volume

### Syntax updates

The `USE_PRIVATELINK_ENDPOINT` property of an external volume determines whether it is accessed through private connectivity or by
traversing the public network. To use private connectivity, set `USE_PRIVATELINK_ENDPOINT = TRUE` when creating or modifying an external
volume.

The syntax for CREATE EXTERNAL VOLUME and ALTER EXTERNAL VOLUME is as follows:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME <ext_volume_name>
  STORAGE_LOCATIONS =
  (
    (
      NAME = '<storage_location_name>'
      STORAGE_PROVIDER = 'S3COMPAT'
      STORAGE_BASE_URL = 's3compat://<bucket>/<path>/'
      CREDENTIALS = (
        AWS_KEY_ID = '<key_id>'
        AWS_SECRET_KEY = '<secret_key>'
      )
      STORAGE_ENDPOINT = '<s3_compatible_endpoint>'
      USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ]
    )
  )
  ALLOW_WRITES = TRUE;

ALTER EXTERNAL VOLUME <ext_volume_name>
  UPDATE STORAGE_LOCATION = '<storage_location_name>'
  USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ];
```

The [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) command includes the `USE_PRIVATELINK_ENDPOINT` property and its value.

### Provision a private endpoint

The steps to provision a private endpoint depend on the cloud provider that hosts your Snowflake account. Follow the steps for your
deployment.

#### AWS

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private endpoint in your
Snowflake VNet for the S3-compatible storage service:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '<service_name>',
  '<s3_compatible_endpoint_hostname>');
```

Where `<service_name>` is the PrivateLink service name provided by your S3-compatible storage provider, and
`<s3_compatible_endpoint_hostname>` is the fully qualified hostname of your S3-compatible API endpoint (the value you specify for
`STORAGE_ENDPOINT` in the external volume).

#### Azure

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private endpoint for the
S3-compatible storage service:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '<resource_id>',
  '<s3_compatible_endpoint_hostname>',
  '<subresource>');
```

Where `<resource_id>` is the Azure resource ID of Azure storage privatelink service, `<s3_compatible_endpoint_hostname>` is the fully
qualified hostname of your S3-compatible API endpoint, and `<subresource>` is the sub-resource type for the storage service, the options
being `blob` or `dfs`.

After calling the function, approve the private endpoint in the Azure Portal as the owner of the Azure storage resource. For details,
see the [approval process](https://learn.microsoft.com/en-us/azure/private-link/manage-private-endpoint?tabs=manage-private-link-powershell#private-endpoint-connections).

#### GCP

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private endpoint for the
S3-compatible storage service:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '<service_endpoint>',
  '<s3_compatible_endpoint_hostname>');
```

Where `<service_endpoint>` is the Private Service Connect service endpoint provided by your S3-compatible storage provider, and
`<s3_compatible_endpoint_hostname>` is the fully qualified hostname of your S3-compatible API endpoint.

### Configure external volume access

After provisioning the private endpoint, follow these steps to create the external volume and verify connectivity:

1. Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your S3-compatible storage service
   will be able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
2. Create the external volume, and set the `USE_PRIVATELINK_ENDPOINT` property to `TRUE`. For example:

   Copy code

   ```
   CREATE EXTERNAL VOLUME ext_vol_s3_compat_private
     STORAGE_LOCATIONS =
     (
       (
         NAME = 'my_s3_compat_storage_location'
         STORAGE_PROVIDER = 'S3COMPAT'
         STORAGE_BASE_URL = 's3compat://mybucket/unload/mys3compatdata'
         CREDENTIALS = (
           AWS_KEY_ID = '1a2b3c...'
           AWS_SECRET_KEY = '4x5y6z...'
         )
         STORAGE_ENDPOINT = 'mystorage.example.com'
         USE_PRIVATELINK_ENDPOINT = TRUE
       )
     )
     ALLOW_WRITES = TRUE;
   ```
3. After the private endpoint has an `"APPROVED"` status, verify that the external volume is functional:

   Copy code

   ```
   SELECT SYSTEM$VERIFY_EXTERNAL_VOLUME('ext_vol_s3_compat_private');
   ```

## Deprovision an endpoint

If you no longer need the private connectivity endpoint for the external volume, unset the `USE_PRIVATELINK_ENDPOINT` property on the
external volume, and then call the [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.
