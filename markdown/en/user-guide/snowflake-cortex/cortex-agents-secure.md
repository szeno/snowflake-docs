# Secure agents

A secure agent is a Cortex Agent whose complete YAML specification is not visible to roles that have only USAGE privilege on the agent. This lets you grant invocation access without granting direct access to potentially business-sensitive configuration through SQL metadata and stage paths. This configuration can include tool definitions, MCP server bindings, orchestration instructions, and other proprietary information. Secure agents follow the same model as secure views, secure functions, and secure procedures in Snowflake.

## How secure agents work

When you mark an agent as secure, Snowflake applies a visibility rule to every surface that can return the agent specification so only the owner role can view the entire specification. The owner role is considered activated when the agent’s owner role is part of the activated role set for the current session. This matches secure view and secure function semantics: a role with MODIFY or USAGE on a secure agent but without the owner role activated cannot read the specification through any SQL or stage path.

The visibility rule applies to the following surfaces:

| Surface | Behavior for non-owner sessions |
| --- | --- |
| DESCRIBE AGENT | The `agent_spec` column returns NULL. |
| SHOW VERSIONS IN AGENT | Output depends on account configuration. See [Usage notes](#label-secure-agents-usage-notes). |
| `GET_DDL('CORTEX_AGENT', ...)` | The specification is omitted from the DDL output. |
| DESCRIBE AS RESOURCE (Snowsight) | `agentSpec` returns NULL. |
| Stage reads (`GET` / `LS`) | Requires OWNERSHIP privilege (owner role activated). USAGE alone is not sufficient. |

Expand

Show lessSee more

Note

Execution paths, including the REST API `agent:run` endpoint, [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex), and tasks that invoke an agent, load the specification using internal system context. Spec redaction applies only to customer-visible metadata surfaces, not to agent invocation.

## Create a secure agent

To create a secure agent, include the `SECURE` modifier or set the `SECURE` property to `TRUE` in [CREATE AGENT](/sql-reference/sql/create-agent):

Copy code

```
CREATE OR REPLACE SECURE AGENT my_sales_agent
  COMMENT = 'Production sales analyst.'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-6
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "RevenueAnalyst"
    - tool_spec:
        type: "cortex_search"
        name: "ProductSearch"
  tool_resources:
    RevenueAnalyst:
      semantic_view: "sales_db.public.revenue_model"
    ProductSearch:
      search_service: "sales_db.public.product_search"
  $$;
```

Note

If account sharing controls require shared agents to be secure, you cannot remove the `SECURE` designation from an agent that is currently in a share or Native App export. See [Sharing requirements](#label-secure-agents-sharing-requirements).

## Alter the secure status of an existing agent

You can mark an existing agent as secure, or remove the secure designation, using [ALTER AGENT](/sql-reference/sql/alter-agent).

Mark an agent as secure:

Copy code

```
ALTER AGENT my_agent SET SECURE = TRUE;
```

Remove the secure designation:

Copy code

```
ALTER AGENT my_agent SET SECURE = FALSE;
```

Important

Whether you can remove the secure designation from an agent in a share or Native App export depends on the account’s sharing controls. If those controls require the agent to remain secure, Snowflake returns error `093932` (`SHARED_AGENT_CANT_BE_UNSECURE`).

To remove the secure designation in that case, revoke the agent from all shares and from any application roles that grant it, then set `SECURE` to `FALSE`:

Copy code

```
REVOKE USAGE ON AGENT my_agent FROM SHARE my_data_share;
REVOKE USAGE ON AGENT my_agent FROM APPLICATION ROLE my_app_role;
ALTER AGENT my_agent SET SECURE = FALSE;
```

## Identify secure agents

[SHOW AGENTS](/sql-reference/sql/show-agents) includes an `is_secure` column. Secure agents show `true` in this column.

Copy code

```
SHOW AGENTS;
```

Example output (selected columns):

```
+-------------------+-----------+-----------+
| name              | owner     | is_secure |
|-------------------+-----------+-----------|
| MY_SALES_AGENT    | SYSADMIN  | true      |
| MY_OTHER_AGENT    | SYSADMIN  | false     |
+-------------------+-----------+-----------+
```

You can also confirm the secure designation in [GET\_DDL](/sql-reference/functions/get_ddl) output. For non-owner sessions, the output includes the `SECURE = TRUE` property and omits `FROM SPECIFICATION` and the specification body entirely.

Copy code

```
SELECT GET_DDL('CORTEX_AGENT', 'my_sales_agent');
```

Example output for a non-owner session:

Copy code

```
CREATE OR REPLACE AGENT MY_SALES_AGENT
  SECURE = TRUE
  COMMENT = 'Production sales analyst.';
```

## Sharing requirements

In accounts where secure agents are required for sharing, only secure agents can be added to shares or exported through Native Apps. Attempting to grant a non-secure agent to a share returns error `093931` (`SHARING_UNSECURE_AGENTS_NOT_SUPPORTED`).

This requirement exists because sharing multiplies the surfaces through which a specification can be read, including DESCRIBE and GET\_DDL in consumer accounts. Marking an agent secure before sharing ensures that spec redaction applies in all consumer contexts.

To share an agent, use the following workflow:

1. Create the agent with the `SECURE` modifier or `SECURE = TRUE` property, or run `ALTER AGENT <name> SET SECURE = TRUE`.
2. Add the agent to the share.
3. If you need to replace the agent definition, preserve the secure designation by using the `SECURE` modifier or setting `SECURE = TRUE`. Also specify `COPY GRANTS` to preserve explicit grants, including grants to shares.

Important

In accounts where secure agents are required for sharing, attempting to replace a shared agent with a non-secure definition returns error `093936` (`CANNOT_RECREATE_UNSECURE_SHARED_AGENT`). Preserve the secure designation on the replacement by using the `SECURE` modifier or setting `SECURE = TRUE`.

For more information about sharing agents, see [Share Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-sharing).

## Security model

The following table summarizes what each role can do with a secure agent:

| Role or privilege | Can invoke the agent | Can read the specification |
| --- | --- | --- |
| OWNERSHIP (owner role activated) | Yes | Yes: full specification on all surfaces. |
| USAGE only (owner role not activated) | Yes | No: specification metadata is redacted according to the surface and output configuration; stage reads are blocked. |
| MODIFY (owner role not activated) | No | No: spec redacted the same as USAGE. |
| Consumer (share or native app) | Yes | No: spec is redacted in consumer account context. |

Expand

Show lessSee more

## Access control

The following privileges are relevant to secure agents. Privilege requirements for invocation and DDL are unchanged from standard agents. The secure designation affects only spec visibility.

| Privilege | Object | Required for |
| --- | --- | --- |
| CREATE AGENT | Schema | Creating a new permanent agent. Not required for temporary agents. |
| OWNERSHIP | Agent | Replacing an existing agent with `CREATE OR REPLACE`; reading the specification of a secure agent; stage reads of the spec file. Also sufficient to alter the agent. |
| USAGE | Agent | Invoking the agent via the REST API or [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex). Does not grant spec visibility on a secure agent. |
| MODIFY | Agent | Altering agent properties, including setting `SECURE` to `TRUE` or `FALSE`. Does not grant spec visibility on a secure agent. `ALTER AGENT` requires OWNERSHIP or MODIFY. |

Expand

Show lessSee more

## Usage notes

- Secure agents are consistent with `SECURE VIEW`, `SECURE FUNCTION`, and `SECURE PROCEDURE` semantics. The owner-role check uses the activated role set for the current session, not a static privilege grant.
- Agent invocation via the REST API, [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex), or tasks is not affected by the secure designation. The specification is loaded with internal system context at runtime.
- [DESCRIBE AGENT](/sql-reference/sql/desc-agent) returns NULL in the `agent_spec` column for non-owner sessions on secure agents. The agent name, owner, model, and other profile fields remain visible.
- `SHOW VERSIONS IN AGENT` output depends on the account’s output configuration. When specification output is enabled, non-owner sessions receive an empty `agent_spec` and a NULL `spec_file_path`. When specification output is disabled, the output doesn’t include `agent_spec`, and that setting doesn’t redact `spec_file_path`.
- Stage reads, including direct downloads of `agent_spec.yaml` from the agent versioned stage, require the owner role to be activated. A role with only USAGE cannot retrieve the spec file.
- Permanent secure agents support all standard versioning operations (`COMMIT`, `VERSION$N`, aliases). Versioning behavior is unchanged; only spec visibility is affected. Temporary agents do not support those operations. See [Working with temporary agents](/user-guide/snowflake-cortex/cortex-agents-temporary).
- Snowflake recommends using the `SECURE` modifier or setting `SECURE = TRUE` when granting USAGE on agents whose tool configurations, semantic model references, or orchestration instructions are proprietary.

## Error reference

| Error code | Message | Cause | Resolution |
| --- | --- | --- | --- |
| `093931` | `SHARING_UNSECURE_AGENTS_NOT_SUPPORTED` | Attempt to add a non-secure agent to a share when secure agents are required for sharing. | Run `ALTER AGENT <name> SET SECURE = TRUE` before adding the agent to a share. |
| `093932` | `SHARED_AGENT_CANT_BE_UNSECURE` | Attempt to set `SECURE = FALSE` on an agent that sharing controls require to remain secure. | Revoke the agent from all shares and from any application roles that grant it, or keep `SECURE` set to `TRUE`. |
| `093936` | `CANNOT_RECREATE_UNSECURE_SHARED_AGENT` | Attempt to replace a shared agent with a non-secure definition when secure agents are required for sharing. | Preserve the secure designation by using the `SECURE` modifier or setting `SECURE = TRUE`. |

Expand

Show lessSee more

## Limitations

- Partial spec visibility (selectively exposing specific sections of the specification to non-owner roles) is not supported. The specification is either fully visible (owner role activated) or fully redacted.
- The secure designation prevents direct retrieval of the agent specification through metadata surfaces such as `DESCRIBE AGENT`, `GET_DDL`, `SHOW VERSIONS IN AGENT`, and stage reads. It does not guarantee that a user who can invoke the agent cannot use conversational prompts or prompt injection techniques to infer or elicit information about the agent’s instructions, tools, or resources.
- The `SECURE` modifier and property are supported for Cortex Agent objects only. [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) artifacts and Agent Server objects are out of scope.
- Depending on account sharing controls, you might need to revoke an agent from shares and Native App exports before you can remove its secure designation.
- Replication copies the secure designation. The visibility rules apply in the target account using that account’s activated role context.

### Reduce the risk of specification disclosure

When you design a secure agent, assume that information available to the model might be disclosed in an agent response. Prompt instructions and filtering can reduce the risk of disclosure, but they cannot eliminate it.

Use the following defense-in-depth practices:

- Don’t include secrets, credentials, or other sensitive values in agent instructions, tool descriptions, or other specification fields.
- Enforce authorization with Snowflake access control, not with agent instructions. Grant the agent and its tools only the privileges required for their intended tasks.
- Consider instructing the agent not to discuss its configuration. Treat this instruction as a mitigation, not as an access control.
- Enable [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails) to detect and mitigate prompt injection and jailbreak attempts. Guardrails reduce risk but don’t guarantee that specification details cannot be disclosed.
- Monitor agent conversations, traces, and Guardrails activity for attempted or successful disclosure. For more information, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor) and [Monitor guardrail activity](/user-guide/snowflake-cortex/cortex-ai-guardrails#label-cortex-ai-guardrails-monitor).

## Examples

### Create and verify a secure agent

Create a secure agent and confirm the designation appears in SHOW AGENTS and GET\_DDL output:

Copy code

```
-- Create the secure agent
CREATE OR REPLACE SECURE AGENT my_sales_agent
  COMMENT = 'Production sales analyst.'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-6
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "RevenueAnalyst"
  tool_resources:
    RevenueAnalyst:
      semantic_view: "sales_db.public.revenue_model"
  $$;

-- Verify is_secure = true
SHOW AGENTS LIKE 'my_sales_agent';

-- Confirm GET_DDL shows SECURE = TRUE
SELECT GET_DDL('CORTEX_AGENT', 'my_sales_agent');
```

### Grant invocation access without spec visibility

Grant a role the ability to invoke the agent without granting direct access to the specification through metadata surfaces:

Copy code

```
-- Grant invocation access to an analyst role
GRANT USAGE ON AGENT my_sales_agent TO ROLE analyst_role;

-- The analyst_role can invoke the agent but cannot read the spec:
-- DESCRIBE AGENT my_sales_agent  ->  agent_spec is NULL
-- GET_DDL(...)                   ->  specification omitted from output
```

### Convert an existing agent to secure and add it to a share

Mark an existing agent secure, then add it to a share:

Copy code

```
-- Step 1: Mark the agent secure
ALTER AGENT my_agent SET SECURE = TRUE;

-- Step 2: Add to a share
GRANT USAGE ON AGENT my_agent TO SHARE my_data_share;
```
