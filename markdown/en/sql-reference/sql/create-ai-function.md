# CREATE AI FUNCTION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

CREATE AI FUNCTION lets you turn custom AI logic into a reusable, governed Snowflake function that can be used
across applications, workflows, and SQL queries. Use CREATE AI FUNCTION when you want to package AI-powered
logic behind a stable SQL interface and manage it consistently with the rest of your Snowflake environment.

You define the function using Snowflake Cortex AI functions such as [AI\_COMPLETE](/sql-reference/functions/ai_complete),
[AI\_CLASSIFY](/sql-reference/functions/ai_classify), or [AI\_FILTER](/sql-reference/functions/ai_filter), then
invoke it like any other scalar function. Because it is a first-class Snowflake object, you can manage it using
familiar Snowflake capabilities for access control, object lifecycle, discovery, and governance.

AI functions can also participate in Snowflake’s evaluation and optimization workflows. This makes it possible
to measure quality and cost, improve prompts or model choices, and promote an optimized implementation into a
production-ready function without changing how downstream users call it.

## Syntax

Create an AI function from a SQL expression:

Copy code

```
CREATE [ OR REPLACE ] AI FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ , ... ] ] )
  RETURNS <result_data_type>
  [ COMMENT = '<string_literal>' ]
  AS $$
    <sql_expression_calling_an_ai_function>
  $$
```

Create an AI function from the winning candidate of an optimization experiment:

Copy code

```
CREATE [ OR REPLACE ] AI FUNCTION [ IF NOT EXISTS ] <name> (
    [ <arg_name> <arg_data_type> [ , ... ] ] )
  RETURNS <result_data_type>
  FROM EXPERIMENT <experiment_name> RUN <run_name>
```

## Arguments

### Required

`name`
:   The identifier for the AI function. Can be fully qualified (`db.schema.name`). The argument data types are part
    of the function’s signature, so `MY_FN(VARCHAR)` and `MY_FN(VARCHAR, VARCHAR)` are distinct functions (standard
    UDF overloading rules).

`( arg_name arg_data_type [ , ... ] )`
:   Zero or more input arguments, each an identifier plus a SQL data type (VARCHAR, FLOAT, BOOLEAN, OBJECT, FILE,
    and so on). The argument list may be empty: `MY_FN()`.

`RETURNS result_data_type`
:   The scalar SQL type the function returns (for example VARCHAR, FLOAT, BOOLEAN, OBJECT). A `TABLE(...)` return
    type is not supported — an AI function’s body is a single scalar expression.

Exactly one body clause:

`AS $$ sql_expression $$`
:   A single scalar SQL expression that calls [AI\_COMPLETE](/sql-reference/functions/ai_complete) at least once. It
    may also call other AI functions (for example [AI\_CLASSIFY](/sql-reference/functions/ai_classify),
    [AI\_FILTER](/sql-reference/functions/ai_filter)) or a nested user-defined AI function, but at least one
    AI\_COMPLETE call is required. The expression can freely reference the function’s arguments and can post-process
    the AI call (for example concatenate a prompt, cast the result to the return type).

`FROM EXPERIMENT experiment_name RUN run_name`
:   Instead of an inline body, materialize the function from a specific run of an existing optimization experiment
    (typically the frontier / winning `ITER_<N>` run). Snowflake copies that run’s tuned implementation into the
    new function. The declared signature and return type must match the optimized function.

### Optional

`OR REPLACE`
:   Replace an existing function with the same name and signature. Cannot be combined with `IF NOT EXISTS`.

`IF NOT EXISTS`
:   Do nothing (no error) if a function with the same name and signature already exists.

`COMMENT = 'string_literal'`
:   An optional description stored with the function (the `WITH` keyword is optional: `WITH COMMENT = '...'` is
    equivalent).

## Returns

Creating the function returns a status row confirming creation. When **invoked**, the function returns a single
scalar value of `<result_data_type>` per input row, exactly like any scalar UDF:

Copy code

```
SELECT id, MY_DB.MY_SCHEMA.CLASSIFY_TICKET(body) AS category
  FROM support_tickets;
```

## Usage notes

- **Body must be a scalar SQL expression, not a procedural block.** Snowflake Scripting / multi-statement bodies
  are rejected. Write one expression; use `||`, `CASE`, casts, and nested function calls as needed.
- **Body must call scalar AI Functions such as `AI_COMPLETE`, `AI_CLASSIFY` at least once.** A body that never
  calls scalar AI Functions is rejected. Legacy non-prefixed Cortex functions (for example
  `SNOWFLAKE.CORTEX.SENTIMENT`) do **not** count — use the `AI_`-prefixed equivalents. `AI_AGG` is considered
  non-scalar and will be rejected.
- **Cast the AI result to your return type.** `AI_COMPLETE(...)` returns VARIANT; if your function
  `RETURNS VARCHAR`, cast explicitly (`AI_COMPLETE(...)::VARCHAR`) so the declared and actual types match.
- **The argument list is the tunable surface.** When you later optimize the function, Snowflake rewrites the
  body (prompt/model) while preserving this signature and return type. Design arguments to carry the inputs the
  model needs (the text to classify, the context, and so on).
- **AI functions are UDFs.** They appear in `SHOW USER FUNCTIONS`, are dropped with `DROP FUNCTION`, and follow
  standard UDF resolution and overloading.
- **Runtime billing.** Each invocation runs the underlying AI calls, which are metered as Cortex AI inference
  (tokens), separate from the compute that runs your query. See
  [AI\_COMPLETE](/sql-reference/functions/ai_complete) for the model-level cost model.

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FUNCTION | Schema | Same privilege as a regular UDF; there is no separate “CREATE AI FUNCTION” privilege. |
| Database role `SNOWFLAKE.CORTEX_USER` | — | Required to run the AI calls in the body at invocation time. |
| USAGE | Function’s database + schema | To call the function. |

Expand

Show lessSee more

## Examples

### Classify sentiment

Create an AI function that classifies a product review into one of four sentiment categories:

Copy code

```
CREATE OR REPLACE AI FUNCTION my_db.my_schema.analyze_sentiment(body VARCHAR)
  RETURNS VARCHAR
  AS $$
    AI_COMPLETE(
      'claude-sonnet-4-6',
      'You are a product-review sentiment classifier.

Analyze the product review provided below and classify its overall sentiment as exactly one of:
- positive
- negative
- mixed
- neutral

Classification rules:
- positive: The reviewer is predominantly satisfied, approving, or recommending the product.
- negative: The reviewer is predominantly dissatisfied, critical, or discouraging purchase.
- mixed: The review contains substantial positive and negative opinions without a clearly dominant sentiment.
- neutral: The review contains little or no discernible evaluative opinion.

PRODUCT REVIEW:
"""' || body
    )::VARCHAR
  $$;
```

Invoke the function like any other scalar UDF:

Copy code

```
SELECT id, my_db.my_schema.analyze_sentiment(body) AS sentiment
  FROM product_reviews
  LIMIT 10;
```

### Classify support tickets

Create an AI function that categorizes support tickets into a fixed label set:

Copy code

```
CREATE OR REPLACE AI FUNCTION my_db.my_schema.classify_ticket(body VARCHAR)
  RETURNS VARCHAR
  AS $$
    AI_COMPLETE(
      'claude-sonnet-4-5',
      'Classify this support ticket into exactly one of: '
      || 'BILLING, BUG, FEATURE_REQUEST, OTHER. '
      || 'Return only the label.' || CHR(10) || body
    )::VARCHAR
  $$;
```

Invoke the function:

Copy code

```
SELECT id, my_db.my_schema.classify_ticket(body) AS category
  FROM support_tickets
  LIMIT 10;
```

### Redact PII from free text

Create an AI function that replaces personally identifiable information (PII) in free text with placeholders:

Copy code

```
CREATE OR REPLACE AI FUNCTION my_db.my_schema.redact(text VARCHAR)
  RETURNS VARCHAR
  AS $$
    AI_COMPLETE(
      'claude-haiku-4-5',
      'Redact all PII in the text below. Replace each PII span with a '
      || 'bracketed placeholder like [NAME], [EMAIL], [PHONE]. '
      || 'Return the full text.' || CHR(10) || text
    )::VARCHAR
  $$;
```

### Materialize the winner of an optimization experiment

After running an AI\_FUNCTION\_OPTIMIZATION experiment (see
[Optimize an AI function](/sql-reference/functions/ai_function_optimization)), promote the best run to a new,
production-ready AI function:

Copy code

```
-- ITER_7 was the frontier (best) run reported by SHOW RUN METRICS.
CREATE OR REPLACE AI FUNCTION my_db.my_schema.redact_tuned(text VARCHAR)
  RETURNS VARCHAR
  FROM EXPERIMENT my_db.my_schema.redact_opt_exp RUN ITER_7;
```

## Limitations

- **Scalar SQL only.** Procedural (Snowflake Scripting) bodies and non-SQL languages (Python/Java/Scala
  handlers) are not supported for AI functions.
- **Model availability.** The models named in the body must be available and authorized in your account and
  region; otherwise calls fail at invocation time.

## Legal

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
