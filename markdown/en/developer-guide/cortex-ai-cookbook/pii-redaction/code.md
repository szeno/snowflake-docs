# PII redaction with AI\_REDACT, AI\_COMPLETE extraction, and an entity cache: code

Every file in the [PII redaction with AI\_REDACT, AI\_COMPLETE extraction, and an entity cache](/developer-guide/cortex-ai-cookbook/pii-redaction) recipe. To run the recipe, download [pii-redaction.zip](/static/samples/cortex-ai-cookbook/pii-redaction.zip), unzip it, and run the scripts from the `pii-redaction/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/pii-redaction); the zip includes it as `README.md`.

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- =============================================================================
-- PII redaction: setup
-- Creates the recipe role, warehouse, database, synthetic document chunks,
-- the model config row, the two UDFs used by the extract-and-replace pattern,
-- and the PII entity cache table.
-- =============================================================================

SET DB        = 'COOKBOOK_PII_REDACTION';
SET SCHEMA_FQ = 'COOKBOOK_PII_REDACTION.REDACTION';
SET WH        = 'COOKBOOK_PII_REDACTION_WH';
SET ROLE_NAME = 'COOKBOOK_PII_REDACTION_ROLE';
SET MODEL     = 'claude-sonnet-4-6';
SET CUR_USER  = '"' || CURRENT_USER() || '"';

-- -----------------------------------------------------------------------------
-- 1. Account objects (ACCOUNTADMIN only for these statements)
-- -----------------------------------------------------------------------------
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($ROLE_NAME)
  COMMENT = 'Cortex AI Cookbook: pii-redaction';
GRANT ROLE IDENTIFIER($ROLE_NAME) TO USER IDENTIFIER($CUR_USER);
-- Keeps the recipe role in the system hierarchy so ACCOUNTADMIN can drop its objects in teardown.
GRANT ROLE IDENTIFIER($ROLE_NAME) TO ROLE SYSADMIN;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($ROLE_NAME);
-- Needed only to RESUME the scheduled task in 04. Dropped with the role.
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($ROLE_NAME);

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($WH)
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Cortex AI Cookbook: pii-redaction';
GRANT USAGE, OPERATE ON WAREHOUSE IDENTIFIER($WH) TO ROLE IDENTIFIER($ROLE_NAME);

CREATE DATABASE IF NOT EXISTS IDENTIFIER($DB)
  COMMENT = 'Cortex AI Cookbook: pii-redaction';
GRANT OWNERSHIP ON DATABASE IDENTIFIER($DB) TO ROLE IDENTIFIER($ROLE_NAME) COPY CURRENT GRANTS;

-- -----------------------------------------------------------------------------
-- 2. Everything else runs as the recipe role
-- -----------------------------------------------------------------------------
USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
CREATE SCHEMA IF NOT EXISTS REDACTION;
USE SCHEMA REDACTION;

-- Model used by the extract-and-replace pattern. Scheduled tasks do not see
-- session variables, so the model name is stored in a one-row config table and
-- read by the refresh procedure in 04.
CREATE OR REPLACE TABLE PII_CONFIG (MODEL_NAME VARCHAR NOT NULL);
INSERT INTO PII_CONFIG SELECT $MODEL;

-- -----------------------------------------------------------------------------
-- 3. Synthetic document chunks (all names, numbers, and organizations are fictional)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE DOCUMENT_CHUNKS (
    DOC_ID       VARCHAR,
    CHUNK_INDEX  NUMBER,
    DOC_TYPE     VARCHAR,
    CHUNK_TEXT   VARCHAR
);

INSERT INTO DOCUMENT_CHUNKS (DOC_ID, CHUNK_INDEX, DOC_TYPE, CHUNK_TEXT) VALUES
('DOC-001', 1, 'contract', 'MASTER SERVICE AGREEMENT between Northwind Traders LLC and Contoso Bank, effective January 15, 2026, for the provision of managed data services.'),
('DOC-001', 2, 'contract', 'Primary contact for Northwind Traders: Sarah Mitchell, VP of Engineering, sarah.mitchell@northwind.example.com, phone (415) 555-0142. Notices go to 2847 Market Street, Suite 400, San Francisco, CA 94105.'),
('DOC-001', 3, 'contract', 'The term of this agreement is thirty-six months with automatic renewal for successive twelve-month periods unless either party gives ninety days written notice.'),
('DOC-001', 4, 'contract', 'Authorized signatory: James Chen, Chief Executive Officer. Signatory date of birth: March 12, 1978. Federal tax ID on file with the Contoso Bank relationship team.'),
('DOC-002', 1, 'email', 'From: jennifer.walsh@acme.example.com\nTo: support@contosobank.example.com\nSubject: Card dispute\n\nHi team, I need to dispute a charge on my card ending 1111.'),
('DOC-002', 2, 'email', 'My full card number is 4111 1111 1111 1111, expiration 09/28, CVV 123. The charge of $412.50 from Fabrikam Outfitters was not authorized.'),
('DOC-002', 3, 'email', 'You can reach me at (628) 555-0291 or at home: 1200 Technology Drive, Austin, TX 78701. Thanks, Jennifer Walsh.'),
('DOC-003', 1, 'support_ticket', 'Ticket CB-4471. Customer Angela Peters (Contoso Bank member ID CB-MBR-20417) reports that the mobile app logged her out during a transfer.'),
('DOC-003', 2, 'support_ticket', 'The customer connected from IP address 203.0.113.54. Session logs show two failed logins before the successful one. No evidence of account takeover.'),
('DOC-003', 3, 'support_ticket', 'Resolution: cleared the device token and asked the customer to update the app. Ticket closed after confirmation by phone at 555-0177.'),
('DOC-004', 1, 'medical_note', 'Patient: Robert Anderson, 54-year-old male, MRN AH-448812, seen at Acme Health Clinic on February 3, 2026 for a follow-up visit.'),
('DOC-004', 2, 'medical_note', 'Patient reports improved sleep since starting the new medication. Blood pressure 128/82. No medication changes today.'),
('DOC-004', 3, 'medical_note', 'Insurance: Fabrikam Mutual policy FM-POL-7730215. Emergency contact: Linda Anderson (spouse), 503-555-0167.'),
('DOC-005', 1, 'financial_report', 'Quarterly operating summary for Northwind Traders. Revenue grew 8 percent quarter over quarter, driven by the logistics segment.'),
('DOC-005', 2, 'financial_report', 'Operating cash is held at Contoso Bank, account number 000123456789, routing number 110000000. The line of credit with Northwind Credit Union remains undrawn.'),
('DOC-005', 3, 'financial_report', 'Prepared by Priya Kapoor, Controller (priya.kapoor@northwind.example.com). Reviewed by the audit committee on April 20, 2026.'),
('DOC-006', 1, 'hr_record', 'Employee onboarding record for Marcus Johnson, hired as a data engineer. Start date: May 4, 2026. Gender: male. Age: 31.'),
('DOC-006', 2, 'hr_record', 'Identity documents verified: US passport 912345678 and California driver license D1234567. SSN 900-12-3456 recorded for payroll.'),
('DOC-006', 3, 'hr_record', 'Direct deposit to Fabrikam Trust account ending 4432. Benefits enrollment window closes thirty days after the start date.'),
('DOC-007', 1, 'email', 'Hola equipo, el cliente Carlos Rivera (carlos.rivera@example.com) llamo desde el 555-0133 para cambiar su direccion a Calle Mayor 12, Madrid.'),
('DOC-007', 2, 'email', 'The on-call rotation for the platform team starts Monday. Please review the runbook before your shift and acknowledge in the tracker.'),
('DOC-008', 1, 'support_ticket', 'Ticket CB-4502. Kevin OBrien, security analyst, rotated the service credentials for the reporting integration after a scheduled review.'),
('DOC-008', 2, 'support_ticket', 'No customer data was involved. The integration was paused for twelve minutes during rotation and resumed without errors.');

-- -----------------------------------------------------------------------------
-- 4. Extract-and-replace building blocks
-- -----------------------------------------------------------------------------

-- EXTRACT_PII: asks the model for the PII values in a chunk as structured JSON.
-- The model argument must be a constant at the call site (a literal, a session
-- variable such as $MODEL, or a Snowflake Scripting bind variable).
-- response_format is its own AI_COMPLETE argument, separate from model_parameters.
CREATE OR REPLACE FUNCTION EXTRACT_PII(MODEL_NAME VARCHAR, CHUNK VARCHAR)
RETURNS VARIANT
COMMENT = 'Cortex AI Cookbook: returns {"redacted_items":[{"phrase","field_type"}]}'
AS
$$
  AI_COMPLETE(
    model => MODEL_NAME,
    prompt => CONCAT(
      'Identify every piece of personally identifiable or sensitive information in the text below: ',
      'person names, email addresses, phone numbers, postal addresses, dates of birth, ages, genders, ',
      'national ID or tax numbers, passport and driver license numbers, payment card data, bank account ',
      'and routing numbers, IP addresses, medical record numbers, insurance policy numbers, and internal ',
      'member or customer IDs. Return each value exactly as it appears in the text as phrase, with its ',
      'category as field_type. Do not return company names or ordinary business dates. ',
      'If there is none, return an empty array. Respond in JSON.\n\n<text>',
      CHUNK,
      '</text>'
    ),
    model_parameters => {'temperature': 0, 'max_tokens': 1024},
    response_format => {
      'type': 'json',
      'schema': {
        'type': 'object',
        'properties': {
          'redacted_items': {
            'type': 'array',
            'items': {
              'type': 'object',
              'properties': {
                'phrase':     {'type': 'string'},
                -- A fixed label set keeps labels stable across rows and runs.
                -- Add your own domain identifiers here.
                'field_type': {'type': 'string', 'enum': [
                  'NAME', 'EMAIL', 'PHONE_NUMBER', 'ADDRESS', 'DATE_OF_BIRTH', 'AGE', 'GENDER',
                  'NATIONAL_ID', 'TAX_ID', 'PASSPORT', 'DRIVERS_LICENSE', 'PAYMENT_CARD',
                  'BANK_ACCOUNT', 'ROUTING_NUMBER', 'IP_ADDRESS', 'MRN', 'POLICY_NUMBER',
                  'MEMBER_ID', 'OTHER_ID']}
              },
              'required': ['phrase', 'field_type']
            }
          }
        },
        'required': ['redacted_items']
      }
    }
  )
$$;

-- REDACT_PII: deterministic replacement of the extracted phrases with typed labels.
-- Longest phrase first, so "Linda Anderson" is replaced before "Anderson".
-- Fails closed: when PII_ENTITIES is NULL (a failed extraction returns NULL when
-- AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR is FALSE) or not the expected shape, it
-- returns '[REDACTION UNAVAILABLE]' instead of the original text.
CREATE OR REPLACE FUNCTION REDACT_PII(CHUNK VARCHAR, PII_ENTITIES VARIANT)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
HANDLER = 'redact_pii'
COMMENT = 'Cortex AI Cookbook: replaces extracted phrases with [FIELD_TYPE REDACTED]'
AS
$$
import json
import re

UNAVAILABLE = '[REDACTION UNAVAILABLE]'

def redact_pii(chunk, pii_entities):
    if chunk is None:
        return None
    if pii_entities is None:
        return UNAVAILABLE
    if isinstance(pii_entities, str):
        try:
            pii_entities = json.loads(pii_entities)
        except ValueError:
            return UNAVAILABLE
    items = pii_entities.get('redacted_items') if isinstance(pii_entities, dict) else None
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        return UNAVAILABLE
    result = chunk
    for item in sorted(items, key=lambda x: len(x.get('phrase') or ''), reverse=True):
        phrase = item.get('phrase') or ''
        label = re.sub(r'[^A-Z0-9]+', '_', (item.get('field_type') or 'PII').upper()).strip('_') or 'PII'
        if phrase:
            result = result.replace(phrase, f'[{label} REDACTED]')
    return result
$$;

-- REDACT_SPANS: selective redaction from AI_REDACT detect-mode output, keeping
-- any values on an allowlist. Accepts the documented {"spans": [...]} object
-- and a bare array of spans. Fails closed like REDACT_PII when SPANS is missing.
-- The view in 03 does not use it.
CREATE OR REPLACE FUNCTION REDACT_SPANS(CHUNK VARCHAR, SPANS VARIANT, ALLOWLIST ARRAY)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
HANDLER = 'redact_spans'
COMMENT = 'Cortex AI Cookbook: applies AI_REDACT detect-mode spans, skipping allowlisted values'
AS
$$
UNAVAILABLE = '[REDACTION UNAVAILABLE]'

def redact_spans(chunk, spans, allowlist):
    if chunk is None:
        return None
    if isinstance(spans, dict):
        spans = spans.get('spans')
    if not isinstance(spans, list):
        return UNAVAILABLE
    keep = set(allowlist or [])
    result = chunk
    # Right to left, so earlier offsets stay valid after each splice.
    for s in sorted(spans, key=lambda x: x['start'], reverse=True):
        if s.get('text') in keep:
            continue
        result = result[:s['start']] + f"[{s['category']}]" + result[s['end']:]
    return result
$$;

-- -----------------------------------------------------------------------------
-- 5. Cache of extracted entities, keyed by chunk and content hash
-- -----------------------------------------------------------------------------
CREATE OR REPLACE TABLE PII_ENTITY_CACHE (
    DOC_ID        VARCHAR,
    CHUNK_INDEX   NUMBER,
    PII_ENTITIES  VARIANT,
    CONTENT_HASH  VARCHAR,
    MODEL_NAME    VARCHAR,
    EXTRACTED_AT  TIMESTAMP_LTZ
);

SELECT DOC_TYPE, COUNT(DISTINCT DOC_ID) AS DOCS, COUNT(*) AS CHUNKS
FROM DOCUMENT_CHUNKS
GROUP BY DOC_TYPE
ORDER BY DOC_TYPE;
```

### `sql/02_ai_redact.sql`

Copy code

```
-- =============================================================================
-- PII redaction: AI_REDACT (managed redaction)
-- Redact mode, detect mode, category filtering, selective redaction with an
-- allowlist, token estimates, and row-level error handling.
-- =============================================================================

SET DB        = 'COOKBOOK_PII_REDACTION';
SET WH        = 'COOKBOOK_PII_REDACTION_WH';
SET ROLE_NAME = 'COOKBOOK_PII_REDACTION_ROLE';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA REDACTION;

-- 1. Redact mode (default): PII is replaced with category placeholders such as [NAME].
SELECT DOC_ID, CHUNK_INDEX, AI_REDACT(CHUNK_TEXT) AS REDACTED_TEXT
FROM DOCUMENT_CHUNKS
ORDER BY DOC_ID, CHUNK_INDEX;

-- 2. Restrict to specific categories. An unsupported category is an error.
SELECT DOC_ID, CHUNK_INDEX,
       AI_REDACT(input => CHUNK_TEXT, categories => ['NAME', 'EMAIL']) AS NAMES_AND_EMAILS_ONLY
FROM DOCUMENT_CHUNKS
WHERE DOC_ID IN ('DOC-001', 'DOC-005')
ORDER BY DOC_ID, CHUNK_INDEX;

-- 3. Detect mode: returns the category, offsets, and text of each span without redacting.
--    The docs describe an object with a "spans" array; the IFF accepts that shape
--    and a bare array of spans.
WITH detected AS (
    SELECT DOC_ID, CHUNK_INDEX, AI_REDACT(input => CHUNK_TEXT, mode => 'detect') AS DETECTED
    FROM DOCUMENT_CHUNKS
    WHERE DOC_ID IN ('DOC-003', 'DOC-008')
)
SELECT d.DOC_ID, d.CHUNK_INDEX,
       s.value:category::VARCHAR AS CATEGORY,
       s.value:text::VARCHAR     AS DETECTED_TEXT,
       s.value:start::NUMBER     AS START_POS,
       s.value:end::NUMBER       AS END_POS
FROM detected d,
     LATERAL FLATTEN(input => IFF(IS_OBJECT(d.DETECTED), d.DETECTED:spans, d.DETECTED)) s
ORDER BY d.DOC_ID, d.CHUNK_INDEX, START_POS;

-- 4. Selective redaction: keep allowlisted values (here, an employee name) and
--    redact everything else that detect mode found.
SELECT DOC_ID, CHUNK_INDEX,
       REDACT_SPANS(CHUNK_TEXT,
                    AI_REDACT(input => CHUNK_TEXT, mode => 'detect'),
                    ['Kevin OBrien']) AS REDACTED_EXCEPT_STAFF
FROM DOCUMENT_CHUNKS
WHERE DOC_ID IN ('DOC-003', 'DOC-008')
ORDER BY DOC_ID, CHUNK_INDEX;

-- 5. Estimate input tokens before a large run. The documented limit is 4,096
--    input plus output tokens, with at most 1,024 output tokens. Split longer
--    text first (for example with SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER).
SELECT DOC_ID, CHUNK_INDEX, AI_COUNT_TOKENS('ai_redact', CHUNK_TEXT) AS INPUT_TOKENS
FROM DOCUMENT_CHUNKS
ORDER BY INPUT_TOKENS DESC
LIMIT 5;

-- 6. Row-level errors. With AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR = TRUE a bad
--    row fails the whole query. With FALSE it returns NULL, and
--    return_error_details => TRUE returns {value, error} so you can see why.
SHOW PARAMETERS LIKE 'AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR' IN SESSION;

ALTER SESSION SET AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR = FALSE;
SELECT r:value::VARCHAR AS REDACTED_TEXT, r:error::VARCHAR AS ERROR_MESSAGE
FROM (
    SELECT AI_REDACT(input => CHUNK_TEXT, categories => ['MRN'], return_error_details => TRUE) AS r
    FROM DOCUMENT_CHUNKS
    WHERE DOC_ID = 'DOC-004' AND CHUNK_INDEX = 1
);
ALTER SESSION UNSET AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR;
```

### `sql/03_extract_and_replace.sql`

Copy code

```
-- =============================================================================
-- PII redaction: AI_COMPLETE extract-and-replace, and the entity cache
-- The model finds PII (including domain identifiers AI_REDACT does not cover)
-- and returns it as structured JSON; a deterministic UDF does the replacement.
-- =============================================================================

SET DB        = 'COOKBOOK_PII_REDACTION';
SET WH        = 'COOKBOOK_PII_REDACTION_WH';
SET ROLE_NAME = 'COOKBOOK_PII_REDACTION_ROLE';
SET MODEL     = 'claude-sonnet-4-6';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA REDACTION;

-- 1. Extract: one structured-output call per chunk.
SELECT DOC_ID, CHUNK_INDEX, EXTRACT_PII($MODEL, CHUNK_TEXT) AS PII_ENTITIES
FROM DOCUMENT_CHUNKS
WHERE DOC_ID IN ('DOC-004', 'DOC-005')
ORDER BY DOC_ID, CHUNK_INDEX;

-- 2. Extract and replace in one query. Compare the MRN, policy number, member ID,
--    and bank numbers with the AI_REDACT output from 02.
WITH extracted AS (
    SELECT DOC_ID, CHUNK_INDEX, CHUNK_TEXT, EXTRACT_PII($MODEL, CHUNK_TEXT) AS PII_ENTITIES
    FROM DOCUMENT_CHUNKS
    WHERE DOC_ID IN ('DOC-003', 'DOC-004', 'DOC-005')
)
SELECT DOC_ID, CHUNK_INDEX,
       ARRAY_SIZE(PII_ENTITIES:redacted_items) AS ITEMS_FOUND,
       REDACT_PII(CHUNK_TEXT, PII_ENTITIES)    AS REDACTED_TEXT
FROM extracted
ORDER BY DOC_ID, CHUNK_INDEX;

-- 3. Populate the cache. Only chunks with no cache row, whose text changed since
--    extraction (hash mismatch), or whose extraction failed (PII_ENTITIES is
--    NULL) call the model. Safe to rerun.
MERGE INTO PII_ENTITY_CACHE c
USING (
    SELECT d.DOC_ID, d.CHUNK_INDEX, d.CHUNK_TEXT, MD5(d.CHUNK_TEXT) AS CONTENT_HASH
    FROM DOCUMENT_CHUNKS d
    LEFT JOIN PII_ENTITY_CACHE x
      ON x.DOC_ID = d.DOC_ID AND x.CHUNK_INDEX = d.CHUNK_INDEX AND x.CONTENT_HASH = MD5(d.CHUNK_TEXT)
     AND x.PII_ENTITIES IS NOT NULL
    WHERE x.DOC_ID IS NULL
) s
ON c.DOC_ID = s.DOC_ID AND c.CHUNK_INDEX = s.CHUNK_INDEX
WHEN MATCHED THEN UPDATE SET
    PII_ENTITIES = EXTRACT_PII($MODEL, s.CHUNK_TEXT),
    CONTENT_HASH = s.CONTENT_HASH,
    MODEL_NAME   = $MODEL,
    EXTRACTED_AT = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (DOC_ID, CHUNK_INDEX, PII_ENTITIES, CONTENT_HASH, MODEL_NAME, EXTRACTED_AT)
    VALUES (s.DOC_ID, s.CHUNK_INDEX, EXTRACT_PII($MODEL, s.CHUNK_TEXT), s.CONTENT_HASH, $MODEL, CURRENT_TIMESTAMP());

-- 4. Query-time redaction. A cache hit needs a matching hash and non-NULL
--    entities, and costs no model call. On a miss (new or edited text, or a
--    failed extraction) the row falls back to AI_REDACT, which covers only its 13
--    categories: domain identifiers such as MRNs and member IDs stay visible until
--    the cache is refreshed. If AI_REDACT also returns NULL, the row shows
--    '[REDACTION UNAVAILABLE]'. No path returns the source text as is.
SELECT d.DOC_ID, d.CHUNK_INDEX,
       IFF(c.DOC_ID IS NOT NULL, 'cache', 'live AI_REDACT') AS SOURCE,
       IFF(c.DOC_ID IS NOT NULL,
           REDACT_PII(d.CHUNK_TEXT, c.PII_ENTITIES),
           COALESCE(AI_REDACT(d.CHUNK_TEXT), '[REDACTION UNAVAILABLE]')) AS REDACTED_TEXT
FROM DOCUMENT_CHUNKS d
LEFT JOIN PII_ENTITY_CACHE c
  ON c.DOC_ID = d.DOC_ID AND c.CHUNK_INDEX = d.CHUNK_INDEX AND c.CONTENT_HASH = MD5(d.CHUNK_TEXT)
 AND c.PII_ENTITIES IS NOT NULL
ORDER BY d.DOC_ID, d.CHUNK_INDEX;

-- 5. A view that downstream consumers can be granted instead of the raw table.
--    Same logic as step 4.
CREATE OR REPLACE VIEW DOCUMENT_CHUNKS_REDACTED AS
SELECT d.DOC_ID, d.CHUNK_INDEX, d.DOC_TYPE,
       IFF(c.DOC_ID IS NOT NULL,
           REDACT_PII(d.CHUNK_TEXT, c.PII_ENTITIES),
           COALESCE(AI_REDACT(d.CHUNK_TEXT), '[REDACTION UNAVAILABLE]')) AS CHUNK_TEXT
FROM DOCUMENT_CHUNKS d
LEFT JOIN PII_ENTITY_CACHE c
  ON c.DOC_ID = d.DOC_ID AND c.CHUNK_INDEX = d.CHUNK_INDEX AND c.CONTENT_HASH = MD5(d.CHUNK_TEXT)
 AND c.PII_ENTITIES IS NOT NULL;
```

### `sql/04_incremental_cache.sql`

Copy code

```
-- =============================================================================
-- PII redaction: keep the cache current with a stream and a task
-- A standard stream (not append-only) records inserts, updates, and deletes,
-- so edited chunks are re-extracted and deleted chunks leave the cache.
-- =============================================================================

SET DB        = 'COOKBOOK_PII_REDACTION';
SET WH        = 'COOKBOOK_PII_REDACTION_WH';
SET ROLE_NAME = 'COOKBOOK_PII_REDACTION_ROLE';

USE ROLE IDENTIFIER($ROLE_NAME);
USE WAREHOUSE IDENTIFIER($WH);
USE DATABASE IDENTIFIER($DB);
USE SCHEMA REDACTION;

-- 1. Standard stream on the source table. APPEND_ONLY = TRUE would miss UPDATE
--    and DELETE, leaving stale entities in the cache.
CREATE OR REPLACE STREAM PII_SOURCE_STREAM ON TABLE DOCUMENT_CHUNKS;

-- 2. Refresh procedure (caller's rights). Reads the model from PII_CONFIG because
--    a task session does not inherit $MODEL. One MERGE consumes the stream:
--    - an UPDATE appears as a DELETE+INSERT pair with METADATA$ISUPDATE = TRUE;
--      the DELETE half is dropped and the INSERT half re-extracts if the text changed
--    - a plain DELETE removes the cache row
--    - a plain INSERT adds a cache row
--    A second statement retries cache rows whose extraction failed (PII_ENTITIES
--    is NULL, which happens when AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR is
--    FALSE). Until a retry succeeds, the view treats those rows as cache misses.
CREATE OR REPLACE PROCEDURE REFRESH_PII_CACHE()
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = 'Cortex AI Cookbook: applies PII_SOURCE_STREAM changes to PII_ENTITY_CACHE'
EXECUTE AS CALLER
AS
$$
DECLARE
  model VARCHAR;
  rows_changed NUMBER DEFAULT 0;
  rows_retried NUMBER DEFAULT 0;
BEGIN
  SELECT MODEL_NAME INTO :model FROM PII_CONFIG LIMIT 1;
  MERGE INTO PII_ENTITY_CACHE c
  USING (
      SELECT DOC_ID, CHUNK_INDEX, CHUNK_TEXT, METADATA$ACTION AS ACTION
      FROM PII_SOURCE_STREAM
      WHERE NOT (METADATA$ACTION = 'DELETE' AND METADATA$ISUPDATE)
  ) s
  ON c.DOC_ID = s.DOC_ID AND c.CHUNK_INDEX = s.CHUNK_INDEX
  WHEN MATCHED AND s.ACTION = 'DELETE' THEN DELETE
  WHEN MATCHED AND s.ACTION = 'INSERT' AND c.CONTENT_HASH <> MD5(s.CHUNK_TEXT) THEN UPDATE SET
      PII_ENTITIES = EXTRACT_PII(:model, s.CHUNK_TEXT),
      CONTENT_HASH = MD5(s.CHUNK_TEXT),
      MODEL_NAME   = :model,
      EXTRACTED_AT = CURRENT_TIMESTAMP()
  WHEN NOT MATCHED AND s.ACTION = 'INSERT' THEN INSERT
      (DOC_ID, CHUNK_INDEX, PII_ENTITIES, CONTENT_HASH, MODEL_NAME, EXTRACTED_AT)
      VALUES (s.DOC_ID, s.CHUNK_INDEX, EXTRACT_PII(:model, s.CHUNK_TEXT), MD5(s.CHUNK_TEXT), :model, CURRENT_TIMESTAMP());
  rows_changed := SQLROWCOUNT;
  UPDATE PII_ENTITY_CACHE c
     SET PII_ENTITIES = EXTRACT_PII(:model, d.CHUNK_TEXT),
         MODEL_NAME   = :model,
         EXTRACTED_AT = CURRENT_TIMESTAMP()
    FROM DOCUMENT_CHUNKS d
   WHERE c.PII_ENTITIES IS NULL
     AND c.DOC_ID = d.DOC_ID AND c.CHUNK_INDEX = d.CHUNK_INDEX
     AND c.CONTENT_HASH = MD5(d.CHUNK_TEXT);
  rows_retried := SQLROWCOUNT;
  RETURN 'cache rows changed: ' || rows_changed || '; failed extractions retried: ' || rows_retried;
END;
$$;

-- 3. Task that runs the procedure only when the stream has data. Created
--    suspended; resume it to schedule (ALTER TASK PII_CACHE_REFRESH RESUME).
--    Failed extractions are retried on the next run, or on a manual CALL.
CREATE OR REPLACE TASK PII_CACHE_REFRESH
  WAREHOUSE = IDENTIFIER($WH)
  SCHEDULE = '60 MINUTE'
  COMMENT = 'Cortex AI Cookbook: pii-redaction cache refresh'
  WHEN SYSTEM$STREAM_HAS_DATA('PII_SOURCE_STREAM')
AS
  CALL REFRESH_PII_CACHE();

-- 4. Simulate source changes: one new chunk, one edited chunk, one deleted chunk.
INSERT INTO DOCUMENT_CHUNKS (DOC_ID, CHUNK_INDEX, DOC_TYPE, CHUNK_TEXT)
SELECT 'DOC-009', 1, 'support_ticket',
       'Ticket CB-4533. Customer Omar Haddad (member ID CB-MBR-30982, omar.haddad@example.com) asked to reset two-factor authentication.'
WHERE NOT EXISTS (SELECT 1 FROM DOCUMENT_CHUNKS WHERE DOC_ID = 'DOC-009' AND CHUNK_INDEX = 1);

UPDATE DOCUMENT_CHUNKS
   SET CHUNK_TEXT = 'Resolution: cleared the device token. Follow-up call scheduled with Angela Peters at 555-0199.'
 WHERE DOC_ID = 'DOC-003' AND CHUNK_INDEX = 3;

DELETE FROM DOCUMENT_CHUNKS WHERE DOC_ID = 'DOC-008' AND CHUNK_INDEX = 2;

SELECT METADATA$ACTION, METADATA$ISUPDATE, DOC_ID, CHUNK_INDEX
FROM PII_SOURCE_STREAM
ORDER BY DOC_ID, CHUNK_INDEX, METADATA$ACTION;

-- 5. Apply the changes now (the task would do the same on its schedule).
CALL REFRESH_PII_CACHE();
```

### `sql/99_teardown.sql`

Copy code

```
-- =============================================================================
-- PII redaction: teardown
-- Drops everything the recipe created. The task, stream, procedure, UDFs,
-- tables, and view go with the database; EXECUTE TASK goes with the role.
-- =============================================================================

SET DB        = 'COOKBOOK_PII_REDACTION';
SET WH        = 'COOKBOOK_PII_REDACTION_WH';
SET ROLE_NAME = 'COOKBOOK_PII_REDACTION_ROLE';

USE ROLE ACCOUNTADMIN;

ALTER SESSION UNSET AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR;
DROP DATABASE IF EXISTS IDENTIFIER($DB);
DROP WAREHOUSE IF EXISTS IDENTIFIER($WH);
DROP ROLE IF EXISTS IDENTIFIER($ROLE_NAME);

SHOW DATABASES LIKE 'COOKBOOK_PII_REDACTION%';
SHOW WAREHOUSES LIKE 'COOKBOOK_PII_REDACTION%';
SHOW ROLES LIKE 'COOKBOOK_PII_REDACTION%';
```
