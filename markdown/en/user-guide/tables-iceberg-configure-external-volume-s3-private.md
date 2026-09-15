# Private connectivity to external volumes for Amazon Web Services

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

This feature is unavailable in AWS Government regions (Commercial Gov and
SnowGov) because of the enforcement of Federal Information Processing
Standard (FIPS) compliance in these regions. AWS PrivateLink for S3
[doesn’t support S3 FIPS endpoints](https://docs.aws.amazon.com/AmazonS3/latest/userguide/privatelink-interface-endpoints.html#privatelink-limitations).
For the AWS regions in which FIPS is enforced, see
[Supported cloud regions](/user-guide/intro-regions).

This topic provides configuration details to set up outbound private connectivity to an external volume on AWS. The primary difference
between the outbound public connectivity and outbound private connectivity is how you set the `USE_PRIVATELINK_ENDPOINT` property for
the external volume.

When the external volume is configured to use private connectivity, your connection to the AWS cloud storage service goes through the
AWS internal network. By configuring your external volume to use outbound private connectivity, you add additional security to your
data-unloading operations by blocking public access to the storage account.

For more information about using external volumes to connect to your external cloud storage for Iceberg tables, see
[Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

Note

You can use AWS PrivateLink to access Snowflake-managed Iceberg tables and Iceberg tables that use a catalog integration for object
storage. In addition, you can use AWS PrivateLink to access externally managed Iceberg tables and Iceberg tables created from Delta files
in object storage.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations

You can configure outbound public connectivity and outbound private connectivity for the same cloud storage service. If you want to do this,
create a dedicated external volume for outbound public connectivity and specify `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Set up outbound private connectivity to an external volume

To set up outbound private connectivity to an external volume, you can [use SQL](#label-configure-external-volume-s3-private-sql)
or [use Snowsight](#label-configure-external-volume-s3-private-snowsight).

### Use SQL

#### Syntax updates

The `USE_PRIVATELINK_ENDPOINT` property of an external volume determines whether it is accessed through private connectivity or
by traversing the public network. To use private connectivity, set `USE_PRIVATELINK_ENDPOINT = TRUE` when creating or modifying an external
volume.

The new syntax for CREATE EXTERNAL VOLUME and ALTER EXTERNAL VOLUME is as follows:

Copy code

```
CREATE OR REPLACE EXTERNAL VOLUME <ext_volume_name>
  STORAGE_LOCATIONS =
  (
    (
      NAME = 'my-s3-loc'
      STORAGE_PROVIDER = 's3'
      STORAGE_BASE_URL = 's3://<bucket>[/<path>/]'
      STORAGE_AWS_ROLE_ARN = '<iam_role>'
      USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ]
    )
  )
  ALLOW_WRITES=true;

ALTER EXTERNAL VOLUME <ext_volume_name>
  UPDATE STORAGE_LOCATION = '<storage_location_name>'
  USE_PRIVATELINK_ENDPOINT = [ TRUE | FALSE ];
```

The [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) command includes the `USE_PRIVATELINK_ENDPOINT` property and its value.

#### Configure external volume access

Use the following steps to use outbound private connectivity to unload data to an external volume on AWS:

1. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system
   function to provision a private endpoint in your Snowflake VNet to enable Snowflake to connect to external AWS cloud
   storage over private connectivity.

   As the following example demonstrates, you must use a wildcard character (`*`) instead of specifying an individual AWS S3 bucket. Using
   the wildcard does not mean that all S3 buckets are accessed over a private connection. Only buckets referenced by an external volume that
   has the USE\_PRIVATELINK\_ENDPOINT parameter enabled can be accessed via the endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
    'com.amazonaws.us-west-2.s3',
    '*.s3.us-west-2.amazonaws.com');
   ```

   This function binds the private endpoint to the hostname, which enables the external volume to use the private endpoint to connect
   to the storage location, as long as AWS PrivateLink is enabled on the object.
2. Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
3. Create the external volume, being sure to set the `USE_PRIVATELINK_ENDPOINT` property to `TRUE`. For example:

   Copy code

   ```
   CREATE EXTERNAL VOLUME external_volume
     STORAGE_LOCATIONS =
    (
      (
        NAME = 'my-s3-loc'
        STORAGE_PROVIDER = 's3'
        STORAGE_BASE_URL = 's3://bucketinuswest2/'
        STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
        USE_PRIVATELINK_ENDPOINT = TRUE
      )
    )
     ALLOW_WRITES=TRUE;
   ```
4. Use the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command to create an Iceberg table that references the external volume. For example:

   Copy code

   ```
   CREATE ICEBERG TABLE rand_table (data string)
     BASE_LOCATION='table'
     EXTERNAL_VOLUME=external_volume
     CATALOG='snowflake';
   ```
5. After the private endpoint has an `"APPROVED"` status, test unloading data from Snowflake to the external volume.

### Use Snowsight

To set up external volume access using private connectivity in Snowsight, follow these steps:

1. Call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system
   function to provision a private endpoint in your Snowflake VNet to enable Snowflake to connect to external AWS cloud
   storage over private connectivity.

   As the following example demonstrates, you must use a wildcard character (`*`) instead of specifying an individual AWS S3 bucket. Using
   the wildcard does not mean that all S3 buckets are accessed over a private connection. Only buckets referenced by an external volume that
   has the USE\_PRIVATELINK\_ENDPOINT parameter enabled can be accessed via the endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
    'com.amazonaws.us-west-2.s3',
    '*.s3.us-west-2.amazonaws.com');
   ```

   This function binds the private endpoint to the hostname, which enables the external volume to use the private endpoint to connect
   to the storage location, as long as AWS PrivateLink is enabled on the object.
2. Call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity.

   You can continue with the next steps while waiting for the `"APPROVED"` status.
3. Follow the steps to
   [create an external volume for S3 by using Snowsight](/user-guide/tables-iceberg-configure-external-volume-s3#label-tables-iceberg-configure-external-volume-s3-snowsight) and enable private
   connectivity when you configure the external volume.

   Important

   To enable private connectivity, on the **Configure external volume** page, from the **Connectivity** field, you must select
   **Private (Azure Private Endpoint)**.
4. Use the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command to create an Iceberg table that references the external volume. For example:

   Copy code

   ```
   CREATE ICEBERG TABLE rand_table (data string)
     BASE_LOCATION='table'
     EXTERNAL_VOLUME=external_volume
     CATALOG='snowflake';
   ```
5. After the private endpoint has an `"APPROVED"` status, test unloading data from Snowflake to the external volume.

## Deprovision an endpoint

If you no longer need the private connectivity endpoint for the external volume, unset the
`USE_PRIVATELINK_ENDPOINT` property on the external volume, and then call the
[SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.
