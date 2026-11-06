# Semantic view description quality: a rubric, a linter, and how to apply fixes: code

Every file in the [Semantic view description quality: a rubric, a linter, and how to apply fixes](/developer-guide/cortex-ai-cookbook/description-quality) recipe. To run the recipe, download [description-quality.zip](/static/samples/cortex-ai-cookbook/description-quality.zip), unzip it, and run the scripts from the `description-quality/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/description-quality); the zip includes it as `README.md`.

## `sql/`

### `sql/01_example_setup.sql`

Copy code

```
-- =============================================================================
-- Semantic view description quality: example setup
-- A small orders table and a semantic view whose descriptions show the common
-- failure modes: missing, circular, padded, vague, and contradicting the SQL.
-- =============================================================================

SET DB        = 'COOKBOOK_DESCRIPTION_QUALITY';
SET WH        = 'COOKBOOK_DESCRIPTION_QUALITY_WH';
SET ROLE_NAME = 'COOKBOOK_DESCRIPTION_QUALITY_ROLE';
SET CUR_USER  = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;
CREATE ROLE IF NOT EXISTS IDENTIFIER($ROLE_NAME) COMMENT = 'Cortex AI Cookbook: description-quality';
GRANT ROLE IDENTIFIER($ROLE_NAME) TO USER IDENTIFIER($CUR_USER);
GRANT ROLE IDENTIFIER($ROLE_NAME) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($ROLE_NAME);
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($WH)
  WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cortex AI Cookbook: description-quality';
GRANT USAGE, OPERATE ON WAREHOUSE IDENTIFIER($WH) TO ROLE IDENTIFIER($ROLE_NAME);
CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB) COMMENT = 'Cortex AI Cookbook: description-quality';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($DB) TO ROLE IDENTIFIER($ROLE_NAME) COPY CURRENT GRANTS;

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
CREATE SCHEMA IF NOT EXISTS SALES;
USE SCHEMA SALES;

-- Fictional Contoso Outdoor orders. ORD_CHNL is a legacy code: W = web, S = store, P = phone.
CREATE OR REPLACE TABLE ORDERS (
    ORDER_ID        NUMBER,
    CUSTOMER_NAME   VARCHAR,
    ORDER_DATE      DATE,
    STATUS          VARCHAR,
    ORD_CHNL        VARCHAR,
    GROSS_AMOUNT    NUMBER(10,2),
    DISCOUNT_AMOUNT NUMBER(10,2),
    NET_AMOUNT      NUMBER(10,2)
);
INSERT INTO ORDERS
SELECT SEQ4() + 1,
       ARRAY_CONSTRUCT('Avery Lin', 'Jordan Blake', 'Sam Ortiz', 'Riley Chen')[MOD(SEQ4(), 4)]::VARCHAR,
       DATEADD(day, MOD(SEQ4() * 7, 90), '2026-01-01'::DATE),
       ARRAY_CONSTRUCT('SHIPPED', 'SHIPPED', 'RETURNED', 'CANCELLED')[MOD(SEQ4(), 4)]::VARCHAR,
       ARRAY_CONSTRUCT('W', 'S', 'P')[MOD(SEQ4(), 3)]::VARCHAR,
       100 + MOD(SEQ4() * 37, 400), MOD(SEQ4() * 11, 40), 0
FROM TABLE(GENERATOR(ROWCOUNT => 40));
UPDATE ORDERS SET NET_AMOUNT = GROSS_AMOUNT - DISCOUNT_AMOUNT;

-- The "before" semantic view. Each weak description is typical of first drafts.
CREATE OR ALTER SEMANTIC VIEW ORDERS_SV
  TABLES (
    orders AS ORDERS PRIMARY KEY (ORDER_ID) COMMENT = 'Orders table'
  )
  FACTS (
    orders.discount_amount AS DISCOUNT_AMOUNT COMMENT = 'Discount',
    orders.net_amount AS NET_AMOUNT
  )
  DIMENSIONS (
    orders.customer_name AS CUSTOMER_NAME COMMENT = 'Name of the customer',
    orders.order_date AS ORDER_DATE
      COMMENT = 'This field represents the date on which the order was placed by the customer in the system and recorded in the database',
    orders.status AS STATUS,
    orders.ord_chnl AS ORD_CHNL COMMENT = 'Channel'
  )
  METRICS (
    orders.total_revenue AS SUM(net_amount)
      WITH SYNONYMS = ('revenue', 'sales', 'income', 'turnover', 'money', 'amount')
      COMMENT = 'The total revenue',
    orders.avg_order_value AS AVG(net_amount) COMMENT = 'Total value of all orders',
    orders.order_count AS COUNT(order_id) COMMENT = 'Orders'
  )
  COMMENT = 'Orders';
```

### `sql/02_lint_descriptions.sql`

Copy code

```
-- =============================================================================
-- Semantic view description quality: lint
-- Part 1 is deterministic: heuristic checks over the INFORMATION_SCHEMA views
-- for semantic views (no model call). Part 2 grades each description with
-- AI_COMPLETE against the four-criteria rubric and proposes a rewrite.
-- Point both at your own view: set DB, SCHEMA_NAME, and SV_NAME to the view, and
-- ROLE_NAME and WH to a role with any privilege on it and a warehouse that role
-- can use. The script reads INFORMATION_SCHEMA only and creates nothing, so the
-- role needs no CREATE privilege in your schema.
-- =============================================================================

SET DB          = 'COOKBOOK_DESCRIPTION_QUALITY';
SET SCHEMA_NAME = 'SALES';
SET SV_NAME     = 'ORDERS_SV';
SET WH          = 'COOKBOOK_DESCRIPTION_QUALITY_WH';
SET ROLE_NAME   = 'COOKBOOK_DESCRIPTION_QUALITY_ROLE';
SET MODEL       = 'claude-sonnet-4-6';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);

-- Both parts start from the same list: every dimension, fact, and metric of the
-- view with its expression, description, and synonyms (the sv CTE below).

-- -----------------------------------------------------------------------------
-- Part 1: heuristic checks. Each flag is a prompt to look, not a verdict.
-- -----------------------------------------------------------------------------
WITH sv AS (
  SELECT 'DIMENSION' AS KIND, SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_DIMENSIONS
  UNION ALL
  SELECT 'FACT', SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_FACTS
  UNION ALL
  SELECT 'METRIC', SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_METRICS
),
e AS (
  SELECT *,
         -- Words in the description that are not in the element name and are not filler.
         ARRAY_EXCEPT(
           SPLIT(REGEXP_REPLACE(LOWER(COALESCE(COMMENT, '')), '[^a-z0-9 ]', ''), ' '),
           ARRAY_CAT(SPLIT(LOWER(NAME), '_'),
                     ['', 'the', 'a', 'an', 'of', 'for', 'in', 'on', 'and', 'or', 'this', 'is', 'field', 'column', 'value'])
         ) AS NEW_WORDS
  FROM sv
  WHERE SEMANTIC_VIEW_SCHEMA = $SCHEMA_NAME AND SEMANTIC_VIEW_NAME = $SV_NAME
)
SELECT KIND, NAME, EXPRESSION, COMMENT,
       ARRAY_COMPACT(ARRAY_CONSTRUCT(
         IFF(NULLIF(TRIM(COMMENT), '') IS NULL, 'MISSING: no description', NULL),
         IFF(NULLIF(TRIM(COMMENT), '') IS NOT NULL AND ARRAY_SIZE(NEW_WORDS) = 0,
             'CIRCULAR: adds nothing beyond the name', NULL),
         IFF(COMMENT ILIKE 'this field%' OR COMMENT ILIKE 'this column%' OR COMMENT ILIKE 'this is the%'
             OR COMMENT ILIKE '%in the database%' OR COMMENT ILIKE '%in the system%',
             'PADDED: boilerplate phrasing', NULL),
         IFF(KIND = 'METRIC' AND EXPRESSION ILIKE 'AVG(%' AND COMMENT ILIKE ANY ('%total%', '%sum%')
             AND NOT COMMENT ILIKE ANY ('%average%', '%mean%'),
             'CONTRADICTS SQL: says total, expression is AVG', NULL),
         IFF(KIND = 'METRIC' AND EXPRESSION ILIKE 'SUM(%' AND COMMENT ILIKE ANY ('%average%', '%mean%'),
             'CONTRADICTS SQL: says average, expression is SUM', NULL),
         IFF(KIND IN ('METRIC', 'FACT') AND NULLIF(TRIM(COMMENT), '') IS NOT NULL
             AND NOT REGEXP_LIKE(COMMENT, '.*(USD|dollar|percent|%|count|number|days|units|currency).*', 'i'),
             'UNIT: no unit or type of quantity stated', NULL),
         IFF(ARRAY_SIZE(SYNONYMS) > 0, 'SYNONYMS: ' || ARRAY_SIZE(SYNONYMS)::VARCHAR
             || ' synonyms; keep only proprietary or legacy terms', NULL)
       )) AS FLAGS
FROM e
ORDER BY ARRAY_SIZE(FLAGS) DESC, KIND, NAME;

-- -----------------------------------------------------------------------------
-- Part 2: model-graded rubric. One AI_COMPLETE call per element; the grade and
-- the rewrite are suggestions for a person to review, not changes.
-- -----------------------------------------------------------------------------
WITH sv AS (
  SELECT 'DIMENSION' AS KIND, SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_DIMENSIONS
  UNION ALL
  SELECT 'FACT', SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_FACTS
  UNION ALL
  SELECT 'METRIC', SEMANTIC_VIEW_SCHEMA, SEMANTIC_VIEW_NAME, TABLE_NAME, NAME, EXPRESSION, COMMENT, SYNONYMS
  FROM INFORMATION_SCHEMA.SEMANTIC_METRICS
)
SELECT KIND, NAME, EXPRESSION, COMMENT,
       g:preciseness::VARCHAR     AS PRECISE,
       g:conciseness::VARCHAR     AS CONCISE,
       g:non_circularity::VARCHAR AS NON_CIRCULAR,
       g:correctness::VARCHAR     AS CORRECT,
       g:issue::VARCHAR           AS ISSUE,
       g:suggested_description::VARCHAR AS SUGGESTED_DESCRIPTION
FROM (
  SELECT e.*,
         AI_COMPLETE(
           model => $MODEL,
           prompt => CONCAT(
             'Grade this semantic view ', LOWER(KIND), ' description from A (best) to F (worst) on four criteria. ',
             'Preciseness: could it be told apart from similar elements (scope, filters, units, grain)? ',
             'Conciseness: does every word add meaning? ',
             'Non-circularity: does it say more than the element name? ',
             'Correctness: does it match the SQL expression, including the aggregation? ',
             'A missing description is F on every criterion. Then write a better description of at most two ',
             'sentences, using only facts you can see in the name and expression; write UNKNOWN for business ',
             'meaning you cannot infer. Respond in JSON.',
             '\nName: ', NAME, '\nKind: ', KIND, '\nExpression: ', EXPRESSION,
             '\nDescription: ', COALESCE(COMMENT, '(missing)')),
           model_parameters => {'temperature': 0},
           response_format => {'type': 'json', 'schema': {'type': 'object', 'properties': {
             'preciseness':     {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'F']},
             'conciseness':     {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'F']},
             'non_circularity': {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'F']},
             'correctness':     {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'F']},
             'issue':           {'type': 'string'},
             'suggested_description': {'type': 'string'}},
             'required': ['preciseness', 'conciseness', 'non_circularity', 'correctness', 'issue', 'suggested_description']}}
         ) AS g
  FROM sv e
  WHERE SEMANTIC_VIEW_SCHEMA = $SCHEMA_NAME AND SEMANTIC_VIEW_NAME = $SV_NAME
)
ORDER BY KIND, NAME;
```

### `sql/03_apply_descriptions.sql`

Copy code

```
-- =============================================================================
-- Semantic view description quality: apply better descriptions
-- Route A (DDL): CREATE OR ALTER SEMANTIC VIEW with the new descriptions.
-- Route B (YAML): SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML with create_or_alter = TRUE.
-- ALTER SEMANTIC VIEW can change only the view-level comment, so element
-- descriptions are changed by redefining the view with one of these routes.
-- The model's suggestions from 02 were a starting point; a person filled in the
-- business meaning the model marked UNKNOWN (status values, channel codes, units).
-- =============================================================================

SET DB        = 'COOKBOOK_DESCRIPTION_QUALITY';
SET WH        = 'COOKBOOK_DESCRIPTION_QUALITY_WH';
SET ROLE_NAME = 'COOKBOOK_DESCRIPTION_QUALITY_ROLE';
SET SCHEMA_FQ = 'COOKBOOK_DESCRIPTION_QUALITY.SALES';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA SALES;

-- -----------------------------------------------------------------------------
-- Route A: DDL
-- Anything omitted is removed: the six synonyms on total_revenue are gone after
-- this runs. The legacy ORD_CHNL is exposed as order_channel, with the old code
-- kept as the one synonym worth having.
-- -----------------------------------------------------------------------------
CREATE OR ALTER SEMANTIC VIEW ORDERS_SV
  TABLES (
    orders AS ORDERS PRIMARY KEY (ORDER_ID)
      COMMENT = 'One row per customer order placed with Contoso Outdoor, January to March 2026, all statuses.'
  )
  FACTS (
    orders.discount_amount AS DISCOUNT_AMOUNT
      COMMENT = 'Discount applied to the order, in USD. NET_AMOUNT = GROSS_AMOUNT - DISCOUNT_AMOUNT.',
    orders.net_amount AS NET_AMOUNT
      COMMENT = 'Order amount after discount, in USD. Excludes tax and shipping.'
  )
  DIMENSIONS (
    orders.customer_name AS CUSTOMER_NAME
      COMMENT = 'Full name of the person who placed the order, as entered at checkout.',
    orders.order_date AS ORDER_DATE
      COMMENT = 'Date the order was placed.',
    orders.status AS STATUS
      COMMENT = 'Fulfillment status. SHIPPED orders count as sales; RETURNED and CANCELLED orders do not.'
      SAMPLE_VALUES ('SHIPPED', 'RETURNED', 'CANCELLED')
      IS_ENUM,
    orders.order_channel AS CASE ORD_CHNL WHEN 'W' THEN 'Web' WHEN 'S' THEN 'Store' WHEN 'P' THEN 'Phone' END
      WITH SYNONYMS = ('ord_chnl')
      COMMENT = 'Channel the order came through, decoded from the legacy ORD_CHNL code (W, S, P).'
      SAMPLE_VALUES ('Web', 'Store', 'Phone')
      IS_ENUM
  )
  METRICS (
    orders.total_revenue AS SUM(net_amount)
      COMMENT = 'Sum of NET_AMOUNT in USD across all order statuses. Filter STATUS = SHIPPED for recognized sales.',
    orders.avg_order_value AS AVG(net_amount)
      COMMENT = 'Average NET_AMOUNT per order, in USD, across all order statuses.',
    orders.order_count AS COUNT(order_id)
      COMMENT = 'Number of orders, across all statuses.'
  )
  COMMENT = 'Contoso Outdoor orders with net revenue, discounts, status, and channel.';

-- Re-run Part 1 of 02_lint_descriptions.sql: the only remaining flag is the
-- ord_chnl synonym, which is kept on purpose because it is a legacy code.

-- -----------------------------------------------------------------------------
-- Route B: YAML. Export the current definition, edit descriptions, and apply it:
--   SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW('COOKBOOK_DESCRIPTION_QUALITY.SALES.ORDERS_SV');
-- Arguments: schema, yaml, verify_only, create_or_alter. TRUE as the third
-- argument validates without creating; FALSE applies it.
-- Applying has the same rule as Route A: an element missing from the YAML is
-- removed from the view. The YAML below is the complete view, element for
-- element the same as Route A (four dimensions, two facts, three metrics), so
-- setting the third argument to FALSE keeps all nine. Edit an export of your own
-- view, never a partial file.
-- -----------------------------------------------------------------------------
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML($SCHEMA_FQ, $$
name: ORDERS_SV
description: Contoso Outdoor orders with net revenue, discounts, status, and channel.
tables:
  - name: ORDERS
    description: One row per customer order placed with Contoso Outdoor, January to March 2026, all statuses.
    base_table:
      database: COOKBOOK_DESCRIPTION_QUALITY
      schema: SALES
      table: ORDERS
    primary_key:
      columns: [ORDER_ID]
    dimensions:
      - name: CUSTOMER_NAME
        expr: CUSTOMER_NAME
        data_type: VARCHAR
        description: Full name of the person who placed the order, as entered at checkout.
      - name: STATUS
        expr: STATUS
        data_type: VARCHAR
        description: Fulfillment status. SHIPPED orders count as sales; RETURNED and CANCELLED orders do not.
        sample_values: [SHIPPED, RETURNED, CANCELLED]
        is_enum: true
      - name: ORDER_CHANNEL
        expr: CASE ORD_CHNL WHEN 'W' THEN 'Web' WHEN 'S' THEN 'Store' WHEN 'P' THEN 'Phone' END
        data_type: VARCHAR
        synonyms: [ord_chnl]
        description: Channel the order came through, decoded from the legacy ORD_CHNL code (W, S, P).
        sample_values: [Web, Store, Phone]
        is_enum: true
    time_dimensions:
      - name: ORDER_DATE
        expr: ORDER_DATE
        data_type: DATE
        description: Date the order was placed.
    facts:
      - name: DISCOUNT_AMOUNT
        expr: DISCOUNT_AMOUNT
        data_type: NUMBER(10,2)
        description: Discount applied to the order, in USD. NET_AMOUNT = GROSS_AMOUNT - DISCOUNT_AMOUNT.
      - name: NET_AMOUNT
        expr: NET_AMOUNT
        data_type: NUMBER(10,2)
        description: Order amount after discount, in USD. Excludes tax and shipping.
    metrics:
      - name: TOTAL_REVENUE
        expr: SUM(orders.net_amount)
        description: Sum of NET_AMOUNT in USD across all order statuses. Filter STATUS = SHIPPED for recognized sales.
      - name: AVG_ORDER_VALUE
        expr: AVG(orders.net_amount)
        description: Average NET_AMOUNT per order, in USD, across all order statuses.
      - name: ORDER_COUNT
        expr: COUNT(orders.order_id)
        description: Number of orders, across all statuses.
$$, TRUE, TRUE);
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- Semantic view description quality: teardown
-- =============================================================================

SET DB        = 'COOKBOOK_DESCRIPTION_QUALITY';
SET WH        = 'COOKBOOK_DESCRIPTION_QUALITY_WH';
SET ROLE_NAME = 'COOKBOOK_DESCRIPTION_QUALITY_ROLE';

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS IDENTIFIER($DB);
DROP WAREHOUSE IF EXISTS IDENTIFIER($WH);
DROP ROLE IF EXISTS IDENTIFIER($ROLE_NAME);

SHOW DATABASES LIKE 'COOKBOOK_DESCRIPTION_QUALITY%';
SHOW WAREHOUSES LIKE 'COOKBOOK_DESCRIPTION_QUALITY%';
SHOW ROLES LIKE 'COOKBOOK_DESCRIPTION_QUALITY%';
```
