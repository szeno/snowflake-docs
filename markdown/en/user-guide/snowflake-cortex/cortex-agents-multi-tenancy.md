# Multi-tenancy for Cortex Agents

Multi-tenancy enables a single Cortex Agent to serve multiple tenants while enforcing data
isolation between them. You achieve tenant isolation by configuring session attributes in the
`variables` block in the `agent:run` API and pairing them with row access policies (RAP) on
your Snowflake tables. Before the agent executes any generated SQL, Snowflake sets the session
attributes you provide, and the row access policy filters rows based on those values.

This approach follows a shared responsibility model. Snowflake provides the tools — session
attributes and row access policies — and you are responsible for configuring them correctly to
enforce your tenant boundaries.

## How multi-tenancy works

When you call the `agent:run` API, you can include a `variables` block that defines one or
more immutable session attributes. The row access policy on your table references
these attributes to filter data for the current tenant.

The execution flow is:

1. You call an `agent:run` API with a `variables` block that includes tenant-specific values.
2. Before executing any generated SQL, the attributes are set on the Snowflake session.
3. The generated SQL runs in the session where the variables are active.
4. The row access policy on the table evaluates the session attributes and filters rows accordingly.

## Session attributes

The `variables` block supports immutable session attributes, configured using
`is_immutable_session_attribute: true`. Once the value of an attribute is set, it cannot be
modified by generated SQL, code execution, or tool invocation during the session. This ensures
the tenant context can’t be altered during the agent’s execution.

To configure session attributes in the `variables` block in the `agent:run` API, use the
following parameter:

| Property | Type | Description |
| --- | --- | --- |
| `is_immutable_session_attribute` | Boolean | Sets the variable as an immutable session attribute that can’t be modified during the session. |

Expand

Show lessSee more

## Configure variables in agent:run

Pass variables in the `agent:run` API to set tenant context for each invocation:

Copy code

```
POST /api/v2/databases/{database}/schemas/{schema}/agents/{agent_name}:run
```

Copy code

```
{
    "variables": {
        "region": {
            "value": "NORTH",
            "type": "string",
            "is_immutable_session_attribute": true
        }
    }
}
```

In this example, `region` is set as an immutable session attribute. The key is `region` and the
value is `NORTH`. The value is set before query execution, so the row access policy can reference
it. Session attributes persist for the duration of the interaction and cannot be overwritten.

## Row access policies with session attributes

To enforce tenant isolation, Snowflake strongly recommends using a session attribute in a row
access policy. The policy filters rows so each tenant sees only their own data.

**Create a row access policy**

The following example creates a row access policy that filters rows based on the `region`
session attribute:

Copy code

```
-- Create a row access policy that filters by the region session attribute
CREATE OR REPLACE ROW ACCESS POLICY rap_region_filter
  AS (region_col STRING) RETURNS BOOLEAN ->
    region_col = SYS_CONTEXT('SNOWFLAKE$SESSION_ATTRIBUTES', 'region');
```

Apply the policy to your table:

Copy code

```
-- Apply the row access policy to the sales table
ALTER TABLE db1.schema1.sales
  ADD ROW ACCESS POLICY rap_region_filter ON (region);
```

When the agent executes a query against the `sales` table, the row access policy evaluates the
`region` session attribute and returns only the rows where the `region` column matches the
value set in the `agent:run` call.

## Best practices

Follow these recommendations when configuring multi-tenancy with Cortex Agents:

- **Use immutable session attributes for row access policies.** Set
  `is_immutable_session_attribute: true` for any variable referenced by a row access policy.
  Immutable attributes can’t be modified by generated SQL or tool execution.
- **Scope variables to the narrowest level.** Set only the variables each invocation requires.
  Don’t pass variables that the agent doesn’t need for the current request.
- **Test your row access policies independently.** Verify that your row access policies filter
  correctly by testing them with `SET` statements outside the agent before deploying.

## Access control

The following table describes the privileges required for multi-tenancy configuration:

| Privilege | Object | Required for |
| --- | --- | --- |
| MODIFY | Agent | Configuring agent instructions with prompt variables |
| USAGE | Agent | Invoking the agent with session attributes |
| CREATE ROW ACCESS POLICY | Schema | Creating row access policies |
| ADD ROW ACCESS POLICY | Table | Applying a row access policy to a table |
| OWNERSHIP | Agent | Full control over the agent configuration |

Expand

Show lessSee more

## Limitations

The following limitations apply to multi-tenancy with Cortex Agents:

- **Session scope**: Session attributes persist for the duration of the interaction and cannot be
  overwritten.

Snowflake provides immutable session attributes and row access policies as tools for tenant
isolation. You are responsible for configuring these correctly to enforce your tenant boundaries.
