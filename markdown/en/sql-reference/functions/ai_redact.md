Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_REDACT

Personally identifiable information (PII) includes names, addresses, phone numbers, email addresses, tax identification
numbers, and other data that can be used (alone or with other information) to identify an individual. Most
organizations have regulatory and compliance requirements around handling PII data. AI\_REDACT is a fully-managed Cortex
AI Function that uses a large language model (LLM) to help you detect, locate, and redact PII from unstructured text
data.

AI\_REDACT can help you prepare text for call center coaching, sentiment analysis, insurance and medical analysis, and
machine learning (ML) model training, among other use cases.

Tip

Use [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) or
[AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe) to convert document or speech data into text before applying
AI\_REDACT.

AI\_REDACT has two modes of operation: `redact` (default) and `detect`.

- Use AI\_REDACT in `redact` mode to replace PII in the input text with placeholder values.
- Use AI\_REDACT in `detect` mode to identify PII locations, then programmatically choose which PII to redact.

Important

AI\_REDACT performs detection and redaction in a best-effort manner using AI models. Always review the output to ensure
compliance with your organization’s data privacy policies. If AI\_REDACT fails to detect or redact any PII in your data,
[contact Snowflake Support](/user-guide/contacting-support).

## Syntax

Copy code

```
AI_REDACT( <input> [, <categories> ] [, <return_error_details> ] [, <mode> ] )
```

## Arguments

**Required:**

`input`
:   A VARCHAR value that contains text data that may contain personally identifiable information (PII).

**Optional:**

`categories`
:   An ARRAY of string values that specify the types of PII to be redacted. If not specified, all supported PII
    categories are redacted. See [Detected PII categories](#label-ai-redact-pii-categories) for a list of supported categories.

    Passing an unsupported category results in an error.

`return_error_details`
:   A BOOLEAN flag that indicates whether to return error details in case of error. When set to TRUE, the function returns
    an OBJECT that contains the value and the error message, one of which is NULL depending on whether the function
    succeeded or failed.

    Requires the session parameter AI\_SQL\_ERROR\_HANDLING\_USE\_FAIL\_ON\_ERROR to be set to FALSE.

`mode`
:   A VARCHAR value that specifies the operating mode. Accepted values:

    - `redact` (default): Replaces detected PII with category placeholders, such as [NAME] and [ADDRESS].
    - `detect`: Returns an OBJECT that contains a `spans` array that identifies the location and category of each detected PII instance
      without redacting the text.

Note

The `mode` argument is case insensitive.

## Returns

The return value of AI\_REDACT depends on the `mode` argument.

### Redact mode (default)

Returns a VARCHAR that contains the input text with PII replaced by category placeholders, such as `[NAME]` where the input
text was “John Smith”.

### Detect mode

Returns an OBJECT that contains a `spans` array. Each element in the array is an OBJECT with the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `category` | VARCHAR | The PII category, such as `NAME` or `ADDRESS`. See [Detected PII categories](#label-ai-redact-pii-categories) for supported categories. |
| `start` | NUMBER | The start index of the detected PII in the input text. |
| `end` | NUMBER | The end index of the detected PII in the input text. |
| `text` | VARCHAR | The matched PII text from the input. |

Expand

Show lessSee more

## Error behavior

By default, if AI\_REDACT cannot process the input, the function returns an error. If the query processes multiple rows,
the entire query fails.

When AI\_SQL\_ERROR\_HANDLING\_USE\_FAIL\_ON\_ERROR is set to FALSE, the return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value` and `error` fields | `value`: A VARCHAR value that contains the redacted text, or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. |
>
> Expand
>
> Show lessSee more

### Handle row-level errors in multi-row queries

Important

If your query fails on every row, the cause might be a known constraint rather than a row-level error.
See [Limitations](#label-ai-redact-pii-limitations) for details on token limits, language support, and other restrictions.

AI\_REDACT raises an error if it cannot process the input text. When a query redacts multiple rows, an error causes the
entire query to fail. To allow processing to continue with other rows, set the session parameter
`AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR` to FALSE. Errors then return NULL instead of stopping the query.

Copy code

```
ALTER SESSION SET AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR=FALSE;
```

With this parameter set to FALSE, you can also pass TRUE as the `return_error_details` argument to AI\_REDACT, which
causes the return value to be an OBJECT that contains separate fields for the redacted text and any error message. One
of these fields is NULL depending on whether the AI\_REDACT call processed successfully.

The following example shows how to use error handling when processing multiple rows:

1. Create a table with unredacted text.

   Copy code

   ```
   CREATE OR REPLACE TABLE raw_table AS
     SELECT 'My previous manager, Washington, used to live in Kirkland. His first name was Mike.' AS my_column
     UNION ALL
     SELECT 'My name is William and I live in San Francisco. You can reach me at (415).450.0973';
   ```
2. Set the session parameter.

   Copy code

   ```
   ALTER SESSION SET AI_SQL_ERROR_HANDLING_USE_FAIL_ON_ERROR=FALSE;
   ```
3. Create a redaction table with columns for `value` and `error`.

   Copy code

   ```
   CREATE OR REPLACE TABLE redaction_table (
     value VARCHAR,
     error VARCHAR
     );
   ```
4. Redact PII from `raw_table` and insert the rows into `redaction_table` to store the redacted text and error messages.

   Copy code

   ```
   INSERT INTO redaction_table
   SELECT
    result:value::STRING AS value,
    result:error::STRING AS error
     FROM (SELECT AI_REDACT(my_column, TRUE) AS result FROM raw_table);
   ```

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this role.

## Detected PII categories

AI\_REDACT supports the detection and redaction of the following categories of PII. The values in the Category column are the strings
that are supported in the optional `categories` argument.

> | Category | Notes |
> | --- | --- |
> | NAME | Recognizes full name, first name, middle name, and last name |
> | EMAIL |  |
> | PHONE\_NUMBER |  |
> | DATE\_OF\_BIRTH |  |
> | GENDER | Recognizes male, female, and nonbinary |
> | AGE |  |
> | ADDRESS | Identifies:   - complete postal address (US, UK, CA) - street address (US, UK, CA) - postal code (US, UK, CA) - city (US, UK, CA) - state (US) or province (CA) - county, borough, or township (US) |
> | NATIONAL\_ID | Identifies Social Security numbers (US) |
> | PASSPORT | Identifies passport numbers (US, UK, CA) |
> | TAX\_IDENTIFIER | Identifies Individual Taxpayer Numbers (ITNs) |
> | PAYMENT\_CARD\_DATA | Identifies complete card information, card number, expiration date, and CVV |
> | DRIVERS\_LICENSE | Identifies US, UK, and CA licenses |
> | IP\_ADDRESS |  |
>
> Expand
>
> Show lessSee more

Note

AI\_REDACT supports partial matches for some PII categories. For example, a first name alone is sufficient to trigger
redaction with the [NAME] placeholder.

## Retain specific PII with detect mode

By default, AI\_REDACT replaces all detected PII with placeholder values. In some cases, you might want to retain certain
PII while redacting the rest. For example, you might want to redact all names in call center transcripts or customer
reviews except for known employee names.

Use `detect` mode to build a selective redaction workflow:

1. Call AI\_REDACT with the `mode` argument set to `detect` to identify and locate PII in the input text.
2. Compare the detected spans against an allowlist of values you want to keep.
3. Redact only the PII that is not in the allowlist.

For examples of using `detect` mode, see [Detection and selective redaction examples](#label-ai-detect-pii-examples).

## Regional availability

See [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

## Limitations

- AI\_REDACT uses AI models and may not find all personally identifiable information. Always review the output
  to ensure compliance with your organization’s data privacy policies. If AI\_REDACT fails to redact certain PII, contact
  [Snowflake Support](/user-guide/contacting-support).
- AI\_REDACT works best with well-formed English text. Performance may vary with other languages or text with many
  spelling, punctuation, or grammatical errors.
- AI\_REDACT currently supports only US PII and some UK and Canadian PII, where noted in
  [Detected PII categories](#label-ai-redact-pii-categories).
- AI\_REDACT is currently limited in the number of tokens it can input and output. Input and output together can be up to
  4,096 tokens. Output is limited to 1,024 tokens. If the input text is longer, split it into smaller chunks and
  redact each chunk separately, perhaps using
  [SPLIT\_TEXT\_RECURSIVE\_CHARACTER](/sql-reference/functions/split_text_recursive_character-snowflake-cortex).
  See [Chunking example](#label-ai-redact-pii-example-chunking) for an example of redacting text that exceeds token limits.

  Note

  A token is the smallest unit of data processed by the AI model. For English text, industry guidelines consider one
  token to be approximately four characters, or 0.75 words.

## Cost considerations

AI\_REDACT incurs costs based on the number of input and output tokens processed, as with other Cortex AI Functions.
See the [Snowflake Pricing Guide](https://www.snowflake.com/pricing/pricing-guide/) for details.

### Estimate token usage for large datasets

Before you run AI\_REDACT on a large dataset, estimate input tokens on representative rows so you can plan for cost and
token limits. Sample text from your table and call [AI\_COUNT\_TOKENS](/sql-reference/functions/ai_count_tokens) with
`'ai_redact'` as the function name, using the same input text and optional `categories` argument you plan to pass to
AI\_REDACT. Compare the result against [AI\_REDACT token limits](#label-ai-redact-pii-limitations). If a row exceeds the
limit, split the text into chunks before redacting. See [Chunking example](#label-ai-redact-pii-example-chunking).

AI\_COUNT\_TOKENS returns an estimate of input tokens only. Output token counts depend on the redacted text and aren’t
included in the estimate.

For examples, see
[AI\_COUNT\_TOKENS examples for AI\_REDACT](/sql-reference/functions/ai_count_tokens#label-ai-count-tokens-ai-redact-examples).

## Redaction examples

- [Basic redaction examples](#basic-redaction-examples)
- [End-to-end example](#end-to-end-example)
- [Chunking example](#chunking-example)

### Basic redaction examples

The following example redacts a name and an address from the input text.

Copy code

```
SELECT AI_REDACT(
  input => 'My name is John Smith and I live at twenty third street, San Francisco.'
  );
```

Basic redaction output:

```
My name is [NAME] and I live at [ADDRESS]
```

The following example redacts only names and email addresses from the input text. Note that the text only contains a
first name, which is recognized and redacted as [NAME]. The input text does not contain an email address, so no email
placeholder appears in the output.

Copy code

```
SELECT AI_REDACT(
  input => 'My name is John and I live at twenty third street, San Francisco.',
  categories => ['NAME', 'EMAIL']
  );
```

Selective redaction output:

```
My name is [NAME] and I live at twenty third street, San Francisco.
```

### End-to-end example

The following example processes rows from one table and inserts the redacted output into another table. You could use a
similar approach to store the redacted data in a column in an existing table. After redaction, the text is passed to
the [AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) function to extract overall sentiment information.

1. Create a table with unredacted text.

   Copy code

   ```
   CREATE OR REPLACE TABLE raw_table AS
     SELECT 'My previous manager, Washington, used to live in Kirkland. His first name was Mike.' AS my_column
     UNION ALL
     SELECT 'My name is William and I live in San Francisco. You can reach me at (415).450.0973';
   ```
2. View unredacted data.

   Copy code

   ```
   SELECT * FROM raw_table;
   ```
3. Create a redaction table.

   Copy code

   ```
   CREATE OR REPLACE TABLE redaction_table (value VARCHAR);
   ```
4. Redact PII from `raw_table` and insert the rows into `redaction_table`.

   Copy code

   ```
   INSERT INTO redaction_table
     SELECT AI_REDACT(my_column) AS value FROM raw_table;
   ```
5. View redacted results.

   Copy code

   ```
   SELECT * FROM redaction_table;
   ```
6. Run the AI\_SENTIMENT function on redacted text.

   Copy code

   ```
   SELECT
    value AS redacted_text,
    AI_SENTIMENT(value) AS summary_sentiment
     FROM redaction_table;
   ```

### Chunking example

This example illustrates how to redact PII from long text by splitting the text into smaller chunks, redacting each
chunk separately, and then recombining the redacted chunks into the final output. This approach works around
AI\_REDACT’s token limits.

1. Create a table with patient data.

   Copy code

   ```
   CREATE OR REPLACE TABLE patients (
     patient_id INT PRIMARY KEY,
     patient_notes TEXT
     );
   ```
2. Split the text into chunks, apply AI\_REDACT to each chunk, and concatenate the redacted chunks.

   Copy code

   ```
   CREATE OR REPLACE TABLE final_temp_table AS
     WITH chunked_data AS (
    SELECT
        patient_id,
        chunk.value AS chunk_text,
        chunk.index AS chunk_index
      FROM
        patients,
        LATERAL FLATTEN(
            input => SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
                patient_notes,
                'none',
                1000
                )
            ) AS chunk
      WHERE
        patient_notes IS NOT NULL
        AND LENGTH(patient_notes) > 0
    ),
     redacted_chunks AS (
      SELECT
          patient_id,
          chunk_index,
          chunk_text,
          TO_VARIANT(results:value) AS redacted_chunk,
          TO_VARIANT(results:error) AS error_string
        FROM (
          SELECT
              patient_id,
              chunk_index,
              chunk_text,
              AI_REDACT(chunk_text,TRUE) AS results
            FROM
              chunked_data
        )
     ),
     final AS (
      SELECT
          chunk_text AS original,
          IFF(error_string IS NOT NULL, chunk_text, redacted_chunk) AS redacted_text,
          patient_id,
          chunk_index
        FROM
          redacted_chunks
     )
     SELECT * FROM final;
   ```
3. Query the results.

   Copy code

   ```
   SELECT
    patient_id,
    LISTAGG(redacted_text, '') WITHIN GROUP (ORDER BY chunk_index) AS full_output
     FROM final_temp_table
     GROUP BY patient_id;
   ```

## Detection and selective redaction examples

- [Basic detection example](#basic-detection-example)
- [End-to-end with allowlist example](#end-to-end-with-allowlist-example)

### Basic detection example

The following example identifies and returns the category, location, and text of each detected PII instance without
redacting the input.

Copy code

```
SELECT AI_REDACT(
    input => 'My old manager, Washington, used to live in Washington. His first name was Mike.',
    return_error_details => FALSE,
    mode => 'detect'
    );
```

Basic detection output:

```
{
  "spans": [
    {
      "category": "NAME",
      "end": 26,
      "start": 16,
      "text": "Washington"
    },
    {
      "category": "ADDRESS",
      "end": 54,
      "start": 44,
      "text": "Washington"
    },
    {
      "category": "NAME",
      "end": 79,
      "start": 75,
      "text": "Mike"
    }
  ]
}
```

### End-to-end with allowlist example

The following example demonstrates a selective redaction workflow that uses `detect` mode and an allowlist. It loads a
list of names to retain from a staged file, uses AI\_REDACT in `detect` mode to identify PII locations, and then passes
the results to a Python UDF that redacts only the PII not in the allowlist.

1. Retain an allowlist of values by loading the list from a stage into a temporary table.

   Copy code

   ```
   CREATE OR REPLACE TEMP TABLE string_list (value STRING);

   COPY INTO string_list
     FROM @mystage/allowlist.txt
     FILE_FORMAT = (
    TYPE = 'CSV'
    RECORD_DELIMITER = '\n'
    FIELD_DELIMITER = '\t'   -- any char NOT in file
    TRIM_SPACE = TRUE
    SKIP_HEADER = 0
    );
   ```
2. View the allowlist table

   Copy code

   ```
   SELECT * FROM string_list;
   ```

   Allowlist table output:

   ```
   VALUE
   Mike
   David
   ```
3. Create a Python UDF that selectively redacts PII based on the allowlist.

   Copy code

   ```
   CREATE OR REPLACE FUNCTION redact_spans_with_allowlist(
     SPAN_DATA VARIANT,
     ALLOWLIST ARRAY,
     ORIGINAL_TEXT STRING
     )
     RETURNS STRING
     LANGUAGE PYTHON
     RUNTIME_VERSION = '3.8'
     HANDLER = 'redact_text'
     AS
     $$
     def redact_text(span_data, allowlist, original_text):
      spans = span_data.get('spans', [])
      # Sort descending to maintain index integrity
      sorted_spans = sorted(spans, key=lambda x: x['start'], reverse=True)

      result = original_text

      for span in sorted_spans:
          text_val = span.get('text')
          if text_val in allowlist:
              continue

          start, end = span['start'], span['end']
          label = f"[{span['category']}]"

          # Splice the string
          result = result[:start] + label + result[end:]

      return result
     $$;
   ```
4. Test the UDF.

   Copy code

   ```
   SELECT redact_spans_with_allowlist(
     PARSE_JSON('{"spans": [{"category": "NAME", "end": 26, "start": 16, "text": "Washington"}, {"category": "NAME", "end": 79, "start": 75, "text": "Mike"}]}'),
     ARRAY_CONSTRUCT('Washington'), -- This will NOT be redacted
     'Hello, my name is Washington and his is Mike.'
     );
   ```
5. Run AI\_REDACT in `detect` mode.

   Copy code

   ```
   CREATE OR REPLACE TABLE raw (message TEXT);

   INSERT INTO raw (message) VALUES
     ('My old manager, Washington, used to live in Washington. His first name was Mike.');

   SELECT
    t.message AS message,
    AI_REDACT(input=>t.message, return_error_details=>FALSE, mode=>'detect') AS spans,
    redact_spans_with_allowlist(spans, l.str_list, message) AS result
     FROM raw t
    CROSS JOIN (
      SELECT ARRAY_AGG(value) AS str_list
        FROM string_list
      ) l;
   ```

End-to-end with allowlist example output:

| MESSAGE | SPANS | RESULT |
| --- | --- | --- |
| My old manager, Washington, used to live in Washington. His first name was Mike. | Copy code  ``` {   "spans": [     {"category": "NAME",     "end": 26,     "start": 16,     "text": "Washington"     },     {"category": "ADDRESS",     "end": 54,     "start": 44,     "text": "Washington"     },     {"category": "NAME",     "end": 79,     "start": 75,     "text": "Mike"     }   ] } ``` | My old manager, [NAME], used to live in [ADDRESS]. His first name was Mike. |

Expand

Show lessSee more

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
