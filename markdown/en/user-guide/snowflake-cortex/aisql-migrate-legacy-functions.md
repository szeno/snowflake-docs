# Migrate legacy SNOWFLAKE.CORTEX functions to AI Functions

The AI Functions (the `AI_*` functions) are the primary interface for Cortex AI
unstructured analytics and the focus of future development. This page lists the
affected legacy functions, explains how each SQL contract changes, and shows how to
find and migrate affected workloads.

For most workloads the migration is a straightforward code update: you replace the
legacy namespace and function name with the corresponding AI Function. Some functions
also change their arguments or return format, so review the guidance for each function
and test the affected workloads before you deploy.

## Function mapping

Each legacy function maps to an AI Function replacement. The migration effort falls
into two groups: *direct replacements*, where only the name changes, and
*replacements that change behavior*, where you review and test the call before you
swap it.

| Legacy function | Replacement | Migration |
| --- | --- | --- |
| `SNOWFLAKE.CORTEX.COMPLETE` | [AI\_COMPLETE](/sql-reference/functions/ai_complete) | Drop-in for the basic `(model, prompt)` form; calls that pass an options object change (see notes). |
| `SNOWFLAKE.CORTEX.TRY_COMPLETE` | [AI\_COMPLETE](/sql-reference/functions/ai_complete) | Behavior change (error handling). |
| `SNOWFLAKE.CORTEX.TRANSLATE` | [AI\_TRANSLATE](/sql-reference/functions/ai_translate) | Direct replacement. |
| `SNOWFLAKE.CORTEX.SUMMARIZE` | [AI\_SUMMARIZE](/sql-reference/functions/ai_summarize) | Direct replacement. |
| `SNOWFLAKE.CORTEX.CLASSIFY_TEXT` | [AI\_CLASSIFY](/sql-reference/functions/ai_classify) | Behavior change (output format). |
| `SNOWFLAKE.CORTEX.EXTRACT_ANSWER` | [AI\_EXTRACT](/sql-reference/functions/ai_extract) | Behavior change (arguments and output). |
| `SNOWFLAKE.CORTEX.PARSE_DOCUMENT` | [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) | Behavior change (file argument). |
| `SNOWFLAKE.CORTEX.COUNT_TOKENS` | [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens) | Behavior change (arguments). |
| `SNOWFLAKE.CORTEX.EMBED_TEXT_768` | [AI\_EMBED](/sql-reference/functions/ai_embed) | Behavior change (arguments). |
| `SNOWFLAKE.CORTEX.EMBED_TEXT_1024` | [AI\_EMBED](/sql-reference/functions/ai_embed) | Behavior change (arguments). |
| `SNOWFLAKE.CORTEX.SENTIMENT` | [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) | Behavior change (output format). |
| `SNOWFLAKE.CORTEX.ENTITY_SENTIMENT` | [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) | Behavior change (output format). |

Expand

Show lessSee more

### Direct replacements

For these functions the arguments and output are unchanged. Replace the namespace and
function name and no other changes are required:

- `SNOWFLAKE.CORTEX.COMPLETE` to AI\_COMPLETE, for the basic `(model, prompt)` form only
- `SNOWFLAKE.CORTEX.TRANSLATE` to AI\_TRANSLATE
- `SNOWFLAKE.CORTEX.SUMMARIZE` to AI\_SUMMARIZE

### Replacements that change behavior

For these functions the arguments or output differ. Review and test each call before
you swap it, using the guidance in [Behavior changes by function](#label-aisql-migrate-behavior-changes):

- `SNOWFLAKE.CORTEX.COMPLETE` to AI\_COMPLETE, for calls that pass an options object
- `SNOWFLAKE.CORTEX.TRY_COMPLETE` to AI\_COMPLETE
- `SNOWFLAKE.CORTEX.CLASSIFY_TEXT` to AI\_CLASSIFY
- `SNOWFLAKE.CORTEX.EXTRACT_ANSWER` to AI\_EXTRACT
- `SNOWFLAKE.CORTEX.PARSE_DOCUMENT` to AI\_PARSE\_DOCUMENT
- `SNOWFLAKE.CORTEX.COUNT_TOKENS` to AI\_COUNT\_TOKENS
- `SNOWFLAKE.CORTEX.EMBED_TEXT_768` and `SNOWFLAKE.CORTEX.EMBED_TEXT_1024` to AI\_EMBED
- `SNOWFLAKE.CORTEX.SENTIMENT` and `SNOWFLAKE.CORTEX.ENTITY_SENTIMENT` to AI\_SENTIMENT

## Behavior changes by function

### COMPLETE: options, response format, and details

`AI_COMPLETE(model, prompt)` is a drop-in replacement for the basic
`SNOWFLAKE.CORTEX.COMPLETE(model, prompt)` form: both return a string. Calls that pass
the legacy `options` object need changes, because AI\_COMPLETE splits that single object
into separate arguments:

- `AI_COMPLETE(<model>, <prompt> [, <model_parameters>, <response_format>, <show_details> ])`
- The legacy `options` object becomes `model_parameters`, which holds only the model
  hyperparameters (`temperature`, `top_p`, `max_tokens`, `guardrails`). The names and
  defaults are unchanged.
- `response_format` moves out of the object into its own argument. If you leave it inside
  `model_parameters`, it isn’t recognized and the response is returned as an unstructured
  string.
- To return the detailed JSON object (with `choices`, `usage`, `model`, and `created`),
  set `show_details` to TRUE. In the legacy function this object was returned implicitly
  whenever `options` was present, so a call that omits `show_details` now returns a plain
  string. Update any consumer that reads a JSON path such as `:choices[0]:messages`.

Basic call with hyperparameters. The legacy call returns the detailed object because
`options` is present; set `show_details` to reproduce it:

Copy code

```
-- Legacy: returns a JSON object (choices, usage, ...)
SELECT SNOWFLAKE.CORTEX.COMPLETE('<model>', prompt, {'temperature': 0.7, 'max_tokens': 100}) AS response
FROM my_table;
```

Copy code

```
-- Migrated
SELECT AI_COMPLETE(
    model => '<model>',
    prompt => prompt,
    model_parameters => {'temperature': 0.7, 'max_tokens': 100},
    show_details => TRUE
) AS response
FROM my_table;
```

Structured output. Move `response_format` out of the options object into its own
argument:

Copy code

```
-- Legacy
SELECT SNOWFLAKE.CORTEX.COMPLETE('<model>', prompt, {'response_format': <json_schema>}) AS response
FROM my_table;
```

Copy code

```
-- Migrated
SELECT AI_COMPLETE(
    model => '<model>',
    prompt => prompt,
    response_format => <json_schema>
) AS response
FROM my_table;
```

For multi-turn prompts or conversation history, use the prompt object form of
AI\_COMPLETE. For details, see [AI\_COMPLETE](/sql-reference/functions/ai_complete).

### TRY\_COMPLETE: error handling

The AI Functions provide native row-level error handling, so a failed record doesn’t
terminate processing for successful records. By default, failed records return NULL.
Set `return_error_details` to TRUE to return the error associated with each failed
record.

Legacy:

Copy code

```
SELECT
    id,
    SNOWFLAKE.CORTEX.TRY_COMPLETE('<model>', prompt_column) AS response
FROM my_table;
```

Migrated:

Copy code

```
SELECT
    id,
    AI_COMPLETE(
        model => '<model>',
        prompt => prompt_column,
        return_error_details => TRUE
    ) AS response
FROM my_table;
```

### CLASSIFY\_TEXT: output format

AI\_CLASSIFY returns an object whose `labels` field is an array. Read `:labels[0]`
instead of `:label`.

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(review, ['refund','shipping','other']):label AS topic
FROM tickets;
```

Migrated:

Copy code

```
SELECT AI_CLASSIFY(review, ['refund','shipping','other']):labels[0] AS topic
FROM tickets;
```

### EXTRACT\_ANSWER: arguments and output

AI\_EXTRACT returns a JSON object instead of a string. Provide the questions to answer
in the `responseFormat` argument, and set the optional `scores` argument to TRUE to
include confidence scores.

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.EXTRACT_ANSWER(doc_text, 'What is the invoice total?') AS answer
FROM docs;
```

Migrated:

Copy code

```
SELECT AI_EXTRACT(
    text => doc_text,
    responseFormat => {'total': 'What is the invoice total?'},
    scores => TRUE
) AS answer
FROM docs;
```

### PARSE\_DOCUMENT: file argument

AI\_PARSE\_DOCUMENT takes a Snowflake FILE object created with
[TO\_FILE](/sql-reference/functions/to_file), rather than separate stage and path arguments.
This provides a consistent file interface across AI Functions.

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
    '@my_stage', 'document.pdf',
    {'mode': 'LAYOUT', 'page_split': true}
) AS parsed_doc;
```

Migrated:

Copy code

```
SELECT AI_PARSE_DOCUMENT(
    TO_FILE('@my_stage', 'document.pdf'),
    {'mode': 'LAYOUT', 'page_split': true}
) AS parsed_doc;
```

### COUNT\_TOKENS: arguments

The first argument to AI\_COUNT\_TOKENS is the AI Function name (for example,
`'ai_complete'`), not the model. Pass the model as a separate argument for functions
that require one.

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.COUNT_TOKENS('<model>', prompt) AS num_tokens
FROM my_table;
```

Migrated:

Copy code

```
SELECT AI_COUNT_TOKENS('ai_complete', '<model>', prompt) AS num_tokens
FROM my_table;
```

### EMBED\_TEXT\_768 and EMBED\_TEXT\_1024: single function

AI\_EMBED replaces both `EMBED_TEXT_768` and `EMBED_TEXT_1024`. The output dimension is
set by the model, so match your `VECTOR(FLOAT, n)` column to the model’s dimension. For
the available embedding models and their dimensions, see
[Models and regional availability](/user-guide/snowflake-cortex/aisql-regional-availability).

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('<model>', content) AS embedding
FROM docs;
```

Migrated:

Copy code

```
SELECT AI_EMBED('<model>', content) AS embedding
FROM docs;
```

### SENTIMENT and ENTITY\_SENTIMENT: output format

AI\_SENTIMENT returns an object with a `categories` array instead of a FLOAT score.
Each category record includes a `sentiment` field with a value such as `positive`,
`negative`, `neutral`, `mixed`, or `unknown`.

Legacy:

Copy code

```
SELECT SNOWFLAKE.CORTEX.SENTIMENT(review) AS score
FROM reviews;
```

Migrated:

Copy code

```
SELECT AI_SENTIMENT(review) AS sentiment
FROM reviews;
```

For entity-level (aspect-based) sentiment, pass the entities as the second argument:

Copy code

```
SELECT AI_SENTIMENT(review, entities) AS sentiment
FROM reviews;
```

If you depend on the legacy numeric score from -1.0 to 1.0, you can reproduce it with
AI\_COMPLETE and a structured output:

Copy code

```
SELECT AI_COMPLETE(
    model => '<model>',
    prompt => CONCAT('Rate the sentiment of the following text from -1.0 (very negative) to 1.0 (very positive). Respond with only the score. Text: ', review),
    model_parameters => {'temperature': 0},
    response_format => TYPE OBJECT(score FLOAT)
):score::FLOAT AS score
FROM reviews;
```

## Identify affected workloads

Legacy calls live in two places: queries that ran recently, and calls embedded in
stored objects such as views, tasks, procedures, user-defined functions (UDFs), and
dynamic tables. Check both.

Note

ACCOUNT\_USAGE views have ingestion latency. SQL scanning also doesn’t reach
application code, notebooks, Streamlit apps, or queries issued by BI tools. Review
those separately.

### Calls in recent query history

This query shows which legacy functions ran, who ran them, and how often in the past
90 days. ACCOUNT\_USAGE retains query history for 365 days:

Copy code

```
SELECT QUERY_ID, USER_NAME, ROLE_NAME, WAREHOUSE_NAME,
       DATABASE_NAME, SCHEMA_NAME, START_TIME,
       LEFT(QUERY_TEXT, 400) AS query_snippet
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME >= DATEADD('day', -90, CURRENT_TIMESTAMP())
  AND REGEXP_LIKE(QUERY_TEXT, '.*CORTEX\.(COMPLETE|TRY_COMPLETE|CLASSIFY_TEXT|TRANSLATE|SUMMARIZE|EXTRACT_ANSWER|PARSE_DOCUMENT|COUNT_TOKENS|EMBED_TEXT_768|EMBED_TEXT_1024|ENTITY_SENTIMENT|SENTIMENT)\s*\(.*', 'is')
ORDER BY START_TIME DESC;
```

### Calls embedded in object definitions

Query history captures only calls that ran within the retention window. Find calls in
view definitions with:

Copy code

```
SELECT TABLE_CATALOG AS database_name, TABLE_SCHEMA AS schema_name, TABLE_NAME AS view_name
FROM SNOWFLAKE.ACCOUNT_USAGE.VIEWS
WHERE DELETED IS NULL
  AND REGEXP_LIKE(VIEW_DEFINITION, '.*CORTEX\.(COMPLETE|TRY_COMPLETE|CLASSIFY_TEXT|TRANSLATE|SUMMARIZE|EXTRACT_ANSWER|PARSE_DOCUMENT|COUNT_TOKENS|EMBED_TEXT_768|EMBED_TEXT_1024|ENTITY_SENTIMENT|SENTIMENT)\s*\(.*', 'is');
```

For procedures, UDFs, tasks, and dynamic tables, retrieve each definition with
GET\_DDL and search it, or dump an entire schema at once and scan the result:

Copy code

```
SELECT GET_DDL('SCHEMA', '<database>.<schema>', TRUE);
```

## Migrate the calls

Replace each call across every layer where it appears: saved queries and views,
scheduled tasks and dynamic tables, stored procedures and UDFs, and external pipelines
or application logic.

When the legacy call is embedded in an object, note the following:

- **Dynamic tables**: Use `CREATE OR ALTER DYNAMIC TABLE` to swap the function in place.
  Any definition change reinitializes the edited table once, but `CREATE OR ALTER`
  leaves downstream dynamic tables untouched. `CREATE OR REPLACE` recreates the table
  as a new object, which additionally forces every downstream dynamic table with
  incremental refresh to reinitialize on its next refresh. Downstream full-refresh
  tables are unaffected. Before deployment, test the updated DDL on a clone and run
  `EXPLAIN CHANGES` to preview whether the refresh reinitializes. Cortex AI Functions
  support incremental refresh only in the SELECT clause, so keeping the call there
  preserves incremental refresh. After deployment, use `SHOW DYNAMIC TABLES` and check
  the `refresh_mode` and `refresh_mode_reason` columns to confirm the table still
  refreshes as expected.
- **UDFs used by dynamic tables**: Replacing a UDF that a dynamic table depends on
  breaks its next incremental refresh, so recreate the dynamic table after you swap the
  UDF.
- **Views and materialized views**: `CREATE OR REPLACE` drops existing grants, so
  reapply them, and update any downstream object that reads a changed output column or
  JSON path.
- **Tasks**: If the task is suspended when you edit it, resume it afterward and confirm
  the new SQL compiles.

Also review downstream schema and types, because the output changes break consumers
that expect the legacy shape:

- AI\_EMBED output dimension must match the `VECTOR(FLOAT, n)` column.
- AI\_SENTIMENT returns an object instead of a FLOAT, which breaks numeric thresholds.
- AI\_CLASSIFY moves from `:label` to `:labels[0]`, which breaks JSON paths.
- AI\_EXTRACT returns an object instead of a string, which breaks string consumers.
- AI\_COMPLETE handles errors per row and returns NULL by default, so a pipeline that
  relied on a legacy COMPLETE call failing the whole query keeps running with NULLs.
  Set `return_error_details` to surface the errors.

### Automate the direct replacements

You can script most of the work for the direct replacements:

1. Find the impacted objects using the queries in
   [Identify affected workloads](#identify-affected-workloads).
2. For each object, fetch the full definition with GET\_DDL, apply the
   direct-replacement swaps with REGEXP\_REPLACE, and leave the behavior-change cases for
   a person to handle.
3. Test the migrated objects on a zero-copy clone before you apply them to production:

   Copy code

   ```
   CREATE DATABASE <db>_migration_test CLONE <db>;
   ```

   Because AI output is non-deterministic, validate that objects compile and that
   column schema and row counts match, rather than expecting identical text.

## Migrate with Cortex Code

If you use Cortex Code (CoCo), two bundled skills can help you build and optimize
Cortex AI Function workflows as you migrate:

- [`ai-functions-pipeline-builder`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-ai-functions-pipeline-builder):
  Turns a plain-language request into a Snowflake-native pipeline across files on a
  stage and your warehouse tables. It builds an incremental pipeline on dynamic tables
  with AI Functions and keeps outputs fresh as new data lands.
- [`cortex-ai-function-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cortex-ai-function-studio):
  Helps you choose the right built-in AI Function for a task, and build, evaluate, and
  optimize custom AI Functions powered by AI\_COMPLETE. It drafts SQL from the current
  documentation and validates it before you run it.

For the full list of bundled skills, see
[CoCo CLI bundled skills](/user-guide/cortex-code/bundled-skills).

## Why migrate to AI Functions

Migrating keeps your workloads supported and gives you access to the latest Cortex AI
capabilities through a single, modern interface. Depending on the function, these
capabilities include:

- **Performance and scale**: Process high-volume workloads directly over large SQL
  tables. AI Functions are optimized for throughput and batch processing across many
  inputs.
- **Row-level error handling**: Preserve successful results when individual records
  can’t be processed. Supported functions return NULL for failed rows or provide
  detailed error information for each affected record.
- **Structured outputs**: Use [AI\_COMPLETE structured outputs](/sql-reference/functions/ai_complete-structured-outputs)
  to return typed objects.
- **Multimodal processing**: Analyze images, audio, and video with supported functions.
- **Document processing**: Parse and analyze documents with
  [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) and [AI\_EXTRACT](/sql-reference/functions/ai_extract).
- **Token and cost planning**: Use [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens) to
  estimate input token usage before you run a supported AI Function. AI\_COUNT\_TOKENS
  works with AI Function names and doesn’t support the legacy `SNOWFLAKE.CORTEX`
  function names.
- **Evaluation and optimization tooling**: Use
  [Cortex AI Function Studio](/user-guide/snowflake-cortex/ai-function-studio) to
  measure output quality and cost, compare prompts and models, and create optimized
  custom AI Functions.
