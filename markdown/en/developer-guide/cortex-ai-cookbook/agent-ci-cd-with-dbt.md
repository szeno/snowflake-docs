# Agent CI/CD with dbt: per-PR builds, versioned deploys, and an evaluation gate

dbt builds the tables and semantic view, the agent ships as a versioned spec from a stage, and an evaluation gate in GitHub Actions blocks promotion.

|  |  |
| --- | --- |
| Stage | Operate, Evaluate |
| Topics | Cortex Agents, Semantic Views |
| Status | GA |
| Time to complete | 60min |
| Edition | Enterprise |
| Regions | Any region with Cortex Agents, dbt Projects on Snowflake, and the claude-sonnet-4-6 model (directly or through cross-region inference) |
| Privileges | ACCOUNTADMIN for 01\_setup.sql, 04\_ci\_service\_user.sql, and 99\_teardown.sql; everything else runs as COOKBOOK\_AGENT\_CI\_CD\_WITH\_DBT\_DEPLOYER |
| Related skills | `dbt-projects-on-snowflake` (bundled with Cortex Code), `agent-studio` (bundled with Cortex Code) |
| Last verified | 2026-10-04 |
| Authors | Parker Erickson |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code) or download [agent-ci-cd-with-dbt.zip](/static/samples/cortex-ai-cookbook/agent-ci-cd-with-dbt.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

A Cortex Agent is only as good as the tables, semantic view, and specification behind it, and all three change. This recipe puts them under one pipeline. dbt builds the tables and the semantic view. The agent specification is a file in Git that ships to Snowflake as an immutable named version. Every pull request gets its own schema, its own copy of the agent, and an evaluation run; the check fails if scores drop below a threshold. On merge, the same steps run against production, and the `PRODUCTION` alias moves to the new version only if the gate passes. GitHub Actions authenticates with OIDC, so no Snowflake credential is stored in GitHub.

## When to use this

- More than one person changes the agent, its semantic view, or the models under it, and you want reviewable, testable changes.
- You want a hard stop on quality regressions before a new agent version serves users.
- You want production to keep its grants and URLs across deployments, with a one-statement rollback.

When not to use it:

- A single developer iterating in Snowsight. Use the live version and evaluations directly; add this pipeline when you have a review process to protect.
- The agent depends on MCP connector tools or on session attributes and row access policies. Evaluations do not call MCP tools and do not pass session attributes, so the gate would not measure what users see.
- You need to rebuild only changed dbt models against production state. This recipe runs a full `dbt build` per PR; see the Slim CI tutorial in References for state and defer.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/agent-ci-cd-with-dbt/diagram-46d57165.svg)](/static/images/cortex-ai-cookbook/agent-ci-cd-with-dbt/diagram-46d57165.svg)

Key concepts:

1. **One dbt project, one schema per environment.** A `deploy_schema` var routes every model to `PROD` or `PR_<number>`. The project runs as a dbt project object inside Snowflake (`snow dbt deploy` and `snow dbt execute`), so the CI runner needs only the Snowflake CLI, not dbt or a warehouse connection of its own.
2. **The semantic view is a dbt model.** A short custom materialization wraps the model body in `CREATE OR ALTER SEMANTIC VIEW`, which keeps grants across runs and needs no external package download.
3. **The agent specification is a file, deployed as a version.** CI renders `agent/agent_spec.yaml` for the target schema, uploads it to a stage, and imports it: `CREATE AGENT ... FROM @stage/dir/` the first time, `ALTER AGENT ... ADD VERSION FROM @stage/dir/` after that. The agent object is never replaced, so grants, the URL, and history stay put.
4. **The evaluation gate scores the exact candidate version.** The eval config pins `agent_version` to the new `VERSION$N` and pins metric versions to `v3`. A procedure starts the run, waits for it, averages `EVAL_AGG_SCORE` per metric from `GET_AI_EVALUATION_DATA`, logs the decision, and raises an error below threshold. `snow sql` exits non-zero and the job fails.
5. **Promotion is an alias move.** After the gate passes on main, `PRODUCTION` moves to the new version and `DEFAULT_VERSION` is pinned to it. Rolling back is one `MODIFY VERSION ... SET ALIAS` statement.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Snowflake Enterprise account | Cortex Agents, agent evaluations, and dbt Projects on Snowflake available in your region |
| Model access | The agent uses `claude-sonnet-4-6`; the v3 evaluation judges use `claude-sonnet-4-6` or `openai-gpt-5.4`. Enable cross-region inference if your region does not host them |
| ACCOUNTADMIN, once | For `01_setup.sql` (roles, warehouse, database, EXECUTE TASK grant), `04_ci_service_user.sql`, and `99_teardown.sql` |
| Snowflake CLI 3.11 or later | 3.28.0 was used to verify this recipe; OIDC in GitHub Actions needs 3.11+ |
| GitHub repository | With Actions enabled and permission to create an environment and a secret |
| dbt | Not needed locally. dbt Core 1.11.11 runs inside Snowflake |

Expand

Show lessSee more

## Quickstart

1. Run `sql/01_setup.sql` as ACCOUNTADMIN. It grants the deployer and consumer roles to you.
2. Run `sql/02_pipeline_procedures.sql` and `sql/03_eval_dataset.sql`. They switch to the deployer role themselves.
3. Deploy production once from your machine to learn the pipeline:

   Copy code

   ```
   SNOW_CONN_FLAGS="-c <your_connection>" ci/scripts/deploy.sh PROD
   ```
4. Simulate a pull request, then clean it up:

   Copy code

   ```
   SNOW_CONN_FLAGS="-c <your_connection>" ci/scripts/deploy.sh PR_1
   SNOW_CONN_FLAGS="-c <your_connection>" ci/scripts/cleanup_pr.sh PR_1
   ```
5. Wire up GitHub:

   1. In `sql/04_ci_service_user.sql`, set `github_subject` to `repo:<owner>/<repo>:environment:snowflake-ci` and run it as ACCOUNTADMIN.
   2. In the repository settings, create the environment `snowflake-ci` and the secret `SNOWFLAKE_ACCOUNT` (your account identifier, for example `myorg-myaccount`).
   3. Copy `ci/workflows/agent-pr.yml` and `ci/workflows/agent-main.yml` to `.github/workflows/` and set `RECIPE_DIR` to this folder’s path in your repository.
   4. Open a pull request that changes `agent/agent_spec.yaml` or a dbt model and watch the check.

## Walkthrough

### Per-environment schemas from one dbt project

[dbt/macros/generate\_schema\_name.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-dbt-macros-generate-schema-name-sql) sends every node to the `deploy_schema` var and rejects anything that is not `PROD` or `PR_<number>`, so a bad var cannot create an arbitrary schema:

Copy code

```
{%- set schema = var('deploy_schema', target.schema) | string | upper -%}
{%- if not modules.re.match('^(PROD|PR_[0-9]{1,6})$', schema) -%}
    {{ exceptions.raise_compiler_error("deploy_schema must be PROD or PR_<number>, got: " ~ schema) }}
{%- endif -%}
```

`deploy.sh` deploys one dbt project object per environment in `OPS` and builds it:

Copy code

```
snow dbt deploy "RETAIL_DBT_${target}" --source dbt --dbt-version 1.11.11 "${ctx[@]}"
snow dbt execute "${ctx[@]}" "RETAIL_DBT_${target}" build --vars "{\"deploy_schema\": \"${target}\"}"
```

`build` runs seeds, models, and the 20 data tests in DAG order, so a failing test stops the pipeline before the agent is touched.

### The semantic view as a model

[dbt/macros/semantic\_view.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-dbt-macros-semantic-view-sql) is the whole materialization:

Copy code

```
{% call statement('main') -%}
    CREATE OR ALTER SEMANTIC VIEW {{ target_relation }}
    {{ sql }}
{%- endcall %}
```

The model [retail\_analytics.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-dbt-models-semantic-retail-analytics-sql) is the DDL body with `ref()` in `TABLES`, so dbt orders it after the tables it describes. Revenue exists at two grains: `orders.total_revenue` at order grain and `order_lines.product_revenue` at line grain. Keeping them separate prevents product-level questions from fanning out order totals. The `dbt_semantic_view` package offers the same idea with more options; it needs an external access integration because dbt Projects on Snowflake runs `dbt deps` inside Snowflake.

### Importing the agent as a version

`DEPLOY_AGENT_VERSION` in [sql/02\_pipeline\_procedures.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-sql-02-pipeline-procedures-sql) runs with caller’s rights and validates every input against a pattern before building DDL:

Copy code

```
IF (agent_count = 0) THEN
    EXECUTE IMMEDIATE 'CREATE AGENT ' || agent_fqn || ' COMMENT = ''...'' FROM ' || SPEC_DIR;
ELSE
    -- ADD VERSION FROM a stage fails while a LIVE version exists.
    IF (live_count > 0) THEN
        EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn || ' COMMIT COMMENT = ''...; not promoted''';
    END IF;
    EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn || ' ADD VERSION FROM ' || SPEC_DIR || ' COMMENT = ''' || VERSION_COMMENT || '''';
END IF;
```

`CREATE AGENT ... FROM @stage` creates `VERSION$1` and a `LIVE` version. `ADD VERSION FROM @stage` is rejected while that live version exists, so the procedure commits it first. That also preserves any edits someone made in Snowsight as a named version, without promoting them. Only versions imported from Git are ever promoted. The procedure returns the newest `VERSION$N`, which is the candidate.

The stage needs server-side encryption for these imports to read the file:

Copy code

```
CREATE STAGE IF NOT EXISTS AGENT_SPECS ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE') DIRECTORY = (ENABLE = TRUE);
```

The spec names the orchestration model (`claude-sonnet-4-6`) instead of `auto`, so a score change reflects your change rather than a model selection change.

### The evaluation gate

The eval config template [evaluation/eval\_config.yaml](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-evaluation-eval-config-yaml) has no `dataset:` block: `03_eval_dataset.sql` registers the dataset once with `SYSTEM$CREATE_EVALUATION_DATASET`, and a `dataset:` block would try to recreate it on every run. Metrics are pinned:

Copy code

```
metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
```

`RUN_EVAL_GATE` starts the run, polls `STATUS`, then scores it:

Copy code

```
CALL EXECUTE_AI_EVALUATION('START', OBJECT_CONSTRUCT('run_name', :RUN_NAME), :CONFIG_PATH);
...
SELECT METRIC_NAME, ROUND(AVG(COALESCE(EVAL_AGG_SCORE, 0)), 3) AS avg_score, ...
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
         CURRENT_DATABASE(), :TARGET_SCHEMA, 'RETAIL_ASSISTANT', 'CORTEX AGENT', :RUN_NAME))
 GROUP BY METRIC_NAME;
```

It fails closed: a partial run, a missing metric, or a record with no score counts against the gate. Every decision is written to `OPS.EVAL_GATE_RESULTS` before the procedure raises, so a failed check still leaves the numbers behind. Evaluations run in the session’s current schema, which is why `deploy.sh` always connects with `--schema OPS`.

The ground truth in [sql/03\_eval\_dataset.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-sql-03-eval-dataset-sql) states literal values scoped to absolute dates (“between January 1 and December 31, 2024”), plus one out-of-scope question the agent must decline.

### Promotion and rollback

`PROMOTE_AGENT_VERSION` runs only on main after the gate passes:

Copy code

```
ALTER AGENT <db>.PROD.RETAIL_ASSISTANT MODIFY VERSION VERSION$3 SET ALIAS = PRODUCTION;
ALTER AGENT <db>.PROD.RETAIL_ASSISTANT SET DEFAULT_VERSION = 'VERSION$3';
```

Setting the alias on a new version moves it off the old one. Pinning `DEFAULT_VERSION` matters: without it the newest version, gated or not, becomes the default. To roll back, run both statements with the previous version.

### GitHub Actions with OIDC

[ci/workflows/agent-pr.yml](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-ci-workflows-agent-pr-yml) and [ci/workflows/agent-main.yml](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-ci-workflows-agent-main-yml) install the CLI with `snowflakedb/snowflake-actions@v3` and exchange GitHub’s OIDC token for a Snowflake session:

Copy code

```
permissions:
  contents: read
  id-token: write
...
    environment: snowflake-ci # must match the SUBJECT of the service user
    steps:
      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.28.0"
      - run: snow connection test -x
```

The service user in [sql/04\_ci\_service\_user.sql](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt/code#label-cookbook-agent-ci-cd-with-dbt-sql-04-ci-service-user-sql) trusts exactly one subject:

Copy code

```
CREATE USER IF NOT EXISTS IDENTIFIER($ci_user)
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://token.actions.githubusercontent.com'
    SUBJECT = $github_subject)
  DEFAULT_ROLE = $deployer_role DEFAULT_WAREHOUSE = $cookbook_wh;
```

The PR number is passed to the script through an environment variable, and `deploy.sh` validates it, so nothing from the pull request is interpolated into shell or SQL.

## Verify

After `deploy.sh PROD`, the production agent has a gated version behind the alias:

Copy code

```
SHOW VERSIONS IN AGENT COOKBOOK_AGENT_CI_CD_WITH_DBT.PROD.RETAIL_ASSISTANT;
-- VERSION$1  alias PRODUCTION  is_default true   (first deploy)
-- After a second deploy: VERSION$2 is the committed live version (no alias),
-- VERSION$3 carries PRODUCTION and is the default.
```

Each gate decision is logged:

Copy code

```
SELECT run_name, target_schema, run_status, scores, thresholds, records_errored, passed
FROM COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS.EVAL_GATE_RESULTS
ORDER BY evaluated_at;
-- On the sample data: answer_correctness 0.945, logical_consistency 1.0, passed = TRUE
```

A deliberately failing run (`MIN_ANSWER_CORRECTNESS=1.0 ci/scripts/deploy.sh PR_1`) ends with `RUN_EVAL_GATE: scores below threshold`, logs `passed = FALSE`, exits 1, and promotes nothing.

The consumer role can use production with only the grants from `01_setup.sql`: USAGE on the agent, SELECT on the semantic view, and SELECT on the tables behind it, because Cortex Analyst runs the SQL it generates with the caller’s role. This check calls the agent from SQL:

Copy code

```
USE ROLE COOKBOOK_AGENT_CI_CD_WITH_DBT_USER;
USE WAREHOUSE COOKBOOK_AGENT_CI_CD_WITH_DBT_WH;
SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'COOKBOOK_AGENT_CI_CD_WITH_DBT.PROD.RETAIL_ASSISTANT!PRODUCTION',
  $${"messages": [{"role": "user", "content": [{"type": "text", "text": "How many orders are in processing status?"}]}]}$$);
-- the text answer reports 6 orders in processing status
SHOW GRANTS ON AGENT COOKBOOK_AGENT_CI_CD_WITH_DBT.PROD.RETAIL_ASSISTANT;
-- USAGE to COOKBOOK_AGENT_CI_CD_WITH_DBT_USER survives every deploy
```

`DATA_AGENT_RUN` in SQL ran the agent and its Cortex Analyst query with the session role set by `USE ROLE`, even for a user whose default role had no access, so this check tests the consumer role’s grants. Callers through the Agents REST API or Snowflake CoWork are authorized with their default role instead, as the access control docs describe. For those users, make `COOKBOOK_AGENT_CI_CD_WITH_DBT_USER` the `DEFAULT_ROLE` and `COOKBOOK_AGENT_CI_CD_WITH_DBT_WH` the `DEFAULT_WAREHOUSE`, or grant the role to their existing default role.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| `No spec file present for the agent. Failed to read agent_spec.yaml from source stage` | The stage uses the default client-side encryption | Create the stage with `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')`, and name the file `agent_spec.yaml` |
| `There is already a live version. Please commit it first.` | `ADD VERSION FROM @stage` is blocked while a LIVE version exists; `CREATE AGENT` always creates one | Commit the live version first, as `DEPLOY_AGENT_VERSION` does. The committed version is kept but never promoted |
| A new version serves unversioned requests before it passed the gate | Without a pinned `DEFAULT_VERSION`, the newest version is the default | Pin it at promotion (`PROMOTE_AGENT_VERSION` does). Clients should call the `PRODUCTION` alias |
| On the very first production deploy, `VERSION$1` is the default before the gate finishes | `CREATE AGENT` makes the first version the default | Grant consumers access after the first successful deploy, or have clients call `!PRODUCTION`, which does not exist until the gate passes |
| dbt fails with `takes no keyword argument 'arguments'` | The project object’s default dbt version predates the `arguments:` test syntax | Deploy with `--dbt-version 1.11.11`, as `deploy.sh` does |
| Evaluation `START` fails because the dataset already exists | The config contains a `dataset:` block, which Snowflake tries to create on every run | Register the dataset once (`03_eval_dataset.sql`) and reference it in `source_metadata` only |
| The gate flips between pass and fail with no change | Agent orchestration is non-deterministic, so each run takes its own path | Run the gate several times on an unchanged agent to learn the normal range, then set thresholds below it. `EVAL_GATE_RESULTS` keeps the history |
| `EVAL_GATE_RESULTS` shows `PARTIALLY_COMPLETED` and `passed = FALSE` with full scores | The docs list `PARTIALLY_COMPLETED` as final, but a run can report it briefly before `COMPLETED` | `RUN_EVAL_GATE` keeps polling for 120 seconds after it first sees `PARTIALLY_COMPLETED` and fails closed only if the run stays there. Raise that window in `02_pipeline_procedures.sql` if your runs need longer |
| The agent answers that it cannot access `FCT_ORDERS` for a consumer | The consumer role has SELECT on the semantic view but not on its base tables | Grant SELECT on the tables too, as `01_setup.sql` does with a future grant on `PROD` |
| A consumer gets access errors in the REST API or Snowflake CoWork that SQL `DATA_AGENT_RUN` does not show | Those surfaces authorize with the user’s default role and default warehouse, not the session role | Set the consumer role and the recipe warehouse as the user’s defaults |
| `snow connection test -x` fails in GitHub | The OIDC subject does not match: wrong repository, or the job has no `environment: snowflake-ci` | Compare `SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR USER COOKBOOK_AGENT_CI_CD_WITH_DBT_CI` with the job’s subject |
| PR and main share one deployer role, so a pull request can change production before anyone reviews it | The PR workflow runs `deploy.sh`, the dbt models, and the agent spec from the PR branch, with a role that owns `PROD`. Anyone who can push a branch and open a pull request can edit those files to run any SQL the deployer can, including dropping or replacing `PROD` objects or moving the `PRODUCTION` alias. GitHub does not give pull requests from forks the OIDC token or the environment, but branches in the repository get both | Before you use this beyond a sandbox, split the identities. Give PR builds their own service user and role that can create and drop `PR_<number>` schemas but has no privileges on `PROD`. Bind the production service user to a separate `production` environment that only `main` can deploy to and that requires reviewers, and give that user its own OIDC subject. Protect `ci/`, `agent/`, and `dbt/` with CODEOWNERS review |
| Costs grow with every push | Each PR run builds tables and runs an evaluation (agent and judge inference) | Keep the dataset small and focused; the workflow cancels superseded runs for the same PR |

Expand

Show lessSee more

## Teardown

Close or clean up any open pull requests first (`ci/scripts/cleanup_pr.sh PR_<number>`), then run `sql/99_teardown.sql` as ACCOUNTADMIN. It drops the database (every schema, agent, semantic view, dbt project object, stage, and dataset), the warehouse, the CI service user, and both roles. No account parameters are changed by this recipe. Remove the two workflow files and the `snowflake-ci` environment from your repository.

## Adapt this recipe

Keep these, so a customized version keeps the recipe’s security model:

- Least privilege: `ACCOUNTADMIN` only for the scripts listed under Privileges; everything else runs as the recipe’s own role.
- No grants to `PUBLIC`.
- Caller’s rights: procedures run as `EXECUTE AS CALLER`, so each user’s own grants apply.
- Service users stay `TYPE = SERVICE` and sign in with a key pair or token, never a password.
- Credentials: create keys, tokens, and secrets yourself, in a separate terminal, and read them from environment variables. Never put them in a script or give them to an agent.
- Dynamic SQL, if you add any, uses bind variables or an allowlist of identifiers, never text concatenated from user or model input.

Change these to fit your use case:

- Object names. Rename them in every script, including teardown, then check that teardown still removes everything.
- Roles, personas, and users: map them to your own, each granted no more than the recipe grants.
- Data: point the scripts at your tables instead of the sample data, then run Verify again.
- Models and warehouse sizes.

To have a coding agent adapt it:

```
Adapt the agent-ci-cd-with-dbt recipe in agent-ci-cd-with-dbt/ (unzipped from agent-ci-cd-with-dbt.zip) to <describe your use case>.
Read README.md first. Keep everything the "Adapt this recipe" section says to keep.
Change only names, roles and personas, data, and models.
Show me each changed file before you run anything, then run the recipe's Verify steps.
```

## Run it with a coding agent

```
Set up the agent-ci-cd-with-dbt recipe in agent-ci-cd-with-dbt/.
1. Install or enable the bundled dbt-projects-on-snowflake and agent-studio skills. Use
   dbt-projects-on-snowflake for the snow dbt deploy and execute steps and agent-studio for
   evaluation runs.
2. Confirm the target account with SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE()
   and show me the result before creating anything.
3. sql/01_setup.sql runs as ACCOUNTADMIN and grants EXECUTE TASK ON ACCOUNT to the deployer role.
   Show me its ACCOUNTADMIN statements and wait for my confirmation. Then run it, then
   sql/02_pipeline_procedures.sql and sql/03_eval_dataset.sql, with snow sql -f.
4. Run SNOW_CONN_FLAGS="-c <my connection>" ci/scripts/deploy.sh PROD and show me SHOW VERSIONS IN AGENT
   COOKBOOK_AGENT_CI_CD_WITH_DBT.PROD.RETAIL_ASSISTANT and the rows in
   COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS.EVAL_GATE_RESULTS.
5. Change the response instruction in agent/agent_spec.yaml, run deploy.sh PR_1, and compare its
   scores with PROD. Clean up with ci/scripts/cleanup_pr.sh PR_1.
6. Do not replace the agent with CREATE OR REPLACE; versions must be added with ADD VERSION FROM
   the stage.
7. sql/04_ci_service_user.sql creates an account-level SERVICE user. Ask me for my GitHub
   owner/repo, show me the edited script, and run it only after I confirm. It creates no secret.
8. When I say so, clean up any open PR_<number> schemas with cleanup_pr.sh, then run
   sql/99_teardown.sql and confirm that SHOW DATABASES, SHOW ROLES, SHOW WAREHOUSES, and
   SHOW USERS LIKE 'COOKBOOK_AGENT_CI_CD_WITH_DBT%' return nothing.
```

## Related skills

- `dbt-projects-on-snowflake` (bundled): deploying, executing, scheduling, and monitoring dbt project objects, and the `dbt_semantic_view` package. Use it to extend the dbt side of this pipeline, for example with a scheduled task.
- `agent-studio` (bundled): curating the evaluation dataset from production questions, running and investigating evaluations, and optimizing the agent. Use it to grow `RETAIL_EVAL_QUESTIONS` beyond the six sample questions.

## References

- [Cortex Agent versioning](/user-guide/snowflake-cortex/cortex-agents-versioning)
- [CREATE AGENT](/sql-reference/sql/create-agent)
- [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations)
- [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation)
- [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset)
- [Tutorial: CI/CD with Slim CI and per-PR databases for dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-advanced-ci-cd-tutorial)
- [Snowflake CLI GitHub Action](/developer-guide/snowflake-cli/cicd/github-action)
- [Workload identity federation](/user-guide/workload-identity-federation)
- [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec)
