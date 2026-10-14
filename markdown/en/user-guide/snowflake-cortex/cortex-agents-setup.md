# Access control and authentication

Access to Cortex Agents is governed by Snowflake’s role-based access control. This topic covers the database roles and privileges that let users create, manage, and call agents, along with the authentication methods the API supports.

## API access roles

To call the Cortex Agents `agent:run` API, use a role that has been granted one of the following database roles:

- **SNOWFLAKE.CORTEX\_USER**: Grants access to all Covered AI Features, including Cortex Agents.
- **SNOWFLAKE.CORTEX\_AGENT\_USER**: Grants access to Cortex Agents only.

By default, the CORTEX\_USER database role is granted to the PUBLIC role, which is automatically granted to all users and roles. If you don’t want all users to have this access, use the `ACCOUNTADMIN` role to run the following command:

Copy code

```
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER FROM ROLE PUBLIC;
```

You can then grant access to specific roles instead. For more information, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).

Caution

The Cortex LLM privileges guidance also recommends revoking `IMPORTED PRIVILEGES` on the `SNOWFLAKE` database from the `PUBLIC` role:

Copy code

```
REVOKE IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE FROM ROLE PUBLIC;
```

This optional revocation affects more than Cortex: it also removes `PUBLIC`’s access to other objects in the shared `SNOWFLAKE` database, such as `ACCOUNT_USAGE` views. Only run this command if you intend to restrict all of that access.

## User requirements

Cortex Agents determines permissions from the Snowflake context of the request. For REST API calls, the authentication method, such as a programmatic access token (PAT), OAuth, key pair authentication, or a session token, identifies the caller. The role used to authorize the request comes from the `X-Snowflake-Role` header, or from the user’s default role if the header is omitted. If the request or session context activates secondary roles, those roles also govern privilege checks and data protection policy evaluation.

For calls made from Snowsight or CoWork, the role selected in the UI is used to authorize the request. If no role is selected, Snowflake uses the user’s default role.

Every user who calls an agent must have:

- An active role with the privileges described on this page.
- Access to any secondary roles that must be active for the run.
- `USAGE` on the warehouses configured for the agent’s tools.

At a minimum, the active role must be granted `USAGE` on the agent and on the database and schema that contain it. Grant `USAGE` on each tool warehouse to a role that is active in the caller’s session:

Copy code

```
GRANT USAGE ON DATABASE <database_name> TO ROLE <role_name>;
GRANT USAGE ON SCHEMA <database_name>.<schema_name> TO ROLE <role_name>;
GRANT USAGE ON AGENT <database_name>.<schema_name>.<agent_name> TO ROLE <role_name>;
GRANT USAGE ON WAREHOUSE <warehouse_name> TO ROLE <role_name>;
```

After you set the required privileges, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

## Limiting access to specific roles

To give only a subset of users access to Cortex Agents, use the SNOWFLAKE.CORTEX\_AGENT\_USER database role. Database roles can’t be granted directly to users (see [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role)), so grant it to a custom role and assign that role to users.

The following example, run with the `ACCOUNTADMIN` role, creates the custom role `cortex_agent_user_role`, grants it the CORTEX\_AGENT\_USER database role, and assigns it to `example_user`:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE cortex_agent_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE cortex_agent_user_role;

GRANT ROLE cortex_agent_user_role TO USER example_user;
```

You can also grant the database role to an existing role:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE analyst_role;
```

Important

A role that also has the CORTEX\_USER database role retains access to all Covered AI Features. To restrict such a role to Cortex Agents only, revoke CORTEX\_USER from it using the `ACCOUNTADMIN` role:

Copy code

```
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER FROM ROLE analyst_role;
```

## Agent privileges

The following privileges control who can create, manage, and use an agent:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE AGENT | Schema | Required to create an agent. |
| USAGE | Agent | Required to query the agent to generate responses. The role also needs `USAGE` on the database and schema containing the agent, along with privileges on the objects used by the agent’s tools. See [Additional privileges for tools](#label-cortex-agents-tool-privileges). |
| USAGE | Warehouse | Required on the warehouse configured for a tool to run agent queries and tools. |
| MODIFY | Agent | Permits updating the agent and removing it with [DROP AGENT](/sql-reference/sql/drop-agent). |
| MONITOR | Agent | Required to view the agent’s threads, logs, and traces. |
| OWNERSHIP | Agent | Automatically granted to the role that creates the agent. Can be transferred to another role with [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership). |

Expand

Show lessSee more

For role and warehouse requirements, see [User requirements](#label-cortex-agents-user-requirements).

## Additional privileges for tools

Because the agent uses the caller’s session roles, those roles also need privileges on the objects used by the agent’s tools:

Important

`USAGE` on the agent isn’t sufficient on its own. A role that is active in the caller’s session also needs privileges on each tool you expect the agent to use. Grant the privileges in the following table for those tools.

By default (`accept`), a missing privilege on a configured tool doesn’t reject the entire run. The agent continues with the tools the role can access and reports the rest as warnings. Set `orchestration.tool_not_accessible` to `reject` or `legacy` if you want the run to fail instead. For modes, which tools Snowflake checks, and warning format, see [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

An `agent_toolset` reference is skipped when the role doesn’t have `USAGE` on the referenced agent.

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Cortex Search service | Required to run the Cortex Search services configured on the agent. The role also needs `USAGE` on the database and schema containing the service. |
| USAGE | Database, schema, table | Required to access the objects referenced in the agent’s semantic view. |
| USAGE | Function or stored procedure | Required to run a custom tool. Stored procedures run with owner’s rights or caller’s rights as defined on the procedure. See [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights). |
| USAGE | Referenced agent | Required to expand an `agent_toolset` reference. Silently skipped if missing. See [Agent toolsets](/user-guide/snowflake-cortex/cortex-agents-toolsets). |

Expand

Show lessSee more

## Authentication

Requests to the Cortex Agents API must include an authorization token. Snowflake REST APIs support authentication via programmatic access tokens (PATs), key pair authentication using JSON Web Tokens (JWTs), and OAuth. For details, see [Authenticating Snowflake REST APIs with Snowflake](/developer-guide/snowflake-rest-api/authentication).
