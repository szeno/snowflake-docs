# DESCRIBE MCP SERVER

Describes the properties of an MCP (Model Context Protocol) server.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server) , [DROP MCP SERVER](/sql-reference/sql/drop-mcp-server) , [SHOW MCP SERVERS](/sql-reference/sql/show-mcp-servers)

## Syntax

Copy code

```
{ DESC | DESCRIBE } MCP SERVER <name>
```

## Parameters

`name`
:   Specifies the identifier for the MCP server to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the MCP server. |
| `database_name` | Database that contains the MCP server. |
| `schema_name` | Schema that contains the MCP server. |
| `owner` | Role that owns the MCP server. |
| `comment` | Comment for the MCP server. |
| `server_spec` | JSON representation of the MCP server specification, including tools configuration. |
| `created_on` | Date and time when the MCP server was created. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| USAGE, MODIFY, or OWNERSHIP | MCP server |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

- The `server_spec` column contains the complete YAML specification that was provided when the MCP server was created, serialized as JSON.

## Examples

The following example describes the MCP server named `my_mcp_server`:

Copy code

```
DESCRIBE MCP SERVER my_mcp_server;
```

```
+-----------------+---------------+-------------+--------------+---------+--------------------------------------------------------------------------------------------------------------------------------+----------------------------------------+
|      name       | database_name | schema_name |    owner     | comment |                                                           server_spec                                                          |               created_on               |
+-----------------+---------------+-------------+--------------+---------+--------------------------------------------------------------------------------------------------------------------------------+----------------------------------------+
| MY_MCP_SERVER   | TEST_DATABASE | TEST_SCHEMA | ACCOUNTADMIN | [NULL]  | {"version":1,"tools":[{"name":"product-search","identifier":"db.schema.search_service","type":"CORTEX_SEARCH_SERVICE_QUERY"}]} | Fri, 23 Jun 1967 07:00:00.123000 +0000 |
+-----------------+---------------+-------------+--------------+---------+--------------------------------------------------------------------------------------------------------------------------------+----------------------------------------+
```
