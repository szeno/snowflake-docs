# SHOW VERSIONS IN LISTING

Lists and provides details of all listing versions.

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
SHOW VERSIONS IN LISTING <name>
  [ LIMIT <rows> ]
```

## Parameters

`name`
:   Specifies the listing identifier (name). If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive.

    For more information, see [Identifier Requirements](/sql-reference/identifiers-syntax).

`LIMIT rows`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `created_on` | Date and time the version was created. |
| `name` | The system generated name of the version. |
| `alias` | The user specified alias of the version. |
| `location_url` | Full URL of the version, against which stage operations can be performed. |
| `is_default` | Identifies the listing version that is published. |
| `is_live` | Identifies if the version is a live version of the listing. |
| `is_first` | Identifies if the version is the first listing version. |
| `is_last` | Identifies if the version is the last listing version. |
| `comment` | Optional comments for the listing version. |
| `source_location_url` | The source location URL where this version is created from. |
| `git_commit_hash` | The git commit hash, if the version is created from a git source. |

Expand

Show lessSee more

## Access control requirements

- To show listing versions, you must be using a role that has USAGE or OWNERSHIP privileges on the listing.

## Usage notes

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Show all versions of the MYLISTING listing:

Copy code

```
SHOW VERSIONS IN LISTING MYLISTING
```

```
+-----------------------------------+------------------------------+------------------------------+-----------------------------------------------+--------------------+--------------------+--------------------+--------------------+---------------------------------------------+---------------------------------------+---------------------------------------+
|             created_on            |             name             |             alias            |                  location_uri                 |     is_default     |       is_live      |      is_first      |       is_last      |                   comment                   |          source_location_uri          |             git_commit_hash           |
+-----------------------------------+------------------------------+------------------------------+-----------------------------------------------+--------------------+--------------------+--------------------+--------------------+---------------------------------------------+---------------------------------------+---------------------------------------+
|   2025-01-08 11:18:39.921 -0800   |                              |                              |  snow://listing/MYLISTING/versions/live/      |        FALSE       |        TRUE        |        FALSE       |       FALSE        |                                             |            @listingstage              |                                       |
|   2025-01-08 11:18:24.550 -0800   |        VERSION$2             |                              |  snow://listing/MYLISTING/versions/version$2/ |        TRUE        |        FALSE       |        FALSE       |       TRUE         |                                             |            @listingstage              |                                       |
|   2025-01-08 11:17:32.894 -0800   |        VERSION$1             |                              |  snow://listing/MYLISTING/versions/version$1/ |        FALSE       |        FALSE       |        TRUE        |       FALSE        |                                             |            @listingstage              |                                       |
+-----------------------------------+------------------------------+------------------------------+-----------------------------------------------+--------------------+--------------------+--------------------+--------------------+---------------------------------------------+---------------------------------------+---------------------------------------+
```
