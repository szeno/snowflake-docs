Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$REGISTRY\_LIST\_IMAGES — *Deprecated*

Deprecated Feature

This function has been deprecated. Use the [SHOW IMAGES IN IMAGE REPOSITORY](/sql-reference/sql/show-images-in-image-repository) command instead.

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists images in an [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

See also:
:   [Working with an Image Registry and Repository](/developer-guide/snowpark-container-services/working-with-registry-repository)

## Syntax

Copy code

```
SYSTEM$REGISTRY_LIST_IMAGES( '/<dbName>/<schemaName>/<repositoryName>' )
```

## Arguments

**Required:**

`dbName`
:   Name of the database in which the repository is created.

`schemaName`
:   Name of the database in which the repository is created.

`repositoryName`
:   Name of the image repository.

## Returns

Returns a JSON object listing all the images.

## Usage notes

- You need the read permission on the repository to get a list of images.

## Examples

This function retrieves a list of images from the `/tutorial_db/data_schema/tutorial_repository` repository.

Copy code

```
SELECT SYSTEM$REGISTRY_LIST_IMAGES('/tutorial_db/data_schema/tutorial_repository');
```

Sample output showing a list of two images in the repository:

```
+-----------------------------------------------------------------------------+
| SYSTEM$REGISTRY_LIST_IMAGES('/TUTORIAL_DB/DATA_SCHEMA/TUTORIAL_REPOSITORY') |
|-----------------------------------------------------------------------------|
| {"images":["my_echo_service_image","my_job_image"]}                         |
+-----------------------------------------------------------------------------+
```
