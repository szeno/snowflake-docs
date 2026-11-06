# Multi-agent orchestration with a CoWork profile

[Preview Feature](/release-notes/preview-features) — Open

This recipe uses features in preview: Snowflake CoWork profiles and the `agent_router` tool.

One Snowflake CoWork profile routes to specialist agents with the agent\_router tool, so Snowflake grants decide which specialist each user reaches.

|  |  |
| --- | --- |
| Stage | Build, Secure |
| Topics | Cortex Agents, Semantic Views |
| Status | Preview |
| Time to complete | 60min |
| Edition | Enterprise |
| Regions | Any region with Cortex Agents and claude-sonnet-4-6 (directly or through cross-region inference) |
| Privileges | ACCOUNTADMIN for 01\_setup.sql, the persona key-pair ALTER USER statements in Verify, and 99\_teardown.sql; everything else runs as COOKBOOK\_MULTI\_AGENT\_ADMIN |
| Related skills | `check-agent-access` ([Snowflake-Labs/coco-skills](https://github.com/Snowflake-Labs/coco-skills)) |
| Last verified | 2026-10-04 |
| Authors | Bala Krishnamoorthy, Parker Erickson |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration/code) or download [multi-agent-orchestration.zip](/static/samples/cortex-ai-cookbook/multi-agent-orchestration.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/multi-agent-orchestration/code#label-cookbook-multi-agent-orchestration-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Build one Snowflake CoWork profile that routes each question to a specialist agent (sales or support), where Snowflake grants, not prompt instructions, decide which specialist a user can reach and which rows the specialist returns. You end with two specialist agents, one profile with an `agent_router` tool, one fail-closed row access policy, persona users that prove the boundary, and a pinned-version evaluation of routing quality.

## When to use this

Start with one agent and split only for ownership. Accuracy is roughly the same with one agent or several, and each routed question adds latency and cost. Before adding an agent for a team, give it its own semantic view, search service, or skill on the existing agent.

Use a profile with specialist agents when you need one entry point and at least one of these:

- Different users must reach different specialists, and that must be enforced by the platform.
- Each domain needs its own instructions, tools, and budget, often owned by different teams.
- Clients (CoWork, REST apps, MCP clients) should all see one agent instead of choosing among several.

When not to use it:

- One agent with several tools covers the use case. That is simpler, cheaper, and keeps native chart and table output. Start there, with the semantic views and tools its users need attached to that one agent. The same applies to [Snowflake CoWork profiles](/developer-guide/cortex-ai-cookbook/scoping-agentic-implementations#snowflake-cowork-profiles).
- You only want to reuse another agent’s tool definitions. Use `agent_toolset`, which copies the tools into one agent at run time.
- Separate agents per role, with no single entry point, are acceptable. Grants alone then give you the boundary with no profile.

If you split, keep tools that are used together in the same agent.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/multi-agent-orchestration/diagram-a9f5b99f.svg)](/static/images/cortex-ai-cookbook/multi-agent-orchestration/diagram-a9f5b99f.svg)

- **Routing is a built-in tool.** The profile is an agent with one `agent_router` tool, created in the recipe’s own schema next to the specialists; a profile can live in any schema. Its `tool_resources` list the specialist agents in a `subagents` field. Each specialist runs as a real agent with its own instructions, model, tools, and budget. `agent_router` and profiles are in preview and not yet generally available.
- **The caller’s role carries through.** With `orchestration.tool_not_accessible: accept`, the profile skips any specialist the caller lacks USAGE on, with warning `399569`, and its instructions turn that into a refusal.
- **Four layers of grants.** USAGE on the profile (anyone may ask), USAGE on each specialist (the boundary), SELECT on the specialist’s semantic view and base table (the specialist’s tools also run as the caller), and a row access policy inside the sales domain.
- **One fail-closed row access policy.** `SALES_THEATER_POLICY` looks `CURRENT_ROLE()` up in an entitlements table. A role with no row sees no rows.
- **Routing is measured, not assumed.** A model follows the profile’s instructions and the specialist descriptions to choose a specialist, so the choice can vary between runs. Each routed response names the specialist in `subagent_name`, and an evaluation with judges pinned to `v3` tells you how often answers are right.

### Which role does an agent run use?

Cortex Agents authorize a run against the calling user’s **default role**, and the user needs a default warehouse the default role can use. How that plays out per surface:

| Surface | Role used for the run | Notes |
| --- | --- | --- |
| Snowsight and Snowflake CoWork | Default role | CoWork starts the session on the default role and warehouse. |
| Agent REST API (`:run`) | Default role, unless the request sets `X-Snowflake-Role` | The header lets an app pick a role the user has been granted. |
| `DATA_AGENT_RUN` from SQL with key-pair (JWT) auth | The session’s current role, in testing | This differs from the access-control docs and from the `399513` message, which both say the default role. A persona that ran `USE ROLE PUBLIC` was denied, and a user whose default role was PUBLIC reached the agent after `USE ROLE` to an entitled role. Do not rely on either; test with users whose default role is the persona role and run no `USE ROLE`. |
| Agent evaluations | The role that runs the evaluation | Evaluations do not impersonate other users. |

Expand

Show lessSee more

Test the boundary as a user whose default role is the persona role, and don’t switch roles in that session. Running the questions yourself after `USE ROLE` doesn’t test what REST and CoWork users get, because those surfaces use the default role.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Enterprise edition or higher | Row access policies |
| Cortex Agents and `claude-sonnet-4-6` | Directly or through cross-region inference |
| Snowflake CoWork profiles (preview, not yet GA) | The account must have profiles and `agent_router` enabled. The profile lives in the recipe database, so teardown removes it with the database |
| `ACCOUNTADMIN` | Only for `01_setup.sql` (roles, users, warehouse, database, `EXECUTE TASK`), the `ALTER USER ... SET RSA_PUBLIC_KEY` statements in Verify, and `99_teardown.sql` |
| Snowflake CLI or a Snowsight worksheet | CLI runs use `snow sql -f <file>` |
| `openssl` | Only to create key pairs for the persona users in Verify |

Expand

Show lessSee more

## Quickstart

1. `sql/01_setup.sql` as `ACCOUNTADMIN`: database, warehouse, `COOKBOOK_MULTI_AGENT_ADMIN`, three persona roles, and three persona service users.
2. `sql/02_data.sql`: synthetic sales and support data.
3. `sql/03_semantic_views.sql`: one semantic view per specialist.
4. `sql/04_row_access_policy.sql`: entitlements table and the fail-closed policy.
5. `sql/05_agents.sql`: two specialists and the profile.
6. `sql/06_grants.sql`: the persona boundary. Re-run after any re-run of 05.
7. `sql/07_routing_eval.sql`: starts a routing evaluation.
8. Verify as the persona users (below).

Scripts 02 to 07 run as `COOKBOOK_MULTI_AGENT_ADMIN`. Every script starts with a `SET` block. Object names are fixed: the same names appear as literals inside `$$` bodies (agent specifications, semantic view DDL, evaluation YAML) and in teardown, so don’t rename them. The orchestration model lives in the agent specifications in `05`; change it there if `claude-sonnet-4-6` is not available to you.

## Walkthrough

### The profile

The profile’s only tool is the router, and its `tool_resources` entry, keyed by the tool’s name, lists the specialists:

Copy code

```
tools:
  - tool_spec:
      type: agent_router
      name: router
tool_resources:
  router:
    subagents:
      - name: COOKBOOK_MULTI_AGENT.APP.SALES_AGENT
        display_name: Sales
        description: >-
          New bookings, targets, attainment, and pipeline by fiscal quarter,
          theater, and territory. Not for product support.
        source:
          type: DATA_AGENT
          fqn: COOKBOOK_MULTI_AGENT.APP.SALES_AGENT
          sample_questions: []
```

The description is what the router reads when it chooses, so say what each specialist covers and what it does not. Its instructions tell it to route both parts of a cross-domain question, to rewrite follow-ups as self-contained questions (specialists do not see the conversation), and to refuse any part no accessible specialist covers. Its specification is the same for every persona.

### The boundary

`06_grants.sql` is the whole access-control surface:

Copy code

```
-- Everyone may open the front door
GRANT USAGE ON AGENT IDENTIFIER($profile) TO ROLE IDENTIFIER($support_role);
-- Only sales personas may run the sales specialist and read its data
GRANT USAGE  ON AGENT SALES_AGENT                 TO ROLE IDENTIFIER($sales_emea);
GRANT SELECT ON SEMANTIC VIEW SALES_SEMANTIC_VIEW TO ROLE IDENTIFIER($sales_emea);
GRANT SELECT ON TABLE SALES_BOOKINGS              TO ROLE IDENTIFIER($sales_emea);
REVOKE USAGE ON AGENT SALES_AGENT FROM ROLE IDENTIFIER($support_role);
```

Reaching the profile also needs USAGE on its database and schema, which `06` grants. A persona without USAGE on a specialist still reaches the profile; the run skips that specialist with warning `399569` instead of failing. Set `tool_not_accessible: reject` if you would rather fail the whole request.

### The row access policy

Copy code

```
ALTER ROW ACCESS POLICY SALES_THEATER_POLICY SET BODY ->
  EXISTS (
    SELECT 1 FROM COOKBOOK_MULTI_AGENT.APP.SALES_ENTITLEMENTS e
    WHERE e.ROLE_NAME = CURRENT_ROLE()
      AND (e.THEATER = 'ALL' OR e.THEATER = theater_col)
  );
ALTER TABLE SALES_BOOKINGS DROP ALL ROW ACCESS POLICIES;
ALTER TABLE SALES_BOOKINGS ADD ROW ACCESS POLICY SALES_THEATER_POLICY ON (THEATER);
```

The policy is created once with a `FALSE` body and updated with `SET BODY`, so re-runs never need to detach it. `DROP ALL ROW ACCESS POLICIES` before `ADD` guarantees the table has exactly one policy. Inside an agent run, `CURRENT_ROLE()` is the role the run executes under (for these users, their default role).

The sales table is stored at one grain (territory by quarter), so `SUM` is always correct. If your table mixes detail rows with pre-aggregated roll-ups, fix that first: see [mixed-grain data and verified queries](/developer-guide/cortex-ai-cookbook/mixed-grain-and-verified-queries).

### The routing evaluation

`07_routing_eval.sql` loads five questions with expected answers, creates a dataset, writes the config to a stage with `COPY INTO`, and starts a run:

Copy code

```
metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
```

Pinning `v3` keeps scores comparable between runs. For the full evaluation workflow see [agent evaluations](/developer-guide/cortex-ai-cookbook/agent-evaluations).

### Optional: show the profile in Snowflake CoWork

The API reaches the profile without this step. To make it selectable in CoWork, attach it to the CoWork object. This changes an account-level object, so coordinate it with your account admin:

Copy code

```
USE ROLE ACCOUNTADMIN;
ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT
  ADD AGENT COOKBOOK_MULTI_AGENT.APP.COOKBOOK_MULTI_AGENT_PROFILE;
GRANT USAGE ON SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT
  TO ROLE COOKBOOK_MULTI_AGENT_SALES_EMEA;
```

The persona users in this recipe are `TYPE = SERVICE` and cannot sign in to the UI. To try it in CoWork, provision person users (for example through your identity provider) with the same `DEFAULT_ROLE` and `DEFAULT_WAREHOUSE`.

## Verify

`04_row_access_policy.sql` ends with `POLICY_CONTEXT` checks. Expected: 44 rows for the admin, 16 rows (EMEA only) for `COOKBOOK_MULTI_AGENT_SALES_EMEA`, 0 rows for `COOKBOOK_MULTI_AGENT_SUPPORT`.

To test as the personas, give each persona user a key pair and run the same question as each user:

Copy code

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out sales_emea.p8 -nocrypt
openssl rsa -in sales_emea.p8 -pubout | grep -v '^-----' | tr -d '\n'   # paste into the ALTER USER below
```

Copy code

```
-- as ACCOUNTADMIN, once per persona user
ALTER USER COOKBOOK_MULTI_AGENT_SALES_EMEA_USER SET RSA_PUBLIC_KEY = '<public key>';
```

Copy code

```
snow sql -x --account <account_identifier> --user COOKBOOK_MULTI_AGENT_SALES_EMEA_USER \
  --authenticator SNOWFLAKE_JWT --private-key-file sales_emea.p8 -q "
SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_MULTI_AGENT.APP.COOKBOOK_MULTI_AGENT_PROFILE',
  \$\${\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"What were total new bookings in FY25-Q4 by theater?\"}]}]}\$\$)) AS response"
```

The response’s `content` holds the answer, a `tool_use` item of type `agent_router` whose `input.subagent_name` names the specialist that answered, and a `warnings` entry with code `399569` for each specialist the persona can’t use, on every run, whether or not the question needed it.

Expected answers to “What were total new bookings in FY25-Q4 by theater?”:

| User | Answer |
| --- | --- |
| `..._SALES_GLOBAL_USER` | Americas $59.6M, EMEA $38.4M, APAC $22.1M, total $120.0M |
| `..._SALES_EMEA_USER` | EMEA $38.4M only (the row access policy removed the other theaters) |
| `..._SUPPORT_USER` | “This type of question is not available at your access level…”, with warning `399569` for `SALES_AGENT` |

Expand

Show lessSee more

A cross-domain question (“What was total new bookings in FY25-Q4, and how do I fix a 401 error from the API?”) returns the part each persona is entitled to and a refusal for the other part.

Evaluation results, once `EXECUTE_AI_EVALUATION('STATUS', ...)` reports completion:

Copy code

```
SELECT METRIC_NAME, ROUND(AVG(EVAL_AGG_SCORE), 2) AS avg_score, COUNT(*) AS n
FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'COOKBOOK_MULTI_AGENT', 'APP', 'COOKBOOK_MULTI_AGENT_PROFILE', 'CORTEX AGENT', 'routing-baseline'))
GROUP BY METRIC_NAME;
```

Expect one row per metric with `n = 5`. Look at low-scoring inputs with `METRIC_CALLS[0]:explanation` before changing instructions.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| Boundary “passes” for every question when you test it | You ran the questions yourself; the run authorized against your default role | Test as the persona users, as in Verify |
| Specialist answers “permissions issue” for a sales persona | The persona has SELECT on the semantic view but not on the base table; Cortex Analyst’s generated SQL reads the table as the caller | Grant SELECT on `SALES_BOOKINGS` (06 does) |
| The profile says it has no agent to route to | A `subagents` entry is missing `name`, `display_name`, `description`, or `source`; one incomplete entry drops the whole list without an error | Give every entry all four fields, with `name` and `source.fqn` the same |
| Error `399518` on every call | The `agent_router` tool has no `tool_resources` entry keyed by its name | Add the entry under the router tool’s `name` (`router` here) |
| A persona can’t reach the profile | It needs USAGE on the profile, its schema, and its database; granting the agent alone breaks the chain | Grant all three levels (06 does) |
| `syntax error ... unexpected 'COMMENT'` (or `'PROFILE'`) on `CREATE OR REPLACE AGENT` | `COPY GRANTS` placed before `COMMENT` or `PROFILE`. This differs from the published syntax in [CREATE AGENT](/sql-reference/sql/create-agent), which lists `COPY GRANTS` first; that order fails when it is followed by `COMMENT` or `PROFILE` | Put `COPY GRANTS` immediately before `FROM SPECIFICATION`, after `COMMENT` and `PROFILE`, as `05` does. Grants are copied with that order |
| Personas reach nothing after re-running a script | An object was replaced without `COPY GRANTS`, or a table was recreated | Re-run `06_grants.sql`. The scripts use `COPY GRANTS`, `CREATE OR ALTER`, and `INSERT OVERWRITE` to avoid this |
| A user with several roles sees an unexpected slice | The policy keys on `CURRENT_ROLE()` only; role hierarchy is not followed | Add an entitlement row per role that should see data, or switch to `IS_ROLE_IN_SESSION` if you want hierarchy and secondary roles to count |
| Follow-up questions lose context | Specialists receive only the router’s `query`, not the conversation | The profile’s instructions rewrite follow-ups as self-contained questions; check `query` in the `agent_router` tool input |
| A refusal names the specialist the user can’t use | The `399569` warning reaches the profile with the specialist’s name and description, and the model repeats them; an instruction not to did not stop it in testing | Write each specialist’s `display_name` and `description` as if every user can read them |
| Slow or costly answers | Each routed question runs the profile and at least one specialist | Budget each agent separately; token budgets cover orchestration only, not tool tokens. For usage and cost by agent, see [AI usage and cost attribution](/developer-guide/cortex-ai-cookbook/ai-usage-cost-attribution) |
| Edited questions in `ROUTING_EVAL_INPUT` are not evaluated | The dataset is a snapshot taken when it was created; 07 creates it once | Use a new dataset name in 07 (and in the YAML `source_metadata`) after changing the input table |
| Evaluation scores do not reflect persona behavior | Evaluations run as the role that starts them and cannot pass session attributes | Evaluate routing and answer quality as the admin; test the boundary with persona users |

Expand

Show lessSee more

## Teardown

Run `sql/99_teardown.sql` as `ACCOUNTADMIN`. It drops the database (profile, specialists, policy, tables, stage, evaluation dataset and runs), the warehouse, the three persona users, and the four roles. If you ran the optional CoWork step, run the `ALTER SNOWFLAKE INTELLIGENCE ... DROP AGENT` statement at the top of the teardown file first. Delete any local `.p8` key files you created.

## Adapt this recipe

Keep these, so a customized version keeps the recipe’s security model:

- Least privilege: `ACCOUNTADMIN` only for the scripts listed under Privileges; everything else runs as the recipe’s own role.
- No grants to `PUBLIC`.
- Row access policies fail closed: a role with no entitlement sees no rows. Keep each policy attached when you rename or add tables, and add entitlements for new roles instead of widening the policy.
- Service users stay `TYPE = SERVICE` and sign in with a key pair or token, never a password.
- Credentials: create keys, tokens, and secrets yourself, in a separate terminal, and read them from environment variables. Never put them in a script or give them to an agent.
- Dynamic SQL, if you add any, uses bind variables or an allowlist of identifiers, never text concatenated from user or model input.

Change these to fit your use case:

- Object names. Rename them in every script, including teardown: the recipe repeats them as literals, including inside `$$` bodies, so change them all at once, then check that teardown still removes everything.
- Roles, personas, and users: map them to your own, each granted no more than the recipe grants.
- Data: point the scripts at your tables instead of the sample data, then run Verify again.
- Models and warehouse sizes.

To have a coding agent adapt it:

```
Adapt the multi-agent-orchestration recipe in multi-agent-orchestration/ (unzipped from multi-agent-orchestration.zip) to <describe your use case>.
Read README.md first. Keep everything the "Adapt this recipe" section says to keep.
Change only names, roles and personas, data, and models.
Show me each changed file before you run anything, then run the recipe's Verify steps.
```

## Run it with a coding agent

```
Run the recipe in multi-agent-orchestration/.
1. Install or enable the check-agent-access skill from Snowflake-Labs/coco-skills
   if it is not already available.
2. Confirm the target with SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(),
   CURRENT_WAREHOUSE() and show me the result before creating anything.
3. sql/01_setup.sql runs as ACCOUNTADMIN and creates account-level objects: four
   roles, three service users, a warehouse, a database, and EXECUTE TASK ON ACCOUNT.
   Show me what it creates and wait for my confirmation. Then run it, and sql/02 through
   sql/06 in order, with snow sql -f. Stop and report on the first error.
4. Confirm the POLICY_CONTEXT checks at the end of 04 return 44, 16 (EMEA), and 0.
5. Use check-agent-access to confirm each persona role reaches the profile and
   only its own specialist.
6. For the persona tests, I create the key pairs and run the ALTER USER ... SET
   RSA_PUBLIC_KEY statements myself, then give you the private key file paths.
   Never create, print, or read a key yourself. Run the Verify question as each
   persona user, with no USE ROLE, and compare with the expected answers table
   and the subagent_name in each response.
7. Run sql/07_routing_eval.sql, poll EXECUTE_AI_EVALUATION('STATUS', ...) until
   the run completes, and report the average score per metric.
8. Do not attach the profile to the Snowflake CoWork object unless I ask.
9. When I say done, run sql/99_teardown.sql and confirm SHOW DATABASES/ROLES/USERS/
   WAREHOUSES LIKE 'COOKBOOK_MULTI_AGENT%' return nothing.
```

## Related skills

- `check-agent-access` ([coco-skills](https://github.com/Snowflake-Labs/coco-skills)): audit who can reach which agent and which tool objects behind it. Use it instead of hand-written `SHOW GRANTS` checks when you extend this pattern to more specialists or roles.

## References

- [Cortex Agents: access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup)
- [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage)
- [CREATE AGENT](/sql-reference/sql/create-agent)
- [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)
- [Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling)
- [Row access policies](/user-guide/security-row-intro)
- [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations)
- [User access and settings for agents in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents)
