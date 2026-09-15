# Workflow: Develop an app with containers

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes the general workflow for creating a Snowflake Native App with Snowpark Container Services.

## Understand Snowpark Container Services and the Snowflake Native App Framework

Before beginning to develop a Snowflake Native App with Snowpark Container Services

1. Ensure that you are familiar with [Snowpark Container Services](/developer-guide/snowpark-container-services/overview)
   and the [Snowflake Native App Framework](/developer-guide/native-apps/native-apps-about).

   The following tutorials are available for these Snowflake products:

   - [Common Setup for Snowpark Container Services Tutorials](/developer-guide/snowpark-container-services/tutorials/common-setup)
   - [Create a Snowpark Container Services service](/developer-guide/snowpark-container-services/tutorials/tutorial-1)
   - [Create a Snowpark Container Services job service](/developer-guide/snowpark-container-services/tutorials/tutorial-2)
   - [Develop an app with the Snowflake Native App Framework](/developer-guide/native-apps/tutorials/getting-started-tutorial)
   - [Create a Snowflake Native App with Snowpark Container Services](/developer-guide/native-apps/tutorials/na-spcs-tutorial)
2. Review [About Snowflake Native Apps with Snowpark Container Services](/developer-guide/native-apps/native-apps-about#label-native-apps-about-na-spcs) to understand how Snowflake Native App with Snowpark Container Services works.
3. Review [Costs associated with apps with containers](/developer-guide/native-apps/container-cost-governance) to understand the
   costs associated with developing, publishing, and using an app with containers.

## Create the containers and services to be managed by an app.

The first step in developing an app with containers is to set up the required containers and services using
[Snowpark Container Services](/developer-guide/snowpark-container-services/overview).

The basic workflow for using Snowpark Container Services is:

1. Create a repository to store container images.

   This repository exists in the provider account and maintains the container images required by the
   app. See [Create an image repository](/developer-guide/native-apps/container-containers#label-native-apps-cont-image-repo)
2. Copy the container images to the image repository.

   After creating the image repository, providers must upload the container images used by the application.
   Snowpark Container Services support using Docker commands to perform the upload.

   See [Upload container images to the image repository](/developer-guide/native-apps/container-containers#label-native-apps-cont-image-docker) for
   more information.
3. Create a service specification file.

   The service specification file is a YAML file used to configure and run services within
   Snowpark Container Services. Snowflake Native App with Snowpark Container Services includes this file within the application package.

   See [Create the service specification file](/developer-guide/native-apps/container-containers#label-native-apps-cont-service-spec) for more information.
4. Configure block storage and snapshots.

   If the services in your app require using block storage, create a `spec.volumes` in your
   service specification file.

   See [Using block storage volumes with services](/developer-guide/snowpark-container-services/block-storage-volume) for more information.
5. Upload the required files to a stage.

   To make the service specification file accessible to the application package,
   providers must upload it to the stage used to store other files required by the application package.

   See [Staging data files from a local file system](/user-guide/data-load-local-file-system-stage) and
   [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui) for more information on uploading files
   to a stage.

   Note

   If you are using the Snowflake CLI, you are not required to upload the files to a stage.

## Develop and publish a Snowflake Native App with Snowpark Container Services

The workflow for developing and publishing an app with containers is similar to the
workflow for any Snowflake Native App. However, within each stage of the workflow there are
differences.

The following is a typical workflow for developing and publishing an app with containers:

1. Create the manifest file for the app.

   The manifest file for an app with containers includes configuration information about the
   containers included in the app. See [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview) for more information.
2. Create the setup script for the app.

   The specific contents of the setup script depend on the requirements of the app. For
   general information on creating the setup script for an app, see [Create the setup script](/developer-guide/native-apps/creating-setup-script).

   Within the setup script you can create the following objects that are specific to
   a Snowflake Native App with Snowpark Container Services:

   - [Add a compute pool to an app with containers](/developer-guide/native-apps/container-compute-pool)
   - [Add services to an app](/developer-guide/native-apps/container-services)
   - [Add job services to an app](/developer-guide/native-apps/container-services-job)

   You can also add other objects that are part of any Snowflake Native App, including:

   - Warehouses
   - External access integrations
   - Secrets
3. Create the application package.

   The process of creating an application package for an app with containers is the
   same as other apps. See [Create and manage an application package](/developer-guide/native-apps/creating-app-package) for more
   information.
4. Publish the app

   Publishing an app as a private listing or on the Snowflake Marketplace is the same
   as other apps. See
   [Share an app with consumers](https://other-docs.snowflake.com/en/native-apps/provider-publishing-app-package)
   for more information.
