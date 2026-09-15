# Tutorial 5: Create a service with a block storage volume mounted

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

## Introduction

This tutorial provides step-by-step instructions for you to create a simple service that uses a block storage volume. You also take a snapshot of the storage volume and explore ways to use the snapshot.

## Create a service

1. Follow [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1) to download code for the sample service, create a Docker image, and upload it to a repository in your Snowflake account.
2. Verify you have the `my_echo_service_image` image in the repository.

   Copy code

   ```
   SHOW IMAGES IN IMAGE REPOSITORY tutorial_db.data_schema.tutorial_repository;
   ```
3. Create a service. When the service runs, the container will have a 10 Gi block volume storage mounted.

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
    - name: block-vol1
      mountPath: /opt/block/path
    readinessProbe:
      port: 8080
      path: /healthcheck
     endpoints:
     - name: echoendpoint
    port: 8080
    public: true
     volumes:
     - name: block-vol1
    source: block
    size: 10Gi
   $$;
   ```

   Note

   This tutorial only shows how to create a service with a block storage volume. The service code
   doesn’t use the volume.
4. To verify that the service is running, execute the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command.

   Copy code

   ```
   DESC SERVICE echo_service;
   ```

   Verify the `status` column shows the service status as RUNNING; if the status is PENDING, it indicates the service is still starting. To investigate why the service is not RUNNING, execute the [SHOW SERVICE CONTAINERS IN SERVICE](/sql-reference/sql/show-service-containers-in-service) command and review the `status` of individual containers:

   Copy code

   ```
   SHOW SERVICE CONTAINERS IN SERVICE echo_service;
   ```

## Take a snapshot

1. Use the [CREATE SNAPSHOT](/sql-reference/sql/create-snapshot) command to take a snapshot of the block storage volume attached to the service
   instance 0. You specify instance 0 because you are running only one service instance.

   Use double-quotes around the name in the VOLUME parameter to match the case of the name in the service specification.

   Copy code

   ```
   CREATE SNAPSHOT my_snapshot
     FROM SERVICE my_service
     VOLUME "block-vol1"
     INSTANCE 0
     COMMENT='new snapshot';
   ```
2. Review the snapshot

   - List snapshots using [SHOW SNAPSHOTS](/sql-reference/sql/show-snapshots).

     Copy code

     ```
     SHOW SNAPSHOTS;
     ```
   - Retrieve information for a specific snapshot using [DESCRIBE SNAPSHOT](/sql-reference/sql/desc-snapshot).

     Copy code

     ```
     DESC SNAPSHOT my_snapshot;
     ```
3. Run the [ALTER SNAPSHOT](/sql-reference/sql/alter-snapshot) command to modify the snapshot.

   Copy code

   ```
   ALTER SNAPSHOT my_snapshot SET comment='updated comment';
   ```

## Use the snapshot

1. You can use the snapshot two ways:

   - **Use snapshot to create a new service:** When creating a new service, you can use the snapshot as the initial content for a block storage volume as shown. The following CREATE SERVICE command creates another service (`new_service`) with a 50 Gi block storage volume. The inline specification includes the snapshot name to use for initializing the block storage volume.

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
         - name: fromsnapshotvol
     mountPath: /opt/block/path
         readinessProbe:
     port: 8080
     path: /healthcheck
       endpoints:
       - name: echoendpoint
         port: 8080
         public: true
       volumes:
       - name: fromsnapshotvol
         source: block
         size: 50Gi
         blockConfig:
     initialContents:
       fromSnapshot: MY_SNAPSHOT
     $$
     min_instances=3
     max_instances=3;
     ```
   - **Restore a snapshot on a storage volume of an existing service:** This example restarts the first service (`my_service`) you created by replacing the original block volume content with the content from the snapshot.

     1. Suspend the service so you can restore the snapshot on the block storage volume.

        Copy code

        ```
        ALTER SERVICE my_service SUSPEND;
        ```
     2. Restore the snapshot on the block storage volume mounted on the container of the
        new\_service instance. You are running only one instance of the Echo Service, so you specify instance ID 0.

        Copy code

        ```
        ALTER SERVICE my_service RESTORE     -- this will auto RESUME the service.
          VOLUME "block-vol1"
          INSTANCES 0
          FROM SNAPSHOT my_snapshot;
        ```
     3. Verify the service status.

        Copy code

        ```
        DESC SERVICE echo_service;
        ```

        The `status` column should show the service status as RUNNING;
2. Use the [DROP SNAPSHOT](/sql-reference/sql/drop-snapshot) command to drop the snapshot.

   Copy code

   ```
   DROP SNAPSHOT my_snapshot;
   ```

## Clean up

Remove the resources you created.

1. Drop the two services you created:

> Copy code
>
> ```
> DROP SERVICE my_service;
> DROP SERVICE new_service;
> ```

1. Follow [Tutorial 1](/developer-guide/snowpark-container-services/tutorials/tutorial-1) steps to clean up other resources created in tutorial 1.

## What’s next?

Now that you’ve completed this tutorial, you can return to [Advanced tutorials](/developer-guide/snowpark-container-services/overview-advanced-tutorials) to explore other topics.
