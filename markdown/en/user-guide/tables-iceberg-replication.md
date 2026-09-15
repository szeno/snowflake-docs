# Configure replication for Snowflake-managed Apache Iceberg™ tables

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Replication of Snowflake-managed Iceberg tables to a replication group is available to all accounts.
- Replication of Snowflake-managed Iceberg tables to a failover group requires Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

With this feature, you can replicate [Snowflake-managed Apache Iceberg™ tables](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog), including dynamic Iceberg tables, from a source account to one or more target accounts in the same organization.

Replication for Iceberg tables works similarly to replication for regular Snowflake tables. Snowflake replicates an Iceberg table
when you add its parent database to a failover or replication group.

However, Snowflake-managed Iceberg tables rely on external volumes, which are account-level objects that require extra configuration to connect
to your external cloud storage. Before you can replicate an Iceberg table, you must configure replication for external volumes.

For details, refer to the [May 2026 BCR bundle](/release-notes/bcr-bundles/2026_05_bundle).

## Enable replication

A user with the ORGADMIN role must enable replication for each source and target account in the organization:

Copy code

```
USE ROLE ORGADMIN;
SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER(
    '<organization_name>.<account_name>',
    'ENABLE_ACCOUNT_DATABASE_REPLICATION',
    'true');
```

For more information, see [Prerequisite: Enable replication for accounts in the organization](/user-guide/account-replication-config#label-enabling-accounts-for-replication).

For more information about replication, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

## Create a replication group or failover group with external volume

When creating a replication group or failover group, you can choose to replicate specific external volumes or all external volumes in your account.

1. To replicate specific external volumes, list them in the `ALLOWED_EXTERNAL_VOLUMES` parameter.

   Copy code

   ```
   CREATE FAILOVER GROUP my_iceberg_fg
     OBJECT_TYPES = EXTERNAL VOLUMES
     ALLOWED_EXTERNAL_VOLUMES = exvol1, exvol2
     ALLOWED_ACCOUNTS = myorg.my_account_1;
   ```
2. To replicate all external volumes in your account, set `ALLOWED_EXTERNAL_VOLUMES = ALL`.

   Copy code

   ```
   CREATE FAILOVER GROUP my_iceberg_fg
     OBJECT_TYPES = EXTERNAL VOLUMES
     ALLOWED_EXTERNAL_VOLUMES = ALL
     ALLOWED_ACCOUNTS = myorg.my_account_1;
   ```

## Replicate an external volume by using a failover group

These steps provide a sample workflow for replicating an external volume and the Iceberg tables that depend on it
to a target account by using a failover group.

Note

If you don’t already have an external volume, you can create one with the storage locations that you want, including a
location *in the same region* as your target account. After configuring storage access for each location,
you can create and replicate an Iceberg table that references the external volume.

To create an external volume, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

1. In the source account, update your external volume to add a storage location *in the same region* as your target account.

   For example:

   Copy code

   ```
   ALTER EXTERNAL VOLUME exvol1
    ADD STORAGE_LOCATION =
    (
   NAME = 'my-s3-us-central-2'
   STORAGE_PROVIDER = 'S3'
   STORAGE_BASE_URL = 's3://my_bucket_us_central-2/'
   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myrole'
   STORAGE_AWS_EXTERNAL_ID = 'iceberg_table_external_id'
    );
   ```

   Important

   If you don’t specify your own `STORAGE_AWS_EXTERNAL_ID` for S3 storage, you must call [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) after you
   add the new storage location to retrieve the Snowflake-generated external ID.
   You need the external ID to configure access to S3 in the next step.

   Snowflake sets this new location as the [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location) for the secondary
   external volume.
2. In the source account, create a Snowflake-managed Iceberg table that uses the external volume that you updated with the additional storage
   location.

   For example:

   Copy code

   ```
   CREATE ICEBERG TABLE my_iceberg_table (amount int)
     CATALOG = 'SNOWFLAKE'
     EXTERNAL_VOLUME = 'exvol1'
     BASE_LOCATION = 'my_iceberg_table';
   ```
3. In the source account, retrieve information about the [Snowflake service principal](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-grant-access-to-storage) for
   your *target account* by following these steps:

   1. Retrieve the name (`account_name`) of your target account by using the [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) command.

      Copy code

      ```
      SHOW REPLICATION ACCOUNTS LIKE 'my_target_account%';
      ```
   2. Call the [SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY](/sql-reference/functions/system_desc_iceberg_access_identity) system function.
      Specify the cloud provider for the target storage location and the name of your target account *exactly* as
      it appears in the `account_name` column of the SHOW REPLICATION ACCOUNTS output.

      For example:

      Copy code

      ```
      SELECT SYSTEM$DESC_ICEBERG_ACCESS_IDENTITY('S3', 'MY_TARGET_ACCOUNT_1');
      ```
4. Configure Snowflake access to the storage location associated with your target account.
   Follow the instructions for your cloud provider, using the information you retrieved for the service principal in the target account:

   - [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3). Use the external ID associated with the storage location for your target account.
   - [Configure an external volume for Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
   - [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure). In the `AZURE_CONSENT_URL_TEMPLATE` returned by
     SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY, replace `your_tenant_id` with the ID for your
     tenant that the storage location belongs to.
5. In the source account, use the [CREATE FAILOVER GROUP](/sql-reference/sql/create-failover-group) command to create a failover group.
   Specify `EXTERNAL VOLUMES` in the `OBJECT_TYPES` list. In the
   `ALLOWED_DATABASES` list, include the database with the Iceberg tables that you want to replicate. In the
   `ALLOWED_EXTERNAL_VOLUMES` list, include the external volumes that provide access to the Iceberg tables that you want to replicate.

   Copy code

   ```
   CREATE FAILOVER GROUP my_iceberg_fg
     OBJECT_TYPES = DATABASES, EXTERNAL VOLUMES
     ALLOWED_DATABASES = my_iceberg_database
     ALLOWED_EXTERNAL_VOLUMES = my_external_volume
     ALLOWED_ACCOUNTS = myorg.my_account_1;
   ```

   Note

   If you receive a SQL parser error, your list of allowed external volumes might be too long. If you receive this error, shorten this
   list in your CREATE FAILOVER GROUP statement, and then use the [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) command to add
   additional allowed external volumes to the failover group. Alternatively, you can set `ALLOWED_EXTERNAL_VOLUMES = ALL` to
   replicate all external volumes in your account. This results in any pre-existing external volumes in your target account
   being dropped and replaced by external volumes from your source account.

   To update an existing group, use the [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group) command to add `EXTERNAL VOLUMES` to the
   `OBJECT_TYPES` list.
   Include any other existing objects in the `OBJECT_TYPES` list to avoid dropping those objects in the target account.

   For example, add `EXTERNAL VOLUMES` to a failover group that already includes `DATABASES`:

   Copy code

   ```
   ALTER FAILOVER GROUP my_iceberg_fg SET
      OBJECT_TYPES = DATABASES, EXTERNAL VOLUMES
      ALLOWED_EXTERNAL_VOLUMES = my_external_volume;
   ```
6. In the target account, create a failover group as a replica of the group in the source account (`my_source_account`):

   Copy code

   ```
   CREATE FAILOVER GROUP my_iceberg_fg
     AS REPLICA OF myorg.my_source_account.my_iceberg_fg;
   ```

   Skip this step if you already have a secondary group that replicates the group in the source account.
7. In the target account, run a refresh command.

   Copy code

   ```
   ALTER FAILOVER GROUP my_iceberg_fg REFRESH;
   ```

   As long as you replicate the database that contains your Snowflake-managed Iceberg table and you’ve
   configured access to your cloud storage for the target account, Snowflake replicates the table in the target account.

   Note

   The refresh operation fails if Snowflake can’t access the storage location configured for the target account.
   If this happens, double-check your access control settings, or try [Verifying storage access](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-storage-verify-storage-access).

## Replicate an external volume by using a replication group

These steps provide a sample workflow for replicating an external volume and the Iceberg tables that depend on it
to a target account by using a replication group.

Note

If you don’t already have an external volume, you can create one with the storage locations that you want, including a
location *in the same region* as your target account. After configuring storage access for each location,
you can create and replicate an Iceberg table that references the external volume.

To create an external volume, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

1. In the source account, update your external volume to add a storage location *in the same region* as your target account.

   For example:

   Copy code

   ```
   ALTER EXTERNAL VOLUME exvol1
    ADD STORAGE_LOCATION =
    (
   NAME = 'my-s3-us-central-2'
   STORAGE_PROVIDER = 'S3'
   STORAGE_BASE_URL = 's3://my_bucket_us_central-2/'
   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myrole'
   STORAGE_AWS_EXTERNAL_ID = 'iceberg_table_external_id'
    );
   ```

   Important

   If you don’t specify your own `STORAGE_AWS_EXTERNAL_ID` for S3 storage, you must call [DESCRIBE EXTERNAL VOLUME](/sql-reference/sql/desc-external-volume) after you
   add the new storage location to retrieve the Snowflake-generated external ID.
   You need the external ID to configure access to S3 in the next step.

   Snowflake sets this new location as the [active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location) for the secondary
   external volume.
2. In the source account, create a Snowflake-managed Iceberg table that uses the external volume that you updated with the additional storage
   location.

   For example:

   Copy code

   ```
   CREATE ICEBERG TABLE my_iceberg_table (amount int)
     CATALOG = 'SNOWFLAKE'
     EXTERNAL_VOLUME = 'exvol1'
     BASE_LOCATION = 'my_iceberg_table';
   ```
3. In the source account, retrieve information about the [Snowflake service principal](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-grant-access-to-storage) for
   your *target account* by following these steps:

   1. Retrieve the name (`account_name`) of your target account by using the [SHOW REPLICATION ACCOUNTS](/sql-reference/sql/show-replication-accounts) command.

      Copy code

      ```
      SHOW REPLICATION ACCOUNTS LIKE 'my_target_account%';
      ```
   2. Call the [SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY](/sql-reference/functions/system_desc_iceberg_access_identity) system function.
      Specify the cloud provider for the target storage location and the name of your target account *exactly* as
      it appears in the `account_name` column of the SHOW REPLICATION ACCOUNTS output.

      For example:

      Copy code

      ```
      SELECT SYSTEM$DESC_ICEBERG_ACCESS_IDENTITY('S3', 'MY_TARGET_ACCOUNT_1');
      ```
4. Configure Snowflake access to the storage location associated with your target account.
   Follow the instructions for your cloud provider, using the information you retrieved for the service principal in the target account:

   - [Configure an external volume for Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3). Use the external ID associated with the storage location for your target account.
   - [Configure an external volume for Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
   - [Configure an external volume for Azure](/user-guide/tables-iceberg-configure-external-volume-azure). In the `AZURE_CONSENT_URL_TEMPLATE` returned by
     SYSTEM$DESC\_ICEBERG\_ACCESS\_IDENTITY, replace `your_tenant_id` with the ID for your
     tenant that the storage location belongs to.
5. In the source account, use the [CREATE REPLICATION GROUP](/sql-reference/sql/create-replication-group) command to create a replication group.
   Specify `EXTERNAL VOLUMES` in the `OBJECT_TYPES` list. In the
   `ALLOWED_DATABASES` list, include the database with the Iceberg table(s) you want to replicate. In the
   `ALLOWED_EXTERNAL_VOLUMES` list, include the external volumes that provide access to the Iceberg table(s) you want to replicate.

   Copy code

   ```
   CREATE REPLICATION GROUP my_iceberg_rg
     OBJECT_TYPES = DATABASES, EXTERNAL VOLUMES
     ALLOWED_DATABASES = my_iceberg_database
     ALLOWED_EXTERNAL_VOLUMES = my_external_volume
     ALLOWED_ACCOUNTS = myorg.my_account_1;
   ```

   Note

   If you receive a SQL parser error, your list of allowed external volumes might be too long. If you receive this error, shorten this
   list in your CREATE REPLICATION GROUP statement, and then use the [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group) command to add
   additional allowed external volumes to the replication group. Alternatively, you can set `ALLOWED_EXTERNAL_VOLUMES = ALL` to
   replicate all external volumes in your account. This results in any pre-existing external volumes in your target account
   being dropped and replaced by external volumes from your source account.

   To update an existing group, use the [ALTER REPLICATION GROUP](/sql-reference/sql/alter-replication-group) command to add `EXTERNAL VOLUMES` to the
   `OBJECT_TYPES` list.
   Include any other existing objects in the `OBJECT_TYPES` list to avoid dropping those objects in the target account.

   For example, add `EXTERNAL VOLUMES` to a replication group that already includes `DATABASES`:

   Copy code

   ```
   ALTER REPLICATION GROUP my_iceberg_rg SET
     OBJECT_TYPES = DATABASES, EXTERNAL VOLUMES
     ALLOWED_EXTERNAL_VOLUMES = my_external_volume;
   ```
6. In the target account, create a replication group as a replica of the group in the source account (`my_source_account`):

   Copy code

   ```
   CREATE REPLICATION GROUP my_iceberg_rg
     AS REPLICA OF myorg.my_source_account.my_iceberg_rg;
   ```

   Skip this step if you already have a secondary group that replicates the group in the source account.
7. In the target account, run a refresh command.

   Copy code

   ```
   ALTER REPLICATION GROUP my_iceberg_rg REFRESH;
   ```

   As long as you replicate the database that contains your Snowflake-managed Iceberg table and you’ve
   configured access to your cloud storage for the target account, Snowflake replicates the table in the target account.

   Note

   The refresh operation fails if Snowflake can’t access the storage location configured for the target account.
   If this happens, double-check your access control settings, or try [Verifying storage access](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-storage-verify-storage-access).

## Considerations and limitations

Consider the following points when you use replication for Iceberg tables:

- Snowflake currently supports replication of Snowflake-managed tables only.
- Replicating converted Iceberg tables isn’t supported. Snowflake skips converted tables during refresh operations.
- For replicated tables, you must configure access to a storage location in the *same region* as the target account.
- If you drop or alter a storage location that is used for replication on the primary external volume, refresh operations might fail.
- Secondary tables in the target account are read-only until you promote the target account to serve as the source account.
- Snowflake maintains the [directory hierarchy](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location)
  of the primary Iceberg table for the secondary table.
- Replication costs apply for this feature. For more information, see [Understanding replication cost](/user-guide/account-replication-cost).
- For considerations about the account objects for replication and failover groups, see [Account objects](/user-guide/account-replication-considerations#label-account-objects).
