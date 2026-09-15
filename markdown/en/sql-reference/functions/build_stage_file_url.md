Categories:
:   [File functions](/sql-reference/functions-file)

# BUILD\_STAGE\_FILE\_URL

Generates a Snowflake *file URL* to a staged file using the stage name and relative file path as inputs. A file URL permits
prolonged access to a specified file. That is, the file URL does not expire.

Call this SQL function in a query, user-defined function (UDF), or stored procedure.

Access files in a stage by sending the file URL in a request to the REST API for file support. When users send a file URL to the REST API
to access files, Snowflake performs the following actions:

1. Authenticate the user.
2. Verify that the role has sufficient privileges on the stage that contains the file.
3. Redirect the user to the staged file in the cloud storage service.

## Syntax

Copy code

```
BUILD_STAGE_FILE_URL( @<stage_name> , '<relative_file_path>' )
```

## Arguments

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

`relative_file_path`
:   Path and filename of the file relative to its location in the stage.

## Returns

The function returns a file URL in the following format:

Copy code

```
https://<account_identifier>/api/files/<db_name>/<schema_name>/<stage_name>/<relative_path>
```

Where:

`account_identifier`
:   Hostname of the Snowflake account for your stage. The hostname starts with an account locator (provided by Snowflake) and ends with the
    Snowflake domain (`snowflakecomputing.com`):

    `account_locator.snowflakecomputing.com`

    For more details, see [Account identifiers](/user-guide/admin-account-identifier).

    Note

    For [Business Critical](/user-guide/intro-editions) accounts, a `privatelink` segment is prepended to the URL just before
    `snowflakecomputing.com` (`privatelink.snowflakecomputing.com`), even if private connectivity to the Snowflake service is not
    enabled for your account.

    Important

    Currently, the function returns the account identifier in the form `organization_name-account_name`. When a file URL is used
    as input to a GET request, the API endpoint returns an error.

    To resolve the error, you must manually convert the account identifier to the applicable form for your account:

    `account_locator.region_id`or`account_locator.region_id.cloud`

    For more information about these forms, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).

    In an upcoming release, the function will return file URLs in the correct form.

`db_name`
:   Name of the database that contains the stage where your files are located.

`schema_name`
:   Name of the schema that contains the stage where your files are located.

`stage_name`
:   Name of the stage where your files are located.

`relative_path`
:   Path to the files to access using the file URL.

## Usage notes

- The permissions required to call this SQL function differ depending on how it is called:

  | SQL Operation | Permissions Required |
  | --- | --- |
  | Query | USAGE (external stage) or READ (internal stage) |
  | Stored procedure | The stored procedure owner (i.e. role that has the OWNERSHIP privilege on the stored procedure) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the stored procedure only requires the USAGE privilege on the stored procedure. |
  | UDF | The UDF owner (i.e. role that has the OWNERSHIP privilege on the UDF) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the UDF only requires the USAGE privilege on the UDF. |

  Expand

  Show lessSee more
- An HTTP client that sends a file URL to the REST API must be configured to allow redirects.
- When a file URL is accessed, the query history shows that the internal GET\_STAGE\_FILE function was called.

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

Retrieve a file URL for a bitmap format image file in an external stage:

Copy code

```
SELECT BUILD_STAGE_FILE_URL(@images_stage,'us/yosemite/half_dome.jpg');
```

Copy code

```
https://my_account.snowflakecomputing.com/api/files/MY_DB/PUBLIC/IMAGES_STAGE/us/yosemite/half_dome.jpg
```
