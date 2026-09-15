# Using Snowflake stage volumes with services

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Snowflake supports [various storage volume types](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-volume-types) for your application containers, including internal stage, local storage, memory storage, and block storage volumes. This section explains how to configure volumes and volume mounts for internal stages. An *internal stage volume* is a volume configured to use a Snowflake stage as persistent storage.

With stage volumes your service can access an internal stage’s objects as if they are files on your file system, simplifying your service code compared to using a Snowflake driver and [GET](/sql-reference/sql/get) and [PUT](/sql-reference/sql/put) SQL commands to access these objects. Stage volumes can also perform better for scenarios with streaming reads or writes of large data files.

If your file system operations can easily be translated to streaming GET and PUT operations, then Stage volumes will work well for your scenario. If your application needs to rename or move files, modify existing files, or perform file system based locking, then stage volume is not a good fit for your workload.

Note

There are currently two implementations of stage volumes; a generally available version and a deprecated version. Snowflake recommends that you use the generally available version for new services and that you migrate your existing applications from the deprecated version.

The stage volume implementation streams file contents directly to and from cloud storage, ensuring that you always get the latest contents. Consider the following points when you use a stage volume:

- A stage volume is optimized for large, sequential reads and writes, providing strong performance for these access patterns. For best results, read and write data in large, contiguous chunks.
- Reads always return the latest data, which lets data sharing occur between services.
- Random writes or file appends aren’t supported. Attempting these operations results in an error. Snowflake recommends that you use [block storage volumes](/developer-guide/snowpark-container-services/block-storage-volume) for these workloads.

## Configure a Snowflake stage as a storage volume in a service specification

To create a service where service containers use a stage volume, you perform two steps to specify the required settings in the service specification:

- Define a stage volume that identifies the Snowflake stage to use as storage volume.
- Specify where to mount the stage volume in your application container.

### Step 1: Define a stage volume

To define a stage volume, add the `spec.volumes` field in the service specification as shown in the following example:

Copy code

```
spec:
  containers:
    ..
  volumes:
  - name: <name>
    source: stage
    stageConfig:
       name: <stage_name>
       metadataCache: <time_period>
       resources:
         requests:
           memory: <amount-of-memory>
           cpu: <cpu-units>
         limits:
           memory: <amount-of-memory>
           cpu: <cpu-units>
```

The following list defines the fields from the example:

- `name`: Provides the name of the volume.
- `source`: Identifies the type of the volume (stage).
- `stageConfig.name`: Identifies the Snowflake internal stage or folder on a stage to mount; for example `@my_stage`, `@my_stage/folder`, or `@my_db.my_schema.my_stage/folder/nestedfolder`. Double quotes must surround this value.

You can include the following optional fields in `stageConfig`:

- `stageConfig.resources` field: The Snowflake component that provides the mounted stage volume requires CPU and memory resources. Use
  this field to specify these CPU and memory requirements, similar to the resource specifications for your application containers. For
  more information, see [`containers.resources` field](/developer-guide/snowpark-container-services/specification-reference#label-spcs-spec-reference-containers-resources-field) fields. If this field isn’t specified, the following default resource settings apply:

  - `resources.requests.cpu: 0`
  - `resources.requests.memory: 0.5Gi`
  - `resources.limits.cpu: 0.5`
  - `resources.limits.memory: 1Gi`

  For most applications with typical data traffic to stage volumes, you don’t need to set this field, because the default resource settings
  should be sufficient. However, if your application performs a high volume of reads and writes, the default settings might lead to performance
  constraints or read/write failures. For more information,
  see [Common guidelines for both implementations of stage volumes](#label-spcs-stage-volume-common-guidelines-both-stage-vol-impl).

  To avoid these problems, check the [CPU and memory metrics](/developer-guide/snowpark-container-services/monitoring-services#label-monitoring-services-platform-metrics) for the container (`stage-mount-v2-sidecar-<stage-volume-name>`). Snowflake adds this container to your service that provides the implementation of the stage volume you configured. This lets you to see exactly what resources your stage volume is using and determine if it is constrained by CPU or memory. Use these metrics to update the CPU and memory limits as needed.
- `stageConfig.metadataCache` field: If your application frequently retrieves file metadata or lists files on a Snowflake stage in a
  loop, and you don’t expect the data to change often, you can enable metadata caching for the Snowflake stage storage volume to significantly
  improve performance. The cache stores this metadata for a specified time period, after which it is cleared. If the application then
  tries to access the metadata, Snowflake refreshes the cache. Use the hours, minutes, and seconds units to specify the `metadataCache`. For example `90s`, `5m`, `1h`, `1h30m`, `1h30m45s`. If not specified, there is no caching.

  Note

  Configure metadata caching only when the data in your Snowflake stage doesn’t change for service lifetime; for example, a service that has read-only workloads that need to work on a static set of data in the stage. Don’t configure metadata caching for workloads where data in your Snowflake stage is updated while the service is running.

The following `spec.volumes` field defines a Snowflake stage volume. The field includes the optional `stageConfig` fields:

Copy code

```
spec:
  containers:
    ..
  volumes:
  - name: <name>
    source: stage
    stageConfig:
      name: <stage_name>
      metadataCache: 1h
      resources:
        requests:
          cpu: 0.35
          memory: 0.4Gi
        limits:
          cpu: 2.0
          memory: 1Gi
```

### Step 2: Specify where to mount the stage volume in the container

After you define a Snowflake stage storage volume by adding the `spec.volumes` field, use the `spec.containers.volumeMounts` field to describe where to mount the stage volume in your application containers, as shown in the following example:

Copy code

```
spec:
  containers:
  - name: ...
    image: ...
    volumeMounts:
    - name: <name>
      mountPath: <absolute_directory_path>
```

The information you provide in this field is consistent across all supported storage volume types and applies to both implementations of stage volumes.

## Example

- Create a service with a stage `mydb.myschema.ai_models_stage` mounted at `/path/to/stage` in the main container.

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
   - name: stage-vol
     mountPath: /path/to/stage
    volumes:
    - name: stage-vol
   source: stage
   stageConfig:
     name: "@mydb.myschema.ai_models_stage"
  $$;
  ```
- Create a service with a stage subpath `mydb.myschema.ai_models_stage/subpath` mounted at `/path/to/stage` in the main container.

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
   - name: stage-vol
     mountPath: /path/to/stage
    volumes:
    - name: stage-vol
   source: stage
   stageConfig:
     name: "@mydb.myschema.ai_models_stage/subpath"
     metadataCache: 1h
     resources:
       requests:
         cpu: 0.35
         memory: 0.4Gi
       limits:
         cpu: 2.0
         memory: 1Gi
  $$;
  ```

## Access control requirements

The service’s owner role is the role that is used to create the service. It is also the role the services use when interacting with Snowflake. This owner role determines the permissions granted to application containers for accessing a mounted stage. The owner role must have the READ privilege on the stage.

If the owner role doesn’t have the WRITE privilege on a stage, the mount for that stage is read-only. That is, the containers can only read the files from the stage. The owner role needs the WRITE privilege on a stage for the stage mount to support both read and write.

## About the deprecated implementation

The deprecated stage-volume implementation uses a shared cache for reads and writes. Although this works well for some scenarios, you can’t control whether data is read from the cache or directly from the stage, which might not be suitable for all applications. Additionally, when you use the cache for reads and writes, this can introduce performance overhead.

### Migrating code from the deprecated implementation

The newer implementation replaces the deprecated implementation, with the following behavioral changes:

- The newer stage-volume implementation streams file contents directly to and from cloud storage, ensuring that you always get the latest contents. This provides predictable behavior and significantly faster throughput. The deprecated stage-volume implementation caches chunks of file data, making it difficult to know if you are reading the latest data.
- Random read performance might be lower with the new implementation because of the removal of caching. However, without a local disk cache, consistency across volumes is improved. File changes are written directly to the backing stage when the file is closed, with no local disk buffering.
- Reads always return the latest data, making this configuration better for sharing data between services.
- Random writes or file appends aren’t supported. Attempting these operations results in an error. Snowflake recommends that you use [block storage volumes](/developer-guide/snowpark-container-services/block-storage-volume) for these workloads.

### Specify a Snowflake stage volume in a service specification (deprecated)

To create a service where service containers use Snowflake stage volume, specify the required settings in the service specification as shown in the following steps:

1. To specify the stage volume, use the `spec.volumes` field as shown in the following example:

   Copy code

   ```
   volumes:
   - name: <name>
     source: <stage_name>
   ```

   The following fields are required:

   - `name`: The name of the volume.
   - `source`: The Snowflake internal stage or folder on the stage to mount; for example `@my_stage`, `@my_stage/folder`. Quotes must surround this value.
2. To describe where to mount the stage volume in your application containers, use the `spec.containers.volumeMounts` field, as shown in the following example:

   Copy code

   ```
   volumeMounts:
   - name: <name>
     mountPath: <absolute_directory_path>
   ```

   The information you provide in this field is consistent across all supported storage volume types and applies to both implementations of stage volumes.

### Example (deprecated)

In the example service specification, the app container mounts an internal stage `@model_stage` by using the deprecated stage volume implementations:

Copy code

```
spec:
  containers:
  - name: app
    image: <image1-name>
    volumeMounts:
    - name: models-legacy
      mountPath: /opt/model-legacy
  volumes:
  - name: models-legacy
    source: "@model_stage"
```

The `volumeMounts` field specifies where inside the container to mount the stage volume. This specification remains the same for both the stage volume implementations.

## Guidelines when using stage volumes

This section provides you with guidelines to follow when you implement application code in which a container uses a Snowflake stage as storage volume.

### Common guidelines for both implementations of stage volumes

- Stage mount is optimized for sequential reads and writes.
- Stage mount I/O operations might have higher latencies than I/O operations on the container’s file system and block storage volumes. You should always check the status code of I/O operations to ensure they succeeded.
- Stage mounts upload file updates asynchronously. Changes to files on a stage mount are only guaranteed to be persisted to the stage after the file descriptor is successfully closed or flushed. There might be a delay before the changes to files on a stage mount become visible to other containers and Snowflake.
- Each directory in a mounted stage should contain fewer than 100,000 files. Expect `readdir` latency to increase with the number of files in the directory.

### Guidelines when using the deprecated version of the stage volume implementation

- Avoid concurrently writing to multiple files within a stage mount.
- Stage mount isn’t a network file system. Don’t use stage mounts for multi-client coordination.
- Don’t open multiple handles to the same file concurrently. Use opened file handles for either read or write operations, but not a mixture of both. To read from a file after writing to it, close the file and then re-open the file before reading.

### Guidelines when using the generally available stage volume implementation

- Concurrent writes to the same file from multiple stage mounts — same stage volume mounted on different containers — aren’t recommended.
- The absence of a local disk cache improves consistency across mounts. File changes are flushed directly to the backing stage upon closing the file, with no local disk buffering. Reads always return the latest data, making the new stage mount better for sharing data between services.
- Read and write data in large, contiguous chunks for optimal performance. The performance penalty for small reads and writes when compared to the generally available stage volume implementation, can mitigate the performance gains from the new implementation.

## Limitations when using stage volumes

This section describes limitations you should be aware of when you implement application code in which containers use stage volumes. If you encounter any issues with these limits, contact your account representative.

### Common limitations for both implementations of stage volumes

- You can only mount a stage or a subdirectory in a stage; for example, @my\_stage, `@my_stage/folder`. You can’t mount a single file in a stage; for example, `@my_stage/folder/file`.
- External stages aren’t supported. Only Snowflake internal stages are supported.
- Stage mounts are not fully POSIX compatible file systems. For example:

  - File and directory renames are not atomic.
  - Hard links are not supported.
- The Linux kernel subsystem inode notify (`inotify`) that monitors changes to file systems doesn’t work on stage mounts.

### Limitations when using the deprecated version of the stage volume implementation

- A maximum of 5 stage volumes is allowed per service. For more information, see [spec.volumes](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-volume).
- A maximum of 8 stage volumes per compute pool node are supported. Snowflake manages the stage
  mount per node limit similar to how it manages memory, CPU, and GPU. Launching a new
  service instance can cause Snowflake to launch new nodes when no existing nodes have the
  capacity to support the requested stage mounts.
- The stage volume capabilities vary depending on the cloud platform for your Snowflake account:

  - Accounts on AWS support internal stages with both SNOWFLAKE\_FULL and SNOWFLAKE\_SSE stage encryption. For more information, see [Internal stage parameters](/sql-reference/sql/create-stage#label-create-stage-internalstageparams).
  - Accounts on Azure currently support internal stages with SNOWFLAKE\_SSE encryption. When you run [CREATE STAGE](/sql-reference/sql/create-stage), use the ENCRYPTION parameter to specify the encryption type: `CREATE STAGE my_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');`
  - Accounts on Google Cloud aren’t supported.
- Concurrent writes to the same file from multiple stage mounts — that is, the same stage volume mounted on different containers — aren’t supported.

### Limitations when using the generally available version of the stage volume implementation

- Random writes, and file appends aren’t supported.
- Each stage that is mounted requires 512 MB memory per stage. This means that there is
  a limitation on the number of stage volumes that can be used based on instance size. Mounting the
  volume on multiple containers doesn’t increase memory consumption.
- A maximum of 20 stage volumes are allowed per service. For more information, see
  [spec.volumes](/developer-guide/snowpark-container-services/specification-reference#label-snowpark-containers-spec-volume).
