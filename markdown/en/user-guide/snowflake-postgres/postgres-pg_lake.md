# pg\_lake

pg\_lake is a Postgres extension that enables selective data movement between Postgres and object storage
formats like Parquet and Iceberg. With pg\_lake, you can create Iceberg tables directly in Postgres,
sync data to Snowflake, and exchange files between Snowflake Postgres and Snowflake.

Snowflake Postgres supports three primary patterns for data movement with pg\_lake, each using a different integration type.

- **Shared Iceberg**: Postgres writes Iceberg tables and Snowflake reads them through
  a catalog integration. Storage is managed automatically. No external cloud storage is needed.
- **Stages**: A managed storage area that enables bidirectional file exchange between Snowflake
  Postgres and Snowflake through Snowflake stages.
- **[Customer-managed cloud storage](#label-pg-lake-customer-cloud)**: You provide your own S3
  bucket or Azure Blob Storage container and configure access through a storage integration.
  Postgres can write files and Iceberg tables to this location.

| Pattern | Integration type | Writes | Reads | File formats |
| --- | --- | --- | --- | --- |
| [Shared Iceberg](#label-pg-lake-managed-iceberg) | Catalog integration | PG → SF | SF only | Parquet (Iceberg tables) |
| [Stages](#label-pg-lake-stages) | Postgres internal storage integration | PG → SF, SF → PG | PG and SF | Parquet, CSV, JSON, and other formats supported by pg\_lake |
| [Customer-managed cloud storage](#label-pg-lake-customer-cloud) | Postgres external storage integration | PG → SF, SF → PG | PG and SF | Parquet, CSV, JSON, and other formats supported by pg\_lake |

Expand

Show lessSee more

## Instance requirements

Data movement with pg\_lake requires a STANDARD or HIGH MEMORY instance tier.
BURSTABLE instances aren’t supported.

Warning

Do not downgrade a Postgres instance using pg\_lake from a higher tier to BURSTABLE if data movement is
still configured. If you do downgrade an instance, you will need to remove the tables in object storage first. Downgrading without cleanup may result in loss of data stored in object storage.

## Shared Iceberg

With shared Iceberg, Postgres acts as the Iceberg catalog and Snowflake reads the tables
through a catalog integration. Storage is handled by Snowflake, so you don’t need to configure
a cloud storage bucket, IAM roles, or storage integrations. You also don’t need to create an external volume:
Snowflake Postgres catalog integrations use
[vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)
to access table data and metadata automatically.

This is the simplest way to make Postgres data available in Snowflake for analytics.

Considerations:

- Tables created through a Snowflake Postgres catalog integration are read-only in Snowflake.
- Auto-refresh uses metadata polling. Change notifications aren’t supported.
- `ACCESS_DELEGATION_MODE` must be set to `VENDED_CREDENTIALS`. The
  `EXTERNAL_VOLUME_CREDENTIALS` mode isn’t supported.
- Snowflake handles authentication with the Postgres instance automatically. You don’t need to
  specify `REST_AUTHENTICATION`.

### Requirements

The role that creates the catalog integration must have `CREATE INTEGRATION` on the account and
`USAGE` on the Postgres instance. For full access control details, see
[CREATE CATALOG INTEGRATION (Snowflake Postgres)](/sql-reference/sql/create-catalog-integration-snowflake-postgres).

### Set up shared Iceberg

1. Connect to your Postgres instance and enable the pg\_lake extension:

   Copy code

   ```
   CREATE EXTENSION pg_lake CASCADE;
   ```
2. Create an Iceberg table in Postgres or copy data to this Iceberg table:

   Copy code

   ```
   CREATE TABLE my_table (
    id INT,
    data TEXT
     ) USING iceberg;
   ```
3. In Snowflake, create a catalog integration that points to your Postgres instance:

   Copy code

   ```
   CREATE OR REPLACE CATALOG INTEGRATION my_postgres_catalog
     CATALOG_SOURCE = SNOWFLAKE_POSTGRES
     TABLE_FORMAT = ICEBERG
     CATALOG_NAMESPACE = 'public'
     REST_CONFIG = (
    POSTGRES_INSTANCE = '{instance_name}'
    CATALOG_NAME = 'postgres'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
     )
     ENABLED = TRUE;
   ```
4. Create an Iceberg table in Snowflake that references the Postgres table:

   Copy code

   ```
   CREATE OR REPLACE ICEBERG TABLE my_iceberg_table
     CATALOG = 'my_postgres_catalog'
     CATALOG_TABLE_NAME = 'my_table';
   ```

   You can optionally specify:

   - `CATALOG_NAMESPACE`: The Postgres schema containing the table. Defaults to the value
     set on the catalog integration.
   - `CATALOG_NAME`: The Postgres database containing the table. Defaults to the value
     set on the catalog integration.
   - `AUTO_REFRESH = TRUE`: Enables automatic metadata refresh by polling.

   You don’t need to specify an `EXTERNAL_VOLUME`.
5. Query the data in Snowflake:

   Copy code

   ```
   SELECT * FROM my_iceberg_table;
   ```

### Catalog-linked databases

Instead of creating individual Iceberg tables, you can create a catalog-linked database that
automatically discovers and syncs tables from your Postgres database:

Copy code

```
CREATE DATABASE my_postgres_db
  LINKED_CATALOG = (
    CATALOG = my_postgres_catalog
    ALLOWED_WRITE_OPERATIONS = NONE
  );
```

Snowflake automatically discovers namespaces and tables from the Postgres database and creates
corresponding schemas and Iceberg tables. `ALLOWED_WRITE_OPERATIONS = NONE` is required because
Postgres-managed Iceberg tables are read-only in Snowflake. For more information, see
[Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

### Access control

To let other roles create Iceberg tables using the catalog integration, grant `USAGE` on the
integration along with the standard Snowflake privileges for creating tables:

Copy code

```
GRANT USAGE ON INTEGRATION my_postgres_catalog TO ROLE analyst_role;
GRANT USAGE ON DATABASE my_db TO ROLE analyst_role;
GRANT USAGE ON SCHEMA my_db.public TO ROLE analyst_role;
GRANT CREATE ICEBERG TABLE ON SCHEMA my_db.public TO ROLE analyst_role;
```

No additional grants on the Postgres instance are required beyond the initial `USAGE` grant
to the catalog integration owner.

### Refresh and auto-refresh

Snowflake reads Iceberg metadata from the Postgres catalog. Because the table is externally managed,
you can refresh the data manually or enable automatic refresh.

To pull the latest data immediately, run a manual refresh:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table REFRESH;
```

To enable continuous automatic refresh:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table SET AUTO_REFRESH = TRUE;
```

You can configure how often Snowflake polls for changes on the catalog integration:

Copy code

```
ALTER CATALOG INTEGRATION my_postgres_catalog SET REFRESH_INTERVAL_SECONDS = 60;
```

For a complete walkthrough, see the guide
[Sync Data from Snowflake Postgres to Snowflake with Iceberg and pg\_lake](https://www.snowflake.com/en/developers/guides/sync-data-from-postgres-to-snowflake-with-iceberg-and-pg-lake/).

### Incremental sync with pg\_incremental

The guide above uses `pg_incremental`, a Postgres extension that tracks a watermark (a sequence
value or timestamp) so that each sync run exports only the rows added since the previous run,
rather than re-exporting the entire table each time. `pg_incremental` depends on `pg_cron`,
which provides the periodic scheduler that drives pipeline execution. Both extensions are
available in Snowflake Postgres. For more information, see [Extensions](/user-guide/snowflake-postgres/postgres-extensions).

Warning

Ensure that there is an index on the column that `pg_incremental` uses as its watermark before creating the
pipeline. Without an index, the pipeline performs a full sequential scan on every run, which
can’t keep up with sustained high-throughput workloads.
BRIN indexes are recommended as they are highly effective in selecting new ranges.

For a sequence pipeline (recommended for append-only event or IoT data):

Copy code

```
CREATE INDEX ON events USING brin (event_id);
```

For a time interval pipeline:

Copy code

```
CREATE INDEX ON events USING brin (event_time);
```

BRIN indexes are very lightweight and particularly effective when rows are inserted in roughly
sequential order, which is typical for time-series and IoT workloads.

## Stages

Postgres stages provide a managed storage area for bidirectional file exchange between Snowflake
Postgres and Snowflake. You can copy files from Postgres to a Snowflake stage, or put files in a
stage from Snowflake and read them from Postgres.

A Snowflake Postgres internal storage integration allows you to read from and write to the managed
storage associated with a Snowflake Postgres instance. This enables seamless data movement
between Snowflake and your Postgres instances using an external stage. For the full SQL syntax, see
[CREATE STORAGE INTEGRATION (Postgres Internal Storage)](/sql-reference/sql/create-storage-integration-postgres-internal).

### Considerations

- **Stage restrictions**: When creating a stage (see [CREATE STAGE](/sql-reference/sql/create-stage))
  that uses a Postgres internal storage integration, the `URL`, `ENCRYPTION`, and `DIRECTORY`
  stage properties are disallowed.
- **Path configuration**: The integration automatically appends a `/files` subpath to the base
  storage location retrieved from the Postgres instance.

### Set up a Postgres stage

1. In Snowflake, create a `POSTGRES_INTERNAL_STORAGE` storage integration that references your
   Postgres instance:

   Copy code

   ```
   CREATE STORAGE INTEGRATION my_pg_stage_integration
     TYPE = POSTGRES_INTERNAL_STORAGE
     POSTGRES_INSTANCE = 'my_postgres_instance';
   ```

   Where:

   - `TYPE = POSTGRES_INTERNAL_STORAGE`: Specifies the integration type for Postgres managed
     storage. Required.
   - `POSTGRES_INSTANCE = '<instance_name>'`: Specifies the name of the Snowflake Postgres
     instance. Required.
2. Create a Snowflake stage that uses the integration. Use the `RELATIVE_URL` property to specify
   a user-chosen path prefix under the Postgres managed storage:

   Copy code

   ```
   CREATE STAGE my_pg_stage
     RELATIVE_URL = '/my_data'
     STORAGE_INTEGRATION = my_pg_stage_integration;
   ```
3. Connect to your Postgres instance and enable the pg\_lake extension:

   Copy code

   ```
   CREATE EXTENSION pg_lake CASCADE;
   ```

You can now exchange files between Postgres and Snowflake through the stage. Use standard Snowflake
stage operations (LIST, GET, PUT) on the Snowflake side, and pg\_lake file operations on the
Postgres side.

### Move data between Snowflake and Postgres

You can use the `COPY FILES` command to move data between Snowflake stages and your Postgres
managed storage. These examples assume you have already created a separate Snowflake stage
in addition to the Postgres stage created above.

**Snowflake to Postgres (write)**

To move data from an existing Snowflake stage into the Postgres managed storage:

Copy code

```
COPY FILES
  INTO @<postgres_stage>
  FROM @<source_stage>;
```

Where `<source_stage>` refers to a pre-existing Snowflake stage that contains the files you want
to move, and `<postgres_stage>` is the Postgres stage created in the previous step.

On the Postgres side, you can then load the data:

Copy code

```
COPY test FROM '@STAGE/my_data/data*.parquet';
```

Where `@STAGE` is a preconfigured placeholder for the stage location on the Postgres side.

**Postgres to Snowflake (read)**

To move data written by Postgres back into an existing Snowflake stage:

Copy code

```
COPY FILES
  INTO @<destination_stage>
  FROM @<postgres_stage>;
```

Where `<destination_stage>` refers to a pre-existing Snowflake stage where you want to copy
the files, and `<postgres_stage>` is the Postgres stage created earlier.

### Access control for stages

- **Creating the integration**: The role that creates the storage integration must have
  `OWNERSHIP` on the Postgres instance and `CREATE INTEGRATION` on the account.
- **Usage**: To use the integration to create a stage, a role must have the `USAGE` privilege on
  the integration object.
- **Stage privileges**: Users need standard privileges (for example, `READ`, `WRITE`) on the
  stage itself to perform data movement operations.

For example, to grant another role the ability to create stages using the storage integration:

Copy code

```
GRANT USAGE ON INTEGRATION my_pg_stage_integration TO ROLE data_engineer_role;
```

## Customer-managed cloud storage

If you need to use your own S3 bucket or Azure Blob Storage container, you can configure pg\_lake
to read and write files and Iceberg tables to your storage location. Using customer-managed
storage requires two storage integrations:

| Integration type | Purpose |
| --- | --- |
| `POSTGRES_EXTERNAL_STORAGE` | Gives pg\_lake (Postgres side) read/write access to your storage |
| `EXTERNAL_STAGE` | Gives Snowflake SQL access to the same storage location |

Expand

Show lessSee more

Both integrations can share the same IAM role (S3) or storage container permissions (Azure),
but both must be granted access explicitly.

Jump to setup instructions: [Amazon S3](#label-pg-lake-customer-s3) | [Azure Blob Storage](#label-pg-lake-customer-azure)

### Prerequisites

Before configuring customer-managed cloud storage for pg\_lake, ensure that you have:

- A [Snowflake Postgres instance](/user-guide/snowflake-postgres/postgres-create-instance) with
  pg\_lake support.
- Privileges to create storage integrations in Snowflake (requires ACCOUNTADMIN role or a role
  with the CREATE INTEGRATION privilege on the account).
- A storage container or bucket in the same region as your Snowflake account. To determine your
  Snowflake account region, execute the following query in Snowflake (not on your Postgres
  instance):

  Copy code

  ```
  SELECT CURRENT_REGION();
  ```

**For S3:**

- An active AWS account with permissions to create and manage S3 buckets and IAM roles.
- Familiarity with [AWS IAM roles and policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html).

**For Azure Blob Storage:**

- An active Azure account with permissions to create storage accounts and containers, and to
  assign Azure RBAC roles.
- Your Azure tenant ID. To find it, sign in to the Azure portal, select **Microsoft Entra ID**,
  then **Properties**. The tenant ID appears in the **Tenant ID** field.

### Set up S3 storage

#### Create an S3 bucket

If you don’t already have one, create an S3 bucket in the same AWS region as your Snowflake account.
For example, if your Snowflake account is in `us-west-2`, create the S3 bucket in the
`us-west-2` region.

See the AWS documentation for instructions on [creating an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html).

#### Create an IAM policy for S3 access

Create an IAM policy that grants the necessary permissions for pg\_lake to read from and write to your S3 bucket:

1. Sign in to the AWS Management Console and navigate to the IAM service.
2. From the left-hand navigation pane, select **Account settings**.
3. Under **Security Token Service (STS)** in the Endpoints list, find the Snowflake region where
   your account is located. If the STS status is inactive, move the toggle to **Active**.
   For more information, see [Activating and deactivating AWS STS in an AWS region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html).
4. From the left-hand navigation pane, select **Policies**, then choose **Create policy**.
5. For **Policy editor**, select **JSON**.
6. Add a policy document that allows Snowflake to access the S3 bucket and folder. Replace
   `bucket_name` and `prefix` with your actual bucket name and folder path prefix:

   Copy code

   ```
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion"
            ],
            "Resource": "arn:aws:s3:::bucket_name/prefix/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::bucket_name",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "prefix/*"
                    ]
                }
            }
        }
    ]
   }
   ```

   This policy provides permissions to:

   - Read, write, and delete objects in the specified S3 path
   - List bucket contents and retrieve bucket location
   - Support pg\_lake’s ability to create and manage Iceberg tables
7. Choose **Next**.
8. Enter a policy name (for example, `snowflake_pg_lake_access`) and an optional description.
9. Choose **Create policy**.

#### Create an IAM role

Create an IAM role that Snowflake will assume to access your S3 bucket.

1. From the left-hand navigation pane in the Identity and Access Management (IAM) Dashboard, select **Roles**.
2. Select **Create role**.
3. Select **AWS account** as the trusted entity type.
4. Select **Another AWS account**.
5. In the **Account ID** field, enter your own AWS account ID temporarily. You will modify the
   trust relationship in a later step to grant access to Snowflake.
6. Select the **Require external ID** option. Enter a placeholder external ID such as `0000`.
   You will update this with the actual external ID generated by Snowflake in a later step. An external ID is used to grant access to your AWS resources (such as S3 buckets) to a third party like Snowflake. For more information, see [How to use an external ID when granting access to your AWS resources to a third party](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).
7. Select **Next**.
8. Search for and select the policy you created in [Create an IAM policy for S3 access](#create-an-iam-policy-for-s3-access).
9. Select **Next**.
10. Enter a name and description for the role (for example, `snowflake_pg_lake_role`), then select
    **Create role**.
11. On the role summary page, locate and record the **Role ARN** value. You will need this when
    creating the storage integration in Snowflake.
12. While on the role summary page, select **Edit** in the summary section and change the
    **Maximum session duration** to `12 hours`. Select **Save changes**. For more
    information, see [Modifying a role maximum session duration (AWS)](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html#id_roles_use_view-role-max-session).

#### Create a storage integration in Snowflake

Create a storage integration object in Snowflake that references the IAM role you created.
For the full command syntax, see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).

Copy code

```
CREATE STORAGE INTEGRATION my_pg_lake_integration
  TYPE = POSTGRES_EXTERNAL_STORAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake_pg_lake_role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-bucket/my-prefix/');
```

Where:

- `my_pg_lake_integration` is the name you choose for the storage integration.
- `TYPE = POSTGRES_EXTERNAL_STORAGE` specifies that this integration is for use with Snowflake Postgres.
- `STORAGE_AWS_ROLE_ARN` is the Role ARN you recorded in [Create an IAM role](#create-an-iam-role).
- `STORAGE_ALLOWED_LOCATIONS` specifies the S3 bucket and path prefix. Replace `my-bucket` and
  `my-prefix` with the bucket name and folder path you created in
  [Create an S3 bucket](#create-an-s3-bucket). Note that only one location is allowed for Postgres
  storage integrations.

#### Retrieve the Snowflake IAM user ARN and external ID

After creating the storage integration, use the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command
to retrieve the AWS IAM user and external ID that Snowflake generated for this integration:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_pg_lake_integration;
```

In the output, locate and record the following values:

- `STORAGE_AWS_IAM_USER_ARN`: The IAM user ARN that Snowflake will use to assume the role
- `STORAGE_AWS_EXTERNAL_ID`: The external ID to use in the trust policy

You will use these values in the next step to configure the IAM role trust policy.

#### Update the IAM role trust policy

Update the trust policy of the IAM role you created in [Create an IAM role](#create-an-iam-role) to allow Snowflake to assume the role:

1. Sign in to the AWS Management Console and navigate to the IAM service.
2. From the left-hand navigation pane, select **Roles**.
3. Select the role you created in [Create an IAM role](#create-an-iam-role).
4. Select the **Trust relationships** tab.
5. Select **Edit trust policy**.
6. Replace the policy document with the following text:

   Copy code

   ```
   {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "<storage_aws_iam_user_arn>"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "<storage_aws_external_id>"
                }
            }
        }
    ]
   }
   ```

   Replace the placeholder values with the values you recorded in
   [Retrieve the Snowflake IAM user ARN and external ID](#retrieve-the-snowflake-iam-user-arn-and-external-id):

   - Replace `storage_aws_iam_user_arn` with the `STORAGE_AWS_IAM_USER_ARN` value.
     This is a full ARN in the form `arn:aws:iam::<account_id>:user/snowflake-postgres-integration-management`,
     where the username is always the same and only the AWS account ID varies.
   - Replace `storage_aws_external_id` with the `STORAGE_AWS_EXTERNAL_ID` value.
7. Select **Update policy** to save the changes.

### Set up Azure Blob Storage

#### Create an Azure Blob Storage container

If you don’t already have one, create an Azure Blob Storage container in the same Azure region
as your Snowflake account. For example, if your Snowflake account is in `eastus`, create the
container in the `eastus` region.

See the Azure documentation for instructions on
[creating a storage container](https://learn.microsoft.com/azure/storage/blobs/storage-quickstart-blobs-portal).

#### Create a storage integration in Snowflake

Create a storage integration object in Snowflake that references your Azure tenant and container.
For the full command syntax, see [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration).

Copy code

```
CREATE STORAGE INTEGRATION my_pg_lake_integration
  TYPE = POSTGRES_EXTERNAL_STORAGE
  STORAGE_PROVIDER = 'AZURE'
  AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('azure://myaccount.blob.core.windows.net/mycontainer/mypath/');
```

Where:

- `my_pg_lake_integration` is the name you choose for the storage integration.
- `TYPE = POSTGRES_EXTERNAL_STORAGE` specifies that this integration is for use with Snowflake
  Postgres.
- `AZURE_TENANT_ID` is the tenant ID you located in [Prerequisites](#prerequisites).
- `STORAGE_ALLOWED_LOCATIONS` specifies your container and path prefix using the `azure://`
  scheme. Replace `myaccount`, `mycontainer`, and `mypath` with your actual values. Use the
  `blob.core.windows.net` endpoint for all Azure Blob Storage account types, including Azure
  Data Lake Storage Gen2. Note that only one location is allowed for Postgres storage
  integrations.

#### Grant Snowflake access to Azure storage

After creating the storage integration, you must grant Snowflake’s service principal access to
your storage container.

**Step 1: Retrieve the consent URL**

Use the [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) command to retrieve the values you need:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_pg_lake_integration;
```

In the output, locate and record:

- `AZURE_CONSENT_URL`: The URL an Azure admin must visit to grant Snowflake access to your
  tenant.
- `AZURE_MULTI_TENANT_APP_NAME`: The name of the Snowflake service principal registered in
  your tenant after consent is granted. You’ll use the portion of the name **before** the
  underscore when searching for it in the Azure portal.

**Step 2: Grant consent**

1. Open `AZURE_CONSENT_URL` in a browser while signed in as an Azure Active Directory admin for
   your tenant.
2. Review the permissions that Snowflake requests and select **Accept**. This registers the
   Snowflake service principal in your tenant.

**Step 3: Assign the Storage Blob Data Contributor role**

Grant the Snowflake service principal read and write access to your container:

1. Sign in to the Azure portal and navigate to your storage account.
2. Select **Access Control (IAM)**, then **Add role assignment**.
3. Select the **Storage Blob Data Contributor** role and select **Next**.
4. Under **Assign access to**, select **User, group, or service principal**, then **Select
   members**.
5. Search for the Snowflake service principal using the name from `AZURE_MULTI_TENANT_APP_NAME`
   (the portion before the underscore).
6. Select the principal and complete the role assignment.

### Attach the storage integration to your Postgres instance

Attach the storage integration to your Snowflake Postgres instance. When the storage integration
is attached, the storage credentials are automatically synchronized to the Postgres control plane
and made available to pg\_lake:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres_instance
  SET STORAGE_INTEGRATION = my_pg_lake_integration;
```

You can also specify the storage integration when creating a new Postgres instance:

Copy code

```
CREATE POSTGRES INSTANCE my_postgres_instance
  ...
  STORAGE_INTEGRATION = my_pg_lake_integration;
```

To remove a storage integration from a Postgres instance:

Copy code

```
ALTER POSTGRES INSTANCE my_postgres_instance
  UNSET STORAGE_INTEGRATION;
```

### Connect Snowflake to your storage

After attaching the Postgres-side integration, create a second storage integration of type
`EXTERNAL_STAGE` so that Snowflake SQL can read the files and Iceberg tables that pg\_lake writes
to your storage. Both integrations can share the same IAM role (S3) or container permissions
(Azure), but each integration has its own service principal that must be granted access.

#### For Amazon S3

Create an `EXTERNAL_STAGE` integration in Snowflake using the same IAM role as the
`POSTGRES_EXTERNAL_STORAGE` integration:

Copy code

```
CREATE STORAGE INTEGRATION my_snowflake_stage_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::<account-id>:role/<role-name>'
  STORAGE_ALLOWED_LOCATIONS = ('s3://<bucket-name>/<path>/');
```

Retrieve the IAM principal and external ID for this new integration:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_snowflake_stage_integration;
```

Record the values for `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID`, then update
the IAM role’s trust policy to include a second statement for this integration alongside the
existing statement for the `POSTGRES_EXTERNAL_STORAGE` integration:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PostgresIntegration",
      "Effect": "Allow",
      "Principal": { "AWS": "<pg_storage_aws_iam_user_arn>" },
      "Action": "sts:AssumeRole",
      "Condition": { "StringEquals": { "sts:ExternalId": "<pg_storage_aws_external_id>" } }
    },
    {
      "Sid": "SnowflakeIntegration",
      "Effect": "Allow",
      "Principal": { "AWS": "<sf_storage_aws_iam_user_arn>" },
      "Action": "sts:AssumeRole",
      "Condition": { "StringEquals": { "sts:ExternalId": "<sf_storage_aws_external_id>" } }
    }
  ]
}
```

Then create an external stage in Snowflake pointing at the same location:

Copy code

```
CREATE STAGE my_pg_lake_stage
  STORAGE_INTEGRATION = my_snowflake_stage_integration
  URL = 's3://<bucket-name>/<path>/';
```

#### For Azure Blob Storage

Create an `EXTERNAL_STAGE` integration in Snowflake for the same container:

Copy code

```
CREATE STORAGE INTEGRATION my_snowflake_stage_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'AZURE'
  ENABLED = TRUE
  AZURE_TENANT_ID = '<tenant-id>'
  STORAGE_ALLOWED_LOCATIONS = ('azure://<account>.blob.core.windows.net/<container>/<path>/');
```

Retrieve the consent URL and service principal name:

Copy code

```
DESCRIBE STORAGE INTEGRATION my_snowflake_stage_integration;
```

Record the values for `AZURE_CONSENT_URL` and `AZURE_MULTI_TENANT_APP_NAME`, then:

1. Open `AZURE_CONSENT_URL` in a browser and grant consent for the new service principal.
2. In the Azure portal, assign the **Storage Blob Data Contributor** role on your container to
   the service principal named in `AZURE_MULTI_TENANT_APP_NAME`. This is in addition to the
   role assignment already created for the `POSTGRES_EXTERNAL_STORAGE` integration.

Then create an external stage in Snowflake pointing at the same container:

Copy code

```
CREATE STAGE my_pg_lake_stage
  STORAGE_INTEGRATION = my_snowflake_stage_integration
  URL = 'azure://<account>.blob.core.windows.net/<container>/<path>/';
```

You can now query files that pg\_lake writes to your storage directly from Snowflake SQL using
this stage.

### Configure and use pg\_lake

After attaching the storage integration, connect to your Postgres instance and configure pg\_lake.
For a list of available extensions, see [Snowflake Postgres Extensions](/user-guide/snowflake-postgres/postgres-extensions).

1. Create the pg\_lake extension:

   Copy code

   ```
   CREATE EXTENSION pg_lake CASCADE;
   ```
2. Set the default storage location for Iceberg tables. This should match the location specified
   in your storage integration.

   The SET command only applies to the current session. For S3:

   Copy code

   ```
   SET pg_lake_iceberg.default_location_prefix = 's3://my-bucket/my-prefix';
   ```

   For Azure Blob Storage:

   Copy code

   ```
   SET pg_lake_iceberg.default_location_prefix = 'azure://myaccount.blob.core.windows.net/mycontainer/mypath';
   ```

   To set the value for all current and future sessions, use the ALTER DATABASE command instead.
   If you use multiple Postgres databases, make sure to set the storage location for each database:

   Copy code

   ```
   -- Substitute the name of your database and storage URL
   ALTER DATABASE my_database SET pg_lake_iceberg.default_location_prefix = '<storage_url>';
   ```
3. Verify that the storage integration is configured correctly by listing the contents of your
   storage location. For S3:

   Copy code

   ```
   SELECT * FROM lake_file.list('s3://my-bucket/my-prefix/*');
   ```

   For Azure Blob Storage:

   Copy code

   ```
   SELECT * FROM lake_file.list('azure://myaccount.blob.core.windows.net/mycontainer/mypath/*');
   ```

   If the configuration is correct, this query returns a list of files at that location. If the
   storage location is empty, the query returns an empty result set without an error.
4. Verify the end-to-end configuration by creating an Iceberg table, inserting data, and
   querying it back. If this succeeds, pg\_lake can read from and write to your storage location:

   Copy code

   ```
   CREATE TABLE my_table (
     id INT,
     data TEXT
   ) USING iceberg;

   INSERT INTO my_table VALUES (1, 'hello iceberg');

   SELECT * FROM my_table;
   ```

For a complete walkthrough using customer-managed S3 with pg\_lake, see the guide
[Bidirectional Data Pipelines with pg\_lake and Snowflake](https://www.snowflake.com/en/developers/guides/snowflake-postgres-pg-lake-iot/).

### Security considerations

#### S3

- **Use IAM roles**: Snowflake Postgres uses IAM role assumption rather than static credentials,
  providing better security through temporary credentials and automatic credential rotation.
- **Limit IAM permissions**: Grant only the minimum necessary permissions to the S3 bucket paths
  that pg\_lake needs to access. The IAM policy should restrict access to specific bucket prefixes.
- **Monitor external ID**: The external ID in the trust policy ensures that only your Snowflake
  account can assume the IAM role.
- **Review storage integration changes**: Any updates to the storage integration’s
  `STORAGE_AWS_ROLE_ARN` or `STORAGE_ALLOWED_LOCATIONS` are automatically synchronized to the
  Postgres instance.
- **Use bucket policies**: Consider using S3 bucket policies in addition to IAM policies for
  defense in depth.
- **Enable S3 access logging**: Enable access logging on your S3 bucket to monitor and audit
  access patterns.
- **Regional alignment**: Ensure your S3 bucket is in the same AWS region as your Snowflake
  account for optimal performance and to meet data residency requirements.

#### Azure Blob Storage

- **Use RBAC roles**: Snowflake Postgres uses service principal role assignments rather than
  static credentials, providing better security through Azure managed identity.
- **Limit role scope**: Assign the Storage Blob Data Contributor role at the container or path
  level rather than the storage account level to restrict access to only the data pg\_lake needs.
- **One tenant per integration**: A `POSTGRES_EXTERNAL_STORAGE` integration can authenticate to
  only one Azure tenant. All paths in `STORAGE_ALLOWED_LOCATIONS` must belong to storage accounts
  in the same tenant.
- **Review storage integration changes**: Any updates to the integration’s `AZURE_TENANT_ID` or
  `STORAGE_ALLOWED_LOCATIONS` are automatically synchronized to the Postgres instance.
- **Regional alignment**: Ensure your Azure Blob Storage container is in the same Azure region
  as your Snowflake account for optimal performance and to meet data residency requirements.

### Support for spatial types

Geometry and geography columns move from Postgres to Iceberg in the form of “well-known binary” BYTE columns. To work with them using Snowflake spatial functionality, once the data is in Iceberg, use the ST\_GeometryFromWKB or ST\_GeographyFromWKB functions to convert the raw bytes into a Geometry or Geography object Snowflake can use.

Note that if your Postgres Geometry column contains specialized types like CircularString or CurvePolygon, Snowflake will not be able to read them from the Iceberg table, as Snowflake supports Point, LineString, and Polygon only.

## Related information

- [Sync Data from Snowflake Postgres to Snowflake with Iceberg and pg\_lake](https://www.snowflake.com/en/developers/guides/sync-data-from-postgres-to-snowflake-with-iceberg-and-pg-lake/) — Step-by-step developer guide with incremental sync using pg\_incremental
- [Bidirectional Data Movement between SPG and SF with pg\_lake - Internal Stage](https://www.snowflake.com/en/developers/guides/snowflake-postgres-pg-lake-iot-internal-stage/) — End-to-end quickstart using internal stages and pg\_lake
- [Bidirectional Data Movement between SPG and SF with pg\_lake - External Stage](https://www.snowflake.com/en/developers/guides/snowflake-postgres-pg-lake-iot/) — End-to-end quickstart using customer-managed S3, pg\_lake, and Snowflake Cortex for IoT anomaly detection
- [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration) — Similar S3 access workflow to the one described in this topic
- [Apache Iceberg™ tables](/user-guide/tables-iceberg) — Overview of Iceberg table support in Snowflake
- [Create an Apache Iceberg™ table in Snowflake](/user-guide/tables-iceberg-create) — Creating Iceberg tables from different catalog sources
- [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume) — Configuring an external volume for Iceberg tables
- [Configure a catalog integration for files in object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage) — Catalog integration setup for files in object storage
- [pg\_lake extension documentation](https://github.com/Snowflake-Labs/pg_lake)
