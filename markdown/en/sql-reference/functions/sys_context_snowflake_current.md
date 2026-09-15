Categories:
:   [Context functions](/sql-reference/functions-context) (General)

# SYS\_CONTEXT (SNOWFLAKE$CURRENT namespace)

Returns information about the current execution context in which the function is called. The current execution context can
differ from the session context when the function is called inside an owner’s rights executable or during an agent invocation.

You can call this function in the following contexts:

- You can call this function directly in the current session.
- You can run a caller’s rights executable (for example, a caller’s rights stored procedure) that calls this function.
- You can run an owner’s rights executable (for example, an owner’s rights stored procedure) that calls this function.

Unlike the [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session), calling this function in
an owner’s rights executable doesn’t require the READ SESSION privilege.

In any other context, the function returns NULL.

See also:
:   [SYS\_CONTEXT](/sql-reference/functions/sys_context) ,
    [SYS\_CONTEXT (SNOWFLAKE$SESSION namespace)](/sql-reference/functions/sys_context_snowflake_session) ,
    [IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated) ,
    [IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_database_role_activated) ,
    [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_role_activated) ,
    [Restricted Session Scope for agents](/user-guide/restricted-session-scope)

## Syntax

**Syntax for retrieving properties:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$CURRENT' ,
  '<property>'
)
```

**Syntax for calling functions:**

Copy code

```
SYS_CONTEXT(
  'SNOWFLAKE$CURRENT' ,
  '<function>' [ , '<argument>' , ... ]
)
```

## Arguments

`'SNOWFLAKE$CURRENT'`
:   Specifies that you want to retrieve a property or call a function to return information about the current execution context.

`'property'`
:   Name of the property that you want to retrieve. You can specify the following properties:

    | Property | Description |
    | --- | --- |
    | `AGENT_TYPE` | Returns the type of agent that is active in the current execution context. Possible values:     - `CORTEX_AGENT`: A persistent, named [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents).   - `CORTEX_LITE_AGENT`: A stateless, on-demand agent invoked through the [REST API](/developer-guide/snowflake-rest-api/cortex-lite-agent/cortex-lite-agent-introduction) or via a Snowflake CoCo client.   - `EXTERNAL_AGENT`: An external agent using a [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) user type or a [custom OAuth integration](/user-guide/oauth-custom#configuring-agent-sessions) configured with `IS_AGENTIC = TRUE`.     Returns NULL if no agent is active in the current execution context. This returns the same value as the `agent_type` column in [QUERY\_HISTORY](/sql-reference/account-usage/query_history). |
    | `IS_AGENT_ACTIVATED` | Returns `'TRUE'` if an agent is active in the current execution context; otherwise, returns `'FALSE'`. An agent is active when:     - A Snowflake first-party agent is executing the query (a named [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents), a stateless [lite agent](/developer-guide/snowflake-rest-api/cortex-lite-agent/cortex-lite-agent-introduction) invoked via the REST API or a Snowflake CoCo client, or a query through Snowflake CoWork)   - An external agent connects through a managed MCP server   - The session was opened by a [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) user   - The session uses a [custom OAuth integration](/user-guide/oauth-custom#configuring-agent-sessions) configured with `IS_AGENTIC = TRUE`     Use this property in masking policies and row access policies to restrict data access when an agent is running a query. For more details, see [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated). |

    Expand

    Show lessSee more

`'function'`
:   Name of the function that you want to call. When called via the SNOWFLAKE$CURRENT namespace, IS\_ROLE\_ACTIVATED and
    IS\_DATABASE\_ROLE\_ACTIVATED check the current execution context rather than the session.

    You can call the following functions:

    - [IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated)
    - [IS\_DATABASE\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_database_role_activated)
    - [IS\_ROLE\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_role_activated)

`'argument' [ , ... ]`
:   Arguments to pass to the function that you want to call.

    [IS\_ROLE\_ACTIVATED](/sql-reference/functions/is_role_activated) accepts one or more role names and returns `'TRUE'` if any of
    the roles is activated. You can specify multiple roles only when each role is a constant value, such as a string literal. When
    the role is an expression that isn’t a constant, you can specify only a single role.

## Returns

The function returns a VARCHAR value or NULL:

- The return value depends on
  [the property that you are retrieving](/sql-reference/functions/sys_context_snowflake_current#label-sys-context-snowflake-current-property) or
  [the function that you are calling](/sql-reference/functions/sys_context_snowflake_current#label-sys-context-snowflake-current-function).
- If you call SYS\_CONTEXT with the SNOWFLAKE$CURRENT namespace outside of
  [any of the supported contexts](/sql-reference/functions/sys_context_snowflake_current#label-sys-context-snowflake-current-contexts), the function returns NULL.

2026\_06 behavior change bundle

When the [2026\_06 behavior change bundle](/release-notes/bcr-bundles/2026_06_bundle) is [enabled in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-check-status), `SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_ROLE_ACTIVATED', '<role>')` and
`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')` return `BOOLEAN`. Other properties and
functions in this namespace continue to return `VARCHAR`.

Existing casts, such as `::BOOLEAN` or `::NUMBER`, continue to work unchanged.

For the return type of every property and function by namespace, see
[SYS\_CONTEXT return types](/sql-reference/functions/sys_context#label-sys-context-returns).

## Usage notes

- The SNOWFLAKE$CURRENT namespace returns values for the innermost execution context. Inside an owner’s rights stored procedure,
  for example, this reflects the owner’s context, not the caller’s session context. Use the
  [SNOWFLAKE$SESSION namespace](/sql-reference/functions/sys_context_snowflake_session) if you need session-level values instead.
- The following table summarizes when SNOWFLAKE$CURRENT and SNOWFLAKE$SESSION return different values:

  | Scenario | SNOWFLAKE$CURRENT | SNOWFLAKE$SESSION |
  | --- | --- | --- |
  | Direct query in the session | Session context | Session context |
  | Inside a caller’s rights stored procedure | Session context | Session context |
  | Inside an owner’s rights stored procedure | Owner’s context (activated roles reflect the owner; no READ SESSION required) | Session context (requires READ SESSION privilege) |
  | During an agent invocation | Agent’s execution context (agent properties are populated) | Session context of the invoking user |

  Expand

  Show lessSee more
- To simulate the values of functions in this namespace when testing policies, use the corresponding
  [POLICY\_CONTEXT arguments](/sql-reference/functions/policy_context#label-policy-context-examples). For example, use
  `SNOWFLAKE$CURRENT_ACTIVATED_ROLES` to simulate the result of IS\_ROLE\_ACTIVATED.
- If you are specifying the function call in a double-quoted string in a shell, escape the `$` character with a backslash
  (`\`) so that `$CURRENT` is not interpreted as a shell variable.

## Examples

The following examples demonstrate how to retrieve agent properties and check role activation in the current execution context:

- [Retrieving the agent type in the current context](#label-sys-context-snowflake-current-example-agent-type)
- [Checking role activation in the current context](#label-sys-context-snowflake-current-example-role)
- [Checking database role activation in the current context](#label-sys-context-snowflake-current-example-db-role)

### Retrieving the agent type in the current context

The following example returns the type of agent that is running the current query, or NULL if no agent is active:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$CURRENT', 'AGENT_TYPE');
```

### Checking role activation in the current context

The following example checks whether a role is activated in the current execution context (which may differ from the session
context inside an owner’s rights executable):

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_ROLE_ACTIVATED', 'analyst')::BOOLEAN;
```

### Checking database role activation in the current context

The following example checks whether a database role is activated in the current execution context:

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_DATABASE_ROLE_ACTIVATED', 'ANALYST_ROLE')::BOOLEAN;
```
