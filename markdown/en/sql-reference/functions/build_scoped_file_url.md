Categories:
:   [File functions](/sql-reference/functions-file)

# BUILD\_SCOPED\_FILE\_URL

Generates a scoped Snowflake file URL to a staged file using the stage name and relative file path as inputs.

A scoped URL is encoded and
permits access to a specified file for a limited period of time. The scoped URL in the output is valid for the
caller until the persisted query result period ends (until the results cache expires). That period is currently 24 hours.

Call this SQL function in a query or view. You can also use this SQL function to pass a scoped URL to a user-defined function (UDF)
or stored procedure.

## Syntax

Copy code

```
BUILD_SCOPED_FILE_URL(
  @<stage_name> ,
  '<relative_file_path>' ,
  <use_privatelink_host_for_business_critical>)
```

## Arguments

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (for example,
    `'@"my stage"'` for a stage named `"my stage"`).

`relative_file_path`
:   Path and filename of the file, relative to its location on the stage.

`use_privatelink_host_for_business_critical`
:   Specifies whether to prepend `privatelink` to the URL for [Business Critical](/user-guide/intro-editions) accounts.

    - `TRUE` prepends `privatelink` to the URL just
      before the hostname; for example, `privatelink.snowflakecomputing.com`.

      Note

      Snowflake prepends `privatelink` to the URL regardless of whether you’ve enabled private connectivity.
    - `FALSE` overrides the default behavior and does not add `privatelink` to the URL.

    Default: TRUE

## Returns

The function returns a scoped URL in the following format:

Copy code

```
https://<account_identifier>/api/files/<query_id>/<encoded_file_path>
```

Where:

`account_identifier`
:   Hostname of the Snowflake account for your stage. The hostname starts with a Snowflake-provided account locator
    and ends with the Snowflake domain (`snowflakecomputing.com`):

    `account_locator.snowflakecomputing.com`

    For more details, see [Account identifiers](/user-guide/admin-account-identifier).

`query_id`
:   Query ID of the BUILD\_SCOPED\_FILE\_URL call that generated the scoped URL.

`encoded_file_path`
:   Encoded path to the files to access using the scoped URL.

## Usage notes

- The permissions required to call this SQL function differ depending on how it is called:

  | SQL Operation | Permissions Required |
  | --- | --- |
  | Query | USAGE (external stage) or READ (internal stage) |
  | Column definition in a view | The view owner (i.e. role that has the OWNERSHIP privilege on the view) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the view only requires the SELECT privilege on the view. |
  | Stored procedure | The stored procedure owner (i.e. role that has the OWNERSHIP privilege on the stored procedure) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the stored procedure only requires the USAGE privilege on the stored procedure. |
  | UDF | The UDF owner (i.e. role that has the OWNERSHIP privilege on the UDF) must have the stage privilege: USAGE (external stage) or READ (internal stage).  A role that queries the UDF only requires the USAGE privilege on the UDF. |

  Expand

  Show lessSee more
- An HTTP client that sends a scoped URL to the REST API must be configured to allow redirects.
- When a scoped URL is accessed, the query history shows that the internal GET\_SCOPED\_FILE function was called.

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

Retrieve a scoped URL for a bitmap format image file in an external stage:

Copy code

```
SELECT BUILD_SCOPED_FILE_URL(@images_stage,'us/yosemite/half_dome.jpg', TRUE);
```

Copy code

```
https://my_account.snowflakecomputing.com/api/files/019260c2-00c0-f2f2-0000-4383001cf046/bXlfZGF0YWJhc2UvbXlfc2NoZW1hL215X3N0YWdlL2ZvbGRlcjEvZm9sZGVyMi9maWxlMQ
```

Create a secure view that filters the results of a BUILD\_SCOPED\_FILE\_URL function call for a specific audience. In this example, querying
the secure view returns only those files in the stage file path that include the string `acct1`:

Copy code

```
-- Create a table that stores the relative file path for each staged file along with any other related data.
CREATE TABLE acct_table (
  acct_name string,
  relative_file_path string
);

-- Create a secure view on the table you created.
-- A role that has the SELECT privilege on the secure view has scoped access to the filtered set of files that include the acct1 text string.
CREATE SECURE VIEW acct1_files
AS
  SELECT BUILD_SCOPED_FILE_URL(@acct_files, relative_file_path, FALSE) scoped_url
  FROM acct_table
  WHERE acct_name = 'acct1';
```
