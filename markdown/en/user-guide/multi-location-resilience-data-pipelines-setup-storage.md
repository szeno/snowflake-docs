# Configure storage locations for multi-location resilience

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical Edition (or higher).
To inquire about upgrading, contact [Snowflake Support](/user-guide/contacting-support).

This is the first task in
[Set up multi-location resilience for data pipelines](/user-guide/multi-location-resilience-data-pipelines-setup). Run it in your
source account, as defined in [How multi-location resilience works](/user-guide/multi-location-resilience-data-pipelines#label-mlsi-how-it-works). In it, you create a
Multi-Location Storage Integration (MLSI) that lists your primary and secondary
storage locations, and you point your external stages at it. Every pipeline
needs this task, including pipelines that load only with `COPY INTO`.

Before you begin, make [the setup decisions](/user-guide/multi-location-resilience-data-pipelines-setup#label-mlsi-setup-decisions).

## Create a Multi-Location Storage Integration (MLSI)

To configure an MLSI, you follow the standard
steps for configuring a storage integration with a few differences noted in
this section.

On AWS, create the IAM policy and IAM role for each bucket before you create the
MLSI, because `STORAGE_LOCATIONS` takes each role’s Amazon Resource Name (ARN). In
[Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration), follow only Step 1 and
Step 2, once for each bucket. Skip that topic’s Step 3, which creates a
single-location storage integration: the following statement replaces it. On
Google Cloud and Azure, you grant access after you create the integration, as
described in the topic for your cloud provider.

An MLSI has one active storage location, and every stage that uses it resolves
its `RELATIVE_URL` against that location’s `STORAGE_BASE_URL`. If your stages read
from more than one bucket or container, create one MLSI for each primary
location, and pair it with that location’s secondary location. For each MLSI,
repeat this section, [Grant access to your primary location](#label-mlsi-grant-primary-storage), and
[Associate the MLSI with your external stages](#label-mlsi-stage-setup), and, in your target account,
[Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage) and [Set the active storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-set-storage).

In your source account, create the MLSI by providing values for each location
in the `STORAGE_LOCATIONS` list. You can mix and match cloud providers for
cross-cloud setups. The following example uses two Amazon S3 locations:

Copy code

```
CREATE STORAGE INTEGRATION my_mlsi
  TYPE = EXTERNAL_STAGE
  STORAGE_LOCATIONS =
  (
    (
      NAME = 'my-s3-us-west-1'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://my-bucket-west'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::12345:role/myrole'
      STORAGE_AWS_EXTERNAL_ID = 'mlsi-external-id'
      ENCRYPTION = ( TYPE = 'AWS_SSE_S3' )
    ),
    (
      NAME = 'my-s3-us-east-1'
      STORAGE_PROVIDER = 'S3'
      STORAGE_BASE_URL = 's3://my-bucket-east'
      STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::67890:role/myrole'
      STORAGE_AWS_EXTERNAL_ID = 'mlsi-external-id'
      ENCRYPTION = ( TYPE = 'AWS_SSE_S3' )
    )
  )
  ENABLED = TRUE
  STORAGE_ALLOWED_LOCATIONS = ('*')
  ACTIVE = 'my-s3-us-west-1';
```

Locations on Azure and Google Cloud have the following form in the
`STORAGE_LOCATIONS` list:

Copy code

```
(
  NAME = 'my-azure-eastus'
  STORAGE_PROVIDER = 'AZURE'
  STORAGE_BASE_URL = 'azure://myaccount.blob.core.windows.net/my-container/'
  AZURE_TENANT_ID = '<tenant_id>'
),
(
  NAME = 'my-gcs-us-central1'
  STORAGE_PROVIDER = 'GCS'
  STORAGE_BASE_URL = 'gcs://my-bucket-central/'
)
```

Where:

- **STORAGE\_LOCATIONS:** Specifies a list of one or more storage locations
  (Amazon S3 bucket, Google Cloud Storage bucket, or Azure container) for the
  storage integration. Each location requires `NAME`, `STORAGE_PROVIDER`, and
  `STORAGE_BASE_URL`. Amazon S3 locations also require `STORAGE_AWS_ROLE_ARN`,
  and Azure locations require `AZURE_TENANT_ID`. A location can also specify
  `ENCRYPTION`, `USE_PRIVATELINK_ENDPOINT` (Amazon S3 and Azure, only for a location on the
  same cloud provider that hosts your Snowflake account), and
  `STORAGE_AWS_EXTERNAL_ID` (Amazon S3). An MLSI doesn’t support
  `STORAGE_AWS_OBJECT_ACL`. For descriptions of these parameters, see
  [Cloud provider parameters](/sql-reference/sql/create-storage-integration#label-create-integration-storage-cloudproviderparams)
  on the [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration) reference page.
- **NAME:** String that specifies the identifier (name) for the storage location.
- **STORAGE\_BASE\_URL:** Specifies the URL of the bucket or container that a
  stage’s `RELATIVE_URL` is appended to, such as `s3://my-bucket-west`,
  `gcs://my-bucket-central`, or a URL that includes a path, such as
  `s3://my-bucket-west/data/`. If the URL includes a path, end it with a slash.
- **ENCRYPTION:** Specifies encryption for the storage location. You must specify
  encryption for the storage location at the storage integration level instead
  of at the stage level. Required only for loading from encrypted files; not
  required if the storage location and files are unencrypted. To view the
  encryption types for each cloud provider, see
  [ENCRYPTION](/sql-reference/sql/create-stage#label-create-stage-encryption-parameters) on the
  [CREATE STAGE](/sql-reference/sql/create-stage) reference page.
- **STORAGE\_ALLOWED\_LOCATIONS:** Required. Limits the stages that use this
  integration to the paths that you list. The `CREATE STORAGE INTEGRATION`
  example uses `('*')`, which allows any path in any of the storage locations. To restrict access,
  replace the wildcard with a list of paths relative to `STORAGE_BASE_URL`, such
  as `('my_folder/')`. The same list applies to every location. Snowflake
  matches each path as a literal prefix of a stage’s `RELATIVE_URL`, so either
  start both the path and the `RELATIVE_URL` with a slash, or start neither with
  one. For example, `('my_folder/')` allows
  `RELATIVE_URL = 'my_folder/my_sub_folder/'` but not
  `RELATIVE_URL = '/my_folder/my_sub_folder/'`.
- **STORAGE\_BLOCKED\_LOCATIONS:** Optional, and not shown in the example. Prevents stages that use this integration from accessing the paths that you list. Snowflake also rejects a stage whose `RELATIVE_URL` is a parent of a blocked path, such as a stage at `my_folder/` when `my_folder/private/` is blocked. Paths are relative to `STORAGE_BASE_URL`, apply to every location, and follow the same slash rule as `STORAGE_ALLOWED_LOCATIONS`. If a blocked path starts with a slash and the stage’s `RELATIVE_URL` doesn’t, or the reverse, the path doesn’t block anything.
- **ACTIVE:** Required. Specifies the name of the storage location to set as the active location for the storage integration in the current account. The value
  must match a location’s `NAME` exactly, including case.

## Grant access to your primary location

After you run the statement, grant Snowflake access only to the location that’s
active in your source account. In the `DESCRIBE STORAGE INTEGRATION` output,
each location’s identity values, such as `STORAGE_AWS_IAM_USER_ARN`, are in the
JSON of its `STORAGE_LOCATION_<n>` row. Follow the tab for the cloud provider
that hosts your primary location:

Amazon S3Google CloudAzure

Run `DESCRIBE STORAGE INTEGRATION my_mlsi`, and then follow Step 4 and Step 5 of
[Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration) to update the trust
policy of the IAM role for `my-s3-us-west-1`.

Follow Step 2 and Step 3 of [Configure an integration for Google Cloud Storage](/user-guide/data-load-gcs-config) for your
primary bucket only. Skip that topic’s Step 1 and Step 4, which create a
single-location storage integration and a stage.

Follow “Step 2: Grant Snowflake Access to the Storage Locations” in
[Configure an Azure container for loading data](/user-guide/data-load-azure-config) for your primary container only. Skip
the steps in that topic that create a storage integration and a stage.

Don’t grant access to your secondary location yet. The replicated integration
in your target account uses that account’s cloud identity, which differs from
your source account’s. You can’t look up that identity with `DESCRIBE STORAGE INTEGRATION`
until the first refresh after you add integrations to the failover group. You
grant that identity access in [Grant access to your secondary storage location](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-target-grant-storage).

If your failover group has a replication schedule

Add your integrations to the failover group now, before you create or alter
stages: read the warnings in [Replicate your integrations to the target account](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-replicate-integrations), follow
[Add your integrations to the failover group](/user-guide/multi-location-resilience-data-pipelines-setup-target-account#label-mlsi-add-integrations-to-group), and then return to this topic to continue with [Associate the MLSI with your external stages](#label-mlsi-stage-setup). If you plan to create a Multi-Queue Notification Integration (MQNI), include `NOTIFICATION INTEGRATIONS`. If you add your integrations after you create or alter stages, a scheduled refresh can replicate your stages before their MLSI, and those stages can’t be used in your
target account until they’re replicated again.

## Associate the MLSI with your external stages

Every stage that a protected pipe or `COPY INTO` statement reads from must use
the MLSI. A pipe whose stage still uses a single-location URL can’t find files
after a failover. If you migrate existing pipes when you
[configure notifications](/user-guide/multi-location-resilience-data-pipelines-setup-notifications),
the migration simultaneously moves every pipe that shares a notification
integration, SNS topic, or bucket with a migrated pipe. Before you migrate,
move each of those pipes to an MLSI stage. A `COPY INTO <table>` statement that reads directly from a URL, rather
than from a stage, always reads that URL, so it doesn’t follow the MLSI’s active
location after a failover. Create a stage as described in this section, and change
the statement to read from it.

Create the stage, its pipes, the tables that those pipes and your `COPY INTO`
statements load, and any tasks that run those statements, in a database that
`my_fg` already replicates. To check, run
[SHOW DATABASES IN FAILOVER GROUP](/sql-reference/sql/show-databases-in-failover-group)
in your source account. If you create a new database, add it to the group’s
allowed databases with [ALTER FAILOVER GROUP](/sql-reference/sql/alter-failover-group).

### Create or alter the stage

Snowflake recommends creating a new stage rather than altering an existing one.
Choose the approach that matches your pipelines and stages:

- **New pipelines:** Create a new stage, and then create pipes against it.
- **Existing pipelines that you can take offline:** Alter the existing stage to
  use the MLSI. If the stage now resolves to a location different from its old
  `URL`, Snowflake marks its pipes invalid, and
  [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) reports
  `STOPPED_STAGE_ALTERED`. Recreate each of those pipes by following
  [Change or recreate a pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes). If the stage resolves to the
  same location as before, its pipes keep working and keep their load history.
- **Existing pipelines that you want to move one at a time:** Create a new stage
  whose `RELATIVE_URL` resolves to the same path as the existing stage’s `URL`.
  To find the value, remove your primary location’s `STORAGE_BASE_URL` from the
  start of the existing stage’s `URL`. Then recreate each pipe against the new
  stage by following [Change or recreate a pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes). Pipes that
  you haven’t moved yet keep loading from the existing stage.
- **Stages that only `COPY INTO` statements read:** No pipe needs recreating.
  If you create a new stage, point each statement at it. For a standalone task,
  suspend it, update its statement with
  [ALTER TASK … MODIFY AS](/sql-reference/sql/alter-task), and then resume it.
  For a task in a task graph, suspend the root task instead of the task whose
  statement you’re changing, update that task’s statement, and then resume the
  root task.
- **Existing stages with a directory table:** Create a new stage instead of
  altering the existing one, because directory tables aren’t supported on a
  stage that uses an MLSI.

Recreating a pipe drops its load history, so a later `ALTER PIPE ... REFRESH` can
load files that the original pipe already loaded. If you plan to move pipes onto
an MQNI with [Scenario B](/user-guide/multi-location-resilience-data-pipelines-setup-notifications#label-mlsi-mqni-scenario-b), keep each
recreated pipe’s original
`INTEGRATION` value (Google Cloud and Azure) or `AWS_SNS_TOPIC` value (Amazon
S3), so that the migration finds the pipe.

In your source account, use the `CREATE STAGE` command to associate the
MLSI that you created with one or more external
stages:

Copy code

```
CREATE STAGE my_db.my_schema.my_ext_stage
  RELATIVE_URL = 'my_folder/my_sub_folder/'
  STORAGE_INTEGRATION = my_mlsi;
```

Where:

- **RELATIVE\_URL:** The relative path to your external stage location from the
  storage location defined in your storage integration. A stage that uses an
  MLSI requires `RELATIVE_URL` instead of `URL`, and `RELATIVE_URL` is allowed
  only with an MLSI. A leading slash is optional, but if you set
  `STORAGE_ALLOWED_LOCATIONS` to specific paths or set
  `STORAGE_BLOCKED_LOCATIONS`, use the same style as those paths. A blocked path
  written in the other style doesn’t block anything. The path must
  resolve in both storage locations. For more information, see
  [How paths resolve in each location](#label-mlsi-path-structure).

  This value must be a literal path. Specifying a pattern or wildcard isn’t
  supported. To specify access to all locations under the `STORAGE_BASE_URL` of
  your storage integration, use an empty string: `RELATIVE_URL = ''`. An empty
  string requires `STORAGE_ALLOWED_LOCATIONS = ('*')` and no
  `STORAGE_BLOCKED_LOCATIONS` on the MLSI.
- **STORAGE\_INTEGRATION:** The name of your MLSI.

If you’re replacing an existing stage, copy its other properties, such as
`FILE_FORMAT`, to the new stage. To see them, run `DESCRIBE STAGE` on the
existing stage. Don’t copy `ENCRYPTION`: set it on the MLSI instead, as described
in [Create a Multi-Location Storage Integration (MLSI)](#label-mlsi-create-mlsi).

To use an existing external stage instead, alter it with
[ALTER STAGE](/sql-reference/sql/alter-stage) to specify `RELATIVE_URL` and
your MLSI:

Copy code

```
ALTER STAGE my_existing_stage SET
  RELATIVE_URL = 'my_folder/my_sub_folder/'
  STORAGE_INTEGRATION = my_mlsi;
```

To roll back this change later, run
`ALTER STAGE my_existing_stage SET STORAGE_INTEGRATION = <original_integration>`.
If the stage used a single-location storage integration before, Snowflake
restores its previous `URL`.

To confirm that a stage resolves to your primary location, run `LIST` on it in
your source account.

### How paths resolve in each location

A stage has one `RELATIVE_URL`. Snowflake appends it to the
`STORAGE_BASE_URL` of whichever storage location is active in the account that
you’re connected to. That’s why both locations need the same folder structure:
the same `RELATIVE_URL` has to be valid in both.

The following table traces the example MLSI and stage from this topic through
both locations:

| Item | Active in the source account | Active in the target account |
| --- | --- | --- |
| Storage location `NAME` | `my-s3-us-west-1` | `my-s3-us-east-1` |
| `STORAGE_BASE_URL` | `s3://my-bucket-west` | `s3://my-bucket-east` |
| Stage `RELATIVE_URL` | `my_folder/my_sub_folder/` | `my_folder/my_sub_folder/` |
| `@my_ext_stage` resolves to | `s3://my-bucket-west/my_folder/my_sub_folder/` | `s3://my-bucket-east/my_folder/my_sub_folder/` |
| A pipe that reads `@my_ext_stage/my_pipe/` reads from | `s3://my-bucket-west/my_folder/my_sub_folder/my_pipe/` | `s3://my-bucket-east/my_folder/my_sub_folder/my_pipe/` |

Expand

Show lessSee more

Bucket names don’t have to match, and the two locations don’t have to be on the
same cloud provider. Everything after the `STORAGE_BASE_URL` must match,
including any subpath that a pipe or `COPY INTO` statement appends to the stage
name.

## Next step

- **If you use Snowpipe auto-ingest:** Continue with
  [Configure notifications for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-notifications).
- **If you load data only with `COPY INTO`:** Skip notifications, and continue
  with
  [Configure your target account for multi-location resilience](/user-guide/multi-location-resilience-data-pipelines-setup-target-account).
