# Call a Snowflake CoWork profile from the Cortex Agents API

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Call a profile with the
[Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-data-agents-run-rest-api)
or [DATA\_AGENT\_RUN](/sql-reference/functions/data_agent_run-snowflake-cortex). It doesn’t need to be
attached to the Snowflake CoWork object.

## Before you begin

- Each `agent_router` tool needs a `tool_resources` entry keyed by its tool name, or calls fail
  with error `399518`. CoWork Admin adds the entry when it creates or saves a profile. If you
  created the profile with SQL, or calls fail with `399518`, add it yourself: `subagents: []` is
  enough, or list agents to route to, as in step 3 of
  [Migrate manually](/user-guide/snowflake-cortex/snowflake-cowork/set-up-cowork-profile-routing#label-cowork-profiles-migrate-manual).
  The list also controls routing in Snowflake CoWork. For how the list affects access, see
  [Choose which agents a profile routes to](/user-guide/snowflake-cortex/snowflake-cowork/set-up-cowork-profile-routing#label-cowork-profiles-routing-scope).
- The calling role needs one of the
  [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control)
  for Cortex Agents, plus `USAGE` on the `SNOWFLAKE_INTELLIGENCE` database, the
  `SNOWFLAKE_INTELLIGENCE.PROFILES` schema, and the profile.

## Call the profile

Set `$SNOWFLAKE_ACCOUNT_BASE_URL` to your account URL and `$PAT` to your
[programmatic access token](/developer-guide/snowflake-rest-api/authentication).
Replace `<profile_name>` and `<role_name>`:

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/SNOWFLAKE_INTELLIGENCE/schemas/PROFILES/agents/<profile_name>:run" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $PAT" \
  --header 'X-Snowflake-Role: <role_name>' \
  --data '{
    "stream": false,
    "messages": [
      { "role": "user", "content": [{ "type": "text", "text": "How many deals closed last quarter?" }] }
    ]
  }'
```

From SQL:

Copy code

```
SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'SNOWFLAKE_INTELLIGENCE.PROFILES.<profile_name>',
  $${ "messages": [{ "role": "user", "content": [{ "type": "text", "text": "How many deals closed last quarter?" }] }] }$$
)) AS response;
```

## See which agent answered

Each time the profile routes the question, the response includes a `tool_use` item of type
`agent_router`. In its `input`, `subagent_name` is the agent that received the question, as in the
following trimmed example:

Copy code

```
{
  "type": "tool_use",
  "tool_use": {
    "type": "agent_router",
    "input": { "subagent_name": "MY_DB.MY_SCHEMA.SALES_AGENT", "display_name": "Sales" }
  }
}
```

With `orchestration.tool_not_accessible: accept`, inaccessible subagents are skipped with warning
`399569`. With `reject`, they fail the request. For more information, see
[Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

## Call the profile from an MCP client

To reach a profile from an MCP client such as Claude, expose it as a `CORTEX_AGENT_RUN` tool on an
MCP server. The profile is an agent, so you set `identifier` to its fully qualified name:

Copy code

```
CREATE OR REPLACE MCP SERVER <database_name>.<schema_name>.<server_name>
  FROM SPECIFICATION $$
  tools:
    - title: "Company profile"
      name: "company_profile"
      type: "CORTEX_AGENT_RUN"
      identifier: "SNOWFLAKE_INTELLIGENCE.PROFILES.<profile_name>"
      description: "Use this profile for questions about company data."
  $$;
```

An MCP call has the same requirement as an API call. The profile needs a `tool_resources` entry with
a `subagents` list, as described earlier on this page. The role that the client connects with needs
USAGE on the MCP server and on the profile. For the full list of grants, see
[Access control](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-access-control).
