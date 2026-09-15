# CREATE MCP SERVER

Creates a new MCP (Model Context Protocol) server or replaces an existing MCP server.

See also:
:   [DESCRIBE MCP SERVER](/sql-reference/sql/desc-mcp-server), [DROP MCP SERVER](/sql-reference/sql/drop-mcp-server), [SHOW MCP SERVERS](/sql-reference/sql/show-mcp-servers)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] MCP SERVER [ IF NOT EXISTS ] <name>
  FROM SPECIFICATION $$<specification_yaml>$$
```

## Parameters

`name`
:   String that specifies the identifier for the MCP server; must be unique for the schema in which the MCP server is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM SPECIFICATION $$specification_yaml$$`
:   Specifies the YAML specification defining the tools and configuration for the MCP server.

    The specification must include a `tools` array with one or more tool definitions. Each tool must specify:

    - `name`: Unique identifier for the tool
    - `type`: Tool type (see supported tool types)
    - `title`: Human-readable title for the tool
    - `description`: Description of what the tool does

    **Supported tool types:**

    - `CORTEX_SEARCH_SERVICE_QUERY`: Cortex Search Service tool
    - `CORTEX_ANALYST_MESSAGE`: Cortex Analyst tool
    - `SYSTEM_EXECUTE_SQL`: SQL execution tool
    - `CORTEX_AGENT_RUN`: Cortex Agent tool
    - `GENERIC`: Custom tool for UDFs and stored procedures

    **Tool-specific requirements:**

    For `CORTEX_SEARCH_SERVICE_QUERY`, `CORTEX_ANALYST_MESSAGE`, and `CORTEX_AGENT_RUN` tools:

    - `identifier`: Fully qualified name of the underlying object (for example, `database.schema.object_name`)

    For `GENERIC` tools:

    - `identifier`: Fully qualified name of the UDF or stored procedure
    - `config`: Configuration object specifying:
      - `type`: Either `function` (for UDF) or `procedure` (for stored procedure)
      - `warehouse`: Warehouse to use for execution
      - `input_schema`: JSON schema defining the function/procedure parameters

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| CREATE MCP SERVER | Schema |
| USAGE | Schema |

Expand

Show lessSee more

For tools that reference other objects, additional privileges are required:

| Privilege | Object |
| --- | --- |
| USAGE | Cortex Search Service (for CORTEX\_SEARCH\_SERVICE\_QUERY tools) |
| SELECT | Semantic View (for CORTEX\_ANALYST\_MESSAGE tools) |
| USAGE | Cortex Agent (for CORTEX\_AGENT\_RUN tools) |
| USAGE | User-defined function or stored procedure (for GENERIC tools) |
| USAGE | Warehouse (for GENERIC tools) |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
- When configuring hostnames for MCP server connections, use hyphens (`-`) instead of underscores (`_`). MCP servers have connection issues with hostnames containing underscores.
- External OAuth authorization-server binding and advertised scopes aren’t set in the MCP server specification. Configure them with the `OAUTH_AUTHORIZATION_SERVER` and `OAUTH_SCOPES_SUPPORTED` parameters on the enclosing account, database, or schema. For details, see [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth).
- The MCP server specification is stored as metadata and can be viewed using [DESCRIBE MCP SERVER](/sql-reference/sql/desc-mcp-server).
- Multiple tools can be defined in a single MCP server specification.
- Tool names must be unique within a single MCP server.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

**Example 1: Create MCP server with Cortex Search and Analyst tools**

Copy code

```
CREATE MCP SERVER my_mcp_server
  FROM SPECIFICATION $$
    tools:
      - name: "product-search"
        type: "CORTEX_SEARCH_SERVICE_QUERY"
        identifier: "database1.schema1.cortex_search_service1"
        description: "Cortex search service for all products"
        title: "Product Search"

      - name: "revenue-semantic-view"
        type: "CORTEX_ANALYST_MESSAGE"
        identifier: "database1.schema1.semantic_view_1"
        description: "Semantic view for all revenue tables"
        title: "Semantic view for revenue"
  $$;
```

**Example 2: Create MCP server with SQL execution tool**

Copy code

```
CREATE MCP SERVER sql_exec_server
  FROM SPECIFICATION $$
    tools:
      - title: "SQL Execution Tool"
        name: "sql_exec_tool"
        type: "SYSTEM_EXECUTE_SQL"
        description: "A tool to execute SQL queries against the connected Snowflake database."
  $$;
```

**Example 3: Create MCP server with custom UDF tool**

Copy code

```
CREATE MCP SERVER custom_tools_server
  FROM SPECIFICATION $$
    tools:
      - title: "Multiply by Ten"
        identifier: "example_database.agents.multiply_by_ten"
        name: "multiply_by_ten"
        type: "GENERIC"
        description: "Multiplies input value by ten and returns the result."
        config:
          type: "function"
          warehouse: "compute_service_warehouse"
          input_schema:
            type: "object"
            properties:
              x:
                description: "A number to be multiplied by ten"
                type: "number"
  $$;
```

**Example 4: Create MCP server with custom stored procedure tool**

Copy code

```
CREATE MCP SERVER procedure_tools_server
  FROM SPECIFICATION $$
    tools:
      - title: "Calculate Values"
        identifier: "example_database.agents.calculate_values_sp"
        name: "calculate_values_sp"
        type: "GENERIC"
        description: "Calculates the product and sum of two numbers and returns them in a JSON object."
        config:
          type: "procedure"
          warehouse: "compute_service_warehouse"
          input_schema:
            type: "object"
            properties:
              x:
                description: "First number"
                type: "number"
              y:
                description: "Second number"
                type: "number"
  $$;
```

**Example 5: Create MCP server with Agent tool**

Copy code

```
CREATE MCP SERVER agent_server
  FROM SPECIFICATION $$
    tools:
      - title: "Customer Service Agent"
        name: "customer_agent"
        type: "CORTEX_AGENT_RUN"
        identifier: "support_db.agents_schema.customer_service_agent"
        description: "Agent that handles customer service inquiries"
  $$;
```
