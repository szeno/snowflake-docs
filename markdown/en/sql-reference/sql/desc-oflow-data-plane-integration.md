# DESCRIBE OPENFLOW DATA PLANE INTEGRATION

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Describes the columns in an Openflow data plane integration.

See also:
:   [ALTER OPENFLOW DATA PLANE](/sql-reference/sql/alter-oflow-data-plane), [SHOW OPENFLOW DATA PLANE INTEGRATIONS](/sql-reference/sql/show-oflow-data-plane-integration)

## Syntax

Copy code

```
{ DESC | DESCRIBE } OPENFLOW DATA PLANE INTEGRATION <name>
```

## Parameters

`name`
:   The identifier for the openflow data plane integration to describe.
    If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

    See [SHOW OPENFLOW DATA PLANE INTEGRATIONS](/sql-reference/sql/show-oflow-data-plane-integration) for openflow data plane integration details, including openflow data plane integration **name**.

## Usage notes

- Openflow data plane integrations cannot be created directly, but rather are created when a deployment is created.
- To DESCRIBE an Openflow data plane integration, you must be using a role that
  has one of USAGE, MODIFY, or OWNERSHIP privilege on the data plane integration.

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

## Output

The command output provides properties and metadata for the Openflow data plane integration in the following columns:

|  |  |
| --- | --- |
| Column | Description |
| `enabled` | True if enabled, otherwise false. |
| `oauth_redirect_uri` | URI used for OATH2 authentication. |
| `data_plane_id` | Internal identifier for the data plane integration. |
| `event_table` | Fully qualified path to the <DATABASE>.<SCHEMA>.<EVENT TABLE NAME> is specified. |
| `comment` | Associated comment. |

Expand

Show lessSee more

## Examples

Describe the columns in the Openflow data plane integration with the specified name:

Copy code

```
DESC OPENFLOW DATA PLANE INTEGRATION edf6f909-d3ff-49d6-925f-xxxxx;
```

```
+------------------------------------+----------------------------------+------------------+---------------+
|   enabled  |   oauth_redirect_uri  |   data_plane_id                  |   event_table    |   comment     |
+------------------------------------+----------------------------------+------------------+---------------+
|   true     |   https://...         |   edf6f909-d3ff-49d6-925f-xxxxx  |                  |   Example     |
+------------------------------------+----------------------------------+------------------+---------------+
```
