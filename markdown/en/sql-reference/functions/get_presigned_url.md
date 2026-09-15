Categories:
:   [File functions](/sql-reference/functions-file)

# GET\_PRESIGNED\_URL

Generates a pre-signed URL to a file on a stage using the stage name and relative file path as inputs.

Access files in a stage using any of the following methods:

- Navigate to the pre-signed URL directly in a web browser.
- Retrieve a pre-signed URL in Snowsight. Click on the pre-signed URL in the results table.
- Send the pre-signed URL in a request to the REST API for file support.

Note

When calling this function for files in an external stage that references Microsoft Azure cloud storage: This function returns
output only when the Azure container that stores the blob object is accessed using a storage integration; querying the function
fails if the container is accessed using a shared access signature (SAS) token you generate.

The GET\_PRESIGNED\_URL function requires Azure Active Directory authentication to create the user delegation SAS token. For this purpose,
a storage integration object stores a generated service principal for your Azure cloud storage. The Snowflake service principal is
granted a role that includes the `Microsoft.Storage/storageAccounts/blobServices/generateUserDelegationKey` permission (or *action*).
Both the `Storage Blob Data Reader` and `Storage Blob Data Contributor` roles include this permission. For more information about
this permission, see the
[Microsoft documentation](https://docs.microsoft.com/en-us/rest/api/storageservices/get-user-delegation-key#authorization).

For more information about accessing an Azure container, see [Configure an Azure container for loading data](/user-guide/data-load-azure-config).

Note

For Microsoft Fabric OneLake stages, pre-signed URLs have a maximum expiration time of 60 minutes (3600 seconds) because of user
delegation key constraints in Microsoft Fabric. If you specify a longer expiration time, the function returns an error.

## Syntax

Copy code

```
GET_PRESIGNED_URL( @<stage_name> , '<relative_file_path>' , [ <expiration_time> ] )
```

## Arguments

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

`relative_file_path`
:   Path and filename of the file relative to its location on the stage.

`expiration_time`
:   Length of time (in seconds) after which the short term access token expires.

    Default value: `3600` (60 minutes).

    Maximum value: If the stage uses an AWS IAM role (`AWS_ROLE`) to securely connect to your S3 bucket,
    the maximum expiration time is `3600` (60 minutes).

    For Microsoft Fabric OneLake stages, the maximum expiration time
    is `3600` (60 minutes). Otherwise, the maximum expiration
    time is `604800` (7 days).

## Returns

Pre-signed URL of the staged file.

Note

This SQL function generates a pre-signed URL for the file path that you specify, even if the file does not exist on the stage.
To ensure that the generated URL returns the expected file, open the URL in a web browser. If the file does not exist,
the browser returns a `NoSuchKey` error in XML format.

## Usage notes

- Server-side encryption is required on the internal or external stage. For details, see [CREATE STAGE](/sql-reference/sql/create-stage).
- This SQL function returns a value for any role that has the following privilege on the stage:

  External stage:
  :   USAGE

  Internal stage:
  :   READ

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

### Querying the function

Copy code

```
SELECT GET_PRESIGNED_URL(@images_stage, 'us/yosemite/half_dome.jpg', 3600);

+================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================-------+
| GET_PRESIGNED_URL(@IMAGES_STAGE, 'US/YOSEMITE/HALF_DOME.JPG', 3600)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================-------|
| http://myaccount.s3.amazonaws.com/national_parks/us/yosemite/half_dome.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxAus-west-xxxxxxxxxaws1_request&X-Amz-Date=20200625T162738Z&X-Amz-Expires=3600&X-Amz-Security-Token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-Amz-SignedHeaders=host&X-Amz-Signature=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   |
+================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================-------+
```

### Loading metadata for an image file and retrieving the pre-signed URL

Use the API for your cloud storage service to generate a list of JSON documents that contain the metadata extracted from the images.

For example, suppose the JSON document for one bitmap image file is as follows:

Copy code

```
{
  "file_url": "s3://photos/national_parks/us/yosemite/half_dome.jpg",
  "image_format": "jpeg",
  "dimensions": {"x" : 1024, "y" : 768},
  "tags":[
    "rock",
    "cliff",
    "valley"
  ],
  "dominant_color": "gray"
}
```

Create a table for the image metadata, load the metadata into the table, and generate the pre-signed URL for the image:

Copy code

```
-- Create a table to store the file metadata

  CREATE TABLE images_table
  (
      file_url string,
      image_format string,
      dimensions_X number,
      dimensions_Y number,
      tags array,
      dominant_color string,
      relative_path string
  );

-- Load the metadata from the JSON document into the table.

COPY INTO images_table
  FROM
  (SELECT $1:file_url::STRING, $1:image_format::STRING, $1:size::NUMBER, $1:tags, $1:dominant_color::STRING, GET_RELATIVE_PATH(@images_stage, $1:file_url)
  FROM
  @images_stage/image_metadata.json)
  FILE_FORMAT = (type = json);

-- Create a view that queries the pre-signed URL for an image as well as the image metadata stored in a table.
CREATE VIEW image_catalog AS
(
  SELECT
   size,
   get_presigned_url(@images_stage, relative_path) AS presigned_url,
   tags
  FROM
    images_table
);
```
