# Private connectivity to S3-compatible stage

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides configuration details to set up outbound private connectivity to an external stage for S3-compatible storage. The
primary difference between outbound public connectivity and outbound private connectivity is how you configure the
`USE_PRIVATELINK_ENDPOINT` property for the stage.

When the stage is configured to use private connectivity, your connection to the S3-compatible storage service goes through your cloud
provider’s internal network. By configuring your stage to use outbound private connectivity, you add security to your data
loading and unloading operations by blocking public access to the storage location.

S3-compatible stages are supported on Snowflake accounts deployed on Amazon Web Services (AWS), Microsoft Azure, and Google Cloud
Platform (GCP). The steps to provision a private endpoint depend on which cloud provider hosts your Snowflake account.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations

The `USE_PRIVATELINK_ENDPOINT` property is set per stage, so a single S3-compatible storage service can support both private and public
connectivity at the same time. To do this, create separate stages that point to the same storage service:

- For private connectivity, create a stage with `USE_PRIVATELINK_ENDPOINT = TRUE`.
- For public connectivity, create a stage with `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Syntax updates

The `USE_PRIVATELINK_ENDPOINT` property of a stage determines whether it is accessed through private connectivity or by traversing the
public network. To use private connectivity, set `USE_PRIVATELINK_ENDPOINT = TRUE` when creating or modifying a stage.

Copy code

```
CREATE OR REPLACE STAGE <stage_name>
  URL = 's3compat://<bucket>/<path>/'
  ENDPOINT = '<s3_compatible_endpoint>'
  CREDENTIALS = (
    AWS_KEY_ID = '<key_id>'
    AWS_SECRET_KEY = '<secret_key>'
  )
  USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ]

ALTER STAGE <stage_name>
  SET USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ]
```

The [DESCRIBE STAGE](/sql-reference/sql/desc-stage) command includes the `USE_PRIVATELINK_ENDPOINT` property and its value.

## Configure external stage access

### Provision a private endpoint

The steps to provision a private endpoint depend on the cloud provider that hosts your Snowflake account. Follow the steps for your
deployment.

#### AWS

Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system function to provision a private endpoint in your
Snowflake VPC for the S3-compatible storage service:

Copy code

```
USE ROLE ACCOUNTADMIN;

SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '<service_name>',
  '<s3_compatible_endpoint_hostname>');
```

Where `<service_name>` is the PrivateLink service name provided by your S3-compatible storage provider (for example,
`com.amazonaws.vpce.us-east-1.vpce-svc-0123456789abcdef0`), and `<s3_compatible_endpoint_hostname>` is the fully qualified hostname of
your S3-compatible API endpoint, for example `mystorage.example.com` (the value you specify for `ENDPOINT` in the stage).

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

Where `<resource_id>` is the Azure resource ID of the Azure storage Private Link service (for example,
`/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount`),
`<s3_compatible_endpoint_hostname>` is the fully qualified hostname of your S3-compatible API endpoint (for example, `mystorage.example.com`),
and `<subresource>` is the subresource type for the storage service, either `blob` or `dfs`.

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

Where `<service_endpoint>` is the Private Service Connect service endpoint provided by your S3-compatible storage provider (for example,
`projects/my-project/regions/us-central1/serviceAttachments/my-service-attachment`), and `<s3_compatible_endpoint_hostname>` is the
fully qualified hostname of your S3-compatible API endpoint (for example, `mystorage.example.com`).

### Create an external stage with private connectivity

After provisioning the private endpoint, follow these steps to create the stage and verify connectivity:

1. Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your S3-compatible storage service
   will be able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
2. Create the external stage, and set the `USE_PRIVATELINK_ENDPOINT` property to `TRUE`. For example:

   Copy code

   ```
   CREATE STAGE my_s3compat_private_stage
     URL = 's3compat://mybucket/files/'
     ENDPOINT = 'mystorage.example.com'
     CREDENTIALS = (
       AWS_KEY_ID = '1a2b3c...'
       AWS_SECRET_KEY = '4x5y6z...'
     )
     USE_PRIVATELINK_ENDPOINT = TRUE;
   ```
3. After the private endpoint has an `"APPROVED"` status, test loading data into Snowflake from the external stage:

   Copy code

   ```
   COPY INTO my_table
     FROM @my_s3compat_private_stage/load/;
   ```

   For more information about loading and unloading data, see [Work with Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage).

## Configure external volume access

To configure private connectivity for S3-compatible storage with an external volume for Iceberg tables, see
[Private connectivity to external volumes for S3-compatible storage](/user-guide/tables-iceberg-s3-compatible-private).

## Deprovision an endpoint

If you no longer need the private connectivity endpoint for the external stage, unset the `USE_PRIVATELINK_ENDPOINT` property on the
stage, and then call the [SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.
