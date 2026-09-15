# Private connectivity to external stages for Amazon Web Services

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

This topic provides configuration details to set up outbound private connectivity to an external stage on AWS. The primary difference
between the outbound public connectivity and outbound private connectivity is how you configure the storage integration or stage. For
example, you can specify the `USE_PRIVATELINK_ENDPOINT` property for the storage integration and then reference this storage
integration in the external stage. The external stage inherits the private endpoint configuration from the storage integration.
Subsequently, your connection to the AWS S3 stage goes through the AWS internal network. By configuring your storage
integration and stage to use outbound private connectivity, you add additional security to your data unloading operations by blocking
public access to the storage account.

## Outbound private connectivity costs

You pay for each private connectivity endpoint along with total data processed. For pricing of these items, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

You can explore the cost of these items by filtering on the following service types when querying billing views in the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas:

- OUTBOUND\_PRIVATELINK\_ENDPOINT
- OUTBOUND\_PRIVATELINK\_DATA\_PROCESSED

For example, you can query the [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) view and filter on these service types.

## Considerations

You can configure outbound public connectivity and outbound private connectivity for the same storage account. If you want to do this,
create a dedicated storage integration for outbound public connectivity and specify `USE_PRIVATELINK_ENDPOINT = FALSE`.

## Syntax updates

Storage integration
:   You can specify the `USE_PRIVATELINK_ENDPOINT` property when you create a storage integration that has one or more locations:

    Copy code

    ```
    CREATE OR REPLACE STORAGE INTEGRATION my_int
      ...
      USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
    ```

    You can modify a storage integration and set the `USE_PRIVATELINK_ENDPOINT` property:

    Copy code

    ```
    ALTER STORAGE INTEGRATION my_int
      SET USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
    ```

External stages
:   A stage that references a storage integration that specifies the `USE_PRIVATELINK_ENDPOINT` property inherits the private endpoint
    configuration. As a result, you do not need to specify the `USE_PRIVATELINK_ENDPOINT` property in the stage, and
    you cannot modify the stage to set the `USE_PRIVATELINK_ENDPOINT` property.

    If you are using the stage’s `CREDENTIALS` property instead of referencing a storage integration, you need to specify the
    `USE_PRIVATELINK_ENDPOINT` property when you create or modify the stage.

    Copy code

    ```
    CREATE OR REPLACE STAGE my_sas_private_stage
      URL = '...'
      CREDENTIALS=(AWS_KEY_ID='1a2b3c' AWS_SECRET_KEY='4x5y6z')
      USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }

    ALTER STAGE my_sas_private_stage
      SET USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
    ```

    The [DESCRIBE STAGE](/sql-reference/sql/desc-stage) command includes the `USE_PRIVATELINK_ENDPOINT` property and its value.

## Configure external stage access

These steps are unique to using outbound private connectivity with a storage integration to unload data to an external stage on AWS. You
need to modify the flow if you are using the stage’s `CREDENTIALS` property instead of referencing a storage integration.

1. In Snowflake, call the [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint) system
   function to provision a private connectivity endpoint in your Snowflake VNet to enable Snowflake to connect to your external AWS S3
   storage using private connectivity.

   As the following example demonstrates, you must use a wildcard character (`*`) instead of specifying an individual AWS S3 bucket. Using
   the wildcard does not mean that all S3 buckets are accessed over a private connection. Only buckets referenced by an external stage that
   is configured for private connectivity can be accessed via the VPC endpoint.

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
    'com.amazonaws.us-west-2.s3',
    '*.s3.us-west-2.amazonaws.com');
   ```

   This function binds the private endpoint to the hostname, which enables the storage integration to use the private endpoint to connect
   to the storage location.
2. In Snowflake, call the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) function.

   When the output of the function includes `"status": "APPROVED"`, your connection from Snowflake to your storage account will be
   able to use private connectivity (after the other necessary Snowflake objects are enabled for outbound private connectivity).

   You can continue with the next steps while waiting for the `"APPROVED"` status.
3. Restrict access on the S3 bucket to access over the VPC endpoint only by updating the bucket policy with the following.

   Copy code

   ```
   {
     "Sid": "AccesstospecificVPCEonly",
     "Effect": "Deny",
     "Principal": {
    "AWS": "arn:aws:iam::001234567890:role/myrole"
     },
     "Action": "s3:*",
     "Resource": [
    "arn:aws:s3:::mybucket1",
    "arn:aws:s3:::mybucket1/*"
     ],
     "Condition": {
    "StringNotEquals": {
      "aws:SourceVpce": "vpce-01c31eb5f4a1e817d"
    }
     }
   }
   ```
4. Create a storage integration which specifies both the limited `STORAGE_AWS_ROLE_ARN` role and the `USE_PRIVATELINK_ENDPOINT` property:

   Copy code

   ```
   CREATE OR REPLACE STORAGE INTEGRATION outbound_private_link_int
     TYPE = EXTERNAL_STAGE
     STORAGE_PROVIDER = 'S3'
     STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::001234567890:role/myrole'
     STORAGE_ALLOWED_LOCATIONS = ('s3://mybucket1/path1/')
     USE_PRIVATELINK_ENDPOINT = TRUE
     ENABLED = TRUE;
   ```

   Note

   For information about creating a role for the storage integration, see
   [Configuring a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration).
5. Create an external stage that references the storage integration:

   Copy code

   ```
   CREATE OR REPLACE STAGE my_storage_private_stage
     URL = 's3://mybucket1/path1/'
     STORAGE_INTEGRATION = outbound_private_link_int;
   ```
6. After the private endpoint has an “APPROVED” status, test unloading data from Snowflake to the external stage:

   Copy code

   ```
   COPY INTO @my_storage_private_stage
     FROM mytable
     FILE_FORMAT = (FORMAT_NAME = my_csv_format);
   ```
7. View the result in your AWS stage.

## Deprovision an endpoint

If you no longer need the private connectivity endpoint for the external stage, unset the
`USE_PRIVATELINK_ENDPOINT` property on the stage or storage integration, and then call the
[SYSTEM$DEPROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_deprovision_privatelink_endpoint) system function.
