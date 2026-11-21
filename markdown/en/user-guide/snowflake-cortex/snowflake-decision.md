# Cortex AI Functions: Snowflake Decision

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Snowflake Decision evaluates content against a set of questions and returns structured answers through
[AI\_COMPLETE](/sql-reference/functions/ai_complete). It supports classification, scoring against an ordered rubric, and
true-or-false assessment, with probabilities that your SQL or application logic can use for routing, review, and
downstream processing.

You provide a state, the text or structured data to evaluate, and a set of typed questions. The model answers each
question using that state and returns the results in a single object. To use the model, specify
`model => 'snowflake-decision'`.

## Key benefits

- **Typed answers:** Return a selected option, a rubric score, or the probability that a statement is true rather than
  free-form text.
- **Multiple assessments per request:** Classify, score, and assess the same content in one call, using separate
  criteria for each question.
- **Confidence-based routing:** Use probabilities and confidence values to send results to automated actions, human
  review, or a fallback.
- **Table-level processing:** Evaluate content across a table or query result in one SQL statement instead of issuing a
  separate query for each row.

## Prerequisites

Your account must have
[CORTEX\_ENABLED\_CROSS\_REGION](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference) set
to `'AWS_US'`, `'AWS_GLOBAL'`, or `'ANY_REGION'`.

## When to use Snowflake Decision

Use Snowflake Decision when you need to select from a defined set of options, assess content against an ordered rubric,
or determine the probability that a statement is true. The model is optimized for throughput across table-based
workloads, so you can apply these assessments to a table or query result in a single SQL statement.

These assessments help determine what happens next in a workflow. Snowflake Decision returns structured answers rather
than free-form text; your SQL or application logic uses those answers to select and execute the next processing step.
For tasks that require extraction, complex reasoning, summaries, or written responses, combine Snowflake Decision with
other Cortex AI Functions or a general-purpose model through AI\_COMPLETE.

The following examples show how Snowflake Decision connects input preparation with downstream processing:

| Workflow | Prepare the input | Assess with Snowflake Decision | Use the result |
| --- | --- | --- | --- |
| Support operations | Use ticket text directly, or transcribe calls with AI\_TRANSCRIBE. | Determine topic and priority. | Application logic routes urgent cases; AI\_AGG summarizes recurring issues within topics. |
| Document processing | Make document content available with AI\_PARSE\_DOCUMENT. | Identify the document type. | Application logic selects an extraction schema for AI\_EXTRACT or sends uncertain classifications for review. |
| Customer feedback | Use AI\_TRANSLATE to bring multilingual feedback into a common language. | Assess whether feedback is actionable under the team’s criteria. | Selected records move to AI\_SENTIMENT and AI\_AGG for further analysis. |
| Risk and compliance review | Provide communications or transaction-related records. | Assess records against defined review criteria. | Application rules select cases; a general-purpose model through AI\_COMPLETE drafts supporting notes for human reviewers. |
| Tool or agent routing | Provide the request and descriptions of available options. | Select the appropriate tool or agent. | The application invokes the selected option and handles uncertain results through a fallback. |

Expand

Show lessSee more

## Examples

The following examples show how to use Snowflake Decision to classify documents, select tools, prioritize support
tickets, and identify actionable feedback. Each query provides the content to evaluate as `state` and defines one or more
typed questions. Snowflake Decision returns structured answers that your SQL or application logic can use to determine
the next processing step.

### Classify documents for downstream processing

Documents that arrive through the same pipeline can require different extraction schemas and validation steps. Use
Snowflake Decision to identify the document type before selecting how to process it. For example, your application can
use the classification to choose an extraction schema for [AI\_EXTRACT](/sql-reference/functions/ai_extract).

This example assumes that `parsed_documents` contains a `doc_id` column and a `doc_text` column with document text
previously obtained using [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document). The query classifies that
text as an invoice, contract, or receipt; it does not perform the document-parsing step.

Copy code

```
SELECT doc_id,
    AI_COMPLETE(model => 'snowflake-decision', prompt => TO_JSON({
      'state': doc_text,
      'questions': {'doc_type': {'type': 'choice', 'instructions': 'What kind of document is this?',
        'criteria': {'invoice': 'Bill with line items and totals',
                     'contract': 'Legal agreement with parties and terms',
                     'receipt': 'Proof of payment'}}}})) AS d
  FROM parsed_documents;
```

Response:

Copy code

```
{
  "answers": {
    "doc_type": {
      "choice": "invoice",
      "confidence": 0.9761490166192129,
      "probabilities": {
        "contract": 0.001281328317600061,
        "invoice": 0.996398485837644,
        "receipt": 0.002320185844756006
      },
      "type": "choice"
    }
  }
}
```

The response selects `invoice`, with a probability of approximately 0.996 and a confidence value of approximately 0.976.
The probability applies to the selected option; confidence reflects the distribution across all three options. These
values are not interchangeable.

Your application can use this classification to select the invoice-processing path, subject to its confidence
threshold. The query returns the document type, not extracted fields.

### Select a tool or agent

Use Snowflake Decision to assess which tool or specialized agent should handle an incoming request. The model returns a
selection; your application invokes the selected tool or chooses a fallback.

This example evaluates the `request` column in `demo_requests`. The available options cover quantitative questions over
tables, questions about policy documents, and scheduling requests. The `none` option provides an explicit outcome when
none of the listed tools is suitable.

Copy code

```
SELECT id, request,
    AI_COMPLETE(model => 'snowflake-decision', prompt => TO_JSON({
      'state': request,
      'questions': {'tool': {'type': 'choice', 'instructions': 'Which tool should handle this request?',
        'criteria': {'sql_analyst': 'Quantitative questions over tables',
                     'doc_search': 'Questions answered from policy documents',
                     'calendar_agent': 'Scheduling and meetings',
                     'none': 'Nothing listed can do this'}}}})) AS d
  FROM demo_requests;
```

Response:

Copy code

```
{
  "answers": {
    "tool": {
      "choice": "none",
      "confidence": 0.5824745505065628,
      "probabilities": {
        "calendar_agent": 0.003214915662746091,
        "doc_search": 0.011221158242299589,
        "none": 0.7866640896947483,
        "sql_analyst": 0.19889983640020595
      },
      "type": "choice"
    }
  }
}
```

The response selects `none`, with a probability of approximately 0.787 and confidence of approximately 0.582. In this
example, `none` is a defined answer, not a failed function call. Your application can use it to trigger a fallback rather
than invoke one of the listed tools.

When the model selects a named tool, application logic can also check confidence before invoking it. The SQL query
itself does not execute any tool or agent.

### Classify and prioritize support tickets

Assess multiple aspects of a support ticket in one request to inform routing and prioritization. This example evaluates
`ticket_text` in `demo_tickets` using two questions: a `choice` question identifies the primary topic, and a `score`
question assesses business urgency against the ordered levels `Can wait`, `Soon`, and `Immediate`.

Both questions use the same ticket text and are evaluated independently. The priority assessment does not depend on the
answer to the topic question.

Copy code

```
SELECT ticket_id, ticket_text,
    AI_COMPLETE(model => 'snowflake-decision', prompt => TO_JSON({
      'state': ticket_text,
      'questions': {
        'topic': {'type': 'choice', 'instructions': 'Primary topic',
                  'criteria': {'billing': 'Charges, invoices',
                               'technical': 'Bugs, outages, integrations',
                               'sales': 'Pricing, plans'}},
        'priority': {'type': 'score', 'instructions': 'Business urgency',
                     'criteria': ['Can wait', 'Soon', 'Immediate']}}})) AS d
  FROM demo_tickets;
```

Response:

Copy code

```
{
  "answers": {
    "priority": {
      "confidence": 0.40749829409697613,
      "legend": {
        "0": "Can wait",
        "1": "Soon",
        "2": "Immediate"
      },
      "probabilities": {
        "0": 0.07342543853746276,
        "1": 0.13717676236755755,
        "2": 0.7893977990949796
      },
      "score": 1.7159723605575168,
      "type": "score"
    },
    "topic": {
      "choice": "billing",
      "confidence": 0.8088073178724315,
      "probabilities": {
        "billing": 0.9556932212852267,
        "sales": 0.015447345260120083,
        "technical": 0.028859433454653204
      },
      "type": "choice"
    }
  }
}
```

The response classifies the ticket as `billing` and returns a priority score of approximately 1.716. The score is a
probability-weighted position on the rubric, where 0 means `Can wait`, 1 means `Soon`, and 2 means `Immediate`. It is not
a discrete priority label or a precise measurement of urgency.

The two assessments have separate confidence values: approximately 0.809 for `topic` and 0.407 for `priority`. Your
routing logic can evaluate each answer separately rather than assume that confidence in the topic also establishes
confidence in the urgency assessment.

Use the topic to select a support queue and the priority assessment to inform processing order or escalation, according
to your application’s rules.

### Identify actionable customer feedback

Use Snowflake Decision to distinguish feedback that describes a specific product problem or feature request from more
general reactions. In a multilingual workflow, translate the feedback into a common language before applying the
assessment. Selected records can then move to sentiment analysis or theme summarization.

This example translates the `feedback` column in `demo_feedback` into English with
[AI\_TRANSLATE](/sql-reference/functions/ai_translate). It then uses a `noul` question to assess whether the translated
feedback describes a specific, fixable product problem or feature request. A `noul` question returns a probability from
0 to 1 that the statement in `instructions` is true.

Copy code

```
SELECT id, feedback_en,
    AI_COMPLETE(model => 'snowflake-decision', prompt => TO_JSON({
      'state': feedback_en,
      'questions': {'actionable': {'type': 'noul',
        'instructions': 'Feedback describes a specific, fixable product problem or feature request'}}})) AS d
  FROM (SELECT id, AI_TRANSLATE(feedback, '', 'en') AS feedback_en FROM demo_feedback);
```

Response:

Copy code

```
{
  "answers": {
    "actionable": {
      "noul": 0.7549149813536518,
      "type": "noul"
    }
  }
}
```

The response returns approximately 0.755 as the probability that the feedback meets the stated criteria. This is not a
Boolean result. Your SQL or application logic must choose a threshold for treating the feedback as actionable. Use a
subsequent SQL expression or application rule to select records for further processing, such as sentiment analysis with
[AI\_SENTIMENT](/sql-reference/functions/ai_sentiment) or summarization across records with
[AI\_AGG](/sql-reference/functions/ai_agg).

## Question types

Each question defines the kind of judgment to make and, where required, the criteria to use.

| Type | Purpose | Criteria | Returned answer |
| --- | --- | --- | --- |
| `choice` | Select one option from a fixed set. | Required. An object mapping each option key to its description. | The selected key, a probability for each option, and confidence. |
| `score` | Evaluate content against an ordered rubric. | Required. An array of level descriptions, ordered from lowest to highest. | The probability-weighted level from 0 to n - 1, a probability for each level, a legend, and confidence. |
| `noul` | Assess whether a statement is true. | Optional. An object with a `"true"` key, a `"false"` key, or both, and their descriptions. | The probability that the statement is true. |

Expand

Show lessSee more

## Interpreting the answers

- **Choice:** `choice` contains the most likely option. In the support ticket example, the selected topic is `billing`.
  The `probabilities` object contains a value for every option, and those values sum to 1.
- **Score:** `score` is the probability-weighted level, not necessarily an integer. Levels are numbered from 0 in the
  order supplied in `criteria`. In the support ticket example, the score is
  0 × 0.073 + 1 × 0.137 + 2 × 0.789 ≈ 1.716. The `legend` maps each level number to its description.
- **True-or-false assessment:** `noul` is the probability that the statement is true. In the customer feedback example,
  the value 0.755 is a probability, not a Boolean result. Your application chooses the threshold for treating the
  statement as true.

### Confidence

For `choice` and `score`, confidence is calculated as:

```
confidence = 1 - H / ln(n)
H = -Σ p_i × ln(p_i)
```

Here, `n` is the number of options or levels, `p_i` is the returned probability of each option or level, and `H` is the
entropy of the returned distribution. Confidence is 0 when every option is equally likely and approaches 1 as one option
dominates.

Confidence reflects the whole distribution, not only the highest probability. In the support ticket example, the
probability of `billing` is approximately 0.956, while the calculated confidence is approximately 0.809.

Returned numeric values are full-precision floats and are not rounded.

## Model limits

| Limit or parameter | Behavior |
| --- | --- |
| Prompt size | Maximum of 256 KiB for the entire JSON request. |
| Questions per request | Maximum of 64. |
| Options per choice question | 2–255. |
| Levels per score question | 2–255. |
| Question ID | 1–64 characters matching `[A-Za-z0-9_-]`. |
| Streaming and guardrails | Not supported. Requests using these features are rejected. |
| `temperature` and `top_p` | Ignored. |

Expand

Show lessSee more
