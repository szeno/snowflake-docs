# Size Cortex Code per-user limits from real usage: code

Every file in the [Size Cortex Code per-user limits from real usage](/developer-guide/cortex-ai-cookbook/coco-user-budget-sizing) recipe. To run the recipe, download [coco-user-budget-sizing.zip](/static/samples/cortex-ai-cookbook/coco-user-budget-sizing.zip), unzip it, and run the scripts from the `coco-user-budget-sizing/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/coco-user-budget-sizing); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- 01_setup.sql
-- Role, warehouse, database, tags, and privileges for sizing and enforcing
-- per-user Cortex Code (CoCo) limits. Run as ACCOUNTADMIN.

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';
SET me            = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

-- Recipe role. It rolls up to SYSADMIN so ACCOUNTADMIN can read the
-- parameter backup table during teardown.
CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_role);
GRANT ROLE IDENTIFIER($cookbook_role) TO USER IDENTIFIER($me);
GRANT ROLE IDENTIFIER($cookbook_role) TO ROLE SYSADMIN;

-- Read SNOWFLAKE_COCO_USAGE_HISTORY, create quotas and budgets.
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER   TO ROLE IDENTIFIER($cookbook_role);
GRANT DATABASE ROLE SNOWFLAKE.QUOTA_CREATOR  TO ROLE IDENTIFIER($cookbook_role);
GRANT DATABASE ROLE SNOWFLAKE.BUDGET_CREATOR TO ROLE IDENTIFIER($cookbook_role);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db)
  TO ROLE IDENTIFIER($cookbook_role) COPY CURRENT GRANTS;

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);

CREATE SCHEMA IF NOT EXISTS SIZING;
CREATE SCHEMA IF NOT EXISTS GOVERNANCE;

-- USAGE_TIER marks power users. Every untagged user is a General user.
CREATE TAG IF NOT EXISTS GOVERNANCE.USAGE_TIER ALLOWED_VALUES 'power'
  COMMENT = 'CoCo usage tier; power = 15+ active days in 30';
-- COST_CENTER scopes alert-only team budgets.
CREATE TAG IF NOT EXISTS GOVERNANCE.COST_CENTER
  COMMENT = 'Team or cost center for CoCo budget alerts';

-- Original account parameter values, captured once by 05 and restored by teardown.
CREATE TABLE IF NOT EXISTS GOVERNANCE.PARAM_BACKUP (
  param_name     STRING,
  account_value  STRING,      -- NULL when the parameter was not set at account level
  captured_at    TIMESTAMP_LTZ
);

SHOW TAGS IN SCHEMA GOVERNANCE;
```

### `sql/02_size_your_limits.sql`

Copy code

```
-- 02_size_your_limits.sql
-- Compute your own monthly and daily CoCo percentiles, back-test candidate
-- limits, and list suggested power users. Creates one view (SIZING.USER_DAILY);
-- everything else is read only.

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';
SET lookback_days    = 30;    -- window for sizing
SET power_min_days   = 15;    -- active days in the window that make a power user
SET general_monthly  = 150;   -- candidate limits to back-test
SET power_monthly    = 1500;
SET general_daily    = 35;
SET power_daily      = 150;

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);

-- One row per user per UTC day, with a tier derived from active days.
CREATE OR REPLACE VIEW SIZING.USER_DAILY AS
WITH daily AS (
  SELECT user_name,
         TO_DATE(CONVERT_TIMEZONE('UTC', usage_time)) AS usage_day,
         SUM(token_credits)                           AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY
  WHERE usage_time >= DATEADD('day', -$lookback_days, CURRENT_TIMESTAMP())
  GROUP BY 1, 2
  HAVING SUM(token_credits) > 0   -- active days only; inactive users never appear
)
SELECT d.*,
       IFF(COUNT(*) OVER (PARTITION BY user_name) >= $power_min_days, 'power', 'general') AS tier
FROM daily d;

-- 1. Monthly (window) spend percentiles by tier.
SELECT tier,
       COUNT(*)                                             AS users,
       ROUND(RATIO_TO_REPORT(SUM(credits)) OVER () * 100, 1) AS pct_of_credits,
       ROUND(PERCENTILE_CONT(0.50)  WITHIN GROUP (ORDER BY credits), 1) AS p50,
       ROUND(PERCENTILE_CONT(0.90)  WITHIN GROUP (ORDER BY credits), 1) AS p90,
       ROUND(PERCENTILE_CONT(0.99)  WITHIN GROUP (ORDER BY credits), 1) AS p99,
       ROUND(PERCENTILE_CONT(0.995) WITHIN GROUP (ORDER BY credits), 1) AS p995
FROM (SELECT user_name, tier, SUM(credits) AS credits FROM SIZING.USER_DAILY GROUP BY 1, 2)
GROUP BY tier ORDER BY tier;
-- Guide: monthly limit ~2x p99 for small groups (<200 users), ~p99.5 for large ones.

-- 2. Daily spend percentiles by tier (active days only).
SELECT tier,
       ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY credits), 1) AS daily_p50,
       ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY credits), 1) AS daily_p90,
       ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY credits), 1) AS daily_p99,
       ROUND(MAX(credits), 1)                                          AS daily_max
FROM SIZING.USER_DAILY
GROUP BY tier ORDER BY tier;
-- Guide: daily limit ~3-4x the daily p99, and well below the monthly limit.

-- 3. Back-test the candidate limits: who would have been blocked, and how much spend was above the limit.
WITH monthly AS (
  SELECT user_name, tier, SUM(credits) AS credits FROM SIZING.USER_DAILY GROUP BY 1, 2
), limits AS (
  SELECT 'general' AS tier, $general_monthly AS monthly_limit, $general_daily AS daily_limit
  UNION ALL SELECT 'power', $power_monthly, $power_daily
), m_test AS (
  SELECT l.tier, l.monthly_limit,
         ROUND(100 * COUNT_IF(m.credits > l.monthly_limit) / COUNT(*), 2)                AS pct_users_blocked_monthly,
         ROUND(100 * SUM(GREATEST(m.credits - l.monthly_limit, 0)) / SUM(m.credits), 1) AS pct_credits_above_monthly
  FROM limits l JOIN monthly m ON m.tier = l.tier
  GROUP BY 1, 2
), d_test AS (
  SELECT l.tier, l.daily_limit,
         ROUND(100 * COUNT_IF(d.credits > l.daily_limit) / COUNT(*), 2)                  AS pct_user_days_blocked_daily,
         ROUND(100 * SUM(GREATEST(d.credits - l.daily_limit, 0)) / SUM(d.credits), 1)   AS pct_credits_clipped_daily
  FROM limits l JOIN SIZING.USER_DAILY d ON d.tier = l.tier
  GROUP BY 1, 2
)
SELECT * FROM m_test JOIN d_test USING (tier) ORDER BY tier;
-- Aim for under 1% of users blocked per month and well under 1% of user-days blocked per day.

-- 4. Suggested power users, with the statements that tag them (run those as a role
--    with APPLY on the tag and on the users, for example ACCOUNTADMIN).
SELECT user_name,
       COUNT(*)               AS active_days,
       ROUND(SUM(credits), 1) AS credits,
       'ALTER USER "' || REPLACE(user_name, '"', '""') || '" SET TAG '
         || $cookbook_db || '.GOVERNANCE.USAGE_TIER = ''power'';' AS tag_statement
FROM SIZING.USER_DAILY
WHERE tier = 'power'
GROUP BY user_name
ORDER BY credits DESC;
```

### `sql/03_quotas_and_budget.sql`

Copy code

```
-- 03_quotas_and_budget.sql
-- Create the General and Power quotas and an alert-only team budget, set their
-- scope and notifications. Limits come in 04, after scope has propagated.

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';
SET tier_tag        = 'COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.USAGE_TIER';
SET cost_center_tag = 'COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.COST_CENTER';
SET admin_emails    = 'admin@example.com';   -- comma-separated, verified email addresses
SET team                 = 'data-platform';  -- COST_CENTER value for the example team budget
SET team_monthly_credits = 3000;
SET notify_user = FALSE;   -- TRUE emails each user at 80% projected and 100% of their limit;
                           -- leave FALSE until admins have reviewed the numbers

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOVERNANCE;

-- General quota: every CoCo user except those tagged USAGE_TIER = 'power'.
CREATE SNOWFLAKE.CORE.QUOTA IF NOT EXISTS COCO_GENERAL_QUOTA();
CALL COCO_GENERAL_QUOTA!ADD_SHARED_RESOURCE('CORTEX CODE');
CALL COCO_GENERAL_QUOTA!EXCLUDE_USERS('TAG',
  [[(SELECT SYSTEM$REFERENCE('TAG', $tier_tag, 'SESSION', 'APPLYBUDGET')), 'power']]);
CALL COCO_GENERAL_QUOTA!ADD_NOTIFICATION_THRESHOLD(80,  'PROJECTED', $notify_user, 'MONTHLY');
CALL COCO_GENERAL_QUOTA!ADD_NOTIFICATION_THRESHOLD(100, 'ACTUAL',    $notify_user, 'MONTHLY');
CALL COCO_GENERAL_QUOTA!SET_ADMIN_EMAILS($admin_emails);

-- Power quota: only users tagged USAGE_TIER = 'power'.
CREATE SNOWFLAKE.CORE.QUOTA IF NOT EXISTS COCO_POWER_QUOTA();
CALL COCO_POWER_QUOTA!ADD_SHARED_RESOURCE('CORTEX CODE');
CALL COCO_POWER_QUOTA!SET_USER_TAGS(
  [[(SELECT SYSTEM$REFERENCE('TAG', $tier_tag, 'SESSION', 'APPLYBUDGET')), 'power']], 'UNION');
CALL COCO_POWER_QUOTA!ADD_NOTIFICATION_THRESHOLD(80,  'PROJECTED', $notify_user, 'MONTHLY');
CALL COCO_POWER_QUOTA!ADD_NOTIFICATION_THRESHOLD(100, 'ACTUAL',    $notify_user, 'MONTHLY');
CALL COCO_POWER_QUOTA!SET_ADMIN_EMAILS($admin_emails);

-- Team budget: watches a team's total CoCo spend and alerts. It has no custom
-- action, so it never blocks anyone; the quotas do the enforcing.
CREATE SNOWFLAKE.CORE.BUDGET IF NOT EXISTS COCO_TEAM_BUDGET();
CALL COCO_TEAM_BUDGET!SET_SPENDING_LIMIT($team_monthly_credits);
CALL COCO_TEAM_BUDGET!SET_USER_TAGS(
  [[(SELECT SYSTEM$REFERENCE('TAG', $cost_center_tag, 'SESSION', 'APPLYBUDGET')), $team]], 'UNION');
CALL COCO_TEAM_BUDGET!ADD_SHARED_RESOURCE('CORTEX CODE');
CALL COCO_TEAM_BUDGET!SET_EMAIL_NOTIFICATIONS($admin_emails);
CALL COCO_TEAM_BUDGET!SET_NOTIFICATION_THRESHOLD(80);

-- Check scope. Wait 5-10 minutes (up to ~2 hours for new tag assignments) before running 04.
CALL COCO_GENERAL_QUOTA!GET_QUOTA_SCOPE();
CALL COCO_POWER_QUOTA!GET_QUOTA_SCOPE();
```

### `sql/04_limits.sql`

Copy code

```
-- 04_limits.sql
-- Set monthly and daily per-user limits. Run 5-10 minutes after 03.
-- Blocking is off by default: the quotas alert but never block. To enforce,
-- set block_enabled = TRUE and rerun this script (see "Turn on enforcement").

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';
SET general_monthly = 150;
SET general_daily   = 35;
SET power_monthly   = 1500;
SET power_daily     = 150;
SET block_enabled   = FALSE;  -- TRUE to block users at their limit
SET notify_blocked  = TRUE;   -- email users when they are blocked (only applies while blocking)

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOVERNANCE;

-- Quota limits. Omitting the cycle means monthly.
CALL COCO_GENERAL_QUOTA!SET_PER_USER_LIMIT($general_monthly);
CALL COCO_GENERAL_QUOTA!SET_PER_USER_LIMIT($general_daily, 'DAILY');
CALL COCO_GENERAL_QUOTA!SET_BLOCK_ENFORCEMENT_ENABLED($block_enabled, $notify_blocked);

CALL COCO_POWER_QUOTA!SET_PER_USER_LIMIT($power_monthly);
CALL COCO_POWER_QUOTA!SET_PER_USER_LIMIT($power_daily, 'DAILY');
CALL COCO_POWER_QUOTA!SET_BLOCK_ENFORCEMENT_ENABLED($block_enabled, $notify_blocked);

CALL COCO_GENERAL_QUOTA!GET_CONFIG();
CALL COCO_POWER_QUOTA!GET_CONFIG();
```

### `sql/05_account_backstop.sql`

Copy code

```
-- 05_account_backstop.sql
-- OPTIONAL. Sets the account-wide CoCo daily limit parameters, which apply to
-- every user on each surface, including anyone no quota covers. This changes
-- account-level state: review it before running. Run as ACCOUNTADMIN.

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';
SET backstop_daily = 300;    -- per user, per surface, rolling 24h; -1 = unlimited, 0 blocks all use

USE ROLE IDENTIFIER($cookbook_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE DATABASE IDENTIFIER($cookbook_db);
USE SCHEMA GOVERNANCE;

-- Back up the current account values once, so teardown restores the originals.
SHOW PARAMETERS LIKE 'CORTEX_CODE_%_DAILY_EST_CREDIT_LIMIT_PER_USER' IN ACCOUNT;
INSERT INTO PARAM_BACKUP
SELECT "key", IFF("level" = 'ACCOUNT', "value", NULL), CURRENT_TIMESTAMP()
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE "key" NOT IN (SELECT param_name FROM PARAM_BACKUP);

USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER       = $backstop_daily;
ALTER ACCOUNT SET CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER   = $backstop_daily;
ALTER ACCOUNT SET CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER = $backstop_daily;

SHOW PARAMETERS LIKE 'CORTEX_CODE_%_DAILY_EST_CREDIT_LIMIT_PER_USER' IN ACCOUNT;
```

### `sql/99_teardown.sql`

Copy code

```
-- 99_teardown.sql
-- Remove quotas, budget, and recipe objects, and restore the original CoCo
-- daily limit parameters if 05 changed them. Run as ACCOUNTADMIN. Safe to re-run.

SET cookbook_db   = 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SET cookbook_wh   = 'COOKBOOK_COCO_USER_BUDGET_SIZING_WH';
SET cookbook_role = 'COOKBOOK_COCO_USER_BUDGET_SIZING_ADMIN';

USE ROLE ACCOUNTADMIN;
-- The parameter restore below needs a warehouse. CREATE IF NOT EXISTS keeps
-- teardown safe to re-run after the warehouse has already been dropped.
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
USE WAREHOUSE IDENTIFIER($cookbook_wh);

-- Drop the quotas and budget, then restore each parameter: re-set the original
-- account value, or unset it if it was not set at account level. Values are cast
-- to NUMBER before use. Skipped when the database is already gone, because
-- DROP ... IF EXISTS on a quota or budget fails if its database does not exist.
EXECUTE IMMEDIATE $$
DECLARE
  db_count INTEGER;
  c CURSOR FOR SELECT param_name, TRY_TO_NUMBER(account_value) AS v
               FROM COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.PARAM_BACKUP;
BEGIN
  SHOW DATABASES LIKE 'COOKBOOK_COCO_USER_BUDGET_SIZING';
  SELECT COUNT(*) INTO :db_count FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
  IF (db_count = 0) THEN
    RETURN 'recipe database not found; quotas, budget and parameters already handled';
  END IF;

  EXECUTE IMMEDIATE 'DROP SNOWFLAKE.CORE.QUOTA  IF EXISTS COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.COCO_GENERAL_QUOTA';
  EXECUTE IMMEDIATE 'DROP SNOWFLAKE.CORE.QUOTA  IF EXISTS COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.COCO_POWER_QUOTA';
  EXECUTE IMMEDIATE 'DROP SNOWFLAKE.CORE.BUDGET IF EXISTS COOKBOOK_COCO_USER_BUDGET_SIZING.GOVERNANCE.COCO_TEAM_BUDGET';

  FOR r IN c DO
    IF (r.param_name NOT IN ('CORTEX_CODE_CLI_DAILY_EST_CREDIT_LIMIT_PER_USER',
                             'CORTEX_CODE_DESKTOP_DAILY_EST_CREDIT_LIMIT_PER_USER',
                             'CORTEX_CODE_SNOWSIGHT_DAILY_EST_CREDIT_LIMIT_PER_USER')) THEN
      CONTINUE;
    END IF;
    IF (r.v IS NULL) THEN
      EXECUTE IMMEDIATE 'ALTER ACCOUNT UNSET ' || r.param_name;
    ELSE
      EXECUTE IMMEDIATE 'ALTER ACCOUNT SET ' || r.param_name || ' = ' || r.v::NUMBER;
    END IF;
  END FOR;
  RETURN 'quotas and budget dropped; parameters restored';
END;
$$;

-- Dropping the database drops the USAGE_TIER and COST_CENTER tags, which also
-- removes their assignments from users.
DROP ROLE      IF EXISTS IDENTIFIER($cookbook_role);
DROP DATABASE  IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);

SHOW ROLES      LIKE 'COOKBOOK_COCO_USER_BUDGET_SIZING%';
SHOW DATABASES  LIKE 'COOKBOOK_COCO_USER_BUDGET_SIZING';
SHOW WAREHOUSES LIKE 'COOKBOOK_COCO_USER_BUDGET_SIZING%';
SHOW PARAMETERS LIKE 'CORTEX_CODE_%_DAILY_EST_CREDIT_LIMIT_PER_USER' IN ACCOUNT;
```
