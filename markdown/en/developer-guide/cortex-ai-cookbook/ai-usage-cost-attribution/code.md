# AI usage and cost attribution across agents, CoWork, Cortex Code, and AI functions: code

Every file in the [AI usage and cost attribution across agents, CoWork, Cortex Code, and AI functions](/developer-guide/cortex-ai-cookbook/ai-usage-cost-attribution) recipe. To run the recipe, download [ai-usage-cost-attribution.zip](/static/samples/cortex-ai-cookbook/ai-usage-cost-attribution.zip), unzip it, and run the scripts from the `ai-usage-cost-attribution/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/ai-usage-cost-attribution); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- 01_setup.sql
-- Creates the recipe database, warehouse, and a read-only analyst role that can
-- read the AI usage views in SNOWFLAKE.ACCOUNT_USAGE. Run as ACCOUNTADMIN once;
-- everything after this file runs as the analyst role.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';
SET cookbook_user = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role)
  COMMENT = 'Cookbook: reads AI usage views and owns the attribution views';
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($cookbook_user);

-- Two SNOWFLAKE database roles instead of IMPORTED PRIVILEGES on the whole database:
--   USAGE_VIEWER    -> the Cortex AI usage views and METERING_DAILY_HISTORY
--   SECURITY_VIEWER -> ACCOUNT_USAGE.USERS, used to turn USER_ID into a user name
--                      (CORTEX_AI_FUNCTIONS_USAGE_HISTORY and CORTEX_REST_API_USAGE_HISTORY
--                      carry USER_ID only)
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER    TO ROLE IDENTIFIER($cookbook_role);
GRANT DATABASE ROLE SNOWFLAKE.SECURITY_VIEWER TO ROLE IDENTIFIER($cookbook_role);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook: ai-usage-cost-attribution';
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
  COMMENT = 'Cookbook: ai-usage-cost-attribution';
-- The analyst role owns the database so the views it creates run with its own
-- (read-only) privileges, not with ACCOUNTADMIN's.
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

USE ROLE IDENTIFIER($cookbook_role);
USE DATABASE IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS ATTRIBUTION COMMENT = 'Unified AI usage and cost attribution views';
CREATE SCHEMA IF NOT EXISTS GOVERNANCE  COMMENT = 'Tags, budgets, and quotas for this recipe';

-- Cost-center tag used for attribution (USER_TAGS / AGENT_TAGS) and budget/quota scoping.
CREATE TAG IF NOT EXISTS GOVERNANCE.COST_CENTER
  ALLOWED_VALUES 'cookbook', 'finance', 'support'
  COMMENT = 'Cookbook: cost center for AI usage attribution';

-- Smoke test: the role can read every view the recipe uses.
USE WAREHOUSE IDENTIFIER($cookbook_wh);
SELECT 'CORTEX_AGENT_USAGE_HISTORY'        AS view_name, COUNT(*) AS rows_last_30d FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AGENT_USAGE_HISTORY        WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'SNOWFLAKE_COWORK_USAGE_HISTORY',    COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COWORK_USAGE_HISTORY    WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'SNOWFLAKE_COCO_USAGE_HISTORY',      COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY      WHERE USAGE_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'CORTEX_AI_FUNCTIONS_USAGE_HISTORY', COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'CORTEX_ANALYST_USAGE_HISTORY',      COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_ANALYST_USAGE_HISTORY      WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'CORTEX_REST_API_USAGE_HISTORY',     COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_REST_API_USAGE_HISTORY     WHERE START_TIME >= DATEADD(day, -30, CURRENT_TIMESTAMP())
UNION ALL SELECT 'USERS',                             COUNT(*) FROM SNOWFLAKE.ACCOUNT_USAGE.USERS;
```

### `sql/02_views.sql`

Copy code

```
-- 02_views.sql
-- Attribution views over SNOWFLAKE.ACCOUNT_USAGE. Run as the analyst role created in 01.
-- Rules the views follow:
--   * One source view per billing service type, so totals never double count
--     (CORTEX_AGENTS, SNOWFLAKE_COWORK, SNOWFLAKE_COCO*, AI_FUNCTIONS, AI_SERVICES for Analyst).
--   * SNOWFLAKE_COCO_USAGE_HISTORY already covers the CLI, Desktop, and Snowsight
--     interfaces, so the per-interface CORTEX_CODE_*_USAGE_HISTORY views are not added.
--   * Warehouse credits reported by agents (METADATA:sql_query_credits) are kept in
--     their own column. They are billed as warehouse compute, not as AI credits.
--   * CORTEX_REST_API_USAGE_HISTORY reports tokens only (billed in currency), so it gets
--     its own view and is never added to credit totals.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA ATTRIBUTION;

-- ---------------------------------------------------------------------------
-- 1. One row per Cortex Agent or CoWork request.
--    The two source views are mutually exclusive: CoWork requests are only in
--    SNOWFLAKE_COWORK_USAGE_HISTORY, direct agent requests only in
--    CORTEX_AGENT_USAGE_HISTORY.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_AGENT_REQUESTS
  COMMENT = 'Cookbook: one row per Cortex Agent or CoWork request'
AS
SELECT
    'CORTEX_AGENT'                                        AS surface,
    COALESCE(METADATA:interaction_interface::STRING, 'unknown') AS interface,
    START_TIME,
    END_TIME,
    USER_ID,
    USER_NAME,
    METADATA:role_name::STRING                            AS role_name,
    REQUEST_ID,
    PARENT_REQUEST_ID,
    COALESCE(PARENT_REQUEST_ID, REQUEST_ID)               AS root_request_id,
    AGENT_DATABASE_NAME || '.' || AGENT_SCHEMA_NAME || '.' || AGENT_NAME AS agent_fqn,
    NULL::STRING                                          AS cowork_name,
    TOKENS,
    TOKEN_CREDITS,
    METADATA:sql_query_credits::NUMBER(38, 9)             AS sql_query_credits,
    METADATA:sql_query_warehouses                         AS sql_query_warehouses,
    METADATA:ai_functions_credits::NUMBER(38, 9)          AS ai_functions_credits,
    METADATA:inference_region::STRING                     AS inference_region,
    USER_TAGS,
    AGENT_TAGS,
    TOKENS_GRANULAR,
    CREDITS_GRANULAR
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AGENT_USAGE_HISTORY
UNION ALL
SELECT
    'SNOWFLAKE_COWORK',
    'cowork',
    START_TIME,
    END_TIME,
    USER_ID,
    USER_NAME,
    METADATA:role_name::STRING,
    REQUEST_ID,
    PARENT_REQUEST_ID,
    COALESCE(PARENT_REQUEST_ID, REQUEST_ID),
    AGENT_DATABASE_NAME || '.' || AGENT_SCHEMA_NAME || '.' || AGENT_NAME,
    SNOWFLAKE_COWORK_NAME,
    TOKENS,
    TOKEN_CREDITS,
    METADATA:sql_query_credits::NUMBER(38, 9),
    METADATA:sql_query_warehouses,
    METADATA:ai_functions_credits::NUMBER(38, 9),
    METADATA:inference_region::STRING,
    USER_TAGS,
    AGENT_TAGS,
    TOKENS_GRANULAR,
    CREDITS_GRANULAR
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COWORK_USAGE_HISTORY;

-- ---------------------------------------------------------------------------
-- 2. Token and credit breakdown per sub-request, service type, and model.
--    TOKENS_GRANULAR / CREDITS_GRANULAR are arrays of
--      { "<sub_request_id>": { "<service_type>": { "<model>": {input, cache_read_input,
--        cache_write_input, output} }, "start_time": "..." } }
--    so the flatten goes: array element -> sub-request -> service type -> model.
--    TOKENS on the parent row equals input + cache_read_input + cache_write_input + output.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_AGENT_TOKENS_BY_MODEL
  COMMENT = 'Cookbook: agent and CoWork tokens and credits per sub-request, service type, and model'
AS
WITH tok AS (
    SELECT
        r.surface, r.interface, r.request_id, r.start_time, r.user_name, r.agent_fqn, r.cowork_name,
        sub.key                                 AS sub_request_id,
        sub.value:start_time::TIMESTAMP_LTZ     AS sub_request_start_time,
        svc.key                                 AS service_type,
        mdl.key                                 AS model_name,
        COALESCE(mdl.value:input::NUMBER, 0)             AS input_tokens,
        COALESCE(mdl.value:cache_read_input::NUMBER, 0)  AS cache_read_input_tokens,
        COALESCE(mdl.value:cache_write_input::NUMBER, 0) AS cache_write_input_tokens,
        COALESCE(mdl.value:output::NUMBER, 0)            AS output_tokens
    FROM V_AGENT_REQUESTS r,
         LATERAL FLATTEN(input => r.tokens_granular) el,
         LATERAL FLATTEN(input => el.value)          sub,
         LATERAL FLATTEN(input => sub.value)         svc,
         LATERAL FLATTEN(input => svc.value)         mdl
    WHERE IS_OBJECT(svc.value)          -- skips the sibling "start_time" key
),
cred AS (
    SELECT
        r.surface, r.request_id,
        sub.key AS sub_request_id,
        svc.key AS service_type,
        mdl.key AS model_name,
        COALESCE(mdl.value:input::FLOAT, 0)
          + COALESCE(mdl.value:cache_read_input::FLOAT, 0)
          + COALESCE(mdl.value:cache_write_input::FLOAT, 0)
          + COALESCE(mdl.value:output::FLOAT, 0)         AS credits,
        COALESCE(mdl.value:cache_read_input::FLOAT, 0)   AS cache_read_input_credits
    FROM V_AGENT_REQUESTS r,
         LATERAL FLATTEN(input => r.credits_granular) el,
         LATERAL FLATTEN(input => el.value)           sub,
         LATERAL FLATTEN(input => sub.value)          svc,
         LATERAL FLATTEN(input => svc.value)          mdl
    WHERE IS_OBJECT(svc.value)
)
SELECT
    t.*,
    t.input_tokens + t.cache_read_input_tokens + t.cache_write_input_tokens AS total_input_tokens,
    c.credits,
    c.cache_read_input_credits
FROM tok t
LEFT JOIN cred c
  ON  c.surface        = t.surface
  AND c.request_id     = t.request_id
  AND c.sub_request_id = t.sub_request_id
  AND c.service_type   = t.service_type
  AND c.model_name     = t.model_name;

-- ---------------------------------------------------------------------------
-- 3. Cortex Code token breakdown. Here TOKENS_GRANULAR is an OBJECT keyed by model name.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_COCO_TOKENS_BY_MODEL
  COMMENT = 'Cookbook: Cortex Code tokens and credits per request and model'
AS
SELECT
    u.USAGE_TIME::TIMESTAMP_LTZ                          AS usage_time,
    u.INTERFACE                                          AS interface,
    u.USER_ID,
    u.USER_NAME,
    u.REQUEST_ID,
    m.key                                                AS model_name,
    COALESCE(m.value:input::NUMBER, 0)                   AS input_tokens,
    COALESCE(m.value:cache_read_input::NUMBER, 0)        AS cache_read_input_tokens,
    COALESCE(m.value:cache_write_input::NUMBER, 0)       AS cache_write_input_tokens,
    COALESCE(m.value:output::NUMBER, 0)                  AS output_tokens,
    COALESCE(m.value:input::NUMBER, 0)
      + COALESCE(m.value:cache_read_input::NUMBER, 0)
      + COALESCE(m.value:cache_write_input::NUMBER, 0)   AS total_input_tokens,
    COALESCE(u.CREDITS_GRANULAR[m.key]:input::FLOAT, 0)
      + COALESCE(u.CREDITS_GRANULAR[m.key]:cache_read_input::FLOAT, 0)
      + COALESCE(u.CREDITS_GRANULAR[m.key]:cache_write_input::FLOAT, 0)
      + COALESCE(u.CREDITS_GRANULAR[m.key]:output::FLOAT, 0) AS credits
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY u,
     LATERAL FLATTEN(input => u.TOKENS_GRANULAR) m;

-- ---------------------------------------------------------------------------
-- 4. Unified AI credit usage across surfaces, one source per service type.
--    CORTEX_AI_FUNCTIONS_USAGE_HISTORY has USER_ID only, so it joins USERS for the name.
--    CORTEX_ANALYST_USAGE_HISTORY is an hourly roll-up by USERNAME (no request id).
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_AI_USAGE_UNIFIED
  COMMENT = 'Cookbook: AI credit usage across agents, CoWork, Cortex Code, AI functions, and Analyst'
AS
SELECT
    surface,
    interface,
    start_time                    AS usage_time,
    user_id,
    user_name,
    COALESCE(cowork_name, agent_fqn) AS object_name,
    NULL::STRING                  AS model_name,
    request_id,
    1                             AS request_count,
    tokens,
    token_credits                 AS ai_credits,
    sql_query_credits,
    'CORTEX_AGENT_USAGE_HISTORY / SNOWFLAKE_COWORK_USAGE_HISTORY' AS source_view
FROM V_AGENT_REQUESTS
UNION ALL
SELECT
    'SNOWFLAKE_COCO',
    INTERFACE,
    USAGE_TIME::TIMESTAMP_LTZ,
    USER_ID,
    USER_NAME,
    NULL,
    NULL,
    REQUEST_ID,
    1,
    TOKENS,
    TOKEN_CREDITS,
    NULL,
    'SNOWFLAKE_COCO_USAGE_HISTORY'
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY
UNION ALL
SELECT
    'AI_FUNCTIONS',
    'sql',
    f.START_TIME,
    f.USER_ID,
    u.NAME,
    f.FUNCTION_NAME,
    NULLIF(f.MODEL_NAME, ''),
    f.QUERY_ID,
    1,
    NULL,
    f.CREDITS,
    NULL,
    'CORTEX_AI_FUNCTIONS_USAGE_HISTORY'
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY f
LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u
  ON u.USER_ID = f.USER_ID
UNION ALL
SELECT
    'CORTEX_ANALYST',
    'hourly_rollup',
    START_TIME,
    NULL,
    USERNAME,
    NULL,
    NULL,
    NULL,
    REQUEST_COUNT,
    NULL,
    CREDITS,
    NULL,
    'CORTEX_ANALYST_USAGE_HISTORY'
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_ANALYST_USAGE_HISTORY;

-- ---------------------------------------------------------------------------
-- 5. REST API inference: tokens only (billed in currency, not credits). USER_ID only.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_REST_API_TOKENS
  COMMENT = 'Cookbook: Cortex REST API tokens per request (currency-billed; no credits)'
AS
SELECT
    r.START_TIME::TIMESTAMP_LTZ                             AS usage_time,
    r.USER_ID,
    u.NAME                                                  AS user_name,
    r.REQUEST_ID,
    r.MODEL_NAME,
    r.INFERENCE_REGION,
    r.QUERY_TAG,
    r.TOKENS,
    COALESCE(r.TOKENS_GRANULAR:input::NUMBER, 0)            AS input_tokens,
    COALESCE(r.TOKENS_GRANULAR:cache_read_input::NUMBER, 0) AS cache_read_input_tokens,
    COALESCE(r.TOKENS_GRANULAR:cache_write_input::NUMBER, 0) AS cache_write_input_tokens,
    COALESCE(r.TOKENS_GRANULAR:output::NUMBER, 0)           AS output_tokens
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_REST_API_USAGE_HISTORY r
LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u
  ON u.USER_ID = r.USER_ID;

-- ---------------------------------------------------------------------------
-- 6. Reconciliation against billing. Compares each surface's daily credits (UTC day)
--    with METERING_DAILY_HISTORY for the matching service type. Analyst is excluded
--    because AI_SERVICES also contains Search, fine-tuning, and other services.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_RECONCILE_METERING
  COMMENT = 'Cookbook: unified view credits vs METERING_DAILY_HISTORY by UTC day'
AS
WITH usage_daily AS (
    SELECT surface, CONVERT_TIMEZONE('UTC', usage_time)::DATE AS usage_date, SUM(ai_credits) AS view_credits
    FROM V_AI_USAGE_UNIFIED
    WHERE surface <> 'CORTEX_ANALYST'
    GROUP BY 1, 2
),
metering_daily AS (
    SELECT
        CASE
            WHEN SERVICE_TYPE = 'CORTEX_AGENTS'                              THEN 'CORTEX_AGENT'
            WHEN SERVICE_TYPE IN ('SNOWFLAKE_COWORK', 'SNOWFLAKE_INTELLIGENCE') THEN 'SNOWFLAKE_COWORK'
            WHEN SERVICE_TYPE LIKE 'SNOWFLAKE_COCO%' OR SERVICE_TYPE LIKE 'CORTEX_CODE%' THEN 'SNOWFLAKE_COCO'
            WHEN SERVICE_TYPE = 'AI_FUNCTIONS'                               THEN 'AI_FUNCTIONS'
        END AS surface,
        USAGE_DATE AS usage_date,
        SUM(CREDITS_USED) AS metered_credits
    FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
    GROUP BY 1, 2
    HAVING surface IS NOT NULL
)
SELECT
    COALESCE(u.surface, m.surface)       AS surface,
    COALESCE(u.usage_date, m.usage_date) AS usage_date,
    ROUND(COALESCE(u.view_credits, 0), 4)    AS view_credits,
    ROUND(COALESCE(m.metered_credits, 0), 4) AS metered_credits,
    ROUND(COALESCE(m.metered_credits, 0) - COALESCE(u.view_credits, 0), 4) AS delta
FROM usage_daily u
FULL OUTER JOIN metering_daily m
  ON m.surface = u.surface AND m.usage_date = u.usage_date;
```

### `sql/03_attribution_queries.sql`

Copy code

```
-- 03_attribution_queries.sql
-- Read-only attribution queries over the views from 02. Change the window in one place.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';
SET lookback_days = 30;

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA ATTRIBUTION;

-- Q1. Surface mix: where AI credits come from. Agent rows split by interaction_interface.
--     sql_query_credits is warehouse compute run by the agent; it is billed as warehouse
--     metering, so it is shown next to AI credits, never added into them.
SELECT
    surface,
    interface,
    SUM(request_count)                  AS requests,
    COUNT(DISTINCT user_name)           AS users,
    ROUND(SUM(ai_credits), 4)           AS ai_credits,
    ROUND(SUM(sql_query_credits), 4)    AS agent_warehouse_credits,
    ROUND(100 * RATIO_TO_REPORT(SUM(ai_credits)) OVER (), 1) AS pct_of_ai_credits
FROM V_AI_USAGE_UNIFIED
WHERE usage_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY ai_credits DESC;

-- Q2. Top users across every surface.
SELECT
    user_name,
    ROUND(SUM(ai_credits), 4)                                               AS ai_credits,
    ROUND(SUM(IFF(surface = 'CORTEX_AGENT',     ai_credits, 0)), 4)         AS agent_credits,
    ROUND(SUM(IFF(surface = 'SNOWFLAKE_COWORK', ai_credits, 0)), 4)         AS cowork_credits,
    ROUND(SUM(IFF(surface = 'SNOWFLAKE_COCO',   ai_credits, 0)), 4)         AS coco_credits,
    ROUND(SUM(IFF(surface = 'AI_FUNCTIONS',     ai_credits, 0)), 4)         AS ai_function_credits,
    ROUND(SUM(IFF(surface = 'CORTEX_ANALYST',   ai_credits, 0)), 4)         AS analyst_credits
FROM V_AI_USAGE_UNIFIED
WHERE usage_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY ai_credits DESC
LIMIT 20;

-- Q3. Per agent: token credits, warehouse credits from its SQL, and cost per request.
SELECT
    agent_fqn,
    surface,
    COUNT(*)                                        AS requests,
    ROUND(SUM(token_credits), 4)                    AS token_credits,
    ROUND(SUM(sql_query_credits), 6)                AS warehouse_credits,
    COUNT_IF(sql_query_credits IS NULL)             AS requests_without_sql_attribution,
    ROUND(AVG(token_credits), 6)                    AS avg_token_credits_per_request,
    ROUND(AVG(tokens), 0)                           AS avg_tokens_per_request
FROM V_AGENT_REQUESTS
WHERE start_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY token_credits DESC
LIMIT 20;

-- Q4. Model mix and prompt-cache ratio for agents and CoWork.
--     Cache ratio = cache_read_input / (input + cache_read_input + cache_write_input):
--     the share of all input tokens served from the prompt cache. Dividing by the
--     "input" field alone is wrong, because "input" counts only the uncached tokens.
SELECT
    surface,
    service_type,
    model_name,
    COUNT(DISTINCT request_id)                                AS requests,
    SUM(total_input_tokens)                                   AS total_input_tokens,
    SUM(cache_read_input_tokens)                              AS cache_read_input_tokens,
    SUM(output_tokens)                                        AS output_tokens,
    ROUND(SUM(cache_read_input_tokens) / NULLIF(SUM(total_input_tokens), 0), 3) AS cache_read_ratio,
    ROUND(SUM(credits), 4)                                    AS credits,
    ROUND(SUM(cache_read_input_credits) / NULLIF(SUM(credits), 0), 3)           AS cache_read_share_of_credits
FROM V_AGENT_TOKENS_BY_MODEL
WHERE start_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY credits DESC;

-- Q5. Same breakdown for Cortex Code, by interface (cli, desktop, snowsight).
SELECT
    interface,
    model_name,
    COUNT(DISTINCT request_id)                                AS requests,
    SUM(total_input_tokens)                                   AS total_input_tokens,
    ROUND(SUM(cache_read_input_tokens) / NULLIF(SUM(total_input_tokens), 0), 3) AS cache_read_ratio,
    ROUND(SUM(credits), 4)                                    AS credits
FROM V_COCO_TOKENS_BY_MODEL
WHERE usage_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY credits DESC;

-- Q6. Cost center attribution from tags. USER_TAGS and AGENT_TAGS are arrays of
--     {level, tag_database, tag_schema, tag_name, tag_value}. A user or agent can inherit
--     the same tag from several levels, so take one value per request (the most specific
--     level wins) before summing, or the request is counted once per level.
WITH tagged AS (
    SELECT
        r.request_id,
        r.token_credits,
        t.value:tag_value::STRING AS cost_center,
        ROW_NUMBER() OVER (
            PARTITION BY r.request_id
            ORDER BY CASE t.value:level::STRING WHEN 'CORTEX_AGENT' THEN 1 WHEN 'SCHEMA' THEN 2
                                                WHEN 'DATABASE' THEN 3 ELSE 4 END
        ) AS rn
    FROM V_AGENT_REQUESTS r,
         LATERAL FLATTEN(input => r.agent_tags) t
    WHERE r.start_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
      AND UPPER(t.value:tag_name::STRING) = 'COST_CENTER'
)
SELECT cost_center, COUNT(*) AS requests, ROUND(SUM(token_credits), 4) AS token_credits
FROM tagged
WHERE rn = 1
GROUP BY 1
ORDER BY token_credits DESC;

-- Q7. REST API inference: tokens by model and user. Billed in currency, so no credits here.
SELECT
    model_name,
    user_name,
    COUNT(*)                     AS requests,
    SUM(tokens)                  AS tokens,
    SUM(input_tokens)            AS input_tokens,
    SUM(output_tokens)           AS output_tokens
FROM V_REST_API_TOKENS
WHERE usage_time >= DATEADD(day, -$lookback_days, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY tokens DESC
LIMIT 20;

-- Q8. Reconciliation: per surface, view totals against billed credits (complete UTC days only).
SELECT
    surface,
    ROUND(SUM(view_credits), 4)     AS view_credits,
    ROUND(SUM(metered_credits), 4)  AS metered_credits,
    ROUND(SUM(delta), 4)            AS delta
FROM V_RECONCILE_METERING
WHERE usage_date >= DATEADD(day, -$lookback_days, CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())::DATE)
  AND usage_date <  DATEADD(day, -1, CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())::DATE)
GROUP BY 1
ORDER BY 1;
```

### `sql/04_budget_and_quota.sql`

Copy code

```
-- 04_budget_and_quota.sql
-- Spend controls. This file changes account-level cost governance, so run it
-- deliberately and read each step. Budgets and quotas behave differently:
--
--   Budget (SNOWFLAKE.CORE.BUDGET)  Monitors a monthly credit limit for tagged objects
--                                   and runs your stored procedure at thresholds.
--                                   Evaluation is periodic: actions can take up to
--                                   8 hours (2 hours with the latency-optimized option).
--                                   It does not stop spend by itself.
--   Quota  (SNOWFLAKE.CORE.QUOTA)   Per-user limits (monthly, weekly, daily) with built-in
--                                   blocking for AI domains, applied within minutes.
--                                   Some overshoot is expected; limits are never pooled.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';
SET cost_tag      = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.COST_CENTER';
SET cost_center   = 'cookbook';
SET agent_budget_credits  = 50;   -- monthly, all agents tagged COST_CENTER = cookbook

-- Step 1 (ACCOUNTADMIN): let the recipe role create budgets and quotas.
USE ROLE ACCOUNTADMIN;
GRANT DATABASE ROLE SNOWFLAKE.BUDGET_CREATOR TO ROLE IDENTIFIER($cookbook_role);
GRANT DATABASE ROLE SNOWFLAKE.QUOTA_CREATOR  TO ROLE IDENTIFIER($cookbook_role);

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOVERNANCE;

-- Step 2: a log table and a budget custom action. The action runs when the budget
-- crosses a threshold. This one only records the event; replace the INSERT with your
-- enforcement (for example, revoking USAGE on the tagged agents from an end-user role).
CREATE TABLE IF NOT EXISTS BUDGET_ACTION_LOG (
    fired_at      TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    cost_center   STRING,
    threshold_pct NUMBER
);

-- Owner's rights: the SNOWFLAKE application calls this procedure, and it must be able
-- to write the log without granting the application anything on the table itself.
CREATE OR REPLACE PROCEDURE ON_AGENT_BUDGET_THRESHOLD(cost_center STRING, threshold_pct NUMBER)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
    INSERT INTO BUDGET_ACTION_LOG (cost_center, threshold_pct) VALUES (:cost_center, :threshold_pct);
    RETURN 'logged ' || :cost_center || ' at ' || :threshold_pct || '%';
END;
$$;

GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA GOVERNANCE TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE ON_AGENT_BUDGET_THRESHOLD(STRING, NUMBER) TO APPLICATION SNOWFLAKE;

-- Step 3: resource budget for Cortex Agents tagged COST_CENTER = cookbook.
-- Tag an agent to bring it under the budget, for example:
--   ALTER AGENT <db>.<schema>.<agent> SET TAG COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.COST_CENTER = 'cookbook';
CREATE SNOWFLAKE.CORE.BUDGET IF NOT EXISTS AGENT_BUDGET();
CALL AGENT_BUDGET!SET_SPENDING_LIMIT($agent_budget_credits);
CALL AGENT_BUDGET!SET_RESOURCE_TAGS(
    [[(SELECT SYSTEM$REFERENCE('TAG', $cost_tag, 'SESSION', 'APPLYBUDGET')), $cost_center]],
    'UNION');
CALL AGENT_BUDGET!ADD_CUSTOM_ACTION(
    SYSTEM$REFERENCE('PROCEDURE', $cookbook_db || '.GOVERNANCE.ON_AGENT_BUDGET_THRESHOLD(STRING, NUMBER)'),
    ARRAY_CONSTRUCT($cost_center, 100),
    'ACTUAL',
    100);
CALL AGENT_BUDGET!GET_CUSTOM_ACTIONS();

-- Step 4: per-user quota for agents and AI functions, scoped to tagged users only.
-- CoWork and Cortex Code spend is not counted or blocked by this quota. To cover them, also
-- add the SNOWFLAKE INTELLIGENCE and CORTEX CODE domains (see the README).
-- A new quota covers ALL users until you narrow the scope, and nothing is enforced until
-- a limit is set. So: create, scope by tag, confirm the scope, and only then set the limit
-- and turn on blocking.
CREATE SNOWFLAKE.CORE.QUOTA IF NOT EXISTS AI_USER_QUOTA();
CALL AI_USER_QUOTA!ADD_SHARED_RESOURCE('CORTEX AGENT');
CALL AI_USER_QUOTA!ADD_SHARED_RESOURCE('AI FUNCTION');
CALL AI_USER_QUOTA!SET_USER_TAGS(
    [[(SELECT SYSTEM$REFERENCE('TAG', $cost_tag, 'SESSION', 'APPLYBUDGET')), $cost_center]],
    'UNION');
CALL AI_USER_QUOTA!GET_QUOTA_SCOPE();
-- Optional: put yourself in scope to see a block happen.
--   ALTER USER <your_user> SET TAG COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.COST_CENTER = 'cookbook';
CALL AI_USER_QUOTA!GET_USERS();   -- tag resolution can lag up to about 2 hours

-- Step 5 is in 05_quota_limit.sql. Run it only after GET_USERS() above returns the users
-- you expect, and at least 10 minutes after this file: scope changes take about 5 to 10
-- minutes to propagate, and until then the quota can still cover every user.
```

### `sql/05_quota_limit.sql`

Copy code

```
-- 05_quota_limit.sql
-- Step 5 of the spend controls: set the per-user limit on the quota from 04 and turn on
-- built-in blocking. Run this only after AI_USER_QUOTA!GET_USERS() in 04 returned the
-- users you expect, and at least 10 minutes after 04, because scope changes take about
-- 5 to 10 minutes to propagate. Limit changes propagate on the same delay.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';
SET per_user_daily_credits = 5;   -- daily, per tagged user

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOVERNANCE;

-- Check the scope once more before enforcing.
CALL AI_USER_QUOTA!GET_QUOTA_SCOPE();
CALL AI_USER_QUOTA!GET_USERS();

CALL AI_USER_QUOTA!SET_PER_USER_LIMIT($per_user_daily_credits, 'DAILY');
-- Second argument: email blocked users. FALSE keeps the recipe quiet; set TRUE in production.
CALL AI_USER_QUOTA!SET_BLOCK_ENFORCEMENT_ENABLED(TRUE, FALSE);
CALL AI_USER_QUOTA!GET_CONFIG();
CALL AI_USER_QUOTA!GET_ACTIVE_BLOCKS_V2();
```

### `sql/99_teardown.sql`

Copy code

```
-- 99_teardown.sql
-- Removes everything the recipe created. Budgets, quotas, the custom-action procedure,
-- and the tag live inside the recipe database, so dropping the database removes them;
-- the explicit drops below make the order visible and are safe to rerun.

SET cookbook_db   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION';
SET cookbook_wh   = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_WH';
SET cookbook_role = 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION_ANALYST';

USE ROLE ACCOUNTADMIN;

-- If you tagged yourself or an agent with the recipe's COST_CENTER tag in 04, remove it
-- first (dropping the database would otherwise leave the assignment orphaned):
--   ALTER USER <your_user> UNSET TAG COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.COST_CENTER;
--   ALTER AGENT <db>.<schema>.<agent> UNSET TAG COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.COST_CENTER;

-- Drop the role first: Snowflake transfers ownership of the role's objects (the
-- database) to the role running DROP ROLE, so ACCOUNTADMIN can then drop them.
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_role);
-- Spend controls from 04 (no-ops if 04 was never run).
DROP SNOWFLAKE.CORE.QUOTA  IF EXISTS COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.AI_USER_QUOTA;
DROP SNOWFLAKE.CORE.BUDGET IF EXISTS COOKBOOK_AI_USAGE_COST_ATTRIBUTION.GOVERNANCE.AGENT_BUDGET;
DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);

SHOW DATABASES  LIKE 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION%';
SHOW WAREHOUSES LIKE 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION%';
SHOW ROLES      LIKE 'COOKBOOK_AI_USAGE_COST_ATTRIBUTION%';
```
