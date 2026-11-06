# PII redaction with AI\_REDACT, AI\_COMPLETE extraction, and an entity cache

Redact PII in free text with AI\_REDACT, cover domain identifiers with AI\_COMPLETE structured extraction, and serve redactions from a stream-maintained cache.

|  |  |
| --- | --- |
| Stage | Build, Secure |
| Topics | Cortex AI Functions |
| Status | GA |
| Time to complete | 30min |
| Edition | Any edition with Cortex AI Functions |
| Regions | Regions where AI\_REDACT and the chosen AI\_COMPLETE model are available, or cross-region inference enabled |
| Privileges | ACCOUNTADMIN for 01\_setup.sql account statements and teardown; the recipe runs as COOKBOOK\_PII\_REDACTION\_ROLE |
| Related skills | `cortex-ai-function-studio` (bundled with Cortex Code), `snowflake-tasks` (bundled with Cortex Code) |
| Last verified | 2026-10-04 |
| Authors | Parker Erickson, Bala Krishnamoorthy |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/pii-redaction/code) or download [pii-redaction.zip](/static/samples/cortex-ai-cookbook/pii-redaction.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Free-text columns (support tickets, clinical notes, contracts, email) hold names, phone numbers, card numbers, and
domain identifiers that should not reach analysts, dashboards, or downstream models. This recipe redacts them inside
Snowflake three ways, each covering a gap in the one before: `AI_REDACT` for the standard categories, `AI_COMPLETE`
structured extraction plus a deterministic UDF for identifiers `AI_REDACT` does not cover, and a cache kept current by a
stream and a task, so reads need no model call. You end with a `DOCUMENT_CHUNKS_REDACTED` view you can grant in place of
the raw table.

## When to use this

- You need PII removed from unstructured text before it is queried, shared, or sent to another model.
- Your text contains identifiers beyond the standard categories (medical record numbers, policy numbers, member IDs,
  bank account numbers).
- The same documents are read many times, so extracting once at ingestion is cheaper than redacting on every read.

When not to use it:

- The PII sits in structured columns (an `EMAIL` column, an `SSN` column). Use masking policies and data classification.
- You need a guarantee. Both `AI_REDACT` and `AI_COMPLETE` are best-effort model output; keep a human review or sampling
  step for regulated data.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/pii-redaction/diagram-999572c3.svg)](/static/images/cortex-ai-cookbook/pii-redaction/diagram-999572c3.svg)

- **AI\_REDACT** is a managed function with 13 fixed categories: `NAME`, `EMAIL`, `PHONE_NUMBER`, `DATE_OF_BIRTH`,
  `GENDER`, `AGE`, `ADDRESS`, `NATIONAL_ID`, `PASSPORT`, `TAX_IDENTIFIER`, `PAYMENT_CARD_DATA`, `DRIVERS_LICENSE`, and
  `IP_ADDRESS`. `redact` mode returns text with placeholders; `detect` mode returns the spans (category, start, end,
  text) so you can redact selectively.
- **Extract, then replace.** `EXTRACT_PII` calls `AI_COMPLETE` with a JSON schema in the `response_format` argument
  (its own argument, separate from `model_parameters`). The model only finds values; the `REDACT_PII` Python UDF does
  the string replacement, so labels and replacement rules are code you control.
- **A fixed label set.** The schema constrains `field_type` to an `enum`, so the same kind of value always gets the same
  label. Without it, labels drift between runs (`PHONE` in one row, `PHONE_NUMBER` in the next).
- **Cache keyed by content hash.** Each cache row stores `MD5(CHUNK_TEXT)`. A read uses the cache only when the hash
  still matches and the entities are present. Otherwise it falls back to `AI_REDACT`, which covers only its 13
  categories, so an edited or new chunk can show MRNs, member IDs, and policy or bank numbers until the cache is
  refreshed.
- **Fail closed.** A failed extraction stores NULL entities when `AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR` is
  `FALSE`. The view treats that row as a cache miss, the refresh retries it, and `REDACT_PII` returns
  `[REDACTION UNAVAILABLE]` for missing or malformed entities. If `AI_REDACT` also returns NULL, the view shows the
  same placeholder. No path returns the source text as is.
- **A standard stream, not append-only.** Append-only streams record inserts only. Edits and deletes would leave stale
  entities in the cache, so the recipe uses a standard stream and one `MERGE` that handles all three change types.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Cortex AI Functions | `AI_REDACT`, `AI_COMPLETE`, and `AI_COUNT_TOKENS` are GA. The recipe role gets `SNOWFLAKE.CORTEX_USER`. |
| Model access | Default `claude-sonnet-4-6`. If it is not in your region, enable cross-region inference or change `MODEL` in `01_setup.sql` and `03_extract_and_replace.sql`. |
| ACCOUNTADMIN | Only for the account statements at the top of `01_setup.sql` (role, warehouse, database, `EXECUTE TASK`) and for `99_teardown.sql`. |
| Warehouse | The recipe creates an XSMALL `COOKBOOK_PII_REDACTION_WH`. |

Expand

Show lessSee more

## Quickstart

Run the scripts in order in one session (Snowsight worksheet, or `snow sql -f <file>`):

1. [sql/01\_setup.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-01-setup-sql): role, warehouse, database, 23 synthetic chunks, `EXTRACT_PII`, `REDACT_PII`,
   `REDACT_SPANS`, and the empty cache.
2. [sql/02\_ai\_redact.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-02-ai-redact-sql): `AI_REDACT` in redact and detect mode, category filters, an allowlist,
   token estimates, and error handling.
3. [sql/03\_extract\_and\_replace.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-03-extract-and-replace-sql): extraction, replacement, cache population, and the
   `DOCUMENT_CHUNKS_REDACTED` view.
4. [sql/04\_incremental\_cache.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-04-incremental-cache-sql): stream, refresh procedure, task, and a simulated
   insert, update, and delete.
5. Run the queries in [Verify](#verify).
6. [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/pii-redaction/code#label-cookbook-pii-redaction-sql-99-teardown-sql) when you are done.

## Walkthrough

### 1. See what AI\_REDACT covers

Copy code

```
SELECT DOC_ID, CHUNK_INDEX, AI_REDACT(CHUNK_TEXT) AS REDACTED_TEXT
FROM DOCUMENT_CHUNKS;
```

On the sample data, names, emails, phones, addresses, card data, passport, driver license, SSN, and IP address come back
as placeholders. The MRN (`AH-448812`), member ID (`CB-MBR-20417`), policy number, and bank account and routing numbers
are left in place, because they are not among the 13 categories. That gap is the reason for step 2.

Detect mode returns spans instead of text. Use it to keep known values (for example, staff names) and redact the rest:

Copy code

```
SELECT REDACT_SPANS(CHUNK_TEXT,
                    AI_REDACT(input => CHUNK_TEXT, mode => 'detect'),
                    ['Kevin OBrien']) AS REDACTED_EXCEPT_STAFF
FROM DOCUMENT_CHUNKS;
```

The docs describe the detect-mode return value as an object with a `spans` array. In testing, it came back as a bare
array of spans, so `REDACT_SPANS` and the `FLATTEN` in `02_ai_redact.sql` accept both shapes.

Check size before a large run. The documented limit is 4,096 input plus output tokens, with at most 1,024 output tokens:

Copy code

```
SELECT AI_COUNT_TOKENS('ai_redact', CHUNK_TEXT) AS INPUT_TOKENS FROM DOCUMENT_CHUNKS;
```

The estimate carries a fixed overhead: a one-sentence chunk measured about 450 tokens. Budget for it when you choose a
chunk size, and split long text first (for example with
`SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER`). `AI_REDACT` does not silently truncate. In testing, inputs well over
the documented limit were still processed in full. Do not depend on that: it is outside the documented contract.

### 2. Extract domain identifiers with AI\_COMPLETE

`EXTRACT_PII` wraps one structured-output call. The important parts:

Copy code

```
AI_COMPLETE(
  model => MODEL_NAME,
  prompt => CONCAT('Identify every piece of personally identifiable ... <text>', CHUNK, '</text>'),
  model_parameters => {'temperature': 0, 'max_tokens': 1024},
  response_format => {
    'type': 'json',
    'schema': {'type': 'object',
               'properties': {'redacted_items': {'type': 'array', 'items': {'type': 'object',
                 'properties': {'phrase': {'type': 'string'},
                                'field_type': {'type': 'string', 'enum': ['NAME', 'EMAIL', 'MRN', 'MEMBER_ID', ...]}},
                 'required': ['phrase', 'field_type']}}},
               'required': ['redacted_items']}})
```

With `response_format` set, `AI_COMPLETE` returns an object rather than a string, so no `PARSE_JSON` is needed. The UDF
must be declared `RETURNS VARIANT`; `RETURNS OBJECT` fails to compile.

The model name must be a constant where `EXTRACT_PII` is called: a literal, a session variable (`$MODEL`), or a Snowflake
Scripting bind variable (`:model`). Passing it from a column or CTE fails with “needs to be a string literal”.

Copy code

```
SELECT DOC_ID, REDACT_PII(CHUNK_TEXT, EXTRACT_PII($MODEL, CHUNK_TEXT)) AS REDACTED_TEXT
FROM DOCUMENT_CHUNKS;
-- ... MRN [MRN REDACTED] ... policy [POLICY_NUMBER REDACTED] ... member ID [MEMBER_ID REDACTED] ...
```

`REDACT_PII` replaces the longest phrases first, so “Linda Anderson” is replaced before “Anderson” can leave a fragment
behind.

Extraction is not automatically cheaper than asking the model to rewrite the text. On this sample’s short chunks,
extraction produced 36 to 150 output tokens against 25 to 57 for a full rewrite, because the JSON structure costs
tokens. Choose extraction for control (custom categories, stable labels, deterministic replacement, and a reusable
entity list), and get the savings from the cache, which removes the model call from reads.

### 3. Cache the entities

`03_extract_and_replace.sql` fills `PII_ENTITY_CACHE` with a `MERGE` that calls the model only for chunks with no
cache row, a changed hash, or NULL entities from a failed extraction, so rerunning it costs nothing when nothing
changed. Reads join on the hash and skip cache rows without entities:

Copy code

```
SELECT d.DOC_ID, d.CHUNK_INDEX,
       IFF(c.DOC_ID IS NOT NULL,
           REDACT_PII(d.CHUNK_TEXT, c.PII_ENTITIES),
           COALESCE(AI_REDACT(d.CHUNK_TEXT), '[REDACTION UNAVAILABLE]')) AS CHUNK_TEXT
FROM DOCUMENT_CHUNKS d
LEFT JOIN PII_ENTITY_CACHE c
  ON c.DOC_ID = d.DOC_ID AND c.CHUNK_INDEX = d.CHUNK_INDEX AND c.CONTENT_HASH = MD5(d.CHUNK_TEXT)
 AND c.PII_ENTITIES IS NOT NULL;
```

The same query backs the `DOCUMENT_CHUNKS_REDACTED` view. The `AI_REDACT` fallback keeps a cache miss readable, but
it leaves domain identifiers in place until the refresh runs. If that window is not acceptable, replace the fallback
with the `'[REDACTION UNAVAILABLE]'` literal, so a miss shows no text at all.

### 4. Keep the cache current

`04_incremental_cache.sql` creates a standard stream on `DOCUMENT_CHUNKS`, a caller’s-rights procedure
`REFRESH_PII_CACHE()`, and a task that calls it when `SYSTEM$STREAM_HAS_DATA` is true. In the stream, an `UPDATE`
appears as a `DELETE` and `INSERT` pair with `METADATA$ISUPDATE = TRUE`. The procedure drops the `DELETE` half, deletes
cache rows for real deletes, and re-extracts only when the text hash changed:

Copy code

```
MERGE INTO PII_ENTITY_CACHE c
USING (SELECT DOC_ID, CHUNK_INDEX, CHUNK_TEXT, METADATA$ACTION AS ACTION
       FROM PII_SOURCE_STREAM
       WHERE NOT (METADATA$ACTION = 'DELETE' AND METADATA$ISUPDATE)) s
ON c.DOC_ID = s.DOC_ID AND c.CHUNK_INDEX = s.CHUNK_INDEX
WHEN MATCHED AND s.ACTION = 'DELETE' THEN DELETE
WHEN MATCHED AND s.ACTION = 'INSERT' AND c.CONTENT_HASH <> MD5(s.CHUNK_TEXT) THEN UPDATE SET ...
WHEN NOT MATCHED AND s.ACTION = 'INSERT' THEN INSERT ...;
```

A second statement in the procedure retries cache rows whose entities are NULL and whose hash still matches, so a
failed extraction is fixed on the next refresh rather than left for the next edit of that chunk.

A task runs in its own session and does not see `$MODEL`, so setup stores the model name in `PII_CONFIG` and the
procedure reads it into a bind variable. The task is created suspended. To schedule it:

Copy code

```
ALTER TASK PII_CACHE_REFRESH RESUME;
-- or run it once now:
EXECUTE TASK PII_CACHE_REFRESH;
```

## Verify

Run as `COOKBOOK_PII_REDACTION_ROLE` after step 4:

Copy code

```
USE ROLE COOKBOOK_PII_REDACTION_ROLE;
USE WAREHOUSE COOKBOOK_PII_REDACTION_WH;
USE SCHEMA COOKBOOK_PII_REDACTION.REDACTION;

SELECT
  (SELECT COUNT(*) FROM DOCUMENT_CHUNKS) AS SOURCE_ROWS,
  (SELECT COUNT(*) FROM PII_ENTITY_CACHE) AS CACHE_ROWS,
  (SELECT COUNT(*) FROM DOCUMENT_CHUNKS d JOIN PII_ENTITY_CACHE c
     ON c.DOC_ID = d.DOC_ID AND c.CHUNK_INDEX = d.CHUNK_INDEX
    AND c.CONTENT_HASH = MD5(d.CHUNK_TEXT) AND c.PII_ENTITIES IS NOT NULL) AS FRESH_ROWS,
  (SELECT COUNT_IF(PII_ENTITIES IS NULL) FROM PII_ENTITY_CACHE) AS FAILED_EXTRACTIONS,
  (SELECT COUNT(*) FROM PII_SOURCE_STREAM) AS PENDING_CHANGES,
  (SELECT COUNT_IF(CHUNK_TEXT REGEXP '.*(555-01[0-9]{2}|@[a-z.]*example\\.com|AH-448812|CB-MBR-[0-9]+).*')
     FROM DOCUMENT_CHUNKS_REDACTED) AS LEAKED_ROWS;
```

Expected: `SOURCE_ROWS = CACHE_ROWS = FRESH_ROWS = 23`, `FAILED_EXTRACTIONS = 0`, `PENDING_CHANGES = 0`,
`LEAKED_ROWS = 0`. `CALL REFRESH_PII_CACHE()` in step 4 returns
`cache rows changed: 3; failed extractions retried: 0` (one insert, one update, one delete). Model output can vary
slightly between runs; if `LEAKED_ROWS` is not zero, inspect that row’s `PII_ENTITIES`.

Then check that a failed extraction fails closed. This sets one cache row’s entities to NULL, as a failed
`EXTRACT_PII` call would, reads the view, and lets the refresh repair the row:

Copy code

```
UPDATE PII_ENTITY_CACHE SET PII_ENTITIES = NULL WHERE DOC_ID = 'DOC-001' AND CHUNK_INDEX = 2;

SELECT v.CHUNK_TEXT                                 AS VIEW_TEXT,
       v.CHUNK_TEXT LIKE '%sarah.mitchell@%'        AS RAW_EMAIL_SHOWN,
       REDACT_PII(d.CHUNK_TEXT, NULL)               AS UDF_WITHOUT_ENTITIES
FROM DOCUMENT_CHUNKS_REDACTED v
JOIN DOCUMENT_CHUNKS d ON d.DOC_ID = v.DOC_ID AND d.CHUNK_INDEX = v.CHUNK_INDEX
WHERE v.DOC_ID = 'DOC-001' AND v.CHUNK_INDEX = 2;

CALL REFRESH_PII_CACHE();
```

Expected: `VIEW_TEXT` is the `AI_REDACT` output (`[NAME]`, `[EMAIL]`, `[PHONE_NUMBER]`, `[ADDRESS]` placeholders),
`RAW_EMAIL_SHOWN = FALSE`, `UDF_WITHOUT_ENTITIES = '[REDACTION UNAVAILABLE]'`, and the `CALL` returns
`cache rows changed: 0; failed extractions retried: 1`. Rerun the first Verify query to see `FAILED_EXTRACTIONS = 0`
again.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| MRNs, member IDs, policy and bank numbers survive `AI_REDACT` | They are outside its 13 categories | Use `EXTRACT_PII` with those labels in the `enum` |
| `AI_REDACT` returns NULL and no error | `AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR` is `FALSE` in the session, so row errors become NULL | Pass `return_error_details => TRUE` and read `:error`, or set the parameter to `TRUE` to fail the query |
| “Unsupported categories: MRN” | `categories` accepts only the 13 built-in names | Handle custom identifiers with `EXTRACT_PII` |
| “Argument number 0 … needs to be a string literal” | The model name came from a column or CTE | Pass a literal, `$MODEL`, or a scripting bind variable |
| “Declared return type ‘OBJECT’ is incompatible with actual return type ‘VARIANT’” | A SQL UDF wrapping `AI_COMPLETE` with `response_format` | Declare `RETURNS VARIANT` |
| Labels differ between rows (`PHONE`, `PHONE_NUMBER`) | `field_type` was free text | Constrain it with an `enum` in the schema |
| Cache serves entities for text that was edited | An `APPEND_ONLY` stream ignores updates and deletes | Use a standard stream, as in `04_incremental_cache.sql` |
| `FLATTEN` over detect-mode output returns no rows | The value is a bare array, not `{spans: [...]}` | `FLATTEN(input => IFF(IS_OBJECT(d), d:spans, d))` |
| MRNs or member IDs show in `DOCUMENT_CHUNKS_REDACTED` for one row | The chunk is new, edited, or its extraction failed, so the view used the `AI_REDACT` fallback | `CALL REFRESH_PII_CACHE()` or resume the task. For no fallback window, replace the fallback with the placeholder |
| A row shows `[REDACTION UNAVAILABLE]` | The cached entities are malformed, or the `AI_REDACT` fallback returned NULL | Check `PII_ENTITIES` for that row, rerun the refresh, and read errors with `return_error_details => TRUE` |
| Task never picks up the model you set | Task sessions do not inherit session variables | Update `PII_CONFIG.MODEL_NAME` |
| `CREATE PROCEDURE` or `CREATE TASK` syntax error at `COMMENT` | Clause order | `COMMENT` before `EXECUTE AS`; for tasks, before `WHEN` |

Expand

Show lessSee more

## Teardown

Copy code

```
-- sql/99_teardown.sql
DROP DATABASE IF EXISTS COOKBOOK_PII_REDACTION;       -- task, stream, procedure, UDFs, tables, view
DROP WAREHOUSE IF EXISTS COOKBOOK_PII_REDACTION_WH;
DROP ROLE IF EXISTS COOKBOOK_PII_REDACTION_ROLE;       -- also removes the EXECUTE TASK grant
```

Setup grants the recipe role to `SYSADMIN` so that `ACCOUNTADMIN` can drop the database the role owns. The recipe makes
no other account-level changes.

## Adapt this recipe

Keep these, so a customized version keeps the recipe’s security model:

- Least privilege: `ACCOUNTADMIN` only for the scripts listed under Privileges; everything else runs as the recipe’s own role.
- No grants to `PUBLIC`.
- Caller’s rights: procedures run as `EXECUTE AS CALLER`, so each user’s own grants apply.
- Credentials: create keys, tokens, and secrets yourself, in a separate terminal, and read them from environment variables. Never put them in a script or give them to an agent.
- Dynamic SQL, if you add any, uses bind variables or an allowlist of identifiers, never text concatenated from user or model input.

Change these to fit your use case:

- Object names. Rename them in every script, including teardown: the recipe repeats them as literals, including inside `$$` bodies, so change them all at once, then check that teardown still removes everything.
- Roles, personas, and users: map them to your own, each granted no more than the recipe grants.
- Data: point the scripts at your tables instead of the sample data, then run Verify again.
- Models and warehouse sizes.

To have a coding agent adapt it:

```
Adapt the pii-redaction recipe in pii-redaction/ (unzipped from pii-redaction.zip) to <describe your use case>.
Read README.md first. Keep everything the "Adapt this recipe" section says to keep.
Change only names, roles and personas, data, and models.
Show me each changed file before you run anything, then run the recipe's Verify steps.
```

## Run it with a coding agent

```
Install or enable these bundled Cortex Code skills before you start, and use them for the sub-tasks they cover:
cortex-ai-function-studio (AI_REDACT, AI_COMPLETE, token estimates) and snowflake-tasks (the refresh task).

Run the recipe in pii-redaction/ on my current Snowflake connection.
1. Confirm the target with SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE() and show me before continuing.
2. sql/01_setup.sql makes account-level changes as ACCOUNTADMIN: it creates a role, a warehouse and a database, and
   grants EXECUTE TASK ON ACCOUNT to the recipe role. Show me those statements and wait for my confirmation.
3. Run sql/01_setup.sql through sql/04_incremental_cache.sql in order (snow sql -f per file; each script sets its own
   context). Do not rename objects. Stop on the first error.
4. Run every Verify query from the README, including the fail-closed check, and report the actual values of
   SOURCE_ROWS, CACHE_ROWS, FRESH_ROWS, FAILED_EXTRACTIONS, PENDING_CHANGES, LEAKED_ROWS, and the fail-closed results.
5. Show three rows from DOCUMENT_CHUNKS_REDACTED next to the AI_REDACT output for the same rows.
6. When I say so, run sql/99_teardown.sql, then confirm nothing named COOKBOOK_PII_REDACTION% remains. Only drop
   objects named COOKBOOK_PII_REDACTION*.
```

## Related skills

- `cortex-ai-function-studio` (bundled): choosing, authoring, and estimating cost for AI functions, including
  `AI_REDACT` and `AI_COMPLETE`.
- `snowflake-tasks` (bundled): scheduling, monitoring, and troubleshooting the refresh task.

## References

- [AI\_REDACT](/sql-reference/functions/ai_redact)
- [AI\_COMPLETE (Single string)](/sql-reference/functions/ai_complete-single-string)
- [AI\_COMPLETE (Structured outputs)](/sql-reference/functions/ai_complete-structured-outputs)
- [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens)
- [Introduction to streams](/user-guide/streams-intro)
- [Introduction to tasks](/user-guide/tasks-intro)
