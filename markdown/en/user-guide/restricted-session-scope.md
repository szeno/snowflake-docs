# Restricted Session Scope for agents

When an agent acts on behalf of a user, it inherits the user’s full privileges by default. That can
include write access to production databases, elevated roles such as ACCOUNTADMIN, or access to data
that shouldn’t enter an LLM context. An agent’s work is usually narrower than the user’s full
privilege set, so that inheritance can create governance risk without any change to the user’s
roles.

A Restricted Session Scope (RSS) is a privilege ceiling that limits what an agent can do on behalf
of a user. An RSS doesn’t replace RBAC and can’t grant privileges the user doesn’t already have
through their roles.

An administrator applies RSS as a standing governance control: set
`AGENT_RESTRICTED_SESSION_SCOPE` on a [session policy](/user-guide/session-policies), then attach
that policy to the account or to specific users. The ceiling applies whenever an agent is active for
users covered by the session policy.

User-managed RSS in CoCo CLI and CoCo Desktop is still in private preview. For that client
experience, see [Restricted Session Scope for agents](/LIMITEDACCESS/security/agent-restricted-session-scope).

`AGENT_RESTRICTED_SESSION_SCOPE` on a session policy applies only when an agent is active. When no
agent is active, that property is ignored. For when
`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` returns `TRUE`, see
[IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated).

## Benefits

Restricted Session Scope helps you:

- Set a privilege ceiling for agents without changing user roles, or duplicating user’s RBAC for the Agent. For example, Agents should only read in production databases, but can write to personal databases.
- Reduce unintended production writes, privilege escalation through secondary roles, and access to
  sensitive data from agent workflows.
- Keep full RBAC available when no agent is active in the session, or when no RSS is applied.
- Apply different agent ceilings account-wide or to specific users through session policy
  attachment.

## Configure Restricted Session Scope with a session policy

Use a session policy when you want an account-wide or per-user privilege ceiling for agent
sessions. An administrator sets `AGENT_RESTRICTED_SESSION_SCOPE` on a session policy, then attaches
that policy to the account or to users.

To apply an RSS when an agent is active:

1. Set `AGENT_RESTRICTED_SESSION_SCOPE` on a session policy.
2. Attach the session policy to the account or to a user.

You can specify the scope value in any of these ways:

1. Reference a Snowflake predefined scope (easiest starting point).
2. Create an RSS object and reference it by fully qualified name.
3. Embed the RSS YAML inline in the session policy.

For SQL syntax, including the `RSS` alias, `CREATE OR ALTER`, and `ADD AS` / `REMOVE AS` patches,
see [CREATE RESTRICTED SESSION SCOPE](/sql-reference/sql/create-restricted-session-scope) and
[ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope).

### RSS YAML structure

An RSS is defined as a YAML document with two top-level sections:

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [<group_privilege>]
      account: [all]                 # or databases: [...] or schemas: [...]
    - privileges: [<privilege>]
      object_types: [<object_type>, ...]
      account: [all]                 # or databases: [...] or schemas: [...]
    - privileges: [<privilege>]
      named_objects:
        - type: <object_type>
          names: [<fqn>, ...]
  # Optional: extend a predefined scope, then add more privileges
  # extend: [SNOWFLAKE$DATA_READ]
role_scopes:
  blocked_roles: [<role>, ...]  # or allowed_roles: [...]
  # Optional: restrict secondary roles only, primary role untouched
  # blocked_secondary_roles: [...]  # or allowed_secondary_roles: [...]
  allow_role_switching: false   # default: true
```

- **Privilege scopes:** Categories of operations that are allowed and the containers they apply to
  (account-wide, specific databases, or specific schemas). Use `USER$` in place of a database name
  to scope to the session user’s own personal database. Operations that aren’t listed are
  implicitly denied. Each entry under `allowed_privileges` takes one of these shapes:
  - **A group privilege**, for example `data read`, `data write`, or `program usage`, is a named
    category of Snowflake operations you list explicitly when you need a custom ceiling. Scope it
    with `account`, `databases`, or `schemas`.
  - **An individual privilege on an object type**, specified under `object_types`, for example
    `cortex search service`, is a fine-grained privilege applied to all objects of that type within
    a container. Scope it with `account`, `databases`, or `schemas`.
  - **An individual privilege on named objects** (`named_objects`, addressed by fully qualified
    name): a fine-grained privilege applied only to the listed objects. Container keys and
    `object_types` are forbidden in this shape.
- **Role scopes:** Roles that can be activated while an agent is active. You can allow specific
  roles, block specific roles, restrict secondary roles only, or disable role switching. A blocked
  role can’t be the primary role (matched by exact name) and can’t be activated as a secondary role.
  Blocking a role doesn’t strip privileges that a non-blocked primary role inherits from it. For
  the matching rules and an example, see [Role scopes](#label-agent-rss-role-scopes).

After an RSS is activated for agent activity in a session, it’s immutable for the lifetime of that
session. It can’t be changed, unset, or escalated. To apply a different scope, close the session and
open a new one.

### Create an RSS object and reference it

Creating an RSS requires the `CREATE RESTRICTED SESSION SCOPE` privilege on the parent schema. If
you later update the RSS object, policies that reference it pick up the change for new agent
activity.

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.agent_scope AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, program usage]
      account: [all]
    - privileges: [data write]
      databases: [SANDBOX_DB, USER$]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SYSADMIN, SECURITYADMIN]
  allow_role_switching: true
$$;

CREATE SESSION POLICY mydb.governance.agent_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'MYDB.GOVERNANCE.AGENT_SCOPE';
```

After you create the object, reference it from a session policy with
`AGENT_RESTRICTED_SESSION_SCOPE`. For a walkthrough of what this YAML allows, see
[Production read-only, write allowed in a sandbox and user’s personal database](#label-agent-rss-example-sandbox-write).

### Embed the RSS YAML inline

Define the scope directly in the session policy without creating a separate object. Useful for
simple or one-off configurations.

Copy code

```
CREATE SESSION POLICY mydb.governance.agent_policy
  AGENT_RESTRICTED_SESSION_SCOPE = $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read]
      account: [all]
$$;
```

### Attach the session policy to the account or a user

**Account-level** (default for users without a user-level override):

Copy code

```
ALTER ACCOUNT SET SESSION POLICY mydb.governance.agent_policy;
```

**Per-user** (overrides the account-level policy for that user):

Copy code

```
ALTER USER <user_name> SET SESSION POLICY mydb.governance.per_user_agent_policy;
```

When a user-level session policy is present, its `AGENT_RESTRICTED_SESSION_SCOPE` is used
exclusively. The account-level policy isn’t consulted or merged for that user.

### Check the active RSS for the current session

`SYS_CONTEXT('SNOWFLAKE$SESSION', 'ACTIVE_RESTRICTED_SESSION_SCOPES')` returns the RSS currently
active for the session, so you can confirm what ceiling is in effect without inspecting the session
policy that applied it. For property details, see
[SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session).

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'ACTIVE_RESTRICTED_SESSION_SCOPES');
```

### Predefined scopes

Snowflake provides coarse-grained predefined scopes you can reference directly in a session policy,
without creating an RSS object. You can also extend a predefined scope inside a custom RSS YAML
definition.

`SNOWFLAKE$DATA_READ_WITH_AI` excludes stored procedures because they may run with owner’s rights
and can’t guarantee read-only execution.

| Predefined scope | What it allows | What it doesn’t allow |
| --- | --- | --- |
| `SNOWFLAKE$DATA_READ` | Read-only access to data objects: SELECT on tables, views, streams, stages, and workspaces across the account. | Writes, DDL, grants, and usage on agents, stored procedures, UDFs, or MCP tools. |
| `SNOWFLAKE$DATA_READ_WITH_AI` | Everything in `SNOWFLAKE$DATA_READ`, plus object discovery and USAGE on agents, UDFs, and Cortex Agent MCP servers. | Writes, DDL, grants, and stored procedures. |
| `SNOWFLAKE$DATA_READ_PROGRAM_USAGE` | Everything in `SNOWFLAKE$DATA_READ`, plus invoke UDFs, stored procedures, and other programmatic objects, whether they run with owner’s rights or caller’s rights. Does not add the AI/agent/MCP USAGE path from `SNOWFLAKE$DATA_READ_WITH_AI`; use that scope when you need agent and MCP usage without stored procedures. | Writes and DDL performed directly by the agent outside those programs. |

Expand

Show lessSee more

Copy code

```
CREATE SESSION POLICY mydb.governance.agent_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'SNOWFLAKE$DATA_READ';
```

Note

For programs that run with owner’s rights under `SNOWFLAKE$DATA_READ_PROGRAM_USAGE`, the data-read
restriction doesn’t apply to actions those programs take. A stored procedure running with owner’s
rights can still modify Snowflake objects such as tables, even when this scope is active.

For the YAML that backs each predefined scope, see
[Appendix: Predefined scope YAML](#label-agent-rss-predefined-scope-yaml).

### Group privileges for custom scopes

When you create an RSS object or embed YAML inline, privilege scopes use group privileges: named
categories of operations that map to [high-level caller privileges](/developer-guide/restricted-callers-rights/high-level-caller-privileges). See that topic
for detailed descriptions of each category.

| Group privilege | Scope containers | What it covers |
| --- | --- | --- |
| `data read` | Account, database, schema | SELECT from tables, views, streams, stages, and workspaces in the target container |
| `data write` | Account, database, schema | Write data to tables in the target container |
| `object discovery` | Account, database, schema | Discover objects (for example, using SHOW) without reading their data |
| `compute usage` | Account | Use compute resources such as warehouses and compute pools |
| `program usage` | Account, database, schema | Execute user-defined functions (UDFs), stored procedures, and Streamlit apps |
| `grant management` | Account, database, schema | GRANT and REVOKE on in-account objects |
| `object management` | Account, database, schema | Full control of non-sensitive objects in the target container |
| `full management` | Account | All operations in the account |

Expand

Show lessSee more

Some group privileges can naturally overlap or subsume others. For example, `object management` subsumes
`object discovery` and `compute usage`. UPDATE and DELETE require the ability to read existing data and can’t be
authorized by `data write` alone; use `data read` in conjunction when those operations are needed.

**Containers:** Privileges can be scoped account-wide (`account: [all]`), to specific databases
(`databases: [db1, db2]`), or to specific schemas (`schemas: [db1.public, db1.private]`). Defining
access to a schema implicitly grants access to its parent database. Warehouses are implicitly
allowed regardless of privilege scope. Personal databases are supported too: use `USER$` in place of
a database name in `databases`, and it resolves to the session user’s own personal database, so one
RSS definition scopes each user to their own data.

**Intersection behavior:** The effective privileges while an agent is active are the intersection of
the user’s RBAC privileges and the RSS. An RSS never expands what RBAC already allows.

### Individual privileges

Instead of a broad group privilege, you can scope an allowed privilege to specific objects, either
by object type or by fully qualified name (FQN). An individual (fine-grained) privilege applies only
to the objects it targets, rather than to every object covered by a group privilege.

#### On an object type

An individual privilege on an object type applies to all objects of the given type within a
container. Set `object_types` to a list of SQL object-type names, written with spaces instead of
underscores, for example `cortex search service`, `mcp server`, or `agent`. As with group
privileges, scope the entry with `account: [all]`, `databases: [...]`, or `schemas: [...]`.

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, object discovery]
      account: [all]
    - privileges: [usage]
      object_types: [mcp server]
      account: [all]
```

This example allows `data read` and `object discovery` account-wide, and `usage` on MCP server
objects account-wide.

#### On named objects by FQN

An individual privilege on named objects applies only to the specific objects you list, addressed by
FQN, regardless of what container they live in. Entries are grouped by object type: each entry sets
`type` to a single SQL object-type name and `names` to a list of FQNs of that type. Container keys
(`account`, `databases`, `schemas`) and `object_types` are forbidden in this mode.

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, object discovery]
      account: [all]
    - privileges: [usage]
      named_objects:
        - type: mcp server
          names: [analytics_db.public.my_mcp]
```

This example allows `data read` and `object discovery` account-wide, and `usage` on one specific MCP
server (`analytics_db.public.my_mcp`), and nothing else of that type.

### Role scopes

| Setting | Behavior |
| --- | --- |
| `allowed_roles: [role1, role2]` | The primary role must be exactly one of these, and secondary roles are limited to these roles plus the roles they inherit. |
| `blocked_roles: [ACCOUNTADMIN, SYSADMIN]` | The listed roles can’t be the primary role (exact name) and can’t be activated as secondary roles - along with the roles they inherit. Inherited privileges through a non-blocked primary role remain. |
| `allow_role_switching: false` | Prevents role switching. The session stays locked to the role active at session open. Default: `true`. |

Expand

Show lessSee more

`allowed_roles` and `blocked_roles` apply to both the primary role and any secondary roles. To
restrict only secondary roles and leave the primary role untouched, use
`allowed_secondary_roles` or `blocked_secondary_roles` instead.

A blocklist matches role names exactly. It doesn’t walk the role hierarchy to find other roles that
inherit a blocked role, and it doesn’t strip privileges that the current primary role already
inherits. For secondary roles, the behavior is the same as
[CREATE SESSION POLICY](/sql-reference/sql/create-session-policy) `BLOCKED_SECONDARY_ROLES`: the listed roles can’t be
activated as secondary roles, but privileges that arrive through the primary role’s hierarchy stay
in the session.

For example, suppose `R3` is granted to `R2`, `R2` is granted to `R1`, and `R1` is the session’s
primary role. If the RSS lists `R2` in `blocked_roles`:

- The agent can’t use `R2` as the primary role, and `R2` can’t be activated as a secondary role.
- Because `R1` isn’t blocked, the session still has the privileges of `R1`, including the
  privileges `R1` inherits from `R2` and `R3`.

If you need those inherited privileges out of agent sessions, block the primary roles that inherit
them, or use `allowed_roles` to list only the roles you want as primary.

### Admin example scenarios

#### Account-wide read-only for agents

Use this as a conservative baseline when agents should read and analyze data and use AI-related
objects, but not write, create objects, or modify anything in the account.

Copy code

```
CREATE SESSION POLICY mydb.governance.agent_readonly_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'SNOWFLAKE$DATA_READ_WITH_AI';

ALTER ACCOUNT SET SESSION POLICY mydb.governance.agent_readonly_policy;
```

#### Production read-only, write allowed in a sandbox and user’s personal database

Allow agents to assist with data engineering work while confining writes to a shared sandbox and to
each user’s personal database. This example uses the same YAML shape as
[Create an RSS object and reference it](#label-agent-rss-create-object).

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.prod_readonly_sandbox_write AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, program usage]
      account: [all]
    - privileges: [data write]
      databases: [SANDBOX_DB, USER$]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SYSADMIN, SECURITYADMIN]
  allow_role_switching: true
$$;

CREATE SESSION POLICY mydb.governance.agent_prod_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'MYDB.GOVERNANCE.PROD_READONLY_SANDBOX_WRITE';

ALTER ACCOUNT SET SESSION POLICY mydb.governance.agent_prod_policy;
```

This definition does the following:

- **Read and programs, account-wide:** `data read` and `program usage` with `account: [all]` let the
  agent SELECT from data objects and invoke UDFs, stored procedures, and Streamlit apps in any
  database the user’s roles already allow. Databases that aren’t listed under `data write` stay
  read-only for the agent.
- **Writes only in a sandbox and personal databases:** `data write` on
  `databases: [SANDBOX_DB, USER$]` lets the agent write in the shared `SANDBOX_DB` database and in
  the session user’s personal database. `USER$` is a placeholder that resolves to that personal
  database at runtime, so one definition covers every user without listing `USER$<username>` by
  name. Writes anywhere else, including production databases, are denied even if the user’s roles
  would allow them.
- **Privileged roles blocked:** `blocked_roles` prevents ACCOUNTADMIN, SYSADMIN, and SECURITYADMIN
  from being used as the primary role, or activated as secondary roles, while the agent is active.
  If the current primary role inherits one of those roles, the inherited privileges remain. See
  [Role scopes](#label-agent-rss-role-scopes).
- **Role switching allowed:** `allow_role_switching: true` (the default) lets the agent switch among
  the user’s other assigned primary roles. Set this key to `false` if you want the session locked to
  the role that was active when the session opened.

The RSS never grants more than the user’s roles already allow. After you create the object, set
`AGENT_RESTRICTED_SESSION_SCOPE` on a session policy to the object’s fully qualified name, then
attach that policy to the account or to specific users.

#### Block privileged roles when an agent is active

Prevent elevated roles such as ACCOUNTADMIN, SYSADMIN, or SECURITYADMIN from being used as the
primary role, or activated as secondary roles, while an agent is active, even when the user holds
those roles. Blocking a role doesn’t remove privileges that a non-blocked primary role inherits
from it. For that behavior, see [Role scopes](#label-agent-rss-role-scopes).

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.no_privilege_escalation AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, object discovery, program usage]
      account: [all]
    - privileges: [data write]
      databases: [DEV_DB, SANDBOX_DB]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SYSADMIN, SECURITYADMIN, ORGADMIN]
  allow_role_switching: false
$$;

CREATE SESSION POLICY mydb.governance.no_privesc_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'MYDB.GOVERNANCE.NO_PRIVILEGE_ESCALATION';

ALTER ACCOUNT SET SESSION POLICY mydb.governance.no_privesc_policy;
```

#### Allow data work, block grant and object management

Allow read, sandbox write, and program usage, while leaving grant management and object management
implicitly denied.

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.data_operations_only AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, object discovery, program usage]
      account: [all]
    - privileges: [data write]
      databases: [SANDBOX_DB, DEV_DB]
role_scopes:
  blocked_roles: [ACCOUNTADMIN, SECURITYADMIN]
$$;

CREATE SESSION POLICY mydb.governance.data_ops_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'MYDB.GOVERNANCE.DATA_OPERATIONS_ONLY';

ALTER ACCOUNT SET SESSION POLICY mydb.governance.data_ops_policy;
```

#### Restrict access to approved databases

Limit what an agent can reach to databases approved for AI use. Databases that aren’t listed are
inaccessible while the agent is active, even if the user’s roles grant SELECT on them.

Copy code

```
CREATE RESTRICTED SESSION SCOPE mydb.governance.ai_approved_databases AS $$
privilege_scopes:
  allowed_privileges:
    - privileges: [data read]
      databases: [ANALYTICS_DB, REPORTING_DB, METRICS_DB]
    - privileges: [data read, data write]
      databases: [AGENT_SANDBOX_DB]
    - privileges: [program usage]
      databases: [ANALYTICS_DB, REPORTING_DB]
$$;

CREATE SESSION POLICY mydb.governance.ai_scope_policy
  AGENT_RESTRICTED_SESSION_SCOPE = 'MYDB.GOVERNANCE.AI_APPROVED_DATABASES';

ALTER ACCOUNT SET SESSION POLICY mydb.governance.ai_scope_policy;
```

Pair this with masking policies that use
`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` on sensitive columns within approved
databases. RSS controls which databases and operations the agent can reach; agent-aware masking
controls which column values are visible within those databases.

## Considerations

- An RSS is a ceiling on the user’s existing RBAC privileges. It never grants additional privileges.
- `AGENT_RESTRICTED_SESSION_SCOPE` on a session policy applies only when an agent is active
  (`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` returns `TRUE`). When no agent is
  active, the property is ignored. For the contexts that set this value, see
  [IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated).
- Session policies are evaluated for each action. If an agent becomes active during a session,
  Snowflake applies the RSS for actions the agent attempts while `IS_AGENT_ACTIVATED` is `TRUE`.
- If a user has a user-level session policy, that policy fully overrides the account-level policy
  for that user. The two aren’t merged.
- If the session policy doesn’t set `AGENT_RESTRICTED_SESSION_SCOPE`, no agent scope is applied.
  While an agent is active, the agent has the same access as the user.
- If a session policy references an RSS object by fully qualified name, Snowflake blocks
  [DROP RESTRICTED SESSION SCOPE](/sql-reference/sql/drop-restricted-session-scope) until you remove or update that reference.
- Once a RSS is active for agent activity in a session, it can’t be escalated. Close the session
  and open a new one to apply a different scope.
- `allowed_roles` and `blocked_roles` apply to both the primary role and any secondary roles. Use
  `allowed_secondary_roles` or `blocked_secondary_roles` when you want to restrict secondary roles
  only. A blocklist matches role names exactly. If a blocked role is in the hierarchy of the
  current primary role, the session still has the privileges that primary role inherits. For
  details, see [Role scopes](#label-agent-rss-role-scopes).
- RSS and agent-aware masking policies are complementary. RSS controls access scope; masking
  controls data visibility within that scope.
- For third-party agents, `IS_AGENT_ACTIVATED` returns `TRUE` when the connection goes through the
  Snowflake MCP Server or an OAuth security integration with `IS_AGENTIC = TRUE`. Agents that
  connect through REST APIs or SDKs with standard authentication (key pair or personal access token)
  and neither of those mechanisms currently activate the agent context, unless the session uses a
  `SERVICE_AGENT` user.
- The session policy RSS applies to agent-active sessions covered by the policy, regardless of
  client.

## Appendix: Predefined scope YAML

The following YAML shows the effective privilege shape of each Snowflake predefined scope. Use these
definitions when you need to understand or extend a built-in scope.

### SNOWFLAKE$DATA\_READ

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [data read]
      account:
        - all
```

### SNOWFLAKE$DATA\_READ\_PROGRAM\_USAGE

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, program usage]
      account:
        - all
```

### SNOWFLAKE$DATA\_READ\_WITH\_AI

Copy code

```
privilege_scopes:
  allowed_privileges:
    - privileges: [data read, object discovery]
      account:
        - all
    - privileges: [usage]
      object_types: [agent, mcp server, cortex search service]
      account:
        - all
```
