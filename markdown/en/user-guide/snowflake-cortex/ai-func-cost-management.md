# Managing Cortex AI Function costs with Account Usage

Snowflake Cortex AI Functions (AI\_COMPLETE, AI\_SUMMARIZE, AI\_TRANSLATE, AI\_SENTIMENT, and others) consume credits based
on token or page usage. Without monitoring and controls, costs for using these functions can escalate quickly due to:

- Unoptimized prompts generating excessive tokens
- Long-running or runaway queries
- Lack of per-user spending limits
- Insufficient visibility into usage patterns

This topic suggests strategies for monitoring, managing, and controlling the costs associated with Snowflake Cortex AI
Functions. Using the CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view, you can track usage patterns and implement automated cost
controls. These techniques can help you monitor usage, alert when spending limits are exceeded, control access to
functions based on monthly limits, and stop runaway queries.

## Usage history view

The SNOWFLAKE.ACCOUNT\_USAGE.CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view provides detailed telemetry for all Cortex AI Functions invoked via SQL.
The view has a maximum latency of five minutes, although data may be available in as few as two minutes after function execution begins.
For detailed information on this view, see the [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_ai_functions_usage_history).

## Basic usage monitoring

The following queries help you understand your AI Functions usage patterns. Run these periodically yourself, or integrate them into dashboards for ongoing visibility.

### Daily credit consumption by function and model

Track daily spending trends to identify usage spikes and understand which functions and models consume the most credits.

Copy code

```
SELECT
    DATE_TRUNC('day', START_TIME) AS usage_date,
    FUNCTION_NAME,
    MODEL_NAME,
    SUM(CREDITS) AS total_credits,
    COUNT(DISTINCT QUERY_ID) AS query_count
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY
WHERE START_TIME >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY usage_date DESC, total_credits DESC;
```

### Monthly credit consumption by user

Identify top consumers and track per-user spending over time. This query joins with the USERS view to provide user details including email and default role for easier identification and follow-up.

Copy code

```
SELECT
    DATE_TRUNC('month', h.START_TIME) AS usage_month,
    u.NAME AS user_name,
    u.EMAIL,
    u.DEFAULT_ROLE,
    SUM(h.CREDITS) AS total_credits,
    COUNT(DISTINCT h.QUERY_ID) AS query_count
FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY h
JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u
    ON h.USER_ID = u.USER_ID
WHERE h.START_TIME >= DATEADD('month', -3, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3, 4
ORDER BY usage_month DESC, total_credits DESC;
```

## Cost control

Define automated mechanisms to detect excessive spending and take corrective action. These queries can be used independently of each other, or combined for comprehensive cost governance.

### Account-level monthly spending alert

Set up an automated alert that monitors total monthly AI Function credit consumption across your entire account. When spending exceeds a defined threshold, the alert sends an email notification to designated administrators.
Setting up the alert requires the following privileges on the role running these examples:

Copy code

```
-- Run as ACCOUNTADMIN
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE <your_role>;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE <your_role>;
GRANT EXECUTE ALERT ON ACCOUNT TO ROLE <your_role>;
GRANT USAGE ON WAREHOUSE <your_warehouse> TO ROLE <your_role>;
-- Grant CREATE TABLE and CREATE PROCEDURE on your target schema:
GRANT CREATE TABLE, CREATE PROCEDURE ON SCHEMA <your_db>.<your_schema> TO ROLE <your_role>;
-- To grant your role to yourself (IDENTIFIER requires a session variable, not a function call):
SET my_user = CURRENT_USER();
GRANT ROLE <your_role> TO USER IDENTIFIER($my_user);

-- Switch to your role for all subsequent steps in this section
-- (Objects must be owned by this role for EXECUTE AS OWNER procedures to work):
USE ROLE <your_role>;
USE WAREHOUSE <your_warehouse>;
```

First, create a notification integration if one does not already exist. This example replaces any existing integration named `ai_cost_alerts`.

Copy code

```
CREATE OR REPLACE NOTIFICATION INTEGRATION ai_cost_alerts
    TYPE = EMAIL
    ENABLED = TRUE
    ALLOWED_RECIPIENTS = ('admin@company.com', 'finops@company.com');
```

Important

For SYSTEM$SEND\_EMAIL to deliver, every recipient address must satisfy all three conditions:

1. Listed in the integration’s `ALLOWED_RECIPIENTS`.
2. Used as the `to_email` argument inside the procedure body (the procedures in this guide hardcode `'admin@company.com'`; replace this with your own address everywhere it appears).
3. Set as the `EMAIL` field on a Snowflake user in this account, with the verification email confirmed.

If any of the three is missing or out of sync, the call fails with `Email recipients in the given list at indexes [...] are not allowed`.

Next, create a table to track when alerts were sent for each month. This is used to prevent duplicate alerts within a month.

Copy code

```
CREATE TABLE IF NOT EXISTS AI_FUNCTIONS_ALERT_STATE (
    ALERT_NAME VARCHAR NOT NULL,
    ALERT_MONTH DATE NOT NULL,
    SENT_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    CREDITS_AT_ALERT NUMBER(38,6),
    PRIMARY KEY (ALERT_NAME, ALERT_MONTH)
);
```

Now create a stored procedure to check if an alert was already sent this month, record the alert state, and send the email notification.

Copy code

```
CREATE OR REPLACE PROCEDURE SEND_MONTHLY_SPEND_ALERT(P_THRESHOLD FLOAT)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    v_already_sent INTEGER;
    v_credits NUMBER(38,6);
    v_email_body VARCHAR;
BEGIN
    -- Check if an alert has already been sent this month
    SELECT COUNT(*) INTO :v_already_sent
    FROM AI_FUNCTIONS_ALERT_STATE
    WHERE ALERT_NAME = 'monthly_spend'
      AND ALERT_MONTH = DATE_TRUNC('month', CURRENT_DATE());

    IF (v_already_sent > 0) THEN
        RETURN 'Alert already sent for this month';
    END IF;

    -- Get the current month spend
    SELECT COALESCE(SUM(CREDITS), 0) INTO :v_credits
    FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY
    WHERE START_TIME >= DATE_TRUNC('month', CURRENT_TIMESTAMP());

    -- Compare against the threshold
    IF (v_credits <= :P_THRESHOLD) THEN
        RETURN 'Threshold not exceeded. Current: ' || v_credits::VARCHAR
            || ' / ' || :P_THRESHOLD::VARCHAR;
    END IF;

    -- Record the alert so it does not fire again this month
    INSERT INTO AI_FUNCTIONS_ALERT_STATE (ALERT_NAME, ALERT_MONTH, CREDITS_AT_ALERT)
    VALUES ('monthly_spend', DATE_TRUNC('month', CURRENT_DATE()), :v_credits);

    -- Build the email body and send the alert
    v_email_body :=
        'Monthly AI Function credit consumption has exceeded the threshold.' || CHR(10) || CHR(10) ||
        'Current spend: ' || v_credits::VARCHAR || ' credits' || CHR(10) ||
        'Threshold: ' || :P_THRESHOLD::VARCHAR || ' credits' || CHR(10) || CHR(10) ||
        'Please review usage accordingly.';

    EXECUTE IMMEDIATE
        'CALL SYSTEM$SEND_EMAIL(''ai_cost_alerts'', ''admin@company.com'', ' ||
        '''AI Functions Monthly Spend Alert'', ''' ||
        REPLACE(v_email_body, '''', '''''') || ''')';

    RETURN 'Alert sent. Credits: ' || v_credits::VARCHAR;
END;
$$;
```

Finally, create an alert that checks usage against the spending threshold each hour and calls the procedure to send the notification if needed.
You should adjust the limit of 1000 credits, which appears in two places in the example below, to the desired threshold.

Copy code

```
CREATE OR REPLACE ALERT ai_functions_monthly_spend_alert
    WAREHOUSE = <your_warehouse>
    SCHEDULE = 'USING CRON 0 * * * * UTC'  -- Runs every hour
    IF (EXISTS (
        SELECT 1
        FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY
        WHERE START_TIME >= DATE_TRUNC('month', CURRENT_TIMESTAMP())
        HAVING SUM(CREDITS) > 1000  -- adjust the limit accordingly
    ))
    THEN
        CALL SEND_MONTHLY_SPEND_ALERT(1000);  -- please adjust the limit accordingly

-- enable the alert
ALTER ALERT ai_functions_monthly_spend_alert RESUME;
```

Tip

For testing purposes, set the limit to 0 at first to trigger the alert immediately. Recreate the alert with the desired threshold after confirming that it works as expected.

After testing with a 0 threshold, run the following SQL to allow the alert to trigger again in the current month.

Copy code

```
DELETE FROM AI_FUNCTIONS_ALERT_STATE
WHERE ALERT_NAME = 'monthly_spend'
AND ALERT_MONTH = DATE_TRUNC('month', CURRENT_DATE());
```

You can make sure that the alert is operating by querying the alert history and the alert state table as follows:

Copy code

```
-- Make sure alert exists
SHOW ALERTS LIKE 'ai_functions_monthly_spend_alert';

-- Check alert history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.ALERT_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP()),
    ALERT_NAME => 'ai_functions_monthly_spend_alert'
))
ORDER BY SCHEDULED_TIME DESC;

-- Check which months have had alerts sent
SELECT * FROM AI_FUNCTIONS_ALERT_STATE ORDER BY ALERT_MONTH DESC;
```

### Per-user monthly spending limits

This example implements per-user monthly spending limits. Users are granted a dedicated custom AI\_FUNCTIONS\_USER\_ROLE that
provides access to Cortex AI Functions. A table stores individual users’ monthly token budget. When a user exceeds their
budget for the month, an hourly task revokes their access to AI Functions by removing AI\_FUNCTIONS\_USER\_ROLE. A monthly
task restores the role at the beginning of the next month.

Setting up per-user limits requires the following privileges on the role running these examples:

Copy code

```
-- Run as ACCOUNTADMIN
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE <your_role>;
GRANT EXECUTE TASK ON ACCOUNT TO ROLE <your_role>;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE <your_role>;
GRANT USAGE ON WAREHOUSE <your_warehouse> TO ROLE <your_role>;
-- Grant CREATE TABLE, CREATE PROCEDURE, and CREATE TASK on your target schema:
GRANT CREATE TABLE, CREATE PROCEDURE, CREATE TASK ON SCHEMA <your_db>.<your_schema> TO ROLE <your_role>;
-- Create AI_FUNCTIONS_USER_ROLE and transfer ownership so the procedures can GRANT/REVOKE it:
CREATE ROLE IF NOT EXISTS AI_FUNCTIONS_USER_ROLE;
GRANT OWNERSHIP ON ROLE AI_FUNCTIONS_USER_ROLE TO ROLE <your_role> COPY CURRENT GRANTS;
-- To grant your role to yourself (IDENTIFIER requires a session variable, not a function call):
SET my_user = CURRENT_USER();
GRANT ROLE <your_role> TO USER IDENTIFIER($my_user);

-- Switch to your role for all subsequent steps in this section
-- (Objects must be owned by this role for EXECUTE AS OWNER procedures to work):
USE ROLE <your_role>;
USE WAREHOUSE <your_warehouse>;
```

Important

By default, all users have access to AI Functions (and other Snowflake Cortex features) because the SNOWFLAKE.CORTEX\_USER database role is granted to the PUBLIC role.
To enforce per-user limits, you must revoke SNOWFLAKE.CORTEX\_USER from PUBLIC and grant it only through the AI\_FUNCTIONS\_USER\_ROLE. Use the
following SQL to revoke the role from PUBLIC (run as ACCOUNTADMIN, then switch back to your role):

Copy code

```
USE ROLE ACCOUNTADMIN;
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER FROM ROLE PUBLIC;
USE ROLE <your_role>;
```

Be sure that all users who need access to Cortex features are granted only the AI\_FUNCTIONS\_USER\_ROLE. Use of
any other role that includes SNOWFLAKE.CORTEX\_USER allows users to bypass the spending limit controls implemented in
this example. In some cases, you could use a more specific role; for example, users who need access only to Cortex Analyst
can be granted the SNOWFLAKE.CORTEX\_ANALYST\_USER role instead of SNOWFLAKE.CORTEX\_USER.

To restore the default state at any point, grant the role back to PUBLIC:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE PUBLIC;
```

To audit which roles still grant SNOWFLAKE.CORTEX\_USER:

Copy code

```
SHOW GRANTS OF DATABASE ROLE SNOWFLAKE.CORTEX_USER;
```

To set up per-user spending limits, first create a role that controls access to AI Functions, allowing this access to be managed separately from other privileges.

Copy code

```
-- Create a role specifically for AI Function access
CREATE ROLE IF NOT EXISTS AI_FUNCTIONS_USER_ROLE;

-- Grant necessary privileges to the role
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE AI_FUNCTIONS_USER_ROLE;

-- Grant usage on warehouse
GRANT USAGE ON WAREHOUSE AI_FUNCTIONS_WAREHOUSE TO ROLE AI_FUNCTIONS_USER_ROLE;
```

Now, set up the access control table, which tracks which users have AI Function access, their individual spending
limits, and their revocation history. It serves as the source of truth for the automated monitoring and access
restoration processes.

Copy code

```
CREATE TABLE IF NOT EXISTS AI_FUNCTIONS_ACCESS_CONTROL (
    USER_NAME VARCHAR NOT NULL,
    USER_ID NUMBER,
    GRANTED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    MONTHLY_CREDIT_LIMIT NUMBER(38,6) DEFAULT 100,  -- adjust the limit accordingly
    IS_ACTIVE BOOLEAN DEFAULT TRUE,
    REVOKED_AT TIMESTAMP_LTZ,
    REVOCATION_REASON VARCHAR,
    PRIMARY KEY (USER_NAME)
);
```

Next, create a stored procedure to grant AI Function access to a user and register them in the access control table with their spending limit. The code looks up the user’s ID from the Account Usage view to enable efficient joins in monitoring queries.

This procedure (and the two below) use `EXECUTE AS OWNER` so that the role that owns the procedure (and AI\_FUNCTIONS\_USER\_ROLE) handles the GRANT/REVOKE. Callers do not need ownership of the user role.

Copy code

```
CREATE OR REPLACE PROCEDURE GRANT_AI_FUNCTIONS_ACCESS(
    P_USER_NAME VARCHAR,
    P_MONTHLY_LIMIT NUMBER(38,6) DEFAULT 100  -- adjust the limit accordingly
)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
    v_user_id NUMBER;
BEGIN
    -- Look up USER_ID from account usage
    SELECT USER_ID INTO :v_user_id
    FROM SNOWFLAKE.ACCOUNT_USAGE.USERS
    WHERE NAME = :P_USER_NAME
    LIMIT 1;

    -- Grant the AI Functions role to the user
    EXECUTE IMMEDIATE 'GRANT ROLE AI_FUNCTIONS_USER_ROLE TO USER ' || P_USER_NAME;

    -- Register or update the user in the access control table
    MERGE INTO AI_FUNCTIONS_ACCESS_CONTROL tgt
    USING (SELECT :P_USER_NAME AS USER_NAME) src
    ON tgt.USER_NAME = src.USER_NAME
    WHEN MATCHED THEN
        UPDATE SET
            USER_ID = :v_user_id,
            IS_ACTIVE = TRUE,
            MONTHLY_CREDIT_LIMIT = :P_MONTHLY_LIMIT,
            GRANTED_AT = CURRENT_TIMESTAMP(),
            REVOKED_AT = NULL,
            REVOCATION_REASON = NULL
    WHEN NOT MATCHED THEN
        INSERT (USER_NAME, USER_ID, MONTHLY_CREDIT_LIMIT, IS_ACTIVE)
        VALUES (:P_USER_NAME, :v_user_id, :P_MONTHLY_LIMIT, TRUE);

    RETURN 'Access granted to ' || P_USER_NAME || ' with monthly limit of ' || P_MONTHLY_LIMIT || ' credits';
END;
$$;
```

Use this stored procedure to add users and their credit quotas to the access control table.

Copy code

```
CALL GRANT_AI_FUNCTIONS_ACCESS('ALICE', 1000);  -- grants access to user ALICE with a monthly limit of 1000 credits
CALL GRANT_AI_FUNCTIONS_ACCESS('BOB', 2000);    -- grants access to user BOB with a monthly limit of 2000 credits
```

Next, create a procedure to revoke access from users who exceed their monthly limit, and an hourly task to run the revocation check.

Copy code

```
-- Create the revocation procedure
CREATE OR REPLACE PROCEDURE REVOKE_EXCESSIVE_SPENDERS()
RETURNS TABLE (USER_NAME VARCHAR, CREDITS_USED NUMBER, CREDIT_LIMIT NUMBER, ACTION VARCHAR)
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
    result RESULTSET;
BEGIN
    -- Find users who exceeded their monthly limit and revoke access
    result := (
        WITH user_spending AS (
            SELECT
                u.NAME AS USER_NAME,
                ac.MONTHLY_CREDIT_LIMIT,
                COALESCE(SUM(h.CREDITS), 0) AS CREDITS_USED
            FROM AI_FUNCTIONS_ACCESS_CONTROL ac
            JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u
                ON ac.USER_NAME = u.NAME
            LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY h
                ON u.USER_ID = h.USER_ID
                AND h.START_TIME >= DATE_TRUNC('month', CURRENT_TIMESTAMP())
            WHERE ac.IS_ACTIVE = TRUE
            GROUP BY u.NAME, ac.MONTHLY_CREDIT_LIMIT
        )
        SELECT
            USER_NAME,
            CREDITS_USED,
            MONTHLY_CREDIT_LIMIT AS CREDIT_LIMIT,
            'REVOKED' AS ACTION
        FROM user_spending
        WHERE CREDITS_USED > MONTHLY_CREDIT_LIMIT
    );

    -- Revoke access for each excessive spender
    FOR rec IN result DO
        LET v_user_name VARCHAR := rec.USER_NAME;
        LET v_credits_used NUMBER := rec.CREDITS_USED;
        LET v_credit_limit NUMBER := rec.CREDIT_LIMIT;

        EXECUTE IMMEDIATE 'REVOKE ROLE AI_FUNCTIONS_USER_ROLE FROM USER ' || v_user_name;

        UPDATE AI_FUNCTIONS_ACCESS_CONTROL
        SET IS_ACTIVE = FALSE,
            REVOKED_AT = CURRENT_TIMESTAMP(),
            REVOCATION_REASON = 'Exceeded monthly limit: ' || :v_credits_used || ' / ' || :v_credit_limit
        WHERE USER_NAME = :v_user_name;
    END FOR;

    RETURN TABLE(result);
END;
$$;

-- Create a task to run the revocation check every hour
CREATE OR REPLACE TASK MONITOR_AI_FUNCTIONS_SPENDING
    WAREHOUSE = <your_warehouse>
    SCHEDULE = 'USING CRON 0 * * * * UTC'  -- Every hour
AS
    CALL REVOKE_EXCESSIVE_SPENDERS();

-- Enable the task
ALTER TASK MONITOR_AI_FUNCTIONS_SPENDING RESUME;

-- Verify task status
SHOW TASKS LIKE 'MONITOR_AI_FUNCTIONS_SPENDING';
```

Finally, create the monthly access refresh task. This task runs on the first day of each month to restore AI Function access for all entitled users. When a user’s access was revoked due to exceeding their limit in the previous month, this task grants them a fresh budget for the new month.

Copy code

```
-- Create a procedure to re-grant access to all entitled users
CREATE OR REPLACE PROCEDURE GRANT_ALL_ENTITLED_USERS()
RETURNS TABLE (USER_NAME VARCHAR, CREDIT_LIMIT NUMBER, ACTION VARCHAR)
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
DECLARE
    result RESULTSET;
BEGIN
    result := (
        SELECT
            USER_NAME,
            MONTHLY_CREDIT_LIMIT AS CREDIT_LIMIT,
            'GRANTED' AS ACTION
        FROM AI_FUNCTIONS_ACCESS_CONTROL
    );

    -- Re-grant access for each entitled user
    FOR rec IN result DO
        LET v_user_name VARCHAR := rec.USER_NAME;
        LET v_credit_limit NUMBER := rec.CREDIT_LIMIT;
        CALL GRANT_AI_FUNCTIONS_ACCESS(:v_user_name, :v_credit_limit);
    END FOR;

    RETURN TABLE(result);
END;
$$;

-- Create a task to run on the 1st of each month at midnight UTC
CREATE OR REPLACE TASK MONTHLY_AI_FUNCTIONS_ACCESS_REFRESH
    WAREHOUSE = <your_warehouse>
    SCHEDULE = 'USING CRON 0 0 1 * * UTC'  -- 1st day of each month at 00:00 UTC
AS
    CALL GRANT_ALL_ENTITLED_USERS();

-- Enable the task
ALTER TASK MONTHLY_AI_FUNCTIONS_ACCESS_REFRESH RESUME;

-- Run once initially to populate grantees
CALL GRANT_ALL_ENTITLED_USERS();

-- Verify task status
SHOW TASKS LIKE 'MONTHLY_AI_FUNCTIONS_ACCESS_REFRESH';
```

### Runaway query detection and cancellation

Long-running AI Function queries can accumulate significant costs. This example implements an automated system to detect queries that exceed a credit threshold and cancel them before they consume even more resources. An email alert is sent with full query details.

Setting up runaway query detection requires the following privileges on the role running these examples:

Copy code

```
-- Run as ACCOUNTADMIN
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE <your_role>;
GRANT EXECUTE TASK ON ACCOUNT TO ROLE <your_role>;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE <your_role>;
GRANT OPERATE ON WAREHOUSE <your_warehouse> TO ROLE <your_role>;
GRANT USAGE ON WAREHOUSE <your_warehouse> TO ROLE <your_role>;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE <your_role>;
-- Grant CREATE PROCEDURE and CREATE TASK on your target schema:
GRANT CREATE PROCEDURE, CREATE TASK ON SCHEMA <your_db>.<your_schema> TO ROLE <your_role>;
-- To grant your role to yourself (IDENTIFIER requires a session variable, not a function call):
SET my_user = CURRENT_USER();
GRANT ROLE <your_role> TO USER IDENTIFIER($my_user);

-- Switch to your role for all subsequent steps in this section
-- (Objects must be owned by this role for EXECUTE AS OWNER procedures to work):
USE ROLE <your_role>;
USE WAREHOUSE <your_warehouse>;
```

Note

When a query is cancelled, the client is still charged for all resources consumed up to the moment of cancellation. Cancelling a runaway query prevents further cost accumulation but does not refund credits already spent.

Tip

The CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY view splits usage into one-hour windows, so a long-running query
produces multiple rows. IS\_COMPLETED is TRUE only on the final row of a completed query. To find
still-running queries, aggregate by QUERY\_ID and check that all rows have IS\_COMPLETED = FALSE.

The procedure also reads `ROLE_NAMES`, `QUERY_TAG`, and `WAREHOUSE_ID` from the view to populate the alert email so the responder knows which user, project, and warehouse owned the query. See the [view reference](/sql-reference/account-usage/cortex_ai_functions_usage_history) for full column descriptions.

Note

If the role running this procedure lacks OPERATE on a target warehouse, the cancellation fails. The email alert subject and body indicate `CANCEL FAILED` and include the underlying error so administrators can act. Grant OPERATE on every warehouse that runs AI Function queries to ensure cancellations succeed.

For each query in the last 48 hours, this procedure sums the credits used across all hourly windows. If the total exceeds the threshold and the query is still running, the procedure cancels it and reports it to an administrator.

Copy code

```
-- Create a procedure to detect and cancel expensive runaway queries
CREATE OR REPLACE PROCEDURE MONITOR_AND_CANCEL_RUNAWAY_QUERIES(
    P_CREDIT_THRESHOLD NUMBER DEFAULT 50  -- adjust the limit accordingly
)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
DECLARE
    result RESULTSET;
    cancelled_count INTEGER DEFAULT 0;
    failed_cancel_count INTEGER DEFAULT 0;
    cancelled_ids VARCHAR DEFAULT '';
    failed_ids VARCHAR DEFAULT '';
    v_query_id VARCHAR;
    v_user_name VARCHAR;
    v_functions VARCHAR;
    v_models VARCHAR;
    v_credits VARCHAR;
    v_start_time VARCHAR;
    v_roles VARCHAR;
    v_query_tag VARCHAR;
    v_warehouse_id VARCHAR;
    v_email_body VARCHAR;
    v_email_subject VARCHAR;
    v_cancel_status VARCHAR;
    v_cancel_error VARCHAR;
BEGIN
    -- Aggregate credits across hourly windows per query. A single query can invoke
    -- multiple AI functions or models, each producing separate rows, so we sum all of them.
    result := (
        WITH query_credits AS (
            SELECT
                h.QUERY_ID,
                ANY_VALUE(h.USER_ID) AS USER_ID,
                ARRAY_AGG(DISTINCT h.FUNCTION_NAME) AS FUNCTION_NAMES,
                ARRAY_AGG(DISTINCT h.MODEL_NAME) AS MODEL_NAMES,
                SUM(h.CREDITS) AS TOTAL_CREDITS,
                MIN(h.START_TIME) AS FIRST_SEEN,
                ANY_VALUE(h.ROLE_NAMES) AS ROLE_NAMES,
                ANY_VALUE(h.QUERY_TAG) AS QUERY_TAG,
                ANY_VALUE(h.WAREHOUSE_ID) AS WAREHOUSE_ID
            FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY h
            WHERE h.START_TIME >= DATEADD('hour', -48, CURRENT_TIMESTAMP())
            GROUP BY h.QUERY_ID
            HAVING SUM(h.CREDITS) > :P_CREDIT_THRESHOLD
                AND BOOLOR_AGG(h.IS_COMPLETED) = FALSE
        )
        SELECT
            qc.QUERY_ID,
            COALESCE(u.NAME, 'Unknown') AS USER_NAME,
            ARRAY_TO_STRING(qc.FUNCTION_NAMES, ', ') AS FUNCTION_NAMES,
            ARRAY_TO_STRING(qc.MODEL_NAMES, ', ') AS MODEL_NAMES,
            qc.TOTAL_CREDITS::VARCHAR AS CREDITS,
            qc.FIRST_SEEN::VARCHAR AS START_TIME,
            COALESCE(qc.ROLE_NAMES::VARCHAR, 'N/A') AS ROLE_NAMES,
            COALESCE(qc.QUERY_TAG, 'N/A') AS QUERY_TAG,
            COALESCE(qc.WAREHOUSE_ID::VARCHAR, 'N/A') AS WAREHOUSE_ID
        FROM query_credits qc
        LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.USERS u
            ON qc.USER_ID = u.USER_ID
    );

    -- Cancel each runaway query and send an alert
    FOR rec IN result DO
        v_query_id     := rec.QUERY_ID;
        v_user_name    := rec.USER_NAME;
        v_functions    := rec.FUNCTION_NAMES;
        v_models       := rec.MODEL_NAMES;
        v_credits      := rec.CREDITS;
        v_start_time   := rec.START_TIME;
        v_roles        := rec.ROLE_NAMES;
        v_query_tag    := rec.QUERY_TAG;
        v_warehouse_id := rec.WAREHOUSE_ID;

        -- Attempt to cancel the query; record the outcome so it can be reported in the email
        v_cancel_status := 'CANCELLED';
        v_cancel_error  := '';
        BEGIN
            EXECUTE IMMEDIATE 'SELECT SYSTEM$CANCEL_QUERY(''' || v_query_id || ''')';
        EXCEPTION
            WHEN OTHER THEN
                v_cancel_status := 'CANCEL FAILED';
                v_cancel_error  := SQLERRM;
        END;

        -- Build the email body and send the alert
        v_email_body :=
            CASE
                WHEN v_cancel_status = 'CANCELLED'
                    THEN 'A runaway AI Function query has been cancelled due to excessive cost.'
                ELSE 'A runaway AI Function query was detected, but cancellation FAILED. The query may still be running and consuming credits. Investigate immediately.'
            END || CHR(10) || CHR(10) ||
            'Query Details:' || CHR(10) ||
            '- Cancellation status: ' || v_cancel_status || CHR(10) ||
            CASE
                WHEN v_cancel_error <> '' THEN '- Cancellation error: ' || v_cancel_error || CHR(10)
                ELSE ''
            END ||
            '- Query ID: ' || v_query_id || CHR(10) ||
            '- User: ' || v_user_name || CHR(10) ||
            '- Function(s): ' || v_functions || CHR(10) ||
            '- Model(s): ' || v_models || CHR(10) ||
            '- Credits Used: ' || v_credits || CHR(10) ||
            '- Threshold: ' || :P_CREDIT_THRESHOLD::VARCHAR || CHR(10) ||
            '- Start Time: ' || v_start_time || CHR(10) ||
            '- Roles: ' || v_roles || CHR(10) ||
            '- Query Tag: ' || v_query_tag || CHR(10) ||
            '- Warehouse ID: ' || v_warehouse_id || CHR(10) || CHR(10) ||
            'Please investigate this query and take appropriate action.';

        v_email_subject :=
            CASE
                WHEN v_cancel_status = 'CANCELLED' THEN 'Runaway AI Query Cancelled - '
                ELSE 'Runaway AI Query Detected, CANCEL FAILED - '
            END || v_query_id;

        EXECUTE IMMEDIATE
            'CALL SYSTEM$SEND_EMAIL(''ai_cost_alerts'', ''admin@company.com'', ''' ||
            REPLACE(v_email_subject, '''', '''''') || ''', ''' ||
            REPLACE(v_email_body, '''', '''''') || ''')';

        IF (v_cancel_status = 'CANCELLED') THEN
            cancelled_count := cancelled_count + 1;
            IF (cancelled_ids = '') THEN
                cancelled_ids := v_query_id;
            ELSE
                cancelled_ids := cancelled_ids || ', ' || v_query_id;
            END IF;
        ELSE
            failed_cancel_count := failed_cancel_count + 1;
            IF (failed_ids = '') THEN
                failed_ids := v_query_id;
            ELSE
                failed_ids := failed_ids || ', ' || v_query_id;
            END IF;
        END IF;
    END FOR;

    IF (cancelled_count = 0 AND failed_cancel_count = 0) THEN
        RETURN 'No runaway queries found exceeding ' || :P_CREDIT_THRESHOLD::VARCHAR || ' credits.';
    END IF;

    LET msg VARCHAR := 'Processed ' || (cancelled_count + failed_cancel_count)::VARCHAR || ' runaway queries.';
    IF (cancelled_count > 0) THEN
        msg := msg || ' Cancelled: ' || cancelled_ids || '.';
    END IF;
    IF (failed_cancel_count > 0) THEN
        msg := msg || ' Cancel failed (still running): ' || failed_ids || '.';
    END IF;
    RETURN msg;
END;
$$;

-- Create a task to monitor and cancel runaway queries every hour
CREATE OR REPLACE TASK MONITOR_RUNAWAY_AI_QUERIES
    WAREHOUSE = <your_warehouse>
    SCHEDULE = 'USING CRON 0 * * * * UTC'  -- Every hour
AS
    CALL MONITOR_AND_CANCEL_RUNAWAY_QUERIES(50);  -- adjust the limit accordingly

-- Enable the task
ALTER TASK MONITOR_RUNAWAY_AI_QUERIES RESUME;

-- Verify task status
SHOW TASKS LIKE 'MONITOR_RUNAWAY_AI_QUERIES';

-- Check task execution history
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START => DATEADD('day', -1, CURRENT_TIMESTAMP()),
    TASK_NAME => 'MONITOR_RUNAWAY_AI_QUERIES'
))
ORDER BY SCHEDULED_TIME DESC;
```

Tip

If you already know that some of your queries will run a long time, define a special role for these queries, and then exclude that role
from the cancellation logic. For example, to create the role:

Copy code

```
CREATE ROLE AI_FUNCTIONS_USER_LONG_RUNNING_ROLE;
GRANT ROLE AI_FUNCTIONS_USER_ROLE TO ROLE AI_FUNCTIONS_USER_LONG_RUNNING_ROLE;
GRANT ROLE AI_FUNCTIONS_USER_LONG_RUNNING_ROLE TO USER LONG_RUNNING_USER;
```

Add the following condition to the HAVING clause of the CTE in the procedure to exclude queries run by users with this role from being cancelled.

Copy code

```
AND NOT ARRAY_CONTAINS('AI_FUNCTIONS_USER_LONG_RUNNING_ROLE'::VARIANT, ANY_VALUE(h.ROLE_NAMES))
```

Now the user can assume the role to run a long-running query without it being cancelled:

Copy code

```
USE ROLE AI_FUNCTIONS_USER_LONG_RUNNING_ROLE;
-- then start the long-running query
```

## Cleanup

After testing, run the following to remove anything created by the examples in this topic. Run only the parts that match what you set up.

Copy code

```
-- Account-level monthly spending alert
ALTER ALERT IF EXISTS ai_functions_monthly_spend_alert SUSPEND;
DROP ALERT IF EXISTS ai_functions_monthly_spend_alert;
DROP PROCEDURE IF EXISTS SEND_MONTHLY_SPEND_ALERT(FLOAT);
DROP TABLE IF EXISTS AI_FUNCTIONS_ALERT_STATE;

-- Per-user monthly spending limits
ALTER TASK IF EXISTS MONTHLY_AI_FUNCTIONS_ACCESS_REFRESH SUSPEND;
ALTER TASK IF EXISTS MONITOR_AI_FUNCTIONS_SPENDING SUSPEND;
DROP TASK IF EXISTS MONTHLY_AI_FUNCTIONS_ACCESS_REFRESH;
DROP TASK IF EXISTS MONITOR_AI_FUNCTIONS_SPENDING;
DROP PROCEDURE IF EXISTS GRANT_ALL_ENTITLED_USERS();
DROP PROCEDURE IF EXISTS REVOKE_EXCESSIVE_SPENDERS();
DROP PROCEDURE IF EXISTS GRANT_AI_FUNCTIONS_ACCESS(VARCHAR, NUMBER(38,6));
DROP TABLE IF EXISTS AI_FUNCTIONS_ACCESS_CONTROL;
DROP ROLE IF EXISTS AI_FUNCTIONS_USER_ROLE;

-- Runaway query detection
ALTER TASK IF EXISTS MONITOR_RUNAWAY_AI_QUERIES SUSPEND;
DROP TASK IF EXISTS MONITOR_RUNAWAY_AI_QUERIES;
DROP PROCEDURE IF EXISTS MONITOR_AND_CANCEL_RUNAWAY_QUERIES(NUMBER);

-- Shared notification integration (only if no other process uses it)
DROP NOTIFICATION INTEGRATION IF EXISTS ai_cost_alerts;

-- If you revoked SNOWFLAKE.CORTEX_USER from PUBLIC, restore it
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE PUBLIC;
```

## Best practices

Keep the following best practices in mind when developing a cost management strategy for AI Function usage:

- **Start with monitoring:** Before implementing automated controls, establish baseline usage patterns using the queries in
  [Basic usage monitoring](#label-ai-functions-basic-usage-queries).
- **Set conservative initial limits:** Begin with lower thresholds and adjust upward based on actual usage patterns.
- **Use query tags:** Encourage teams to use QUERY\_TAG session parameters to enable cost attribution by project or team.
- **Review regularly:** Periodically review the access control table and adjust per-user limits based on legitimate needs.
- **Test alerts:** Verify that email notifications work correctly before relying on them for critical alerts.
- **Consider latency:** The ACCOUNT\_USAGE view has up to 5 minutes of latency; factor this into your monitoring strategy.
