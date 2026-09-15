# Directory tables

This topic introduces key concepts, provides ancillary information, and links to instructions for using directory tables.

## About directory tables

A directory table is an implicit object layered on a stage (not a separate database object) and is conceptually similar to an
external table because it stores file-level metadata about the data files in the stage. A directory table has no grantable privileges of its own.

Both external (external cloud storage) and internal (Snowflake) stages support directory tables. You can add a directory table
to a stage when you create a stage (using [CREATE STAGE](/sql-reference/sql/create-stage)) or later
(using [ALTER STAGE](/sql-reference/sql/alter-stage)).

In particular, you can use a directory table to accomplish the following unstructured data tasks:

- [Query a list of all the unstructured files on a stage](/user-guide/data-load-dirtables-query).
  You can query a directory table to retrieve a list of all the files on a stage. The query output contains information about each file,
  including the size, a timestamp of when it was last modified, and its [Snowflake file URL](/user-guide/unstructured-intro#label-unstructured-data-urls).
- [Create views of unstructured data](/user-guide/data-load-dirtables-query#label-data-load-dirtables-rich-views).
  You can join a directory table with a Snowflake table that contains additional
  data and metadata about unstructured files to see unstructured files and their related data in a single view.
- [Construct a file processing pipeline](/user-guide/data-load-dirtables-pipeline). You can use a directory table with
  the Snowpark API or external functions to create a file processing pipeline.

To register changes to files on a stage, you can [refresh the directory table metadata](/user-guide/data-load-dirtables-manage#label-directory-table-refreshes).

## Billing for directory tables

An overhead to manage event notifications for the automatic refreshing of directory table metadata is included in your charges. This overhead increases in
relation to the number of files added in cloud storage for your stages that include directory tables. This overhead charge appears as
Snowpipe charges in your billing statement because Snowpipe is used for event notifications for the automatic directory table refreshes.
You can estimate this charge by querying the [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) function or examining the Account Usage [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history).

In addition, a small maintenance overhead is charged for manually refreshing the directory table metadata (using ALTER STAGE …
REFRESH). This overhead is charged in accordance with the standard [cloud services billing model](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage),
like all similar activity in Snowflake. Manual refreshes of directory table metadata don’t appear in queries to the [PIPE\_USAGE\_HISTORY](/sql-reference/functions/pipe_usage_history) function or in the Account Usage [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history).

Users with the ACCOUNTADMIN role, or a role with the global MONITOR USAGE privilege, can query the
[AUTO\_REFRESH\_REGISTRATION\_HISTORY](/sql-reference/functions/auto_refresh_registration_history) table function to retrieve the history of data files registered in the
metadata of specified objects and the credits billed for these operations.

## Access control requirements for directory tables

The following table summarizes the stage [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) that you need to execute common
SQL commands when you work with directory tables.

| Operation | Object Type | Privilege Required |
| --- | --- | --- |
| Retrieve file URLs from a directory table using a SELECT FROM DIRECTORY statement. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the READ privilege on the stage. - External stage: An account role or database role with either the READ or USAGE privilege on the stage. |
| Upload data using the [PUT](/sql-reference/sql/put) command. | Stage (internal only) | An account role or database role with the WRITE privilege on the stage. |
| Remove files using the [REMOVE](/sql-reference/sql/remove) command. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the WRITE privilege on the stage. - External stage: An account role or database role with either the WRITE or USAGE privilege on the stage. |
| Refresh the metadata using the [ALTER STAGE](/sql-reference/sql/alter-stage) command. | Stage | One of the following, depending on the type of stage:   - Internal stage: An account role or database role with the WRITE privilege on the stage. - External stage: An account role or database role with either the WRITE or USAGE privilege on the stage. |

Expand

Show lessSee more

## Information Schema

The Snowflake [Snowflake Information Schema](/sql-reference/info-schema) includes table functions you can query to retrieve information about your directory
tables.

### Table functions

[AUTO\_REFRESH\_REGISTRATION\_HISTORY](/sql-reference/functions/auto_refresh_registration_history)
:   Retrieve the history of data files registered in the metadata of specified objects and the credits billed for these operations.

[STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/stage_directory_file_registration_history)
:   Retrieve information about the metadata history for a directory table, including any errors found when refreshing the metadata.

**Next Topics:**

- [Manage directory tables](/user-guide/data-load-dirtables-manage)
- [Query directory tables](/user-guide/data-load-dirtables-query)
- [Automated directory table metadata refreshes](/user-guide/data-load-dirtables-auto)
- [Build a data processing pipeline using a directory table](/user-guide/data-load-dirtables-pipeline)
