Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$VALIDATE\_STORAGE\_INTEGRATION

Validates the configuration for a specified storage integration.
The function attempts to use the storage integration to write, read, list, or delete a file for a storage location that you specify by path.

For more information about configuring storage integrations, see:

- [Snowflake storage integration for AWS](/user-guide/data-load-s3-config-storage-integration)
- [Snowflake storage integration for Google Cloud Storage](/user-guide/data-load-gcs-config)
- [Snowflake storage integration for Microsoft Azure](/user-guide/data-load-azure-config)

See also:
:   [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration), [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration)

## Syntax

Copy code

```
SYSTEM$VALIDATE_STORAGE_INTEGRATION( '<storage_integration_name>', '<storage_path>', '<test_file_name>', '<validate_action>' )
```

## Arguments

`storage_integration_name`
:   Name of the storage integration to test.

    Storage integration names are case-sensitive.

`storage_path`
:   The full path to a storage location that you want to validate.
    The storage path must be a URL in the `STORAGE_ALLOWED_LOCATIONS` list for the storage integration.

    **Amazon S3**

    > `'s3://bucket/path/'`
    > > - The `s3` prefix refers to S3 storage in public AWS regions. The `s3gov` prefix refers to S3 storage in
    > >   [government regions](/user-guide/intro-regions#label-us-gov-regions).
    > > - `bucket` is the name of an S3 bucket that stores your data files.
    > > - `path` is an optional path or directory in the bucket.

    **Google Cloud Storage**

    > `'gcs://bucket/path/'`
    > > - `bucket` is the name of a GCS bucket that stores your data files.
    > > - `path` is an optional path or directory in the bucket.

    **Microsoft Azure**

    > `'azure://account.blob.core.windows.net/container/path/'`
    > > - `account` is the name of the Azure storage account.
    > > - `container` is the name of an Azure blob storage container that stores your data files.
    > > - `path` is an optional path or directory in the bucket.

`test_file_name`
:   The name of the file to use in storage integration validation.

`validate_action`
:   The validation action to perform.

    Values:
    :   - `read` - Validates that Snowflake can read from the storage location. This action fails if the file doesn’t exist.
        - `write` - Validate that Snowflake can write to the storage location. This action fails if the file already exists.
        - `list` - Validates that Snowflake can list the files in the storage location.
        - `delete` - Validates that Snowflake can delete files in the storage location.
        - `all` - Validates all possible actions in the storage location.

## Returns

The function returns a JSON object with the properties described below:

| Property | Description |
| --- | --- |
| `status` | The status of the validation test. Returns a status of `success` if all actions completed successfully; returns `failure` if any action didn’t complete as expected. |
| `actions` | Array of objects that contain the requested validation action (`READ`, `DELETE`, `LIST`, `WRITE`) and status. |

Expand

Show lessSee more

Copy code

```
{
  "status" : "success",
  "actions" : {
    "READ" : {
      "status" : "success"
    },
    "DELETE" : {
      "status" : "success"
    },
    "LIST" : {
      "status" : "success"
    },
    "WRITE" : {
      "status" : "success"
    }
  }
}
```

## Examples

The following example validates the configuration of the storage integration `example_integration` for all validation actions. The
example returns a successful result in JSON.

Copy code

```
SELECT
  SYSTEM$VALIDATE_STORAGE_INTEGRATION(
    'example_integration',
    's3://example_bucket/test_path/'',
    'validate_all.txt', 'all');
```

Output:

```
+----------------------------+
|           RESULT           |
+----------------------------+
| {                          |
|   "status" : "success",    |
|   "actions" : {            |
|     "READ" : {             |
|       "status" : "success" |
|     },                     |
|     "DELETE" : {           |
|       "status" : "success" |
|     },                     |
|     "LIST" : {             |
|       "status" : "success" |
|     },                     |
|     "WRITE" : {            |
|       "status" : "success" |
|     }                      |
|   }                        |
| }                          |
+----------------------------+
```

The following example shows the result when the storage integration doesn’t have `read` permissions.

Copy code

```
SELECT
  SYSTEM$VALIDATE_STORAGE_INTEGRATION(
    'example_integration',
    'gcs://example_bucket/test_path/'',
    'read_fail.txt', 'all');
```

Output:

```
+----------------------------------------------------------------------------------------------------------------+
|                                                     RESULT                                                     |
+----------------------------------------------------------------------------------------------------------------+
| {                                                                                                              |
|   "status" : "failure",                                                                                        |
|   "actions" : {                                                                                                |
|     "READ" : {                                                                                                 |
|       "message" : "Access Denied (Status Code: 403; Error Code: AccessDenied)",                                |
|       "status" : "failure"                                                                                     |
|     },                                                                                                         |
|     "DELETE" : {                                                                                               |
|       "status" : "success"                                                                                     |
|     },                                                                                                         |
|     "LIST" : {                                                                                                 |
|       "status" : "success"                                                                                     |
|     },                                                                                                         |
|     "WRITE" : {                                                                                                |
|       "status" : "success"                                                                                     |
|     }                                                                                                          |
|   },                                                                                                           |
|   "message" : "Some of the integration checks failed. Check the Snowflake documentation for more information." |
| }                                                                                                              |
+----------------------------------------------------------------------------------------------------------------+
```
