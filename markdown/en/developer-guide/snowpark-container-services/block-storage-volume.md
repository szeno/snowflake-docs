# Using block storage volumes with services

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Snowflake supports these storage volume types for your containerized applications: Snowflake internal stage, local storage, memory storage volumes, and block storage volumes.

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Using block storage volumes with job services is a [preview feature](/release-notes/preview-features).

## Specifying block storage in service specification

To create a service (including job service) that uses block storage, you provide the necessary configuration in the service specification as follows:

### Step 1: Define a block storage volume

Specify the `spec.volumes` field to define the block storage volumes to create.

Copy code

```
spec:
  containers:
  ...
  volumes:
    - name: <name>
      source: block
      size: <size-in-Gi>
      blockConfig:                             # optional
        initialContents:
          fromSnapshot: <snapshot-name>
        iops: <number-of-operations>
        throughput: <MiB-per-second>
        encryption: SNOWFLAKE_SSE | SNOWFLAKE_FULL
```

The following fields are required:

- `name`: Name of the volume.
- `source`: Type of the volume. For block storage volume, the value
  is `block`.
- `size`: Storage capacity of the block storage volume measured in bytes.
  The value must always be an integer, specified using the Gi unit suffix. For example, `5Gi` means `5*1024*1024*1024`
  bytes. The size value ranges for cloud providers:
  - `1Gi` to `65536Gi` for AWS.
  - `1Gi` to `16384Gi` for Azure.
  - `4Gi` to `16384Gi` for Google Cloud.

The following are optional fields:

- `blockConfig.initialContents.fromSnapshot`: Specifies a previously taken snapshot of another volume to initialize the block volume.
  The snapshot name can be a [fully qualified object identifier](/sql-reference/name-resolution), such as
  `TUTORIAL_DB.DATA_SCHEMA.MY_SNAPSHOT`. Also, the snapshot name is resolved relative to the database and the schema of the service.
  For example, if you created your service in `TUTORIAL_DB.DATA_SCHEMA`, then `fromSnapshot: MY_SNAPSHOT` is equivalent to
  `fromSnapshot: TUTORIAL_DB.DATA_SCHEMA.MY_SNAPSHOT`.

  Note the following:

  - The snapshot must be in the CREATED state before it can be used to create a volume or the service creation will fail.
  - The encryption type of the snapshot must match that of the volume being created.

  Use the [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot) command to get the snapshot’s status and encryption type.
- `blockConfig.iops`: Specifies the supported peak number of input/output operations per second. Note that the data size per operation is capped at 256 KiB.

  - For AWS: The supported range is 3000-80000, with a default of 3000.
  - For Azure: The supported range is 3000-80000, with a default of 3000.
  - For Google Cloud:
    - Google Cloud CPU instances: The supported range is 2000-160000, with the following defaults:

      - 2000 IOPS for a 4 Gi disk size
      - 2500 IOPS for a 5 Gi disk size
      - 3000 IOPS for all other disk sizes
    - Google Cloud GPU instances: Snowflake recommends specifying only throughput. `blockConfig.iops` must be 16 \* `blockConfig.throughput` for GPU instances in Google Cloud.
- `blockConfig.throughput`: Specifies the peak throughput, in MiB/second, to provision for the volume.

  - For AWS: The supported range is 125 - 2000, with a default of 125.
  - For Azure: The supported range is 125 - 1200, with a default of 125.
  - For Google Cloud:
    - Google Cloud CPU instances: The supported range is 140 - 2400, with the default of 140.
    - Google Cloud GPU instances: The supported range is 400 - 1,200,000, with the default of 400, but not less than 0.12 per GB of volume size.
- `blockConfig.encryption`: Specify encryption type of the volume: `SNOWFLAKE_SSE` or `SNOWFLAKE_FULL`. For more information, see [Encryption support](#label-spcs-block-storage-encryption-support).

### Step 2: Specify where to mount the volume in the container

After you define a block storage volume by adding the `spec.volumes` field, use the `spec.containers.volumeMounts` field to describe where to mount the volume in your application containers, as shown in the following example:

Copy code

```
spec:
  containers:
  - name: ...
    image: ...
    volumeMounts:
    - name: <volume-name>
      mountPath: <absolute_directory_path>
```

### Example

- Create a service with a block storage volume with size 10Gi. The volume is mounted at path `/opt/block/path` in the main container.

  Copy code

  ```
  CREATE SERVICE my_service
  IN COMPUTE POOL tutorial_compute_pool
  FROM SPECIFICATION $$
  spec:
    containers:
    - name: echo
   image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest
   volumeMounts:
   - name: block-vol
     mountPath: /opt/block/path
   readinessProbe:
     port: 8080
     path: /healthcheck
    endpoints:
    - name: echoendpoint
   port: 8080
   public: true
    volumes:
    - name: block-vol
   source: block
   size: 10Gi
  $$;
  ```
- Create a service with a block storage volume initialized from a snapshot.

  Copy code

  ```
  CREATE SERVICE new_service
    IN COMPUTE POOL tutorial_compute_pool
    FROM SPECIFICATION $$
  spec:
    containers:
    - name: echo
   image: /tutorial_db/data_schema/tutorial_repository/my_echo_service_image:tutorial
   volumeMounts:
   - name: vol-from-snapshot
     mountPath: /opt/block/path
   readinessProbe:
     port: 8080
     path: /healthcheck
    endpoints:
    - name: echoendpoint
   port: 8080
   public: true
    volumes:
    - name: vol-from-snapshot
   source: block
   size: 50Gi
   blockConfig:
     initialContents:
       fromSnapshot: BACKUP_DB.SNAPSHOTS.MY_SNAPSHOT
  $$
  ```

For an example with step-by-step instructions, see [Tutorial 5: Create a service with a block storage volume mounted](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-5-block-storage). This tutorial shows you how to create a service with a block storage volume mounted.

### About IOPS and throughput

If your service IO performance is not meeting your expectations and the service is affected by block volume IO or throughput, you might consider
increasing IOPS or throughput. In the current implementation, any such changes require you to recreate the service.

You can review these [available platform metrics](/developer-guide/snowpark-container-services/monitoring-services#label-spcs-available-platform-metrics) to identify if your service is bottlenecked on block storage:

> - `container.cpu.usage`
> - `volume.read.iops`
> - `volume.write.iops`
> - `volume.read.throughput`
> - `volume.write.throughput`

Depending on the cloud provider the following considerations apply:

- Configuring iops and throughput for AWS:

  - The maximum IOPS that can be configured is 500 IOPS per GiB of volume size, to a maximum of 80,000 IOPS. For example, the
    maximum IOPS of a 10 GiB volume can be 500 \* 10 = 5000. Accordingly, note that the maximum IOPS of 80,000 can only be configured if your volume is 160 GiB or larger.
  - The maximum throughput that can be configured is 1 MiB/second for every 4 IOPS, to a maximum of 2000 MiBs/second.
    For example, with the default 3000 IOPS you can configure throughput up to 750 MiB/second (3000/4=750).
- Configuring iops and throughput for Azure:

  - After a volume size of 6 GB, the supported number of IOPS increase by 500 for each GB beyond 6 GB (disks-types). The maximum IOPS of a 10GB volume can be 500 \* 4 + 3000 = 5000. Accordingly, note that the maximum IOPS of 80,000 can only be configured if your volume is 160 GiB or larger.
  - After 6 GB, the maximum throughput that can be configured is 0.25 MiB/second for every IOPS, to a maximum of 1200 MiBs/second. For example, with the default 3000 IOPS you can configure throughput up to 750 MiB/second (3000\*0.25=750).
- Configuring iops and throughput for Google Cloud:

  - For CPU instances:

    - IOPS are configurable up to 500 IOPS per Gi of volume size, with a maximum of 160,000 IOPS. For example, a 10 Gi volume can achieve a maximum of 5,000 IOPS (500 IOPS \* 10 Gi). To reach the maximum of 160,000 IOPS, a volume size of 320 Gi or larger is required.
    - A maximum throughput of 2400 MiB/second can be configured, with a rate of 1 MiB/second for every 4 IOPS. For example, 3000 IOPS enables up to 750 MiB/second throughput (3000 / 4 = 750).
  - For GPU instances:

    - IOPS cannot be set independent of throughput; IOPS is calculated as 16 multiplied by the throughput value. Therefore, specifying throughput automatically determines the IOPS. Configuring IOPS is not advised for disks used with GPU instances.
    - You must configure a minimum throughput. It must be at least 400 MiB/s, or 0.12 MiB/s for every GiB of volume size, whichever is higher.
    - The configurable throughput rate is 1600 MiB/s per GiB of volume size, subject to a maximum of 1,200,000 MiB/s. As an example, a 10 GiB volume can achieve a maximum throughput of 16,000 MiB/s (1600 \* 10). Note that the upper limit of 1,200,000 MiB/s is only attainable with volumes of 750 GiB or greater.

### Snapshot on Delete

Any of the following commands result in deletion of block volume associated with the service:

- DROP SERVICE <service-name> FORCE
- ALTER COMPUTE POOL <compute-pool-name> STOP ALL
- ALTER SERVICE <service-name> RESTORE VOLUME <volume-name> FROM SNAPSHOT

The `snapshotOnDelete` option defaults to true for services and false for jobs. When the value is true, Snowflake takes a snapshot of the volume before deletion, to protect you from accidental data loss. You add this option in the service specification as part of the `blockConfig` configuration.

Unlike other snapshots, these snapshots are automatically deleted after a period of time. The snapshot retention period defaults to 7 days and can be configured using the `snapshotDeleteAfter` field.

Snowflake assigns a snapshot name in this format: `SYS_BACKUP_ON_DELETE<string>_<timestamp>`.

## Access control requirements

If you want to use an existing snapshot (`fromSnapshot` is in the specification) to initialize the volume, the service’s owner role must have the USAGE privilege on the snapshot.

The service’s owner role must also have the USAGE privilege on the database and schema that contain the snapshot.

## Managing snapshots

You can take snapshots of your block storage volume and later use the backup as follows:

- Use the snapshot backup to restore an existing block storage volume.
- Use the snapshot backup as seed data to initialize a new block storage volume when creating a new service.

You should ensure all your updates are flushed to the disk before you take the snapshot.

Snowflake provides the following commands to create and manage snapshots:

- [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot)
- [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot)
- [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot)
- [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots)
- [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot)

In addition, to restore a snapshot on an existing
block storage volume, you can execute the
[ALTER SERVICE … RESTORE VOLUME](/sql-reference/sql/alter-service) command. Note that you need to suspend the service before you can restore a snapshot. After restoring a volume, the service is automatically resumed.

## Block storage costs

For more information, see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

When a block storage volume is used with a job service, Snowflake stops charging block storage costs after the job service is either dropped by the user or cleaned up by Snowflake after completion.

After a snapshot is dropped, you will continue to be billed through the configured [data retention period](/user-guide/data-time-travel#label-time-travel-data-retention-period). The default data retention period is 1 day.

## Encryption support

Block storage volumes and snapshots support the same two encryption modes that are also used for other Snowflake-managed storage:

- **SNOWFLAKE\_SSE:** Server-side encryption only. This is the default configuration for customers who don’t have Tri-Secret-Secure enabled on their Snowflake accounts.

  Snowflake uses the cloud service provider’s (CSP) encryption for block storage volumes and snapshots.
- **SNOWFLAKE\_FULL:** On-host and server-side encryption. This is the default configuration for customers who have Tri-Secret-Secure enabled on their Snowflake accounts.

  Data is first encrypted at the client (Snowpark Container Services host) before being sent to a CSP for storage. Each volume is encrypted with a unique volume key. The same key is used for encrypting snapshots that you create from that volume.

  Because Snowflake performs additional encryption of data, there is a performance and resource usage impact associated with using `SNOWFLAKE_FULL` volumes. Snowflake uses the encryption mechanisms provided by the Linux kernel, so the effect should not be significant. Any performance impact is likely workload-specific, so we recommend that you identify service or job bottlenecks, increase volume throughput, or provide a more powerful server.

  Key rotation or rekeying isn’t supported for block storage volumes and snapshots in Snowflake. To change a volume’s encryption key, create a new volume, and copy the data through the snapshot.

  For customers who have Tri-Secret Secure enabled on their accounts, note that when the access to a customer managed key is revoked, the volume data remains available for currently running services using the volume. We recommend that you shut down these services when you revoke access to the customer managed key so that data is not available. Also, after you revoke the key, the services with encrypted volumes cannot start.

Volume snapshots retain the encryption type of their source volume. For example, a snapshot of a `SNOWFLAKE_SSE` volume also uses `SNOWFLAKE_SSE` encryption. When a snapshot is used as the initial content of a volume or with the [ALTER SERVICE … RESTORE VOLUME](/sql-reference/sql/alter-service) command, its encryption type must match the volume’s encryption type. Otherwise, the command fails.

You can require the SNOWFLAKE\_FULL encryption type for all Snowpark Container Services
block-storage volumes and snapshots in the account by setting
the [ENABLE\_SPCS\_BLOCK\_STORAGE\_SNOWFLAKE\_FULL\_ENCRYPTION\_ENFORCEMENT](/sql-reference/parameters#label-enable-spcs-block-storage-snowflake-full-encryption-enforcement) parameter to TRUE for the account.

After this parameter is enabled, creation of block-storage volumes and snapshot with the SNOWFLAKE\_SSE encryption type isn’t permitted.

## Example

For an example, see
[Tutorial](/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-5-block-storage). The tutorial provides step-by-step instructions to create a service with a block storage volume mounted.

## Guidelines and limitations

The following restrictions apply on services that use block storage volumes:

- General limitations. If you encounter any issues with these limitations, contact your account representative.

  - The maximum number of block storage volumes per service is 3.
  - The maximum number of block storage volumes per Snowflake account is 100.
  - The following table lists the maximum number of block storage volumes that can be mounted per compute pool node depending on the instance type of the node. Snowflake ensures that service instances using block storage volumes are placed in accordance with these limits. This might result in services in the PENDING state waiting for additional resources.

    | Instance family | AWS limit | Azure limit | GCP limit |
    | --- | --- | --- | --- |
    | CPU\_X64\_XS | 22 | 3 | 14 |
    | CPU\_X64\_S | 22 | 8 | 14 |
    | CPU\_X64\_M | 22 | 16 | 14 |
    | CPU\_X64\_SL | 27 | 31 | 14 |
    | CPU\_X64\_L | 22 | 32 | 14 |
    | HIGHMEM\_X64\_S | 22 | 16 | 14 |
    | HIGHMEM\_X64\_M | 22 | 32 | 14 |
    | HIGHMEM\_X64\_SL | n/a | 32 | 14 |
    | HIGHMEM\_X64\_L | 22 | n/a | n/a |
    | GPU\_NV\_S (AWS only) | 22 | n/a | n/a |
    | GPU\_NV\_M (AWS only) | 21 | n/a | n/a |
    | GPU\_NV\_L (AWS only) | 14 | n/a | n/a |
    | GPU\_NV\_XS (Azure only) | n/a | 8 | n/a |
    | GPU\_NV\_SM (Azure only) | n/a | 32 | n/a |
    | GPU\_NV\_2M (Azure only) | n/a | 32 | n/a |
    | GPU\_NV\_3M (Azure only) | n/a | 16 | n/a |
    | GPU\_NV\_SL (Azure only) | n/a | 32 | n/a |
    | GPU\_GCP\_NV\_L4\_1\_24G (Google Cloud only) | n/a | n/a | 14 |
    | GPU\_GCP\_NV\_L4\_4\_24G (Google Cloud only) | n/a | n/a | 14 |
    | GPU\_GCP\_NV\_A100\_8\_40G (Google Cloud only) | n/a | n/a | 14 |

    Expand

    Show lessSee more
  - The maximum number of snapshots allowed per Snowflake account is 100.
- The service using block storage volumes must have the same minimum and maximum number of instances.
- After the service is created, the following apply:

  - You can’t change the number of service instances using the ALTER SERVICE … SET … command when a service is using block storage volumes.
  - You can’t change the `size`, `iops`, `throughput`, or `encryption` fields of block storage volumes.
  - No new block storage volumes can be added, and no existing block storage volumes can be removed.
  - Block storage volumes are preserved if a service is upgraded, or suspended and resumed. When a service is suspended, you continue to pay for the volume because it is preserved. After you upgrade or resume a service, Snowflake attaches each block storage volume to the same service instance ID as before.
  - Block storage volumes are deleted if the service is dropped. To preserve data in the volumes, [take snapshots](#label-snowpark-containers-block-storage-manage-snapshots) of the volumes. You can use the snapshots later to initialize new volumes.
