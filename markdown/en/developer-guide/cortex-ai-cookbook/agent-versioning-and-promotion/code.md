# Agent versioning and promotion: code

Every file in the [Agent versioning and promotion](/developer-guide/cortex-ai-cookbook/agent-versioning-and-promotion) recipe. To run the recipe, download [agent-versioning-and-promotion.zip](/static/samples/cortex-ai-cookbook/agent-versioning-and-promotion.zip), unzip it, and run the scripts from the `agent-versioning-and-promotion/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/agent-versioning-and-promotion); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- 01_setup.sql
-- Agent versioning and promotion: role, warehouse, database, and the agent.
--
-- The first block runs as ACCOUNTADMIN and only creates this recipe's own
-- COOKBOOK_ objects. Everything after USE ROLE IDENTIFIER($agentver_role) runs
-- as the recipe role, which owns the agent.
--
-- The agent has no tools on purpose. Each version's response instruction makes
-- it start every answer with a version tag ("[v1]", "[v2]", ...), so you can
-- see which version served a request without opening traces.
--
-- CREATE AGENT produces two versions with the same spec: a committed VERSION$1
-- and a mutable LIVE version. This file then pins DEFAULT to VERSION$1 and
-- points the PRODUCTION alias at it, so later commits do not change what
-- unversioned or production callers get.
--
-- Idempotent: CREATE ... IF NOT EXISTS never replaces the agent. On a rerun the
-- pin and alias statements re-point DEFAULT and PRODUCTION at VERSION$1, which
-- is the same as a rollback (see 05).
-- =============================================================================

SET agentver_db    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';
SET agentver_wh    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_role  = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_agent = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT';
SET agentver_user  = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($agentver_role)
  COMMENT = 'Cookbook agent-versioning-and-promotion: owns the recipe objects.';
-- Granting the role to SYSADMIN lets ACCOUNTADMIN, which inherits SYSADMIN,
-- drop what the role owns in 99_teardown.sql without relying on secondary roles.
GRANT ROLE IDENTIFIER($agentver_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($agentver_role) TO USER IDENTIFIER($agentver_user);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($agentver_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cookbook agent-versioning-and-promotion';
GRANT USAGE ON WAREHOUSE IDENTIFIER($agentver_wh) TO ROLE IDENTIFIER($agentver_role);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($agentver_db)
  COMMENT = 'Cookbook agent-versioning-and-promotion';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($agentver_db) TO ROLE IDENTIFIER($agentver_role) COPY CURRENT GRANTS;

-- Cortex Agents need SNOWFLAKE.CORTEX_USER or SNOWFLAKE.CORTEX_AGENT_USER.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($agentver_role);

-- ---------------------------------------------------------------------------
-- From here on, run as the recipe role.
-- ---------------------------------------------------------------------------
USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);
USE DATABASE IDENTIFIER($agentver_db);
CREATE SCHEMA IF NOT EXISTS AGENTS;
USE SCHEMA AGENTS;

CREATE AGENT IF NOT EXISTS RELEASE_AGENT
  COMMENT = 'Cookbook: agent used to demonstrate versioning and promotion'
  FROM SPECIFICATION
$$
models:
  orchestration: auto
instructions:
  response: |
    Start every answer with the tag [v1] followed by a space.
    Answer in one short sentence.
$$;

-- Pin DEFAULT to a named version. Without a pin, DEFAULT follows the newest
-- commit, so every COMMIT would silently change what unversioned callers get.
ALTER AGENT IDENTIFIER($agentver_agent) SET DEFAULT_VERSION = 'VERSION$1';

-- Applications call the PRODUCTION alias, never a version number.
-- Unquoted aliases are stored in uppercase: callers must use !PRODUCTION.
ALTER AGENT IDENTIFIER($agentver_agent) MODIFY VERSION VERSION$1 SET ALIAS = production;

SHOW VERSIONS IN AGENT IDENTIFIER($agentver_agent);
```

### `sql/02_commit_candidate.sql`

Copy code

```
-- =============================================================================
-- 02_commit_candidate.sql
-- Iterate on the LIVE version, commit it as a new named version, and point the
-- CANARY alias at that new version.
--
-- Behavior this file relies on:
--   * COMMIT consumes LIVE. A new LIVE version is not created automatically.
--   * ADD LIVE VERSION FROM LAST fails if a LIVE version already exists, so the
--     first block adds one only when it is missing.
--   * MODIFY LIVE VERSION SET SPECIFICATION replaces the whole spec.
--   * Because 01 pinned DEFAULT_VERSION, the commit does not change what
--     unversioned callers or PRODUCTION callers get.
--   * MODIFY VERSION does not accept shortcuts (MODIFY VERSION LAST is a syntax
--     error), so the new version name is read from DESCRIBE AGENT and checked
--     against ^VERSION\$[0-9]+$ before it is used in a statement.
--
-- Rerunnable: each run commits one more named version and moves CANARY to it.
-- =============================================================================

SET agentver_role  = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_agent = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);

-- 1. Make sure there is a LIVE version to edit.
EXECUTE IMMEDIATE $$
BEGIN
  SHOW VERSIONS IN AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET live_count INTEGER := (SELECT COUNT(*) FROM TABLE(RESULT_SCAN(:qid))
                             WHERE "spec_file_path" ILIKE '%/versions/live/');
  IF (live_count = 0) THEN
    ALTER AGENT IDENTIFIER($agentver_agent) ADD LIVE VERSION FROM LAST
      COMMENT = 'Next iteration';
    RETURN 'Added a LIVE version from LAST';
  END IF;
  RETURN 'LIVE version already exists';
END;
$$;

-- 2. Edit LIVE. The whole spec is replaced.
ALTER AGENT IDENTIFIER($agentver_agent) MODIFY LIVE VERSION SET SPECIFICATION =
$$
models:
  orchestration: auto
instructions:
  response: |
    Start every answer with the tag [v2] followed by a space.
    Answer in one short sentence.
$$;

-- 3. Freeze LIVE into the next VERSION$N.
ALTER AGENT IDENTIFIER($agentver_agent) COMMIT COMMENT = 'v2 candidate: new response instructions';

-- 4. Point CANARY at the version just committed (LAST).
EXECUTE IMMEDIATE $$
BEGIN
  DESCRIBE AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET last_version VARCHAR := (SELECT TRY_PARSE_JSON("aliases"):LAST::STRING FROM TABLE(RESULT_SCAN(:qid)));
  IF (NOT REGEXP_LIKE(last_version, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Unexpected version name: ' || COALESCE(last_version, 'NULL');
  END IF;
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) MODIFY VERSION '
                    || last_version || ' SET ALIAS = canary';
  RETURN 'CANARY now points at ' || last_version;
END;
$$;

-- 5. Resume development. The new LIVE starts from the version just committed.
ALTER AGENT IDENTIFIER($agentver_agent) ADD LIVE VERSION FROM LAST
  COMMENT = 'Next iteration after the v2 candidate';

DESCRIBE AGENT IDENTIFIER($agentver_agent);
SELECT "default_version_name", "aliases" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### `sql/03_route_by_version.sql`

Copy code

```
-- =============================================================================
-- 03_route_by_version.sql
-- Send the same question to each version reference and read the version tag
-- in the answer. Shows how aliases and shortcuts resolve.
--
-- Reference forms for DATA_AGENT_RUN('<db>.<schema>.<agent>[!<version>]', ...):
--   !VERSION$N   a named version (system identifier)
--   !<ALIAS>     a user-defined alias; unquoted aliases are stored in uppercase,
--                so use !PRODUCTION, not !production (lowercase returns error
--                399535 "Version not found")
--   !LIVE        the mutable live version (shown as DRAFT in Snowsight)
--   !FIRST       the first committed named version
--   !LAST        the most recently created named version
--   !DEFAULT     the default version; same as omitting the suffix
--
-- The agent argument must be a constant (a literal or a session variable).
-- A column expression fails to compile, so routing logic has to choose between
-- fixed references (see 04).
-- =============================================================================

SET agentver_role = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh   = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_q    = '{"messages":[{"role":"user","content":[{"type":"text","text":"Say hello."}]}]}';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);

WITH runs AS (
  SELECT 'PRODUCTION' AS ref, TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!PRODUCTION', $agentver_q)) AS j
  UNION ALL SELECT 'CANARY',  TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!CANARY', $agentver_q))
  UNION ALL SELECT 'DEFAULT', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!DEFAULT', $agentver_q))
  UNION ALL SELECT '(none)',  TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT', $agentver_q))
  UNION ALL SELECT 'FIRST',   TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!FIRST', $agentver_q))
  UNION ALL SELECT 'LAST',    TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!LAST', $agentver_q))
  UNION ALL SELECT 'LIVE',    TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!LIVE', $agentver_q))
  UNION ALL SELECT 'production (lowercase)', TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN('COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!production', $agentver_q))
)
SELECT r.ref,
       REGEXP_SUBSTR(MAX(IFF(f.value:type::STRING = 'text', f.value:text::STRING, NULL)), '\\[v[0-9]+\\]') AS version_tag,
       ANY_VALUE(r.j:message::STRING) AS error_message
FROM runs r, LATERAL FLATTEN(input => r.j:content, OUTER => TRUE) f
GROUP BY r.ref
ORDER BY r.ref;
```

### `sql/04_ab_routing.sql`

Copy code

```
-- =============================================================================
-- 04_ab_routing.sql
-- Application-layer A/B routing by alias.
--
-- Snowflake does not split traffic between agent versions. The caller decides
-- which alias serves a request. This procedure buckets a stable routing key
-- (for example a user id) into 0-99 and sends the request to CANARY when the
-- bucket is below CANARY_PERCENT, otherwise to PRODUCTION. The same key always
-- lands in the same bucket, so a user sees one version consistently.
--
-- Design notes:
--   * The agent argument of DATA_AGENT_RUN must be a constant, so the procedure
--     chooses between two literal references. That is also an allowlist: a
--     caller cannot route to any other agent or version.
--   * The request body is built with OBJECT_CONSTRUCT from the question, never
--     by concatenating text into JSON.
--   * EXECUTE AS CALLER: the agent runs with the caller's privileges.
--   * Every request is logged with the alias that served it, so feedback and
--     scores can be compared per version. The routing key is stored hashed.
-- =============================================================================

SET agentver_role = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh   = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_db   = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);
USE DATABASE IDENTIFIER($agentver_db);
USE SCHEMA AGENTS;

CREATE TABLE IF NOT EXISTS AB_REQUEST_LOG (
  LOGGED_AT        TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
  ROUTING_KEY_HASH VARCHAR,
  BUCKET           NUMBER,
  SERVED_ALIAS     VARCHAR,
  QUESTION         VARCHAR,
  ANSWER           VARCHAR,
  RESPONSE         VARIANT
);

CREATE OR REPLACE PROCEDURE ASK_WITH_AB_ROUTING(
  ROUTING_KEY VARCHAR, QUESTION VARCHAR, CANARY_PERCENT NUMBER)
RETURNS VARIANT
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
  bucket NUMBER;
  served_alias VARCHAR;
  body VARCHAR;
  raw VARCHAR;
  resp VARIANT;
  answer VARCHAR;
BEGIN
  IF (CANARY_PERCENT IS NULL OR CANARY_PERCENT < 0 OR CANARY_PERCENT > 100) THEN
    RETURN OBJECT_CONSTRUCT('error', 'CANARY_PERCENT must be between 0 and 100');
  END IF;
  bucket := MOD(ABS(HASH(:ROUTING_KEY)), 100);
  body := TO_JSON(OBJECT_CONSTRUCT('messages', ARRAY_CONSTRUCT(OBJECT_CONSTRUCT(
            'role', 'user',
            'content', ARRAY_CONSTRUCT(OBJECT_CONSTRUCT('type', 'text', 'text', :QUESTION))))));
  IF (bucket < CANARY_PERCENT) THEN
    served_alias := 'CANARY';
    raw := (SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
              'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!CANARY', :body));
  ELSE
    served_alias := 'PRODUCTION';
    raw := (SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
              'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT!PRODUCTION', :body));
  END IF;
  resp := TRY_PARSE_JSON(:raw);
  answer := (SELECT LISTAGG(f.value:text::STRING, '')
             FROM TABLE(FLATTEN(input => :resp:content)) f
             WHERE f.value:type::STRING = 'text');
  INSERT INTO COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.AB_REQUEST_LOG
    (ROUTING_KEY_HASH, BUCKET, SERVED_ALIAS, QUESTION, ANSWER, RESPONSE)
    SELECT SHA2(:ROUTING_KEY, 256), :bucket, :served_alias, :QUESTION, :answer, :resp;
  RETURN OBJECT_CONSTRUCT('served_alias', served_alias, 'bucket', bucket,
                          'answer', answer, 'error', resp:message::STRING);
END;
$$;

-- Send a few synthetic users through a 50/50 split.
CALL ASK_WITH_AB_ROUTING('user-001@example.com', 'Say hello.', 50);
CALL ASK_WITH_AB_ROUTING('user-002@example.com', 'Say hello.', 50);
CALL ASK_WITH_AB_ROUTING('user-003@example.com', 'Say hello.', 50);
CALL ASK_WITH_AB_ROUTING('user-001@example.com', 'Say hello again.', 50);

-- Which alias served which bucket, and which version tag came back.
SELECT BUCKET, SERVED_ALIAS,
       REGEXP_SUBSTR(ANSWER, '\\[v[0-9]+\\]') AS VERSION_TAG,
       LEFT(ROUTING_KEY_HASH, 12) AS KEY_HASH
FROM COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.AB_REQUEST_LOG
ORDER BY LOGGED_AT;
```

### `sql/05_promote.sql`

Copy code

```
-- =============================================================================
-- 05_promote.sql
-- Promote the CANARY version to PRODUCTION and make it the DEFAULT.
--
-- Promotion is metadata only: it moves the PRODUCTION alias and the DEFAULT pin.
-- Callers keep calling !PRODUCTION (or no suffix) and get the new version on
-- their next request.
--
-- Observed behavior this relies on:
--   * MODIFY VERSION VERSION$N SET ALIAS = x succeeds when another version
--     already holds alias x. The alias moves to VERSION$N and the previous
--     holder is left without it. No UNSET is needed first.
--   * A version holds at most one alias. Setting PRODUCTION on the version that
--     holds CANARY replaces CANARY, so after promotion there is no CANARY alias
--     until 02 commits the next candidate. Callers of !CANARY get error 399535
--     in the meantime; 04 routes by alias, so run it only while CANARY exists.
--
-- The previous PRODUCTION version is written to PROMOTION_LOG so 06 can roll
-- back to it without anyone having to remember a version number.
-- =============================================================================

SET agentver_role  = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_db    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';
SET agentver_agent = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);
USE DATABASE IDENTIFIER($agentver_db);
USE SCHEMA AGENTS;

CREATE TABLE IF NOT EXISTS PROMOTION_LOG (
  PROMOTED_AT   TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
  ACTION        VARCHAR,
  FROM_VERSION  VARCHAR,
  TO_VERSION    VARCHAR,
  PROMOTED_BY   VARCHAR DEFAULT CURRENT_USER()
);

EXECUTE IMMEDIATE $$
BEGIN
  DESCRIBE AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET aliases VARIANT := (SELECT TRY_PARSE_JSON("aliases") FROM TABLE(RESULT_SCAN(:qid)));
  LET candidate VARCHAR := aliases:CANARY::STRING;
  LET current_prod VARCHAR := aliases:PRODUCTION::STRING;

  IF (candidate IS NULL) THEN
    RETURN 'No CANARY alias to promote. Run 02 first.';
  END IF;
  IF (NOT REGEXP_LIKE(candidate, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Refusing to promote unexpected version name: ' || candidate;
  END IF;
  IF (candidate = current_prod) THEN
    RETURN candidate || ' is already PRODUCTION';
  END IF;

  INSERT INTO PROMOTION_LOG (ACTION, FROM_VERSION, TO_VERSION)
    VALUES ('promote', :current_prod, :candidate);

  -- Move the alias, then the default pin. Both are metadata-only changes.
  -- A version holds at most one alias, so this also removes CANARY from the
  -- candidate, and the previous PRODUCTION version is left with no alias.
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) MODIFY VERSION '
                    || candidate || ' SET ALIAS = production';
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) SET DEFAULT_VERSION = '''
                    || candidate || '''';
  RETURN 'Promoted ' || candidate || ' (previous PRODUCTION: ' || COALESCE(current_prod, 'none') || ')';
END;
$$;

DESCRIBE AGENT IDENTIFIER($agentver_agent);
SELECT "default_version_name", "aliases" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### `sql/06_rollback.sql`

Copy code

```
-- =============================================================================
-- 06_rollback.sql
-- Roll PRODUCTION and DEFAULT back to the version that was PRODUCTION before
-- the most recent promotion (read from PROMOTION_LOG, written by 05).
--
-- Rollback is the same metadata operation as promotion, pointed backwards.
-- Named versions are immutable, so the version you roll back to is exactly the
-- configuration that served production before.
-- =============================================================================

SET agentver_role  = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_db    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';
SET agentver_agent = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);
USE DATABASE IDENTIFIER($agentver_db);
USE SCHEMA AGENTS;

EXECUTE IMMEDIATE $$
BEGIN
  LET target VARCHAR := (SELECT FROM_VERSION FROM PROMOTION_LOG
                         WHERE ACTION = 'promote'
                         ORDER BY PROMOTED_AT DESC LIMIT 1);
  IF (target IS NULL) THEN
    RETURN 'Nothing to roll back: no promotion recorded in PROMOTION_LOG.';
  END IF;
  IF (NOT REGEXP_LIKE(target, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Refusing to roll back to unexpected version name: ' || target;
  END IF;

  DESCRIBE AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET current_prod VARCHAR := (SELECT TRY_PARSE_JSON("aliases"):PRODUCTION::STRING FROM TABLE(RESULT_SCAN(:qid)));
  IF (current_prod = target) THEN
    RETURN target || ' is already PRODUCTION';
  END IF;

  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) MODIFY VERSION '
                    || target || ' SET ALIAS = production';
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) SET DEFAULT_VERSION = '''
                    || target || '''';
  INSERT INTO PROMOTION_LOG (ACTION, FROM_VERSION, TO_VERSION)
    VALUES ('rollback', :current_prod, :target);
  RETURN 'Rolled PRODUCTION back from ' || COALESCE(current_prod, 'none') || ' to ' || target;
END;
$$;

DESCRIBE AGENT IDENTIFIER($agentver_agent);
SELECT "default_version_name", "aliases" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

SELECT * FROM PROMOTION_LOG ORDER BY PROMOTED_AT;
```

### `sql/07_import_version_from_stage.sql`

Copy code

```
-- =============================================================================
-- 07_import_version_from_stage.sql
-- Create a named version from a spec file on a stage, bypassing LIVE.
--
-- This is the CI/CD path: the agent spec lives in Git, a pipeline puts the
-- merged file on a stage (or reads it from a Git repository stage), and
-- ADD VERSION FROM creates the next VERSION$N without editing LIVE. The
-- DEFAULT pin is not touched; you promote the imported version with 05 like
-- any other. ADD VERSION FROM requires that no LIVE version exists (see below).
--
-- The stage folder must contain agent_spec.yaml, the same layout Snowflake uses
-- for each version (LIST 'snow://agent/<agent>/versions/VERSION$1/').
--
-- To keep the recipe self-contained this file writes the spec with COPY INTO.
-- In a pipeline you would PUT the file from your repository instead, for
-- example: PUT file://agent/agent_spec.yaml @AGENT_SPECS/release_v3/
--          AUTO_COMPRESS = FALSE OVERWRITE = TRUE;
--
-- Rerunnable: each run imports one more named version and moves CANARY to it.
-- =============================================================================

SET agentver_role  = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';
SET agentver_wh    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_db    = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';
SET agentver_agent = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION.AGENTS.RELEASE_AGENT';

USE ROLE IDENTIFIER($agentver_role);
USE WAREHOUSE IDENTIFIER($agentver_wh);
USE DATABASE IDENTIFIER($agentver_db);
USE SCHEMA AGENTS;

-- Agent specs are copied onto this stage by CI. Server-side encryption keeps the
-- files readable by Snowflake services.
CREATE STAGE IF NOT EXISTS AGENT_SPECS
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  COMMENT = 'Agent spec files imported as named versions';

COPY INTO @AGENT_SPECS/release_v3/agent_spec.yaml
FROM (SELECT $$models:
  orchestration: auto
instructions:
  response: |
    Start every answer with the tag [v3] followed by a space.
    Answer in one short sentence.
$$)
FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_DELIMITER = NONE
               FIELD_OPTIONALLY_ENCLOSED_BY = NONE ESCAPE_UNENCLOSED_FIELD = NONE)
SINGLE = TRUE HEADER = FALSE OVERWRITE = TRUE;

LIST @AGENT_SPECS/release_v3/;

-- Observed: ADD VERSION FROM fails with "There is already a live version.
-- Please commit it first." while a LIVE version exists, and LIVE cannot be
-- dropped. Agents that are deployed from CI should not keep a LIVE version.
-- Here 02 left one behind, so commit it as a snapshot before importing.
EXECUTE IMMEDIATE $$
BEGIN
  SHOW VERSIONS IN AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET live_count INTEGER := (SELECT COUNT(*) FROM TABLE(RESULT_SCAN(:qid))
                             WHERE "spec_file_path" ILIKE '%/versions/live/');
  IF (live_count > 0) THEN
    ALTER AGENT IDENTIFIER($agentver_agent) COMMIT
      COMMENT = 'Snapshot of LIVE before importing a version from stage';
    RETURN 'Committed the existing LIVE version';
  END IF;
  RETURN 'No LIVE version';
END;
$$;

ALTER AGENT IDENTIFIER($agentver_agent) ADD VERSION FROM @AGENT_SPECS/release_v3
  COMMENT = 'v3: imported from stage';

-- Make the imported version the next canary.
EXECUTE IMMEDIATE $$
BEGIN
  DESCRIBE AGENT IDENTIFIER($agentver_agent);
  LET qid VARCHAR := SQLID;
  LET last_version VARCHAR := (SELECT TRY_PARSE_JSON("aliases"):LAST::STRING FROM TABLE(RESULT_SCAN(:qid)));
  IF (last_version IS NULL OR NOT REGEXP_LIKE(last_version, '^VERSION\\$[0-9]+$')) THEN
    RETURN 'Unexpected version name: ' || COALESCE(last_version, 'NULL');
  END IF;
  EXECUTE IMMEDIATE 'ALTER AGENT IDENTIFIER($agentver_agent) MODIFY VERSION '
                    || last_version || ' SET ALIAS = canary';
  RETURN 'Imported ' || last_version || ' and pointed CANARY at it';
END;
$$;

SHOW VERSIONS IN AGENT IDENTIFIER($agentver_agent);
SELECT "name", "alias", "is_default", "comment" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- 99_teardown.sql
-- Removes everything this recipe created. There are no account-level
-- parameter changes to restore.
-- =============================================================================

SET agentver_db   = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION';
SET agentver_wh   = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_WH';
SET agentver_role = 'COOKBOOK_AGENT_VERSIONING_AND_PROMOTION_ADMIN';

USE ROLE ACCOUNTADMIN;

-- Dropping the database drops the agent, every named version, the stage, and
-- the log tables.
DROP DATABASE IF EXISTS IDENTIFIER($agentver_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($agentver_wh);
DROP ROLE IF EXISTS IDENTIFIER($agentver_role);

SHOW DATABASES LIKE 'COOKBOOK_AGENT_VERSIONING%';
SHOW WAREHOUSES LIKE 'COOKBOOK_AGENT_VERSIONING%';
SHOW ROLES LIKE 'COOKBOOK_AGENT_VERSIONING%';
```
