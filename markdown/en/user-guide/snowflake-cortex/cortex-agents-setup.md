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

Cortex Agents determines session permissions from the querying user’s default role, not the role active in their session. Every user who calls an agent must have:

- A default role with the privileges described on this page.
- A default warehouse, with `USAGE` on that warehouse granted to the default role.

If either is missing, agent calls fail even when the user’s current role has the required privileges.

At a minimum, the default role must be granted `USAGE` on the agent, on the database and schema that contain it, and on the user’s default warehouse:

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
| USAGE | Warehouse | Required on the user’s default warehouse to run agent queries and tools. |
| MODIFY | Agent | Required to update the agent. |
| MONITOR | Agent | Required to view the agent’s threads, logs, and traces. |
| OWNERSHIP | Agent | Automatically granted to the role that creates the agent. Can be transferred to another role with [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership). |

Expand

Show lessSee more

For default role and warehouse requirements, see [User requirements](#label-cortex-agents-user-requirements).

## Additional privileges for tools

Because the agent runs with the querying user’s default role, that role also needs privileges on the objects used by the agent’s tools:

Important

`USAGE` on the agent isn’t sufficient on its own. The user’s default role also needs privileges on each tool you expect the agent to use. Grant the privileges in the following table for those tools.

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
